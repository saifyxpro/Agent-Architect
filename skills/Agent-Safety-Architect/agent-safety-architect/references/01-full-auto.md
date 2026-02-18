# Full Auto Tier

The agent executes actions without human approval. Reserved for low-risk, reversible operations.

## Source Pattern

- **Kimi Base Chat**: Auto-executes read operations, web searches, code formatting
- **Windsurf Cascade**: Auto-runs linters, formatters, read-only file operations
- **Claude Code**: Auto-approves codebase_search, view_file, list_dir

## Criteria for Full Auto

ALL of these must be true:
- Action is **read-only** (no state mutation)
- Action is **reversible** (can undo if wrong)
- Action scope is **bounded** (within workspace, no external reach)
- Action has **no side effects** (doesn't trigger external services)

## Template

```
<autonomy_tier level="full_auto">
  <allowed_actions>
    - Read file contents
    - Search codebase (text and semantic)
    - List directory contents
    - View file outlines and metadata
    - Run linters and formatters (dry-run)
    - Execute read-only database queries (SELECT only)
    - Analyze code structure
  </allowed_actions>

  <logging level="minimal">
    - Action name and target
    - Success/failure status
    - No parameter details needed (low risk)
  </logging>

  <guardrails>
    - File access limited to workspace directory
    - No network requests
    - No process spawning
    - Time limit: 30 seconds per action
  </guardrails>
</autonomy_tier>
```

## Escalation Trigger

Auto-escalate to Supervised tier if:
- Action would read files outside workspace
- File contains patterns suggesting credentials
- Read operation returns data larger than 1MB
