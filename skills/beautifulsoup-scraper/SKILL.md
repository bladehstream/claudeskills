---
name: beautifulsoup-scraper
description: HTML/XML parsing and data extraction using BeautifulSoup4 with requests. Use when tasks require scraping static web pages, extracting structured data (tables, links, lists), parsing HTML/XML files, cleaning HTML content, or preparing web data for analysis. Triggers include "scrape this page", "extract data from", "parse HTML", "get all links/tables/items from", or any structured data extraction from web content.
---

# BeautifulSoup Scraper

Parse HTML/XML and extract structured data using BeautifulSoup4 with the lxml parser for optimal performance.

## Setup

```bash
pip install beautifulsoup4 lxml requests cchardet --break-system-packages
```

**Dependencies:**
- `beautifulsoup4`: Core parsing library
- `lxml`: Fast C-based parser (10x faster than html.parser)
- `requests`: HTTP client
- `cchardet`: Fast encoding detection

## Quick Start

```python
import requests
from bs4 import BeautifulSoup

# Fetch and parse
response = requests.get('https://example.com')
soup = BeautifulSoup(response.content, 'lxml')  # Use .content not .text

# Extract data
title = soup.title.string
links = [a['href'] for a in soup.find_all('a', href=True)]
```

## Parser Selection

| Parser | Speed | Tolerance | Use When |
|--------|-------|-----------|----------|
| `lxml` | Fastest | Good | **Default choice** - most scraping tasks |
| `html.parser` | Medium | Good | No external dependencies needed |
| `html5lib` | Slowest | Best | Extremely malformed HTML |
| `lxml-xml` | Fast | Strict | XML documents |

```python
# Performance-critical (recommended)
soup = BeautifulSoup(html, 'lxml')

# Fallback for broken HTML
soup = BeautifulSoup(html, 'html5lib')
```

## Core Methods

### Finding Elements

```python
# Single element
soup.find('div')                          # First <div>
soup.find('div', class_='content')        # By class
soup.find('div', id='main')               # By ID
soup.find('a', href=True)                 # Has attribute
soup.find('input', {'type': 'email'})     # By attribute dict

# Multiple elements
soup.find_all('p')                        # All <p> tags
soup.find_all(['h1', 'h2', 'h3'])         # Multiple tags
soup.find_all('div', limit=5)             # First 5 matches
soup.find_all(class_='item')              # All with class
soup.find_all(string='exact text')        # By text content
```

### CSS Selectors (Often More Efficient)

```python
# select() returns list, select_one() returns first match
soup.select('div.content')                # Class
soup.select('#main')                      # ID
soup.select('div > p')                    # Direct child
soup.select('div p')                      # Any descendant
soup.select('a[href^="https"]')           # Attribute starts with
soup.select('a[href$=".pdf"]')            # Attribute ends with
soup.select('a[href*="example"]')         # Attribute contains
soup.select('tr:nth-of-type(2)')          # nth element
soup.select('p.intro, p.summary')         # Multiple selectors
```

### Extracting Data

```python
element = soup.find('div')

# Text content
element.text                   # All text (including children)
element.get_text(strip=True)   # Stripped whitespace
element.get_text(separator=' ') # Custom separator

# Attributes
element['class']               # Direct access (raises KeyError if missing)
element.get('href')            # Safe access (returns None if missing)
element.attrs                  # All attributes as dict

# Navigation
element.parent                 # Parent element
element.children               # Direct children (generator)
element.descendants            # All descendants (generator)
element.next_sibling           # Next sibling
element.find_next('p')         # Next <p> in document
```

## Common Extraction Patterns

### Extract All Links
```python
links = []
for a in soup.find_all('a', href=True):
    links.append({
        'text': a.get_text(strip=True),
        'url': a['href']
    })
```

### Extract Table to List of Dicts
```python
def table_to_dicts(table):
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    rows = []
    for tr in table.find_all('tr')[1:]:  # Skip header row
        cells = [td.get_text(strip=True) for td in tr.find_all('td')]
        if cells:
            rows.append(dict(zip(headers, cells)))
    return rows

tables = soup.find_all('table')
data = table_to_dicts(tables[0])
```

### Extract Structured Items
```python
items = []
for card in soup.select('.product-card'):
    items.append({
        'title': card.select_one('.title').get_text(strip=True),
        'price': card.select_one('.price').get_text(strip=True),
        'image': card.select_one('img').get('src'),
        'link': card.select_one('a').get('href')
    })
```

## Performance Optimization

### Use SoupStrainer for Large Documents
```python
from bs4 import BeautifulSoup, SoupStrainer

# Parse only <a> tags - much faster for large documents
only_links = SoupStrainer('a')
soup = BeautifulSoup(html, 'lxml', parse_only=only_links)
```

### Efficient Selectors
```python
# Good - specific selector
soup.select('div.products > article.item')

# Avoid - traverses entire DOM
soup.find_all('article')  # then filter manually
```

### Session Reuse
```python
session = requests.Session()
session.headers.update({'User-Agent': 'Research Bot (contact@example.com)'})

# Reuses TCP connection
for url in urls:
    response = session.get(url)
    # parse...
```

## Error Handling

```python
def safe_extract(element, selector, attr=None, default=None):
    """Safely extract text or attribute from element."""
    found = element.select_one(selector) if element else None
    if not found:
        return default
    if attr:
        return found.get(attr, default)
    return found.get_text(strip=True)

# Usage
title = safe_extract(card, '.title')
image = safe_extract(card, 'img', attr='src')
```

## Ethical Scraping Guidelines

Consult `references/scraping-methodology.md` for:
- robots.txt compliance
- Rate limiting patterns
- User-Agent best practices
- Legal considerations

Key principles:
1. **Check robots.txt** before scraping any site
2. **Rate limit** requests (1-2 seconds between requests minimum)
3. **Identify yourself** with a descriptive User-Agent
4. **Cache responses** to avoid duplicate requests
5. **Respect Terms of Service**

## Script Usage

```bash
# Basic extraction
python scripts/scrape.py "https://example.com" --output data.json

# With selectors
python scripts/scrape.py "https://example.com" --select "div.content" --output content.json

# Table extraction
python scripts/scrape.py "https://example.com" --tables --output tables.json
```

## Reference Documents

- `references/scraping-methodology.md` — Ethical guidelines, rate limiting, error handling
- `references/selector-patterns.md` — Common CSS selectors and extraction patterns
