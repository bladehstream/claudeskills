#!/bin/bash
# Claude Code Bootstrap Script
# Restores skills, plugins, and configuration from this repo

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "=== Claude Code Bootstrap ==="
echo "Source: $SCRIPT_DIR"
echo "Target: $CLAUDE_DIR"
echo ""

# Ensure Claude directory exists
mkdir -p "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/commands"

# Copy CLAUDE.md
if [ -f "$SCRIPT_DIR/config/CLAUDE.md" ]; then
    echo "[1/4] Installing CLAUDE.md..."
    cp "$SCRIPT_DIR/config/CLAUDE.md" "$CLAUDE_DIR/CLAUDE.md"
    echo "      -> $CLAUDE_DIR/CLAUDE.md"
else
    echo "[1/4] CLAUDE.md not found, skipping..."
fi

# Copy skills
echo "[2/4] Installing skills..."
if [ -d "$SCRIPT_DIR/skills" ]; then
    cp -r "$SCRIPT_DIR/skills/"* "$CLAUDE_DIR/skills/" 2>/dev/null || true
    echo "      -> Copied $(ls -1 "$SCRIPT_DIR/skills" | wc -l) skills to $CLAUDE_DIR/skills/"
else
    echo "      -> No skills directory found"
fi

# Copy commands
echo "[3/4] Installing commands..."
if [ -d "$SCRIPT_DIR/commands" ]; then
    cp -r "$SCRIPT_DIR/commands/"* "$CLAUDE_DIR/commands/" 2>/dev/null || true
    echo "      -> Copied $(ls -1 "$SCRIPT_DIR/commands" | wc -l) commands to $CLAUDE_DIR/commands/"
else
    echo "      -> No commands directory found"
fi

# Install plugins
echo "[4/4] Installing plugins..."
echo "      Note: Requires 'claude' CLI to be installed and authenticated"
echo ""

# Check if claude CLI exists
if ! command -v claude &> /dev/null; then
    echo "      WARNING: 'claude' command not found. Install Claude Code first:"
    echo "      npm install -g @anthropic-ai/claude-code"
    echo ""
    echo "      After installing, run these commands manually:"
    echo ""
    cat << 'EOF'
claude plugin install superpowers@superpowers-marketplace
claude plugin install frontend-design@claude-plugins-official
claude plugin install feature-dev@claude-plugins-official
claude plugin install code-review@claude-plugins-official
claude plugin install security-guidance@claude-plugins-official
claude plugin install agent-sdk-dev@claude-plugins-official
claude plugin install pr-review-toolkit@claude-plugins-official
claude plugin install linear@claude-plugins-official
claude plugin install plugin-dev@claude-plugins-official
claude plugin install hookify@claude-plugins-official
claude plugin install greptile@claude-plugins-official
claude plugin install document-skills@anthropic-agent-skills
claude plugin install episodic-memory@superpowers-marketplace
EOF
    echo ""
    exit 0
fi

# Install each plugin
PLUGINS=(
    "superpowers@superpowers-marketplace"
    "frontend-design@claude-plugins-official"
    "feature-dev@claude-plugins-official"
    "code-review@claude-plugins-official"
    "security-guidance@claude-plugins-official"
    "agent-sdk-dev@claude-plugins-official"
    "pr-review-toolkit@claude-plugins-official"
    "linear@claude-plugins-official"
    "plugin-dev@claude-plugins-official"
    "hookify@claude-plugins-official"
    "greptile@claude-plugins-official"
    "document-skills@anthropic-agent-skills"
    "episodic-memory@superpowers-marketplace"
)

for plugin in "${PLUGINS[@]}"; do
    echo "      Installing $plugin..."
    claude plugin install "$plugin" 2>/dev/null || echo "      -> Failed or already installed: $plugin"
done

echo ""
echo "=== Bootstrap Complete ==="
echo ""
echo "Installed:"
echo "  - CLAUDE.md (global instructions)"
echo "  - $(ls -1 "$CLAUDE_DIR/skills" 2>/dev/null | wc -l) user skills"
echo "  - $(ls -1 "$CLAUDE_DIR/commands" 2>/dev/null | wc -l) user commands"
echo "  - ${#PLUGINS[@]} plugins"
echo ""
echo "Note: Some plugins may require additional configuration (API keys, etc.)"
