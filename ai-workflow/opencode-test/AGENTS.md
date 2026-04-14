# OpenCode Test Project

This is a minimal test project for verifying that OpenCode works with GLM via Z.AI
and that web search functions correctly through the web-search-prime MCP server.

## Test Checklist

When asked to run the test, perform these steps in order:

1. **MCP connectivity:** Confirm the `web-search-prime` tool is available (check tool list)
2. **Search test:** Use `web_search_prime` to search for "OpenCode AI coding assistant 2026"
   - Expected: array of results with titles, URLs, and summaries
   - Failure: empty array `[]` or connection error
3. **Second search:** Use `web_search_prime` to search for something else (e.g., "Python 3.13 new features")
   - Expected: different results from the first query
4. **WebReader test (if available):** Fetch a known URL to confirm basic HTTP works
5. **Report:** Summarize pass/fail for each step
