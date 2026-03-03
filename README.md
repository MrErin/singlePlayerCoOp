# singlePlayerCoOp

Repository of AI prompts, skills, commands, agents, etc. for a solo dev
# General Info

- I use Claude Code and GLM for coding stuff, so you may find references to both. 
- I have raging ADHD and am very silly.
- I hope this README finds you well.

# Installation

Follow the Anthropic docs here: 
- Skill installation
  - https://code.claude.com/docs/en/skills
- Command installation:
  - Technically commands are now skills. I still use them as commands because I invoke them directly in my process rather than letting Claude determine when they are needed.
  - As of this writing, you drop the "commands" directory in `.claude`
- Agents installation:
  - https://code.claude.com/docs/en/sub-agents

# Workflow

- The main process follows a plan -> build -> audit cycle. 
- There are hard stop-gates between each step so you can review what's been planned/built/audited.
- Clear the context window between steps.

| Step                                                                      | Command                                                         | What it does                                                                                                                      | Notes                                                                                                                   |
| ------------------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 1.                                                                        | `/plan:interrogate`                                             | Talks to you about your idea and builds a structured requirements doc                                                             | Can also be invoked after requirements exist in order to discuss new features or clarify things.                        |
| 2.                                                                        | `/plan:init`                                                    | Initializes a new project in the system, creating foundational docs and breaking the work into phases                             | Works for greenfield or brownfield apps. Loads the `iterative-build` skill for phase breakdown                          |
| 3.                                                                        | `/plan:phase [X]`                                               | References `iterative-build` and `my-style`, as well as foundational docs to formulate a detailed plan for the given phase        |                                                                                                                         |
| 4.                                                                        | `/plan:build [X]`                                               | Builds according to the skills and the plan                                                                                       |                                                                                                                         |
| 5.                                                                        | `/plan:review [X]`                                              | Verifies that the built code achieves the plan's goals                                                                            | Spawns a `code-reviewer` agent and creates some more documentation                                                      |
| 6.                                                                        | Continue 3-5 through all phases with the noted exceptions below |                                                                                                                                   |                                                                                                                         |
| After any TEST phase                                                      | `/plan:test-audit`                                              | Assesses the test suite and creates a mini-gamified doc to address issues early                                                   | Spawns a `test-writer` agent. Need to run mutation packages and establish code coverage for best results. Can be rerun. |
| After full buildout (or honestly, after a TEST phase is a good place too) | `/plan:debt`                                                    | Assesses entire codebase against `my-style` standards and lists issues to address in order of severity, along with time estimates |                                                                                                                         |
| At the very bitter end                                                    | `post-build-review`                                             | Skill that creates a high-level document that goes over the major features of the app and major logic flows                       |                                                                                                                         |

# The Code Buddy

`code-buddy` is a fun coworking partner that sits in the terminal to answer questions, rubber duck, and occasionally wax philosophical or tell me dumb jokes. 

It is never supposed to write code or modify files directly, other than `scratch.md` or the Code Buddy Plan if I've asked it for something complicated. The point of code-buddy is to let me write the code and think through problems directly, with the support of a superpowered reference doc that can see my exact use cases.

# Other Stuff

- I generally open the `_planning` directory inside Obsidian. It makes it much easier and engaging to work with Markdown files. This is why the directory has a leading underscore rather than a period: Obsidian won't open `.planning` as a vault.
- It's really nice to track changes to the files in git though. Can't believe I went *weeks* without thinking of doing that. It would have been so cool to see how much this system changed from its inception.
- My system owes a lot to https://github.com/gsd-build/get-shit-done. That system was way too automated for me - I need to check in with the code frequently or I'll lose the thread. But if that constraint doesn't bother you, go check it out!