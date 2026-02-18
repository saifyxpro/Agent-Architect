#!/usr/bin/env python3

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

VALID_TOPOLOGIES = {"hub-and-spoke", "pipeline", "broadcast", "hierarchical", "mesh"}

REQUIRED_SECTIONS = {
    "roles": r"(?:role|agent)\s*[:=]",
    "routing": r"(?:route|routing|dispatch|delegate)",
    "communication": r"(?:message|protocol|channel|event)",
    "error_handling": r"(?:fallback|error|failure|timeout|retry)",
}

ANTI_PATTERNS = [
    ("O001", "WARNING", r"(?:single[- ]?point[- ]?of[- ]?failure|spof)", "Single point of failure risk detected"),
    ("O002", "WARNING", r"(?:circular[- ]?dependency|deadlock)", "Circular dependency or deadlock risk"),
    ("O003", "INFO", r"(?:unlimited|infinite|unbounded)\s+(?:retry|loop|recursion)", "Unbounded retry/loop — add max iteration limits"),
    ("O004", "WARNING", r"(?:shared[- ]?mutable[- ]?state|global[- ]?state)", "Shared mutable state — use message passing instead"),
    ("O005", "INFO", r"(?:hardcoded|hard[- ]?coded)\s+(?:agent|role|name)", "Hardcoded agent references — use role-based routing"),
]


@dataclass
class ValidationResult:
    code: str
    severity: str
    line: int | None
    message: str


@dataclass
class TopologyReport:
    file_path: Path
    topology_detected: str | None = None
    agent_count: int = 0
    sections_found: list[str] = field(default_factory=list)
    sections_missing: list[str] = field(default_factory=list)
    issues: list[ValidationResult] = field(default_factory=list)

    @property
    def score(self) -> int:
        base = 10
        base -= len(self.sections_missing) * 2
        base -= sum(1 for i in self.issues if i.severity == "WARNING")
        base -= sum(2 for i in self.issues if i.severity == "ERROR")
        return max(0, min(10, base))


def detect_topology(content: str) -> str | None:
    content_lower = content.lower()
    for topology in VALID_TOPOLOGIES:
        if topology.replace("-", " ") in content_lower or topology in content_lower:
            return topology
    return None


def count_agents(content: str) -> int:
    agent_patterns = [
        r"(?:agent|role|worker|specialist)\s*[:=]\s*[\"']?\w+",
        r"##\s+(?:Agent|Role|Worker)\s+\d+",
        r"name:\s*[\"']?\w+[\"']?\s*\n\s*role:",
    ]
    agents = set()
    for pattern in agent_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            agents.add(match.group(0).strip().lower())
    return max(len(agents), 1)


def validate_file(file_path: Path) -> TopologyReport:
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")
    report = TopologyReport(file_path=file_path)

    report.topology_detected = detect_topology(content)
    report.agent_count = count_agents(content)

    for section_name, pattern in REQUIRED_SECTIONS.items():
        if re.search(pattern, content, re.IGNORECASE):
            report.sections_found.append(section_name)
        else:
            report.sections_missing.append(section_name)
            report.issues.append(ValidationResult(
                code="O010",
                severity="WARNING",
                line=None,
                message=f"Missing recommended section: {section_name}",
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

    if report.topology_detected == "hub-and-spoke" and report.agent_count > 10:
        report.issues.append(ValidationResult(
            code="O006",
            severity="WARNING",
            line=None,
            message=f"Hub-and-spoke with {report.agent_count} agents — consider hierarchical topology",
        ))

    return report


def format_report(report: TopologyReport) -> str:
    lines: list[str] = [f"\n📐 Orchestration Topology Validation: {report.file_path}"]
    lines.append(f"   Topology: {report.topology_detected or 'Not detected'}")
    lines.append(f"   Agents:   ~{report.agent_count}")
    lines.append(f"   Sections: {len(report.sections_found)}/{len(REQUIRED_SECTIONS)} found")
    lines.append(f"   Score:    {report.score}/10")

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
        description="Validate multi-agent orchestration topology configurations",
    )
    parser.add_argument("files", type=Path, nargs="+", help="Orchestration config file(s)")
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
