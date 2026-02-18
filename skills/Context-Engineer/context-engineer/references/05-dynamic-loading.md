# Dynamic Context Loading

Load, prefetch, and evict context at runtime based on task needs.

## Source Pattern

- **Kimi Just-in-Time**: `read_file(SKILL.md)` only when task requires that skill
- **Kimi Route Selection**: PDF skill loads HTML sub-instructions OR LaTeX, never both
- **Dynamic Error Recovery**: Load troubleshooting docs only when compilation fails

## Three Loading Patterns

### 1. Just-In-Time (Reactive)

Load context when a trigger condition is met.

```
<loading_rule name="[RULE_NAME]">
  <trigger>[Condition that activates loading]</trigger>
  <source>[Where to load from — file, DB, API]</source>
  <target>[Context section to place content in]</target>
  <evicts>[What gets removed to make room]</evicts>
  <ttl>[How long to keep loaded — turns, minutes, task completion]</ttl>
</loading_rule>
```

Use when: Trigger is detectable, loading latency is acceptable.

### 2. Prefetch (Predictive)

Predict what context will be needed and load proactively.

```
<prefetch_rule name="[RULE_NAME]">
  <prediction>[How to predict need — task classification, user history]</prediction>
  <source>[Where to load from]</source>
  <confidence_threshold>[Minimum prediction confidence to prefetch]</confidence_threshold>
  <preempt>[If wrong prediction, evict immediately]</preempt>
</prefetch_rule>
```

Use when: Prediction accuracy > 70%, latency sensitivity is high.

### 3. Eviction (Cleanup)

Remove context that is no longer relevant.

```
<eviction_rule name="[RULE_NAME]">
  <trigger>[When to check for eviction — budget exceeded, task change]</trigger>
  <strategy>
    LRU (least recently used) |
    LFU (least frequently used) |
    TTL (expired time-to-live) |
    Relevance (lowest similarity to current task)
  </strategy>
  <protected>[Sections that CANNOT be evicted]</protected>
</eviction_rule>
```

Use when: Context budget is tight, stale content is accumulating.

## Implementation Principles

- Load knowledge BEFORE the agent starts reasoning (not mid-stream)
- Evict AFTER task completion, not during active processing
- Log all load/evict events for debugging
- Measure hit rates — if JIT loading triggers on >80% of tasks, prefetch instead
- Never load both branches of a conditional path (Kimi PDF pattern)
