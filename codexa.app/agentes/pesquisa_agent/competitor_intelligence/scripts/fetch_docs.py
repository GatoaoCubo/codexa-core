#!/usr/bin/env python3
"""
Competitor Intelligence Documentation Fetcher
Fetches and processes documentation from competitor sources.

Usage:
    python fetch_docs.py --category ai_courses --force-refresh
    python fetch_docs.py --source sebrae --verbose
    python fetch_docs.py --all
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import hashlib

# Add parent directory to path for imports
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
SOURCES_DIR = ROOT_DIR / "sources"
DOCS_DIR = ROOT_DIR / "docs"
SNAPSHOTS_DIR = ROOT_DIR / "snapshots"


class CompetitorDocsFetcher:
    """Fetches and manages competitor documentation."""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        self.snapshot_dir = SNAPSHOTS_DIR / datetime.now().strftime("%Y-%m-%d")
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)

    def log(self, message: str, level: str = "INFO"):
        """Log message if verbose mode is enabled."""
        if self.verbose or level == "ERROR":
            print(f"[{level}] {message}")

    def load_sources(self, category: str) -> Dict:
        """Load source URLs from JSON file."""
        source_file = SOURCES_DIR / f"{category}.json"
        if not source_file.exists():
            self.log(f"Source file not found: {source_file}", "ERROR")
            return {}

        with open(source_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def fetch_url_content(self, url: str, name: str) -> Optional[str]:
        """
        Fetch content from URL.
        NOTE: This is a placeholder. In Claude Code, use WebFetch tool.
        In production, use requests library or similar.
        """
        self.log(f"Fetching: {url}")

        # Placeholder - In real implementation, this would:
        # 1. Use WebFetch tool in Claude Code environment
        # 2. Use requests library in standalone Python
        # 3. Handle rate limiting, retries, errors

        return f"# {name}\n\nURL: {url}\n\nContent would be fetched here.\n\nTimestamp: {self.timestamp}"

    def save_doc(self, category: str, source_name: str, content: str, metadata: Dict):
        """Save fetched documentation to file."""
        # Save to main docs directory
        doc_dir = DOCS_DIR / category / source_name
        doc_dir.mkdir(parents=True, exist_ok=True)

        doc_file = doc_dir / f"overview_{self.timestamp}.md"
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # Save latest version link
        latest_file = doc_dir / "latest.md"
        with open(latest_file, 'w', encoding='utf-8') as f:
            f.write(content)

        # Save metadata
        meta_file = doc_dir / f"metadata_{self.timestamp}.json"
        metadata['fetched_at'] = self.timestamp
        metadata['content_hash'] = hashlib.md5(content.encode()).hexdigest()

        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)

        # Copy to snapshot directory
        snapshot_file = self.snapshot_dir / f"{category}_{source_name}_{self.timestamp}.md"
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            f.write(content)

        self.log(f"Saved: {doc_file}")
        return doc_file

    def fetch_category(self, category: str, force_refresh: bool = False):
        """Fetch all sources for a category."""
        self.log(f"\n=== Fetching category: {category} ===")

        sources = self.load_sources(category)
        if not sources:
            return

        # Determine which key contains the source data
        # (e.g., 'platforms', 'marketplaces', 'news_portals', etc.)
        source_keys = [k for k in sources.keys() if k not in ['metadata', 'tracking', 'cross_references', 'best_practices']]

        fetched_count = 0
        for source_group_key in source_keys:
            source_group = sources[source_group_key]

            for source_name, source_data in source_group.items():
                if not isinstance(source_data, dict) or 'urls' not in source_data:
                    continue

                self.log(f"\nProcessing: {source_data.get('name', source_name)}")

                # Fetch main URL or first available URL
                urls = source_data['urls']
                main_url = urls.get('main') or urls.get('main_course') or urls.get('main_site') or list(urls.values())[0]

                content = self.fetch_url_content(main_url, source_data.get('name', source_name))

                if content:
                    metadata = {
                        'source_name': source_data.get('name', source_name),
                        'category': category,
                        'priority': source_data.get('priority', 'medium'),
                        'urls': urls,
                        'monitoring': source_data.get('monitoring', {}),
                        'metrics': source_data.get('metrics', {})
                    }

                    self.save_doc(category, source_name, content, metadata)
                    fetched_count += 1

        self.log(f"\n=== Completed: {fetched_count} sources fetched ===")

    def fetch_all(self, force_refresh: bool = False):
        """Fetch all categories."""
        categories = [
            'ai_courses_platforms',
            'marketplaces_docs',
            'ecommerce_trends',
            'compliance_sources'
        ]

        for category in categories:
            self.fetch_category(category, force_refresh)

    def generate_index(self):
        """Generate index of all fetched documentation."""
        index = {
            'generated_at': self.timestamp,
            'categories': {}
        }

        for category_dir in DOCS_DIR.iterdir():
            if not category_dir.is_dir():
                continue

            category_name = category_dir.name
            index['categories'][category_name] = []

            for source_dir in category_dir.iterdir():
                if not source_dir.is_dir():
                    continue

                latest_file = source_dir / "latest.md"
                if latest_file.exists():
                    # Find most recent metadata
                    meta_files = sorted(source_dir.glob("metadata_*.json"))
                    if meta_files:
                        with open(meta_files[-1], 'r', encoding='utf-8') as f:
                            metadata = json.load(f)

                        index['categories'][category_name].append({
                            'source': source_dir.name,
                            'latest_doc': str(latest_file),
                            'last_updated': metadata.get('fetched_at'),
                            'content_hash': metadata.get('content_hash')
                        })

        index_file = ROOT_DIR / f"docs_index_{self.timestamp}.json"
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

        # Also save as latest
        latest_index = ROOT_DIR / "docs_index_latest.json"
        with open(latest_index, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)

        self.log(f"\nIndex generated: {index_file}")
        return index_file


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Fetch competitor intelligence documentation')
    parser.add_argument('--category', help='Specific category to fetch')
    parser.add_argument('--source', help='Specific source to fetch')
    parser.add_argument('--all', action='store_true', help='Fetch all categories')
    parser.add_argument('--force-refresh', action='store_true', help='Force refresh even if recently fetched')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--generate-index', action='store_true', help='Generate documentation index')

    args = parser.parse_args()

    fetcher = CompetitorDocsFetcher(verbose=args.verbose)

    if args.generate_index:
        fetcher.generate_index()
        return

    if args.all:
        fetcher.fetch_all(force_refresh=args.force_refresh)
    elif args.category:
        fetcher.fetch_category(args.category, force_refresh=args.force_refresh)
    else:
        parser.print_help()
        return

    # Generate index after fetching
    fetcher.generate_index()


if __name__ == "__main__":
    main()
