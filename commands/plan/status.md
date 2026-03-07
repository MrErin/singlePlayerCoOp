---
description: Check project progress and suggest next action. Reads all planning state and provides a clear summary. Use when resuming work, switching sessions, or unsure where things stand. 
allowed-tools: bash_tool view
---

# Check Project Status
## Defaults
Load `iterative-build` skill. No git commits.

## Steps

1. **Read all planning state:**
    - `_planning/state.md` — current phase, status, blockers
    - `_planning/roadmap.md` — overall progress
    - `_planning/requirements.md` — current feature scope
    - `_planning/decisions.md` — key decisions made
    - `_planning/deferred.md` — cross-phase flags
    - `_planning/codebase.md` — stack and structure context
    - `_planning/technical_debt.md` — known technical debt issues
    - `_planning/project-requirements/index.md` — if it exists, note how many features have been archived
2. **Check the current phase directory** for existing artifacts (plan.md, ua_testing.md).   
3. **Output a brief status report:**    
	- Project name and stack (from codebase.md)
    - Overall progress (e.g., "3 of 5 phases complete")
    - Current phase and its status
    - Any blockers or open questions
    - Open deferred items (if any) — list them so the user can see what's been flagged for upcoming phases
    - If all phases are complete, surface this: "All phases complete — consider running `/plan:archive` to archive this feature."
    - **Suggested next action** (e.g., "Run /plan:phase 3" or "Run /plan:build to execute phase 2")
4. **If `_planning/` doesn't exist:** Tell the user to run `/plan:init` first.   
5. **If `codebase.md` is missing but other planning files exist:** Note this and suggest the user run `/plan:init` to generate it.   

## Rules

- Read only. Do NOT modify any files.
- Do NOT start building anything.
- Keep the output concise — this is a status check, not a report.

$ARGUMENTS