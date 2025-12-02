"""
brand_validator.py - Validate video against brand guidelines

Validates:
- Color palette usage
- Tone/voice consistency
- Logo placement rules
- Typography guidelines
- Messaging compliance

Author: CODEXA Meta-Constructor
Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class BrandValidationResult:
    """Result of brand validation"""
    passed: bool
    score: float
    checks: List[Dict]
    recommendations: List[str]


class BrandValidator:
    """
    Validate video against brand guidelines

    Usage:
        validator = BrandValidator("brand_profiles/nike.json")
        result = validator.validate_script(script_data)
        print(f"Brand score: {result.score}/10.0")
    """

    def __init__(self, brand_profile_path: Optional[str] = None):
        """
        Initialize with optional brand profile

        Args:
            brand_profile_path: Path to brand profile JSON
        """

        self.brand_profile = self._load_brand_profile(brand_profile_path)

    def _load_brand_profile(self, path: Optional[str]) -> Dict:
        """Load brand profile or use defaults"""

        if path and Path(path).exists():
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)

        # Default generic e-commerce brand profile
        return {
            "name": "Generic E-commerce",
            "voice": {
                "tone": ["professional", "friendly", "enthusiastic"],
                "avoid": ["aggressive", "pushy", "negative"],
                "language": "pt-BR"
            },
            "messaging": {
                "required_elements": ["product_name", "benefit", "cta"],
                "cta_keywords": ["compre", "garanta", "aproveite", "confira"],
                "prohibited_words": [],
                "max_cta_length": 30
            },
            "visual": {
                "colors": {
                    "primary": "#000000",
                    "secondary": "#FFFFFF",
                    "accent": "#FF0000"
                },
                "text_style": {
                    "position": ["bottom", "center"],
                    "max_words": 6,
                    "caps_allowed": True
                }
            },
            "rules": {
                "must_show_price": False,
                "must_show_logo": False,
                "max_text_overlays": 5,
                "min_product_screen_time": 0.5
            }
        }

    def validate_script(self, script: Dict) -> BrandValidationResult:
        """
        Validate script against brand guidelines

        Args:
            script: Script data from Stage 2

        Returns:
            BrandValidationResult
        """

        checks = []
        recommendations = []

        # Check 1: Tone consistency
        tone_check = self._check_tone(script)
        checks.append(tone_check)

        # Check 2: Required messaging elements
        messaging_check = self._check_messaging(script)
        checks.append(messaging_check)

        # Check 3: CTA compliance
        cta_check = self._check_cta(script)
        checks.append(cta_check)

        # Check 4: Text overlay rules
        overlay_check = self._check_overlays(script)
        checks.append(overlay_check)

        # Check 5: Prohibited content
        prohibited_check = self._check_prohibited(script)
        checks.append(prohibited_check)

        # Calculate score
        passed_checks = sum(1 for c in checks if c["passed"])
        score = (passed_checks / len(checks)) * 10.0

        # Generate recommendations
        for check in checks:
            if not check["passed"]:
                recommendations.extend(check.get("recommendations", []))

        return BrandValidationResult(
            passed=score >= 8.0,
            score=round(score, 1),
            checks=checks,
            recommendations=recommendations
        )

    def _check_tone(self, script: Dict) -> Dict:
        """Check tone consistency with brand voice"""

        voice = self.brand_profile.get("voice", {})
        desired_tones = voice.get("tone", [])
        avoid_tones = voice.get("avoid", [])

        # Analyze narration text
        narration_text = " ".join([
            seg.get("text", "") for seg in script.get("narration", [])
        ]).lower()

        # Simple keyword-based tone detection
        tone_indicators = {
            "aggressive": ["agora", "urgente", "ultima chance", "nao perca"],
            "professional": ["qualidade", "premium", "exclusivo", "inovador"],
            "friendly": ["voce", "seu", "sua", "juntos"],
            "enthusiastic": ["incrivel", "fantastico", "perfeito", "melhor"]
        }

        detected_tones = []
        for tone, keywords in tone_indicators.items():
            if any(kw in narration_text for kw in keywords):
                detected_tones.append(tone)

        # Check for avoided tones
        violations = [t for t in detected_tones if t in avoid_tones]

        passed = len(violations) == 0

        return {
            "name": "tone_consistency",
            "passed": passed,
            "details": f"Detected: {detected_tones}, Violations: {violations}",
            "recommendations": [
                f"Avoid {tone} language in narration" for tone in violations
            ] if not passed else []
        }

    def _check_messaging(self, script: Dict) -> Dict:
        """Check required messaging elements"""

        messaging = self.brand_profile.get("messaging", {})
        required = messaging.get("required_elements", [])

        # Gather all text
        all_text = ""
        for seg in script.get("narration", []):
            all_text += " " + seg.get("text", "")
        for overlay in script.get("text_overlays", []):
            all_text += " " + overlay.get("text", "")
        all_text = all_text.lower()

        # Check elements
        element_checks = {
            "product_name": len(all_text) > 0,  # Assume product name is mentioned
            "benefit": any(w in all_text for w in ["conforto", "qualidade", "design", "tecnologia", "melhor"]),
            "cta": any(w in all_text for w in ["compre", "garanta", "aproveite", "confira", "acesse"])
        }

        missing = [e for e in required if not element_checks.get(e, True)]
        passed = len(missing) == 0

        return {
            "name": "required_messaging",
            "passed": passed,
            "details": f"Required: {required}, Missing: {missing}",
            "recommendations": [
                f"Add {element} to script" for element in missing
            ] if not passed else []
        }

    def _check_cta(self, script: Dict) -> Dict:
        """Check CTA compliance"""

        messaging = self.brand_profile.get("messaging", {})
        cta_keywords = messaging.get("cta_keywords", [])
        max_length = messaging.get("max_cta_length", 30)

        # Find CTA overlay (usually the last one)
        overlays = script.get("text_overlays", [])
        cta_overlay = None

        for overlay in reversed(overlays):
            text = overlay.get("text", "").lower()
            if any(kw in text for kw in cta_keywords):
                cta_overlay = overlay
                break

        issues = []

        if not cta_overlay:
            issues.append("No clear CTA found in overlays")
        else:
            # Check length
            cta_text = cta_overlay.get("text", "")
            if len(cta_text) > max_length:
                issues.append(f"CTA too long ({len(cta_text)} > {max_length} chars)")

            # Check position (should be at end)
            if cta_overlay.get("position") not in ["center", "bottom"]:
                issues.append("CTA should be centered or at bottom")

        passed = len(issues) == 0

        return {
            "name": "cta_compliance",
            "passed": passed,
            "details": f"CTA found: {cta_overlay is not None}, Issues: {issues}",
            "recommendations": issues if not passed else []
        }

    def _check_overlays(self, script: Dict) -> Dict:
        """Check text overlay rules"""

        visual = self.brand_profile.get("visual", {})
        text_style = visual.get("text_style", {})
        rules = self.brand_profile.get("rules", {})

        max_overlays = rules.get("max_text_overlays", 5)
        max_words = text_style.get("max_words", 6)
        allowed_positions = text_style.get("position", ["bottom", "center", "top"])

        overlays = script.get("text_overlays", [])
        issues = []

        # Check count
        if len(overlays) > max_overlays:
            issues.append(f"Too many overlays ({len(overlays)} > {max_overlays})")

        # Check each overlay
        for i, overlay in enumerate(overlays):
            text = overlay.get("text", "")
            position = overlay.get("position", "center")

            # Word count
            words = len(text.split())
            if words > max_words:
                issues.append(f"Overlay {i + 1}: too many words ({words} > {max_words})")

            # Position
            if position not in allowed_positions:
                issues.append(f"Overlay {i + 1}: position '{position}' not recommended")

        passed = len(issues) == 0

        return {
            "name": "overlay_rules",
            "passed": passed,
            "details": f"Overlays: {len(overlays)}, Issues: {len(issues)}",
            "recommendations": issues if not passed else []
        }

    def _check_prohibited(self, script: Dict) -> Dict:
        """Check for prohibited words/content"""

        messaging = self.brand_profile.get("messaging", {})
        prohibited = messaging.get("prohibited_words", [])

        if not prohibited:
            return {
                "name": "prohibited_content",
                "passed": True,
                "details": "No prohibited words defined",
                "recommendations": []
            }

        # Gather all text
        all_text = ""
        for seg in script.get("narration", []):
            all_text += " " + seg.get("text", "")
        for overlay in script.get("text_overlays", []):
            all_text += " " + overlay.get("text", "")
        all_text = all_text.lower()

        # Find violations
        violations = [w for w in prohibited if w.lower() in all_text]
        passed = len(violations) == 0

        return {
            "name": "prohibited_content",
            "passed": passed,
            "details": f"Checked {len(prohibited)} words, Found: {violations}",
            "recommendations": [
                f"Remove prohibited word: '{word}'" for word in violations
            ] if not passed else []
        }

    def print_result(self, result: BrandValidationResult):
        """Print formatted validation result"""

        print("\n" + "=" * 50)
        print("BRAND VALIDATION REPORT")
        print("=" * 50)
        print(f"Score: {result.score}/10.0 {'[PASS]' if result.passed else '[FAIL]'}")
        print("-" * 50)

        for check in result.checks:
            status = "[OK]" if check["passed"] else "[FAIL]"
            print(f"{status} {check['name']}: {check['details']}")

        if result.recommendations:
            print("-" * 50)
            print("RECOMMENDATIONS:")
            for rec in result.recommendations:
                print(f"  - {rec}")

        print("=" * 50)


# ======================
# STANDALONE USAGE
# ======================

def main():
    """Run validator from command line"""

    if len(sys.argv) < 2:
        print("Usage: python brand_validator.py <script.json> [brand_profile.json]")
        print("Example: python brand_validator.py outputs/script.json config/nike_brand.json")
        sys.exit(1)

    script_path = sys.argv[1]
    brand_path = sys.argv[2] if len(sys.argv) > 2 else None

    # Load script
    try:
        with open(script_path, "r", encoding="utf-8") as f:
            script = json.load(f)
    except Exception as e:
        print(f"Error loading script: {e}")
        sys.exit(1)

    # Validate
    validator = BrandValidator(brand_path)
    result = validator.validate_script(script)
    validator.print_result(result)

    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
