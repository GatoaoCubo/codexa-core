"""
CODEXA Validators
=================

Quality gates for HOPs, documentation, and system consistency.

Available Validators:
    - 07_hop_sync_validator: TAC-7 compliance
    - 09_readme_validator: Documentation standards
    - 10_taxonomy_validator: Registry consistency
    - 12_doc_sync_validator: Full doc sync
    - 16_path_consistency_validator: Path normalization

Usage:
    # CLI
    python validators/07_hop_sync_validator.py prompts/91_*.md

    # Via codexa.py
    python codexa.py validate all
"""

__version__ = "2.0.0"

# Validators are script-based, no class imports needed
# Use subprocess to call them:
#
# import subprocess
# subprocess.run(["python", "validators/07_hop_sync_validator.py", "file.md"])
