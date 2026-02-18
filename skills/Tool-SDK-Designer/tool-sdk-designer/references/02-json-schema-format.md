# JSON Schema Tool Format

Define tools using JSON Schema for OpenAI-style function calling and MCP.

## Source Pattern

- **OpenAI Function Calling**: JSON Schema for parameter definitions
- **Model Context Protocol**: JSON Schema as the standard tool format
- **Anthropic tool_use**: JSON Schema parameter definitions

## Template

```json
{
  "name": "[tool_name]",
  "description": "[Clear purpose statement — what this tool does and when to use it]",
  "parameters": {
    "type": "object",
    "properties": {
      "[param_1]": {
        "type": "string",
        "description": "[What this parameter controls]",
        "enum": ["option_a", "option_b"]
      },
      "[param_2]": {
        "type": "number",
        "description": "[Description]",
        "minimum": 0,
        "maximum": 100,
        "default": 50
      },
      "[param_3]": {
        "type": "boolean",
        "description": "[Description]",
        "default": false
      },
      "[param_4]": {
        "type": "array",
        "items": { "type": "string" },
        "description": "[Description]",
        "minItems": 1,
        "maxItems": 10
      }
    },
    "required": ["[param_1]"]
  },
  "returns": {
    "type": "object",
    "properties": {
      "result": { "type": "string" },
      "error": { "type": "string" }
    }
  },
  "metadata": {
    "safety": "safe|moderate|dangerous",
    "side_effects": ["file_write", "network_request", "state_mutation"],
    "idempotent": true,
    "timeout_ms": 30000
  }
}
```

## JSON Schema Best Practices

- Use `enum` for parameters with fixed options
- Set `minimum`/`maximum` for numeric ranges
- Mark `required` fields explicitly (don't assume)
- Add `default` values for optional parameters
- Keep `description` under 200 characters
- Use `metadata.safety` for risk classification
- Include `metadata.side_effects` array for state-changing tools
