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
