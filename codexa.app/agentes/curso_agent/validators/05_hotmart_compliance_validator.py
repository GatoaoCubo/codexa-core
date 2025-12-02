#!/usr/bin/env python3
"""
05_hotmart_compliance_validator.py | Hotmart Compliance Validator

Purpose: Validate Hotmart compliance (DRM, LGPD, claims, specs)
Threshold: >=8.0/10.0 (stricter due to legal requirements)

Usage:
    python validators/05_hotmart_compliance_validator.py --file outputs/hotmart_package/MANIFEST.json
"""

import sys
import json
import argparse
import re
from pathlib import Path
from datetime import datetime
from typing import Dict

sys.path.insert(0, str(Path(__file__).parent.parent))


class HotmartComplianceValidator:
    """Validate Hotmart platform compliance"""

    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.version = "2.0.0"
        self.threshold = 8.0  # Stricter threshold

        self.prohibited_claims = ["garantido", "certeza", "100%", "sempre", "nunca falha"]

    def validate(self, file_path: Path) -> Dict:
        if not file_path.exists():
            return {"status": "error", "error": f"File not found", "score": 0.0}

        # Handle both JSON manifests and markdown content
        if file_path.suffix == '.json':
            with open(file_path, encoding='utf-8') as f:
                data = json.load(f)
            content = json.dumps(data, ensure_ascii=False)
        else:
            content = file_path.read_text(encoding="utf-8")

        results = {}
        results["drm_mentioned"] = self._check_drm_mentioned(content)
        results["lgpd_compliant"] = self._check_lgpd_compliant(content)
        results["no_prohibited_claims"] = self._check_no_prohibited_claims(content)
        results["garantia_present"] = self._check_garantia_present(content)
        results["video_specs_correct"] = self._check_video_specs(content)

        score = self._calculate_score(results)

        return {
            "file": str(file_path),
            "validator": "05_hotmart_compliance_validator.py",
            "version": self.version,
            "validated_at": datetime.now().isoformat(),
            "score": score,
            "threshold": self.threshold,
            "passed": score >= self.threshold,
            "checks": results,
        }

    def _check_drm_mentioned(self, content: str) -> Dict:
        has_drm = bool(re.search(r'drm|anti-download|watermark|proteção', content, re.IGNORECASE))
        return {"passed": has_drm, "message": "DRM protection mentioned" if has_drm else "DRM not mentioned"}

    def _check_lgpd_compliant(self, content: str) -> Dict:
        has_lgpd = bool(re.search(r'lgpd|privacidade|opt-out|consentimento', content, re.IGNORECASE))
        return {"passed": has_lgpd, "message": "LGPD compliance mentioned" if has_lgpd else "LGPD not mentioned"}

    def _check_no_prohibited_claims(self, content: str) -> Dict:
        found = [c for c in self.prohibited_claims if c in content.lower()]
        passed = len(found) == 0
        return {"passed": passed, "message": f"Found {len(found)} prohibited claims (should be 0)", "claims": found}

    def _check_garantia_present(self, content: str) -> Dict:
        has_garantia = bool(re.search(r'garantia|refund|reembolso|7.*30.*dia', content, re.IGNORECASE))
        return {"passed": has_garantia, "message": "Garantia terms present" if has_garantia else "No garantia terms"}

    def _check_video_specs(self, content: str) -> Dict:
        # Check for video spec mentions (MP4, H.264, 1080p, etc.)
        has_specs = bool(re.search(r'mp4|h\.?264|1080p|720p|codec', content, re.IGNORECASE))
        return {"passed": has_specs, "message": "Video specs mentioned" if has_specs else "No video specs"}

    def _calculate_score(self, results: Dict) -> float:
        weights = {"drm_mentioned": 2.0, "lgpd_compliant": 2.5, "no_prohibited_claims": 2.5, "garantia_present": 1.5, "video_specs_correct": 1.5}
        total_weight = sum(weights.values())
        score = sum(weights[k] for k, v in results.items() if v["passed"])
        return round((score / total_weight) * 10.0, 2)


def main():
    parser = argparse.ArgumentParser(description="Validate Hotmart compliance")
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    validator = HotmartComplianceValidator(verbose=args.verbose)
    report = validator.validate(Path(args.file))

    print(f"Score: {report['score']}/10.0 (Threshold: {validator.threshold}) - {'PASSED' if report['passed'] else 'FAILED'}")
    exit(0 if report['passed'] else 1)


if __name__ == "__main__":
    main()
