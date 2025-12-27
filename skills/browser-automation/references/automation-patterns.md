# Browser Automation Patterns

Common automation recipes for Claude Code with Chrome DevTools MCP.

## Data Extraction Patterns

### Table Scraping

```
Claude, navigate to https://example.com/data-table, 
extract all rows from the main table,
and save as a CSV file with headers.
```

**How it works:**
1. Navigate to page
2. Wait for table to load
3. Execute JS to extract table data
4. Format and save to CSV

### Paginated Content

```
Claude, go to https://example.com/articles,
collect all article titles and links from pages 1-5,
save results to articles.json
```

**Pattern:**
```
1. Navigate to first page
2. Extract content
3. Click "Next" or navigate to page N
4. Repeat until done
5. Aggregate and save
```

### Dynamic Content (Infinite Scroll)

```
Claude, go to the Twitter profile page I have open,
scroll down to load 50 tweets,
extract the text of each tweet and save to tweets.txt
```

**Pattern:**
```
1. Navigate to page
2. Scroll down
3. Wait for network idle
4. Check if more content loaded
5. Repeat until target count reached
6. Extract all loaded content
```

## Form Automation Patterns

### Simple Form Fill

```
Claude, go to localhost:3000/contact,
fill in:
- Name: John Doe
- Email: john@example.com
- Message: This is a test message
Then submit the form.
```

### Multi-Step Form (Wizard)

```
Claude, complete the checkout process:
Step 1 - Shipping:
  - Address: 123 Main St
  - City: Anytown
  - Zip: 12345
Step 2 - Payment:
  - Use saved card ending in 4242
Step 3 - Review and confirm order
```

**Pattern:**
```
1. Fill current step fields
2. Click "Next" / "Continue"
3. Wait for next step to load
4. Repeat until complete
5. Click final submit
6. Verify confirmation
```

### Form with File Upload

```
Claude, go to the upload page at localhost:3000/upload,
upload the file ./test-document.pdf,
wait for upload to complete,
and verify the success message.
```

## Testing Patterns

### Smoke Test Flow

```
Claude, verify my app is working:
1. Go to https://myapp.com
2. Log in with test@example.com / TestPass123
3. Navigate to /dashboard
4. Verify the welcome message appears
5. Click the "New Project" button
6. Verify the create form loads
7. Report pass/fail for each step
```

### Visual Regression Check

```
Claude, take screenshots of these pages for visual comparison:
- / (homepage)
- /login
- /dashboard
- /settings

Save each at 1920x1080 and 375x667 viewports
to ./screenshots/current/
```

### Cross-Browser Check

```
Claude, open my site and check that:
1. The hero section renders correctly
2. Navigation menu works
3. Contact form submits
4. No console errors appear

Run in both desktop and mobile viewports.
```

### Error State Testing

```
Claude, test error handling on my login form:
1. Submit empty form - verify validation messages
2. Submit invalid email - verify email error
3. Submit wrong password - verify auth error
4. Check that sensitive data isn't leaked in errors
```

## Monitoring Patterns

### Console Error Check

```
Claude, navigate through my app's main pages:
- /
- /products
- /cart
- /checkout

Report any console errors or warnings on each page.
```

### Network Performance Check

```
Claude, load my homepage and analyze:
1. Total requests made
2. Total bytes transferred
3. Largest resources
4. Any failed requests
5. Time to interactive
```

### Broken Link Detection

```
Claude, crawl my site starting from https://mysite.com,
find all internal links,
check each for 404 errors,
report any broken links found.
```

## Authenticated Session Patterns

### Session Preservation

```bash
# Start Chrome with persistent profile
google-chrome --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.chrome-work-profile"
```

Then:
```
Claude, using my logged-in session,
go to my GitHub notifications,
list any mentions or review requests.
```

### Multi-Account Handling

Create separate profiles for different accounts:

```bash
# Work profile
--user-data-dir="$HOME/.chrome-work"

# Personal profile  
--user-data-dir="$HOME/.chrome-personal"

# Testing profile
--user-data-dir="$HOME/.chrome-test"
```

### Session Token Extraction

```
Claude, after I log in,
extract my authentication token from:
1. localStorage
2. sessionStorage
3. Cookies

Save these to .env.test for API testing.
```

## Batch Processing Patterns

### URL List Processing

```
Claude, read URLs from ./urls.txt,
for each URL:
1. Navigate to the page
2. Take a screenshot
3. Extract the page title and meta description
4. Save results to ./results.json
```

### Scheduled Checking

```
Claude, every time I run this:
1. Go to https://competitor.com/pricing
2. Extract current pricing
3. Compare to ./baseline-prices.json
4. Alert me if anything changed
```

## Integration Patterns

### Export to Spreadsheet

```
Claude, extract data from the dashboard tables,
format as CSV with headers,
save to ./exports/data-{date}.csv
```

### Screenshot for Documentation

```
Claude, document the user flow:
1. Go to login page - screenshot as "01-login.png"
2. Log in - screenshot as "02-dashboard.png"
3. Click settings - screenshot as "03-settings.png"
4. Save all to ./docs/screenshots/
```

### API + Browser Hybrid

```
Claude, 
1. Use the browser to log into the internal dashboard
2. Extract the session cookie
3. Use that cookie to make API calls directly
4. Save API responses to ./api-data/
```

## Debugging Patterns

### Console Log Monitoring

```
Claude, open localhost:3000 and:
1. Interact with the search feature
2. Capture all console output
3. Filter for errors and warnings
4. Report any issues found
```

### Network Request Inspection

```
Claude, load the checkout page and:
1. Log all API calls made
2. Show request/response bodies for /api/cart
3. Check for any failed requests
4. Verify expected endpoints are called
```

### Performance Profiling

```
Claude, run a performance trace on the product listing page:
1. Start trace
2. Scroll through 50 products
3. Stop trace
4. Summarize main thread blocking time
5. Identify any long tasks
```

## Error Handling Patterns

### Retry on Failure

```
Claude, try to load the page 3 times if it fails.
Wait 5 seconds between attempts.
Report if it still fails after retries.
```

### Graceful Degradation

```
Claude, extract product data from the page.
If the modern layout isn't present,
try the legacy layout selectors.
Report which layout was found.
```

### Timeout Handling

```
Claude, load the slow report page with a 60-second timeout.
If it times out, take a screenshot of the current state
and report what loaded so far.
```
