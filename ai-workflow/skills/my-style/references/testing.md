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

## Mocking Philosophy

Mock at the boundary between your code and the outside world. Don't mock internals.

- **Mock:** External I/O (network, filesystem, database, LLM calls, third-party APIs)
- **Don't mock:** Internal functions you're trying to test — mock the seam below them, not the function under test
- **Coupling signal:** If mocking 5+ things to test 1 function, the design is too coupled — refactor the code, don't add more mocks
- **Integration > unit for AI-generated code:** Unit tests with mocks only verify "this code calls these functions." Integration tests verify "the right thing actually happens." AI-generated code benefits more from the latter because it catches hallucinated APIs, wrong argument order, and logic errors that mocked tests can't see.

## Critical Rules

- **Pure unit tests for business logic** — frozen dataclasses as input, no database
- **Zero external IO** — database/network/disk in tests = design failure
- **Edge and corner cases** must be covered
- **Pre-existing tests** must still pass after new features

## Test Class Naming

**Pattern:** `Test[Feature]` or `Test[Feature][Category]` where Category is a specific subset.

```python
# ✅ Clear scope
TestUserAuthentication   # All auth-related user tests
TestOrderPricing         # All pricing calculations for orders
TestInventoryQueries     # All inventory read operations

# ❌ Vague or misleading
TestUserCRUD             # If not testing all CRUD operations
TestUser                 # Too broad — what aspect?
TestUserHelper           # Helpers are implementation detail
```

**CRUD claim rule:** If class name includes `CRUD`, it MUST test all four operations:
- **C**reate — happy path + validation failures
- **R**ead — single fetch + list + not-found cases
- **U**pdate — happy path + immutable field attempts
- **D**elete — happy path + not-found handling

If testing only a subset, name accordingly: `TestUserRead`, `TestOrderMutations`.

## Test Method Naming

**Behavior-focused plain English.** Describe what the system does, not which method is called.

```python
# ✅ Behavior-focused — survives refactoring
test_login_fails_with_expired_password
test_order_total_includes_regional_tax
test_duplicate_email_shows_error

# ❌ Method-coupled — brittle, tells nothing about requirements
test_login
test_process_order
test_validate_email
```

**Pattern:** `test_[action]_[condition]_[expected_result]`

The action is what the user/system does, not the method name.

## Category-Specific Test Classes

When testing a function that dispatches on categories, types, or variants (e.g., an enum, a status field, an entry type), organize tests into per-category classes.

**Pattern:** `Test{FunctionName}{CategoryName}` — one class per category, testing that category's specific behavior (section headers, output shape, category-specific fields).

Cross-cutting concerns (parameter validation, error handling, budget enforcement) go in separate classes named for the concern: `Test{FunctionName}ErrorHandling`, `Test{FunctionName}TokenBudget`.

**Anti-patterns:**
- ❌ `TestBuildContextIntegration` with 8 tests spanning 4 categories — split by category
- ❌ `TestMisc` or `TestOther` catch-all classes — if a class has >3 tests covering different categories, split them
- ❌ Generic test names like `test_produces_valid_output` — name for what specifically is verified: `test_testing_category_includes_coverage_subsection`

**Audit signal:** Flag classes named `*Integration*`, `*Misc*`, `*Other*` with more than 3 tests. Flag test names referencing specific categories that live in a generic class.

## Test Suite Structure

**Standard categories by module type:**

| Module Type | Required Test Categories |
|-------------|-------------------------|
| Repository/DAO | Create, Read (single + list), Update, Delete, Not Found cases |
| Service | Happy path, validation errors, business rule violations |
| API/Endpoint | Auth, success response, error responses, malformed input |
| Calculator/Pure | Happy path, edge cases, boundary values, property invariants |

**Parallel modules must have parallel tests.** If `UserRepo` has `create_with_duplicate_raises`, then `OrderRepo` needs the equivalent.

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

**Name-Assertion Alignment** — Test name must describe what's actually asserted, not a side effect or unrelated behavior.
- ❌ `test_file_created` that only asserts a mock was called
- ✅ `test_file_created` that asserts `path.exists()` or the file content

**No Mirror Tests** — Never reimplement production logic in test. Assert `== 25`, not `== 5 * input`.

**No Tautologies** — Asserting setup data tests nothing. The value must be **computed** by the function. This applies to ALL languages and frameworks, not just Python.

```python
# ❌ Tautology — you set name="Alice"
user = User(name="Alice")
assert get_user("Alice").name == "Alice"

# ✅ Function computed something
user = User(name="Alice", role="admin")
assert get_display_name(user) == "Alice (admin)"
```

```tsx
// ❌ Tautology — you pass level_name="Intermediate"
render(<ProgressOverview level_name="Intermediate" />)
expect(screen.getByText('Intermediate')).toBeInTheDocument()

// ✅ Component computed something — conditional branch
render(<ProgressOverview next_level_xp={null} />)
expect(screen.getByText('Maximum Level Reached!')).toBeInTheDocument()
```

**The replacement test:** If you can replace the function/component with `return input` (or `<div>{props.x}</div>`) and the test still passes, it's a tautology.

**No Section Dividers** — No `# ---` or flowerboxes. Class names are the grouping mechanism.

**No Generic Assertions** — `is not None`, `isinstance(dict)`, `len > 0` never acceptable as sole assertion.

## React / JSX Component Testing

Component tests have a different failure mode than function tests: it's trivially easy to write tests that pass by accident because they only verify that React renders props. These tests create false confidence.

### The "Would This Catch a Bug?" Standard

Before writing a component test, ask: **if the component's logic were wrong, would this test fail?**

If the answer is "no" or "only if someone deleted the JSX entirely," the test is not worth writing. Replace it with a test that exercises actual behavior.

### Prop-In-Text-Out Is a Tautology

Passing a prop and asserting that value appears in the DOM is the React equivalent of `assert x == x`. The test checks React's rendering pipeline, not your component's logic.

```tsx
// ❌ Tautology — tests React, not the component
test('renders level name', () => {
  render(<ProgressOverview level_name="Intermediate" />)
  expect(screen.getByText('Intermediate')).toBeInTheDocument()
})

// ❌ Same problem, even with multiple props
test('renders name and XP', () => {
  render(<BadgeCard name="First Steps" achievements_completed={1} />)
  expect(screen.getByText('First Steps')).toBeInTheDocument()
  expect(screen.getByText('1/3')).toBeInTheDocument()
})

// ✅ Tests component logic — the conditional branch
test('shows maximum reached when no next level', () => {
  render(<ProgressOverview next_level_xp={null} total_xp={500} />)
  expect(screen.getByText('Maximum Level Reached!')).toBeInTheDocument()
})
```

**Rule:** A render-only assertion (prop appears in DOM) is acceptable ONLY when testing a conditional rendering branch. If the prop ALWAYS appears regardless of other props/state, the test is a tautology.

### Test Behavior, Not Rendering

Component tests should focus on what the component **does**, not what it **looks like**:

**Test these:**
- Conditional rendering based on computed values (not raw props)
- User interactions (clicks, selections, form submissions)
- Callback firing with correct arguments
- State transitions (loading → error → success)
- Side effects (timers, scroll lock, focus management)
- Data fetching lifecycle (mount fetch, refetch on prop change)

**Don't test these (unless they're conditional):**
- That a prop value appears as text in the DOM
- That child components render (that's the child's responsibility)
- CSS class names (they break on style refactors with zero logic change)
- Hardcoded label text (they break on copy changes with zero logic change)

### API Wrapper Tests: Skip or Consolidate

When the production code is a thin `fetch` wrapper with no business logic (URL construction + `response.json()` + error check), individual unit tests have negative value — they test the mock framework, not application code.

**When to skip entirely:** If the function is `fetch(url) → response.json()` with no transformation, parameter construction, or conditional logic beyond `if (!response.ok) throw`, do not write a test for it.

**When to consolidate:** Multiple API wrappers in the same module can share a single integration test that verifies URL construction, parameter encoding, and error handling in one test per non-trivial function.

**What IS worth testing in API modules:**
- Non-obvious error handling (e.g., HTTP 409 treated as success)
- Request body construction (verify `activity_id`, `bonus_completed` are in the POST body)
- Query parameter construction with multiple filters
- Error message parsing from response body (especially fallback paths for non-JSON responses)

### Factory-Default Tautologies

When using test factories, asserting that factory defaults appear in the output is a tautology wrapped in indirection:

```tsx
// ❌ Tautology — factory default passes through unchanged
const response = createActivitiesResponse()  // creates { activities: [{ name: 'Forward Crossovers' }] }
render(<ActivityList activities={response.activities} />)
expect(screen.getByText('Forward Crossovers')).toBeInTheDocument()

// ✅ Tests computed behavior — filter logic, sorting, conditional display
const activities = createActivitiesResponse({ activities: [
  createActivity({ name: 'A', branch_code: 'BAL' }),
  createActivity({ name: 'B', branch_code: 'CORE' }),
]})
render(<ActivityList activities={activities} filterBranch="BAL" />)
expect(screen.getByText('A')).toBeInTheDocument()
expect(screen.queryByText('B')).not.toBeInTheDocument()
```

**Rule:** When asserting values from factory-created data, the value must be **computed** by the component (filtered, transformed, formatted, conditionally shown) — not passed through unchanged.

### Interaction Tests Over Render Tests

The ratio in a component test file should favor interaction and behavior tests over render-only tests. A file with 7 render tests and 3 interaction tests is inverted.

**Target ratio:** At least 50% of tests in a component file should exercise behavior (interactions, callbacks, state transitions, conditional branches).

### Thin Wrapper Components

Components that only compose other components (e.g., `ProgressView` renders `<ProgressOverview />`, `<BranchBreakdown />`, `<XPGraph />`) have no logic to test. Do not write render tests for them — the child components' tests provide that coverage.

**Exception:** If the wrapper conditionally shows/hides children, test that conditional logic.

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

## Blocking Entry Points Must Be Mocked

When a CLI command, API endpoint, or orchestrator calls a blocking function (TUI `app.run()`, HTTP server `serve_forever()`, event loop `run_until_complete()`), tests that exercise that code path **must mock the blocking call**. Otherwise the test hangs indefinitely waiting for interactive input or a shutdown signal.

**Common pattern:** CLI command evolves to launch an interactive session (e.g., TUI). Existing tests mocked business logic but not the new blocking call. Tests pass in CI until the code path changes, then silently hang.

**Rule:** When a code path gains a blocking entry point, add a mock for it in every test that reaches it. Treat unmocked blocking calls like unmocked network I/O — a test isolation failure.

```python
# ❌ Hangs — investigate reaches _launch_tui → app.run() blocks forever
with patch("myapp.cli.create_campaign", return_value=mock_campaign):
    runner.invoke(app, ["investigate", str(repo)])

# ✅ Mock the blocking entry point
with (
    patch("myapp.cli.create_campaign", return_value=mock_campaign),
    patch("myapp.cli._launch_tui"),  # blocks without this
):
    runner.invoke(app, ["investigate", str(repo)])
```

**Detection:** Test suite hangs at a fixed percentage. The stalled test is always immediately after the last passing test in pytest -v output.

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

## Test File Organization

**Tests belong in existing test modules.** Match the project's test structure:

| Source File | Test File |
|-------------|-----------|
| `src/services/user.py` | `tests/services/test_user.py` |
| `src/repo/order.py` | `tests/repo/test_order.py` |

**Never create catch-all test files.** Names like `test_phase20_functions.py`, `test_bugfixes.py`, or `test_misc.py` are forbidden. They:
- Hide related tests across multiple files
- Make test discovery harder
- Signal "I didn't check where this belongs"

**When adding tests for bug fixes:**
1. Find the existing test file for that module
2. Add a test class or method to that file if the appropriate test class or method does not exist
3. If no test file exists, create one with the canonical name (`test_<module>.py`)

**Exception:** If the bug spans multiple modules and requires integration-style testing, create a file named for the *feature* being tested (e.g., `test_checkout_flow.py`), not the *phase* that found it.

### Frontend (Vitest + React)

All frontend tests live in a single flat directory beneath `src/`:

```
frontend/src/tests/
├── BadgesView.test.tsx
├── ActivityCard.test.tsx
├── ProgressView.test.tsx
└── ...
```

**Rules:**

- **Location:** `src/tests/` — one directory, flat, no subdirectories
- **Naming:** `[Component].test.tsx` — matches the component under test
- **Vitest include:** `src/tests/**/*.{test,spec}.{ts,tsx}`
- **No co-location** — tests do not live next to their source files

**Why:** A single tests directory keeps test infrastructure (MSW server, setup files) close to the tests, avoids cluttering component directories, and makes test discovery trivial — one glob finds everything.

## Test Adequacy Verification

Checklist for verifying test completeness during review (used by `/plan:review` and `code-reviewer`).

For each function or feature added, verify tests exist for all three categories:

| Category | What to check | Common gaps |
|----------|--------------|-------------|
| **Success path** | Primary happy path with realistic input produces correct output | Missing for utility functions, "obvious" helpers |
| **Failure/error path** | At least one invalid-input or error-condition test per function | Missing `None`/null handling, type errors, permission denied |
| **Boundary conditions** | Empty input, `None`/null, zero, max values, empty collections | Missing edge-of-domain tests that expose off-by-one and type errors |

**Minimum standard:** 1 error/edge case test per 2 happy path tests (see "Negative Test Ratio" above).

**Verification method:** After identifying functions added in a phase, grep for test classes/functions covering each one. If a function has tests but all are success-path, flag it as under-tested — even if the tests pass.

## Phase Integration (with iterative-build)

- **Setup/data layer:** Tests optional — verify manually
- **Read/write/logic:** Interface contracts generated during planning, tests in dedicated phase
- **Business logic:** Property-based tests required for pure calculations
- **Test phases can batch** — one phase covers multiple implementation phases
