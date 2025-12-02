#!/usr/bin/env python3
"""
CODEXA Prompt Layer Composer
Version: 1.0.0
Created: 2025-11-24

Composes prompt layers into complete agent prompts.
Supports presets, custom compositions, and validation.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Dict, Optional, Any
import yaml


class LayerComposer:
    """Compose CODEXA prompt layers into complete prompts."""

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize layer composer.

        Args:
            config_path: Path to prompt_layers.yml config file
        """
        self.config_path = config_path or Path("config/prompt_layers.yml")
        self.layers_dir = Path("prompts/layers")
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load prompt layers configuration from YAML."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Config not found: {self.config_path}")

        with open(self.config_path, encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _find_layer_config(self, layer_id: str) -> Optional[Dict[str, Any]]:
        """
        Find layer configuration by ID.

        Args:
            layer_id: Layer ID to search for

        Returns:
            Layer configuration dict if found, None otherwise
        """
        layers = self.config.get("layers", {})
        for layer_key, layer_config in layers.items():
            if layer_config.get("id") == layer_id:
                return layer_config
        return None

    def get_layer_path(self, layer_id: str) -> Path:
        """
        Get file path for a layer by ID.

        Args:
            layer_id: Layer ID (e.g., "01_identity_layer")

        Returns:
            Path to layer file

        Raises:
            ValueError: If layer ID not found in config
        """
        layer_config = self._find_layer_config(layer_id)
        if layer_config is None:
            raise ValueError(f"Layer not found: {layer_id}")

        return Path(layer_config["file"])

    def read_layer(self, layer_id: str) -> str:
        """
        Read content of a layer file.

        Args:
            layer_id: Layer ID

        Returns:
            Layer file contents

        Raises:
            FileNotFoundError: If layer file doesn't exist
        """
        layer_path = self.get_layer_path(layer_id)

        if not layer_path.exists():
            raise FileNotFoundError(f"Layer file not found: {layer_path}")

        with open(layer_path, encoding="utf-8") as f:
            return f.read()

    def validate_dependencies(self, layer_ids: List[str]) -> bool:
        """
        Validate that all layer dependencies are satisfied.

        Args:
            layer_ids: List of layer IDs to compose

        Returns:
            True if all dependencies satisfied

        Raises:
            ValueError: If dependencies not satisfied
        """
        for layer_id in layer_ids:
            layer_config = self._find_layer_config(layer_id)
            if layer_config is None:
                raise ValueError(f"Layer not found: {layer_id}")

            dependencies = layer_config.get("dependencies", [])

            for dep in dependencies:
                if dep not in layer_ids:
                    raise ValueError(
                        f"Layer {layer_id} requires {dep}, but it's not included"
                    )

                # Check that dependency comes before this layer
                if layer_ids.index(dep) > layer_ids.index(layer_id):
                    raise ValueError(
                        f"Layer {dep} must come before {layer_id}"
                    )

        return True

    def compose_layers(
        self,
        layer_ids: List[str],
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Compose multiple layers into a single prompt.

        Args:
            layer_ids: List of layer IDs to compose (in order)
            context: Optional context variables for template substitution

        Returns:
            Composed prompt text

        Raises:
            ValueError: If dependencies not satisfied or layers not found
        """
        # Validate dependencies
        self.validate_dependencies(layer_ids)

        # Read all layers
        composed_parts = []
        composed_parts.append("# CODEXA Agent Prompt\n")
        composed_parts.append(f"# Composed from {len(layer_ids)} layers\n")
        composed_parts.append(f"# Layers: {', '.join(layer_ids)}\n")
        composed_parts.append("\n" + "=" * 80 + "\n\n")

        for layer_id in layer_ids:
            layer_content = self.read_layer(layer_id)

            # Add layer separator
            composed_parts.append(f"## LAYER: {layer_id}\n\n")
            composed_parts.append(layer_content)
            composed_parts.append("\n\n" + "=" * 80 + "\n\n")

        composed_text = "".join(composed_parts)

        # Apply context substitution if provided
        if context:
            for key, value in context.items():
                composed_text = composed_text.replace(f"{{{{{key}}}}}", str(value))

        return composed_text

    def load_preset(self, preset_name: str) -> Dict[str, Any]:
        """
        Load a preset configuration.

        Args:
            preset_name: Name of preset (e.g., "planning", "execution")

        Returns:
            Preset configuration dictionary

        Raises:
            ValueError: If preset not found
        """
        presets = self.config.get("presets", {})
        if preset_name not in presets:
            raise ValueError(f"Preset not found: {preset_name}")

        return presets[preset_name]

    def compose_preset(
        self,
        preset_name: str,
        context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Compose layers from a preset.

        Args:
            preset_name: Name of preset
            context: Optional context variables

        Returns:
            Composed prompt text
        """
        preset = self.load_preset(preset_name)
        layer_ids = preset["layers"]

        return self.compose_layers(layer_ids, context)

    def list_presets(self) -> List[Dict[str, Any]]:
        """
        List all available presets.

        Returns:
            List of preset dictionaries with name, description, layers
        """
        presets = self.config.get("presets", {})
        result = []

        for name, config in presets.items():
            result.append({
                "name": name,
                "description": config.get("description", ""),
                "layers": config.get("layers", []),
                "use_cases": config.get("use_cases", [])
            })

        return result

    def list_layers(self) -> List[Dict[str, Any]]:
        """
        List all available layers.

        Returns:
            List of layer dictionaries with id, description, dependencies
        """
        layers = self.config.get("layers", {})
        result = []

        for layer_id, config in layers.items():
            result.append({
                "id": layer_id,
                "file": config.get("file", ""),
                "description": config.get("description", ""),
                "category": config.get("category", ""),
                "dependencies": config.get("dependencies", []),
                "size_lines": config.get("size_lines", 0)
            })

        return result

    def validate_composition(self, layer_ids: List[str]) -> Dict[str, Any]:
        """
        Validate a composition without generating it.

        Args:
            layer_ids: List of layer IDs

        Returns:
            Validation result with status, errors, warnings
        """
        result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "total_lines": 0
        }

        # Check dependencies
        try:
            self.validate_dependencies(layer_ids)
        except ValueError as e:
            result["valid"] = False
            result["errors"].append(str(e))
            return result

        # Check total size
        total_lines = 0
        for layer_id in layer_ids:
            layer_config = self._find_layer_config(layer_id)
            if layer_config:
                total_lines += layer_config.get("size_lines", 0)
        result["total_lines"] = total_lines

        # Warn if size exceeds threshold
        if total_lines > 5000:
            result["warnings"].append(
                f"Composed prompt is large ({total_lines} lines). "
                "Consider using fewer layers or splitting into multiple agents."
            )

        return result


def main():
    """CLI entry point for prompt layer composer."""
    parser = argparse.ArgumentParser(
        description="CODEXA Prompt Layer Composer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List available presets
  python composer.py --list-presets

  # List available layers
  python composer.py --list-layers

  # Compose using preset
  python composer.py --preset planning --output planning_agent.md

  # Compose custom layers
  python composer.py --layers 01_identity_layer,02_operating_modes --output custom.md

  # Validate composition
  python composer.py --layers 01_identity_layer,02_operating_modes --validate
        """
    )

    parser.add_argument(
        "--preset",
        type=str,
        help="Preset name (planning, execution, verification, etc.)"
    )

    parser.add_argument(
        "--layers",
        type=str,
        help="Comma-separated list of layer IDs to compose"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output file path for composed prompt"
    )

    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate composition without generating output"
    )

    parser.add_argument(
        "--list-presets",
        action="store_true",
        help="List all available presets"
    )

    parser.add_argument(
        "--list-layers",
        action="store_true",
        help="List all available layers"
    )

    parser.add_argument(
        "--config",
        type=str,
        help="Path to prompt_layers.yml config file"
    )

    args = parser.parse_args()

    # Initialize composer
    try:
        config_path = Path(args.config) if args.config else None
        composer = LayerComposer(config_path)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Handle --list-presets
    if args.list_presets:
        presets = composer.list_presets()
        print("Available Presets:\n")
        for preset in presets:
            print(f"  {preset['name']}")
            print(f"    Description: {preset['description']}")
            print(f"    Layers: {', '.join(preset['layers'])}")
            print(f"    Use Cases: {', '.join(preset['use_cases'])}")
            print()
        return

    # Handle --list-layers
    if args.list_layers:
        layers = composer.list_layers()
        print("Available Layers:\n")
        for layer in layers:
            print(f"  {layer['id']}")
            print(f"    Description: {layer['description']}")
            print(f"    Category: {layer['category']}")
            print(f"    Size: {layer['size_lines']} lines")
            if layer['dependencies']:
                print(f"    Dependencies: {', '.join(layer['dependencies'])}")
            print()
        return

    # Determine layer IDs
    layer_ids = []
    if args.preset:
        preset = composer.load_preset(args.preset)
        layer_ids = preset["layers"]
        print(f"Using preset: {args.preset}")
    elif args.layers:
        layer_ids = [lid.strip() for lid in args.layers.split(",")]
    else:
        print("Error: Must specify --preset or --layers", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Validate composition
    if args.validate or not args.output:
        validation = composer.validate_composition(layer_ids)

        if validation["valid"]:
            print("✅ Composition is valid")
            print(f"Total lines: {validation['total_lines']}")
        else:
            print("❌ Composition is invalid")
            for error in validation["errors"]:
                print(f"  Error: {error}")

        for warning in validation["warnings"]:
            print(f"  Warning: {warning}")

        if args.validate:
            sys.exit(0 if validation["valid"] else 1)

    # Compose and write output
    if args.output:
        try:
            composed_prompt = composer.compose_layers(layer_ids)
            output_path = Path(args.output)

            # Create parent directories if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write output
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(composed_prompt)

            print(f"✅ Composed prompt written to: {output_path}")
            print(f"   Layers: {', '.join(layer_ids)}")
            print(f"   Size: {len(composed_prompt)} characters")

        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
