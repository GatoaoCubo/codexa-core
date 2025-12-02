"""
Validator System Tests
Tests for CODEXA validators and report generation.
"""

import pytest
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
import json


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    severity: str  # error, warning, info
    category: str
    message: str
    file: Optional[str] = None
    line: Optional[int] = None

    def to_dict(self) -> dict:
        return {
            "severity": self.severity,
            "category": self.category,
            "message": self.message,
            "file": self.file,
            "line": self.line
        }


@dataclass
class ValidationReport:
    """
    Structured validation report following ##report standard.
    """
    module: str
    version: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "pending"
    issues: list[ValidationIssue] = field(default_factory=list)
    metrics: dict = field(default_factory=dict)

    def add_issue(
        self,
        severity: str,
        category: str,
        message: str,
        file: Optional[str] = None,
        line: Optional[int] = None
    ):
        """Add an issue to the report."""
        self.issues.append(ValidationIssue(
            severity=severity,
            category=category,
            message=message,
            file=file,
            line=line
        ))

    def has_errors(self) -> bool:
        """Check if report has any errors."""
        return any(i.severity == "error" for i in self.issues)

    def has_warnings(self) -> bool:
        """Check if report has any warnings."""
        return any(i.severity == "warning" for i in self.issues)

    def count_by_severity(self) -> dict[str, int]:
        """Count issues by severity."""
        counts = {"error": 0, "warning": 0, "info": 0}
        for issue in self.issues:
            if issue.severity in counts:
                counts[issue.severity] += 1
        return counts

    def finalize(self) -> tuple[bool, str, str]:
        """
        Finalize the report and determine status.

        Returns:
            (success, json_report, md_report)
        """
        counts = self.count_by_severity()

        if counts["error"] > 0:
            self.status = "error"
        elif counts["warning"] > 0:
            self.status = "warning"
        else:
            self.status = "success"

        success = self.status != "error"

        # Generate JSON report
        json_report = json.dumps({
            "module": self.module,
            "version": self.version,
            "timestamp": self.timestamp,
            "status": self.status,
            "metrics": self.metrics,
            "issue_counts": counts,
            "issues": [i.to_dict() for i in self.issues]
        }, indent=2)

        # Generate Markdown report
        md_report = self._generate_markdown(counts)

        return success, json_report, md_report

    def _generate_markdown(self, counts: dict[str, int]) -> str:
        """Generate markdown report."""
        status_emoji = {
            "success": "✅",
            "warning": "⚠️",
            "error": "❌"
        }

        lines = [
            f"# Validation Report: {self.module}",
            "",
            f"**Version**: {self.version}",
            f"**Timestamp**: {self.timestamp}",
            f"**Status**: {status_emoji.get(self.status, '?')} {self.status.upper()}",
            "",
            "## Summary",
            "",
            f"- Errors: {counts['error']}",
            f"- Warnings: {counts['warning']}",
            f"- Info: {counts['info']}",
            ""
        ]

        if self.issues:
            lines.extend([
                "## Issues",
                ""
            ])

            for issue in self.issues:
                severity_icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}
                icon = severity_icon.get(issue.severity, "•")
                location = ""
                if issue.file:
                    location = f" ({issue.file}"
                    if issue.line:
                        location += f":{issue.line}"
                    location += ")"
                lines.append(f"- {icon} [{issue.category}] {issue.message}{location}")

        return "\n".join(lines)


class CodeQualityChecker:
    """
    Simplified code quality checker for testing.
    Mirrors validators/13_code_quality_validator.py patterns.
    """

    PYTHON_NAMING_PATTERNS = {
        'variable': r'^[a-z][a-z0-9_]*$',
        'function': r'^[a-z][a-z0-9_]*$',
        'class': r'^[A-Z][a-zA-Z0-9]*$',
        'constant': r'^[A-Z][A-Z0-9_]*$'
    }

    def __init__(self):
        self.report = None

    def check_file(self, file_path: Path) -> ValidationReport:
        """Check a Python file for quality issues."""
        self.report = ValidationReport(
            module="code_quality_checker",
            version="2.0.0"
        )

        if not file_path.exists():
            self.report.add_issue(
                severity="error",
                category="file",
                message=f"File not found: {file_path}"
            )
            return self.report

        content = file_path.read_text(encoding='utf-8')
        lines = content.split('\n')

        self._check_file_length(file_path, lines)
        self._check_line_lengths(file_path, lines)
        self._check_docstrings(file_path, content)

        self.report.metrics = {
            "lines": len(lines),
            "issues": len(self.report.issues)
        }

        return self.report

    def _check_file_length(self, file_path: Path, lines: list[str]):
        """Check file length limits."""
        if len(lines) > 600:
            self.report.add_issue(
                severity="error",
                category="structure",
                message=f"File exceeds 600 line limit ({len(lines)} lines)",
                file=str(file_path)
            )
        elif len(lines) > 400:
            self.report.add_issue(
                severity="warning",
                category="structure",
                message=f"File approaching limit ({len(lines)}/600 lines)",
                file=str(file_path)
            )

    def _check_line_lengths(self, file_path: Path, lines: list[str]):
        """Check individual line lengths."""
        for i, line in enumerate(lines, 1):
            if len(line) > 88:
                self.report.add_issue(
                    severity="warning",
                    category="style",
                    message=f"Line exceeds 88 characters ({len(line)})",
                    file=str(file_path),
                    line=i
                )

    def _check_docstrings(self, file_path: Path, content: str):
        """Check for docstrings in public functions."""
        import re

        # Find functions without docstrings
        func_pattern = r'^\s*def\s+([a-z][a-z0-9_]*)\s*\('
        for match in re.finditer(func_pattern, content, re.MULTILINE):
            func_name = match.group(1)
            if not func_name.startswith('_'):  # Public function
                # Check if next line is docstring
                start = match.end()
                remaining = content[start:start+100]
                if '"""' not in remaining[:50] and "'''" not in remaining[:50]:
                    self.report.add_issue(
                        severity="warning",
                        category="documentation",
                        message=f"Public function '{func_name}' missing docstring",
                        file=str(file_path)
                    )


class TestValidationIssue:
    """Tests for ValidationIssue."""

    def test_create_issue(self):
        """Test creating a validation issue."""
        issue = ValidationIssue(
            severity="error",
            category="syntax",
            message="Invalid syntax"
        )

        assert issue.severity == "error"
        assert issue.category == "syntax"

    def test_issue_with_location(self):
        """Test issue with file and line info."""
        issue = ValidationIssue(
            severity="warning",
            category="style",
            message="Line too long",
            file="test.py",
            line=42
        )

        data = issue.to_dict()
        assert data["file"] == "test.py"
        assert data["line"] == 42


class TestValidationReport:
    """Tests for ValidationReport."""

    def test_create_report(self):
        """Test creating a validation report."""
        report = ValidationReport(
            module="test_validator",
            version="1.0.0"
        )

        assert report.module == "test_validator"
        assert report.status == "pending"

    def test_add_issues(self):
        """Test adding issues to report."""
        report = ValidationReport(module="test", version="1.0.0")

        report.add_issue("error", "syntax", "Error 1")
        report.add_issue("warning", "style", "Warning 1")
        report.add_issue("info", "hint", "Info 1")

        assert len(report.issues) == 3
        assert report.has_errors()
        assert report.has_warnings()

    def test_count_by_severity(self):
        """Test counting issues by severity."""
        report = ValidationReport(module="test", version="1.0.0")

        report.add_issue("error", "a", "e1")
        report.add_issue("error", "b", "e2")
        report.add_issue("warning", "c", "w1")

        counts = report.count_by_severity()
        assert counts["error"] == 2
        assert counts["warning"] == 1
        assert counts["info"] == 0

    def test_finalize_with_errors(self):
        """Test finalizing report with errors."""
        report = ValidationReport(module="test", version="1.0.0")
        report.add_issue("error", "syntax", "Bad syntax")

        success, json_out, md_out = report.finalize()

        assert not success
        assert report.status == "error"
        assert "error" in json_out.lower()
        assert "❌" in md_out

    def test_finalize_with_warnings(self):
        """Test finalizing report with only warnings."""
        report = ValidationReport(module="test", version="1.0.0")
        report.add_issue("warning", "style", "Style issue")

        success, json_out, md_out = report.finalize()

        assert success  # Warnings don't fail
        assert report.status == "warning"
        assert "⚠️" in md_out

    def test_finalize_clean(self):
        """Test finalizing clean report."""
        report = ValidationReport(module="test", version="1.0.0")

        success, json_out, md_out = report.finalize()

        assert success
        assert report.status == "success"
        assert "✅" in md_out


class TestCodeQualityChecker:
    """Tests for CodeQualityChecker."""

    @pytest.fixture
    def checker(self):
        return CodeQualityChecker()

    @pytest.fixture
    def good_python_file(self, tmp_path):
        """Create a well-structured Python file."""
        content = '''"""
Module docstring.
"""

def public_function():
    """Function docstring."""
    return True

class MyClass:
    """Class docstring."""
    pass
'''
        file_path = tmp_path / "good.py"
        file_path.write_text(content)
        return file_path

    @pytest.fixture
    def bad_python_file(self, tmp_path):
        """Create a Python file with issues."""
        content = '''def public_function_without_docstring():
    return True

x = "a" * 100  # This line is very long and exceeds the limit for line length in Python files
'''
        file_path = tmp_path / "bad.py"
        file_path.write_text(content)
        return file_path

    def test_check_good_file(self, checker, good_python_file):
        """Test checking a well-structured file."""
        report = checker.check_file(good_python_file)
        success, _, _ = report.finalize()

        # May have warnings but no errors
        assert report.count_by_severity()["error"] == 0

    def test_check_bad_file(self, checker, bad_python_file):
        """Test checking a file with issues."""
        report = checker.check_file(bad_python_file)
        report.finalize()

        # Should have issues
        assert len(report.issues) > 0

    def test_nonexistent_file(self, checker, tmp_path):
        """Test checking nonexistent file."""
        report = checker.check_file(tmp_path / "nonexistent.py")
        success, _, _ = report.finalize()

        assert not success
        assert report.has_errors()

    def test_long_file(self, checker, tmp_path):
        """Test detection of file length issues."""
        # Create file with 650 lines
        content = "\n".join([f"line_{i} = {i}" for i in range(650)])
        file_path = tmp_path / "long.py"
        file_path.write_text(content)

        report = checker.check_file(file_path)
        report.finalize()

        assert report.has_errors()
        assert any("600 line limit" in i.message for i in report.issues)


class TestValidatorFilesExist:
    """Tests that actual validator files exist."""

    VALIDATORS_DIR = Path(__file__).parent.parent / "validators"

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "validators").exists(),
        reason="Validators directory not found"
    )
    def test_validators_directory_exists(self):
        """Test validators directory exists."""
        assert self.VALIDATORS_DIR.exists()

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "validators").exists(),
        reason="Validators directory not found"
    )
    def test_code_quality_validator_exists(self):
        """Test code quality validator exists."""
        validator = self.VALIDATORS_DIR / "13_code_quality_validator.py"
        assert validator.exists(), "Missing 13_code_quality_validator.py"

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "validators").exists(),
        reason="Validators directory not found"
    )
    def test_hop_sync_validator_exists(self):
        """Test HOP sync validator exists."""
        validator = self.VALIDATORS_DIR / "07_hop_sync_validator.py"
        assert validator.exists(), "Missing 07_hop_sync_validator.py"

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "validators").exists(),
        reason="Validators directory not found"
    )
    def test_report_generator_exists(self):
        """Test report generator exists."""
        generator = self.VALIDATORS_DIR / "report_generator.py"
        assert generator.exists(), "Missing report_generator.py"


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
