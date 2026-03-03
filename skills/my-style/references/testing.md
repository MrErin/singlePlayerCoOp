# Testing Standards

## Write Testable Code

Separate pure logic from I/O:

```python
# ✅ Easy to test (pure function)
def calculate_xp(exercise_type: str, quantity: int) -> int:
    """Calculate XP - no external dependencies."""
    if exercise_type == 'binary':
        return 10 if quantity else 0
    return 5 * quantity

# Then use it in context
def process_form():
    """Route handler - uses testable function."""
    data = request.form
    xp = calculate_xp(data['type'], data['quantity'])
    save_xp(xp)
    return redirect('/success')
```

## Testing Approach

Write tests before or alongside implementation for business logic and complex operations.

- **Strict TDD (red-green-refactor):** Valid path, especially useful when the design isn't clear yet — tests help discover the interface.
- **Test-alongside:** Also acceptable when the design is clear and you're iterating quickly. Write tests as the implementation takes shape.
- **The requirement:** Test coverage exists and covers edge cases before a feature is considered complete.

## Critical Rules

- **Pure unit tests for business logic.** Use frozen dataclasses (or equivalent) as input. No database access in tests.
- **Zero external IO.** Any test requiring a database connection, network call, or disk access is a design failure, not a test infrastructure problem.
- **Edge and corner cases** must be covered.
- **Pre-existing tests** must still pass after new features are developed.


## AI-Generated Test Rules

AI agents produce tests with predictable blind spots. These rules are mandatory when AI writes tests, and good practice for human-written tests too.

### Field Coverage

For any model/object returned from a function under test, assert ALL fields — not just the ones relevant to the current test scenario. If `get_user()` returns a User with 8 fields, all 8 fields get asserted.

### Exact Count Assertions

Never use `>=` or `assertTrue(len(result) > 0)` for count assertions. Always use `==` with the exact expected count. Know exactly what your test data produces.

### Negative Test Ratio

Minimum 1 error/edge case test per 2 happy path tests. AI defaults to happy path — this rule forces thinking about what goes wrong. Every public function with error conditions needs at least one test that triggers each error path.

### "Would This Fail?" Self-Check

After writing each test, ask: "If the implementation returned wrong data, would this test catch it?" Specifically:

- If a list function returned duplicates, would this test fail?
- If a create function ignored half the input fields, would this test fail?
- If a calculation was off by 1, would this test fail? 
 
If the answer is "no," the test is insufficient. Fix it before moving on.

### No Mirror Tests

Never reimplement the production calculation inside a test and assert they match. Tests must assert against independently-determined expected values. If `calculate_xp` multiplies by 5, the test asserts `== 25` for input 5, not `== 5 * input`.

### No Generic Assertions

These assertions are never acceptable as the sole assertion in a test:

- `assert result is not None`
- `assert isinstance(result, dict)`
- `assert len(result) > 0` They may appear alongside specific assertions, but never alone.

## Test Independence from Implementation

Tests should be written from **interface contracts**, not from reading the implementation code. During phase planning, interface contracts are generated that describe what each public function promises — inputs, outputs, invariants, and error conditions.

Test phases are separate phases run in a **new session**. This is a structural guarantee that the test-writing agent works from contracts rather than implementation memory. See the `iterative-build` skill for how test phases fit into the phase system.

## Property-Based Testing

For business logic with clear invariants, use **Hypothesis** (Python) or **fast-check** (TypeScript) alongside example-based tests. Property-based tests define rules that must hold for all valid inputs, then the framework generates hundreds of random inputs to find counterexamples.

Good candidates for property-based tests:

- Pure calculation functions with mathematical properties (e.g., XP is always non-negative)
- Serialization/deserialization roundtrips
- Sort/filter operations (output is always a subset of input, ordering is preserved)
- Any function where the valid input domain is well-defined

```python
from hypothesis import given, strategies as st

@given(quantity=st.integers(min_value=0, max_value=10000))
def test_xp_never_negative(quantity):
    result = calculate_xp('reps', quantity)
    assert result >= 0

@given(quantity=st.integers(min_value=1, max_value=10000))
def test_reps_xp_scales_with_quantity(quantity):
    result = calculate_xp('reps', quantity)
    assert result == 5 * quantity
```

Property-based tests complement example-based tests — they don't replace them. Use example-based tests for specific documented behaviors and property-based tests for invariants across the input space.

## Phase Integration (with iterative-build)

- **Setup and data layer phases:** Tests optional — schema and simple queries are straightforward to verify manually.
- **Read/write/logic phases:** Interface contracts generated during planning. Tests written in a dedicated test phase in a new session.
- **Business logic phases:** Property-based tests required for pure calculation functions alongside example-based tests.
- **Test phases can batch:** One test phase can cover multiple preceding implementation phases.