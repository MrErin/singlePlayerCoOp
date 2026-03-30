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

### HTTP-based (remote) MCP servers

Remote MCP servers require no local installation — they run as hosted services.
Register with the `--type http` flag:

```bash
claude mcp add -s user -t http <name> <url> --header "Authorization: Bearer <api-key>"
```

The API key is sent as a header on every request. Store the key in your
credential manager, not in version control.

**Example:** Z.AI web-search-prime uses `https://api.z.ai/api/mcp/web_search_prime/mcp`

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

## GLM Fish Tank: Web Search

Claude Code's built-in `WebSearch` tool is an Anthropic-only server-side feature.
It does not work through the Z.AI proxy (`ANTHROPIC_BASE_URL`), returning Zhipu
error code `1210`. The `WebFetch` tool may also be affected (it uses Anthropic's
domain validation and server-side Haiku summarization).

**Fix:** Use Z.AI's `web-search-prime` MCP server instead. It provides a
`webSearchPrime` tool that works independently of the model provider.

### Setup

```bash
claude mcp add -s user -t http web-search-prime \
  https://api.z.ai/api/mcp/web_search_prime/mcp \
  --header "Authorization: Bearer YOUR_Z_AI_API_KEY"
```

Use the same API key from your Z.AI console (https://z.ai/manage-apikey/apikey-list).

Quota limits by Z.AI plan: Lite = 100, Pro = 1,000, Max = 4,000 searches.

### Already done

- `settings-glm.json` has `mcp__web_search_prime__*` in the allow list
- `settings-glm.json` sets `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1` to suppress
  beta headers that the Z.AI proxy can't handle

### Verification

After running the `claude mcp add` command:

1. `claude mcp list` — should show `web-search-prime` as connected
2. Start a GLM fish tank (`gcode`) and ask the agent to search for something
3. The agent should use the `webSearchPrime` tool (not the built-in `WebSearch`)

For full details, see `still-thinking/web-search-troubleshooting.md`.

## Troubleshooting

**"Failed to connect" in `claude mcp list`**

1. Verify the binary exists on your host: `which <command>`
2. Test it runs: `<command>` (should start and wait for input)
3. Check registration: `claude mcp get <name>` — ensure the command matches the installed binary
