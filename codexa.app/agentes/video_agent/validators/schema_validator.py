"""
schema_validator.py - Validate pipeline data against JSON schemas

Validates:
- video_input.json schema
- video_output.json schema
- concept.json structure
- script.json structure
- visual_prompts.json structure

Author: CODEXA Meta-Constructor
Version: 1.0.0
"""

import json
import sys
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class SchemaValidationResult:
    """Result of schema validation"""
    schema_name: str
    passed: bool
    errors: List[str]
    warnings: List[str]


class SchemaValidator:
    """
    Validate pipeline data against JSON schemas

    Usage:
        validator = SchemaValidator()
        result = validator.validate_input({"produto": "Nike", "duracao": 30})
        print(f"Valid: {result.passed}")
    """

    def __init__(self, schemas_dir: str = "schemas"):
        self.schemas_dir = Path(schemas_dir)

        # Define schemas inline for portability
        self.schemas = {
            "video_input": {
                "type": "object",
                "required": ["produto", "duracao", "objetivo"],
                "properties": {
                    "produto": {"type": "string", "minLength": 3, "maxLength": 200},
                    "duracao": {"type": "integer", "minimum": 15, "maximum": 60},
                    "formato": {"type": "string", "enum": ["9:16", "16:9", "1:1"]},
                    "tom": {"type": "string"},
                    "objetivo": {"type": "string", "minLength": 10, "maxLength": 500}
                }
            },
            "concept": {
                "type": "object",
                "required": ["shots", "total_duration"],
                "properties": {
                    "shots": {
                        "type": "array",
                        "minItems": 3,
                        "maxItems": 8,
                        "items": {
                            "type": "object",
                            "required": ["number", "duration", "description", "narrative"],
                            "properties": {
                                "number": {"type": "integer", "minimum": 1},
                                "duration": {"type": "number", "minimum": 1, "maximum": 15},
                                "description": {"type": "string", "minLength": 10},
                                "composition": {"type": "string"},
                                "narrative": {"type": "string", "enum": ["hook", "build", "benefit", "proof", "cta"]}
                            }
                        }
                    },
                    "total_duration": {"type": "integer", "minimum": 15, "maximum": 60},
                    "narrative_arc": {"type": "string"},
                    "style_preset": {"type": "string"}
                }
            },
            "script": {
                "type": "object",
                "required": ["narration", "text_overlays"],
                "properties": {
                    "narration": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["start", "end", "text"],
                            "properties": {
                                "start": {"type": "number", "minimum": 0},
                                "end": {"type": "number", "minimum": 0},
                                "text": {"type": "string", "minLength": 1}
                            }
                        }
                    },
                    "text_overlays": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "required": ["start", "end", "text"],
                            "properties": {
                                "start": {"type": "number", "minimum": 0},
                                "end": {"type": "number", "minimum": 0},
                                "text": {"type": "string", "minLength": 1},
                                "position": {"type": "string", "enum": ["top", "center", "bottom"]},
                                "style": {"type": "string", "enum": ["normal", "bold"]}
                            }
                        }
                    },
                    "music": {
                        "type": "object",
                        "properties": {
                            "track": {"type": "string"},
                            "volume": {"type": "number", "minimum": 0, "maximum": 1}
                        }
                    },
                    "voice": {"type": "string"}
                }
            },
            "visual_prompts": {
                "type": "array",
                "minItems": 3,
                "maxItems": 8,
                "items": {
                    "type": "object",
                    "required": ["shot_number", "duration", "runway_prompt"],
                    "properties": {
                        "shot_number": {"type": "integer", "minimum": 1},
                        "duration": {"type": "number", "minimum": 1},
                        "runway_prompt": {"type": "string", "minLength": 20, "maxLength": 500},
                        "pika_prompt": {"type": "string"},
                        "camera": {"type": "object"},
                        "lighting": {"type": "string"},
                        "transition": {"type": "string"}
                    }
                }
            },
            "clips": {
                "type": "array",
                "minItems": 1,
                "items": {
                    "type": "object",
                    "required": ["shot_number", "success"],
                    "properties": {
                        "shot_number": {"type": "integer", "minimum": 1},
                        "clip_path": {"type": "string"},
                        "success": {"type": "boolean"},
                        "api_used": {"type": "string"},
                        "cost_usd": {"type": "number", "minimum": 0},
                        "generation_time_s": {"type": "number", "minimum": 0},
                        "error": {"type": ["string", "null"]}
                    }
                }
            }
        }

    def validate(self, data: Any, schema_name: str) -> SchemaValidationResult:
        """
        Validate data against named schema

        Args:
            data: Data to validate
            schema_name: Name of schema (video_input, concept, script, etc.)

        Returns:
            SchemaValidationResult
        """

        if schema_name not in self.schemas:
            return SchemaValidationResult(
                schema_name=schema_name,
                passed=False,
                errors=[f"Unknown schema: {schema_name}"],
                warnings=[]
            )

        schema = self.schemas[schema_name]
        errors = []
        warnings = []

        # Validate type
        if schema.get("type") == "object" and not isinstance(data, dict):
            errors.append(f"Expected object, got {type(data).__name__}")
            return SchemaValidationResult(schema_name, False, errors, warnings)

        if schema.get("type") == "array" and not isinstance(data, list):
            errors.append(f"Expected array, got {type(data).__name__}")
            return SchemaValidationResult(schema_name, False, errors, warnings)

        # Validate object
        if schema.get("type") == "object":
            errors, warnings = self._validate_object(data, schema)

        # Validate array
        elif schema.get("type") == "array":
            errors, warnings = self._validate_array(data, schema)

        return SchemaValidationResult(
            schema_name=schema_name,
            passed=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )

    def _validate_object(self, data: Dict, schema: Dict) -> tuple:
        """Validate object against schema"""

        errors = []
        warnings = []

        # Check required fields
        required = schema.get("required", [])
        for field in required:
            if field not in data:
                errors.append(f"Missing required field: {field}")

        # Check properties
        properties = schema.get("properties", {})
        for field, rules in properties.items():
            if field in data:
                field_errors, field_warnings = self._validate_field(
                    data[field], rules, field
                )
                errors.extend(field_errors)
                warnings.extend(field_warnings)

        return errors, warnings

    def _validate_array(self, data: List, schema: Dict) -> tuple:
        """Validate array against schema"""

        errors = []
        warnings = []

        # Check min/max items
        min_items = schema.get("minItems", 0)
        max_items = schema.get("maxItems", float("inf"))

        if len(data) < min_items:
            errors.append(f"Array has {len(data)} items, minimum is {min_items}")

        if len(data) > max_items:
            errors.append(f"Array has {len(data)} items, maximum is {max_items}")

        # Check items
        items_schema = schema.get("items", {})
        for i, item in enumerate(data):
            if items_schema.get("type") == "object":
                item_errors, item_warnings = self._validate_object(item, items_schema)
                errors.extend([f"[{i}] {e}" for e in item_errors])
                warnings.extend([f"[{i}] {w}" for w in item_warnings])

        return errors, warnings

    def _validate_field(self, value: Any, rules: Dict, field_name: str) -> tuple:
        """Validate single field against rules"""

        errors = []
        warnings = []

        # Type check
        expected_type = rules.get("type")
        if expected_type:
            type_map = {
                "string": str,
                "integer": int,
                "number": (int, float),
                "boolean": bool,
                "array": list,
                "object": dict
            }

            if expected_type in type_map:
                expected = type_map[expected_type]
                if not isinstance(value, expected):
                    errors.append(f"{field_name}: expected {expected_type}, got {type(value).__name__}")
                    return errors, warnings

        # String validations
        if isinstance(value, str):
            min_len = rules.get("minLength", 0)
            max_len = rules.get("maxLength", float("inf"))

            if len(value) < min_len:
                errors.append(f"{field_name}: string too short ({len(value)} < {min_len})")

            if len(value) > max_len:
                errors.append(f"{field_name}: string too long ({len(value)} > {max_len})")

            # Enum check
            enum = rules.get("enum")
            if enum and value not in enum:
                errors.append(f"{field_name}: '{value}' not in {enum}")

        # Number validations
        if isinstance(value, (int, float)):
            minimum = rules.get("minimum")
            maximum = rules.get("maximum")

            if minimum is not None and value < minimum:
                errors.append(f"{field_name}: {value} < minimum {minimum}")

            if maximum is not None and value > maximum:
                errors.append(f"{field_name}: {value} > maximum {maximum}")

        # Nested object
        if isinstance(value, dict) and rules.get("type") == "object":
            nested_errors, nested_warnings = self._validate_object(value, rules)
            errors.extend([f"{field_name}.{e}" for e in nested_errors])
            warnings.extend([f"{field_name}.{w}" for w in nested_warnings])

        # Nested array
        if isinstance(value, list) and rules.get("type") == "array":
            nested_errors, nested_warnings = self._validate_array(value, rules)
            errors.extend([f"{field_name}{e}" for e in nested_errors])
            warnings.extend([f"{field_name}{w}" for w in nested_warnings])

        return errors, warnings

    def validate_input(self, data: Dict) -> SchemaValidationResult:
        """Validate video input brief"""
        return self.validate(data, "video_input")

    def validate_concept(self, data: Dict) -> SchemaValidationResult:
        """Validate concept/storyboard output"""
        return self.validate(data, "concept")

    def validate_script(self, data: Dict) -> SchemaValidationResult:
        """Validate script output"""
        return self.validate(data, "script")

    def validate_visual_prompts(self, data: List) -> SchemaValidationResult:
        """Validate visual prompts output"""
        return self.validate(data, "visual_prompts")

    def validate_clips(self, data: List) -> SchemaValidationResult:
        """Validate production clips output"""
        return self.validate(data, "clips")

    def validate_pipeline(self, pipeline_data: Dict) -> Dict[str, SchemaValidationResult]:
        """
        Validate all pipeline stages

        Args:
            pipeline_data: Dict with keys matching schema names

        Returns:
            Dict of schema_name -> ValidationResult
        """

        results = {}

        for schema_name, data in pipeline_data.items():
            if schema_name in self.schemas:
                results[schema_name] = self.validate(data, schema_name)

        return results

    def print_result(self, result: SchemaValidationResult):
        """Print formatted validation result"""

        status = "[PASS]" if result.passed else "[FAIL]"
        print(f"{status} {result.schema_name}")

        for error in result.errors:
            print(f"  [ERROR] {error}")

        for warning in result.warnings:
            print(f"  [WARN] {warning}")


# ======================
# STANDALONE USAGE
# ======================

def main():
    """Run validator from command line"""

    if len(sys.argv) < 3:
        print("Usage: python schema_validator.py <schema_name> <json_file>")
        print("Schemas: video_input, concept, script, visual_prompts, clips")
        print("Example: python schema_validator.py concept outputs/concept.json")
        sys.exit(1)

    schema_name = sys.argv[1]
    json_file = sys.argv[2]

    # Load JSON
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error loading JSON: {e}")
        sys.exit(1)

    # Validate
    validator = SchemaValidator()
    result = validator.validate(data, schema_name)

    print("\n" + "=" * 50)
    print("SCHEMA VALIDATION REPORT")
    print("=" * 50)
    validator.print_result(result)
    print("=" * 50)

    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
