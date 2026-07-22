# Skills

**Before writing or modifying any code — including quick fixes, debugging, and one-liners — load `my-style` first. Do not write a single line until you have done this.** This applies even when the task seems too small to matter. If context was just cleared, load it again — it does not persist across context resets.

**If `_planning/` exists in the project, read `state.md` before making any code changes.** Understand what phase is active and what's in scope before touching anything.

**If you defer a UA testing item rather than fixing it, add it to `_planning/deferred.md` before the conversation ends.** Do not wait for `/plan:review` — log it immediately.

Always load and follow these skills:

- **iterative-build**: Use for all multi-step development. Follow its phase gates and `_planning/` directory structure. Invoked via /plan: commands.
- **my-style**: Follow for ALL code written in any language. Covers formatting, naming, accessibility, and ADHD-friendly patterns.
- **post-build-review**: Use after completing all phases to generate review docs.

When any /plan: command is invoked, load the iterative-build skill first.

Always use Context7 MCP for code generation, library usage, setup steps, and API documentation without me explicitly asking.

## Guardrails Gap Check

When asked what rule, wording, or guardrail would have prevented or caught an issue — including questions like "what rule would have flagged this?", "where does this belong in the instructions?", "what's missing from the guardrails?", or "how do I stop this from happening again?":

1. **Do not edit any deployed skill, config, or CLAUDE.md file.** Deployed files are overwritten on the next deploy from the source repo. In-place edits will be lost.
2. Identify the correct source file in `/project/ai-workflow/` where the rule belongs — skill reference file, agent, command, or CLAUDE.md template.
3. Output the exact text to add as a copyable block.
4. State the insertion point: file path + section name + whether it's a new section or an addition to existing text.
5. If multiple files need changes, output each as a separate block with its own insertion point.

The user will copy the output and apply it in the source repository manually.

When templates or skill files include emojis, always use them — they serve as visual cues.

## Effort Levels

Claude Code has 5 effort levels (low, medium, high, xhigh, max). Use appropriate effort per task — don't pay high-effort token costs for mechanical work.

**Defaults by task type:**
- **low**: `/plan:status`, file reading/summarization, simple search
- **medium**: `/plan:build` (task execution), `code-fixer`, `test-writer`, routine edits
- **high**: `/plan:phase` (architecture decisions), `/plan:shift`, complex debugging
- **max**: `/plan:MVP`, `/plan:feature` (requirements interviews), unfamiliar codebase deep exploration

Default to medium when unsure. Only explicitly lower effort for known-mechanical tasks.

## Output Format

**Write instructions, research, and reference material to markdown files — not the terminal.**

The user works from their IDE, not the terminal. Long blocks of text in the terminal are hard to follow, can't be bookmarked, and scroll away. Write them to markdown files at the project root (or wherever makes sense for the document type). The user will move them where needed.

**Applies to:**
- Step-by-step setup instructions (installations, configurations, troubleshooting)
- Research findings, comparisons, or analysis
- Reference guides and how-tos
- Any document longer than ~15 lines that the user will need to refer back to

**Does NOT apply to:**
- Brief status updates or answers to direct questions
- Code diffs or small inline explanations
- Single-command fixes

### Incremental Writing for Long Documents

When producing a long document (research, analysis, migration plan, audit, etc.), **write incrementally to the file as you go** — do not compose the entire document in your response and write it at the end.

**Why:** Context windows are finite. If you spend 50% of your context composing a long document in your response, you have less context available for the actual work. If context fills up before you finish writing, the document is lost.

**How:**
1. **Start with a skeleton** — write the file with headings and placeholder sections early in the process
2. **Fill sections as you complete them** — use Edit to update each section as research/work progresses
3. **Never hold more than one section's worth of content in your response** — write it to the file immediately
4. **If the compaction nudge fires**, you've already saved your work to the file — no lost research

This also applies to the `still-thinking/` directory — write research drafts there incrementally rather than composing them in one shot.

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

System modifications (permissions, package installation, process management, privilege escalation) are blocked at the kernel/policy level by the deny list in `settings.json` and `block-dangerous.py`.

**When a command is denied or fails due to permissions: stop. Do not try alternative approaches. Ask the user to handle it outside the container.**

## Secrets and Environment Variables

Secret and credential files are blocked by the settings deny list and `block-secrets.py` hook across all tools.

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

## Testing

**The user runs all test suites.** Do not run full test suites (`pytest`, `npm test`, `npx vitest`) yourself. The fish tank creates friction with test running — missing packages, version mismatches, seccomp blocks — and full-suite runs consume context with fix-rerun-fix churn. The `block-test-suite.py` hook enforces this.

**What you can do:**
- Run targeted tests on a specific file or class: `pytest path/to/test_file.py::TestClass`
- Run `pytest --collect-only -q path/to/file.py` to verify test collection

**What to ask the user to do:**
- Run full test suites and paste failures
- Run `coverage-wrapper` and `mutmut-wrapper` and paste results

**Do NOT modify `pyproject.toml` mutmut config** unless the user asks.
