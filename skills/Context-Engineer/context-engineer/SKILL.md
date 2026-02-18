---
name: context-engineer
description: Design agent memory architectures and context window optimization strategies. Use when building persistent memory systems, context budgeting, dynamic context loading, knowledge retrieval, or managing token limits. Covers three-tier memory (episodic, semantic, procedural), context priority frameworks, just-in-time loading patterns, cache invalidation, and provider-agnostic context layers. Based on patterns from Kimi's skill injection, Cursor's scratchpad, BabyAGI's graph memory, and emerging context engineering practices.
---

# Context Engineer

Design memory architectures and context window strategies for AI agents.

## Workflow

### Memory Design Workflow

1. Identify what the agent needs to remember (facts, procedures, episodes)
2. Classify memory into tiers using the three-tier model
3. Select storage backend for each tier
4. Define retrieval strategies and cache invalidation rules
5. Set token budgets per context section

### Context Audit Workflow

1. Measure current context utilization (tokens per section)
2. Identify redundant or stale content
3. Apply the priority framework to rank sections
4. Implement dynamic loading for low-priority knowledge
5. Re-measure and compare

## Three-Tier Memory Model

Read the relevant reference for implementation templates.

| Tier | What It Stores | Lifespan | Reference |
|------|---------------|----------|-----------|
| Episodic | Specific interaction logs and outcomes | Session or cross-session | `references/01-episodic-memory.md` |
| Semantic | General knowledge and learned patterns | Persistent | `references/02-semantic-memory.md` |
| Procedural | Workflows, strategies, and refined processes | Persistent, versioned | `references/03-procedural-memory.md` |

## Context Budgeting

Read the reference for budget allocation templates.

| Section | Priority | Budget | Reference |
|---------|----------|--------|-----------|
| System Identity | Critical | Fixed (5-10%) | `references/04-context-budgeting.md` |
| Active Task Context | Critical | Dynamic (30-50%) | `references/04-context-budgeting.md` |
| Retrieved Knowledge | High | Dynamic (20-30%) | `references/04-context-budgeting.md` |
| Conversation History | Medium | Sliding window (10-20%) | `references/04-context-budgeting.md` |
| Cached Results | Low | Evictable (5-10%) | `references/04-context-budgeting.md` |

## Dynamic Context Loading

Read the reference for loading pattern templates.

| Pattern | Description | Reference |
|---------|------------|-----------|
| Just-In-Time | Load knowledge only when task requires it | `references/05-dynamic-loading.md` |
| Prefetch | Predict and preload likely-needed context | `references/05-dynamic-loading.md` |
| Eviction | Remove low-relevance content when budget exceeded | `references/05-dynamic-loading.md` |

## Context Priority Framework

When context window is full, evict in this order (lowest priority first):

1. **Cached tool outputs** — regenerable on demand
2. **Old conversation turns** — summarize instead of keeping verbatim
3. **Background reference material** — reload from storage if needed
4. **Retrieved examples** — keep only the most relevant
5. **NEVER evict** — system identity, safety rules, active task state

## Provider-Agnostic Context Layer

Separate context from model:

```
<context_layer>
  <identity>[System prompt — model-independent]</identity>
  <knowledge>[Retrieved facts — stored externally]</knowledge>
  <state>[Task progress — persisted to DB/file]</state>
  <history>[Conversation — sliding window]</history>
</context_layer>

<model_layer>
  <provider>[OpenAI | Anthropic | Google | Local]</provider>
  <model>[Specific model name]</model>
  <token_limit>[Context window size]</token_limit>
</model_layer>
```

Switching providers requires ONLY changing the model layer. Context layer stays identical.

## Anti-Patterns

- **Context Stuffing** — cramming everything into the prompt regardless of relevance
- **Stateless Agent** — no memory between sessions, relearns everything
- **Stale Cache** — cached information never expires, becomes incorrect
- **Token Waste** — verbose formatting consuming budget (XML when plain text suffices)
- **Lost in the Middle** — critical information buried in the center of long contexts
