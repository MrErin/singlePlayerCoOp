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