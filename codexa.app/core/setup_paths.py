#!/usr/bin/env python3
"""
CODEXA Path Setup Script
Generates .mcp.json and .claude/settings.json with correct paths for current machine.

Usage:
    python setup_paths.py           # Generate config files
    python setup_paths.py --check   # Check current paths
    python setup_paths.py --dry-run # Show what would be generated
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Optional


def get_project_root() -> Path:
    """Detect project root - the directory containing codexa.app AND path_registry.json."""
    # Walk up from this file looking for codexa.gato (our actual project root)
    current = Path(__file__).resolve()
    for parent in current.parents:
        # The real project root has codexa.app as DIRECT child (not parent)
        if (parent / "codexa.app").exists() and parent.name != "codexa.app":
            # Verify this is codexa.gato by checking for path_registry.json or CLAUDE.md
            if (parent / "path_registry.json").exists() or (parent / "CLAUDE.md").exists():
                return parent
            # Also check if parent name suggests it's the right one
            if "codexa" in parent.name.lower() or "gato" in parent.name.lower():
                return parent

    # Fallback: try git root but validate it's the right level
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--show-toplevel'],
            capture_output=True, text=True,
            cwd=Path(__file__).parent
        )
        if result.returncode == 0:
            git_root = Path(result.stdout.strip())
            # Check if codexa.gato is inside git_root
            for child in git_root.iterdir():
                if child.is_dir() and (child / "codexa.app").exists():
                    return child
            # Or if git_root itself is the project
            if (git_root / "codexa.app").exists():
                return git_root
    except Exception:
        pass

    raise RuntimeError("Could not detect project root")


def generate_mcp_json(project_root: Path, elevenlabs_key: Optional[str] = None) -> dict:
    """Generate .mcp.json configuration with correct paths."""
    # Use forward slashes for JSON (works on both Windows and Unix)
    root = str(project_root).replace('\\', '/')

    config = {
        "mcpServers": {
            "voice": {
                "type": "stdio",
                "command": "py",
                "args": [
                    "-3.12",
                    f"{root}/codexa.app/voice/server.py"
                ],
                "env": {
                    "PYTHONPATH": root,
                    "ELEVENLABS_API_KEY": elevenlabs_key or "${ELEVENLABS_API_KEY}"
                }
            },
            "browser": {
                "type": "stdio",
                "command": "node",
                "args": [
                    f"{root}/codexa.app/mcp-servers/browser-mcp/index.js"
                ]
            },
            "scout": {
                "type": "stdio",
                "command": "node",
                "args": [
                    f"{root}/codexa.app/mcp-servers/scout-mcp/index.js"
                ],
                "env": {
                    "SCOUT_ROOT": root,
                    "SCOUT_CACHE_MODE": "session",
                    "SCOUT_LOG_LEVEL": "info"
                }
            }
        }
    }

    return config


def generate_claude_settings(project_root: Path) -> dict:
    """Generate .claude/settings.json with correct paths."""
    # Use forward slashes for JSON
    root = str(project_root).replace('\\', '/')

    config = {
        "mcpServers": {
            "scout": {
                "command": "node",
                "args": [
                    f"{root}/codexa.app/mcp-servers/scout-mcp/index.js"
                ],
                "env": {
                    "SCOUT_ROOT": root
                }
            },
            "browser": {
                "command": "node",
                "args": [
                    f"{root}/codexa.app/mcp-servers/browser-mcp/index.js"
                ]
            },
            "voice": {
                "command": "python",
                "args": [
                    f"{root}/codexa.app/voice/server.py"
                ]
            }
        },
        "hooks": {
            "PreToolUse": [
                {
                    "matcher": "Bash",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python",
                            "args": [f"{root}/codexa.app/.claude/hooks/validate_paths.py"]
                        }
                    ]
                },
                {
                    "matcher": "Write",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python",
                            "args": [f"{root}/codexa.app/.claude/hooks/validate_paths.py"]
                        }
                    ]
                },
                {
                    "matcher": "Edit",
                    "hooks": [
                        {
                            "type": "command",
                            "command": "python",
                            "args": [f"{root}/codexa.app/.claude/hooks/validate_paths.py"]
                        }
                    ]
                }
            ]
        }
    }

    return config


def check_current_paths(project_root: Path) -> bool:
    """Check if current config files have correct paths."""
    root_str = str(project_root).replace('\\', '/')
    all_ok = True

    # Check .mcp.json
    mcp_path = project_root / ".mcp.json"
    if mcp_path.exists():
        with open(mcp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if root_str in content:
                print(f"[OK] .mcp.json contains current root")
            else:
                print(f"[OUTDATED] .mcp.json has different root")
                all_ok = False
    else:
        print(f"[MISSING] .mcp.json")
        all_ok = False

    # Check .claude/settings.json
    settings_path = project_root / "codexa.app" / ".claude" / "settings.json"
    if settings_path.exists():
        with open(settings_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if root_str in content:
                print(f"[OK] .claude/settings.json contains current root")
            else:
                print(f"[OUTDATED] .claude/settings.json has different root")
                all_ok = False
    else:
        print(f"[MISSING] .claude/settings.json")
        all_ok = False

    return all_ok


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate CODEXA config files with correct paths')
    parser.add_argument('--check', action='store_true', help='Check current paths')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be generated')
    parser.add_argument('--elevenlabs-key', type=str, help='ElevenLabs API key')
    args = parser.parse_args()

    try:
        project_root = get_project_root()
        print(f"Project Root: {project_root}")
        print()
    except RuntimeError as e:
        print(f"ERROR: {e}")
        sys.exit(1)

    if args.check:
        all_ok = check_current_paths(project_root)
        sys.exit(0 if all_ok else 1)

    # Generate configs
    mcp_config = generate_mcp_json(project_root, args.elevenlabs_key)
    claude_settings = generate_claude_settings(project_root)

    if args.dry_run:
        print("=== .mcp.json ===")
        print(json.dumps(mcp_config, indent=2))
        print()
        print("=== .claude/settings.json ===")
        print(json.dumps(claude_settings, indent=2))
        return

    # Write .mcp.json
    mcp_path = project_root / ".mcp.json"
    with open(mcp_path, 'w', encoding='utf-8') as f:
        json.dump(mcp_config, f, indent=2)
    print(f"[UPDATED] {mcp_path}")

    # Write .claude/settings.json
    settings_path = project_root / "codexa.app" / ".claude" / "settings.json"
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    with open(settings_path, 'w', encoding='utf-8') as f:
        json.dump(claude_settings, f, indent=2)
    print(f"[UPDATED] {settings_path}")

    print()
    print("Config files updated with paths for this machine.")
    print("Run again with --check to verify.")


if __name__ == "__main__":
    main()
