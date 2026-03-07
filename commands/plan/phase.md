---
description: Plan a specific phase. Reads requirements and current state, then generates a detailed plan.md with tasks, verify criteria, and done conditions. Pass phase number as argument (e.g., /plan:phase 2) or omit to plan the next incomplete phase. 
allowed-tools: bash_tool create_file str_replace view
---

# Plan a Phase
## Defaults
Load `iterative-build` and `my-style` skills. No git commits.

## Steps

1. **Read current state:**    
    - `_planning/state.md` — what phase are we on?
    - `_planning/roadmap.md` — what's the phase breakdown?
    - `_planning/decisions.md` — any constraints to honor?
    - `_planning/codebase.md` — understand existing structure
2. **Determine which phase to plan:**    
    - If argument provided: plan that phase number.
    - If no argument: find the next incomplete phase from roadmap.
3. **Read requirements** from the path recorded in `state.md`.    
4. **Read previous phase artifacts** — check what was built and any testing and user feedback notes. Initiate discussion with user to resolve issues and discuss questions if notes are present from previous phase.
5. **Research before planning tasks:**
    - Libraries/packages that provide needed functionality
    - Best practices and common patterns for the approach being used
    - Relevant API documentation or framework guides
    - Accessibility requirements for any UI components planned
    - Known pitfalls or gotchas with the chosen approach
    - Check for security concerns relevant to what's being built
    - Document findings in the plan.md under the "Research Notes" section
    - Flag anything uncertain for user review
6. **Generate `plan.md`** in the phase directory (e.g., `_planning/phases/02-read-ops/plan.md`) with:    
    - Clear goal statement
    - Specific tasks with files, action, verify, and done-when criteria
    - Dependencies on previous phases
7. **For implementation phases that will have a corresponding test phase:** Generate the **Interface Contracts** section in the plan. For each public function/method planned:
    - Signature with types
    - Purpose (one sentence)
    - Invariants (rules that always hold)
    - Valid inputs and constraints
    - Error conditions and what the errors look like
    - Edge cases to test — each must include the expected return value, not just a description (e.g., "empty list input → returns `0`, not an error" not just "empty list")
    - These contracts are written from requirements and expected behaviors — not from implementation code, which doesn't exist yet. DO read existing code to understand available interfaces and patterns.
8. **Check phase size:** If the plan has more than ~10 tasks, it's too big for one phase. Split the work into multiple sequential phases and plan only the first one now. Inform the user of the proposed split and update the `roadmap.md` accordingly.
9. **For test phases:** The plan should reference:
    - Which implementation phases are being tested
    - The interface contracts from those phases' plans
    - Which functions are candidates for property-based testing (pure functions with clear invariants)
    - The Test Rules from `testing.md`
10. **Update `state.md`** — set current phase and status to "planning".
11. **Output:** Show the plan. Ask for approval or adjustments before building. 

## Rules

- Do NOT start building. Planning only.
- Do NOT make git commits.
- Keep tasks specific — each should target identifiable files.
- One plan per phase. If the work is too big, split into multiple phases.
- Interface contracts are required for implementation phases that will have a test phase.
- Reference the `iterative-build` skill for plan.md format.

$ARGUMENTS