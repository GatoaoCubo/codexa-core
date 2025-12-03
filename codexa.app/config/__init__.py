"""
CODEXA Global Configuration Package

Provides centralized configuration for multi-agent orchestration.

Main exports:
    - paths: Global path configuration for all agents
    - env_loader: Centralized environment variable management

Usage:
    from config.paths import AGENTS_ROOT, get_agent_paths, get_all_agents
    from config.env_loader import env, supabase, llm, voice

    # Get paths for any agent
    anuncio_paths = get_agent_paths('anuncio')

    # Access environment config
    api_key = llm.anthropic_key
    db_url = supabase.url

    # Check configuration status
    env.print_status()

Version: 2.1.0
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

# Re-export environment loader for convenience
from .env_loader import (
    env,
    llm,
    supabase,
    voice,
    video,
    google,
    storage,
    automation,
    pesquisa,
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

    # Environment config
    'env',
    'llm',
    'supabase',
    'voice',
    'video',
    'google',
    'storage',
    'automation',
    'pesquisa',
]

__version__ = '2.1.0'
