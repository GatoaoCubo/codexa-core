"""
CODEXA Configuration Package

Centralized configuration for paths, constants, and settings.
"""

from .paths import *

__all__ = [
    # Path hierarchy
    'SCRIPT_DIR',
    'CONFIG_DIR',
    'CODEXA_AGENT_DIR',
    'AGENTS_ROOT',
    'CODEXA_APP',
    'PROJECT_ROOT',

    # Common paths
    'PATH_BUILDERS',
    'PATH_VALIDATORS',
    'PATH_TEMPLATES',
    'PATH_WORKFLOWS',
    'PATH_PROMPTS',
    'PATH_COMMANDS',

    # Registry and docs
    'PATH_REGISTRY',
    'PATH_HOP_FRAMEWORK',
    'PATH_DOCS_CONSOLIDATED',
]
