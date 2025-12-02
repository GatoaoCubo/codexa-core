#!/usr/bin/env python3
"""
CODEXA - Main Entry Point

Intelligent launcher that chooses between optimized and full versions
based on the operation requested.
"""

import sys
import os
from pathlib import Path

# Operations that need full initialization
FULL_OPS = ['migrate', 'update-readme', 'introspect', 'full-status']

# Quick operations that can use optimized version
QUICK_OPS = ['status', 'list', 'read', 'scan', 'find', 'quick']


def needs_full_init(args):
    """Check if operation needs full module initialization."""
    if len(args) < 2:
        return False

    operation = args[1].lower()

    # Check for operations that need full system
    for op in FULL_OPS:
        if op in operation:
            return True

    return False


def main():
    """Smart launcher for CODEXA."""
    codexa_dir = Path(__file__).parent

    # Determine which CLI to use
    if needs_full_init(sys.argv):
        # Use full CLI for complex operations
        cli_script = codexa_dir / "cli.py"
        print("Loading full CODEXA system...")
    else:
        # Use optimized CLI for quick operations
        cli_script = codexa_dir / "cli_optimized.py"
        # Don't print anything for quick ops

    # Execute the appropriate CLI
    import subprocess
    cmd = [sys.executable, str(cli_script)] + sys.argv[1:]

    try:
        result = subprocess.run(cmd)
        return result.returncode
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.")
        return 130
    except Exception as e:
        print(f"Error: {e}")
        return 1


def show_help():
    """Show help message."""
    print("""
CODEXA - HOP Meta-Agent System
==============================

Quick Commands (Fast):
  codexa status         - Show system status
  codexa list          - List documents
  codexa scan          - Scan repository
  codexa read <file>   - Read a file
  codexa find <pattern> - Find files

Full Commands (All Features):
  codexa full-status   - Complete system check
  codexa migrate       - Run migrations
  codexa introspect    - System introspection

Groups:
  codexa crud ...      - CRUD operations
  codexa scout ...     - Scout operations
  codexa ecom ...      - E-commerce operations

Options:
  --quiet, -q          - Suppress messages
  --help, -h           - Show help

Examples:
  codexa status                    # Quick status
  codexa crud list --type document # List documents
  codexa scout scan --cache        # Scan with cache
  codexa ecom products list        # List products

For detailed help on any command:
  codexa [command] --help
""")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        show_help()
        sys.exit(0)

    sys.exit(main())