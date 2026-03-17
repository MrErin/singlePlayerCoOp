---
description: Generate or update the testing document for a completed phase. Use after building to create verification steps, or after testing to record results. Pass phase number as argument or omit to review the most recently completed phase. 
allowed-tools: Read, Write
---

# Review Phase

**Skill:** Load `iterative-build`
**Read first:** `_planning/state.md`

## Steps

1. **Determine which phase to review:**
    - If argument provided: review that phase.
    - If no argument: review the most recently completed phase (status = "review").
2. **Read the phase's `plan.md` and all code created in that phase.** Use jcodemunch `get_file_outline` and `get_symbol` to efficiently review code structure and implementations.
3. **Check** the work completed in the phase you're reviewing and ensure the code meets the goal set out by the plan and utilizes best practices for the patterns implemented.
    - If a `code-reviewer` subagent is available, delegate the code quality review to it for an independent assessment against `my-style` standards
    - Research if you are uncertain about a pattern or architectural decision
    - Alert the user if problems are found
4. **Read the phase's `user_feedback.md` if it exists.**
5. **Generate or update `phase_summary.md`** in the phase directory using the `phase_summary` template from `iterative-build` references.
    - **Generate "At a Glance" section FIRST** — this is the most important section for quick understanding:
        - **One-sentence summary:** What this phase accomplishes overall
        - **Files Changed:** List each file with one-line description of changes (use `git diff` or file exploration to identify changes)
        - **Key Functions:** List each function added/modified with one-line behavior description (use jcodemunch `get_file_outline` and `get_symbol`)
        - **Behavior Changes:** User-visible changes or API/contract changes
    - **Write this early** — generate "At a Glance" first, then detailed sections
    - Use jcodemunch `search_text` to find how functions are called to understand connections
    - **Skip obvious code** — only explain what's worth explaining
6. **If `ua_testing.md` doesn't exist yet:** Generate it from the `ua_testing` template. Use **progressive disclosure** — put "Quick Smoke" tests first (5-10 min), then "Priority 1" features (15-20 min), then "Priority 2" if time permits. Don't overwhelm the user with one giant checklist.
7. **If ua_testing.md exists:** Ask the user what needs updating. Common scenarios:
    - Tests failed — document what went wrong, suggest fixes
    - User found issues — record them, adjust
    - Everything passed — mark phase complete
8. **If issues surface during review** add them to a new section of `ua_testing` rather than reporting exclusively in the terminal.
9. **Verify all phase artifacts exist** before proceeding:
	- [ ] `ua_testing.md` exists in the phase directory
	- [ ] `user_feedback.md` exists in the phase directory
	- [ ] `phase_summary.md` exists in the phase directory
	- [ ] `state.md` reflects current phase status
	- If any are missing, create them before continuing.
10. **When phase is approved:**
    - Update `state.md` — set phase status to "complete", log session
    - Update `roadmap.md` — check off the phase
    - Suggest: "Ready for next phase. Run `/plan:phase` to plan it."

## Rules

- Do not start building next phase.
- Testing docs should be practical — real steps, 15 min max.
- All phase artifacts required (ua_testing.md, user_feedback.md, phase_summary.md).

$ARGUMENTS