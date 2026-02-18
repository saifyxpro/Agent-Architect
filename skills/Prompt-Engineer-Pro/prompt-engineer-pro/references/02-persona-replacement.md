# Pattern: Persona Replacement (Identity Swap)

Source: Kimi Slides (McKinsey consultant persona)

## When to Use

- Task requires subjective aesthetic judgment
- Quality criteria cannot be specified procedurally
- Creative output depends on taste, not rules
- Domain expertise is better conveyed as character than documentation

## When NOT to Use

- Task has objective correctness criteria (formulas, validation, compilation)
- Output can be verified with binary pass/fail checks
- Domain knowledge can be written as procedural rules

## Decision Matrix

| Task Type | Quality Criteria | Approach |
|-----------|-----------------|----------|
| Spreadsheets | Formula correctness | Skill Injection |
| Documents | Format compliance | Skill Injection |
| Presentations | Visual impact | Persona Replacement |
| UX copy | Tone and engagement | Persona Replacement |
| Code review | Correctness + style | Hybrid |

## Template

```markdown
You are a [role] who has worked at [prestige marker] for [N] years,
specializing in [specific competency].

Your approach:
1. [Phase 1: analysis/discovery from the persona's perspective]
2. [Phase 2: structure/outline with interactive approval]
3. [Phase 3: execution/rendering — this part is procedural]

Your aesthetic values:
- [Value 1: e.g., "high-information-density layouts"]
- [Value 2: e.g., "clean hierarchical structure"]
- [Value 3: e.g., "data-driven visual storytelling"]

Your communication style:
- [Style trait: e.g., "authoritative but collaborative"]
- [Tone: e.g., "consultant-grade professional"]
```

## What Persona Provides (that SKILL.md Cannot)

1. **Aesthetic direction** — the persona knows implicit visual conventions
2. **Workflow authority** — presents as expert, not tool
3. **Design philosophy** — balances competing concerns via judgment
4. **Communication standards** — tone aligns with domain expectations

## Key Principle

Technical tasks get skill scaffolding. Creative tasks get persona replacement. The absence of a SKILL.md is not a gap — it is the signature of a persona-based paradigm.
