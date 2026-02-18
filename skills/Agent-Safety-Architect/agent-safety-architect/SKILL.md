---
name: agent-safety-architect
description: Design safety architectures for AI agents — autonomy tiers, permission zones, command approval gates, secret handling, escalation paths, and observability. Use when building agents that execute code, modify files, access networks, handle credentials, or make consequential decisions. Covers three autonomy tiers (full-auto, supervised, human-led), container security models, tool safety classifications, and audit logging. Based on patterns from Kimi's 4-layer container model, Claude Code's approval workflows, Devin's data security, and Windsurf's safety protocols.
---

# Agent Safety Architect

Design safety boundaries, permission models, and observability for AI agents.

## Workflow

### Safety Design Workflow

1. Classify agent actions by risk level (safe, moderate, dangerous)
2. Assign autonomy tier for each action class
3. Define permission zones for file system and network access
4. Implement approval gates for high-risk operations
5. Add audit logging and observability

### Safety Audit Workflow

1. Map all agent capabilities to risk levels
2. Check for missing approval gates on dangerous operations
3. Verify secret handling (no credentials in prompts or logs)
4. Test escalation paths end-to-end
5. Score against the safety checklist

## Autonomy Tiers

Three levels of agent autonomy based on risk. Read references for templates.

| Tier | Risk Level | Agent Role | Reference |
|------|-----------|------------|-----------|
| Full Auto | Low | Execute without approval | `references/01-full-auto.md` |
| Supervised | Medium | Execute after approval | `references/02-supervised.md` |
| Human-Led | High | Recommend only, human executes | `references/03-human-led.md` |

## Permission Zones

| Zone | Access | Reference |
|------|--------|-----------|
| File System | Read/write/execute boundaries | `references/04-permission-zones.md` |
| Network | Allowed endpoints and protocols | `references/04-permission-zones.md` |
| Secrets | Environment variables, credential vaults | `references/05-secret-handling.md` |

## Action Risk Classification

```
<risk_classification>
  <safe auto_approve="true">
    - Read files within workspace
    - Search codebase
    - View file outlines
    - List directories
    - Run read-only database queries
  </safe>

  <moderate requires_approval="first_time">
    - Write/modify files within workspace
    - Run shell commands (non-destructive)
    - Install dependencies
    - Create branches
    - Make API calls to allowed endpoints
  </moderate>

  <dangerous requires_approval="always">
    - Delete files or directories
    - Run commands with sudo/root
    - Push to main/production branches
    - Drop database tables
    - Modify environment variables
    - Access external APIs not in allowlist
    - Execute arbitrary network requests
  </dangerous>
</risk_classification>
```

## Approval Gate Template

```
<approval_gate>
  <trigger>[Action that requires approval]</trigger>
  <display>
    - Exact command/action to be performed
    - One-sentence purpose explanation
    - Risk assessment (what could go wrong)
  </display>
  <options>
    <approve>Execute the action</approve>
    <modify>Suggest alternative</modify>
    <reject>Cancel the action</reject>
  </options>
  <timeout>[Auto-reject after N minutes of no response]</timeout>
</approval_gate>
```

## Audit Logging Requirements

Every consequential agent action MUST log:
- Timestamp
- Action taken (tool name + parameters)
- Approval status (auto-approved, user-approved, system-approved)
- Outcome (success, failure, partial)
- State changes caused (files modified, commands run)

## Anti-Patterns

- **Blanket Trust** — auto-approving all actions regardless of risk
- **Security Theater** — approval gates on safe actions, none on dangerous ones
- **Credential Leaking** — API keys in prompts, logs, or generated code
- **Silent Failure** — agent fails destructively with no audit trail
- **Privilege Creep** — agent gradually escalates permissions without review

## Validation Scripts

Validate safety architecture with automated scoring (0-10):

```bash
python3 scripts/validate_safety.py <config_file> [--strict]
```

Checks autonomy tier definitions, 5 safety mechanisms (secret handling, permission zones, audit logging, escalation, input validation), detects hardcoded credentials, and flags unsafe patterns (bypass instructions, elevated defaults).
