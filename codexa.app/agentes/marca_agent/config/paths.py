"""
Marca Agent Path Configuration

Centralized path management for marca_agent using global orchestrator.

This agent uses the global orchestrator at codexa.app/config/paths.py
and defines its own local paths for marca-specific resources.

Usage:
    from config.paths import (
        MARCA_AGENT_ROOT,
        PATH_CONFIG,
        PATH_PROMPTS,
        PATH_TEMPLATES,
        PATH_SRC,
    )

Version: 1.0.0
Created: 2025-11-16
Purpose: Path normalization for marca_agent
"""

import sys
from pathlib import Path

# === LOCAL HIERARCHY (Marca Agent) ===

# Start from THIS file's location (marca_agent/config/paths.py)
SCRIPT_DIR = Path(__file__).parent.resolve()

# Level 1: config/ directory
CONFIG_DIR = SCRIPT_DIR  # marca_agent/config/

# Level 2: marca_agent/ directory (agent root)
MARCA_AGENT_ROOT = CONFIG_DIR.parent  # marca_agent/

# === GLOBAL ORCHESTRATOR IMPORT ===

# Add codexa.app to path (3 levels up: config → marca_agent → agentes → codexa.app)
CODEXA_APP = MARCA_AGENT_ROOT.parent.parent
sys.path.insert(0, str(CODEXA_APP))

try:
    from config.paths import (
        AGENTS_ROOT,
        get_agent_dir,
        get_agent_paths,
        PATH_GLOBAL_OUTPUTS,
        PATH_GLOBAL_LOGS,
    )
    GLOBAL_ORCHESTRATOR_AVAILABLE = True
except ImportError:
    # Fallback if global orchestrator not available
    GLOBAL_ORCHESTRATOR_AVAILABLE = False
    AGENTS_ROOT = MARCA_AGENT_ROOT.parent
    PATH_GLOBAL_OUTPUTS = CODEXA_APP / "outputs"
    PATH_GLOBAL_LOGS = CODEXA_APP / "logs"


# === MARCA AGENT LOCAL PATHS ===

# Core directories
PATH_CONFIG = CONFIG_DIR
PATH_PROMPTS = MARCA_AGENT_ROOT / "prompts"
PATH_TEMPLATES = MARCA_AGENT_ROOT / "templates"
PATH_SRC = MARCA_AGENT_ROOT / "src"
PATH_SCRIPTS = MARCA_AGENT_ROOT / "scripts"
PATH_ISO_VECTORSTORE = MARCA_AGENT_ROOT / "iso_vectorstore"

# Output directories (local to this agent)
PATH_OUTPUTS = MARCA_AGENT_ROOT / "outputs"
PATH_LOGS = MARCA_AGENT_ROOT / "logs"

# Create output directories if they don't exist
PATH_OUTPUTS.mkdir(exist_ok=True)
PATH_LOGS.mkdir(exist_ok=True)


# === VALIDATION ===

def validate_paths() -> dict:
    """
    Validate that all defined paths exist.

    Returns:
        Dictionary mapping path name to existence boolean
    """
    paths_to_check = {
        'MARCA_AGENT_ROOT': MARCA_AGENT_ROOT,
        'PATH_CONFIG': PATH_CONFIG,
        'PATH_PROMPTS': PATH_PROMPTS,
        'PATH_TEMPLATES': PATH_TEMPLATES,
        'PATH_SRC': PATH_SRC,
        'PATH_SCRIPTS': PATH_SCRIPTS,
        'PATH_ISO_VECTORSTORE': PATH_ISO_VECTORSTORE,
        'PATH_OUTPUTS': PATH_OUTPUTS,
        'PATH_LOGS': PATH_LOGS,
    }

    return {name: path.exists() for name, path in paths_to_check.items()}


# === DEBUG INFO ===

if __name__ == "__main__":
    # Windows-safe symbols
    CHECK = '[OK]' if sys.platform == 'win32' else '✓'
    CROSS = '[X]' if sys.platform == 'win32' else '✗'

    print("=" * 70)
    print("Marca Agent - Path Configuration")
    print("=" * 70)
    print()

    print("LOCAL HIERARCHY:")
    print(f"  MARCA_AGENT_ROOT:     {MARCA_AGENT_ROOT}")
    print(f"  PATH_CONFIG:          {PATH_CONFIG}")
    print()

    print("GLOBAL ORCHESTRATOR:")
    if GLOBAL_ORCHESTRATOR_AVAILABLE:
        print(f"  {CHECK} Connected to global orchestrator")
        print(f"  AGENTS_ROOT:          {AGENTS_ROOT}")
        print(f"  PATH_GLOBAL_OUTPUTS:  {PATH_GLOBAL_OUTPUTS}")
    else:
        print(f"  {CROSS} Global orchestrator not available (using fallback)")
    print()

    print("LOCAL PATHS:")
    print(f"  PATH_PROMPTS:         {PATH_PROMPTS}")
    print(f"  PATH_TEMPLATES:       {PATH_TEMPLATES}")
    print(f"  PATH_SRC:             {PATH_SRC}")
    print(f"  PATH_SCRIPTS:         {PATH_SCRIPTS}")
    print(f"  PATH_ISO_VECTORSTORE: {PATH_ISO_VECTORSTORE}")
    print(f"  PATH_OUTPUTS:         {PATH_OUTPUTS}")
    print(f"  PATH_LOGS:            {PATH_LOGS}")
    print()

    print("VALIDATION:")
    validation = validate_paths()
    for name, exists in validation.items():
        symbol = CHECK if exists else CROSS
        print(f"  {symbol} {name}")
    print()

    print("=" * 70)
    if all(validation.values()):
        print(f"{CHECK} All paths validated successfully")
    else:
        print(f"{CROSS} Some paths are missing")
    print("=" * 70)
