# Contents

This project is a repository of working files that build my AI-assisted development workflow. 
Do not suggest changes to the locations of files in this repository. These are the working files. I know where they need to be deployed.

## File Paths for Configuration Changes

When I ask you to modify configuration, skills, or settings files, **always edit files in this repository**, never the deployed/active versions:

- **Global CLAUDE.md template:** Edit `/project/fish_tanks/CLAUDE.md` — NOT `/home/node/.claude/CLAUDE.md`
- **Agents:** Edit `/project/agents/` — NOT `/home/node/.claude/agents/`
- **Commands:** Edit `/project/commands/` — NOT `/home/node/.claude/commands/`
- **Skills:** Edit `/project/skills/` — NOT `/home/node/.claude/skills/`
- **Hooks:** Edit `/project/hooks/` — NOT `/home/node/.claude/hooks/`
- **Settings templates:** Edit `/project/fish_tanks/settings*.json` — NOT `/home/node/.claude/settings.json`
- **Fish Tanks (Docker Container)** Edit `/project/fish_tanks/aidev.Dockerfile`

This repository contains the source-of-truth configuration files. I deploy them separately using the deploy script.