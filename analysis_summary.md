# Agent Architecture Analysis — Complete Findings

> Deep analysis of 16+ production AI agent systems from `kimi-agent-internals` and `system-prompts-and-models-of-ai-tools` repositories.

---

## Architectural Pattern Taxonomy

Eight distinct architectural patterns used across production agent systems.

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

### Pattern 8: Prompt Structure Blueprint

**Sources:** Kimi, Cursor, Claude Code, Devin, Replit, Windsurf | **Mechanism:** Canonical section ordering and structural paradigms. Three paradigms identified: XML-Tagged Blocks (Replit, Windsurf, Devin), Markdown-Headed Sections (Kimi, Claude Code, Cursor), and Hybrid approaches. Universal 8-section order: identity → communication → capabilities → skills → rules → tools → output format → environment.

---

## Cross-Agent Comparison Matrix

| Agent | Skill Inject | Persona | State Machine | Scratchpad | Todo | XML Protocol | Design System |
| ----- | :---------: | :-----: | :-----------: | :--------: | :--: | :----------: | :-----------: |
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

## Prompt Structure Analysis

Structural paradigms extracted from 7 production agent prompts:

| Paradigm | Systems | Structure |
| -------- | ------- | --------- |
| XML-Tagged Blocks | Replit, Windsurf, Devin | `<identity>`, `<tools>`, `<rules>` semantic containers |
| Markdown-Headed | Kimi, Claude Code, Cursor | `# Section` headers with nested subsections |
| Hybrid | Most production agents | Mixed XML + Markdown within sections |

**Prompt Archetypes:**

- **Identity-Heavy** (Kimi, Claude Code) — 20-30% of tokens on identity/persona
- **Tool-Heavy** (Cursor, Devin) — 40-60% of tokens on tool definitions
- **Structure-Heavy** (Replit, Windsurf) — Rigid XML protocol, minimal prose

---

## Unique Innovations

- **Kimi** — Skill-Gated Shell: generic tools + SKILL.md = no new API endpoints needed
- **Kiro** — Formal EARS requirements engineering with 3-phase approval gates
- **Devin** — Mandatory `<think>` in 10 specific situations for self-audit
- **Cursor** — Most aggressive parallel tool execution strategy
- **Traycer** — Role-based capability restriction (read-only planning)
- **Replit** — Most granular response protocol (6 structured action types)

## Skills Built From This Research

| Skill | What It Covers |
| ----- | -------------- |
| Prompt Engineer Pro | All 8 patterns + 3 archetypes + validation toolchain |
| Agent Orchestrator | Multi-agent topologies, routing, error recovery |
| Context Engineer | Three-tier memory, token budgeting, retrieval |
| Agent Safety Architect | Autonomy tiers, permissions, secret handling |
| Tool SDK Designer | Tool specs across XML/JSON/Markdown formats |
| Agent FinOps | Model tiering, cost estimation across 12 LLMs |

## Source Repositories

- [kimi-agent-internals](https://github.com/nicekid1/kimi-agent-internals)
- [system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)
