#!/usr/bin/env python3
"""
Python Integrity Test Script for TAC-7 Repository
Tests all Python files for syntax errors, import errors, and dependency issues.
"""

import sys
import os
import py_compile
import importlib.util
import ast
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class TestResult:
    """Result of testing a single Python file"""
    file_path: str
    category: str  # 'script', 'backend', 'agent', 'adw', 'hook'
    syntax_ok: bool = True
    syntax_error: str = ""
    import_ok: bool = True
    import_error: str = ""
    dependencies: List[str] = field(default_factory=list)
    missing_deps: List[str] = field(default_factory=list)
    circular_imports: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def is_ok(self) -> bool:
        """Check if all tests passed"""
        return (self.syntax_ok and self.import_ok and
                not self.missing_deps and not self.circular_imports)

class PythonIntegrityTester:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root)
        self.results: Dict[str, TestResult] = {}
        self.py_files: Dict[str, List[Path]] = defaultdict(list)

    def discover_python_files(self):
        """Discover all Python files organized by category"""
        # Scripts
        scripts_dir = self.repo_root / "scripts"
        if scripts_dir.exists():
            for py_file in scripts_dir.glob("*.py"):
                if py_file.name != "test_python_integrity.py":
                    self.py_files["script"].append(py_file)

        # Backend core modules
        core_dir = self.repo_root / "app" / "server" / "core"
        if core_dir.exists():
            for py_file in core_dir.glob("*.py"):
                self.py_files["backend"].append(py_file)

        # Backend tests
        tests_dir = self.repo_root / "app" / "server" / "tests"
        if tests_dir.exists():
            for py_file in tests_dir.glob("**/*.py"):
                if py_file.name != "__pycache__":
                    self.py_files["backend_test"].append(py_file)

        # Backend main
        server_main = self.repo_root / "app" / "server" / "server.py"
        if server_main.exists():
            self.py_files["backend"].append(server_main)

        # Agent files
        for agent_dir in self.repo_root.glob("*-agent"):
            for py_file in agent_dir.glob("*.py"):
                self.py_files["agent"].append(py_file)
            for py_file in agent_dir.glob("tests/**/*.py"):
                if py_file.name != "__pycache__":
                    self.py_files["agent_test"].append(py_file)

        # ADW modules
        adws_dir = self.repo_root / "adws"
        if adws_dir.exists():
            for py_file in adws_dir.glob("**/*.py"):
                if "__pycache__" not in str(py_file):
                    self.py_files["adw"].append(py_file)

        # Claude Code hooks
        hooks_dir = self.repo_root / ".claude" / "hooks"
        if hooks_dir.exists():
            for py_file in hooks_dir.glob("**/*.py"):
                if "__pycache__" not in str(py_file):
                    self.py_files["hook"].append(py_file)

        # Claude Code utilities
        utils_dir = self.repo_root / ".claude" / "commands"
        if utils_dir.exists():
            for py_file in utils_dir.glob("*.py"):
                self.py_files["hook"].append(py_file)

    def test_syntax(self, file_path: Path) -> Tuple[bool, str]:
        """Test Python syntax using py_compile"""
        try:
            py_compile.compile(str(file_path), doraise=True)
            return True, ""
        except py_compile.PyCompileError as e:
            return False, str(e)

    def get_imports_from_ast(self, file_path: Path) -> List[str]:
        """Extract import statements from file using AST"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read())

            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append(node.module)
            return imports
        except Exception as e:
            return []

    def test_imports(self, file_path: Path) -> Tuple[bool, str, List[str]]:
        """Try to import the file and detect missing dependencies"""
        try:
            spec = importlib.util.spec_from_file_location("test_module", str(file_path))
            if spec is None or spec.loader is None:
                return False, "Could not load module spec", []

            # Create a unique module name based on file path to avoid conflicts
            module_name = f"test_module_{id(file_path)}"
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module

            try:
                spec.loader.exec_module(module)
                return True, "", self.get_imports_from_ast(file_path)
            except ModuleNotFoundError as e:
                missing = str(e).split("'")[1] if "'" in str(e) else str(e)
                return False, str(e), []
            except Exception as e:
                # Try to extract imports anyway for documentation
                return False, str(e), self.get_imports_from_ast(file_path)
            finally:
                # Clean up module
                if module_name in sys.modules:
                    del sys.modules[module_name]
        except Exception as e:
            return False, str(e), self.get_imports_from_ast(file_path)

    def categorize_file(self, file_path: Path) -> str:
        """Determine the category of a file"""
        rel_path = str(file_path.relative_to(self.repo_root))

        if rel_path.startswith("scripts"):
            return "script"
        elif rel_path.startswith("app/server"):
            return "backend"
        elif "agent" in rel_path:
            return "agent"
        elif rel_path.startswith("adws"):
            return "adw"
        elif rel_path.startswith(".claude"):
            return "hook"
        else:
            return "other"

    def test_file(self, file_path: Path) -> TestResult:
        """Test a single Python file"""
        rel_path = str(file_path.relative_to(self.repo_root))
        category = self.categorize_file(file_path)

        result = TestResult(
            file_path=rel_path,
            category=category
        )

        try:
            # Test syntax
            result.syntax_ok, result.syntax_error = self.test_syntax(file_path)

            # Test imports only for non-script files (scripts can have execution side effects)
            if result.syntax_ok and category != "script":
                try:
                    result.import_ok, result.import_error, result.dependencies = self.test_imports(file_path)
                except Exception as e:
                    result.import_ok = False
                    result.import_error = f"Import test error: {str(e)[:100]}"
            elif result.syntax_ok and category == "script":
                # For scripts, just check for imports via AST
                result.dependencies = self.get_imports_from_ast(file_path)
        except Exception as e:
            result.syntax_ok = False
            result.syntax_error = f"Test error: {str(e)[:100]}"

        return result

    def run_all_tests(self):
        """Run all tests"""
        self.discover_python_files()

        total_files = sum(len(files) for files in self.py_files.values())
        print(f"Found {total_files} Python files to test")
        print("-" * 80)

        for category, files in sorted(self.py_files.items()):
            print(f"\nTesting {category.upper()} ({len(files)} files):")
            for file_path in sorted(files):
                try:
                    result = self.test_file(file_path)
                    self.results[result.file_path] = result

                    status = "[OK]" if result.is_ok() else "[FAIL]"
                    print(f"  {status} {result.file_path}")

                    if result.syntax_error:
                        print(f"      Syntax Error: {result.syntax_error[:100]}")
                    if result.import_error:
                        print(f"      Import Error: {result.import_error[:100]}")
                except Exception as e:
                    # Fallback for files that cause issues
                    rel_path = str(file_path.relative_to(self.repo_root))
                    result = TestResult(file_path=rel_path, category=category)
                    result.syntax_ok = False
                    result.syntax_error = f"Test exception: {str(e)[:100]}"
                    self.results[rel_path] = result
                    print(f"  [ERR] {rel_path}")
                    print(f"      Error: {str(e)[:100]}")

    def generate_report(self) -> str:
        """Generate a comprehensive report"""
        report = []
        report.append("# Python Integrity Test Report - TAC-7\n")
        report.append(f"**Test Date**: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.append(f"**Python Version**: {sys.version}\n")
        report.append(f"**Repository Root**: {self.repo_root}\n")

        # Summary statistics
        total = len(self.results)
        passing = sum(1 for r in self.results.values() if r.is_ok())
        failing = total - passing

        report.append(f"\n## Summary\n")
        report.append(f"- **Total Files Tested**: {total}\n")
        report.append(f"- **Passing**: {passing} ({100*passing//total if total > 0 else 0}%)\n")
        report.append(f"- **Failing**: {failing} ({100*failing//total if total > 0 else 0}%)\n")

        # Results by category
        by_category = defaultdict(lambda: {"total": 0, "passing": 0})
        for result in self.results.values():
            by_category[result.category]["total"] += 1
            if result.is_ok():
                by_category[result.category]["passing"] += 1

        report.append(f"\n## Results by Category\n")
        for category in sorted(by_category.keys()):
            stats = by_category[category]
            pct = 100 * stats["passing"] // stats["total"] if stats["total"] > 0 else 0
            report.append(f"- **{category.upper()}**: {stats['passing']}/{stats['total']} passing ({pct}%)\n")

        # Passing files
        passing_results = [r for r in self.results.values() if r.is_ok()]
        if passing_results:
            report.append(f"\n## [OK] Modules Working Correctly ({len(passing_results)})\n")
            by_cat = defaultdict(list)
            for result in passing_results:
                by_cat[result.category].append(result.file_path)

            for category in sorted(by_cat.keys()):
                report.append(f"\n### {category.upper()}\n")
                for file_path in sorted(by_cat[category]):
                    report.append(f"- {file_path}\n")

        # Failing files with details
        failing_results = [r for r in self.results.values() if not r.is_ok()]
        if failing_results:
            report.append(f"\n## [FAIL] Modules with Problems ({len(failing_results)})\n")

            for result in sorted(failing_results, key=lambda r: r.file_path):
                report.append(f"\n### {result.file_path}\n")
                report.append(f"**Category**: {result.category}\n\n")

                if not result.syntax_ok:
                    report.append(f"**Syntax Error**:\n```\n{result.syntax_error}\n```\n\n")

                if not result.import_ok:
                    report.append(f"**Import Error**:\n```\n{result.import_error}\n```\n\n")

                if result.dependencies:
                    report.append(f"**Dependencies Detected**: {', '.join(sorted(set(result.dependencies)))}\n\n")

                if result.warnings:
                    report.append(f"**Warnings**:\n")
                    for warning in result.warnings:
                        report.append(f"- {warning}\n")
                    report.append("\n")

        # Warnings section
        all_warnings = [w for r in self.results.values() for w in r.warnings]
        if all_warnings:
            report.append(f"\n## [WARN] Warnings ({len(all_warnings)})\n")
            for warning in sorted(set(all_warnings)):
                report.append(f"- {warning}\n")

        # Recommendations
        report.append(f"\n## Recommendations\n")
        if failing_results:
            report.append(f"\n1. **Fix Syntax Errors**: {sum(1 for r in failing_results if not r.syntax_ok)} files have syntax errors\n")
            report.append(f"2. **Install Missing Dependencies**: Check error messages for missing packages\n")
            report.append(f"3. **Resolve Import Issues**: {sum(1 for r in failing_results if not r.import_ok)} files have import problems\n")
        else:
            report.append("[OK] All Python files pass integrity checks!\n")

        return "".join(report)

def main():
    # Get repo root from various possible locations
    repo_root = (
        os.environ.get("REPO_ROOT") or
        os.path.dirname(os.path.abspath(__file__))
    )

    print(f"Repository root: {repo_root}")

    tester = PythonIntegrityTester(repo_root)
    tester.run_all_tests()

    report = tester.generate_report()

    # Save report with UTF-8 encoding
    report_path = Path(repo_root) / "PYTHON_INTEGRITY_TEST_REPORT.md"
    report_path.write_text(report, encoding='utf-8')

    print(f"\nReport saved to: {report_path}")

if __name__ == "__main__":
    main()
