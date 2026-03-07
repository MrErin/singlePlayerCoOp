# singlePlayerCoOp

Personal repository of AI prompts, skills, commands, agents, etc. for a solo developer.
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

# Workflow

- The main process follows a plan -> build -> audit cycle. 
- There are hard stop-gates between each step so you can review what's been planned/built/audited.

| Step                                                            | Command                                                         | What it does                                                                                                                      | Notes                                                                                            | Model                                                         |
| --------------------------------------------------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| 1.                                                              | `/plan:interrogate`                                             | Talks to you about your idea and builds a structured requirements doc                                                             | Can also be invoked after requirements exist in order to discuss new features or clarify things. | Depends on the complexity of the idea                         |
| 2.                                                              | `/plan:init`                                                    | Initializes a new project in the system, creating foundational docs and breaking the work into phases                             | Works for greenfield or brownfield apps. Loads the `iterative-build` skill for phase breakdown   | Sonnet                                                        |
| 3.                                                              | `/plan:phase [X]`                                               | References `iterative-build` and `my-style`, as well as foundational docs to formulate a detailed plan for the given phase        |                                                                                                  | Opus                                                          |
| 4.                                                              | `/plan:build [X]`                                               | Builds according to the skills and the plan                                                                                       |                                                                                                  | GLM                                                           |
| 5.                                                              | `/plan:review [X]`                                              | Verifies that the built code achieves the plan's goals                                                                            | Spawns a `code-reviewer` agent and creates some more documentation                               | Sonnet                                                        |
| 6.                                                              | Continue 3-5 through all phases with the noted exceptions below |                                                                                                                                   |                                                                                                  |                                                               |
| TEST phases                                                     |                                                                 | The roadmap will usually batch a few phases together to build test suites via a `test-writer` agent                               |                                                                                                  | Planning: Opus (maybe Sonnet, mixed results)<br>Building: GLM |
| After any TEST phase                                            | `/plan:test-audit`                                              | Assesses the test suite and creates a mini-gamified doc to address issues discovered                                              | Need to run mutation packages and establish code coverage for best results. Can be rerun.        | Opus                                                          |
| After full buildout (or after a TEST phase is a good place too) | `/plan:debt`                                                    | Assesses entire codebase against `my-style` standards and lists issues to address in order of severity, along with time estimates |                                                                                                  | Opus                                                          |
| At the very bitter end                                          | `post-build-review`                                             | Skill that creates a high-level document that goes over the major features of the app and major logic flows                       |                                                                                                  | Sonnet                                                        |

# System Conventions

I don't let AI make git commits. I like to review all changes.

The phase boundaries are strict. The AI stops at the end of each phase/command so that I can review changes and adjust course if necessary.

Clear the context window between steps if there isn't a model change.

For test phases especially, clear the damn context AND change the model. Maybe reboot the computer. Switch offices with someone. Gotta make sure the model writing the tests isn't the same one that wrote the code.

This system generates a *ton* of documentation, both Markdown files and in code comments. This helps both the hoomans and the AIs maintain context while they're looking at older work. But put it in the .gitignore if you don't like it cluttering the repo.

# The Code Buddy

`code-buddy` is a fun coworking partner that sits in the terminal to answer questions, rubber duck, and occasionally wax philosophical or tell me dumb jokes. 

It is never supposed to write code or modify files directly, other than `scratch.md` or the Code Buddy Plan if I've asked it for something complicated. The point of code-buddy is to let me write the code and think through problems, with the support of a superpowered reference doc that can see my exact use cases.

# Other Stuff

- I open the `_planning` directory inside [Obsidian](https://obsidian.md/). It makes it much easier and engaging to work with Markdown files than editing in the IDE. 
	- This is why the directory has a leading underscore rather than a period: Obsidian won't open `.planning` as a vault.
- My system owes a lot to https://github.com/gsd-build/get-shit-done. That system was way too automated for me - I need to check in with the code frequently or I'll lose the thread. But if that constraint doesn't bother you, go check it out! 
- I have raging ADHD and am very silly.
- I hope this README finds you well.
