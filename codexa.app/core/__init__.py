"""
CODEXA Core Module
Central utilities for path resolution, configuration, and cross-agent coordination.
"""

from .path_resolver import (
    PathResolver,
    resolve_path,
    get_resolver,
    get_project_root,
    get_agent_dir,
)

__all__ = [
    'PathResolver',
    'resolve_path',
    'get_resolver',
    'get_project_root',
    'get_agent_dir',
]
