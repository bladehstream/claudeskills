# CSS Selector Patterns Reference

## Basic Selectors

| Selector | Description | Example |
|----------|-------------|---------|
| `tag` | Element type | `soup.select('div')` |
| `.class` | Class name | `soup.select('.product')` |
| `#id` | ID | `soup.select('#main')` |
| `*` | All elements | `soup.select('*')` |

## Attribute Selectors

| Selector | Description | Example |
|----------|-------------|---------|
| `[attr]` | Has attribute | `soup.select('a[href]')` |
| `[attr=value]` | Exact match | `soup.select('input[type="text"]')` |
| `[attr^=value]` | Starts with | `soup.select('a[href^="https"]')` |
| `[attr$=value]` | Ends with | `soup.select('a[href$=".pdf"]')` |
| `[attr*=value]` | Contains | `soup.select('a[href*="example"]')` |
| `[attr~=value]` | Word in list | `soup.select('[class~="active"]')` |

## Combinators

| Selector | Description | Example |
|----------|-------------|---------|
| `A B` | Descendant | `soup.select('div p')` |
| `A > B` | Direct child | `soup.select('ul > li')` |
| `A + B` | Adjacent sibling | `soup.select('h1 + p')` |
| `A ~ B` | General sibling | `soup.select('h1 ~ p')` |

## Pseudo-classes

| Selector | Description | Example |
|----------|-------------|---------|
| `:first-child` | First child | `soup.select('li:first-child')` |
| `:last-child` | Last child | `soup.select('li:last-child')` |
| `:nth-child(n)` | Nth child | `soup.select('tr:nth-child(2)')` |
| `:nth-child(odd)` | Odd children | `soup.select('tr:nth-child(odd)')` |
| `:nth-child(even)` | Even children | `soup.select('tr:nth-child(even)')` |
| `:nth-of-type(n)` | Nth of type | `soup.select('p:nth-of-type(3)')` |
| `:not(selector)` | Negation | `soup.select('div:not(.hidden)')` |
| `:empty` | No children | `soup.select('td:empty')` |
| `:has(selector)` | Contains | `soup.select('div:has(> img)')` |

## Common Extraction Patterns

### E-commerce Product Listing

```python
products = []
for card in soup.select('.product-card, .product-item, [data-product]'):
    product = {
        'title': safe_get_text(card, '.product-title, .product-name, h2'),
        'price': safe_get_text(card, '.price, .product-price, [data-price]'),
        'image': safe_get_attr(card, 'img', 'src'),
        'link': safe_get_attr(card, 'a', 'href'),
        'rating': safe_get_text(card, '.rating, .stars'),
        'reviews': safe_get_text(card, '.review-count'),
    }
    products.append(product)

def safe_get_text(element, selectors):
    for sel in selectors.split(', '):
        found = element.select_one(sel)
        if found:
            return found.get_text(strip=True)
    return None

def safe_get_attr(element, selector, attr):
    found = element.select_one(selector)
    return found.get(attr) if found else None
```

### News Article

```python
article = {
    'headline': soup.select_one('h1, .headline, .article-title').get_text(strip=True),
    'author': safe_get_text(soup, '.author, .byline, [rel="author"]'),
    'date': safe_get_text(soup, 'time, .date, .published'),
    'content': '\n'.join(p.get_text() for p in soup.select('article p, .article-body p')),
    'tags': [t.get_text(strip=True) for t in soup.select('.tags a, .topics a')],
}
```

### Table Extraction

```python
def extract_table(table):
    """Extract table to list of dicts."""
    rows = []
    
    # Get headers
    headers = []
    header_row = table.select_one('thead tr') or table.select_one('tr:first-child')
    if header_row:
        headers = [th.get_text(strip=True) for th in header_row.select('th, td')]
    
    # Get data rows
    data_rows = table.select('tbody tr') or table.select('tr')[1:]
    for tr in data_rows:
        cells = [td.get_text(strip=True) for td in tr.select('td')]
        if headers and len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
        elif cells:
            rows.append(cells)
    
    return {'headers': headers, 'rows': rows}
```

### Navigation/Menu Links

```python
nav_links = []
for a in soup.select('nav a, .navigation a, .menu a, header a'):
    nav_links.append({
        'text': a.get_text(strip=True),
        'href': a.get('href'),
        'is_active': 'active' in a.get('class', []),
    })
```

### Form Fields

```python
forms = []
for form in soup.select('form'):
    fields = []
    for input_el in form.select('input, select, textarea'):
        fields.append({
            'name': input_el.get('name'),
            'type': input_el.get('type', 'text'),
            'id': input_el.get('id'),
            'required': input_el.has_attr('required'),
            'placeholder': input_el.get('placeholder'),
        })
    
    forms.append({
        'action': form.get('action'),
        'method': form.get('method', 'get'),
        'fields': fields,
    })
```

### Social Media Meta Tags

```python
social = {
    # Open Graph
    'og_title': soup.select_one('meta[property="og:title"]'),
    'og_description': soup.select_one('meta[property="og:description"]'),
    'og_image': soup.select_one('meta[property="og:image"]'),
    'og_url': soup.select_one('meta[property="og:url"]'),
    
    # Twitter Cards
    'twitter_card': soup.select_one('meta[name="twitter:card"]'),
    'twitter_title': soup.select_one('meta[name="twitter:title"]'),
    'twitter_description': soup.select_one('meta[name="twitter:description"]'),
    'twitter_image': soup.select_one('meta[name="twitter:image"]'),
}

# Extract content attribute
social = {k: v.get('content') if v else None for k, v in social.items()}
```

### Structured Data (JSON-LD)

```python
import json

structured_data = []
for script in soup.select('script[type="application/ld+json"]'):
    try:
        data = json.loads(script.string)
        structured_data.append(data)
    except json.JSONDecodeError:
        pass
```

### Pagination Links

```python
def get_pagination(soup):
    """Extract pagination information."""
    pagination = {
        'current': None,
        'next': None,
        'prev': None,
        'pages': [],
    }
    
    # Current page
    current = soup.select_one('.pagination .active, .pagination .current')
    if current:
        pagination['current'] = int(current.get_text(strip=True))
    
    # Next/prev links
    next_link = soup.select_one('.pagination .next a, a[rel="next"]')
    if next_link:
        pagination['next'] = next_link.get('href')
    
    prev_link = soup.select_one('.pagination .prev a, a[rel="prev"]')
    if prev_link:
        pagination['prev'] = prev_link.get('href')
    
    # All page links
    for a in soup.select('.pagination a[href]'):
        text = a.get_text(strip=True)
        if text.isdigit():
            pagination['pages'].append({
                'page': int(text),
                'href': a.get('href'),
            })
    
    return pagination
```

## Performance Tips

### Use Specific Selectors

```python
# Good - targets directly
soup.select('table.data-table > tbody > tr')

# Slow - searches entire document
soup.select('tr')  # Then manually filter
```

### Use SoupStrainer for Large Documents

```python
from bs4 import BeautifulSoup, SoupStrainer

# Only parse links - much faster
only_links = SoupStrainer('a')
soup = BeautifulSoup(html, 'lxml', parse_only=only_links)

# Only parse specific class
only_products = SoupStrainer('div', class_='product')
soup = BeautifulSoup(html, 'lxml', parse_only=only_products)
```

### Limit Results When Possible

```python
# Get only first 10
soup.find_all('div', class_='item', limit=10)

# Use select_one for single element
soup.select_one('.header')  # Better than soup.select('.header')[0]
```

### Avoid Re-parsing

```python
# Bad - parses twice
soup.select('.products')[0].select('.price')

# Good - store reference
products_section = soup.select_one('.products')
prices = products_section.select('.price')
```

## Debugging Selectors

### Check What You're Getting

```python
# Print matched elements
elements = soup.select('.product')
print(f"Found {len(elements)} elements")
for el in elements[:3]:  # First 3
    print(f"  Tag: {el.name}, Classes: {el.get('class')}")
    print(f"  Text: {el.get_text(strip=True)[:50]}...")
```

### Test Selectors in Browser

1. Open DevTools (F12)
2. Go to Console
3. Test: `document.querySelectorAll('.your-selector')`

### Handle Missing Elements

```python
def extract_or_default(soup, selector, default=''):
    el = soup.select_one(selector)
    if el is None:
        return default
    return el.get_text(strip=True)
```
