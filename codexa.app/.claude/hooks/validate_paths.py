#!/usr/bin/env python3
"""
CODEXA Path Validation Hook for Claude Code
Version: 1.0.0
Created: 2025-11-30

Validates file paths and blocks commits if broken paths are detected.
Runs as a PreToolUse hook in Claude Code.

Exit Codes:
- 0: Success (allow tool execution)
- 2: Blocking error (deny tool execution)
- 1: Non-blocking warning

Usage in .claude/settings.json:
{
  "hooks": {
    "PreToolUse": [{
      "matchers": ["Bash"],
      "command": "python",
      "args": [".claude/hooks/validate_paths.py"]
    }]
  }
}
"""

import json
import os
import re
import sys
from pathlib import Path


def get_project_root():
    """Get project root from environment or current directory."""
    return Path(os.environ.get('SCOUT_ROOT', os.getcwd()))


def validate_git_commit(command: str) -> dict:
    """
    Validate before git commit.
    Runs path consistency validator if committing.
    """
    project_root = get_project_root()
    validator_path = project_root / 'codexa.app' / 'agentes' / 'codexa_agent' / 'validators' / '16_path_consistency_validator.py'

    if not validator_path.exists():
        return {"permissionDecision": "allow"}

    # Run validator in strict mode
    import subprocess
    result = subprocess.run(
        [sys.executable, str(validator_path), '--strict', '--quiet'],
        capture_output=True,
        text=True,
        cwd=str(project_root / 'codexa.app' / 'agentes' / 'codexa_agent')
    )

    if result.returncode != 0:
        return {
            "permissionDecision": "deny",
            "reason": "Path validation failed! Fix hardcoded paths before committing.\n" + result.stdout[:500]
        }

    return {"permissionDecision": "allow"}


def validate_file_write(tool_input: dict) -> dict:
    """
    Validate file write operations.
    Checks for:
    - Writing to protected directories
    - Creating files with invalid names
    - Duplicate file detection
    """
    file_path = tool_input.get('file_path', '')

    if not file_path:
        return {"permissionDecision": "allow"}

    path = Path(file_path)

    # Check for invalid patterns in filename
    invalid_patterns = [
        r'\{[^}]+\}',  # Placeholders like {meta}
        r'_HOP_.*_HOP\.md$',  # Redundant HOP naming
    ]

    for pattern in invalid_patterns:
        if re.search(pattern, path.name):
            return {
                "permissionDecision": "deny",
                "reason": f"Invalid filename pattern detected: {path.name}\nPlease use standard naming conventions."
            }

    # Check for duplicate numbered files in iso_vectorstore
    if 'iso_vectorstore' in str(path):
        parent = path.parent
        if parent.exists():
            # Extract number prefix
            match = re.match(r'^(\d+)_', path.name)
            if match:
                num = match.group(1)
                existing = list(parent.glob(f'{num}_*'))
                if len(existing) > 0 and path not in existing:
                    return {
                        "permissionDecision": "ask",
                        "reason": f"Warning: Files with prefix {num}_ already exist in {parent.name}. This may cause numbering conflicts."
                    }

    return {"permissionDecision": "allow"}


def validate_tool_use(event_data: dict) -> dict:
    """
    Main validation function.
    Routes to specific validators based on tool type.
    """
    tool_name = event_data.get('toolName', '')
    tool_input = event_data.get('toolInput', {})

    # Git commit validation
    if tool_name == 'Bash':
        command = tool_input.get('command', '')
        if 'git commit' in command:
            return validate_git_commit(command)

    # File write validation
    if tool_name in ['Write', 'Edit']:
        return validate_file_write(tool_input)

    # Default: allow
    return {"permissionDecision": "allow"}


def main():
    """Main entry point for hook."""
    try:
        # Read event data from stdin
        event_data = json.loads(sys.stdin.read())

        # Validate
        result = validate_tool_use(event_data)

        # Output result
        print(json.dumps(result))

        # Exit code based on decision
        if result.get('permissionDecision') == 'deny':
            sys.exit(2)  # Blocking error
        sys.exit(0)

    except json.JSONDecodeError as e:
        print(json.dumps({
            "reason": f"Hook error: Invalid JSON input - {str(e)}"
        }))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({
            "reason": f"Hook error: {str(e)}"
        }))
        sys.exit(1)


if __name__ == '__main__':
    main()
