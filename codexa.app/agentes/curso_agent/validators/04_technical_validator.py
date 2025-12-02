#!/usr/bin/env python3
"""
04_technical_validator.py | Technical Validator

Purpose: Validate technical quality ([OPEN_VARIABLES], timing, examples)
Threshold: >=7.0/10.0

Usage:
    python validators/04_technical_validator.py --file outputs/video_scripts/script.md
"""

import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent))


class TechnicalValidator:
    """Validate technical quality"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.version = "2.0.0"
        self.threshold = 7.0

    def validate(self, file_path: Path) -> Dict:
        if not file_path.exists():
            return {"status": "error", "error": f"File not found", "score": 0.0}

        content = file_path.read_text(encoding="utf-8")

        results = {}
        results["open_variables"] = self._check_open_variables(content)
        results["timing_feasible"] = self._check_timing_feasible(content)
        results["examples_brazilian"] = self._check_examples_brazilian(content)
        results["technical_accuracy"] = self._check_technical_accuracy(content)

        score = self._calculate_score(results)

        return {
            "file": str(file_path),
            "validator": "04_technical_validator.py",
            "version": self.version,
            "validated_at": datetime.now().isoformat(),
            "score": score,
            "threshold": self.threshold,
            "passed": score >= self.threshold,
            "checks": results,
        }

    def _check_open_variables(self, content: str) -> Dict:
        variables = re.findall(r'\[([A-Z_]+)\]', content)
        variables = [v for v in variables if not re.match(r'\d{2}:\d{2}', v)]
        count = len(set(variables))
        passed = count >= 2
        return {"passed": passed, "message": f"Found {count} [OPEN_VARIABLES] (min 2)", "variables": list(set(variables))[:5]}

    def _check_timing_feasible(self, content: str) -> Dict:
        # Check if duration estimates are realistic (not too ambitious)
        durations = re.findall(r'(\d+)\s*h(?:ours?|oras?)', content, re.IGNORECASE)
        durations = [int(d) for d in durations]
        if durations:
            avg = sum(durations) / len(durations)
            passed = 5 <= avg <= 50  # Reasonable range
            return {"passed": passed, "message": f"Average duration: {avg:.1f}h (range: 5-50h)"}
        return {"passed": True, "message": "No duration estimates found"}

    def _check_examples_brazilian(self, content: str) -> Dict:
        brazilian = ["mercado livre", "shopee", "magalu", "anvisa", "inmetro", "brasil", "r$"]
        found = [kw for kw in brazilian if kw in content.lower()]
        passed = len(found) >= 2
        return {"passed": passed, "message": f"Found {len(found)} Brazilian keywords (min 2)", "keywords": found[:5]}

    def _check_technical_accuracy(self, content: str) -> Dict:
        # Check for CODEXA-specific terms
        codexa_terms = ["agent", "codexa", "meta-construção", "hop", "adw"]
        found = sum(1 for t in codexa_terms if t in content.lower())
        passed = found >= 3
        return {"passed": passed, "message": f"Found {found} CODEXA terms (min 3)"}

    def _calculate_score(self, results: Dict) -> float:
        weights = {"open_variables": 3.0, "timing_feasible": 2.0, "examples_brazilian": 2.5, "technical_accuracy": 2.5}
        total_weight = sum(weights.values())
        score = sum(weights[k] for k, v in results.items() if v["passed"])
        return round((score / total_weight) * 10.0, 2)


def main():
    parser = argparse.ArgumentParser(description="Validate technical quality")
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    validator = TechnicalValidator(verbose=args.verbose)
    report = validator.validate(Path(args.file))

    print(f"Score: {report['score']}/10.0 ({'PASSED' if report['passed'] else 'FAILED'})")
    exit(0 if report['passed'] else 1)


if __name__ == "__main__":
    main()
