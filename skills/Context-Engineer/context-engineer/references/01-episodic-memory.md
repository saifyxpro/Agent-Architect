# Episodic Memory

Records of specific agent interactions, tool calls, and their outcomes. Used for learning from past experiences.

## Source Pattern

- **Kimi `.store/` directory**: Append-only audit logs of every action taken
- **Claude Code conversation logs**: Session transcripts with decision reasoning
- **Cursor recent changes**: Tracking what was modified and why

## What to Store

```
<episode>
  <timestamp>[ISO 8601]</timestamp>
  <task_type>[Classification of the task]</task_type>
  <actions_taken>
    <action tool="[TOOL]" input="[SUMMARY]" output="[RESULT]" success="true|false" />
  </actions_taken>
  <outcome>[Final result — success/failure/partial]</outcome>
  <lessons>[What could be improved next time]</lessons>
  <duration>[Time taken]</duration>
</episode>
```

## Retrieval Strategy

- Index episodes by task_type for quick filtering
- Retrieve top-3 most similar episodes when starting a new task
- Weight recent episodes higher (temporal decay)
- Retrieve failure episodes specifically when current task is struggling

## Retention Policy

- Keep last 100 episodes in hot storage (fast retrieval)
- Summarize older episodes into semantic memory
- Delete raw episodes after 30 days (keep summaries)
- Always retain failure episodes (learning signal)
