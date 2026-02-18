# Pattern: XML-Tagged Response Protocol

Sources: Replit, Devin, Kiro, Traycer, Windsurf

## When to Use

- Agent output must be machine-parseable
- Multiple action types need disambiguation
- System needs to route agent responses to different handlers
- Structured metadata (file paths, safety flags) accompanies actions

## Variant A: Structured Action Proposals (Replit)

Six distinct action types, each with specific XML tags and attributes:

```xml
<!-- File edit (substring replacement) -->
<proposed_file_replace_substring file_path="src/app.tsx"
  change_summary="Update button color to primary">
  <old_str>className="bg-gray-500"</old_str>
  <new_str>className="bg-blue-600"</new_str>
</proposed_file_replace_substring>

<!-- Full file replacement -->
<proposed_file_replace file_path="config.json"
  change_summary="Update API endpoint">
  {"endpoint": "https://api.example.com/v2"}
</proposed_file_replace>

<!-- Line insertion -->
<proposed_file_insert file_path="src/utils.ts"
  change_summary="Add helper function" line_number="42">
  export function formatDate(d: Date): string { ... }
</proposed_file_insert>

<!-- Shell command -->
<proposed_shell_command working_directory="/app"
  is_dangerous="false">
  npm install @tanstack/react-query
</proposed_shell_command>

<!-- Package installation -->
<proposed_package_install language="typescript"
  package_list="zod,drizzle-orm" />

<!-- Change summary (max 58 chars) -->
<proposed_actions summary="Add date formatting utility" />
```

## Variant B: XML Commands (Devin)

Tools as XML elements with attribute parameters:

```xml
<shell id="default" exec_dir="/home/ubuntu/project">
npm run build && npm test
</shell>

<str_replace path="/home/ubuntu/src/app.tsx">
<old_str>const TIMEOUT = 5000;</old_str>
<new_str>const TIMEOUT = 10000;</new_str>
</str_replace>

<create_file path="/home/ubuntu/src/utils.ts">
export function calculateTotal(items: CartItem[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}
</create_file>
```

## Variant C: Tagged Sections (Windsurf/Cursor)

Semantic XML tags to organize prompt sections:

```xml
<identity>Who the agent is</identity>
<capabilities>What the agent can do</capabilities>
<behavioral_rules>Hard constraints</behavioral_rules>
<communication>Output format rules</communication>
<tool_calling>How to invoke tools</tool_calling>
<making_code_changes>Code editing protocol</making_code_changes>
<linter_errors>Error handling policy</linter_errors>
```

## Template

```xml
<identity>[Agent name, role, core purpose]</identity>

<capabilities>[List of what the agent can do]</capabilities>

<rules>[Hard behavioral constraints]</rules>

<response_protocol>
Define each action type with its own XML tag.
Include required attributes (file_path, safety flags).
Add a summary tag for all proposed changes.
</response_protocol>

<environment>[OS, shell, runtime details]</environment>
```

## Key Principle

XML tags serve dual purposes: they structure the prompt for the LLM to understand sections, AND they make the output machine-parseable for IDEs and tooling. The `is_dangerous` flag on shell commands is a recurring safety pattern.
