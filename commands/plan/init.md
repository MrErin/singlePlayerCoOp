---
description: Initialize a new project's _planning/ directory. Creates roadmap, state tracking, and phase structure from requirements. Use at the start of any new project or when _planning/ doesn't exist yet.
allowed-tools: Bash, Read, Write
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
    - `_planning/` exists but no `project-requirements/` → Upgrade Planning (see section below)
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
    - `deferred.md` — Empty template, ready for entries.
    - `project-requirements/index.md` — Empty template with format instructions.
    - `project-requirements/core.md` — Empty template for non-feature requirements.
    - `codebase.md` — (brownfield only, see step 3)
    - `phases/` subdirectories for each planned phase.
5. **Create initial plan.md** for the first phase only.    
6. **Output:** Once all documents are created, notify user that initialization is complete. Do not write any code.    

## Upgrade Planning Mode

**Triggered when:** `_planning/` exists with content but `project-requirements/` does not.

This is a retroactive setup — applying the two-tier requirements structure to an existing project. Do not regenerate any planning documents that already exist.

**Steps:**

1. Read everything in `_planning/`: `requirements.md`, `decisions.md`, `codebase.md`, `state.md`, `roadmap.md`, any phase summaries, and any files in `archive/`.
2. Create `_planning/project-requirements/` directory.
3. **Build `core.md`**: Extract non-feature requirements from what you've read — data model structure, auth model, non-functional constraints (performance, accessibility, platform), anything that applies system-wide regardless of feature. Write to `project-requirements/core.md`.
4. **Build feature files**: For each archived feature found in `archive/`, extract its permanent behaviors and write to `project-requirements/[feature-name].md`.
5. **If `requirements.md` has active content** (current in-progress feature): leave it as-is — it represents the current scope. Note to the user that it will be extracted at the next `/plan:archive`.
6. **Build `index.md`**: Write one-liner summaries of everything captured, organized by area with file references.
7. Present the created files for user review. Say: "Review `project-requirements/` — edit any file directly if something is wrong or missing."

**STOP. Do not modify any existing planning documents.**

## Rules

- Read the requirements thoroughly before generating anything.
- Do NOT start building. Planning only.
- Do NOT make git commits.
- Reference the `iterative-build` skill for directory structure and document formats.

$ARGUMENTS