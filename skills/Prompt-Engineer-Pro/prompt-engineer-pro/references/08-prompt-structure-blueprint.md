# Prompt Structure Blueprint

Correct section ordering and structural patterns extracted from 7 production agent system prompts. Use this as the canonical reference when composing new agent prompts.

## Source Systems Analyzed

| System | Structural Style | Section Count | Token Size |
|--------|-----------------|---------------|------------|
| Kimi OK Computer | Markdown `#` headings | 8 sections | ~15K |
| Kimi Base Chat | Markdown `#` headings | 7 sections | ~8K |
| Cursor Agent 2.0 | Markdown `#` + tool JSON | 4 sections | ~12K |
| Claude Code | Markdown `#` headings | 8 sections | ~6K |
| Devin | XML tags + prose | 6 sections (implicit) | ~18K |
| Replit | XML `<tag>` blocks | 6 sections | ~10K |
| Windsurf Cascade | XML `<tag>` blocks | 11 sections | ~8K |

---

## Paradigm 1: XML-Tagged Blocks (Replit, Windsurf, Devin)

Sections wrapped in XML tags. Best for machine-parseable prompts and strict section isolation.

### Replit Structure

```xml
<identity>
  Name, role, 2 sentences.
</identity>

<capabilities>
  What the agent CAN do, organized by action type:
  - Proposing file changes (with examples)
  - Proposing shell commands (with examples)
  - Answering queries (with examples)
  - Tool nudges (redirecting to other tools)
</capabilities>

<behavioral_rules>
  Hard constraints: focus on request, follow existing patterns,
  precise modifications, no creative extensions unless asked.
</behavioral_rules>

<environment>
  Platform (Replit IDE), OS (Linux/Nix), runtime context,
  auto-install behavior.
</environment>

<response_protocol>
  Exact output format per action type:
  - File edits: <proposed_file_replace_substring>
  - New files: <proposed_file_create>
  - Shell commands: <proposed_shell_command>
  - Packages: <proposed_package_install>
</response_protocol>

<tool_definitions>
  Per-tool blocks with name, parameters, examples.
</tool_definitions>
```

### Windsurf Cascade Structure

```xml
[Identity paragraph — inline, no tag]
You are Cascade, a powerful agentic AI coding assistant...

<user_information>
  OS, workspace paths, open files.
</user_information>

<tool_calling>
  Tool invocation rules, parallel call guidance, examples.
</tool_calling>

<making_code_changes>
  Edit principles: read before write, minimal diffs,
  argument ordering requirements.
</making_code_changes>

<debugging>
  Systematic debugging protocol.
</debugging>

<memory_system>
  Memory storage and retrieval rules.
  IMPORTANT: always pay attention to memories.
</memory_system>

<code_research>
  Search strategy rules.
</code_research>

<running_commands>
  Command execution and approval rules.
</running_commands>

<browser_preview>
  Browser tool usage rules.
</browser_preview>

<calling_external_apis>
  API call restrictions and approval.
</calling_external_apis>

<communication_style>
  Tone, formatting, conciseness rules.
</communication_style>

<planning>
  When and how to plan before acting.
</planning>
```

### Devin Structure

```xml
[Identity + capabilities as inline prose at top]
You are Devin, a software engineer...

[Tool definitions as XML tags — bulk of prompt]
<shell>...</shell>
<open_file>...</open_file>
<str_replace>...</str_replace>
<create_file>...</create_file>
<find_filecontent>...</find_filecontent>
<semantic_search>...</semantic_search>
<navigate_browser>...</navigate_browser>
<message_user>...</message_user>
<deploy_frontend>...</deploy_frontend>
<suggest_plan>...</suggest_plan>

[Behavioral rules as inline IMPORTANT blocks at end]
IMPORTANT: Always verify before deploying...
IMPORTANT: Never expose secrets...
```

**Key Insight**: Devin is tool-definition heavy (~60% of prompt is tool specs). Identity and rules surround the tools as thin wrappers.

---

## Paradigm 2: Markdown-Headed Sections (Kimi, Claude Code, Cursor)

Sections use `#` and `##` headings. Best for human readability and agents that reason over their own prompt.

### Kimi OK Computer Structure (Most Comprehensive)

```markdown
[Identity paragraph — inline at very top]
Kimi is an AI agent developed by Moonshot AI...
Current date: YYYY-MM-DD

# Communication Guidelines
  ## Core Stance
  ## Principles
  ## Boundaries

# Capability System
  ## Skills (Domain Extensions)
    - Skills Path
    - Available Skills (name + description table)
    - Usage Principles (when to read, when not to)
    - Example workflow
  ## Slides generation rule

# External Data Acquisition
  - Priority order: datasource tools → web search
  - Available Datasources (table)
  - Data Citation Rule
  - Time Handling

# Special Deliverable Tools Policy
  ## Image generation policy
  ## Slides policy
  ## Deploy policy

# Artifact Output Rules
  - KIMI_REF tag format
  - Single file / multiple file examples
  - What to include vs exclude

# Skill Reading Instructions
  ## docx skill
  ## pdf skill
  ## xlsx skill
  ## webapp skill

# Available Tools
  ## mshtools-todo_read
  ## mshtools-todo_write
  ## mshtools-ipython
  ## mshtools-read_file
  ## mshtools-edit_file
  ## mshtools-write_file
  ## mshtools-shell
  ## mshtools-browser_*
  ## mshtools-web_search
  ## mshtools-generate_image
  ## mshtools-deploy_website
  ## mshtools-slides_generator
```

### Kimi Base Chat Structure (Constrained Version)

```markdown
[Identity — short paragraph]
You are Kimi K2.5, an AI assistant developed by Moonshot AI...

# Boundaries
  - Cannot generate downloadable files
  - Redirect to appropriate Kimi alternatives

# Available tools
  [CRITICAL] 10-step budget limit
  ## web (web_search, web_open_url, image search, datasource)
  ## ipython environment
  ## memory_space

# Content display rules
  ## Search citation
  ## Deliverables (images, downloads, math, HTML)

# Memory
  Long-term memory integration rules.

# Config
  UI language, current date, memory space contents.
```

**Key Insight**: Base Chat and OK Computer share the same identity but Base Chat strips down capabilities (10-step budget, no file write, no skills). This shows how to create **tiered agent variants** from the same base.

### Claude Code Structure

```markdown
[Identity — inline paragraph]
You are Claude Code...

# Tone and style
  - Be direct, minimal filler
  - Technical but accessible
  - Honest about limitations

# Proactiveness
  - Scope of proactive action rules

# Following conventions
  - Match existing code patterns

# Code style
  - Formatting and naming rules

# Task Management
  - TodoWrite usage rules

# Doing tasks
  - Execution order and verification

# Tool usage policy
  - When to use which tool

# Code References
  - Citation format for existing code
```

**Key Insight**: Claude Code is the most compact production prompt (~6K tokens). It achieves this by relying on tool descriptions (separate JSON) rather than inlining tool specs in the prompt. Rules are brief imperatives.

### Cursor Agent 2.0 Structure

```markdown
# Tools
  ## functions
    [JSON tool definitions — 40+ tools]
  ## multi_tool_use

## METHOD 1: CODE REFERENCES
  ### Content Rules

## METHOD 2: MARKDOWN CODE BLOCKS
  ### Format

## Critical Formatting Rules for Both Methods
  ### Never Include Line Numbers
  ### NEVER Indent Triple Backticks
  ### ALWAYS Add Newline Before Code Fences
```

**Key Insight**: Cursor's prompt is dominated by tool definitions and output formatting rules. Identity is minimal. This is the **tool-first** paradigm — the agent's behavior comes from its tools, not from identity paragraphs.

---

## Universal Section Ordering

Based on all 7 systems, the correct prompt section order is:

```
┌──────────────────────────────────────────────────────────┐
│ 1. IDENTITY (Top)                                         │
│    Name, role, hosting context, 2-3 sentences max         │
│    Position: ALWAYS first (highest attention zone)         │
├──────────────────────────────────────────────────────────┤
│ 2. COMMUNICATION / TONE                                   │
│    How to respond: style, verbosity, formatting            │
│    Kimi: "Communication Guidelines"                        │
│    Claude Code: "Tone and style"                           │
│    Windsurf: <communication_style>                         │
├──────────────────────────────────────────────────────────┤
│ 3. CAPABILITIES / BOUNDARIES                              │
│    What agent CAN and CANNOT do                            │
│    Kimi: "Capability System" + "Boundaries"                │
│    Replit: <capabilities> + <behavioral_rules>             │
│    Claude Code: "Proactiveness"                            │
├──────────────────────────────────────────────────────────┤
│ 4. SKILLS / DOMAIN KNOWLEDGE                              │
│    Modular knowledge injection points                      │
│    Kimi: Skills path + available skills + usage principles  │
│    Only in multi-domain agents                             │
├──────────────────────────────────────────────────────────┤
│ 5. BEHAVIORAL RULES                                       │
│    Hard constraints: ALWAYS/NEVER imperatives               │
│    Kimi: "Special Deliverable Tools Policy"                │
│    Claude Code: "Following conventions" + "Code style"     │
│    Windsurf: <making_code_changes> + <debugging>           │
├──────────────────────────────────────────────────────────┤
│ 6. TOOLS                                                   │
│    Complete tool specifications with types and examples     │
│    Kimi: "Available Tools" (~50% of prompt)                │
│    Cursor: "Tools > functions" (~70% of prompt)            │
│    Devin: XML tool tags (~60% of prompt)                   │
├──────────────────────────────────────────────────────────┤
│ 7. OUTPUT FORMAT / RESPONSE PROTOCOL                      │
│    How to structure responses and deliverables              │
│    Kimi: "Artifact Output Rules" + "Content display rules" │
│    Replit: <response_protocol>                             │
│    Cursor: "METHOD 1/2" + "Critical Formatting Rules"      │
├──────────────────────────────────────────────────────────┤
│ 8. ENVIRONMENT / CONFIG (Bottom)                          │
│    OS, shell, date, workspace paths, user preferences      │
│    Kimi: "Config" section at very end                      │
│    Windsurf: <user_information> near top                   │
│    Replit: <environment>                                   │
│    Position: Bottom or injected dynamically                │
└──────────────────────────────────────────────────────────┘
```

---

## Attention Optimization Rules

From the "Lost in the Middle" research and confirmed by production prompts:

1. **Identity at the top** — every production prompt starts with identity
2. **Safety rules at the top or bottom** — never buried in the middle
3. **Tool specs can go in the middle** — they dominate token count but are retrieved by name, not position
4. **Config/environment at the bottom** — dynamic, injected per session
5. **Examples near their rules** — not grouped separately

---

## Three Prompt Archetypes

### Archetype A: Identity-Heavy (Kimi, Claude Code)
- Long identity + communication section
- Skills/capabilities front-loaded
- Tools listed after rules
- Best for: General-purpose agents, user-facing assistants

### Archetype B: Tool-Heavy (Cursor, Devin)
- Minimal identity (1-2 sentences)
- Tool specs dominate (60-70% of tokens)
- Formatting rules at the end
- Best for: IDE-embedded coding assistants

### Archetype C: Structure-Heavy (Replit, Windsurf)
- XML-tagged sections with strict boundaries
- Equal weight across sections
- Explicit response protocols
- Best for: Agents with structured output requirements

---

## Production Prompt Template

Combining the best patterns from all 7 systems:

```
<identity>
  [Name], [role] developed by [org].
  [2-sentence purpose statement].
  [Hosting context: IDE/platform name].
</identity>

<communication>
  [Tone: professional/casual/adaptive]
  [Verbosity: match user's depth]
  [Format: markdown, no headers in chat, structured for deliverables]
  [Boundaries: no meta-instructions, no tool implementations exposed]
</communication>

<capabilities>
  CAN:
  - [Capability 1]
  - [Capability 2]

  CANNOT:
  - [Limitation 1]
  - [Limitation 2]
</capabilities>

<skills>
  [Only if multi-domain]
  Path: [skills directory]
  Available: [skill_name]: [description]
  Rule: MUST read SKILL.md before executing domain tasks.
</skills>

<rules>
  [Safety-critical rules first]
  NEVER expose API keys, secrets, or credentials.
  NEVER execute destructive commands without approval.

  [Behavioral rules]
  ALWAYS read file before editing.
  ALWAYS prefer editing existing files over creating new ones.

  [Style rules]
  Follow existing code patterns.
  Match user's language and depth.
</rules>

<tools>
  [Tool definitions — XML, JSON Schema, or markdown tables]
  [Each tool: name, description, parameters (typed), example, safety flag]
</tools>

<output_format>
  [Response structure rules]
  [Code block formatting rules]
  [Deliverable format (file references, citations)]
</output_format>

<environment>
  OS: [detected]
  Shell: [detected]
  Date: [injected]
  Workspace: [injected path]
  User preferences: [injected from memory/config]
</environment>
```
