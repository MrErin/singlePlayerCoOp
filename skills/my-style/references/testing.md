# Testing Standards

## Write Testable Code

Separate pure logic from I/O:

```python
# ✅ Easy to test - no external dependencies
def calculate_xp(exercise_type: str, quantity: int) -> int:
    if exercise_type == 'binary':
        return 10 if quantity else 0
    return 5 * quantity

# ❌ Hard to test - mixed concerns
def process_form():
    data = request.form  # external dependency
    save_xp(calculate_xp(data['type'], data['quantity']))  # I/O
```

## Testing Approach

Write tests before or alongside implementation. **TDD** when design is unclear; **test-alongside** when iterating quickly on clear design. Requirement: coverage exists and covers edge cases before feature is complete.

## Critical Rules

- **Pure unit tests for business logic** — frozen dataclasses as input, no database
- **Zero external IO** — database/network/disk in tests = design failure
- **Edge and corner cases** must be covered
- **Pre-existing tests** must still pass after new features

## Test Design

**One concept per test.** If you need "and" to describe what it verifies, split it.

```python
# ❌ Two concepts    →    # ✅ One concept each
def test_create_user_saves_and_returns():
    assert create_user("Alice").name == "Alice"
    assert get_user("Alice") is not None

def test_create_user_returns_name():
    assert create_user("Alice").name == "Alice"

def test_create_user_persists():
    create_user("Alice")
    assert get_user("Alice") is not None
```

**Descriptive names.** `test_create_user_with_duplicate_name_raises_conflict()` not `test_user()`.

**No conditional logic.** No `if`/`else`, no assertion-generating loops. Each test is linear.

**Proportional setup.** 20 lines of setup for one assertion = test too coupled or code needs refactoring.

## Test Independence

- **Order-independent** — each test self-contained, no relying on prior tests
- **No shared mutable state** — fresh state per test
- **No timing dependencies** — no `sleep()`, use mocks for async

```python
# ❌ Timing-dependent    →    # ✅ Mock time
time.sleep(0.1)                mock_clock.advance(100)
assert result.is_ready()       assert result.is_ready()
```

## AI-Generated Test Rules

AI agents have predictable blind spots. These rules are mandatory for AI-written tests.

**Field Coverage** — Assert ALL fields on returned objects, not just the ones you care about.

**Exact Counts** — Use `==` for counts, never `>=` or `> 0`.

**Negative Test Ratio** — Minimum 1 error/edge case per 2 happy path tests.

**"Would This Fail?" Check** — After writing, ask: if implementation returned wrong data, would this catch it?
- List returned duplicates?
- Create ignored half the input fields?
- Calculation off by 1?

**No Mirror Tests** — Never reimplement production logic in test. Assert `== 25`, not `== 5 * input`.

**No Tautologies** — Asserting setup data tests nothing. The value must be **computed** by the function.

```python
# ❌ Tautology — you set name="Alice"
user = User(name="Alice")
assert get_user("Alice").name == "Alice"

# ✅ Function computed something
user = User(name="Alice", role="admin")
assert get_display_name(user) == "Alice (admin)"
```

**No Section Dividers** — No `# ---` or flowerboxes. Class names are the grouping mechanism.

**No Generic Assertions** — `is not None`, `isinstance(dict)`, `len > 0` never acceptable as sole assertion.

## Test Independence from Implementation

Tests written from **interface contracts**, not implementation code. Test phases run in separate sessions to guarantee test-writer works from contracts, not implementation memory.

## Mocking Framework Objects

When mocking objects from frameworks (LangChain, SQLAlchemy, Django, etc.), plain `MagicMock` often breaks because frameworks use operator overloading, metaclasses, or internal dispatch that bypasses mock's `__getattr__`.

**Common failure modes:**
- `MagicMock` with `|` operator — framework wraps mock in adapter, `invoke()` never called
- `MagicMock` with `>>` or `<<` — pipeline/stream operators create new objects
- `MagicMock` as context manager — `__enter__`/`__exit__` not properly chained
- `MagicMock` with `__iter__` — framework checks for iterator protocol

**Rules:**
1. **Smoke-test your mock.** Before writing 10+ tests with a mock helper, write ONE test that exercises the exact production code path end-to-end with the mock. Run it. If it fails, the mock setup is wrong.
2. **Prefer patching at the call site.** Instead of mocking the object that enters an operator chain, patch the object it chains WITH (e.g., patch the prompt template, not the model).
3. **Use framework test utilities.** Many frameworks provide fake/stub implementations for testing (e.g., LangChain's `FakeListLLM`, Django's `RequestFactory`). Prefer these over MagicMock.
4. **If mock_helper exists, use it.** If conftest.py already has a helper that patches the chain correctly (e.g., `mock_mission_chain`), use it. Don't create a parallel mock setup that bypasses the helper.

## Property-Based Testing

For business logic with invariants, use **Hypothesis** (Python) or **fast-check** (TypeScript) alongside example tests.

**Good candidates:** pure calculations, serialization roundtrips, sort/filter operations, well-defined input domains.

```python
@given(quantity=st.integers(min_value=0, max_value=10000))
def test_xp_never_negative(quantity):
    assert calculate_xp('reps', quantity) >= 0
```

## Seam Tests (Integration at Boundaries)

Verify the handoff between modules. Both may have unit tests with mocked boundaries, but the boundary itself can still break.

**When needed:** Module A calls B, both have mocked unit tests, no test exercises A→B end-to-end.

**What makes a seam test:** Full path across modules, no mocking the boundary itself. External deps (DB, API) may still be mocked.

```python
# Unit test (mocked)            # Seam test (real boundary)
mock_repo = Mock()              repo = InMemoryUserRepo([User(id=1)])
service = UserService(mock_repo)  service = UserService(repo)
service.get_user(1)             result = service.get_user(1)
mock_repo.find_by_id.assert_    assert result.name == "Alice"
  called_once_with(1)
```

**Catches:** contract mismatch, type drift, missing adapters between modules.

## Redundancy

Delete tests exercising the exact same code path with same assertions. Keep if genuinely different scenarios (e.g., `get_user(1)` vs `get_user("1")` — tests string coercion).

## Obsolete Tests

Tests must track code they verify. Delete/update when:
- Function deleted or renamed
- Behavior changed
- Module moved

**Detection:** Failing imports are obvious. Tests that never fail (even when they should) may be orphaned.

## Parallel Module Coverage

Modules sharing architecture (e.g., all repos with `create_many()`) need test parity. If Module A has edge case test X, Module B (same pattern) needs it too. Bug fix without parallel tests invites regression.

## Phase Integration (with iterative-build)

- **Setup/data layer:** Tests optional — verify manually
- **Read/write/logic:** Interface contracts generated during planning, tests in dedicated phase
- **Business logic:** Property-based tests required for pure calculations
- **Test phases can batch** — one phase covers multiple implementation phases
