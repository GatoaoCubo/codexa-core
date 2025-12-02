#!/usr/bin/env python3
"""
Path Consistency Validator for CODEXA Builders and Validators
Version: 2.0.0
Updated: 2025-11-24

Ensures all scripts use centralized path configuration from config.paths
instead of hardcoded relative paths.

Features:
- Detects hardcoded path patterns
- Enforces config.paths imports
- Generates ##report (JSON + MD) following REPORT_STANDARD

Usage:
    python validators/16_path_consistency_validator.py
    python validators/16_path_consistency_validator.py --file builders/14_tac7_header_generator.py
    python validators/16_path_consistency_validator.py --output-dir reports/
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

# Add config to path for centralized path management
sys.path.insert(0, str(Path(__file__).parent.parent / 'config'))
from paths import PATH_VALIDATORS

# Import report generator for ##report standard
try:
    from validators.report_generator import ValidatorReportGenerator
    REPORT_GENERATOR_AVAILABLE = True
except ImportError:
    REPORT_GENERATOR_AVAILABLE = False


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

    @staticmethod
    def strip_colors(text: str) -> str:
        """Remove ANSI color codes from text"""
        ansi_escape = re.compile(r'\033\[[0-9;]+m')
        return ansi_escape.sub('', text)


# Windows-safe symbols (ASCII only)
CHECK = '[OK]' if sys.platform == 'win32' else '✓'
CROSS = '[X]' if sys.platform == 'win32' else '✗'
WARNING = '[!]' if sys.platform == 'win32' else '⚠'
INFO = '[i]' if sys.platform == 'win32' else 'ℹ'
ARROW = '->' if sys.platform == 'win32' else '→'


@dataclass
class PathIssue:
    """Represents a path-related issue found in a file"""
    file_path: Path
    line_number: int
    line_content: str
    issue_type: str
    severity: str  # 'error', 'warning', 'info'
    description: str
    suggestion: Optional[str] = None


@dataclass
class ValidationResult:
    """Result of validating a single file"""
    file_path: Path
    is_valid: bool
    issues: List[PathIssue] = field(default_factory=list)
    uses_config_paths: bool = False
    is_adw_script: bool = False

    def __post_init__(self):
        """Calculate validity based on issues"""
        # File is valid if no errors (warnings are ok)
        self.is_valid = all(issue.severity != 'error' for issue in self.issues)


class PathConsistencyValidator:
    """Validates path usage consistency across builders and validators"""

    # Patterns that indicate hardcoded paths (potential issues)
    HARDCODED_PATH_PATTERNS = [
        (r'["\']\.\.\/agentes\/', 'Hardcoded relative path to agentes/'),
        (r'["\']\.\.\/\.\.\/agentes\/', 'Hardcoded relative path to agentes/'),
        (r'["\']templates\/', 'Hardcoded path to templates/ (use PATH_TEMPLATES)'),
        (r'["\']workflows\/', 'Hardcoded path to workflows/ (use PATH_WORKFLOWS)'),
        (r'["\']prompts\/', 'Hardcoded path to prompts/ (use PATH_PROMPTS)'),
        (r'["\']validators\/', 'Hardcoded path to validators/ (use PATH_VALIDATORS)'),
        (r'["\']51_AGENT_REGISTRY\.json', 'Hardcoded registry path (use PATH_REGISTRY)'),
        (r'["\']42_HOP_FRAMEWORK\.md', 'Hardcoded HOP framework path (use PATH_HOP_FRAMEWORK)'),
    ]

    # Patterns that are ALLOWED (exceptions to the rules)
    ALLOWED_PATTERNS = [
        r'adw_modules',  # ADW scripts use this module
        r'sys\.path\.insert.*adw_modules',  # ADW module imports
        r'#.*templates/',  # Comments mentioning paths
        r'""".*templates/',  # Docstrings mentioning paths
        r"'.*\.md'.*#.*example",  # Example paths in comments
        r'pattern\d*\s*=\s*r["\']',  # Regex pattern assignments (e.g., pattern1 = r'prompts/')
        r':\s*str\s*=\s*["\'].*["\']',  # Type-annotated string constants (e.g., CORE_FILE_3: str = "prompts/")
    ]

    # Indicators that file is an ADW script (doesn't need config.paths)
    ADW_INDICATORS = [
        r'from agent import',
        r'AgentTemplateRequest',
        r'AgentPromptRequest',
        r'execute_template',
        r'adw_modules',
    ]

    # Indicators that file SHOULD use config.paths
    SHOULD_USE_CONFIG_PATHS = [
        r'PATH_TEMPLATES',
        r'PATH_WORKFLOWS',
        r'PATH_PROMPTS',
        r'PATH_VALIDATORS',
        r'PATH_REGISTRY',
        r'AGENTS_ROOT',
        r'CODEXA_APP',
    ]

    def __init__(self, script_dir: Path):
        """Initialize validator with codexa_agent directory"""
        self.script_dir = script_dir
        self.agent_dir = script_dir.parent if script_dir.name == 'validators' else script_dir.parent
        self.builders_dir = self.agent_dir / 'builders'
        self.validators_dir = self.agent_dir / 'validators'

    def is_allowed_pattern(self, line: str) -> bool:
        """Check if line matches any allowed pattern"""
        for pattern in self.ALLOWED_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                return True
        return False

    def is_adw_script(self, content: str) -> bool:
        """Check if file is an ADW wrapper script"""
        for pattern in self.ADW_INDICATORS:
            if re.search(pattern, content):
                return True
        return False

    def uses_config_paths(self, content: str) -> bool:
        """Check if file imports from config.paths"""
        return bool(re.search(r'from config\.paths import', content))

    def validate_file(self, file_path: Path) -> ValidationResult:
        """Validate a single Python file for path consistency"""
        issues: List[PathIssue] = []

        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            return ValidationResult(
                file_path=file_path,
                is_valid=False,
                issues=[PathIssue(
                    file_path=file_path,
                    line_number=0,
                    line_content='',
                    issue_type='read_error',
                    severity='error',
                    description=f'Failed to read file: {e}'
                )]
            )

        # Check if this is an ADW script
        is_adw = self.is_adw_script(content)
        uses_config = self.uses_config_paths(content)

        lines = content.split('\n')

        # Scan for hardcoded path patterns
        for line_num, line in enumerate(lines, start=1):
            # Skip allowed patterns
            if self.is_allowed_pattern(line):
                continue

            # Check for hardcoded paths
            for pattern, description in self.HARDCODED_PATH_PATTERNS:
                if re.search(pattern, line):
                    # Determine severity
                    severity = 'warning' if is_adw else 'error'

                    # Get suggestion based on pattern
                    suggestion = self._get_suggestion(pattern)

                    issues.append(PathIssue(
                        file_path=file_path,
                        line_number=line_num,
                        line_content=line.strip(),
                        issue_type='hardcoded_path',
                        severity=severity,
                        description=description,
                        suggestion=suggestion
                    ))

        # If file has hardcoded paths but doesn't use config.paths (and isn't ADW)
        if issues and not uses_config and not is_adw:
            # Check if any CODEXA system paths are referenced
            has_system_paths = any(
                re.search(pattern, content)
                for pattern, _ in self.HARDCODED_PATH_PATTERNS
                if not self.is_allowed_pattern(content)
            )

            if has_system_paths:
                issues.insert(0, PathIssue(
                    file_path=file_path,
                    line_number=1,
                    line_content='',
                    issue_type='missing_config_import',
                    severity='error',
                    description='File uses system paths but does not import config.paths',
                    suggestion='Add: from config.paths import PATH_TEMPLATES, PATH_WORKFLOWS, ...'
                ))

        return ValidationResult(
            file_path=file_path,
            is_valid=len([i for i in issues if i.severity == 'error']) == 0,
            issues=issues,
            uses_config_paths=uses_config,
            is_adw_script=is_adw
        )

    def _get_suggestion(self, pattern: str) -> str:
        """Get suggestion for fixing a hardcoded path pattern"""
        suggestions = {
            r'templates\/': 'Use: from config.paths import PATH_TEMPLATES',
            r'workflows\/': 'Use: from config.paths import PATH_WORKFLOWS',
            r'prompts\/': 'Use: from config.paths import PATH_PROMPTS',
            r'validators\/': 'Use: from config.paths import PATH_VALIDATORS',
            r'51_AGENT_REGISTRY': 'Use: from config.paths import PATH_REGISTRY',
            r'42_HOP_FRAMEWORK': 'Use: from config.paths import PATH_HOP_FRAMEWORK',
            r'agentes\/': 'Use: from config.paths import AGENTS_ROOT',
        }

        for key, suggestion in suggestions.items():
            if key in pattern:
                return suggestion

        return 'Use centralized paths from config.paths'

    def validate_all(self, strict: bool = False) -> Tuple[List[ValidationResult], bool]:
        """Validate all builders and validators"""
        results = []
        all_valid = True

        # Get all Python files in builders/ and validators/
        files_to_check = []

        if self.builders_dir.exists():
            files_to_check.extend(self.builders_dir.glob('*.py'))

        if self.validators_dir.exists():
            files_to_check.extend(self.validators_dir.glob('*.py'))

        # Validate each file
        for file_path in sorted(files_to_check):
            # Skip __init__.py and adw_modules/
            if file_path.name == '__init__.py' or 'adw_modules' in str(file_path):
                continue

            result = self.validate_file(file_path)
            results.append(result)

            if not result.is_valid:
                all_valid = False

        return results, all_valid

    def print_results(self, results: List[ValidationResult], verbose: bool = True):
        """Print validation results to console with colors"""
        total_files = len(results)
        valid_files = sum(1 for r in results if r.is_valid)
        files_with_issues = total_files - valid_files
        total_errors = sum(len([i for i in r.issues if i.severity == 'error']) for r in results)
        total_warnings = sum(len([i for i in r.issues if i.severity == 'warning']) for r in results)

        print(f"\n{Colors.BOLD}{'=' * 70}{Colors.END}")
        print(f"{Colors.BOLD}{Colors.CYAN}Path Consistency Validation Report{Colors.END}")
        print(f"{Colors.BOLD}{'=' * 70}{Colors.END}\n")

        # Summary
        print(f"{Colors.BOLD}Summary:{Colors.END}")
        print(f"  Total files checked: {total_files}")
        print(f"  {Colors.GREEN}{CHECK} Valid files: {valid_files}{Colors.END}")
        if files_with_issues > 0:
            print(f"  {Colors.RED}{CROSS} Files with errors: {files_with_issues}{Colors.END}")
        print(f"  {Colors.YELLOW}{WARNING} Total warnings: {total_warnings}{Colors.END}")
        print(f"  {Colors.RED}{CROSS} Total errors: {total_errors}{Colors.END}\n")

        # File-by-file results
        if verbose:
            for result in results:
                self._print_file_result(result)

        # Final status
        print(f"{Colors.BOLD}{'=' * 70}{Colors.END}")
        if files_with_issues == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}{CHECK} All files pass path consistency checks!{Colors.END}\n")
            return True
        else:
            print(f"{Colors.RED}{Colors.BOLD}{CROSS} {files_with_issues} file(s) have path consistency issues{Colors.END}\n")
            return False

    def _print_file_result(self, result: ValidationResult):
        """Print result for a single file"""
        file_name = result.file_path.name

        if result.is_valid:
            # Only show valid files if they use config.paths
            if result.uses_config_paths:
                print(f"{Colors.GREEN}{CHECK} {file_name}{Colors.END} - Uses config.paths")
            elif result.is_adw_script:
                print(f"{Colors.BLUE}{INFO} {file_name}{Colors.END} - ADW script (uses adw_modules)")
            else:
                print(f"{Colors.GREEN}{CHECK} {file_name}{Colors.END}")
        else:
            print(f"{Colors.RED}{CROSS} {file_name}{Colors.END}")

            for issue in result.issues:
                self._print_issue(issue)
            print()  # Blank line between files

    def _print_issue(self, issue: PathIssue):
        """Print a single issue"""
        # Color based on severity
        if issue.severity == 'error':
            color = Colors.RED
            symbol = CROSS
        elif issue.severity == 'warning':
            color = Colors.YELLOW
            symbol = WARNING
        else:
            color = Colors.CYAN
            symbol = INFO

        # Print issue
        if issue.line_number > 0:
            print(f"  {color}{symbol} Line {issue.line_number}: {issue.description}{Colors.END}")
            if issue.line_content:
                print(f"    {Colors.BOLD}Code:{Colors.END} {issue.line_content[:80]}")
        else:
            print(f"  {color}{symbol} {issue.description}{Colors.END}")

        # Print suggestion
        if issue.suggestion:
            print(f"    {Colors.CYAN}{ARROW} {issue.suggestion}{Colors.END}")

    def write_report(self, results: List[ValidationResult], report_path: Path):
        """Write detailed validation report to file"""
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("Path Consistency Validation Report\n")
            f.write("=" * 70 + "\n\n")

            # Summary
            total_files = len(results)
            valid_files = sum(1 for r in results if r.is_valid)
            total_issues = sum(len(r.issues) for r in results)

            f.write(f"Total files checked: {total_files}\n")
            f.write(f"Valid files: {valid_files}\n")
            f.write(f"Files with issues: {total_files - valid_files}\n")
            f.write(f"Total issues: {total_issues}\n\n")

            # Detailed results
            f.write("=" * 70 + "\n")
            f.write("Detailed Results\n")
            f.write("=" * 70 + "\n\n")

            for result in results:
                f.write(f"\nFile: {result.file_path.name}\n")
                f.write(f"Status: {'PASS' if result.is_valid else 'FAIL'}\n")
                f.write(f"Uses config.paths: {result.uses_config_paths}\n")
                f.write(f"Is ADW script: {result.is_adw_script}\n")

                if result.issues:
                    f.write(f"\nIssues ({len(result.issues)}):\n")
                    for issue in result.issues:
                        f.write(f"  - Line {issue.line_number}: {issue.description}\n")
                        if issue.line_content:
                            f.write(f"    Code: {issue.line_content}\n")
                        if issue.suggestion:
                            f.write(f"    Suggestion: {issue.suggestion}\n")

                f.write("\n" + "-" * 70 + "\n")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Validate path consistency in CODEXA builders and validators'
    )
    parser.add_argument(
        '--file',
        type=str,
        help='Validate specific file instead of all files'
    )
    parser.add_argument(
        '--strict',
        action='store_true',
        help='Exit with code 1 if any issues found (for CI/CD)'
    )
    parser.add_argument(
        '--report',
        type=str,
        help='Write detailed report to file'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Only show summary, not individual file results'
    )

    args = parser.parse_args()

    # Initialize validator using centralized path
    validator = PathConsistencyValidator(PATH_VALIDATORS)

    # Validate
    if args.file:
        # Validate single file
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"{Colors.RED}Error: File not found: {file_path}{Colors.END}")
            sys.exit(1)

        result = validator.validate_file(file_path)
        results = [result]
        all_valid = result.is_valid
    else:
        # Validate all files
        results, all_valid = validator.validate_all(strict=args.strict)

    # Print results
    success = validator.print_results(results, verbose=not args.quiet)

    # Write report if requested
    if args.report:
        report_path = Path(args.report)
        validator.write_report(results, report_path)
        print(f"{Colors.CYAN}Report written to: {report_path}{Colors.END}\n")

    # Exit with appropriate code
    if args.strict and not all_valid:
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
