#!/usr/bin/env python3

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class LintResult:
    code: str
    severity: str
    line: int | None
    message: str


LINT_RULES: list[tuple[str, str, str | None, str]] = [
    ("P001", "ERROR", r"^(?!.*(<\w+>|^#{1,6}\s)).*$", "No structural markup detected"),
    ("P002", "WARNING", r"you are (a |an )?(helpful|general) (assistant|ai)\b", "Vague identity — use specific name and role"),
    ("P003", "WARNING", r"\bTODO\b|\bFIXME\b|\bHACK\b", "Incomplete placeholder in production prompt"),
    ("P004", "WARNING", r"\[insert\b|\[your\b|\[placeholder\b", "Unfilled placeholder template text"),
    ("P005", "INFO", r"(?:timeout|delay|limit|max)\s*[:=]\s*\d{3,}", "Magic number — extract to named constant"),
    ("P006", "WARNING", r"try your best|do what you can|best effort", "Vague error handling — define explicit recovery steps"),
    ("P007", "INFO", r"(?:add comments|write comments|comment.*every)", "Instructs commenting — prefer self-documenting code"),
    ("P008", "WARNING", r"(?:api[_.]?key|password|secret|token)\s*[:=]\s*['\"][^'\"]{8,}", "Possible hardcoded credential"),
    ("P009", "INFO", r"lorem ipsum", "Lorem Ipsum placeholder text"),
    ("P010", "WARNING", r"(?:always|never|must)\s+(?:always|never|must)", "Redundant emphasis — single modifier sufficient"),
]


def lint_file(file_path: Path) -> list[LintResult]:
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    results: list[LintResult] = []

    has_structure = bool(re.search(r"<\w+>|^#{1,6}\s", content, re.MULTILINE))
    if not has_structure and len(lines) > 30:
        results.append(LintResult(
            code="P001",
            severity="ERROR",
            line=None,
            message="No XML tags or markdown headers found in prompt (>30 lines)",
        ))

    for line_num, line in enumerate(lines, start=1):
        for code, severity, pattern, message in LINT_RULES:
            if code == "P001":
                continue
            if pattern and re.search(pattern, line, re.IGNORECASE):
                results.append(LintResult(
                    code=code,
                    severity=severity,
                    line=line_num,
                    message=message,
                ))

    if len(lines) > 2000:
        results.append(LintResult(
            code="P011",
            severity="WARNING",
            line=None,
            message=f"Prompt is {len(lines)} lines — consider modularizing with Skill Injection",
        ))

    if len(content) > 100000:
        results.append(LintResult(
            code="P012",
            severity="WARNING",
            line=None,
            message=f"Prompt is {len(content):,} chars — excessive context consumption",
        ))

    empty_blocks = re.findall(r"\n{5,}", content)
    if empty_blocks:
        results.append(LintResult(
            code="P013",
            severity="INFO",
            line=None,
            message=f"{len(empty_blocks)} blocks of 5+ consecutive empty lines",
        ))

    seen_rules: dict[str, list[int]] = {}
    for line_num, line in enumerate(lines, start=1):
        match = re.search(
            r"((?:always|never|must|do not)\s+.{10,50})",
            line, re.IGNORECASE,
        )
        if match:
            normalized = re.sub(r"\s+", " ", match.group(1).lower().strip())
            seen_rules.setdefault(normalized, []).append(line_num)

    for rule_text, occurrences in seen_rules.items():
        if len(occurrences) >= 3:
            results.append(LintResult(
                code="P014",
                severity="WARNING",
                line=occurrences[0],
                message=f"Rule repeated {len(occurrences)}x: \"{rule_text[:40]}...\"",
            ))

    return results


def format_results(results: list[LintResult], file_path: Path) -> str:
    if not results:
        return f"✅ {file_path}: No issues found"

    lines: list[str] = []
    errors = sum(1 for r in results if r.severity == "ERROR")
    warnings = sum(1 for r in results if r.severity == "WARNING")
    infos = sum(1 for r in results if r.severity == "INFO")

    for result in sorted(results, key=lambda item: (
        {"ERROR": 0, "WARNING": 1, "INFO": 2}[item.severity],
        item.line or 0,
    )):
        loc = f":{result.line}" if result.line else ""
        icon = {"ERROR": "❌", "WARNING": "⚠️ ", "INFO": "ℹ️ "}[result.severity]
        lines.append(f"  {icon} {result.code} {file_path}{loc}: {result.message}")

    summary_icon = "❌" if errors > 0 else "⚠️ " if warnings > 0 else "ℹ️ "
    lines.append(f"\n{summary_icon} {errors} errors, {warnings} warnings, {infos} info")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Quick lint check for AI agent system prompts",
    )
    parser.add_argument(
        "files",
        type=Path,
        nargs="+",
        help="System prompt file(s) to lint",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any warnings or errors found",
    )

    args = parser.parse_args()

    exit_code = 0
    for file_path in args.files:
        if not file_path.exists():
            print(f"Error: File not found: {file_path}", file=sys.stderr)
            exit_code = 1
            continue

        results = lint_file(file_path)
        print(format_results(results, file_path))

        if args.strict and any(
            r.severity in ("ERROR", "WARNING") for r in results
        ):
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
