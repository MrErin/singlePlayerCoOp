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
   - Copy `_planning/lessons.md` → `_planning/archive/[name]/lessons.md` (historical record; the root copy is NOT deleted — lessons accumulate across features)

4. **Extract permanent requirements**:
   - Read `_planning/requirements.md`
   - Read any `phase_shift_requirements_*.md` files — merge their scope and requirements into the permanent record
   - Read all `phase_summary.md` files across `_planning/phases/` — the "Behavior Changes" section captures user-visible and API/contract changes that may not appear in requirements.md
   - Read `_planning/project-requirements/index.md` if it exists (understand what's already captured)
   - Read `_planning/decisions.md` for architectural decisions that imply permanent behaviors
   - Identify what is permanent: capabilities the system now has, data model facts, business rules, non-functional constraints that will always apply
   - Skip: acceptance criteria, phase-specific implementation notes, "how to test X", transitional requirements
   - Write permanent requirements to `_planning/project-requirements/[name].md`
   - If `project-requirements/` does not exist yet, create it. Also create `core.md` if `requirements.md` contains non-feature requirements (data model, auth model, constraints that apply system-wide).
   - Add one-liner entries to `_planning/project-requirements/index.md` for everything written:
     ```
     ## [Area Name] (→ [name].md)
     - [one-line summary of permanent behavior]
     - [one-line summary of permanent behavior]
     ```

5. **Triage deferred items**: Read `_planning/deferred.md`.
   - If there are open items, present them to the user: "These items were deferred during this feature. For each one: carry forward to next feature, promote to a phase shift via `/plan:shift`, or close as won't-fix."
   - Do NOT close or remove open items automatically — the user decides.
   - Once the user has made decisions, update `deferred.md` to reflect them (remove won't-fix items, leave carry-forwards as open).

6. **Update backlog statuses**: If `_planning/backlog/` exists:
   - Read the archived `requirements.md` for any `**Incorporates:**` lines listing backlog IDs (e.g., `F-008, B-003, Q-003`)
   - For each referenced ID, find its entry in the corresponding catalog file and update its status from `planned` to `shipped`
   - Add a note to each entry: `Shipped in [archive-slug] (YYYY-MM-DD)`
   - If `_planning/backlog/` doesn't exist, skip this step silently.

7. **Present the extraction for review**: Show the user what was written to `project-requirements/[name].md` and what lines were added to `index.md`. If backlog items were updated in step 6, include them: "Updated backlog items to shipped: F-008, B-003, Q-003." Say: "Review these before I clear the workspace. Edit the files directly if anything is missing or wrong."
   - **STOP and wait for user confirmation before continuing.**

8. **Clear the workspace** (only after user confirms step 7):
   - Delete `_planning/requirements.md`
   - Reset `_planning/roadmap.md` to an empty template (phases moved to archive)
   - Delete the `_planning/phases/` directory
   - Delete any `phase_shift_requirements_*.md` files from `_planning/` root
   - Update `_planning/state.md`: clear the current phase, wipe the session log, set status to "archived — ready for next feature", and add a one-line entry noting the archive slug and date
   - Leave `decisions.md`, `deferred.md`, `codebase.md`, and `lessons.md` at root — these persist across features unchanged

9. **Output**: Confirm archive location, confirm `project-requirements/` was updated, and suggest next step: "Run `/plan:MVP` for a new project or `/plan:feature` for the next feature on this codebase."

## Rules

- Do not clear workspace before user confirms extraction (step 7)
- `decisions.md`, `deferred.md`, `codebase.md`, and `lessons.md` stay at root and are never deleted — only `lessons.md` gets an archive copy
- Phase summaries are required reading in step 4 — they capture behavior changes the requirements doc may not mention
- Deferred triage (step 5) must happen before workspace clear — do not skip it even if deferred.md looks empty
- Keep `index.md` entries dense: one line per requirement
- For new `project-requirements/`, scan `decisions.md` and phase summaries for additional permanent behaviors

$ARGUMENTS
