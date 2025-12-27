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

## Maintaining Skills

### Syncing Local Changes to This Repo

When you create or modify skills on your development machine:

```bash
cd /path/to/claudeskills

# Sync all skills
cp -r ~/.claude/skills/* skills/

# Sync CLAUDE.md if changed
cp ~/.claude/CLAUDE.md config/

# Review changes
git status
git diff

# Commit with descriptive message
git add -A && git commit -m "feat: Add new skill for X" && git push
```

### Recommended Workflow

1. **Develop skills locally** in `~/.claude/skills/`
2. **Test thoroughly** before syncing
3. **Sync to repo** using commands above
4. **Use meaningful commits** - one commit per logical change

### Keeping Multiple Machines in Sync

On secondary machines after initial bootstrap:

```bash
cd /path/to/claudeskills
git pull

# Re-run bootstrap to apply updates
./bootstrap.sh
```

Or manually copy specific updates:

```bash
git pull
cp -r skills/* ~/.claude/skills/
cp config/CLAUDE.md ~/.claude/CLAUDE.md
```

### Adding New Plugins

When you install new plugins via `claude plugin install`:

1. Update `manifest.yaml` with the new plugin entry
2. Update `bootstrap.sh` to include the install command
3. Commit both files

```bash
# After installing a new plugin locally
echo "  - newplugin@marketplace" >> manifest.yaml
# Edit bootstrap.sh to add the install command
git add -A && git commit -m "feat: Add newplugin" && git push
```

### Handling Conflicts

If skills diverge between machines:

```bash
# See what changed
git diff HEAD~1 skills/

# Keep local version
cp ~/.claude/skills/skillname.md skills/skillname.md

# Or keep repo version
cp skills/skillname.md ~/.claude/skills/skillname.md
```

### Backup Before Major Changes

```bash
# Create a backup branch before significant refactoring
git checkout -b backup/$(date +%Y%m%d)
git checkout main
```

## Requirements

- Git
- Claude Code CLI (`npm install -g @anthropic-ai/claude-code`)
- Authenticated Claude Code session
