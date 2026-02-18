---
name: prompt-engineer-pro
description: Generate, audit, and optimize system prompts for AI agents using 7 proven architectural patterns extracted from 16+ production systems (Kimi, Cursor, Devin, Kiro, Claude Code, v0, Windsurf, Lovable, Replit, Traycer, Manus). Use when creating new agent system prompts, auditing existing prompts for quality and completeness, optimizing prompt architecture for specific use cases, or designing multi-agent workflows. Covers skill injection, persona replacement, state machine planning, structured scratchpad, todo tracking, XML response protocols, and design system enforcement.
---

# Prompt Engineer Pro

Generate and audit production-grade AI agent system prompts using proven architectural patterns.

## Workflow

Prompt engineering involves two workflows: **Generation** (creating new prompts) and **Auditing** (evaluating existing ones).

### Generation Workflow

1. Identify agent type and primary use case
2. Select applicable patterns from the pattern library
3. Compose the prompt using pattern templates
4. Validate against the audit checklist

### Auditing Workflow

1. Read the target prompt
2. Run through the audit checklist (see `references/audit-checklist.md`)
3. Score each section and identify anti-patterns
4. Propose specific improvements with pattern references

## Pattern Library

Seven patterns extracted from production agent systems. Read the relevant reference file before using each pattern.

| # | Pattern | When to Use | Reference |
|---|---------|-------------|-----------|
| 1 | Skill Injection | Multi-domain agents, modular knowledge | `references/01-skill-injection.md` |
| 2 | Persona Replacement | Creative/subjective tasks | `references/02-persona-replacement.md` |
| 3 | State Machine Planning | Multi-step workflows with approval gates | `references/03-state-machine-planning.md` |
| 4 | Structured Scratchpad | Irreversible decisions, self-audit | `references/04-structured-scratchpad.md` |
| 5 | Todo Tracking | Session-persistent task management | `references/05-todo-tracking.md` |
| 6 | XML Response Protocol | Machine-parseable structured output | `references/06-xml-response-protocol.md` |
| 7 | Design System Enforcement | UI code generation with consistency | `references/07-design-system-enforcement.md` |

## Pattern Selection Guide

Use this to determine which patterns to include based on agent type:

**Coding assistant** (IDE-embedded, writes/edits code):
→ Pattern 3 (State Machine) + Pattern 5 (Todo) + Pattern 6 (XML) + Pattern 4 (Scratchpad)

**Creative agent** (design, writing, presentations):
→ Pattern 2 (Persona) + Pattern 7 (Design System)

**Research/analysis agent** (read-only exploration, reports):
→ Pattern 1 (Skill Injection) + Pattern 3 (State Machine, read-only variant)

**Multi-domain agent** (handles many task types):
→ Pattern 1 (Skill Injection) + Pattern 3 (State Machine) + Pattern 5 (Todo)

**Full-stack agent** (plans, codes, deploys, tests):
→ All 7 patterns, with Patterns 1-3-5 as core and 4-6-7 as supporting

## Prompt Composition Rules

When generating a prompt, follow this structure:

```
1. <identity>        — Name, role, 2-3 sentence purpose
2. <capabilities>    — Explicit CAN/CANNOT lists
3. <rules>           — Hard behavioral constraints
4. <tools>           — Tool specs with typed parameters and examples
5. <workflow>        — Mode/phase definitions and transitions
6. <communication>   — Output format, markdown, tone
7. <safety>          — Secret handling, command approval, data security
8. <environment>     — OS, shell, runtime context
```

### Identity Block Best Practices

- State the name, then the role, then the purpose
- Keep it to 2-3 sentences maximum
- Include the hosting context (IDE name, platform)
- Example: "You are Kiro, an AI assistant and IDE built to assist developers."

### Tool Specification Best Practices

For each tool, include:
- Name and one-line description
- Required vs optional parameters with types
- At least one concrete input/output example
- Edge cases and error handling
- Safety flags where applicable (e.g., `is_dangerous` for shell commands)

### Rules Best Practices

- State rules as imperatives: "ALWAYS do X" / "NEVER do Y"
- Group related rules under subheadings
- Prioritize: safety rules first, then behavioral, then stylistic
- Avoid redundancy — each rule should appear exactly once

## Validation Scripts

Three Python scripts for automated prompt analysis. Run directly or use within the skill workflow.

**Full audit** — section coverage, anti-patterns, tool specs, hygiene, scoring (0-10):

```bash
python3 scripts/validate_prompt.py <prompt_file> [--format json] [--strict]
```

**Tool spec analysis** — extracts tool definitions (XML, JSON, markdown), checks quality:

```bash
python3 scripts/analyze_tools.py <prompt_file> [--format json]
```

**Quick lint** — fast check with 14 rules, supports multiple files, CI/CD compatible:

```bash
python3 scripts/lint_prompt.py <file1> [file2 ...] [--strict]
```

## Audit Quick Reference

Read `references/audit-checklist.md` for the full checklist. Key items:

**Must have:** Identity, capability boundaries, tool specs, behavioral rules, safety guardrails
**Should have:** Communication style, error handling, environment context
**Anti-patterns to flag:** Wall of text, vague identity, no boundaries, missing examples, redundant rules
**Score:** 0-3 Poor, 4-6 Fair, 7-8 Good, 9-10 Excellent
