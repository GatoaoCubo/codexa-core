#!/usr/bin/env python3
"""
Schema Validator - JSON Schema Validation

Purpose: Validate output files against official JSON schemas
Uses: jsonschema library (optional, fallback to basic validation)

Version: 1.0.0
Author: CODEXA Meta-Construction System
"""

import json
import sys
from pathlib import Path

# Import centralized path configuration
sys.path.insert(0, str(Path(__file__).parent.parent))
from config.paths import PATH_SCHEMAS

# Try to import jsonschema, fallback to basic validation if not available
try:
    import jsonschema
    from jsonschema import validate, ValidationError
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False
    print("[WARN] jsonschema library not found. Using basic validation.")
    print("[INFO] Install with: pip install jsonschema")


def validate_against_schema(data: dict, schema: dict) -> dict:
    """
    Validate data against JSON schema.

    Args:
        data: Output data to validate
        schema: JSON schema to validate against

    Returns:
        dict with validation results
    """
    results = {
        "validation_status": "PASS",
        "schema_valid": False,
        "errors": [],
        "warnings": []
    }

    if JSONSCHEMA_AVAILABLE:
        try:
            validate(instance=data, schema=schema)
            results["schema_valid"] = True
            results["validation_status"] = "PASS"
        except ValidationError as e:
            results["schema_valid"] = False
            results["validation_status"] = "FAIL"
            results["errors"].append({
                "code": "SCHEMA_VALIDATION_ERROR",
                "message": str(e.message),
                "path": list(e.path),
                "severity": "critical"
            })
    else:
        # Basic validation without jsonschema
        required_fields = schema.get("required", [])
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            results["schema_valid"] = False
            results["validation_status"] = "FAIL"
            results["errors"].append({
                "code": "MISSING_REQUIRED_FIELDS",
                "message": f"Missing required fields: {', '.join(missing_fields)}",
                "severity": "critical"
            })
        else:
            results["schema_valid"] = True
            results["validation_status"] = "PASS"
            results["warnings"].append({
                "code": "BASIC_VALIDATION_ONLY",
                "message": "Using basic validation (install jsonschema for full validation)",
                "severity": "low"
            })

    return results


def load_schema(workflow: str) -> dict:
    """Load appropriate schema based on workflow type"""
    schema_map = {
        "marketplace": "photo_marketplace_output.json",
        "brand": "photo_brand_output.json"
    }

    schema_path = PATH_SCHEMAS / schema_map.get(workflow)

    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] Schema not found: {schema_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in schema: {e}")
        return None


def validate_file(file_path: str, workflow: str) -> dict:
    """Validate output file against schema"""
    # Load schema
    schema = load_schema(workflow)
    if not schema:
        return {
            "validation_status": "FAIL",
            "errors": [{"code": "SCHEMA_LOAD_ERROR", "message": "Failed to load schema"}]
        }

    # Load data
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return {
            "validation_status": "FAIL",
            "errors": [{"code": "FILE_NOT_FOUND", "message": f"File not found: {file_path}"}]
        }
    except json.JSONDecodeError as e:
        return {
            "validation_status": "FAIL",
            "errors": [{"code": "INVALID_JSON", "message": f"Invalid JSON: {e}"}]
        }

    # Validate
    return validate_against_schema(data, schema)


def print_validation_report(results: dict):
    """Print human-readable validation report"""
    print("=" * 60)
    print("SCHEMA VALIDATION REPORT")
    print("=" * 60)
    print()
    print(f"Status: {results['validation_status']}")
    print(f"Schema Valid: {results.get('schema_valid', False)}")
    print()

    if results.get("errors"):
        print("ERRORS:")
        for error in results["errors"]:
            print(f"  [ERROR] {error['message']}")
            if "path" in error and error["path"]:
                print(f"          Path: {' -> '.join(map(str, error['path']))}")
        print()

    if results.get("warnings"):
        print("WARNINGS:")
        for warning in results["warnings"]:
            print(f"  [WARN] {warning['message']}")
        print()

    print("=" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python schema_validator.py <workflow> <file.llm.json>")
        print("  workflow: 'marketplace' or 'brand'")
        print("  file.llm.json: Path to output file to validate")
        sys.exit(1)

    workflow = sys.argv[1]
    file_path = sys.argv[2]

    if workflow not in ["marketplace", "brand"]:
        print(f"[ERROR] Invalid workflow: {workflow}. Must be 'marketplace' or 'brand'")
        sys.exit(1)

    results = validate_file(file_path, workflow)
    print_validation_report(results)

    # Exit with appropriate code
    sys.exit(0 if results["validation_status"] == "PASS" else 1)
