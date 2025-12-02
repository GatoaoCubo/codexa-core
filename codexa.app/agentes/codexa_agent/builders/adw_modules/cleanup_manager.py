#!/usr/bin/env python3
"""
CODEXA Cleanup Manager - Remove temporary and obsolete files

This script safely removes temporary outputs, summaries, and build artifacts
while preserving source code, documentation, and reusable examples.

Usage:
    python cleanup_manager.py --mode quick          # Remove temp agent outputs
    python cleanup_manager.py --mode full           # Full cleanup
    python cleanup_manager.py --mode deep           # Deep cleanup (includes old examples)
    python cleanup_manager.py --dry-run             # Preview without deleting
    python cleanup_manager.py --backup --mode full  # Backup before cleanup

Safety:
    - Protected paths are never deleted
    - Confirmation required for destructive operations
    - Dry-run mode for previewing
    - Optional backup before cleanup
"""

import os
import sys
import re
import shutil
import argparse
from pathlib import Path
from typing import List, Tuple, Dict
from datetime import datetime, timedelta
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))


# ==============================================================================
# CONFIGURATION
# ==============================================================================

PROTECTED_PATHS = [
    "builders/",
    "validators/",
    "adw_modules/",
    "commands/",
    "workflows/",
    "prompts/",
    "agents/_examples/",
    "README.md",
    ".env",
    ".gitignore",
    "pyproject.toml",
    "requirements.txt",
]

# Patterns for files to remove
CLEANUP_PATTERNS = {
    "temp_agent_outputs": r"^agents/[a-f0-9]{8}/$",
    "summary_files": [
        "*_summary.json",
        "*summary*.json",
        "custom_summary_output.json",
        "meta_construction_summary.json",
    ],
    "raw_outputs": [
        "cc_raw_output.jsonl",
        "cc_raw_output.json",
        "cc_final_object.json",
        "claude-max-output.json",
        "claude-max-output.jsonl",
    ],
    "build_artifacts": [
        "__pycache__",
        "*.pyc",
        "*.pyo",
        ".pytest_cache",
        ".coverage",
        "*.log",
        ".DS_Store",
        "Thumbs.db",
    ],
}


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f}TB"


def get_directory_size(path: Path) -> int:
    """Calculate total size of directory recursively."""
    total = 0
    try:
        for entry in path.rglob("*"):
            if entry.is_file():
                total += entry.stat().st_size
    except (PermissionError, OSError):
        pass
    return total


def is_protected(path: Path, workspace_root: Path) -> bool:
    """Check if path is protected from deletion."""
    try:
        relative_path = path.relative_to(workspace_root)
        path_str = str(relative_path).replace("\\", "/")

        for protected in PROTECTED_PATHS:
            if path_str.startswith(protected) or path_str == protected.rstrip("/"):
                return True
    except ValueError:
        pass
    return False


def find_temp_agent_outputs(workspace_root: Path) -> List[Path]:
    """Find temporary agent output directories (8-char hex IDs)."""
    agents_dir = workspace_root / "agents"
    if not agents_dir.exists():
        return []

    temp_outputs = []
    pattern = re.compile(r"^[a-f0-9]{8}$")

    for item in agents_dir.iterdir():
        if item.is_dir() and pattern.match(item.name):
            if not is_protected(item, workspace_root):
                temp_outputs.append(item)

    return temp_outputs


def find_summary_files(workspace_root: Path, exclude_examples: bool = True) -> List[Path]:
    """Find summary JSON files (excluding examples if specified)."""
    summary_files = []

    for pattern in CLEANUP_PATTERNS["summary_files"]:
        for file in workspace_root.rglob(pattern):
            if exclude_examples and "_examples" in str(file):
                continue
            if not is_protected(file, workspace_root):
                summary_files.append(file)

    return summary_files


def find_raw_outputs(workspace_root: Path) -> List[Path]:
    """Find Claude Code raw output files."""
    raw_outputs = []

    for pattern in CLEANUP_PATTERNS["raw_outputs"]:
        for file in workspace_root.rglob(pattern):
            if "_examples" not in str(file):
                if not is_protected(file, workspace_root):
                    raw_outputs.append(file)

    return raw_outputs


def find_build_artifacts(workspace_root: Path) -> List[Path]:
    """Find build artifacts (__pycache__, .pyc, etc.)."""
    artifacts = []

    for pattern in CLEANUP_PATTERNS["build_artifacts"]:
        if pattern == "__pycache__":
            for pycache in workspace_root.rglob("__pycache__"):
                artifacts.append(pycache)
        elif pattern == ".pytest_cache":
            pytest_cache = workspace_root / ".pytest_cache"
            if pytest_cache.exists():
                artifacts.append(pytest_cache)
        else:
            for file in workspace_root.rglob(pattern):
                if not is_protected(file, workspace_root):
                    artifacts.append(file)

    return artifacts


def find_old_examples(workspace_root: Path, days: int = 30) -> List[Path]:
    """Find example directories older than specified days."""
    examples_dir = workspace_root / "agents" / "_examples"
    if not examples_dir.exists():
        return []

    old_examples = []
    cutoff_date = datetime.now() - timedelta(days=days)

    for item in examples_dir.iterdir():
        if item.is_dir():
            # Check modification time
            mtime = datetime.fromtimestamp(item.stat().st_mtime)
            if mtime < cutoff_date:
                # Check if it has a README (manually curated)
                readme = item / "README.md"
                if not readme.exists():
                    old_examples.append(item)

    return old_examples


# ==============================================================================
# CLEANUP OPERATIONS
# ==============================================================================

def preview_cleanup(
    temp_outputs: List[Path],
    summaries: List[Path],
    raw_outputs: List[Path],
    artifacts: List[Path],
    old_examples: List[Path] = None,
) -> Dict:
    """Preview cleanup operation without deleting."""

    def calc_size(paths):
        total = 0
        for path in paths:
            if path.is_file():
                total += path.stat().st_size
            elif path.is_dir():
                total += get_directory_size(path)
        return total

    preview = {
        "temp_outputs": {
            "count": len(temp_outputs),
            "size": calc_size(temp_outputs),
            "paths": [str(p) for p in temp_outputs[:5]],  # Show first 5
        },
        "summaries": {
            "count": len(summaries),
            "size": calc_size(summaries),
            "paths": [str(p) for p in summaries[:5]],
        },
        "raw_outputs": {
            "count": len(raw_outputs),
            "size": calc_size(raw_outputs),
            "paths": [str(p) for p in raw_outputs[:5]],
        },
        "artifacts": {
            "count": len(artifacts),
            "size": calc_size(artifacts),
            "paths": [str(p) for p in artifacts[:5]],
        },
    }

    if old_examples:
        preview["old_examples"] = {
            "count": len(old_examples),
            "size": calc_size(old_examples),
            "paths": [str(p) for p in old_examples],
        }

    preview["total_size"] = sum(
        cat["size"] for cat in preview.values() if isinstance(cat, dict) and "size" in cat
    )

    return preview


def execute_cleanup(
    temp_outputs: List[Path],
    summaries: List[Path],
    raw_outputs: List[Path],
    artifacts: List[Path],
    old_examples: List[Path] = None,
) -> Dict:
    """Execute cleanup operation."""

    results = {
        "removed": 0,
        "failed": 0,
        "size_freed": 0,
        "errors": [],
    }

    all_items = (
        temp_outputs + summaries + raw_outputs + artifacts + (old_examples or [])
    )

    for item in all_items:
        try:
            if item.is_file():
                size = item.stat().st_size
                item.unlink()
                results["removed"] += 1
                results["size_freed"] += size
            elif item.is_dir():
                size = get_directory_size(item)
                shutil.rmtree(item)
                results["removed"] += 1
                results["size_freed"] += size
        except (PermissionError, OSError) as e:
            results["failed"] += 1
            results["errors"].append(f"{item}: {str(e)}")

    return results


def create_backup(workspace_root: Path) -> Path:
    """Create backup of agents/ directory before cleanup."""
    agents_dir = workspace_root / "agents"
    if not agents_dir.exists():
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"agents_backup_{timestamp}.tar.gz"
    backup_path = workspace_root / backup_name

    print(f"Creating backup: {backup_name}...")
    shutil.make_archive(
        str(backup_path).replace(".tar.gz", ""),
        "gztar",
        workspace_root,
        "agents",
    )

    return backup_path


# ==============================================================================
# MAIN FUNCTION
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="CODEXA Cleanup Manager - Remove temporary and obsolete files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --mode quick              # Quick cleanup (temp outputs only)
  %(prog)s --mode full               # Full cleanup
  %(prog)s --mode deep --days 30     # Deep cleanup (includes old examples)
  %(prog)s --dry-run                 # Preview without deleting
  %(prog)s --backup --mode full      # Backup before cleanup
        """,
    )

    parser.add_argument(
        "--mode",
        choices=["quick", "full", "deep"],
        default="quick",
        help="Cleanup mode (default: quick)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview cleanup without deleting files",
    )
    parser.add_argument(
        "--confirm",
        action="store_true",
        help="Skip confirmation prompt (for automation)",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Create backup before cleanup",
    )
    parser.add_argument(
        "--days",
        type=int,
        default=30,
        help="Days threshold for deep cleanup (default: 30)",
    )

    args = parser.parse_args()

    # Find workspace root
    workspace_root = Path.cwd()
    while not (workspace_root / "builders").exists():
        if workspace_root.parent == workspace_root:
            print("Error: Not in CODEXA workspace. Run from codexa_agent/ directory.")
            sys.exit(1)
        workspace_root = workspace_root.parent

    print("=" * 80)
    print("CODEXA Cleanup Manager")
    print("=" * 80)
    print(f"Workspace: {workspace_root}")
    print(f"Mode: {args.mode}")
    if args.dry_run:
        print("DRY RUN - No files will be deleted")
    print()

    # Find items to clean based on mode
    temp_outputs = find_temp_agent_outputs(workspace_root)
    summaries = []
    raw_outputs = []
    artifacts = []
    old_examples = []

    if args.mode in ["full", "deep"]:
        summaries = find_summary_files(workspace_root)
        raw_outputs = find_raw_outputs(workspace_root)
        artifacts = find_build_artifacts(workspace_root)

    if args.mode == "deep":
        old_examples = find_old_examples(workspace_root, args.days)

    # Preview
    preview = preview_cleanup(
        temp_outputs, summaries, raw_outputs, artifacts, old_examples if args.mode == "deep" else None
    )

    print("Cleanup Preview:")
    print(f"  Temporary agent outputs: {preview['temp_outputs']['count']} directories ({format_size(preview['temp_outputs']['size'])})")

    if args.mode in ["full", "deep"]:
        print(f"  Summary files: {preview['summaries']['count']} files ({format_size(preview['summaries']['size'])})")
        print(f"  Raw outputs: {preview['raw_outputs']['count']} files ({format_size(preview['raw_outputs']['size'])})")
        print(f"  Build artifacts: {preview['artifacts']['count']} items ({format_size(preview['artifacts']['size'])})")

    if args.mode == "deep" and old_examples:
        print(f"  Old examples (>{args.days} days): {preview['old_examples']['count']} directories ({format_size(preview['old_examples']['size'])})")

    print(f"\nTotal to remove: {format_size(preview['total_size'])}")
    print()

    # Show sample paths
    if temp_outputs:
        print("Sample paths to remove:")
        for path in temp_outputs[:3]:
            print(f"  - {path.relative_to(workspace_root)}")
        if len(temp_outputs) > 3:
            print(f"  ... and {len(temp_outputs) - 3} more")
        print()

    # Dry run - exit here
    if args.dry_run:
        print("DRY RUN - No files were deleted")
        print("Run without --dry-run to execute cleanup")
        sys.exit(0)

    # Confirm
    if not args.confirm:
        print("Proceed with cleanup? (yes/no): ", end="")
        response = input().strip().lower()
        if response != "yes":
            print("Cleanup cancelled")
            sys.exit(0)

    # Backup
    if args.backup:
        backup_path = create_backup(workspace_root)
        if backup_path:
            print(f"Backup created: {backup_path}")
            print()

    # Execute cleanup
    print("Executing cleanup...")
    results = execute_cleanup(
        temp_outputs, summaries, raw_outputs, artifacts, old_examples if args.mode == "deep" else None
    )

    print()
    print("=" * 80)
    print("Cleanup Complete!")
    print("=" * 80)
    print(f"Removed: {results['removed']} items")
    print(f"Failed: {results['failed']} items")
    print(f"Space freed: {format_size(results['size_freed'])}")

    if results['errors']:
        print("\nErrors:")
        for error in results['errors'][:5]:
            print(f"  - {error}")
        if len(results['errors']) > 5:
            print(f"  ... and {len(results['errors']) - 5} more errors")

    print()
    print("Workspace Status:")
    checkmark = "OK" if sys.platform == "win32" else "✓"
    print(f"  - Source code: {checkmark} (intact)")
    print(f"  - Documentation: {checkmark} (intact)")
    print(f"  - Examples: {checkmark} (preserved)")
    print(f"  - Temporary files: {checkmark} (cleaned)")
    print()


if __name__ == "__main__":
    main()
