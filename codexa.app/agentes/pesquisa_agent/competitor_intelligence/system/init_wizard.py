#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meta System Initialization Wizard
Interactive setup for user-driven configuration.

Philosophy: Ask, don't assume. Learn from user context.
"""

import json
import os
import sys
import io
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Fix Windows console encoding for UTF-8
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, io.UnsupportedOperation):
        pass  # Already wrapped or not supported


class InitWizard:
    """Interactive wizard for initializing meta-configuration."""

    def __init__(self, meta_dir: Optional[Path] = None):
        self.meta_dir = meta_dir or Path(__file__).parent
        self.root_dir = self.meta_dir.parent
        self.config = {}

    def run(self):
        """Run the complete initialization wizard."""
        print("\n" + "="*70)
        print("  🚀 COMPETITOR INTELLIGENCE - META SYSTEM INITIALIZATION")
        print("="*70 + "\n")

        print("This wizard will help you configure your competitive intelligence system")
        print("based on YOUR specific needs and context.\n")

        print("Philosophy: We leave values intentionally blank ({NULL}) so YOU decide")
        print("what matters for your project. No assumptions, just flexibility.\n")

        input("Press ENTER to begin...")

        # Collect configuration
        self._project_info()
        self._categories_setup()
        self._preferences_setup()
        self._integrations_setup()

        # Save configuration
        self._save_configuration()

        print("\n" + "="*70)
        print("  ✅ INITIALIZATION COMPLETE!")
        print("="*70 + "\n")

        self._show_next_steps()

    def _project_info(self):
        """Collect basic project information."""
        print("\n" + "-"*70)
        print("  📋 PROJECT INFORMATION")
        print("-"*70 + "\n")

        self.config['project'] = {}

        # Project name
        name = input("Project name (e.g., 'AI Courses Tracker', 'SaaS Intelligence'): ").strip()
        self.config['project']['name'] = name or "Competitor Intelligence"

        # Domain
        print("\nWhat domain are you tracking?")
        print("  1. AI Courses / Training")
        print("  2. SaaS Tools")
        print("  3. E-commerce Platforms")
        print("  4. Marketplaces")
        print("  5. Other (specify)")

        domain_choice = input("\nChoose [1-5]: ").strip()
        domain_map = {
            "1": "ai_courses",
            "2": "saas_tools",
            "3": "ecommerce_platforms",
            "4": "marketplaces",
            "5": input("  Specify domain: ").strip()
        }
        self.config['project']['domain'] = domain_map.get(domain_choice, "custom")

        # Market
        print("\nTarget market?")
        print("  1. Brazil")
        print("  2. LATAM")
        print("  3. Global")
        print("  4. Other (specify)")

        market_choice = input("\nChoose [1-4]: ").strip()
        market_map = {
            "1": "brazil",
            "2": "latam",
            "3": "global",
            "4": input("  Specify market: ").strip()
        }
        self.config['project']['market'] = market_map.get(market_choice, "custom")

        # Language
        print("\nPrimary language?")
        print("  1. Portuguese (Brazil)")
        print("  2. Spanish")
        print("  3. English")
        print("  4. Other (specify)")

        lang_choice = input("\nChoose [1-4]: ").strip()
        lang_map = {
            "1": "pt-BR",
            "2": "es",
            "3": "en-US",
            "4": input("  Specify language code (e.g., fr-FR): ").strip()
        }
        self.config['project']['language'] = lang_map.get(lang_choice, "en-US")

        self.config['project']['created'] = datetime.now().isoformat()

        print(f"\n✓ Project configured: {self.config['project']['name']}")

    def _categories_setup(self):
        """Setup categories to track."""
        print("\n" + "-"*70)
        print("  📊 CATEGORIES SETUP")
        print("-"*70 + "\n")

        print("Categories help organize different types of sources you want to track.")
        print("Examples: 'competitors', 'marketplaces', 'news_sources', 'regulations'\n")

        self.config['categories'] = {}

        while True:
            add = input("Add a category? [y/N]: ").strip().lower()
            if add != 'y':
                break

            cat_id = input("  Category ID (lowercase, underscores): ").strip()
            if not cat_id:
                continue

            cat_name = input("  Display name: ").strip()
            cat_desc = input("  Description (optional): ").strip()

            print("\n  Update frequency?")
            print("    1. Daily")
            print("    2. Weekly")
            print("    3. Monthly")
            print("    4. On-demand")
            freq_choice = input("  Choose [1-4]: ").strip()
            freq_map = {"1": "daily", "2": "weekly", "3": "monthly", "4": "on_demand"}
            freq = freq_map.get(freq_choice, "weekly")

            self.config['categories'][cat_id] = {
                "id": cat_id,
                "name": cat_name or cat_id.replace('_', ' ').title(),
                "description": cat_desc,
                "update_frequency": freq,
                "enabled": True,
                "sources": {}
            }

            print(f"  ✓ Category '{cat_name}' added\n")

        if not self.config['categories']:
            print("  ℹ️  No categories added. You can add them later manually.\n")

    def _preferences_setup(self):
        """Setup user preferences."""
        print("\n" + "-"*70)
        print("  ⚙️  PREFERENCES")
        print("-"*70 + "\n")

        self.config['preferences'] = {}

        # Output format
        print("Preferred output format?")
        print("  1. Markdown only")
        print("  2. JSON only")
        print("  3. Both")
        format_choice = input("\nChoose [1-3]: ").strip()
        format_map = {"1": "markdown", "2": "json", "3": "both"}
        self.config['preferences']['output_format'] = format_map.get(format_choice, "markdown")

        # Report detail
        print("\nReport detail level?")
        print("  1. Summary (key insights only)")
        print("  2. Standard (balanced)")
        print("  3. Detailed (comprehensive)")
        detail_choice = input("\nChoose [1-3]: ").strip()
        detail_map = {"1": "summary", "2": "standard", "3": "detailed"}
        self.config['preferences']['report_detail_level'] = detail_map.get(detail_choice, "standard")

        # Snapshot retention
        retention = input("\nSnapshot retention days [default: 90]: ").strip()
        self.config['preferences']['snapshot_retention_days'] = int(retention) if retention else 90

        print("\n✓ Preferences configured")

    def _integrations_setup(self):
        """Setup integrations."""
        print("\n" + "-"*70)
        print("  🔌 INTEGRATIONS")
        print("-"*70 + "\n")

        self.config['integrations'] = {}

        # Alerts
        print("Enable alerts?")
        alerts = input("  [y/N]: ").strip().lower() == 'y'

        if alerts:
            print("\n  Alert channels:")
            print("    1. Email")
            print("    2. Slack")
            print("    3. Discord")
            print("    4. None (just logs)")
            channel_choice = input("  Choose [1-4]: ").strip()
            channel_map = {"1": "email", "2": "slack", "3": "discord", "4": "none"}
            channel = channel_map.get(channel_choice, "none")

            self.config['integrations']['alerts'] = {
                "enabled": True,
                "channels": [channel] if channel != "none" else []
            }
        else:
            self.config['integrations']['alerts'] = {"enabled": False, "channels": []}

        print("\n✓ Integrations configured")

    def _save_configuration(self):
        """Save configuration to user_context."""
        print("\n" + "-"*70)
        print("  💾 SAVING CONFIGURATION")
        print("-"*70 + "\n")

        user_context_dir = self.meta_dir / "user_context"
        user_context_dir.mkdir(exist_ok=True)

        # Save main config
        config_file = user_context_dir / "user_config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

        print(f"✓ Configuration saved: {config_file}")

        # Create categories files
        if self.config.get('categories'):
            for cat_id, cat_data in self.config['categories'].items():
                cat_file = self.root_dir / "sources" / f"{cat_id}.json"
                if not cat_file.exists():
                    # Create from template
                    template = {
                        "metadata": {
                            "category": cat_data['name'],
                            "market": self.config['project']['market'],
                            "last_updated": datetime.now().strftime('%Y-%m-%d'),
                            "total_sources": 0,
                            "update_frequency": cat_data['update_frequency']
                        },
                        "sources": {}
                    }
                    with open(cat_file, 'w', encoding='utf-8') as f:
                        json.dump(template, f, indent=2, ensure_ascii=False)

                    print(f"✓ Category file created: {cat_file}")

    def _show_next_steps(self):
        """Show next steps to user."""
        print("Next steps:\n")
        print("1. Add sources to your categories:")
        print(f"   python {system}/init_wizard.py --add-source\n")

        print("2. Or edit source files directly:")
        for cat_id in self.config.get('categories', {}).keys():
            print(f"   sources/{cat_id}.json")
        print()

        print("3. Run your first update:")
        print("   python system/executor.py --workflow quick_update\n")

        print("4. Read documentation:")
        print("   system/README.md\n")

        print("Enjoy your flexible, user-driven competitor intelligence system! 🚀\n")


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description='Initialize meta-configuration')
    parser.add_argument('--add-source', action='store_true',
                       help='Add source to existing category')

    args = parser.parse_args()

    wizard = InitWizard()

    if args.add_source:
        print("Adding source feature coming soon!")
    else:
        wizard.run()


if __name__ == "__main__":
    main()
