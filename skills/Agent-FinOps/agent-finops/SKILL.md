---
name: agent-finops
description: Design cost-efficient AI agent architectures. Use when optimizing token usage, selecting model tiers, budgeting compute costs, implementing caching strategies, or designing plan-and-execute patterns for cost reduction. Covers model tiering (frontier for planning, cheap for execution), token budgeting, response caching, the plan-and-execute cost reduction pattern (up to 90% savings), and cost monitoring. Based on emerging FinOps-for-AI trends, heterogeneous model architectures, and production cost optimization practices.
---

# Agent FinOps

Design cost-efficient AI agent architectures with model tiering, token budgeting, and caching.

## Workflow

### Cost Optimization Workflow

1. Audit current token usage per agent component
2. Classify tasks by complexity (planning vs execution)
3. Assign model tiers to each task class
4. Implement caching for repeated queries
5. Set up cost monitoring and alerts

### Cost Audit Workflow

1. Measure tokens consumed per agent interaction
2. Identify the most expensive operations
3. Check for cacheable or downgradable operations
4. Calculate potential savings from model tiering
5. Generate cost reduction recommendations

## Model Tiering

Three model tiers for different task complexities. Read references for templates.

| Tier | Model Class | Use For | Reference |
|------|-----------|---------|-----------|
| Frontier | GPT-4o, Claude Opus, Gemini Ultra | Complex reasoning, planning, orchestration | `references/01-model-tiering.md` |
| Mid-Tier | GPT-4o-mini, Claude Sonnet, Gemini Pro | Standard tasks, code generation | `references/01-model-tiering.md` |
| Economy | GPT-3.5, Claude Haiku, Gemini Flash | High-frequency, simple execution | `references/01-model-tiering.md` |

## Plan-and-Execute Pattern

Read the reference for the cost reduction architecture.

| Component | Description | Reference |
|-----------|------------|-----------|
| Planner | Frontier model creates strategy (high cost, low frequency) | `references/02-plan-and-execute.md` |
| Executor | Economy model follows plan (low cost, high frequency) | `references/02-plan-and-execute.md` |
| Verifier | Mid-tier model checks results (medium cost, as needed) | `references/02-plan-and-execute.md` |

## Token Optimization

Read the reference for token reduction strategies.

| Strategy | Savings | Reference |
|----------|---------|-----------|
| Response Caching | 40-80% for repeated queries | `references/03-token-optimization.md` |
| Structured Outputs | 20-40% vs free-form text | `references/03-token-optimization.md` |
| Context Compression | 30-50% on conversation history | `references/03-token-optimization.md` |
| Batch Processing | 10-30% on similar requests | `references/03-token-optimization.md` |

## Cost Monitoring

Read the reference for monitoring and alerting setup.

| Metric | Description | Reference |
|--------|------------|-----------|
| Cost per Interaction | Average spend per user session | `references/04-cost-monitoring.md` |
| Token Efficiency | Useful output tokens / total tokens | `references/04-cost-monitoring.md` |
| Cache Hit Rate | Percentage of requests served from cache | `references/04-cost-monitoring.md` |
| Model Tier Distribution | Percentage of requests per tier | `references/04-cost-monitoring.md` |

## Anti-Patterns

- **Frontier Everything** — using the most expensive model for all tasks
- **No Caching** — regenerating identical responses repeatedly
- **Token Bloat** — verbose system prompts consuming budget on every call
- **Invisible Costs** — no monitoring, no budget alerts, surprise bills
- **Premature Optimization** — optimizing cost before validating quality

## Validation Scripts

Estimate agent operational costs with automated scoring (0-10):

```bash
python3 scripts/estimate_cost.py <prompt_file> [--strict]
```

Detects model references across 12 LLMs, calculates per-call and monthly costs (1K/10K calls), checks for tiering/caching/budget strategies, and flags cost anti-patterns (premium models for all requests, full history inclusion, disabled caching).
