# Pipeline Topology

Agents process tasks sequentially, each stage transforming input before passing to the next with validation gates between stages.

## Source Pattern

- **Kimi DOCX Skill**: read_file → ipython → shell:build → validate → deliver
- **Kiro Spec-Driven**: requirements → design → tasks → implementation
- **ETL Systems**: extract → transform → validate → load

## When to Use

- Tasks have natural sequential phases
- Each phase produces a distinct artifact
- Quality gates between phases prevent error propagation
- Later stages depend on earlier stage outputs

## When NOT to Use

- Phases can execute independently (use Broadcast instead)
- Iterative refinement needed between non-adjacent stages
- Pipeline latency is unacceptable

## Template

```
<orchestration topology="pipeline">
  <stage order="1" name="[STAGE_NAME]" agent="[AGENT_NAME]">
    <input>[Raw input or previous stage output]</input>
    <output>[Artifact produced]</output>
    <validation>
      <check>[Quality criterion 1]</check>
      <check>[Quality criterion 2]</check>
      <on_failure>retry | escalate | abort</on_failure>
    </validation>
  </stage>

  <stage order="2" name="[STAGE_NAME]" agent="[AGENT_NAME]">
    <input>[Stage 1 output]</input>
    <output>[Transformed artifact]</output>
    <validation>
      <check>[Quality criterion]</check>
      <on_failure>retry | escalate | abort</on_failure>
    </validation>
  </stage>

  <stage order="3" name="[STAGE_NAME]" agent="[AGENT_NAME]">
    <input>[Stage 2 output]</input>
    <output>[Final deliverable]</output>
    <validation>
      <check>[Final quality gate]</check>
      <on_failure>retry_from_stage_2 | escalate</on_failure>
    </validation>
  </stage>
</orchestration>
```

## Gate Design Principles

- Every stage MUST have at least one validation check
- Gates should be automated (script-based) not LLM-judged when possible
- Failed gates should specify retry scope (same stage vs earlier stage)
- Pipeline should support resumption from any stage (checkpoint pattern)
- Log stage transitions with timing data for bottleneck detection
