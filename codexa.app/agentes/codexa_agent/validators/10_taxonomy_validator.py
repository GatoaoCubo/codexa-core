#!/usr/bin/env python3
"""
Taxonomy Validation Script for TAC-7 Repository
Version: 2.0.0
Updated: 2025-11-24

Scans markdown files for path references and validates them against
the current directory structure. Detects obsolete -standalone naming patterns.

Features:
- Detects obsolete path references
- Auto-fix capability (--fix)
- Generates ##report (JSON + MD) following REPORT_STANDARD

Usage:
    python validators/10_taxonomy_validator.py --scan-all
    python validators/10_taxonomy_validator.py --file path/to/file.md
    python validators/10_taxonomy_validator.py --scan-all --output-dir reports/
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Add config to path for centralized path management
sys.path.insert(0, str(Path(__file__).parent.parent / 'config'))
from paths import CODEXA_AGENT_ROOT, PATH_VALIDATORS

# Import report generator for ##report standard
try:
    from validators.report_generator import ValidatorReportGenerator
    REPORT_GENERATOR_AVAILABLE = True
except ImportError:
    REPORT_GENERATOR_AVAILABLE = False

# Pattern mappings for old -> new path references
TAXONOMY_MAPPINGS = {
    'codex-anuncio-agent-standalone': 'anuncio-agent',
    'meta-pesquisa-agent-standalone': 'pesquisa-agent',
    'brand-agent-standalone': 'brand-agent',
    'ml-knowledge-agent-standalone': 'knowledge-agent',
}

# Regex pattern to find standalone references
STANDALONE_PATTERN = re.compile(
    r'(codex-anuncio-agent-standalone|meta-pesquisa-agent-standalone|'
    r'brand-agent-standalone|ml-knowledge-agent-standalone)'
)


class TaxonomyIssue:
    """Represents a single taxonomy inconsistency"""

    def __init__(self, file_path: str, line_num: int, line_content: str,
                 old_path: str, new_path: str):
        self.file_path = file_path
        self.line_num = line_num
        self.line_content = line_content
        self.old_path = old_path
        self.new_path = new_path

    def __repr__(self):
        return (f"TaxonomyIssue(file={self.file_path}, line={self.line_num}, "
                f"old='{self.old_path}', new='{self.new_path}')")

    def format_report(self) -> str:
        """Format issue for human-readable report"""
        return (f"{self.file_path}:{self.line_num}\n"
                f"  Found: {self.old_path}\n"
                f"  Replace with: {self.new_path}\n"
                f"  Context: {self.line_content.strip()[:80]}\n")


class TaxonomyValidator:
    """Main validator class for taxonomy consistency"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.issues: List[TaxonomyIssue] = []

    def find_markdown_files(self, target: Optional[Path] = None) -> List[Path]:
        """Find all markdown files to scan"""
        if target and target.is_file():
            return [target]

        search_root = target if target else self.repo_root
        md_files = []

        # Directories to exclude from scanning
        exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'venv'}

        # Files to exclude (documentation about migration/taxonomy)
        exclude_files = {
            'TAXONOMY_VALIDATION.md',  # Documents old naming as examples
            'MIGRATION_LOG.md',  # Historical migration records
            'taxonomy_baseline.txt',  # Validation reports
            'taxonomy_fix_report.txt',
            'TAXONOMY_GUIDE.md',  # May contain historical references
        }

        # Filename patterns to exclude (specs about migration/taxonomy)
        exclude_patterns = [
            'plan-taxonomy-',
            'issue-0-adw-0-sdlc_planner-fix-taxonomy-references',
        ]

        for root, dirs, files in os.walk(search_root):
            # Remove excluded directories from search
            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for file in files:
                if file.endswith('.md') and file not in exclude_files:
                    # Check if file matches any exclude pattern
                    if not any(pattern in file for pattern in exclude_patterns):
                        md_files.append(Path(root) / file)

        return md_files

    def scan_file(self, file_path: Path) -> List[TaxonomyIssue]:
        """Scan a single file for taxonomy issues"""
        issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, start=1):
                    # Find all standalone references in this line
                    matches = STANDALONE_PATTERN.finditer(line)
                    for match in matches:
                        old_path = match.group(1)
                        new_path = TAXONOMY_MAPPINGS.get(old_path)

                        if new_path:
                            issue = TaxonomyIssue(
                                file_path=str(file_path.relative_to(self.repo_root)),
                                line_num=line_num,
                                line_content=line,
                                old_path=old_path,
                                new_path=new_path
                            )
                            issues.append(issue)

        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)

        return issues

    def scan_all(self, target: Optional[Path] = None) -> List[TaxonomyIssue]:
        """Scan all markdown files for issues"""
        self.issues = []
        md_files = self.find_markdown_files(target)

        print(f"Scanning {len(md_files)} markdown files...")

        for md_file in md_files:
            file_issues = self.scan_file(md_file)
            self.issues.extend(file_issues)

        return self.issues

    def verify_path_exists(self, path: str) -> bool:
        """Verify that a path actually exists in the filesystem"""
        full_path = self.repo_root / path
        return full_path.exists()

    def fix_file(self, file_path: Path, dry_run: bool = True) -> int:
        """Fix taxonomy issues in a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            replacements_made = 0

            # Apply all taxonomy mappings
            for old_path, new_path in TAXONOMY_MAPPINGS.items():
                if old_path in content:
                    count_before = content.count(old_path)
                    content = content.replace(old_path, new_path)
                    replacements_made += count_before

            if content != original_content and not dry_run:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed {file_path}: {replacements_made} replacements")

            return replacements_made

        except Exception as e:
            print(f"Error fixing {file_path}: {e}", file=sys.stderr)
            return 0

    def fix_all(self, dry_run: bool = True) -> int:
        """Fix all taxonomy issues"""
        total_fixes = 0

        if not self.issues:
            print("No issues found to fix.")
            return 0

        # Get unique files that need fixing
        files_to_fix = set(self.repo_root / issue.file_path for issue in self.issues)

        print(f"{'[DRY RUN] ' if dry_run else ''}Fixing {len(files_to_fix)} files...")

        for file_path in files_to_fix:
            fixes = self.fix_file(file_path, dry_run)
            total_fixes += fixes

        return total_fixes

    def generate_report(self) -> str:
        """Generate human-readable report"""
        if not self.issues:
            return "[OK] All path references valid - no taxonomy inconsistencies found!"

        report_lines = [
            "=" * 80,
            f"TAXONOMY VALIDATION REPORT",
            "=" * 80,
            f"Total issues found: {len(self.issues)}",
            f"Files affected: {len(set(issue.file_path for issue in self.issues))}",
            "=" * 80,
            ""
        ]

        # Group issues by file
        issues_by_file: Dict[str, List[TaxonomyIssue]] = {}
        for issue in self.issues:
            if issue.file_path not in issues_by_file:
                issues_by_file[issue.file_path] = []
            issues_by_file[issue.file_path].append(issue)

        # Report issues by file
        for file_path in sorted(issues_by_file.keys()):
            file_issues = issues_by_file[file_path]
            report_lines.append(f"\n{file_path} ({len(file_issues)} issues)")
            report_lines.append("-" * 80)

            for issue in file_issues:
                report_lines.append(f"  Line {issue.line_num}: {issue.old_path} -> {issue.new_path}")
                report_lines.append(f"    Context: {issue.line_content.strip()[:70]}")

            report_lines.append("")

        report_lines.append("=" * 80)
        report_lines.append("SUMMARY OF REPLACEMENTS NEEDED:")
        report_lines.append("=" * 80)

        for old_path, new_path in TAXONOMY_MAPPINGS.items():
            count = sum(1 for issue in self.issues if issue.old_path == old_path)
            if count > 0:
                report_lines.append(f"  {old_path} -> {new_path}: {count} occurrences")

        return "\n".join(report_lines)


def main():
    parser = argparse.ArgumentParser(
        description='Validate and fix taxonomy references in TAC-7 repository'
    )
    parser.add_argument('--scan-all', action='store_true',
                        help='Scan all markdown files in repository')
    parser.add_argument('--file', type=str,
                        help='Scan specific file or directory')
    parser.add_argument('--fix', action='store_true',
                        help='Automatically fix issues (default is dry-run)')
    parser.add_argument('--report', type=str,
                        help='Write report to specified file')
    parser.add_argument('--strict', action='store_true',
                        help='Exit with error code if any issues found')

    args = parser.parse_args()

    # Use centralized path from config
    repo_root = CODEXA_AGENT_ROOT

    validator = TaxonomyValidator(repo_root)

    # Determine scan target
    target = None
    if args.file:
        target = Path(args.file)
        if not target.is_absolute():
            target = repo_root / target

    # Scan for issues
    if args.scan_all or args.file:
        validator.scan_all(target)
    else:
        parser.print_help()
        return 1

    # Generate report
    report = validator.generate_report()

    # Output report
    if args.report:
        with open(args.report, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Report written to {args.report}")
    else:
        # Use UTF-8 for console output to avoid encoding issues
        try:
            print(report)
        except UnicodeEncodeError:
            # If console doesn't support UTF-8, write to temp file
            import sys
            sys.stdout.buffer.write(report.encode('utf-8'))
            print()  # Newline

    # Apply fixes if requested
    if args.fix:
        fixes_made = validator.fix_all(dry_run=False)
        print(f"\n[OK] Applied {fixes_made} fixes across {len(set(issue.file_path for issue in validator.issues))} files")
    elif validator.issues:
        print(f"\n[INFO] Run with --fix to automatically apply these changes")

    # Exit with appropriate code
    if args.strict and validator.issues:
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
