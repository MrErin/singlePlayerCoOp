# Comment Standards

## Core Rule: Explain WHY, Not WHAT

```
# ❌ Bad - explains WHAT (obvious from code)
# Loop through exercises
for exercise in exercises:
    process(exercise)

# ✅ Good - explains WHY (decision rationale)
# Process exercises in order to maintain XP calculation accuracy
# (later exercises may have bonuses dependent on earlier ones)
for exercise in exercises:
    process(exercise)
```

## Comments at Decision Points

```
def calculate_xp(exercise, quantity):
    if exercise.type == 'binary':
        # Binary exercises always award full XP regardless of quantity
        # This prevents gaming the system by logging partial completion
        return exercise.base_xp if quantity else 0
    
    elif exercise.type == 'reps':
        # For reps, we award full XP if any reps completed
        # Future enhancement: scale XP based on rep count
        return exercise.base_xp if quantity > 0 else 0
```

## Document Non-Obvious Choices Only

Do not create comments for trivial or obvious code. No tutorials in the comments.

Good reasons for comments:

- Why this algorithm over alternatives?
- Why this structure?
- What constraint led to this decision?
- What did you try that didn't work?

## Comment Maintenance

When modifying any function or code block, review ALL comments within that scope:

- Remove comments that describe behavior that no longer exists
- Update comments that describe behavior that has changed
- A stale comment is worse than no comment — it actively misleads both humans and AI agents

This applies during all development, not as a separate review pass. The developer (human or AI) modifying the code has the best context for why the change was made and which comments are now wrong.

## Module-Level Docstrings

Every non-trivial file should have a brief docstring at the top describing:

- What this module does (one sentence)
- How it relates to adjacent modules
- Key concepts needed to understand the code

This serves both human onboarding and AI context — agents can understand a file's role without reading every line.

## Interface Contracts on Public Functions

Document what a function promises, not how it works:

```python
def award_xp(user_id: int, exercise: Exercise, quantity: int) -> XPResult:
    """Award XP for completing an exercise.
    
    Returns XPResult with earned amount and new total.
    Returns error if user not found or exercise is inactive.
    Does not persist — caller is responsible for saving.
    """
```