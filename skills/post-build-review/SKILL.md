---
name: post-build-review
description: Generate comprehensive review documentation after completing a build. Creates ADHD-friendly guides with checkboxes, time estimates, and progressive disclosure to help users test, understand, and extend the codebase without feeling overwhelmed.
allowed-tools: Read, Write, Glob
---

# Post-Build Review

## Purpose

Generate `review_guide.md` in the project root after completing any multi-file project or iterative build. For feature additions, generate as `feature_[name]_review_guide.md`.

## Resume Detection

Before starting, check if `review_guide.md` exists with `<!-- STATUS: DRAFT -->`. If so, read it to identify which sections are already written. Continue from the next unwritten section — do not redo completed sections.

## Progressive Output Strategy

This document can be large. To preserve work if interrupted:
1. **Scaffold first** — Write the document header with `<!-- STATUS: DRAFT -->` and all section headings (empty)
2. **Write incrementally** — Complete each section and append to the file before starting the next
3. **Mark complete** — Replace `<!-- STATUS: DRAFT -->` with `<!-- STATUS: COMPLETE -->` only when all sections are done

## Steps

1. **Resume Check**: If `review_guide.md` (or `feature_*.md` for feature additions) exists with `<!-- STATUS: DRAFT -->`, read it. Identify which sections have content and resume from the next empty section.
2. **Read Context**:
    - `_planning/requirements.md` — what was built and why
    - `_planning/codebase.md` — project structure
    - `_planning/decisions.md` — architectural choices made
    - `_planning/lessons.md` — pitfalls to highlight
    - Phase `plan.md` files — what each phase built
    - Use Glob to find source files in the project
3. **Scaffold the document**: Write the output file (`review_guide.md` or `feature_[name]_review_guide.md`) with:
    - `<!-- STATUS: DRAFT -->` marker at top
    - Title and all six section headers (empty placeholders)
    - This file is now the working output
4. **Generate section by section** (in order, writing each to disk before continuing):
    - **Quick Start** — prerequisites, setup steps, expected output
    - **Feature Testing** — one subsection per feature with test steps
    - **Code Understanding** — levels 1-5 with file-by-file guides
    - **Testing Guide** — automated and manual testing instructions
    - **Known Issues** — honest inventory of gaps and limitations
    - **Next Steps** — ordered by effort with estimates
    - **Append each completed section to the file before starting the next.**
5. **Finalize**: Replace `<!-- STATUS: DRAFT -->` with `<!-- STATUS: COMPLETE -->`.
6. **Output**: Show the user the completed guide or the resume point if interrupted.

## ADHD Requirements (Critical)

Every section must have:
- [ ] Checkboxes for progress tracking
- [ ] Time estimates (realistic)
- [ ] Numbered steps
- [ ] Expected output per step

Document structure:
- Progressive disclosure (simple → complex)
- Short sections (5-20 min each)
- Multiple session completable
- Clear stopping points

## Required Sections

### 1. Quick Start (5 min)

Prerequisites checklist → numbered setup steps → expected output → troubleshooting redirect.

### 2. Feature Testing (15-20 min)

For each feature: description, test steps (checkboxes), expected results, verification method, common issues.

### 3. Code Understanding (30-45 min)

Structure as levels:
- Level 1: Data Structure
- Level 2: Data Flow
- Level 3: Application Logic
- Level 4: Database Operations
- Level 5: Frontend

For each file: read time, one-sentence purpose, key concepts, what to notice, what to skip, optional hands-on test.

**Order logically, not alphabetically.**

### 4. Testing Guide

Automated: how to run, what validates, coverage, how to add.
Manual: main feature testing instructions.

### 5. Known Issues

Honest list: unimplemented features, technical limitations, edge cases, performance, browser compatibility.

### 6. Next Steps

Ordered by effort:
1. Easiest (1-2 hours)
2. Medium (3-5 hours)
3. Larger (8+ hours)

Each: complexity, impact, files, approach.

## What to Skip

- Trivial comments
- Line-by-line walkthroughs
- Standard algorithm explanations
- Setup covered in phase testing docs

## Focus on

- Why decisions were made
- How pieces connect
- Where to look for specific features
- What to test for verification

## Integration

**Greenfield:** Generate after Phase 5 complete.

**Feature addition:** Generate as `feature_[name]_review_guide.md`.

## Critical Reminders

- User has ADHD — structure reduces cognitive load
- Checkboxes provide progress sense
- Time estimates help planning
- Testing-first approach (do before reading code)
- Code reading order is logical
- Break into resumable sections
