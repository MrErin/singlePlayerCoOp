# Audit Scorecard Template

Load this file when writing a new snapshot entry to `_planning/audit-scorecard.md`.

Prepend the new entry (newest at top). Create the file with the header if it doesn't exist.

---

## File Header (write once, on first creation)

```markdown
# Audit Scorecard History

_Append-only. Newest entry at top. Persists across /plan:archive — do not delete._

---
```

---

## Entry Format

```markdown
## [YYYY-MM-DD]

### Coverage & Mutation
| Branch coverage | [n%] |
| Mutation score | [n% or "deferred"] |
| Zero-coverage modules | [n] |

### Test Quality
| Total tests | [n] |
| Total assertions | [n] |
| Assertion ratio | [n.n] |
| Tests with 0 assertions | [n] |
| Skipped tests | [n] |
| Largest file assertion share | [n%] |

### Summary
| Category | Review cards | Auto-fix items |
|----------|-------------|----------------|
| DOC | [n] | [n] |
| Debt | [n] | [n] |
| Test | [n] | [n] |
| **Total** | [n] | [n] |

---
```
