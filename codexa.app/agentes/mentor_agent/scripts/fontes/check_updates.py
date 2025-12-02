#!/usr/bin/env python3
"""
Check for updates in external documentation sources.

This script checks if external documentation has been updated by:
1. Fetching URL headers (Last-Modified, ETag)
2. Comparing with stored hashes
3. Logging changes detected
4. Notifying when updates are available

Usage:
    python check_updates.py [--fonte FONTE_ID] [--priority PRIORITY] [--all]
"""

import json
import hashlib
import requests
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Paths
MENTOR_ROOT = Path(__file__).parent.parent.parent
CATALOGO_PATH = MENTOR_ROOT / "FONTES" / "catalogo_fontes.json"
CACHE_PATH = MENTOR_ROOT / "FONTES" / ".cache"
CACHE_PATH.mkdir(exist_ok=True)

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

        # Try to get Last-Modified or ETag
        last_modified = response.headers.get('Last-Modified')
        etag = response.headers.get('ETag')

        if etag:
            return etag
        elif last_modified:
            return hashlib.md5(last_modified.encode()).hexdigest()
        else:
            # Fallback: fetch full content and hash it
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

def should_check_fonte(fonte: Dict) -> bool:
    """Determine if fonte should be checked based on refresh schedule"""
    if fonte['status'] != 'active':
        return False

    last_refresh = fonte.get('last_refresh')
    if not last_refresh:
        return True  # Never refreshed, should check

    last_refresh_date = datetime.fromisoformat(last_refresh)
    now = datetime.now()

    frequency = fonte['refresh_frequency']
    if frequency == 'weekly':
        return (now - last_refresh_date).days >= 7
    elif frequency == 'bi-weekly':
        return (now - last_refresh_date).days >= 14
    elif frequency == 'monthly':
        return (now - last_refresh_date).days >= 30
    elif frequency == 'quarterly':
        return (now - last_refresh_date).days >= 90

    return True

def check_fonte_updates(fonte: Dict) -> Dict:
    """Check if fonte has updates available"""
    fonte_id = fonte['id']
    url_oficial = fonte['url_oficial']

    logger.info(f"Checking {fonte_id} ({url_oficial})...")

    current_hash = get_url_hash(url_oficial)
    if not current_hash:
        return {
            'fonte_id': fonte_id,
            'status': 'error',
            'message': 'Failed to fetch URL'
        }

    stored_hash = get_stored_hash(fonte_id)

    if stored_hash is None:
        # First time checking
        store_hash(fonte_id, current_hash)
        return {
            'fonte_id': fonte_id,
            'status': 'new',
            'message': 'First check - baseline stored'
        }

    if current_hash != stored_hash:
        return {
            'fonte_id': fonte_id,
            'status': 'updated',
            'message': 'Update detected!',
            'old_hash': stored_hash,
            'new_hash': current_hash
        }

    return {
        'fonte_id': fonte_id,
        'status': 'unchanged',
        'message': 'No changes detected'
    }

def notify_updates(updates: List[Dict]):
    """Notify about detected updates"""
    updated_fontes = [u for u in updates if u['status'] == 'updated']

    if not updated_fontes:
        logger.info("✅ No updates detected")
        return

    logger.info(f"\n🚨 {len(updated_fontes)} UPDATES DETECTED:\n")

    for update in updated_fontes:
        logger.info(f"  📢 {update['fonte_id']}: {update['message']}")

    # Write to notification file
    notification_file = MENTOR_ROOT / "FONTES" / "updates_available.json"
    with open(notification_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'updates': updated_fontes
        }, f, indent=2, ensure_ascii=False)

    logger.info(f"\n📝 Notification saved to: {notification_file}")

def main():
    parser = argparse.ArgumentParser(description='Check for documentation updates')
    parser.add_argument('--fonte', help='Check specific fonte by ID')
    parser.add_argument('--priority', choices=['critical', 'high', 'medium', 'low'],
                       help='Check fontes by priority')
    parser.add_argument('--all', action='store_true', help='Check all fontes')
    parser.add_argument('--force', action='store_true',
                       help='Force check regardless of schedule')

    args = parser.parse_args()

    catalogo = load_catalogo()
    fontes_to_check = []

    if args.fonte:
        # Check specific fonte
        fonte = next((f for f in catalogo['fontes'] if f['id'] == args.fonte), None)
        if fonte:
            fontes_to_check = [fonte]
        else:
            logger.error(f"Fonte '{args.fonte}' not found")
            return

    elif args.priority:
        # Check by priority
        fontes_to_check = [f for f in catalogo['fontes']
                          if f['priority'] == args.priority]

    elif args.all:
        # Check all active fontes
        fontes_to_check = [f for f in catalogo['fontes'] if f['status'] == 'active']

    else:
        # Default: check fontes due for refresh
        fontes_to_check = [f for f in catalogo['fontes'] if should_check_fonte(f)]

    if not fontes_to_check:
        logger.info("No fontes to check")
        return

    logger.info(f"Checking {len(fontes_to_check)} fontes...\n")

    updates = []
    for fonte in fontes_to_check:
        if args.force or should_check_fonte(fonte):
            result = check_fonte_updates(fonte)
            updates.append(result)

    notify_updates(updates)

    # Summary
    logger.info(f"\n📊 SUMMARY:")
    logger.info(f"  Total checked: {len(updates)}")
    logger.info(f"  Updated: {len([u for u in updates if u['status'] == 'updated'])}")
    logger.info(f"  Unchanged: {len([u for u in updates if u['status'] == 'unchanged'])}")
    logger.info(f"  Errors: {len([u for u in updates if u['status'] == 'error'])}")

if __name__ == '__main__':
    main()
