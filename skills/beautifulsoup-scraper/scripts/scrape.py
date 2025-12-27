#!/usr/bin/env python3
"""
BeautifulSoup Web Scraper
Extracts structured data from web pages.

Usage:
    python scrape.py <url> [options]

Options:
    --output, -o <file>     Output file (JSON or CSV based on extension)
    --select <selector>     CSS selector for elements to extract
    --tables                Extract all tables as structured data
    --links                 Extract all links
    --images                Extract all image sources
    --text                  Extract all text content
    --meta                  Extract page metadata
    --raw                   Output raw HTML of selected elements
    --delay <seconds>       Delay between requests (default: 1)
    --parser <parser>       Parser to use: lxml, html.parser, html5lib (default: lxml)
"""

import argparse
import json
import csv
import sys
import time
from urllib.parse import urljoin, urlparse

try:
    import requests
    from bs4 import BeautifulSoup, SoupStrainer
except ImportError:
    print("Required packages not installed. Run:")
    print("pip install beautifulsoup4 lxml requests cchardet --break-system-packages")
    sys.exit(1)


def get_page(url, session=None, delay=1):
    """Fetch page content with rate limiting."""
    headers = {
        'User-Agent': 'Research Bot (academic/personal research)',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    
    if session is None:
        session = requests.Session()
        session.headers.update(headers)
    
    time.sleep(delay)  # Rate limiting
    
    try:
        response = session.get(url, timeout=30)
        response.raise_for_status()
        return response.content, session
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None, session


def extract_metadata(soup, url):
    """Extract page metadata."""
    meta = {
        'url': url,
        'title': soup.title.string if soup.title else None,
        'description': None,
        'keywords': None,
        'author': None,
        'og_title': None,
        'og_description': None,
        'og_image': None,
    }
    
    # Standard meta tags
    desc_tag = soup.find('meta', attrs={'name': 'description'})
    if desc_tag:
        meta['description'] = desc_tag.get('content')
    
    keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
    if keywords_tag:
        meta['keywords'] = keywords_tag.get('content')
    
    author_tag = soup.find('meta', attrs={'name': 'author'})
    if author_tag:
        meta['author'] = author_tag.get('content')
    
    # Open Graph tags
    og_title = soup.find('meta', attrs={'property': 'og:title'})
    if og_title:
        meta['og_title'] = og_title.get('content')
    
    og_desc = soup.find('meta', attrs={'property': 'og:description'})
    if og_desc:
        meta['og_description'] = og_desc.get('content')
    
    og_image = soup.find('meta', attrs={'property': 'og:image'})
    if og_image:
        meta['og_image'] = og_image.get('content')
    
    return meta


def extract_links(soup, base_url):
    """Extract all links with text and resolved URLs."""
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        # Resolve relative URLs
        full_url = urljoin(base_url, href)
        
        links.append({
            'text': a.get_text(strip=True),
            'url': full_url,
            'title': a.get('title'),
            'rel': a.get('rel'),
        })
    return links


def extract_images(soup, base_url):
    """Extract all images with sources and alt text."""
    images = []
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src:
            full_url = urljoin(base_url, src)
            images.append({
                'src': full_url,
                'alt': img.get('alt'),
                'title': img.get('title'),
                'width': img.get('width'),
                'height': img.get('height'),
            })
    return images


def extract_tables(soup):
    """Extract all tables as list of dicts."""
    tables = []
    for i, table in enumerate(soup.find_all('table')):
        table_data = {
            'index': i,
            'id': table.get('id'),
            'class': table.get('class'),
            'headers': [],
            'rows': []
        }
        
        # Extract headers
        header_row = table.find('tr')
        if header_row:
            headers = []
            for th in header_row.find_all(['th', 'td']):
                headers.append(th.get_text(strip=True))
            table_data['headers'] = headers
        
        # Extract rows
        for tr in table.find_all('tr')[1:]:  # Skip header row
            cells = [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])]
            if cells and any(cells):  # Skip empty rows
                if table_data['headers'] and len(cells) == len(table_data['headers']):
                    # Convert to dict if headers match
                    table_data['rows'].append(dict(zip(table_data['headers'], cells)))
                else:
                    table_data['rows'].append(cells)
        
        tables.append(table_data)
    
    return tables


def extract_text(soup):
    """Extract all text content, cleaned."""
    # Remove script and style elements
    for script in soup(['script', 'style', 'noscript']):
        script.decompose()
    
    text = soup.get_text(separator='\n', strip=True)
    # Clean up multiple newlines
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return '\n'.join(lines)


def extract_by_selector(soup, selector, raw=False):
    """Extract elements matching CSS selector."""
    elements = soup.select(selector)
    
    if raw:
        return [str(el) for el in elements]
    
    results = []
    for el in elements:
        result = {
            'tag': el.name,
            'text': el.get_text(strip=True),
            'attrs': dict(el.attrs) if el.attrs else {},
        }
        
        # Include common attributes directly
        if el.get('href'):
            result['href'] = el['href']
        if el.get('src'):
            result['src'] = el['src']
        if el.get('id'):
            result['id'] = el['id']
        
        results.append(result)
    
    return results


def save_output(data, output_file):
    """Save data to JSON or CSV file."""
    if output_file.endswith('.csv'):
        # CSV output (works best with flat data)
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        else:
            print("CSV output requires list of dicts. Falling back to JSON.", file=sys.stderr)
            output_file = output_file.replace('.csv', '.json')
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        # JSON output (default)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(description='BeautifulSoup Web Scraper')
    parser.add_argument('url', help='URL to scrape')
    parser.add_argument('--output', '-o', help='Output file (JSON or CSV)')
    parser.add_argument('--select', help='CSS selector for elements')
    parser.add_argument('--tables', action='store_true', help='Extract tables')
    parser.add_argument('--links', action='store_true', help='Extract links')
    parser.add_argument('--images', action='store_true', help='Extract images')
    parser.add_argument('--text', action='store_true', help='Extract text')
    parser.add_argument('--meta', action='store_true', help='Extract metadata')
    parser.add_argument('--raw', action='store_true', help='Output raw HTML')
    parser.add_argument('--delay', type=float, default=1, help='Delay between requests')
    parser.add_argument('--parser', default='lxml', 
                        choices=['lxml', 'html.parser', 'html5lib'],
                        help='Parser to use')
    
    args = parser.parse_args()
    
    # Fetch page
    content, _ = get_page(args.url, delay=args.delay)
    if content is None:
        sys.exit(1)
    
    # Parse
    soup = BeautifulSoup(content, args.parser)
    
    # Extract based on options
    result = {}
    
    if args.select:
        result['selected'] = extract_by_selector(soup, args.select, args.raw)
    
    if args.tables:
        result['tables'] = extract_tables(soup)
    
    if args.links:
        result['links'] = extract_links(soup, args.url)
    
    if args.images:
        result['images'] = extract_images(soup, args.url)
    
    if args.text:
        result['text'] = extract_text(soup)
    
    if args.meta:
        result['metadata'] = extract_metadata(soup, args.url)
    
    # Default: extract metadata if no options specified
    if not any([args.select, args.tables, args.links, args.images, args.text, args.meta]):
        result['metadata'] = extract_metadata(soup, args.url)
        result['links'] = extract_links(soup, args.url)[:20]  # First 20 links
    
    # Output
    if args.output:
        # For single extraction type, flatten output
        if len(result) == 1:
            save_output(list(result.values())[0], args.output)
        else:
            save_output(result, args.output)
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
