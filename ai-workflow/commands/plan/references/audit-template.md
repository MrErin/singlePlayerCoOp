# Code Audit Review Card & Document Templates

Load this file when ready to generate `audit-review.md` output.

Review cards are for items that require a **decision** — choosing between valid alternatives or accepting a tradeoff. If the fix has one correct answer, it belongs in `audit-auto.md` instead.

---

## Emoji Reference

**Type emoji goes in the card heading. Never omit it.**

| Emoji | Prefix | Domain | What it flags |
|-------|--------|--------|---------------|
| 📄 | DOC | Doc | Documentation drift — planning docs out of sync with codebase or each other |
| 🔥 | ARCH | Debt | Architecture violations — structural issues with multiple valid fixes |
| ⚙️ | DESIGN | Debt | Design principle violations — SRP, DI, separation of concerns |
| 🗃️ | DATA | Debt | DB/SQL issues requiring design decisions |
| ♿ | ACCESS | Debt | Accessibility issues requiring UX decisions |
| 🔒 | SEC | Debt | Security concerns with usability/complexity tradeoffs |
| 🔍 | SMELL | Test | Test smell requiring redesign (not just a mechanical fix) |
| 🎯 | GAP | Test | Coverage gap where what to test is unclear |
| 💀 | MUTANT | Test | Survived mutant where the right assertion is ambiguous |
| 🔗 | SEAM | Test | Missing integration test where boundary contract is unclear |

---

## Card Template (all types use the same format)

```markdown
### [EMOJI] [PREFIX]-[NNN]: [Short Description]
- **Files**: [affected file paths]
- **What's wrong**: [1-2 sentences — what the issue is]
- **Options**:
  - A: [first valid approach and its tradeoff]
  - B: [second valid approach and its tradeoff]
- **Recommendation**: [which option and why, or "needs discussion"]
```

Keep cards tight. If you can't articulate two valid options, the item belongs in `audit-auto.md`.

---

## audit-review.md Document Template

```markdown
# Code Audit — [Project Name]

<!-- STATUS: DRAFT -->
<!-- DOC PASS: PENDING -->
<!-- DEBT PASS: PENDING -->
<!-- TEST PASS: PENDING -->

**Date**: [today's date]
**Assessed Against**: my-style standards, test quality standards
**Codebase**: [languages, frameworks]
**Auto-fix list**: `_planning/audit-auto.md` ([n] items delegated for agent execution)

---

## Scorecard

> **Trend columns**: Previous = most recent entry in `_planning/audit-scorecard.md`. Δ = Current − Previous. Leave blank on first run. For card counts: ↓ is good. For coverage/mutation/ratio: ↑ is good.

### Coverage & Mutation

| Metric | Current | Previous | Δ |
|--------|---------|----------|---|
| Branch coverage | [n%] | | |
| Mutation score | [n% or "deferred — coverage <80%"] | | |
| Modules with zero test coverage | [n] | | |

### Test Quality

| Metric | Current | Previous | Δ | Healthy |
|--------|---------|----------|---|---------|
| Total tests | [n] | | | — |
| Total assertions | [n] | | | — |
| Assertion ratio | [n.n per test] | | | 1.5–3.0 |
| Tests with 0 assertions | [n] | | | 0 |
| Skipped tests | [n] | | | 0 or documented |
| Largest file assertion share | [n%] | | | <30% |

### ⚠️ Warning Signs

Check these before closing. A checked box means the signal is present — investigate before moving on.

- [ ] Coverage ≥80% but mutation score <50% — tests run code but don't verify behavior
- [ ] One file holds >30% of all assertions — concentrated coverage, gaps elsewhere
- [ ] Assertion ratio <1.5 — tests are probably too shallow overall
- [ ] Tests with 0 assertions exist — coverage theater
- [ ] No negative/error path tests visible in test names — missing edge cases

### Summary

| Category | Review cards | Auto-fix items |
|----------|-------------|----------------|
| 📄 DOC | [n] | [n] |
| Debt (🔥 ⚙️ 🗃️ ♿ 🔒) | [n] | [n] |
| Test (🔍 🎯 💀 🔗) | [n] | [n] |
| **Total** | [n] | [n] |

### Untested Modules

[List production modules with no corresponding test files, or "None"]

---

## 📄 Documentation Drift

[DOC cards — only items where the correct resolution is ambiguous]

---

## Debt

[ARCH, DESIGN, DATA, ACCESS, SEC cards — only items with multiple valid approaches]

---

## Tests

[SMELL, GAP, MUTANT, SEAM cards — only items where what to test or how to restructure is unclear]
```
