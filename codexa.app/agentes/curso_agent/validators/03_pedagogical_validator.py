#!/usr/bin/env python3
"""
03_pedagogical_validator.py | Pedagogical Validator

Purpose: Validate pedagogical quality (complexity, prerequisites, outcomes)
Threshold: >=7.0/10.0

Usage:
    python validators/03_pedagogical_validator.py --file outputs/workbooks/workbook.md
"""

import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent))


class PedagogicalValidator:
    """Validate pedagogical quality"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.version = "2.0.0"
        self.threshold = 7.0

    def validate(self, file_path: Path) -> Dict:
        if not file_path.exists():
            return {"status": "error", "error": f"File not found", "score": 0.0}

        content = file_path.read_text(encoding="utf-8")

        results = {}
        results["progressive_complexity"] = self._check_progressive_complexity(content)
        results["prerequisites_clear"] = self._check_prerequisites_clear(content)
        results["outcomes_actionable"] = self._check_outcomes_actionable(content)
        results["exercises_present"] = self._check_exercises_present(content)

        score = self._calculate_score(results)

        return {
            "file": str(file_path),
            "validator": "03_pedagogical_validator.py",
            "version": self.version,
            "validated_at": datetime.now().isoformat(),
            "score": score,
            "threshold": self.threshold,
            "passed": score >= self.threshold,
            "checks": results,
        }

    def _check_progressive_complexity(self, content: str) -> Dict:
        # Look for Layer 1, Layer 2, Layer 3 mentions or progression patterns
        layers = re.findall(r'layer\s*[123]|camada\s*[123]', content, re.IGNORECASE)
        passed = len(set(layers)) >= 2
        return {"passed": passed, "message": f"Found {len(set(layers))} complexity layers (min 2)"}

    def _check_prerequisites_clear(self, content: str) -> Dict:
        # Look for prerequisites section or mentions
        has_prereq = bool(re.search(r'pré-requisito|prerequisite|antes de|você precisa', content, re.IGNORECASE))
        return {"passed": has_prereq, "message": "Prerequisites section present" if has_prereq else "No prerequisites found"}

    def _check_outcomes_actionable(self, content: str) -> Dict:
        # Look for action verbs in objectives
        action_verbs = ["criar", "implementar", "aplicar", "analisar", "demonstrar", "identificar"]
        found = sum(1 for v in action_verbs if v in content.lower())
        passed = found >= 2
        return {"passed": passed, "message": f"Found {found} action verbs (min 2)"}

    def _check_exercises_present(self, content: str) -> Dict:
        # Look for exercise sections
        exercises = re.findall(r'exerc[íi]cio|prática|atividade|hands-on', content, re.IGNORECASE)
        passed = len(exercises) >= 2
        return {"passed": passed, "message": f"Found {len(exercises)} exercise mentions (min 2)"}

    def _calculate_score(self, results: Dict) -> float:
        weights = {"progressive_complexity": 2.5, "prerequisites_clear": 2.5, "outcomes_actionable": 2.5, "exercises_present": 2.5}
        total_weight = sum(weights.values())
        score = sum(weights[k] for k, v in results.items() if v["passed"])
        return round((score / total_weight) * 10.0, 2)


def main():
    parser = argparse.ArgumentParser(description="Validate pedagogical quality")
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    validator = PedagogicalValidator(verbose=args.verbose)
    report = validator.validate(Path(args.file))

    print(f"Score: {report['score']}/10.0 ({'PASSED' if report['passed'] else 'FAILED'})")
    exit(0 if report['passed'] else 1)


if __name__ == "__main__":
    main()
