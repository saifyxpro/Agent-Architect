# MCP Interoperability

Design tools compatible with the Model Context Protocol standard for cross-system use.

## Source Pattern

- **Model Context Protocol (MCP)**: Open standard for AI tool interfaces
- **Google A2A Protocol**: Agent-to-Agent communication standard
- **Anthropic Claude MCP**: Reference implementation of MCP servers

## MCP Tool Requirements

A tool is MCP-compatible when it satisfies:

```json
{
  "name": "[unique_tool_name]",
  "description": "[Purpose — clear enough for any LLM to use]",
  "inputSchema": {
    "type": "object",
    "properties": {
      "[param]": {
        "type": "[JSON Schema type]",
        "description": "[Clear description]"
      }
    },
    "required": ["[required_params]"]
  }
}
```

## MCP Server Structure

An MCP server exposes tools through a standard transport:

```
MCP Server
├── Transport (stdio | SSE | HTTP)
├── Tool Registry
│   ├── list_tools() → Returns all available tools
│   ├── call_tool(name, args) → Executes a tool
│   └── Tool schemas (JSON Schema)
├── Resource Registry (optional)
│   ├── list_resources() → Available data sources
│   └── read_resource(uri) → Read a resource
└── Prompt Registry (optional)
    ├── list_prompts() → Available prompt templates
    └── get_prompt(name) → Render a prompt
```

## Converting Existing Tools to MCP

| From | To MCP | Key Changes |
|------|--------|-------------|
| XML Tags | JSON Schema inputSchema | Convert `<param>` to `properties` |
| Markdown Tables | JSON Schema properties | Convert table rows to typed properties |
| Python Functions | JSON Schema + callable | Extract type hints → schema |
| Custom REST APIs | MCP HTTP transport | Wrap endpoints in MCP call_tool |

## Conversion Template

From a Python function:

```python
def search_files(query: str, path: str, max_results: int = 10) -> list[str]: ...
```

To MCP tool:

```json
{
  "name": "search_files",
  "description": "Search for files matching a query pattern within a directory",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": { "type": "string", "description": "Search pattern" },
      "path": { "type": "string", "description": "Directory to search" },
      "max_results": { "type": "number", "default": 10, "description": "Max results" }
    },
    "required": ["query", "path"]
  }
}
```

## Interop Best Practices

- Use JSON Schema for ALL parameter definitions
- Tool names must be unique across the server
- Descriptions must be self-contained (no referring to system prompt)
- Include transport-layer error codes (not just tool-level errors)
- Test with multiple LLM providers to verify schema compatibility
