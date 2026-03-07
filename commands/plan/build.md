---
description: Execute the current planned phase. Reads the plan.md for the active phase and builds it task by task. Generates ua_testing.md when complete. Use after /plan:phase has been approved.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
---

# Build Current Phase
## Defaults
Load `iterative-build` and `my-style` skills. Read `_planning/state.md` before starting. No git commits.

For phases with UI/template/component work: also load the `frontend-design` skill.

For test phases: use the `test-writer` subagent for all test generation tasks.

## Steps

1. **Read the phase's `plan.md`** for task list and verify criteria. 
2. **Read `decisions.md`** for any constraints.    
3. **Read `codebase.md`** for current project structure and stack context.    
4. **Check for user modifications** — re-read all project files from previous phases. Note anything the user changed and adapt.    
5. **Execute tasks** from the plan sequentially:    
    - Follow each task's action description.
    - After each task, verify against the task's verify criteria.
    - If a task can't be completed as planned, note why and adapt.
    - **Comment maintenance:** When modifying existing code, review all comments within the modified function/block. Update or remove comments that no longer reflect the current logic. A stale comment is worse than no comment. Also scan the corresponding test file for any tests targeting renamed, removed, or gutted behavior in the modified function — flag these in `ua_testing.md` under "Possibly Obsolete Tests." Do not delete them.
6. **Verify the build:** 
    - Run the application/tests and confirm no errors
	    - If the application is not yet runnable (setup or early data layer phase), verify by running available checks instead:
		    - Dependency installation completes without errors
		    - Schema migrations run successfully
		    - Import statements resolve without errors
    - Review all new/modified code against `my-style` standards 
    - Check: functions approaching 30+ lines - evaluate whether they're doing multiple things, single responsibility, early returns 
    - Check: descriptive naming, comments explain WHY, error handling 
    - For web projects: verify semantic HTML, ARIA attributes, keyboard navigation 
    - If issues found, fix them before proceeding 
    - Add information to the Security Checklist heading of the `plan.md`, scoped to what was built in this phase. Verify that security concerns are flagged and addressed. Examples: 
	    - Inputs are validated
	    - SQL queries are parameterized
	    - Secrets are handled appropriately and never checked in to source control
	    - Error messages do not leak internal details
    - Log any issues discovered and fixes applied in the plan.md "Issues Discovered During Verification Stage" section
7. **Generate `ua_testing.md`** in the phase directory with:    
    - Summary of what was built
    - Instructions for running automated testing, if any
    - Manual testing steps to cover all functionality built in this phase
    - Expected behaviors
    - Edge cases to check
    - Phase completion checklist
8. **Update planning state:**
    - `_planning/state.md` — log what was built, set status to "review"
    - `_planning/roadmap.md` — check off the completed phase
    - `_planning/deferred.md` — add any cross-phase items noticed during this build; remove any items that were addressed
    - `_planning/codebase.md`:
        - **Setup phase:** Generate it (captures the project structure just created)
        - **Other phases:** Update only if new directories, dependencies, or architectural patterns were introduced. Skip if structure unchanged.
9. **STOP.** Output the testing checklist. Wait for user approval.

## If Build Fails Mid-Phase
1. Document what completed and what failed in `plan.md` "Issues Discovered" section
2. Do NOT attempt to roll back successful tasks unless they depend on the failed one
3. Fix the failure, re-verify from the failed task forward
4. Update state.md with interruption note

## Rules

- Follow the `my-style` skill for all code quality standards.
- Do NOT proceed to the next phase. STOP after this one.
- Do NOT make git commits.
- If the plan feels too big, tell the user and suggest splitting into multiple phases before building.
- Accessibility is not optional for web projects.

$ARGUMENTS