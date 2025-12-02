#!/usr/bin/env python3
"""
CODEXA Task Boundary System
Version: 1.0.0
Created: 2025-11-24

Implements Cursor's task boundary pattern for clear progress communication.
Provides structured messages for mode transitions, task progress, and status updates.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional, Any
import time


class AgentMode(Enum):
    """Operating modes for CODEXA agents."""
    PLANNING = "PLANNING"
    EXECUTION = "EXECUTION"
    VERIFICATION = "VERIFICATION"
    FIX = "FIX"
    RESEARCH = "RESEARCH"
    ORCHESTRATION = "ORCHESTRATION"
    REVIEW = "REVIEW"


class TaskStatus(Enum):
    """Status of a task in a checklist."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class Task:
    """A single task in a task checklist."""
    id: int
    content: str
    active_form: str
    status: TaskStatus = TaskStatus.PENDING
    estimated_duration_min: Optional[int] = None
    actual_duration_min: Optional[int] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    dependencies: List[int] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class TaskProgress:
    """Progress tracking for a task list."""
    total_tasks: int
    completed_tasks: int
    in_progress_tasks: int
    failed_tasks: int
    files_created: int = 0
    files_modified: int = 0
    tests_added: int = 0
    lines_added: int = 0
    duration_minutes: int = 0

    @property
    def completion_percentage(self) -> int:
        """Calculate completion percentage."""
        if self.total_tasks == 0:
            return 0
        return int((self.completed_tasks / self.total_tasks) * 100)

    @property
    def remaining_tasks(self) -> int:
        """Calculate remaining tasks."""
        return self.total_tasks - self.completed_tasks - self.failed_tasks


class TaskBoundary:
    """
    Task Boundary System for progress communication.

    Implements Cursor's task boundary pattern with clear mode-aware messaging.
    """

    def __init__(
        self,
        mode: AgentMode,
        total_tasks: Optional[int] = None,
        workflow_name: Optional[str] = None
    ):
        """
        Initialize task boundary system.

        Args:
            mode: Current agent operating mode
            total_tasks: Total number of tasks (optional)
            workflow_name: Name of workflow/feature being worked on
        """
        self.mode = mode
        self.total_tasks = total_tasks or 0
        self.workflow_name = workflow_name or "Task"
        self.tasks: List[Task] = []
        self.started_at = datetime.now()
        self.files_created = 0
        self.files_modified = 0
        self.tests_added = 0
        self.lines_added = 0

    def add_task(
        self,
        content: str,
        active_form: str,
        estimated_duration_min: Optional[int] = None,
        dependencies: Optional[List[int]] = None,
        tags: Optional[List[str]] = None
    ) -> Task:
        """
        Add a new task to the checklist.

        Args:
            content: Task description (imperative form)
            active_form: Task description (present continuous form)
            estimated_duration_min: Estimated duration in minutes
            dependencies: List of task IDs this task depends on
            tags: Tags for categorization

        Returns:
            Created Task object
        """
        task = Task(
            id=len(self.tasks) + 1,
            content=content,
            active_form=active_form,
            estimated_duration_min=estimated_duration_min,
            dependencies=dependencies or [],
            tags=tags or []
        )
        self.tasks.append(task)
        self.total_tasks = len(self.tasks)
        return task

    def start_task(self, task_id: int) -> str:
        """
        Mark a task as started and generate task boundary message.

        Args:
            task_id: ID of task to start

        Returns:
            Formatted task boundary message
        """
        task = self._get_task(task_id)
        task.status = TaskStatus.IN_PROGRESS
        task.started_at = datetime.now()

        progress = self._calculate_progress()
        duration = self._elapsed_time()

        return self._format_task_boundary(
            task=task,
            progress=progress,
            duration=duration,
            action="starting"
        )

    def complete_task(
        self,
        task_id: int,
        files_created: int = 0,
        files_modified: int = 0,
        tests_added: int = 0,
        lines_added: int = 0
    ) -> str:
        """
        Mark a task as completed and generate completion message.

        Args:
            task_id: ID of task to complete
            files_created: Number of files created
            files_modified: Number of files modified
            tests_added: Number of tests added
            lines_added: Number of lines added

        Returns:
            Formatted task completion message
        """
        task = self._get_task(task_id)
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()

        if task.started_at:
            duration = (task.completed_at - task.started_at).total_seconds() / 60
            task.actual_duration_min = int(duration)

        # Update counters
        self.files_created += files_created
        self.files_modified += files_modified
        self.tests_added += tests_added
        self.lines_added += lines_added

        progress = self._calculate_progress()

        return self._format_task_completion(
            task=task,
            progress=progress,
            files_created=files_created,
            files_modified=files_modified,
            tests_added=tests_added
        )

    def fail_task(self, task_id: int, error_message: str) -> str:
        """
        Mark a task as failed.

        Args:
            task_id: ID of task that failed
            error_message: Error message describing failure

        Returns:
            Formatted failure message
        """
        task = self._get_task(task_id)
        task.status = TaskStatus.FAILED
        task.completed_at = datetime.now()
        task.error_message = error_message

        return self._format_task_failure(task, error_message)

    def block_task(self, task_id: int, reason: str) -> str:
        """
        Mark a task as blocked.

        Args:
            task_id: ID of task that is blocked
            reason: Reason for blocking

        Returns:
            Formatted blocked message
        """
        task = self._get_task(task_id)
        task.status = TaskStatus.BLOCKED

        return f"⏸️ Task {task_id}/{self.total_tasks} blocked: {task.content}\n   Reason: {reason}"

    def generate_progress_summary(self) -> str:
        """
        Generate comprehensive progress summary.

        Returns:
            Formatted progress summary
        """
        progress = self._calculate_progress()
        duration = self._elapsed_time()

        summary = [
            "📊 Progress Update:",
            f"   - Completed: {progress.completed_tasks} / {progress.total_tasks} tasks ({progress.completion_percentage}%)",
            f"   - Files created: {self.files_created}",
            f"   - Files modified: {self.files_modified}",
            f"   - Tests added: {self.tests_added}",
            f"   - Lines added: {self.lines_added}",
            f"   - Time elapsed: {duration}",
        ]

        # Add estimated remaining time
        if progress.completed_tasks > 0:
            avg_time_per_task = (datetime.now() - self.started_at).total_seconds() / 60 / progress.completed_tasks
            remaining_time = int(avg_time_per_task * progress.remaining_tasks)
            summary.append(f"   - Estimated remaining: {remaining_time} minutes")

        return "\n".join(summary)

    def change_mode(self, new_mode: AgentMode, reason: str) -> str:
        """
        Change operating mode and generate transition message.

        Args:
            new_mode: New mode to transition to
            reason: Reason for mode change

        Returns:
            Formatted mode transition message
        """
        old_mode = self.mode
        self.mode = new_mode

        return self._format_mode_transition(old_mode, new_mode, reason)

    def _get_task(self, task_id: int) -> Task:
        """Get task by ID."""
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError(f"Task {task_id} not found")

    def _calculate_progress(self) -> TaskProgress:
        """Calculate current progress statistics."""
        completed = sum(1 for t in self.tasks if t.status == TaskStatus.COMPLETED)
        in_progress = sum(1 for t in self.tasks if t.status == TaskStatus.IN_PROGRESS)
        failed = sum(1 for t in self.tasks if t.status == TaskStatus.FAILED)

        duration = int((datetime.now() - self.started_at).total_seconds() / 60)

        return TaskProgress(
            total_tasks=self.total_tasks,
            completed_tasks=completed,
            in_progress_tasks=in_progress,
            failed_tasks=failed,
            files_created=self.files_created,
            files_modified=self.files_modified,
            tests_added=self.tests_added,
            lines_added=self.lines_added,
            duration_minutes=duration
        )

    def _elapsed_time(self) -> str:
        """Format elapsed time as human-readable string."""
        delta = datetime.now() - self.started_at
        minutes = int(delta.total_seconds() / 60)

        if minutes < 60:
            return f"{minutes} minutes"
        else:
            hours = minutes // 60
            mins = minutes % 60
            return f"{hours}h {mins}min"

    def _format_task_boundary(
        self,
        task: Task,
        progress: TaskProgress,
        duration: str,
        action: str
    ) -> str:
        """Format task boundary message (starting new task)."""
        mode_emoji = self._get_mode_emoji()

        lines = [
            "═══════════════════════════════════════════",
            f"  MODE: {self.mode.value} {mode_emoji}",
            f"  TASK: {task.id}/{self.total_tasks} - {task.content}",
            f"  PROGRESS: {progress.completed_tasks} / {self.total_tasks} ({progress.completion_percentage}%)",
            f"  FILES: {self.files_created} created, {self.files_modified} modified",
            f"  DURATION: {duration} elapsed",
            "═══════════════════════════════════════════",
            "",
            f"{task.active_form}..."
        ]

        return "\n".join(lines)

    def _format_task_completion(
        self,
        task: Task,
        progress: TaskProgress,
        files_created: int,
        files_modified: int,
        tests_added: int
    ) -> str:
        """Format task completion message."""
        lines = [
            f"✅ Task {task.id}/{self.total_tasks} completed: {task.content}"
        ]

        # Add details about what was done
        details = []
        if files_created > 0:
            details.append(f"Created: {files_created} file(s)")
        if files_modified > 0:
            details.append(f"Modified: {files_modified} file(s)")
        if tests_added > 0:
            details.append(f"Tests: +{tests_added}")

        if details:
            lines.append("   - " + ", ".join(details))

        # Add duration if available
        if task.actual_duration_min:
            lines.append(f"   - Duration: {task.actual_duration_min} min")

        # Add next task info
        next_task = self._get_next_pending_task()
        if next_task:
            lines.append(f"   - Next: Task {next_task.id}/{self.total_tasks} - {next_task.content}")

        return "\n".join(lines)

    def _format_task_failure(self, task: Task, error_message: str) -> str:
        """Format task failure message."""
        return f"❌ Task {task.id}/{self.total_tasks} failed: {task.content}\n   Error: {error_message}"

    def _format_mode_transition(
        self,
        old_mode: AgentMode,
        new_mode: AgentMode,
        reason: str
    ) -> str:
        """Format mode transition message."""
        old_emoji = self._get_mode_emoji(old_mode)
        new_emoji = self._get_mode_emoji(new_mode)

        return f"Mode transition: {old_mode.value} {old_emoji} → {new_mode.value} {new_emoji}\nReason: {reason}"

    def _get_next_pending_task(self) -> Optional[Task]:
        """Get next pending task."""
        for task in self.tasks:
            if task.status == TaskStatus.PENDING:
                # Check if dependencies are met
                dependencies_met = all(
                    self._get_task(dep_id).status == TaskStatus.COMPLETED
                    for dep_id in task.dependencies
                )
                if dependencies_met:
                    return task
        return None

    def _get_mode_emoji(self, mode: Optional[AgentMode] = None) -> str:
        """Get emoji for operating mode."""
        m = mode or self.mode
        emoji_map = {
            AgentMode.PLANNING: "🔍",
            AgentMode.EXECUTION: "⚙️",
            AgentMode.VERIFICATION: "✅",
            AgentMode.FIX: "🔧",
            AgentMode.RESEARCH: "📚",
            AgentMode.ORCHESTRATION: "🎭",
            AgentMode.REVIEW: "🔍📋"
        }
        return emoji_map.get(m, "")


class TaskBoundaryBuilder:
    """
    Builder class for creating task boundaries with fluent API.

    Example:
        boundary = (TaskBoundaryBuilder()
            .with_mode(AgentMode.EXECUTION)
            .with_workflow_name("Add dark mode")
            .add_task("Install dependencies", "Installing dependencies", estimated_min=5)
            .add_task("Create component", "Creating component", estimated_min=20)
            .build())
    """

    def __init__(self):
        self._mode: Optional[AgentMode] = None
        self._workflow_name: Optional[str] = None
        self._tasks: List[Dict[str, Any]] = []

    def with_mode(self, mode: AgentMode) -> "TaskBoundaryBuilder":
        """Set the operating mode."""
        self._mode = mode
        return self

    def with_workflow_name(self, name: str) -> "TaskBoundaryBuilder":
        """Set the workflow name."""
        self._workflow_name = name
        return self

    def add_task(
        self,
        content: str,
        active_form: str,
        estimated_min: Optional[int] = None,
        dependencies: Optional[List[int]] = None,
        tags: Optional[List[str]] = None
    ) -> "TaskBoundaryBuilder":
        """Add a task to the boundary."""
        self._tasks.append({
            "content": content,
            "active_form": active_form,
            "estimated_min": estimated_min,
            "dependencies": dependencies,
            "tags": tags
        })
        return self

    def build(self) -> TaskBoundary:
        """Build the TaskBoundary instance."""
        if not self._mode:
            raise ValueError("Mode must be set")

        boundary = TaskBoundary(
            mode=self._mode,
            total_tasks=len(self._tasks),
            workflow_name=self._workflow_name
        )

        for task_data in self._tasks:
            boundary.add_task(
                content=task_data["content"],
                active_form=task_data["active_form"],
                estimated_duration_min=task_data["estimated_min"],
                dependencies=task_data["dependencies"],
                tags=task_data["tags"]
            )

        return boundary


def main():
    """Example usage of task boundary system."""
    # Example 1: Simple execution workflow
    boundary = (TaskBoundaryBuilder()
        .with_mode(AgentMode.EXECUTION)
        .with_workflow_name("Add dark mode")
        .add_task("Install dependencies", "Installing dependencies", estimated_min=5)
        .add_task("Create component", "Creating component", estimated_min=20)
        .add_task("Add styling", "Adding styling", estimated_min=15)
        .add_task("Add tests", "Adding tests", estimated_min=10)
        .build())

    # Start first task
    print(boundary.start_task(1))
    print()

    # Complete first task
    time.sleep(1)  # Simulate work
    print(boundary.complete_task(1, files_modified=1))
    print()

    # Start second task
    print(boundary.start_task(2))
    print()

    # Progress summary
    time.sleep(1)  # Simulate work
    print(boundary.generate_progress_summary())
    print()

    # Complete second task
    print(boundary.complete_task(2, files_created=1, lines_added=87))


if __name__ == "__main__":
    main()
