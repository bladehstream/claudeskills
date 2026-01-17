---
argument-hint: [path|github-url]
description: Analyze a project and explain its purpose, architecture, interfaces, and languages
---

# /whatis - Project Understanding

Analyze the target project and provide a concise summary to seed context.

**Arguments:** $ARGUMENTS

## Instructions

1. **Determine the target:**
   - If no argument provided: use current working directory
   - If local path (starts with `/`, `./`, `~`, or is a relative path without `github.com`): use that path directly
   - If GitHub URL (contains `github.com`): clone to `/tmp/whatis-{repo-name}` and use that

2. **For GitHub URLs:**
   - Parse owner/repo from URL formats:
     - `github.com/owner/repo`
     - `https://github.com/owner/repo`
     - `github.com/owner/repo.git`
     - `https://github.com/owner/repo.git`
   - Extract the repo name (last segment, without `.git`)
   - Run: `git clone --depth 1 https://github.com/{owner}/{repo}.git /tmp/whatis-{repo-name}`
   - If the directory already exists, use it (skip cloning)
   - If clone fails, report error and stop

3. **Explore the project** using the Task tool with `subagent_type: Explore`:

   Prompt the Explore agent to analyze the target directory with focus on:
   - Manifest files: package.json, pyproject.toml, Cargo.toml, go.mod, pom.xml, build.gradle, Makefile, etc.
   - Documentation: README.md, README, CONTRIBUTING.md, docs/ directory
   - Directory structure and organization
   - Key source files (entry points, main modules)
   - Configuration files (.eslintrc, tsconfig.json, .env.example, Dockerfile, CI configs)
   - Test structure and patterns

   Ask the agent to gather enough information to answer: What does this project do? How is it structured? What interfaces does it expose? What technologies does it use?

4. **Output format** (display directly to user, no file output):

```
## Project: {name}

**Purpose:** {1 paragraph explaining what this project does, the problem it solves, and why it exists}

**Architecture:** {1 paragraph describing the high-level structure - key modules/packages, data flow, design patterns, and how components interact}

**Interfaces:** {1 paragraph covering how users or systems interact with this project - APIs, CLIs, UIs, libraries, configuration, etc.}

**Languages & Stack:** {1 paragraph listing the primary language(s), frameworks, major dependencies, build tools, and runtime requirements}
```

5. **No cleanup needed** - `/tmp` is ephemeral and clears on reboot
