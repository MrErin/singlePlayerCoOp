# Python-Specific Standards

Use alongside the core `my-style` skill. Formatting (line length, indentation, blank lines) is enforced by Black/Ruff — not repeated here.

## Project Structure

### File Naming

Required names:

- `app.py` — entry point
- `database.py` — all DB operations
- `routes.py` — HTTP handlers (not views.py)
- `services.py` — business logic separate from routes
- `validators.py` — input validation

Group by feature for larger apps: `[feature]/routes.py`, `[feature]/services.py`

## Type Hints

Type hints are required on all public function signatures per core standards. For Python specifically:

```python
# ✅ Public functions — always type hinted
def calculate_xp(exercise_id: int, quantity: float) -> int:
    """Calculate XP for exercise."""
    pass

def get_user(user_id: int) -> dict | None:
    """Fetch user or None if not found."""
    pass

# ✅ Complex structures — use modern syntax (3.10+) or typing imports
def get_exercises() -> list[dict[str, str | int]]:
    """Return list of exercise dictionaries."""
    pass

# ✅ Internal one-liners in small scope — lighter hints acceptable
_format = lambda v: str(v).strip()
```

When `Any` is unavoidable (e.g., JSON payloads before validation), import it properly and comment where validation occurs.

## Connection Management

```python
# ✅ Context manager ensures cleanup
def get_user(user_id: int) -> dict | None:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))
        return cursor.fetchone()

# ❌ Manual management — easy to leak connections
def get_user(user_id: int) -> dict | None:
    conn = get_db_connection()
    cursor = conn.cursor()
    result = cursor.fetchone()
    conn.close()  # Easy to forget, especially on exceptions
    return result
```

For SQL query formatting and parameterization, see `references/sql.md`.