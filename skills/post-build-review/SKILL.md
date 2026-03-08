---
name: post-build-review
description: Generate comprehensive review documentation after completing a build. Creates ADHD-friendly guides with checkboxes, time estimates, and progressive disclosure to help users test, understand, and extend the codebase without feeling overwhelmed.
allowed-tools: Read, Write
---

# Post-Build Review

## Purpose

Generate `review_guide.md` after completing any multi-file project or iterative build.

**No git commits.** User controls all git operations.

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
