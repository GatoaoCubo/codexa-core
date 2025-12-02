"""
Configuration package for curso_agent
"""

from .paths import (
    # Directories
    CURSO_AGENT_DIR,
    PATH_CONFIG,
    PATH_CONTEXT,
    PATH_ISO_VECTORSTORE,
    PATH_ARTIFACTS,
    PATH_TEMPLATES,
    PATH_BUILDERS,
    PATH_VALIDATORS,
    PATH_COMMANDS,
    PATH_WORKFLOWS,
    PATH_PROMPTS,
    PATH_OUTPUTS,

    # Key files
    PATH_PRIME,
    PATH_README,
    PATH_INSTRUCTIONS,
    PATH_SETUP,
    PATH_REGISTRY,

    # Collections
    CONTEXT_FILES,
    HOTMART_HOPS,
    ARTIFACTS,

    # Validation
    validate_paths,
)

__all__ = [
    "CURSO_AGENT_DIR",
    "PATH_CONFIG",
    "PATH_CONTEXT",
    "PATH_ISO_VECTORSTORE",
    "PATH_ARTIFACTS",
    "PATH_TEMPLATES",
    "PATH_BUILDERS",
    "PATH_VALIDATORS",
    "PATH_COMMANDS",
    "PATH_WORKFLOWS",
    "PATH_PROMPTS",
    "PATH_OUTPUTS",
    "PATH_PRIME",
    "PATH_README",
    "PATH_INSTRUCTIONS",
    "PATH_SETUP",
    "PATH_REGISTRY",
    "CONTEXT_FILES",
    "HOTMART_HOPS",
    "ARTIFACTS",
    "validate_paths",
]
