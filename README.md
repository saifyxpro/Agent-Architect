# Agent Architect

A collection of AI agent skills for designing, generating, auditing, and optimizing system prompts and agent architectures.

## Skills

### Prompt Engineer Pro

Generate and audit production-grade AI agent system prompts using **7 proven architectural patterns** extracted from 16+ production agent systems.

**Patterns covered:**

| # | Pattern | Source |
|---|---------|--------|
| 1 | Skill Injection | Kimi |
| 2 | Persona Replacement | Kimi Slides |
| 3 | State Machine Planning | Devin, Kiro, Traycer |
| 4 | Structured Scratchpad | Devin, Cursor |
| 5 | Todo Tracking | Claude Code, Cursor |
| 6 | XML Response Protocol | Replit, Devin, Windsurf |
| 7 | Design System Enforcement | v0, Lovable |

**Capabilities:**

- **Generate** new system prompts with pattern-based composition
- **Audit** existing prompts with a scored checklist (section coverage, anti-patterns, pattern compliance)
- **Optimize** prompt architecture for specific agent types (coding, creative, research, multi-domain)

### Installation

Download the `.skill` file from `public/` and install it in your agent environment.

```
public/prompt-engineer-pro.skill
```

## Repository Structure

```
Agent-Architect/
├── README.md                           # This file
├── CLAUDE.md                           # Claude/agent-specific instructions
├── .gitignore                          # Git ignore rules
├── analysis_summary.md                 # Full research analysis (16+ agents)
├── public/                             # Packaged distributable skills
│   └── prompt-engineer-pro.skill       # Installable skill package
└── skills/                             # Skill source code
    └── Prompt-Engineer-Pro/
        └── prompt-engineer-pro/
            ├── SKILL.md                # Core instructions
            └── references/             # Pattern library + audit checklist
                ├── 01-skill-injection.md
                ├── 02-persona-replacement.md
                ├── 03-state-machine-planning.md
                ├── 04-structured-scratchpad.md
                ├── 05-todo-tracking.md
                ├── 06-xml-response-protocol.md
                ├── 07-design-system-enforcement.md
                └── audit-checklist.md
```

## Research Methodology

Patterns were extracted from deep analysis of two repositories:

- [**kimi-agent-internals**](https://github.com/nicekid1/kimi-agent-internals) — Reverse-engineered internals of Kimi/Moonshot AI agents
- [**system-prompts-and-models-of-ai-tools**](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) — Collection of leaked/documented system prompts from Cursor, Devin, Kiro, Claude Code, v0, Windsurf, Lovable, Replit, Traycer, Manus, and more

See [analysis_summary.md](analysis_summary.md) for the full research findings.

## License

MIT
