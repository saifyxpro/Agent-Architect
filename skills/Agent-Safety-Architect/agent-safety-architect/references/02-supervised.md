# Supervised Tier

The agent proposes actions and executes only after human approval. For moderate-risk operations with recoverable consequences.

## Source Pattern

- **Claude Code**: Displays exact command + purpose, waits for approval
- **Devin**: Plans visible in sidebar, user approves before execution
- **Antigravity SafeToAutoRun**: Commands default to requiring approval

## Criteria for Supervised

ANY of these is true:
- Action **mutates state** (writes files, modifies DB)
- Action **installs software** (npm install, pip install)
- Action accesses **external services** (APIs, webhooks)
- Action **creates resources** (branches, PRs, deployments)

## Template

```
<autonomy_tier level="supervised">
  <approval_flow>
    1. Agent prepares the action
    2. Agent displays to user:
       - Exact action (command, file path, parameters)
       - One-sentence purpose
       - Risk assessment
    3. User reviews and chooses: Approve | Modify | Reject
    4. On approve → execute and log
    5. On modify → agent adjusts and re-presents
    6. On reject → agent skips and suggests alternative
  </approval_flow>

  <display_format>
    Command: [exact command or action]
    Purpose: [one sentence]
    Risk: [what could go wrong]
    Reversible: [yes/no — how to undo]
  </display_format>

  <logging level="detailed">
    - Full action parameters
    - User decision (approve/modify/reject)
    - Execution result
    - State changes caused
  </logging>

  <first_time_approval>
    For repetitive actions in the same session, ask once.
    After first approval, same action type auto-approved for session.
  </first_time_approval>
</autonomy_tier>
```

## Escalation Trigger

Escalate to Human-Led tier if:
- Action would affect production environment
- Action involves financial transactions
- Action modifies security configurations
- User explicitly requests manual control
