---
name: web-research-agent
description: Visual web research using Playwright to capture screenshots and extract data from live websites. Use when tasks require analyzing visual webpage layouts, capturing charts/graphs/dashboards, extracting dynamic content from SPAs, or synthesizing both visual and textual web data. Triggers include "screenshot this page", "capture the dashboard", "show me what [site] looks like", "analyze this webpage visually", or research tasks needing current visual state of websites.
---

# Web Research Agent

Capture and analyze live web content visually using Playwright with your existing Chrome installation.

## Setup (One-Time per Session)

Install Playwright package (uses existing Chrome, no browser download):

```bash
npm install playwright
```

Verify Chrome is available:
```bash
which google-chrome || which google-chrome-stable
```

## Core Workflow

### 1. Screenshot Capture

```javascript
// scripts/capture.js - adapt paths as needed
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ 
    channel: 'chrome',  // Uses existing Chrome installation
    headless: true 
  });
  const page = await browser.newPage();
  
  // Set viewport for consistent captures
  await page.setViewportSize({ width: 1280, height: 800 });
  
  await page.goto(process.argv[2], { waitUntil: 'networkidle' });
  await page.screenshot({ 
    path: process.argv[3] || 'screenshot.png',
    fullPage: process.argv[4] === '--full'
  });
  
  await browser.close();
})();
```

Usage:
```bash
node scripts/capture.js "https://example.com" output.png
node scripts/capture.js "https://example.com" output.png --full  # Full page
```

### 2. Screenshot + Text Extraction (Hybrid)

```javascript
// scripts/capture_hybrid.js
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const url = process.argv[2];
  const outputBase = process.argv[3] || 'capture';
  
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  const page = await browser.newPage();
  await page.setViewportSize({ width: 1280, height: 800 });
  await page.goto(url, { waitUntil: 'networkidle' });
  
  // Capture screenshot
  await page.screenshot({ path: `${outputBase}.png` });
  
  // Extract text content
  const text = await page.evaluate(() => document.body.innerText);
  fs.writeFileSync(`${outputBase}.txt`, text);
  
  // Extract structured data if present
  const metadata = await page.evaluate(() => ({
    title: document.title,
    h1: Array.from(document.querySelectorAll('h1')).map(e => e.innerText),
    h2: Array.from(document.querySelectorAll('h2')).map(e => e.innerText),
    links: Array.from(document.querySelectorAll('a[href]')).slice(0, 20).map(a => ({
      text: a.innerText.trim().slice(0, 50),
      href: a.href
    }))
  }));
  fs.writeFileSync(`${outputBase}_meta.json`, JSON.stringify(metadata, null, 2));
  
  await browser.close();
  console.log(`Captured: ${outputBase}.png, ${outputBase}.txt, ${outputBase}_meta.json`);
})();
```

### 3. Element-Specific Capture

```javascript
// Capture specific element (charts, tables, etc.)
const element = await page.locator('selector').first();
await element.screenshot({ path: 'element.png' });
```

### 4. Wait Strategies for Dynamic Content

```javascript
// Wait for specific element
await page.waitForSelector('.data-loaded', { timeout: 10000 });

// Wait for network idle (SPAs)
await page.waitForLoadState('networkidle');

// Wait for specific text
await page.waitForFunction(() => 
  document.body.innerText.includes('Loading complete')
);

// Custom delay (last resort)
await page.waitForTimeout(2000);
```

## Research Workflow Pattern

1. **Capture**: Run capture script to get screenshot + text
2. **View**: Use Claude's `view` tool on the screenshot for visual analysis
3. **Parse**: Read extracted text/JSON for searchable data
4. **Synthesize**: Combine visual observations with text data

Example:
```bash
node scripts/capture_hybrid.js "https://dashboard.example.com" ./research/site1
# Then use view tool on ./research/site1.png
```

## Handling Authentication

For sites requiring login, use persistent context:

```javascript
const context = await chromium.launchPersistentContext(
  '/path/to/chrome/profile',  // e.g., ~/.config/google-chrome/Default
  { channel: 'chrome', headless: false }  // headless: false for initial auth
);
```

Or inject cookies:
```javascript
await context.addCookies([{ name: 'session', value: 'xxx', domain: '.example.com' }]);
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Chrome not found | Verify path: `which google-chrome` or set `executablePath` explicitly |
| Timeout on SPA | Increase timeout, add `waitForSelector` for dynamic content |
| Blank screenshot | Add delay or wait for `networkidle` |
| Permission denied | Run Chrome with `--no-sandbox` in containerized environments |

## Limitations

- Cannot bypass CAPTCHAs or bot detection without additional tooling
- Some sites block headless browsers (try `headless: false` for debugging)
- Heavy JS sites may need longer wait times
- Authentication requires manual session setup or cookie injection

## Research Guidance

Before starting research, consult `references/research-methodology.md` for:
- Source priority framework (primary sources > expert analysis > community > general)
- What to screenshot vs. text-extract
- Source evaluation checklist (currency, authority, accuracy, purpose, bias)
- Domain-specific guidance (cybersecurity, fintech, technical, medical)
- Synthesis guidelines and red flags

Key principles:
1. **Lead with authoritative sources**: .gov, official docs, peer-reviewed first
2. **Screenshot visuals, extract text**: Charts/diagrams need visual capture; prose doesn't
3. **Note contradictions**: Flag conflicting sources for human review
4. **State confidence levels**: Distinguish fact from consensus from speculation

## Technical Reference

See `references/advanced-patterns.md` for:
- Table/chart data extraction
- Multi-page crawling
- PDF capture
- Mobile viewport emulation
- Network interception (capturing API responses)
- Bot detection workarounds
