# Agent Architect — Claude Instructions

## Project Context

This repository contains AI agent skills for prompt engineering and agent architecture design. The primary skill is **Prompt Engineer Pro**, which generates and audits system prompts using 7 proven patterns.

## Key Files

- `skills/Prompt-Engineer-Pro/prompt-engineer-pro/SKILL.md` — Main skill instructions
- `skills/Prompt-Engineer-Pro/prompt-engineer-pro/references/` — 7 pattern library files + audit checklist
- `analysis_summary.md` — Full research analysis of 16+ production agent systems
- `public/` — Packaged `.skill` files for distribution

## Development Guidelines

- Patterns are based on real production agent prompts — cite sources when extending
- Each pattern reference file follows the format: Source → When to Use → Template → Key Principle
- SKILL.md should stay under 500 lines per skill-creator guidelines
- Reference files are loaded on-demand — keep them self-contained

## Working with Skills

- Validate skill structure: `python3 quick_validate.py <skill-path>`
- Package for distribution: `python3 package_skill.py <skill-path> ./public`
- Both scripts are in the skill-creator at `~/.agents/skills/skill-creator/scripts/`

## Conventions

- Pattern files are numbered `01-` through `07-` for consistent ordering
- Templates use XML tags matching production implementations
- Audit checklist uses checkbox format for actionable evaluation
