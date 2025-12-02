#!/usr/bin/env python3
"""
FONTES - Unified CLI for External Documentation Management

Single entry point for all FONTES operations:
- sync: Update all external documentation (check + refresh + validate)
- status: Show current state of all sources
- validate: Check health of all links

Usage:
    python scripts/fontes.py sync [--priority PRIORITY] [--dry-run]
    python scripts/fontes.py status [--show-pending]
    python scripts/fontes.py validate [--fix-broken]
"""

import sys
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import logging

# Optional dependencies (for refresh functionality)
try:
    import requests
    from bs4 import BeautifulSoup
    import html2text
    HAS_REFRESH_DEPS = True
except ImportError:
    HAS_REFRESH_DEPS = False
    requests = None
    BeautifulSoup = None
    html2text = None

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
MENTOR_ROOT = Path(__file__).parent.parent
CATALOGO_PATH = MENTOR_ROOT / "FONTES" / "catalogo_fontes.json"
CACHE_PATH = MENTOR_ROOT / "FONTES" / ".cache"
CACHE_PATH.mkdir(exist_ok=True)
REPORTS_DIR = MENTOR_ROOT / "outputs" / "fontes_reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================================
# CORE FUNCTIONS (consolidated from separate scripts)
# ============================================================================

def load_catalogo() -> Dict:
    """Load catalogo_fontes.json"""
    with open(CATALOGO_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_catalogo(catalogo: Dict):
    """Save catalogo_fontes.json"""
    with open(CATALOGO_PATH, 'w', encoding='utf-8') as f:
        json.dump(catalogo, f, indent=2, ensure_ascii=False)

def get_url_hash(url: str) -> Optional[str]:
    """Fetch URL and return content hash"""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        etag = response.headers.get('ETag')
        last_modified = response.headers.get('Last-Modified')

        if etag:
            return etag
        elif last_modified:
            return hashlib.md5(last_modified.encode()).hexdigest()
        else:
            response = requests.get(url, timeout=30)
            return hashlib.md5(response.content).hexdigest()
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None

def get_stored_hash(fonte_id: str) -> Optional[str]:
    """Get stored hash for fonte_id from cache"""
    cache_file = CACHE_PATH / f"{fonte_id}.hash"
    if cache_file.exists():
        return cache_file.read_text().strip()
    return None

def store_hash(fonte_id: str, hash_value: str):
    """Store hash for fonte_id in cache"""
    cache_file = CACHE_PATH / f"{fonte_id}.hash"
    cache_file.write_text(hash_value)

def check_updates(catalogo: Dict, priority: str = None) -> Dict:
    """Check for updates in external sources"""
    updates = []
    fontes_to_check = catalogo['fontes']

    if priority:
        fontes_to_check = [f for f in fontes_to_check if f['priority'] == priority]

    logger.info(f"🔍 Checking {len(fontes_to_check)} sources for updates...\n")

    for fonte in fontes_to_check:
        if fonte['status'] != 'active':
            continue

        fonte_id = fonte['id']
        url_oficial = fonte['url_oficial']

        logger.info(f"  Checking {fonte_id}...")

        current_hash = get_url_hash(url_oficial)
        if not current_hash:
            updates.append({
                'fonte_id': fonte_id,
                'status': 'error',
                'message': 'Failed to fetch URL'
            })
            continue

        stored_hash = get_stored_hash(fonte_id)

        if stored_hash is None:
            store_hash(fonte_id, current_hash)
            updates.append({
                'fonte_id': fonte_id,
                'status': 'new',
                'message': 'First check - baseline stored'
            })
        elif current_hash != stored_hash:
            updates.append({
                'fonte_id': fonte_id,
                'status': 'updated',
                'message': 'Update detected!',
                'old_hash': stored_hash,
                'new_hash': current_hash
            })
        else:
            updates.append({
                'fonte_id': fonte_id,
                'status': 'unchanged',
                'message': 'No changes detected'
            })

    return updates

def fetch_url_content(url: str) -> Optional[str]:
    """Fetch URL content"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Mentor Agent Documentation Fetcher)'}
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
    h.body_width = 0
    return h.handle(html_content)

def extract_main_content(html_content: str) -> str:
    """Extract main content from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')

    selectors = ['main', 'article', '[role="main"]', '.main-content', '.content', '#content']
    main_content = None

    for selector in selectors:
        main_content = soup.select_one(selector)
        if main_content:
            break

    if not main_content:
        main_content = soup.body

    if main_content:
        for element in main_content.select('nav, footer, aside, .sidebar'):
            element.decompose()
        return str(main_content)

    return html_content

def refresh_fonte(fonte: Dict, catalogo: Dict) -> bool:
    """Refresh documentation for a fonte"""
    fonte_id = fonte['id']
    categoria = fonte['categoria']
    plataforma = fonte['plataforma']

    logger.info(f"  🔄 Refreshing: {fonte_id}")

    output_dir = MENTOR_ROOT / "FONTES" / categoria / plataforma
    urls_especificas = fonte.get('urls_especificas', {})
    success_count = 0

    for topic, url in urls_especificas.items():
        html_content = fetch_url_content(url)
        if not html_content:
            continue

        main_content = extract_main_content(html_content)
        markdown_content = html_to_markdown(main_content)

        header = f"""---
source: {url}
fetched: {datetime.now().isoformat()}
---

"""
        full_content = header + markdown_content

        output_file = output_dir / f"{topic}.md"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(full_content, encoding='utf-8')

        success_count += 1

    if success_count > 0:
        # Update catalogo
        for i, f in enumerate(catalogo['fontes']):
            if f['id'] == fonte_id:
                catalogo['fontes'][i]['last_refresh'] = datetime.now().isoformat()
                break
        save_catalogo(catalogo)
        logger.info(f"    ✅ {success_count} files refreshed")
        return True

    return False

def validate_url(url: str) -> Dict:
    """Validate single URL"""
    result = {
        'url': url,
        'status': 'unknown',
        'accessible': False
    }

    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        result['status_code'] = response.status_code

        if 200 <= response.status_code < 400:
            result['status'] = 'ok'
            result['accessible'] = True
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)

    return result

def validate_fontes(catalogo: Dict) -> Dict:
    """Validate all URLs in catalogo"""
    results = []

    logger.info("🔗 Validating all source URLs...\n")

    for fonte in catalogo['fontes']:
        fonte_id = fonte['id']
        logger.info(f"  Checking {fonte_id}...")

        # Validate main URL
        main_result = validate_url(fonte['url_oficial'])

        fonte_results = {
            'fonte_id': fonte_id,
            'main_url_accessible': main_result['accessible'],
            'total_urls': 1,
            'accessible': 1 if main_result['accessible'] else 0
        }

        results.append(fonte_results)

    total_accessible = sum(r['accessible'] for r in results)
    total_urls = sum(r['total_urls'] for r in results)

    return {
        'results': results,
        'summary': {
            'total_fontes': len(results),
            'total_accessible': total_accessible,
            'total_urls': total_urls,
            'success_rate': round(total_accessible / total_urls * 100, 2) if total_urls > 0 else 0
        }
    }

# ============================================================================
# COMMANDS
# ============================================================================

def cmd_sync(args):
    """Sync all sources: check updates → refresh → validate"""
    if not HAS_REFRESH_DEPS:
        logger.error("❌ Missing dependencies!")
        logger.error("Run: pip install -r scripts/requirements.txt")
        logger.error("Required: requests, beautifulsoup4, html2text")
        sys.exit(1)

    logger.info("🚀 Starting FONTES synchronization...\n")

    catalogo = load_catalogo()
    priority = args.priority
    dry_run = args.dry_run

    # Step 1: Check for updates
    logger.info("=" * 60)
    logger.info("STEP 1: Checking for updates")
    logger.info("=" * 60)
    updates = check_updates(catalogo, priority=priority)

    updated_fontes = [u for u in updates if u['status'] == 'updated']
    logger.info(f"\n✅ Found {len(updated_fontes)} sources with updates")

    if dry_run:
        logger.info("\n🔍 Dry run mode - stopping here")
        for update in updated_fontes:
            logger.info(f"  - {update['fonte_id']}: {update['message']}")
        return

    # Step 2: Refresh updated sources
    if updated_fontes:
        logger.info("\n" + "=" * 60)
        logger.info("STEP 2: Refreshing updated sources")
        logger.info("=" * 60)

        refreshed = []
        for update in updated_fontes:
            fonte_id = update['fonte_id']
            fonte = next((f for f in catalogo['fontes'] if f['id'] == fonte_id), None)

            if fonte:
                success = refresh_fonte(fonte, catalogo)
                refreshed.append({'fonte_id': fonte_id, 'success': success})

        logger.info(f"\n✅ Refreshed {len([r for r in refreshed if r['success']])} sources")
    else:
        logger.info("\n✅ All sources up to date - no refresh needed")

    # Step 3: Validate (quick check)
    logger.info("\n" + "=" * 60)
    logger.info("STEP 3: Validating source URLs")
    logger.info("=" * 60)
    validation = validate_fontes(catalogo)

    logger.info(f"\n✅ Validation: {validation['summary']['success_rate']}% URLs accessible")

    # Generate report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"sync_report_{timestamp}.md"

    report_content = f"""# FONTES Sync Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

- 🔍 Updates detected: {len(updated_fontes)}
- 🔄 Sources refreshed: {len([r for r in refreshed if r['success']]) if updated_fontes else 0}
- ✅ URLs accessible: {validation['summary']['total_accessible']}/{validation['summary']['total_urls']} ({validation['summary']['success_rate']}%)

## Status

"""

    if updated_fontes:
        report_content += "### Updated Sources\n\n"
        for update in updated_fontes:
            report_content += f"- ✅ {update['fonte_id']}\n"
    else:
        report_content += "All sources are up to date.\n"

    report_file.write_text(report_content, encoding='utf-8')

    logger.info(f"\n📄 Report saved: {report_file}")
    logger.info("\n✅ Sync complete!")

def cmd_status(args):
    """Show current status of all sources"""
    catalogo = load_catalogo()

    logger.info("📊 FONTES Status\n")
    logger.info("=" * 80)

    # Group by category
    by_category = {}
    for fonte in catalogo['fontes']:
        cat = fonte['categoria']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(fonte)

    # Display by category
    for categoria, fontes in by_category.items():
        logger.info(f"\n📂 {categoria}")
        logger.info("-" * 80)

        for fonte in fontes:
            fonte_id = fonte['id']
            priority = fonte['priority']
            status = fonte['status']
            last_refresh = fonte.get('last_refresh', 'Never')

            if last_refresh and last_refresh != 'Never':
                try:
                    last_refresh_date = datetime.fromisoformat(last_refresh)
                    days_ago = (datetime.now() - last_refresh_date).days
                    last_refresh = f"{days_ago} days ago"
                except (ValueError, TypeError):
                    last_refresh = 'Invalid date'
            else:
                last_refresh = 'Never'

            status_icon = "✅" if status == 'active' else "⏸️"
            priority_icon = {"critical": "🔴", "high": "🟡", "medium": "🔵", "low": "⚪"}.get(priority, "⚪")

            logger.info(f"  {status_icon} {priority_icon} {fonte_id:30s} | Last refresh: {last_refresh}")

    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("📈 Summary")
    logger.info("-" * 80)

    total = len(catalogo['fontes'])
    active = len([f for f in catalogo['fontes'] if f['status'] == 'active'])
    by_priority = {}
    for fonte in catalogo['fontes']:
        p = fonte['priority']
        by_priority[p] = by_priority.get(p, 0) + 1

    logger.info(f"  Total sources: {total}")
    logger.info(f"  Active: {active}")
    logger.info(f"  By priority:")
    for priority in ['critical', 'high', 'medium', 'low']:
        count = by_priority.get(priority, 0)
        logger.info(f"    - {priority.capitalize()}: {count}")

    # Show pending updates if requested
    if args.show_pending:
        logger.info("\n🔍 Checking for pending updates...")
        updates = check_updates(catalogo)
        pending = [u for u in updates if u['status'] == 'updated']

        if pending:
            logger.info(f"\n⚠️  {len(pending)} sources have pending updates:")
            for update in pending:
                logger.info(f"  - {update['fonte_id']}")
        else:
            logger.info("\n✅ All sources are up to date")

def cmd_validate(args):
    """Validate health of all source URLs"""
    catalogo = load_catalogo()
    validation = validate_fontes(catalogo)

    summary = validation['summary']

    logger.info("\n" + "=" * 80)
    logger.info("📊 Validation Summary")
    logger.info("=" * 80)
    logger.info(f"  Total fontes: {summary['total_fontes']}")
    logger.info(f"  Total URLs: {summary['total_urls']}")
    logger.info(f"  Accessible: {summary['total_accessible']}")
    logger.info(f"  Success rate: {summary['success_rate']}%")

    # Show broken links
    broken = [r for r in validation['results'] if not r['main_url_accessible']]

    if broken:
        logger.info(f"\n⚠️  {len(broken)} sources have accessibility issues:")
        for result in broken:
            logger.info(f"  - {result['fonte_id']}")
    else:
        logger.info("\n✅ All sources are accessible")

    # Generate report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"validation_report_{timestamp}.md"

    report_content = f"""# FONTES Validation Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

- Total fontes: {summary['total_fontes']}
- Total URLs: {summary['total_urls']}
- Accessible: {summary['total_accessible']}
- Success rate: {summary['success_rate']}%

"""

    if broken:
        report_content += "\n## Issues Found\n\n"
        for result in broken:
            report_content += f"- ❌ {result['fonte_id']}\n"
    else:
        report_content += "\n✅ All sources are accessible.\n"

    report_file.write_text(report_content, encoding='utf-8')
    logger.info(f"\n📄 Report saved: {report_file}")

# ============================================================================
# MAIN CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='FONTES - Unified CLI for External Documentation Management',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/fontes.py sync                 # Sync all sources
  python scripts/fontes.py sync --priority critical --dry-run
  python scripts/fontes.py status               # Show current status
  python scripts/fontes.py status --show-pending
  python scripts/fontes.py validate             # Validate all URLs
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to execute')

    # Sync command
    sync_parser = subparsers.add_parser('sync', help='Sync external documentation (check + refresh + validate)')
    sync_parser.add_argument('--priority', choices=['critical', 'high', 'medium', 'low'],
                            help='Only sync specific priority level')
    sync_parser.add_argument('--dry-run', action='store_true',
                            help='Check for updates but do not refresh')

    # Status command
    status_parser = subparsers.add_parser('status', help='Show current status of all sources')
    status_parser.add_argument('--show-pending', action='store_true',
                              help='Check and show pending updates')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate health of all source URLs')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == 'sync':
        cmd_sync(args)
    elif args.command == 'status':
        cmd_status(args)
    elif args.command == 'validate':
        cmd_validate(args)

if __name__ == '__main__':
    main()
