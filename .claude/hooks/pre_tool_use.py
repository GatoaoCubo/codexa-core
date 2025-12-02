#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = []
# ///
"""
CODEXA.app Pre-Tool-Use Hook

Security validation before tool execution.
Based on TAC-8 pre_tool_use.py patterns.
"""

import json
import sys
import re
from pathlib import Path

# Blocked patterns
DANGEROUS_COMMANDS = [
    r"rm\s+-rf\s+/",
    r"rm\s+-rf\s+~",
    r"rm\s+-rf\s+\*",
    r":(){ :|:& };:",  # Fork bomb
    r"mkfs\.",
    r"dd\s+if=",
    r">\s*/dev/sd",
    r"chmod\s+-R\s+777\s+/",
]

SENSITIVE_FILES = [
    ".env",
    "credentials.json",
    "secrets.json",
    ".npmrc",
    ".pypirc",
    "id_rsa",
    "id_ed25519",
]

# Allowed patterns (exceptions)
ALLOWED_PATTERNS = [
    ".env.example",
    ".env.sample",
    ".env.template",
]


def is_dangerous_command(command: str) -> tuple[bool, str]:
    """Check if command is dangerous."""
    for pattern in DANGEROUS_COMMANDS:
        if re.search(pattern, command, re.IGNORECASE):
            return True, f"Blocked dangerous pattern: {pattern}"
    return False, ""


def is_sensitive_file(file_path: str) -> tuple[bool, str]:
    """Check if file is sensitive."""
    path = Path(file_path)
    filename = path.name.lower()

    # Check allowed exceptions first
    for allowed in ALLOWED_PATTERNS:
        if allowed in filename:
            return False, ""

    # Check sensitive patterns
    for sensitive in SENSITIVE_FILES:
        if sensitive in filename:
            return True, f"Sensitive file access: {sensitive}"

    return False, ""


def validate_tool_input(tool_name: str, tool_input: dict) -> tuple[bool, str]:
    """Validate tool input for security."""

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        dangerous, reason = is_dangerous_command(command)
        if dangerous:
            return False, reason

    elif tool_name in ["Write", "Edit", "Read"]:
        file_path = tool_input.get("file_path", "")
        sensitive, reason = is_sensitive_file(file_path)
        if sensitive:
            return False, reason

    return True, ""


def main():
    """Pre-tool-use validation."""
    try:
        input_data = json.loads(sys.stdin.read())

        tool_name = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})

        # Validate
        allowed, reason = validate_tool_input(tool_name, tool_input)

        if not allowed:
            # Return error to block execution
            print(json.dumps({
                "decision": "block",
                "reason": reason
            }))
            sys.exit(1)

        # Allow execution
        sys.exit(0)

    except Exception as e:
        # On error, allow (fail open for dev)
        print(f"[CODEXA] Hook error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
