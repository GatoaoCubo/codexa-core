"""
CODEXA Global Configuration Package

Provides centralized configuration for multi-agent orchestration.

Main exports:
    - paths: Global path configuration for all agents

Usage:
    from config.paths import AGENTS_ROOT, get_agent_paths, get_all_agents

    # Get paths for any agent
    anuncio_paths = get_agent_paths('anuncio')

    # List all agents
    all_agents = get_all_agents()

Version: 2.0.0
"""

# Re-export main path utilities for convenience
from .paths import (
    # Hierarchy
    PROJECT_ROOT,
    CODEXA_APP,
    AGENTS_ROOT,
    CONFIG_DIR,

    # Global paths
    PATH_REGISTRY,
    PATH_HOP_FRAMEWORK,
    PATH_DOCUMENTATION_INDEX,
    PATH_DOCS_CONSOLIDATED,
    PATH_PRIME,
    PATH_README,
    PATH_GLOBAL_OUTPUTS,
    PATH_GLOBAL_LOGS,

    # Multi-agent orchestration functions
    get_agent_dir,
    get_agent_paths,
    get_all_agents,
    get_agent_output,
    get_agent_count,
    validate_global_paths,
)

__all__ = [
    # Hierarchy
    'PROJECT_ROOT',
    'CODEXA_APP',
    'AGENTS_ROOT',
    'CONFIG_DIR',

    # Global paths
    'PATH_REGISTRY',
    'PATH_HOP_FRAMEWORK',
    'PATH_DOCUMENTATION_INDEX',
    'PATH_DOCS_CONSOLIDATED',
    'PATH_PRIME',
    'PATH_README',
    'PATH_GLOBAL_OUTPUTS',
    'PATH_GLOBAL_LOGS',

    # Functions
    'get_agent_dir',
    'get_agent_paths',
    'get_all_agents',
    'get_agent_output',
    'get_agent_count',
    'validate_global_paths',
]

__version__ = '2.0.0'
