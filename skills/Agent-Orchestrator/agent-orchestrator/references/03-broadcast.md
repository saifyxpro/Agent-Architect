# Broadcast Topology

Multiple agents process the same input in parallel, with results aggregated by a collector.

## Source Pattern

- **Multi-perspective review**: Multiple reviewer agents evaluate same code/document
- **DyLAN architecture**: Dynamic evaluation of which agents contribute meaningfully
- **Ensemble methods**: Multiple models produce outputs, best is selected

## When to Use

- Same input needs multiple independent perspectives
- Agents have overlapping but different expertise
- Speed matters and tasks can execute in parallel
- Quality improves with diverse viewpoints

## When NOT to Use

- Agents would produce identical outputs (wasteful)
- Sequential dependency between agent outputs
- Resource constraints prevent parallel execution

## Template

```
<orchestration topology="broadcast">
  <dispatcher>
    <input>[Task to broadcast]</input>
    <recipients>
      <agent name="[AGENT_1]" perspective="[LENS_1]" />
      <agent name="[AGENT_2]" perspective="[LENS_2]" />
      <agent name="[AGENT_3]" perspective="[LENS_3]" />
    </recipients>
    <timeout>[Max wait for all responses]</timeout>
    <min_responses>[Minimum needed to proceed]</min_responses>
  </dispatcher>

  <aggregator strategy="[voting|ranking|synthesis|best-of]">
    <voting>Majority wins, ties broken by authority ranking</voting>
    <ranking>Score each response on criteria, select highest</ranking>
    <synthesis>Merge non-conflicting parts from all responses</synthesis>
    <best_of>Select single best response by quality metric</best_of>
  </aggregator>

  <dynamic_evaluation enabled="true">
    <description>
      After each round, evaluate agent contribution quality.
      Exclude low-value agents from future broadcasts (DyLAN pattern).
    </description>
    <threshold>[Minimum contribution score to remain active]</threshold>
  </dynamic_evaluation>
</orchestration>
```

## Aggregation Principles

- Define aggregation strategy BEFORE broadcasting
- Set timeouts — proceed with partial results if needed
- Track per-agent response quality over time
- Dynamically prune low-contributing agents (DyLAN)
- Weight responses by agent expertise domain relevance
