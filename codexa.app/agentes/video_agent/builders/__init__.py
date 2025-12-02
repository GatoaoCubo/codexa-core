"""
builders/__init__.py - Video Agent Builders Package

Exports all builder classes for the 5-stage video generation pipeline.

Note: Builder files are named with numeric prefixes (01_, 02_, etc.) for ordering.
This __init__.py uses importlib to load them properly since Python modules
cannot start with numbers.

Author: CODEXA Meta-Constructor
Version: 1.0.0
"""

import importlib.util
from pathlib import Path

# Get the directory containing this __init__.py
_BUILDERS_DIR = Path(__file__).parent


def _load_module(filename: str, class_name: str):
    """
    Load a module from a file with numeric prefix.

    Args:
        filename: Name of the .py file (e.g., "01_concept_builder.py")
        class_name: Name of the class to extract

    Returns:
        The class object
    """
    filepath = _BUILDERS_DIR / filename

    if not filepath.exists():
        raise ImportError(f"Builder file not found: {filepath}")

    # Create module name without numeric prefix for cleaner namespace
    module_name = filename.replace(".py", "").lstrip("0123456789_")

    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return getattr(module, class_name)


# Load all builder classes
ConceptBuilder = _load_module("01_concept_builder.py", "ConceptBuilder")
ScriptBuilder = _load_module("02_script_builder.py", "ScriptBuilder")
VisualBuilder = _load_module("03_visual_builder.py", "VisualBuilder")
ProductionBuilder = _load_module("04_production_builder.py", "ProductionBuilder")
EditingBuilder = _load_module("05_editing_builder.py", "EditingBuilder")

# Export list for "from builders import *"
__all__ = [
    "ConceptBuilder",
    "ScriptBuilder",
    "VisualBuilder",
    "ProductionBuilder",
    "EditingBuilder",
]
