---
description: Independent verification of a completed phase. Run after /plan:build in a fresh context. First pass verifies code and generates testing documents. Second pass (after UA testing) confirms results and closes the phase.
allowed-tools: Read, Write, Agent
---

# Review Phase

**Skill:** Load `iterative-build`
**Read first:** `_planning/state.md`

## Mode Detection

Check `state.md` for the current phase status, then run the matching pass below:

| State | Pass to run |
|-------|-------------|
| `review` | [Code Review Pass] — verify build, generate docs |
| `ua-testing` | [UA Confirmation Pass] — record test results, close phase |
| `complete` | Tell user this phase is already closed. Suggest `/plan:phase` for next. |
| anything else | Tell user what state the phase is in and what command makes sense next. |

If a phase number is provided as an argument, use that phase regardless of state.md.

---

## Code Review Pass (state = "review")

This is an independent verification pass. You are in a fresh context — do not assume the build was correct.

1. **Determine which phase to review:**
    - If argument provided: review that phase.
    - If no argument: review the most recently built phase (status = "review" in state.md).

2. **Read the phase's `plan.md`** — get the full task list and verify criteria.

3. **Verify task completion:** For each task in the plan, confirm it was actually completed as described.
    - Use Grep and Read to inspect code structure and implementations.
    - Use Grep to find how functions are called and connected.
    - For each task: check that the code matches what the plan called for. Missing, partial, or incorrect implementations must be flagged.
    - If a task is incomplete or incorrect, document it in a "Review Findings" section — flag it to the user before proceeding.

4. **Code quality review:** Check all new/modified code against `my-style` standards.
    - If a `code-reviewer` subagent is available, delegate this for an independent assessment.
    - Research any uncertain patterns or architectural decisions.

5. **UI quality check (frontend phases only):** If the phase modified any `.tsx`, `.jsx`, `.html`, `.css`, or `.vue` files:
    - Load `my-style/references/ui-antipatterns.md`.
    - Run the grep patterns from each section against all frontend files modified in this phase.
    - Organize findings by severity: CRITICAL → HIGH → MEDIUM → LOW.
    - CRITICAL violations must be added to Review Findings and block phase closure the same as broken implementations.
    - HIGH and MEDIUM violations are summarized in the review output (file + line) and included in `ua_testing.md` for user awareness.
    - If no frontend files were modified, skip this step.

6. **Security verification:** Explicitly verify each applicable Security Checklist item:
    - If the phase added new dependencies, confirm dependency review was performed (viewed source, checked for suspicious patterns)
    - If the phase has user input, confirm validation/sanitization is in place
    - If the phase has sensitive routes, confirm auth checks exist
    - Flag any unchecked items or gaps found during verification

7. **Generate `phase_summary.md`** in the phase directory using the `phase_summary` template from `iterative-build` references.
    - Generate "At a Glance" section first (most important):
        - One-sentence summary of what this phase accomplishes
        - Files Changed: each file with one-line description
        - Key Functions: each function added/modified with one-line behavior description
        - Behavior Changes: user-visible or API/contract changes
    - Then complete the remaining sections (What Was Built, Key Decisions, Major Logic Flows, Connection to Previous Phases).
    - Write incrementally — mark `<!-- STATUS: DRAFT -->` at top while generating, replace with `<!-- STATUS: COMPLETE -->` when done.

8. **Generate `ua_testing.md`** in the phase directory using the `ua_testing` template from `iterative-build` references.
    - Use progressive disclosure: Quick Smoke tests first (2–5 min), then Priority 1 features (15–20 min), then Priority 2 if time permits.
    - Include any "Possibly Obsolete Tests" flagged during the build.
    - Include any coverage gaps, code-fixer flags from plan.md "Issues Discovered", and HIGH/MEDIUM UI violations from step 5 — remaining violations, scope warnings, and linter bypass flags all need user visibility.
    - The User Testing Notes section at the bottom is left blank — the user fills it in after testing.
    - Write incrementally — mark `<!-- STATUS: DRAFT -->` at top while generating, replace with `<!-- STATUS: COMPLETE -->` when done.

9. **Update `state.md`** — set phase status to `ua-testing`.

10. **STOP.** Output:
    - **Review Findings** (if any issues were found — be explicit, don't bury them)
    - Confirmation that `phase_summary.md` and `ua_testing.md` are ready in the phase directory
    - Instruction: "Complete UA testing using the checklist in `ua_testing.md`. Fill in the User Testing Notes section with what you find. Then run `/plan:review` to record results and close the phase."

---

## UA Confirmation Pass (state = "ua-testing")

1. **Determine which phase:**
    - If argument provided: use that phase.
    - If no argument: use the most recent phase with status = "ua-testing".

2. **Read `ua_testing.md`** — specifically the User Testing Notes section.

3. **If User Testing Notes are empty:** Ask the user to describe their UA testing results. Do not proceed until you have findings. Prompt: "What did you find during UA testing? Share any issues, errors, questions, or a thumbs up if everything passed."

4. **Record the user's findings** in the User Testing Notes section of `ua_testing.md`:
    - Issues Found: numbered list
    - Error Messages / Logs: paste any error output
    - Questions: numbered list
    - General Feedback: long-form notes
    - **Do NOT touch the Result checkboxes** — those are for the user only. The user marks their own acceptance. Agents must never check these boxes.

5. **If issues were found:**
    - Add them to a "Follow-up Items" section of `ua_testing.md` with priority (blocker / nice-to-fix / next phase).
    - Ask the user: "Are any of these blockers, or can we proceed to the next phase?"
    - If blockers: do NOT close the phase. Update state.md to note what's blocking. User should fix and re-run `/plan:review`.
    - If non-blockers: proceed to close.

6. **When user confirms approval (no blockers):**
    - **Triage all open items before closing.** Scan `ua_testing.md` for any unresolved items in "Issues Found," "Follow-up Items," and "Known Limitations." Every open item must be accounted for:
        - Add to `_planning/deferred.md` — items to address in a future phase, or
        - Record in `_planning/decisions.md` — items accepted as known trade-offs or out of scope
        - Do NOT close the phase if any open item is unaccounted for. Ask the user how to handle it.
    - Update `state.md` — set phase status to `complete`, log session.
    - Update `roadmap.md` — check off the completed phase.
    - Suggest: "Phase complete. Run `/plan:phase` to plan the next phase."

---

## Rules

- Do not start building the next phase.
- Testing docs should be practical — real steps, 15 min max for priority 1 items.
- **Do not mark a phase complete** until the user has confirmed UA testing results.
- Both `phase_summary.md` and `ua_testing.md` are required before the phase can close.
- If issues surface during code review, add them to a "Review Findings" section of `ua_testing.md` — not only in the terminal.

$ARGUMENTS
