# Human-Led Tier

The agent provides recommendations only. Humans make all decisions and execute actions. For high-stakes, irreversible operations.

## Source Pattern

- **Compliance systems**: Agent recommends, compliance officer decides
- **Production deployments**: Agent prepares, SRE approves and executes
- **Financial operations**: Agent analyzes, human authorizes transactions

## Criteria for Human-Led

ANY of these is true:
- Action is **irreversible** (data deletion, production deploy)
- Action involves **financial transactions**
- Action modifies **security or access controls**
- Action affects **user-facing production systems**
- Regulatory compliance requires **human accountability**

## Template

```
<autonomy_tier level="human_led">
  <agent_role>
    - Analyze the situation
    - Present findings with evidence
    - Recommend specific actions with rationale
    - Provide step-by-step instructions for human execution
    - NEVER execute the action itself
  </agent_role>

  <recommendation_format>
    Analysis: [What the agent found]
    Recommendation: [Specific action to take]
    Rationale: [Why this action, with evidence]
    Alternatives: [Other options with trade-offs]
    Risk: [What could go wrong, impact severity]
    Steps: [Exact steps for human to execute]
    Verification: [How to confirm the action worked]
  </recommendation_format>

  <logging level="comprehensive">
    - Full analysis and reasoning
    - Recommendation presented
    - Human decision (followed/modified/rejected)
    - Outcome after human action
    - Post-action verification results
  </logging>
</autonomy_tier>
```

## Boundary Rules

- Agent MUST NOT include executable commands that auto-run
- Agent MUST present alternatives, not just one option
- Agent MUST include rollback instructions
- Agent MUST flag if recommendation confidence is low
