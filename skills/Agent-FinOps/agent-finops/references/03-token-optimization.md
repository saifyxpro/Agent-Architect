# Token Optimization

Strategies to reduce token consumption without reducing output quality.

## Strategy 1: Response Caching (40-80% savings)

Cache responses for identical or near-identical requests.

```
<cache_strategy>
  <exact_match>
    Cache key: hash(tool_name + parameters)
    TTL: 5 minutes for volatile data, 24 hours for stable data
    Hit rate target: > 60%
  </exact_match>

  <semantic_match>
    Cache key: embedding similarity > 0.95
    Use for: FAQ responses, documentation lookups
    Caution: May return stale answers if source changes
  </semantic_match>

  <never_cache>
    - User-specific queries with personal data
    - Time-sensitive information (stock prices, weather)
    - Creative/generative tasks (want diversity)
  </never_cache>
</cache_strategy>
```

## Strategy 2: Structured Outputs (20-40% savings)

Constrain output format to eliminate verbose prose.

| Format | Token Cost | Use When |
|--------|-----------|----------|
| Free-form text | 100% (baseline) | Creative writing, explanations |
| JSON | 60-80% | Data extraction, API responses |
| Enum/classification | 5-10% | Routing, categorization |
| Boolean | 1% | Yes/no decisions |

Force structured outputs with:
- JSON mode in API calls
- Schema-constrained generation
- Enum-only response fields

## Strategy 3: Context Compression (30-50% savings)

Reduce tokens in conversation history.

- Summarize turns older than 5 messages (keep last 5 verbatim)
- Remove system prompt boilerplate from follow-up calls
- Compress tool outputs to essential data (drop formatting)
- Use abbreviations in internal agent communication

## Strategy 4: Batch Processing (10-30% savings)

Group similar requests into single calls.

- Combine 5 file reads into one multi-file read
- Batch similar classification tasks into one prompt
- Aggregate search results before analysis (one analysis call, not N)
