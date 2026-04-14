# OpenCode + GLM Test Setup

Minimal project for verifying that OpenCode can run GLM through Z.AI's OpenAI-compatible
endpoint and that web search works — the two things that are broken in the Claude Code GLM
fish tank.

## Prerequisites

- OpenCode installed on host (`go install` or binary download)
- `ZHIPU_API_KEY` environment variable set (your Z.AI API key)

## Quick Start

```bash
cd ai-workflow/opencode-test
ZHIPU_API_KEY=your-key-here opencode
```

Then paste this prompt:

```
Run the test checklist from AGENTS.md. Use the web_search_prime tool to search for
"OpenCode AI coding assistant 2026" and report the results.
```

## What We're Testing

| Test | Why It Matters |
|------|---------------|
| GLM model responds | Confirms Z.AI OpenAI-compatible endpoint works with OpenCode |
| `web-search-prime` returns results | Confirms MCP search works outside Claude Code's API proxy |
| No 1210 errors | Confirms the Anthropic-specific API features aren't being forwarded |

## Expected Outcome

If this works, the migration to OpenCode is viable. If `web-search-prime` still returns
empty results, the problem is with Z.AI's MCP service, not with Claude Code.

## Files

- `opencode.json` — OpenCode config with Z.AI provider and web-search-prime MCP
- `AGENTS.md` — Test checklist with pass/fail criteria
- `test-prompt.md` — Copy-paste prompt for running the test
