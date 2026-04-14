---
name: copywriting
description: Write blog posts, marketing copy, landing pages, and short-form content that reads as human-authored. Enforces anti-AI-writing patterns, varied structure, and genuine voice.
allowed-tools: Read, Write, Edit
skills:
  - my-style
---

# Copywriting

Write blog posts, marketing copy, landing pages, docs intros, and other short-form content that sounds like a specific person wrote it, not a language model.

**Invoke with:** `/copywriting` or when the user asks to write, edit, or review copy.

# Load First

Before writing a single word, load `references/ai-writing-antipatterns.md` and `my-style`. The antipatterns reference is mandatory — it defines the ban list and structural rules. `my-style` provides formatting and voice standards.

# Writing Principles

## Voice

- Sound like a specific person, not a brand. Quirks, opinions, and mild irreverence are features.
- Matter-of-fact over enthusiastic. Neutral tone is fine. Fake positivity is the tell.
- Use contractions. Start sentences with "And" or "But" sometimes. Break minor grammar rules when it sounds better.
- Have opinions. "I think X is wrong" is better than "X has both benefits and drawbacks."

## Structure

- Vary paragraph length deliberately. Mix 1-2 sentence paragraphs with longer ones.
- Vary sentence length. Short sentences land harder after a long one.
- Open with something specific, not a generic hook. Close briefly — 1-2 sentences.
- Don't announce what you're about to say. Say it.
- Don't summarize at every level. One conclusion, not fractal summaries.
- Use "also" or "and" instead of "moreover," "furthermore," or "additionally."
- Break the rule-of-three rhythm. Use two or four items sometimes.

## Specificity

- Every claim needs a concrete anchor: real names, real numbers, real examples.
- Use proper nouns. "PostgreSQL 16" not "modern databases." "4 hours" not "significant time."
- Don't tell the reader what they already know. Tell them something new.

## Banned Patterns

The full ban list is in `references/ai-writing-antipatterns.md`. Key rules:

- No words from the ban list. No exceptions.
- No corrective antithesis ("It's not X, it's Y"). Just say Y.
- No dramatic countdowns ("Not X. Not Y. Just Z."). Lead with the point.
- No adverb-fronted authority ("Crucially, ..."). Let the content justify itself.
- No nominalization ("conduct an investigation" → "investigate"). Use the verb.
- No superficial participial tagging ("...highlighting its significance"). Delete it or make it its own sentence.
- No thematic echo. Say each thing once, then move on.

# Workflow

## When the user asks to write something new

1. **Clarify scope**: What's the piece? Who's the audience? Where will it live?
2. **Ask for voice input**: "Anything you want me to match — a previous post, a tone, things you hate in writing?" If they provide a sample, read it and mirror the patterns.
3. **Draft section by section**. Write each section to disk before starting the next (prevents lost work on long pieces).
4. **Self-check against antipatterns** before presenting. Run through the Quick Self-Check in the reference.
5. **Present the draft**. Note any spots where you made a deliberate style choice and why.

## When the user asks to review or edit existing copy

1. **Read the copy**.
2. **Flag antipatterns** by category (banned words, structural issues, tone, specificity). Cite the reference.
3. **Propose fixes** for each flag. Show the before/after.
4. **Apply fixes** only after user approves.

## When the user asks to rewrite in a different voice

1. Read the source material.
2. Ask: "What voice? Give me a sample or describe it — dry humor, technical, casual, formal."
3. Rewrite. Apply antipatterns rules to the new version too.

# Output

- Blog posts and articles: write to the project or location the user specifies.
- Short copy (intros, blurbs, taglines): output inline unless the user says otherwise.
- Reviews of existing copy: output inline with before/after diffs.

# What This Skill Is Not

- Not a content strategy tool. It writes and edits copy.
- Not an SEO optimizer. Write for humans; if the user asks about SEO, address it directly but don't sacrifice voice for keywords.
- Not a replacement for the user's judgment. If something feels off to them, trust that over the rules.
