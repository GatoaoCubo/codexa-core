#!/usr/bin/env python3
"""
CODEXA Orchestrator - Multi-Agent Coordination System
Version: 2.0.0
Created: 2025-11-24

Manages multi-agent workflows, coordination, and communication.
"""

import asyncio
import uuid
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================================================
# ENUMS
# ============================================================================

class AgentType(Enum):
    """Available agent types."""
    PLANNING = "planning"
    EXECUTION = "execution"
    VERIFICATION = "verification"
    FIX = "fix"
    RESEARCH = "research"
    ORCHESTRATOR = "orchestrator"


class AgentStatus(Enum):
    """Agent execution status."""
    IDLE = "idle"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    CANCELLED = "cancelled"


class WorkflowStatus(Enum):
    """Workflow execution status."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLBACK = "rollback"
    FAILED_FINAL = "failed_final"


class MessageType(Enum):
    """Message types for agent communication."""
    COMMAND = "command"
    STATUS = "status"
    RESULT = "result"
    ERROR = "error"
    HANDOFF = "handoff"


# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Artifact:
    """Represents a file or data artifact produced by an agent."""
    id: str
    type: str  # plan, code, report, data
    producer: str  # Agent ID
    created_at: datetime
    path: Path
    metadata: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "type": self.type,
            "producer": self.producer,
            "created_at": self.created_at.isoformat(),
            "path": str(self.path),
            "metadata": self.metadata,
            "dependencies": self.dependencies
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Artifact':
        """Create from dictionary."""
        return cls(
            id=data["id"],
            type=data["type"],
            producer=data["producer"],
            created_at=datetime.fromisoformat(data["created_at"]),
            path=Path(data["path"]),
            metadata=data.get("metadata", {}),
            dependencies=data.get("dependencies", [])
        )


@dataclass
class Message:
    """Message for agent communication."""
    type: MessageType
    sender: str
    receiver: str
    payload: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    correlation_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "type": self.type.value,
            "sender": self.sender,
            "receiver": self.receiver,
            "payload": self.payload,
            "timestamp": self.timestamp.isoformat(),
            "correlation_id": self.correlation_id
        }


@dataclass
class AgentState:
    """State of an agent execution."""
    agent_id: str
    agent_type: AgentType
    status: AgentStatus
    current_task: Optional[str] = None
    artifacts_produced: List[str] = field(default_factory=list)
    tools_used: List[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration: Optional[float] = None  # seconds
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "agent_type": self.agent_type.value,
            "status": self.status.value,
            "current_task": self.current_task,
            "artifacts_produced": self.artifacts_produced,
            "tools_used": self.tools_used,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "duration": self.duration,
            "metadata": self.metadata,
            "error_message": self.error_message
        }


@dataclass
class WorkflowState:
    """State of a workflow execution."""
    workflow_id: str
    status: WorkflowStatus
    current_phase: Optional[str] = None
    phases_completed: List[str] = field(default_factory=list)
    artifacts_created: List[str] = field(default_factory=list)
    agents_spawned: List[str] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "workflow_id": self.workflow_id,
            "status": self.status.value,
            "current_phase": self.current_phase,
            "phases_completed": self.phases_completed,
            "artifacts_created": self.artifacts_created,
            "agents_spawned": self.agents_spawned,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "metadata": self.metadata,
            "error_message": self.error_message
        }


@dataclass
class Handoff:
    """Agent handoff information."""
    from_agent: str
    to_agent: str
    artifacts: List[str]
    context: Dict[str, Any]
    instructions: str
    success_criteria: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "from_agent": self.from_agent,
            "to_agent": self.to_agent,
            "artifacts": self.artifacts,
            "context": self.context,
            "instructions": self.instructions,
            "success_criteria": self.success_criteria
        }


# ============================================================================
# ARTIFACT STORAGE
# ============================================================================

class ArtifactStorage:
    """Manages artifact storage and retrieval."""

    def __init__(self, base_path: Path):
        """
        Initialize artifact storage.

        Args:
            base_path: Base directory for artifacts
        """
        self.base_path = Path(base_path)
        self.artifacts: Dict[str, Artifact] = {}
        self.index_file = self.base_path / "artifacts_index.json"

        # Create directory
        self.base_path.mkdir(parents=True, exist_ok=True)

        # Load existing index
        self._load_index()

    def _load_index(self):
        """Load artifact index from disk."""
        if self.index_file.exists():
            try:
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.artifacts = {
                        aid: Artifact.from_dict(adata)
                        for aid, adata in data.items()
                    }
                logger.info(f"Loaded {len(self.artifacts)} artifacts from index")
            except Exception as e:
                logger.error(f"Failed to load artifact index: {e}")
                self.artifacts = {}

    def _save_index(self):
        """Save artifact index to disk."""
        try:
            data = {
                aid: artifact.to_dict()
                for aid, artifact in self.artifacts.items()
            }
            with open(self.index_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            logger.debug("Saved artifact index")
        except Exception as e:
            logger.error(f"Failed to save artifact index: {e}")

    def store(self, artifact: Artifact) -> str:
        """
        Store an artifact.

        Args:
            artifact: Artifact to store

        Returns:
            Artifact ID
        """
        self.artifacts[artifact.id] = artifact
        self._save_index()
        logger.info(f"Stored artifact: {artifact.id} at {artifact.path}")
        return artifact.id

    def get(self, artifact_id: str) -> Optional[Artifact]:
        """
        Get an artifact by ID.

        Args:
            artifact_id: Artifact ID

        Returns:
            Artifact if found, None otherwise
        """
        return self.artifacts.get(artifact_id)

    def get_by_producer(self, producer_id: str) -> List[Artifact]:
        """
        Get all artifacts produced by an agent.

        Args:
            producer_id: Agent ID

        Returns:
            List of artifacts
        """
        return [
            artifact for artifact in self.artifacts.values()
            if artifact.producer == producer_id
        ]

    def delete(self, artifact_id: str) -> bool:
        """
        Delete an artifact.

        Args:
            artifact_id: Artifact ID

        Returns:
            True if deleted, False if not found
        """
        if artifact_id in self.artifacts:
            artifact = self.artifacts[artifact_id]

            # Delete file if exists
            if artifact.path.exists():
                artifact.path.unlink()

            # Remove from index
            del self.artifacts[artifact_id]
            self._save_index()

            logger.info(f"Deleted artifact: {artifact_id}")
            return True

        return False


# ============================================================================
# MESSAGE BUS
# ============================================================================

class MessageBus:
    """Manages message passing between agents and orchestrator."""

    def __init__(self):
        """Initialize message bus."""
        self.messages: List[Message] = []
        self.subscribers: Dict[str, List[Callable]] = {}

    def publish(self, message: Message):
        """
        Publish a message to the bus.

        Args:
            message: Message to publish
        """
        self.messages.append(message)
        logger.debug(f"Published message: {message.type.value} from {message.sender} to {message.receiver}")

        # Notify subscribers
        if message.receiver in self.subscribers:
            for callback in self.subscribers[message.receiver]:
                try:
                    callback(message)
                except Exception as e:
                    logger.error(f"Error in message subscriber: {e}")

    def subscribe(self, agent_id: str, callback: Callable):
        """
        Subscribe to messages for an agent.

        Args:
            agent_id: Agent ID to subscribe for
            callback: Callback function to call when message arrives
        """
        if agent_id not in self.subscribers:
            self.subscribers[agent_id] = []
        self.subscribers[agent_id].append(callback)
        logger.debug(f"Subscribed callback for agent: {agent_id}")

    def get_messages(self, agent_id: str, message_type: Optional[MessageType] = None) -> List[Message]:
        """
        Get messages for an agent.

        Args:
            agent_id: Agent ID
            message_type: Optional filter by message type

        Returns:
            List of messages
        """
        messages = [m for m in self.messages if m.receiver == agent_id]

        if message_type:
            messages = [m for m in messages if m.type == message_type]

        return messages


# ============================================================================
# AGENT REGISTRY
# ============================================================================

class AgentRegistry:
    """Registry of available agents and their states."""

    def __init__(self):
        """Initialize agent registry."""
        self.agents: Dict[str, AgentState] = {}

    def register(self, agent_id: str, agent_type: AgentType) -> AgentState:
        """
        Register a new agent.

        Args:
            agent_id: Unique agent ID
            agent_type: Type of agent

        Returns:
            Agent state
        """
        state = AgentState(
            agent_id=agent_id,
            agent_type=agent_type,
            status=AgentStatus.IDLE
        )
        self.agents[agent_id] = state
        logger.info(f"Registered agent: {agent_id} ({agent_type.value})")
        return state

    def get(self, agent_id: str) -> Optional[AgentState]:
        """Get agent state by ID."""
        return self.agents.get(agent_id)

    def update_status(self, agent_id: str, status: AgentStatus, error_message: Optional[str] = None):
        """Update agent status."""
        if agent_id in self.agents:
            self.agents[agent_id].status = status
            if error_message:
                self.agents[agent_id].error_message = error_message
            logger.info(f"Agent {agent_id} status updated: {status.value}")

    def get_by_type(self, agent_type: AgentType) -> List[AgentState]:
        """Get all agents of a specific type."""
        return [
            state for state in self.agents.values()
            if state.agent_type == agent_type
        ]

    def get_active(self) -> List[AgentState]:
        """Get all currently running agents."""
        return [
            state for state in self.agents.values()
            if state.status == AgentStatus.RUNNING
        ]


# ============================================================================
# MAIN ORCHESTRATOR
# ============================================================================

class Orchestrator:
    """
    Main orchestrator for multi-agent workflows.

    Coordinates agent execution, manages state, handles communication.
    """

    def __init__(self, workspace_path: Path):
        """
        Initialize orchestrator.

        Args:
            workspace_path: Path to workspace directory
        """
        self.workspace_path = Path(workspace_path)
        self.artifacts_path = self.workspace_path / "artifacts"
        self.logs_path = self.workspace_path / "logs"
        self.workflows_path = self.workspace_path / "workflows"

        # Create directories
        for path in [self.artifacts_path, self.logs_path, self.workflows_path]:
            path.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.artifact_storage = ArtifactStorage(self.artifacts_path)
        self.message_bus = MessageBus()
        self.agent_registry = AgentRegistry()

        # Workflow tracking
        self.workflows: Dict[str, WorkflowState] = {}

        logger.info(f"Orchestrator initialized at {workspace_path}")

    def create_workflow(self, workflow_id: Optional[str] = None) -> WorkflowState:
        """
        Create a new workflow.

        Args:
            workflow_id: Optional workflow ID (generated if not provided)

        Returns:
            Workflow state
        """
        if workflow_id is None:
            workflow_id = f"wf_{uuid.uuid4().hex[:8]}"

        state = WorkflowState(
            workflow_id=workflow_id,
            status=WorkflowStatus.PENDING,
            started_at=datetime.now()
        )

        self.workflows[workflow_id] = state
        logger.info(f"Created workflow: {workflow_id}")

        return state

    def spawn_agent(
        self,
        agent_type: AgentType,
        workflow_id: str,
        agent_id: Optional[str] = None
    ) -> AgentState:
        """
        Spawn a new agent for a workflow.

        Args:
            agent_type: Type of agent to spawn
            workflow_id: Parent workflow ID
            agent_id: Optional agent ID (generated if not provided)

        Returns:
            Agent state
        """
        if agent_id is None:
            agent_id = f"{agent_type.value}_{uuid.uuid4().hex[:8]}"

        # Register agent
        state = self.agent_registry.register(agent_id, agent_type)
        state.started_at = datetime.now()
        state.metadata["workflow_id"] = workflow_id

        # Update workflow
        if workflow_id in self.workflows:
            self.workflows[workflow_id].agents_spawned.append(agent_id)

        logger.info(f"Spawned {agent_type.value} agent: {agent_id} for workflow {workflow_id}")

        return state

    def execute_handoff(self, handoff: Handoff):
        """
        Execute a handoff between agents.

        Args:
            handoff: Handoff information
        """
        logger.info(f"Executing handoff: {handoff.from_agent} → {handoff.to_agent}")

        # Send handoff message
        message = Message(
            type=MessageType.HANDOFF,
            sender=handoff.from_agent,
            receiver=handoff.to_agent,
            payload=handoff.to_dict()
        )

        self.message_bus.publish(message)

    def update_workflow_status(
        self,
        workflow_id: str,
        status: WorkflowStatus,
        error_message: Optional[str] = None
    ):
        """Update workflow status."""
        if workflow_id in self.workflows:
            workflow = self.workflows[workflow_id]
            workflow.status = status

            if error_message:
                workflow.error_message = error_message

            if status in [WorkflowStatus.SUCCESS, WorkflowStatus.FAILED, WorkflowStatus.FAILED_FINAL]:
                workflow.completed_at = datetime.now()

            logger.info(f"Workflow {workflow_id} status updated: {status.value}")

            # Save workflow state
            self._save_workflow_state(workflow_id)

    def _save_workflow_state(self, workflow_id: str):
        """Save workflow state to disk."""
        if workflow_id not in self.workflows:
            return

        workflow = self.workflows[workflow_id]
        state_file = self.workflows_path / f"{workflow_id}_state.json"

        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(workflow.to_dict(), f, indent=2)
            logger.debug(f"Saved workflow state: {workflow_id}")
        except Exception as e:
            logger.error(f"Failed to save workflow state: {e}")

    def get_workflow_state(self, workflow_id: str) -> Optional[WorkflowState]:
        """Get workflow state by ID."""
        return self.workflows.get(workflow_id)

    def get_workflow_artifacts(self, workflow_id: str) -> List[Artifact]:
        """Get all artifacts created during a workflow."""
        if workflow_id not in self.workflows:
            return []

        workflow = self.workflows[workflow_id]
        artifacts = []

        for artifact_id in workflow.artifacts_created:
            artifact = self.artifact_storage.get(artifact_id)
            if artifact:
                artifacts.append(artifact)

        return artifacts


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

async def main():
    """Example usage of orchestrator."""
    # Initialize orchestrator
    orchestrator = Orchestrator(Path(".codexa/workspace"))

    # Create workflow
    workflow = orchestrator.create_workflow()
    print(f"Created workflow: {workflow.workflow_id}")

    # Spawn planning agent
    planning_agent = orchestrator.spawn_agent(
        AgentType.PLANNING,
        workflow.workflow_id
    )
    print(f"Spawned planning agent: {planning_agent.agent_id}")

    # Simulate agent producing an artifact
    artifact = Artifact(
        id=f"art_{uuid.uuid4().hex[:8]}",
        type="plan",
        producer=planning_agent.agent_id,
        created_at=datetime.now(),
        path=Path("specs/feature_plan.md"),
        metadata={"feature": "user_auth"}
    )
    orchestrator.artifact_storage.store(artifact)

    # Spawn execution agent
    execution_agent = orchestrator.spawn_agent(
        AgentType.EXECUTION,
        workflow.workflow_id
    )
    print(f"Spawned execution agent: {execution_agent.agent_id}")

    # Execute handoff
    handoff = Handoff(
        from_agent=planning_agent.agent_id,
        to_agent=execution_agent.agent_id,
        artifacts=[artifact.id],
        context={"feature": "user_auth"},
        instructions="Implement authentication according to plan",
        success_criteria=["All tests pass", "No security vulnerabilities"]
    )
    orchestrator.execute_handoff(handoff)

    # Update workflow status
    orchestrator.update_workflow_status(workflow.workflow_id, WorkflowStatus.RUNNING)

    print("\nOrchestrator example complete!")


if __name__ == "__main__":
    asyncio.run(main())
