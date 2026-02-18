#!/usr/bin/env python3

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


class Severity(Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class Finding:
    severity: Severity
    category: str
    message: str
    line: int | None = None
    suggestion: str | None = None


@dataclass
class SectionCheck:
    name: str
    present: bool = False
    patterns: list[str] = field(default_factory=list)
    line: int | None = None


@dataclass
class AuditReport:
    file_path: str
    total_lines: int
    total_chars: int
    sections_found: list[SectionCheck] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)
    score: int = 0
    max_score: int = 10
    rating: str = "Not Rated"


SECTION_DEFINITIONS: dict[str, list[str]] = {
    "identity": [
        r"<identity>", r"## identity", r"## persona", r"## role",
        r"you are \w+", r"your name is", r"## who you are",
        r"## about you", r"<agent_identity>",
    ],
    "capabilities": [
        r"<capabilities>", r"## capabilities", r"## what you can do",
        r"you can\b", r"you are able to", r"## abilities",
        r"things you can do", r"<tools>",
    ],
    "boundaries": [
        r"you cannot", r"you must not", r"never\b", r"do not\b",
        r"## limitations", r"## boundaries", r"## restrictions",
        r"things you cannot do", r"<limitations>",
    ],
    "tool_specs": [
        r"<tool", r"## tools", r"function\s*\(", r"parameters?:",
        r"type:\s*(string|number|boolean|object|array)",
        r"required:", r"<tools_available>", r"tool_use",
    ],
    "behavioral_rules": [
        r"<rules>", r"## rules", r"## guidelines", r"## instructions",
        r"always\b", r"<behavioral_rules>", r"## behavioral",
        r"## constraints", r"important:",
    ],
    "communication_style": [
        r"<communication>", r"## communication", r"## output format",
        r"## response format", r"markdown", r"## formatting",
        r"## style", r"<response_format>",
    ],
    "safety_guardrails": [
        r"<safety>", r"## safety", r"## security", r"api.key",
        r"secret", r"credential", r"<security>", r"do not expose",
        r"sensitive", r"approval", r"confirm before",
    ],
    "error_handling": [
        r"<error", r"## error", r"if.*fail", r"try.again",
        r"fallback", r"retry", r"when.*stuck", r"## troubleshoot",
        r"escalat", r"## recovery",
    ],
    "environment": [
        r"<environment>", r"## environment", r"operating.system",
        r"os:", r"shell:", r"## system", r"linux|macos|windows",
        r"runtime", r"## platform",
    ],
}

ANTI_PATTERNS: list[tuple[str, str, str]] = [
    (
        "vague_identity",
        r"you are (a |an )?(helpful|general|versatile|powerful) (assistant|ai|agent)\b",
        "Vague identity detected. Use a specific name, role, and domain.",
    ),
    (
        "wall_of_text",
        None,
        "No structural tags or headers found. Break into tagged sections.",
    ),
    (
        "redundant_rules",
        None,
        "Same rule stated 3+ times. Consolidate into a single section.",
    ),
    (
        "magic_strings",
        r"(?:timeout|delay|limit|max|min)\s*[:=]\s*\d{2,}(?!\w)",
        "Magic numbers detected. Extract to named constants.",
    ),
    (
        "over_commenting",
        r"(?:add comments|write comments|comment.*code|document.*function)",
        "Prompt instructs adding comments. Trust self-documenting code instead.",
    ),
    (
        "silent_failure",
        None,
        "No error handling guidance. Add instructions for when tools fail.",
    ),
    (
        "swallowed_errors",
        r"try your best|do what you can|best effort",
        "Vague error handling. Add explicit escalation paths.",
    ),
    (
        "todo_fixme",
        r"\bTODO\b|\bFIXME\b|\bHACK\b|\bXXX\b",
        "Incomplete placeholder found. Remove TODOs from production prompts.",
    ),
    (
        "placeholder_text",
        r"\[insert\b|\[your\b|\[placeholder\b|\[fill in\b|lorem ipsum",
        "Placeholder text detected. Replace with actual content.",
    ),
]

TOOL_SPEC_PATTERNS: list[tuple[str, str]] = [
    ("typed_parameters", r"type:\s*(string|number|boolean|integer|object|array)"),
    ("required_fields", r"required:\s*(true|false|\[)"),
    ("tool_examples", r"example[s]?:|input:|output:|usage:"),
    ("error_cases", r"error|fail|exception|invalid|edge.case"),
    ("safety_flags", r"dangerous|destructive|safe|approval|confirm"),
    ("descriptions", r"description:\s*[\"']"),
]


def read_prompt_file(file_path: Path) -> str:
    return file_path.read_text(encoding="utf-8")


def count_structural_elements(content: str) -> dict[str, int]:
    return {
        "xml_tags": len(re.findall(r"<\w+[^>]*>", content)),
        "headers": len(re.findall(r"^#{1,6}\s+", content, re.MULTILINE)),
        "code_blocks": len(re.findall(r"```", content)) // 2,
        "bullet_lists": len(re.findall(r"^\s*[-*]\s+", content, re.MULTILINE)),
        "numbered_lists": len(re.findall(r"^\s*\d+\.\s+", content, re.MULTILINE)),
        "tables": len(re.findall(r"^\|.*\|$", content, re.MULTILINE)),
    }


def check_sections(content: str) -> list[SectionCheck]:
    lines = content.lower().split("\n")
    results: list[SectionCheck] = []

    for section_name, patterns in SECTION_DEFINITIONS.items():
        check = SectionCheck(name=section_name, patterns=patterns)
        for line_num, line in enumerate(lines, start=1):
            for pattern in patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    check.present = True
                    check.line = line_num
                    break
            if check.present:
                break
        results.append(check)

    return results


def detect_anti_patterns(content: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = content.split("\n")
    structural = count_structural_elements(content)

    for ap_name, pattern, message in ANTI_PATTERNS:
        if ap_name == "wall_of_text":
            if structural["xml_tags"] == 0 and structural["headers"] <= 2:
                if len(lines) > 50:
                    findings.append(Finding(
                        severity=Severity.ERROR,
                        category="anti_pattern",
                        message=message,
                        suggestion="Add <identity>, <rules>, <tools> XML sections or ## headers",
                    ))
            continue

        if ap_name == "redundant_rules":
            rule_phrases = re.findall(
                r"(?:always|never|must|do not|don't)\s+.{10,60}",
                content, re.IGNORECASE,
            )
            normalized = [re.sub(r"\s+", " ", p.lower().strip()) for p in rule_phrases]
            from collections import Counter
            counts = Counter(normalized)
            repeated = {phrase: count for phrase, count in counts.items() if count >= 3}
            if repeated:
                findings.append(Finding(
                    severity=Severity.WARNING,
                    category="anti_pattern",
                    message=f"{message} Repeated: {list(repeated.keys())[:3]}",
                ))
            continue

        if ap_name == "silent_failure":
            sections = check_sections(content)
            error_section = next(
                (s for s in sections if s.name == "error_handling"), None,
            )
            if error_section and not error_section.present:
                findings.append(Finding(
                    severity=Severity.WARNING,
                    category="anti_pattern",
                    message=message,
                    suggestion="Add ## Error Handling or <error_handling> section",
                ))
            continue

        if pattern is None:
            continue

        for line_num, line in enumerate(lines, start=1):
            if re.search(pattern, line, re.IGNORECASE):
                findings.append(Finding(
                    severity=Severity.WARNING,
                    category="anti_pattern",
                    message=message,
                    line=line_num,
                ))
                break

    return findings


def analyze_tool_specs(content: str) -> list[Finding]:
    findings: list[Finding] = []
    has_tools = bool(re.search(
        r"<tool|## tools|function\s*\(|parameters?:", content, re.IGNORECASE,
    ))

    if not has_tools:
        findings.append(Finding(
            severity=Severity.INFO,
            category="tools",
            message="No tool specifications detected in prompt.",
        ))
        return findings

    for check_name, pattern in TOOL_SPEC_PATTERNS:
        matches = re.findall(pattern, content, re.IGNORECASE)
        if not matches:
            severity = Severity.WARNING if check_name in (
                "typed_parameters", "descriptions",
            ) else Severity.INFO
            findings.append(Finding(
                severity=severity,
                category="tools",
                message=f"Missing {check_name.replace('_', ' ')} in tool definitions.",
                suggestion=f"Add {check_name.replace('_', ' ')} to all tool specs.",
            ))

    return findings


def check_prompt_hygiene(content: str) -> list[Finding]:
    findings: list[Finding] = []
    lines = content.split("\n")
    total_lines = len(lines)
    total_chars = len(content)

    if total_lines > 2000:
        findings.append(Finding(
            severity=Severity.WARNING,
            category="hygiene",
            message=f"Prompt is {total_lines} lines. Consider splitting into base + skills.",
            suggestion="Use Skill Injection pattern (01-skill-injection.md) to modularize.",
        ))

    if total_chars > 100000:
        findings.append(Finding(
            severity=Severity.WARNING,
            category="hygiene",
            message=f"Prompt is {total_chars:,} chars. May consume excessive context.",
        ))

    long_lines = [
        (i, len(line))
        for i, line in enumerate(lines, start=1)
        if len(line) > 500
    ]
    if len(long_lines) > 5:
        findings.append(Finding(
            severity=Severity.INFO,
            category="hygiene",
            message=f"{len(long_lines)} lines exceed 500 chars. Consider breaking up.",
        ))

    empty_blocks = re.findall(r"\n{4,}", content)
    if empty_blocks:
        findings.append(Finding(
            severity=Severity.INFO,
            category="hygiene",
            message=f"{len(empty_blocks)} blocks of 4+ empty lines. Clean up whitespace.",
        ))

    return findings


def calculate_score(
    sections: list[SectionCheck],
    findings: list[Finding],
) -> tuple[int, str]:
    score = sum(1 for s in sections if s.present)

    anti_pattern_count = sum(
        1 for f in findings
        if f.category == "anti_pattern" and f.severity in (Severity.ERROR, Severity.WARNING)
    )
    score = max(0, score - anti_pattern_count)

    score = min(score, 10)

    rating_map = {
        range(0, 4): "Poor",
        range(4, 7): "Fair",
        range(7, 9): "Good",
        range(9, 11): "Excellent",
    }
    rating = next(
        (label for r, label in rating_map.items() if score in r),
        "Not Rated",
    )

    return score, rating


def run_audit(file_path: Path) -> AuditReport:
    content = read_prompt_file(file_path)
    lines = content.split("\n")

    report = AuditReport(
        file_path=str(file_path),
        total_lines=len(lines),
        total_chars=len(content),
    )

    report.sections_found = check_sections(content)
    report.findings.extend(detect_anti_patterns(content))
    report.findings.extend(analyze_tool_specs(content))
    report.findings.extend(check_prompt_hygiene(content))
    report.score, report.rating = calculate_score(
        report.sections_found, report.findings,
    )

    return report


def format_text_report(report: AuditReport) -> str:
    lines: list[str] = []
    lines.append(f"{'=' * 60}")
    lines.append(f"  PROMPT AUDIT REPORT")
    lines.append(f"{'=' * 60}")
    lines.append(f"  File:  {report.file_path}")
    lines.append(f"  Lines: {report.total_lines}  |  Chars: {report.total_chars:,}")
    lines.append(f"  Score: {report.score}/{report.max_score} ({report.rating})")
    lines.append(f"{'=' * 60}")

    lines.append(f"\n  SECTION COVERAGE")
    lines.append(f"  {'-' * 40}")
    for section in report.sections_found:
        icon = "✅" if section.present else "❌"
        loc = f" (line {section.line})" if section.line else ""
        lines.append(f"  {icon}  {section.name:<25}{loc}")

    present = sum(1 for s in report.sections_found if s.present)
    total = len(report.sections_found)
    lines.append(f"\n  Coverage: {present}/{total} sections")

    if report.findings:
        lines.append(f"\n  FINDINGS")
        lines.append(f"  {'-' * 40}")
        for finding in sorted(report.findings, key=lambda f: f.severity.value):
            loc = f" L{finding.line}" if finding.line else ""
            lines.append(f"  [{finding.severity.value:<7}] {finding.category}: {finding.message}{loc}")
            if finding.suggestion:
                lines.append(f"           → {finding.suggestion}")

    errors = sum(1 for f in report.findings if f.severity == Severity.ERROR)
    warnings = sum(1 for f in report.findings if f.severity == Severity.WARNING)
    infos = sum(1 for f in report.findings if f.severity == Severity.INFO)
    lines.append(f"\n  Summary: {errors} errors, {warnings} warnings, {infos} info")
    lines.append(f"{'=' * 60}")

    return "\n".join(lines)


def format_json_report(report: AuditReport) -> str:
    return json.dumps({
        "file": report.file_path,
        "lines": report.total_lines,
        "chars": report.total_chars,
        "score": report.score,
        "max_score": report.max_score,
        "rating": report.rating,
        "sections": [
            {"name": s.name, "present": s.present, "line": s.line}
            for s in report.sections_found
        ],
        "findings": [
            {
                "severity": f.severity.value,
                "category": f.category,
                "message": f.message,
                "line": f.line,
                "suggestion": f.suggestion,
            }
            for f in report.findings
        ],
    }, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate and audit AI agent system prompts",
    )
    parser.add_argument(
        "prompt_file",
        type=Path,
        help="Path to the system prompt file to audit",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if any errors found",
    )

    args = parser.parse_args()

    if not args.prompt_file.exists():
        print(f"Error: File not found: {args.prompt_file}", file=sys.stderr)
        sys.exit(1)

    report = run_audit(args.prompt_file)

    if args.format == "json":
        print(format_json_report(report))
    else:
        print(format_text_report(report))

    if args.strict:
        error_count = sum(1 for f in report.findings if f.severity == Severity.ERROR)
        if error_count > 0:
            sys.exit(1)


if __name__ == "__main__":
    main()
