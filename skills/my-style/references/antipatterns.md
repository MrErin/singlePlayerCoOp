# AI-Generated Code Anti-Patterns

Patterns commonly found in AI-generated code that indicate poor quality, hidden bugs, or workarounds. 

## Severity Classification

- **CRITICAL** — Will cause bugs in production (data loss, security, crashes)
- **HIGH** — Indicates systemic quality issues, will cause maintenance pain
- **MEDIUM** — Code smell, should be cleaned but not urgent
- **LOW** — Minor inconsistency, fix opportunistically

---

## Environment Workarounds (CRITICAL)

Patterns where AI masked a broken environment instead of escalating.

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| `sys.modules` manipulation | `sys.modules[` | CRITICAL | Remove, verify import works, escalate if broken |
| Mock in production code | `from unittest.mock import` in `src/` | CRITICAL | Move to test file or remove |
| Silent import fallback | `except ImportError:` + assignment | CRITICAL | Remove fallback for core deps |
| Deferred core imports | `import` inside function for core deps | HIGH | Import at module level |

**Why it matters:** These patterns indicate the environment was broken. The AI "solved" the symptom while hiding the root cause.

---

## Error Handling Anti-Patterns (CRITICAL/HIGH)

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| Bare except | `except:` (no exception type) | CRITICAL | Catch specific exception |
| Swallowed exception | `except.*: pass` or `except.*: ... pass` | CRITICAL | Handle, log, or re-raise |
| Catch-all with continue | `except Exception.*:\s*\n.*continue` | HIGH | Narrow exception or handle properly |
| Impossible try/except | `try:` around code that can't raise | MEDIUM | Remove try/except |
| Log and continue | `except.*:\s*\n.*log` without raise/return | HIGH | Either handle or escalate, don't silence |

**Why it matters:** Silenced errors hide bugs, make debugging impossible, and corrupt state silently.

---

## State & Mutability Issues (CRITICAL/HIGH)

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| Mutable default arg | `=\[\]` or `={}` in function signature | CRITICAL | Use `None` and create inside function |
| Global mutable state | Module-level `dict` or `list` that's modified | HIGH | Move to class or function scope |
| Shared class attribute | Mutable class attribute accessed by instances | HIGH | Make instance attribute in `__init__` |
| Cache without invalidation | Module-level cache dict with no clear path | MEDIUM | Add TTL or invalidation logic |

**Why it matters:** Mutable defaults and shared state cause subtle bugs where one call affects another.

```python
# ❌ Mutable default - shared across all calls
def add_item(item, cart=[]):
    cart.append(item)
    return cart

# ✅ Immutable default, create inside
def add_item(item, cart=None):
    if cart is None:
        cart = []
    cart.append(item)
    return cart
```

---

## Over-Engineering Patterns (HIGH/MEDIUM)

| Pattern | Detection | Severity | Action |
|---------|-----------|----------|--------|
| Single implementation ABC | ABC with 1 concrete class | MEDIUM | Remove abstraction until needed |
| Factory of factories | `*Factory*Factory*` in names | HIGH | Flatten to direct instantiation |
| Strategy for 2 options | Strategy pattern with 2 strategies | MEDIUM | Use if/else or dict dispatch |
| Excessive interfaces | Protocol/ABC for every class | MEDIUM | Create interfaces when needed for testing |
| Premature plugin architecture | Plugin system for known integrations | HIGH | Build what's needed now |

**Why it matters:** Over-abstraction adds cognitive load and maintenance burden without benefit. AI tends to "enterprise" simple problems.

---

## AI-Specific Tells (MEDIUM)

Patterns that strongly suggest AI-generated code without human review.

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| Conversational comments | `as mentioned`, `as discussed`, `note that` | MEDIUM | Remove conversational filler |
| Obvious docstrings | Docstrings on trivial getters/setters | LOW | Remove or make meaningful |
| Defensive null checks | `if x is None` where x can't be None | MEDIUM | Remove if truly impossible |
| Inconsistent naming | Mixed snake_case/camelCase in same file | LOW | Standardize |
| Boilerplate comments | `# This function does X` restating code | LOW | Remove or explain WHY |

**Why it matters:** These indicate AI-generated code that wasn't reviewed. Often accompanies deeper issues.

---

## Testing Anti-Patterns (HIGH/MEDIUM)

| Pattern | Detection | Severity | Action |
|---------|-----------|----------|--------|
| Mirror test | Assert compares computed value to itself | HIGH | Test against known expected value |
| No assertions | Test function with no `assert` | CRITICAL | Add assertions or delete test |
| Over-mocked | Every dependency mocked, no real code tested | HIGH | Add integration tests |
| Giant setup | 30+ line setup for 1 assertion | MEDIUM | Extract to fixture or helper |
| Happy path only | No error/edge case tests | HIGH | Add negative tests (1:2 ratio minimum) |
| Tautological assertion | `assert x == x` or `assert True` | CRITICAL | Remove or test something real |

---

## Database/API Patterns (HIGH)

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| N+1 queries | Query inside loop over results | HIGH | Use join or batch fetch |
| String concat in SQL | `+` or f-string in query string | CRITICAL | Use parameterized queries |
| No pagination | List endpoint without limit/offset | HIGH | Add pagination |
| Business logic in routes | Route handler > 20 lines with logic | HIGH | Extract to service layer |
| Fetch all columns | `SELECT *` in production code | MEDIUM | Select only needed columns |

---

## Import Anti-Patterns (MEDIUM)

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| Unused imports | Import not referenced in file | LOW | Remove (let linter catch) |
| Star imports | `from x import *` | HIGH | Import specific names |
| Circular imports | Import errors at module load | HIGH | Restructure or use deferred import |
| Shadow imports | Local name shadows imported name | MEDIUM | Rename one of them |

---

## How to Use This Reference

### For /plan:debt
Use `search_text` to find patterns. Start with CRITICAL patterns, then HIGH. Each match becomes a debt card with the pattern's severity and action.

### For code-reviewer agent
Check modified files against patterns in the "Environment Workarounds", "Error Handling", and "State & Mutability" sections. These are the most damaging if introduced.

### For /plan:test-audit
Focus on "Testing Anti-Patterns" section. Flag tests that don't actually verify behavior.

### For new code review
The "AI-Specific Tells" section helps identify code that needs deeper scrutiny — if it looks AI-generated without review, there may be hidden issues.

---

## Pattern Discovery Log

When you encounter a new anti-pattern in the wild, add it here:

```
## [Date] [Pattern Name]
**Found in:** [project type/context]
**Pattern:** [description or code snippet]
**Search:** [grep pattern if detectable]
**Severity:** [CRITICAL/HIGH/MEDIUM/LOW]
**Why it matters:** [explanation]
**Action:** [what to do]
```
