# Web Scraping Methodology

## Ethical Guidelines

### Before Scraping Any Site

1. **Check robots.txt**
   ```
   https://example.com/robots.txt
   ```
   Respect `Disallow` directives. If a path is disallowed, don't scrape it.

2. **Review Terms of Service**
   Many sites explicitly prohibit scraping. Violating ToS can have legal consequences.

3. **Consider the Impact**
   - Will your scraping affect site performance?
   - Are you accessing data meant to be public?
   - Is there an official API available instead?

### Rate Limiting

**Always implement delays between requests:**

```python
import time

# Minimum: 1 second between requests
time.sleep(1)

# Better: Randomized delays (looks more natural)
import random
time.sleep(random.uniform(1, 3))

# Best: Respect Crawl-delay in robots.txt
# Some sites specify: Crawl-delay: 10
```

**Rate Limiting Patterns:**

| Site Type | Recommended Delay |
|-----------|-------------------|
| Small/personal sites | 5-10 seconds |
| Medium sites | 2-5 seconds |
| Large sites with APIs | Use the API |
| Sites with no robots.txt | 2-3 seconds minimum |

### User-Agent Best Practices

**Always identify yourself:**

```python
headers = {
    'User-Agent': 'ResearchBot/1.0 (contact@yoursite.com; academic research on topic X)'
}
```

**Bad practice (impersonation):**
```python
# Don't pretend to be a browser if you're a bot
headers = {'User-Agent': 'Mozilla/5.0...'}  # Deceptive
```

**Include:**
- Bot name
- Contact information (email or URL)
- Purpose (briefly)

## Error Handling Patterns

### Robust Request Function

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    session = requests.Session()
    
    # Retry configuration
    retries = Retry(
        total=3,
        backoff_factor=1,  # 1s, 2s, 4s
        status_forcelist=[429, 500, 502, 503, 504]
    )
    
    adapter = HTTPAdapter(max_retries=retries)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    return session

def safe_request(url, session=None):
    if session is None:
        session = create_session()
    
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        return response
    except requests.exceptions.Timeout:
        print(f"Timeout: {url}")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error {e.response.status_code}: {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
```

### Handling Rate Limiting (429)

```python
def request_with_backoff(url, session, max_retries=5):
    for attempt in range(max_retries):
        response = session.get(url)
        
        if response.status_code == 429:
            # Check for Retry-After header
            retry_after = response.headers.get('Retry-After', 60)
            wait_time = int(retry_after) if retry_after.isdigit() else 60
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
            continue
        
        return response
    
    return None
```

### Handling Missing Elements

```python
def safe_extract(element, selector, attr=None, default=None):
    """Extract data without raising exceptions."""
    if element is None:
        return default
    
    found = element.select_one(selector)
    if found is None:
        return default
    
    if attr:
        return found.get(attr, default)
    
    text = found.get_text(strip=True)
    return text if text else default

# Usage
title = safe_extract(card, 'h2.title')
price = safe_extract(card, '.price', default='N/A')
image = safe_extract(card, 'img', attr='src')
```

## Caching Strategies

### Simple File Cache

```python
import hashlib
import os
import json

CACHE_DIR = './cache'

def get_cached(url):
    """Retrieve cached response if exists."""
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.html")
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def save_cache(url, content):
    """Cache response content."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_key = hashlib.md5(url.encode()).hexdigest()
    cache_file = os.path.join(CACHE_DIR, f"{cache_key}.html")
    
    with open(cache_file, 'w', encoding='utf-8') as f:
        f.write(content if isinstance(content, str) else content.decode('utf-8'))

def fetch_with_cache(url, session):
    """Fetch URL, using cache if available."""
    cached = get_cached(url)
    if cached:
        return cached
    
    response = session.get(url)
    if response.ok:
        save_cache(url, response.text)
        return response.text
    return None
```

## Common Scraping Challenges

### Dynamic Content (JavaScript Rendered)

BeautifulSoup only sees static HTML. For JS-rendered content:

1. **Check for JSON in page source** - Many SPAs embed data as JSON
   ```python
   import re
   import json
   
   # Look for embedded JSON data
   script_tags = soup.find_all('script')
   for script in script_tags:
       if script.string and '__NEXT_DATA__' in script.string:
           data = json.loads(script.string)
   ```

2. **Check network requests** - Use browser DevTools to find API endpoints

3. **Use Playwright/Selenium** - For truly dynamic content, use the `web-research-agent` or `qa-testing-agent` skills instead

### Pagination

```python
def scrape_paginated(base_url, session):
    """Scrape all pages of paginated content."""
    all_items = []
    page = 1
    
    while True:
        url = f"{base_url}?page={page}"
        response = session.get(url)
        soup = BeautifulSoup(response.content, 'lxml')
        
        items = soup.select('.item')
        if not items:
            break  # No more items
        
        all_items.extend(items)
        
        # Check for next page link
        next_link = soup.select_one('a.next')
        if not next_link:
            break
        
        page += 1
        time.sleep(2)  # Rate limit
    
    return all_items
```

### Handling Encoding Issues

```python
# Use .content (bytes) not .text (string)
response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

# For problematic encoding, use cchardet
import cchardet

detected = cchardet.detect(response.content)
encoding = detected['encoding']
html = response.content.decode(encoding, errors='replace')
soup = BeautifulSoup(html, 'lxml')
```

### Relative URLs

```python
from urllib.parse import urljoin

base_url = 'https://example.com/products/'

for link in soup.select('a'):
    href = link.get('href')
    if href:
        full_url = urljoin(base_url, href)  # Handles relative URLs
```

## Legal Considerations

**This is not legal advice.** Consult a lawyer for specific situations.

### Generally Accepted
- Scraping publicly available data
- Personal/academic research
- Creating transformative works
- Checking your own content

### Generally Problematic
- Ignoring robots.txt
- Violating Terms of Service
- Scraping behind authentication
- Scraping and republishing copyrighted content
- Causing service disruption
- Scraping personal data (GDPR concerns)

### Key Legal Cases
- *hiQ Labs v. LinkedIn* (2022): Scraping public data may be legal
- *Van Buren v. United States* (2021): CFAA requires unauthorized access

## Data Quality Checklist

Before using scraped data:

- [ ] Verify sample of extracted data against source
- [ ] Check for encoding issues (mojibake characters)
- [ ] Validate URLs are properly resolved
- [ ] Confirm numeric data parsed correctly
- [ ] Check for missing/null values
- [ ] Verify date formats are consistent
- [ ] Look for duplicates
- [ ] Spot check edge cases (empty, very long, special characters)
