#!/usr/bin/env python3
"""
Code Quality Validator for CODEXA System
Version: 2.2.0
Created: 2025-11-24
Updated: 2025-11-29

Validates code files against CODEXA Code Style Guide (05_code_conventions.md).
Checks for naming conventions, type annotations, documentation, structure limits.

Features:
- Multi-language support (Python, TypeScript, JavaScript)
- Naming convention validation
- Type annotation checks
- Documentation coverage
- Code structure limits (function/file length)
- Generates ##report (JSON + MD) following REPORT_STANDARD
- **v2.1.0**: Value Function integration for gradient feedback
- **v2.2.0**: Intelligent Fallback for refined autonomy

Value Function Integration:
- Confidence scoring (0.0-1.0) instead of binary pass/fail
- Intermediate checkpoints during validation
- Gradient feedback with action recommendations
- Use --gradient flag for Value Function output

Intelligent Fallback (v2.2.0):
- Cascading fallback actions (6 levels)
- Auto-correction strategies for common issues
- Policy-driven autonomy (development/staging/production)
- Historical learning for strategy optimization
- Use --fallback flag for intelligent retry loop

Usage:
    python validators/13_code_quality_validator.py --file path/to/file.py
    python validators/13_code_quality_validator.py --dir src/
    python validators/13_code_quality_validator.py --all --output-dir reports/
    python validators/13_code_quality_validator.py --all --gradient  # Gradient output
    python validators/13_code_quality_validator.py --all --fallback  # With fallback loop
"""

import argparse
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import report generator for ##report standard
try:
    from validators.report_generator import ValidatorReportGenerator
    REPORT_GENERATOR_AVAILABLE = True
except ImportError:
    REPORT_GENERATOR_AVAILABLE = False

# Import Value Function for gradient feedback (v2.1.0)
try:
    from validators.value_function import ValueFunctionMixin, GradientReport, ConfidenceLevel
    VALUE_FUNCTION_AVAILABLE = True
except ImportError:
    VALUE_FUNCTION_AVAILABLE = False
    # Fallback: create a dummy mixin if not available
    class ValueFunctionMixin:
        def reset_checkpoints(self): pass
        def add_checkpoint(self, *args, **kwargs): pass
        def generate_gradient_report(self): return None
        def print_gradient_summary(self, *args): pass

# Import Intelligent Fallback for refined autonomy (v2.2.0)
try:
    from validators.intelligent_fallback import (
        IntelligentFallbackOrchestrator,
        FallbackMixin,
        FallbackAction,
        FallbackResult,
        get_policy,
        detect_context,
    )
    FALLBACK_AVAILABLE = True
except ImportError:
    FALLBACK_AVAILABLE = False
    # Fallback: create a dummy mixin if not available
    class FallbackMixin:
        def init_fallback(self, *args, **kwargs): pass
        def run_with_fallback(self, fn, **kwargs): return {"status": "fallback_unavailable", "result": fn()}


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


# Windows-safe symbols
CHECK = '[OK]' if sys.platform == 'win32' else '✓'
CROSS = '[X]' if sys.platform == 'win32' else '✗'
WARNING = '[!]' if sys.platform == 'win32' else '⚠'
INFO = '[i]' if sys.platform == 'win32' else 'ℹ'


# === CODE QUALITY RULES ===

# Naming patterns from 05_code_conventions.md
PYTHON_PATTERNS = {
    'variable': re.compile(r'^[a-z][a-z0-9_]*$'),  # snake_case
    'function': re.compile(r'^[a-z][a-z0-9_]*$'),  # snake_case (verb_noun)
    'class': re.compile(r'^[A-Z][a-zA-Z0-9]*$'),   # PascalCase
    'constant': re.compile(r'^[A-Z][A-Z0-9_]*$'),  # UPPER_SNAKE_CASE
    'private': re.compile(r'^_[a-z][a-z0-9_]*$'),  # _private_method
}

TYPESCRIPT_PATTERNS = {
    'variable': re.compile(r'^[a-z][a-zA-Z0-9]*$'),  # camelCase
    'function': re.compile(r'^[a-z][a-zA-Z0-9]*$'),  # camelCase
    'class': re.compile(r'^[A-Z][a-zA-Z0-9]*$'),     # PascalCase
    'constant': re.compile(r'^[A-Z][A-Z0-9_]*$'),    # UPPER_SNAKE_CASE
    'interface': re.compile(r'^[A-Z][a-zA-Z0-9]*$'), # PascalCase
}

# Structure limits from 05_code_conventions.md
LIMITS = {
    'function_lines_target': 30,
    'function_lines_max': 50,
    'file_lines_target': 400,
    'file_lines_max': 600,
    'line_length_max': 88,
}


@dataclass
class QualityIssue:
    """Represents a code quality issue"""
    file_path: str
    line_number: int
    rule: str
    severity: str  # 'error', 'warning', 'info'
    message: str
    suggestion: Optional[str] = None


@dataclass
class FileMetrics:
    """Metrics for a single file"""
    path: str
    language: str
    total_lines: int
    code_lines: int
    comment_lines: int
    blank_lines: int
    function_count: int
    class_count: int
    avg_function_length: float
    max_function_length: int
    type_annotation_coverage: float
    docstring_coverage: float


@dataclass
class ValidationResult:
    """Complete validation result"""
    files_analyzed: int
    total_issues: int
    errors: int
    warnings: int
    info: int
    quality_score: float  # 0-100
    issues: List[QualityIssue] = field(default_factory=list)
    metrics: List[FileMetrics] = field(default_factory=list)


class CodeQualityValidator(ValueFunctionMixin, FallbackMixin):
    """
    Validates code against CODEXA Code Style Guide.

    Rules based on prompts/layers/05_code_conventions.md

    v2.1.0: Now includes Value Function integration for gradient feedback.
    Use generate_gradient_report() for confidence-scored output.

    v2.2.0: Now includes Intelligent Fallback for refined autonomy.
    Use run_with_fallback() for automatic retry with corrections.
    """

    VERSION = "2.2.0"

    def __init__(self, output_dir: Optional[Path] = None):
        # Initialize Value Function mixin first
        super().__init__()

        self.output_dir = output_dir
        self.issues: List[QualityIssue] = []
        self.metrics: List[FileMetrics] = []

        # Initialize report generator
        if REPORT_GENERATOR_AVAILABLE:
            self.reporter = ValidatorReportGenerator("code_quality_validator", self.VERSION)
        else:
            self.reporter = None

    def detect_language(self, file_path: Path) -> str:
        """Detect programming language from file extension."""
        ext = file_path.suffix.lower()
        mapping = {
            '.py': 'python',
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.js': 'javascript',
            '.jsx': 'javascript',
        }
        return mapping.get(ext, 'unknown')

    def validate_file(self, file_path: Path) -> FileMetrics:
        """
        Validate a single file against code quality rules.

        v2.1.0: Now adds Value Function checkpoints during validation.
        """
        language = self.detect_language(file_path)

        if language == 'unknown':
            return None

        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            self._add_issue(str(file_path), 0, "FILE-001", "error",
                          f"Cannot read file: {e}")
            # Add checkpoint for file read failure
            self.add_checkpoint(
                name="file_access",
                score=0.0,
                context=f"Failed to read {file_path.name}",
                details={"error": str(e)}
            )
            return None

        lines = content.split('\n')

        # Calculate basic metrics
        metrics = self._calculate_metrics(file_path, content, lines, language)
        self.metrics.append(metrics)

        # Add checkpoint for metrics calculation (v2.1.0)
        self._add_metrics_checkpoint(metrics)

        # Run validation rules
        self._validate_file_length(file_path, lines)
        self._validate_line_length(file_path, lines)

        if language == 'python':
            self._validate_python(file_path, content, lines)
        elif language in ('typescript', 'javascript'):
            self._validate_typescript(file_path, content, lines)

        return metrics

    def _add_metrics_checkpoint(self, metrics: FileMetrics) -> None:
        """
        Add Value Function checkpoints based on calculated metrics.

        This implements intermediate feedback during validation.
        """
        # Checkpoint: Type annotation coverage
        type_score = metrics.type_annotation_coverage / 100.0
        self.add_checkpoint(
            name="type_coverage",
            score=type_score,
            context=f"Type annotation coverage for {Path(metrics.path).name}",
            details={"coverage_percent": metrics.type_annotation_coverage}
        )

        # Checkpoint: Documentation coverage
        doc_score = metrics.docstring_coverage / 100.0
        self.add_checkpoint(
            name="doc_coverage",
            score=doc_score,
            context=f"Documentation coverage for {Path(metrics.path).name}",
            details={"coverage_percent": metrics.docstring_coverage}
        )

        # Checkpoint: File structure (length)
        if metrics.total_lines <= LIMITS['file_lines_target']:
            structure_score = 1.0
        elif metrics.total_lines <= LIMITS['file_lines_max']:
            # Linear interpolation between target and max
            overage = metrics.total_lines - LIMITS['file_lines_target']
            max_overage = LIMITS['file_lines_max'] - LIMITS['file_lines_target']
            structure_score = 1.0 - (overage / max_overage) * 0.3
        else:
            structure_score = 0.3

        self.add_checkpoint(
            name="file_structure",
            score=structure_score,
            context=f"File length check for {Path(metrics.path).name}",
            details={"total_lines": metrics.total_lines, "target": LIMITS['file_lines_target']}
        )

        # Checkpoint: Function complexity
        if metrics.max_function_length <= LIMITS['function_lines_target']:
            func_score = 1.0
        elif metrics.max_function_length <= LIMITS['function_lines_max']:
            overage = metrics.max_function_length - LIMITS['function_lines_target']
            max_overage = LIMITS['function_lines_max'] - LIMITS['function_lines_target']
            func_score = 1.0 - (overage / max_overage) * 0.3
        else:
            func_score = 0.4

        self.add_checkpoint(
            name="function_complexity",
            score=func_score,
            context=f"Function length check for {Path(metrics.path).name}",
            details={"max_function_length": metrics.max_function_length, "target": LIMITS['function_lines_target']}
        )

    def _calculate_metrics(self, file_path: Path, content: str, lines: List[str],
                          language: str) -> FileMetrics:
        """Calculate code metrics for a file."""
        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if not line.strip())
        comment_lines = self._count_comments(lines, language)
        code_lines = total_lines - blank_lines - comment_lines

        # Count functions/classes
        if language == 'python':
            function_count = len(re.findall(r'^\s*def\s+\w+', content, re.MULTILINE))
            class_count = len(re.findall(r'^\s*class\s+\w+', content, re.MULTILINE))
            function_lengths = self._get_python_function_lengths(content)
            type_coverage = self._python_type_coverage(content)
            docstring_coverage = self._python_docstring_coverage(content)
        else:
            function_count = len(re.findall(r'(?:function|async function)\s+\w+|(?:const|let)\s+\w+\s*=\s*(?:async\s*)?\(', content))
            class_count = len(re.findall(r'\bclass\s+\w+', content))
            function_lengths = self._get_ts_function_lengths(content)
            type_coverage = self._typescript_type_coverage(content)
            docstring_coverage = self._jsdoc_coverage(content)

        avg_func_len = sum(function_lengths) / len(function_lengths) if function_lengths else 0
        max_func_len = max(function_lengths) if function_lengths else 0

        return FileMetrics(
            path=str(file_path),
            language=language,
            total_lines=total_lines,
            code_lines=code_lines,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            function_count=function_count,
            class_count=class_count,
            avg_function_length=round(avg_func_len, 1),
            max_function_length=max_func_len,
            type_annotation_coverage=round(type_coverage * 100, 1),
            docstring_coverage=round(docstring_coverage * 100, 1),
        )

    def _count_comments(self, lines: List[str], language: str) -> int:
        """Count comment lines."""
        count = 0
        in_multiline = False

        for line in lines:
            stripped = line.strip()

            if language == 'python':
                if stripped.startswith('#'):
                    count += 1
                elif stripped.startswith('"""') or stripped.startswith("'''"):
                    in_multiline = not in_multiline
                    count += 1
                elif in_multiline:
                    count += 1
            else:  # TypeScript/JavaScript
                if stripped.startswith('//'):
                    count += 1
                elif stripped.startswith('/*'):
                    in_multiline = True
                    count += 1
                elif stripped.endswith('*/'):
                    in_multiline = False
                    count += 1
                elif in_multiline:
                    count += 1

        return count

    def _get_python_function_lengths(self, content: str) -> List[int]:
        """Get lengths of Python functions."""
        lengths = []
        lines = content.split('\n')
        in_function = False
        function_start = 0
        indent_level = 0

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Function definition
            if re.match(r'^\s*def\s+\w+', line):
                if in_function:
                    lengths.append(i - function_start)
                in_function = True
                function_start = i
                indent_level = len(line) - len(line.lstrip())
            elif in_function and stripped:
                # Check if we've exited the function (dedented)
                current_indent = len(line) - len(line.lstrip())
                if current_indent <= indent_level and not stripped.startswith('#'):
                    lengths.append(i - function_start)
                    in_function = False

        if in_function:
            lengths.append(len(lines) - function_start)

        return lengths

    def _get_ts_function_lengths(self, content: str) -> List[int]:
        """Get lengths of TypeScript/JavaScript functions (simplified)."""
        # Simplified: count lines between function definitions
        function_pattern = re.compile(r'(?:function|async function)\s+\w+|(?:const|let)\s+\w+\s*=\s*(?:async\s*)?\(')
        matches = list(function_pattern.finditer(content))

        if not matches:
            return []

        lines = content.split('\n')
        lengths = []

        for i, match in enumerate(matches):
            start_line = content[:match.start()].count('\n')
            if i + 1 < len(matches):
                end_line = content[:matches[i + 1].start()].count('\n')
            else:
                end_line = len(lines)

            lengths.append(end_line - start_line)

        return lengths

    def _python_type_coverage(self, content: str) -> float:
        """Calculate type annotation coverage for Python."""
        # Count functions with type hints vs total
        all_functions = re.findall(r'def\s+\w+\s*\([^)]*\)', content)
        typed_functions = re.findall(r'def\s+\w+\s*\([^)]*\)\s*->', content)

        if not all_functions:
            return 1.0

        return len(typed_functions) / len(all_functions)

    def _typescript_type_coverage(self, content: str) -> float:
        """Calculate type coverage for TypeScript (simplified)."""
        # Check for explicit type annotations
        typed_declarations = len(re.findall(r':\s*\w+', content))
        total_declarations = len(re.findall(r'(?:const|let|var)\s+\w+', content))

        if total_declarations == 0:
            return 1.0

        # Simplified heuristic
        return min(typed_declarations / max(total_declarations, 1), 1.0)

    def _python_docstring_coverage(self, content: str) -> float:
        """Calculate docstring coverage for Python functions."""
        # Find all function definitions
        functions = re.findall(r'def\s+(\w+)\s*\([^)]*\):', content)
        public_functions = [f for f in functions if not f.startswith('_')]

        if not public_functions:
            return 1.0

        # Count functions followed by docstrings
        documented = len(re.findall(r'def\s+\w+\s*\([^)]*\):\s*\n\s+["\']', content))

        return documented / len(public_functions)

    def _jsdoc_coverage(self, content: str) -> float:
        """Calculate JSDoc coverage for TypeScript/JavaScript."""
        functions = re.findall(r'(?:function|async function)\s+\w+|(?:const|let)\s+\w+\s*=\s*(?:async\s*)?\(', content)

        if not functions:
            return 1.0

        # Count JSDoc comments
        jsdocs = len(re.findall(r'/\*\*[\s\S]*?\*/', content))

        return min(jsdocs / len(functions), 1.0)

    def _validate_file_length(self, file_path: Path, lines: List[str]) -> None:
        """Check file length limits."""
        total = len(lines)

        if total > LIMITS['file_lines_max']:
            self._add_issue(str(file_path), 0, "STRUCT-001", "error",
                          f"File too long: {total} lines (max {LIMITS['file_lines_max']})",
                          "Split into multiple modules by responsibility")
        elif total > LIMITS['file_lines_target']:
            self._add_issue(str(file_path), 0, "STRUCT-002", "warning",
                          f"File exceeds target length: {total} lines (target {LIMITS['file_lines_target']})",
                          "Consider splitting into smaller modules")

    def _validate_line_length(self, file_path: Path, lines: List[str]) -> None:
        """Check line length limits."""
        for i, line in enumerate(lines, 1):
            if len(line) > LIMITS['line_length_max']:
                self._add_issue(str(file_path), i, "STRUCT-003", "warning",
                              f"Line too long: {len(line)} chars (max {LIMITS['line_length_max']})",
                              "Break into multiple lines")

    def _validate_python(self, file_path: Path, content: str, lines: List[str]) -> None:
        """Python-specific validation rules."""
        # Check function lengths
        self._check_python_function_lengths(file_path, content)

        # Check naming conventions
        self._check_python_naming(file_path, content)

        # Check type annotations
        self._check_python_types(file_path, content)

        # Check docstrings
        self._check_python_docstrings(file_path, content)

    def _validate_typescript(self, file_path: Path, content: str, lines: List[str]) -> None:
        """TypeScript/JavaScript-specific validation rules."""
        # Check function lengths
        self._check_ts_function_lengths(file_path, content)

        # Check naming conventions
        self._check_ts_naming(file_path, content)

    def _check_python_function_lengths(self, file_path: Path, content: str) -> None:
        """Check Python function length limits."""
        pattern = re.compile(r'def\s+(\w+)\s*\(', re.MULTILINE)

        for match in pattern.finditer(content):
            func_name = match.group(1)
            start_line = content[:match.start()].count('\n') + 1

            # Simplified length estimation
            remaining = content[match.start():]
            lines_to_next = remaining.find('\ndef ')
            if lines_to_next == -1:
                lines_to_next = len(remaining)

            func_lines = remaining[:lines_to_next].count('\n')

            if func_lines > LIMITS['function_lines_max']:
                self._add_issue(str(file_path), start_line, "FUNC-001", "error",
                              f"Function '{func_name}' too long: ~{func_lines} lines (max {LIMITS['function_lines_max']})",
                              "Extract helper functions")
            elif func_lines > LIMITS['function_lines_target']:
                self._add_issue(str(file_path), start_line, "FUNC-002", "warning",
                              f"Function '{func_name}' exceeds target: ~{func_lines} lines (target {LIMITS['function_lines_target']})",
                              "Consider splitting into smaller functions")

    def _check_ts_function_lengths(self, file_path: Path, content: str) -> None:
        """Check TypeScript function length limits."""
        pattern = re.compile(r'(?:function|async function)\s+(\w+)')

        for match in pattern.finditer(content):
            func_name = match.group(1)
            start_line = content[:match.start()].count('\n') + 1

            # Simplified estimation
            self._add_issue(str(file_path), start_line, "FUNC-003", "info",
                          f"Review function '{func_name}' length manually",
                          "Target: 10-30 lines, max: 50 lines")

    def _check_python_naming(self, file_path: Path, content: str) -> None:
        """Check Python naming conventions."""
        # Check function names
        for match in re.finditer(r'def\s+(\w+)\s*\(', content):
            name = match.group(1)
            line = content[:match.start()].count('\n') + 1

            if name.startswith('_'):
                if not PYTHON_PATTERNS['private'].match(name):
                    self._add_issue(str(file_path), line, "NAME-001", "warning",
                                  f"Private function '{name}' should use _snake_case")
            elif not PYTHON_PATTERNS['function'].match(name):
                self._add_issue(str(file_path), line, "NAME-002", "warning",
                              f"Function '{name}' should use snake_case (verb_noun)")

        # Check class names
        for match in re.finditer(r'class\s+(\w+)', content):
            name = match.group(1)
            line = content[:match.start()].count('\n') + 1

            if not PYTHON_PATTERNS['class'].match(name):
                self._add_issue(str(file_path), line, "NAME-003", "warning",
                              f"Class '{name}' should use PascalCase")

    def _check_ts_naming(self, file_path: Path, content: str) -> None:
        """Check TypeScript naming conventions."""
        # Check function names
        for match in re.finditer(r'function\s+(\w+)', content):
            name = match.group(1)
            line = content[:match.start()].count('\n') + 1

            if not TYPESCRIPT_PATTERNS['function'].match(name):
                self._add_issue(str(file_path), line, "NAME-004", "warning",
                              f"Function '{name}' should use camelCase")

        # Check class names
        for match in re.finditer(r'class\s+(\w+)', content):
            name = match.group(1)
            line = content[:match.start()].count('\n') + 1

            if not TYPESCRIPT_PATTERNS['class'].match(name):
                self._add_issue(str(file_path), line, "NAME-005", "warning",
                              f"Class '{name}' should use PascalCase")

        # Check interface names
        for match in re.finditer(r'interface\s+(\w+)', content):
            name = match.group(1)
            line = content[:match.start()].count('\n') + 1

            if not TYPESCRIPT_PATTERNS['interface'].match(name):
                self._add_issue(str(file_path), line, "NAME-006", "warning",
                              f"Interface '{name}' should use PascalCase")

    def _check_python_types(self, file_path: Path, content: str) -> None:
        """Check Python type annotation coverage."""
        # Find functions without return type hints
        for match in re.finditer(r'def\s+(\w+)\s*\([^)]*\)\s*:', content):
            name = match.group(1)
            line = content[:match.start()].count('\n') + 1

            if not name.startswith('_'):  # Public function
                self._add_issue(str(file_path), line, "TYPE-001", "info",
                              f"Public function '{name}' missing return type hint",
                              "Add -> ReturnType after parameters")

    def _check_python_docstrings(self, file_path: Path, content: str) -> None:
        """Check Python docstring coverage."""
        # Find public functions without docstrings
        pattern = re.compile(r'def\s+([a-z]\w*)\s*\([^)]*\):\s*\n(\s+)(?!["\'])')

        for match in pattern.finditer(content):
            name = match.group(1)
            line = content[:match.start()].count('\n') + 1

            self._add_issue(str(file_path), line, "DOC-001", "warning",
                          f"Public function '{name}' missing docstring",
                          'Add """Description.""" after function definition')

    def _add_issue(self, file_path: str, line: int, rule: str, severity: str,
                   message: str, suggestion: Optional[str] = None) -> None:
        """Add a quality issue."""
        issue = QualityIssue(
            file_path=file_path,
            line_number=line,
            rule=rule,
            severity=severity,
            message=message,
            suggestion=suggestion
        )
        self.issues.append(issue)

        # Also add to reporter if available
        if self.reporter:
            self.reporter.add_issue(
                file=file_path,
                severity=severity,
                message=message,
                line=line,
                rule=rule,
                fix_suggestion=suggestion
            )

    def validate_directory(self, dir_path: Path, extensions: List[str] = None) -> None:
        """Validate all code files in a directory."""
        if extensions is None:
            extensions = ['.py', '.ts', '.tsx', '.js', '.jsx']

        for file_path in dir_path.rglob('*'):
            if file_path.suffix.lower() in extensions:
                # Skip test files and __pycache__
                if '__pycache__' in str(file_path) or 'node_modules' in str(file_path):
                    continue
                self.validate_file(file_path)

    def calculate_quality_score(self) -> float:
        """Calculate overall quality score (0-100)."""
        if not self.metrics:
            return 100.0

        # Scoring weights
        weights = {
            'type_coverage': 0.25,
            'docstring_coverage': 0.20,
            'no_errors': 0.30,
            'no_warnings': 0.15,
            'structure': 0.10,
        }

        # Calculate component scores
        avg_type_coverage = sum(m.type_annotation_coverage for m in self.metrics) / len(self.metrics)
        avg_doc_coverage = sum(m.docstring_coverage for m in self.metrics) / len(self.metrics)

        error_count = sum(1 for i in self.issues if i.severity == 'error')
        warning_count = sum(1 for i in self.issues if i.severity == 'warning')

        error_penalty = max(0, 100 - error_count * 10)
        warning_penalty = max(0, 100 - warning_count * 5)

        # Structure score (files under limit)
        files_under_limit = sum(1 for m in self.metrics if m.total_lines <= LIMITS['file_lines_target'])
        structure_score = (files_under_limit / len(self.metrics)) * 100 if self.metrics else 100

        # Weighted score
        score = (
            avg_type_coverage * weights['type_coverage'] +
            avg_doc_coverage * weights['docstring_coverage'] +
            error_penalty * weights['no_errors'] +
            warning_penalty * weights['no_warnings'] +
            structure_score * weights['structure']
        )

        return round(score, 1)

    def get_result(self) -> ValidationResult:
        """Get complete validation result."""
        errors = sum(1 for i in self.issues if i.severity == 'error')
        warnings = sum(1 for i in self.issues if i.severity == 'warning')
        info = sum(1 for i in self.issues if i.severity == 'info')

        return ValidationResult(
            files_analyzed=len(self.metrics),
            total_issues=len(self.issues),
            errors=errors,
            warnings=warnings,
            info=info,
            quality_score=self.calculate_quality_score(),
            issues=self.issues,
            metrics=self.metrics
        )

    def validate_with_fallback(
        self,
        target: Path,
        policy: str = "development",
        max_iterations: int = 5
    ) -> Dict[str, any]:
        """
        Validate with intelligent fallback loop.

        This method:
        1. Validates the target (file or directory)
        2. Checks confidence via Value Function
        3. If low confidence, attempts auto-correction or retry
        4. Returns final result with fallback history

        Args:
            target: Path to file or directory to validate
            policy: Autonomy policy (development, staging, production, research)
            max_iterations: Maximum fallback iterations

        Returns:
            Dict with status, result, and fallback history
        """
        if not FALLBACK_AVAILABLE:
            # Run without fallback
            if target.is_file():
                self.validate_file(target)
            else:
                self.validate_directory(target)
            return {
                "status": "fallback_unavailable",
                "result": self.get_result(),
                "iterations": 1
            }

        # Initialize fallback with specified policy
        self.init_fallback(policy=policy)

        def do_validation():
            # Reset for fresh validation
            self.issues = []
            self.metrics = []
            self.reset_checkpoints()

            if target.is_file():
                self.validate_file(target)
            else:
                self.validate_directory(target)

            return self.get_result()

        # Run with fallback loop
        fallback_result = self.run_with_fallback(
            do_validation,
            max_iterations=max_iterations
        )

        return fallback_result

    def print_fallback_summary(self, fallback_result: Dict[str, any]) -> None:
        """Print summary of fallback execution."""
        print(f"\n{'=' * 60}")
        print(f"  INTELLIGENT FALLBACK SUMMARY")
        print(f"{'=' * 60}\n")

        status = fallback_result.get("status", "unknown")
        iterations = fallback_result.get("iterations", 0)
        history = fallback_result.get("history", [])

        status_color = {
            "success": Colors.GREEN,
            "escalated": Colors.YELLOW,
            "max_iterations": Colors.RED,
            "fallback_unavailable": Colors.BLUE
        }.get(status, Colors.END)

        print(f"Status: {status_color}{status.upper()}{Colors.END}")
        print(f"Iterations: {iterations}")

        if history:
            print(f"\nFallback History:")
            for entry in history:
                action = entry.get("action", "?")
                confidence = entry.get("confidence", 0)
                symbol = CHECK if action in ["PROCEED", "PROCEED_WITH_WARNING"] else WARNING
                print(f"  {symbol} Iteration {entry.get('iteration', '?')}: {action} (confidence: {confidence:.1%})")

        if status == "escalated":
            fallback = fallback_result.get("fallback", {})
            questions = fallback.get("questions", [])
            if questions:
                print(f"\n{Colors.YELLOW}Questions for human review:{Colors.END}")
                for q in questions:
                    print(f"  - {q.get('question', '?')}")

        print(f"\n{'=' * 60}\n")

    def print_report(self, result: ValidationResult) -> None:
        """Print validation report to console."""
        print(f"\n{'=' * 60}")
        print(f"  CODE QUALITY VALIDATION REPORT")
        print(f"{'=' * 60}\n")

        # Summary
        status_color = Colors.GREEN if result.errors == 0 else Colors.RED
        status = "PASS" if result.errors == 0 else "FAIL"

        print(f"Status: {status_color}{status}{Colors.END}")
        print(f"Quality Score: {result.quality_score}/100")
        print(f"Files Analyzed: {result.files_analyzed}")
        print(f"Issues: {result.errors} errors, {result.warnings} warnings, {result.info} info\n")

        # Issues by severity
        if result.issues:
            print(f"{'-' * 60}")  # ASCII-safe
            print("ISSUES:\n")

            for severity in ['error', 'warning', 'info']:
                severity_issues = [i for i in result.issues if i.severity == severity]
                if severity_issues:
                    color = {'error': Colors.RED, 'warning': Colors.YELLOW, 'info': Colors.BLUE}[severity]
                    print(f"{color}{severity.upper()}S ({len(severity_issues)}):{Colors.END}")

                    for issue in severity_issues[:10]:  # Limit to 10 per severity
                        loc = f":{issue.line_number}" if issue.line_number else ""
                        print(f"  [{issue.rule}] {issue.file_path}{loc}")
                        print(f"    {issue.message}")
                        if issue.suggestion:
                            print(f"    {Colors.CYAN}Fix: {issue.suggestion}{Colors.END}")
                    print()

        # Metrics summary
        if result.metrics:
            print(f"{'-' * 60}")  # ASCII-safe
            print("METRICS SUMMARY:\n")

            avg_type = sum(m.type_annotation_coverage for m in result.metrics) / len(result.metrics)
            avg_doc = sum(m.docstring_coverage for m in result.metrics) / len(result.metrics)
            avg_lines = sum(m.total_lines for m in result.metrics) / len(result.metrics)

            print(f"  Avg Type Coverage: {avg_type:.1f}%")
            print(f"  Avg Doc Coverage: {avg_doc:.1f}%")
            print(f"  Avg File Length: {avg_lines:.0f} lines")

        print(f"\n{'=' * 60}\n")

    def generate_report(self, result: ValidationResult) -> Optional[str]:
        """Generate ##report (JSON + MD)."""
        if not self.reporter or not self.output_dir:
            return None

        # Add recommendations
        if result.errors > 0:
            self.reporter.add_recommendation("Fix all errors before proceeding")
        if result.quality_score < 70:
            self.reporter.add_recommendation("Quality score below threshold - review code conventions")
        if any(m.type_annotation_coverage < 50 for m in result.metrics):
            self.reporter.add_recommendation("Add type annotations to improve coverage")
        if any(m.docstring_coverage < 50 for m in result.metrics):
            self.reporter.add_recommendation("Add docstrings to public functions")

        # Generate report
        report = self.reporter.generate(
            target=f"{result.files_analyzed} files",
            passed=result.files_analyzed - len([i for i in result.issues if i.severity == 'error']),
            failed=len([i for i in result.issues if i.severity == 'error']),
            warnings=result.warnings,
            output_dir=self.output_dir
        )

        self.reporter.print_summary(report)

        return str(self.output_dir / f"{self.reporter.execution_id}.json")


def main():
    parser = argparse.ArgumentParser(
        description='Validate code against CODEXA Code Style Guide',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python validators/13_code_quality_validator.py --file src/main.py
    python validators/13_code_quality_validator.py --dir src/
    python validators/13_code_quality_validator.py --all --output-dir reports/

Quality Score Components:
    - Type annotation coverage (25%)
    - Docstring coverage (20%)
    - No errors (30%)
    - No warnings (15%)
    - Structure limits (10%)
"""
    )

    parser.add_argument('--file', type=str, help='Validate single file')
    parser.add_argument('--dir', type=str, help='Validate directory')
    parser.add_argument('--all', action='store_true', help='Validate all builders/validators')
    parser.add_argument('--output-dir', type=str, help='Directory for ##report output')
    parser.add_argument('--json', action='store_true', help='Output JSON result')
    parser.add_argument('--strict', action='store_true', help='Exit 1 if errors found')
    parser.add_argument('--gradient', action='store_true',
                       help='Output Value Function gradient report (v2.1.0)')
    parser.add_argument('--gradient-json', action='store_true',
                       help='Output gradient report as JSON')
    parser.add_argument('--fallback', action='store_true',
                       help='Enable intelligent fallback loop (v2.2.0)')
    parser.add_argument('--policy', type=str, default='development',
                       choices=['development', 'staging', 'production', 'research', 'testing'],
                       help='Autonomy policy for fallback (default: development)')
    parser.add_argument('--max-iterations', type=int, default=5,
                       help='Maximum fallback iterations (default: 5)')

    args = parser.parse_args()

    # Parse output directory
    output_dir = Path(args.output_dir) if args.output_dir else None

    # Create validator
    validator = CodeQualityValidator(output_dir=output_dir)

    # Determine what to validate
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"{Colors.RED}Error: File not found: {args.file}{Colors.END}")
            sys.exit(1)
        validator.validate_file(file_path)

    elif args.dir:
        dir_path = Path(args.dir)
        if not dir_path.exists():
            print(f"{Colors.RED}Error: Directory not found: {args.dir}{Colors.END}")
            sys.exit(1)
        validator.validate_directory(dir_path)

    elif args.all:
        # Validate builders and validators
        codexa_root = Path(__file__).parent.parent
        target_dirs = [codexa_root / 'builders', codexa_root / 'validators']

        if args.fallback and FALLBACK_AVAILABLE:
            # Run with intelligent fallback
            all_results = []
            for target_dir in target_dirs:
                if target_dir.exists():
                    fb_result = validator.validate_with_fallback(
                        target_dir,
                        policy=args.policy,
                        max_iterations=args.max_iterations
                    )
                    all_results.append(fb_result)
                    validator.print_fallback_summary(fb_result)

            # Get final result from last iteration
            result = validator.get_result()

            # Print combined fallback summary
            print(f"\n{Colors.CYAN}Fallback mode complete. Policy: {args.policy}{Colors.END}\n")
        else:
            for target_dir in target_dirs:
                if target_dir.exists():
                    validator.validate_directory(target_dir)

    else:
        parser.print_help()
        sys.exit(0)

    # Handle fallback mode for single file/dir
    if args.fallback and FALLBACK_AVAILABLE and (args.file or args.dir):
        target = Path(args.file) if args.file else Path(args.dir)
        fb_result = validator.validate_with_fallback(
            target,
            policy=args.policy,
            max_iterations=args.max_iterations
        )
        validator.print_fallback_summary(fb_result)

        # Check if escalation needed
        if fb_result.get("status") == "escalated":
            print(f"{Colors.YELLOW}{WARNING} Validation escalated - human review required{Colors.END}")
            if args.strict:
                sys.exit(2)

    # Get results
    result = validator.get_result()

    # Output - check for gradient mode first (v2.1.0)
    if args.gradient_json and VALUE_FUNCTION_AVAILABLE:
        gradient_report = validator.generate_gradient_report()
        if gradient_report:
            print(json.dumps(gradient_report.to_dict(), indent=2))
        else:
            print('{"error": "No gradient report available"}')
    elif args.gradient and VALUE_FUNCTION_AVAILABLE:
        # Print gradient summary
        gradient_report = validator.generate_gradient_report()
        if gradient_report:
            validator.print_gradient_summary(gradient_report)
            # Also print traditional report
            print("\n--- Traditional Report ---")
            validator.print_report(result)
        else:
            print("No gradient report available (no files validated)")
            validator.print_report(result)
    elif args.json:
        output = {
            'files_analyzed': result.files_analyzed,
            'quality_score': result.quality_score,
            'total_issues': result.total_issues,
            'errors': result.errors,
            'warnings': result.warnings,
            'info': result.info,
            'issues': [asdict(i) for i in result.issues],
            'metrics': [asdict(m) for m in result.metrics],
        }
        # Add gradient data if available (v2.1.0)
        if VALUE_FUNCTION_AVAILABLE:
            gradient_report = validator.generate_gradient_report()
            if gradient_report:
                output['gradient'] = gradient_report.to_dict()
        print(json.dumps(output, indent=2))
    else:
        validator.print_report(result)

    # Generate ##report
    if output_dir:
        report_path = validator.generate_report(result)
        if report_path:
            print(f"{Colors.GREEN}{CHECK} ##report saved to: {output_dir}/{Colors.END}")

    # Exit code - check gradient for more nuanced exit (v2.1.0)
    if args.strict:
        if VALUE_FUNCTION_AVAILABLE:
            gradient_report = validator.generate_gradient_report()
            if gradient_report and gradient_report.escalation_required:
                sys.exit(2)  # Critical escalation
        if result.errors > 0:
            sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
