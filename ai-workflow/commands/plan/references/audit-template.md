# Code Audit Card & Document Templates

Load this file when ready to generate `code_audit.md` output.

---

## Emoji Reference — Required in Every Card

**Type emoji goes in the card heading. Difficulty emoji goes in the Difficulty field. Never omit either.**

| Emoji | Prefix | Domain | What it flags |
|-------|--------|--------|---------------|
| 🔥 | ARCH | Debt | Architecture violations — invisible deps, global state, env workarounds, swallowed errors |
| ⚙️ | DESIGN | Debt | Design principle violations — SRP, DI, separation of concerns |
| 🧹 | QUALITY | Debt | Code quality — long functions, missing types, stale comments, dead code |
| 🗃️ | DATA | Debt | DB/SQL issues — context managers, parameterized queries, N+1 |
| ♿ | ACCESS | Debt | Web accessibility — semantic HTML, ARIA, keyboard nav |
| 🔍 | SMELL | Test | Test smell — bad naming, conditionals, setup problems |
| 🎯 | GAP | Test | Coverage gap — untested behavior, branch, or edge case |
| 💀 | MUTANT | Test | Survived mutant — logic change not caught by any test |
| 🧪 | UPGRADE | Test | Property-based testing candidate |
| 🔗 | SEAM | Test | Missing integration test at module boundary |
| 🔁 | REDUNDANT | Test | Duplicate tests covering the same path with the same assertions |
| 👻 | ORPHAN | Test | Test for renamed or deleted code |
| 👾 | BOSS | Either | Entry point for clusters with 3+ cards |

**Difficulty scale (use for all card types):**
- 🟢 Quick — under 30 min
- 🟡 Medium — 30–60 min
- 🔴 Large — 1–3 hr
- ⚫ XL — 3+ hr

---

## Card Templates

### 👾 BOSS-[NNN]: [Module Name]

```markdown
### 👾 BOSS-[NNN]: [Module Name]
- **Difficulty**: 🔴
- **Module**: [source module or feature area]
- **Cards in this cluster**: [count] — [list card IDs, e.g., ARCH-002, GAP-001, SMELL-003]
- **The situation**: [2–3 sentences describing the combined debt + test problem in this area]
- **Your mission**: Review all cards in this cluster. Decide: fix incrementally or restructure from scratch?
- **Done when**: All referenced cards resolved AND a brief decision comment added at the top of the affected source file
- **Time box**: 45 min (or split across sessions)
```

---

### 🔥 ARCH-[NNN]: [Issue Name]

```markdown
### 🔥 ARCH-[NNN]: [Issue Name]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Large | ⚫ XL]
- **Risk**: [Low — isolated change | Medium — shared interface | High — core component]
- **Files**: [affected file paths]
- **What's wrong**: [what the violation is and where]
- **Fix**: [specific action — what exactly to do, not just "refactor"]
- **Done when**: [clear completion criteria]
- **Time box**: [N minutes]
```

---

### ⚙️ DESIGN-[NNN]: [Issue Name]

```markdown
### ⚙️ DESIGN-[NNN]: [Issue Name]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Large | ⚫ XL]
- **Risk**: [Low | Medium | High]
- **Files**: [affected file paths]
- **What's wrong**: [what principle is violated and where]
- **Fix**: [specific action]
- **Done when**: [clear completion criteria]
- **Time box**: [N minutes]
```

---

### 🧹 QUALITY-[NNN]: [Issue Name]

```markdown
### 🧹 QUALITY-[NNN]: [Issue Name]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Large | ⚫ XL]
- **Risk**: [Low | Medium | High]
- **Files**: [affected file paths]
- **What's wrong**: [what the quality issue is]
- **Fix**: [specific action]
- **Done when**: [clear completion criteria]
- **Time box**: [N minutes]
```

---

### 🗃️ DATA-[NNN]: [Issue Name]

```markdown
### 🗃️ DATA-[NNN]: [Issue Name]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Large | ⚫ XL]
- **Risk**: [Low | Medium | High]
- **Files**: [affected file paths]
- **What's wrong**: [the data handling issue]
- **Fix**: [specific action]
- **Done when**: [clear completion criteria]
- **Time box**: [N minutes]
```

---

### ♿ ACCESS-[NNN]: [Issue Name]

```markdown
### ♿ ACCESS-[NNN]: [Issue Name]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Large | ⚫ XL]
- **Risk**: Low
- **Files**: [affected file paths]
- **What's wrong**: [the accessibility issue]
- **Fix**: [specific action]
- **Done when**: [clear completion criteria]
- **Time box**: [N minutes]
```

---

### 🔍 SMELL-[NNN]: [Smell Name]

```markdown
### 🔍 SMELL-[NNN]: [Smell Name]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Large | ⚫ XL]
- **File**: [test file path]::[test function name]
- **Smell**: [which smell from the test standards]
- **What's suspicious**: [1–2 sentence description]
- **Your mission**: [specific question to answer or action to take]
- **Done when**: [clear completion criteria]
- **Time box**: [N minutes]
```

---

### 🎯 GAP-[NNN]: [Untested Behavior]

```markdown
### 🎯 GAP-[NNN]: [Untested Behavior]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Large | ⚫ XL]
- **Source file**: [production code path]::[function/method name]
- **What's untested**: [specific behavior, branch, or edge case]
- **Why it matters**: [what could go wrong]
- **Your mission**: Write a test that would catch a bug in this behavior
- **Starter hint**: [suggest what to assert, not how]
- **Done when**: A new test exists that fails if the described behavior breaks
- **Time box**: [N minutes]
```

---

### 💀 MUTANT-[NNN]: [Description of Mutation]

```markdown
### 💀 MUTANT-[NNN]: [Description of Mutation]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Large | ⚫ XL]
- **Source file**: [production code file]:[line number]
- **Mutation**: [what was changed, e.g., "Changed `>` to `>=`"]
- **Survived?**: Yes — no test caught this
- **Nearest test**: [test file most likely responsible]
- **Your mission**: Find which test should catch this and why it doesn't. Fix or write a new test.
- **Done when**: Re-running this mutation results in a killed mutant
- **Time box**: [N minutes]
```

---

### 🧪 UPGRADE-[NNN]: [Function Name]

```markdown
### 🧪 UPGRADE-[NNN]: [Function Name]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Large | ⚫ XL]
- **File**: [test file path]::[test function name(s)]
- **Subject**: [production function/class being tested]
- **Why it's a candidate**: [property or invariant that makes this suitable for property-based testing]
- **What's missing**: [the invariant to test — stated as a rule, not an example]
- **Your mission**: Add Hypothesis (Python) or fast-check (TypeScript) tests. Keep existing tests.
- **Done when**: At least one property-based test exists for the stated invariant
- **Time box**: [N minutes]
```

---

### 🔗 SEAM-[NNN]: [Module A → Module B]

```markdown
### 🔗 SEAM-[NNN]: [Module A → Module B]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Large | ⚫ XL]
- **Boundary**: [call site — function in Module A that calls Module B]
- **What crosses the boundary**: [data or behavior being handed off]
- **Why it's untested**: [both sides unit-tested but the handoff has no test]
- **What could go wrong**: [failure mode unit tests on each side would miss]
- **Your mission**: Write one integration test that exercises the full path. Do not mock the boundary itself.
- **Done when**: A test exists that fails if the contract between modules breaks
- **Time box**: [N minutes]
```

---

### 🔁 REDUNDANT-[NNN]: [Description]

```markdown
### 🔁 REDUNDANT-[NNN]: [Description]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Large | ⚫ XL]
- **Files**: [test file(s) and function names]
- **What's duplicated**: [code path or behavior both tests exercise]
- **Why it matters**: [maintenance cost — what breaks when this is touched]
- **Your mission**: Confirm truly redundant (same path, same assertions). If so, delete the weaker one. If they differ meaningfully, document why both are needed.
- **Done when**: Either one test is deleted, or you've documented why both are needed
- **Time box**: [N minutes]
```

---

### 👻 ORPHAN-[NNN]: [Test Name]

```markdown
### 👻 ORPHAN-[NNN]: [Test Name]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Large | ⚫ XL]
- **File**: [test file path]::[test function name]
- **Subject**: [function/class/behavior the test appears to target]
- **Why it may be obsolete**: [what changed — rename, removal, or behavior shift]
- **Your mission**: Confirm whether this test still tests anything real. Delete if not, update if salvageable.
- **Done when**: Either deleted or updated to test real current behavior
- **Time box**: [N minutes]
```

---

## audit-review.md Document Template

```markdown
# Code Audit — [Project Name]

<!-- STATUS: DRAFT -->
<!-- DEBT PASS: PENDING -->
<!-- TEST PASS: PENDING -->

**Date**: [today's date]
**Assessed Against**: my-style standards, test quality standards
**Codebase**: [languages, frameworks]
**Auto-fix list**: `_planning/audit-auto.md` ([n] items delegated for agent execution)

---

## Scorecard

### Coverage & Mutation

| Metric | Value | Notes |
|--------|-------|-------|
| Branch coverage | [n%] | |
| Mutation score | [n% or "deferred — coverage gaps must be addressed first"] | |
| Modules with zero test coverage | [n] | [list below] |

### Debt Summary

| Severity | Cards |
|----------|-------|
| 🔥 ARCH (Critical) | [n] |
| ⚙️ DESIGN (High) | [n] |
| 🧹 QUALITY (Medium) | [n] |
| 🗃️ DATA | [n] |
| ♿ ACCESS | [n] |

### Test Summary

| Type | Cards |
|------|-------|
| 🔍 SMELL | [n] |
| 🎯 GAP | [n] |
| 💀 MUTANT | [n] |
| 🧪 UPGRADE | [n] |
| 🔗 SEAM | [n] |
| 🔁 REDUNDANT | [n] |
| 👻 ORPHAN | [n] |
| 👾 BOSS | [n] |
| **Total** | [n] |

### Untested Modules

[List production modules with no corresponding test files, or "None"]

---

## 🃏 The Cluster Deck

> **How to use**: One cluster = one source module. Each cluster contains all debt AND test cards for that area.
> Complete one cluster before moving to the next — fixing debt and tests together prevents churn.
> Boss cards are the entry point for clusters with 3+ cards — read those first.
>
> **Debt cards**: 🔥 ARCH | ⚙️ DESIGN | 🧹 QUALITY | 🗃️ DATA | ♿ ACCESS
> **Test cards**: 🔍 SMELL | 🎯 GAP | 💀 MUTANT | 🧪 UPGRADE | 🔗 SEAM | 🔁 REDUNDANT | 👻 ORPHAN
> **Boss card**: 👾 BOSS (clusters with 3+ cards)
>
> **Difficulty**: 🟢 Quick (<30 min) | 🟡 Medium (30–60 min) | 🔴 Large (1–3 hr) | ⚫ XL (3+ hr)
> **Risk** (debt cards): Low — isolated | Medium — shared interface | High — core component

### Cluster: [Module Name]

Source: `[module path]` | Tests: `[test file path or "none"]`
Total: [n] cards ([n] debt / [n] test) | Est. effort: [time] | Risk ceiling: [High / Medium / Low / —]
Auto-fix items delegated: [n or "none"] → see `audit-auto.md`

| # | Done | Card | Type | Difficulty | Time |
|---|------|------|------|------------|------|
| 1 | [ ] | BOSS-001 | 👾 | 🔴 | 45 min |
| 2 | [ ] | ARCH-001 | 🔥 | 🔴 | 60 min |
| 3 | [ ] | GAP-001 | 🎯 | 🟡 | 30 min |
| 4 | [ ] | SMELL-001 | 🔍 | 🟢 | 15 min |

**Total estimated effort**: [time]

---

## Card Details

> All cards in card-number order. Use the cluster deck above to find priority order.

[Cards appear here, each using the exact template format from audit-template.md]
```
