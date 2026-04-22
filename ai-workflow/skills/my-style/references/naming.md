# Variable Naming Conventions

## Descriptive Over Short

- Use full words: `user_total_xp` not `utxp`
- Avoid abbreviations except common ones: `db`, `id`, `url`, `api`
- Context-appropriate length:
    - Local variables: Can be shorter in small scopes
    - Function parameters: Always descriptive
    - Class/module constants: Very descriptive

## Boolean Naming

Always prefix with `is`, `has`, or `can`:

```
is_valid = check_validation()
has_permission = user.check_access()
can_submit = form.is_complete()
```

## Collection Naming

Plurals for collections, singular for items:

```
exercises = get_all_exercises()  # Collection
exercise = exercises[0]          # Single item

user_list = fetch_users()        # Collection
current_user = user_list[0]      # Single item
```

## Loop Counter Exception

Single letters acceptable ONLY for loop counters:

```
# ✅ Acceptable
for i in range(10):
    print(i)

# ❌ Not acceptable elsewhere
x = get_user_data()
y = calculate_total(x)
```

---

## Cross-Layer Naming Consistency

When two parts of the same system refer to the same concept, they use the same name. One concept, one name — everywhere it appears.

If the backend calls something `ProductVariant`, the frontend calls it `ProductVariant`. If a Python model is `OrderItem`, the TypeScript type is `OrderItem`. Names travel with the concept across layers.

**API-derived types are a hard case, not a soft one.** Types shaped by `response.json()` from your own backend must use the backend's exact property names — no mapping layer, no renaming. The casing may differ (camelCase in TypeScript is fine), but the *words* must match. If the backend returns `{ daily_tasks: [...] }`, the TypeScript type has `daily_tasks`, not `tasksOfTheDay`.

### When Mappers Are Acceptable

Only at **external system boundaries** — where you don't control the naming:

- Parsing a third-party API response
- Reading from a legacy system with fixed field names
- Consuming a webhook payload from an external service

### The Anti-Pattern: Spurious Adapter

A mapper created to paper over a rename that wasn't propagated:

```typescript
// ❌ Backend renamed the fields — frontend wasn't updated, mapper added instead
const toFrontendUser = (user: BackendUser): User => ({
  id: user.userId,
  name: user.displayName,
});

// ✅ Rename the frontend interface to match — no mapper needed
interface User {
  userId: string;
  displayName: string;
}
```

The mapper feels like a solution but it creates two names for one concept. Every future developer must learn both names and follow the translation. When the backend changes again, the mapper grows.

### File Renames

When a type rename requires renaming a file, **always use `git mv`** — never delete and recreate. Deleting a file and recreating it under a new name destroys git history for that file.

```bash
git mv src/types/user.ts src/types/user-profile.ts
```

This must be done manually. Never delegate file renames to an agent.

### Detection Patterns

```bash
# Mapper/adapter/transform files (any typed language)
grep -rl --include="*.ts" --include="*.tsx" --include="*.py" --include="*.js" \
  -E '(mapper|transform|adapter)\.(ts|tsx|py|js)$' .

# Type conversion functions (to/from prefix signals divergence)
grep -rnE '(const|function|def)\s+(to|from)[A-Z_][a-zA-Z_0-9]+\s*[=(]' \
  --include="*.ts" --include="*.tsx" --include="*.py"

# Explicit field-rename mapping objects (TypeScript)
grep -rnE 'const\s+\w+(Map|Mapping|Mapper|Keys)\s*=\s*\{' \
  --include="*.ts" --include="*.tsx"

# Type alias that purely renames another type (may hide "we used to call this X")
grep -rnE '^(export\s+)?type\s+\w+\s*=\s*\w+\s*;' \
  --include="*.ts" --include="*.tsx"

# Pydantic field aliases — legitimate at API boundary, suspect if internal
grep -rnE 'Field\s*\(\s*alias\s*=' --include="*.py"
```

For each match: determine whether the mapper is at a genuine external boundary. If it bridges two parts of your own system, it is HIGH severity — identify the canonical name (usually the backend/source-of-truth name) and document the rename needed.

**Severity:**
- **HIGH** — mapper bridges two parts of the same system
- **MEDIUM** — mapper detected, boundary unclear; flag for human review