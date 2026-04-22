---
description: Archive a completed feature or initial build. Moves phase documents to archive, extracts permanent requirements into project-requirements/, cycles decisions into project-requirements or archive, and clears the workspace for the next feature. Run after all phases in the current roadmap are complete and reviewed.
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

5. **Cycle decisions**: Read `_planning/decisions.md`. For each entry, classify it and act:

   | Decision type | Where it goes | Prune from decisions.md? |
   |---|---|---|
   | Became a permanent requirement (behavior the system now has) | `project-requirements/[name].md` (already extracted in step 4) | Yes |
   | Architectural constraint (how things are built, applies system-wide) | `project-requirements/core.md` — add to existing constraints section or create one | Yes |
   | Rejected alternative / scope cut (what the system is NOT) | `project-requirements/core.md` — add to a "Scope Exclusions" section (create if absent) | Yes |
   | Trade-off accepted for current feature only (not a permanent constraint) | `_planning/archive/[name]/decisions.md` — copy for historical reference | Yes |
   | Active undecided item (still relevant to upcoming work) | Keep in `decisions.md` | No |

   After classification:
   - Write all prunable decisions to their destinations
   - Copy the full `decisions.md` to `_planning/archive/[name]/decisions.md` (historical record, like lessons.md)
   - Reset `decisions.md` to empty template — only "active undecided" entries survive

   **Why:** `decisions.md` is read by every `/plan:*` command and the `code-reviewer` agent. Uncapped growth wastes tokens on every invocation. Decisions that have been codified into `project-requirements/` are redundant at best and stale at worst.

6. **Triage deferred items**: Read `_planning/deferred.md`.
   - If there are open items, present them to the user: "These items were deferred during this feature. For each one: carry forward to next feature, promote to a phase shift via `/plan:shift`, or close as won't-fix."
   - Do NOT close or remove open items automatically — the user decides.
   - Once the user has made decisions, update `deferred.md` to reflect them (remove won't-fix items, leave carry-forwards as open).

7. **Update backlog statuses**: If `_planning/backlog/` exists:
   - Read the archived `requirements.md` for any `**Incorporates:**` lines listing backlog IDs (e.g., `F-008, B-003, Q-003`)
   - For each referenced ID, find its entry in the corresponding catalog file and update its status from `planned` to `shipped`
   - Add a note to each entry: `Shipped in [archive-slug] (YYYY-MM-DD)`
   - If `_planning/backlog/` doesn't exist, skip this step silently.

8. **Present the extraction for review**: Show the user what was written to `project-requirements/[name].md` and what lines were added to `index.md` and `core.md`. If backlog items were updated in step 7, include them: "Updated backlog items to shipped: F-008, B-003, Q-003." If decisions were cycled in step 5, include a summary: "Moved N decisions to project-requirements, archived M as feature-specific trade-offs, kept K as active." Say: "Review these before I clear the workspace. Edit the files directly if anything is missing or wrong."
   - **STOP and wait for user confirmation before continuing.**

9. **Clear the workspace** (only after user confirms step 8):
   - Delete `_planning/requirements.md`
   - Reset `_planning/roadmap.md` to an empty template (phases moved to archive)
   - Delete the `_planning/phases/` directory
   - Delete any `phase_shift_requirements_*.md` files from `_planning/` root
   - Update `_planning/state.md`: clear the current phase, wipe the session log, set status to "archived — ready for next feature", and add a one-line entry noting the archive slug and date
   - Leave `deferred.md`, `codebase.md`, `lessons.md`, and `audit-scorecard.md` at root — these persist across features unchanged
   - `decisions.md` is reset to empty template by step 5 (only "active undecided" entries survive)
   - If `_planning/audit-review.md` or `_planning/audit-auto.md` exist, copy them to `_planning/archive/[name]/` before clearing (the user may have already deleted them — skip silently if absent)

10. **Output**: Confirm archive location, confirm `project-requirements/` was updated, and suggest next step: "Run `/plan:MVP` for a new project or `/plan:feature` for the next feature on this codebase."

## Rules

- Do not clear workspace before user confirms extraction (step 8)
- `decisions.md` is **cycled at archive** — codified decisions move to `project-requirements/`, feature-specific trade-offs archive with the feature, only active undecided items survive into the next cycle
- `deferred.md`, `codebase.md`, and `lessons.md` stay at root and are never deleted — only `lessons.md` gets an archive copy
- Phase summaries are required reading in step 4 — they capture behavior changes the requirements doc may not mention
- Deferred triage (step 6) must happen before workspace clear — do not skip it even if deferred.md looks empty
- Keep `index.md` entries dense: one line per requirement
- For new `project-requirements/`, scan `decisions.md` and phase summaries for additional permanent behaviors

$ARGUMENTS
