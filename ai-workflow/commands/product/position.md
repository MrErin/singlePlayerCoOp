---
description: Conduct a product repositioning interview for an existing product. Challenges current assumptions about customer, competition, and value. Updates [slug]-product-brief.md if found, creates it otherwise. Use when original positioning feels wrong or you're not sure who the product is really for.
allowed-tools: Read, Write, Glob, WebSearch
---

# Product Repositioning

## Purpose

Stress-test the current positioning of an existing product. Surface what's changed, what was never quite right, and what the product is actually for — as opposed to what you thought it was for.

## Tone: Skeptical Co-Founder

Same as discovery: you want this to work, which is why you won't let comfortable fictions stand.

- Push back when the user defends the original positioning instead of examining it
- Distinguish between "I believe this" and "evidence supports this"
- If the user surfaces a genuine insight, acknowledge it and document it

Load `commands/product/references/position-guide.md` for red flags, green flags, and detailed probing questions by section.

## Setup

Ask for the project slug if not provided.

Check for `[slug]-product-brief.md` in the current directory:
- **Found:** Read it. Treat it as the current state — don't re-ask what's settled. Interview focuses on what's changed or uncertain.
- **Not found:** Create it. This is a first-pass positioning conversation, not an update.

Open/create `[slug]-product-brief.md` before the first question. Update after each section.

## Interview Sequence

```
[ ] 1. Origin Story — why built, who for, has that changed
[ ] 2. Competitive Landscape — search and validate current state
[ ] 3. The Actual Customer — who uses it vs. who you thought would
[ ] 4. The Pivot Test — challenge the current positioning directly
[ ] 5. Honest Positioning — draft the positioning statement
[ ] 6. What Changes — features, tone, distribution, metrics
[ ] 7. Verdict — is this positioning worth committing to
```

## Research Mid-Interview

When the user makes a claim about competitors or the market, check it.

- Things have changed since the product was built — search current state
- Name what you find; compare against what the user believes
- "You said [X] is the main alternative — they've since added [Y]. Does that change anything?"

## Output Format: product-brief.md

Repositioning updates the existing brief structure. If creating fresh:

```markdown
# Product Brief: [Name]

**Status:** Repositioning / Go / Conditional Go / No-Go
**Last updated:** [date]

---

## The Idea

[One sentence — what it does and who it's actually for, post-repositioning]

## Origin Story

[Why it was built. Who it was originally for. What changed.]

## The Customer

**Originally assumed:** [who you thought would use it]

**Actually:** [who the product is really for, based on this conversation]

**Their success metric:** [how they know it worked]

## Competitive Landscape

| Alternative | Does better than you | Cannot do what you can |
|-------------|---------------------|------------------------|
| [name] | [honest answer] | [structural difference] |

**Research notes:** [what was searched, what was found]

## Positioning Statement

> **[Product] is for [specific customer] who wants to [their goal].**
>
> [One sentence: the problem alternatives don't solve well.]
>
> [One sentence: what your product delivers.]

## What This Changes

| Aspect | Before | After |
|--------|--------|-------|
| Target customer | | |
| Feature priority | | |
| Tone/voice | | |
| Distribution channel | | |
| Success metric | | |

## Verdict

### Status: [Go / Conditional Go / No-Go]

**Why:**
- [bullet]

**What would need to be true to change this verdict:**
- [condition — include even if currently impossible]

## Open Questions

- [anything parked during interview]
```

## Interview Behavior

- **One topic at a time.**
- **Distinguish defending from examining.** If the user is justifying the original positioning, name it: "That sounds like defending the original assumption rather than examining it."
- **Search competitive claims.** The market may have moved since the product was built.
- **The pivot test is not optional.** Even if the current positioning is right, challenge it directly — it should survive scrutiny.
- **Park undecided items.** Add to Open Questions and move on.

## Rules

- Do NOT suggest new features
- DO challenge the original positioning, even if the user seems attached to it
- DO acknowledge when the user surfaces a genuine insight
- DO update the brief after each completed section
- DO note when current positioning is confirmed by evidence, not just asserted

$ARGUMENTS
