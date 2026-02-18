# Permission Zones

Define filesystem and network boundaries that constrain agent access.

## Source Pattern

- **Kimi Container Model**: `/mnt/okcomputer/upload/` (read-only) + `output/` (read-write) + `.store/` (append-only)
- **Claude Code**: Workspace-relative paths only, no system directory access
- **Windsurf**: File operations restricted to project directory

## File System Zones

```
<permission_zones>
  <zone name="workspace" path="[PROJECT_ROOT]" access="read-write">
    Agent can freely read and modify project files.
    Excludes: .env, .git/config, secrets/
  </zone>

  <zone name="uploads" path="[UPLOAD_DIR]" access="read-only">
    User-provided files. Agent can read but never modify or delete.
  </zone>

  <zone name="output" path="[OUTPUT_DIR]" access="write-only">
    Agent deliverables. Agent can create and write but not delete.
  </zone>

  <zone name="audit" path="[AUDIT_DIR]" access="append-only">
    Logs and citations. Agent can add entries but never modify or delete.
  </zone>

  <zone name="system" path="/etc, /usr, /var" access="denied">
    System directories. Agent has no access whatsoever.
  </zone>

  <zone name="home" path="~/" access="denied">
    User home directory. Agent cannot access dotfiles, SSH keys, etc.
  </zone>
</permission_zones>
```

## Network Access Zones

```
<network_zones>
  <zone name="allowed_apis" access="permitted">
    <endpoint>api.github.com</endpoint>
    <endpoint>registry.npmjs.org</endpoint>
    <endpoint>[EXPLICITLY_ALLOWED_ENDPOINTS]</endpoint>
  </zone>

  <zone name="blocked" access="denied">
    All endpoints not in the allowed list.
    Agent cannot make arbitrary HTTP requests.
  </zone>

  <zone name="browser_only" access="browser_tool">
    Web browsing through controlled browser tools only.
    No direct curl, wget, or requests.get().
  </zone>
</network_zones>
```

## Implementation Principles

- Default deny — only explicitly allowed paths/endpoints are accessible
- Log all access attempts (including denied ones)
- Review and update zones quarterly
- Separate user data from agent workspace
