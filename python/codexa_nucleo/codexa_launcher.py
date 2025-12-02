#!/usr/bin/env python3
"""
CODEXA Quick Launcher

Fast launcher for CODEXA system with minimal overhead.
This script is designed to be called by the /codexa command.
"""

import sys
import os
from pathlib import Path

# Add codexa to path
codexa_dir = Path(__file__).parent
sys.path.insert(0, str(codexa_dir))


def main():
    """Main entry point for quick CODEXA launch."""
    import subprocess

    # Default to status if no args
    if len(sys.argv) == 1:
        sys.argv.append('status')

    # Use optimized CLI
    cli_path = codexa_dir / "cli_optimized.py"

    # Run with python explicitly
    cmd = [sys.executable, str(cli_path), '--quiet'] + sys.argv[1:]

    try:
        result = subprocess.run(cmd, capture_output=False, text=True)
        return result.returncode
    except Exception as e:
        print(f"Error launching CODEXA: {e}")
        return 1


def quick_menu():
    """Show quick menu of common operations."""
    print("""
CODEXA Quick Menu:
==================
1. status    - Show system status
2. list      - List documents
3. scan      - Scan repository
4. products  - List products
5. help      - Show full help

Usage: python codexa_launcher.py [command]

Examples:
  python codexa_launcher.py status
  python codexa_launcher.py crud list
  python codexa_launcher.py scout scan
""")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['--help', '-h', 'help']:
        quick_menu()
    else:
        sys.exit(main())