# Phase [N] Testing: [Name]

## At a Glance

**One sentence: what this phase tests.**

### What To Verify
- [ ] [core behavior 1 - describe expected behavior]
- [ ] [core behavior 2 - describe expected behavior]
- [ ] [edge case 1 - describe expected behavior]

---

## Automated Tests

**How to run:** `[command to run tests]`

[If no automated tests exist, explain why not]

---

## Manual Testing Steps

### Quick Smoke Test (2-5 min)
1. [Step to verify basic functionality works]
2. [Step]
- **Expected:** [what should happen]

### [Feature 1] — [Feature Name] (5-10 min)

1. [step]
2. [step]
- **Expected:** [what should happen]
- **If fails:** [what might be wrong]

### [Feature 2] — [Feature Name]

...

---

## Edge Cases to Check

### Priority 1 (Test First)
- [ ] [edge case 1 - describe expected behavior]

### Priority 2
- [ ] [edge case 1 - describe expected behavior]

---

## Phase Completion Checklist

### Must Pass
- [ ] All manual tests pass
- [ ] Edge cases checked
- [ ] No regressions in existing features

### Nice to Have
- [ ] [optional item]

### Known Limitations
- [any known issues or limitations to leave for user to decide whether to address]

---

## Required Manual Renames

*Naming consistency check found the following divergences between layers. Complete all renames before marking the phase complete — they must be done with `git mv` to preserve git history. Never delete and recreate a file to rename it.*

*Agents: delete this section if no renames were identified.*

| What | Rename from | Rename to | Command |
|------|-------------|-----------|---------|
|      |             |           |         |

---

## User Testing Notes

*Fill in this section after completing the testing steps above. Then run `/plan:review` to record your results and close the phase.*

### Issues Found

1.

### Error Messages / Logs

```
[paste error output here]
```

### Questions

1.

### General Feedback

[long-form notes, observations, or concerns]

### Deferred this session

*Agents: fill this out as you work — do not wait for /plan:review. Each item deferred (not fixed now) must be listed here AND added to `_planning/deferred.md` before the conversation ends.*

| Item | Reason deferred | Added to deferred.md? |
|------|-----------------|-----------------------|
| | | |

### Result

<!-- ⚠️ USER ONLY — Agents must never check these boxes. Only the user marks acceptance. -->
- [ ] All good — ready to proceed
- [ ] Issues found — see above
