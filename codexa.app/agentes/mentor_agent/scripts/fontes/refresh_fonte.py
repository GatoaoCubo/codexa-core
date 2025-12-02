#!/usr/bin/env python3
"""
Refresh documentation from external sources.

This script fetches latest documentation, processes it, and saves locally:
1. Fetches content from URLs
2. Converts HTML to Markdown
3. Structures content by topics
4. Saves to FONTES/ directory
5. Updates catalogo_fontes.json

Usage:
    python refresh_fonte.py --fonte FONTE_ID
    python refresh_fonte.py --all
    python refresh_fonte.py --priority critical
"""

import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import logging
from bs4 import BeautifulSoup
import html2text

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
MENTOR_ROOT = Path(__file__).parent.parent.parent
CATALOGO_PATH = MENTOR_ROOT / "FONTES" / "catalogo_fontes.json"
FONTES_ROOT = MENTOR_ROOT / "FONTES"

def load_catalogo() -> Dict:
    """Load catalogo_fontes.json"""
    with open(CATALOGO_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_catalogo(catalogo: Dict):
    """Save catalogo_fontes.json"""
    with open(CATALOGO_PATH, 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, indent=2, ensure_ascii=False)

def fetch_url_content(url: str) -> Optional[str]:
    """Fetch URL content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Mentor Agent Documentation Fetcher)'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

def html_to_markdown(html_content: str) -> str:
    """Convert HTML to Markdown"""
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = False
    h.ignore_emphasis = False
    h.body_width = 0  # Don't wrap lines
    return h.handle(html_content)

def extract_main_content(html_content: str) -> str:
    """Extract main content from HTML (remove nav, footer, etc)"""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Try to find main content area
    main_content = None

    # Common content selectors
    selectors = [
        'main',
        'article',
        '[role="main"]',
        '.main-content',
        '.content',
        '#content',
        '.documentation',
        '.doc-content'
    ]

    for selector in selectors:
        main_content = soup.select_one(selector)
        if main_content:
            break

    if not main_content:
        main_content = soup.body

    if main_content:
        # Remove unwanted elements
        for element in main_content.select('nav, footer, aside, .sidebar, .nav, .footer'):
            element.decompose()

        return str(main_content)

    return html_content

def process_documentation_url(url: str, output_path: Path) -> bool:
    """Fetch URL, convert to markdown, and save"""
    logger.info(f"  Fetching: {url}")

    html_content = fetch_url_content(url)
    if not html_content:
        return False

    # Extract main content
    main_content = extract_main_content(html_content)

    # Convert to markdown
    markdown_content = html_to_markdown(main_content)

    # Add metadata header
    header = f"""---
source: {url}
fetched: {datetime.now().isoformat()}
---

"""

    full_content = header + markdown_content

    # Save to file
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(full_content, encoding='utf-8')

    logger.info(f"  ✅ Saved to: {output_path}")
    return True

def refresh_fonte(fonte: Dict, catalogo: Dict) -> bool:
    """Refresh documentation for a fonte"""
    fonte_id = fonte['id']
    categoria = fonte['categoria']
    plataforma = fonte['plataforma']

    logger.info(f"\n🔄 Refreshing: {fonte_id}")
    logger.info(f"   Platform: {fonte['nome']}")

    # Determine output directory
    output_dir = FONTES_ROOT / categoria / plataforma

    # Process each specific URL
    urls_especificas = fonte.get('urls_especificas', {})
    success_count = 0
    total_count = len(urls_especificas)

    if total_count == 0:
        # Fallback to main URL
        main_url = fonte['url_oficial']
        output_file = output_dir / "index.md"
        if process_documentation_url(main_url, output_file):
            success_count += 1
        total_count = 1
    else:
        for topic, url in urls_especificas.items():
            output_file = output_dir / f"{topic}.md"
            if process_documentation_url(url, output_file):
                success_count += 1

    # Update catalogo
    if success_count > 0:
        # Find fonte in catalogo and update
        for i, f in enumerate(catalogo['fontes']):
            if f['id'] == fonte_id:
                catalogo['fontes'][i]['last_refresh'] = datetime.now().isoformat()
                break

        save_catalogo(catalogo)
        logger.info(f"✅ Successfully refreshed {success_count}/{total_count} documents")
        return True
    else:
        logger.error(f"❌ Failed to refresh {fonte_id}")
        return False

def create_index_file(fonte: Dict):
    """Create _index.json for the fonte directory"""
    categoria = fonte['categoria']
    plataforma = fonte['plataforma']
    output_dir = FONTES_ROOT / categoria / plataforma

    index_data = {
        "fonte_id": fonte['id'],
        "nome": fonte['nome'],
        "url_oficial": fonte['url_oficial'],
        "topics": fonte['topics'],
        "last_refresh": fonte.get('last_refresh'),
        "arquivos": []
    }

    # List all .md files in directory
    if output_dir.exists():
        for md_file in output_dir.glob("*.md"):
            index_data["arquivos"].append(md_file.name)

    index_file = output_dir / "_index.json"
    index_file.parent.mkdir(parents=True, exist_ok=True)

    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index_data, f, indent=2, ensure_ascii=False)

    logger.info(f"📝 Created index: {index_file}")

def main():
    parser = argparse.ArgumentParser(description='Refresh external documentation')
    parser.add_argument('--fonte', help='Refresh specific fonte by ID')
    parser.add_argument('--priority', choices=['critical', 'high', 'medium', 'low'],
                       help='Refresh fontes by priority')
    parser.add_argument('--all', action='store_true', help='Refresh all active fontes')

    args = parser.parse_args()

    catalogo = load_catalogo()
    fontes_to_refresh = []

    if args.fonte:
        fonte = next((f for f in catalogo['fontes'] if f['id'] == args.fonte), None)
        if fonte:
            fontes_to_refresh = [fonte]
        else:
            logger.error(f"Fonte '{args.fonte}' not found")
            return

    elif args.priority:
        fontes_to_refresh = [f for f in catalogo['fontes']
                            if f['priority'] == args.priority and f['status'] == 'active']

    elif args.all:
        fontes_to_refresh = [f for f in catalogo['fontes'] if f['status'] == 'active']

    else:
        logger.error("Please specify --fonte, --priority, or --all")
        return

    logger.info(f"🚀 Starting refresh of {len(fontes_to_refresh)} fontes...\n")

    success_count = 0
    for fonte in fontes_to_refresh:
        if refresh_fonte(fonte, catalogo):
            create_index_file(fonte)
            success_count += 1

    logger.info(f"\n✅ Refresh complete: {success_count}/{len(fontes_to_refresh)} successful")

if __name__ == '__main__':
    main()
