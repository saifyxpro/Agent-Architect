# Procedural Memory

Learned workflows, strategies, and step-by-step processes that the agent refines over time.

## Source Pattern

- **Kimi SKILL.md files**: 925-line procedural manuals (DOCX build pipeline, XLSX validation loop)
- **Claude Code TodoWrite**: Task management workflow refined across sessions
- **Workflows (.md files)**: Step-by-step procedures saved for reuse

## What to Store

```
<procedure>
  <name>[Workflow identifier]</name>
  <version>[Semantic version]</version>
  <trigger>[When this procedure should activate]</trigger>
  <steps>
    <step order="1">[Action description]</step>
    <step order="2">[Action description]</step>
    <step order="3" conditional="[CONDITION]">[Conditional action]</step>
  </steps>
  <success_criteria>[How to verify the procedure worked]</success_criteria>
  <failure_recovery>[What to do if a step fails]</failure_recovery>
  <performance>
    <avg_duration>[Historical average]</avg_duration>
    <success_rate>[Historical success rate]</success_rate>
    <last_used>[Timestamp]</last_used>
  </performance>
</procedure>
```

## Refinement Strategy

1. Track success/failure rate per procedure
2. When success rate drops below 80%, flag for review
3. A/B test procedure variants (try alternative steps)
4. Merge successful variants into the canonical version
5. Retire procedures not used in 180 days

## Loading Strategy

- Load procedure on trigger match (just-in-time)
- Preload procedures for predicted task types
- Keep frequently-used procedures in hot cache
- Archive rarely-used procedures to cold storage
