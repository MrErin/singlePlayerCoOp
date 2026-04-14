---
description: Execute the current planned phase. Reads the plan.md for the active phase and builds it task by task. Use after /plan:phase has been approved. Supports /plan:build [phase] for full phase or /plan:build [phase].[task] (e.g., /plan:build 3.2) for single-task execution.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
---

# Build Current Phase

**Skill:** Load `iterative-build`
**Read first:** `_planning/state.md`

For phases with UI/template/component work: also load the `frontend-design` skill.

For test phases: use the `test-writer` subagent for all test generation tasks. If test-writer flags implementation bugs, follow the "If Test-Writer Flags Implementation Bugs" section below before proceeding to step 6.

## Tests in Non-Test Phases

Polish, bugfix, and implementation phases may include tests. These are **inline tests**, not a dedicated test phase.

**Rules:**
- **Substantial test work (>5 tests or new test file):** Delegate to `test-writer` subagent
- **Minor test additions (1-2 tests):** Write inline, but place in existing test files per `my-style` testing standards
- **Never create phase-named test files** — `test_phaseN_*.py` indicates the agent didn't check existing test structure

If the phase plan includes "write tests for X" and X is a substantial feature, treat it as a test-writer task even though it's not a dedicated test phase.

## Argument Modes

The command accepts arguments in two formats:
- **No argument or phase number only:** Build the entire phase (e.g., `/plan:build` or `/plan:build 2`)
- **Phase.task format:** Build a single task (e.g., `/plan:build 3.2` builds task 2 of phase 3)

Single-task mode:
- Reads the specified phase's plan.md
- Executes only the specified task number
- Skips final phase-level verification (step 6) — task-level verification still applies
- Does not update state.md phase status (that happens after the full phase completes)
- Keeps context cleaner — each task starts with fresh focus
- Lets user catch problems early instead of reviewing a whole phase at once

## Steps

1. **Read the phase's `plan.md`** for task list and verify criteria.
2. **Read `decisions.md`** for any constraints.
3. **Read `codebase.md`** for current project structure and stack context.
4. **Environment Preflight Check** — Verify the runtime environment is functional before writing any code:
    - **Python projects:** Run `.venv/bin/python -c "import sys; print(sys.version)"` and compare against `codebase.md` Stack section. If the Python version doesn't match what the venv was created with (check `.venv/pyvenv.cfg`), STOP — this is an environment mismatch, not a missing package.
    - **Import smoke test:** For each dependency listed in the phase's Dependencies section, run a bare import:
      ```
      .venv/bin/python -c "import <package>"
      ```
      If any import fails, investigate the cause BEFORE proceeding. Common causes:
      - **Python version mismatch** (packages in wrong `lib/pythonX.Y/` directory) — STOP, ask user to fix Docker image or venv
      - **Package genuinely not installed** — STOP, ask user to install on host
      - **Native extension incompatibility** (`.so` compiled for different arch/version) — STOP, ask user to rebuild venv
    - **Node.js projects:** Run `node -e "require('<package>')"` for key dependencies. Same diagnostic approach.
    - **If any preflight check fails:** Log the exact error and diagnosis in plan.md "Issues Discovered" section with "Fix Requires User Input: YES". Do NOT proceed to task execution. Do NOT create mocks, shims, or workarounds for import failures in production code.
5. **Check for user modifications** — read `phase_summary.md` and `ua_testing.md` (User Testing Notes section) from previous phases and scan git for modified files.
6. **Explore codebase** — use Grep and Glob to find existing patterns, similar implementations, and relevant interfaces before writing code.
7. **Execute tasks** from the plan:
    - **Resume detection:** Scan task headings for status markers. Start at the first task NOT marked `DONE`. If a task is `BLOCKED`, read its issue in "Issues Discovered" section.
    - **Single-task mode:** If argument is `[phase].[task]` format, execute only that task number from the specified phase. Skip steps 7-10 after completion — output the task result and STOP.
    - **Full-phase mode:** Execute all tasks sequentially.
    - **Mark task `IN_PROGRESS`** in plan.md heading before starting work.
    - Follow each task's action description.
    - **3-Strike Rule:** If the same operation fails 3 times (same error, same file, or same approach), STOP. Log to plan.md "Issues Discovered" section:
      ```
      ### Issue N: [Task Name] - Blocked

      **Description:** Attempted [operation] 3 times. Error: [error]. Likely cause: [environment limitation / missing dependency / other].
      **Fix Requires User Input:** YES
      **Resolution:** [EMPTY - awaiting user guidance]
      ```
      Mark task `BLOCKED` in heading. Do NOT proceed to next task. Output blocker summary and wait for user.
    - After each task, verify against the task's verify criteria.
    - **Deliverable existence check:** Before marking a task done, confirm the task's stated deliverable physically exists — function signatures present in the expected file, files created are non-empty, test files contain actual test functions. If the deliverable is missing, do NOT mark the task DONE — investigate and fix or log a blocker.
    - **Per-task style fix** (mandatory for tasks that write business logic or features; skip for config-only, comment-only, or scaffold-only tasks): Delegate to a `code-fixer` subagent after each task completes. Provide: task name, files touched, and the file types involved (so it loads the correct my-style reference). The fixer runs the project linter first for deterministic violations, then does an LLM style pass for what the linter cannot reach, and applies all fixes in-place. It operates with a two-round maximum — if violations remain after two rounds it reports them. Log all items from the code-fixer's **Needs User Review** section in plan.md "Issues Discovered" — these will surface in `ua_testing.md` when `/plan:review` generates it.
    - **Mark task `DONE`** in plan.md heading after the code-fixer pass completes.
    - **Explore during implementation** — use Grep to find existing similar code and match patterns and conventions.
    - If a task can't be completed as planned, note why and adapt.
    - **Comment maintenance:** When modifying existing code, review all comments within the modified function/block. Update or remove comments that no longer reflect the current logic. A stale comment is worse than no comment. Also scan the corresponding test file for any tests targeting renamed, removed, or gutted behavior in the modified function — flag these in a note for `ua_testing.md` under "Possibly Obsolete Tests." Do not delete them.
8. **Verify the build:**
    - Run tests with coverage: `coverage-wrapper run` — confirm no errors and review coverage summary
	    - If the application is not yet runnable (setup or early data layer phase), verify by running available checks instead:
		    - Dependency installation completes without errors
		    - Schema migrations run successfully
		    - Import statements resolve without errors
    - Check for coverage gaps in new/modified code: `coverage-wrapper gaps` — flag uncovered new code in plan.md "Issues Discovered" section for /plan:review to carry forward
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
    - **Append to `_planning/lessons.md`:** For any significant issue caught during verification (not minor typos or trivial fixes), add an entry following the format in `iterative-build/references/lessons.md`. Include: date, phase, brief title, what happened, root cause, fix applied, and prevention tip. This builds institutional memory for future phases.
9. **Update planning state:**
    - `_planning/state.md` — log what was built, set status to **"review"** (not complete — phase must pass /plan:review and UA testing first)
    - `_planning/roadmap.md` — mark phase as "in review" but do NOT check it off as complete
    - `_planning/deferred.md` — add any cross-phase items noticed during this build; remove any items that were addressed
    - `_planning/lessons.md` — entries already appended during step 7 verification (if any issues were found)
    - `_planning/codebase.md`:
        - **Setup phase:** Generate it (captures the project structure just created)
        - **Other phases:** Update only if new directories, dependencies, or architectural patterns were introduced. Skip if structure unchanged.
10. **Output quick summary:**
    - **One-sentence:** What this phase accomplished
    - **Files changed:** List with one-line descriptions
    - **Key functions:** List with one-line descriptions
    - **Behavior changes:** User-visible changes

11. **STOP.** Output the quick summary. Tell the user: "Build complete. Clear your context or switch models, then run `/plan:review` for independent verification and to generate testing documents."

## If Test-Writer Flags Implementation Bugs

When `test-writer` reports that a test fails because the implementation appears wrong (not the test):

1. **Do not modify the test** to make it pass. The test is correct; the implementation is wrong.
2. **Read the flagged test and the interface contract** it was written from — confirm the test is actually testing the promised behavior, not a misreading of the contract.
3. **Fix the implementation** in the source file. Scope the fix tightly to the failing behavior — do not refactor beyond what the contract requires.
4. **Re-run the full test suite** to confirm the fix passes and no previously passing tests broke.
5. **If fixing the implementation reveals the contract was wrong** (the planned behavior was itself incorrect), do not change the contract unilaterally — stop and ask the user to decide whether to update the contract or adjust the implementation.
6. **Document all implementation fixes** in the phase's `plan.md` under "Issues Discovered During Verification Stage" with: what the test caught, what was wrong in the implementation, and what was changed.
7. **If more than 2–3 functions required implementation fixes**, note this in plan.md so /plan:review can surface it in `ua_testing.md`.

## If Build Fails Mid-Phase
1. Mark the failed task `BLOCKED` in plan.md heading
2. Document what completed and what failed in `plan.md` "Issues Discovered" section with "Fix Requires User Input: YES"
3. Do NOT attempt to roll back successful tasks unless they depend on the failed one
4. Do NOT proceed to next task — output blocker summary and wait for user
5. Update state.md with interruption note

## Recovery After Blocker Resolution
1. User fixes the blocker and tells you it's resolved
2. Update the "Issues Discovered" section with the resolution
3. Re-run the blocked task: `/plan:build [phase].[task]`
4. After task passes verification, continue with next task or full phase
5. At phase end, run `coverage-wrapper run` to ensure no regressions from previous tasks

## Rules

- STOP after this phase. Do not proceed to next.
- **STOP on blocked tasks** — if a task has "Fix Requires User Input: YES" with no Resolution, do not proceed to the next task.
- If plan feels too big, tell user and suggest splitting.
- Accessibility required for web projects.
- Mark task status in plan.md: `PENDING` → `IN_PROGRESS` → `DONE` or `BLOCKED`.
- **Do not generate `phase_summary.md` or `ua_testing.md`** — those are generated by `/plan:review` in a fresh context.

## Do Not

- Do not refactor code outside the current task's scope
- Do not add error handling for impossible states
- Do not change function signatures defined in interface contracts without asking
- If a task's verify step fails, stop and report — do not silently adapt the next task
- **Do not work around import failures** — no mocks, shims, deferred imports, or try/except fallbacks in production code for environment issues. See `my-style` Mandatory Restrictions. STOP and escalate to the user.

$ARGUMENTS
