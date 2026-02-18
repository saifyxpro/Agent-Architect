# Hierarchical Topology

Multi-level delegation with coordinators at each level managing sub-teams of specialists.

## Source Pattern

- **Kimi Agent Swarm**: ~100 agents across 1,500 steps with layered coordination
- **MetaGPT**: Product Manager → Architect → Engineers → QA hierarchy
- **Enterprise systems**: Department heads delegate to team leads to individual workers

## When to Use

- Large-scale tasks requiring 10+ agents
- Natural organizational hierarchy in the domain
- Different levels need different autonomy levels
- Sub-tasks can be managed independently by sub-coordinators

## When NOT to Use

- Fewer than 5 agents (overhead exceeds benefit)
- Flat task structure with no natural grouping
- Real-time latency requirements (hierarchy adds delay)

## Template

```
<orchestration topology="hierarchical">
  <level depth="0" name="executive">
    <coordinator name="lead_agent">
      <responsibilities>
        - Decompose top-level goal into department tasks
        - Allocate resources across departments
        - Resolve cross-department conflicts
        - Report final results
      </responsibilities>
      <delegates_to>level_1_coordinators</delegates_to>
    </coordinator>
  </level>

  <level depth="1" name="department">
    <coordinator name="[DEPT_COORDINATOR]" domain="[DOMAIN]">
      <responsibilities>
        - Break department task into worker assignments
        - Monitor worker progress
        - Escalate blockers to lead agent
      </responsibilities>
      <workers>
        <agent name="[WORKER_1]" specialization="[SPEC]" />
        <agent name="[WORKER_2]" specialization="[SPEC]" />
      </workers>
      <escalation_rules>
        - Escalate if worker fails 2 consecutive attempts
        - Escalate if cross-department dependency detected
        - Escalate if deadline at risk
      </escalation_rules>
    </coordinator>
  </level>
</orchestration>
```

## Hierarchy Design Principles

- Maximum 3 levels deep (executive → department → worker)
- Each coordinator manages at most 7 direct reports (span of control)
- Cross-level communication only through coordinators (no skip-level)
- Escalation paths must be explicit and tested
- Sub-coordinators have full autonomy within their domain boundaries
