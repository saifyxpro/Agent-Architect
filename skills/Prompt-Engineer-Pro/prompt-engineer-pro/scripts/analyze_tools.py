#!/usr/bin/env python3

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ToolDefinition:
    name: str
    line: int
    has_description: bool = False
    has_typed_params: bool = False
    has_required_fields: bool = False
    has_examples: bool = False
    has_error_handling: bool = False
    has_safety_flag: bool = False
    param_count: int = 0
    raw_block: str = ""


@dataclass
class ToolAnalysisReport:
    file_path: str
    total_tools: int = 0
    tools: list[ToolDefinition] = field(default_factory=list)
    quality_score: int = 0
    issues: list[str] = field(default_factory=list)


def extract_xml_tools(content: str) -> list[ToolDefinition]:
    tools: list[ToolDefinition] = []
    lines = content.split("\n")

    tool_pattern = re.compile(
        r"<tool\s+(?:name=[\"']([^\"']+)[\"']|[^>]*name=[\"']([^\"']+)[\"'])",
        re.IGNORECASE,
    )

    for line_num, line in enumerate(lines, start=1):
        match = tool_pattern.search(line)
        if match:
            name = match.group(1) or match.group(2)
            tool = ToolDefinition(name=name, line=line_num)

            block_end = min(line_num + 50, len(lines))
            block = "\n".join(lines[line_num - 1:block_end])

            close_idx = block.find("</tool")
            if close_idx > 0:
                block = block[:close_idx]

            tool.raw_block = block
            tools.append(tool)

    return tools


def extract_function_tools(content: str) -> list[ToolDefinition]:
    tools: list[ToolDefinition] = []
    lines = content.split("\n")

    func_patterns = [
        re.compile(r'"name":\s*"([^"]+)"', re.IGNORECASE),
        re.compile(r"'name':\s*'([^']+)'", re.IGNORECASE),
        re.compile(r"function\s+(\w+)\s*\(", re.IGNORECASE),
    ]

    seen_names: set[str] = set()

    for line_num, line in enumerate(lines, start=1):
        for pattern in func_patterns:
            match = pattern.search(line)
            if match:
                name = match.group(1)
                if name in seen_names or len(name) < 2:
                    continue
                seen_names.add(name)

                block_end = min(line_num + 30, len(lines))
                block = "\n".join(lines[line_num - 1:block_end])

                tool = ToolDefinition(name=name, line=line_num, raw_block=block)
                tools.append(tool)
                break

    return tools


def extract_xml_action_tags(content: str) -> list[ToolDefinition]:
    tools: list[ToolDefinition] = []
    lines = content.split("\n")
    seen_names: set[str] = set()

    action_pattern = re.compile(
        r"<(shell|str_replace|create_file|browser_action|open_file|"
        r"view_file|search_files|delete_file|write_to_file|run_command|"
        r"execute|submit|think|suggest_plan|search_dir|find_and_replace)"
        r"[\s>]",
        re.IGNORECASE,
    )

    for line_num, line in enumerate(lines, start=1):
        match = action_pattern.search(line)
        if match:
            name = match.group(1).lower()
            if name in seen_names:
                continue
            seen_names.add(name)

            block_end = min(line_num + 20, len(lines))
            block = "\n".join(lines[line_num - 1:block_end])
            tool = ToolDefinition(name=name, line=line_num, raw_block=block)
            tools.append(tool)

    return tools


def extract_markdown_tools(content: str) -> list[ToolDefinition]:
    tools: list[ToolDefinition] = []
    lines = content.split("\n")

    header_pattern = re.compile(r"^#{2,4}\s+(?:tool:\s*)?(\w[\w_.-]+)", re.IGNORECASE)

    for line_num, line in enumerate(lines, start=1):
        match = header_pattern.match(line)
        if match:
            name = match.group(1).lower()
            skip_words = {
                "the", "and", "for", "with", "about", "this", "that",
                "how", "when", "what", "why", "where", "overview",
                "introduction", "summary", "example", "usage", "notes",
                "tools", "parameters", "description", "rules", "guidelines",
            }
            if name in skip_words:
                continue

            block_end = min(line_num + 25, len(lines))
            block = "\n".join(lines[line_num - 1:block_end])

            next_header = re.search(r"^#{2,4}\s+", block[len(line):], re.MULTILINE)
            if next_header:
                block = block[:len(line) + next_header.start()]

            tool = ToolDefinition(name=name, line=line_num, raw_block=block)
            tools.append(tool)

    return tools


def analyze_tool_quality(tool: ToolDefinition) -> None:
    block = tool.raw_block.lower()

    tool.has_description = bool(re.search(
        r"description|purpose|what it does|used for|helps with",
        block,
    ))

    type_matches = re.findall(
        r"type:\s*(string|number|boolean|integer|object|array|float)",
        block,
    )
    tool.has_typed_params = len(type_matches) > 0
    tool.param_count = len(type_matches)

    tool.has_required_fields = bool(re.search(
        r"required:\s*(true|false|\[)|required\s+param",
        block,
    ))

    tool.has_examples = bool(re.search(
        r"example[s]?:|sample:|input:|output:|usage:|e\.g\.|for instance",
        block,
    ))

    tool.has_error_handling = bool(re.search(
        r"error|fail|invalid|exception|edge.case|if.*not found|when.*wrong",
        block,
    ))

    tool.has_safety_flag = bool(re.search(
        r"danger|destruct|safe|unsafe|approval|confirm|irreversib|warning|cautio",
        block,
    ))


def generate_report(file_path: Path, tools: list[ToolDefinition]) -> ToolAnalysisReport:
    report = ToolAnalysisReport(
        file_path=str(file_path),
        total_tools=len(tools),
    )

    for tool in tools:
        analyze_tool_quality(tool)
        report.tools.append(tool)

    if not tools:
        report.issues.append("No tool definitions detected in the prompt.")
        return report

    checks_per_tool = 6
    total_checks = len(tools) * checks_per_tool
    passed = sum(
        sum([
            t.has_description,
            t.has_typed_params,
            t.has_required_fields,
            t.has_examples,
            t.has_error_handling,
            t.has_safety_flag,
        ])
        for t in tools
    )
    report.quality_score = round((passed / total_checks) * 100) if total_checks > 0 else 0

    no_desc = [t.name for t in tools if not t.has_description]
    no_types = [t.name for t in tools if not t.has_typed_params]
    no_examples = [t.name for t in tools if not t.has_examples]
    no_safety = [t.name for t in tools if not t.has_safety_flag]

    if no_desc:
        report.issues.append(f"Missing descriptions: {', '.join(no_desc[:5])}")
    if no_types:
        report.issues.append(f"Missing typed parameters: {', '.join(no_types[:5])}")
    if no_examples:
        report.issues.append(f"Missing examples: {', '.join(no_examples[:5])}")
    if no_safety:
        report.issues.append(f"Missing safety flags: {', '.join(no_safety[:5])}")

    return report


def format_text(report: ToolAnalysisReport) -> str:
    lines: list[str] = []
    lines.append(f"{'=' * 60}")
    lines.append(f"  TOOL SPECIFICATION ANALYSIS")
    lines.append(f"{'=' * 60}")
    lines.append(f"  File:    {report.file_path}")
    lines.append(f"  Tools:   {report.total_tools}")
    lines.append(f"  Quality: {report.quality_score}%")
    lines.append(f"{'=' * 60}")

    if report.tools:
        lines.append(f"\n  TOOL DETAILS")
        lines.append(f"  {'-' * 40}")
        for tool in report.tools:
            lines.append(f"\n  📦 {tool.name} (line {tool.line})")
            checks = [
                ("Description", tool.has_description),
                ("Typed params", tool.has_typed_params),
                (f"Param count", tool.param_count > 0),
                ("Required fields", tool.has_required_fields),
                ("Examples", tool.has_examples),
                ("Error handling", tool.has_error_handling),
                ("Safety flags", tool.has_safety_flag),
            ]
            for label, passed in checks:
                icon = "✅" if passed else "❌"
                lines.append(f"     {icon} {label}")

    if report.issues:
        lines.append(f"\n  ISSUES")
        lines.append(f"  {'-' * 40}")
        for issue in report.issues:
            lines.append(f"  ⚠️  {issue}")

    lines.append(f"\n{'=' * 60}")
    return "\n".join(lines)


def format_json_output(report: ToolAnalysisReport) -> str:
    return json.dumps({
        "file": report.file_path,
        "total_tools": report.total_tools,
        "quality_score": report.quality_score,
        "tools": [
            {
                "name": t.name,
                "line": t.line,
                "has_description": t.has_description,
                "has_typed_params": t.has_typed_params,
                "param_count": t.param_count,
                "has_required_fields": t.has_required_fields,
                "has_examples": t.has_examples,
                "has_error_handling": t.has_error_handling,
                "has_safety_flag": t.has_safety_flag,
            }
            for t in report.tools
        ],
        "issues": report.issues,
    }, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze tool specifications in AI agent system prompts",
    )
    parser.add_argument(
        "prompt_file",
        type=Path,
        help="Path to the system prompt file to analyze",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    if not args.prompt_file.exists():
        print(f"Error: File not found: {args.prompt_file}", file=sys.stderr)
        sys.exit(1)

    content = args.prompt_file.read_text(encoding="utf-8")

    tools = extract_xml_tools(content)
    if not tools:
        tools = extract_xml_action_tags(content)
    if not tools:
        tools = extract_function_tools(content)
    if not tools:
        tools = extract_markdown_tools(content)

    report = generate_report(args.prompt_file, tools)

    if args.format == "json":
        print(format_json_output(report))
    else:
        print(format_text(report))


if __name__ == "__main__":
    main()
