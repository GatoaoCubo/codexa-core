#!/usr/bin/env python3
"""
13_fractal_nav_sync.py | Fractal Navigation Synchronization

Generates and synchronizes PRIME.md and README.md files across the project hierarchy
to create fractal navigation patterns that facilitate LLM navigation and user UX.

Hierarchy Levels:
    Level 1 (ROOT): codexa/
    Level 2 (SYSTEM): codexa.app/
    Level 3 (AGENTS): agentes/
    Level 4 (INDIVIDUAL): {agent}/

Usage:
    # Generate all fractal navigation files
    python builders/13_fractal_nav_sync.py

    # Dry run (preview changes)
    python builders/13_fractal_nav_sync.py --dry-run

    # Validate pathways only
    python builders/13_fractal_nav_sync.py --validate-only

Version: 1.0.0
Created: 2025-11-14
Purpose: Fractal navigation implementation
"""

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# === CONFIGURATION ===

# Import centralized path configuration
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import (
    CODEXA_AGENT_DIR,
    AGENTS_ROOT,
    CODEXA_APP,
    PROJECT_ROOT,
    PATH_TEMPLATES,
    PATH_WORKFLOWS,
    PATH_REGISTRY,
)

# Alias for backwards compatibility
AGENT_DIR = CODEXA_AGENT_DIR

# Derived paths
TEMPLATES_DIR = PATH_TEMPLATES / "docs" / "fractal"
REPORTS_DIR = PATH_WORKFLOWS / "reports"
REGISTRY_FILE = PATH_REGISTRY

# Ensure reports directory exists
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Version and date
VERSION = "1.0.0"
LAST_UPDATED = datetime.now().strftime("%Y-%m-%d")

# === DATA MODELS ===

@dataclass
class NavigationFile:
    """Represents a navigation file to be created/updated"""
    level: int
    path: Path
    template_name: str
    exists: bool
    needs_update: bool
    backup_path: Optional[Path] = None

@dataclass
class PathwayValidation:
    """Validation result for pathway cross-references"""
    source_file: Path
    target_path: str
    exists: bool
    valid: bool
    error_message: Optional[str] = None

@dataclass
class SyncReport:
    """Complete sync operation report"""
    timestamp: str
    files_processed: int
    files_created: int
    files_updated: int
    files_validated: int
    pathways_checked: int
    pathways_valid: int
    errors: List[str]
    warnings: List[str]

# === TEMPLATE LOADING ===

def load_template(template_name: str) -> str:
    """Load template content from fractal templates directory"""
    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def replace_variables(content: str, variables: Dict[str, str]) -> str:
    """Replace {VARIABLE} placeholders in template content"""
    for key, value in variables.items():
        placeholder = f"{{{key}}}"
        content = content.replace(placeholder, value)
    return content

# === AGENT REGISTRY ===

def load_agent_registry() -> Dict:
    """Load agent registry JSON"""
    if not REGISTRY_FILE.exists():
        print(f"Warning: Agent registry not found at {REGISTRY_FILE}")
        return {"agents": {}}

    with open(REGISTRY_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# === FILE GENERATION ===

def generate_root_prime(dry_run: bool = False) -> NavigationFile:
    """Generate codexa/PRIME.md"""
    target_path = PROJECT_ROOT / "PRIME.md"

    nav_file = NavigationFile(
        level=1,
        path=target_path,
        template_name="ROOT_PRIME.md",
        exists=target_path.exists(),
        needs_update=not target_path.exists()
    )

    if dry_run:
        print(f"[DRY RUN] Would {'update' if nav_file.exists else 'create'}: {target_path}")
        return nav_file

    # Load template and replace variables
    template = load_template("ROOT_PRIME.md")

    variables = {
        "VERSION": VERSION,
        "LAST_UPDATED": LAST_UPDATED
    }

    content = replace_variables(template, variables)

    # Backup existing file
    if nav_file.exists:
        backup_path = target_path.with_suffix('.md.backup')
        shutil.copy2(target_path, backup_path)
        nav_file.backup_path = backup_path
        print(f"Backed up existing file: {backup_path}")

    # Write new content
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)

    action = "Updated" if nav_file.exists else "Created"
    print(f"{action}: {target_path}")

    return nav_file

def generate_agents_prime(dry_run: bool = False) -> NavigationFile:
    """Generate agentes/PRIME.md"""
    target_path = AGENTS_ROOT / "PRIME.md"

    nav_file = NavigationFile(
        level=3,
        path=target_path,
        template_name="AGENTS_PRIME.md",
        exists=target_path.exists(),
        needs_update=not target_path.exists()
    )

    if dry_run:
        print(f"[DRY RUN] Would {'update' if nav_file.exists else 'create'}: {target_path}")
        return nav_file

    # Load template and replace variables
    template = load_template("AGENTS_PRIME.md")

    variables = {
        "VERSION": VERSION,
        "LAST_UPDATED": LAST_UPDATED
    }

    content = replace_variables(template, variables)

    # Backup existing file
    if nav_file.exists:
        backup_path = target_path.with_suffix('.md.backup')
        shutil.copy2(target_path, backup_path)
        nav_file.backup_path = backup_path
        print(f"Backed up existing file: {backup_path}")

    # Write new content
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)

    action = "Updated" if nav_file.exists else "Created"
    print(f"{action}: {target_path}")

    return nav_file

def generate_agents_readme(dry_run: bool = False) -> NavigationFile:
    """Generate agentes/README.md"""
    target_path = AGENTS_ROOT / "README.md"

    nav_file = NavigationFile(
        level=3,
        path=target_path,
        template_name="AGENTS_README.md",
        exists=target_path.exists(),
        needs_update=not target_path.exists()
    )

    if dry_run:
        print(f"[DRY RUN] Would {'update' if nav_file.exists else 'create'}: {target_path}")
        return nav_file

    # Load template and replace variables
    template = load_template("AGENTS_README.md")

    variables = {
        "VERSION": VERSION,
        "LAST_UPDATED": LAST_UPDATED
    }

    content = replace_variables(template, variables)

    # Backup existing file
    if nav_file.exists:
        backup_path = target_path.with_suffix('.md.backup')
        shutil.copy2(target_path, backup_path)
        nav_file.backup_path = backup_path
        print(f"✅ Backed up existing file: {backup_path}")

    # Write new content
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)

    action = "Updated" if nav_file.exists else "Created"
    print(f"✅ {action}: {target_path}")

    return nav_file

# === PATHWAY VALIDATION ===

def extract_pathways(file_path: Path) -> List[str]:
    """Extract pathway references from a markdown file"""
    if not file_path.exists():
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find markdown links: [text](path)
    links = re.findall(r'\[.*?\]\((.*?)\)', content)

    # Find direct file references (e.g., `../PRIME.md`)
    file_refs = re.findall(r'`([^`]+\.md)`', content)

    return links + file_refs

def validate_pathway(source_file: Path, target_path: str) -> PathwayValidation:
    """Validate a single pathway reference"""
    # Resolve relative path from source file directory
    source_dir = source_file.parent

    # Handle relative paths
    if target_path.startswith('../') or target_path.startswith('./'):
        resolved_path = (source_dir / target_path).resolve()
    elif target_path.startswith('/'):
        # Absolute path (unlikely in our case)
        resolved_path = Path(target_path)
    else:
        # Assume it's relative to source directory
        resolved_path = (source_dir / target_path).resolve()

    exists = resolved_path.exists()

    validation = PathwayValidation(
        source_file=source_file,
        target_path=target_path,
        exists=exists,
        valid=exists
    )

    if not exists:
        validation.error_message = f"Target not found: {resolved_path}"

    return validation

def validate_all_pathways(files: List[NavigationFile]) -> List[PathwayValidation]:
    """Validate all pathway cross-references in generated files"""
    validations = []

    for nav_file in files:
        if not nav_file.path.exists():
            continue

        pathways = extract_pathways(nav_file.path)

        for pathway in pathways:
            # Skip external URLs
            if pathway.startswith('http://') or pathway.startswith('https://'):
                continue

            # Skip anchors
            if pathway.startswith('#'):
                continue

            validation = validate_pathway(nav_file.path, pathway)
            validations.append(validation)

    return validations

# === REPORT GENERATION ===

def generate_report(sync_report: SyncReport, validations: List[PathwayValidation]) -> None:
    """Generate JSON and Markdown reports"""
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")

    # JSON report
    json_report_path = REPORTS_DIR / f"fractal_nav_sync_{timestamp_str}.json"
    json_data = {
        "report": asdict(sync_report),
        "pathway_validations": [
            {
                "source": str(v.source_file),
                "target": v.target_path,
                "valid": v.valid,
                "error": v.error_message
            }
            for v in validations
        ]
    }

    with open(json_report_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)

    print(f"\nJSON report: {json_report_path}")

    # Markdown report
    md_report_path = REPORTS_DIR / f"fractal_nav_sync_{timestamp_str}.md"

    md_content = f"""# Fractal Navigation Sync Report

**Timestamp**: {sync_report.timestamp}
**Version**: {VERSION}

## Summary

- **Files Processed**: {sync_report.files_processed}
- **Files Created**: {sync_report.files_created}
- **Files Updated**: {sync_report.files_updated}
- **Files Validated**: {sync_report.files_validated}
- **Pathways Checked**: {sync_report.pathways_checked}
- **Pathways Valid**: {sync_report.pathways_valid}

## Errors

"""

    if sync_report.errors:
        for error in sync_report.errors:
            md_content += f"- ERROR: {error}\n"
    else:
        md_content += "- No errors\n"

    md_content += "\n## Warnings\n\n"

    if sync_report.warnings:
        for warning in sync_report.warnings:
            md_content += f"- WARNING: {warning}\n"
    else:
        md_content += "- No warnings\n"

    md_content += "\n## Pathway Validation\n\n"

    invalid_pathways = [v for v in validations if not v.valid]
    if invalid_pathways:
        md_content += "### Invalid Pathways\n\n"
        for v in invalid_pathways:
            md_content += f"- **Source**: `{v.source_file}`\n"
            md_content += f"  - Target: `{v.target_path}`\n"
            md_content += f"  - Error: {v.error_message}\n\n"
    else:
        md_content += "- All pathways valid\n"

    with open(md_report_path, 'w', encoding='utf-8') as f:
        f.write(md_content)

    print(f"Markdown report: {md_report_path}")

# === MAIN EXECUTION ===

def main():
    # Set UTF-8 encoding for Windows console
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    parser = argparse.ArgumentParser(description="Fractal Navigation Synchronization")
    parser.add_argument('--dry-run', action='store_true', help='Preview changes without applying')
    parser.add_argument('--validate-only', action='store_true', help='Only validate pathways')
    args = parser.parse_args()

    print("=" * 80)
    print("FRACTAL NAVIGATION SYNC")
    print("=" * 80)
    print(f"Version: {VERSION}")
    print(f"Date: {LAST_UPDATED}")
    print()

    if args.validate_only:
        print("VALIDATION MODE - Checking existing files only")
        print()
    elif args.dry_run:
        print("DRY RUN MODE - No files will be modified")
        print()

    # Initialize report
    sync_report = SyncReport(
        timestamp=datetime.now().isoformat(),
        files_processed=0,
        files_created=0,
        files_updated=0,
        files_validated=0,
        pathways_checked=0,
        pathways_valid=0,
        errors=[],
        warnings=[]
    )

    generated_files = []

    try:
        if not args.validate_only:
            # Generate files
            print("Generating navigation files...")
            print()

            # Level 1: ROOT
            print("Level 1 (ROOT): codexa/")
            root_prime = generate_root_prime(args.dry_run)
            generated_files.append(root_prime)
            sync_report.files_processed += 1
            if not root_prime.exists:
                sync_report.files_created += 1
            else:
                sync_report.files_updated += 1
            print()

            # Level 3: AGENTS (agentes/)
            print("Level 3 (AGENTS): agentes/")
            agents_prime = generate_agents_prime(args.dry_run)
            agents_readme = generate_agents_readme(args.dry_run)
            generated_files.extend([agents_prime, agents_readme])
            sync_report.files_processed += 2

            for f in [agents_prime, agents_readme]:
                if not f.exists:
                    sync_report.files_created += 1
                else:
                    sync_report.files_updated += 1
            print()

        # Validate pathways
        if not args.dry_run:
            print("Validating pathways...")
            print()

            # Find all PRIME.md and README.md files to validate
            all_nav_files = []

            # Add generated files
            all_nav_files.extend(generated_files)

            # Add existing files at other levels
            existing_files = [
                PROJECT_ROOT / "README.md",
                CODEXA_APP / "PRIME.md",
                CODEXA_APP / "README.md",
            ]

            for f in existing_files:
                if f.exists():
                    all_nav_files.append(NavigationFile(
                        level=0,
                        path=f,
                        template_name="",
                        exists=True,
                        needs_update=False
                    ))

            validations = validate_all_pathways(all_nav_files)

            sync_report.pathways_checked = len(validations)
            sync_report.pathways_valid = sum(1 for v in validations if v.valid)
            sync_report.files_validated = len(all_nav_files)

            invalid_count = sync_report.pathways_checked - sync_report.pathways_valid
            if invalid_count > 0:
                sync_report.warnings.append(f"{invalid_count} invalid pathways found")
                print(f"Found {invalid_count} invalid pathways")
            else:
                print("All pathways valid")
            print()

            # Generate report
            print("Generating reports...")
            generate_report(sync_report, validations)

        print()
        print("=" * 80)
        print("SYNC COMPLETE")
        print("=" * 80)
        print(f"Files processed: {sync_report.files_processed}")
        print(f"Files created: {sync_report.files_created}")
        print(f"Files updated: {sync_report.files_updated}")
        if not args.dry_run:
            print(f"Pathways validated: {sync_report.pathways_checked}")
            print(f"Valid pathways: {sync_report.pathways_valid}")
        print()

    except Exception as e:
        sync_report.errors.append(str(e))
        print(f"\nERROR: {e}")
        if not args.dry_run:
            generate_report(sync_report, [])
        sys.exit(1)

if __name__ == "__main__":
    main()
