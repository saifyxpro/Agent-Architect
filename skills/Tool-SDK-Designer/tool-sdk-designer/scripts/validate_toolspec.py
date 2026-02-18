#!/usr/bin/env python3

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SPEC_FORMATS = {
    "xml": r"<(?:function|tool|command)\b[^>]*>",
    "json_schema": r"\"(?:type|function|name|parameters)\":\s*\{",
    "markdown": r"(?:^##\s+\w+|^\|\s*(?:param|name|type))",
}

QUALITY_INDICATORS = {
    "description": r"\"?description\"?\s*[:=]",
    "parameters": r"\"?param(?:eter)?s?\"?\s*[:=\{]",
    "examples": r"(?:example|usage|sample)\s*[:=]|```",
    "error_handling": r"(?:error|exception|failure|invalid)\s*[:=]",
    "return_type": r"(?:return|output|response)\s*(?:type|format|schema)",
    "safety_flag": r"(?:dangerous|destructive|irreversible|requires_approval|is_dangerous)",
}

ANTI_PATTERNS = [
    ("T001", "WARNING", r"\"description\"\s*:\s*\"\"", "Empty tool description"),
    ("T002", "WARNING", r"\"type\"\s*:\s*\"any\"", "Parameter typed as 'any' — use specific type"),
    ("T003", "INFO", r"\"required\"\s*:\s*\[\s*\]", "Empty required array — verify all params are optional"),
    ("T004", "WARNING", r"(?:TODO|FIXME|TBD)\s+(?:param|description|example)", "Incomplete tool specification"),
    ("T005", "INFO", r"\"(?:enum|oneOf)\"\s*:\s*\[[^\]]{500,}", "Large enum — consider dynamic loading"),
]


@dataclass
class ValidationResult:
    code: str
    severity: str
    line: int | None
    message: str


@dataclass
class ToolSpec:
    name: str
    has_description: bool = False
    has_params: bool = False
    has_examples: bool = False
    has_error_handling: bool = False
    has_return_type: bool = False
    has_safety_flag: bool = False


@dataclass
class ToolSpecReport:
    file_path: Path
    format_detected: str | None = None
    tool_count: int = 0
    tools: list[ToolSpec] = field(default_factory=list)
    quality_coverage: dict[str, bool] = field(default_factory=dict)
    issues: list[ValidationResult] = field(default_factory=list)

    @property
    def score(self) -> int:
        base = 10
        missing = sum(1 for v in self.quality_coverage.values() if not v)
        base -= missing
        base -= sum(1 for i in self.issues if i.severity == "WARNING")
        base -= sum(2 for i in self.issues if i.severity == "ERROR")
        return max(0, min(10, base))


def detect_format(content: str) -> str | None:
    for fmt, pattern in SPEC_FORMATS.items():
        if re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            return fmt
    return None


def extract_json_tools(content: str) -> list[ToolSpec]:
    tools: list[ToolSpec] = []
    try:
        data = json.loads(content)
        tool_list = data if isinstance(data, list) else data.get("tools", data.get("functions", []))
        if isinstance(tool_list, list):
            for item in tool_list:
                if isinstance(item, dict):
                    func = item.get("function", item)
                    tool = ToolSpec(
                        name=func.get("name", "unknown"),
                        has_description=bool(func.get("description", "")),
                        has_params="parameters" in func or "params" in func,
                    )
                    tools.append(tool)
    except (json.JSONDecodeError, TypeError):
        pass
    return tools


def count_xml_tools(content: str) -> int:
    return len(re.findall(r"<(?:function|tool|command)\b", content, re.IGNORECASE))


def count_md_tools(content: str) -> int:
    return len(re.findall(r"^##\s+\w+", content, re.MULTILINE))


def validate_file(file_path: Path) -> ToolSpecReport:
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    report = ToolSpecReport(file_path=file_path)

    report.format_detected = detect_format(content)

    if report.format_detected == "json_schema":
        report.tools = extract_json_tools(content)
        report.tool_count = len(report.tools)
    elif report.format_detected == "xml":
        report.tool_count = count_xml_tools(content)
    elif report.format_detected == "markdown":
        report.tool_count = count_md_tools(content)

    for indicator_name, pattern in QUALITY_INDICATORS.items():
        report.quality_coverage[indicator_name] = bool(
            re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        )

    if not report.quality_coverage.get("description"):
        report.issues.append(ValidationResult(
            code="T010", severity="WARNING", line=None,
            message="No tool descriptions found",
        ))

    if not report.quality_coverage.get("examples"):
        report.issues.append(ValidationResult(
            code="T011", severity="INFO", line=None,
            message="No usage examples found — add at least one per tool",
        ))

    if not report.quality_coverage.get("safety_flag"):
        report.issues.append(ValidationResult(
            code="T012", severity="INFO", line=None,
            message="No safety flags found — consider marking destructive tools",
        ))

    for line_num, line in enumerate(lines, start=1):
        for code, severity, pattern, message in ANTI_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                report.issues.append(ValidationResult(
                    code=code, severity=severity, line=line_num, message=message,
                ))

    return report


def format_report(report: ToolSpecReport) -> str:
    lines: list[str] = [f"\n🔧 Tool Specification Validation: {report.file_path}"]
    lines.append(f"   Format:   {report.format_detected or 'Not detected'}")
    lines.append(f"   Tools:    {report.tool_count}")
    coverage = sum(1 for v in report.quality_coverage.values() if v)
    lines.append(f"   Quality:  {coverage}/{len(QUALITY_INDICATORS)} indicators present")
    lines.append(f"   Score:    {report.score}/10")

    if report.quality_coverage:
        lines.append("\n   Quality Indicators:")
        for name, present in report.quality_coverage.items():
            icon = "✅" if present else "❌"
            lines.append(f"   {icon} {name.replace('_', ' ').title()}")

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
        description="Validate tool specifications — format, quality indicators, anti-patterns",
    )
    parser.add_argument("files", type=Path, nargs="+", help="Tool spec file(s)")
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
