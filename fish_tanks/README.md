# Claude Code Docker Fishtank

Runs Claude Code in a container so it can read/write project files but can't
damage your system or change file permissions.

## Setup

```bash
# 1. Build the image. Run this from ~/.claude/docker
docker build -t ai-safe-env - f aidev.Dockerfile .

# 2. Copy the seccomp profile where the functions expect it
cp seccomp-no-chmod.json ~/.claude/docker/

# 3. Add the functions to your shell config
# copy `claude.zshrc` to the ~/.zshrc file. Put the correct token in the indicated spot

# 4. Use from any project directory
cd ~/projects/my-app
arch-code          # Opus
plan-code          # Sonnet
gcode              # GLM endpoint
arch-code -p "fix the login bug"   # extra args pass through
```

## What Each Security Layer Does

| Flag                               | Protects Against                                                                               |
| ---------------------------------- | ---------------------------------------------------------------------------------------------- |
| `--cap-drop=ALL`                   | `chown`, binding privileged ports, raw sockets, loading kernel modules, all other capabilities |
| `--security-opt no-new-privileges` | Processes escalating via setuid/setgid binaries                                                |
| `seccomp-no-chmod.json`            | `chmod`/`fchmod` — the thing that bit you                                                      |
| `--user $(id -u):$(id -g)`         | Files created in the container are owned by YOUR host user, not root                           |
| Container isolation                | Claude can't touch anything outside `/project` and `/home/node/.claude`                        |

## What Claude CAN Still Do

- Read and write file *contents* in your project directory
- Read your global Claude settings, commands, and skills from `~/.claude`
- Write to `~/.claude` (session state, auth tokens, etc.)
- Access the network (needed for API calls, MCP, web search)
- Run git commands within the project
- Install npm/pip packages inside the container (they disappear when it exits)

## What Claude CANNOT Do

- Change file permissions (`chmod`) — blocked by seccomp profile
- Change file ownership (`chown`) — blocked by `--cap-drop=ALL`
- Modify anything outside the mounted volumes
- Escalate privileges
- Survive a container restart (no persistent damage possible)

## Seccomp Profile Trade-off

The included `seccomp-no-chmod.json` uses `defaultAction: ALLOW` and blocks
specific syscalls. This is slightly MORE permissive than Docker's default
seccomp profile (which blocks ~44 syscalls). However, `--cap-drop=ALL` already
covers most of what the default profile blocks.

If you want belt-AND-suspenders, download Docker's default profile and add the
chmod blocks to it:

```bash
# Download Docker's default seccomp profile
curl -o ~/.claude/docker/seccomp-default.json \
  https://raw.githubusercontent.com/moby/moby/master/profiles/seccomp/default.json

# Then manually add the chmod/chown entries to the "syscalls" array
# and use that file instead
```

## Troubleshooting

**"permission denied" writing to /home/node:**
The Dockerfile sets `/home/node` to 777. If you still get errors, your host
UID may not match. Verify with: `docker run --rm --user $(id -u):$(id -g) ai-safe-env --version`

**Claude can't find settings/commands:**
Your `~/.claude` directory is mounted at `/home/node/.claude`. Claude Code
should find `settings.json`, `commands/`, etc. there automatically. Verify
the mount: `docker run --rm -v "$HOME/.claude":/home/node/.claude ai-safe-env ls /home/node/.claude`

**MCP servers not connecting:**
MCP servers that use local unix sockets won't work across the container
boundary. MCP servers accessed via HTTP/HTTPS (like remote APIs) work fine
since the container has network access. If you need socket-based MCP, you'd
need to mount the specific socket with an additional `-v` flag.

**Need additional tools (python, make, etc.):**
Add them to the Dockerfile:
```dockerfile
RUN apt-get update && apt-get install -y \
    git curl python3 python3-pip make \
    && rm -rf /var/lib/apt/lists/*
```
Then rebuild: `docker build -t ai-safe-env /path/to/directory/`

**Packages installed by Claude disappear:**
By design. The container is `--rm` so everything resets. If Claude needs
persistent packages, add them to the Dockerfile.
