"""
Pytest configuration and shared fixtures for CODEXA tests
"""
import pytest
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data."""
    temp_dir = tempfile.mkdtemp(prefix="codexa_test_")
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(autouse=True)
def disable_git_operations(monkeypatch):
    """Disable git operations during testing to avoid side effects."""
    # Mock git operations to avoid committing during tests
    def mock_auto_commit(*args, **kwargs):
        return True

    # This would need to be imported from the actual module
    # monkeypatch.setattr("modules.utils.git_helper.GitHelper.auto_commit", mock_auto_commit)
    pass


@pytest.fixture
def sample_markdown():
    """Sample markdown content for testing."""
    return """# Test Document

## Section 1

This is a test document with some content.

## Section 2

- List item 1
- List item 2
- List item 3

## Code Example

```python
def hello():
    print("Hello, CODEXA!")
```
"""


@pytest.fixture
def sample_json():
    """Sample JSON data for testing."""
    return {
        "id": "test-001",
        "name": "Test Product",
        "price": 19.99,
        "category": "testing",
        "tags": ["test", "sample", "demo"]
    }


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "windows: mark test as Windows-specific"
    )
