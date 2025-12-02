"""
Prompt Layer Composition Tests
Tests for the CODEXA composable prompt layer system.
"""

import pytest
from pathlib import Path
from typing import Optional
import re


# Path to prompt layers
LAYERS_DIR = Path(__file__).parent.parent / "prompts" / "layers"


class PromptLayerValidator:
    """Validates prompt layer files."""

    REQUIRED_SECTIONS = [
        "MODULE_METADATA",
        "PURPOSE",
    ]

    def __init__(self, layer_path: Path):
        self.path = layer_path
        self.content = ""
        self.metadata = {}

    def load(self) -> bool:
        """Load and parse the layer file."""
        if not self.path.exists():
            return False

        self.content = self.path.read_text(encoding='utf-8')
        self._parse_metadata()
        return True

    def _parse_metadata(self):
        """Extract metadata from layer content."""
        # Extract YAML metadata block
        yaml_match = re.search(r'```yaml\n(.*?)\n```', self.content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
            # Simple parsing (no yaml library needed)
            for line in yaml_content.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    self.metadata[key.strip()] = value.strip()

    def validate_structure(self) -> tuple[bool, list[str]]:
        """Validate layer structure."""
        errors = []

        # Check required sections
        for section in self.REQUIRED_SECTIONS:
            if section not in self.content:
                errors.append(f"Missing required section: {section}")

        # Check has title
        if not self.content.startswith('#'):
            errors.append("Layer must start with title (# heading)")

        return len(errors) == 0, errors

    def validate_metadata(self) -> tuple[bool, list[str]]:
        """Validate metadata completeness."""
        errors = []
        required_metadata = ['id', 'version', 'category']

        for field in required_metadata:
            if field not in self.metadata:
                errors.append(f"Missing metadata field: {field}")

        return len(errors) == 0, errors

    def get_id(self) -> Optional[str]:
        """Get layer ID from metadata."""
        return self.metadata.get('id')

    def get_version(self) -> Optional[str]:
        """Get layer version from metadata."""
        return self.metadata.get('version')


class PromptComposer:
    """Composes multiple prompt layers into a single prompt."""

    def __init__(self, layers_dir: Path):
        self.layers_dir = layers_dir
        self._layer_cache: dict[str, str] = {}

    def load_layer(self, layer_name: str) -> Optional[str]:
        """Load a single layer by name."""
        if layer_name in self._layer_cache:
            return self._layer_cache[layer_name]

        # Try with .md extension
        layer_path = self.layers_dir / f"{layer_name}.md"
        if not layer_path.exists():
            # Try without extension
            layer_path = self.layers_dir / layer_name
            if not layer_path.exists():
                return None

        content = layer_path.read_text(encoding='utf-8')
        self._layer_cache[layer_name] = content
        return content

    def compose(self, layer_names: list[str]) -> str:
        """Compose multiple layers into a single prompt."""
        composed = []

        for name in layer_names:
            content = self.load_layer(name)
            if content:
                composed.append(content)
                composed.append("\n---\n")  # Separator

        return "\n".join(composed)

    def list_available_layers(self) -> list[str]:
        """List all available layers."""
        if not self.layers_dir.exists():
            return []

        return [
            f.stem for f in self.layers_dir.glob("*.md")
            if f.is_file()
        ]


class TestPromptLayerValidator:
    """Tests for PromptLayerValidator."""

    @pytest.fixture
    def sample_layer_content(self, tmp_path):
        """Create a sample layer file for testing."""
        content = """# 01_identity_layer | CODEXA Identity

## MODULE_METADATA

```yaml
id: 01_identity_layer
version: 1.0.0
category: core
type: composable_layer
```

## PURPOSE

Define the core identity and capabilities of CODEXA.

## CONTENT

CODEXA is a meta-construction system for building AI agents.
"""
        layer_file = tmp_path / "01_identity_layer.md"
        layer_file.write_text(content)
        return layer_file

    def test_load_valid_layer(self, sample_layer_content):
        """Test loading a valid layer file."""
        validator = PromptLayerValidator(sample_layer_content)
        assert validator.load()
        assert len(validator.content) > 0

    def test_validate_structure(self, sample_layer_content):
        """Test structure validation."""
        validator = PromptLayerValidator(sample_layer_content)
        validator.load()

        valid, errors = validator.validate_structure()
        assert valid
        assert len(errors) == 0

    def test_validate_metadata(self, sample_layer_content):
        """Test metadata validation."""
        validator = PromptLayerValidator(sample_layer_content)
        validator.load()

        valid, errors = validator.validate_metadata()
        assert valid
        assert validator.get_id() == "01_identity_layer"
        assert validator.get_version() == "1.0.0"

    def test_missing_section(self, tmp_path):
        """Test detection of missing required section."""
        content = """# Layer Without Metadata

Some content here.
"""
        layer_file = tmp_path / "bad_layer.md"
        layer_file.write_text(content)

        validator = PromptLayerValidator(layer_file)
        validator.load()

        valid, errors = validator.validate_structure()
        assert not valid
        assert any("MODULE_METADATA" in e for e in errors)

    def test_nonexistent_file(self, tmp_path):
        """Test handling of nonexistent file."""
        validator = PromptLayerValidator(tmp_path / "nonexistent.md")
        assert not validator.load()


class TestPromptComposer:
    """Tests for PromptComposer."""

    @pytest.fixture
    def layers_dir(self, tmp_path):
        """Create a temporary layers directory with test files."""
        layers = tmp_path / "layers"
        layers.mkdir()

        # Create test layers
        (layers / "01_identity.md").write_text("# Identity\nI am CODEXA.")
        (layers / "02_tools.md").write_text("# Tools\nAvailable tools: Read, Write.")
        (layers / "03_rules.md").write_text("# Rules\nFollow coding standards.")

        return layers

    def test_load_single_layer(self, layers_dir):
        """Test loading a single layer."""
        composer = PromptComposer(layers_dir)
        content = composer.load_layer("01_identity")

        assert content is not None
        assert "I am CODEXA" in content

    def test_compose_multiple_layers(self, layers_dir):
        """Test composing multiple layers."""
        composer = PromptComposer(layers_dir)
        composed = composer.compose(["01_identity", "02_tools", "03_rules"])

        assert "I am CODEXA" in composed
        assert "Available tools" in composed
        assert "Follow coding standards" in composed

    def test_layer_caching(self, layers_dir):
        """Test that layers are cached after first load."""
        composer = PromptComposer(layers_dir)

        # Load twice
        content1 = composer.load_layer("01_identity")
        content2 = composer.load_layer("01_identity")

        assert content1 == content2
        assert "01_identity" in composer._layer_cache

    def test_list_available_layers(self, layers_dir):
        """Test listing available layers."""
        composer = PromptComposer(layers_dir)
        layers = composer.list_available_layers()

        assert len(layers) == 3
        assert "01_identity" in layers
        assert "02_tools" in layers
        assert "03_rules" in layers

    def test_nonexistent_layer(self, layers_dir):
        """Test handling of nonexistent layer."""
        composer = PromptComposer(layers_dir)
        content = composer.load_layer("nonexistent")

        assert content is None

    def test_compose_with_missing_layer(self, layers_dir):
        """Test composition skips missing layers gracefully."""
        composer = PromptComposer(layers_dir)
        composed = composer.compose(["01_identity", "nonexistent", "02_tools"])

        assert "I am CODEXA" in composed
        assert "Available tools" in composed


class TestActualPromptLayers:
    """Tests for actual prompt layer files in the project."""

    @pytest.mark.skipif(
        not LAYERS_DIR.exists(),
        reason="Prompt layers directory not found"
    )
    def test_layers_directory_exists(self):
        """Test that layers directory exists."""
        assert LAYERS_DIR.exists()
        assert LAYERS_DIR.is_dir()

    @pytest.mark.skipif(
        not LAYERS_DIR.exists(),
        reason="Prompt layers directory not found"
    )
    def test_has_identity_layer(self):
        """Test that identity layer exists."""
        identity_layer = LAYERS_DIR / "01_identity_layer.md"
        assert identity_layer.exists(), "Missing 01_identity_layer.md"

    @pytest.mark.skipif(
        not LAYERS_DIR.exists(),
        reason="Prompt layers directory not found"
    )
    def test_has_code_conventions_layer(self):
        """Test that code conventions layer exists."""
        code_layer = LAYERS_DIR / "05_code_conventions.md"
        assert code_layer.exists(), "Missing 05_code_conventions.md"

    @pytest.mark.skipif(
        not LAYERS_DIR.exists(),
        reason="Prompt layers directory not found"
    )
    def test_has_design_system_layer(self):
        """Test that design system layer exists."""
        design_layer = LAYERS_DIR / "06_design_system.md"
        assert design_layer.exists(), "Missing 06_design_system.md"

    @pytest.mark.skipif(
        not LAYERS_DIR.exists(),
        reason="Prompt layers directory not found"
    )
    def test_all_layers_have_valid_structure(self):
        """Test that all layer files have valid structure."""
        errors = []

        for layer_file in LAYERS_DIR.glob("*.md"):
            validator = PromptLayerValidator(layer_file)
            if validator.load():
                valid, layer_errors = validator.validate_structure()
                if not valid:
                    errors.extend([f"{layer_file.name}: {e}" for e in layer_errors])

        assert len(errors) == 0, f"Layer validation errors: {errors}"


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
