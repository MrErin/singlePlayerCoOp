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

## Known Fish Tank Errors

These errors are caused by the fish tank security boundary, not by incorrect usage. **Do not retry, work around, or attempt alternative approaches.** Report to the user and stop.

| Error Pattern | Cause | Action |
|---------------|-------|--------|
| `PermissionError: [Errno 1] Operation not permitted` during file copy | `shutil.copy2` calls `chmod` internally, blocked by seccomp | Stop. Report to user. Reference the fish tank chmod restriction. |
| `OSError: [Errno 1]` from any chmod/chown/fchmod operation | Seccomp profile blocks all permission-change syscalls | Stop. Report to user. Do not attempt Python or shell workarounds. |
| `Operation not permitted` from `os.chmod`, `os.chown`, or `os.fchmod` | Same seccomp restriction reached via Python stdlib | Stop. Report to user. |

**Pattern to watch for:** If a tool fails with `PermissionError` or `Operation not permitted` and the traceback includes `shutil`, `os.chmod`, `os.fchmod`, or `copystat` — this is always a fish tank limitation. No amount of retrying or flag changes will fix it.

## Testing Tools — Order of Operations

When assessing or improving test quality, always follow this order:

1. **Coverage first** — `coverage-wrapper run`, then `coverage-wrapper gaps`. Cheap (one test run), clear actionable output.
2. **Mutation testing second** — `mutmut-wrapper run`. Expensive (one test run per mutant). Only run after branch coverage is ≥80%.
3. **Never skip to mutation testing.** If coverage is poor, mutation results are noise.

## Coverage in the Fish Tank

**Always use `coverage-wrapper`, never raw `pytest --cov` or `coverage` commands.** The wrapper handles src detection, output management, and token-efficient formatting.

```bash
# Run tests with branch coverage
coverage-wrapper run

# Run with extra pytest args
coverage-wrapper run tests/test_config.py -x

# Show coverage summary
coverage-wrapper report

# Show coverage for one file
coverage-wrapper report src/myapp/config.py

# Show only files with gaps, sorted worst-first
coverage-wrapper gaps

# Show uncovered lines for one file
coverage-wrapper gaps src/myapp/config.py

# Generate HTML report
coverage-wrapper html
```

### How output works

The wrapper writes detailed output to `/project/mutmut_output/` and only prints summaries to stdout.

- `run` — prints the coverage table (extracted from pytest output), saves full log to `mutmut_output/coverage_run.log`
- `report` — if under 60 lines, prints directly. Otherwise writes to file and shows TOTAL + worst 10 files.
- `gaps` — shows only files with missing coverage, sorted worst-first. Writes to `mutmut_output/coverage_gaps.txt` if large.

**Typical workflow:**
1. `coverage-wrapper run` — get the summary table
2. `coverage-wrapper gaps` — see what needs tests
3. Use `Read` tool on specific gap files to decide what tests to write

## Mutmut in the Fish Tank

**Always use `mutmut-wrapper`, never raw `mutmut` commands.** The wrapper handles spinner suppression, correct v3 CLI usage, and token-efficient output. Do NOT run `mutmut run`, `mutmut results`, `mutmut show`, etc. directly.

```bash
# Run all mutation tests
mutmut-wrapper run

# Run mutations for a specific module/function
mutmut-wrapper run "mymodule.myfunction*"

# Show summary of last run
mutmut-wrapper results

# Show all survived mutant diffs (writes to file if large)
mutmut-wrapper show-all

# Show survived mutants for one file
mutmut-wrapper show src/myapp/config.py

# Generate HTML report
mutmut-wrapper html
```

### How output works

The wrapper writes detailed output to `/project/mutmut_output/` and only prints summaries to stdout. This keeps context tokens low.

- `run` — prints only the last 20 lines (summary), saves full log to `mutmut_output/run.log`
- `results` — prints the compact results summary
- `show` / `show-all` — if output is under 60 lines, prints directly. If larger, writes to `mutmut_output/survived_*.txt` and prints a preview. **Use the Read tool** with offset/limit to inspect the full file.

**Typical workflow:**
1. `mutmut-wrapper run` — get the summary
2. `mutmut-wrapper show-all` — see where diffs were written
3. Use `Read` tool on `mutmut_output/survived_all.txt` to inspect specific sections

**Do NOT modify `pyproject.toml` mutmut config** unless the user asks. The project's existing config is intentional.

If `mutmut-wrapper` fails with a `PermissionError` during file copy, the entrypoint shutil patch may not have deployed (e.g., the venv already had a `sitecustomize.py`). Report this to the user — do not attempt to create or modify `sitecustomize.py` yourself.
