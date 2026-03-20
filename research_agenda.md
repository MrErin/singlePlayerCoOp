# Research Agenda — Agentic Workflow Continual Improvement

This is a standing research agenda for the workflow system in this repository (skills, commands, agents). Agentic coding is fast-moving — approaches that are impractical today may be standard practice in a few months. This document keeps track of what to re-investigate, what we've already decided, and why, so research effort compounds instead of repeating.

**How to use this document**: Each quarter (or when something feels like it isn't working), work through the Active Topics list. For each topic, run a targeted search using the questions provided. If a finding warrants a change, implement it and log it in Incorporated Findings. If a finding confirms the current approach, update the "Last checked" date and note why. Add new topics as they surface.

---

## Review Cadences

- **Quarterly**: Fast-moving areas — model capabilities, multi-agent patterns, memory systems, benchmarks
- **Semi-annual**: Slower-moving areas — tooling conventions, spec-driven debate

---

## Active Research Topics

---

### 1. Agent Memory and Cross-Session Style Consistency

**Why it matters**: Within a build session, the code-fixer handles style drift. Across sessions, we rely on planning artifacts (lessons.md, decisions.md, codebase.md). Structured memory systems could make cross-session quality more consistent — agents that learn from previous phases rather than starting fresh each time.

**Current baseline** *(as of 2026-03-20)*:
- MemCoder (arXiv 2603.13258) converts git commit history into structured retrievable memory (functional keywords, root-cause analysis, verified solution summaries). Uses dual-stage retrieval — approximate nearest-neighbor then cross-encoder reranker.
- Letta Context Repositories: git-backed agent memory with version-controlled commits per memory update. Concurrent subagents work in isolated worktrees and merge learned context back via standard git conflict resolution.
- Both require external infrastructure not available in this setup. lessons.md is the current lightweight equivalent.

**Questions to ask when re-researching**:
- Are there practical, file-based structured memory approaches that work with Claude Code's session model without external services?
- Has the "tiered context" pattern (constitution + specialist files + cold retrieval) produced published results showing measurable quality improvement?
- Is there evidence that lessons.md-style accumulation actually changes agent output quality over time, or does it get ignored?

**What would trigger a change**: A file-based structured memory approach that works within the existing worktree/planning-artifacts model — no vector database, no external service required.

**Review cadence**: Quarterly
**Maps to**: iterative-build SKILL.md, lessons.md, potentially a new structured memory format

**Last checked**: 2026-03-20

---

### 2. Multi-Agent Orchestration Patterns

**Why it matters**: The current agent set (code-fixer per-task, code-reviewer at phase level, test-writer for test phases) was designed around today's model context and cost constraints. As parallelism gets cheaper and models improve, the optimal agent split may shift.

**Current baseline** *(as of 2026-03-20)*:
- Qodo 2.0: parallel specialist reviewers (security, logic, style, test quality) running concurrently, merged by a synthesizer. Achieves 60.1% F1 on real issues — best in class, but still misses 40%.
- SWE-Search (arXiv 2410.20285, ICLR 2025): Value Agent evaluates whether a solution strategy is worth pursuing before code is written. 23% relative improvement over baseline SWE-agent via Monte Carlo Tree Search.
- OpenHands `AgentDelegateAction`: formal primitive for any agent to spawn a subtask agent with clean context, receive condensed summary, continue.

**Questions to ask when re-researching**:
- Have parallel specialist reviewer F1 scores improved past 80%? What architecture enabled it?
- Is trajectory evaluation (Value Agent / MCTS pattern) being used in production workflows at non-research scale? What does the latency/cost look like?
- Are there new agent role patterns that aren't code-writer / code-reviewer / test-writer — roles that address a different part of the quality problem?

**What would trigger a change**: Parallel specialist reviewers exceeding ~80% F1 at reasonable cost, OR evidence that trajectory evaluation produces measurable quality improvement in a human-gated workflow (not just benchmark settings).

**Review cadence**: Quarterly
**Maps to**: code-reviewer agent, code-fixer agent, plan:build, plan:review

**Last checked**: 2026-03-20

---

### 3. Linter-as-Executable-Specification

**Why it matters**: Factory.ai's framing — lint rules as executable specifications, not style preferences — suggests that more of my-style's reasoning could be encoded deterministically rather than relying on LLM judgment. Deterministic catches are cheaper, faster, and more consistent than LLM-based ones.

**Current baseline** *(as of 2026-03-20)*:
- Factory.ai (factory.ai/news/using-linters-to-direct-agents): categorizes lint rules into seven types for agent navigability: grep-ability, glob-ability, architectural boundaries, security/privacy, testability, observability, documentation signals.
- CodeRabbit: AST Grep extracts deterministic structural facts (variable names, call graphs) which ground LLM review — reduces hallucination in review feedback.
- Ruff supports custom plugins but the ecosystem for AI-generated antipattern rules is thin as of early 2026.

**Questions to ask when re-researching**:
- Are teams publishing shared ruff/eslint rule sets for AI-generated antipatterns specifically (mutable defaults, bare except, mirror tests, etc.)?
- Has ruff's plugin ecosystem grown to the point where my-style/references/antipatterns.md could be expressed as actual lint rules?
- Is there tooling that helps convert prose guidelines into lint configuration?

**What would trigger a change**: A practical ruff plugin or published rule set that encodes the antipatterns in my-style/references/antipatterns.md, making them deterministically catchable. Would reduce code-fixer's LLM pass scope.

**Review cadence**: Semi-annual
**Maps to**: code-fixer agent, my-style/references/antipatterns.md

**Last checked**: 2026-03-20

---

### 4. Context Window Size vs. Context Relevance

**Why it matters**: The core quality problem this system addresses is context dilution over long builds. If larger context windows (200k+, 1M+) genuinely solve dilution, the architecture simplifies significantly. If it's a relevance problem rather than a size problem, the current approach of loading specialist files on demand is correct and should be strengthened.

**Current baseline** *(as of 2026-03-20)*:
- Agent READMEs study (arXiv 2511.12884): context files score 16.6 Flesch Reading Ease (comparable to legal documents) — effectively unreadable even in large windows. Suggests relevance, not size, is the binding constraint.
- Stripe's directory-scoped rules: rules attach automatically as agents traverse the filesystem. Works better than large single context dumps regardless of model window size.
- Codified Context paper (arXiv 2602.20478): 660-line always-loaded constitution + specialist files loaded per context outperforms one large file across 283 sessions.

**Questions to ask when re-researching**:
- Is there published evidence (not vendor claims) that 200k+ context windows reduce style-drift errors in multi-task builds?
- Have teams published comparisons of tiered-context vs. flat-context approaches on real codebases?
- Has directory-scoped context injection (Stripe's approach) become a native Claude Code or Cursor feature?

**What would trigger a change**: Evidence that large context windows eliminate dilution in practice would simplify the code-fixer's tiered loading approach. Evidence confirming it's a relevance problem would push toward adding directory-scoped my-style files per source module.

**Review cadence**: Quarterly
**Maps to**: code-fixer tiered loading, CLAUDE.md structure, my-style skill loading discipline

**Last checked**: 2026-03-20

---

### 5. Agentic Coding Benchmarks and Capability Signals

**Why it matters**: Benchmark scores are a rough proxy for underlying model and scaffold improvement. Significant score jumps usually signal an architectural change worth understanding, not just a better model. They're also useful for calibrating expectations — the 29.6% regression rate on "plausible" agent fixes (arXiv 2509.06216) is a useful grounding number to track over time.

**Current baseline** *(as of 2026-03-20)*:
- SWE-bench Verified: Live-SWE-agent at 77.4% (open scaffolds). SWE-bench Pro (harder subset): 45.8%.
- SWE-bench-CL (arXiv 2507.00014): new continual learning benchmark — measures cross-task knowledge accumulation. Directly relevant to whether lessons.md-style accumulation works.
- Production: Devin's merged PR rate at 67% (up from 34% in 2024). 29.6% of plausible agent fixes introduce behavioral regressions on rigorous retesting.
- Review delay: 68%+ of agent PRs face review delays, suggesting output quality is a human-trust bottleneck as much as a technical one.

**Questions to ask when re-researching**:
- Have SWE-bench Verified scores crossed 85%+ for open scaffolds? What scaffold change enabled it?
- Has SWE-bench-CL produced results comparing memory approaches for cross-task consistency?
- Are new benchmarks emerging that measure code style quality or style consistency (not just task completion)?
- Is the merged PR rate for production agentic systems still improving, and what's driving it?

**What would trigger a change**: A benchmark specifically measuring style consistency across multi-task sessions would directly validate or challenge this system's quality approach. A significant SWE-bench jump alongside a novel scaffold pattern is worth investigating for applicable techniques.

**Review cadence**: Quarterly
**Maps to**: Calibration baseline; architectural decisions about agent complexity

**Last checked**: 2026-03-20

---

### 6. Spec-Driven Development with Human Gates

**Why it matters**: Fowler's critique of Kiro/spec-kit/Tessl is about fully autonomous spec-to-code generation — agents ignore specs, specs drift from code, false confidence accumulates. This system avoids those failure modes via continuous planning artifact updates and human phase gates. But the tools in this space are evolving, and if spec-driven approaches add meaningful human checkpoints, there may be useful techniques to borrow.

**Current baseline** *(as of 2026-03-20)*:
- Fowler (martinfowler.com, 2025): agents frequently ignore specs in autonomous tools. Parallel to Model-Driven Development's failure — model drifts from code, maintaining both becomes more expensive than just maintaining the code.
- This system's distinction: plans serve the human (approved at each phase, adaptive, updated continuously). Spec-driven tools' plans serve the agent (autonomous generation target, static, allowed to drift).
- The key prevention mechanism: state.md, decisions.md, lessons.md surface agent decisions into planning artifacts rather than leaving them undocumented.

**Questions to ask when re-researching**:
- Have Kiro, spec-kit, or similar tools added human gate patterns that bring them closer to this system's model?
- Has Fowler or others updated their assessment based on newer tools or evidence?
- Is there published work on hybrid approaches (spec-driven + human-gated) with measured results?

**What would trigger a change**: Evidence that spec-driven tools with robust human gates show measurable improvement over the current planning-artifact approach — particularly around requirements traceability.

**Review cadence**: Semi-annual
**Maps to**: plan:interrogate, plan:phase, requirements.md management

**Last checked**: 2026-03-20

---

## Watching
*(Ideas not ready to incorporate — monitor for maturity)*

### Online Session-Local Tool Synthesis
**What it is**: Agents synthesizing custom analysis tools (parsers, static analyzers) during a session for the specific problem structure. Live-SWE-agent (arXiv 2511.13646) achieved 77.4% SWE-bench Verified this way.
**Why not yet**: Tools don't persist across sessions, so style consistency gains don't carry forward. Requires careful sandboxing.
**Watch for**: Session-local tool synthesis that is safe and containable within Claude Code's environment, with a mechanism for promoting useful tools to the permanent toolkit.

### Trajectory Evaluation / Value Agent
**What it is**: A Value Agent that scores candidate solution strategies before code is written, with backtracking support (SWE-Search, arXiv 2410.20285). 23% relative improvement over baseline SWE-agent.
**Why not yet**: Adds significant latency and cost. Requires MCTS infrastructure. Overkill for this workflow's scale.
**Watch for**: A simplified version of pre-write strategy evaluation that fits within a /plan:phase context without full MCTS overhead.

### Git-Backed Concurrent Agent Memory
**What it is**: Version-controlled agent memory where subagents work in isolated git worktrees and merge learned context back via git conflict resolution (Letta Context Repositories).
**Why not yet**: Requires external infrastructure or the Letta platform. Not adoptable as a file-based change.
**Watch for**: A file-based implementation pattern that works with Claude Code's existing worktree model.

---

## Incorporated Findings
*(Newest first — add new entries at top when findings are acted on)*

### 2026-03-20 — Tiered my-style Reference Loading in code-fixer
**Research**: Codified Context paper (arXiv 2602.20478), Agent READMEs study (arXiv 2511.12884).
**Decision**: code-fixer loads only the specific my-style reference file(s) matching file types being fixed (python.md / typescript.md / testing.md / web.md / sql.md), not the full skill.
**Rationale**: Loading the full skill recreates the dilution problem being solved. Specialist files loaded on demand keep style guidance prominent in a short, focused context.

### 2026-03-20 — Two-Round Maximum on code-fixer
**Research**: Stripe Minions (stripe.dev) — empirically observed diminishing returns from LLM iteration cycles, hard two-round CI limit enforced architecturally.
**Decision**: code-fixer stops after two rounds regardless of remaining violations. Unfixed items are reported for user review, not silently retried.
**Rationale**: Unlimited retry loops mask tasks that require human judgment. The two-round limit surfaces those rather than hiding them under endless LLM iteration.

### 2026-03-20 — Linter-First Pass in code-fixer
**Research**: Factory.ai (linter-as-executable-specification), Cursor agent best practices ("lint feedback is extremely high signal"), CodeRabbit AST Grep + LLM hybrid.
**Decision**: code-fixer runs the project linter with autofix (ruff/eslint) before the LLM style pass. Deterministic violations are resolved cheaply before spending tokens on LLM reasoning.
**Rationale**: Linters catch a class of violations that LLMs miss or hallucinate about. Running linter first gives the LLM pass grounded, already-partially-cleaned code to work on.

### 2026-03-20 — code-fixer Agent (replaces code-reviewer in plan:build per-task loop)
**Research**: Full session — see notes on context dilution, multi-agent patterns, Stripe two-round limit.
**Decision**: Created code-fixer agent. Operates on finished, connected code after each task in plan:build. Finds and fixes style violations in-place. Replaces the pattern of code-reviewer reporting + diluted main agent applying fixes.
**Rationale**: The failure point was the fix application step, not the initial code writing. A dedicated fixer with fresh context and a tight scope (style only, never public interfaces) addresses that step without introducing the disconnection risk of a codewriter agent.

---

## Decided Against
*(Add entries when an idea is explicitly evaluated and rejected — prevents re-investigating the same ground)*

### Codewriter Agent
**Evaluated**: 2026-03-20. A dedicated agent that writes code fresh with style as primary concern, invoked per-task instead of having the main agent write.
**Rejected because**: Most phase tasks are interdependent in ways that don't appear in signatures — a service written in task 4 needs to match patterns from task 2, a function calls a utility written two tasks earlier. Gating to "truly isolatable tasks" would exclude the majority of tasks in a typical phase. Disconnection risk was judged higher than quality benefit.
**Revisit if**: A reliable method emerges for packaging cross-task dependency context compactly — one that doesn't recreate the context dilution problem in the packaging step.

### Parallel Specialist Reviewers (Qodo 2.0 pattern)
**Evaluated**: 2026-03-20. Running parallel domain-specific review agents (security, style, logic) simultaneously after each task.
**Rejected because**: F1 of 60.1% means 40% of real issues are still missed. Cost and latency overhead not justified at current quality gain. The code-fixer + code-reviewer two-gate model achieves the key benefits more cheaply.
**Revisit if**: F1 scores exceed ~80%, or the cost of parallel agents drops significantly. See Active Topics item 2.
