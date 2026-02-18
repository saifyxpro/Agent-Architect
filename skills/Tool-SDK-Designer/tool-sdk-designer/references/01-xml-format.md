# XML Tool Format

Define tools using XML tags for agents that use XML response protocols.

## Source Pattern

- **Replit**: `<create_file>`, `<edit_file>`, `<shell>` action tags
- **Devin**: `<shell>`, `<create_file>`, `<browser_action>` XML actions
- **Windsurf**: XML-structured tool invocations

## Template

```xml
<tool name="[TOOL_NAME]" safety="safe|moderate|dangerous">
  <description>[Clear, one-line purpose statement]</description>

  <parameters>
    <param name="[PARAM_1]" type="string|number|boolean|array|object" required="true">
      <description>[What this parameter controls]</description>
      <constraints>[Validation rules: min/max, pattern, enum values]</constraints>
      <default>[Default value if optional]</default>
    </param>
    <param name="[PARAM_2]" type="string" required="false">
      <description>[Description]</description>
      <default>[Default]</default>
    </param>
  </parameters>

  <returns type="string|object">
    <description>[What the tool returns on success]</description>
    <error>[What the tool returns on failure]</error>
  </returns>

  <side_effects>
    <effect>[State change 1: e.g., "Creates a new file on disk"]</effect>
    <effect>[State change 2: e.g., "Triggers a webhook"]</effect>
  </side_effects>

  <examples>
    <example>
      <input>[Example invocation]</input>
      <output>[Expected output]</output>
    </example>
  </examples>
</tool>
```

## XML Design Rules

- Use self-closing tags for empty values: `<default />`
- Nest parameters logically (group related params)
- Keep descriptions under 100 characters
- Include at least one example per tool
- Safety attribute is REQUIRED on every tool tag
