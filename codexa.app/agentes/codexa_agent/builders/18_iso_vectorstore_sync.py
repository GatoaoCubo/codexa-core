#!/usr/bin/env python3
"""
18_iso_vectorstore_sync.py | ISO Vectorstore Synchronization Builder

Synchronizes source files from agent root to iso_vectorstore/ export package.
Designed to run as pre-commit hook for automatic sync on every commit.

Architecture:
    {agent}/
    ├── PRIME.md              ← SOURCE (active development)
    ├── INSTRUCTIONS.md       ← SOURCE
    ├── README.md             ← SOURCE
    ├── ARCHITECTURE.md       ← SOURCE (if exists)
    ├── config/               ← SOURCE
    ├── workflows/            ← SOURCE
    ├── prompts/              ← SOURCE
    │
    └── iso_vectorstore/      ★ EXPORT PACKAGE (auto-synced) ★
        ├── 01_QUICK_START.md
        ├── 02_PRIME.md           ← Copy of PRIME.md
        ├── 03_INSTRUCTIONS.md    ← Copy of INSTRUCTIONS.md
        ├── 04_README.md          ← Copy of README.md
        ├── 05_ARCHITECTURE.md
        ├── 06_input_schema.json
        ├── 07_output_template.md
        ├── 08-10_*.json          ← From config/
        ├── 11_ADW_orchestrator.md ← From workflows/
        ├── 12_execution_plans.json
        ├── 13-19_HOP_*.md        ← From prompts/
        └── 20_CHANGELOG.md

Usage:
    # Sync all agents
    python builders/18_iso_vectorstore_sync.py

    # Sync specific agent
    python builders/18_iso_vectorstore_sync.py --agent anuncio_agent

    # Dry run (preview changes)
    python builders/18_iso_vectorstore_sync.py --dry-run

    # Pre-commit hook mode (only changed files)
    python builders/18_iso_vectorstore_sync.py --pre-commit

    # Verbose output
    python builders/18_iso_vectorstore_sync.py --verbose

Version: 1.0.0
Created: 2025-11-30
Purpose: Auto-sync source → iso_vectorstore on commit
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# === CONFIGURATION ===

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from config.paths import AGENTS_ROOT, CODEXA_AGENT_ROOT
except ImportError:
    # Fallback
    SCRIPT_DIR = Path(__file__).parent.resolve()
    CODEXA_AGENT_ROOT = SCRIPT_DIR.parent
    AGENTS_ROOT = CODEXA_AGENT_ROOT.parent

# File mapping: source → iso_vectorstore destination
FILE_MAPPING = {
    # Core docs (direct copy)
    'PRIME.md': '02_PRIME.md',
    'INSTRUCTIONS.md': '03_INSTRUCTIONS.md',
    'README.md': '04_README.md',
    'ARCHITECTURE.md': '05_ARCHITECTURE.md',
    'CHANGELOG.md': '20_CHANGELOG.md',

    # Templates
    'templates/output_template.md': '07_output_template.md',
}

# Config files mapping (08-10 range)
CONFIG_MAPPING = {
    'copy_rules.json': '08_copy_rules.json',
    'marketplace_specs.json': '09_marketplace_specs.json',
    'persuasion_patterns.json': '10_persuasion_patterns.json',
    'brand_rules.json': '08_brand_rules.json',
    'brand_strategy.json': '08_brand_strategy.json',
    'color_psychology.json': '11_color_psychology.json',
    'archetype_specs.json': '12_archetype_specs.json',
    'storytelling_frameworks.json': '13_storytelling_frameworks.json',
    'identity_patterns.json': '15_identity_patterns.json',
    'domain_rules.json': '08_domain_rules.json',
    'domain_specs.json': '09_domain_specs.json',
    'domain_patterns.json': '10_domain_patterns.json',
}

# Plans mapping
PLANS_MAPPING = {
    'full_anuncio.json': '12_execution_plans.json',
    'quick_anuncio.json': '12_execution_plans.json',
    'execution_plans.json': '12_execution_plans.json',
}

# HOP range (13-19)
HOP_START_NUM = 13
HOP_END_NUM = 19

# Maximum tokens per file (for validation)
MAX_TOKENS_PER_FILE = 4096


# === DATA MODELS ===

@dataclass
class SyncAction:
    """Represents a file sync action"""
    source: Path
    dest: Path
    action: str  # 'copy', 'update', 'skip', 'create'
    reason: str
    source_hash: Optional[str] = None
    dest_hash: Optional[str] = None


@dataclass
class AgentSyncReport:
    """Report for a single agent sync"""
    agent_name: str
    agent_path: Path
    iso_path: Path
    actions: List[SyncAction] = field(default_factory=list)
    files_copied: int = 0
    files_updated: int = 0
    files_skipped: int = 0
    files_created: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class GlobalSyncReport:
    """Global sync report"""
    timestamp: str
    mode: str
    agents_processed: int = 0
    total_files_synced: int = 0
    total_errors: int = 0
    agent_reports: List[AgentSyncReport] = field(default_factory=list)


# === UTILITY FUNCTIONS ===

def file_hash(path: Path) -> str:
    """Calculate MD5 hash of file content"""
    if not path.exists():
        return ""
    content = path.read_bytes()
    return hashlib.md5(content).hexdigest()


def estimate_tokens(text: str) -> int:
    """Rough estimate of tokens (4 chars per token)"""
    return len(text) // 4


def get_changed_files_git() -> List[Path]:
    """Get list of files changed in current git staging"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True,
            cwd=AGENTS_ROOT.parent.parent  # git root
        )
        if result.returncode == 0:
            files = result.stdout.strip().split('\n')
            return [Path(f) for f in files if f]
    except Exception:
        pass
    return []


def should_sync_agent(agent_path: Path, changed_files: List[Path]) -> bool:
    """Check if agent has changed files that need sync"""
    if not changed_files:
        return True  # No filter, sync all

    agent_rel = agent_path.relative_to(AGENTS_ROOT.parent.parent)
    for changed in changed_files:
        if str(changed).startswith(str(agent_rel)):
            return True
    return False


def extract_version_from_content(content: str) -> Optional[str]:
    """Extract version from file content"""
    patterns = [
        r'\*\*Version\*\*:\s*([0-9]+\.[0-9]+\.[0-9]+)',
        r'Version:\s*([0-9]+\.[0-9]+\.[0-9]+)',
        r'v([0-9]+\.[0-9]+\.[0-9]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return None


def add_iso_header(content: str, source_file: str, agent_name: str) -> str:
    """Add iso_vectorstore header to content if not present"""
    header_marker = "<!-- iso_vectorstore -->"

    if header_marker in content:
        return content

    version = extract_version_from_content(content) or "1.0.0"
    today = datetime.now().strftime('%Y-%m-%d')

    header = f"""{header_marker}
<!--
  Source: {source_file}
  Agent: {agent_name}
  Synced: {today}
  Version: {version}
  Package: iso_vectorstore (export package)
-->

"""
    return header + content


# === SYNC FUNCTIONS ===

def sync_direct_files(
    agent_path: Path,
    iso_path: Path,
    agent_name: str,
    dry_run: bool = False
) -> List[SyncAction]:
    """Sync direct file mappings (PRIME.md → 02_PRIME.md, etc.)"""
    actions = []

    for source_name, dest_name in FILE_MAPPING.items():
        source = agent_path / source_name
        dest = iso_path / dest_name

        if not source.exists():
            continue

        source_h = file_hash(source)
        dest_h = file_hash(dest) if dest.exists() else ""

        if source_h == dest_h:
            actions.append(SyncAction(
                source=source,
                dest=dest,
                action='skip',
                reason='identical content',
                source_hash=source_h,
                dest_hash=dest_h
            ))
            continue

        action_type = 'update' if dest.exists() else 'copy'

        if not dry_run:
            content = source.read_text(encoding='utf-8')
            content = add_iso_header(content, source_name, agent_name)
            dest.write_text(content, encoding='utf-8')

        actions.append(SyncAction(
            source=source,
            dest=dest,
            action=action_type,
            reason='content changed' if dest_h else 'new file',
            source_hash=source_h,
            dest_hash=dest_h
        ))

    return actions


def sync_config_files(
    agent_path: Path,
    iso_path: Path,
    agent_name: str,
    dry_run: bool = False
) -> List[SyncAction]:
    """Sync config/*.json files to iso_vectorstore"""
    actions = []
    config_dir = agent_path / 'config'

    if not config_dir.exists():
        return actions

    for config_file in config_dir.glob('*.json'):
        dest_name = CONFIG_MAPPING.get(config_file.name)

        if not dest_name:
            # Auto-assign number in 08-10 range if not mapped
            existing_nums = [
                int(f.name.split('_')[0])
                for f in iso_path.glob('*.json')
                if f.name.split('_')[0].isdigit()
            ]
            next_num = 8
            while next_num in existing_nums and next_num <= 10:
                next_num += 1
            if next_num > 10:
                continue  # Skip if no slots available
            dest_name = f"{next_num:02d}_{config_file.name}"

        source = config_file
        dest = iso_path / dest_name

        source_h = file_hash(source)
        dest_h = file_hash(dest) if dest.exists() else ""

        if source_h == dest_h:
            actions.append(SyncAction(
                source=source,
                dest=dest,
                action='skip',
                reason='identical',
                source_hash=source_h,
                dest_hash=dest_h
            ))
            continue

        action_type = 'update' if dest.exists() else 'copy'

        if not dry_run:
            shutil.copy2(source, dest)

        actions.append(SyncAction(
            source=source,
            dest=dest,
            action=action_type,
            reason='synced',
            source_hash=source_h,
            dest_hash=dest_h
        ))

    return actions


def sync_workflow_files(
    agent_path: Path,
    iso_path: Path,
    agent_name: str,
    dry_run: bool = False
) -> List[SyncAction]:
    """Sync workflows/100_ADW*.md → 11_ADW_orchestrator.md"""
    actions = []
    workflows_dir = agent_path / 'workflows'

    if not workflows_dir.exists():
        return actions

    # Find main ADW file
    adw_files = list(workflows_dir.glob('100_ADW*.md'))
    if not adw_files:
        adw_files = list(workflows_dir.glob('*ADW*.md'))

    if not adw_files:
        return actions

    source = adw_files[0]  # Use first ADW file found
    dest = iso_path / '11_ADW_orchestrator.md'

    source_h = file_hash(source)
    dest_h = file_hash(dest) if dest.exists() else ""

    if source_h == dest_h:
        actions.append(SyncAction(
            source=source,
            dest=dest,
            action='skip',
            reason='identical',
            source_hash=source_h,
            dest_hash=dest_h
        ))
        return actions

    action_type = 'update' if dest.exists() else 'copy'

    if not dry_run:
        content = source.read_text(encoding='utf-8')
        content = add_iso_header(content, source.name, agent_name)
        dest.write_text(content, encoding='utf-8')

    actions.append(SyncAction(
        source=source,
        dest=dest,
        action=action_type,
        reason='synced',
        source_hash=source_h,
        dest_hash=dest_h
    ))

    return actions


def sync_prompt_files(
    agent_path: Path,
    iso_path: Path,
    agent_name: str,
    dry_run: bool = False
) -> List[SyncAction]:
    """Sync prompts/*.md → 13-19_HOP_*.md"""
    actions = []
    prompts_dir = agent_path / 'prompts'

    if not prompts_dir.exists():
        return actions

    # Get all prompt files
    prompt_files = sorted(prompts_dir.glob('*.md'))

    hop_num = HOP_START_NUM
    for prompt_file in prompt_files:
        if hop_num > HOP_END_NUM:
            break  # Max 7 HOP files in iso_vectorstore

        # Generate destination name
        base_name = prompt_file.stem
        # Clean up name for iso
        clean_name = re.sub(r'^\d+_', '', base_name)  # Remove leading number
        dest_name = f"{hop_num}_HOP_{clean_name}.md"

        source = prompt_file
        dest = iso_path / dest_name

        source_h = file_hash(source)
        dest_h = file_hash(dest) if dest.exists() else ""

        if source_h == dest_h:
            actions.append(SyncAction(
                source=source,
                dest=dest,
                action='skip',
                reason='identical',
                source_hash=source_h,
                dest_hash=dest_h
            ))
            hop_num += 1
            continue

        action_type = 'update' if dest.exists() else 'copy'

        if not dry_run:
            content = source.read_text(encoding='utf-8')
            content = add_iso_header(content, prompt_file.name, agent_name)
            dest.write_text(content, encoding='utf-8')

        actions.append(SyncAction(
            source=source,
            dest=dest,
            action=action_type,
            reason='synced',
            source_hash=source_h,
            dest_hash=dest_h
        ))

        hop_num += 1

    return actions


def sync_plans_files(
    agent_path: Path,
    iso_path: Path,
    agent_name: str,
    dry_run: bool = False
) -> List[SyncAction]:
    """Sync plans/*.json → 12_execution_plans.json (consolidated)"""
    actions = []
    plans_dir = agent_path / 'plans'

    if not plans_dir.exists():
        return actions

    plan_files = list(plans_dir.glob('*.json'))
    if not plan_files:
        return actions

    # Consolidate all plans into single file
    dest = iso_path / '12_execution_plans.json'

    consolidated = {
        "_meta": {
            "source": "consolidated from plans/",
            "agent": agent_name,
            "synced": datetime.now().isoformat(),
            "files": [f.name for f in plan_files]
        },
        "plans": {}
    }

    for plan_file in plan_files:
        try:
            plan_data = json.loads(plan_file.read_text(encoding='utf-8'))
            plan_name = plan_file.stem
            consolidated["plans"][plan_name] = plan_data
        except json.JSONDecodeError:
            continue

    new_content = json.dumps(consolidated, indent=2, ensure_ascii=False)
    new_hash = hashlib.md5(new_content.encode()).hexdigest()

    dest_h = file_hash(dest) if dest.exists() else ""

    if new_hash == dest_h:
        actions.append(SyncAction(
            source=plans_dir,
            dest=dest,
            action='skip',
            reason='identical',
            source_hash=new_hash,
            dest_hash=dest_h
        ))
        return actions

    action_type = 'update' if dest.exists() else 'create'

    if not dry_run:
        dest.write_text(new_content, encoding='utf-8')

    actions.append(SyncAction(
        source=plans_dir,
        dest=dest,
        action=action_type,
        reason='consolidated plans',
        source_hash=new_hash,
        dest_hash=dest_h
    ))

    return actions


def ensure_quick_start(
    iso_path: Path,
    agent_name: str,
    dry_run: bool = False
) -> Optional[SyncAction]:
    """Ensure 01_QUICK_START.md exists"""
    quick_start = iso_path / '01_QUICK_START.md'

    if quick_start.exists():
        return None

    # Generate basic quick start from template
    agent_title = agent_name.replace('_agent', '').replace('_', ' ').title()

    template = f"""<!-- iso_vectorstore -->
# {agent_title} Agent | Quick Start Guide v1.0.0

**Package**: iso_vectorstore (export package)
**Agent**: {agent_name}

---

## IDENTITY

**Agent**: {agent_title} Agent
**Domain**: Specialized domain
**Function**: Primary function
**Model**: GPT-4+ / Sonnet 4.5+

---

## FILE ARCHITECTURE

### Core (01-05) | Read First
| File | Purpose |
|------|---------|
| 01_QUICK_START.md | This file - navigation |
| 02_PRIME.md | Identity, philosophy |
| 03_INSTRUCTIONS.md | Workflow rules |
| 04_README.md | Documentation |
| 05_ARCHITECTURE.md | Technical architecture |

### Schemas (06-10) | Validation
| File | Purpose |
|------|---------|
| 06_input_schema.json | Input validation |
| 07_output_template.md | Output format |
| 08-10_*.json | Domain configs |

### Execution (11-15) | Run
| File | Purpose |
|------|---------|
| 11_ADW_orchestrator.md | Main workflow |
| 12_execution_plans.json | Plans |
| 13-19_HOP_*.md | Prompts |

### Reference (16-20)
| File | Purpose |
|------|---------|
| 20_CHANGELOG.md | Version history |

---

**Next**: Read 02_PRIME.md -> 03_INSTRUCTIONS.md
"""

    if not dry_run:
        quick_start.write_text(template, encoding='utf-8')

    return SyncAction(
        source=iso_path,
        dest=quick_start,
        action='create',
        reason='generated from template'
    )


def ensure_input_schema(
    agent_path: Path,
    iso_path: Path,
    agent_name: str,
    dry_run: bool = False
) -> Optional[SyncAction]:
    """Ensure 06_input_schema.json exists"""
    schema_dest = iso_path / '06_input_schema.json'

    # Check for existing schema in various locations
    schema_sources = [
        agent_path / 'schemas' / 'input_schema.json',
        agent_path / 'config' / 'input_schema.json',
        agent_path / 'input_schema.json',
    ]

    for source in schema_sources:
        if source.exists():
            source_h = file_hash(source)
            dest_h = file_hash(schema_dest) if schema_dest.exists() else ""

            if source_h != dest_h:
                if not dry_run:
                    shutil.copy2(source, schema_dest)
                return SyncAction(
                    source=source,
                    dest=schema_dest,
                    action='copy',
                    reason='found schema',
                    source_hash=source_h
                )
            return None

    # Generate minimal schema if none exists
    if schema_dest.exists():
        return None

    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": f"{agent_name} Input Schema",
        "type": "object",
        "properties": {
            "task": {
                "type": "string",
                "description": "Task description"
            },
            "context": {
                "type": "object",
                "description": "Additional context"
            }
        },
        "required": ["task"]
    }

    if not dry_run:
        schema_dest.write_text(json.dumps(schema, indent=2), encoding='utf-8')

    return SyncAction(
        source=iso_path,
        dest=schema_dest,
        action='create',
        reason='generated minimal schema'
    )


# === MAIN SYNC FUNCTION ===

def sync_agent(
    agent_path: Path,
    dry_run: bool = False,
    verbose: bool = False
) -> AgentSyncReport:
    """Sync a single agent's iso_vectorstore"""
    agent_name = agent_path.name
    iso_path = agent_path / 'iso_vectorstore'

    report = AgentSyncReport(
        agent_name=agent_name,
        agent_path=agent_path,
        iso_path=iso_path
    )

    # Ensure iso_vectorstore directory exists
    if not dry_run:
        iso_path.mkdir(exist_ok=True)

    # Run all sync functions
    all_actions = []

    # 1. Direct file mappings
    all_actions.extend(sync_direct_files(agent_path, iso_path, agent_name, dry_run))

    # 2. Config files
    all_actions.extend(sync_config_files(agent_path, iso_path, agent_name, dry_run))

    # 3. Workflow files
    all_actions.extend(sync_workflow_files(agent_path, iso_path, agent_name, dry_run))

    # 4. Prompt files (HOPs)
    all_actions.extend(sync_prompt_files(agent_path, iso_path, agent_name, dry_run))

    # 5. Plans consolidation
    all_actions.extend(sync_plans_files(agent_path, iso_path, agent_name, dry_run))

    # 6. Ensure required files exist
    quick_start_action = ensure_quick_start(iso_path, agent_name, dry_run)
    if quick_start_action:
        all_actions.append(quick_start_action)

    schema_action = ensure_input_schema(agent_path, iso_path, agent_name, dry_run)
    if schema_action:
        all_actions.append(schema_action)

    # Compile report
    report.actions = all_actions
    for action in all_actions:
        if action.action == 'copy':
            report.files_copied += 1
        elif action.action == 'update':
            report.files_updated += 1
        elif action.action == 'skip':
            report.files_skipped += 1
        elif action.action == 'create':
            report.files_created += 1

    if verbose:
        print(f"\n  {agent_name}:")
        for action in all_actions:
            if action.action != 'skip':
                print(f"    [{action.action.upper()}] {action.dest.name}")

    return report


def sync_all_agents(
    target_agent: Optional[str] = None,
    dry_run: bool = False,
    pre_commit: bool = False,
    verbose: bool = False
) -> GlobalSyncReport:
    """Sync all agents or specific agent"""

    report = GlobalSyncReport(
        timestamp=datetime.now().isoformat(),
        mode='dry-run' if dry_run else ('pre-commit' if pre_commit else 'full')
    )

    # Get changed files for pre-commit mode
    changed_files = get_changed_files_git() if pre_commit else []

    # Find all agent directories
    agent_dirs = [
        d for d in AGENTS_ROOT.iterdir()
        if d.is_dir() and d.name.endswith('_agent')
    ]

    if target_agent:
        agent_dirs = [d for d in agent_dirs if d.name == target_agent]

    print("=" * 60)
    print("ISO VECTORSTORE SYNC")
    print("=" * 60)
    print(f"Mode: {report.mode}")
    print(f"Agents found: {len(agent_dirs)}")
    if target_agent:
        print(f"Target: {target_agent}")

    for agent_dir in sorted(agent_dirs):
        # Skip if pre-commit and no changes in this agent
        if pre_commit and not should_sync_agent(agent_dir, changed_files):
            if verbose:
                print(f"  [SKIP] {agent_dir.name} (no changes)")
            continue

        agent_report = sync_agent(agent_dir, dry_run, verbose)
        report.agent_reports.append(agent_report)
        report.agents_processed += 1

        synced = agent_report.files_copied + agent_report.files_updated + agent_report.files_created
        report.total_files_synced += synced
        report.total_errors += len(agent_report.errors)

        if not verbose and synced > 0:
            print(f"  {agent_dir.name}: {synced} files synced")

    # Summary
    print("\n" + "-" * 60)
    print("SUMMARY")
    print("-" * 60)
    print(f"Agents processed: {report.agents_processed}")
    print(f"Total files synced: {report.total_files_synced}")
    print(f"Errors: {report.total_errors}")

    if dry_run:
        print("\n[DRY-RUN] No files were modified")
    else:
        print("\n[OK] Sync complete")

    return report


# === CLI ===

def main():
    parser = argparse.ArgumentParser(
        description='Sync agent source files to iso_vectorstore export package',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Sync all agents
  python builders/18_iso_vectorstore_sync.py

  # Sync specific agent
  python builders/18_iso_vectorstore_sync.py --agent anuncio_agent

  # Dry run (preview)
  python builders/18_iso_vectorstore_sync.py --dry-run

  # Pre-commit hook mode
  python builders/18_iso_vectorstore_sync.py --pre-commit
        """
    )

    parser.add_argument(
        '--agent',
        type=str,
        help='Specific agent to sync (e.g., anuncio_agent)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying files'
    )

    parser.add_argument(
        '--pre-commit',
        action='store_true',
        help='Pre-commit hook mode (only sync changed agents)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )

    args = parser.parse_args()

    report = sync_all_agents(
        target_agent=args.agent,
        dry_run=args.dry_run,
        pre_commit=args.pre_commit,
        verbose=args.verbose
    )

    return 0 if report.total_errors == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
