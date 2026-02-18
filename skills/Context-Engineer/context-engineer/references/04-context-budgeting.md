# Context Budgeting

Allocate tokens across context sections to maximize agent effectiveness within window limits.

## Source Pattern

- **Kimi's context stack**: Identity at bottom, skill at top, conversation in middle
- **Cursor's system prompt**: ~15K tokens with structured sections and priorities
- **Lost-in-the-Middle research**: Critical info at start and end, not middle

## Budget Allocation Template

```
Total context window: [MODEL_LIMIT] tokens

┌─────────────────────────────────────┐
│ System Identity         │  5-10%    │ ← FIXED, never evicted
│ Safety & Boundaries     │  3-5%     │ ← FIXED, never evicted
├─────────────────────────────────────┤
│ Active Task State       │ 30-50%    │ ← DYNAMIC, current work
│  - Task description     │           │
│  - Intermediate results │           │
│  - Tool outputs         │           │
├─────────────────────────────────────┤
│ Retrieved Knowledge     │ 20-30%    │ ← DYNAMIC, from memory
│  - Relevant skills      │           │
│  - Domain facts         │           │
│  - Similar examples     │           │
├─────────────────────────────────────┤
│ Conversation History    │ 10-20%    │ ← SLIDING WINDOW
│  - Recent turns (full)  │           │
│  - Older turns (summary)│           │
├─────────────────────────────────────┤
│ Cached Results          │  5-10%    │ ← EVICTABLE first
│  - Previous tool outputs│           │
│  - Computed values      │           │
└─────────────────────────────────────┘
```

## Model-Specific Budgets

| Model | Window | Identity | Task | Knowledge | History | Cache |
|-------|--------|----------|------|-----------|---------|-------|
| 8K   | 8,192  | 800  | 3,200 | 2,000 | 1,400 | 792  |
| 32K  | 32,768 | 1,600 | 13,000 | 8,000 | 6,000 | 4,168 |
| 128K | 131,072 | 3,000 | 52,000 | 32,000 | 26,000 | 18,072 |
| 200K | 204,800 | 3,000 | 80,000 | 50,000 | 40,000 | 31,800 |

## Eviction Rules

When context exceeds 90% capacity:

1. Evict cached tool outputs (oldest first)
2. Summarize conversation turns older than 5 messages
3. Remove lowest-relevance retrieved knowledge
4. Compress examples (keep template, remove duplicates)
5. NEVER evict identity, safety rules, or active task state

## Position Optimization

Place critical information at:
- **Start** of context (highest attention)
- **End** of context (recency bias)
- **NOT** in the middle (lowest attention — "Lost in the Middle")
