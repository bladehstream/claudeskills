---
name: qa-testing-agent
description: Functional testing agent using Playwright to test web applications across desktop and mobile viewports. Use when tasks require UI testing, regression testing, cross-browser validation, responsive design verification, form testing, user flow validation, accessibility checks, or performance profiling. Triggers include "test this app", "check if [feature] works", "verify mobile layout", "find bugs", "regression test", "smoke test", or any application quality assurance task.
---

# QA Testing Agent

Functional testing for web applications using Playwright with existing Chrome installation. Supports desktop, tablet, and mobile viewports.

## Setup (One-Time per Session)

```bash
npm install playwright
```

## Core Testing Script

```bash
node scripts/test-runner.js <url> [options]
```

Options:
| Flag | Description |
|------|-------------|
| `--viewport` | desktop (1280x800), tablet (768x1024), mobile (375x667) |
| `--flow` | Path to test flow JSON file |
| `--output` | Output directory for screenshots/reports |
| `--full` | Capture full-page screenshots |
| `--trace` | Enable Playwright trace recording |
| `--slow` | Slow down actions by ms (for debugging) |

## Quick Start Examples

### Basic Page Load Test
```bash
node scripts/test-runner.js "https://app.example.com" --viewport desktop --output ./results
```

### Multi-Viewport Responsive Test
```bash
node scripts/test-runner.js "https://app.example.com" --viewport all --output ./results
```

### User Flow Test
```bash
node scripts/test-runner.js "https://app.example.com" --flow flows/login-flow.json --output ./results
```

## Test Flow Definition

Create JSON files to define test sequences:

```json
{
  "name": "Login Flow",
  "steps": [
    { "action": "goto", "url": "https://app.example.com/login" },
    { "action": "screenshot", "name": "login-page" },
    { "action": "fill", "selector": "#email", "value": "test@example.com" },
    { "action": "fill", "selector": "#password", "value": "testpass123" },
    { "action": "screenshot", "name": "filled-form" },
    { "action": "click", "selector": "button[type=submit]" },
    { "action": "wait", "for": "navigation" },
    { "action": "screenshot", "name": "post-login" },
    { "action": "assert", "type": "url", "contains": "/dashboard" },
    { "action": "assert", "type": "visible", "selector": ".welcome-message" }
  ]
}
```

### Available Actions

| Action | Parameters | Description |
|--------|------------|-------------|
| `goto` | url | Navigate to URL |
| `click` | selector | Click element |
| `fill` | selector, value | Type into input |
| `select` | selector, value | Select dropdown option |
| `check` | selector | Check checkbox |
| `uncheck` | selector | Uncheck checkbox |
| `hover` | selector | Hover over element |
| `screenshot` | name | Capture screenshot |
| `wait` | for (navigation\|networkidle\|timeout), ms | Wait condition |
| `waitFor` | selector, state (visible\|hidden\|attached) | Wait for element |
| `assert` | type, various | Verify condition (see assertions) |
| `scroll` | selector OR position (top\|bottom\|{x,y}) | Scroll page/element |
| `press` | key | Press keyboard key |
| `evaluate` | script | Run JS in page context |

### Assertion Types

| Type | Parameters | Example |
|------|------------|---------|
| `url` | contains, equals, matches | `{"type": "url", "contains": "/dashboard"}` |
| `title` | contains, equals | `{"type": "title", "equals": "Home"}` |
| `visible` | selector | `{"type": "visible", "selector": ".success"}` |
| `hidden` | selector | `{"type": "hidden", "selector": ".loading"}` |
| `text` | selector, contains/equals | `{"type": "text", "selector": "h1", "contains": "Welcome"}` |
| `count` | selector, equals/min/max | `{"type": "count", "selector": ".item", "min": 1}` |
| `attribute` | selector, attr, value | `{"type": "attribute", "selector": "input", "attr": "disabled", "value": "true"}` |

## Device Presets

The test runner includes these viewport presets:

| Preset | Dimensions | User Agent |
|--------|------------|------------|
| `desktop` | 1280x800 | Chrome desktop |
| `desktop-hd` | 1920x1080 | Chrome desktop |
| `tablet` | 768x1024 | iPad |
| `tablet-landscape` | 1024x768 | iPad landscape |
| `mobile` | 375x667 | iPhone SE |
| `mobile-large` | 414x896 | iPhone 11 Pro Max |
| `mobile-android` | 360x740 | Pixel 5 |

Use `--viewport all` to run tests across desktop, tablet, and mobile.

## Output Structure

```
results/
├── desktop/
│   ├── screenshots/
│   │   ├── 01-login-page.png
│   │   ├── 02-filled-form.png
│   │   └── 03-post-login.png
│   ├── trace.zip          # If --trace enabled
│   └── report.json
├── tablet/
│   └── ...
├── mobile/
│   └── ...
└── summary.json           # Cross-viewport summary
```

## Testing Guidelines

Consult `references/testing-methodology.md` for:
- Test case prioritization (critical paths first)
- What to test on each viewport
- Common failure patterns to check
- Accessibility testing checklist
- Performance metrics to capture
- Bug report formatting

Key principles:
1. **Critical paths first**: Login, checkout, core features before edge cases
2. **Mobile breakpoints matter**: Test at exact breakpoints, not just "mobile"
3. **State capture**: Screenshot before AND after interactions
4. **Error states**: Intentionally trigger validation errors, 404s, timeouts
5. **Console monitoring**: Capture JS errors and warnings

## Technical Reference

See `references/advanced-testing.md` for:
- Network request mocking
- Authentication handling
- File upload testing
- iframe and popup handling
- Performance profiling (Core Web Vitals)
- Visual regression comparison
- Accessibility audits (axe-core integration)
