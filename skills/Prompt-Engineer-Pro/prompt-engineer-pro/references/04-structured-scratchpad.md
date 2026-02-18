# Pattern: Structured Scratchpad (Explicit Reasoning)

Sources: Devin (`<think>`), Cursor (`status_update_spec`)

## When to Use

- Agent makes irreversible decisions (git operations, deployments, file deletions)
- Agent transitions between exploration and implementation
- Agent needs to self-audit before reporting completion
- Complex multi-step reasoning benefits from explicit verbalization

## Variant A: Think Tool (Devin)

A dedicated scratchpad invisible to the user for free-form reasoning.

### Mandatory Triggers

The agent MUST use `<think>` in these situations:
1. Before critical git/GitHub decisions (branching, checkout, PR creation)
2. When transitioning from exploring code to making changes
3. Before reporting completion to the user

### Optional Triggers

Use `<think>` when:
- No clear next step exists
- Details are unclear but important to get right
- Facing unexpected difficulties
- Multiple approaches have failed
- Making a critical decision that benefits from extra thought
- Tests, lint, or CI failed — step back and think big picture
- Viewing screenshots or images — interpret meaning in context

### Template

```xml
<think>Freely describe and reflect on what you know so far, things you tried,
and how that aligns with your objective. You can play through different
scenarios, weigh options, and reason about possible next steps.
The user will not see any of your thoughts here, so you can think freely.</think>
```

## Variant B: Status Updates (Cursor)

Continuous progress narration in conversational style. Visible to the user.

### Rules

- Use correct tenses: "I'll" for future, past tense for past, present for in-progress
- Skip what just happened if no new info since previous update
- Reference todo task names (not IDs); never reprint the full list
- Only pause if truly blocked

### Template

```xml
<status_update_spec>
A brief progress note (1-3 sentences) about what just happened, what you're
about to do, blockers/risks if relevant. Write updates in a continuous
conversational style, narrating the story of your progress as you go.

Critical rule: If you say you're about to do something, actually do it
in the same turn.
</status_update_spec>
```

## Key Principle

Reasoning first, action second. Mandatory think-before-act triggers prevent costly mistakes in irreversible operations. The `<think>` tool is especially powerful because the user cannot see it — the agent reasons freely without performance anxiety.
