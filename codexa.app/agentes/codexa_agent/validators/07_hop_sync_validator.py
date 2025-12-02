#!/usr/bin/env python3
"""
HOP Synchronization Validator
Version: 2.0.0
Updated: 2025-11-24

Validates that HOP orchestrators (main_agent_hop.md) are synchronized
with low-level prompts they reference.

Features:
- Validates prompt references in HOPs
- Detects missing and unused prompts
- Generates ##report (JSON + MD) following REPORT_STANDARD

Usage:
    python validators/07_hop_sync_validator.py
    python validators/07_hop_sync_validator.py --agent anuncio-agent
    python validators/07_hop_sync_validator.py --output-dir reports/
"""

import argparse
import re
import sys
import io
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional

# Import centralized path configuration
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import AGENTS_ROOT

# Import report generator for ##report standard
try:
    from validators.report_generator import ValidatorReportGenerator
    REPORT_GENERATOR_AVAILABLE = True
except ImportError:
    REPORT_GENERATOR_AVAILABLE = False

# Força UTF-8 encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class HOPValidator:
    """Validates HOP orchestrator synchronization"""

    VERSION = "2.0.0"

    def __init__(self, repo_root: Path, output_dir: Optional[Path] = None):
        self.repo_root = repo_root
        self.output_dir = output_dir
        self.agents = ['anuncio-agent', 'pesquisa-agent', 'brand-agent', 'knowledge-agent']
        self.issues = []
        self.warnings = []
        self.successes = []

        # Initialize report generator if available
        if REPORT_GENERATOR_AVAILABLE:
            self.reporter = ValidatorReportGenerator("hop_sync_validator", self.VERSION)
        else:
            self.reporter = None

    def extract_prompt_references(self, content: str) -> Set[str]:
        """
        Extract references to prompt files from HOP orchestrator

        Looks for patterns like:
        - prompts/titulo_generator.md
        - titulo_generator.md
        - [[titulo_generator]]
        - Execute: titulo_generator
        """
        references = set()

        # Pattern 1: Direct file references
        pattern1 = r'prompts/([a-zA-Z0-9_]+)\.md'
        references.update(re.findall(pattern1, content))

        # Pattern 2: Markdown links
        pattern2 = r'\[.*?\]\(([a-zA-Z0-9_]+)\.md\)'
        references.update(re.findall(pattern2, content))

        # Pattern 3: Wiki-style links
        pattern3 = r'\[\[([a-zA-Z0-9_]+)\]\]'
        references.update(re.findall(pattern3, content))

        # Pattern 4: Execute/Call statements
        pattern4 = r'(?:Execute|Call|Run|Use):\s*([a-zA-Z0-9_]+)'
        references.update(re.findall(pattern4, content, re.IGNORECASE))

        # Pattern 5: Quoted prompt names
        pattern5 = r'["\']([a-zA-Z0-9_]+)["\']\.md'
        references.update(re.findall(pattern5, content))

        return references

    def validate_agent_hop(self, agent_name: str) -> Dict:
        """Validate HOP sync for a single agent"""
        agent_path = self.repo_root / agent_name
        prompts_dir = agent_path / 'prompts'

        result = {
            'agent': agent_name,
            'hop_exists': False,
            'missing_prompts': [],
            'unused_prompts': [],
            'referenced_prompts': set(),
            'available_prompts': set(),
            'status': 'unknown'
        }

        # Check if HOP exists
        hop_file = prompts_dir / 'main_agent_hop.md'
        if not hop_file.exists():
            # Try alternative names
            alternatives = ['main_agent_HOP.md', 'orchestrator.md', 'high_order_prompt.md']
            for alt in alternatives:
                alt_path = prompts_dir / alt
                if alt_path.exists():
                    hop_file = alt_path
                    break

        if not hop_file.exists():
            result['status'] = 'no_hop'
            self.warnings.append(f"{agent_name}: No HOP orchestrator found")
            return result

        result['hop_exists'] = True
        result['hop_file'] = str(hop_file.relative_to(self.repo_root))

        # Read HOP content
        try:
            hop_content = hop_file.read_text(encoding='utf-8')
        except Exception as e:
            result['status'] = 'error'
            self.issues.append(f"{agent_name}: Error reading HOP: {e}")
            return result

        # Extract prompt references
        result['referenced_prompts'] = self.extract_prompt_references(hop_content)

        # Get available prompts
        if prompts_dir.exists():
            for prompt_file in prompts_dir.glob('*.md'):
                # Skip HOP itself and historical files
                if prompt_file.name.lower() in ['main_agent_hop.md', 'readme.md']:
                    continue
                if '_historical' in str(prompt_file):
                    continue

                result['available_prompts'].add(prompt_file.stem)

        # Find missing prompts
        for ref in result['referenced_prompts']:
            if ref not in result['available_prompts']:
                result['missing_prompts'].append(ref)

        # Find unused prompts (available but not referenced)
        for available in result['available_prompts']:
            if available not in result['referenced_prompts']:
                # Skip special files
                if available.endswith('_hop') or available.startswith('main_agent'):
                    continue
                result['unused_prompts'].append(available)

        # Determine status
        if result['missing_prompts']:
            result['status'] = 'error'
            self.issues.append(
                f"{agent_name}: HOP references missing prompts: {', '.join(result['missing_prompts'])}"
            )
            # Add to structured report
            if self.reporter:
                for missing in result['missing_prompts']:
                    self.reporter.add_issue(
                        file=str(hop_file.relative_to(self.repo_root)),
                        severity="error",
                        message=f"Missing referenced prompt: {missing}.md",
                        rule="HOP-001",
                        fix_suggestion=f"Create {missing}.md or remove reference from HOP"
                    )
        elif len(result['unused_prompts']) > len(result['available_prompts']) * 0.5:
            result['status'] = 'warning'
            self.warnings.append(
                f"{agent_name}: Many unused prompts ({len(result['unused_prompts'])}): {', '.join(result['unused_prompts'][:3])}..."
            )
            # Add to structured report
            if self.reporter:
                for unused in result['unused_prompts'][:5]:
                    self.reporter.add_issue(
                        file=f"{agent_name}/prompts/{unused}.md",
                        severity="warning",
                        message=f"Prompt not referenced in HOP",
                        rule="HOP-002",
                        fix_suggestion="Add reference to HOP or move to _archived/"
                    )
        else:
            result['status'] = 'ok'
            self.successes.append(
                f"{agent_name}: HOP synchronized ({len(result['referenced_prompts'])} prompts)"
            )

        return result

    def validate_all_agents(self) -> List[Dict]:
        """Validate HOP sync for all agents"""
        results = []

        for agent_name in self.agents:
            agent_path = self.repo_root / agent_name
            if not agent_path.exists():
                self.warnings.append(f"{agent_name}: Agent directory not found")
                continue

            result = self.validate_agent_hop(agent_name)
            results.append(result)

        return results

    def generate_report(self, results: List[Dict]) -> str:
        """Generate validation report"""
        report = []
        report.append("=" * 80)
        report.append("HOP SYNCHRONIZATION VALIDATION REPORT")
        report.append("=" * 80)
        report.append("")

        # Summary
        total_issues = len(self.issues)
        total_warnings = len(self.warnings)
        total_successes = len(self.successes)

        report.append("SUMMARY")
        report.append("-" * 80)
        report.append(f"✅ Agents synchronized:  {total_successes}")
        report.append(f"⚠️  Warnings:            {total_warnings}")
        report.append(f"❌ Issues found:        {total_issues}")
        report.append("")

        # Detailed results
        for result in results:
            agent = result['agent']
            status = result['status']

            if status == 'no_hop':
                report.append(f"⚠️  {agent}: NO HOP ORCHESTRATOR")
                report.append(f"   Recommendation: Create main_agent_hop.md")
                report.append("")
            elif status == 'error':
                report.append(f"❌ {agent}: ERRORS FOUND")
                report.append(f"   HOP file: {result.get('hop_file', 'N/A')}")
                if result['missing_prompts']:
                    report.append(f"   Missing prompts ({len(result['missing_prompts'])}):")
                    for prompt in result['missing_prompts']:
                        report.append(f"     - {prompt}.md")
                report.append("")
            elif status == 'warning':
                report.append(f"⚠️  {agent}: WARNINGS")
                report.append(f"   HOP file: {result.get('hop_file', 'N/A')}")
                report.append(f"   Referenced: {len(result['referenced_prompts'])} prompts")
                report.append(f"   Available:  {len(result['available_prompts'])} prompts")
                if result['unused_prompts']:
                    report.append(f"   Unused prompts ({len(result['unused_prompts'])}):")
                    for prompt in result['unused_prompts'][:5]:
                        report.append(f"     - {prompt}.md")
                    if len(result['unused_prompts']) > 5:
                        report.append(f"     ... and {len(result['unused_prompts']) - 5} more")
                report.append("")
            else:  # ok
                report.append(f"✅ {agent}: SYNCHRONIZED")
                report.append(f"   HOP file: {result.get('hop_file', 'N/A')}")
                report.append(f"   Orchestrates: {len(result['referenced_prompts'])} prompts")
                report.append(f"   Prompts: {', '.join(sorted(list(result['referenced_prompts'])[:3]))}...")
                report.append("")

        # Recommendations
        if total_issues > 0 or total_warnings > 0:
            report.append("=" * 80)
            report.append("RECOMMENDATIONS")
            report.append("=" * 80)
            report.append("")

            if total_issues > 0:
                report.append("1. FIX MISSING PROMPTS:")
                report.append("   - Create missing prompt files")
                report.append("   - OR remove references from HOP")
                report.append("")

            if total_warnings > 0:
                report.append("2. REVIEW UNUSED PROMPTS:")
                report.append("   - Add references to HOP if needed")
                report.append("   - OR move to _archived/ if obsolete")
                report.append("")

        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)

        return '\n'.join(report)

    def print_colored_report(self, results: List[Dict]):
        """Print report with colors"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}HOP Synchronization Validation{Colors.END}\n")

        for result in results:
            agent = result['agent']
            status = result['status']

            if status == 'ok':
                print(f"{Colors.GREEN}✅ {agent}: SYNCHRONIZED{Colors.END}")
                print(f"   Orchestrates: {len(result['referenced_prompts'])} prompts")
            elif status == 'warning':
                print(f"{Colors.YELLOW}⚠️  {agent}: WARNINGS{Colors.END}")
                print(f"   Unused: {len(result['unused_prompts'])} prompts")
            elif status == 'error':
                print(f"{Colors.RED}❌ {agent}: ERRORS{Colors.END}")
                print(f"   Missing: {len(result['missing_prompts'])} prompts")
            elif status == 'no_hop':
                print(f"{Colors.YELLOW}⚠️  {agent}: NO HOP{Colors.END}")

        print("")
        print(f"Total: {Colors.GREEN}{len(self.successes)} OK{Colors.END} | "
              f"{Colors.YELLOW}{len(self.warnings)} Warnings{Colors.END} | "
              f"{Colors.RED}{len(self.issues)} Errors{Colors.END}")
        print("")

    def generate_structured_report(self, results: List[Dict]) -> Optional[str]:
        """
        Generate structured ##report (JSON + MD).

        Returns:
            Path to generated report, or None if reporter not available
        """
        if not self.reporter or not self.output_dir:
            return None

        # Add recommendations based on issues
        if len(self.issues) > 0:
            self.reporter.add_recommendation("Fix all missing prompt references before proceeding")
        if len(self.warnings) > 0:
            self.reporter.add_recommendation("Review unused prompts - archive or integrate into HOP")
        if len(self.successes) == len(results):
            self.reporter.add_recommendation("All agents synchronized - ready for deployment")

        # Generate report
        report = self.reporter.generate(
            target=f"{len(self.agents)} agents",
            passed=len(self.successes),
            failed=len([r for r in results if r['status'] == 'error']),
            warnings=len(self.warnings),
            output_dir=self.output_dir
        )

        # Print summary
        self.reporter.print_summary(report)

        return str(self.output_dir / f"{self.reporter.execution_id}.json")


def main():
    parser = argparse.ArgumentParser(
        description='Validate HOP orchestrator synchronization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python validators/07_hop_sync_validator.py
    python validators/07_hop_sync_validator.py --agent anuncio-agent
    python validators/07_hop_sync_validator.py --output-dir reports/

##report Standard:
    When --output-dir is specified, generates:
    - {execution_id}.json (machine-parsable)
    - {execution_id}.md (human-readable)
"""
    )

    parser.add_argument(
        '--agent',
        type=str,
        help='Validate specific agent only'
    )

    parser.add_argument(
        '--report',
        type=str,
        help='Save text report to file (legacy)'
    )

    parser.add_argument(
        '--output-dir',
        type=str,
        help='Directory for ##report output (JSON + MD)'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output'
    )

    args = parser.parse_args()

    # Get repo root (agents directory)
    repo_root = AGENTS_ROOT

    # Parse output directory
    output_dir = Path(args.output_dir) if args.output_dir else None

    # Create validator
    validator = HOPValidator(repo_root, output_dir=output_dir)

    # Validate
    if args.agent:
        validator.agents = [args.agent]

    results = validator.validate_all_agents()

    # Print colored report
    validator.print_colored_report(results)

    # Generate text report
    report = validator.generate_report(results)

    if args.verbose:
        print(report)

    # Save legacy report if requested
    if args.report:
        report_path = Path(args.report)
        # Remove color codes
        report_plain = re.sub(r'\033\[\d+m', '', report)
        report_path.write_text(report_plain, encoding='utf-8')
        print(f"{Colors.GREEN}[OK] Report saved to: {report_path}{Colors.END}")

    # Generate structured ##report if output-dir specified
    if output_dir:
        report_path = validator.generate_structured_report(results)
        if report_path:
            print(f"{Colors.GREEN}[OK] ##report saved to: {output_dir}/{Colors.END}")

    # Exit code
    sys.exit(1 if len(validator.issues) > 0 else 0)


if __name__ == '__main__':
    main()
