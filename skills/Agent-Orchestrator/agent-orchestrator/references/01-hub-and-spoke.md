# Hub-and-Spoke Topology

A single coordinator agent receives all requests, delegates to specialist workers, and aggregates results.

## Source Pattern

- **Kimi Agent Swarm**: Lead agent orchestrates ~100 specialized agents
- **BabyAGI**: Task creation agent + execution agent + prioritization agent
- **Customer service systems**: Triage → specialist routing

## When to Use

- One clear entry point for all requests
- Specialists have non-overlapping domains
- Results need unified formatting before delivery
- Task routing decisions are straightforward

## When NOT to Use

- Specialists need to communicate with each other directly
- Coordinator becomes a bottleneck (>50 concurrent tasks)
- Task decomposition requires iterative refinement

## Template

```
<orchestration topology="hub-and-spoke">
  <coordinator name="[NAME]">
    <responsibilities>
      - Receive and classify incoming requests
      - Select appropriate specialist agent(s)
      - Provide task context and constraints
      - Aggregate specialist outputs
      - Handle failures and retries
    </responsibilities>
    <routing_rules>
      <route condition="[CONDITION_1]" to="specialist_a" />
      <route condition="[CONDITION_2]" to="specialist_b" />
      <route condition="ambiguous" to="clarification_flow" />
      <route condition="out_of_scope" to="escalation" />
    </routing_rules>
  </coordinator>

  <specialist name="specialist_a" domain="[DOMAIN]">
    <input>[What it receives from coordinator]</input>
    <output>[What it returns to coordinator]</output>
    <timeout>[Max execution time]</timeout>
    <fallback>[What happens on failure]</fallback>
  </specialist>

  <specialist name="specialist_b" domain="[DOMAIN]">
    <input>[What it receives from coordinator]</input>
    <output>[What it returns to coordinator]</output>
    <timeout>[Max execution time]</timeout>
    <fallback>[What happens on failure]</fallback>
  </specialist>
</orchestration>
```

## Coordinator Design Principles

- Route based on intent classification, not keyword matching
- Include full task context in every delegation (no back-and-forth)
- Set timeouts for every specialist call
- Always have a fallback agent for unclassified requests
- Log every routing decision for observability
