#!/usr/bin/env python3

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

MODEL_PRICING = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4": {"input": 30.00, "output": 60.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-haiku": {"input": 0.25, "output": 1.25},
    "claude-3-opus": {"input": 15.00, "output": 75.00},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    "deepseek-v3": {"input": 0.27, "output": 1.10},
    "deepseek-r1": {"input": 0.55, "output": 2.19},
}

TIER_THRESHOLDS = {
    "lightweight": 1.00,
    "standard": 5.00,
    "premium": 15.00,
}

ANTI_PATTERNS = [
    ("F001", "WARNING", r"(?:gpt-4|claude-3-opus|claude-3.5-sonnet).*(?:every|all|each)\s+(?:request|call|message)", "Premium model used for all requests — use model tiering"),
    ("F002", "WARNING", r"(?:no|without|skip)\s+(?:cache|caching)", "Caching explicitly disabled — reconsider for repeated queries"),
    ("F003", "INFO", r"(?:retry|retries)\s*[:=]\s*(?:[5-9]|\d{2,})", "High retry count — consider circuit breaker pattern"),
    ("F004", "WARNING", r"(?:include|send)\s+(?:full|entire|complete)\s+(?:history|context|conversation)", "Full history inclusion inflates input tokens — summarize or compress"),
    ("F005", "INFO", r"(?:streaming|stream)\s*[:=]\s*(?:false|off|disabled)", "Streaming disabled — enable for better UX with lower perceived latency"),
]


@dataclass
class ValidationResult:
    code: str
    severity: str
    line: int | None
    message: str


@dataclass
class CostEstimate:
    model: str
    input_tokens: int
    output_tokens: int
    cost_per_call: float
    monthly_cost_1k: float
    monthly_cost_10k: float

    @property
    def tier(self) -> str:
        price_per_m = MODEL_PRICING.get(self.model, {}).get("input", 0)
        if price_per_m <= TIER_THRESHOLDS["lightweight"]:
            return "lightweight"
        if price_per_m <= TIER_THRESHOLDS["standard"]:
            return "standard"
        return "premium"


@dataclass
class FinOpsReport:
    file_path: Path
    models_detected: list[str] = field(default_factory=list)
    estimates: list[CostEstimate] = field(default_factory=list)
    has_tiering: bool = False
    has_caching: bool = False
    has_budgets: bool = False
    issues: list[ValidationResult] = field(default_factory=list)

    @property
    def score(self) -> int:
        base = 10
        if not self.has_tiering:
            base -= 2
        if not self.has_caching:
            base -= 1
        if not self.has_budgets:
            base -= 1
        base -= sum(1 for i in self.issues if i.severity == "WARNING")
        return max(0, min(10, base))


def estimate_tokens(content: str) -> int:
    return len(content) // 4


def detect_models(content: str) -> list[str]:
    found = []
    for model in MODEL_PRICING:
        if re.search(re.escape(model), content, re.IGNORECASE):
            found.append(model)
    return found


def validate_file(file_path: Path) -> FinOpsReport:
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    report = FinOpsReport(file_path=file_path)

    report.models_detected = detect_models(content)
    input_tokens = estimate_tokens(content)
    output_estimate = input_tokens // 2

    for model in report.models_detected or ["gpt-4o-mini", "gpt-4o"]:
        pricing = MODEL_PRICING.get(model, {"input": 1.0, "output": 3.0})
        cost_per_call = (
            (input_tokens / 1_000_000) * pricing["input"]
            + (output_estimate / 1_000_000) * pricing["output"]
        )
        estimate = CostEstimate(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_estimate,
            cost_per_call=cost_per_call,
            monthly_cost_1k=cost_per_call * 1_000,
            monthly_cost_10k=cost_per_call * 10_000,
        )
        report.estimates.append(estimate)

    report.has_tiering = bool(re.search(
        r"(?:tier|routing|fallback|cascade)\s*(?:model|strategy|level)",
        content, re.IGNORECASE,
    ))

    report.has_caching = bool(re.search(
        r"(?:cache|memo|deduplic|reuse)",
        content, re.IGNORECASE,
    ))

    report.has_budgets = bool(re.search(
        r"(?:budget|limit|cap|threshold|alert)\s*(?:cost|spend|token|dollar|\$)",
        content, re.IGNORECASE,
    ))

    for line_num, line in enumerate(lines, start=1):
        for code, severity, pattern, message in ANTI_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                report.issues.append(ValidationResult(
                    code=code, severity=severity, line=line_num, message=message,
                ))

    if not report.has_tiering:
        report.issues.append(ValidationResult(
            code="F010", severity="WARNING", line=None,
            message="No model tiering strategy detected — use lightweight models for simple tasks",
        ))

    return report


def format_report(report: FinOpsReport) -> str:
    out: list[str] = [f"\n💰 Agent FinOps Cost Estimation: {report.file_path}"]
    out.append(f"   Models detected: {', '.join(report.models_detected) or 'None (using defaults)'}")
    out.append(f"   Model tiering: {'✅' if report.has_tiering else '❌ Missing'}")
    out.append(f"   Caching: {'✅' if report.has_caching else '❌ Missing'}")
    out.append(f"   Cost budgets: {'✅' if report.has_budgets else '❌ Missing'}")
    out.append(f"   Score: {report.score}/10")

    if report.estimates:
        out.append("\n   Cost Estimates (prompt as system message):")
        out.append(f"   {'Model':<22} {'Tier':<13} {'Per Call':>10} {'1K/mo':>10} {'10K/mo':>10}")
        out.append(f"   {'─' * 22} {'─' * 13} {'─' * 10} {'─' * 10} {'─' * 10}")
        for est in sorted(report.estimates, key=lambda e: e.cost_per_call):
            out.append(
                f"   {est.model:<22} {est.tier:<13} "
                f"${est.cost_per_call:>8.4f} "
                f"${est.monthly_cost_1k:>8.2f} "
                f"${est.monthly_cost_10k:>8.2f}"
            )

    if report.issues:
        out.append("\n   Issues:")
        for issue in sorted(report.issues, key=lambda i: (
            {"ERROR": 0, "WARNING": 1, "INFO": 2}[i.severity], i.line or 0,
        )):
            loc = f":{issue.line}" if issue.line else ""
            icon = {"ERROR": "❌", "WARNING": "⚠️ ", "INFO": "ℹ️ "}[issue.severity]
            out.append(f"   {icon} {issue.code}{loc}: {issue.message}")

    return "\n".join(out)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estimate agent operational costs — model pricing, tiering, optimization",
    )
    parser.add_argument("files", type=Path, nargs="+", help="Agent config/prompt file(s)")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any warnings")

    args = parser.parse_args()
    exit_code = 0

    for file_path in args.files:
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            exit_code = 1
            continue

        report = validate_file(file_path)
        print(format_report(report))

        if args.strict and any(i.severity in ("ERROR", "WARNING") for i in report.issues):
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
