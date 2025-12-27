---
name: browser-automation
description: Chrome browser automation via MCP for Claude Code. Use when tasks require browser control, web scraping authenticated pages, visual testing, form filling, or end-to-end testing. Triggers include "control browser", "browse to", "fill form", "test my website", "scrape with login", "screenshot page", or any task requiring live browser interaction. This skill complements the web-research-agent (Playwright) skill - use this when you need MCP integration with Claude Code or authenticated session access.
---

# Browser Automation via Chrome DevTools MCP

Control a live Chrome browser directly from Claude Code using the Model Context Protocol.

## When to Use This vs Other Skills

| Skill | Use When |
|-------|----------|
| **browser-automation** (this) | Claude Code MCP integration, authenticated sessions, real-time debugging |
| **web-research-agent** | Standalone Playwright scripts, batch captures, no MCP needed |
| **qa-testing-agent** | Automated test suites, CI/CD integration, test flow definitions |
| **beautifulsoup-scraper** | Static HTML parsing, no JavaScript rendering needed |

## Quick Setup

### 1. Add MCP Server to Claude Code

```bash
# One-liner install
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest
```

### 2. Launch Chrome with Remote Debugging

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chrome-debug-profile"

# Linux
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chrome-debug-profile"

# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" ^
  --remote-debugging-port=9222 ^
  --user-data-dir="%USERPROFILE%\.chrome-debug-profile"
```

### 3. Verify Connection

In Claude Code:
```
/mcp
```
Look for `chrome-devtools` with status "Connected".

## Available MCP Tools

All tools are prefixed with `mcp__chrome-devtools__`:

| Tool | Description |
|------|-------------|
| `navigate` | Go to a URL |
| `click` | Click an element by selector |
| `type` | Type text into an input field |
| `screenshot` | Capture page or element screenshot |
| `evaluate` | Execute JavaScript in the page |
| `get_page_content` | Get page HTML or text content |
| `get_console_logs` | Retrieve browser console output |
| `get_network_requests` | List network requests/responses |
| `wait_for_selector` | Wait for element to appear |
| `scroll` | Scroll page or element |

## Common Workflows

### Web Navigation & Data Extraction

```
Claude, navigate to https://news.ycombinator.com, 
extract the top 10 story titles and their point counts,
and save them to a CSV file.
```

### Form Automation

```
Claude, go to localhost:3000/signup, fill out the form with:
- Name: Test User
- Email: test@example.com  
- Password: SecurePass123
Then submit and verify the success message appears.
```

### Visual Testing

```
Claude, take screenshots of my homepage at:
- 1920x1080 (desktop)
- 768x1024 (tablet)
- 375x667 (mobile)
Save them to ./screenshots/ with descriptive names.
```

### Authenticated Session Scraping

```
Claude, I'm logged into LinkedIn in Chrome.
Go to my notifications page and summarize any connection requests.
```

### Performance Analysis

```
Claude, navigate to my production site at https://myapp.com,
run a Lighthouse performance audit, and summarize the key issues.
```

### Console Log Debugging

```
Claude, open localhost:3000, interact with the login form,
and show me any console errors that appear.
```

## Persistent Session Setup

For tasks requiring login state (email, social media, internal tools):

### 1. Create Dedicated Debug Profile

```bash
# Start Chrome with persistent profile
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chrome-debug-profile"
```

### 2. Log Into Your Accounts

Manually log into Gmail, GitHub, LinkedIn, etc. in this Chrome window.
Sessions persist across restarts when using the same `--user-data-dir`.

### 3. Configure MCP with Browser URL

```bash
claude mcp add --transport stdio chrome-devtools -- \
  npx -y chrome-devtools-mcp@latest \
  --browserUrl=http://127.0.0.1:9222
```

### 4. Use Authenticated Sessions

```
Claude, check my GitHub notifications and summarize any important ones.
```

## Safety Considerations

### ⚠️ Security Warnings

1. **Remote debugging exposes your browser** - Any process on your machine can connect to port 9222
2. **AI can see everything** - All content in the browser window is accessible to Claude
3. **Use a dedicated profile** - Don't use your main Chrome profile with sensitive accounts
4. **Close when done** - Debugging port closes when Chrome exits

### Best Practices

- ✅ Use a separate `--user-data-dir` for debug sessions
- ✅ Only log into accounts you're comfortable exposing
- ✅ Avoid banking, healthcare, and highly sensitive sites
- ✅ Review actions before confirming high-risk operations
- ❌ Don't browse sensitive personal accounts
- ❌ Don't store passwords for critical services in the debug profile

## Troubleshooting

### "Chrome DevTools not connected"

```bash
# Check if Chrome is running with debugging
curl http://127.0.0.1:9222/json/version

# Should return JSON with Chrome info
# If empty/error, restart Chrome with --remote-debugging-port=9222
```

### "Cannot connect to browser"

```bash
# Kill existing Chrome instances
pkill -f chrome

# Restart with debugging port
google-chrome --remote-debugging-port=9222 --user-data-dir="$HOME/.chrome-debug"
```

### MCP Server Not Appearing

```bash
# Re-add the MCP server
claude mcp remove chrome-devtools
claude mcp add chrome-devtools -- npx -y chrome-devtools-mcp@latest

# Restart Claude Code
```

### "Permission denied" on macOS

```bash
# Chrome 136+ requires user-data-dir for security
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chrome-debug-profile"  # Required!
```

## Alternative: Browser MCP Extension

For simpler setup without command-line Chrome launching:

1. Install [Browser MCP](https://chromewebstore.google.com/detail/browser-mcp-automate-your/bjfgambnhccakkhmkepdoekmckoijdlc) from Chrome Web Store
2. Configure in Claude Code:

```bash
claude mcp add browser-mcp -- npx -y @anthropic/browser-mcp
```

## Integration with Other Skills

### Combined with web-research-agent

Use browser-automation for authenticated access, web-research-agent for batch processing:

```
1. Use browser-automation to log into internal dashboard
2. Export data to CSV
3. Use beautifulsoup-scraper to parse the exported data
```

### Combined with qa-testing-agent

Use browser-automation for exploratory testing, qa-testing-agent for repeatable test suites:

```
1. Explore app manually with browser-automation
2. Create test flow JSON based on discoveries  
3. Run automated tests with qa-testing-agent
```

## Reference Documents

- `references/mcp-tools-reference.md` — Complete tool API documentation
- `references/automation-patterns.md` — Common automation recipes
