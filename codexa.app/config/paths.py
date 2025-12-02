"""
Global Path Configuration for CODEXA Multi-Agent Orchestration

MASTER ORCHESTRATOR - Single source of truth for ALL agents.

This is the TOP-LEVEL path configuration at codexa.app/ that coordinates
all agents. Each agent can import from here for multi-agent workflows.

Philosophy:
- Global orchestrator for multi-agent coordination
- Type-safe Path objects (cross-platform)
- Single source of truth for all agents
- Enables $variable chaining between agents
- ADW multi-agent workflows support

Usage (from any agent):
    import sys
    from pathlib import Path

    # Add codexa.app to path (2 levels up from agent/config/)
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from config.paths import (
        AGENTS_ROOT,
        CODEXA_APP,
        PROJECT_ROOT,
        get_agent_dir,
        get_agent_paths,
        get_all_agents,
    )

    # Get paths for any agent
    anuncio_paths = get_agent_paths('anuncio')
    all_agents = get_all_agents()

Version: 2.0.0 (Global Orchestrator)
Created: 2025-11-16
Purpose: Multi-agent orchestration and coordination
"""

from pathlib import Path
from typing import Dict, List, Optional


# === GLOBAL HIERARCHY (Fractal Architecture) ===
#
# Structure:
#   codexa/                    (PROJECT_ROOT)
#   └── codexa.app/                   (CODEXA_APP) ← THIS LEVEL
#       ├── config/                   (CONFIG_DIR)
#       │   └── paths.py              ← YOU ARE HERE
#       └── agentes/                  (AGENTS_ROOT)
#           ├── codexa_agent/
#           ├── anuncio_agent/
#           ├── marca_agent/
#           └── pesquisa_agent/

# Start from THIS file's location (codexa.app/config/paths.py)
SCRIPT_DIR = Path(__file__).parent.resolve()

# Level 1: config/ directory
CONFIG_DIR = SCRIPT_DIR  # codexa.app/config/

# Level 2: codexa.app/ directory (THIS is the orchestrator level)
CODEXA_APP = CONFIG_DIR.parent  # codexa.app/

# Level 3: codexa/ directory (repository root)
PROJECT_ROOT = CODEXA_APP.parent  # codexa/

# Level 4: agentes/ directory (contains ALL agents)
AGENTS_ROOT = CODEXA_APP / "agentes"  # codexa.app/agentes/


# === GLOBAL PATHS (Shared across all agents) ===

# Top-level documentation and configuration
PATH_REGISTRY = CODEXA_APP / "51_AGENT_REGISTRY.json"
PATH_HOP_FRAMEWORK = CODEXA_APP / "42_HOP_FRAMEWORK.md"
PATH_DOCUMENTATION_INDEX = CODEXA_APP / "41_DOCUMENTATION_INDEX.md"
PATH_DOCS_CONSOLIDATED = CODEXA_APP / "docs_consolidados"
PATH_PRIME = CODEXA_APP / "PRIME.md"
PATH_README = CODEXA_APP / "README.md"

# Global outputs for multi-agent coordination
PATH_GLOBAL_OUTPUTS = CODEXA_APP / "outputs"
PATH_GLOBAL_LOGS = CODEXA_APP / "logs"


# === MULTI-AGENT ORCHESTRATION FUNCTIONS ===

def get_agent_dir(agent_name: str) -> Path:
    """
    Get the directory path for a specific agent.

    Args:
        agent_name: Name of the agent (e.g., 'anuncio_agent', 'anuncio', 'codexa')

    Returns:
        Path object pointing to the agent's directory

    Examples:
        >>> get_agent_dir('anuncio_agent')
        Path('.../agentes/anuncio_agent')

        >>> get_agent_dir('codexa')
        Path('.../agentes/codexa_agent')
    """
    # Normalize agent name (add _agent suffix if missing)
    if not agent_name.endswith('_agent'):
        agent_name = f"{agent_name}_agent"

    agent_path = AGENTS_ROOT / agent_name

    if not agent_path.exists():
        raise ValueError(f"Agent not found: {agent_name} at {agent_path}")

    return agent_path


def get_agent_paths(agent_name: str) -> Dict[str, Path]:
    """
    Get all common paths for a specific agent.

    Returns a dictionary with standard agent directory structure.
    This is useful for multi-agent workflows that need to access
    another agent's files.

    Args:
        agent_name: Name of the agent

    Returns:
        Dictionary with keys: root, builders, validators, templates,
        workflows, prompts, config, outputs

    Example:
        >>> paths = get_agent_paths('anuncio')
        >>> print(paths['templates'])
        Path('.../agentes/anuncio_agent/templates')

        >>> # Access another agent's output in a workflow
        >>> research_output = get_agent_paths('pesquisa')['outputs'] / 'research_notes.md'
    """
    agent_dir = get_agent_dir(agent_name)

    return {
        'root': agent_dir,
        'builders': agent_dir / 'builders',
        'validators': agent_dir / 'validators',
        'templates': agent_dir / 'templates',
        'workflows': agent_dir / 'workflows',
        'prompts': agent_dir / 'prompts',
        'config': agent_dir / 'config',
        'outputs': agent_dir / 'outputs',
        'logs': agent_dir / 'logs',
    }


def get_all_agents() -> List[Path]:
    """
    Get all agent directories.

    Returns:
        Sorted list of Path objects for all *_agent directories

    Example:
        >>> agents = get_all_agents()
        >>> print([a.name for a in agents])
        ['anuncio_agent', 'codexa_agent', 'marca_agent', 'pesquisa_agent']

        >>> # Orchestrate across all agents
        >>> for agent in agents:
        ...     print(f"Processing {agent.name}...")
    """
    return sorted(AGENTS_ROOT.glob("*_agent"))


def get_agent_output(agent_name: str, filename: str) -> Path:
    """
    Get path to a specific agent's output file.

    Convenience function for multi-agent workflows that chain
    outputs between agents ($variable pattern).

    Args:
        agent_name: Name of the agent
        filename: Name of the output file

    Returns:
        Path to the output file

    Example:
        >>> # In a multi-agent workflow:
        >>> # 1. pesquisa_agent generates research_notes.md
        >>> research_output = get_agent_output('pesquisa', 'research_notes.md')
        >>>
        >>> # 2. anuncio_agent uses that as input
        >>> with open(research_output) as f:
        ...     research_data = f.read()
    """
    return get_agent_paths(agent_name)['outputs'] / filename


def validate_global_paths() -> Dict[str, bool]:
    """
    Validate that all defined global paths exist.

    Returns:
        Dictionary mapping path name to existence boolean

    Example:
        >>> results = validate_global_paths()
        >>> if not all(results.values()):
        ...     print("Some paths are missing!")
    """
    paths_to_check = {
        'CODEXA_APP': CODEXA_APP,
        'PROJECT_ROOT': PROJECT_ROOT,
        'AGENTS_ROOT': AGENTS_ROOT,
        'CONFIG_DIR': CONFIG_DIR,
        'PATH_REGISTRY': PATH_REGISTRY,
        'PATH_HOP_FRAMEWORK': PATH_HOP_FRAMEWORK,
        'PATH_DOCUMENTATION_INDEX': PATH_DOCUMENTATION_INDEX,
        'PATH_PRIME': PATH_PRIME,
        'PATH_README': PATH_README,
    }

    return {name: path.exists() for name, path in paths_to_check.items()}


def get_agent_count() -> int:
    """
    Get total number of agents in the system.

    Returns:
        Number of agent directories found

    Example:
        >>> print(f"System has {get_agent_count()} agents")
        System has 4 agents
    """
    return len(get_all_agents())


# === DEBUG INFO ===
# Print path info when running this file directly

if __name__ == "__main__":
    import sys

    # Windows-safe symbols
    CHECK = '[OK]' if sys.platform == 'win32' else '✓'
    CROSS = '[X]' if sys.platform == 'win32' else '✗'

    print("=" * 70)
    print("CODEXA Global Orchestrator - Path Configuration")
    print("=" * 70)
    print()

    print("GLOBAL HIERARCHY:")
    print(f"  PROJECT_ROOT:       {PROJECT_ROOT}")
    print(f"  CODEXA_APP:         {CODEXA_APP}")
    print(f"  AGENTS_ROOT:        {AGENTS_ROOT}")
    print(f"  CONFIG_DIR:         {CONFIG_DIR}")
    print()

    print("GLOBAL PATHS:")
    print(f"  PATH_REGISTRY:      {PATH_REGISTRY}")
    print(f"  PATH_HOP_FRAMEWORK: {PATH_HOP_FRAMEWORK}")
    print(f"  PATH_PRIME:         {PATH_PRIME}")
    print(f"  PATH_README:        {PATH_README}")
    print()

    print("VALIDATION:")
    validation = validate_global_paths()
    for name, exists in validation.items():
        symbol = CHECK if exists else CROSS
        print(f"  {symbol} {name}")
    print()

    print(f"AGENTS ({get_agent_count()} total):")
    agents = get_all_agents()
    for agent in agents:
        print(f"  - {agent.name}")
        # Show agent structure
        paths = get_agent_paths(agent.name.replace('_agent', ''))
        for key, path in paths.items():
            exists = path.exists()
            symbol = CHECK if exists else CROSS
            print(f"      {symbol} {key:12} {path.name}/")
    print()

    print("=" * 70)
    print(f"{CHECK} Global orchestrator paths ready for multi-agent workflows")
    print("=" * 70)
