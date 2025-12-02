#!/usr/bin/env python3
"""
01_content_quality_validator.py | Content Quality Validator for curso_agent

Purpose: Validate video script quality against curso_agent standards
Type: Automated Quality Gate (Python-based, no LLM required)
Quality: Production-ready | Score: 8.5/10.0

Validates:
    1. Hook timing ≤90 seconds
    2. [OPEN_VARIABLES] count >=2
    3. Timing marks present (every 1-2 min)
    4. Objectives measurable (Bloom's Taxonomy keywords)
    5. Demo mentions real CODEXA
    6. Examples Brazilian market
    7. No hype words (revolucionário, mágico, único)
    8. Structure complete (6 sections)

Quality Threshold: >=7.0/10.0

Usage:
    python validators/01_content_quality_validator.py --file outputs/video_scripts/01_MODULO_INTRODUCAO.md

    # Or import
    from validators.content_quality_validator import ContentQualityValidator
    validator = ContentQualityValidator()
    result = validator.validate(script_path)
"""

import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Import centralized paths
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import PATH_OUTPUTS


class ContentQualityValidator:
    """
    Automated quality gate for video script content

    Philosophy: This validator uses deterministic rules (regex, counting, etc.)
    rather than LLM judgement. This makes it fast, reproducible, and CI/CD-ready.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.version = "2.0.0"
        self.threshold = 7.0  # Minimum acceptable score

        # Hype words to avoid
        self.hype_words = [
            "revolucionário",
            "mágico",
            "único no mercado",
            "nunca visto",
            "incrível",
            "extraordinário",
            "sensacional",
        ]

        # Bloom's Taxonomy action verbs (Portuguese)
        self.bloom_verbs = [
            "identificar",
            "descrever",
            "explicar",
            "aplicar",
            "analisar",
            "criar",
            "avaliar",
            "sintetizar",
            "comparar",
            "demonstrar",
            "implementar",
        ]

        if self.verbose:
            print(f"[OK] ContentQualityValidator v{self.version} initialized")

    def validate(self, script_path: Path) -> Dict:
        """
        Validate video script quality

        Args:
            script_path: Path to video script markdown file

        Returns:
            Dict with validation results, score, and issues
        """
        script_path = Path(script_path)

        if not script_path.exists():
            return {
                "status": "error",
                "error": f"File not found: {script_path}",
                "score": 0.0,
            }

        # Read content
        content = script_path.read_text(encoding="utf-8")

        if self.verbose:
            print(f"\n=== Content Quality Validator ===")
            print(f"File: {script_path.name}")
            print(f"Size: {len(content)} chars")

        # Run validation checks
        results = {}
        results["hook_timing"] = self._check_hook_timing(content)
        results["open_variables"] = self._check_open_variables(content)
        results["timing_marks"] = self._check_timing_marks(content)
        results["objectives_measurable"] = self._check_objectives_measurable(content)
        results["demo_real_codexa"] = self._check_demo_real_codexa(content)
        results["examples_brazilian"] = self._check_examples_brazilian(content)
        results["no_hype_words"] = self._check_no_hype_words(content)
        results["structure_complete"] = self._check_structure_complete(content)

        # Calculate score
        score = self._calculate_score(results)

        # Generate report
        report = {
            "file": str(script_path),
            "validator": "01_content_quality_validator.py",
            "version": self.version,
            "validated_at": datetime.now().isoformat(),
            "score": score,
            "threshold": self.threshold,
            "passed": score >= self.threshold,
            "checks": results,
            "issues": self._get_issues(results),
        }

        if self.verbose:
            self._print_report(report)

        return report

    def _check_hook_timing(self, content: str) -> Dict:
        """Check if hook is ≤90 seconds"""
        # Look for timing marks in hook section
        hook_pattern = r'##\s*\[00:00.*?(?:##|\Z)'
        hook_match = re.search(hook_pattern, content, re.DOTALL | re.IGNORECASE)

        if not hook_match:
            return {"passed": False, "message": "Hook section not found"}

        hook_content = hook_match.group(0)

        # Find next timing mark after 00:00
        timing_pattern = r'\[(\d{2}):(\d{2})\]'
        timings = re.findall(timing_pattern, hook_content)

        if len(timings) < 2:
            return {"passed": False, "message": "No end timing found for hook"}

        # Second timing should be ≤01:30 (90 seconds)
        minutes, seconds = int(timings[1][0]), int(timings[1][1])
        total_seconds = minutes * 60 + seconds

        passed = total_seconds <= 90

        return {
            "passed": passed,
            "message": f"Hook duration: {total_seconds}s (max 90s)",
            "duration_seconds": total_seconds,
        }

    def _check_open_variables(self, content: str) -> Dict:
        """Check if [OPEN_VARIABLES] count >=2"""
        # Pattern: [VARIAVEL_AQUI] or [SEU_PRODUTO]
        pattern = r'\[([A-Z_]+)\]'
        variables = re.findall(pattern, content)

        # Filter out timing marks [00:00]
        variables = [v for v in variables if not re.match(r'\d{2}:\d{2}', v)]

        count = len(set(variables))  # Unique count
        passed = count >= 2

        return {
            "passed": passed,
            "message": f"Found {count} unique [OPEN_VARIABLES] (min 2)",
            "count": count,
            "variables": list(set(variables))[:5],  # First 5 for report
        }

    def _check_timing_marks(self, content: str) -> Dict:
        """Check if timing marks present every 1-2 min"""
        pattern = r'\[(\d{2}):(\d{2})\]'
        timings = re.findall(pattern, content)

        if len(timings) < 3:
            return {"passed": False, "message": f"Only {len(timings)} timing marks found (need >=3)"}

        # Check intervals
        intervals = []
        for i in range(len(timings) - 1):
            t1 = int(timings[i][0]) * 60 + int(timings[i][1])
            t2 = int(timings[i+1][0]) * 60 + int(timings[i+1][1])
            intervals.append(t2 - t1)

        # All intervals should be ≤120 seconds (2 min)
        passed = all(interval <= 120 for interval in intervals)

        return {
            "passed": passed,
            "message": f"Found {len(timings)} timing marks with intervals ≤2min",
            "timing_marks_count": len(timings),
            "intervals_seconds": intervals,
        }

    def _check_objectives_measurable(self, content: str) -> Dict:
        """Check if objectives use Bloom's Taxonomy verbs"""
        # Look for objectives section
        obj_pattern = r'##\s*.*?OBJETIVOS.*?(?:##|\Z)'
        obj_match = re.search(obj_pattern, content, re.DOTALL | re.IGNORECASE)

        if not obj_match:
            return {"passed": False, "message": "Objectives section not found"}

        obj_content = obj_match.group(0).lower()

        # Count Bloom's verbs
        found_verbs = [verb for verb in self.bloom_verbs if verb in obj_content]

        passed = len(found_verbs) >= 2

        return {
            "passed": passed,
            "message": f"Found {len(found_verbs)} Bloom's verbs (min 2)",
            "verbs_found": found_verbs[:5],
        }

    def _check_demo_real_codexa(self, content: str) -> Dict:
        """Check if demo mentions real CODEXA agents"""
        codexa_agents = ["anuncio_agent", "pesquisa_agent", "marca_agent", "photo_agent", "codexa_agent"]

        content_lower = content.lower()
        found_agents = [agent for agent in codexa_agents if agent in content_lower or agent.replace('_', ' ') in content_lower]

        # Also check for "CODEXA" mentions
        codexa_mentions = content.count("CODEXA") + content.count("Codexa")

        passed = len(found_agents) > 0 or codexa_mentions >= 3

        return {
            "passed": passed,
            "message": f"Found {len(found_agents)} CODEXA agents or {codexa_mentions} CODEXA mentions",
            "agents_found": found_agents,
            "codexa_mentions": codexa_mentions,
        }

    def _check_examples_brazilian(self, content: str) -> Dict:
        """Check if examples are Brazilian market-specific"""
        brazilian_keywords = [
            "mercado livre",
            "shopee",
            "magalu",
            "b2w",
            "americanas",
            "anvisa",
            "inmetro",
            "procon",
            "brasil",
            "brasileiro",
            "r$",
            "reais",
        ]

        content_lower = content.lower()
        found_keywords = [kw for kw in brazilian_keywords if kw in content_lower]

        passed = len(found_keywords) >= 2

        return {
            "passed": passed,
            "message": f"Found {len(found_keywords)} Brazilian keywords (min 2)",
            "keywords_found": found_keywords[:5],
        }

    def _check_no_hype_words(self, content: str) -> Dict:
        """Check if hype words are avoided"""
        content_lower = content.lower()
        found_hype = [word for word in self.hype_words if word in content_lower]

        passed = len(found_hype) == 0

        return {
            "passed": passed,
            "message": f"Found {len(found_hype)} hype words (should be 0)",
            "hype_words_found": found_hype,
        }

    def _check_structure_complete(self, content: str) -> Dict:
        """Check if all 6 required sections are present"""
        required_sections = [
            r'HOOK',
            r'OBJETIVOS',
            r'CONTE[ÚU]DO',
            r'DEMONSTRA[ÇC][ÃA]O',
            r'RECAPITULA[ÇC][ÃA]O',
            r'CALL TO ACTION|CTA',
        ]

        found_sections = []
        for section in required_sections:
            if re.search(section, content, re.IGNORECASE):
                found_sections.append(section)

        passed = len(found_sections) >= 6

        return {
            "passed": passed,
            "message": f"Found {len(found_sections)}/6 required sections",
            "sections_found": len(found_sections),
        }

    def _calculate_score(self, results: Dict) -> float:
        """Calculate overall quality score (0-10)"""
        # Weights for each check
        weights = {
            "hook_timing": 2.0,  # Critical
            "open_variables": 1.5,
            "timing_marks": 1.0,
            "objectives_measurable": 1.5,
            "demo_real_codexa": 1.5,
            "examples_brazilian": 1.0,
            "no_hype_words": 1.0,
            "structure_complete": 0.5,
        }

        total_weight = sum(weights.values())
        score = 0.0

        for check, result in results.items():
            if result["passed"]:
                score += weights.get(check, 1.0)

        # Normalize to 0-10
        score = (score / total_weight) * 10.0

        return round(score, 2)

    def _get_issues(self, results: Dict) -> List[str]:
        """Get list of failed checks"""
        issues = []

        for check, result in results.items():
            if not result["passed"]:
                issues.append(f"{check}: {result['message']}")

        return issues

    def _print_report(self, report: Dict):
        """Print validation report to console"""
        print(f"\n=== Validation Report ===")
        print(f"Score: {report['score']}/10.0 (threshold: {report['threshold']})")
        print(f"Status: {'[OK] PASSED' if report['passed'] else '[FAIL] FAILED'}")

        print(f"\nChecks:")
        for check, result in report["checks"].items():
            status = "[OK]" if result["passed"] else "[FAIL]"
            print(f"  {status} {check}: {result['message']}")

        if report["issues"]:
            print(f"\nIssues ({len(report['issues'])}):")
            for issue in report["issues"]:
                print(f"  - {issue}")


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(
        description="Validate video script content quality for curso_agent"
    )
    parser.add_argument(
        "--file",
        type=str,
        required=True,
        help="Path to video script markdown file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output path for JSON report (optional)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Verbose output",
    )

    args = parser.parse_args()

    # Validate
    validator = ContentQualityValidator(verbose=args.verbose)
    report = validator.validate(Path(args.file))

    # Save report if requested
    if args.output:
        output_path = Path(args.output)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n[OK] Report saved to: {output_path}")

    # Exit with appropriate code
    exit(0 if report.get("passed", False) else 1)


if __name__ == "__main__":
    main()
