# Contents

This project is a repository of working files that build my solo developer AI-assisted development workflow. 
Do not suggest changes to the locations of files in this repository. These are the working files. I know where they need to be deployed.

## File Paths for Configuration Changes

When I ask you to modify configuration, skills, or settings files, **always edit files in this repository**, never the deployed/active versions:

- **Global CLAUDE.md template:** Edit `/project/fish_tanks/CLAUDE.md` — NOT `/home/node/.claude/CLAUDE.md`
- **Agents:** Edit `/project/agents/` — NOT `/home/node/.claude/agents/`
- **Commands:** Edit `/project/commands/` — NOT `/home/node/.claude/commands/`
- **Skills:** Edit `/project/skills/` — NOT `/home/node/.claude/skills/`
- **Hooks:** Edit `/project/hooks/` — NOT `/home/node/.claude/hooks/`
- **Settings templates:** Edit `/project/fish_tanks/settings*.json` — NOT `/home/node/.claude/settings.json`
  - Note: there are two settings files. They need to be kept in sync with each other. Edits to `/project/fish_tanks/settings.json` need to be also made to `/project/fish_tanks/settings-glm.json` 
- **Fish Tanks (Docker Container)** Edit `/project/fish_tanks/aidev.Dockerfile`

This repository contains the source-of-truth configuration files. I deploy them separately using the deploy script.

## External Skills

The `/plan:build` command references `frontend-design`, which is an Anthropic-maintained external skill, not part of this repository. Do not look for it locally or flag it as missing.

## Instruction System Review

When asked to "review instructions", "audit the system", or "check for redundancy":

1. Read all files: both CLAUDE.md files, all skills (`/project/skills/`), agents (`/project/agents/`), commands (`/project/commands/`), hooks (`/project/hooks/`), and settings (`/project/fish_tanks/settings*.json`)
2. Check for: redundancies across files, contradictions, dangling references, gaps, token waste
3. Report organized as: **Redundancies** (with line citations and frequency count), **Contradictions**, **Gaps**, **Token Efficiency** (estimated line savings)
4. Propose specific edits — do not apply without approval

Key principle: hooks and settings deny lists are the mechanical enforcement layer. CLAUDE.md and skills should provide *behavioral guidance* (what to do instead) without re-listing what's already enforced. Skills loaded independently may repeat critical rules that also appear in CLAUDE.md — flag these but note whether the repetition serves a purpose (independent load context) or is pure waste.

## Workflow Research and Reoptimization

`/project/research_agenda.md` is a standing research agenda for this workflow system. Use it when asked to research, review, or improve the workflow.

### When to use it

- When the user asks to review or improve the workflow
- When the user mentions something feeling slow, inconsistent, or broken in a build
- When the user asks about agentic coding practices or "what are teams doing with X"
- Periodically on user request ("let's do a research pass")

### How to run a research pass

1. **Read `research_agenda.md`** — identify topics whose "Last checked" date is overdue for their cadence (quarterly = 3 months, semi-annual = 6 months), or any topic the user has flagged.
2. **Research each topic** using the "Questions to ask when re-researching" provided. Use WebSearch. These questions are intentionally directed — use them rather than broad searches.
3. **For each topic**: compare findings against the "Current baseline." If something meaningful has changed:
   - Determine whether it warrants a change to skills, commands, or agents in this repo
   - If yes: implement the change, then add a dated entry to "Incorporated Findings"
   - If no: update the "Current baseline" text and "Last checked" date to reflect the new state of the art
4. **Update the Watching section** — move items to Active Topics if they've matured, or to Decided Against if they've been evaluated and rejected.
5. **Add new topics** the user surfaces during the session to Active Topics before closing.

### What a finding needs before it becomes a change

- A clear "what would trigger a change" condition from the topic entry must be met, OR the user explicitly directs a change
- The change must map to a specific file in this repo (skill, command, agent)
- A Decided Against entry exists for things evaluated and rejected — check it before re-investigating familiar ground