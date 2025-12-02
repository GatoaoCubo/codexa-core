"""
Unit tests for HOP Orchestrator
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from hop_orchestrator import HOPOrchestrator, BaseModule


class MockModule(BaseModule):
    """Mock module for testing."""

    def __init__(self):
        super().__init__("mock", "Mock module for testing")
        self.register_operation("test_op", self._test_op, "Test operation")

    def list_operations(self):
        return ["test_op"]

    def get_operation_info(self, operation):
        return {
            "description": "Test operation",
            "parameters": ["param1"]
        }

    def execute(self, operation, **kwargs):
        if operation == "test_op":
            return self._test_op(**kwargs)
        return {"success": False, "error": f"Unknown operation: {operation}"}

    def _test_op(self, **kwargs):
        return {"success": True, "data": kwargs}


@pytest.fixture
def orchestrator(tmp_path):
    """Create a test orchestrator."""
    return HOPOrchestrator(str(tmp_path))


@pytest.fixture
def mock_module():
    """Create a mock module."""
    return MockModule()


class TestHOPOrchestrator:
    """Test suite for HOP Orchestrator."""

    def test_initialization(self, orchestrator):
        """Test orchestrator initialization."""
        assert orchestrator.working_dir is not None
        assert len(orchestrator.modules) == 0
        assert orchestrator.readme_path.name == "README.md"

    def test_register_module(self, orchestrator, mock_module):
        """Test module registration."""
        orchestrator.register_module(mock_module)

        assert "mock" in orchestrator.modules
        assert orchestrator.get_module("mock") == mock_module

    def test_list_modules(self, orchestrator, mock_module):
        """Test listing modules."""
        orchestrator.register_module(mock_module)

        modules = orchestrator.list_modules()
        assert "mock" in modules
        assert len(modules) == 1

    def test_route_operation_success(self, orchestrator, mock_module):
        """Test successful operation routing."""
        orchestrator.register_module(mock_module)

        result = orchestrator.route_operation("mock", "test_op", param1="value1")

        assert result["success"] is True
        assert result["data"]["param1"] == "value1"

    def test_route_operation_module_not_found(self, orchestrator):
        """Test routing to non-existent module."""
        result = orchestrator.route_operation("nonexistent", "test_op")

        assert result["success"] is False
        assert "not found" in result["error"].lower()

    def test_route_operation_operation_not_found(self, orchestrator, mock_module):
        """Test routing to non-existent operation."""
        orchestrator.register_module(mock_module)

        result = orchestrator.route_operation("mock", "nonexistent_op")

        assert result["success"] is False
        assert "not found" in result["error"].lower()

    def test_introspect(self, orchestrator, mock_module):
        """Test system introspection."""
        orchestrator.register_module(mock_module)

        info = orchestrator.introspect()

        assert "capabilities" in info
        assert "mock" in info["capabilities"]
        assert "codexa_version" in info
        assert info["modules_count"] == 1

    def test_get_status(self, orchestrator, mock_module):
        """Test status retrieval."""
        orchestrator.register_module(mock_module)

        status = orchestrator.get_status()

        assert "working_dir" in status
        assert status["modules_registered"] == 1
        assert "mock" in status["modules"]
        assert "readme_exists" in status
        assert "git_repo" in status


class TestBaseModule:
    """Test suite for BaseModule abstract class."""

    def test_mock_module_operations(self, mock_module):
        """Test mock module operations."""
        assert "test_op" in mock_module.list_operations()

        info = mock_module.get_operation_info("test_op")
        assert info["description"] == "Test operation"

        result = mock_module.execute("test_op", key="value")
        assert result["success"] is True
        assert result["data"]["key"] == "value"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
