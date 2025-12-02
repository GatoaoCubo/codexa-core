#!/usr/bin/env python3
"""
Marketplace Validator - 13-Point Compliance Checklist

Purpose: Validate marketplace output against strict compliance rules
Target: Brazilian marketplaces (ML, Shopee, Amazon BR, Magalu)

Checklist (13 points):
  1. Scene 1 has #FFFFFF white background (CRITICAL)
  2. Scene 9 has #FFFFFF white background (CRITICAL)
  3. All prompts 100-400 characters
  4. All prompts specify camera settings
  5. All prompts describe lighting
  6. All prompts mention background
  7. All prompts define composition
  8. All prompts state "8K quality"
  9. All prompts include "no watermarks"
  10. All prompts include "no text"
  11. All prompts include "no third-party logos" (scenes 1+9)
  12. All prompts include PNL trigger
  13. All prompts include {INSERIR_IMAGEM_PRODUTO_AQUI} placeholder

Version: 1.0.0
Author: CODEXA Meta-Construction System
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple


def validate_marketplace_output(output_data: dict) -> dict:
    """
    Validate marketplace output against 13-point checklist.

    Args:
        output_data: Output data matching photo_marketplace_output.json schema

    Returns:
        dict with validation_status, score, details, errors, warnings
    """
    results = {
        "validation_status": "PASS",
        "total_score": 0.0,
        "max_score": 13.0,
        "checks_passed": 0,
        "checks_failed": 0,
        "details": {},
        "errors": [],
        "warnings": []
    }

    prompts = output_data.get("prompts_grid_3x3", [])

    if len(prompts) != 9:
        results["errors"].append({
            "code": "WRONG_PROMPT_COUNT",
            "message": f"Expected 9 prompts, found {len(prompts)}",
            "severity": "critical"
        })
        results["validation_status"] = "FAIL"
        return results

    # Check 1: Scene 1 has #FFFFFF white background
    scene_1 = next((p for p in prompts if p["scene_number"] == 1), None)
    check_1_pass = False
    if scene_1:
        check_1_pass = (
            scene_1.get("compliance_white_bg") == True and
            "#FFFFFF" in scene_1["technical_specs"].get("background", "")
        )
    results["details"]["scene_1_white_bg"] = check_1_pass
    if check_1_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1
        results["errors"].append({
            "code": "SCENE_1_WHITE_BG_MISSING",
            "message": "Scene 1 MUST have #FFFFFF white background (CRITICAL)",
            "severity": "critical"
        })

    # Check 2: Scene 9 has #FFFFFF white background
    scene_9 = next((p for p in prompts if p["scene_number"] == 9), None)
    check_2_pass = False
    if scene_9:
        check_2_pass = (
            scene_9.get("compliance_white_bg") == True and
            "#FFFFFF" in scene_9["technical_specs"].get("background", "")
        )
    results["details"]["scene_9_white_bg"] = check_2_pass
    if check_2_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1
        results["errors"].append({
            "code": "SCENE_9_WHITE_BG_MISSING",
            "message": "Scene 9 MUST have #FFFFFF white background (CRITICAL)",
            "severity": "critical"
        })

    # Check 3: All prompts 100-400 characters
    check_3_pass = all(
        100 <= p.get("character_count", 0) <= 400
        for p in prompts
    )
    results["details"]["all_lengths_valid"] = check_3_pass
    if check_3_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1
        invalid_prompts = [
            p["scene_number"] for p in prompts
            if not (100 <= p.get("character_count", 0) <= 400)
        ]
        results["warnings"].append({
            "code": "INVALID_LENGTH",
            "message": f"Scenes {invalid_prompts} have invalid prompt length (must be 100-400 chars)",
            "severity": "medium"
        })

    # Check 4: All prompts specify camera settings
    check_4_pass = all(
        "camera" in p.get("technical_specs", {}) and
        p["technical_specs"]["camera"]
        for p in prompts
    )
    results["details"]["all_camera_specified"] = check_4_pass
    if check_4_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 5: All prompts describe lighting
    check_5_pass = all(
        "lighting" in p.get("technical_specs", {}) and
        p["technical_specs"]["lighting"]
        for p in prompts
    )
    results["details"]["all_lighting_described"] = check_5_pass
    if check_5_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 6: All prompts mention background
    check_6_pass = all(
        "background" in p.get("technical_specs", {}) and
        p["technical_specs"]["background"]
        for p in prompts
    )
    results["details"]["all_background_mentioned"] = check_6_pass
    if check_6_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 7: All prompts define composition
    check_7_pass = all(
        "composition" in p.get("technical_specs", {}) and
        p["technical_specs"]["composition"]
        for p in prompts
    )
    results["details"]["all_composition_defined"] = check_7_pass
    if check_7_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 8: All prompts state "8K quality"
    check_8_pass = all(
        "8K quality" in p.get("prompt_with_reference", "")
        for p in prompts
    )
    results["details"]["all_8k_stated"] = check_8_pass
    if check_8_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 9: All prompts include "no watermarks"
    check_9_pass = all(
        "no watermarks" in p.get("prompt_with_reference", "")
        for p in prompts
    )
    results["details"]["all_no_watermarks"] = check_9_pass
    if check_9_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 10: All prompts include "no text"
    check_10_pass = all(
        "no text" in p.get("prompt_with_reference", "")
        for p in prompts
    )
    results["details"]["all_no_text"] = check_10_pass
    if check_10_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 11: Scenes 1+9 include "no third-party logos"
    check_11_pass = all(
        "no third-party logos" in p.get("prompt_with_reference", "")
        for p in prompts if p["scene_number"] in [1, 9]
    )
    results["details"]["all_no_logos"] = check_11_pass
    if check_11_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 12: All prompts include PNL trigger
    check_12_pass = all(
        "pnl_trigger" in p and p["pnl_trigger"]
        for p in prompts
    )
    results["details"]["all_pnl_included"] = check_12_pass
    if check_12_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1

    # Check 13: All prompts include {INSERIR_IMAGEM_PRODUTO_AQUI} placeholder
    check_13_pass = all(
        "{INSERIR_IMAGEM_PRODUTO_AQUI}" in p.get("prompt_with_reference", "")
        for p in prompts
    )
    results["details"]["all_reference_placeholder"] = check_13_pass
    if check_13_pass:
        results["checks_passed"] += 1
        results["total_score"] += 1.0
    else:
        results["checks_failed"] += 1
        results["errors"].append({
            "code": "MISSING_REFERENCE_PLACEHOLDER",
            "message": "All prompts must include {INSERIR_IMAGEM_PRODUTO_AQUI} placeholder",
            "severity": "high"
        })

    # Calculate final score
    results["validation_score"] = results["total_score"] / results["max_score"]

    # Determine status (≥0.90 = PASS)
    if results["validation_score"] >= 0.90 and check_1_pass and check_2_pass:
        results["validation_status"] = "PASS"
    else:
        results["validation_status"] = "FAIL"

    return results


def validate_from_file(file_path: str) -> dict:
    """Validate marketplace output from .llm.json file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return validate_marketplace_output(data)
    except FileNotFoundError:
        return {"validation_status": "FAIL", "errors": [{"code": "FILE_NOT_FOUND", "message": f"File not found: {file_path}"}]}
    except json.JSONDecodeError as e:
        return {"validation_status": "FAIL", "errors": [{"code": "INVALID_JSON", "message": f"Invalid JSON: {e}"}]}


def print_validation_report(results: dict):
    """Print human-readable validation report"""
    print("=" * 60)
    print("MARKETPLACE VALIDATION REPORT")
    print("=" * 60)
    print()
    print(f"Status: {results['validation_status']}")
    print(f"Score: {results['validation_score']:.2f} ({results['checks_passed']}/{int(results['max_score'])} checks passed)")
    print()

    if results["details"]:
        print("CHECKLIST DETAILS:")
        for check, passed in results["details"].items():
            status = "[OK]" if passed else "[FAIL]"
            print(f"  {status} {check}")
        print()

    if results["errors"]:
        print("ERRORS:")
        for error in results["errors"]:
            print(f"  [ERROR] {error['message']} (severity: {error['severity']})")
        print()

    if results["warnings"]:
        print("WARNINGS:")
        for warning in results["warnings"]:
            print(f"  [WARN] {warning['message']} (severity: {warning['severity']})")
        print()

    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python marketplace_validator.py <file.llm.json>")
        sys.exit(1)

    file_path = sys.argv[1]
    results = validate_from_file(file_path)
    print_validation_report(results)

    # Exit with appropriate code
    sys.exit(0 if results["validation_status"] == "PASS" else 1)
