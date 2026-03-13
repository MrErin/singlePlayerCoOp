---
description: Archive a completed feature or initial build. Moves phase documents to archive, extracts permanent requirements into project-requirements/, and clears the workspace for the next feature. Run after all phases in the current roadmap are complete and reviewed.
allowed-tools: Bash, Read, Write
---

# Archive Feature

**Skill:** Load `iterative-build`

## Steps

1. **Confirm readiness**: Check `roadmap.md` — all phases must be complete (all checked). If any are incomplete, warn the user and ask whether to proceed anyway.

2. **Get archive name**: Ask the user for a short slug to identify this archive (e.g., `mvp`, `feature-user-auth`, `feature-xp-system`). This becomes the subdirectory name.

3. **Create archive**: `_planning/archive/[name]/`
   - Copy all phase directories from `_planning/phases/` → `_planning/archive/[name]/phases/`
   - Copy `_planning/roadmap.md` → `_planning/archive/[name]/roadmap.md`
   - Copy `_planning/requirements.md` → `_planning/archive/[name]/requirements.md`
   - Copy any `phase_shift_requirements_*.md` files → `_planning/archive/[name]/`

4. **Extract permanent requirements**:
   - Read `_planning/requirements.md`
   - Read any `phase_shift_requirements_*.md` files — merge their requirements into the permanent record
   - Read `_planning/project-requirements/index.md` if it exists (understand what's already captured)
   - Read `_planning/decisions.md` for any architectural decisions that imply permanent behaviors
   - Identify what is permanent: capabilities the system now has, data model facts, business rules, non-functional constraints that will always apply
   - Skip: acceptance criteria, phase-specific implementation notes, "how to test X", transitional requirements
   - Write permanent requirements to `_planning/project-requirements/[name].md`
   - If `project-requirements/` does not exist yet, create it. Also create `core.md` if `requirements.md` contains non-feature requirements (data model, auth model, constraints that apply system-wide).
   - Add one-liner entries to `_planning/project-requirements/index.md` for everything written, in this format:
     ```
     ## [Area Name] (→ [name].md)
     - [one-line summary of permanent behavior]
     - [one-line summary of permanent behavior]
     ```

5. **Present the extraction for review**: Show the user what was written to `project-requirements/[name].md` and what lines were added to `index.md`. Say: "Review these before I clear the workspace. Edit the files directly if anything is missing or wrong."
   - **STOP and wait for user confirmation before continuing.**

6. **Clear the workspace** (only after user confirms step 5):
   - Delete any `phase_shift_requirements_*.md` files (already archived in step 3)
   - Overwrite `_planning/requirements.md` with an empty placeholder:
     ```markdown
     # Requirements

     _No active feature in progress. Run /plan:interrogate to begin requirements gathering for the next feature._
     ```
   - Delete the contents of `_planning/phases/` (already archived in step 3)
   - Reset `_planning/roadmap.md` to an empty template (phases moved to archive)
   - Update `_planning/state.md`: log the archive event, set status to "archived — ready for next feature"

7. **Output**: Confirm archive location, confirm project-requirements/ was updated, and suggest next step: "Run `/plan:interrogate` to start requirements gathering for the next feature."

## Rules

- Do not clear workspace before user confirms extraction
- Do not archive `decisions.md`, `deferred.md`, or `codebase.md` — these stay at root
- Keep `index.md` entries dense: one line per requirement
- If `deferred.md` has open items, surface them for user decision
- For new `project-requirements/`, scan `decisions.md` and phase summaries for additional permanent behaviors

$ARGUMENTS
