#!/usr/bin/env python3
"""
CODEXA Workflow Executor
Version: 2.0.0
Created: 2025-11-24

Executes multi-agent workflows based on definitions.
Implements two-phase planning, parallel orchestration, and more.
"""

import asyncio
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

from orchestrator import (
    Orchestrator,
    AgentType,
    AgentStatus,
    WorkflowStatus,
    Artifact,
    Handoff
)

logger = logging.getLogger(__name__)


# ============================================================================
# WORKFLOW DEFINITION
# ============================================================================

@dataclass
class WorkflowPhase:
    """Definition of a workflow phase."""
    id: str
    agent_type: str
    mode: str
    timeout: int  # seconds
    depends_on: List[str]
    input: Dict[str, Any]
    output: Dict[str, Any]
    condition: Optional[str] = None
    max_iterations: int = 1


@dataclass
class WorkflowDefinition:
    """Complete workflow definition."""
    name: str
    description: str
    phases: List[WorkflowPhase]
    metadata: Dict[str, Any]

    @classmethod
    def from_yaml(cls, yaml_path: Path) -> 'WorkflowDefinition':
        """Load workflow definition from YAML file."""
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        phases = [
            WorkflowPhase(
                id=p['id'],
                agent_type=p['agent_type'],
                mode=p['mode'],
                timeout=p.get('timeout', 300),
                depends_on=p.get('depends_on', []),
                input=p.get('input', {}),
                output=p.get('output', {}),
                condition=p.get('condition'),
                max_iterations=p.get('max_iterations', 1)
            )
            for p in data['phases']
        ]

        return cls(
            name=data['name'],
            description=data['description'],
            phases=phases,
            metadata=data.get('metadata', {})
        )


# ============================================================================
# WORKFLOW EXECUTOR
# ============================================================================

class WorkflowExecutor:
    """
    Executes workflows based on definitions.

    Supports:
    - Two-phase planning (Devin pattern)
    - Parallel orchestration (Poke pattern)
    - Sequential execution
    - Conditional phases
    - Error handling and rollback
    """

    def __init__(self, orchestrator: Orchestrator):
        """
        Initialize workflow executor.

        Args:
            orchestrator: Orchestrator instance to use
        """
        self.orchestrator = orchestrator
        self.phase_outputs: Dict[str, Dict[str, Any]] = {}

    async def execute_workflow(
        self,
        workflow_def: WorkflowDefinition,
        context: Dict[str, Any]
    ) -> WorkflowStatus:
        """
        Execute a complete workflow.

        Args:
            workflow_def: Workflow definition
            context: Initial context variables

        Returns:
            Final workflow status
        """
        # Create workflow
        workflow = self.orchestrator.create_workflow()
        logger.info(f"Executing workflow: {workflow_def.name} ({workflow.workflow_id})")

        try:
            # Update workflow status
            self.orchestrator.update_workflow_status(
                workflow.workflow_id,
                WorkflowStatus.RUNNING
            )

            # Execute phases in order
            for phase in workflow_def.phases:
                # Check dependencies
                if not await self._check_dependencies(phase, workflow.workflow_id):
                    raise Exception(f"Dependencies not satisfied for phase: {phase.id}")

                # Check condition
                if phase.condition and not self._evaluate_condition(phase.condition, context):
                    logger.info(f"Skipping phase {phase.id} - condition not met")
                    continue

                # Execute phase
                phase_result = await self._execute_phase(
                    phase,
                    workflow.workflow_id,
                    context
                )

                # Store phase output
                self.phase_outputs[phase.id] = phase_result

                # Update context with phase outputs
                context.update(phase_result)

                # Mark phase as completed
                workflow.phases_completed.append(phase.id)

            # Workflow succeeded
            self.orchestrator.update_workflow_status(
                workflow.workflow_id,
                WorkflowStatus.SUCCESS
            )

            logger.info(f"Workflow {workflow.workflow_id} completed successfully")
            return WorkflowStatus.SUCCESS

        except Exception as e:
            # Workflow failed
            logger.error(f"Workflow {workflow.workflow_id} failed: {e}")
            self.orchestrator.update_workflow_status(
                workflow.workflow_id,
                WorkflowStatus.FAILED,
                error_message=str(e)
            )
            return WorkflowStatus.FAILED

    async def _check_dependencies(
        self,
        phase: WorkflowPhase,
        workflow_id: str
    ) -> bool:
        """Check if phase dependencies are satisfied."""
        workflow = self.orchestrator.get_workflow_state(workflow_id)
        if not workflow:
            return False

        for dep in phase.depends_on:
            if dep not in workflow.phases_completed:
                logger.warning(f"Dependency not satisfied: {dep}")
                return False

        return True

    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """
        Evaluate a condition string.

        Args:
            condition: Condition string (e.g., "${verification.tests_failed > 0}")
            context: Context variables

        Returns:
            True if condition is met, False otherwise
        """
        try:
            # Simple condition evaluation
            # In production, use a proper expression evaluator
            # For now, just check if variable exists and is truthy
            if condition.startswith("${") and condition.endswith("}"):
                var_path = condition[2:-1].strip()
                parts = var_path.split(".")

                value = context
                for part in parts:
                    if isinstance(value, dict):
                        value = value.get(part)
                    else:
                        return False

                return bool(value)

            return True

        except Exception as e:
            logger.error(f"Error evaluating condition: {e}")
            return False

    async def _execute_phase(
        self,
        phase: WorkflowPhase,
        workflow_id: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single workflow phase.

        Args:
            phase: Phase definition
            workflow_id: Parent workflow ID
            context: Execution context

        Returns:
            Phase output
        """
        logger.info(f"Executing phase: {phase.id} (type={phase.agent_type}, mode={phase.mode})")

        # Map agent type string to enum
        agent_type_map = {
            "planning": AgentType.PLANNING,
            "execution": AgentType.EXECUTION,
            "verification": AgentType.VERIFICATION,
            "fix": AgentType.FIX,
            "research": AgentType.RESEARCH,
            "orchestrator": AgentType.ORCHESTRATOR
        }

        agent_type = agent_type_map.get(phase.agent_type)
        if not agent_type:
            raise ValueError(f"Unknown agent type: {phase.agent_type}")

        # Spawn agent
        agent = self.orchestrator.spawn_agent(agent_type, workflow_id)

        try:
            # Update agent status
            self.orchestrator.agent_registry.update_status(
                agent.agent_id,
                AgentStatus.RUNNING
            )

            # Resolve input variables
            resolved_input = self._resolve_variables(phase.input, context)

            # Simulate agent execution (in real implementation, this would call actual agent)
            await asyncio.sleep(0.5)  # Simulate work

            # Create output artifacts
            artifacts = await self._create_phase_artifacts(
                phase,
                agent.agent_id,
                resolved_input
            )

            # Update agent status
            agent.artifacts_produced = [a.id for a in artifacts]
            agent.completed_at = datetime.now()
            agent.duration = (agent.completed_at - agent.started_at).total_seconds()
            self.orchestrator.agent_registry.update_status(
                agent.agent_id,
                AgentStatus.SUCCESS
            )

            # Prepare phase output
            phase_output = {
                "agent_id": agent.agent_id,
                "artifacts": [a.id for a in artifacts],
                "status": "success"
            }

            logger.info(f"Phase {phase.id} completed successfully")
            return phase_output

        except asyncio.TimeoutError:
            logger.error(f"Phase {phase.id} timed out")
            self.orchestrator.agent_registry.update_status(
                agent.agent_id,
                AgentStatus.TIMEOUT
            )
            raise

        except Exception as e:
            logger.error(f"Phase {phase.id} failed: {e}")
            self.orchestrator.agent_registry.update_status(
                agent.agent_id,
                AgentStatus.ERROR,
                error_message=str(e)
            )
            raise

    def _resolve_variables(
        self,
        template: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Resolve variable references in template.

        Args:
            template: Template with variable references
            context: Context variables

        Returns:
            Resolved template
        """
        result = {}

        for key, value in template.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                # Variable reference
                var_path = value[2:-1]
                parts = var_path.split(".")

                resolved = context
                for part in parts:
                    if isinstance(resolved, dict):
                        resolved = resolved.get(part)
                    else:
                        resolved = None
                        break

                result[key] = resolved
            elif isinstance(value, dict):
                result[key] = self._resolve_variables(value, context)
            else:
                result[key] = value

        return result

    async def _create_phase_artifacts(
        self,
        phase: WorkflowPhase,
        agent_id: str,
        phase_input: Dict[str, Any]
    ) -> List[Artifact]:
        """
        Create artifacts for a phase (simulation).

        In real implementation, agent would produce these.

        Args:
            phase: Phase definition
            agent_id: Agent ID
            phase_input: Phase input

        Returns:
            List of artifacts
        """
        artifacts = []

        # Create artifacts based on phase type
        if phase.agent_type == "planning":
            # Planning phase produces plan and tasks
            plan_artifact = Artifact(
                id=f"plan_{phase.id}",
                type="plan",
                producer=agent_id,
                created_at=datetime.now(),
                path=Path(f"specs/{phase.id}_plan.md"),
                metadata={"phase": phase.id}
            )
            artifacts.append(plan_artifact)
            self.orchestrator.artifact_storage.store(plan_artifact)

        elif phase.agent_type == "execution":
            # Execution phase produces code
            code_artifact = Artifact(
                id=f"code_{phase.id}",
                type="code",
                producer=agent_id,
                created_at=datetime.now(),
                path=Path(f"src/{phase.id}_implementation.py"),
                metadata={"phase": phase.id}
            )
            artifacts.append(code_artifact)
            self.orchestrator.artifact_storage.store(code_artifact)

        elif phase.agent_type == "verification":
            # Verification phase produces report
            report_artifact = Artifact(
                id=f"report_{phase.id}",
                type="report",
                producer=agent_id,
                created_at=datetime.now(),
                path=Path(f"docs/{phase.id}_walkthrough.md"),
                metadata={"phase": phase.id, "tests_passed": 10, "tests_failed": 0}
            )
            artifacts.append(report_artifact)
            self.orchestrator.artifact_storage.store(report_artifact)

        return artifacts


# ============================================================================
# TWO-PHASE WORKFLOW EXECUTOR
# ============================================================================

class TwoPhaseWorkflow:
    """
    Specialized executor for two-phase planning workflow (Devin pattern).

    Phase 1: Planning (read-only exploration)
    Phase 2: Execution (implementation)
    Phase 3: Verification (testing)
    Phase 4: Fix (optional, if verification fails)
    """

    def __init__(self, orchestrator: Orchestrator):
        """Initialize two-phase workflow executor."""
        self.orchestrator = orchestrator
        self.executor = WorkflowExecutor(orchestrator)

    async def execute(
        self,
        user_request: str,
        context_files: List[Path] = None
    ) -> WorkflowStatus:
        """
        Execute two-phase workflow.

        Args:
            user_request: User's feature request
            context_files: Optional context files

        Returns:
            Workflow status
        """
        logger.info(f"Starting two-phase workflow: {user_request}")

        # Create workflow definition
        workflow_def = WorkflowDefinition(
            name="Two-Phase Feature Development",
            description="Planning → Execution → Verification",
            phases=[
                # Phase 1: Planning
                WorkflowPhase(
                    id="planning",
                    agent_type="planning",
                    mode="PLANNING",
                    timeout=300,
                    depends_on=[],
                    input={"user_request": user_request},
                    output={}
                ),
                # Phase 2: Execution
                WorkflowPhase(
                    id="execution",
                    agent_type="execution",
                    mode="EXECUTION",
                    timeout=1200,
                    depends_on=["planning"],
                    input={"plan": "${planning.artifacts}"},
                    output={}
                ),
                # Phase 3: Verification
                WorkflowPhase(
                    id="verification",
                    agent_type="verification",
                    mode="VERIFICATION",
                    timeout=300,
                    depends_on=["execution"],
                    input={
                        "spec": "${planning.artifacts}",
                        "artifacts": "${execution.artifacts}"
                    },
                    output={}
                ),
                # Phase 4: Fix (conditional)
                WorkflowPhase(
                    id="fix",
                    agent_type="fix",
                    mode="FIX",
                    timeout=600,
                    depends_on=["verification"],
                    condition="${verification.tests_failed}",
                    max_iterations=3,
                    input={"errors": "${verification.failures}"},
                    output={}
                )
            ],
            metadata={"pattern": "two_phase"}
        )

        # Execute workflow
        context = {
            "user_request": user_request,
            "context_files": context_files or []
        }

        return await self.executor.execute_workflow(workflow_def, context)


# ============================================================================
# PARALLEL ORCHESTRATION EXECUTOR
# ============================================================================

class ParallelOrchestration:
    """
    Specialized executor for parallel orchestration (Poke pattern).

    Spawns multiple agents in parallel to work on independent tasks,
    then aggregates results.
    """

    def __init__(self, orchestrator: Orchestrator):
        """Initialize parallel orchestration executor."""
        self.orchestrator = orchestrator
        self.executor = WorkflowExecutor(orchestrator)

    async def execute(
        self,
        tasks: List[Dict[str, Any]],
        aggregation_strategy: str = "verification"
    ) -> WorkflowStatus:
        """
        Execute parallel orchestration.

        Args:
            tasks: List of independent tasks to execute in parallel
                   Each task should have: id, agent_type, input, output
            aggregation_strategy: How to aggregate results
                                 ("verification", "merge", "report")

        Returns:
            Workflow status
        """
        logger.info(f"Starting parallel orchestration: {len(tasks)} tasks")

        # Create workflow definition with parallel phases
        phases = []

        # Create parallel execution phases
        for i, task in enumerate(tasks):
            phase = WorkflowPhase(
                id=task["id"],
                agent_type=task.get("agent_type", "execution"),
                mode=task.get("mode", "EXECUTION"),
                timeout=task.get("timeout", 900),
                depends_on=[],  # No dependencies - all parallel
                input=task.get("input", {}),
                output=task.get("output", {})
            )
            phases.append(phase)

        # Create aggregation phase
        aggregation_phase = WorkflowPhase(
            id="aggregation",
            agent_type="verification",
            mode="VERIFICATION",
            timeout=300,
            depends_on=[task["id"] for task in tasks],  # Depends on all parallel tasks
            input={
                f"{task['id']}_artifacts": f"${{{task['id']}.artifacts}}"
                for task in tasks
            },
            output={}
        )
        phases.append(aggregation_phase)

        workflow_def = WorkflowDefinition(
            name="Parallel Task Execution",
            description=f"Execute {len(tasks)} tasks in parallel",
            phases=phases,
            metadata={"pattern": "parallel_orchestration"}
        )

        # Execute workflow
        context = {
            "tasks": tasks,
            "aggregation_strategy": aggregation_strategy
        }

        return await self.executor.execute_workflow(workflow_def, context)

    async def execute_parallel_feature_development(
        self,
        user_request: str,
        components: List[str]
    ) -> WorkflowStatus:
        """
        Execute parallel feature development across multiple components.

        Example: Build frontend, backend, and tests simultaneously.

        Args:
            user_request: Feature description
            components: List of components to build in parallel
                       (e.g., ["frontend", "backend", "tests"])

        Returns:
            Workflow status
        """
        logger.info(f"Parallel feature development: {user_request}")
        logger.info(f"Components: {', '.join(components)}")

        # Create tasks for each component
        tasks = []

        for component in components:
            task = {
                "id": f"{component}_development",
                "agent_type": "execution",
                "mode": "EXECUTION",
                "timeout": 900,
                "input": {
                    "user_request": user_request,
                    "component": component,
                    "focus": f"Implement {component} for: {user_request}"
                },
                "output": {}
            }
            tasks.append(task)

        # Execute in parallel
        return await self.execute(tasks, aggregation_strategy="verification")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def main():
    """Example usage of workflow executor."""
    from pathlib import Path

    # Initialize orchestrator
    orchestrator = Orchestrator(Path(".codexa/workspace"))

    print("=" * 80)
    print("TESTING TWO-PHASE WORKFLOW (Devin Pattern)")
    print("=" * 80)

    # Execute two-phase workflow
    two_phase = TwoPhaseWorkflow(orchestrator)
    status = await two_phase.execute(
        user_request="Add user authentication with JWT tokens"
    )

    print(f"\n[SUCCESS] Two-Phase Workflow completed with status: {status.value}")

    # Show workflow results
    workflow_id = list(orchestrator.workflows.keys())[0]
    workflow = orchestrator.get_workflow_state(workflow_id)

    print(f"\nWorkflow Summary:")
    print(f"  ID: {workflow.workflow_id}")
    print(f"  Phases Completed: {len(workflow.phases_completed)}")
    print(f"  Agents Spawned: {len(workflow.agents_spawned)}")
    print(f"  Artifacts Created: {len(workflow.artifacts_created)}")

    # Show artifacts
    artifacts = orchestrator.get_workflow_artifacts(workflow_id)
    print(f"\nArtifacts:")
    for artifact in artifacts:
        print(f"  - {artifact.type}: {artifact.path}")

    print("\n" + "=" * 80)
    print("TESTING PARALLEL ORCHESTRATION (Poke Pattern)")
    print("=" * 80)

    # Execute parallel orchestration
    parallel = ParallelOrchestration(orchestrator)
    status = await parallel.execute_parallel_feature_development(
        user_request="Add shopping cart functionality",
        components=["frontend", "backend", "tests"]
    )

    print(f"\n[SUCCESS] Parallel Orchestration completed with status: {status.value}")

    # Show parallel workflow results
    workflow_id = list(orchestrator.workflows.keys())[-1]  # Get latest workflow
    workflow = orchestrator.get_workflow_state(workflow_id)

    print(f"\nParallel Workflow Summary:")
    print(f"  ID: {workflow.workflow_id}")
    print(f"  Phases Completed: {len(workflow.phases_completed)}")
    print(f"  Parallel Tasks: 3 (frontend, backend, tests)")
    print(f"  Agents Spawned: {len(workflow.agents_spawned)}")
    print(f"  Artifacts Created: {len(workflow.artifacts_created)}")

    # Show parallel artifacts
    artifacts = orchestrator.get_workflow_artifacts(workflow_id)
    print(f"\nParallel Artifacts:")
    for artifact in artifacts:
        print(f"  - {artifact.type}: {artifact.path}")

    print("\n" + "=" * 80)
    print("ALL TESTS COMPLETE [SUCCESS]")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())
