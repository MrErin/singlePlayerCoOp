# singlePlayerCoOp

Personal repository of AI prompts, skills, commands, agents, etc. for a solo developer.

Used with Claude Code and GLM/Claude keys.

# The Problem

I've been a software developer and data analyst on the self-taught-to-bootcamp-to-professional spectrum for my entire adult life. I love the speed of AI-driven development. I don't have to stop and think about the syntax of something; I can just have a conversation about my idea and it generates requirements. And then it can generate code from the requirements. It's awesome.

But.

I mean. We all know the problems. Weak tests. Shitty architecture. Infinite loops. Dead code in brand new files. Plus, it generates *so much* at once it's impossible to review everything. The overwhelm is real. As much as I love the speed and being able to go from "cool idea" to something working in the space of a day, you can't just leave it all to the bots. 

And you wouldn't really want to. Most of the reason we do this is because playing with code is fun.

So this system keeps the fun bits. The "what if it did this..." bits. The "I want to dig into a puzzle" bits. My goal here is to get something that's walking at least as well as a baby giraffe. And then I can give it wings. 

By which I mean, review the code and docs written in each phase and do a bunch of manual checking and testing and iterating on requirements and fixing some structural stuff. The system prioritizes building in smallish reviewable chunks and offering checklists and time boxes whenever possible. This scaffolding was designed to help my brain work best, but it has the side benefit of not letting the AI go too wild down a bad road. So it's mutually beneficial.

Baby giraffes with wings would be cool though.

# Installation

Follow the Anthropic docs here: 
- Skill installation
	- https://code.claude.com/docs/en/skills
- Command installation:
	- Technically commands are now skills. I still use them as commands because I invoke them directly in my process rather than letting Claude determine when they are needed.
	- As of this writing, you drop the "commands" directory in `.claude` and they'll work.
- Agents installation:
	- https://code.claude.com/docs/en/sub-agents
- Hooks installation:
	- https://code.claude.com/docs/en/hooks

# Workflow

- The main process follows a plan -> build -> audit cycle. 
- There are hard stop-gates between each step so you can review what's been planned/built/audited.

| Step                                                          | Command                                                         | What it does                                                                                                                                                    | Notes                                                                                                                       | Model                                                         |
| ------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| 1. New project                                                | `/plan:MVP`                                                     | Full requirements interview for a greenfield project                                                                                                            | Produces `requirements.md`. Run before `/plan:init`.                                                                        | Opus                                                          |
| 1. Next feature                                               | `/plan:feature`                                                 | Scoped requirements interview for the next feature on an existing project                                                                                       | Only runs after `/plan:archive` has cleared the workspace. Stops if `requirements.md` already exists.                       | Sonnet or GLM                                                 |
| Mid-build                                                     | `/plan:shift`                                                   | Handles requirements gaps or phase insertions when something unexpected comes up                                                                                | Can update `requirements.md` only, insert new phases into the roadmap, or both — figures out which during the conversation. | Sonnet                                                        |
| 2.                                                            | `/plan:init`                                                    | Initializes a new project in the system, creating foundational docs and breaking the work into phases                                                           | Works for greenfield or brownfield apps. Loads the `iterative-build` skill for phase breakdown                              | Sonnet                                                        |
| 3.                                                            | `/plan:phase [X]`                                               | References `iterative-build` and `my-style`, as well as foundational docs to formulate a detailed plan for the given phase                                      |                                                                                                                             | Opus                                                          |
| 4.                                                            | `/plan:build [X]`                                               | Builds according to the skills and the plan                                                                                                                     | Uses `code-fixer` agent per-task to catch style violations before they accumulate                                           | GLM                                                           |
| 5.                                                            | `/plan:review [X]`                                              | Verifies that the built code achieves the plan's goals                                                                                                          | Spawns a `code-reviewer` agent to review the entire phase and creates some more documentation                               | Sonnet                                                        |
| 6.                                                            | Continue 3-5 through all phases with the noted exceptions below |                                                                                                                                                                 |                                                                                                                             |                                                               |
| TEST phases                                                   |                                                                 | The roadmap will usually batch a few phases together to build test suites via a `test-writer` agent                                                             |                                                                                                                             | Planning: Opus (maybe Sonnet, mixed results)<br>Building: GLM |
| At predetermined audit checkpoints and/or after full buildout | `/plan:audit`                                                   | Full codebase sweep — debt analysis, test analysis, and documentation drift check. Produces a gamified human review deck and an agent-executable auto-fix list. |                                                                                                                             | Opus                                                          |
| At the very bitter end                                        | `post-build-review`                                             | Skill that creates a high-level document that goes over the major features of the app/feature and major logic flows                                             |                                                                                                                             | Sonnet                                                        |
| At the even bitter-er end                                     | `/plan:archive`                                                 | Archives all feature-specific `_planning` documents, extracts permanent requirements, and clears the workspace for the next feature                             |                                                                                                                             | Sonnet                                                        |

### Backlog Management

The backlog system lives in `_planning/backlog/`. It lets me dump random ideas, notes, bugs, etc. that I collect while using the app (or going for a walk or whatever) into an inbox as a disorganized mess. The agent can sort out the list into categories that allow us to pull specific ideas into features during `/plan:MVP` or `/plan:feature`.

| Command              | What it does                                                          | When to use                                              |
| -------------------- | --------------------------------------------------------------------- | -------------------------------------------------------- |
| `/backlog:init`      | Creates `_planning/backlog/` with catalog files and inbox             | Once per project, when adopting the backlog workflow     |
| `/backlog:triage`    | Processes inbox items, assigns stable IDs, appends to catalog files   | After dumping ideas into `_inbox.md`                     |
| `/backlog:status`    | Shows counts by type/status, lists open items, flags stale entries    | Quick check of what's queued without opening four files  |

Backlog items use permanent IDs (`B-001`, `F-012`, `Q-003`, `D-007`) that never change or get reused. Status flows: `open` → `planned` → `shipped` (or `wont-fix`).

# Skills

Skills define core behaviors loaded during sessions. These are the four main skills:

| Skill              | Purpose                                                                                              | Key Behavior                                                                                |
| ------------------ | ---------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `iterative-build`  | Build applications in digestible phases with persistent planning state                               | Stop after each phase for review; maintains `_planning/` directory as source of truth      |
| `my-style`         | Coding standards and preferences for all projects                                                    | Clean readable code, accessibility-first web, testable design, no linter bypasses          |
| `code-buddy`       | Collaborative coding and teaching partner                                                            | User writes code; AI guides, explains, and reviews. Never edits project code directly      |
| `post-build-review`| Generate comprehensive review documentation after completing a build                                  | Creates ADHD-friendly guides with checkboxes, time estimates, and progressive disclosure   |

# Agents

Sub-agents handle delegated tasks during builds. Each has specific scope and model assignments:

| Agent            | Model  | Purpose                                                                                  | Key Constraint                                                       |
| ---------------- | ------ | ---------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `code-reviewer`  | Sonnet | Review code quality against project standards                                            | Read-only; reports issues but doesn't fix them                       |
| `test-writer`    | Sonnet | Write tests from interface contracts, not implementation                                 | Must run in new session for context separation from code writers     |
| `code-fixer`     | Sonnet | Fix style violations in code just written during a build task                            | Only touches style, never logic or public interfaces; two-round max  |

# Hooks

Hooks enforce safety and formatting at the tool boundary. These run automatically:

| Hook                | Purpose                                                                                 |
| ------------------- | --------------------------------------------------------------------------------------- |
| `block-dangerous`   | Blocks destructive commands (chmod, chown, kill, sudo, etc.) at kernel/policy level     |
| `block-secrets`     | Prevents reading secret files (.env, *.pem, *.key, credentials.*, etc.)                 |
| `block-git`         | Prevents git writes (commits, pushes, rebases) — user handles version control           |
| `block-workarounds` | Blocks environment workarounds in production code (sys.modules manipulation, etc.)      |
| `format-on-save`    | Auto-formats files after writes using project linters                                   |
| `allow-readonly`    | Permits read-only git operations (status, diff, log)                                    |

# System Conventions

I don't let AI make git commits. I like to review all changes.

The phase boundaries are strict. The AI stops at the end of each phase/command so that I can review changes and adjust course if necessary.

Clear the context window between steps if there isn't a model change.

For test phases especially, clear the damn context AND change the model. Maybe reboot the computer. Switch offices with someone. Gotta make sure the model writing the tests isn't the same one that wrote the code.

This system generates a *ton* of documentation, both Markdown files and in code comments. This helps both the hoomans and the AIs maintain context while they're looking at older work. But put it in the .gitignore if you don't like it cluttering the repo.

# Fish Tanks

I run all AI agents inside Docker containers on my machine, mounted to the individual projects they're working on. The configs are specific to my own setup and needs but I put it up here as a reference. That directory also contains my general settings files.

I've found in particular it's useful (and entertaining) to make Claude call its own environment the "fish tank" to differentiate communications about the AI environment from communications about the host machine or the project environments. Calling it the "Bat Cave" was also considered, but rejected because I didn't want the agents to get too broody.

# The Code Buddy

`code-buddy` is a fun coworking partner that sits in the terminal to answer questions, rubber duck, and occasionally wax philosophical or tell me dumb jokes. 

It is never supposed to write code or modify files directly, other than `scratch.md` or the Code Buddy Plan if I've asked it for something complicated. The point of code-buddy is to let me write the code and think through problems, with the support of a superpowered reference doc that can see my exact use cases.

# Other Stuff

- I open the `_planning` directory inside [Obsidian](https://obsidian.md/). It makes it much easier and engaging to work with Markdown files than editing in the IDE. 
	- This is why the directory has a leading underscore rather than a period: Obsidian won't open `.planning` as a vault.
- My system owes a lot to https://github.com/gsd-build/get-shit-done. That system was way too automated for me - I need to check in with the code frequently or I'll lose the thread. But if that constraint doesn't bother you, go check it out! 
- I have raging ADHD and am very silly.
- I hope this README finds you well.
