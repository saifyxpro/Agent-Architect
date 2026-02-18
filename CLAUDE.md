# Agent Architect — Agent Instructions

## Project Context

This repository contains 6 AI agent skills for prompt engineering and agent architecture design. Skills are located under `skills/` with each following the structure: `SKILL.md` + `references/` + `scripts/`.

## Key Files

| Skill | SKILL.md | References | Script |
| ----- | -------- | ---------- | ------ |
| Prompt Engineer Pro | `skills/Prompt-Engineer-Pro/prompt-engineer-pro/SKILL.md` | 8 patterns + audit checklist | `validate_prompt.py` `lint_prompt.py` `analyze_tools.py` |
| Agent Orchestrator | `skills/Agent-Orchestrator/agent-orchestrator/SKILL.md` | 5 topology/routing refs | `validate_topology.py` |
| Context Engineer | `skills/Context-Engineer/context-engineer/SKILL.md` | 5 memory/budgeting refs | `validate_context.py` |
| Agent Safety Architect | `skills/Agent-Safety-Architect/agent-safety-architect/SKILL.md` | 5 safety/permission refs | `validate_safety.py` |
| Tool SDK Designer | `skills/Tool-SDK-Designer/tool-sdk-designer/SKILL.md` | 5 spec/composition refs | `validate_toolspec.py` |
| Agent FinOps | `skills/Agent-FinOps/agent-finops/SKILL.md` | 4 cost/tiering refs | `estimate_cost.py` |

Other important files:

- `analysis_summary.md` — Full research analysis of 16+ production agent systems
- `public/` — Packaged `.skill` files for distribution

## Development Guidelines

- Patterns are based on real production agent prompts — cite sources when extending
- Each pattern reference file follows the format: Source → When to Use → Template → Key Principle
- SKILL.md should stay under 500 lines per skill-creator guidelines
- Reference files are loaded on-demand — keep them self-contained
- Each skill must have a `scripts/` directory with at least one validation script

## Validation Scripts

All scripts use the same interface pattern:

```bash
python3 scripts/<script_name>.py <file> [--strict]
```

Scripts produce 0-10 scores, categorized issues (ERROR/WARNING/INFO), and use dataclass-based results with regex rule matching. The `--strict` flag exits with code 1 on any warnings or errors.

## Conventions

- Pattern files are numbered `01-` through `08-` for consistent ordering
- Templates use XML tags matching production implementations
- Audit checklist uses checkbox format for actionable evaluation
- Skill directories follow `Kebab-Case/kebab-case/` nesting
- All scripts are standalone Python 3 CLI tools with argparse
