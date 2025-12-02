"""
Task Boundary System Tests
Tests for the CODEXA task boundary declarations and tracking.
"""

import pytest
from dataclasses import dataclass
from typing import Optional
from enum import Enum
from pathlib import Path


class AgentType(Enum):
    """Agent types with different access levels."""
    PLANNING = "planning_agent"
    EXECUTION = "execution_agent"
    VERIFICATION = "verification_agent"


class AccessLevel(Enum):
    """Access levels for task boundaries."""
    READ_ONLY = "read_only"
    WRITE = "write"
    EXECUTE = "execute"


@dataclass
class TaskBoundary:
    """
    Task boundary declaration for controlled operations.

    Implements the Claude Code pattern of explicit scope declarations.
    """
    name: str
    agent: AgentType
    access: AccessLevel
    scope: str
    files: list[str]
    rollback: Optional[str] = None
    _completed: bool = False
    _artifacts: list[str] = None

    def __post_init__(self):
        self._artifacts = []

    def validate(self) -> tuple[bool, list[str]]:
        """Validate task boundary configuration."""
        errors = []

        if not self.name:
            errors.append("Task boundary name is required")

        if not self.scope:
            errors.append("Task boundary scope is required")

        if self.access == AccessLevel.WRITE and self.agent == AgentType.PLANNING:
            errors.append("Planning agent cannot have write access")

        if self.access == AccessLevel.WRITE and not self.rollback:
            errors.append("Write access requires rollback strategy")

        return len(errors) == 0, errors

    def add_artifact(self, artifact_path: str):
        """Register an artifact generated within this boundary."""
        self._artifacts.append(artifact_path)

    def complete(self):
        """Mark the task boundary as completed."""
        self._completed = True

    @property
    def is_completed(self) -> bool:
        return self._completed

    @property
    def artifacts(self) -> list[str]:
        return self._artifacts.copy()

    def to_declaration(self) -> str:
        """Generate task boundary declaration string."""
        return f"""TASK_BOUNDARY: {self.name}
AGENT: {self.agent.value}
ACCESS: {self.access.value}
SCOPE: {self.scope}
FILES: {', '.join(self.files)}
ROLLBACK: {self.rollback or 'N/A'}"""


class TaskBoundaryManager:
    """
    Manages task boundaries throughout workflow execution.
    """

    def __init__(self):
        self._boundaries: list[TaskBoundary] = []
        self._current: Optional[TaskBoundary] = None

    def start(self, boundary: TaskBoundary) -> tuple[bool, list[str]]:
        """Start a new task boundary."""
        if self._current and not self._current.is_completed:
            return False, ["Cannot start new boundary while another is active"]

        valid, errors = boundary.validate()
        if not valid:
            return False, errors

        self._current = boundary
        self._boundaries.append(boundary)
        return True, []

    def complete_current(self) -> bool:
        """Complete the current task boundary."""
        if not self._current:
            return False
        self._current.complete()
        self._current = None
        return True

    def add_artifact(self, path: str) -> bool:
        """Add artifact to current boundary."""
        if not self._current:
            return False
        self._current.add_artifact(path)
        return True

    @property
    def current(self) -> Optional[TaskBoundary]:
        return self._current

    @property
    def history(self) -> list[TaskBoundary]:
        return self._boundaries.copy()

    def generate_report(self) -> dict:
        """Generate report of all task boundaries."""
        return {
            "total_boundaries": len(self._boundaries),
            "completed": sum(1 for b in self._boundaries if b.is_completed),
            "artifacts": sum(len(b.artifacts) for b in self._boundaries),
            "boundaries": [
                {
                    "name": b.name,
                    "agent": b.agent.value,
                    "access": b.access.value,
                    "completed": b.is_completed,
                    "artifacts": b.artifacts
                }
                for b in self._boundaries
            ]
        }


class TestTaskBoundary:
    """Tests for TaskBoundary class."""

    def test_create_valid_boundary(self):
        """Test creating a valid task boundary."""
        boundary = TaskBoundary(
            name="UPDATE_AUTH",
            agent=AgentType.EXECUTION,
            access=AccessLevel.WRITE,
            scope="Add JWT validation",
            files=["src/auth/validator.py"],
            rollback="git revert HEAD"
        )

        valid, errors = boundary.validate()
        assert valid
        assert len(errors) == 0

    def test_planning_agent_cannot_write(self):
        """Test that planning agent cannot have write access."""
        boundary = TaskBoundary(
            name="RESEARCH",
            agent=AgentType.PLANNING,
            access=AccessLevel.WRITE,  # Invalid
            scope="Research codebase",
            files=["src/"]
        )

        valid, errors = boundary.validate()
        assert not valid
        assert "Planning agent cannot have write access" in errors

    def test_write_requires_rollback(self):
        """Test that write access requires rollback strategy."""
        boundary = TaskBoundary(
            name="MODIFY",
            agent=AgentType.EXECUTION,
            access=AccessLevel.WRITE,
            scope="Modify file",
            files=["test.py"],
            rollback=None  # Missing rollback
        )

        valid, errors = boundary.validate()
        assert not valid
        assert "Write access requires rollback strategy" in errors

    def test_read_only_no_rollback_needed(self):
        """Test that read-only access doesn't need rollback."""
        boundary = TaskBoundary(
            name="ANALYZE",
            agent=AgentType.PLANNING,
            access=AccessLevel.READ_ONLY,
            scope="Analyze code patterns",
            files=["src/"]
        )

        valid, errors = boundary.validate()
        assert valid

    def test_artifact_tracking(self):
        """Test artifact tracking within boundary."""
        boundary = TaskBoundary(
            name="BUILD",
            agent=AgentType.EXECUTION,
            access=AccessLevel.WRITE,
            scope="Build component",
            files=["src/component.py"],
            rollback="git revert"
        )

        boundary.add_artifact("output/component.md")
        boundary.add_artifact("output/component.json")

        assert len(boundary.artifacts) == 2
        assert "output/component.md" in boundary.artifacts

    def test_completion_status(self):
        """Test boundary completion status."""
        boundary = TaskBoundary(
            name="TASK",
            agent=AgentType.EXECUTION,
            access=AccessLevel.WRITE,
            scope="Do task",
            files=["file.py"],
            rollback="git revert"
        )

        assert not boundary.is_completed
        boundary.complete()
        assert boundary.is_completed

    def test_declaration_generation(self):
        """Test declaration string generation."""
        boundary = TaskBoundary(
            name="UPDATE_CONFIG",
            agent=AgentType.EXECUTION,
            access=AccessLevel.WRITE,
            scope="Update configuration",
            files=["config.py", "settings.json"],
            rollback="git checkout -- config.py settings.json"
        )

        declaration = boundary.to_declaration()
        assert "TASK_BOUNDARY: UPDATE_CONFIG" in declaration
        assert "AGENT: execution_agent" in declaration
        assert "ACCESS: write" in declaration


class TestTaskBoundaryManager:
    """Tests for TaskBoundaryManager class."""

    def test_start_boundary(self):
        """Test starting a task boundary."""
        manager = TaskBoundaryManager()
        boundary = TaskBoundary(
            name="TASK1",
            agent=AgentType.EXECUTION,
            access=AccessLevel.WRITE,
            scope="First task",
            files=["file.py"],
            rollback="git revert"
        )

        success, errors = manager.start(boundary)
        assert success
        assert manager.current == boundary

    def test_cannot_start_while_active(self):
        """Test cannot start new boundary while one is active."""
        manager = TaskBoundaryManager()

        boundary1 = TaskBoundary(
            name="TASK1",
            agent=AgentType.EXECUTION,
            access=AccessLevel.WRITE,
            scope="First task",
            files=["file.py"],
            rollback="git revert"
        )

        boundary2 = TaskBoundary(
            name="TASK2",
            agent=AgentType.EXECUTION,
            access=AccessLevel.WRITE,
            scope="Second task",
            files=["file2.py"],
            rollback="git revert"
        )

        manager.start(boundary1)
        success, errors = manager.start(boundary2)

        assert not success
        assert "Cannot start new boundary while another is active" in errors

    def test_complete_allows_new_boundary(self):
        """Test completing boundary allows starting new one."""
        manager = TaskBoundaryManager()

        boundary1 = TaskBoundary(
            name="TASK1",
            agent=AgentType.EXECUTION,
            access=AccessLevel.WRITE,
            scope="First task",
            files=["file.py"],
            rollback="git revert"
        )

        boundary2 = TaskBoundary(
            name="TASK2",
            agent=AgentType.EXECUTION,
            access=AccessLevel.WRITE,
            scope="Second task",
            files=["file2.py"],
            rollback="git revert"
        )

        manager.start(boundary1)
        manager.complete_current()
        success, errors = manager.start(boundary2)

        assert success
        assert manager.current == boundary2

    def test_history_tracking(self):
        """Test boundary history tracking."""
        manager = TaskBoundaryManager()

        for i in range(3):
            boundary = TaskBoundary(
                name=f"TASK{i}",
                agent=AgentType.EXECUTION,
                access=AccessLevel.WRITE,
                scope=f"Task {i}",
                files=[f"file{i}.py"],
                rollback="git revert"
            )
            manager.start(boundary)
            manager.complete_current()

        assert len(manager.history) == 3
        assert all(b.is_completed for b in manager.history)

    def test_report_generation(self):
        """Test report generation."""
        manager = TaskBoundaryManager()

        boundary = TaskBoundary(
            name="TASK",
            agent=AgentType.EXECUTION,
            access=AccessLevel.WRITE,
            scope="Task",
            files=["file.py"],
            rollback="git revert"
        )

        manager.start(boundary)
        manager.add_artifact("output.md")
        manager.complete_current()

        report = manager.generate_report()

        assert report["total_boundaries"] == 1
        assert report["completed"] == 1
        assert report["artifacts"] == 1


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
