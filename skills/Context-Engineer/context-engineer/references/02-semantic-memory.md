# Semantic Memory

General knowledge and patterns extracted from multiple episodes. The agent's accumulated understanding of domains, tools, and user preferences.

## Source Pattern

- **Knowledge Items (KI)**: Distilled knowledge on specific topics, updated over conversations
- **Kimi Skill Files**: 925-line domain manuals loaded at runtime
- **Graph-based knowledge engines**: BabyAGI's three-layer knowledge graph

## What to Store

```
<knowledge_item>
  <topic>[Domain or concept]</topic>
  <facts>
    <fact confidence="high|medium|low">[Factual statement]</fact>
  </facts>
  <patterns>
    <pattern frequency="[occurrences]">[Observed behavior or rule]</pattern>
  </patterns>
  <source_episodes>[List of episode IDs this was derived from]</source_episodes>
  <last_validated>[Timestamp of last verification]</last_validated>
</knowledge_item>
```

## Storage Backend Options

| Backend | Best For | Trade-offs |
|---------|---------|------------|
| Vector DB | Semantic similarity search | Fuzzy, non-deterministic results |
| Knowledge Graph | Relational queries, reasoning | Complex setup, schema required |
| Key-Value Store | Fast exact lookups | No similarity search |
| Document Store | Structured domain knowledge | Manual organization needed |

## Maintenance Rules

- Re-validate knowledge items when source domain changes
- Merge duplicate items with confidence weighting
- Flag items not accessed in 90 days for review
- Version knowledge items — track what changed and when
