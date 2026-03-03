---
description: Initialize a new project's _planning/ directory. Creates roadmap, state tracking, and phase structure from requirements. Use at the start of any new project or when _planning/ doesn't exist yet.
allowed-tools: bash_tool create_file str_replace view
---

# Initialize Project Planning

## Defaults
Load `iterative-build` and `my-style` skills. No git commits.

## Steps

1. **Find requirements:** Ask the user where requirements live, or check common locations:
	- `requirements.md`
    - `_planning/requirements.md`
2. **Detect project type:**
    - No existing code → Greenfield (phases 0-5)
    - Existing code → Brownfield / Feature addition (skip phase 0, scope phases to feature)
3. **If brownfield — map the codebase:**
    - Read package.json / requirements.txt / Cargo.toml for stack and dependencies
    - Read directory structure (src/ level depth, not individual files)
    - Identify key patterns: routing, state management, data flow
    - Check for external integrations (API calls, database connections, env vars)
    - Generate `_planning/codebase.md` from what you find
    - If greenfield, skip this step — codebase.md is generated after Phase 0 build
4. **Create `_planning/` directory** with:
    - `roadmap.md` — Phase breakdown with checkboxes. Customize phase names to match the project's actual scope.
    - `state.md` — Set current phase, record requirements location, start session log.
    - `decisions.md` — Empty template, ready for entries.
    - `codebase.md` — (brownfield only, see step 3)
    - `phases/` subdirectories for each planned phase.
5. **Create initial plan.md** for the first phase only.    
6. **Output:** Once all documents are created, notify user that initialization is complete. Do not write any code.    

## Rules

- Read the requirements thoroughly before generating anything.
- Do NOT start building. Planning only.
- Do NOT make git commits.
- Reference the `iterative-build` skill for directory structure and document formats.

$ARGUMENTS