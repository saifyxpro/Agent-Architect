# Cost Monitoring

Track, alert, and optimize agent costs in production.

## Core Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Cost per Interaction | total_cost / total_interactions | < $0.50 |
| Token Efficiency | useful_output_tokens / total_tokens | > 40% |
| Cache Hit Rate | cached_responses / total_requests | > 50% |
| Model Tier Distribution | requests_per_tier / total_requests | Economy > 60% |
| Error Cost Waste | tokens_on_failed_requests / total_tokens | < 10% |

## Dashboard Template

```
┌─────────────────────────────────────────────────────────┐
│  Agent Cost Dashboard — Last 24 Hours                    │
├─────────────────────────────────────────────────────────┤
│  Total Spend:        $XX.XX                              │
│  Total Interactions: X,XXX                               │
│  Avg Cost/Interact:  $X.XX                               │
│                                                          │
│  Model Distribution:                                     │
│    Frontier: XX% ($XX.XX)                                │
│    Mid-Tier: XX% ($XX.XX)                                │
│    Economy:  XX% ($XX.XX)                                │
│                                                          │
│  Cache Hit Rate:     XX%                                 │
│  Token Efficiency:   XX%                                 │
│  Error Waste:        XX%                                 │
│                                                          │
│  Top 5 Expensive Operations:                             │
│    1. [Operation] — $XX.XX (XX calls)                    │
│    2. [Operation] — $XX.XX (XX calls)                    │
│    3. [Operation] — $XX.XX (XX calls)                    │
│    4. [Operation] — $XX.XX (XX calls)                    │
│    5. [Operation] — $XX.XX (XX calls)                    │
├─────────────────────────────────────────────────────────┤
│  Alerts:                                                 │
│    ⚠ Budget threshold 80% reached                        │
│    ⚠ Cache hit rate below target                         │
│    ✅ Token efficiency above target                      │
└─────────────────────────────────────────────────────────┘
```

## Alert Rules

```
<alerts>
  <alert name="budget_warning" condition="daily_spend > budget * 0.8">
    Notify when 80% of daily budget consumed.
  </alert>

  <alert name="cost_spike" condition="hourly_spend > avg_hourly * 3">
    Notify on 3x cost spike (potential runaway agent).
  </alert>

  <alert name="low_efficiency" condition="token_efficiency < 0.3">
    Notify when less than 30% of tokens produce useful output.
  </alert>

  <alert name="cache_miss" condition="cache_hit_rate < 0.4">
    Notify when cache effectiveness drops below 40%.
  </alert>

  <alert name="tier_imbalance" condition="frontier_percentage > 0.3">
    Notify when frontier model usage exceeds 30% of requests.
  </alert>
</alerts>
```

## Optimization Cadence

- **Daily**: Review dashboard, check alerts
- **Weekly**: Analyze top expensive operations, identify downgrade candidates
- **Monthly**: Review model tier distribution, update routing rules
- **Quarterly**: Benchmark against new model pricing, evaluate model upgrades
