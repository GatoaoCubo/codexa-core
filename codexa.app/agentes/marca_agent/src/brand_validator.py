#!/usr/bin/env python3
"""
Brand Strategy Validator
Version: 1.1
Date: 2025-11-09

Validates brand_strategy.md outputs from Brand Agent.
Checks:
- Tagline length (40-60 chars strict)
- Required fields presence
- Brand archetype validity
- Tone of voice dimensions (1-5 scale)
- Compliance keywords (ANVISA/CONAR)
- Content word count (target 5,000-8,000 words)
- Improved error handling and reporting
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Result of validation check."""
    is_valid: bool
    score: float  # 0.0 to 1.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)


class BrandValidator:
    """Validates brand strategy outputs."""

    # Valid brand archetypes (12 total)
    VALID_ARCHETYPES = {
        "hero", "sage", "innocent", "explorer", "creator", "ruler",
        "magician", "lover", "caregiver", "jester", "everyman", "rebel"
    }

    # Compliance red flags (Brazilian regulations)
    COMPLIANCE_RED_FLAGS = [
        (r"\bcura\b", "Claims cure without evidence (ANVISA violation)"),
        (r"\btrata(?:mento)?\b", "Medical treatment claims without evidence (ANVISA violation)"),
        (r"\belimica\b", "Elimination claims without scientific proof"),
        (r"\bemagrece\b", "Weight loss claims without evidence (ANVISA violation)"),
        (r"\b#1\b", "Superlative claim #1 without verified source (CONAR violation)"),
        (r"\bmelhor do brasil\b", "Best in Brazil claim without proof (CONAR violation)"),
        (r"\baprovado por m[ée]dicos\b", "Doctor approval claim without evidence"),
        (r"\b(?:100%|cem por cento)\s+(?:natural|org[aâ]nico)\b", "100% natural/organic claim requires certification"),
        (r"\bgarante\b", "Guarantee claims may require legal backing"),
        (r"\bresultados?\s+(?:imediatos?|instant[aâ]neos?)\b", "Immediate results claims without evidence"),
    ]

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize validator."""
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict:
        """Load validation configuration."""
        if self.config_path and self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError as e:
                print(f"Warning: Failed to parse config file {self.config_path}: {e}")
                return {}
            except Exception as e:
                print(f"Warning: Failed to load config file {self.config_path}: {e}")
                return {}
        return {}

    def validate_file(self, file_path: Path) -> ValidationResult:
        """Validate a brand_strategy.md file."""
        if not file_path.exists():
            return ValidationResult(
                is_valid=False,
                score=0.0,
                errors=[f"File not found: {file_path}"]
            )

        try:
            content = file_path.read_text(encoding='utf-8')
            return self.validate_content(content)
        except UnicodeDecodeError:
            return ValidationResult(
                is_valid=False,
                score=0.0,
                errors=[f"File encoding error: {file_path}. Expected UTF-8."]
            )
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                score=0.0,
                errors=[f"Error reading file {file_path}: {str(e)}"]
            )

    def validate_content(self, content: str) -> ValidationResult:
        """Validate brand strategy content."""
        errors = []
        warnings = []
        details = {}

        # Run all validation checks
        tagline_valid, tagline_errors, tagline_warnings = self._check_taglines(content)
        if not tagline_valid:
            errors.extend(tagline_errors)
        warnings.extend(tagline_warnings)

        required_valid, required_errors = self._check_required_fields(content)
        if not required_valid:
            errors.extend(required_errors)

        archetype_valid, archetype_errors, archetype_found = self._check_archetype(content)
        if not archetype_valid:
            errors.extend(archetype_errors)
        details['archetype'] = archetype_found

        tone_valid, tone_errors, tone_values = self._check_tone_of_voice(content)
        if not tone_valid:
            errors.extend(tone_errors)
        details['tone_dimensions'] = tone_values

        compliance_valid, compliance_warnings = self._check_compliance(content)
        warnings.extend(compliance_warnings)

        # New checks
        word_count = len(content.split())
        details['word_count'] = word_count
        if word_count < 3000:
            warnings.append(f"Content is short ({word_count} words). Target: 5,000-8,000 words for complete strategy.")
        elif word_count > 10000:
            warnings.append(f"Content is very long ({word_count} words). Consider reducing to 5,000-8,000 words.")

        # Calculate score
        checks_passed = sum([
            tagline_valid,
            required_valid,
            archetype_valid,
            tone_valid,
            compliance_valid
        ])
        total_checks = 5
        score = checks_passed / total_checks

        # Penalty for warnings (max 20% reduction)
        if warnings:
            penalty = min(len(warnings) * 0.05, 0.20)
            score -= penalty
            score = max(0.0, score)

        is_valid = len(errors) == 0 and score >= 0.75

        return ValidationResult(
            is_valid=is_valid,
            score=score,
            errors=errors,
            warnings=warnings,
            details=details
        )

    def _check_taglines(self, content: str) -> Tuple[bool, List[str], List[str]]:
        """Check tagline length (40-60 characters strict)."""
        errors = []
        warnings = []

        # Extract taglines section
        tagline_pattern = r"(?:Tagline|tagline)[^\n]*:\s*(.+?)(?:\n|$)"
        taglines = re.findall(tagline_pattern, content, re.IGNORECASE | re.MULTILINE)

        if not taglines:
            errors.append("No taglines found in content")
            return False, errors, warnings

        for i, tagline in enumerate(taglines, 1):
            # Clean tagline (remove markdown, quotes, etc.)
            clean_tagline = re.sub(r'[*_"`]', '', tagline).strip()
            length = len(clean_tagline)

            if length < 40:
                errors.append(f"Tagline {i} too short: {length} chars (min 40). Content: '{clean_tagline}'")
            elif length > 60:
                errors.append(f"Tagline {i} too long: {length} chars (max 60). Content: '{clean_tagline}'")
            elif length < 45 or length > 55:
                warnings.append(f"Tagline {i} length {length} chars is acceptable but not ideal (45-55 preferred)")

        is_valid = len(errors) == 0
        return is_valid, errors, warnings

    def _check_required_fields(self, content: str) -> Tuple[bool, List[str]]:
        """Check presence of required fields."""
        errors = []

        required_sections = [
            r"brand\s+name",
            r"tagline",
            r"archetype",
            r"(?:unique\s+value\s+proposition|uvp)",
            r"target\s+(?:segment|audience)",
            r"tone\s+of\s+voice",
            r"color\s+palette",
            r"mission",
            r"vision",
        ]

        for section in required_sections:
            if not re.search(section, content, re.IGNORECASE):
                errors.append(f"Required section missing: {section.replace(r'\\s+', ' ')}")

        is_valid = len(errors) == 0
        return is_valid, errors

    def _check_archetype(self, content: str) -> Tuple[bool, List[str], Optional[str]]:
        """Check brand archetype validity."""
        errors = []
        archetype_found = None

        # Extract archetype
        archetype_pattern = r"(?:archetype|arquétipo)[^\n]*:\s*([a-zA-Z]+)"
        match = re.search(archetype_pattern, content, re.IGNORECASE)

        if not match:
            errors.append("Brand archetype not found")
            return False, errors, None

        archetype_found = match.group(1).lower().strip()

        if archetype_found not in self.VALID_ARCHETYPES:
            errors.append(
                f"Invalid archetype '{archetype_found}'. "
                f"Must be one of: {', '.join(sorted(self.VALID_ARCHETYPES))}"
            )
            return False, errors, archetype_found

        return True, errors, archetype_found

    def _check_tone_of_voice(self, content: str) -> Tuple[bool, List[str], Dict[str, int]]:
        """Check tone of voice dimensions (1-5 scale)."""
        errors = []
        tone_values = {}

        # Expected 4 dimensions (Nielsen Norman Group)
        dimensions = [
            "funny.*serious",
            "formal.*casual",
            "respectful.*irreverent",
            "enthusiastic.*matter.*fact"
        ]

        for dimension in dimensions:
            # Look for dimension with value 1-5
            pattern = rf"{dimension}[^\d]*(\d)"
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)

            if match:
                value = int(match.group(1))
                if 1 <= value <= 5:
                    tone_values[dimension.split('.*')[0]] = value
                else:
                    errors.append(f"Tone dimension '{dimension}' has invalid value {value} (must be 1-5)")
            else:
                errors.append(f"Tone dimension '{dimension}' not found")

        # Should have 4 dimensions
        if len(tone_values) < 4:
            errors.append(f"Missing tone dimensions. Found {len(tone_values)}, expected 4")

        is_valid = len(errors) == 0
        return is_valid, errors, tone_values

    def _check_compliance(self, content: str) -> Tuple[bool, List[str]]:
        """Check for compliance red flags (Brazilian regulations)."""
        warnings = []

        for pattern, description in self.COMPLIANCE_RED_FLAGS:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                warnings.append(
                    f"⚠️  COMPLIANCE: Found '{matches[0]}' - {description}"
                )

        # Always valid (warnings don't fail validation)
        return True, warnings


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Validate brand strategy outputs")
    parser.add_argument("file", type=Path, help="Path to brand_strategy.md file")
    parser.add_argument("--config", type=Path, help="Path to validation config JSON")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    validator = BrandValidator(config_path=args.config)
    result = validator.validate_file(args.file)

    if args.json:
        # JSON output
        import json
        output = {
            "is_valid": result.is_valid,
            "score": result.score,
            "errors": result.errors,
            "warnings": result.warnings,
            "details": result.details
        }
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        # Human-readable output
        print("=" * 60)
        print("BRAND STRATEGY VALIDATION REPORT")
        print("=" * 60)
        print()
        print(f"File: {args.file}")
        print(f"Status: {'✅ VALID' if result.is_valid else '❌ INVALID'}")
        print(f"Score: {result.score:.2%}")
        print()

        if result.errors:
            print("ERRORS:")
            for error in result.errors:
                print(f"  ❌ {error}")
            print()

        if result.warnings:
            print("WARNINGS:")
            for warning in result.warnings:
                print(f"  ⚠️  {warning}")
            print()

        if result.details:
            print("DETAILS:")
            for key, value in result.details.items():
                print(f"  {key}: {value}")
            print()

        print("=" * 60)

        # Exit code
        exit(0 if result.is_valid else 1)


if __name__ == "__main__":
    main()
