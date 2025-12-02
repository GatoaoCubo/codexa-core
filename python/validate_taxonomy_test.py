#!/usr/bin/env python3
"""
Unit tests for taxonomy validation script

Run with: python scripts/validate_taxonomy_test.py
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from validate_taxonomy import (
    TaxonomyValidator,
    TaxonomyIssue,
    TAXONOMY_MAPPINGS,
    STANDALONE_PATTERN
)


class TestTaxonomyPatterns(unittest.TestCase):
    """Test pattern matching for old path references"""

    def test_standalone_pattern_matches_codex_anuncio(self):
        """Test that pattern matches codex-anuncio-agent-standalone"""
        text = "See codex-anuncio-agent-standalone/config/plans/"
        match = STANDALONE_PATTERN.search(text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), 'codex-anuncio-agent-standalone')

    def test_standalone_pattern_matches_meta_pesquisa(self):
        """Test that pattern matches meta-pesquisa-agent-standalone"""
        text = "Check meta-pesquisa-agent-standalone/prompts/"
        match = STANDALONE_PATTERN.search(text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), 'meta-pesquisa-agent-standalone')

    def test_standalone_pattern_matches_brand(self):
        """Test that pattern matches brand-agent-standalone"""
        text = "Go to brand-agent-standalone/config/"
        match = STANDALONE_PATTERN.search(text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), 'brand-agent-standalone')

    def test_standalone_pattern_matches_ml_knowledge(self):
        """Test that pattern matches ml-knowledge-agent-standalone"""
        text = "Use ml-knowledge-agent-standalone/data/"
        match = STANDALONE_PATTERN.search(text)
        self.assertIsNotNone(match)
        self.assertEqual(match.group(1), 'ml-knowledge-agent-standalone')

    def test_standalone_pattern_no_match_correct_path(self):
        """Test that pattern doesn't match correct new paths"""
        text = "See anuncio-agent/config/plans/"
        match = STANDALONE_PATTERN.search(text)
        self.assertIsNone(match)

    def test_standalone_pattern_multiple_matches(self):
        """Test finding multiple old references in one line"""
        text = "Copy from codex-anuncio-agent-standalone/ to brand-agent-standalone/"
        matches = list(STANDALONE_PATTERN.finditer(text))
        self.assertEqual(len(matches), 2)
        self.assertEqual(matches[0].group(1), 'codex-anuncio-agent-standalone')
        self.assertEqual(matches[1].group(1), 'brand-agent-standalone')


class TestTaxonomyMappings(unittest.TestCase):
    """Test taxonomy mapping dictionary"""

    def test_all_old_paths_have_mappings(self):
        """Test that all old path patterns have replacement mappings"""
        expected_mappings = {
            'codex-anuncio-agent-standalone': 'anuncio-agent',
            'meta-pesquisa-agent-standalone': 'pesquisa-agent',
            'brand-agent-standalone': 'brand-agent',
            'ml-knowledge-agent-standalone': 'knowledge-agent',
        }
        self.assertEqual(TAXONOMY_MAPPINGS, expected_mappings)

    def test_mapping_values_are_correct(self):
        """Test that replacement values are correct new paths"""
        self.assertEqual(TAXONOMY_MAPPINGS['codex-anuncio-agent-standalone'], 'anuncio-agent')
        self.assertEqual(TAXONOMY_MAPPINGS['meta-pesquisa-agent-standalone'], 'pesquisa-agent')
        self.assertEqual(TAXONOMY_MAPPINGS['brand-agent-standalone'], 'brand-agent')
        self.assertEqual(TAXONOMY_MAPPINGS['ml-knowledge-agent-standalone'], 'knowledge-agent')


class TestTaxonomyIssue(unittest.TestCase):
    """Test TaxonomyIssue class"""

    def test_issue_creation(self):
        """Test creating a taxonomy issue"""
        issue = TaxonomyIssue(
            file_path=".claude/commands/hop_anuncio.md",
            line_num=95,
            line_content="Path: codex-anuncio-agent-standalone/config/",
            old_path="codex-anuncio-agent-standalone",
            new_path="anuncio-agent"
        )
        self.assertEqual(issue.file_path, ".claude/commands/hop_anuncio.md")
        self.assertEqual(issue.line_num, 95)
        self.assertEqual(issue.old_path, "codex-anuncio-agent-standalone")
        self.assertEqual(issue.new_path, "anuncio-agent")

    def test_issue_format_report(self):
        """Test issue formatting for report"""
        issue = TaxonomyIssue(
            file_path="test.md",
            line_num=10,
            line_content="Reference to codex-anuncio-agent-standalone",
            old_path="codex-anuncio-agent-standalone",
            new_path="anuncio-agent"
        )
        report = issue.format_report()
        self.assertIn("test.md:10", report)
        self.assertIn("codex-anuncio-agent-standalone", report)
        self.assertIn("anuncio-agent", report)


class TestTaxonomyValidator(unittest.TestCase):
    """Test TaxonomyValidator class"""

    def setUp(self):
        """Create temporary directory for testing"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        self.validator = TaxonomyValidator(self.test_path)

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)

    def test_find_markdown_files(self):
        """Test finding markdown files in directory"""
        # Create test markdown files
        (self.test_path / "test1.md").write_text("# Test 1")
        (self.test_path / "test2.md").write_text("# Test 2")
        (self.test_path / "test.txt").write_text("Not markdown")

        md_files = self.validator.find_markdown_files()
        self.assertEqual(len(md_files), 2)
        self.assertTrue(all(f.suffix == '.md' for f in md_files))

    def test_find_markdown_files_excludes_git(self):
        """Test that .git directory is excluded from scanning"""
        git_dir = self.test_path / ".git"
        git_dir.mkdir()
        (git_dir / "test.md").write_text("# Should be excluded")
        (self.test_path / "test.md").write_text("# Should be included")

        md_files = self.validator.find_markdown_files()
        self.assertEqual(len(md_files), 1)
        self.assertNotIn(".git", str(md_files[0]))

    def test_scan_file_detects_issue(self):
        """Test scanning a file and detecting taxonomy issues"""
        test_file = self.test_path / "test.md"
        test_file.write_text(
            "# Test\n"
            "Reference to codex-anuncio-agent-standalone/config/\n"
            "Another line with brand-agent-standalone/\n"
        )

        issues = self.validator.scan_file(test_file)
        self.assertEqual(len(issues), 2)
        self.assertEqual(issues[0].old_path, "codex-anuncio-agent-standalone")
        self.assertEqual(issues[0].new_path, "anuncio-agent")
        self.assertEqual(issues[0].line_num, 2)
        self.assertEqual(issues[1].old_path, "brand-agent-standalone")
        self.assertEqual(issues[1].new_path, "brand-agent")
        self.assertEqual(issues[1].line_num, 3)

    def test_scan_file_no_issues(self):
        """Test scanning a file with correct paths"""
        test_file = self.test_path / "test.md"
        test_file.write_text(
            "# Test\n"
            "Reference to anuncio-agent/config/\n"
            "Another line with brand-agent/\n"
        )

        issues = self.validator.scan_file(test_file)
        self.assertEqual(len(issues), 0)

    def test_scan_all_multiple_files(self):
        """Test scanning multiple files"""
        (self.test_path / "file1.md").write_text("Path: codex-anuncio-agent-standalone/")
        (self.test_path / "file2.md").write_text("Path: meta-pesquisa-agent-standalone/")
        (self.test_path / "file3.md").write_text("Path: anuncio-agent/ (correct)")

        issues = self.validator.scan_all()
        self.assertEqual(len(issues), 2)

    def test_verify_path_exists(self):
        """Test path existence verification"""
        test_dir = self.test_path / "existing-dir"
        test_dir.mkdir()

        self.assertTrue(self.validator.verify_path_exists("existing-dir"))
        self.assertFalse(self.validator.verify_path_exists("non-existent-dir"))

    def test_fix_file_dry_run(self):
        """Test fixing file in dry-run mode"""
        test_file = self.test_path / "test.md"
        original_content = "Path: codex-anuncio-agent-standalone/config/"
        test_file.write_text(original_content)

        fixes = self.validator.fix_file(test_file, dry_run=True)

        # File should not be modified in dry-run
        self.assertEqual(test_file.read_text(), original_content)

    def test_fix_file_actual_fix(self):
        """Test actually fixing file"""
        test_file = self.test_path / "test.md"
        test_file.write_text("Path: codex-anuncio-agent-standalone/config/")

        self.validator.fix_file(test_file, dry_run=False)

        # File should be modified
        fixed_content = test_file.read_text()
        self.assertIn("anuncio-agent", fixed_content)
        self.assertNotIn("codex-anuncio-agent-standalone", fixed_content)

    def test_generate_report_no_issues(self):
        """Test report generation with no issues"""
        report = self.validator.generate_report()
        self.assertIn("✅", report)
        self.assertIn("no taxonomy inconsistencies", report.lower())

    def test_generate_report_with_issues(self):
        """Test report generation with issues"""
        self.validator.issues = [
            TaxonomyIssue(
                file_path="test.md",
                line_num=5,
                line_content="codex-anuncio-agent-standalone/config/",
                old_path="codex-anuncio-agent-standalone",
                new_path="anuncio-agent"
            )
        ]

        report = self.validator.generate_report()
        self.assertIn("test.md", report)
        self.assertIn("Line 5", report)
        self.assertIn("codex-anuncio-agent-standalone", report)
        self.assertIn("anuncio-agent", report)


class TestIntegration(unittest.TestCase):
    """Integration tests for complete workflow"""

    def setUp(self):
        """Create temporary directory with test files"""
        self.test_dir = tempfile.mkdtemp()
        self.test_path = Path(self.test_dir)
        self.validator = TaxonomyValidator(self.test_path)

    def tearDown(self):
        """Clean up temporary directory"""
        shutil.rmtree(self.test_dir)

    def test_complete_scan_and_fix_workflow(self):
        """Test complete workflow: scan, detect, report, fix"""
        # Create test files with issues
        (self.test_path / "file1.md").write_text(
            "# Command\n"
            "```bash\n"
            "ls -1 codex-anuncio-agent-standalone/config/plans/*.json\n"
            "```\n"
        )
        (self.test_path / "file2.md").write_text(
            "See meta-pesquisa-agent-standalone/prompts/ for details.\n"
        )

        # Scan for issues
        issues = self.validator.scan_all()
        self.assertEqual(len(issues), 2)

        # Generate report
        report = self.validator.generate_report()
        self.assertIn("file1.md", report)
        self.assertIn("file2.md", report)

        # Fix issues
        self.validator.fix_all(dry_run=False)

        # Verify fixes applied
        file1_content = (self.test_path / "file1.md").read_text()
        file2_content = (self.test_path / "file2.md").read_text()

        self.assertIn("anuncio-agent/config/plans", file1_content)
        self.assertNotIn("codex-anuncio-agent-standalone", file1_content)
        self.assertIn("pesquisa-agent/prompts", file2_content)
        self.assertNotIn("meta-pesquisa-agent-standalone", file2_content)

        # Rescan - should find no issues
        validator2 = TaxonomyValidator(self.test_path)
        issues_after = validator2.scan_all()
        self.assertEqual(len(issues_after), 0)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
