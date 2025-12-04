"""
ADW Workflow System Tests
Tests for CODEXA ADW (Agentic Developer Workflow) specifications.
"""

import pytest
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
import re
import json


class WorkflowPhaseStatus(Enum):
    """Status of a workflow phase."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class WorkflowPhase:
    """Represents a single phase in an ADW workflow."""
    phase_id: str
    phase_name: str
    description: str
    duration: Optional[str] = None
    agent: Optional[str] = None
    status: WorkflowPhaseStatus = WorkflowPhaseStatus.PENDING

    def start(self):
        self.status = WorkflowPhaseStatus.IN_PROGRESS

    def complete(self):
        self.status = WorkflowPhaseStatus.COMPLETED

    def fail(self):
        self.status = WorkflowPhaseStatus.FAILED

    def skip(self):
        self.status = WorkflowPhaseStatus.SKIPPED


@dataclass
class ADWWorkflow:
    """
    Represents an ADW (Agentic Developer Workflow) specification.
    """
    workflow_id: str
    workflow_name: str
    version: str
    phases: list[WorkflowPhase] = field(default_factory=list)
    context_strategy: str = "full_history"
    failure_handling: str = "stop"
    v2_enhancements: dict = field(default_factory=dict)

    def add_phase(self, phase: WorkflowPhase):
        """Add a phase to the workflow."""
        self.phases.append(phase)

    def get_current_phase(self) -> Optional[WorkflowPhase]:
        """Get the currently active phase."""
        for phase in self.phases:
            if phase.status == WorkflowPhaseStatus.IN_PROGRESS:
                return phase
        return None

    def get_next_phase(self) -> Optional[WorkflowPhase]:
        """Get the next pending phase."""
        for phase in self.phases:
            if phase.status == WorkflowPhaseStatus.PENDING:
                return phase
        return None

    def is_complete(self) -> bool:
        """Check if all phases are complete."""
        return all(
            p.status in [WorkflowPhaseStatus.COMPLETED, WorkflowPhaseStatus.SKIPPED]
            for p in self.phases
        )

    def has_failed(self) -> bool:
        """Check if any phase has failed."""
        return any(p.status == WorkflowPhaseStatus.FAILED for p in self.phases)

    def get_progress(self) -> float:
        """Get workflow progress as percentage."""
        if not self.phases:
            return 0.0
        completed = sum(
            1 for p in self.phases
            if p.status in [WorkflowPhaseStatus.COMPLETED, WorkflowPhaseStatus.SKIPPED]
        )
        return (completed / len(self.phases)) * 100


class ADWParser:
    """Parser for ADW workflow markdown files."""

    def parse_file(self, file_path: Path) -> Optional[ADWWorkflow]:
        """Parse an ADW workflow file."""
        if not file_path.exists():
            return None

        content = file_path.read_text(encoding='utf-8')
        return self.parse_content(content)

    def parse_content(self, content: str) -> Optional[ADWWorkflow]:
        """Parse ADW workflow content."""
        # Extract JSON specification
        json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
        if not json_match:
            return None

        try:
            spec = json.loads(json_match.group(1))
        except json.JSONDecodeError:
            return None

        # Create workflow
        workflow = ADWWorkflow(
            workflow_id=spec.get("workflow_id", ""),
            workflow_name=spec.get("workflow_name", ""),
            version=spec.get("version", "1.0.0"),
            context_strategy=spec.get("context_strategy", "full_history"),
            failure_handling=spec.get("failure_handling", "stop"),
            v2_enhancements=spec.get("v2_enhancements", {})
        )

        # Add phases
        for phase_spec in spec.get("phases", []):
            phase = WorkflowPhase(
                phase_id=phase_spec.get("phase_id", ""),
                phase_name=phase_spec.get("phase_name", ""),
                description=phase_spec.get("description", ""),
                duration=phase_spec.get("duration"),
                agent=phase_spec.get("agent")
            )
            workflow.add_phase(phase)

        return workflow


class ADWValidator:
    """Validates ADW workflow specifications."""

    REQUIRED_FIELDS = ["workflow_id", "workflow_name", "version"]

    def validate(self, workflow: ADWWorkflow) -> tuple[bool, list[str]]:
        """Validate a workflow specification."""
        errors = []

        # Check required fields
        if not workflow.workflow_id:
            errors.append("Missing workflow_id")
        if not workflow.workflow_name:
            errors.append("Missing workflow_name")
        if not workflow.version:
            errors.append("Missing version")

        # Check has phases
        if not workflow.phases:
            errors.append("Workflow must have at least one phase")

        # Check phase IDs are unique
        phase_ids = [p.phase_id for p in workflow.phases]
        if len(phase_ids) != len(set(phase_ids)):
            errors.append("Phase IDs must be unique")

        # Check v2.0 requirements
        if workflow.version.startswith("2."):
            v2_errors = self._validate_v2_requirements(workflow)
            errors.extend(v2_errors)

        return len(errors) == 0, errors

    def _validate_v2_requirements(self, workflow: ADWWorkflow) -> list[str]:
        """Validate v2.0 specific requirements."""
        errors = []

        # v2 should have enhancements block
        if not workflow.v2_enhancements:
            errors.append("v2.0 workflows should have v2_enhancements block")

        return errors


class TestWorkflowPhase:
    """Tests for WorkflowPhase."""

    def test_create_phase(self):
        """Test creating a workflow phase."""
        phase = WorkflowPhase(
            phase_id="phase_1",
            phase_name="Planning",
            description="Plan the implementation"
        )

        assert phase.phase_id == "phase_1"
        assert phase.status == WorkflowPhaseStatus.PENDING

    def test_phase_lifecycle(self):
        """Test phase status transitions."""
        phase = WorkflowPhase(
            phase_id="phase_1",
            phase_name="Test",
            description="Test phase"
        )

        assert phase.status == WorkflowPhaseStatus.PENDING

        phase.start()
        assert phase.status == WorkflowPhaseStatus.IN_PROGRESS

        phase.complete()
        assert phase.status == WorkflowPhaseStatus.COMPLETED

    def test_phase_failure(self):
        """Test phase failure."""
        phase = WorkflowPhase(
            phase_id="phase_1",
            phase_name="Test",
            description="Test phase"
        )

        phase.start()
        phase.fail()
        assert phase.status == WorkflowPhaseStatus.FAILED


class TestADWWorkflow:
    """Tests for ADWWorkflow."""

    def test_create_workflow(self):
        """Test creating a workflow."""
        workflow = ADWWorkflow(
            workflow_id="test_workflow",
            workflow_name="Test Workflow",
            version="2.0.0"
        )

        assert workflow.workflow_id == "test_workflow"
        assert len(workflow.phases) == 0

    def test_add_phases(self):
        """Test adding phases to workflow."""
        workflow = ADWWorkflow(
            workflow_id="test",
            workflow_name="Test",
            version="1.0.0"
        )

        workflow.add_phase(WorkflowPhase("p1", "Phase 1", "First"))
        workflow.add_phase(WorkflowPhase("p2", "Phase 2", "Second"))

        assert len(workflow.phases) == 2

    def test_get_current_phase(self):
        """Test getting current active phase."""
        workflow = ADWWorkflow(
            workflow_id="test",
            workflow_name="Test",
            version="1.0.0"
        )

        p1 = WorkflowPhase("p1", "Phase 1", "First")
        p2 = WorkflowPhase("p2", "Phase 2", "Second")

        workflow.add_phase(p1)
        workflow.add_phase(p2)

        # Initially no active phase
        assert workflow.get_current_phase() is None

        # Start first phase
        p1.start()
        assert workflow.get_current_phase() == p1

    def test_get_next_phase(self):
        """Test getting next pending phase."""
        workflow = ADWWorkflow(
            workflow_id="test",
            workflow_name="Test",
            version="1.0.0"
        )

        p1 = WorkflowPhase("p1", "Phase 1", "First")
        p2 = WorkflowPhase("p2", "Phase 2", "Second")

        workflow.add_phase(p1)
        workflow.add_phase(p2)

        # First pending is p1
        assert workflow.get_next_phase() == p1

        # After p1 completes, next is p2
        p1.complete()
        assert workflow.get_next_phase() == p2

    def test_workflow_completion(self):
        """Test workflow completion status."""
        workflow = ADWWorkflow(
            workflow_id="test",
            workflow_name="Test",
            version="1.0.0"
        )

        p1 = WorkflowPhase("p1", "Phase 1", "First")
        p2 = WorkflowPhase("p2", "Phase 2", "Second")

        workflow.add_phase(p1)
        workflow.add_phase(p2)

        assert not workflow.is_complete()

        p1.complete()
        assert not workflow.is_complete()

        p2.complete()
        assert workflow.is_complete()

    def test_workflow_progress(self):
        """Test workflow progress calculation."""
        workflow = ADWWorkflow(
            workflow_id="test",
            workflow_name="Test",
            version="1.0.0"
        )

        for i in range(4):
            workflow.add_phase(WorkflowPhase(f"p{i}", f"Phase {i}", f"Phase {i}"))

        assert workflow.get_progress() == 0.0

        workflow.phases[0].complete()
        assert workflow.get_progress() == 25.0

        workflow.phases[1].complete()
        assert workflow.get_progress() == 50.0


class TestADWParser:
    """Tests for ADWParser."""

    @pytest.fixture
    def parser(self):
        return ADWParser()

    @pytest.fixture
    def valid_adw_content(self):
        return '''# Test ADW Workflow

**Purpose**: Test workflow

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "test_workflow",
  "workflow_name": "Test Workflow",
  "version": "2.0.0",
  "context_strategy": "full_history",
  "failure_handling": "stop",

  "v2_enhancements": {
    "two_phase_planning": true,
    "task_boundaries": true
  },

  "phases": [
    {"phase_id": "phase_1", "phase_name": "Planning", "description": "Plan work"},
    {"phase_id": "phase_2", "phase_name": "Execution", "description": "Do work"}
  ]
}
```
'''

    def test_parse_valid_content(self, parser, valid_adw_content):
        """Test parsing valid ADW content."""
        workflow = parser.parse_content(valid_adw_content)

        assert workflow is not None
        assert workflow.workflow_id == "test_workflow"
        assert workflow.version == "2.0.0"
        assert len(workflow.phases) == 2

    def test_parse_extracts_v2_enhancements(self, parser, valid_adw_content):
        """Test v2 enhancements are extracted."""
        workflow = parser.parse_content(valid_adw_content)

        assert "two_phase_planning" in workflow.v2_enhancements
        assert workflow.v2_enhancements["two_phase_planning"] is True

    def test_parse_invalid_json(self, parser):
        """Test handling of invalid JSON."""
        content = '''# Bad ADW

```json
{ invalid json }
```
'''
        workflow = parser.parse_content(content)
        assert workflow is None

    def test_parse_missing_json(self, parser):
        """Test handling of missing JSON block."""
        content = '''# ADW without JSON

Just some text.
'''
        workflow = parser.parse_content(content)
        assert workflow is None


class TestADWValidator:
    """Tests for ADWValidator."""

    @pytest.fixture
    def validator(self):
        return ADWValidator()

    def test_validate_valid_workflow(self, validator):
        """Test validating a valid workflow."""
        workflow = ADWWorkflow(
            workflow_id="test",
            workflow_name="Test",
            version="1.0.0"
        )
        workflow.add_phase(WorkflowPhase("p1", "Phase", "Desc"))

        valid, errors = validator.validate(workflow)
        assert valid
        assert len(errors) == 0

    def test_validate_missing_id(self, validator):
        """Test detection of missing workflow_id."""
        workflow = ADWWorkflow(
            workflow_id="",
            workflow_name="Test",
            version="1.0.0"
        )

        valid, errors = validator.validate(workflow)
        assert not valid
        assert "Missing workflow_id" in errors

    def test_validate_no_phases(self, validator):
        """Test detection of workflow with no phases."""
        workflow = ADWWorkflow(
            workflow_id="test",
            workflow_name="Test",
            version="1.0.0"
        )

        valid, errors = validator.validate(workflow)
        assert not valid
        assert "Workflow must have at least one phase" in errors

    def test_validate_duplicate_phase_ids(self, validator):
        """Test detection of duplicate phase IDs."""
        workflow = ADWWorkflow(
            workflow_id="test",
            workflow_name="Test",
            version="1.0.0"
        )
        workflow.add_phase(WorkflowPhase("p1", "Phase 1", "First"))
        workflow.add_phase(WorkflowPhase("p1", "Phase 2", "Second"))  # Duplicate

        valid, errors = validator.validate(workflow)
        assert not valid
        assert "Phase IDs must be unique" in errors

    def test_validate_v2_requires_enhancements(self, validator):
        """Test v2 workflows should have enhancements."""
        workflow = ADWWorkflow(
            workflow_id="test",
            workflow_name="Test",
            version="2.0.0",
            v2_enhancements={}  # Empty
        )
        workflow.add_phase(WorkflowPhase("p1", "Phase", "Desc"))

        valid, errors = validator.validate(workflow)
        assert not valid
        assert any("v2_enhancements" in e for e in errors)


class TestActualADWFiles:
    """Tests for actual ADW workflow files."""

    WORKFLOWS_DIR = Path(__file__).parent.parent / "workflows"

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "workflows").exists(),
        reason="Workflows directory not found"
    )
    def test_workflows_directory_exists(self):
        """Test workflows directory exists."""
        assert self.WORKFLOWS_DIR.exists()

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "workflows").exists(),
        reason="Workflows directory not found"
    )
    def test_feature_development_adw_exists(self):
        """Test 201_ADW_FEATURE_DEVELOPMENT exists."""
        adw = self.WORKFLOWS_DIR / "201_ADW_FEATURE_DEVELOPMENT.md"
        assert adw.exists(), "Missing 201_ADW_FEATURE_DEVELOPMENT.md"

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "workflows").exists(),
        reason="Workflows directory not found"
    )
    def test_bug_fixing_adw_exists(self):
        """Test 202_ADW_BUG_FIXING exists."""
        adw = self.WORKFLOWS_DIR / "202_ADW_BUG_FIXING.md"
        assert adw.exists(), "Missing 202_ADW_BUG_FIXING.md"

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "workflows").exists(),
        reason="Workflows directory not found"
    )
    def test_parallel_orchestration_adw_exists(self):
        """Test 203_ADW_PARALLEL_ORCHESTRATION exists."""
        adw = self.WORKFLOWS_DIR / "203_ADW_PARALLEL_ORCHESTRATION.md"
        assert adw.exists(), "Missing 203_ADW_PARALLEL_ORCHESTRATION.md"

    @pytest.mark.skipif(
        not (Path(__file__).parent.parent / "workflows").exists(),
        reason="Workflows directory not found"
    )
    def test_all_adws_have_json_spec(self):
        """Test all ADW files have JSON specification."""
        parser = ADWParser()
        missing_spec = []

        for adw_file in self.WORKFLOWS_DIR.glob("*_ADW_*.md"):
            # Skip README files (documentation, not workflow specs)
            if adw_file.name.startswith("README"):
                continue
            workflow = parser.parse_file(adw_file)
            if workflow is None:
                missing_spec.append(adw_file.name)

        assert len(missing_spec) == 0, f"ADWs missing JSON spec: {missing_spec}"


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
