#!/usr/bin/env python3

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

MEMORY_TIERS = {
    "episodic": r"(?:episodic|conversation|session|short[- ]?term)\s*(?:memory|context|store)",
    "semantic": r"(?:semantic|knowledge|long[- ]?term|persistent)\s*(?:memory|context|store|base)",
    "procedural": r"(?:procedural|workflow|skill|action)\s*(?:memory|context|store)",
}

BUDGET_INDICATORS = [
    r"(?:token|context)\s*(?:budget|limit|cap|window|allocation)",
    r"(?:max[_\s]?tokens|context[_\s]?length|context[_\s]?size)",
    r"\b\d+k?\s*tokens?\b",
]

ANTI_PATTERNS = [
    ("C001", "WARNING", r"(?:dump|include|inject)\s+(?:all|everything|entire)", "Unbounded context injection — use budgeting"),
    ("C002", "WARNING", r"(?:never|no)\s+(?:evict|remove|expire|forget)", "No eviction policy — memory will grow unbounded"),
    ("C003", "INFO", r"(?:always|every)\s+(?:include|prepend|attach)", "Always-include directive — verify necessity per call"),
    ("C004", "WARNING", r"(?:raw|unprocessed|verbatim)\s+(?:history|log|transcript)", "Raw history inclusion — summarize or compress"),
    ("C005", "INFO", r"(?:TODO|FIXME|placeholder)\s+(?:memory|context|retrieval)", "Incomplete context implementation"),
]


@dataclass
class ValidationResult:
    code: str
    severity: str
    line: int | None
    message: str


@dataclass
class ContextReport:
    file_path: Path
    tiers_found: list[str] = field(default_factory=list)
    tiers_missing: list[str] = field(default_factory=list)
    has_budget: bool = False
    has_eviction: bool = False
    has_retrieval_strategy: bool = False
    estimated_static_tokens: int = 0
    issues: list[ValidationResult] = field(default_factory=list)

    @property
    def score(self) -> int:
        base = 10
        base -= len(self.tiers_missing)
        if not self.has_budget:
            base -= 2
        if not self.has_eviction:
            base -= 1
        base -= sum(1 for i in self.issues if i.severity == "WARNING")
        return max(0, min(10, base))


def estimate_tokens(content: str) -> int:
    return len(content) // 4


def validate_file(file_path: Path) -> ContextReport:
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    report = ContextReport(file_path=file_path)
    report.estimated_static_tokens = estimate_tokens(content)

    for tier_name, pattern in MEMORY_TIERS.items():
        if re.search(pattern, content, re.IGNORECASE):
            report.tiers_found.append(tier_name)
        else:
            report.tiers_missing.append(tier_name)

    report.has_budget = any(
        re.search(p, content, re.IGNORECASE) for p in BUDGET_INDICATORS
    )

    report.has_eviction = bool(re.search(
        r"(?:evict|eviction|expire|ttl|lru|fifo|priority[- ]?queue|drop[- ]?oldest)",
        content, re.IGNORECASE,
    ))

    report.has_retrieval_strategy = bool(re.search(
        r"(?:retriev|fetch|load|query|search|embed|vector|similarity|rag)\s",
        content, re.IGNORECASE,
    ))

    if not report.has_budget:
        report.issues.append(ValidationResult(
            code="C010",
            severity="WARNING",
            line=None,
            message="No token budget or context limit defined",
        ))

    if not report.has_eviction and report.tiers_found:
        report.issues.append(ValidationResult(
            code="C011",
            severity="WARNING",
            line=None,
            message="Memory tiers defined but no eviction policy found",
        ))

    for line_num, line in enumerate(lines, start=1):
        for code, severity, pattern, message in ANTI_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                report.issues.append(ValidationResult(
                    code=code,
                    severity=severity,
                    line=line_num,
                    message=message,
                ))

    return report


def format_report(report: ContextReport) -> str:
    lines: list[str] = [f"\n🧠 Context Architecture Validation: {report.file_path}"]
    lines.append(f"   Memory tiers: {', '.join(report.tiers_found) or 'None detected'}")
    if report.tiers_missing:
        lines.append(f"   Missing tiers: {', '.join(report.tiers_missing)}")
    lines.append(f"   Token budget: {'✅ Defined' if report.has_budget else '❌ Missing'}")
    lines.append(f"   Eviction policy: {'✅ Found' if report.has_eviction else '❌ Missing'}")
    lines.append(f"   Static tokens: ~{report.estimated_static_tokens:,}")
    lines.append(f"   Score: {report.score}/10")

    if report.issues:
        lines.append("\n   Issues:")
        for issue in sorted(report.issues, key=lambda i: (
            {"ERROR": 0, "WARNING": 1, "INFO": 2}[i.severity], i.line or 0,
        )):
            loc = f":{issue.line}" if issue.line else ""
            icon = {"ERROR": "❌", "WARNING": "⚠️ ", "INFO": "ℹ️ "}[issue.severity]
            lines.append(f"   {icon} {issue.code}{loc}: {issue.message}")
    else:
        lines.append("\n   ✅ No issues found")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate context engineering architecture — memory tiers, budgeting, eviction",
    )
    parser.add_argument("files", type=Path, nargs="+", help="Context config file(s)")
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
