#!/usr/bin/env python3
"""
CODEXA Multi-Agent Orchestrator
Version: 1.0.0
Created: 2025-11-24

Orchestrates multiple specialized agents in parallel or sequence.
Implements Poke's parallel orchestration + Devin's two-phase workflow patterns.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
import json
import uuid


class OrchestrationPattern(Enum):
    """Available orchestration patterns."""
    SEQUENTIAL = "sequential"           # Phase 1 → Phase 2 → Phase 3
    PARALLEL = "parallel"               # All agents run simultaneously
    ITERATIVE = "iterative"             # Loop with verification gates
    HYBRID = "hybrid"                   # Mix of sequential and parallel


class AgentStatus(Enum):
    """Status of an agent in the orchestration."""
    PENDING = "pending"
    SPAWNED = "spawned"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class AgentDefinition:
    """Definition of an agent to spawn."""
    agent_id: str
    agent_type: str  # planning_agent, execution_agent, etc.
    mode: str  # PLANNING, EXECUTION, etc.
    task_description: str
    input_sources: List[str] = field(default_factory=list)  # $variable references
    output_artifacts: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # Agent IDs
    estimated_duration_min: Optional[int] = None
    max_retries: int = 3
    retry_count: int = 0


@dataclass
class AgentExecution:
    """Runtime information for an executing agent."""
    agent_def: AgentDefinition
    status: AgentStatus = AgentStatus.PENDING
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output_data: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    retry_count: int = 0


@dataclass
class OrchestrationPlan:
    """Complete orchestration plan."""
    workflow_id: str
    workflow_name: str
    pattern: OrchestrationPattern
    agents: List[AgentDefinition]
    created_at: datetime = field(default_factory=datetime.now)
    adw_path: Optional[Path] = None  # Agent Development Workspace path


class MultiAgentOrchestrator:
    """
    Multi-agent orchestration engine.

    Coordinates multiple specialized agents, handles $arguments chaining,
    monitors progress, and aggregates results.
    """

    def __init__(
        self,
        workflow_name: str,
        pattern: OrchestrationPattern,
        adw_base_path: Optional[Path] = None
    ):
        """
        Initialize orchestrator.

        Args:
            workflow_name: Name of the workflow being orchestrated
            pattern: Orchestration pattern to use
            adw_base_path: Base path for Agent Development Workspaces
        """
        self.workflow_id = self._generate_workflow_id()
        self.workflow_name = workflow_name
        self.pattern = pattern
        self.adw_base_path = adw_base_path or Path("agents")
        self.adw_path = self._create_adw()

        self.agents: List[AgentExecution] = []
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.context: Dict[str, Any] = {}  # Shared context for $arguments

    def _generate_workflow_id(self) -> str:
        """Generate unique workflow ID."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"adw_{timestamp}"

    def _create_adw(self) -> Path:
        """
        Create Agent Development Workspace directory.

        Returns:
            Path to ADW directory
        """
        adw_path = self.adw_base_path / self.workflow_id
        adw_path.mkdir(parents=True, exist_ok=True)
        return adw_path

    def add_agent(self, agent_def: AgentDefinition) -> None:
        """
        Add an agent to the orchestration.

        Args:
            agent_def: Agent definition
        """
        execution = AgentExecution(agent_def=agent_def)
        self.agents.append(execution)

    def execute(self) -> Dict[str, Any]:
        """
        Execute the orchestration.

        Returns:
            Orchestration results with status and outputs
        """
        self.started_at = datetime.now()

        try:
            if self.pattern == OrchestrationPattern.SEQUENTIAL:
                result = self._execute_sequential()
            elif self.pattern == OrchestrationPattern.PARALLEL:
                result = self._execute_parallel()
            elif self.pattern == OrchestrationPattern.ITERATIVE:
                result = self._execute_iterative()
            elif self.pattern == OrchestrationPattern.HYBRID:
                result = self._execute_hybrid()
            else:
                raise ValueError(f"Unknown pattern: {self.pattern}")

            self.completed_at = datetime.now()
            return result

        except Exception as e:
            self.completed_at = datetime.now()
            return {
                "status": "FAILED",
                "error": str(e),
                "workflow_id": self.workflow_id,
                "duration_minutes": self._elapsed_minutes()
            }

    def _execute_sequential(self) -> Dict[str, Any]:
        """
        Execute agents sequentially (Phase 1 → Phase 2 → Phase 3).

        Returns:
            Execution results
        """
        results = []

        for agent_exec in self.agents:
            # Check dependencies
            if not self._dependencies_met(agent_exec):
                agent_exec.status = AgentStatus.BLOCKED
                return {
                    "status": "BLOCKED",
                    "blocked_agent": agent_exec.agent_def.agent_id,
                    "reason": "Dependencies not met"
                }

            # Resolve input $arguments
            inputs = self._resolve_arguments(agent_exec.agent_def.input_sources)

            # Execute agent
            result = self._execute_agent(agent_exec, inputs)
            results.append(result)

            if result["status"] == "FAILED":
                # Try retry if available
                if agent_exec.retry_count < agent_exec.agent_def.max_retries:
                    agent_exec.retry_count += 1
                    result = self._execute_agent(agent_exec, inputs)

                if result["status"] == "FAILED":
                    return {
                        "status": "FAILED",
                        "failed_agent": agent_exec.agent_def.agent_id,
                        "error": result.get("error"),
                        "partial_results": results
                    }

            # Store outputs in context for next agents
            self._store_outputs(agent_exec)

        return {
            "status": "SUCCESS",
            "workflow_id": self.workflow_id,
            "pattern": "sequential",
            "agents_executed": len(results),
            "results": results,
            "duration_minutes": self._elapsed_minutes(),
            "adw_path": str(self.adw_path)
        }

    def _execute_parallel(self) -> Dict[str, Any]:
        """
        Execute agents in parallel (all simultaneously).

        Returns:
            Execution results
        """
        # In a real implementation, this would spawn agents truly in parallel
        # For now, we simulate by executing all without waiting for $arguments
        results = []

        for agent_exec in self.agents:
            # Resolve input $arguments
            inputs = self._resolve_arguments(agent_exec.agent_def.input_sources)

            # Execute agent
            result = self._execute_agent(agent_exec, inputs)
            results.append(result)

            # Store outputs immediately
            self._store_outputs(agent_exec)

        # Check if all succeeded
        failed_agents = [
            r for r in results
            if r["status"] == "FAILED"
        ]

        if failed_agents:
            return {
                "status": "PARTIAL",
                "workflow_id": self.workflow_id,
                "pattern": "parallel",
                "agents_executed": len(results),
                "agents_succeeded": len(results) - len(failed_agents),
                "agents_failed": len(failed_agents),
                "failed_agents": [a["agent_id"] for a in failed_agents],
                "results": results,
                "duration_minutes": self._elapsed_minutes()
            }

        return {
            "status": "SUCCESS",
            "workflow_id": self.workflow_id,
            "pattern": "parallel",
            "agents_executed": len(results),
            "results": results,
            "duration_minutes": self._elapsed_minutes(),
            "adw_path": str(self.adw_path)
        }

    def _execute_iterative(self) -> Dict[str, Any]:
        """
        Execute agents with verification loops (Plan → Execute → Verify → Fix loop).

        Returns:
            Execution results
        """
        results = []
        max_iterations = 3
        iteration = 0

        while iteration < max_iterations:
            iteration += 1

            # Execute all agents in sequence
            for agent_exec in self.agents:
                inputs = self._resolve_arguments(agent_exec.agent_def.input_sources)
                result = self._execute_agent(agent_exec, inputs)
                results.append(result)
                self._store_outputs(agent_exec)

            # Check if verification passed
            verification_passed = self._check_verification()

            if verification_passed:
                return {
                    "status": "SUCCESS",
                    "workflow_id": self.workflow_id,
                    "pattern": "iterative",
                    "iterations": iteration,
                    "agents_executed": len(results),
                    "results": results,
                    "duration_minutes": self._elapsed_minutes()
                }

            # If not passed and iterations remain, continue loop
            if iteration < max_iterations:
                # Would transition to FIX mode here
                continue

        return {
            "status": "FAILED",
            "workflow_id": self.workflow_id,
            "pattern": "iterative",
            "reason": "Max iterations reached without passing verification",
            "iterations": iteration,
            "results": results
        }

    def _execute_hybrid(self) -> Dict[str, Any]:
        """
        Execute hybrid pattern (mix of sequential and parallel).

        Returns:
            Execution results
        """
        # Hybrid would be defined by grouping agents into phases
        # Some phases sequential, some parallel
        # This is a placeholder for complex orchestrations
        return self._execute_sequential()

    def _execute_agent(
        self,
        agent_exec: AgentExecution,
        inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single agent.

        Args:
            agent_exec: Agent execution context
            inputs: Input arguments for agent

        Returns:
            Agent execution result
        """
        agent_def = agent_exec.agent_def

        agent_exec.status = AgentStatus.RUNNING
        agent_exec.started_at = datetime.now()

        try:
            # In real implementation, this would use the Task tool to spawn agent
            # For now, simulate execution
            print(f"[ORCHESTRATOR] Spawning {agent_def.agent_type} ({agent_def.agent_id})")
            print(f"  Mode: {agent_def.mode}")
            print(f"  Task: {agent_def.task_description}")
            print(f"  Inputs: {list(inputs.keys())}")

            # Simulate successful execution
            agent_exec.status = AgentStatus.COMPLETED
            agent_exec.completed_at = datetime.now()

            # Mock output data
            agent_exec.output_data = {
                "agent_id": agent_def.agent_id,
                "output_files": agent_def.output_artifacts,
                "status": "success"
            }

            return {
                "status": "SUCCESS",
                "agent_id": agent_def.agent_id,
                "agent_type": agent_def.agent_type,
                "duration_minutes": self._agent_elapsed_minutes(agent_exec),
                "outputs": agent_exec.output_data
            }

        except Exception as e:
            agent_exec.status = AgentStatus.FAILED
            agent_exec.error_message = str(e)
            agent_exec.completed_at = datetime.now()

            return {
                "status": "FAILED",
                "agent_id": agent_def.agent_id,
                "error": str(e)
            }

    def _dependencies_met(self, agent_exec: AgentExecution) -> bool:
        """
        Check if all dependencies for an agent are met.

        Args:
            agent_exec: Agent execution to check

        Returns:
            True if all dependencies completed successfully
        """
        for dep_id in agent_exec.agent_def.dependencies:
            dep_agent = self._get_agent(dep_id)
            if not dep_agent or dep_agent.status != AgentStatus.COMPLETED:
                return False
        return True

    def _resolve_arguments(self, input_sources: List[str]) -> Dict[str, Any]:
        """
        Resolve $argument references to actual values.

        Args:
            input_sources: List of $variable references

        Returns:
            Dictionary of resolved values
        """
        resolved = {}
        for source in input_sources:
            if source.startswith("$"):
                # Extract value from context
                key = source[1:]  # Remove $ prefix
                if key in self.context:
                    resolved[key] = self.context[key]
            else:
                # Literal value
                resolved[source] = source
        return resolved

    def _store_outputs(self, agent_exec: AgentExecution) -> None:
        """
        Store agent outputs in context for $arguments chaining.

        Args:
            agent_exec: Completed agent execution
        """
        agent_id = agent_exec.agent_def.agent_id
        self.context[agent_id] = agent_exec.output_data

        # Also store individual output artifacts
        for artifact in agent_exec.agent_def.output_artifacts:
            key = f"{agent_id}.{artifact}"
            self.context[key] = agent_exec.output_data.get(artifact)

    def _check_verification(self) -> bool:
        """
        Check if verification gates passed (for iterative pattern).

        Returns:
            True if all verification gates passed
        """
        # In real implementation, would check verification_agent output
        # For now, simulate
        return True

    def _get_agent(self, agent_id: str) -> Optional[AgentExecution]:
        """Get agent execution by ID."""
        for agent in self.agents:
            if agent.agent_def.agent_id == agent_id:
                return agent
        return None

    def _elapsed_minutes(self) -> int:
        """Calculate total elapsed time in minutes."""
        if not self.started_at:
            return 0
        end = self.completed_at or datetime.now()
        return int((end - self.started_at).total_seconds() / 60)

    def _agent_elapsed_minutes(self, agent_exec: AgentExecution) -> int:
        """Calculate agent elapsed time in minutes."""
        if not agent_exec.started_at:
            return 0
        end = agent_exec.completed_at or datetime.now()
        return int((end - agent_exec.started_at).total_seconds() / 60)

    def generate_orchestration_report(self) -> str:
        """
        Generate comprehensive orchestration report.

        Returns:
            Markdown-formatted report
        """
        report_lines = [
            f"# Orchestration Report: {self.workflow_name}",
            "",
            f"**Orchestration ID**: {self.workflow_id}",
            f"**Pattern**: {self.pattern.value}",
            f"**Status**: {self._overall_status()}",
            f"**Duration**: {self._elapsed_minutes()} minutes",
            f"**ADW Path**: {self.adw_path}",
            "",
            "---",
            "",
            "## Agent Execution Summary",
            ""
        ]

        # Table of agents
        report_lines.append("| Agent | Type | Status | Duration |")
        report_lines.append("|-------|------|--------|----------|")

        for agent_exec in self.agents:
            status_emoji = self._status_emoji(agent_exec.status)
            duration = self._agent_elapsed_minutes(agent_exec)
            report_lines.append(
                f"| {agent_exec.agent_def.agent_id} | "
                f"{agent_exec.agent_def.agent_type} | "
                f"{status_emoji} {agent_exec.status.value} | "
                f"{duration} min |"
            )

        report_lines.extend([
            "",
            "---",
            "",
            "## $arguments Chain",
            "",
            "```yaml"
        ])

        # Show $arguments flow
        for i, agent_exec in enumerate(self.agents):
            agent_def = agent_exec.agent_def
            report_lines.append(f"{agent_def.agent_id}:")
            if agent_def.input_sources:
                report_lines.append(f"  inputs: {agent_def.input_sources}")
            if agent_def.output_artifacts:
                report_lines.append(f"  outputs: {agent_def.output_artifacts}")
            if i < len(self.agents) - 1:
                report_lines.append("  ↓")

        report_lines.extend([
            "```",
            "",
            "---",
            "",
            "## Artifacts Generated",
            ""
        ])

        # List all output artifacts
        for agent_exec in self.agents:
            if agent_exec.agent_def.output_artifacts:
                report_lines.append(f"**{agent_exec.agent_def.agent_id}**:")
                for artifact in agent_exec.agent_def.output_artifacts:
                    report_lines.append(f"- {artifact}")
                report_lines.append("")

        report_lines.extend([
            "---",
            "",
            f"**Generated By**: Orchestrator v1.0.0",
            f"**Generated At**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ])

        return "\n".join(report_lines)

    def save_orchestration_report(self) -> Path:
        """
        Save orchestration report to ADW.

        Returns:
            Path to saved report
        """
        report = self.generate_orchestration_report()
        report_path = self.adw_path / "orchestration_report.md"

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)

        return report_path

    def _overall_status(self) -> str:
        """Determine overall orchestration status."""
        statuses = [a.status for a in self.agents]

        if all(s == AgentStatus.COMPLETED for s in statuses):
            return "✅ SUCCESS"
        elif any(s == AgentStatus.FAILED for s in statuses):
            completed = sum(1 for s in statuses if s == AgentStatus.COMPLETED)
            total = len(statuses)
            if completed > 0:
                return f"⚠️ PARTIAL ({completed}/{total} succeeded)"
            else:
                return "❌ FAILED"
        elif any(s == AgentStatus.RUNNING for s in statuses):
            return "🔄 RUNNING"
        else:
            return "⏳ PENDING"

    def _status_emoji(self, status: AgentStatus) -> str:
        """Get emoji for agent status."""
        emoji_map = {
            AgentStatus.PENDING: "⏳",
            AgentStatus.SPAWNED: "🚀",
            AgentStatus.RUNNING: "🔄",
            AgentStatus.COMPLETED: "✅",
            AgentStatus.FAILED: "❌",
            AgentStatus.BLOCKED: "⏸️"
        }
        return emoji_map.get(status, "")


class OrchestrationBuilder:
    """
    Builder for creating orchestration plans with fluent API.

    Example:
        orchestrator = (OrchestrationBuilder()
            .with_workflow_name("Add dark mode")
            .with_pattern(OrchestrationPattern.SEQUENTIAL)
            .add_agent("planning", "planning_agent", "PLANNING", "Plan dark mode implementation")
            .add_agent("execution", "execution_agent", "EXECUTION", "Execute dark mode", dependencies=["planning"])
            .build())
    """

    def __init__(self):
        self._workflow_name: Optional[str] = None
        self._pattern: Optional[OrchestrationPattern] = None
        self._agents: List[AgentDefinition] = []
        self._adw_base_path: Optional[Path] = None

    def with_workflow_name(self, name: str) -> "OrchestrationBuilder":
        """Set workflow name."""
        self._workflow_name = name
        return self

    def with_pattern(self, pattern: OrchestrationPattern) -> "OrchestrationBuilder":
        """Set orchestration pattern."""
        self._pattern = pattern
        return self

    def with_adw_path(self, path: Path) -> "OrchestrationBuilder":
        """Set ADW base path."""
        self._adw_base_path = path
        return self

    def add_agent(
        self,
        agent_id: str,
        agent_type: str,
        mode: str,
        task_description: str,
        input_sources: Optional[List[str]] = None,
        output_artifacts: Optional[List[str]] = None,
        dependencies: Optional[List[str]] = None,
        estimated_duration_min: Optional[int] = None
    ) -> "OrchestrationBuilder":
        """Add an agent to the orchestration."""
        agent_def = AgentDefinition(
            agent_id=agent_id,
            agent_type=agent_type,
            mode=mode,
            task_description=task_description,
            input_sources=input_sources or [],
            output_artifacts=output_artifacts or [],
            dependencies=dependencies or [],
            estimated_duration_min=estimated_duration_min
        )
        self._agents.append(agent_def)
        return self

    def build(self) -> MultiAgentOrchestrator:
        """Build the orchestrator."""
        if not self._workflow_name:
            raise ValueError("Workflow name must be set")
        if not self._pattern:
            raise ValueError("Orchestration pattern must be set")

        orchestrator = MultiAgentOrchestrator(
            workflow_name=self._workflow_name,
            pattern=self._pattern,
            adw_base_path=self._adw_base_path
        )

        for agent_def in self._agents:
            orchestrator.add_agent(agent_def)

        return orchestrator


def main():
    """Example usage of multi-agent orchestrator."""
    # Example: Two-phase workflow (Planning → Execution → Verification → Review)
    orchestrator = (OrchestrationBuilder()
        .with_workflow_name("Add dark mode feature")
        .with_pattern(OrchestrationPattern.SEQUENTIAL)
        .add_agent(
            agent_id="planning",
            agent_type="planning_agent",
            mode="PLANNING",
            task_description="Analyze codebase and plan dark mode implementation",
            output_artifacts=["implementation_plan.md", "task.md"],
            estimated_duration_min=60
        )
        .add_agent(
            agent_id="execution",
            agent_type="execution_agent",
            mode="EXECUTION",
            task_description="Execute dark mode implementation",
            input_sources=["$planning.implementation_plan", "$planning.task"],
            output_artifacts=["code_files", "tests", "execution_report.md"],
            dependencies=["planning"],
            estimated_duration_min=120
        )
        .add_agent(
            agent_id="verification",
            agent_type="verification_agent",
            mode="VERIFICATION",
            task_description="Verify implementation quality",
            input_sources=["$execution.code_files", "$execution.tests"],
            output_artifacts=["verification_report.md", "walkthrough.md"],
            dependencies=["execution"],
            estimated_duration_min=60
        )
        .add_agent(
            agent_id="review",
            agent_type="review_agent",
            mode="REVIEW",
            task_description="Review against specification",
            input_sources=["$execution.execution_report", "$verification.verification_report"],
            output_artifacts=["review_report.md"],
            dependencies=["verification"],
            estimated_duration_min=80
        )
        .build())

    print(f"Orchestration created: {orchestrator.workflow_id}")
    print(f"ADW path: {orchestrator.adw_path}")
    print(f"Pattern: {orchestrator.pattern.value}")
    print(f"Agents: {len(orchestrator.agents)}\n")

    # Execute orchestration
    result = orchestrator.execute()

    print(f"\nOrchestration status: {result['status']}")
    print(f"Duration: {result.get('duration_minutes', 0)} minutes")

    # Generate report
    report_path = orchestrator.save_orchestration_report()
    print(f"Report saved: {report_path}")


if __name__ == "__main__":
    main()
