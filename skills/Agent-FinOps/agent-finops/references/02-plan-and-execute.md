# Plan-and-Execute Pattern

A frontier model creates a strategy that cheaper models follow. Reduces cost by 80-90% compared to using frontier models for everything.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    PLANNER       │     │   EXECUTOR       │     │   VERIFIER       │
│  (Frontier)      │────▶│   (Economy)      │────▶│   (Mid-Tier)     │
│                  │     │                  │     │                  │
│ Creates detailed │     │ Follows plan     │     │ Checks results   │
│ step-by-step     │     │ step by step     │     │ against plan     │
│ plan with        │     │ using cheap,     │     │ expectations     │
│ success criteria │     │ fast model       │     │                  │
│                  │     │                  │     │ Pass → Deliver   │
│ Cost: HIGH       │     │ Cost: LOW        │     │ Fail → Re-plan   │
│ Frequency: 1x    │     │ Frequency: Nx    │     │ Frequency: 1x    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Plan Format Template

The planner MUST produce a plan structured enough for an economy model:

```
<execution_plan>
  <goal>[High-level objective]</goal>

  <step order="1">
    <action>[Exact action — no ambiguity]</action>
    <input>[Specific inputs and variables]</input>
    <expected_output>[What success looks like]</expected_output>
    <tools>[Which tools to use]</tools>
  </step>

  <step order="2">
    <action>[Next exact action]</action>
    <input>[Use {{step_1.output}} for referencing previous outputs]</input>
    <expected_output>[Success criteria]</expected_output>
    <tools>[Tools needed]</tools>
  </step>

  <verification>
    <criterion>[How to verify the plan succeeded]</criterion>
    <criterion>[Second verification check]</criterion>
  </verification>
</execution_plan>
```

## Key Rules

- Planner writes plans detailed enough that a junior developer could follow
- Executor NEVER deviates from the plan (no creative decisions)
- Verifier checks outputs against plan expectations, not its own judgment
- If verification fails, re-plan with frontier model (include failure context)
- Track plan success rate — if < 80%, plans are too vague

## Cost Savings Example

| Approach | Calls | Cost per Call | Total |
|----------|-------|---------------|-------|
| Frontier-only (10 steps) | 10 | $0.50 | $5.00 |
| Plan-Execute (1 plan + 10 exec + 1 verify) | 12 | Plan: $0.50, Exec: $0.01, Verify: $0.10 | $0.70 |
| **Savings** | | | **86%** |
