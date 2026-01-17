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
| `commands/` | Custom slash commands |
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

### User Commands
Custom slash commands for workflow automation:
- `/handoff [session-name]` - Generate a context handoff document before clearing
- `/resume [session-name] [--keep]` - Load handoff document after clearing to restore context
- `/whatis [path|github-url]` - Analyze a project and explain its purpose, architecture, interfaces, and languages

### Plugins (from marketplaces)
Installed from official and community marketplaces:
- superpowers, episodic-memory (superpowers-marketplace)
- frontend-design, feature-dev, code-review, etc. (claude-plugins-official)
- document-skills (anthropic-agent-skills)

## Context Management with Handoff/Resume

Long Claude Code sessions can suffer from "context rot" where performance degrades as the context window fills with noise, dead ends, and outdated information. The `/handoff` and `/resume` commands provide a structured way to clear context while preserving essential state.

### Workflow

```
/handoff [session-name]  →  /clear  →  /resume [session-name]
```

1. **`/handoff [session-name]`** - Generates a comprehensive context document containing:
   - Current objective and architectural context
   - Work completed and remaining
   - Discovered constraints and rejected approaches
   - Current state (git, tests, processes)
   - A resumption prompt for the fresh instance

   Output location:
   - With session name: `.claude/handoffs/handoff-{session-name}.md`
   - Without session name: `.claude/handoffs/handoff.md`

2. **`/clear`** - Built-in Claude Code command that clears the context window

3. **`/resume [session-name] [--keep]`** - Loads the handoff document, internalizes the state, and continues work
   - Use `--keep` to preserve the handoff file after loading (useful for debugging or re-resuming)

### When to Use

- **MID_TASK**: Context is degrading, work is incomplete
- **TASK_COMPLETE**: Clean handoff to next phase
- **CHECKPOINT**: Before risky operations
- **SESSION_END**: Ending for now, will resume later

### Multi-Session Support

Named sessions allow parallel workstreams without collision:

```bash
# Working on feature A
/handoff feature-a
/clear

# Start working on feature B
/handoff feature-b
/clear

# Resume either session independently
/resume feature-a
/resume feature-b
```

### Design Notes

- **Explicit user intent**: Three separate commands ensure deliberate action at each step
- **Auto-cleanup**: The handoff file is deleted after successful resume to prevent stale reloads (use `--keep` to override)
- **Isolated storage**: Handoff files live in `.claude/handoffs/` to prevent accidental deletion of other config files
- **Not hooks**: SessionStart hooks fire on ALL sessions and can't reliably distinguish post-clear resume from new sessions

## Quick Project Understanding with /whatis

The `/whatis` command provides rapid context about any project, useful when:
- Starting work on an unfamiliar codebase
- Quickly understanding a GitHub repository before cloning
- Seeding context at the start of a session

### Usage

```bash
# Analyze current directory
/whatis

# Analyze a local path
/whatis /path/to/project

# Analyze a GitHub repository (clones to /tmp)
/whatis https://github.com/owner/repo
/whatis github.com/owner/repo
```

### Output

Returns a structured summary with four sections:
- **Purpose**: What the project does and why it exists
- **Architecture**: High-level structure, modules, and design patterns
- **Interfaces**: How users/systems interact (APIs, CLIs, UIs, libraries)
- **Languages & Stack**: Technologies, frameworks, and dependencies

## Maintaining Skills

### Syncing Local Changes to This Repo

When you create or modify skills or commands on your development machine:

```bash
cd /path/to/claudeskills

# Sync all skills
cp -r ~/.claude/skills/* skills/

# Sync all commands
cp -r ~/.claude/commands/* commands/

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
cp -r commands/* ~/.claude/commands/
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
