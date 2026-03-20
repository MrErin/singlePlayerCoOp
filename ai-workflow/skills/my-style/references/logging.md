# Logging Standards

## What to Log

- **At boundaries only:** Route handlers, controllers, event handlers
- **Log:** Entry/exit points, external service calls, state transitions, errors
- **Don't log:** Internal business logic calculations, sensitive data (passwords, tokens, PII)

## Log Levels

- `ERROR`: System-level failures requiring attention (database down, external API failure)
- `WARN`: Unexpected but recoverable situations (fallback used, deprecated path taken)
- `INFO`: Significant business events (user logged in, order completed, challenge earned)
- `DEBUG`: Detailed execution flow (disabled in production)

## Structure

Use structured logging (key-value pairs) for searchability:

```
logger.info("Exercise logged", {exercise_code: "BAL-1", xp_earned: 15, user_level: 3})
```

## Business Logic and Logging

Business logic must never log directly. Instead, return information (results, status, metrics) that the calling route/controller can log if needed. This keeps business logic pure and testable.