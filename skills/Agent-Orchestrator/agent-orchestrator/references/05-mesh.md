# Mesh Topology

Peer-to-peer agents collaborate through a shared state layer with no central coordinator.

## Source Pattern

- **Collaborative research agents**: Agents share findings and build on each other's work
- **Graph-based memory engines**: BabyAGI rebuilt with three internal graph layers
- **Distributed systems**: Eventual consistency with conflict-free state merging

## When to Use

- No clear authority hierarchy for the task
- Agents need to dynamically discover and use each other's outputs
- Task requires emergent collaboration patterns
- Resilience matters — no single point of failure

## When NOT to Use

- Clear sequential or hierarchical task structure exists
- State consistency is critical (mesh has eventual consistency)
- Agent count exceeds 10 (coordination overhead explodes)

## Template

```
<orchestration topology="mesh">
  <shared_state>
    <type>graph | key-value | document</type>
    <access>read-write for all agents</access>
    <conflict_resolution>last-write-wins | merge | version-vector</conflict_resolution>
  </shared_state>

  <peer name="[AGENT_1]" expertise="[DOMAIN]">
    <reads_from>[State keys this agent monitors]</reads_from>
    <writes_to>[State keys this agent produces]</writes_to>
    <triggers>
      <on event="[STATE_CHANGE]" action="[RESPONSE]" />
    </triggers>
  </peer>

  <peer name="[AGENT_2]" expertise="[DOMAIN]">
    <reads_from>[State keys]</reads_from>
    <writes_to>[State keys]</writes_to>
    <triggers>
      <on event="[STATE_CHANGE]" action="[RESPONSE]" />
    </triggers>
  </peer>

  <convergence>
    <condition>[When the mesh considers the task complete]</condition>
    <timeout>[Max time before forced termination]</timeout>
    <quorum>[Minimum agents that must agree on completion]</quorum>
  </convergence>
</orchestration>
```

## Mesh Design Principles

- Define state schema upfront — agents must agree on data format
- Use event-driven triggers, not polling
- Set convergence criteria to prevent infinite loops
- Log all state mutations for debugging
- Implement quorum-based completion (not unanimous)
- Keep mesh size under 10 agents to manage complexity
