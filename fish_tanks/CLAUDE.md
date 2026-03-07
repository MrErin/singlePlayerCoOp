# Skills

Always load and follow these skills when doing development work:

- **iterative-build**: Use for all multi-step development. Follow its phase gates and .planning/ directory structure. Invoked via /plan: commands.
- **my-style**: Follow for ALL code written in any language. Covers formatting, naming, accessibility, and ADHD-friendly patterns.
- **post-build-review**: Use after completing all phases to generate review docs.

When any /plan: command is invoked, load the iterative-build skill first.

Always use Context7 MCP for code generation, library usage, setup steps, and API documentation without me explicitly asking.

Always use jcodemunch MCP when exploring a codebase.

# Environment

You are running inside a Docker container. This determines what is and is not possible.

## Hard Limits

These will never work. Do not attempt them, do not try variations or workarounds:

- `sudo` — blocked by policy
- `chmod`, `chown`, `chgrp`, `setfacl` — blocked at the kernel level
- `apt-get`, `apt`, `dpkg` — require sudo
- `killall`, `pkill`, `kill -9` — blocked by policy
- `systemctl`, `shutdown`, `reboot` — blocked by policy

**When a command is denied or fails due to permissions: stop. Do not try alternative approaches to the same blocked operation. Explain what you need and ask the user to handle it outside the container.**

## What Works

- `pip3 install <package> --break-system-packages` — Python packages
- Standard dev tools already installed: pytest, coverage, mutmut, hypothesis, ruff
- Git is available for reading (status, diff, log) — commits are handled by the user
