# Secret Handling

Prevent credential exposure in agent prompts, logs, generated code, and outputs.

## Source Pattern

- **Devin Security Protocol**: Explicit data security rules in system prompt
- **Claude Code**: Never expose API keys in code suggestions
- **Windsurf**: Environment variable enforcement for credentials

## Secret Classification

| Type | Examples | Handling |
|------|---------|----------|
| API Keys | OpenAI, Stripe, AWS keys | Environment variables only |
| Passwords | Database, service passwords | Vault references only |
| Tokens | JWT, OAuth, session tokens | Never log, never display |
| SSH Keys | Private keys, deploy keys | File system only, never in context |
| Certificates | TLS, signing certs | Mounted secrets, never copied |

## Rules

```
<secret_handling>
  <rule id="S001" severity="critical">
    NEVER include credentials in system prompts or agent context.
    Use environment variable references: ${API_KEY}
  </rule>

  <rule id="S002" severity="critical">
    NEVER log credential values. Log the key name, not the value.
    Correct: "Using API key: OPENAI_API_KEY"
    Wrong: "Using API key: sk-abc123..."
  </rule>

  <rule id="S003" severity="critical">
    NEVER generate code with hardcoded credentials.
    Always use: process.env.API_KEY or os.environ["API_KEY"]
  </rule>

  <rule id="S004" severity="high">
    Detect credential patterns in user-provided files.
    Patterns: sk-, ghp_, AKIA, password=, secret=, token=
    If detected: warn user, do not include in context or logs.
  </rule>

  <rule id="S005" severity="high">
    NEVER include .env file contents in generated outputs.
    Reference .env.example with placeholder values instead.
  </rule>

  <rule id="S006" severity="medium">
    Mask sensitive values in error messages.
    Show first 4 and last 4 characters only: sk-ab...yz12
  </rule>
</secret_handling>
```

## Detection Patterns

Regex patterns to detect credentials in text:

```
API Keys:     sk-[a-zA-Z0-9]{20,}
GitHub:       ghp_[a-zA-Z0-9]{36}
AWS Access:   AKIA[A-Z0-9]{16}
JWT:          eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+
Password:     (password|passwd|pwd)\s*[=:]\s*\S+
Bearer:       Bearer\s+[a-zA-Z0-9._-]+
```

## Audit Requirements

- Log all secret detection events (but NOT the secret values)
- Track which files contain detected credentials
- Report secret exposure incidents immediately
- Maintain a credential rotation schedule reference
