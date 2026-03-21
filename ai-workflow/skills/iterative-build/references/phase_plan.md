# Phase [N]: [Name]

## Goal

[One sentence: what this phase accomplishes]

## Research Notes

[Research notes organized with subheadings and bullets if necessary/useful]

## Interface Contracts

> Required for implementation phases that will have a corresponding test phase. These contracts are the source of truth for test generation — tests are written from these contracts in a separate session, not from reading implementation code. Omit this section for setup, data layer, polish, and test phases.

### [function_name]

- **Signature:** `function_name(param: type, ...) -> return_type`
- **Purpose:** [one sentence — what it does]
- **Invariants:** [rules that always hold, e.g., "return value >= 0", "output list length <= input list length"]
- **Valid inputs:** [constraints on parameters]
- **Error conditions:** [what triggers errors and what error looks like]
- **Edge cases to test:** [zero, empty, boundary values, null/None where applicable]

## Tasks

> Task status is marked in the heading: `PENDING` → `IN_PROGRESS` → `DONE` or `BLOCKED`. When resuming a phase, scan for the first non-DONE task.

### Task 1: [Name] `PENDING`

**Files:** [files to create or modify] **Action:** [what to do — specific and unambiguous] **Verify:** [how to confirm it worked] **Done when:** [concrete completion criteria]

### Task 2: [Name] `PENDING`

...

## Dependencies

[anything from previous phases this builds on]

## Environment Constraints

> For test phases: list any container or environment limitations that affect test design. Check CLAUDE.md "Hard Limits" and the project's known constraints.
> Tests must be designed to work within these constraints.
- [e.g., "chmod blocked at kernel level — tests verifying file permissions must mock Path.chmod or use @pytest.mark.skipif"]
- [e.g., "No network access — all HTTP calls must be mocked"]
- [e.g., "No sudo/apt — cannot install additional packages"]

## Security Checklist

> Complete applicable items during build. Review verifies these were addressed.

- [ ] Input validation: user input sanitized before use
- [ ] SQL injection prevention: parameterized queries, no string concatenation
- [ ] Auth protection: sensitive routes check authentication
- [ ] Secrets handling: no hardcoded credentials, secrets excluded from source control
- [ ] Destructive actions: confirmation required before irreversible operations
- [ ] Dependency review: (if new dependencies added) viewed source, no unexpected network calls or dynamic code execution

**Notes:** [Any security-relevant decisions or trade-offs made in this phase]

## Issues Discovered During Verification Stage

> Log blocking issues here with "Fix Requires User Input: YES" and empty Resolution. Do NOT proceed past a blocked task.

### Issue 1: [Name]

**Description:** [description of issue] **Fix Requires User Input:** [If yes, ask user for direction. If no, research and fix the issue.] **Resolution:** [description of fix applied]

### Issue 2: [Name]

...