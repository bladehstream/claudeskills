# Chrome DevTools MCP Tools Reference

Complete reference for all tools available via the Chrome DevTools MCP server.

## Navigation Tools

### navigate

Navigate to a URL.

```
mcp__chrome-devtools__navigate
  url: string (required) - The URL to navigate to
  waitUntil?: "load" | "domcontentloaded" | "networkidle0" | "networkidle2"
```

**Example:**
```
Navigate to https://example.com and wait for full load
```

### go_back / go_forward

Navigate browser history.

```
mcp__chrome-devtools__go_back
mcp__chrome-devtools__go_forward
```

### reload

Reload the current page.

```
mcp__chrome-devtools__reload
  ignoreCache?: boolean - Hard reload ignoring cache
```

## Interaction Tools

### click

Click an element.

```
mcp__chrome-devtools__click
  selector: string (required) - CSS selector or XPath
  button?: "left" | "right" | "middle"
  clickCount?: number - Double-click = 2
```

**Example:**
```
Click the submit button using selector "button[type=submit]"
```

### type

Type text into an input.

```
mcp__chrome-devtools__type
  selector: string (required) - Input element selector
  text: string (required) - Text to type
  delay?: number - Delay between keystrokes (ms)
```

**Example:**
```
Type "hello@example.com" into the email input field "#email"
```

### press

Press a keyboard key.

```
mcp__chrome-devtools__press
  key: string (required) - Key name (Enter, Tab, Escape, etc.)
```

### select

Select option(s) from a dropdown.

```
mcp__chrome-devtools__select
  selector: string (required) - Select element
  values: string[] (required) - Option values to select
```

### hover

Hover over an element.

```
mcp__chrome-devtools__hover
  selector: string (required) - Element to hover
```

### scroll

Scroll the page or an element.

```
mcp__chrome-devtools__scroll
  selector?: string - Element to scroll (page if omitted)
  x?: number - Horizontal scroll pixels
  y?: number - Vertical scroll pixels
  behavior?: "auto" | "smooth"
```

### drag_and_drop

Drag element to target.

```
mcp__chrome-devtools__drag_and_drop
  sourceSelector: string (required)
  targetSelector: string (required)
```

## Content Extraction Tools

### get_page_content

Get page content as HTML or text.

```
mcp__chrome-devtools__get_page_content
  format?: "html" | "text" | "markdown"
  selector?: string - Get specific element only
```

### screenshot

Capture screenshot.

```
mcp__chrome-devtools__screenshot
  path?: string - Save path (returns base64 if omitted)
  selector?: string - Screenshot specific element
  fullPage?: boolean - Capture entire scrollable page
  type?: "png" | "jpeg" | "webp"
  quality?: number - JPEG/WebP quality (0-100)
```

**Example:**
```
Take a full-page screenshot of the current page and save to ./screenshots/home.png
```

### get_element_text

Get text content of elements.

```
mcp__chrome-devtools__get_element_text
  selector: string (required) - CSS selector
  all?: boolean - Get all matching elements
```

### get_element_attribute

Get attribute value.

```
mcp__chrome-devtools__get_element_attribute
  selector: string (required)
  attribute: string (required) - href, src, class, etc.
```

### get_element_bounding_box

Get element position and dimensions.

```
mcp__chrome-devtools__get_element_bounding_box
  selector: string (required)
```

Returns: `{ x, y, width, height }`

## JavaScript Execution

### evaluate

Execute JavaScript in page context.

```
mcp__chrome-devtools__evaluate
  expression: string (required) - JS code to execute
  returnByValue?: boolean - Return result value
```

**Examples:**
```
Execute: document.title
Execute: localStorage.getItem('token')
Execute: Array.from(document.querySelectorAll('h2')).map(h => h.textContent)
```

### add_script

Inject a script tag.

```
mcp__chrome-devtools__add_script
  content?: string - Inline script
  url?: string - External script URL
```

## Wait Tools

### wait_for_selector

Wait for element to appear.

```
mcp__chrome-devtools__wait_for_selector
  selector: string (required)
  visible?: boolean - Wait until visible
  hidden?: boolean - Wait until hidden
  timeout?: number - Max wait time (ms)
```

### wait_for_navigation

Wait for page navigation.

```
mcp__chrome-devtools__wait_for_navigation
  waitUntil?: "load" | "domcontentloaded" | "networkidle0"
  timeout?: number
```

### wait_for_network_idle

Wait for network activity to stop.

```
mcp__chrome-devtools__wait_for_network_idle
  idleTime?: number - Required idle time (ms)
  timeout?: number
```

## Debugging Tools

### get_console_logs

Get browser console output.

```
mcp__chrome-devtools__get_console_logs
  level?: "log" | "info" | "warn" | "error" | "all"
  clear?: boolean - Clear logs after retrieval
```

### get_network_requests

Get network request log.

```
mcp__chrome-devtools__get_network_requests
  filter?: {
    urlPattern?: string - Regex pattern
    resourceType?: "document" | "script" | "stylesheet" | "image" | "xhr" | "fetch"
    status?: number - HTTP status code
  }
```

### get_cookies

Get browser cookies.

```
mcp__chrome-devtools__get_cookies
  urls?: string[] - Filter by URLs
```

### set_cookie

Set a cookie.

```
mcp__chrome-devtools__set_cookie
  name: string (required)
  value: string (required)
  domain?: string
  path?: string
  expires?: number - Unix timestamp
  httpOnly?: boolean
  secure?: boolean
```

### delete_cookies

Delete cookies.

```
mcp__chrome-devtools__delete_cookies
  name?: string - Specific cookie name
  domain?: string - All cookies for domain
```

## Viewport Tools

### set_viewport

Set browser viewport size.

```
mcp__chrome-devtools__set_viewport
  width: number (required)
  height: number (required)
  deviceScaleFactor?: number - DPI scaling
  isMobile?: boolean
  hasTouch?: boolean
```

**Common viewports:**
```
Desktop: 1920x1080
Tablet: 768x1024
Mobile: 375x667 (iPhone SE)
Mobile Large: 414x896 (iPhone 11)
```

### emulate_device

Emulate a specific device.

```
mcp__chrome-devtools__emulate_device
  device: string - "iPhone 12", "iPad Pro", "Pixel 5", etc.
```

## Performance Tools

### start_tracing

Start performance trace.

```
mcp__chrome-devtools__start_tracing
  categories?: string[] - Trace categories
```

### stop_tracing

Stop trace and get results.

```
mcp__chrome-devtools__stop_tracing
  path?: string - Save trace file
```

### get_metrics

Get page performance metrics.

```
mcp__chrome-devtools__get_metrics
```

Returns: Layout count, script duration, task duration, JS heap size, etc.

### run_lighthouse

Run Lighthouse audit (if available).

```
mcp__chrome-devtools__run_lighthouse
  url?: string - URL to audit (current page if omitted)
  categories?: ["performance", "accessibility", "best-practices", "seo"]
  output?: "json" | "html"
```

## Page Management

### get_tabs

List open browser tabs.

```
mcp__chrome-devtools__get_tabs
```

### switch_tab

Switch to a different tab.

```
mcp__chrome-devtools__switch_tab
  tabId: string (required)
```

### new_tab

Open a new tab.

```
mcp__chrome-devtools__new_tab
  url?: string - URL to open
```

### close_tab

Close a tab.

```
mcp__chrome-devtools__close_tab
  tabId?: string - Current tab if omitted
```

## File Operations

### upload_file

Handle file input.

```
mcp__chrome-devtools__upload_file
  selector: string (required) - File input selector
  filePath: string (required) - Local file path
```

### download

Trigger and wait for download.

```
mcp__chrome-devtools__download
  triggerSelector: string (required) - Element that triggers download
  savePath?: string - Where to save
```

## Accessibility

### get_accessibility_tree

Get accessibility tree.

```
mcp__chrome-devtools__get_accessibility_tree
  selector?: string - Specific element
  interestingOnly?: boolean - Filter to actionable elements
```

### run_axe_audit

Run axe accessibility audit (if available).

```
mcp__chrome-devtools__run_axe_audit
  selector?: string - Scope to element
  rules?: string[] - Specific rules to check
```
