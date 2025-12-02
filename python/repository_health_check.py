#!/usr/bin/env python3
"""
Repository Health Check Script

Performs comprehensive validation of the TAC-7 repository structure,
documentation, and agent integrity.

Usage:
    python scripts/repository_health_check.py
    python scripts/repository_health_check.py --verbose
    python scripts/repository_health_check.py --report health_report.md
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from collections import defaultdict
from datetime import datetime, timedelta


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'


class RepositoryHealthCheck:
    """Comprehensive repository health checker"""

    def __init__(self, repo_root: Path, verbose: bool = False):
        self.repo_root = repo_root
        self.verbose = verbose
        self.issues = defaultdict(list)
        self.warnings = defaultdict(list)
        self.successes = defaultdict(list)

        # Agent configuration
        self.agents = ['anuncio-agent', 'pesquisa-agent', 'brand-agent', 'knowledge-agent']
        self.prime_files = ['.claude/prime/anuncio.md', '.claude/prime/pesquisa.md',
                           '.claude/prime/brand.md', '.claude/prime/knowledge.md']

    def log(self, message: str, level: str = 'info'):
        """Log message with color"""
        if level == 'success':
            print(f"{Colors.GREEN}[OK]{Colors.END} {message}")
        elif level == 'warning':
            print(f"{Colors.YELLOW}[WARN]{Colors.END} {message}")
        elif level == 'error':
            print(f"{Colors.RED}[ERROR]{Colors.END} {message}")
        elif level == 'info':
            if self.verbose:
                print(f"{Colors.BLUE}[INFO]{Colors.END} {message}")

    def check_agent_structure(self) -> Dict[str, bool]:
        """Check if all agents have required directory structure"""
        results = {}

        required_dirs = ['prompts', 'config', 'templates']
        required_files = ['README.md']

        for agent in self.agents:
            agent_path = self.repo_root / agent

            if not agent_path.exists():
                self.issues['agent_structure'].append(f"Agent directory missing: {agent}")
                results[agent] = False
                continue

            # Check directories
            for dir_name in required_dirs:
                dir_path = agent_path / dir_name
                if not dir_path.exists():
                    self.warnings['agent_structure'].append(
                        f"{agent}: Missing '{dir_name}' directory"
                    )

            # Check files
            for file_name in required_files:
                file_path = agent_path / file_name
                if not file_path.exists():
                    self.issues['agent_structure'].append(
                        f"{agent}: Missing '{file_name}'"
                    )
                    results[agent] = False
                else:
                    self.successes['agent_structure'].append(
                        f"{agent}: Has {file_name}"
                    )
                    results[agent] = True

        return results

    def check_prime_files(self) -> Dict[str, bool]:
        """Check if all prime files exist and are valid"""
        results = {}

        for prime_file in self.prime_files:
            prime_path = self.repo_root / prime_file
            agent_name = Path(prime_file).stem

            if not prime_path.exists():
                self.issues['prime_files'].append(f"Prime file missing: {prime_file}")
                results[agent_name] = False
            else:
                # Check basic structure
                content = prime_path.read_text(encoding='utf-8')

                required_sections = [
                    '## 🎯 Purpose',
                    '## 🤖 INSTRUCTIONS FOR AI ASSISTANTS',
                    '### When to Use',
                    '### When to Read Source'
                ]

                missing_sections = []
                for section in required_sections:
                    if section not in content:
                        missing_sections.append(section)

                if missing_sections:
                    self.issues['prime_files'].append(
                        f"{prime_file}: Missing sections: {', '.join(missing_sections)}"
                    )
                    results[agent_name] = False
                else:
                    self.successes['prime_files'].append(f"{prime_file}: All sections present")
                    results[agent_name] = True

        return results

    def check_scripts_directory(self) -> Dict[str, bool]:
        """Check scripts directory structure"""
        results = {}
        scripts_dir = self.repo_root / 'scripts'

        if not scripts_dir.exists():
            self.issues['scripts'].append("Scripts directory missing")
            return {'scripts_dir': False}

        # Check for key scripts
        key_scripts = [
            'validate_readme_pattern.py',
            'generate_readme_template.py',
            'repository_health_check.py'  # This script itself
        ]

        for script in key_scripts:
            script_path = scripts_dir / script
            if script_path.exists():
                self.successes['scripts'].append(f"Found: {script}")
                results[script] = True
            else:
                self.warnings['scripts'].append(f"Missing: {script}")
                results[script] = False

        return results

    def check_ci_cd_setup(self) -> Dict[str, bool]:
        """Check CI/CD configuration"""
        results = {}

        workflows_dir = self.repo_root / '.github' / 'workflows'

        if not workflows_dir.exists():
            self.warnings['ci_cd'].append(".github/workflows directory missing")
            return {'workflows_dir': False}

        # Check for validation workflow
        validation_workflow = workflows_dir / 'validate-readme-pattern.yml'
        if validation_workflow.exists():
            self.successes['ci_cd'].append("Found: validate-readme-pattern.yml")
            results['validation_workflow'] = True
        else:
            self.warnings['ci_cd'].append("Missing: validate-readme-pattern.yml")
            results['validation_workflow'] = False

        return results

    def check_documentation_completeness(self) -> Dict[str, bool]:
        """Check if key documentation files exist"""
        results = {}

        key_docs = [
            'README.md',
            'TAXONOMY_VALIDATION.md',
            'CONFIGURATION.md',
            'INSTALLATION.md',
            'docs/CI_CD_VALIDATION_GUIDE.md'
        ]

        for doc in key_docs:
            doc_path = self.repo_root / doc
            if doc_path.exists():
                self.successes['documentation'].append(f"Found: {doc}")
                results[doc] = True
            else:
                self.warnings['documentation'].append(f"Missing: {doc}")
                results[doc] = False

        return results

    def check_cross_references(self) -> Dict[str, List[str]]:
        """Check for broken cross-references in documentation"""
        broken_links = []

        # Check prime files for references to agent directories
        for prime_file in self.prime_files:
            prime_path = self.repo_root / prime_file
            if not prime_path.exists():
                continue

            content = prime_path.read_text(encoding='utf-8')
            agent_name = Path(prime_file).stem

            # Expected agent directory
            expected_agent_dir = f"{agent_name}-agent"

            # Check if prime references the correct agent directory
            if expected_agent_dir not in content:
                self.warnings['cross_references'].append(
                    f"{prime_file}: May not reference {expected_agent_dir}"
                )

        return {'broken_links': broken_links}

    def check_prompt_consistency(self) -> Dict[str, bool]:
        """Check if agents have consistent prompt structures"""
        results = {}

        for agent in self.agents:
            prompts_dir = self.repo_root / agent / 'prompts'

            if not prompts_dir.exists():
                continue

            prompt_files = list(prompts_dir.glob('*.md'))

            if len(prompt_files) == 0:
                self.warnings['prompts'].append(f"{agent}: No prompt files found")
                results[agent] = False
            else:
                self.successes['prompts'].append(
                    f"{agent}: Has {len(prompt_files)} prompt files"
                )
                results[agent] = True

        return results

    def check_documentation_coverage(self) -> Dict[str, Dict[str, bool]]:
        """Check documentation coverage for each agent"""
        results = {}

        essential_docs = ['README.md', 'QUICK_START.md']
        recommended_docs = ['ARCHITECTURE.md', 'MIGRATION_GUIDE.md']

        for agent in self.agents:
            agent_path = self.repo_root / agent
            agent_results = {}

            if not agent_path.exists():
                continue

            # Check essential docs
            for doc in essential_docs:
                doc_path = agent_path / doc
                # Also check in docs/ subdirectory
                doc_path_alt = agent_path / 'docs' / doc

                if doc_path.exists() or doc_path_alt.exists():
                    self.successes['doc_coverage'].append(f"{agent}: Has {doc}")
                    agent_results[doc] = True
                else:
                    self.issues['doc_coverage'].append(f"{agent}: Missing {doc}")
                    agent_results[doc] = False

            # Check recommended docs
            for doc in recommended_docs:
                doc_path = agent_path / doc
                doc_path_alt = agent_path / 'docs' / doc

                if doc_path.exists() or doc_path_alt.exists():
                    self.successes['doc_coverage'].append(f"{agent}: Has {doc}")
                    agent_results[doc] = True
                else:
                    self.warnings['doc_coverage'].append(f"{agent}: Recommended {doc} missing")
                    agent_results[doc] = False

            results[agent] = agent_results

        return results

    def check_link_integrity(self) -> Dict[str, List[str]]:
        """Check for broken markdown links in key documentation files"""
        broken_links = []
        total_links = 0
        valid_links = 0

        # Find all markdown files (excluding archived)
        md_files = []
        for agent in self.agents:
            agent_path = self.repo_root / agent
            if agent_path.exists():
                for md_file in agent_path.rglob('*.md'):
                    if '_archived' not in str(md_file):
                        md_files.append(md_file)

        # Also check root documentation
        for md_file in self.repo_root.glob('*.md'):
            md_files.append(md_file)

        # Pattern to find markdown links
        link_pattern = re.compile(r'\[([^\]]+)\]\(([^\)]+\.md)\)')

        # Files to skip (contain template/example links)
        skip_files = [
            'GUIA_COMPLETO_AGENTES_CRUD_REPOSITORIOS.md'  # Template file with example links
        ]

        for md_file in md_files:
            try:
                # Skip template files
                if md_file.name in skip_files:
                    continue

                content = md_file.read_text(encoding='utf-8')

                # Remove code blocks to avoid false positives
                # Remove fenced code blocks (```...```)
                content_no_code = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
                # Remove inline code (`...`)
                content_no_code = re.sub(r'`[^`]+`', '', content_no_code)

                matches = link_pattern.findall(content_no_code)

                for link_text, link_path in matches:
                    total_links += 1

                    # Skip external links and anchors
                    if link_path.startswith('http') or link_path.startswith('#'):
                        continue

                    # Skip regex patterns and placeholders
                    if '.*' in link_path or link_path in ['path.md', 'file.md']:
                        continue

                    # Resolve relative path
                    if link_path.startswith('../') or not link_path.startswith('/'):
                        target_path = (md_file.parent / link_path).resolve()
                    else:
                        target_path = (self.repo_root / link_path.lstrip('/')).resolve()

                    if target_path.exists():
                        valid_links += 1
                    else:
                        broken_links.append({
                            'file': str(md_file.relative_to(self.repo_root)),
                            'link': link_path,
                            'text': link_text
                        })
                        self.issues['link_integrity'].append(
                            f"{md_file.relative_to(self.repo_root)}: Broken link to '{link_path}'"
                        )

            except Exception as e:
                self.warnings['link_integrity'].append(
                    f"Error checking {md_file.name}: {str(e)}"
                )

        # Calculate link integrity percentage
        if total_links > 0:
            integrity_pct = (valid_links / total_links) * 100
            self.successes['link_integrity'].append(
                f"Link integrity: {integrity_pct:.1f}% ({valid_links}/{total_links} valid)"
            )

        return {'broken_links': broken_links, 'total': total_links, 'valid': valid_links}

    def check_archived_files_tracking(self) -> Dict[str, Dict[str, int]]:
        """Track archived vs active documentation files"""
        results = {}

        for agent in self.agents:
            agent_path = self.repo_root / agent

            if not agent_path.exists():
                continue

            # Count active files
            active_files = list(agent_path.rglob('*.md'))
            active_count = len([f for f in active_files if '_archived' not in str(f)])

            # Count archived files
            archived_path = agent_path / '_archived' / 'old_versions'
            archived_count = 0

            if archived_path.exists():
                archived_files = list(archived_path.glob('*.md'))
                archived_count = len(archived_files)

            results[agent] = {
                'active': active_count,
                'archived': archived_count,
                'total': active_count + archived_count
            }

            # Calculate archived ratio
            total = active_count + archived_count
            if total > 0:
                archived_ratio = (archived_count / total) * 100
                self.successes['archived_tracking'].append(
                    f"{agent}: {active_count} active, {archived_count} archived ({archived_ratio:.1f}% archived)"
                )

                # Warn if too many archived files (>50%)
                if archived_ratio > 50:
                    self.warnings['archived_tracking'].append(
                        f"{agent}: High archived ratio ({archived_ratio:.1f}%) - consider cleanup"
                    )

        return results

    def check_documentation_staleness(self) -> Dict[str, List[Dict[str, str]]]:
        """Check for documentation files that haven't been updated in 6+ months"""
        stale_docs = []
        six_months_ago = datetime.now() - timedelta(days=180)

        # Find all markdown files
        md_files = []
        for agent in self.agents:
            agent_path = self.repo_root / agent
            if agent_path.exists():
                for md_file in agent_path.rglob('*.md'):
                    if '_archived' not in str(md_file):
                        md_files.append(md_file)

        # Also check root documentation
        for md_file in self.repo_root.glob('*.md'):
            md_files.append(md_file)

        # Check special directories
        for special_dir in ['docs', 'specs', '.claude']:
            special_path = self.repo_root / special_dir
            if special_path.exists():
                for md_file in special_path.rglob('*.md'):
                    md_files.append(md_file)

        for md_file in md_files:
            try:
                mtime = datetime.fromtimestamp(md_file.stat().st_mtime)

                if mtime < six_months_ago:
                    days_old = (datetime.now() - mtime).days
                    stale_docs.append({
                        'file': str(md_file.relative_to(self.repo_root)),
                        'last_modified': mtime.strftime('%Y-%m-%d'),
                        'days_old': days_old
                    })
                    self.warnings['staleness'].append(
                        f"{md_file.relative_to(self.repo_root)}: Last updated {mtime.strftime('%Y-%m-%d')} ({days_old} days ago)"
                    )
                else:
                    # Count as success if recently updated
                    self.successes['staleness'].append(
                        f"{md_file.relative_to(self.repo_root)}: Recently updated"
                    )

            except Exception as e:
                self.warnings['staleness'].append(
                    f"Error checking {md_file.name}: {str(e)}"
                )

        # Summary
        if not stale_docs:
            self.successes['staleness'].append(
                "All documentation files updated within last 6 months"
            )
        else:
            self.warnings['staleness'].append(
                f"Found {len(stale_docs)} stale documentation files (6+ months old)"
            )

        return {'stale_docs': stale_docs}

    def check_todo_fixme_tracking(self) -> Dict[str, Dict[str, int]]:
        """Track TODO and FIXME comments in documentation"""
        results = {}
        total_todos = 0
        total_fixmes = 0

        # Find all markdown files
        md_files = []
        for agent in self.agents:
            agent_path = self.repo_root / agent
            if agent_path.exists():
                for md_file in agent_path.rglob('*.md'):
                    if '_archived' not in str(md_file):
                        md_files.append(md_file)

        # Also check root and special directories
        for md_file in self.repo_root.glob('*.md'):
            md_files.append(md_file)

        for special_dir in ['docs', 'specs', '.claude']:
            special_path = self.repo_root / special_dir
            if special_path.exists():
                for md_file in special_path.rglob('*.md'):
                    md_files.append(md_file)

        for md_file in md_files:
            try:
                content = md_file.read_text(encoding='utf-8')

                # Count TODOs (case insensitive)
                todos = re.findall(r'TODO:?', content, re.IGNORECASE)
                # Count FIXMEs (case insensitive)
                fixmes = re.findall(r'FIXME:?', content, re.IGNORECASE)

                if todos or fixmes:
                    file_rel = str(md_file.relative_to(self.repo_root))
                    results[file_rel] = {
                        'todos': len(todos),
                        'fixmes': len(fixmes)
                    }
                    total_todos += len(todos)
                    total_fixmes += len(fixmes)

                    if len(todos) + len(fixmes) > 5:
                        self.warnings['todos'].append(
                            f"{file_rel}: {len(todos)} TODO, {len(fixmes)} FIXME items (high count)"
                        )
                    else:
                        self.successes['todos'].append(
                            f"{file_rel}: {len(todos)} TODO, {len(fixmes)} FIXME items"
                        )

            except Exception as e:
                self.warnings['todos'].append(
                    f"Error checking {md_file.name}: {str(e)}"
                )

        # Summary
        if total_todos == 0 and total_fixmes == 0:
            self.successes['todos'].append(
                "No TODO/FIXME items found in documentation"
            )
        else:
            self.warnings['todos'].append(
                f"Total technical debt: {total_todos} TODO, {total_fixmes} FIXME items"
            )

        return {
            'files': results,
            'total_todos': total_todos,
            'total_fixmes': total_fixmes
        }

    def generate_report(self) -> str:
        """Generate comprehensive health report"""
        report = []
        report.append("=" * 80)
        report.append("TAC-7 REPOSITORY HEALTH CHECK REPORT")
        report.append("=" * 80)
        report.append("")

        # Summary
        total_issues = sum(len(v) for v in self.issues.values())
        total_warnings = sum(len(v) for v in self.warnings.values())
        total_successes = sum(len(v) for v in self.successes.values())

        report.append("SUMMARY")
        report.append("-" * 80)
        report.append(f"[OK] Successes: {total_successes}")
        report.append(f"[WARN] Warnings:  {total_warnings}")
        report.append(f"[ERROR] Issues:    {total_issues}")
        report.append("")

        # Overall health score
        total_checks = total_issues + total_warnings + total_successes
        if total_checks > 0:
            health_score = (total_successes / total_checks) * 100
            report.append(f"Overall Health Score: {health_score:.1f}%")

            if health_score >= 90:
                status = f"{Colors.GREEN}EXCELLENT{Colors.END}"
            elif health_score >= 75:
                status = f"{Colors.GREEN}GOOD{Colors.END}"
            elif health_score >= 60:
                status = f"{Colors.YELLOW}FAIR{Colors.END}"
            else:
                status = f"{Colors.RED}NEEDS ATTENTION{Colors.END}"

            report.append(f"Status: {status}")
        report.append("")

        # Issues section
        if self.issues:
            report.append("=" * 80)
            report.append("ISSUES (REQUIRES ACTION)")
            report.append("=" * 80)
            for category, items in self.issues.items():
                report.append(f"\n{category.upper().replace('_', ' ')}:")
                for item in items:
                    report.append(f"  [ERROR] {item}")
            report.append("")

        # Warnings section
        if self.warnings:
            report.append("=" * 80)
            report.append("WARNINGS (RECOMMENDED FIXES)")
            report.append("=" * 80)
            for category, items in self.warnings.items():
                report.append(f"\n{category.upper().replace('_', ' ')}:")
                for item in items:
                    report.append(f"  [WARN] {item}")
            report.append("")

        # Successes section (only in verbose mode)
        if self.verbose and self.successes:
            report.append("=" * 80)
            report.append("SUCCESSES")
            report.append("=" * 80)
            for category, items in self.successes.items():
                report.append(f"\n{category.upper().replace('_', ' ')}:")
                for item in items:
                    report.append(f"  [OK] {item}")
            report.append("")

        # Recommendations
        if total_issues > 0 or total_warnings > 0:
            report.append("=" * 80)
            report.append("RECOMMENDATIONS")
            report.append("=" * 80)
            report.append("")

            if self.issues.get('agent_structure'):
                report.append("1. Fix missing agent directories/files:")
                report.append("   python scripts/generate_readme_template.py --type agent --name [agent]")
                report.append("")

            if self.issues.get('prime_files'):
                report.append("2. Create/fix missing prime files:")
                report.append("   python scripts/generate_readme_template.py --type prime --name [agent]")
                report.append("")

            if total_warnings > 0:
                report.append("3. Review and address warnings to improve repository health")
                report.append("")

        report.append("=" * 80)
        report.append("END OF REPORT")
        report.append("=" * 80)

        return '\n'.join(report)

    def run_all_checks(self):
        """Run all health checks"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}Starting TAC-7 Repository Health Check...{Colors.END}\n")

        checks = [
            ("Agent Structure", self.check_agent_structure),
            ("Prime Files", self.check_prime_files),
            ("Scripts Directory", self.check_scripts_directory),
            ("CI/CD Setup", self.check_ci_cd_setup),
            ("Documentation", self.check_documentation_completeness),
            ("Cross References", self.check_cross_references),
            ("Prompt Consistency", self.check_prompt_consistency),
            ("Documentation Coverage", self.check_documentation_coverage),
            ("Link Integrity", self.check_link_integrity),
            ("Archived Files Tracking", self.check_archived_files_tracking),
            ("Documentation Staleness", self.check_documentation_staleness),
            ("TODO/FIXME Tracking", self.check_todo_fixme_tracking),
        ]

        for check_name, check_func in checks:
            self.log(f"Running check: {check_name}", 'info')
            try:
                check_func()
            except Exception as e:
                self.issues['system'].append(f"Check '{check_name}' failed: {str(e)}")

        print(f"\n{Colors.CYAN}{Colors.BOLD}Health check complete!{Colors.END}\n")

        return self.generate_report()


def main():
    parser = argparse.ArgumentParser(
        description='TAC-7 Repository Health Check',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show detailed output including successes'
    )

    parser.add_argument(
        '--report',
        type=str,
        help='Save report to file (markdown format)'
    )

    args = parser.parse_args()

    # Determine repository root
    repo_root = Path(__file__).parent.parent.resolve()

    # Run health check
    checker = RepositoryHealthCheck(repo_root, verbose=args.verbose)
    report = checker.run_all_checks()

    # Print report
    print(report)

    # Save report if requested
    if args.report:
        report_path = Path(args.report)
        # Remove color codes for file output
        report_plain = re.sub(r'\033\[\d+m', '', report)
        report_path.write_text(report_plain, encoding='utf-8')
        print(f"\n{Colors.GREEN}Report saved to: {report_path}{Colors.END}")

    # Exit with appropriate code
    total_issues = sum(len(v) for v in checker.issues.values())
    sys.exit(1 if total_issues > 0 else 0)


if __name__ == '__main__':
    main()
