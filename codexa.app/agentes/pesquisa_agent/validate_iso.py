#!/usr/bin/env python3
"""
ISO Vectorstore Validator - pesquisa_agent
Validates conformance with anuncio_agent v3.2.0 patterns

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
    """Validates ISO vectorstore compliance for pesquisa_agent"""

    def __init__(self, iso_path: str):
        self.iso_path = Path(iso_path)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.info: List[str] = []

    def validate_quick_start_size(self) -> bool:
        """CRITICAL: 01_QUICK_START.md < 8000 chars"""
        quick_start = self.iso_path / "01_QUICK_START.md"

        if not quick_start.exists():
            self.errors.append("[FAIL] 01_QUICK_START.md NOT FOUND")
            return False

        try:
            content = quick_start.read_text(encoding='utf-8')
            char_count = len(content)

            if char_count > 8000:
                self.errors.append(
                    f"[FAIL] QUICK_START too large: {char_count} chars (max 8000)"
                )
                return False
            elif char_count > 7950:
                self.warnings.append(
                    f"[WARN] QUICK_START near limit: {char_count}/8000 chars"
                )
            else:
                self.info.append(
                    f"[OK] QUICK_START size: {char_count}/8000 chars ({100 - char_count/80:.1f}% below limit)"
                )

            return True

        except Exception as e:
            self.errors.append(f"[FAIL] Error reading QUICK_START: {e}")
            return False

    def validate_manifest(self) -> bool:
        """Validates 00_MANIFEST.md exists and has correct structure"""
        manifest = self.iso_path / "00_MANIFEST.md"

        if not manifest.exists():
            self.errors.append("[FAIL] 00_MANIFEST.md NOT FOUND")
            return False

        try:
            content = manifest.read_text(encoding='utf-8')

            # Check for required sections
            required = [
                "pesquisa_agent",
                "iso_vectorstore",
                "v3.0.0"
            ]

            missing = [r for r in required if r.lower() not in content.lower()]

            if missing:
                self.warnings.append(f"[WARN] MANIFEST missing: {missing}")
            else:
                self.info.append("[OK] MANIFEST has all required markers")

            return True

        except Exception as e:
            self.errors.append(f"[FAIL] Error reading MANIFEST: {e}")
            return False

    def validate_schemas_exist(self) -> bool:
        """Validates existence and syntax of JSON schemas"""
        required_schemas = [
            "06_input_schema.json",
            "07_brief_schema.json",
            "08_execution_plan.json",
            "09_marketplaces.json",
            "10_research_config.json",
            "12_execution_plans.json",
        ]

        all_valid = True

        for schema in required_schemas:
            schema_path = self.iso_path / schema

            if not schema_path.exists():
                self.errors.append(f"[FAIL] Schema missing: {schema}")
                all_valid = False
                continue

            # Validate JSON syntax
            try:
                content = schema_path.read_text(encoding='utf-8')
                json.loads(content)
                self.info.append(f"[OK] {schema} valid JSON")
            except json.JSONDecodeError as e:
                self.errors.append(f"[FAIL] {schema} invalid JSON: {e}")
                all_valid = False
            except Exception as e:
                self.errors.append(f"[FAIL] Error reading {schema}: {e}")
                all_valid = False

        return all_valid

    def validate_hops_exist(self) -> bool:
        """Validates all 8 HOP files exist"""
        required_hops = [
            "13_HOP_main_agent.md",
            "14_HOP_intake_validation.md",
            "15_HOP_competitor_analysis.md",
            "16_HOP_gap_identification.md",
            "17_HOP_image_analysis.md",
            "18_HOP_price_comparison.md",
            "19_HOP_sentiment_analysis.md",
            "20_HOP_qa_validation.md",
        ]

        all_valid = True
        found_count = 0

        for hop in required_hops:
            hop_path = self.iso_path / hop

            if not hop_path.exists():
                self.errors.append(f"[FAIL] HOP missing: {hop}")
                all_valid = False
            else:
                found_count += 1
                # Check token size (should be < 1500 tokens ~ 6000 chars)
                try:
                    content = hop_path.read_text(encoding='utf-8')
                    if len(content) > 6000:
                        self.warnings.append(
                            f"[WARN] {hop} large: {len(content)} chars (target <6000)"
                        )
                except Exception:
                    pass

        self.info.append(f"[OK] Found {found_count}/{len(required_hops)} HOPs")
        return all_valid

    def validate_adw_orchestrator(self) -> bool:
        """Validates ADW orchestrator has proper structure"""
        adw_file = self.iso_path / "11_ADW_orchestrator.md"

        if not adw_file.exists():
            self.errors.append("[FAIL] 11_ADW_orchestrator.md NOT FOUND")
            return False

        try:
            content = adw_file.read_text(encoding='utf-8')

            # Check for required workflow markers
            markers = {
                "STEP": "Step definitions",
                "Input": "Input contract",
                "Output": "Output contract",
                "9": "9-step workflow"
            }

            found = {k: k in content for k in markers}
            missing = [k for k, v in found.items() if not v]

            if missing:
                self.warnings.append(
                    f"[WARN] ADW missing markers: {missing}"
                )
            else:
                self.info.append("[OK] ADW has all workflow markers")

            return True

        except Exception as e:
            self.errors.append(f"[FAIL] Error reading ADW: {e}")
            return False

    def validate_opop_compliance(self) -> bool:
        """Validates OPOP (One-Prompt-One-Purpose) heuristics"""
        files = list(self.iso_path.glob("*.md")) + list(self.iso_path.glob("*.json"))

        large_files = []

        for file in files:
            if file.suffix in ['.md', '.json']:
                try:
                    content = file.read_text(encoding='utf-8')
                    line_count = len(content.splitlines())
                    char_count = len(content)

                    # Heuristic: files >2000 lines or >15000 chars may violate OPOP
                    if line_count > 2000 or char_count > 15000:
                        large_files.append((file.name, line_count, char_count))
                except Exception:
                    continue

        if large_files:
            for name, lines, chars in large_files:
                self.warnings.append(
                    f"[WARN] {name} large ({lines} lines, {chars} chars) - possible OPOP violation"
                )
        else:
            self.info.append("[OK] OPOP compliance: all files within limits")

        return True

    def validate_example_exists(self) -> bool:
        """Validates existence of EXAMPLE_*.md file in user_research/"""
        parent = self.iso_path.parent
        user_research = parent / "user_research"

        examples = []
        if user_research.exists():
            examples = list(user_research.glob("EXEMPLO_*.md")) + list(user_research.glob("EXAMPLE_*.md"))

        if not examples:
            self.warnings.append(
                "[WARN] No EXEMPLO_*.md found in user_research/ (recommended)"
            )
            return False

        self.info.append(f"[OK] Example found: {examples[0].name}")
        return True

    def validate_system_instructions(self) -> bool:
        """Validates SYSTEM_INSTRUCTIONS_AGENT_BUILDER.md exists"""
        parent = self.iso_path.parent
        sys_instr = parent / "SYSTEM_INSTRUCTIONS_AGENT_BUILDER.md"

        if not sys_instr.exists():
            self.errors.append("[FAIL] SYSTEM_INSTRUCTIONS_AGENT_BUILDER.md NOT FOUND")
            return False

        try:
            content = sys_instr.read_text(encoding='utf-8')

            # Check version
            if "v3.0.0" in content or "v3." in content:
                self.info.append("[OK] SYSTEM_INSTRUCTIONS is v3.x")
            else:
                self.warnings.append("[WARN] SYSTEM_INSTRUCTIONS version may be outdated")

            # Check 22 blocks mentioned
            if "22" in content and "block" in content.lower():
                self.info.append("[OK] SYSTEM_INSTRUCTIONS mentions 22 blocks")
            else:
                self.warnings.append("[WARN] SYSTEM_INSTRUCTIONS should mention 22 blocks")

            return True

        except Exception as e:
            self.errors.append(f"[FAIL] Error reading SYSTEM_INSTRUCTIONS: {e}")
            return False

    def validate_file_numbering(self) -> bool:
        """Validates file numbering consistency (00-20)"""
        expected_prefixes = [
            "00_", "01_", "02_", "03_", "04_", "05_", "06_", "07_", "08_", "09_", "10_",
            "11_", "12_", "13_", "14_", "15_", "16_", "17_", "18_", "19_", "20_"
        ]

        files = sorted([f.name for f in self.iso_path.glob("*") if f.is_file()])
        numbered_files = [f for f in files if f[:3] in expected_prefixes]

        self.info.append(f"[OK] Found {len(numbered_files)} numbered files (target: 21)")

        # Check for gaps
        found_prefixes = set(f[:3] for f in numbered_files)
        missing = [p for p in expected_prefixes if p not in found_prefixes]

        if missing:
            self.warnings.append(f"[WARN] Missing file prefixes: {missing}")

        return len(numbered_files) >= 20

    def validate_core_docs(self) -> bool:
        """Validates core documentation files (01-05)"""
        core_files = [
            "01_QUICK_START.md",
            "02_PRIME.md",
            "03_INSTRUCTIONS.md",
            "04_README.md",
            "05_ARCHITECTURE.md",
        ]

        all_valid = True
        for filename in core_files:
            file_path = self.iso_path / filename
            if not file_path.exists():
                self.errors.append(f"[FAIL] Core file missing: {filename}")
                all_valid = False
            else:
                self.info.append(f"[OK] {filename} exists")

        return all_valid

    def run_all_validations(self) -> Tuple[int, int]:
        """
        Executes all validations
        Returns: (passed_count, total_count)
        """
        print("\n" + "="*60)
        print("ISO VECTORSTORE VALIDATION - pesquisa_agent v3.0.0")
        print("="*60 + "\n")

        validations = [
            ("MANIFEST Exists", self.validate_manifest),
            ("QUICK_START Size (<8000 chars)", self.validate_quick_start_size),
            ("Core Docs (01-05)", self.validate_core_docs),
            ("JSON Schemas", self.validate_schemas_exist),
            ("HOPs (13-20)", self.validate_hops_exist),
            ("ADW Orchestrator", self.validate_adw_orchestrator),
            ("OPOP Compliance", self.validate_opop_compliance),
            ("EXAMPLE Exists", self.validate_example_exists),
            ("SYSTEM_INSTRUCTIONS", self.validate_system_instructions),
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
                self.errors.append(f"[FAIL] {name} validation crashed: {e}")

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
        elif score >= 7.0:
            print("[STATUS] NEEDS IMPROVEMENTS")
        else:
            print("[STATUS] CRITICAL ISSUES - NOT READY")

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
        print(f"[FAIL] Error: Path does not exist: {iso_path}")
        sys.exit(1)

    if not os.path.isdir(iso_path):
        print(f"[FAIL] Error: Not a directory: {iso_path}")
        sys.exit(1)

    print(f"Validating: {iso_path}\n")

    validator = ISOValidator(iso_path)
    passed, total = validator.run_all_validations()

    # Exit code: 0 if production ready, 1 otherwise
    sys.exit(0 if passed >= (total * 0.9) else 1)


if __name__ == "__main__":
    main()
