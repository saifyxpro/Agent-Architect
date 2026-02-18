# Tool Composition Patterns

Combine multiple tools into workflows, chains, and fallback structures.

## Source Pattern

- **Kimi Execution Flows**: read_file → ipython → shell:build → validate → deliver
- **Devin Tool Chains**: browser_action → shell → create_file → browser verify
- **Cursor Multi-tool**: search → view → edit → verify

## Pattern 1: Sequential Chain

Output of tool A feeds input of tool B.

```
<chain name="[WORKFLOW_NAME]">
  <step order="1" tool="[TOOL_A]">
    <input>[Parameters]</input>
    <output_key>[Variable name to store result]</output_key>
  </step>
  <step order="2" tool="[TOOL_B]">
    <input>{{step_1.output_key}}</input>
    <output_key>[Next variable]</output_key>
  </step>
  <step order="3" tool="[TOOL_C]">
    <input>{{step_2.output_key}}</input>
  </step>
</chain>
```

## Pattern 2: Conditional Branch

Tool selection based on runtime conditions.

```
<conditional>
  <condition test="[EXPRESSION]">
    <then tool="[TOOL_A]" />
  </condition>
  <condition test="[EXPRESSION]">
    <then tool="[TOOL_B]" />
  </condition>
  <otherwise tool="[FALLBACK_TOOL]" />
</conditional>
```

## Pattern 3: Parallel Execution

Multiple tools invoked simultaneously when independent.

```
<parallel>
  <invoke tool="[TOOL_A]" input="[PARAMS]" />
  <invoke tool="[TOOL_B]" input="[PARAMS]" />
  <invoke tool="[TOOL_C]" input="[PARAMS]" />
  <join strategy="all|any|first">[How to combine results]</join>
</parallel>
```

## Pattern 4: Fallback Chain

Try primary tool, fall back to alternatives on failure.

```
<fallback name="[FALLBACK_NAME]">
  <try tool="[PRIMARY]" />
  <catch error="[ERROR_TYPE]">
    <try tool="[SECONDARY]" />
  </catch>
  <catch error="any">
    <try tool="[LAST_RESORT]" />
  </catch>
</fallback>
```

## Composition Rules

- Never chain more than 5 tools without a validation gate
- Parallel tools MUST be independent (no shared state)
- Fallback chains MUST have a terminal catch-all
- Log each step transition for debugging
- Set per-step timeouts, not just chain-level timeouts
