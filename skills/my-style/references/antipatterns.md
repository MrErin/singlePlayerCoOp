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
| Mock protocol mismatch | MagicMock used with operator overloading (`\|`, `>>`, `@`) | HIGH | Verify mock works with actual operator usage; prefer patching call site or using framework test utilities |

---

## Mock Protocol Mismatch (HIGH)

When frameworks use Python's operator overloading (`__or__`, `__ror__`, `__rshift__`, `__matmul__`), MagicMock's auto-generated dunder methods return new MagicMocks instead of following the framework's dispatch protocol.

| Pattern | Detection | Severity | Action |
|---------|-----------|----------|--------|
| MagicMock in pipe chain | `MagicMock()` passed to `\|` operator | HIGH | Patch the prompt/template side, not the model |
| Mock invoke never called | `mock.invoke.called` is False after chain execution | HIGH | Mock is being wrapped, not called directly |
| Mock helper exists but unused | conftest has `mock_X_chain()` but tests use `mock_chat_model()` | HIGH | Use the chain-aware helper |

**Example:**
```python
# BAD: MagicMock doesn't work with LangChain's | operator
mock_model = MagicMock()
mock_model.with_structured_output.return_value = MagicMock()
chain = PROMPT | mock_model.with_structured_output(Schema)  # Wraps mock in RunnableLambda
chain.invoke(data)  # Returns MagicMock, not the configured response

# GOOD: Patch the prompt template to return a mock chain
mock_chain = MagicMock()
mock_chain.invoke.return_value = expected_response
with patch("module.PROMPT") as mock_prompt:
    mock_prompt.__or__ = MagicMock(return_value=mock_chain)
    result = generate(model)  # Works correctly
```

**Why it matters:** Tests compile, collection succeeds, but every test fails at runtime with confusing errors like "Expected X, got MagicMock". The failure is in the mock setup, not the production code.

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

## Import Anti-Patterns (MEDIUM/HIGH)

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| Unused imports | Import not referenced in file | LOW | Remove (let linter catch) |
| Star imports | `from x import *` | HIGH | Import specific names |
| Circular imports | Import errors at module load | HIGH | Restructure or use deferred import |
| Shadow imports | Local name shadows imported name | MEDIUM | Rename one of them |
| Convenience deferred imports | `import` inside function without structural necessity | HIGH | Move to module level |
| Undocumented deferred imports | `import` inside function without comment explaining why | MEDIUM | Add justification comment or move to top |

**When deferred imports ARE acceptable:**
- Avoiding circular imports (document: `# Deferred to avoid circular import with module X`)
- Optional dependencies with graceful degradation (document: `# Optional dependency for feature X`)
- Lazy loading heavy modules at runtime (document: `# Lazy load to reduce startup time`)

**When deferred imports are NOT acceptable:**
- "I forgot to add it at the top"
- "It was more convenient here"
- Avoiding a linter warning about unused imports (remove the import instead)

---

## Linter Bypass Anti-Patterns (HIGH)

Using comments to silence linter warnings instead of fixing the underlying issue.

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| Type ignore without justification | `# type: ignore` without explanatory comment | HIGH | Fix the type issue or document why bypass is necessary |
| Noqa without justification | `# noqa` without explanatory comment | HIGH | Fix the issue or document why bypass is necessary |
| Pylint disable without justification | `# pylint: disable` without explanatory comment | HIGH | Fix the issue or document why bypass is necessary |
| Blanket type ignore | `# type: ignore` (no specific error code) | HIGH | Use specific code (`# type: ignore[attr-defined]`) and justify |
| File-level ignore | `# type: ignore` at top of file | CRITICAL | This is hiding systemic issues — fix them |

**Why it matters:** Linter bypasses accumulate debt silently. Each `# type: ignore` hides a potential bug, incorrect type annotation, or API misuse. The AI uses these as shortcuts to "make the error go away" rather than understanding and fixing the root cause.

**When bypasses ARE acceptable (with documentation):**
```python
# ✅ Documented justification for legitimate bypass
result = external_lib.untyped_func()  # type: ignore[no-untyped-call]  # Third-party lib lacks stubs, filed issue #123
```

**When bypasses are NOT acceptable:**
```python
# ❌ No justification, just silencing the linter
def process(data):  # type: ignore[no-untyped-def]
    return data

# ❌ Should be fixed instead of bypassed
user.name = data.get('name')  # type: ignore[assignment]  # "data might have wrong type"
# FIX: Validate and cast properly
```

---

## Hallucinated APIs (CRITICAL)

AI confidently generates calls to functions, methods, or packages that don't exist. 20-40% hallucination rate on API names in studies.

| Pattern | Detection | Severity | Action |
|---------|-----------|----------|--------|
| Non-existent function call | `python3 -m py_compile <file>` fails on import | CRITICAL | Verify function exists in dependency docs |
| Wrong method signature | Function called with args it doesn't accept | CRITICAL | Check actual signature in library |
| Fake package import | `import` of package not in requirements | HIGH | Verify package exists on PyPI/npm |
| Plausible but wrong attribute | `response.data.items` when API returns `response.results` | CRITICAL | Test against real API response |
| Deprecated API usage | Using removed functions from older library versions | HIGH | Check current library docs |

**Why it matters:** Code compiles and looks correct but crashes at runtime. AI predicts plausible API shapes from training data without verifying against actual library signatures.

**Detection:** Run import smoke tests and `py_compile` checks. For runtime attributes, verify against library documentation or a REPL session.

---

## Resource Management (HIGH)

File handles, database connections, and sockets opened without proper cleanup — especially in error paths.

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| File open without context manager | `open(` not preceded by `with` | HIGH | Use `with open(...) as f:` |
| Connection without cleanup | `.connect(` without corresponding `.close()` or context manager | HIGH | Use context manager or connection pool |
| Missing error path cleanup | Resource acquired in `try`, no `finally` block | HIGH | Add `finally` or use context manager |
| Manual resource lifecycle | Paired `.open()`/`.close()` calls | MEDIUM | Replace with context manager |

```python
# ❌ Leaks on exception
f = open('data.csv')
data = process(f.read())  # If this throws, f is never closed
f.close()

# ✅ Context manager handles cleanup
with open('data.csv') as f:
    data = process(f.read())
```

**Why it matters:** AI generates the happy path and skips cleanup in error paths. Resource leaks cause connection exhaustion and file descriptor limits under load.

---

## Hardcoded Secrets (CRITICAL)

API keys, passwords, and tokens embedded directly in source code. AI reproduces tutorial patterns where secrets are inline for convenience.

| Pattern | Search | Severity | Action |
|---------|--------|----------|--------|
| Credential assignment | `password =`, `api_key =`, `secret =` with string literal | CRITICAL | Move to env var or secrets manager |
| Known key prefixes | `sk_test_`, `sk_live_`, `ghp_`, `glpat_`, `AKIA` | CRITICAL | Rotate immediately, move to env |
| Connection string with credentials | `://user:pass@` in source | CRITICAL | Use env var for connection string |
| Auth header with token | `Bearer ` + string literal | HIGH | Inject token at runtime |
| Commented-out credentials | `# password: ...` or `# mongodb+srv://user:pass@` | HIGH | Remove entirely |

**Why it matters:** Credentials in source code end up in version control. Even after removal, they persist in git history. AI reproduces this pattern because training data is full of tutorials with inline secrets.

---

## Copy-Paste Artifacts (MEDIUM)

When AI implements similar features, it copies and partially adapts code rather than abstracting. Leftover names and parameters from the source context leak through.

| Pattern | Detection | Severity | Action |
|---------|-----------|----------|--------|
| Mismatched variable names | Variable name doesn't match its content (e.g., `users = fetch_products()`) | MEDIUM | Rename to match actual content |
| Unused function parameters | Parameter defined but never referenced in body | MEDIUM | Remove parameter or use it |
| Near-duplicate code blocks | Two functions with >80% identical logic | HIGH | Extract shared logic to common function |
| Partial rename | Some references updated, others still use old name | HIGH | Complete the rename |
| Wrong context in comments | Comment describes different behavior than the code | MEDIUM | Update or remove comment |

**Why it matters:** Copy-paste artifacts confuse future readers (including AI in the next session) and indicate the code wasn't reviewed. Unused parameters mask API surface bugs.

**Detection:** Linters catch unused parameters. Near-duplicates require manual review or tools like `pylint --enable=duplicate-code`.

---

## Dead Code (MEDIUM/HIGH)

Code that exists but is never executed — functions never called, classes never instantiated, modules never imported. Accumulates over multiple build passes as features evolve.

| Pattern | Detection | Severity | Action |
|---------|-----------|----------|--------|
| Uncalled functions | Function defined but name never appears in call site | HIGH | Verify unused, then remove |
| Orphan classes | Class defined but never instantiated or imported elsewhere | HIGH | Verify unused, then remove |
| Unreachable branches | Code after `return`/`raise`, impossible conditions | MEDIUM | Remove dead branches |
| Exported but unused | Public function/class with no external callers | MEDIUM | Make private or remove |
| Zombie imports | Import statement for module never used | LOW | Remove (linter catches) |
| Commented-out code | Large blocks of code in comments | MEDIUM | Delete — git is the history |
| Dead feature flags | Feature flag checks for removed features | HIGH | Remove flag and dead branch |

**Why it matters:** Dead code increases cognitive load, slows down IDEs and linters, and confuses AI agents who try to understand relationships that no longer exist. Multiple build passes leave behind "just in case" code that never gets used.

**Detection challenges:**
- Dynamic calls (`getattr(obj, method_name)`) hide usage — grep for the string literal
- Test fixtures may reference "unused" code — check test files
- API endpoints may look unused but are called externally — check route decorators
- Plugin/extension points may be intentionally unused yet — document these

**Verification process:**
1. Find candidate via jcodemunch `search_symbols` + `search_text`
2. Grep for all references to the symbol name
3. Check for dynamic invocation patterns
4. Verify not used in tests, configs, or external APIs
5. Only then create CLEANUP card

---

## How to Use This Reference

### For /plan:debt
Use `search_text` to find patterns. Start with CRITICAL patterns, then HIGH. Each match becomes a debt card with the pattern's severity and action. Include Hallucinated APIs, Resource Management, Hardcoded Secrets, and Dead Code sections. For dead code, use jcodemunch `get_file_outline` to list symbols, then `search_text` to verify each has callers.

### For code-reviewer agent
Check modified files against: Environment Workarounds, Error Handling, State & Mutability, Database/API Patterns, Resource Management, and Hardcoded Secrets. These are the sections most likely to introduce bugs per-task.

### For test-writer agent
Check your own output against "Testing Anti-Patterns" before delivering. AI-generated tests have the same blind spots documented here — mirror tests, tautological assertions, and happy-path-only coverage.

### For /plan:test-audit
Focus on "Testing Anti-Patterns" and "Copy-Paste Artifacts" sections. Flag tests that don't actually verify behavior or that were duplicated across test modules without adaptation.

### For new code review
The "AI-Specific Tells" and "Copy-Paste Artifacts" sections help identify code that needs deeper scrutiny — if it looks AI-generated without review, there may be hidden issues.

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
