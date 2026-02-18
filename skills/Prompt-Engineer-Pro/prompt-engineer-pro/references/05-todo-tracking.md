# Pattern: Todo Tracking (Session-Persistent Task State)

Sources: Claude Code (TodoWrite), Cursor (todo_write), Kimi (todo_read/todo_write)

## When to Use

- Multi-step implementation tasks
- Agent needs to track completion status across turns
- User needs visibility into progress
- Tasks should be reconciled before new edits

## Architecture

A dedicated tool maintains a checklist that persists throughout the session.

```
Goal detected → Create todo list → Execute tasks → Update status → Reconcile
```

## Cursor's Implementation (Most Detailed)

### Todo Creation Rules

- Create atomic items (≤14 words, verb-led, clear outcome)
- Items should take a user ≥5 minutes — meaningful, nontrivial
- Prefer fewer, larger items over granular sub-steps
- Do NOT include operational actions done in service of higher tasks
- If asked to plan but not implement, don't create todos until implementation time

### Todo Content Style

- Simple, clear, short with just enough context
- Verb and action-oriented: "Add LRUCache interface to types.ts"
- Should NOT include specific types, variable names, event names

### Enforcement Rules

```xml
<gating>
Gate before new edits: Before starting any new file or code edit,
reconcile the TODO list via todo_write (merge=true): mark newly completed
tasks as completed and set the next task to in_progress.
</gating>

<cadence>
After each successful step (install, file created, endpoint added,
migration run), immediately update the corresponding TODO item's status.
</cadence>

<non_compliance>
If you fail to check off tasks before claiming them done, self-correct
in the next turn immediately.
If you report code work as done without a successful test/build run,
self-correct next turn by running and fixing first.
</non_compliance>
```

## Template

```xml
<todo_spec>
Use todo_write to track and manage tasks.

Create items before starting implementation:
- Atomic items, ≤14 words, verb-led, clear outcome
- High-level meaningful tasks (≥5 min for a user)
- Do NOT include operational sub-steps

Update flow:
1. Mark completed tasks via todo_write(merge=true)
2. Set next task to in_progress
3. Execute the task
4. Update status immediately after completion
5. Repeat until all tasks done
6. Final: reconcile and close the todo list
</todo_spec>
```

## Key Principle

Todo tracking is not just for organization — it enforces execution discipline. The gate-before-edit pattern prevents the agent from losing track of where it is. The self-correction rules handle the common failure mode of claiming work is done when it isn't.
