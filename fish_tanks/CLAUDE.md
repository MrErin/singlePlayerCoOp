# Skills

Always load and follow these skills when doing development work:

- **iterative-build**: Use for all multi-step development. Follow its phase gates and .planning/ directory structure. Invoked via /plan: commands.
- **my-style**: Follow for ALL code written in any language. Covers formatting, naming, accessibility, and ADHD-friendly patterns.
- **post-build-review**: Use after completing all phases to generate review docs.

When any /plan: command is invoked, load the iterative-build skill first.

Always use Context7 MCP for code generation, library usage, setup steps, and API documentation without me explicitly asking.

Always use jcodemunch MCP for codebase exploration and code analysis:
- **index_folder** or **index_repo** — when starting work on a project not yet indexed
- **search_symbols** — find functions, classes, methods by name or signature
- **get_symbol** / **get_symbols** — retrieve full source code for specific symbols
- **get_file_outline** — see all symbols in a file with signatures
- **search_text** — full-text search for string literals, comments, config values

Always use sequential-thinking MCP for complex planning decisions that benefit from chain of thought reasoning.

# Environment

You are running inside a Docker container. This determines what is and is not possible.

User uses JetBrains IDEs.

## Fish Tank Terminology

When you encounter issues with **your own container environment** (not a project container, not a production environment), refer to it as the **"fish tank"**. This helps distinguish:
- **Fish tank issues** — problems with the AI agent's container (permissions, missing packages, blocked syscalls)
- **Project issues** — problems with the codebase being worked on
- **Environment issues** — problems with other containers or systems

Example: "I can't install that package in the fish tank — it's an ephemeral container."

## Hard Limits

These will never work. Do not attempt them, do not try variations or workarounds:

- `sudo` — blocked by policy
- `chmod`, `chown`, `chgrp`, `setfacl` — blocked at the kernel level
- `apt-get`, `apt`, `dpkg` — require sudo
- `killall`, `pkill`, `kill -9` — blocked by policy
- `systemctl`, `shutdown`, `reboot` — blocked by policy

**When a command is denied or fails due to permissions: stop. Do not try alternative approaches to the same blocked operation. Explain what you need and ask the user to handle it outside the container.**

## Secrets and Environment Variables

**Never read, write, grep, cat, diff, base64-encode, or otherwise access `.env` files or any other secret/credential file.** This applies to all access paths — not just the Read tool, but every Bash command and every write operation.

Secret files include:

- `.env`, `.env.local`, `.env.production`, `.envrc`, and any `.env.*` variant
- `*.pem`, `*.key`, `*.p12`, `*.pfx`
- `id_rsa`, `id_ed25519`, `id_ecdsa`, `id_dsa` (SSH private keys)
- `.netrc`, `.aws/credentials`
- Anything inside a `secrets/` directory
- Files named `credentials.json`, `credentials.yaml`, etc.

**If you need to know what environment variables an app expects:**
Read `.env.example` or search source code for `os.getenv(...)`, `process.env.X`, or equivalent config lookups. Do not read `.env` to answer this question.

**If a task requires knowing an actual secret value** (e.g., verifying a connection string, checking an API key is correct): stop. Ask the user to check, verify, or provide what's needed. Never attempt to read the file yourself.

Access attempts via `cat`, `grep`, `awk`, `python3 -c`, `find -exec`, or any other method are blocked at the hook level and will be denied automatically. When you see a deny, do not try an alternative approach — ask the user instead.

## What Works

- Standard dev tools already installed: pytest, coverage, mutmut, hypothesis, ruff
- Git is available for reading (status, diff, log) — commits are handled by the user

## Ephemeral Environment

**Do NOT install packages via pip or npm.** The container uses `--rm` — everything outside mounted volumes disappears on exit. Installing packages is wasted effort.

## Using the Project's Virtual Environment

The project is mounted at `/project` with its `.venv` and `node_modules` intact.

**Python projects:**
- Run tools via: `pytest`, `coverage`, `ruff` (pre-installed in container)
- For venv-only packages: `python3 -m <module>` (e.g., `python3 -m mypy`)
- The venv's site-packages is added to PYTHONPATH automatically

**Node.js projects:**
- Run tools via: `npx <tool>`, `node_modules/.bin/<tool>`
- Local binaries are added to PATH automatically

If a package is missing:
1. Tell the user what's missing
2. They will install it on the host and restart the container

## When Imports Fail

If a package import fails (`ModuleNotFoundError`, `ImportError`), diagnose before reporting:

1. **Check if the package files exist:** `ls .venv/lib/python*/site-packages/ | grep <package>`
2. **If files exist but import fails:** This is a Python version mismatch, not a missing package. The venv was created with a different Python version than the container provides. Report the mismatch (container Python version vs. venv Python version from `.venv/pyvenv.cfg`) and ask the user to fix the Docker image.
3. **If files don't exist:** The package is genuinely missing. Tell the user what's missing. They will install it on the host and restart the container.

**Never work around import failures with mocks in production code.** If imports don't work, the environment is broken. Stop and escalate.

## Known Fish Tank Errors

These errors are caused by the fish tank security boundary, not by incorrect usage. **Do not retry, work around, or attempt alternative approaches.** Report to the user and stop.

| Error Pattern | Cause | Action |
|---------------|-------|--------|
| `PermissionError: [Errno 1] Operation not permitted` during file copy | `shutil.copy2` calls `chmod` internally, blocked by seccomp | Stop. Report to user. Reference the fish tank chmod restriction. |
| `OSError: [Errno 1]` from any chmod/chown/fchmod operation | Seccomp profile blocks all permission-change syscalls | Stop. Report to user. Do not attempt Python or shell workarounds. |
| `Operation not permitted` from `os.chmod`, `os.chown`, or `os.fchmod` | Same seccomp restriction reached via Python stdlib | Stop. Report to user. |

**Pattern to watch for:** If a tool fails with `PermissionError` or `Operation not permitted` and the traceback includes `shutil`, `os.chmod`, `os.fchmod`, or `copystat` — this is always a fish tank limitation. No amount of retrying or flag changes will fix it.

## Testing Tools

Use the wrapper scripts, never raw commands. They handle output formatting, suppress noise, and write detailed results to `/project/mutmut_output/` for token-efficient inspection via the Read tool.

**Order of operations — always coverage first, mutation second:**

1. `coverage-wrapper run` then `coverage-wrapper gaps` — cheap (one test run)
2. `mutmut-wrapper run` — expensive (one run per mutant), only after branch coverage ≥80%
3. Never skip to mutation testing. If coverage is poor, mutation results are noise.

Run `coverage-wrapper --help` or `mutmut-wrapper --help` for full command reference.

**Do NOT modify `pyproject.toml` mutmut config** unless the user asks.

If `mutmut-wrapper` fails with `PermissionError` during file copy, the entrypoint shutil patch may not have deployed. Report to the user — do not attempt to create or modify `sitecustomize.py` yourself.
