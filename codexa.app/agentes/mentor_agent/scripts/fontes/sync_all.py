#!/usr/bin/env python3
"""
Sync all external documentation sources.

Master script that:
1. Checks for updates
2. Refreshes fontes with detected updates
3. Validates all links
4. Generates report

Usage:
    python sync_all.py [--dry-run] [--force]
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path
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
SCRIPTS_DIR = Path(__file__).parent
CATALOGO_PATH = MENTOR_ROOT / "FONTES" / "catalogo_fontes.json"
REPORTS_DIR = MENTOR_ROOT / "outputs" / "fontes_reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def load_catalogo() -> dict:
    """Load catalogo_fontes.json"""
    with open(CATALOGO_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def run_check_updates(priority: str = None) -> dict:
    """Run check_updates.py and return results"""
    logger.info("🔍 Step 1: Checking for updates...")

    cmd = ["python", str(SCRIPTS_DIR / "check_updates.py"), "--all"]
    if priority:
        cmd = ["python", str(SCRIPTS_DIR / "check_updates.py"), "--priority", priority]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        logger.info(result.stdout)

        # Read updates file if exists
        updates_file = MENTOR_ROOT / "FONTES" / "updates_available.json"
        if updates_file.exists():
            with open(updates_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error checking updates: {e}")

    return {'updates': []}

def run_refresh_fonte(fonte_id: str) -> bool:
    """Run refresh_fonte.py for specific fonte"""
    logger.info(f"🔄 Refreshing: {fonte_id}")

    cmd = ["python", str(SCRIPTS_DIR / "refresh_fonte.py"), "--fonte", fonte_id]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        logger.info(result.stdout)
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error refreshing {fonte_id}: {e}")
        return False

def run_validate_links() -> dict:
    """Run validate_links.py and return results"""
    logger.info("✅ Step 3: Validating links...")

    cmd = ["python", str(SCRIPTS_DIR / "validate_links.py"), "--all"]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        logger.info(result.stdout)

        # Parse validation results (simplified)
        return {
            'validated': True,
            'output': result.stdout
        }
    except Exception as e:
        logger.error(f"Error validating links: {e}")
        return {'validated': False, 'error': str(e)}

def generate_sync_report(updates: dict, refreshed: list, validated: dict) -> Path:
    """Generate sync report"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = REPORTS_DIR / f"sync_report_{timestamp}.json"

    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total_updates_detected": len(updates.get('updates', [])),
            "total_refreshed": len(refreshed),
            "successful_refreshes": len([r for r in refreshed if r['success']]),
            "failed_refreshes": len([r for r in refreshed if not r['success']]),
            "links_validated": validated.get('validated', False)
        },
        "updates_detected": updates.get('updates', []),
        "refreshed_fontes": refreshed,
        "validation": validated
    }

    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Also create markdown report
    md_report_file = REPORTS_DIR / f"sync_report_{timestamp}.md"
    md_content = f"""# FONTES Sync Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

- 📊 Updates detected: {report['summary']['total_updates_detected']}
- 🔄 Fontes refreshed: {report['summary']['total_refreshed']}
- ✅ Successful: {report['summary']['successful_refreshes']}
- ❌ Failed: {report['summary']['failed_refreshes']}
- 🔗 Links validated: {'Yes' if report['summary']['links_validated'] else 'No'}

## Updates Detected

"""

    if updates.get('updates'):
        for update in updates['updates']:
            md_content += f"- **{update['fonte_id']}**: {update['message']}\n"
    else:
        md_content += "No updates detected.\n"

    md_content += "\n## Refreshed Fontes\n\n"

    if refreshed:
        for refresh in refreshed:
            status = "✅" if refresh['success'] else "❌"
            md_content += f"{status} **{refresh['fonte_id']}**\n"
    else:
        md_content += "No fontes refreshed.\n"

    md_report_file.write_text(md_content, encoding='utf-8')

    logger.info(f"\n📄 Report generated: {report_file}")
    logger.info(f"📄 Markdown report: {md_report_file}")

    return report_file

def main():
    parser = argparse.ArgumentParser(description='Sync all external documentation')
    parser.add_argument('--dry-run', action='store_true',
                       help='Check for updates but do not refresh')
    parser.add_argument('--force', action='store_true',
                       help='Force refresh all fontes regardless of updates')
    parser.add_argument('--priority', choices=['critical', 'high', 'medium', 'low'],
                       help='Sync only specific priority level')

    args = parser.parse_args()

    logger.info("🚀 Starting FONTES synchronization...\n")

    # Step 1: Check for updates
    updates = run_check_updates(priority=args.priority)

    if args.dry_run:
        logger.info("\n🔍 Dry run mode - stopping here")
        logger.info(f"Found {len(updates.get('updates', []))} updates")
        return

    # Step 2: Refresh fontes
    refreshed = []

    if args.force:
        # Force refresh all
        catalogo = load_catalogo()
        fontes_to_refresh = catalogo['fontes']
        if args.priority:
            fontes_to_refresh = [f for f in fontes_to_refresh
                               if f['priority'] == args.priority]

        logger.info(f"\n🔄 Force refreshing {len(fontes_to_refresh)} fontes...")

        for fonte in fontes_to_refresh:
            success = run_refresh_fonte(fonte['id'])
            refreshed.append({
                'fonte_id': fonte['id'],
                'success': success
            })

    else:
        # Refresh only updated fontes
        updates_list = updates.get('updates', [])

        if not updates_list:
            logger.info("\n✅ No updates to refresh")
        else:
            logger.info(f"\n🔄 Refreshing {len(updates_list)} updated fontes...")

            for update in updates_list:
                fonte_id = update['fonte_id']
                success = run_refresh_fonte(fonte_id)
                refreshed.append({
                    'fonte_id': fonte_id,
                    'success': success
                })

    # Step 3: Validate links (optional, if script exists)
    validated = {'validated': False}
    validate_script = SCRIPTS_DIR / "validate_links.py"
    if validate_script.exists():
        validated = run_validate_links()

    # Step 4: Generate report
    report_file = generate_sync_report(updates, refreshed, validated)

    logger.info("\n✅ Sync complete!")
    logger.info(f"📊 Full report: {report_file}")

if __name__ == '__main__':
    main()
