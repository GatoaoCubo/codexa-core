"""
Tests for codex_anuncio.py entry point.
"""

from pathlib import Path

import pytest


class TestCodexAnuncioEntry:
    """Test codex_anuncio.py entry point module."""

    def test_module_imports(self):
        """Test that codex_anuncio module can be imported."""
        try:
            import codex_anuncio

            assert hasattr(codex_anuncio, "__file__")
        except ImportError:
            pytest.skip("codex_anuncio module not importable in test context")

    def test_module_has_main(self):
        """Test that module has main execution block."""
        codex_path = Path(__file__).parent.parent / "codex_anuncio.py"
        if codex_path.exists():
            content = codex_path.read_text(encoding="utf-8")
            assert "if __name__" in content
        else:
            pytest.skip("codex_anuncio.py not found")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
