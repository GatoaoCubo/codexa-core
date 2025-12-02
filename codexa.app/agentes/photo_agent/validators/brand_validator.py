#!/usr/bin/env python3
"""
Brand Validator - 11-Point Brand Alignment Checklist

Purpose: Validate brand social media output against brand consistency rules
Target: Instagram, TikTok, Pinterest, Facebook

Checklist (11 points):
  1. All prompts 120-500 characters
  2. All prompts specify camera settings
  3. All prompts describe lighting
  4. All prompts mention background
  5. All prompts define composition
  6. All aspect ratios valid (1:1, 4:5, 9:16, etc.)
  7. All brand colors applied from palette
  8. All PNL triggers aligned with brand archetype
  9. All prompts state "8K quality"
  10. All prompts include "no watermarks"
  11. Platform optimization complete (aspect ratio + platform tags)

Version: 1.0.0
Author: CODEXA Meta-Construction System
"""

import json
import sys
from pathlib import Path
from typing import Dict, List


def validate_brand_output(output_data: dict) -> dict:
    """
    Validate brand output against 11-point checklist.

    Args:
        output_data: Output data matching photo_brand_output.json schema

    Returns:
        dict with validation_status, score, details, errors, warnings
    """
    results = {
        "validation_status": "PASS",
        "total_score": 0.0,
        "max_score": 11.0,
        "checks_passed": 0,
        "checks_failed": 0,
        "details": {},
        "errors": [],
        "warnings": []
    }

    prompts = output_data.get("prompts_social_grid", [])

    if not prompts:
        results["errors"].append({
            "code": "NO_PROMPTS",
            "message": "No prompts found in output",
            "severity": "critical"
        })
        results["validation_status"] = "FAIL"
        return results

    # Check 1: All prompts 120-500 characters
    check_1_pass = all(
        120 <= p.get("character_count", 0) <= 500
        for p in prompts
    )
    results["details"]["all_lengths_valid"] = check_1_pass
    if check_1_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1
        invalid_prompts = [
            p["scene_number"] for p in prompts
            if not (120 <= p.get("character_count", 0) <= 500)
        ]
        results["warnings"].append({
            "code": "INVALID_LENGTH",
            "message": f"Scenes {invalid_prompts} have invalid prompt length (must be 120-500 chars)",
            "severity": "medium"
        })

    # Check 2: All prompts specify camera settings
    check_2_pass = all(
        "camera" in p.get("technical_specs", {}) and
        p["technical_specs"]["camera"]
        for p in prompts
    )
    results["details"]["all_camera_specified"] = check_2_pass
    if check_2_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 3: All prompts describe lighting
    check_3_pass = all(
        "lighting" in p.get("technical_specs", {}) and
        p["technical_specs"]["lighting"]
        for p in prompts
    )
    results["details"]["all_lighting_described"] = check_3_pass
    if check_3_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 4: All prompts mention background
    check_4_pass = all(
        "background" in p.get("technical_specs", {}) and
        p["technical_specs"]["background"]
        for p in prompts
    )
    results["details"]["all_background_mentioned"] = check_4_pass
    if check_4_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 5: All prompts define composition
    check_5_pass = all(
        "composition" in p.get("technical_specs", {}) and
        p["technical_specs"]["composition"]
        for p in prompts
    )
    results["details"]["all_composition_defined"] = check_5_pass
    if check_5_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 6: All aspect ratios valid
    valid_aspect_ratios = ["1:1", "4:5", "9:16", "16:9", "2:3", "3:4"]
    check_6_pass = all(
        p.get("aspect_ratio") in valid_aspect_ratios
        for p in prompts
    )
    results["details"]["all_aspect_ratios_valid"] = check_6_pass
    if check_6_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1
        invalid_ratios = [
            p["scene_number"] for p in prompts
            if p.get("aspect_ratio") not in valid_aspect_ratios
        ]
        results["warnings"].append({
            "code": "INVALID_ASPECT_RATIO",
            "message": f"Scenes {invalid_ratios} have invalid aspect ratios",
            "severity": "medium"
        })

    # Check 7: All brand colors applied from palette
    brand_identity = output_data.get("brand_integration", {}).get("brand_identity", {})
    brand_palette = brand_identity.get("color_palette", {})

    if brand_palette:
        all_brand_colors = [brand_palette.get("primary", "")] + brand_palette.get("secondary", [])
        check_7_pass = all(
            any(color in p.get("brand_elements", {}).get("brand_colors_applied", [])
                for color in all_brand_colors if color)
            for p in prompts
        )
    else:
        check_7_pass = False

    results["details"]["all_brand_colors_applied"] = check_7_pass
    if check_7_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1
        results["warnings"].append({
            "code": "BRAND_COLORS_NOT_APPLIED",
            "message": "Some prompts don't use brand colors from palette",
            "severity": "high"
        })

    # Check 8: All PNL triggers aligned with brand archetype
    archetype = brand_identity.get("primary_archetype", "")
    archetype_pnl_map = {
        "Hero": ["coragem", "transformação", "confiança"],
        "Sage": ["clareza", "controle", "confiança"],
        "Creator": ["liberdade", "exclusividade", "transformação"],
        "Caregiver": ["conforto", "segurança", "pertencimento"],
        "Lover": ["desejo", "prazer", "exclusividade"],
        "Jester": ["alegria", "liberdade", "pertencimento"],
        "Everyman": ["pertencimento", "conforto", "confiança"]
    }

    expected_pnl = archetype_pnl_map.get(archetype, [])
    if expected_pnl:
        check_8_pass = all(
            p.get("pnl_trigger_key") in expected_pnl or
            any(trigger in p.get("pnl_trigger_archetype", "") for trigger in expected_pnl)
            for p in prompts
        )
    else:
        check_8_pass = True  # Pass if archetype not in map

    results["details"]["all_pnl_aligned_archetype"] = check_8_pass
    if check_8_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1
        results["warnings"].append({
            "code": "PNL_NOT_ALIGNED",
            "message": f"PNL triggers not aligned with {archetype} archetype",
            "severity": "medium"
        })

    # Check 9: All prompts state "8K quality"
    check_9_pass = all(
        "8K quality" in p.get("prompt_brand_aligned", "")
        for p in prompts
    )
    results["details"]["all_8k_stated"] = check_9_pass
    if check_9_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 10: All prompts include "no watermarks"
    check_10_pass = all(
        "no watermarks" in p.get("prompt_brand_aligned", "")
        for p in prompts
    )
    results["details"]["all_no_watermarks"] = check_10_pass
    if check_10_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 11: Platform optimization complete
    check_11_pass = all(
        "platform_optimization" in p and
        "primary_platform" in p["platform_optimization"] and
        p.get("aspect_ratio")
        for p in prompts
    )
    results["details"]["platform_optimized"] = check_11_pass
    if check_11_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Calculate final score
    results["validation_score"] = results["total_score"] / results["max_score"]

    # Determine status (≥0.85 = PASS for brand, more flexible than marketplace)
    if results["validation_score"] >= 0.85:
        results["validation_status"] = "PASS"
        if results["validation_score"] >= 0.95:
            results["brand_consistency"] = "EXCELLENT"
        elif results["validation_score"] >= 0.90:
            results["brand_consistency"] = "GOOD"
        else:
            results["brand_consistency"] = "ACCEPTABLE"
    else:
        results["validation_status"] = "FAIL"
        results["brand_consistency"] = "NEEDS_REFINEMENT"

    return results


def validate_from_file(file_path: str) -> dict:
    """Validate brand output from .llm.json file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return validate_brand_output(data)
    except FileNotFoundError:
        return {"validation_status": "FAIL", "errors": [{"code": "FILE_NOT_FOUND", "message": f"File not found: {file_path}"}]}
    except json.JSONDecodeError as e:
        return {"validation_status": "FAIL", "errors": [{"code": "INVALID_JSON", "message": f"Invalid JSON: {e}"}]}


def print_validation_report(results: dict):
    """Print human-readable validation report"""
    print("=" * 60)
    print("BRAND VALIDATION REPORT")
    print("=" * 60)
    print()
    print(f"Status: {results['validation_status']}")
    print(f"Score: {results['validation_score']:.2f} ({results['checks_passed']}/{int(results['max_score'])} checks passed)")
    if "brand_consistency" in results:
        print(f"Brand Consistency: {results['brand_consistency']}")
    print()

    if results["details"]:
        print("CHECKLIST DETAILS:")
        for check, passed in results["details"].items():
            status = "[OK]" if passed else "[FAIL]"
            print(f"  {status} {check}")
        print()

    if results.get("errors"):
        print("ERRORS:")
        for error in results["errors"]:
            print(f"  [ERROR] {error['message']} (severity: {error.get('severity', 'unknown')})")
        print()

    if results.get("warnings"):
        print("WARNINGS:")
        for warning in results["warnings"]:
            print(f"  [WARN] {warning['message']} (severity: {warning.get('severity', 'unknown')})")
        print()

    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python brand_validator.py <file.llm.json>")
        sys.exit(1)

    file_path = sys.argv[1]
    results = validate_from_file(file_path)
    print_validation_report(results)

    # Exit with appropriate code
    sys.exit(0 if results["validation_status"] == "PASS" else 1)
