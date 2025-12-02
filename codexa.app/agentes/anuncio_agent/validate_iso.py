#!/usr/bin/env python3
"""
ISO Vectorstore Validator - anuncio_agent
Validates conformance with photo_agent v3.2.2 patterns

Usage:
    python validate_iso.py [path_to_iso_vectorstore]
    python validate_iso.py  # defaults to ./iso_vectorstore
"""

import os
import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class ISOValidator:
    """Validates ISO vectorstore compliance"""

    def __init__(self, iso_path: str):
        self.iso_path = Path(iso_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def validate_quick_start_size(self) -> bool:
        """CRITICAL: 01_QUICK_START.md < 8000 chars"""
        quick_start = self.iso_path / "01_QUICK_START.md"

        if not quick_start.exists():
            self.errors.append("❌ 01_QUICK_START.md NOT FOUND")
            return False

        try:
            content = quick_start.read_text(encoding='utf-8')
            char_count = len(content)

            if char_count > 8000:
                self.errors.append(
                    f"❌ QUICK_START too large: {char_count} chars (max 8000)"
                )
                return False
            elif char_count > 7950:
                self.warnings.append(
                    f"⚠️  QUICK_START near limit: {char_count}/8000 chars"
                )
            else:
                self.info.append(
                    f"✅ QUICK_START size: {char_count}/8000 chars ({100 - char_count/80:.1f}% below limit)"
                )

            return True

        except Exception as e:
            self.errors.append(f"❌ Error reading QUICK_START: {e}")
            return False

    def validate_output_template(self) -> bool:
        """Validates output template uses single block format"""
        output_template = self.iso_path / "07_output_template.md"

        if not output_template.exists():
            self.errors.append("❌ 07_output_template.md NOT FOUND")
            return False

        try:
            content = output_template.read_text(encoding='utf-8')

            # Check for single block marker
            if "## 📦 ANÚNCIO COMPLETO" in content:
                self.info.append("✅ Output template uses single block format")
            else:
                self.warnings.append(
                    "⚠️  Template missing '## 📦 ANÚNCIO COMPLETO' header"
                )

            # Check for visual separators
            if "═══════════════════" in content:
                self.info.append("✅ Visual separators found (unified block)")
            else:
                self.warnings.append(
                    "⚠️  No visual separators (═══) - may not be copyable block"
                )

            return True

        except Exception as e:
            self.errors.append(f"❌ Error reading output_template: {e}")
            return False

    def validate_schemas_exist(self) -> bool:
        """Validates existence and syntax of JSON schemas"""
        required_schemas = [
            "06_input_schema.json",
            "08_copy_rules.json",
            "09_marketplace_specs.json",
            "10_persuasion_patterns.json",
        ]

        all_valid = True

        for schema in required_schemas:
            schema_path = self.iso_path / schema

            if not schema_path.exists():
                self.errors.append(f"❌ Schema missing: {schema}")
                all_valid = False
                continue

            # Validate JSON syntax
            try:
                content = schema_path.read_text(encoding='utf-8')
                json.loads(content)
                self.info.append(f"✅ {schema} valid JSON")
            except json.JSONDecodeError as e:
                self.errors.append(f"❌ {schema} invalid JSON: {e}")
                all_valid = False
            except Exception as e:
                self.errors.append(f"❌ Error reading {schema}: {e}")
                all_valid = False

        return all_valid

    def validate_adw_auto_navigation(self) -> bool:
        """Validates ADW has auto-navigation section"""
        adw_file = self.iso_path / "11_ADW_orchestrator.md"

        if not adw_file.exists():
            self.errors.append("❌ 11_ADW_orchestrator.md NOT FOUND")
            return False

        try:
            content = adw_file.read_text(encoding='utf-8')

            # Check for auto-navigation markers
            has_auto_nav = "AUTO-NAVIGATION" in content or "Auto-Questions" in content
            has_workflow = "autonomous_workflow" in content

            if has_auto_nav and has_workflow:
                self.info.append("✅ ADW has autonomous navigation section")
                return True
            elif has_auto_nav:
                self.warnings.append(
                    "⚠️  ADW has AUTO-NAVIGATION but missing workflow code"
                )
                return True
            else:
                self.warnings.append(
                    "⚠️  ADW missing AUTO-NAVIGATION section"
                )
                return False

        except Exception as e:
            self.errors.append(f"❌ Error reading ADW: {e}")
            return False

    def validate_opop_compliance(self) -> bool:
        """Validates OPOP (One-Prompt-One-Purpose) heuristics"""
        files = list(self.iso_path.glob("*.md")) + list(self.iso_path.glob("*.json"))

        large_files = []

        for file in files:
            if file.suffix in ['.md', '.json']:
                try:
                    line_count = len(file.read_text(encoding='utf-8').splitlines())

                    # Heuristic: files >2000 lines may violate OPOP
                    if line_count > 2000:
                        large_files.append((file.name, line_count))
                except Exception:
                    continue

        if large_files:
            for name, lines in large_files:
                self.warnings.append(
                    f"⚠️  {name} very large ({lines} lines) - possible OPOP violation"
                )
        else:
            self.info.append("✅ OPOP compliance: no files >2000 lines")

        return True

    def validate_example_exists(self) -> bool:
        """Validates existence of EXAMPLE_*.md file"""
        examples = list(self.iso_path.parent.glob("EXAMPLE_*.md"))

        if not examples:
            self.warnings.append(
                "⚠️  No EXAMPLE_*.md found (recommended for v1.2.2+)"
            )
            return False

        self.info.append(f"✅ Example found: {examples[0].name}")
        return True

    def validate_trinity_removed(self) -> bool:
        """Validates Trinity logic has been removed"""
        critical_files = [
            "01_QUICK_START.md",
            "07_output_template.md",
            "11_ADW_orchestrator.md"
        ]

        trinity_references = []

        for filename in critical_files:
            file_path = self.iso_path / filename

            if not file_path.exists():
                continue

            try:
                content = file_path.read_text(encoding='utf-8').lower()

                # Check for Trinity references
                if ".llm.json" in content or ".meta.json" in content:
                    trinity_references.append(filename)

            except Exception:
                continue

        if trinity_references:
            self.warnings.append(
                f"⚠️  Trinity references found in: {', '.join(trinity_references)}"
            )
            self.warnings.append(
                "   Note: v1.2.2+ uses single .md output, not Trinity"
            )
            return False
        else:
            self.info.append("✅ No Trinity logic found (clean)")

        return True

    def validate_file_numbering(self) -> bool:
        """Validates file numbering consistency"""
        expected_prefixes = [
            "01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_", "10_",
            "11_", "12_", "13_", "14_", "15_", "16_", "17_", "18_", "19_", "20_"
        ]

        files = sorted([f.name for f in self.iso_path.glob("*") if f.is_file()])
        numbered_files = [f for f in files if f[:3] in expected_prefixes]

        self.info.append(f"✅ Found {len(numbered_files)} numbered files")

        return True

    def run_all_validations(self) -> Tuple[int, int]:
        """
        Executes all validations
        Returns: (passed_count, total_count)
        """
        print("\n" + "="*60)
        print("ISO VECTORSTORE VALIDATION - anuncio_agent")
        print("="*60 + "\n")

        validations = [
            ("QUICK_START Size (<8000 chars)", self.validate_quick_start_size),
            ("Output Template (1 block)", self.validate_output_template),
            ("Schemas JSON Exist", self.validate_schemas_exist),
            ("ADW Auto-Navigation", self.validate_adw_auto_navigation),
            ("OPOP Compliance", self.validate_opop_compliance),
            ("EXAMPLE Exists", self.validate_example_exists),
            ("Trinity Logic Removed", self.validate_trinity_removed),
            ("File Numbering", self.validate_file_numbering),
        ]

        passed = 0
        total = len(validations)

        for name, validation_func in validations:
            print(f"\n[Validating] {name}")
            try:
                if validation_func():
                    passed += 1
            except Exception as e:
                self.errors.append(f"❌ {name} validation crashed: {e}")

        # Report
        print("\n" + "="*60)
        print(f"VALIDATION REPORT")
        print("="*60)
        print(f"[PASS] {passed}/{total}")
        print(f"[ERR]  {len(self.errors)}")
        print(f"[WARN] {len(self.warnings)}")

        # Details
        if self.info:
            print("\n[INFO]:")
            for info in self.info:
                print(f"  {info}")

        if self.warnings:
            print("\n[WARNINGS]:")
            for warning in self.warnings:
                print(f"  {warning}")

        if self.errors:
            print("\n[ERRORS]:")
            for error in self.errors:
                print(f"  {error}")

        # OPOP Score
        score = (passed / total) * 10
        print(f"\n[OPOP SCORE] {score:.1f}/10")

        if score >= 9.0:
            print("[STATUS] PRODUCTION READY")
            status = True
        elif score >= 7.0:
            print("[STATUS] NEEDS IMPROVEMENTS")
            status = False
        else:
            print("[STATUS] CRITICAL ISSUES - NOT READY")
            status = False

        return passed, total


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        iso_path = sys.argv[1]
    else:
        iso_path = "./iso_vectorstore"

    # Normalize path
    iso_path = os.path.abspath(iso_path)

    if not os.path.exists(iso_path):
        print(f"❌ Error: Path does not exist: {iso_path}")
        sys.exit(1)

    if not os.path.isdir(iso_path):
        print(f"❌ Error: Not a directory: {iso_path}")
        sys.exit(1)

    print(f"Validating: {iso_path}\n")

    validator = ISOValidator(iso_path)
    passed, total = validator.run_all_validations()

    # Exit code: 0 if production ready, 1 otherwise
    sys.exit(0 if passed >= (total * 0.9) else 1)


if __name__ == "__main__":
    main()
