# SQL-Specific Standards

Use alongside the core `my-style` skill.

## Query Formatting: Leading Commas

```sql
SELECT
     user_id
   , exercise_name
   , total_xp
   , level
FROM user_stats;
```

**Why:** Easy to comment out any line, commas align vertically for scanning, no trailing comma issues.

## Naming Conventions

- **Tables:** Singular nouns, snake_case — `user` not `users`, `exercise_log` not `exercise_logs`
- **Why singular:** Each row represents one entity. Reads naturally: `SELECT * FROM user WHERE...`
- **Why snake_case:** Works without quotes in PostgreSQL, MySQL, SQLite. Maximum portability.
- **Foreign keys:** `{table}_id` — `user_id`, `exercise_id`, `skill_branch_id`
- **Indexes:** `idx_{table}_{columns}` — `idx_exercise_log_user_timestamp`

## Parameterized Queries (Non-Negotiable)

```python
# ✅ Positional parameters
cursor.execute('SELECT * FROM user WHERE id = ?', (user_id,))

# ✅ Named parameters
cursor.execute('SELECT * FROM user WHERE id = :user_id', {'user_id': user_id})

# ❌ NEVER — SQL injection vulnerability
cursor.execute(f'SELECT * FROM user WHERE id = {user_id}')
cursor.execute('SELECT * FROM user WHERE id = ' + str(user_id))
```

Input validation happens at the system boundary (per core `my-style`), before data reaches query functions.

## Migration Best Practices

### Numbered migration files

```sql
-- 001_create_users.sql
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT
  , name TEXT NOT NULL
  , email TEXT UNIQUE NOT NULL
  , created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 002_add_user_xp.sql
ALTER TABLE user ADD COLUMN total_xp INTEGER DEFAULT 0;
```

### Always include rollback

```sql
-- 004_add_skill_branches.sql (up)
CREATE TABLE skill_branch (
    id INTEGER PRIMARY KEY AUTOINCREMENT
  , name TEXT NOT NULL UNIQUE
  , description TEXT
);

ALTER TABLE exercise
ADD COLUMN skill_branch TEXT
REFERENCES skill_branch(name);

-- 004_add_skill_branches_rollback.sql (down)
ALTER TABLE exercise DROP COLUMN skill_branch;
DROP TABLE skill_branch;
```