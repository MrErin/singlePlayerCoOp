FROM node:20-slim

RUN apt-get update && apt-get install -y \
    git \
    curl \
    ripgrep \
    fd-find \
    jq \
    less \
    procps \
    openssh-client \
    ca-certificates \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Symlink for fd-find
RUN ln -s $(which fdfind) /usr/local/bin/fd

# Install Python tools
RUN pip3 install \
    pytest \
    pytest-cov \
    coverage \
    hypothesis \
    mutmut \
    ruff \
    playwright \
    --break-system-packages

# Install Playwright browser binaries (Chromium only to save image size)
RUN playwright install --with-deps chromium

# Install Claude Code globally AS ROOT — binary goes to /usr/local/bin/claude,
# which is NOT under ~/.claude and won't be shadowed by volume mounts
RUN npm install -g @anthropic-ai/claude-code@2.1.80

# Make /home/node writable for any UID (needed when --user maps to host UID)
RUN chmod 777 /home/node

WORKDIR /project

# Copy and set up entrypoint for PYTHONPATH auto-detection
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Agent-friendly tool wrappers (token-efficient output, correct CLI usage)
COPY mutmut-wrapper.sh /usr/local/bin/mutmut-wrapper
COPY coverage-wrapper.sh /usr/local/bin/coverage-wrapper
RUN chmod +x /usr/local/bin/mutmut-wrapper /usr/local/bin/coverage-wrapper

ENTRYPOINT ["/usr/local/bin/entrypoint.sh", "claude"]