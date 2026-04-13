# =============================================================================
# Claude Code Docker Functions
# Add to ~/.zshrc (or source from a separate file)
# =============================================================================
# Base function — all Claude Docker invocations go through this.
# Accepts additional docker flags BEFORE the image name, then claude args AFTER.
# Usage: _claude_run [extra-docker-flags...] ai-safe-env [claude-args...]
_claude_run() {
  docker run -it --rm \
    --user "$(id -u):$(id -g)" \
    --cap-drop=ALL \
    --security-opt no-new-privileges \
    --security-opt seccomp="$HOME/.claude/docker/seccomp-no-chmod.json" \
    -e HOME=/home/node \
    -v "$(pwd)":/project \
    -v "$HOME/.claude":/home/node/.claude \
    -v "$HOME/.claude.json":/home/node/.claude.json \
    "$@"
}

# Claude Code with Opus
arch-code() { _claude_run ai-safe-env --model opus "$@"; }

# Claude Code with Sonnet
plan-code() { _claude_run ai-safe-env --model sonnet "$@"; }

# Claude Code with Haiku
mech-code() { _claude_run ai-safe-env --model haiku "$@";}

# Claude Code with GLM (third-party endpoint)
# CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS: suppress anthropic-beta headers that
# the Z.AI proxy forwards to Zhipu, causing 400 errors (also set in settings-glm.json
# env block — belt-and-suspenders since the env var has had bugs with inconsistent
# suppression across Claude Code versions)
gcode() {
  _claude_run \
    -e ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic \
    -e ANTHROPIC_AUTH_TOKEN=[token] \
    -e CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1 \
    ai-safe-env --settings /home/node/.claude/settings-glm.json "$@"
}
