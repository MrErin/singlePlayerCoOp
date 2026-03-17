# Claude Code Docker Fishtank

Runs Claude Code in a container so it can read/write project files but can't
damage your system or change file permissions.

## Setup

```bash
# 1. Build the image. Run this from ~/.claude/docker
docker build -t ai-safe-env -f aidev.Dockerfile .

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
- Use the project's `.venv` and `node_modules` (mounted with the project)

## What Claude CANNOT Do

- Change file permissions (`chmod`) — blocked by seccomp profile
- Change file ownership (`chown`) — blocked by `--cap-drop=ALL`
- Modify anything outside the mounted volumes
- Escalate privileges
- Survive a container restart (no persistent damage possible)

## Security Architecture: Why Three Layers

The fish tank uses three distinct layers to control agent behavior. Each serves
a different purpose and **none of them is redundant**.

### Layer 1: Seccomp Profile (Kernel Enforcement)

`seccomp-no-chmod.json` blocks chmod/chown family syscalls at the Linux kernel.

**This is the hard security boundary.** It cannot be bypassed by any code
running inside the container — not by Python, not by C, not by shell tricks.
If a process calls `chmod()`, `fchmod()`, `fchmodat()`, `chown()`, etc., the
kernel returns `EPERM` before the call executes.

**Why it must never be removed:**

1. **It's the only layer that catches indirect chmod.** An agent can write a
   Python script that calls `os.chmod()`, execute a compiled binary, or use
   `ctypes` to invoke the syscall directly. The hooks and deny rules only
   inspect the Bash command string — they can't see what runs *inside* a
   process. The seccomp profile can.

2. **It blocks entire categories of bypass.** Without seccomp, an agent could:
   - `python3 -c "import os; os.chmod('file', 0o777)"`
   - Write and compile a C program that calls the chmod syscall
   - Use `ctypes` to invoke syscalls directly
   - Invoke `chmod` from within a script written by the `Write` tool
   - Use process substitution: `bash <(echo "chmod 777 file")`
   - Encode commands: `echo Y2htb2QgNzc3IGZpbGU= | base64 -d | bash`
   The hooks would miss all of these. Seccomp catches every one.

3. **It protects tools you haven't thought of yet.** Any future tool, library,
   or script that internally calls chmod will be caught automatically. You
   don't need to anticipate every code path — the kernel does it for you.

4. **It enables safe shutil patching.** The entrypoint deploys a
   `sitecustomize.py` that replaces `shutil.copy2` with `cp`-based
   alternatives so tools like mutmut work. If you removed seccomp instead,
   you'd lose the guarantee that *only* the patched code path is used.
   With seccomp in place, even if the patch fails to load, the worst case
   is a clean error — not a silent permission change.

### Layer 2: Claude Code Deny Rules (Tool-Level Gating)

`settings.json` `permissions.deny` blocks commands like `Bash(chmod *)` at the
Claude Code permission system level. This prevents the agent from even
*attempting* blocked commands, saving tokens and context window.

**Purpose:** Early rejection. Stops the agent before it wastes a tool call.

### Layer 3: PreToolUse Hooks (Command Parsing)

`block-dangerous.py` parses compound commands (pipes, chains, subshells,
newline-separated commands) and blocks dangerous patterns.

**Purpose:** Catches blocked commands hidden in compound expressions that the
simple prefix-matching deny rules would miss, like `echo foo && chmod 777 bar`.
Also catches indirect attempts like `python3 -c "os.chmod(...)"`.

### How the Layers Interact

```
Agent wants to run a command
    │
    ▼
[Layer 2: Deny Rules]  ── direct "chmod ..." prefix? → BLOCKED (no tool call)
    │
    ▼
[Layer 3: Hooks]  ── chmod in pipeline/subshell/python -c? → BLOCKED (hook denies)
    │
    ▼
[Command executes]
    │
    ▼
[Layer 1: Seccomp]  ── process calls chmod syscall? → BLOCKED (kernel EPERM)
```

Layers 2 and 3 are **token-saving optimizations**. Layer 1 is **security**.
If you had to pick only one layer, keep seccomp. But all three together give
you: fast rejection (saves tokens) + deep inspection (catches tricks) +
kernel enforcement (catches everything else).


## Troubleshooting

**"permission denied" writing to /home/node:**
The Dockerfile sets `/home/node` to 777. If you still get errors, your host
UID may not match. Verify with: `docker run --rm --user $(id -u):$(id -g) ai-safe-env claude --version`

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

**Agent can't find packages:**
Ensure your project has a `.venv` directory (Python) or `node_modules` (Node.js)
in the project root. Install packages on your host machine before running the
container. Python tools (pytest, coverage, ruff) are pre-installed in the container.
Use `pytest` directly, or `python3 -m <module>` for venv-only packages.

**mutmut fails with `PermissionError` during file copy:**
The entrypoint auto-deploys a `sitecustomize.py` patch that replaces
`shutil.copy2` with `cp`-based alternatives. If mutmut still fails:
- Check if the project's venv already has a `sitecustomize.py` (the entrypoint
  won't overwrite it). Merge the shutil patch into the existing file.
- Verify the patch loaded: `python3 -c "import shutil; print(shutil.copy.__name__)"`
  — should print `_copy_file`, not `copy`.

**Agent churning on PermissionError / "Operation not permitted":**
If an agent keeps retrying after hitting `PermissionError` or `EPERM`, the
`CLAUDE.md` has a "Known Fish Tank Errors" table that should stop this. If an
agent ignores it, the instructions may need stronger language or the error
pattern may not be listed. Add the specific error to the table.
