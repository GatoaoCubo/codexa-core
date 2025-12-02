#!/usr/bin/env python3
"""
02_brand_voice_validator.py | Brand Voice Validator

Purpose: Validate brand voice compliance (seed words, tone, no hype)
Threshold: >=7.0/10.0

Usage:
    python validators/02_brand_voice_validator.py --file outputs/video_scripts/script.md
"""

import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent))


class BrandVoiceValidator:
    """Validate brand voice compliance"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.version = "2.0.0"
        self.threshold = 7.0

        self.seed_words = ["meta-construção", "destilação", "cérebro plugável", "codexa"]
        self.hype_words = ["revolucionário", "mágico", "único no mercado", "incrível", "extraordinário"]
        self.attack_targets = ["banalização", "lock-in", "commodity"]

    def validate(self, file_path: Path) -> Dict:
        if not file_path.exists():
            return {"status": "error", "error": f"File not found: {file_path}", "score": 0.0}

        content = file_path.read_text(encoding="utf-8").lower()

        results = {}
        results["seed_words"] = self._check_seed_words(content)
        results["no_hype_words"] = self._check_no_hype_words(content)
        results["attack_present"] = self._check_attack_present(content)
        results["tone_formal"] = self._check_tone_formal(content)

        score = self._calculate_score(results)

        return {
            "file": str(file_path),
            "validator": "02_brand_voice_validator.py",
            "version": self.version,
            "validated_at": datetime.now().isoformat(),
            "score": score,
            "threshold": self.threshold,
            "passed": score >= self.threshold,
            "checks": results,
            "issues": [k for k, v in results.items() if not v["passed"]],
        }

    def _check_seed_words(self, content: str) -> Dict:
        found = [w for w in self.seed_words if w in content]
        passed = len(found) >= 3
        return {"passed": passed, "message": f"Found {len(found)} seed words (min 3)", "found": found}

    def _check_no_hype_words(self, content: str) -> Dict:
        found = [w for w in self.hype_words if w in content]
        passed = len(found) == 0
        return {"passed": passed, "message": f"Found {len(found)} hype words (should be 0)", "found": found}

    def _check_attack_present(self, content: str) -> Dict:
        found = [t for t in self.attack_targets if t in content]
        passed = len(found) >= 1
        return {"passed": passed, "message": f"Attacks {len(found)} targets (min 1)", "targets": found}

    def _check_tone_formal(self, content: str) -> Dict:
        # Simple heuristic: check for technical terms
        technical_terms = ["agent", "sistema", "arquitetura", "meta", "workflow"]
        found = sum(1 for t in technical_terms if t in content)
        passed = found >= 3
        return {"passed": passed, "message": f"Found {found} technical terms (min 3)"}

    def _calculate_score(self, results: Dict) -> float:
        weights = {"seed_words": 3.0, "no_hype_words": 2.0, "attack_present": 2.0, "tone_formal": 3.0}
        total_weight = sum(weights.values())
        score = sum(weights[k] for k, v in results.items() if v["passed"])
        return round((score / total_weight) * 10.0, 2)


def main():
    parser = argparse.ArgumentParser(description="Validate brand voice")
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    validator = BrandVoiceValidator(verbose=args.verbose)
    report = validator.validate(Path(args.file))

    print(f"Score: {report['score']}/10.0 ({'PASSED' if report['passed'] else 'FAILED'})")
    exit(0 if report['passed'] else 1)


if __name__ == "__main__":
    main()
