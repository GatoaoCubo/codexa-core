#!/usr/bin/env python3
"""
Validates README.md and /prime files follow the documented pattern in TAXONOMY_VALIDATION.md

This script checks for:
1. 🤖 INSTRUCTIONS FOR AI ASSISTANTS section
2. Workflow Pattern section
3. Available Discovery Commands section
4. When to Read Source Code section
5. When to Use section (new requirement)
6. Example Workflow section
7. Integration Points section
8. Benefits checklist at end

Usage:
    # Validate all README files
    python scripts/validate_readme_pattern.py --scan-all

    # Validate specific file
    python scripts/validate_readme_pattern.py --file scripts/README.md

    # Generate validation report
    python scripts/validate_readme_pattern.py --scan-all --report readme_pattern_report.txt

    # Strict mode for CI (exit code 1 if issues found)
    python scripts/validate_readme_pattern.py --scan-all --strict

    # Check /prime files only
    python scripts/validate_readme_pattern.py --scan-prime
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


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


class PatternValidator:
    """Validates README and /prime files against the documented pattern"""

    # Required sections for README.md files
    README_REQUIRED_SECTIONS = [
        (r'🤖\s*INSTRUCTIONS FOR AI ASSISTANTS', 'AI Assistant Instructions Header'),
        (r'Workflow Pattern', 'Workflow Pattern Section'),
        (r'Available Discovery Commands', 'Discovery Commands Section'),
        (r'When to Read Source Code', 'When to Read Source Section'),
        (r'When to Use', 'When to Use Section'),  # NEW REQUIREMENT
        (r'Example Workflow', 'Example Workflow Section'),
        (r'Integration Points', 'Integration Points Section'),
        (r'✅.*Always up-to-date', 'Benefits Checklist'),
    ]

    # Required sections for /prime files
    PRIME_REQUIRED_SECTIONS = [
        (r'🎯\s*Purpose', 'Purpose Statement'),
        (r'🤖\s*INSTRUCTIONS FOR AI ASSISTANTS', 'AI Assistant Instructions Header'),
        (r'Discovery-First Workflow', 'Discovery-First Workflow Section'),
        (r'When to Read Source', 'When to Read Source Section'),
        (r'When to Use', 'When to Use Section'),  # NEW REQUIREMENT
        (r'Key Files for Context', 'Key Files Section'),
    ]

    # Pattern for "When to Use" section content
    WHEN_TO_USE_PATTERN = re.compile(
        r'###?\s*When to Use[:\s]*\n'
        r'(?P<content>(?:.*\n){3,})',  # At least 3 lines of content
        re.MULTILINE
    )

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.issues_found = []

    def find_readme_files(self) -> List[Path]:
        """Find all README.md files in repository"""
        readme_files = []

        # Exclude directories
        exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}

        for root, dirs, files in os.walk(self.repo_root):
            # Remove excluded directories from traversal
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.upper() == 'README.MD':
                    readme_files.append(Path(root) / file)

        return sorted(readme_files)

    def find_prime_files(self) -> List[Path]:
        """Find all /prime files in .claude directory"""
        prime_dir = self.repo_root / '.claude' / 'prime'

        if not prime_dir.exists():
            return []

        return sorted(prime_dir.glob('**/*'))

    def validate_section_exists(self, content: str, pattern: str, section_name: str,
                               file_path: Path) -> bool:
        """Check if a required section exists in the content"""
        if not re.search(pattern, content, re.MULTILINE | re.IGNORECASE):
            self.issues_found.append({
                'file': file_path,
                'type': 'missing_section',
                'section': section_name,
                'severity': 'error'
            })
            return False
        return True

    def validate_when_to_use_content(self, content: str, file_path: Path) -> bool:
        """Validate the 'When to Use' section has proper content"""
        match = self.WHEN_TO_USE_PATTERN.search(content)

        if not match:
            self.issues_found.append({
                'file': file_path,
                'type': 'invalid_when_to_use',
                'message': 'When to Use section exists but lacks proper content',
                'severity': 'warning'
            })
            return False

        when_to_use_content = match.group('content').strip()

        # Check for minimum content quality
        if len(when_to_use_content) < 100:  # At least 100 characters
            self.issues_found.append({
                'file': file_path,
                'type': 'insufficient_when_to_use',
                'message': f'When to Use section too short ({len(when_to_use_content)} chars, minimum 100)',
                'severity': 'warning'
            })
            return False

        # Check for bullet points or use cases
        if not (re.search(r'^[-*•]\s+', when_to_use_content, re.MULTILINE) or
                re.search(r'^\d+\.\s+', when_to_use_content, re.MULTILINE)):
            self.issues_found.append({
                'file': file_path,
                'type': 'unstructured_when_to_use',
                'message': 'When to Use section should contain bullet points or numbered list',
                'severity': 'info'
            })

        return True

    def validate_readme(self, file_path: Path) -> Dict[str, any]:
        """Validate a README.md file against the pattern"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return {
                'file': file_path,
                'status': 'error',
                'message': f'Failed to read file: {e}'
            }

        # Check if file has AI assistant instructions section
        if '🤖' not in content and 'INSTRUCTIONS FOR AI ASSISTANTS' not in content:
            # This README doesn't follow the pattern (might be legacy)
            return {
                'file': file_path,
                'status': 'skip',
                'message': 'No AI assistant instructions found (legacy README)'
            }

        # Validate all required sections
        all_sections_valid = True
        for pattern, section_name in self.README_REQUIRED_SECTIONS:
            if not self.validate_section_exists(content, pattern, section_name, file_path):
                all_sections_valid = False

        # Validate "When to Use" content quality
        if 'When to Use' in content:
            self.validate_when_to_use_content(content, file_path)

        return {
            'file': file_path,
            'status': 'valid' if all_sections_valid else 'invalid',
            'issues': [i for i in self.issues_found if i['file'] == file_path]
        }

    def validate_prime_file(self, file_path: Path) -> Dict[str, any]:
        """Validate a /prime file against the pattern"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return {
                'file': file_path,
                'status': 'error',
                'message': f'Failed to read file: {e}'
            }

        # Validate all required sections for prime files
        all_sections_valid = True
        for pattern, section_name in self.PRIME_REQUIRED_SECTIONS:
            if not self.validate_section_exists(content, pattern, section_name, file_path):
                all_sections_valid = False

        # Validate "When to Use" content quality
        if 'When to Use' in content:
            self.validate_when_to_use_content(content, file_path)

        return {
            'file': file_path,
            'status': 'valid' if all_sections_valid else 'invalid',
            'issues': [i for i in self.issues_found if i['file'] == file_path]
        }

    def generate_report(self) -> str:
        """Generate a human-readable validation report"""
        report_lines = []
        report_lines.append('=' * 80)
        report_lines.append('README PATTERN VALIDATION REPORT')
        report_lines.append('=' * 80)
        report_lines.append('')

        if not self.issues_found:
            report_lines.append(f'{Colors.GREEN}✓ All files pass validation!{Colors.END}')
            return '\n'.join(report_lines)

        # Group issues by file
        issues_by_file = {}
        for issue in self.issues_found:
            file_path = issue['file']
            if file_path not in issues_by_file:
                issues_by_file[file_path] = []
            issues_by_file[file_path].append(issue)

        # Generate report for each file
        for file_path, issues in sorted(issues_by_file.items()):
            relative_path = file_path.relative_to(self.repo_root)

            report_lines.append(f'{Colors.BOLD}{relative_path}{Colors.END}')
            report_lines.append('-' * 80)

            for issue in issues:
                severity_color = {
                    'error': Colors.RED,
                    'warning': Colors.YELLOW,
                    'info': Colors.CYAN
                }.get(issue.get('severity', 'error'), Colors.RED)

                severity = issue.get('severity', 'error').upper()
                issue_type = issue.get('type', 'unknown')

                if issue_type == 'missing_section':
                    report_lines.append(
                        f'  {severity_color}[{severity}]{Colors.END} '
                        f'Missing required section: {issue["section"]}'
                    )
                else:
                    message = issue.get('message', issue.get('section', 'Unknown issue'))
                    report_lines.append(
                        f'  {severity_color}[{severity}]{Colors.END} '
                        f'{message}'
                    )

            report_lines.append('')

        # Summary
        report_lines.append('=' * 80)
        report_lines.append('SUMMARY')
        report_lines.append('=' * 80)

        error_count = sum(1 for i in self.issues_found if i.get('severity') == 'error')
        warning_count = sum(1 for i in self.issues_found if i.get('severity') == 'warning')
        info_count = sum(1 for i in self.issues_found if i.get('severity') == 'info')

        report_lines.append(f'Files with issues: {len(issues_by_file)}')
        report_lines.append(f'{Colors.RED}Errors: {error_count}{Colors.END}')
        report_lines.append(f'{Colors.YELLOW}Warnings: {warning_count}{Colors.END}')
        report_lines.append(f'{Colors.CYAN}Info: {info_count}{Colors.END}')
        report_lines.append('')

        return '\n'.join(report_lines)


def main():
    # Fix Windows console encoding for Unicode characters
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    parser = argparse.ArgumentParser(
        description='Validate README and /prime files follow the documented pattern',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--file',
        type=str,
        help='Validate a specific README or /prime file'
    )

    parser.add_argument(
        '--scan-all',
        action='store_true',
        help='Scan all README files in repository'
    )

    parser.add_argument(
        '--scan-prime',
        action='store_true',
        help='Scan all /prime files in .claude directory'
    )

    parser.add_argument(
        '--report',
        type=str,
        help='Save validation report to file'
    )

    parser.add_argument(
        '--strict',
        action='store_true',
        help='Exit with code 1 if any issues found (for CI)'
    )

    args = parser.parse_args()

    # Determine repository root
    repo_root = Path(__file__).parent.parent.resolve()

    validator = PatternValidator(repo_root)

    # Determine what to validate
    if args.file:
        file_path = Path(args.file).resolve()
        if not file_path.exists():
            print(f'{Colors.RED}Error: File not found: {file_path}{Colors.END}')
            sys.exit(1)

        if 'prime' in str(file_path):
            result = validator.validate_prime_file(file_path)
        else:
            result = validator.validate_readme(file_path)

        print(validator.generate_report())

    elif args.scan_all:
        print(f'{Colors.CYAN}Scanning all README files...{Colors.END}\n')
        readme_files = validator.find_readme_files()

        for readme_file in readme_files:
            result = validator.validate_readme(readme_file)
            if result['status'] == 'skip':
                print(f'{Colors.YELLOW}⊘{Colors.END} {readme_file.relative_to(repo_root)} (legacy)')
            elif result['status'] == 'valid':
                print(f'{Colors.GREEN}✓{Colors.END} {readme_file.relative_to(repo_root)}')
            elif result['status'] == 'invalid':
                print(f'{Colors.RED}✗{Colors.END} {readme_file.relative_to(repo_root)}')

        print('\n' + validator.generate_report())

    elif args.scan_prime:
        print(f'{Colors.CYAN}Scanning all /prime files...{Colors.END}\n')
        prime_files = validator.find_prime_files()

        if not prime_files:
            print(f'{Colors.YELLOW}No /prime files found in .claude/prime directory{Colors.END}')
        else:
            for prime_file in prime_files:
                if prime_file.is_file():
                    result = validator.validate_prime_file(prime_file)
                    if result['status'] == 'valid':
                        print(f'{Colors.GREEN}✓{Colors.END} {prime_file.relative_to(repo_root)}')
                    elif result['status'] == 'invalid':
                        print(f'{Colors.RED}✗{Colors.END} {prime_file.relative_to(repo_root)}')

            print('\n' + validator.generate_report())
    else:
        parser.print_help()
        sys.exit(1)

    # Save report if requested
    if args.report:
        report_path = Path(args.report)
        report_content = validator.generate_report()
        # Remove color codes for file output
        report_content_plain = re.sub(r'\033\[\d+m', '', report_content)
        report_path.write_text(report_content_plain, encoding='utf-8')
        print(f'\n{Colors.GREEN}Report saved to: {report_path}{Colors.END}')

    # Exit with error code if issues found in strict mode
    if args.strict and validator.issues_found:
        error_count = sum(1 for i in validator.issues_found if i.get('severity') == 'error')
        if error_count > 0:
            sys.exit(1)


if __name__ == '__main__':
    main()
