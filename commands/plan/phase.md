---
description: Plan a specific phase. Reads requirements and current state, then generates a detailed plan.md with tasks, verify criteria, and done conditions. Pass phase number as argument (e.g., /plan:phase 2) or omit to plan the next incomplete phase.
allowed-tools: Read, Write, Edit
---

# Plan a Phase

**Skills:** Load `iterative-build`, `my-style`
**No git commits.** User controls all git operations.

## Steps

1. **Read current state:**
    - `_planning/state.md` — what phase are we on?
    - `_planning/roadmap.md` — what's the phase breakdown?
    - `_planning/decisions.md` — any constraints to honor?
    - `_planning/codebase.md` — understand existing structure
    - `_planning/lessons.md` — avoid repeating known pitfalls
2. **Determine which phase to plan:**
    - If argument provided: plan that phase number.
    - If no argument: find the next incomplete phase from roadmap.
3. **Read requirements**: `_planning/requirements.md` (current feature scope). If this phase integrates with or modifies existing functionality, also read `_planning/project-requirements/index.md` and load any specific detail file that is directly relevant to this phase's work.    
4. **Read previous phase artifacts** — check what was built and any testing and user feedback notes. Initiate discussion with user to resolve issues and discuss questions if notes are present from previous phase.
5. **Check `_planning/deferred.md`** for any items targeting this phase or a relevant work area. Incorporate them into the plan explicitly — note their origin so the user knows they're being surfaced from a previous phase's flag.
6. **Research before planning:** Libraries, patterns, API docs, accessibility, security, and pitfalls relevant to this phase. Document findings in plan.md under "Research Notes." Flag uncertainties for user review.
7. **Generate `plan.md`** in the phase directory (e.g., `_planning/phases/02-read-ops/plan.md`) with:
    - Clear goal statement
    - Specific tasks with files, action, verify, and done-when criteria
    - Dependencies on previous phases
8. **For implementation phases that will have a corresponding test phase:** Generate the **Interface Contracts** section in the plan. For each public function/method planned:
    - Signature with types
    - Purpose (one sentence)
    - Invariants (rules that always hold)
    - Valid inputs and constraints
    - Error conditions and what the errors look like
    - Edge cases to test — each must include the expected return value, not just a description (e.g., "empty list input → returns `0`, not an error" not just "empty list")
    - These contracts are written from requirements and expected behaviors — not from implementation code, which doesn't exist yet. DO read existing code to understand available interfaces and patterns.
9. **Check phase size:** If the plan has more than ~10 tasks, it's too big for one phase. Split the work into multiple sequential phases and plan only the first one now. Inform the user of the proposed split and update the `roadmap.md` accordingly.
10. **For test phases:** The plan should reference:
    - Which implementation phases are being tested
    - The interface contracts from those phases' plans
    - Which functions are candidates for property-based testing (pure functions with clear invariants)
    - The Test Rules from `testing.md`
11. **Update `state.md`** — set current phase and status to "planning".
12. **Output:** Show the plan. Ask for approval or adjustments before building.

## Rules

- Planning only. Do not start building.
- Keep tasks specific — target identifiable files.
- One plan per phase. If too big, split into multiple phases.
- Interface contracts required for implementation phases with test phases.
- Reference `iterative-build` skill for plan.md format.

## Do Not

- Do not generate tasks for work outside this phase's scope
- Do not assume technology choices — research first, flag options for user
- Do not skip interface contracts for implementation phases that have test phases

$ARGUMENTS