# Test Audit Card & Document Templates

Load this file when ready to generate `test_audit.md` output.

## Investigation Card Templates

### 🔍 Smell Check Card

```markdown
### 🔍 SMELL-[NNN]: [Smell Name]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Deep Dive]
- **File**: [test file path]::[test function name]
- **Smell**: [which smell from the standards list]
- **What's suspicious**: [1-2 sentence description]
- **Your mission**: [specific question to answer or action to take]
- **Done when**: [clear completion criteria]
- **Time box**: [minutes]
```

### 🎯 Coverage Gap Card

```markdown
### 🎯 GAP-[NNN]: [Untested Behavior]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Deep Dive]
- **Source file**: [production code path]::[function/method name]
- **What's untested**: [specific behavior, branch, or edge case]
- **Why it matters**: [what could go wrong]
- **Your mission**: Write a test that would catch a bug in this behavior
- **Starter hint**: [suggest what to assert, not how]
- **Done when**: A new test exists that fails if the described behavior breaks
- **Time box**: [minutes]
```

### 💀 Mutant Hunt Card

> Requires mutation testing tools installed and a run completed. If not available, include setup instructions instead of cards.

```markdown
### 💀 MUTANT-[NNN]: [Description of the Mutation]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Deep Dive]
- **Source file**: [production code file]:[line number]
- **Mutation**: [what was changed, e.g., "Changed `>` to `>=`"]
- **Survived?**: Yes — no test caught this
- **Nearest test**: [test file most likely responsible]
- **Your mission**: Figure out which test should catch this and why it doesn't. Fix or write a new one.
- **Done when**: Re-running the mutation on this line results in a killed mutant
- **Time box**: [minutes]
```

### 🧪 Upgrade Card (Property-Based Testing)

```markdown
### 🧪 UPGRADE-[NNN]: [Function Name]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Deep Dive]
- **File**: [test file path]::[test function name(s)]
- **Subject**: [production function/class being tested]
- **Why it's a candidate**: [what property or invariant makes this suitable]
- **What's missing**: [the invariant to test — stated as a rule, not an example]
- **Your mission**: Add Hypothesis (Python) or fast-check (TypeScript) tests. Keep existing example-based tests.
- **Done when**: At least one property-based test exists for the stated invariant
- **Time box**: [minutes]
```

### 🔗 Seam Card

```markdown
### 🔗 SEAM-[NNN]: [Module A -> Module B]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Deep Dive]
- **Boundary**: [the call site — function in Module A that calls Module B]
- **What crosses the boundary**: [the data or behavior being handed off]
- **Why it's untested**: [both sides have unit tests but the handoff has no test]
- **What could go wrong**: [failure mode unit tests on each side would miss]
- **Your mission**: Write one integration test that exercises the full path. No mocking the boundary itself.
- **Done when**: A test exists that would fail if the contract between modules broke
- **Time box**: [minutes]
```

### 🔁 Redundancy Card

```markdown
### 🔁 REDUNDANT-[NNN]: [Description]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Deep Dive]
- **Files**: [test file(s) and function names]
- **What's duplicated**: [the code path or behavior both tests exercise]
- **Why it matters**: [maintenance cost]
- **Your mission**: Confirm truly redundant (same path, same assertions). If so, delete the weaker one. If they differ meaningfully, document why both are needed.
- **Done when**: Either one test is deleted, or you've documented why both are needed
- **Time box**: [minutes]
```

### 👻 Orphan Card

```markdown
### 👻 ORPHAN-[NNN]: [Test Name]
- **Difficulty**: [🟢 Quick | 🟡 Medium | 🔴 Deep Dive]
- **File**: [test file path]::[test function name]
- **Subject**: [the function/class/behavior the test appears to target]
- **Why it may be obsolete**: [what changed]
- **Your mission**: Confirm whether this test still tests anything real. Delete if not, update if salvageable.
- **Done when**: Either deleted or updated to test real current behavior
- **Time box**: [minutes]
```

### 👾 Boss Battle Card

```markdown
### 👾 BOSS-[NNN]: [Module Name]
- **Difficulty**: 🔴
- **Module**: [source module or feature area]
- **Issues found**: [count] — references: [list card numbers]
- **The situation**: [2-3 sentences describing the overall testing problem in this area]
- **Your mission**: Review related cards, then decide: restructure from scratch or fix incrementally?
- **Done when**: Referenced cards completed AND decision documented in a comment at top of test file
- **Time box**: 45 min (or split across sessions)
```

## test_audit.md Template

```markdown
# Test Suite Audit

**Date**: [today's date]
**Assessed Against**: Test quality standards (assertion quality, test design, coverage quality, test independence, AI-generated test red flags)
**Test Framework(s)**: [e.g., pytest, vitest, jest]
**Codebase**: [languages, frameworks involved]

---

## Scorecard

| Metric | Value | Notes |
|--------|-------|-------|
| Total test files | [n] | |
| Total test functions/methods | [n] | |
| Line coverage (if available) | [n%] | [tool used or "not configured"] |
| Mutation score (if available) | [n%] | [tool used or "not configured"] |
| Tests with no meaningful assertions | [n] | |
| Tests with smell flags | [n] | |
| Source modules with zero test coverage | [n] | list below |
| Investigation cards generated | [n] | 🔍 [n] 🎯 [n] 💀 [n] 👾 [n] 👻 [n] 🧪 [n] 🔗 [n] 🔁 [n] |

### Untested Modules
[List any production code modules/files with no corresponding tests]

---

## Tool Setup

### Coverage
- **Status**: [Configured / Not configured]
- **How to run**: [exact command]
- **Install if needed**: [e.g., `pip install pytest-cov --break-system-packages`]

### Mutation Testing
- **Status**: [Installed / Not installed]
- **Tool recommended**: [mutmut for Python / Stryker for TypeScript]
- **Install**: `pip install mutmut --break-system-packages` (Python) or `npm install --save-dev @stryker-mutator/core` (TypeScript)

---

## Standards Check

|Standard|Status|Notes|
|---|---|---|
|Every test has meaningful assertions|[PASS/FAIL/PARTIAL]|[n violations]|
|Assertions test behavior, not implementation|[PASS/FAIL/PARTIAL]||
|One concept per test|[PASS/FAIL/PARTIAL]||
|No conditional logic in tests|[PASS/FAIL/PARTIAL]||
|Business logic has correct AND incorrect input tests|[PASS/FAIL/PARTIAL]||
|Edge cases covered|[PASS/FAIL/PARTIAL]||
|Error paths tested|[PASS/FAIL/PARTIAL]||
|Tests are order-independent|[PASS/FAIL/PARTIAL]||
|No external resource dependencies|[PASS/FAIL/PARTIAL]||
|No AI-generated test red flags|[PASS/FAIL/PARTIAL]||

---

## 🃏 The Deck

> **How to use**: Work through one cluster at a time — all cards in a cluster cover the same source module. Within each cluster, cards run hardest-to-easiest. Boss cards are the entry point for clusters with 3+ issues. Check off cards as you go.
>
> **Card types**: 🔍 Smell Check | 🎯 Coverage Gap | 💀 Mutant Hunt | 👾 Boss Battle | 👻 Orphan | 🧪 Upgrade | 🔗 Seam | 🔁 Redundancy
>
> **Difficulty**: 🟢 Quick (10-15 min) | 🟡 Medium (20-30 min) | 🔴 Deep Dive (30-45 min)

### Cluster: [Module Name]

Source: `[module path]` | Tests: `[test file path]`
Total: [n] cards | Est. effort: [time]

|#|Done|Card|Type|Difficulty|Time|
|---|---|---|---|---|---|
|1|[ ]|[BOSS-001]|👾|🔴|45 min|
|2|[ ]|[GAP-001]|🎯|🔴|30 min|
|3|[ ]|[SMELL-001]|🔍|🟢|15 min|

**Total estimated effort**: [hour estimate]

---

## Card Details

[All investigation cards here, in card-number order for reference]

```
