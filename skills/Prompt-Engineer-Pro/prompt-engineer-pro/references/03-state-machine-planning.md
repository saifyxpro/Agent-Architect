# Pattern: State Machine Planning (Mode Switching)

Sources: Devin, Kiro, Traycer, Cursor, Antigravity

## When to Use

- Multi-step workflows with distinct phases
- User needs visibility into agent's current phase
- Planning should be separated from execution
- Approval gates are required between phases

## Variant A: Two-Mode (Devin)

```
┌──────────┐     suggest_plan     ┌──────────┐
│ PLANNING ├─────────────────────►│ STANDARD │
│          │◄─────────────────────┤          │
└──────────┘     user override    └──────────┘
```

**Planning mode:** Gather info, search codebase, browse web. Call `<suggest_plan/>` when confident.
**Standard mode:** Execute plan steps. User sees current and next steps. Follow plan requirements.

### Template

```xml
<planning>
You are always in "planning" or "standard" mode. The user indicates your current mode.

While in "planning":
- Gather all information needed to fulfill the task
- Search and understand the codebase
- Ask the user for help if missing context or credentials
- Call <suggest_plan .../> once confident in your approach

While in "standard":
- Execute the current plan step
- Abide by the plan requirements
- Output actions for current or next steps
</planning>
```

## Variant B: Three-Phase Spec-Driven (Kiro)

```
Requirements ──► [approval gate] ──► Design ──► [approval gate] ──► Tasks
```

Each phase produces an artifact file. The agent MUST NOT proceed without explicit "yes" approval.

### Template

```xml
<workflow>
Phase 1: Requirements (EARS format user stories + acceptance criteria)
  → Write to .kiro/specs/{feature}/requirements.md
  → Ask user: "Do the requirements look good?"
  → MUST receive explicit approval before proceeding

Phase 2: Design (architecture, components, data models, testing)
  → Write to .kiro/specs/{feature}/design.md
  → Ask user: "Does the design look good?"
  → MUST receive explicit approval before proceeding

Phase 3: Tasks (numbered checkbox implementation plan)
  → Write to .kiro/specs/{feature}/tasks.md
  → Ask user: "Do the tasks look good?"
  → MUST receive explicit approval before proceeding
</workflow>
```

## Variant C: Read-Only Planning (Traycer)

The planning agent explicitly CANNOT edit or execute. It can only search, read, and propose phases.

### Template

```xml
<role>
You are the tech lead. You have readonly access to the codebase.
You DO NOT write code, but mention symbols, classes, and functions relevant to the task.
</role>

<limitations>
Things you can NOT do:
1. Edit files
2. Run terminal commands
</limitations>

<decision_tree>
1. Use search tools extensively to understand the codebase
2. Once you have complete clarity, use write_phases to break down the task
3. Ask for clarification only for critical missing info or pivotal decisions
</decision_tree>
```

## Key Principle

Separate information-gathering from action-taking. The agent should know everything it needs BEFORE making changes. Mode transitions should be explicit and user-controlled.
