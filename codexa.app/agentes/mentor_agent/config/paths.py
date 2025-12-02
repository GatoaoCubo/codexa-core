"""
Mentor Agent Path Configuration

Centralized path management for mentor_agent using global orchestrator.

This agent uses the global orchestrator at codexa.app/config/paths.py
and defines its own local paths for mentor-specific resources.

Usage:
    from config.paths import (
        MENTOR_AGENT_ROOT,
        PATH_CONFIG,
        PATH_PROMPTS,
        PATH_SRC,
        PATH_VOICE,
    )

Version: 1.0.0
Created: 2025-11-16
Purpose: Path normalization for mentor_agent
"""

import sys
from pathlib import Path

# === LOCAL HIERARCHY (Mentor Agent) ===

# Start from THIS file's location (mentor_agent/config/paths.py)
SCRIPT_DIR = Path(__file__).parent.resolve()

# Level 1: config/ directory
CONFIG_DIR = SCRIPT_DIR  # mentor_agent/config/

# Level 2: mentor_agent/ directory (agent root)
MENTOR_AGENT_ROOT = CONFIG_DIR.parent  # mentor_agent/

# === GLOBAL ORCHESTRATOR IMPORT ===

# Add codexa.app to path (3 levels up: config → mentor_agent → agentes → codexa.app)
CODEXA_APP = MENTOR_AGENT_ROOT.parent.parent
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
    AGENTS_ROOT = MENTOR_AGENT_ROOT.parent
    PATH_GLOBAL_OUTPUTS = CODEXA_APP / "outputs"
    PATH_GLOBAL_LOGS = CODEXA_APP / "logs"


# === MENTOR AGENT LOCAL PATHS ===

# Core directories
PATH_CONFIG = CONFIG_DIR
PATH_PROMPTS = MENTOR_AGENT_ROOT / "prompts"
PATH_SRC = MENTOR_AGENT_ROOT / "src"
PATH_SCRIPTS = MENTOR_AGENT_ROOT / "scripts"
PATH_VOICE = MENTOR_AGENT_ROOT / "voice"
PATH_COMMANDS = MENTOR_AGENT_ROOT / "commands"
PATH_EXAMPLES = MENTOR_AGENT_ROOT / "examples"
PATH_ISO_VECTORSTORE = MENTOR_AGENT_ROOT / "iso_vectorstore"

# Special directories
PATH_DISTRIBUICAO = MENTOR_AGENT_ROOT / "DISTRIBUICAO"
PATH_PROCESSADOS = MENTOR_AGENT_ROOT / "PROCESSADOS"
PATH_RASCUNHO = MENTOR_AGENT_ROOT / "RASCUNHO"
PATH_USER = MENTOR_AGENT_ROOT / "USER"
PATH_STRATEGIC_PLANS = MENTOR_AGENT_ROOT / "strategic_plans"

# Output directories (local to this agent)
PATH_OUTPUTS = MENTOR_AGENT_ROOT / "outputs"
PATH_LOGS = MENTOR_AGENT_ROOT / "logs"

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
        'MENTOR_AGENT_ROOT': MENTOR_AGENT_ROOT,
        'PATH_CONFIG': PATH_CONFIG,
        'PATH_PROMPTS': PATH_PROMPTS,
        'PATH_SRC': PATH_SRC,
        'PATH_SCRIPTS': PATH_SCRIPTS,
        'PATH_VOICE': PATH_VOICE,
        'PATH_COMMANDS': PATH_COMMANDS,
        'PATH_EXAMPLES': PATH_EXAMPLES,
        'PATH_ISO_VECTORSTORE': PATH_ISO_VECTORSTORE,
        'PATH_DISTRIBUICAO': PATH_DISTRIBUICAO,
        'PATH_PROCESSADOS': PATH_PROCESSADOS,
        'PATH_RASCUNHO': PATH_RASCUNHO,
        'PATH_USER': PATH_USER,
        'PATH_STRATEGIC_PLANS': PATH_STRATEGIC_PLANS,
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
    print("Mentor Agent - Path Configuration")
    print("=" * 70)
    print()

    print("LOCAL HIERARCHY:")
    print(f"  MENTOR_AGENT_ROOT:    {MENTOR_AGENT_ROOT}")
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
    print(f"  PATH_SRC:             {PATH_SRC}")
    print(f"  PATH_SCRIPTS:         {PATH_SCRIPTS}")
    print(f"  PATH_VOICE:           {PATH_VOICE}")
    print(f"  PATH_COMMANDS:        {PATH_COMMANDS}")
    print(f"  PATH_EXAMPLES:        {PATH_EXAMPLES}")
    print(f"  PATH_ISO_VECTORSTORE: {PATH_ISO_VECTORSTORE}")
    print(f"  PATH_DISTRIBUICAO:    {PATH_DISTRIBUICAO}")
    print(f"  PATH_PROCESSADOS:     {PATH_PROCESSADOS}")
    print(f"  PATH_STRATEGIC_PLANS: {PATH_STRATEGIC_PLANS}")
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
        missing_count = sum(1 for exists in validation.values() if not exists)
        print(f"{CROSS} {missing_count} paths are missing (optional directories)")
    print("=" * 70)
