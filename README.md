# Claude Code Configuration

Personal Claude Code configuration backup for bootstrapping new development machines.

## Quick Start

```bash
git clone https://github.com/bladehstream/claudeskills.git
cd claudeskills
./bootstrap.sh
```

## Contents

| Directory | Description |
|-----------|-------------|
| `config/` | Global configuration files (CLAUDE.md) |
| `skills/` | User-developed skills |
| `manifest.yaml` | Plugin and marketplace inventory |
| `bootstrap.sh` | Automated setup script |

## What Gets Installed

### Configuration
- `~/.claude/CLAUDE.md` - Global instructions for all projects

### User Skills (13 total)
Custom skills developed locally:
- Game development agents (master_orchestrator, game_feel_developer, etc.)
- Web automation skills (browser-automation, web-research-agent, etc.)
- HTML5 game development workflow

### Plugins (from marketplaces)
Installed from official and community marketplaces:
- superpowers, episodic-memory (superpowers-marketplace)
- frontend-design, feature-dev, code-review, etc. (claude-plugins-official)
- document-skills (anthropic-agent-skills)

## Updating

To sync changes from your current machine:

```bash
# Copy updated skills
cp -r ~/.claude/skills/* skills/

# Copy updated CLAUDE.md
cp ~/.claude/CLAUDE.md config/

# Commit and push
git add -A && git commit -m "Update configuration" && git push
```

## Requirements

- Git
- Claude Code CLI (`npm install -g @anthropic-ai/claude-code`)
- Authenticated Claude Code session
