---
description: Generate or update the testing document for a completed phase. Use after building to create verification steps, or after testing to record results. Pass phase number as argument or omit to review the most recently completed phase. 
allowed-tools: bash_tool create_file str_replace view
---

# Review Phase

## Defaults
Load `iterative-build` and `my-style` skills. Read `_planning/state.md` before starting. No git commits.

## Steps

1. **Determine which phase to review:**    
    - If argument provided: review that phase.
    - If no argument: review the most recently completed phase (status = "review").
2. **Read the phase's `plan.md` and all code created in that phase.** 
3. **Check** the work completed in the phase you're reviewing and ensure the code meets the goal set out by the plan and utilizes best practices for the patterns implemented.
    - If a `code-reviewer` subagent is available, delegate the code quality review to it for an independent assessment against `my-style` standards
    - Research if you are uncertain about a pattern or architectural decision
    - Alert the user if problems are found
4. **Read the phase's `user_feedback.md` if it exists.**
5. **If `ua_testing.md` doesn't exist yet:** Generate it with:    
    - Summary of what was built
    - Instructions for running automated tests, if they exist
    - Manual testing steps with expected outcomes
    - Edge cases to verify
    - Completion checklist
6. **If ua_testing.md exists:** Ask the user what needs updating. Common scenarios:    
    - Tests failed — document what went wrong, suggest fixes
    - User found issues — record them, adjust
    - Everything passed — mark phase complete
7. **Generate or update `phase_summary.md`** in the phase directory with: 
    - **What Was Built:** A plain-language paragraph describing what this phase accomplished — not a file list 
    - **Key Decisions:** Why things were built this way, including entries from `decisions.md` for this phase and any implicit decisions visible in the code 
    - **Complex Logic Explained:** The 2-3 most non-obvious logical flows in plain language — the parts where reading the code alone wouldn't make the "why" clear 
    - **Connection to Previous Phases:** What data or patterns from earlier phases this builds on, and what it sets up for later phases 
    - Skip obvious code (CRUD operations, config, boilerplate) — only explain what's worth explaining 
    - Keep it concise — this is a reference for maintaining your mental model, not a code walkthrough
- 9. **Verify all phase artifacts exist** before proceeding:
	- [ ] `ua_testing.md` exists in the phase directory
	- [ ] `user_feedback.md` exists in the phase directory
	- [ ] `phase_summary.md` exists in the phase directory
	- [ ] `state.md` reflects current phase status
	- If any are missing, create them before continuing.
1. **When phase is approved:**    
    - Update `state.md` — set phase status to "complete", log session
    - Update `roadmap.md` — check off the phase
    - Suggest: "Ready for next phase. Run `/plan:phase` to plan it."

## Rules

- Do NOT start building the next phase.
- Do NOT make git commits.
- Testing documents should be practical — real steps a human can follow in 15 minutes.
- All phase artifacts (ua_testing.md, user_feedback.md, phase_summary.md) are required. Do not skip any.

$ARGUMENTS