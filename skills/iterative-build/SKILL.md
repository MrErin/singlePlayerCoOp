---
name: iterative-build
description: Build applications in digestible phases with persistent planning state. Use for new apps, features, or multi-step development tasks. Works with /plan: commands.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Core Principle

Build in digestible phases. Maintain persistent planning state. Never build everything at once. Always stop after each phase for human review.

**CRITICAL:** Load `my-style` skill when using this one.

# Slash Commands

`/plan:interrogate` · `/plan:init` · `/plan:phase` · `/plan:build` · `/plan:status` · `/plan:review` · `/plan:debt` · `/plan:test-audit` · `/plan:archive`

If command invoked, follow its instructions. Otherwise, determine appropriate phase.

# The `_planning/` Directory

Single source of truth. Any session can read it and know exactly where things stand.

```
_planning/
├── roadmap.md              # Phase breakdown with status
├── state.md                # Current progress, session log, blockers
├── decisions.md            # Architectural decisions (append-only)
├── deferred.md             # Cross-phase flags
├── lessons.md              # Issues caught during builds (append-only)
├── codebase.md             # Stack, structure, architecture
├── requirements.md         # Current active scope
├── technical_debt.md       # Existing codebase problems
├── test_audit.md           # Test suite analysis
├── project-requirements/   # Accumulated permanent requirements
│   ├── index.md            # Dense summaries + file refs
│   ├── core.md             # Non-feature requirements
│   └── [feature].md        # Per-feature permanent requirements
├── archive/                # Frozen snapshots — NEVER MODIFY
├── phase_shift_*.md        # Requirements for inserted phases (archived after use)
└── phases/                 # Phase directories created on-demand by /plan:phase
    └── [NN-name]/
        ├── plan.md
        ├── phase_summary.md
        ├── ua_testing.md
        └── user_feedback.md
```

## Requirements Tiers

**`requirements.md`** — current active scope. Short, focused. Cleared at archive.

**`project-requirements/`** — accumulated project truth. Load `index.md` for full context. Load specific feature file only when phase touches that area.

**If `project-requirements/` doesn't exist:** work from `requirements.md` only.

## Archived Documentation

**Never modify archived documentation.** Only update:

- **Modifiable:** `state.md`, `requirements.md`, `codebase.md`, `project-requirements/`, active phase files in `phases/[NN-name]/`
- **Append-only:** `decisions.md`, `lessons.md`
- **Never touch:** `_planning/archive/` — frozen snapshots reflecting state at time of build. Modifying them creates false history.

# Phase System

## Ordering

1. Setup (greenfield only)
2. Data layer
3. Read operations
4. Write operations
5. Business logic
6. Polish

Each phase: 10-20 min review, <15 min test. If >10 tasks, split into multiple phases.

## Test Phases

**Separate phases, not tasks within implementation.**

Why: Agent that wrote implementation has same blind spots when testing.

Rules:
- Test phases receive: interface contracts, function signatures, `my-style/testing.md`
- Test phases do NOT receive: implementation conversation context (enforced by new session)
- Test phases can batch multiple implementation phases
- Business logic test phases require property-based tests
- Test phase plans MUST include an "Environment Constraints" section that lists container/environment limitations affecting test design. Load the project's CLAUDE.md and check the "Hard Limits" section when generating test phase plans.

## Phase Shifts

When requirements change mid-build or unexpected work is discovered:

1. **Run `/plan:interrogate`** — automatically detects phase shift mode when user mentions requirements change, refactoring needs, or blocked work
2. **Creates `phase_shift_requirements_phase[N].md`** — documents the trigger, scope, and approach
3. **Updates roadmap** — inserts new phase(s) and renumbers all subsequent phases
4. **Continue with `/plan:phase [N]`** — plans the new phase using the shift requirements

Typical phase shift adds 1-2 phases (implementation + optional test phase). Phase shift requirements files are archived during `/plan:archive`.

## Test Phase Execution Rules

Test phases have stricter verification requirements than implementation phases because tests that don't run are worse than no tests (they create false confidence).

1. **Per-task verification is mandatory.** After writing tests for each task, run `pytest <test_file> -v` and confirm all tests pass. If any fail:
   - If the failure is a test bug (wrong mock setup, bad assertion): fix the test
   - If the failure is an implementation bug: log it in the Issues section, do NOT fix the implementation (test phase doesn't modify source)
   - If the failure is an environment limitation (blocked syscall, missing package): log it in the Issues section and ask the user for direction

2. **Full suite check at phase end.** After all tasks are complete, run the FULL test suite (`pytest --tb=short -q`) and report:
   - Total pass/fail count
   - Any regressions from existing tests (new failures in files not touched by this phase)
   - Regressions are blockers — do not mark the phase complete

3. **Environment setup before first test.** At the start of a test phase, verify the test environment works by running `pytest --collect-only -q` on existing tests. If collection fails, resolve the environment issue before writing any tests.

4. **Helper consistency check.** After creating test helpers (Task 1 of test phases), review all helpers and document which scenarios each is designed for. When writing subsequent test tasks, reference this documentation. If multiple helpers exist for similar purposes (e.g., `mock_chat_model` vs `mock_mission_chain`), explicitly note which one to use and why.

## Context Detection

- **Greenfield:** No code → setup phase
- **Feature Addition:** Code exists → skip setup, generate `codebase.md` if missing
- **Resuming:** `_planning/` exists → read `state.md`, continue

If unclear: "I see existing code and `_planning/`. Continue previous work, add feature, or start fresh?"

# Critical Rules

- Never proceed without permission. STOP after each phase.
- Phase boundaries are strict.
- Keep phases reviewable.
- One plan per phase.
- **Incremental writes:** When generating documents (plans, audits, reviews), write to disk after each major section — not at the end. If the session ends mid-task, partial work survives. Mark documents `<!-- STATUS: DRAFT -->` at the top while in progress, replace with `<!-- STATUS: COMPLETE -->` when done. On resume, check for DRAFT files and continue from the last written section.

# Reference Files (Lazy Load)

| File | Load When |
|------|-----------|
| `references/roadmap.md` | Creating/updating roadmap |
| `references/state.md` | Creating/updating state |
| `references/decisions.md` | Creating decisions file |
| `references/lessons.md` | Creating lessons file |
| `references/phase_plan.md` | Writing a phase plan |
| `references/phase_summary.md` | Writing phase summary |
| `references/ua_testing.md` | Writing testing doc |
| `references/codebase.md` | Documenting codebase structure |

**Do NOT preload references.**

# Integration

- **my-style**: Coding standards (always)
- **post-build-review**: Final review (project end)
- **Domain skills**: Project-specific requirements

# Notes

- User has ADHD — clear structure and STOP points prevent overwhelm
- `_planning/` is memory across sessions
- Always read state.md before starting
- Always update state.md after completing
