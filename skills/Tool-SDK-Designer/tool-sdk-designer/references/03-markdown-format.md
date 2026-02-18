# Markdown Tool Format

Define tools using structured markdown for documentation-first agents.

## Source Pattern

- **Cursor**: Tool descriptions in markdown within system prompts
- **Windsurf Cascade**: Markdown-documented tool capabilities
- **Claude Code**: Markdown tool descriptions with usage guidelines

## Template

```markdown
## [tool_name]

[One paragraph purpose statement — what, when, why]

### Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| [param_1] | string | Yes | — | [Description] |
| [param_2] | number | No | 50 | [Description] |
| [param_3] | boolean | No | false | [Description] |

### Safety

- **Risk Level**: safe | moderate | dangerous
- **Side Effects**: [List state changes]
- **Reversible**: yes | no
- **Approval Required**: never | first-time | always

### Error Handling

| Error Condition | Behavior |
|----------------|----------|
| [Invalid input] | Returns error message with expected format |
| [Resource not found] | Returns null with descriptive error |
| [Permission denied] | Escalates to user with explanation |

### Examples

**Basic usage:**
[tool_name](param_1="value", param_2=42)
→ Returns: [expected output]

**Error case:**
[tool_name](param_1="invalid")
→ Error: [expected error message]
```

## Markdown Format Best Practices

- Use tables for parameters (scannable by both LLMs and humans)
- Include both success and error examples
- Document the exact error message format
- Keep examples realistic with actual values
- Use the Safety section consistently across all tools
