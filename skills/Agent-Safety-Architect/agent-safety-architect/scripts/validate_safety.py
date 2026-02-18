#!/usr/bin/env python3

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

AUTONOMY_TIERS = {
    "full-auto": r"(?:full[- ]?auto|autonomous|auto[- ]?approve|no[- ]?confirmation)",
    "supervised": r"(?:supervised|approval|confirm|review[- ]?before|ask[- ]?user)",
    "human-led": r"(?:human[- ]?led|manual|user[- ]?only|require[- ]?explicit[- ]?approval)",
}

SAFETY_CHECKS = {
    "secret_handling": r"(?:secret|credential|api[_\s]?key|password|token)\s*(?:handling|policy|rule|protection|redact)",
    "permission_zones": r"(?:permission|zone|sandbox|container|allow[- ]?list|deny[- ]?list|workspace)",
    "audit_logging": r"(?:audit|log|trail|record|trace)\s*(?:action|operation|decision|change)",
    "escalation": r"(?:escalat|fallback|human[- ]?in[- ]?the[- ]?loop|override|abort)",
    "input_validation": r"(?:validat|sanitiz|whitelist|allowlist|reject|filter)\s*(?:input|command|path|url)",
}

CREDENTIAL_PATTERNS = [
    ("S001", "ERROR", r"(?:api[_.]?key|password|secret|token)\s*[:=]\s*['\"][A-Za-z0-9+/=_-]{8,}", "Possible hardcoded credential detected"),
    ("S002", "ERROR", r"(?:sk-|ghp_|gho_|AKIA|xox[bps]-)[A-Za-z0-9]{10,}", "High-confidence API key pattern detected"),
    ("S003", "WARNING", r"(?:curl|wget|fetch)\s+.*(?:password|token|secret)", "Credential in command example — use env var reference"),
]

ANTI_PATTERNS = [
    ("S004", "WARNING", r"(?:trust|allow)\s+(?:all|any|everything)", "Overly permissive trust — define explicit boundaries"),
    ("S005", "WARNING", r"(?:skip|bypass|disable)\s+(?:auth|validation|check|verify)", "Safety bypass instruction detected"),
    ("S006", "WARNING", r"(?:sudo|root|admin)\s+(?:by default|always)", "Elevated privileges by default — use least privilege"),
    ("S007", "INFO", r"(?:rm -rf|drop table|delete \*|format)", "Destructive command reference — ensure approval gate exists"),
    ("S008", "WARNING", r"(?:execute|run|eval)\s+(?:arbitrary|user[- ]?provided|untrusted)", "Arbitrary execution of untrusted input"),
]


@dataclass
class ValidationResult:
    code: str
    severity: str
    line: int | None
    message: str


@dataclass
class SafetyReport:
    file_path: Path
    tiers_found: list[str] = field(default_factory=list)
    tiers_missing: list[str] = field(default_factory=list)
    checks_found: list[str] = field(default_factory=list)
    checks_missing: list[str] = field(default_factory=list)
    issues: list[ValidationResult] = field(default_factory=list)

    @property
    def score(self) -> int:
        base = 10
        base -= len(self.checks_missing)
        base -= sum(2 for i in self.issues if i.severity == "ERROR")
        base -= sum(1 for i in self.issues if i.severity == "WARNING")
        return max(0, min(10, base))


def validate_file(file_path: Path) -> SafetyReport:
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    report = SafetyReport(file_path=file_path)

    for tier_name, pattern in AUTONOMY_TIERS.items():
        if re.search(pattern, content, re.IGNORECASE):
            report.tiers_found.append(tier_name)
        else:
            report.tiers_missing.append(tier_name)

    for check_name, pattern in SAFETY_CHECKS.items():
        if re.search(pattern, content, re.IGNORECASE):
            report.checks_found.append(check_name)
        else:
            report.checks_missing.append(check_name)
            report.issues.append(ValidationResult(
                code="S010",
                severity="WARNING",
                line=None,
                message=f"Missing safety mechanism: {check_name.replace('_', ' ')}",
            ))

    for line_num, line in enumerate(lines, start=1):
        for code, severity, pattern, message in CREDENTIAL_PATTERNS + ANTI_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                report.issues.append(ValidationResult(
                    code=code,
                    severity=severity,
                    line=line_num,
                    message=message,
                ))

    if not report.tiers_found:
        report.issues.append(ValidationResult(
            code="S009",
            severity="ERROR",
            line=None,
            message="No autonomy tier definitions found — define full-auto/supervised/human-led boundaries",
        ))

    return report


def format_report(report: SafetyReport) -> str:
    lines: list[str] = [f"\n🛡️  Safety Architecture Validation: {report.file_path}"]
    lines.append(f"   Autonomy tiers: {', '.join(report.tiers_found) or 'None detected'}")
    lines.append(f"   Safety checks:  {len(report.checks_found)}/{len(SAFETY_CHECKS)} present")
    lines.append(f"   Score:          {report.score}/10")

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
        description="Validate agent safety architecture — autonomy tiers, permissions, secret handling",
    )
    parser.add_argument("files", type=Path, nargs="+", help="Safety config file(s)")
    parser.add_argument("--strict", action="store_true", help="Exit 1 on any warnings or errors")

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
