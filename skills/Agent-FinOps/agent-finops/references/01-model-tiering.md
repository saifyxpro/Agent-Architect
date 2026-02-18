# Model Tiering

Assign different model classes to different task complexities to reduce cost without sacrificing quality.

## Source Pattern

- **Plan-and-Execute trend**: Frontier models plan, cheap models execute
- **Heterogeneous Model Architecture**: Mix model sizes based on task needs
- **Kimi's model routing**: K2.5 Instant (fast/cheap) vs K2.5 Thinking (slow/better)

## Three-Tier Model

```
┌──────────────────────────────────────────────────────────────┐
│                    FRONTIER TIER                              │
│  Models: GPT-4o, Claude Opus, Gemini Ultra                   │
│  Cost: $$$  │  Speed: Slow  │  Quality: Highest              │
│  Use for:                                                     │
│    - Complex multi-step reasoning                             │
│    - Orchestration and planning                               │
│    - Novel problem solving                                    │
│    - System prompt generation                                 │
│  Frequency: 5-10% of total calls                             │
├──────────────────────────────────────────────────────────────┤
│                    MID TIER                                    │
│  Models: GPT-4o-mini, Claude Sonnet, Gemini Pro              │
│  Cost: $$  │  Speed: Medium  │  Quality: Good                │
│  Use for:                                                     │
│    - Standard code generation                                 │
│    - Document analysis and summarization                      │
│    - Quality verification and review                          │
│    - Moderate complexity reasoning                            │
│  Frequency: 20-30% of total calls                            │
├──────────────────────────────────────────────────────────────┤
│                    ECONOMY TIER                               │
│  Models: GPT-3.5, Claude Haiku, Gemini Flash                 │
│  Cost: $  │  Speed: Fast  │  Quality: Adequate               │
│  Use for:                                                     │
│    - Template filling and formatting                          │
│    - Intent classification and routing                        │
│    - Data extraction and parsing                              │
│    - Simple Q&A and lookups                                   │
│  Frequency: 60-75% of total calls                            │
└──────────────────────────────────────────────────────────────┘
```

## Router Template

```
<model_router>
  <rule condition="task requires multi-step reasoning" tier="frontier" />
  <rule condition="task requires code generation" tier="mid" />
  <rule condition="task is classification or extraction" tier="economy" />
  <rule condition="task is formatting or template fill" tier="economy" />
  <rule condition="task confidence < 70%" tier="upgrade_one_tier" />
  <default tier="mid" />
</model_router>
```

## Cost Comparison (per 1M tokens, approximate 2025 pricing)

| Tier | Input | Output | Relative Cost |
|------|-------|--------|---------------|
| Frontier | $5-15 | $15-75 | 1x (baseline) |
| Mid | $0.15-3 | $0.60-15 | 0.1x |
| Economy | $0.01-0.25 | $0.04-1.25 | 0.01x |
