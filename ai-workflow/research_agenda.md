# Research Agenda — Agentic Workflow Continual Improvement

This is a standing research agenda for the workflow system in this repository (skills, commands, agents). Agentic coding is fast-moving — approaches that are impractical today may be standard practice in a few months. This document keeps track of what to re-investigate, what we've already decided, and why, so research effort compounds instead of repeating.

**How to use this document**: Each quarter (or when something feels like it isn't working), work through the Active Topics list. For each topic, run a targeted search using the questions provided. If a finding warrants a change, implement it and log it in Incorporated Findings. If a finding confirms the current approach, update the "Last checked" date and note why. Add new topics as they surface.

---

## Review Cadences

- **Quarterly**: Fast-moving areas — model capabilities, multi-agent patterns, memory systems, benchmarks
- **Semi-annual**: Slower-moving areas — tooling conventions, spec-driven debate

---

## Active Research Topics

> **"Harness Engineering"** — the practice of engineering the system around an AI agent (CLAUDE.md, hooks, skills, agents, phase gates) rather than just prompting — is now a recognized discipline. Multiple 2026 sources use this term (AWS re:Invent 2025, builder.aws, Addy Osmani). This agenda is a harness engineering effort. The term is useful for future research framing.

---

### 0. MCP Server Ecosystem for Development Workflow

**Why it matters**: MCP servers extend Claude Code's capabilities with specialized tools for code analysis, documentation retrieval, testing, and more. The ecosystem is rapidly expanding — new servers appear weekly. Periodic re-evaluation ensures we're using the best tools available and not missing capabilities that would meaningfully improve the workflow.

**Current baseline** *(as of 2026-07-14)*:
- **In use**: Context7 (documentation lookup — still dominant, no challenger with broader coverage), web_reader (URL to markdown), 4_5v_mcp (image analysis)
- **Reference servers available**: Memory (knowledge graph), Sequential Thinking, Filesystem, Git, Fetch, Time
- **Ecosystem size**: 500+ official + 200+ community servers (steady growth, no new dominant category)
- **Key categories**: Database connectors, code analysis, browser automation, documentation, memory/RAG, API integrations
- GitHub MCP integration for full PR lifecycle (read issues, implement, test, submit) now common across Claude Code, Cursor, and Windsurf
- Browser automation (Playwright MCP) more stable but still not CI-gate-reliable
- No AST-based code navigation server without pre-indexing; no file-based memory MCP integrating with git worktrees

**Questions to ask when re-researching**:
- Are there new servers specifically designed for agentic coding workflows (not just API wrappers)?
- Has the Memory server matured enough to replace or supplement lessons.md-style accumulation?
- Are there AST-based code analysis servers that work without external indexing infrastructure?
- Have browser automation servers (Playwright, Puppeteer) become reliable enough for CI-gated test verification?
- Are there servers that provide structured diff/patch operations for code transformation?
- Has anyone built a server that implements the "linter-as-executable-specification" pattern?

**What would trigger a change**:
- A memory server that works file-based without external infrastructure (Neo4j, Qdrant, etc.)
- An AST-based code navigation server that doesn't require pre-indexing
- A browser testing server stable enough for phase verification
- A documentation server with better coverage than Context7

**Review cadence**: Quarterly
**Maps to**: All skills and agents; potentially replaces manual context management

**Last checked**: 2026-07-14

---

### 1. Agent Memory and Cross-Session Style Consistency

**Why it matters**: Within a build session, the code-fixer handles style drift. Across sessions, we rely on planning artifacts (lessons.md, decisions.md, codebase.md). Structured memory systems could make cross-session quality more consistent — agents that learn from previous phases rather than starting fresh each time.

**Current baseline** *(as of 2026-07-14)*:
- Claude Code's **auto-memory** is now a first-class, documented system. Per-project `MEMORY.md` in `.claude/projects/` loads into every session. This system already has it in place.
- Top 8 memory frameworks in 2026: Hindsight, mem0, Zep, Letta, Cognee, MemSync, plus AWS and Azure managed offerings — **all require external infrastructure** (vector DBs, graph DBs, or managed services).
- File-based memory with CLAUDE.md + auto-memory + lessons.md remains the practical state of the art for Claude Code workflows without external dependencies.
- Oracle published a comparison (filesystem vs database for agent memory) confirming filesystems excel for single-user prototypes and small teams — exactly this use case.
- No published evidence that lessons.md-style accumulation measurably changes agent output quality over time. Benefit appears to be human-facing (audit trail, onboarding) rather than agent-facing.

**Questions to ask when re-researching**:
- Are there practical, file-based structured memory approaches that work with Claude Code's session model without external services?
- Has the "tiered context" pattern (constitution + specialist files + cold retrieval) produced published results showing measurable quality improvement?
- Is there evidence that lessons.md-style accumulation actually changes agent output quality over time, or does it get ignored?

**What would trigger a change**: A file-based structured memory approach that works within the existing worktree/planning-artifacts model — no vector database, no external service required.

**Review cadence**: Quarterly
**Maps to**: iterative-build SKILL.md, lessons.md, auto-memory MEMORY.md, potentially a new structured memory format

**Last checked**: 2026-07-14

> **Potential action**: Consider whether high-value `lessons.md` entries should be selectively promoted to auto-memory MEMORY.md for stronger cross-session persistence. Auto-memory loads into every session; lessons.md only loads when iterative-build is active. Caveat: MEMORY.md has a 200-line truncation limit — only truly stable, cross-project patterns should be promoted. Requires careful curation, not automation.

---

### 2. Multi-Agent Orchestration Patterns

**Why it matters**: The current agent set (code-fixer per-task, code-reviewer at phase level, test-writer for test phases) was designed around today's model context and cost constraints. As parallelism gets cheaper and models improve, the optimal agent split may shift.

**Current baseline** *(as of 2026-07-14)*:
- Claude Code's subagent system is mature and well-documented. Worktree isolation (`isolation: "worktree"`) is a first-class feature — each subagent gets its own git worktree, preventing conflicts.
- Qodo 2.0: parallel specialist reviewers (security, logic, style, test quality) running concurrently, merged by a synthesizer. Achieves 60.1% F1 on real issues — best in class, but still misses 40%. No F1 improvement past 80% threshold yet.
- "Harness Engineering" is emerging as a named discipline for exactly what this system does — the harness (CLAUDE.md, hooks, skills, agents) that shapes agent behavior.
- Running 10+ parallel Claude agents on the same codebase is now documented and practical. Orchestration patterns: sequential delegation, parallel specialist, fan-out/fan-in, hierarchical coordination.
- Agent Teams: emerging Claude Code feature for coordinated multi-agent work beyond simple subagents. Worth monitoring (see Watching section).

**Questions to ask when re-researching**:
- Have parallel specialist reviewer F1 scores improved past 80%? What architecture enabled it?
- Is trajectory evaluation (Value Agent / MCTS pattern) being used in production workflows at non-research scale? What does the latency/cost look like?
- Are there new agent role patterns that aren't code-writer / code-reviewer / test-writer — roles that address a different part of the quality problem?

**What would trigger a change**: Parallel specialist reviewers exceeding ~80% F1 at reasonable cost, OR evidence that trajectory evaluation produces measurable quality improvement in a human-gated workflow (not just benchmark settings).

**Review cadence**: Quarterly
**Maps to**: code-reviewer agent, code-fixer agent, plan:build, plan:review

**Last checked**: 2026-07-14

---

### 3. Linter-as-Executable-Specification

**Why it matters**: Factory.ai's framing — lint rules as executable specifications, not style preferences — suggests that more of my-style's reasoning could be encoded deterministically rather than relying on LLM judgment. Deterministic catches are cheaper, faster, and more consistent than LLM-based ones.

**Current baseline** *(as of 2026-07-14)*:
- Ruff now has **900+ built-in rules** (up from ~800). GitHub discussion on custom plugin support (astral-sh/ruff#8409) remains open — no resolution.
- Factory.ai (factory.ai/news/using-linters-to-direct-agents): categorizes lint rules into seven types for agent navigability.
- CodeRabbit: AST Grep + LLM hybrid for grounded review feedback.
- Semgrep Assistant added AI-powered triage and remediation guidance. The `/project/semgrep-rules/` directory with 16 custom rules remains the best option for custom antipattern detection.
- No tooling converts prose guidelines into lint configuration. "AI-native Python stack" articles in 2026 consistently recommend uv + ruff + Claude Code but all use ruff's built-in rules only.

**Questions to ask when re-researching**:
- Are teams publishing shared ruff/eslint rule sets for AI-generated antipatterns specifically (mutable defaults, bare except, mirror tests, etc.)?
- Has ruff's plugin ecosystem grown to the point where my-style/references/antipatterns.md could be expressed as actual lint rules?
- Is there tooling that helps convert prose guidelines into lint configuration?

**What would trigger a change**: A practical ruff plugin or published rule set that encodes the antipatterns in my-style/references/antipatterns.md, making them deterministically catchable. Would reduce code-fixer's LLM pass scope.

**Review cadence**: Semi-annual
**Maps to**: code-fixer agent, my-style/references/antipatterns.md

**Last checked**: 2026-07-14

---

### 4. Context Window Size vs. Context Relevance

**Why it matters**: The core quality problem this system addresses is context dilution over long builds. If larger context windows (200k+, 1M+) genuinely solve dilution, the architecture simplifies significantly. If it's a relevance problem rather than a size problem, the current approach of loading specialist files on demand is correct and should be strengthened.

**Current baseline** *(as of 2026-07-14)*:
- **"Context Engineering" is now a named discipline.** Multiple 2026 articles and guides on curating agent context for quality.
- Research paper "The Maximum Effective Context Window": all tested models fall **far short of their maximum context window by as much as >99%**. Effective context shrinks dramatically as window fills.
- "State of Context Engineering in 2026" (Towards AI): "Every token in the context window competes for attention. As context grows, precision drops, reasoning weakens." Frames this as a relevance problem, not a size problem.
- Stanford research: model accuracy drops 30%+ when relevant information sits in the **middle** of long context ("lost in the middle" problem persists into 2026).
- Agent READMEs study (arXiv 2511.12884): context files score 16.6 Flesch Reading Ease — effectively unreadable even in large windows.
- Codified Context paper (arXiv 2602.20478): 660-line constitution + specialist files loaded per context outperforms one large file.
- Directory-scoped context injection has NOT become a native Claude Code feature — still requires manual implementation.

**Questions to ask when re-researching**:
- Is there published evidence (not vendor claims) that 200k+ context windows reduce style-drift errors in multi-task builds?
- Have teams published comparisons of tiered-context vs. flat-context approaches on real codebases?
- Has directory-scoped context injection (Stripe's approach) become a native Claude Code or Cursor feature?

**What would trigger a change**: Evidence that large context windows eliminate dilution in practice would simplify the code-fixer's tiered loading approach. Evidence confirming it's a relevance problem would push toward adding directory-scoped my-style files per source module.

**Review cadence**: Quarterly
**Maps to**: code-fixer tiered loading, CLAUDE.md structure, my-style skill loading discipline

**Last checked**: 2026-07-14

---

### 5. Agentic Coding Benchmarks and Capability Signals

**Why it matters**: Benchmark scores are a rough proxy for underlying model and scaffold improvement. Significant score jumps usually signal an architectural change worth understanding, not just a better model. They're also useful for calibrating expectations — the 29.6% regression rate on "plausible" agent fixes (arXiv 2509.06216) is a useful grounding number to track over time.

**Current baseline** *(as of 2026-07-14)*:

| Model | SWE-bench Verified | SWE-bench Pro | Notes |
|---|---|---|---|
| Fable 5 | 95.0% | 80.3% | New leader |
| Claude Mythos Preview | 93.9% | — | Anthropic preview |
| Claude Opus 4.8 | 88.6% | 69.2% | Released May 28, 2026 |
| GPT-5.5 | 88.7% | — | Near-tied with Opus 4.8 |
| Claude Opus 4.7 | 87.6% | 64.3% | Released April 16, 2026 |
| Claude Opus 4.6 | 80.8% | ~57.5% | **Current system model** |
| Claude Sonnet 4.6 | 79.6% | — | **Current execution model** |

- **AI-assisted PRs merge at less than half the rate of human code** (LinearB 2026 benchmarks) — worse than the previous 68% review delay baseline. Quality/trust remains the primary bottleneck.
- Human reviewers exchange **11.8% more rounds** when reviewing AI-generated code vs human-written (arXiv 2603.15911).
- Devin's merged PR rate: still at **67%** on defined tasks (unchanged). Pricing dropped to $20/month + $2.25/agent.
- SWE-bench Verified scores have crossed 85%+ for Opus 4.7/4.8. The scaffold change: improved tool use, better reasoning chains, harness-level improvements.
- Windsurf merged with/acquired Devin.

**Questions to ask when re-researching**:
- Have SWE-bench Verified scores crossed 85%+ for open scaffolds? What scaffold change enabled it?
- Has SWE-bench-CL produced results comparing memory approaches for cross-task consistency?
- Are new benchmarks emerging that measure code style quality or style consistency (not just task completion)?
- Is the merged PR rate for production agentic systems still improving, and what's driving it?

**What would trigger a change**: A benchmark specifically measuring style consistency across multi-task sessions would directly validate or challenge this system's quality approach. A significant SWE-bench jump alongside a novel scaffold pattern is worth investigating for applicable techniques.

**Review cadence**: Quarterly
**Maps to**: Calibration baseline; architectural decisions about agent complexity

**Last checked**: 2026-07-14

---

### 6. Model Selection and Benchmark Tracking for This Workflow

**Why it matters**: The right model choice per task is one of the highest-leverage cost and quality levers in this workflow. Model lineups and pricing change fast — Anthropic, Z.ai, and Google have all made significant changes in the last 6 months. The plan/execute split (Opus plans, Sonnet executes) is now explicitly supported in Claude Code, but GLM pricing pressure may shift what "default" means. An outdated selection guide means paying too much for mechanical tasks or getting worse results on planning tasks.

**Current baseline** *(as of 2026-07-14)*:
- Claude model lineup: Haiku 4.5 ($1/$5), Sonnet 4.6 ($3/$15), Opus 4.8 ($5/$25). All 200K context.
- **Opus 4.7** released April 16, 2026. **Opus 4.8** released May 28, 2026 (SWE-bench Verified: 88.6%, SWE-bench Pro: 69.2%). Same pricing as Opus 4.6.
- **Opus 4.8 fast mode pricing dropped 3x** — worth noting for cost-conscious sessions.
- Plan/execute split is even more justified — gap between Opus 4.8 and Sonnet 4.6 widened (88.6% vs 79.6%).
- Sonnet 4.6: users prefer over Sonnet 4.5 ~70% of the time; preferred over Opus 4.6 for many practical tasks; 128K output vs Opus 4.6's 64K output.
- GLM-5.1 (Z.ai): no new independent corroboration since last check. No GLM-5.2 or next-gen release found.
- GLM-4.7-Flash: free tier status unchanged. Still best free-tier model.
- Haiku 4.5's key constraint: IFBench still at **54.3%**. Claude models cluster between 54.3% and 58.6% on IFBench. Not suitable for code-fixer, test-writer, code-reviewer agents. No Haiku update released.
- Fable 5 at 95.0% SWE-bench Verified — new leader. GPT-5.5 at 88.7% — near-tied with Opus 4.8.
- Full model selection guide written at: `still-thinking/dev-workflow_model-selection-guide.md`

**Questions to ask when re-researching**:
- Has the Haiku-tier IFBench score improved enough to use in code-fixer/test-writer agents?
- Has GLM-5.1's SWE-bench performance been independently corroborated? What's the current external benchmark standing?
- Are new GLM models (5.2+, Z.ai next-gen) available that change the cost/quality math?
- Has Claude Code's plan mode (Opus plan + Sonnet execute) improved or changed in how it routes model selection?
- Have free tier caps changed for Gemini 2.5 Pro or GLM-4.7-Flash?
- Are any new frontier models from Anthropic, Z.ai, or Google meaningfully changing the value proposition for any specific workflow task?
- Has anyone published empirical comparisons of Opus vs. Sonnet specifically for requirements interview quality (not just code benchmarks)?

**What would trigger a change**:
- Haiku IFBench score crosses ~70%+ → reconsider for code-fixer and test-writer agents
- GLM-5.1 benchmarks independently corroborated → update confidence level for code generation recommendation
- A new Claude or GLM model that materially changes the pricing tier structure
- Any model that meaningfully outperforms Opus specifically on conversational requirements ambiguity-surfacing tasks
- Opus 4.8 fast mode quality benchmarks suggesting it's viable as the default for execution tasks (cost savings without quality regression)

**Review cadence**: Event-driven (triggered by Anthropic model announcements, major benchmark shifts, or pricing changes). Quarterly at minimum.
**Maps to**: `still-thinking/dev-workflow_model-selection-guide.md`; agent frontmatter model settings in `agents/`

**Last checked**: 2026-07-14

---

### 7. Spec-Driven Development with Human Gates

**Why it matters**: Fowler's critique of Kiro/spec-kit/Tessl is about fully autonomous spec-to-code generation — agents ignore specs, specs drift from code, false confidence accumulates. This system avoids those failure modes via continuous planning artifact updates and human phase gates. But the tools in this space are evolving, and if spec-driven approaches add meaningful human checkpoints, there may be useful techniques to borrow.

**Current baseline** *(as of 2026-07-14)*:
- Fowler (martinfowler.com, 2025): agents frequently ignore specs in autonomous tools. Parallel to Model-Driven Development's failure — model drifts from code, maintaining both becomes more expensive than just maintaining the code.
- This system's distinction: plans serve the human (approved at each phase, adaptive, updated continuously). Spec-driven tools' plans serve the agent (autonomous generation target, static, allowed to drift).
- The key prevention mechanism: state.md, decisions.md, lessons.md surface agent decisions into planning artifacts rather than leaving them undocumented.
- Kiro has matured — now enforces human-in-the-loop at **every** phase (requirement, design, implementation). Converges with this system's phase gate model.
- **"Harness Engineering"** is the emerging term for exactly what this system does — engineering the system around the AI agent (CLAUDE.md, hooks, skills, agents, phase gates) rather than just prompting. Used in AWS re:Invent 2025 talks and builder.aws articles.

**Questions to ask when re-researching**:
- Have Kiro, spec-kit, or similar tools added human gate patterns that bring them closer to this system's model?
- Has Fowler or others updated their assessment based on newer tools or evidence?
- Is there published work on hybrid approaches (spec-driven + human-gated) with measured results?

**What would trigger a change**: Evidence that spec-driven tools with robust human gates show measurable improvement over the current planning-artifact approach — particularly around requirements traceability.

**Review cadence**: Semi-annual
**Maps to**: plan:MVP, plan:feature, plan:shift, plan:phase, requirements.md management

**Last checked**: 2026-07-14

---

### 8. Cost Efficiency and Instruction Overhead

**Why it matters**: The research agenda tracks quality metrics only (SWE-bench, F1 scores). It has no trigger conditions for cost efficiency or instruction overhead. Models have improved significantly (Opus 4.8 at 88.6% vs 4.6 at 80.8%), and Claude Code now has effort levels (low through max). Some instructions may exist to correct failure modes that newer models no longer exhibit, and the system may be paying full-effort token costs for mechanical tasks.

**Current baseline** *(as of 2026-07-14)*:
- The deployed CLAUDE.md is ~147 lines. A typical `/plan:build` session loads: CLAUDE.md + iterative-build SKILL.md (~195 lines) + my-style SKILL.md (~116 lines) + reference files + planning files = ~500-800 lines of instructions before user code.
- Claude Code has 5 effort levels (low, medium, high, xhigh, max). Research shows "Low quietly killed Opus 4.6" — Opus at low effort outperforms older models at default. Max effort is often wasteful for mechanical tasks.
- No effort level guidance exists in any command, agent, or skill in this system.
- No instruction has been systematically tested for whether it's still needed with current models (Opus 4.8, Sonnet 4.6).
- Auto-memory MEMORY.md is currently empty — stable project patterns could accumulate here for cross-session persistence, reducing the need for always-loaded instructions.

**Questions to ask when re-researching**:
- Has the instruction load for a `/plan:build` session been measured? What fraction of context window does it consume?
- Can specific instructions be removed without quality regression on a controlled build test?
- Are effort levels producing measurable cost savings without quality loss?
- Are there instructions in CLAUDE.md that duplicate what hooks/settings already enforce mechanically?
- Should high-value lessons.md entries be selectively promoted to auto-memory for stronger cross-session persistence?

**What would trigger a change**: If the instruction load for a `/plan:build` session exceeds a reasonable token budget and a controlled test shows removing specific instructions produces no quality regression, simplify. If effort level optimization shows measurable cost savings without quality regression, add guidance to commands/agents.

**Review cadence**: Quarterly
**Maps to**: CLAUDE.md template, all skills, all commands, all agents, auto-memory

**Last checked**: 2026-07-14

---

### 9. AI Code Antipattern Discovery

**Why it matters**: AI-generated code introduces failure patterns that differ from human-written code — hallucinated packages, placeholder credentials, scope over-exposure, orthogonal damage. New patterns emerge as models change, adoption scales, and attackers adapt. If the antipatterns reference falls behind, the audit and code-fixer miss real issues.

**Current baseline** *(as of 2026-07-23)*:
- `my-style/references/antipatterns.md` covers: environment workarounds, error handling, state/mutability, over-engineering, AI-specific tells, testing antipatterns, mock protocol mismatch, enum exhaustiveness, database/API patterns, import antipatterns, linter bypasses, hallucinated APIs & package hallucination, resource management, hardcoded secrets (including AI placeholder patterns), copy-paste artifacts, dead code, scope/visibility over-exposure.
- Key external sources: Snyk (package hallucination), GitGuardian State of Secrets Sprawl (credential patterns), Trend Micro (slopsquatting), Karpathy's four structural failure patterns, arXiv empirical studies on agent-generated code maintainability.
- 45% of AI-generated code introduces OWASP Top 10 vulnerabilities (Veracode 2026, unchanged across testing cycles).
- AI-assisted commits show 3.2% secret-leak rate vs 1.5% baseline (GitGuardian 2026).
- 74 AI-linked CVEs through March 2026, ~6x monthly increase (Georgia Tech Vibe Security Radar).

**Questions to ask when re-researching**:
- Are there newly documented AI code failure patterns from security research (Snyk, GitGuardian, CSA, OWASP), empirical studies (arXiv), or post-incident analysis not yet in `antipatterns.md`?
- Have the OWASP Top 10 vulnerability rates in AI-generated code improved or worsened? Are new vulnerability categories emerging?
- Are there new supply-chain attack vectors specific to AI-generated code beyond slopsquatting?
- Has the credential leak rate in AI-assisted commits changed? Are there new placeholder patterns to detect?
- Are practitioners documenting new testing antipatterns specific to AI-generated tests?

**What would trigger a change**: A documented antipattern category not covered by the existing reference, or a significant shift in vulnerability rates that suggests existing checks are insufficient. Each finding maps to: a new section or entries in `antipatterns.md`, new grep patterns in `/plan:audit` Pass 1, or new checks in `/plan:review`.

**Review cadence**: Quarterly
**Maps to**: `my-style/references/antipatterns.md`, `/plan:audit` Pass 1, `/plan:review` structural verification

**Last checked**: 2026-07-23

---

## Watching
*(Ideas not ready to incorporate — monitor for maturity)*

### Online Session-Local Tool Synthesis
**What it is**: Agents synthesizing custom analysis tools (parsers, static analyzers) during a session for the specific problem structure. Live-SWE-agent (arXiv 2511.13646) achieved 77.4% SWE-bench Verified this way.
**Why not yet**: Tools don't persist across sessions, so style consistency gains don't carry forward. Requires careful sandboxing. Live-SWE-agent's 77.4% is now far from SOTA (Fable 5 at 95.0%, Opus 4.8 at 88.6%).
**Watch for**: Session-local tool synthesis that is safe and containable within Claude Code's environment, with a mechanism for promoting useful tools to the permanent toolkit.

### Trajectory Evaluation / Value Agent
**What it is**: A Value Agent that scores candidate solution strategies before code is written, with backtracking support (SWE-Search, arXiv 2410.20285). 23% relative improvement over baseline SWE-agent.
**Why not yet**: Adds significant latency and cost. Requires MCTS infrastructure. Overkill for this workflow's scale.
**Watch for**: A simplified version of pre-write strategy evaluation that fits within a /plan:phase context without full MCTS overhead.

### Git-Backed Concurrent Agent Memory
**What it is**: Version-controlled agent memory where subagents work in isolated git worktrees and merge learned context back via git conflict resolution (Letta Context Repositories).
**Why not yet**: Requires external infrastructure or the Letta platform. Not adoptable as a file-based change.
**Watch for**: A file-based implementation pattern that works with Claude Code's existing worktree model.

### Memory MCP Reference Server
**What it is**: Official MCP reference server providing knowledge graph-based persistent memory. Stores entities (people, concepts, files) and relations between them, retrieved via semantic search.
**Why not yet**: Designed to replace context files, not supplement them. Stores in SQLite or in-memory — no git-backed persistence. Would require maintaining two parallel systems (lessons.md + Memory graph) with no clear benefit over current lessons.md pattern.
**Watch for**: Git-backed persistence support (commits per memory update, mergeable via standard git) that would integrate with the existing worktree/planning-artifact model.

### Third-Party Component Security Scanning
**What it is**: Automated vetting of third-party code before adding to codebase — scanning for unexpected network calls, dynamic code execution, environment access, and obfuscation patterns.
**Why not yet**: Currently only practical for specific ecosystems (shadcn registries have `view` commands). Generalizable pattern needs more ecosystem support — npm/pip don't have standardized "view source before install" workflows.
**Watch for**: IDE-integrated supply chain security tools, `npm audit`-style vetting that checks behavioral patterns (not just CVEs), or registry-level malware scanning that makes per-package review unnecessary.

### De-Sloppify Pattern (Separate Cleanup Agent)
**What it is**: Instead of constraining the coding agent with negative instructions ("don't over-engineer", "don't add unnecessary tests"), let it build freely, then run a separate cleanup agent that removes unnecessary defensive code, over-engineered abstractions, redundant tests, and excessive error handling for impossible scenarios. From ECC's autonomous loops skill.
**Why not yet**: Works best for greenfield code. On brownfield projects with existing complexity, the cleanup agent might remove things that look unnecessary but serve a purpose. Current code-fixer agent operates on style only and explicitly cannot touch logic. Would need a new agent definition with careful scoping.
**Watch for**: A cleanup agent pattern that reliably distinguishes intentional complexity from over-engineering on brownfield code, OR a benchmark showing measurable reduction in code complexity without regression increase.

### Agent Teams in Claude Code
**What it is**: Coordinated multi-agent work beyond simple subagents. Agent Teams enable patterns like parallel feature development, concurrent audit passes, or long-running parallel work on the same codebase with shared state coordination.
**Why not yet**: Emerging feature — maturity and reliability unclear. Current subagent model handles most needs. Parallel development patterns need careful merge conflict management.
**Watch for**: Agent Teams stabilizing enough for parallel feature development on independent phases, or for concurrent audit/review passes that the current sequential approach can't handle.

### Continuous Learning / Instinct System
**What it is**: An observation-and-extraction pipeline where hooks capture tool use events, a background agent analyzes them for behavioral patterns, and extracted patterns become "instincts" — atomic behavioral units with one trigger, one action, a confidence score (0.3-0.9), and domain tag. Instincts scoped per-project and promoted to global at high confidence. From ECC v1.9.0.
**Why not yet**: Complex system (multiple hooks, background agents, confidence scoring, project scoping). Adds token overhead per turn. Quality of automatically extracted "instincts" is unproven. Current explicit memory approach is simpler and more predictable.
**Watch for**: Evidence that automatically extracted behavioral patterns improve agent output quality over explicit memory, OR a simplified implementation that captures the key benefit (project-scoped behavioral patterns) without the full pipeline complexity. See Active Topics item 1 (Agent Memory).

---

## Incorporated Findings
*(Newest first — add new entries at top when findings are acted on)*

### 2026-07-23 — AI Antipatterns Update: Package Hallucination, Placeholder Credentials, Scope Visibility
**Research**: Multiple 2025-2026 sources — Snyk (package hallucination), Trend Micro (slopsquatting), GitGuardian State of Secrets Sprawl 2026, arXiv studies on agent-generated code maintainability, Karpathy's structural failure patterns.
**Decision**: Added three new detection categories to `my-style/references/antipatterns.md`: (1) package hallucination / slopsquatting (hallucinated package names as supply-chain risk), (2) AI-specific placeholder credentials (`password123`, `supersecretkey`, etc.), (3) scope/visibility over-exposure (public functions with no external callers). Added corresponding mechanical checks to `/plan:audit` Pass 1 (all AUTO tier). Added orthogonal damage detection to `/plan:review` step 3c.
**Rationale**: Existing antipatterns covered most documented AI code issues. These three gaps represent genuinely new risk categories (supply-chain attacks via hallucinated packages, AI-specific credential patterns, systematic scope over-exposure) that weren't in the original reference. Orthogonal damage (Karpathy's "collateral changes") is better caught per-phase in review than per-feature in audit.

### 2026-03-20 — Centralized Semgrep Rules Repository
**Research**: Semgrep MCP installation and custom rule syntax.
**Decision**: Created `/project/semgrep-rules/` with `ai-antipatterns.yml` containing 16 custom rules derived from `my-style/references/antipatterns.md`. Rules cover: mutable defaults, bare except, swallowed exceptions, hardcoded secrets, SQL injection, resource leaks, mock imports in production, tautological assertions, star imports.
**Rationale**: Centralizing rules in this repository (rather than per-project) ensures consistency across all projects and makes rule maintenance trackable via git.
**Update 2026-03-20**: Abandoned MCP integration after ~10 failed attempts. MCP servers run on the HOST, not inside the fish tank — installing in the Dockerfile was architecturally wrong. Rules retained in `/project/semgrep-rules/` for potential future use in CI/pre-commit workflows.

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

### Wholesale Commands → Skills Migration
**Evaluated**: 2026-03-22. Migrating all files in `commands/` to the Skills directory format (each flat `.md` becomes a `SKILL.md` in its own directory), to align with Anthropic's forward-looking Skills surface.
**Rejected because**: The additional Skills capabilities don't solve problems this workflow currently has. Auto-discovery (Claude loads a skill without explicit invocation) is unwanted for plan: commands — you always know which one you need and uninvited activation would be disruptive. `context: fork` (isolated subagent execution) is theoretically useful for `plan:review` but the current manual new-session practice handles it adequately. Dynamic context injection (`!`command``) has no current use case. The existing `commands/plan/references/` structure already provides supporting files. Migration cost is real: every flat `.md` becomes a directory, internal references update, deploy scripts change.
**Revisit if**: A specific command clearly benefits from auto-loading without unwanted activation risk, OR `context: fork` becomes meaningfully better than the current manual new-session approach for `plan:review`, OR dynamic context injection enables a capability (e.g., auto-injecting git status or current date into `plan:status`) that's worth the migration overhead. Migrate that one command, not the whole set.

### jcodemunch MCP for Codebase Exploration
**Evaluated**: 2026-03-20. AST-indexed symbol retrieval MCP server, used via `index_repo`, `search_symbols`, `get_symbol`, `get_file_outline`, `search_text` as a supplement to native Grep/Glob/Read.
**Rejected because**: Token savings are 5–20% in independent testing (vs. the author's claimed 95%), and only on code-reading tokens — which are a small fraction of session cost. The tools actually used duplicate Grep, Glob, and Read. ROI only materializes on monorepos with 500k+ lines and deep call-graph workflows. The largest project in this workflow is ~37k lines; native tools find anything in under 2 seconds. Index goes stale without auto-reindex, creating false negatives. Adds a second overlapping toolset that creates tool-choice overhead. The distinctive tools (`find_importers`, `get_blast_radius`) were not in use.
**Revisit if**: Working regularly on a monorepo with 500k+ lines where repeated cross-file symbol lookups dominate session costs, or if blast-radius analysis becomes a routine part of the workflow.

### Codewriter Agent
**Evaluated**: 2026-03-20. A dedicated agent that writes code fresh with style as primary concern, invoked per-task instead of having the main agent write.
**Rejected because**: Most phase tasks are interdependent in ways that don't appear in signatures — a service written in task 4 needs to match patterns from task 2, a function calls a utility written two tasks earlier. Gating to "truly isolatable tasks" would exclude the majority of tasks in a typical phase. Disconnection risk was judged higher than quality benefit.
**Revisit if**: A reliable method emerges for packaging cross-task dependency context compactly — one that doesn't recreate the context dilution problem in the packaging step.

### Parallel Specialist Reviewers (Qodo 2.0 pattern)
**Evaluated**: 2026-03-20. Running parallel domain-specific review agents (security, style, logic) simultaneously after each task.
**Rejected because**: F1 of 60.1% means 40% of real issues are still missed. Cost and latency overhead not justified at current quality gain. The code-fixer + code-reviewer two-gate model achieves the key benefits more cheaply.
**Revisit if**: F1 scores exceed ~80%, or the cost of parallel agents drops significantly. See Active Topics item 2.
