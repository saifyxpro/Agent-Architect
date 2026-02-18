# Audit Checklist

Use this checklist to evaluate existing system prompts for completeness, anti-patterns, and architectural quality.

## Section Coverage

Check that the prompt includes these sections (mark N/A if genuinely not needed):

- [ ] **Identity block** — Name, role, core purpose (clear in ≤3 sentences)
- [ ] **Capability boundaries** — What the agent CAN and CANNOT do
- [ ] **Tool specifications** — Typed parameters, examples, edge cases
- [ ] **Behavioral rules** — Hard constraints that override other instructions
- [ ] **Communication style** — Output format, markdown rules, tone
- [ ] **Safety guardrails** — Data security, command approval, secret handling
- [ ] **Error handling** — What to do when tools fail, retries, fallbacks
- [ ] **Environment context** — OS, shell, runtime, available packages

## Anti-Pattern Detection

Flag these if found:

| Anti-Pattern | Description | Fix |
|-------------|-------------|-----|
| **Wall of text** | Single block with no XML tags or headers | Break into tagged sections |
| **Vague identity** | "You are a helpful assistant" | Add specific name, role, domain |
| **No boundaries** | Agent can do anything | Add explicit CAN/CANNOT lists |
| **Missing examples** | Tool usage described but never demonstrated | Add input/output examples |
| **Redundant rules** | Same rule stated 3+ times | Consolidate; move to a single section |
| **Magic strings** | Inline values without explanation | Extract to named constants or config |
| **Silent failure** | No guidance on what to do when stuck | Add error-handling section |
| **Swallowed errors** | "Try your best" without escalation path | Add user-communication triggers |
| **Over-commenting** | Instructions say "add comments to all code" | Remove; trust self-documenting code |
| **Scope creep** | Prompt handles 10+ unrelated domains | Split into base + skill injection |

## Pattern Compliance

For each pattern the prompt claims to use, verify proper implementation:

### Skill Injection
- [ ] Skills referenced by path with clear triggers
- [ ] Skill loading is mandatory before domain-specific work
- [ ] Dynamic sub-document loading is described

### State Machine Planning
- [ ] Modes are explicitly named
- [ ] Transitions are user-gated or rule-gated
- [ ] Each mode has distinct allowed actions

### Todo Tracking
- [ ] Creation rules define granularity
- [ ] Update cadence is specified (after each step)
- [ ] Self-correction rules exist for missed updates

### XML Protocol
- [ ] Each section has a semantic tag
- [ ] Action types have distinct XML tags
- [ ] Required attributes are documented

### Design System
- [ ] Tokens defined (colors, typography, spacing)
- [ ] Component library specified
- [ ] Ad-hoc values explicitly prohibited

## Scoring

| Score | Rating | Meaning |
|-------|--------|---------|
| 0-3 | Poor | Missing critical sections, multiple anti-patterns |
| 4-6 | Fair | Has basics but lacks depth in key areas |
| 7-8 | Good | Comprehensive with minor gaps |
| 9-10 | Excellent | Production-grade, follows proven patterns |

Count: 1 point per section covered, subtract 1 per anti-pattern found, add 1 per properly implemented pattern.
