# Agent Architecture Analysis — Complete Findings

> Deep analysis of 16+ production AI agent systems from `kimi-agent-internals` and `system-prompts-and-models-of-ai-tools` repositories.

---

## Architectural Pattern Taxonomy

Seven distinct architectural patterns used across production agent systems.

### Pattern 1: Skill Injection (Runtime Knowledge Loading)
**Source:** Kimi | **Mechanism:** Generic tools + runtime SKILL.md loading. Knowledge is modular, transient, and task-specific. Uses Dynamic Context Loading — sub-documents loaded/unloaded during execution based on what the agent encounters.

### Pattern 2: Persona Replacement (Identity Swap)
**Source:** Kimi Slides | **Mechanism:** Entire identity replaced with domain expert character for creative tasks with subjective quality criteria. Cannot be encoded as procedural SKILL.md.

### Pattern 3: State Machine Planning (Mode Switching)
**Sources:** Devin, Kiro, Traycer, Cursor, Antigravity | **Mechanism:** Explicit named states with enforced transitions. Three variants: Two-mode (Devin: planning/standard), Three-phase spec-driven (Kiro: EARS requirements→design→tasks), Read-only (Traycer: search/read only, no edits).

### Pattern 4: Structured Scratchpad (Explicit Reasoning)
**Sources:** Devin, Cursor | **Mechanism:** Dedicated `<think>` tool or `status_update_spec` for internal reasoning. Devin mandates `<think>` in 10 specific situations including before git decisions and before reporting completion.

### Pattern 5: Todo Tracking (Session-Persistent Task State)
**Sources:** Claude Code, Cursor, Kimi | **Mechanism:** TodoWrite/todo_write tool maintains checklist throughout session. Cursor enforces gate-before-edit and self-correction for missed updates.

### Pattern 6: XML-Tagged Response Protocol
**Sources:** Replit, Devin, Kiro, Windsurf | **Mechanism:** All communication wrapped in semantic XML tags. Replit uses 6 distinct action types with specific attributes. Devin uses XML commands with parameters as attributes.

### Pattern 7: Design System Enforcement
**Sources:** v0, Lovable | **Mechanism:** Prompt enforces specific design tokens (colors, typography, spacing), component libraries, and prohibits ad-hoc styling.

---

## Cross-Agent Comparison Matrix

| Agent | Skill Inject | Persona | State Machine | Scratchpad | Todo | XML Protocol | Design System |
|-------|:-----------:|:-------:|:------------:|:----------:|:----:|:------------:|:------------:|
| **Kimi** | ✅ | ✅ | — | — | ✅ | — | — |
| **Kiro** | — | — | ✅✅✅ | — | — | ✅ | — |
| **Cursor** | — | — | ✅ | ✅ | ✅✅ | ✅ | — |
| **Devin** | — | — | ✅✅ | ✅✅ | — | ✅✅ | — |
| **Traycer** | — | — | ✅ | — | — | ✅ | — |
| **Replit** | — | — | — | — | — | ✅✅✅ | — |
| **Claude Code** | — | — | — | — | ✅✅ | — | — |
| **v0** | — | — | — | — | — | — | ✅✅ |
| **Lovable** | — | — | — | — | — | — | ✅✅ |
| **Windsurf** | — | — | ✅ | — | — | ✅ | — |
| **Manus** | — | — | — | — | — | — | — |
| **Antigravity** | ✅ | — | ✅✅ | — | ✅ | ✅ | ✅ |

---

## Unique Innovations

- **Kimi** — Skill-Gated Shell: generic tools + SKILL.md = no new API endpoints needed
- **Kiro** — Formal EARS requirements engineering with 3-phase approval gates
- **Devin** — Mandatory `<think>` in 10 specific situations for self-audit
- **Cursor** — Most aggressive parallel tool execution strategy
- **Traycer** — Role-based capability restriction (read-only planning)
- **Replit** — Most granular response protocol (6 structured action types)

## Source Repositories

- [kimi-agent-internals](https://github.com/nicekid1/kimi-agent-internals)
- [system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)
