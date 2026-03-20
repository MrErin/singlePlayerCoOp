# Installing MCP Servers with the Fish Tank

This document captures the constraints for adding MCP servers when using the fish tank environment.

## Critical Insight

**MCP servers run on the HOST machine, not inside the fish tank container.**

Claude Code spawns MCP servers as subprocesses from the host process — they never execute inside the container. Installing MCP binaries in the Dockerfile will NOT make them available.

## Fish Tank Constraints (for reference)

These apply to code running INSIDE the container, not MCP servers:

- **Seccomp restrictions** — The container blocks `chmod`, `chown`, and related syscalls
- **No sudo** — Blocked by policy
- **Ephemeral** — `--rm` means changes outside mounted volumes disappear on exit

Since MCP servers run on the host, these restrictions do not affect them.

## Installation Patterns

### Node-based MCP servers

**Recommended approach** — Node-based servers work cleanly via npx:

```bash
claude mcp add <name> npx -y <npm-package>
```

**Example:** context7 uses `npx -y @upstash/context7-mcp`

### Python-based MCP servers

Install on your host machine directly:

```bash
# On the host machine
pip install <package-name>
# OR
uv tool install <package-name>

# Then register
claude mcp add <name> <package-name>
```

## Permissions

The `fish_tanks/settings*.json` files control tool permissions for the agent. To allow an MCP server's tools:

```json
"allow": [
  "mcp__<server-name>__*"
]
```

This is separate from configuring the MCP server itself.

## Checklist for New MCP Servers

1. [ ] Install on HOST (not in Dockerfile)
2. [ ] Register: `claude mcp add <name> <command>`
3. [ ] Add permission to `settings.json` and `settings-glm.json`
4. [ ] Run `./deploy/deploy.sh`
5. [ ] Verify: `claude mcp list` should show the server as connected

## Troubleshooting

**"Failed to connect" in `claude mcp list`**

1. Verify the binary exists on your host: `which <command>`
2. Test it runs: `<command>` (should start and wait for input)
3. Check registration: `claude mcp get <name>` — ensure the command matches the installed binary
