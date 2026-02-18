# Pattern: Skill Injection (Runtime Knowledge Loading)

Source: Kimi (Moonshot AI)

## When to Use

- Agent serves multiple domains (docs, spreadsheets, code, etc.)
- Knowledge is modular and domain-specific
- Context window must stay efficient — load only what's needed
- Adding new capabilities should not require code changes

## Architecture

Generic tools (`shell`, `ipython`, `read_file`) become specialists via runtime documentation loading.

```
User Request → Intent Classification → Skill Detection
  → read_file(SKILL.md) → Context enriched → Execute with expertise
```

### Context Stack Model

```
Top:    SKILL.md (domain expertise, transient)
Middle: Base prompt (identity, permanent)
Bottom: Conversation history + user message
```

### Dynamic Context Loading

During execution, sub-documents are loaded/unloaded based on what the agent encounters:
- Compilation fails → load troubleshooting docs
- Route chosen (HTML vs LaTeX) → load only relevant sub-instructions
- Validation fails → load element ordering guidance

## Template

```xml
<identity>
You are [Agent Name], an AI assistant.
</identity>

<skills>
You have access to specialized skills. Each skill folder contains a SKILL.md file.
When you detect a task matching a skill domain, read the SKILL.md BEFORE doing anything else.

Available skills:
- domain-a/ → Use for [domain A tasks]
- domain-b/ → Use for [domain B tasks]

If no skill matches, proceed with general knowledge.
</skills>

<skill_loading_rules>
1. ALWAYS read SKILL.md before starting domain-specific work
2. Follow SKILL.md instructions exactly
3. If SKILL.md references sub-documents, load them as needed
4. Discard skill context when task is complete
</skill_loading_rules>
```

## Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| Skill-gated shell | New capabilities via docs only, no code deploy | Agent may ignore instructions |
| Specialized tools | Clear failure modes (function doesn't exist) | New capabilities require backend changes |

## Key Principle

The tool doesn't change. The knowledge changes. Adding Excel support means writing xlsx/SKILL.md, not deploying a new API endpoint.
