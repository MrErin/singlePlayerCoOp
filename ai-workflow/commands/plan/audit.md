---
description: Full codebase sweep combining technical debt and test suite quality into one actionable cluster deck. Each cluster contains all debt AND test cards for that module — fix both together. Replaces running /plan:debt and /plan:test-audit separately.
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Agent
---

# Code Audit

**Skill:** Load `my-style`

## Resume Detection

Before starting, check if `_planning/code_audit.md` exists:

- `<!-- STATUS: COMPLETE -->` → tell the user the audit is current. Suggest re-running only if significant code has changed since the audit date.
- `<!-- STATUS: DRAFT -->` + `<!-- TEST PASS: COMPLETE -->` → skip to Pass 3 (Merge).
- `<!-- STATUS: DRAFT -->` + `<!-- DEBT PASS: COMPLETE -->` → skip to Pass 2 (Test Analysis).
- `<!-- STATUS: DRAFT -->` + no pass markers → resume debt analysis from the last written module cluster.

---

## Setup — Run Once

1. **Read**: `_planning/codebase.md`, `_planning/requirements.md`, `_planning/decisions.md`
   - If `_planning/` does not exist: STOP. Tell user to run `/plan:init` first.

2. **Map module structure**: Use Glob to enumerate source files and directories to see the full module structure.

3. **Triage modules**: From `codebase.md`, identify all source modules and rank by importance:
   business logic > data layer > API/routes > utilities > config

4. **Scaffold the document**: Read `commands/plan/references/audit-template.md` for card formats and the document template. Write `_planning/code_audit.md` with:
   - `<!-- STATUS: DRAFT -->`
   - `<!-- DEBT PASS: PENDING -->`
   - `<!-- TEST PASS: PENDING -->`
   - Document header and ranked module list

---

## Pass 1 — Debt Analysis

Update the draft marker to `<!-- DEBT PASS: IN_PROGRESS -->`.

**Quick antipattern scan first** — before per-module analysis, use Grep to find critical patterns across the whole codebase. Create ARCH or QUALITY cards immediately for any match:

| Pattern | Card type | Severity |
|---------|-----------|----------|
| `sys.modules[` | 🔥 ARCH | Critical |
| `except:` or `except.*: pass` | 🔥 ARCH | Critical |
| `=[` or `={}` in function signature | 🔥 ARCH | Critical |
| `from unittest.mock import` in `src/` | 🔥 ARCH | High |
| `+` or f-string in SQL | 🗃️ DATA | High |
| query inside loop over results | 🗃️ DATA | High |

See `my-style/references/antipatterns.md` for the full detection pattern list and severity mappings.

**Per-module analysis** (highest priority first):

For each module, delegate to a `code-reviewer` subagent. The subagent receives:
- The module's files (use Grep and Read to gather them)
- `my-style` standards
- The debt-specific checks listed below

Debt-specific checks per module:
- File organization follows feature-folder pattern
- DB connections use context managers (no manual open/close)
- All queries use parameterized syntax (no string concatenation or f-strings)
- Semantic HTML used appropriately (not div-for-everything)
- Interactive elements have ARIA labels, keyboard navigation, and focus management
- **Dead code**: use Grep to find functions/classes defined but never called outside their own file. Verify before flagging — check for dynamic calls, test fixtures, and API endpoints that may not appear as static callers. Confirmed dead code → 🧹 QUALITY card.
- **Redundant code**: near-identical functions across files, copy-paste artifacts, multiple implementations of the same utility → 🧹 QUALITY card.

**Write each module's debt cards to the document before moving to the next module.**

When all modules are complete: update marker to `<!-- DEBT PASS: COMPLETE -->`.

---

## Pass 2 — Test Analysis

Update the draft marker to `<!-- TEST PASS: IN_PROGRESS -->`.

**Run tooling first — always coverage before mutation:**

1. Run `coverage-wrapper run` → get branch coverage percentage. Append results to document.
2. Run `coverage-wrapper gaps` → identify uncovered files. Append results to document.
3. Assess:
   - **Below 80%**: Skip mutation testing entirely. Focus all test cards on 🎯 GAP cards. Add note to document: "Mutation testing deferred — branch coverage must reach 80% first."
   - **80–90%**: Run `mutmut-wrapper run` (no pattern filter — targeted runs fail without complete coverage data). Append results.
   - **Above 90%**: Run `mutmut-wrapper run`, then `mutmut-wrapper show-all`. Read `mutmut_output/survived_all.txt` for diffs. Append results.

**Quick antipattern scan for test files** — use Grep before per-module analysis:
- `sys.modules[` in test files → 🔍 SMELL card
- `MagicMock` in `src/` → 🔍 SMELL card (mock in production)
- `assert True` or assertion-free tests → 🔍 SMELL card

**Per-module test analysis** (same priority order as Pass 1):

For each module's test file(s), use Grep for test function definitions to see all test functions. Evaluate against these standards:

| Category | What to check |
|----------|---------------|
| **Naming** | `Test[Feature]` class names; `test_[action]_[condition]_[result]` method names; no vague names like `TestUser` |
| **Design** | One concept per test; no conditionals; proportional setup; no section dividers |
| **Independence** | Order-independent; no shared mutable state; no timing dependencies |
| **Assertions** | All return fields asserted; exact counts (not `>=`); no tautologies; no mirror tests |
| **Coverage** | Edge cases; error paths; minimum 1:2 negative:happy-path ratio |
| **Seams** | Module boundaries have integration tests, not just mocked units |
| **Redundancy** | No duplicate tests covering same path with same assertions |
| **Obsolete** | Tests for renamed or deleted functions |
| **Parallel coverage** | Similar modules (same pattern) have similar test coverage |

**Write each module's test cards to the document before moving to the next module.**

When all modules are complete: update marker to `<!-- TEST PASS: COMPLETE -->`.

---

## Pass 3 — Merge and Cluster

1. **Read all cards** from Passes 1 and 2.

2. **Group into module clusters**: Every card that touches the same source module belongs in one cluster — debt and test cards together. A card spanning multiple files may appear in multiple clusters; add a cross-reference note when it does.

3. **Within each cluster**:
   - Assign a 👾 BOSS card if the cluster has 3 or more cards total (debt + test combined).
   - Order: BOSS card first, then remaining cards by severity/difficulty descending.

4. **Order clusters**: Higher-severity clusters first. Tiebreak: clusters whose files are touched by other clusters come first (fixing them unblocks others).

5. **Write the cluster deck** to the document using the template format from `audit-template.md`. Each row in the cluster table must include the type emoji in the Type column.

6. **Generate the scorecard** now that all cards are counted. Fill in the Scorecard section at the top of the document.

7. Replace `<!-- STATUS: DRAFT -->` with `<!-- STATUS: COMPLETE -->`.

---

## Rules

- **Emojis are required — not optional.** Every card heading must open with its type emoji (🔥 ⚙️ 🧹 🗃️ ♿ 🔍 🎯 💀 🧪 🔗 🔁 👻 👾). Every Difficulty field must include a colored circle (🟢 🟡 🔴 ⚫). Every Type column in cluster tables must show the emoji. These are functional visual cues — never omit them, never replace them with plain text.
- Do not rewrite production code. Trivial test fixes during the test pass are allowed.
- Delegate per-module debt analysis to `code-reviewer` subagents — do not analyze debt inline.
- Always run `coverage-wrapper` before `mutmut-wrapper` — never skip the order of operations.
- Use `coverage-wrapper` and `mutmut-wrapper` — never raw `coverage` or `mutmut` commands.
- Write cards to disk after each module — do not batch all writes to the end.
- Provide a brief corrected example when the fix is obvious.
- Explain why each issue matters — connect it to the bug or maintenance cost it creates.


$ARGUMENTS
