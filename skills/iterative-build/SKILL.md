---
name: iterative-build 
description: Build applications in digestible phases with persistent planning state. Combines spec-driven planning artifacts with human-controlled phase gates. Use when creating new apps, adding features, or working on multi-step development tasks. Supports Python, TypeScript, React, and fullstack projects. Works with slash commands in .claude/commands/plan/. 
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Core Principle

Build applications in digestible phases. Maintain persistent planning state that survives session changes and Agent switches. Never build everything at once. Always stop after each phase for human review.

**CRITICAL**: This skill is used in conjunction with the `my-style` skill. Load that skill every time you utilize this one.

# Slash Commands

This skill works with commands in `.claude/commands/plan/`:

| Command             | Purpose                                                                                    |
|---------------------|--------------------------------------------------------------------------------------------|
| `/plan:interrogate` | Discuss and synthesize or clarify requirements for project or feature                      |
| `/plan:init`        | Initialize `_planning/` directory and generate roadmap                                     |
| `/plan:phase`       | Plan the next (or specified) phase                                                         |
| `/plan:build`       | Execute the current planned phase                                                          |
| `/plan:status`      | Read state, show progress, suggest next action                                             |
| `/plan:review`      | Generate testing doc for completed phase                                                   |
| `/plan:debt`        | Generate document detailing technical debt of an existing codebase                         |
| `/plan:test-audit`  | Generate investigation cards for reviewing/improving test suite                            |
| `/plan:archive`     | Archive all _planning documentation from a given phase and update the project requirements |

If a command is invoked, follow its instructions. If the user says "use iterative-build" without a command, use this skill directly and determine the appropriate phase.

# The `_planning/` Directory

All planning state lives in `_planning/` at the project root. This is the single source of truth for project progress. Any Agent, any session can read it and know exactly where things stand.

## Directory Structure

```
_planning/
├── roadmap.md              # Phase breakdown with status markers
├── state.md                # Current progress, session log, blockers
├── decisions.md            # Architectural decisions with rationale (append-only, permanent)
├── deferred.md             # Cross-phase flags: items noticed now, relevant to a future phase
├── codebase.md             # Stack, structure, architecture (generated)
├── requirements.md         # Current active scope (this feature or initial build)
├── technical_debt.md       # Details of existing problems in codebase
├── test_audit.md           # Test suite analysis and recommendations
├── project-requirements/   # Accumulated permanent requirements across all shipped features
│   ├── index.md            # Dense one-liner per area + file refs; load for project context
│   ├── core.md             # Non-feature requirements: data model, auth, constraints
│   └── [feature-name].md  # Per-feature permanent requirements; created at archive time
├── archive/                # Frozen snapshots of completed work
│   └── [feature-name]/
│       ├── requirements.md # Snapshot of requirements.md at archive time
│       ├── roadmap.md      # Snapshot of roadmap at archive time
│       └── phases/...
└── phases/
    └── [NN-phase-name]/    # One directory per phase
        ├── plan.md         # What will be built (task list)
        ├── phase_summary.md # What was built (post-build)
        ├── ua_testing.md   # UAT verification steps + results
        └── user_feedback.md # User comments after code review
```

## Requirements Location

**Two tiers, two different jobs:**

`requirements.md` is the **current active scope** — what is being built right now. It is short and focused. Created or updated by `/plan:interrogate`. Read by all phase commands. Cleared by `/plan:archive` when a feature ships.

`project-requirements/` is the **accumulated project truth** — permanent behaviors extracted from every shipped feature. Load `index.md` when you need full project context (integration work, brownfield features, understanding what already exists). Load a specific feature file only if the current work directly touches that area. Do not load these files by default in routine phases.

**When `project-requirements/` does not exist:** the project has not yet archived its first feature. Work from `requirements.md` only.

## Requirements as Living Document

`requirements.md` is always the current feature scope. It gets cleared at archive time once its permanent behaviors have been extracted into `project-requirements/`.

`project-requirements/index.md` is the living project-wide record. It grows at each archive. When a new feature changes behavior already captured in `project-requirements/`, update the relevant detail file and `index.md` at archive time.

## Archive Directory

The archive directory exists to preserve historical documentation. Do not load or read items in the directory unless the user requests it.

Archiving is done via `/plan:archive`. When archiving:

- Phase directories are moved to `archive/[name]/phases/`
- `requirements.md` is copied to the archive as a snapshot, then cleared at root
- `roadmap.md` is copied to the archive as a snapshot, then reset at root
- `decisions.md` is never archived — append-only, permanent
- `deferred.md`, `codebase.md` stay at root — they are continuous across features
- Permanent requirements are extracted into `project-requirements/` before clearing `requirements.md`

# Document Formats

Markdown template files for all document formats are in the `references` directory of the `iterative-build` skill.

- **Roadmap** (`roadmap.md`): Phase breakdown with checkboxes
- **State** (`state.md`): Current phase, session log, blockers
- **Decisions** (`decisions.md`): Permanent record of architectural and design decisions — why unconventional choices were made, what alternatives were rejected, what constraints shaped the design. Append-only, never archived or deleted. If a decision is superseded, note that in a follow-up entry rather than removing the original.
- **Deferred** (`deferred.md`): Items noticed during a phase that need attention in a future phase. Format: `- [ ] **Phase N** *(noted in Phase X)*: description`. Use "before [area]" if the target phase isn't known. Remove entries once addressed — this file should stay lean.
- **Project Requirements Index** (`project-requirements/index.md`): Dense one-liner summaries of all permanent requirements organized by area, with references to detail files. Format: `## [Area] (→ [file].md)` followed by one-liner bullets. Load this when you need full project context. Never pad it — maximum signal per token.
- **Project Requirements Detail** (`project-requirements/core.md`, `project-requirements/[feature-name].md`): Full permanent requirements for a given area. `core.md` holds non-feature requirements (data model, auth, constraints). Feature files hold per-feature permanent behaviors. Load only when the current phase directly touches that area.
- **Codebase** (`codebase.md`): Generated during `/plan:init` (brownfield) or after Phase 0 (greenfield). Updated when structure changes significantly. Answers "what exists and how is it organized."
- **Plan** (`phase_plan.md`): Tasks targeting identifiable files with verify/done criteria. "Issues Discovered During Verification Stage" filled out after code is written if iterations needed.
- **Testing** (`ua_testing.md`): Verification steps to be performed by user
- **User Feedback** (`user_feedback.md`): After resolving issues, check boxes and note changes in `decisions.md`
- **Summary** (`phase_summary.md`): Post-build description of what was accomplished

# Phase System

## Ordering Principles

Phases follow a logical dependency order. The specific number of phases is determined by the project's scope, not a fixed template. A small project might need 4 phases. A complex one might need 12.

The ordering constraint is:

1. **Setup** (greenfield only) — dependencies, config, directory structure
2. **Data layer** — schema, models, types, seed data
3. **Read operations** — queries, GET endpoints, display components
4. **Write operations** — create/update/delete, forms, validation
5. **Business logic** — calculations, rules, aggregations
6. **Polish** — styling, accessibility, error handling, responsive design

Within this order, scope each phase to be reviewable in 10-20 minutes and testable in under 15 minutes. If a logical area of work has more than ~10 tasks, split it into multiple sequential phases rather than cramming it into one.

**Example — a fitness tracking app might have:**

```
Phase 1: Project setup
Phase 2: Schema and models
Phase 3: Exercise read operations
Phase 4: User CRUD
Phase 5: Exercise logging and validation
Phase 6: Tests for phases 3-5
Phase 7: XP calculation engine
Phase 8: Tests for phase 7 (includes property-based)
Phase 9: Dashboard and stats display
Phase 10: Styling and accessibility
```

Phase names are descriptive of the actual work, not generic labels.

## Test Phases

Test phases are separate phases, not tasks within implementation phases. This is a structural requirement, not a preference.

**Why:** The agent that wrote the implementation has the same blind spots when writing tests for it. A test phase runs in a **new session**, ensuring the agent works from interface contracts rather than implementation memory.

**Rules for test phases:**

- Test phases receive: interface contracts from the implementation phase's plan, function signatures from the built code, and the `my-style/testing.md` rules
- Test phases do NOT receive: implementation phase conversation context (enforced by new session)
- Test phases can batch — one test phase can cover multiple preceding implementation phases
- Test phases are not needed for setup or data layer phases (phases where tests are optional)
- Business logic test phases must include property-based tests (Hypothesis/fast-check) for pure calculation functions

**Interface contracts** are generated during implementation phase planning (in `/plan:phase`). They document each public function's signature, purpose, invariants, valid inputs, error conditions, and edge cases. These contracts are the source of truth for test design.

## Phase-Specific Skills

- **Phases building UI** (read ops with display, write ops with forms, polish): Load the `frontend-design` skill alongside `my-style`.
- **Business logic and Test phases:** Load `my-style` references/testing.md. Note property-based test candidates.
- **After setup phase:** Generate `_planning/codebase.md`.

**After every phase: STOP. Wait for explicit approval before continuing.**

# Before Each Phase

Automatically and silently:

1. Read `state.md` for current progress
2. Read `roadmap.md` for phase context
3. Read `codebase.md` for project structure and stack context
4. Read plan and summary files from previous phases
5. Check if user modified any code since last phase
6. Read `decisions.md` for constraints
7. Read `deferred.md` — note any items targeting this phase
8. If this phase integrates with or modifies existing functionality, read `project-requirements/index.md`. Load specific detail files only if the current phase directly touches that area.
9. Adapt plan to incorporate changes

# After Each Phase

1. Create `ua_testing.md` in the phase directory
2. Create `user_feedback.md` in the phase directory
3. Update `state.md` with completion status and session log
4. Update `roadmap.md` checkbox
5. Update `deferred.md` — add any cross-phase items noticed during this phase; remove any that were addressed
6. If new directories, dependencies, or architectural patterns were introduced, update `codebase.md`
7. Output completion message with testing checklist
8. **STOP completely. Wait for explicit approval to continue.**

All three artifacts (ua_testing.md, user_feedback.md, phase_summary.md) are required for every phase. Do not skip any.

# Feature Additions

When adding features to an existing project:

1. Check for `_planning/` directory — create if missing
2. If `codebase.md` doesn't exist, generate it by reading the existing project
3. Create new `phases` directory at `_planning` root to store current work. This will be archived after feature is complete.
4. Determine which phases are needed and in what order
5. Follow same plan → build → review → stop cycle
6. Track in `state.md` as feature work

# Context Detection

- **Greenfield:** No existing code → start with setup phase
- **Feature Addition:** Existing code → skip setup, read structure, generate `codebase.md` if missing
- **Resuming Work:** `_planning/` exists → read `state.md`, continue from current phase

**If unclear, ask:** "I see existing code and a `_planning` directory. Are we continuing previous work, adding a new feature, or starting fresh?"

# Critical Rules

- **Never proceed without permission.** STOP after each phase. Wait for user to invoke next phase.
- **Never make git commits.** No `git add`, `git commit`, or `git push`. User controls all git operations.
- **Phase boundaries are strict.** Don't add things from the next phase. If unsure, put it in a later phase.
- **Keep phases reviewable.** Each phase should take 10-20 minutes to review and under 15 minutes to test. If too big, split into multiple phases.
- **One plan per phase.** If the work is too big for one plan, it's too big for one phase.

# Code Quality

Follow the `my-style` skill for all coding standards. For web projects, verify semantic HTML, ARIA attributes, and keyboard navigation. Accessibility is not optional.

# Integration with Other Skills

- **my-style**: Coding standards (always applies)
- **frontend-design**: UI/component quality (phases building UI)
- **post-build-review**: Final review generation (end of project)
- **Domain skills**: Project-specific requirements

# Notes for Any Agent Reading This

- User has ADHD — clear structure and STOP points prevent overwhelm
- Phases are about pacing and understanding, not speed
- The `_planning/` directory is your memory across sessions
- Always read state.md before starting work
- Always update state.md after completing work
- Never make git commits
- When in doubt, stop and ask