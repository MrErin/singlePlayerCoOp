# Skills

**Before writing or modifying any code — including quick fixes, debugging, and one-liners — always load `my-style`.** This applies even when the task seems too small to matter.

**If `_planning/` exists in the project, read `state.md` before making any code changes.** Understand what phase is active and what's in scope before touching anything.

**If you defer a UA testing item rather than fixing it, add it to `_planning/deferred.md` before the conversation ends.** Do not wait for `/plan:review` — log it immediately.

Always load and follow these skills:

- **iterative-build**: Use for all multi-step development. Follow its phase gates and `_planning/` directory structure. Invoked via /plan: commands.
- **my-style**: Follow for ALL code written in any language. Covers formatting, naming, accessibility, and ADHD-friendly patterns.
- **post-build-review**: Use after completing all phases to generate review docs.

When any /plan: command is invoked, load the iterative-build skill first.

Always use Context7 MCP for code generation, library usage, setup steps, and API documentation without me explicitly asking.

When templates or skill files include emojis, always use them — they serve as visual cues.

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

Permission changes (`chmod`, `chown`), package installation (`apt`, `pip`, `npm`), process management (`kill`, `systemctl`), and privilege escalation (`sudo`) are blocked at the kernel/policy level. The deny list in `settings.json` and `block-dangerous.py` hook enforce this mechanically.

**When a command is denied or fails due to permissions: stop. Do not try alternative approaches. Ask the user to handle it outside the container.**

## Secrets and Environment Variables

Secret and credential files (`.env*`, `*.pem`, `*.key`, SSH keys, `secrets/`, `credentials.*`) are blocked by the settings deny list and `block-secrets.py` hook across all tools.

**If you need to know what environment variables an app expects:** Read `.env.example` or search source code for `os.getenv(...)`, `process.env.X`, or equivalent config lookups.

**If a task requires an actual secret value:** Stop and ask the user. Never attempt to read secret files yourself.

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

1. **Check if files exist:** `ls .venv/lib/python*/site-packages/ | grep <package>`
2. **Files exist but import fails:** Python version mismatch — report the mismatch (container vs `.venv/pyvenv.cfg`) and ask user to fix.
3. **Files don't exist:** Package genuinely missing — tell user to install on host and restart container.

## Known Fish Tank Errors

`PermissionError` or `Operation not permitted` from `shutil`, `os.chmod`, `os.fchmod`, or `copystat` is always a fish tank seccomp limitation. Do not retry or work around — stop and report to user.

## Testing Tools

Use the wrapper scripts, never raw commands. They handle output formatting, suppress noise, and write detailed results to `/project/mutmut_output/` for token-efficient inspection via the Read tool.

**Order of operations — always coverage first, mutation second:**

1. `coverage-wrapper run` then `coverage-wrapper gaps` — cheap (one test run)
2. `mutmut-wrapper run` — expensive (one run per mutant), only after branch coverage ≥80%
3. Never skip to mutation testing. If coverage is poor, mutation results are noise.

Run `coverage-wrapper --help` or `mutmut-wrapper --help` for full command reference.

**Do NOT modify `pyproject.toml` mutmut config** unless the user asks.

If `mutmut-wrapper` fails with `PermissionError` during file copy, the entrypoint shutil patch may not have deployed. Report to the user — do not attempt to create or modify `sitecustomize.py` yourself.
