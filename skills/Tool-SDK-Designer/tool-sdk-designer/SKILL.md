---
name: tool-sdk-designer
description: Design production-grade tool specifications for AI agents. Use when defining tool interfaces, parameter schemas, safety flags, error handling, MCP compatibility, or tool composition rules. Covers three specification formats (XML, JSON Schema, markdown), 6 quality indicators, safety classification, error recovery patterns, and MCP interoperability. Based on analysis of 40+ tool specs from Cursor, Replit, Devin, Kimi, Windsurf, and the Model Context Protocol standard.
---

# Tool SDK Designer

Design tool specifications that AI agents can use reliably and safely.

## Workflow

### Tool Design Workflow

1. Define the tool's purpose and scope (single responsibility)
2. Select a specification format (XML, JSON Schema, or markdown)
3. Define parameters with types, descriptions, constraints, and defaults
4. Add safety classification (safe, moderate, dangerous)
5. Implement error handling and recovery patterns
6. Document examples with expected inputs and outputs

### Tool Audit Workflow

1. Extract all tool definitions from a system prompt
2. Score each tool against the 6 quality indicators
3. Flag tools without descriptions, types, or error handling
4. Check MCP compatibility if cross-system use is planned
5. Generate improvement recommendations

## Specification Formats

Three formats for defining tools. Read references for templates.

| Format | Best For | Reference |
|--------|---------|-----------|
| XML | Agents using XML response protocol (Replit, Devin) | `references/01-xml-format.md` |
| JSON Schema | OpenAI-style function calling, MCP tools | `references/02-json-schema-format.md` |
| Markdown | Documentation-first agents (Cursor, Windsurf) | `references/03-markdown-format.md` |

## Quality Indicators

Six indicators for a well-specified tool:

| # | Indicator | Description | Weight |
|---|-----------|-------------|--------|
| 1 | Description | Clear purpose statement | 20% |
| 2 | Typed Parameters | Each parameter has a type | 20% |
| 3 | Required Fields | Required vs optional is explicit | 15% |
| 4 | Examples | At least one input/output example | 15% |
| 5 | Error Handling | Failure modes documented | 15% |
| 6 | Safety Flags | Risk level and side effects noted | 15% |

Quality score = sum of weighted indicators (0-100%).

## Tool Design Principles

1. **Single Responsibility** — one tool, one action, no multi-purpose tools
2. **Descriptive Names** — `search_codebase` not `search`, `write_file` not `write`
3. **Typed Everything** — every parameter has a type, every return has a schema
4. **Fail Loudly** — errors include actionable messages, not silent nulls
5. **Idempotent When Possible** — safe to retry without side effects
6. **Document Side Effects** — if a tool modifies state, say so explicitly

## Tool Composition

Read the reference for composition patterns.

| Pattern | Description | Reference |
|---------|------------|-----------|
| Sequential | Output of tool A feeds input of tool B | `references/04-composition.md` |
| Conditional | Tool selection based on runtime conditions | `references/04-composition.md` |
| Parallel | Multiple tools invoked simultaneously | `references/04-composition.md` |
| Fallback | Alternative tool when primary fails | `references/04-composition.md` |

## MCP Compatibility

Read the reference for MCP interop requirements.

| Requirement | Description | Reference |
|-------------|------------|-----------|
| Schema Format | JSON Schema for parameters | `references/05-mcp-interop.md` |
| Transport | stdio, SSE, or HTTP | `references/05-mcp-interop.md` |
| Discovery | List tools endpoint | `references/05-mcp-interop.md` |

## Anti-Patterns

- **God Tool** — one tool that does everything via a "command" parameter
- **Missing Types** — parameters described in prose without formal types
- **Silent Side Effects** — tool modifies state but doesn't declare it
- **No Error Contract** — caller has no way to know what went wrong
- **Prompt-Coupled** — tool only works with one specific system prompt
