"""
Utility functions for ADW workflow builders.

This module provides formatting, status tracking, and helper functions
used across multiple builder scripts.
"""

from typing import Optional, Dict, Any
from datetime import datetime


# ============================================================================
# STATUS FORMATTING
# ============================================================================

def format_agent_status(
    agent_name: str,
    status: str,
    phase: Optional[str] = None,
    details: Optional[str] = None
) -> str:
    """Format agent status for display.

    Args:
        agent_name: Name/ID of the agent
        status: Current status (running, success, error, etc.)
        phase: Optional phase name
        details: Optional additional details

    Returns:
        Formatted status string
    """
    timestamp = datetime.now().strftime("%H:%M:%S")

    parts = [f"[{timestamp}]", agent_name, status]

    if phase:
        parts.append(f"({phase})")

    status_line = " ".join(parts)

    if details:
        status_line += f"\n  {details}"

    return status_line


def format_worktree_status(
    worktree_name: str,
    branch: str,
    status: str,
    path: Optional[str] = None
) -> str:
    """Format git worktree status for display.

    Args:
        worktree_name: Name of the worktree
        branch: Branch name
        status: Current status
        path: Optional path to worktree

    Returns:
        Formatted worktree status string
    """
    parts = [f"Worktree: {worktree_name}", f"Branch: {branch}", f"Status: {status}"]

    if path:
        parts.append(f"Path: {path}")

    return "\n".join(parts)


def format_phase_summary(
    phase_name: str,
    duration: float,
    success: bool,
    key_outputs: Optional[Dict[str, Any]] = None
) -> str:
    """Format a phase execution summary.

    Args:
        phase_name: Name of the phase
        duration: Execution time in seconds
        success: Whether phase succeeded
        key_outputs: Optional dictionary of key outputs

    Returns:
        Formatted summary string
    """
    status_icon = "✅" if success else "❌"
    status_text = "SUCCESS" if success else "FAILED"

    summary = f"{status_icon} {phase_name}: {status_text}\n"
    summary += f"   Duration: {duration:.2f}s\n"

    if key_outputs:
        summary += "   Key Outputs:\n"
        for key, value in key_outputs.items():
            value_str = str(value)[:50]  # Truncate long values
            summary += f"     - {key}: {value_str}\n"

    return summary


# ============================================================================
# TIME UTILITIES
# ============================================================================

def format_duration(seconds: float) -> str:
    """Format duration in human-readable format.

    Args:
        seconds: Duration in seconds

    Returns:
        Formatted duration string (e.g., "2m 30s", "45s")
    """
    if seconds < 60:
        return f"{seconds:.1f}s"

    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60

    if minutes < 60:
        return f"{minutes}m {remaining_seconds:.0f}s"

    hours = int(minutes // 60)
    remaining_minutes = minutes % 60

    return f"{hours}h {remaining_minutes}m"


def timestamp_iso() -> str:
    """Get current timestamp in ISO format.

    Returns:
        ISO formatted timestamp string
    """
    return datetime.now().isoformat()


def timestamp_readable() -> str:
    """Get current timestamp in human-readable format.

    Returns:
        Readable timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============================================================================
# FILE UTILITIES
# ============================================================================

def truncate_text(
    text: str,
    max_length: int = 100,
    suffix: str = "..."
) -> str:
    """Truncate text to maximum length.

    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add if truncated

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def format_file_size(size_bytes: int) -> str:
    """Format file size in human-readable format.

    Args:
        size_bytes: Size in bytes

    Returns:
        Formatted size string (e.g., "1.5 KB", "2.3 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0

    return f"{size_bytes:.1f} TB"


# ============================================================================
# VALIDATION UTILITIES
# ============================================================================

def validate_adw_id(adw_id: str) -> bool:
    """Validate ADW ID format.

    Args:
        adw_id: ADW ID to validate

    Returns:
        True if valid, False otherwise
    """
    if not adw_id:
        return False

    # ADW IDs should be alphanumeric, typically 8-16 characters
    if not adw_id.isalnum():
        return False

    if len(adw_id) < 4 or len(adw_id) > 32:
        return False

    return True


def validate_agent_name(name: str) -> bool:
    """Validate agent name format.

    Args:
        name: Agent name to validate

    Returns:
        True if valid, False otherwise
    """
    if not name:
        return False

    # Agent names should be alphanumeric with hyphens/underscores
    allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_")

    if not all(c in allowed_chars for c in name):
        return False

    if len(name) < 3 or len(name) > 64:
        return False

    return True


# ============================================================================
# RICH FORMATTING HELPERS
# ============================================================================

def create_status_emoji(success: bool) -> str:
    """Get status emoji based on success/failure.

    Args:
        success: Whether operation succeeded

    Returns:
        Appropriate emoji
    """
    return "✅" if success else "❌"


def create_phase_emoji(phase_name: str) -> str:
    """Get emoji for a workflow phase.

    Args:
        phase_name: Name of the phase

    Returns:
        Appropriate emoji for the phase
    """
    phase_emojis = {
        "plan": "📋",
        "planning": "📋",
        "build": "🔨",
        "building": "🔨",
        "construction": "🏗️",
        "test": "🧪",
        "testing": "🧪",
        "validation": "✓",
        "review": "🔍",
        "document": "📝",
        "documentation": "📝",
        "deploy": "🚀",
        "deployment": "🚀",
    }

    phase_lower = phase_name.lower()

    for key, emoji in phase_emojis.items():
        if key in phase_lower:
            return emoji

    return "⚙️"  # Default gear emoji


def color_by_status(status: str) -> str:
    """Get Rich color name based on status.

    Args:
        status: Status string

    Returns:
        Rich color name
    """
    status_lower = status.lower()

    if any(word in status_lower for word in ['success', 'complete', 'done', 'pass']):
        return "green"
    elif any(word in status_lower for word in ['error', 'fail', 'failed']):
        return "red"
    elif any(word in status_lower for word in ['warning', 'warn']):
        return "yellow"
    elif any(word in status_lower for word in ['running', 'progress', 'working']):
        return "cyan"
    else:
        return "white"


# ============================================================================
# MODULE INFO
# ============================================================================

__version__ = "1.0.0"
__author__ = "CODEXA Team"
__description__ = "Utility functions for ADW workflow builders"
