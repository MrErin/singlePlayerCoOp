---
description: Initialize a new project's _planning/ directory. Creates roadmap, state tracking, and phase structure from requirements. Use at the start of any new project or when _planning/ doesn't exist yet.
allowed-tools: Bash, Read, Write
---

# Initialize Project Planning

**Skill:** Load `iterative-build`

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
    - **Capture runtime environment:**
        - Read `.venv/pyvenv.cfg` (or equivalent) for the Python/Node version the venv targets
        - Run `python3 --version` in the container for the container's runtime version
        - If they differ, log a warning in `codebase.md` Stack section and flag it in `deferred.md`
    - Use Glob to enumerate source directories and Grep to identify key patterns
    - Read directory structure (src/ level depth, not individual files)
    - Identify key patterns: routing, state management, data flow
    - **Capture patterns & conventions:**
        - Key patterns used (repository, service layer, factory, etc.)
        - Naming conventions for files, functions, classes, constants
        - Module boundaries and responsibilities
        - Dependency flow direction
        - Import conventions and aliases
    - Check for external integrations (API calls, database connections, env vars)
    - Generate `_planning/codebase.md` from what you find — see `iterative-build/references/codebase.md` for full template
    - If greenfield, skip this step — codebase.md is generated after Phase 0 build
4. **Create `_planning/` directory** with:
    - `roadmap.md` — Phase breakdown with checkboxes. Customize phase names to match the project's actual scope. After the phase list, add a **Phase intent notes** section with a 2-3 sentence entry per phase capturing: what is built in this phase, what is explicitly excluded, and what the "done" state looks like. This section is written once at init and updated only when phases are inserted via phase shift — it is not a changelog.
    - `state.md` — Set current phase, record requirements location, start session log.
    - `decisions.md` — Empty template, ready for entries.
    - `deferred.md` — Empty template, ready for entries.
    - `lessons.md` — Empty template for capturing issues discovered during builds. See `iterative-build/references/lessons.md` for format.
    - `codebase.md` — (brownfield only, see step 3)
    - `phases/` — empty directory. Phase subdirectories are created on-demand by `/plan:phase` when planning each phase, NOT upfront.
    - `project-requirements/` — populated differently depending on project type:

    **Greenfield:** Create both files as empty templates. Nothing has shipped yet; they will be populated at the first `/plan:archive`.
    - `project-requirements/index.md` — empty template with format instructions only
    - `project-requirements/core.md` — empty template with section headings only

    **Brownfield:** Populate from the requirements and codebase analysis done in steps 1–3. Do not leave these empty.
    - `project-requirements/core.md` — extract system-wide, non-feature-specific content from `requirements.md` and `codebase.md`: data model structure (entities and relationships), auth model, non-functional constraints (performance targets, accessibility level, platform), and any architectural patterns that apply regardless of which feature is being built. Do NOT extract feature-specific behavior — that stays in `requirements.md` and will move to a feature file at archive time.
    - `project-requirements/index.md` — write one-liner summaries of everything captured in `core.md`, organized by area with a reference to `core.md`. Format: `## [Area] (→ core.md)` followed by one-liner bullets. Maximum signal per token — no prose.
    - Present both files to the user: "Review `project-requirements/` — edit directly if anything is missing or wrong." Wait for confirmation before continuing.
5. **Create `CLAUDE.md` in the project root** (or append to it if one exists) with a planning guard block:

    ```markdown
    ## Planning Workflow

    This project uses the iterative-build workflow.

    Before making any code changes — including quick fixes:
    - Load `my-style`
    - Read `_planning/state.md` — understand the active phase and what is in scope

    If you defer a UA testing item rather than fixing it, add it to `_planning/deferred.md` before the conversation ends.
    ```

    If a `CLAUDE.md` already exists, append the block under a `## Planning Workflow` heading. Do not overwrite any existing content.

6. **Create initial plan.md** for the first phase only.
7. **Output:** Once all documents are created, notify user that initialization is complete. Do not write any code.

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

- Read requirements thoroughly before generating.
- Planning only. Do not start building.
- Reference `iterative-build` skill for directory structure and formats.

$ARGUMENTS