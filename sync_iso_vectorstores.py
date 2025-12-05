#!/usr/bin/env python3
"""
ADW-300 Knowledge Hydration - Batch Sync iso_vectorstores
Syncs source files (PRIME, README, INSTRUCTIONS) to iso_vectorstore/ for all agents
"""

import os
import re
from pathlib import Path
from datetime import datetime

# Configuration
AGENTS_DIR = Path("codexa.app/agentes")
SYNC_DATE = "2025-12-05"

# Agents to sync with expected versions
AGENTS_TO_SYNC = {
    "voice_agent": "7.0.0",  # Already synced manually
    "pesquisa_agent": "3.2.0",  # Source shows 3.2.0
    "video_agent": "3.0.0",
    "photo_agent": "2.6.0",
    "marca_agent": "3.1.0",
    "mentor_agent": "2.6.0",
    "curso_agent": "2.5.1",
    "scout_agent": "1.1.0",
    "anuncio_agent": "3.2.0",  # Verify only
}

# File mapping: source_file -> iso_vectorstore_file
FILE_MAPPINGS = {
    "PRIME.md": "02_PRIME.md",
    "INSTRUCTIONS.md": "03_INSTRUCTIONS.md",
    "README.md": "04_README.md",
}

def extract_version(content):
    """Extract version from content"""
    patterns = [
        r'\*\*Version\*\*:\s*(\d+\.\d+(?:\.\d+)?)',
        r'Version:\s*(\d+\.\d+(?:\.\d+)?)',
        r'v(\d+\.\d+(?:\.\d+)?)',
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return None

def create_iso_header(agent_name, source_file, version):
    """Create ISO_VECTORSTORE header"""
    return f"""<!--
ISO_VECTORSTORE EXPORT
Source: {agent_name}/{source_file}
Synced: {SYNC_DATE}
Version: {version}
-->

"""

def sync_file(agent_path, source_file, iso_file, version):
    """Sync a single file"""
    source_path = agent_path / source_file
    iso_path = agent_path / "iso_vectorstore" / iso_file

    if not source_path.exists():
        return f"SKIP: {source_path} not found"

    if not iso_path.parent.exists():
        return f"SKIP: {iso_path.parent} not found"

    # Read source
    with open(source_path, 'r', encoding='utf-8') as f:
        source_content = f.read()

    # Read existing iso file
    if iso_path.exists():
        with open(iso_path, 'r', encoding='utf-8') as f:
            iso_content = f.read()

        # Check if already synced with same version
        if f"Version: {version}" in iso_content and f"Synced: {SYNC_DATE}" in iso_content:
            return f"OK: Already synced {iso_file} (v{version})"

    # Remove old header if exists
    if source_content.startswith('<!--'):
        # Find end of comment
        end_idx = source_content.find('-->')
        if end_idx != -1:
            # Skip the comment and any following newlines
            content = source_content[end_idx + 3:].lstrip('\n')
        else:
            content = source_content
    else:
        content = source_content

    # Create new content with ISO header
    new_content = create_iso_header(agent_path.name, source_file, version) + content

    # Write to iso_vectorstore
    with open(iso_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_content)

    return f"UPDATED: {iso_file} (v{version})"

def sync_agent(agent_name, expected_version):
    """Sync all files for one agent"""
    agent_path = AGENTS_DIR / agent_name

    if not agent_path.exists():
        return [f"ERROR: {agent_path} not found"]

    results = [f"\n=== {agent_name} (v{expected_version}) ==="]

    for source_file, iso_file in FILE_MAPPINGS.items():
        result = sync_file(agent_path, source_file, iso_file, expected_version)
        results.append(f"  {result}")

    return results

def main():
    """Main sync function"""
    print(f"ADW-300 Knowledge Hydration - Batch Sync")
    print(f"Sync Date: {SYNC_DATE}")
    print(f"Agents: {len(AGENTS_TO_SYNC)}")
    print("=" * 60)

    all_results = []
    stats = {"updated": 0, "skipped": 0, "ok": 0, "errors": 0}

    for agent_name, version in AGENTS_TO_SYNC.items():
        results = sync_agent(agent_name, version)
        all_results.extend(results)

        # Count stats
        for result in results:
            if "UPDATED:" in result:
                stats["updated"] += 1
            elif "SKIP:" in result:
                stats["skipped"] += 1
            elif "OK:" in result:
                stats["ok"] += 1
            elif "ERROR:" in result:
                stats["errors"] += 1

    # Print results
    for result in all_results:
        print(result)

    print("\n" + "=" * 60)
    print("SUMMARY:")
    print(f"  Updated: {stats['updated']}")
    print(f"  Already synced: {stats['ok']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Total files processed: {sum(stats.values())}")

if __name__ == "__main__":
    main()
