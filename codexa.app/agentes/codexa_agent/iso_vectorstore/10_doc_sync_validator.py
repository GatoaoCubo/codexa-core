#!/usr/bin/env python3
"""
12_doc_sync_validator.py | Documentation Synchronization Validator

Validates that all agent documentation is synchronized and consistent:
- All 4 files present (README, PRIME, INSTRUCTIONS, SETUP)
- Version consistency across all docs
- README structure ↔ filesystem accuracy
- INSTRUCTIONS ↔ prompts/ directory sync
- Registry ↔ documentation accuracy

Usage:
    # Validate single agent
    uv run validators/12_doc_sync_validator.py anuncio_agent

    # Validate all agents
    uv run validators/12_doc_sync_validator.py --all

    # Generate report only (no validation)
    uv run validators/12_doc_sync_validator.py --audit

Version: 1.0.0
Created: 2025-11-14
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# === DATA MODELS ===

@dataclass
class DocumentationFile:
    """Represents a documentation file"""
    path: Path
    exists: bool
    version: Optional[str] = None
    last_updated: Optional[str] = None
    line_count: int = 0
    variables_found: List[str] = field(default_factory=list)

@dataclass
class AgentDocumentation:
    """Complete documentation state for an agent"""
    name: str
    path: Path
    readme: DocumentationFile
    prime: DocumentationFile
    instructions: DocumentationFile
    setup: DocumentationFile
    prompts_count: int = 0
    config_count: int = 0
    structure_declared: List[str] = field(default_factory=list)
    structure_actual: List[str] = field(default_factory=list)
    registry_entry: Optional[Dict] = None

@dataclass
class ValidationResult:
    """Validation result for a single check"""
    check_name: str
    passed: bool
    score: float  # 0.0 to 1.0
    message: str
    details: Optional[Dict] = None

@dataclass
class AgentValidationReport:
    """Complete validation report for an agent"""
    agent_name: str
    timestamp: str
    results: List[ValidationResult]
    overall_score: float
    quality_level: str  # EXCELLENT, GOOD, FAIR, POOR
    critical_errors: List[str]
    warnings: List[str]
    recommendations: List[str]

# === UTILITY FUNCTIONS ===

def extract_version(content: str) -> Optional[str]:
    """Extract version from documentation content"""
    patterns = [
        r'\*\*Version\*\*:\s*([0-9]+\.[0-9]+\.[0-9]+)',
        r'Version:\s*([0-9]+\.[0-9]+\.[0-9]+)',
        r'v([0-9]+\.[0-9]+\.[0-9]+)',
        r'"version":\s*"([0-9]+\.[0-9]+\.[0-9]+)"'
    ]

    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return None

def extract_last_updated(content: str) -> Optional[str]:
    """Extract last updated date from documentation"""
    patterns = [
        r'\*\*Last Updated\*\*:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})',
        r'Last Updated:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})',
        r'Updated:\s*([0-9]{4}-[0-9]{2}-[0-9]{2})',
        r'"updated":\s*"([0-9]{4}-[0-9]{2}-[0-9]{2})"'
    ]

    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return None

def count_lines(file_path: Path) -> int:
    """Count lines in file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except Exception:
        return 0

def find_variables(content: str) -> List[str]:
    """Find [VARIABLE] placeholders in content

    Excludes common non-variable patterns like [OK], [FAIL], [WARN]
    """
    # Common patterns that look like variables but aren't
    EXCLUDED_PATTERNS = {'OK', 'FAIL', 'WARN', 'TIP', 'NOTE', 'INFO', 'ERROR'}

    all_variables = re.findall(r'\[([A-Z_][A-Z0-9_]*)\]', content)
    return [v for v in all_variables if v not in EXCLUDED_PATTERNS]

def scan_directory_tree(path: Path) -> List[str]:
    """Scan directory and return list of subdirectories"""
    if not path.exists():
        return []

    dirs = []
    for item in path.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            dirs.append(item.name)
    return sorted(dirs)

def extract_readme_structure(content: str) -> List[str]:
    """Extract declared structure from README.md"""
    structure = []
    in_structure_section = False

    for line in content.split('\n'):
        if '## STRUCTURE' in line or '## 📁 STRUCTURE' in line or '## 📂 PROJECT STRUCTURE' in line:
            in_structure_section = True
            continue

        if in_structure_section:
            if line.startswith('##'):  # Next section
                break
            # Match directory entries like "├── config/" or "│   ├── builders/"
            match = re.search(r'[├└│]\s*──\s*([a-z_]+)/', line)
            if match:
                structure.append(match.group(1))

    return sorted(set(structure))

def load_documentation_file(file_path: Path) -> DocumentationFile:
    """Load and analyze a documentation file"""
    doc = DocumentationFile(path=file_path, exists=file_path.exists())

    if doc.exists:
        try:
            content = file_path.read_text(encoding='utf-8')
            doc.version = extract_version(content)
            doc.last_updated = extract_last_updated(content)
            doc.line_count = len(content.split('\n'))
            doc.variables_found = find_variables(content)
        except Exception as e:
            print(f"⚠️  Error reading {file_path}: {e}")

    return doc

def load_agent_documentation(agent_path: Path, registry: Optional[Dict] = None) -> AgentDocumentation:
    """Load all documentation for an agent"""
    agent_name = agent_path.name

    # Load documentation files
    readme = load_documentation_file(agent_path / 'README.md')
    prime = load_documentation_file(agent_path / 'PRIME.md')

    # Check for INSTRUCTIONS (with or without agent name suffix)
    instructions_path = agent_path / f'INSTRUCTIONS_{agent_name}.md'
    if not instructions_path.exists():
        instructions_path = agent_path / 'INSTRUCTIONS.md'
    instructions = load_documentation_file(instructions_path)

    setup = load_documentation_file(agent_path / 'SETUP.md')

    # Count prompts and configs
    prompts_dir = agent_path / 'prompts'
    config_dir = agent_path / 'config'

    prompts_count = len(list(prompts_dir.glob('*.md'))) if prompts_dir.exists() else 0
    config_count = len(list(config_dir.glob('*.json'))) if config_dir.exists() else 0

    # Extract structure
    structure_declared = []
    structure_actual = scan_directory_tree(agent_path)

    if readme.exists:
        readme_content = readme.path.read_text(encoding='utf-8')
        structure_declared = extract_readme_structure(readme_content)

    # Load registry entry
    registry_entry = None
    if registry and agent_name in registry.get('agents', {}):
        registry_entry = registry['agents'][agent_name]

    return AgentDocumentation(
        name=agent_name,
        path=agent_path,
        readme=readme,
        prime=prime,
        instructions=instructions,
        setup=setup,
        prompts_count=prompts_count,
        config_count=config_count,
        structure_declared=structure_declared,
        structure_actual=structure_actual,
        registry_entry=registry_entry
    )

# === VALIDATION FUNCTIONS ===

def validate_files_present(agent_doc: AgentDocumentation) -> ValidationResult:
    """Validate that all 4 documentation files are present"""
    files = {
        'README.md': agent_doc.readme.exists,
        'PRIME.md': agent_doc.prime.exists,
        'INSTRUCTIONS.md': agent_doc.instructions.exists,
        'SETUP.md': agent_doc.setup.exists
    }

    present_count = sum(files.values())
    score = present_count / 4.0

    missing = [name for name, exists in files.items() if not exists]

    if score == 1.0:
        message = "✅ All 4 documentation files present"
    else:
        message = f"⚠️  Missing {len(missing)} file(s): {', '.join(missing)}"

    return ValidationResult(
        check_name="files_present",
        passed=score >= 0.75,  # At least 3 of 4 files
        score=score,
        message=message,
        details={'missing_files': missing}
    )

def validate_version_consistency(agent_doc: AgentDocumentation) -> ValidationResult:
    """Validate that all files have consistent versions"""
    versions = {}

    if agent_doc.readme.exists and agent_doc.readme.version:
        versions['README.md'] = agent_doc.readme.version
    if agent_doc.prime.exists and agent_doc.prime.version:
        versions['PRIME.md'] = agent_doc.prime.version
    if agent_doc.instructions.exists and agent_doc.instructions.version:
        versions['INSTRUCTIONS.md'] = agent_doc.instructions.version
    if agent_doc.setup.exists and agent_doc.setup.version:
        versions['SETUP.md'] = agent_doc.setup.version

    if not versions:
        return ValidationResult(
            check_name="version_consistency",
            passed=False,
            score=0.0,
            message="⚠️  No versions found in documentation",
            details={'versions': {}}
        )

    unique_versions = set(versions.values())

    if len(unique_versions) == 1:
        version = list(unique_versions)[0]
        return ValidationResult(
            check_name="version_consistency",
            passed=True,
            score=1.0,
            message=f"✅ All files have consistent version: {version}",
            details={'versions': versions}
        )
    else:
        return ValidationResult(
            check_name="version_consistency",
            passed=False,
            score=0.0,
            message=f"❌ Version mismatch: {dict(versions)}",
            details={'versions': versions}
        )

def validate_structure_sync(agent_doc: AgentDocumentation) -> ValidationResult:
    """Validate that README structure matches filesystem"""
    declared = set(agent_doc.structure_declared)
    actual = set(agent_doc.structure_actual)

    if not declared:
        return ValidationResult(
            check_name="structure_sync",
            passed=False,
            score=0.5,
            message="⚠️  README has no STRUCTURE section",
            details={'declared': [], 'actual': list(actual)}
        )

    # Calculate sync score
    matches = declared & actual
    missing = declared - actual
    extra = actual - declared

    if len(declared) > 0:
        score = len(matches) / len(declared)
    else:
        score = 1.0 if len(actual) == 0 else 0.0

    if score >= 0.95:
        message = f"✅ Structure sync: {len(matches)}/{len(declared)} directories match"
    elif score >= 0.75:
        message = f"⚠️  Structure sync: {len(matches)}/{len(declared)} directories match"
    else:
        message = f"❌ Structure sync poor: {len(matches)}/{len(declared)} directories match"

    details = {
        'declared': sorted(list(declared)),
        'actual': sorted(list(actual)),
        'matches': sorted(list(matches)),
        'missing_from_filesystem': sorted(list(missing)),
        'not_in_readme': sorted(list(extra))
    }

    return ValidationResult(
        check_name="structure_sync",
        passed=score >= 0.75,
        score=score,
        message=message,
        details=details
    )

def validate_line_limits(agent_doc: AgentDocumentation) -> ValidationResult:
    """Validate that no file exceeds 1000 lines"""
    MAX_LINES = 1000

    files_over_limit = []

    for file_name, doc_file in [
        ('README.md', agent_doc.readme),
        ('PRIME.md', agent_doc.prime),
        ('INSTRUCTIONS.md', agent_doc.instructions),
        ('SETUP.md', agent_doc.setup)
    ]:
        if doc_file.exists and doc_file.line_count > MAX_LINES:
            files_over_limit.append((file_name, doc_file.line_count))

    if not files_over_limit:
        return ValidationResult(
            check_name="line_limits",
            passed=True,
            score=1.0,
            message=f"✅ All files ≤{MAX_LINES} lines",
            details={'max_lines': MAX_LINES}
        )
    else:
        message = f"❌ {len(files_over_limit)} file(s) exceed {MAX_LINES} lines: " + \
                  ', '.join(f"{name} ({lines}L)" for name, lines in files_over_limit)
        return ValidationResult(
            check_name="line_limits",
            passed=False,
            score=0.0,
            message=message,
            details={'over_limit': files_over_limit, 'max_lines': MAX_LINES}
        )

def validate_no_template_variables(agent_doc: AgentDocumentation) -> ValidationResult:
    """Validate that no [VARIABLE] placeholders remain

    Note: A small number of [VARIABLES] (<=15) is acceptable for documentation
    examples and explanatory text (e.g., explaining how templates work)
    """
    variables_found = {}
    ACCEPTABLE_THRESHOLD = 15  # Allow up to 15 variables for documentation examples

    for file_name, doc_file in [
        ('README.md', agent_doc.readme),
        ('PRIME.md', agent_doc.prime),
        ('INSTRUCTIONS.md', agent_doc.instructions),
        ('SETUP.md', agent_doc.setup)
    ]:
        if doc_file.exists and doc_file.variables_found:
            variables_found[file_name] = doc_file.variables_found

    total_vars = sum(len(vars) for vars in variables_found.values())

    if total_vars == 0:
        return ValidationResult(
            check_name="no_template_variables",
            passed=True,
            score=1.0,
            message="[OK] No template [VARIABLES] found",
            details={}
        )
    elif total_vars <= ACCEPTABLE_THRESHOLD:
        return ValidationResult(
            check_name="no_template_variables",
            passed=True,
            score=0.9,  # Slightly lower score but still passing
            message=f"[OK] {total_vars} [VARIABLES] found (acceptable for documentation examples)",
            details={'variables_by_file': variables_found, 'threshold': ACCEPTABLE_THRESHOLD}
        )
    else:
        message = f"[FAIL] Found {total_vars} template variable(s) in {len(variables_found)} file(s) (threshold: {ACCEPTABLE_THRESHOLD})"
        return ValidationResult(
            check_name="no_template_variables",
            passed=False,
            score=0.0,
            message=message,
            details={'variables_by_file': variables_found, 'threshold': ACCEPTABLE_THRESHOLD}
        )

def validate_registry_sync(agent_doc: AgentDocumentation) -> ValidationResult:
    """Validate that agent is in registry and metadata matches"""
    if not agent_doc.registry_entry:
        return ValidationResult(
            check_name="registry_sync",
            passed=False,
            score=0.0,
            message="❌ Agent not found in AGENT_REGISTRY.json",
            details={}
        )

    # Check key fields
    checks = []

    # Version check
    registry_version = agent_doc.registry_entry.get('version')
    readme_version = agent_doc.readme.version if agent_doc.readme.exists else None

    if registry_version and readme_version:
        if registry_version == readme_version:
            checks.append(True)
        else:
            checks.append(False)

    # Prompts count check (if specified in registry)
    registry_prompts = agent_doc.registry_entry.get('prompts_count')
    if registry_prompts is not None:
        if registry_prompts == agent_doc.prompts_count:
            checks.append(True)
        else:
            checks.append(False)

    score = sum(checks) / len(checks) if checks else 1.0

    if score == 1.0:
        message = "✅ Registry metadata matches documentation"
    else:
        message = f"⚠️  Registry metadata partially matches ({int(score*100)}%)"

    return ValidationResult(
        check_name="registry_sync",
        passed=score >= 0.75,
        score=score,
        message=message,
        details={
            'registry_entry': agent_doc.registry_entry,
            'prompts_count_match': registry_prompts == agent_doc.prompts_count if registry_prompts else None
        }
    )

def validate_agent(agent_doc: AgentDocumentation) -> AgentValidationReport:
    """Run all validations on an agent"""
    from datetime import datetime

    results = [
        validate_files_present(agent_doc),
        validate_version_consistency(agent_doc),
        validate_structure_sync(agent_doc),
        validate_line_limits(agent_doc),
        validate_no_template_variables(agent_doc),
        validate_registry_sync(agent_doc)
    ]

    # Calculate overall score (weighted)
    weights = {
        'files_present': 0.25,
        'version_consistency': 0.20,
        'structure_sync': 0.15,
        'line_limits': 0.10,
        'no_template_variables': 0.15,
        'registry_sync': 0.15
    }

    overall_score = sum(
        result.score * weights.get(result.check_name, 0.0)
        for result in results
    )

    # Determine quality level
    if overall_score >= 0.90:
        quality_level = "EXCELLENT"
    elif overall_score >= 0.85:
        quality_level = "GOOD"
    elif overall_score >= 0.75:
        quality_level = "FAIR"
    else:
        quality_level = "POOR"

    # Extract critical errors, warnings, recommendations
    critical_errors = [r.message for r in results if not r.passed and r.score < 0.5]
    warnings = [r.message for r in results if not r.passed and r.score >= 0.5]

    recommendations = []
    if overall_score < 0.85:
        for result in results:
            if result.score < 1.0:
                recommendations.append(f"Improve {result.check_name}: {result.message}")

    return AgentValidationReport(
        agent_name=agent_doc.name,
        timestamp=datetime.now().isoformat(),
        results=results,
        overall_score=overall_score,
        quality_level=quality_level,
        critical_errors=critical_errors,
        warnings=warnings,
        recommendations=recommendations[:5]  # Top 5 recommendations
    )

# === MAIN FUNCTIONS ===

def clean_unicode_for_windows(text: str) -> str:
    """Remove Unicode characters that cause issues on Windows console"""
    replacements = {
        "✅": "[OK]",
        "❌": "[FAIL]",
        "⚠️": "[WARN]",
        "≤": "<=",
        "≥": ">=",
        "→": "->",
        "←": "<-",
        "↔": "<->",
        "🚨": "[!]",
        "💡": "[TIP]",
        "📊": "[DATA]",
        "🔄": "[SYNC]",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def print_report(report: AgentValidationReport, verbose: bool = False):
    """Print validation report to console"""
    print(f"\n{'='*60}")
    print(f"VALIDATION REPORT: {report.agent_name}")
    print(f"{'='*60}")
    print(f"Timestamp: {report.timestamp}")
    print(f"Overall Score: {report.overall_score:.2f} ({report.quality_level})")
    print()

    # Print results
    print("Validation Checks:")
    for result in report.results:
        status = "[OK]" if result.passed else "[FAIL]"
        # Clean Unicode characters for Windows
        message = clean_unicode_for_windows(result.message)
        print(f"  {status} {result.check_name}: {result.score:.2f} - {message}")

        if verbose and result.details:
            print(f"      Details: {json.dumps(result.details, indent=6)}")

    # Print critical errors
    if report.critical_errors:
        print(f"\n[!] CRITICAL ERRORS ({len(report.critical_errors)}):")
        for error in report.critical_errors:
            error_clean = clean_unicode_for_windows(error)
            print(f"  - {error_clean}")

    # Print warnings
    if report.warnings:
        print(f"\n[WARN] WARNINGS ({len(report.warnings)}):")
        for warning in report.warnings:
            warning_clean = clean_unicode_for_windows(warning)
            print(f"  - {warning_clean}")

    # Print recommendations
    if report.recommendations:
        print(f"\n[TIP] RECOMMENDATIONS:")
        for i, rec in enumerate(report.recommendations, 1):
            rec_clean = clean_unicode_for_windows(rec)
            print(f"  {i}. {rec_clean}")

    print(f"\n{'='*60}\n")

def validate_all_agents(agents_dir: Path, registry_path: Optional[Path] = None, verbose: bool = False) -> Dict[str, AgentValidationReport]:
    """Validate all agents in directory"""
    # Load registry
    registry = None
    if registry_path and registry_path.exists():
        try:
            registry = json.loads(registry_path.read_text(encoding='utf-8'))
        except Exception as e:
            print(f"⚠️  Could not load registry: {e}")

    # Find all agent directories
    agent_dirs = [d for d in agents_dir.iterdir() if d.is_dir() and d.name.endswith('_agent')]

    print(f"\nFound {len(agent_dirs)} agent(s) to validate\n")

    reports = {}

    for agent_dir in sorted(agent_dirs):
        print(f"Validating {agent_dir.name}...")
        agent_doc = load_agent_documentation(agent_dir, registry)
        report = validate_agent(agent_doc)
        reports[agent_dir.name] = report

        if not verbose:
            status = "[OK]" if report.overall_score >= 0.85 else "[WARN]" if report.overall_score >= 0.75 else "[FAIL]"
            print(f"  {status} Score: {report.overall_score:.2f} ({report.quality_level})")

    return reports

def generate_summary_report(reports: Dict[str, AgentValidationReport]) -> str:
    """Generate summary report for all agents"""
    from datetime import datetime

    summary = []
    summary.append("# Documentation Synchronization Summary Report")
    summary.append(f"\n**Generated**: {datetime.now().isoformat()}")
    summary.append(f"**Agents Validated**: {len(reports)}\n")

    # Overall statistics
    avg_score = sum(r.overall_score for r in reports.values()) / len(reports) if reports else 0
    excellent = sum(1 for r in reports.values() if r.quality_level == "EXCELLENT")
    good = sum(1 for r in reports.values() if r.quality_level == "GOOD")
    fair = sum(1 for r in reports.values() if r.quality_level == "FAIR")
    poor = sum(1 for r in reports.values() if r.quality_level == "POOR")

    summary.append("## Summary Statistics\n")
    summary.append(f"- **Average Score**: {avg_score:.2f}")
    summary.append(f"- **EXCELLENT** (≥0.90): {excellent} agent(s)")
    summary.append(f"- **GOOD** (0.85-0.89): {good} agent(s)")
    summary.append(f"- **FAIR** (0.75-0.84): {fair} agent(s)")
    summary.append(f"- **POOR** (<0.75): {poor} agent(s)\n")

    # Agents table
    summary.append("## Agents by Quality\n")
    summary.append("| Agent | Score | Quality | Critical Errors | Warnings |")
    summary.append("|-------|-------|---------|-----------------|----------|")

    for agent_name in sorted(reports.keys()):
        report = reports[agent_name]
        summary.append(
            f"| {agent_name} | {report.overall_score:.2f} | {report.quality_level} | "
            f"{len(report.critical_errors)} | {len(report.warnings)} |"
        )

    summary.append("\n## Recommendations\n")

    # Aggregate recommendations
    all_recommendations = []
    for report in reports.values():
        all_recommendations.extend(report.recommendations)

    if all_recommendations:
        for i, rec in enumerate(all_recommendations[:10], 1):  # Top 10
            summary.append(f"{i}. {rec}")
    else:
        summary.append("✅ All agents meet quality standards!")

    return '\n'.join(summary)

def main():
    parser = argparse.ArgumentParser(description='Validate agent documentation synchronization')
    parser.add_argument('agent', nargs='?', help='Agent directory name (e.g., anuncio_agent)')
    parser.add_argument('--all', action='store_true', help='Validate all agents')
    parser.add_argument('--audit', action='store_true', help='Audit mode (report only)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output with details')
    parser.add_argument('--agents-dir', type=str, help='Path to agentes directory')
    parser.add_argument('--registry', type=str, help='Path to AGENT_REGISTRY.json')
    parser.add_argument('--output', '-o', type=str, help='Output report to file')

    args = parser.parse_args()

    # Determine agents directory
    if args.agents_dir:
        agents_dir = Path(args.agents_dir)
    else:
        # Try to find it relative to this script
        script_dir = Path(__file__).parent
        agents_dir = script_dir.parent.parent

    if not agents_dir.exists():
        print(f"❌ Agents directory not found: {agents_dir}")
        sys.exit(1)

    # Determine registry path
    if args.registry:
        registry_path = Path(args.registry)
    else:
        registry_path = agents_dir.parent / '51_AGENT_REGISTRY.json'

    # Execute validation
    if args.all or not args.agent:
        # Validate all agents
        reports = validate_all_agents(agents_dir, registry_path, args.verbose)

        # Print individual reports if verbose
        if args.verbose:
            for report in reports.values():
                print_report(report, verbose=True)

        # Generate summary
        summary = generate_summary_report(reports)
        print(clean_unicode_for_windows(summary))

        # Save to file if requested
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(summary, encoding='utf-8')
            print(f"\n[OK] Report saved to: {output_path}")

        # Exit code based on results
        avg_score = sum(r.overall_score for r in reports.values()) / len(reports) if reports else 0
        sys.exit(0 if avg_score >= 0.85 else 1)

    else:
        # Validate single agent
        agent_dir = agents_dir / args.agent

        if not agent_dir.exists():
            print(f"❌ Agent directory not found: {agent_dir}")
            sys.exit(1)

        # Load registry
        registry = None
        if registry_path.exists():
            try:
                registry = json.loads(registry_path.read_text(encoding='utf-8'))
            except Exception as e:
                print(f"⚠️  Could not load registry: {e}")

        # Validate
        agent_doc = load_agent_documentation(agent_dir, registry)
        report = validate_agent(agent_doc)

        # Print report
        print_report(report, verbose=args.verbose)

        # Exit code based on result
        sys.exit(0 if report.overall_score >= 0.85 else 1)

if __name__ == '__main__':
    main()
