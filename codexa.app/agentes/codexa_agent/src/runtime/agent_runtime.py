"""
Agent Runtime
Main execution engine for CODEXA agents.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from pathlib import Path
from datetime import datetime
from enum import Enum
import logging
import json

from ..llm.provider import LLMProvider, Message, ToolCall, LLMResponse
from ..llm.cost_tracker import CostTracker
from ..tools.executor import ToolExecutor, ToolResult
from ..tools.permissions import PermissionManager, Permission

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent execution status."""
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING_TOOL = "executing_tool"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class AgentConfig:
    """
    Agent configuration.

    Defines how an agent should behave and what it has access to.
    """
    agent_id: str
    agent_type: str  # e.g., "planning", "execution", "verification"
    system_prompt: str
    llm_provider: LLMProvider
    tool_executor: ToolExecutor
    permission: Permission
    max_iterations: int = 50
    max_tool_calls_per_iteration: int = 10
    temperature: float = 0.7
    workspace_path: Optional[Path] = None


@dataclass
class AgentState:
    """
    Runtime state of an agent.

    Tracks the current execution state and history.
    """
    agent_id: str
    workflow_id: str
    status: AgentStatus = AgentStatus.IDLE
    conversation: List[Message] = field(default_factory=list)
    iteration: int = 0
    total_tool_calls: int = 0
    total_cost: float = 0.0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error: Optional[str] = None
    artifacts_created: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "workflow_id": self.workflow_id,
            "status": self.status.value,
            "iteration": self.iteration,
            "total_tool_calls": self.total_tool_calls,
            "total_cost": self.total_cost,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error": self.error,
            "artifacts_created": self.artifacts_created,
            "metadata": self.metadata,
        }


class AgentRuntime:
    """
    Agent runtime execution engine.

    Features:
    - LLM-based reasoning with tool calling
    - Tool execution with permission checking
    - Conversation history management
    - Cost tracking
    - State persistence
    - Iteration limits for safety
    """

    def __init__(
        self,
        config: AgentConfig,
        cost_tracker: Optional[CostTracker] = None,
        state_path: Optional[Path] = None
    ):
        """
        Initialize agent runtime.

        Args:
            config: Agent configuration
            cost_tracker: Optional cost tracker
            state_path: Optional path to persist state
        """
        self.config = config
        self.cost_tracker = cost_tracker
        self.state_path = state_path or Path(".codexa/agent_states")
        self.state_path.mkdir(parents=True, exist_ok=True)

        # Initialize state
        self.state: Optional[AgentState] = None

        logger.info(
            f"Initialized agent runtime: {config.agent_id} "
            f"(type={config.agent_type})"
        )

    async def run(
        self,
        task: str,
        workflow_id: str,
        initial_context: Optional[Dict[str, Any]] = None
    ) -> AgentState:
        """
        Run agent on a task.

        Args:
            task: Task description for the agent
            workflow_id: Workflow this agent belongs to
            initial_context: Optional initial context/artifacts

        Returns:
            Final agent state

        Raises:
            RuntimeError: If execution fails
        """
        # Initialize state
        self.state = AgentState(
            agent_id=self.config.agent_id,
            workflow_id=workflow_id,
            started_at=datetime.now()
        )

        # Add initial user message
        self.state.conversation.append(Message(
            role="user",
            content=task
        ))

        logger.info(
            f"[{self.config.agent_id}] Starting task: {task[:100]}..."
        )

        try:
            # Main agent loop
            while self.state.iteration < self.config.max_iterations:
                self.state.iteration += 1
                self.state.status = AgentStatus.THINKING

                logger.info(
                    f"[{self.config.agent_id}] Iteration {self.state.iteration}"
                )

                # Get LLM response
                response = await self._get_llm_response()

                # Track cost
                if self.cost_tracker:
                    self.cost_tracker.track_llm_call(
                        workflow_id=workflow_id,
                        agent_id=self.config.agent_id,
                        response=response
                    )
                self.state.total_cost += response.cost_usd

                # Add assistant message to conversation
                self.state.conversation.append(Message(
                    role="assistant",
                    content=response.content or "",
                    tool_calls=response.tool_calls
                ))

                # Check for tool calls
                if response.tool_calls:
                    # Execute tools
                    tool_results = await self._execute_tools(response.tool_calls)

                    # Add tool results to conversation
                    for result in tool_results:
                        self.state.conversation.append(Message(
                            role="tool",
                            content=json.dumps(result.to_dict()),
                            tool_call_id=result.metadata.get("tool_call_id")
                        ))

                    # Continue loop to let agent process results
                    continue

                else:
                    # No tool calls = agent is done
                    self.state.status = AgentStatus.COMPLETED
                    self.state.completed_at = datetime.now()

                    logger.info(
                        f"[{self.config.agent_id}] Completed: "
                        f"{self.state.iteration} iterations, "
                        f"${self.state.total_cost:.4f}"
                    )

                    self._save_state()
                    return self.state

            # Max iterations reached
            self.state.status = AgentStatus.BLOCKED
            self.state.error = f"Max iterations ({self.config.max_iterations}) reached"
            self.state.completed_at = datetime.now()

            logger.warning(
                f"[{self.config.agent_id}] Max iterations reached"
            )

            self._save_state()
            return self.state

        except Exception as e:
            self.state.status = AgentStatus.FAILED
            self.state.error = str(e)
            self.state.completed_at = datetime.now()

            logger.error(
                f"[{self.config.agent_id}] Failed: {e}",
                exc_info=True
            )

            self._save_state()
            raise RuntimeError(f"Agent execution failed: {e}") from e

    async def _get_llm_response(self) -> LLMResponse:
        """Get response from LLM provider."""
        # Prepare tool definitions
        tools = self._get_available_tools()

        # Call LLM
        response = await self.config.llm_provider.complete(
            messages=self.state.conversation,
            tools=tools,
            system=self.config.system_prompt,
            temperature=self.config.temperature
        )

        logger.debug(
            f"[{self.config.agent_id}] LLM response: "
            f"tokens={response.tokens_used}, "
            f"cost=${response.cost_usd:.4f}, "
            f"tool_calls={len(response.tool_calls)}"
        )

        return response

    async def _execute_tools(
        self,
        tool_calls: List[ToolCall]
    ) -> List[ToolResult]:
        """
        Execute tool calls.

        Args:
            tool_calls: List of tool calls from LLM

        Returns:
            List of tool results
        """
        self.state.status = AgentStatus.EXECUTING_TOOL

        # Limit tool calls per iteration
        if len(tool_calls) > self.config.max_tool_calls_per_iteration:
            logger.warning(
                f"[{self.config.agent_id}] Too many tool calls: "
                f"{len(tool_calls)} > {self.config.max_tool_calls_per_iteration}"
            )
            tool_calls = tool_calls[:self.config.max_tool_calls_per_iteration]

        results = []

        for tool_call in tool_calls:
            self.state.total_tool_calls += 1

            logger.info(
                f"[{self.config.agent_id}] Executing tool: {tool_call.name}"
            )

            try:
                # Execute tool through executor
                result = await self.config.tool_executor.execute(
                    tool_name=tool_call.name,
                    arguments=tool_call.arguments,
                    agent_id=self.config.agent_id
                )

                # Store tool_call_id in metadata for conversation tracking
                result.metadata["tool_call_id"] = tool_call.id

                results.append(result)

                logger.info(
                    f"[{self.config.agent_id}] Tool {tool_call.name}: "
                    f"{'success' if result.success else 'failed'}"
                )

            except Exception as e:
                logger.error(
                    f"[{self.config.agent_id}] Tool {tool_call.name} error: {e}"
                )

                # Create error result
                error_result = ToolResult(
                    tool_name=tool_call.name,
                    success=False,
                    output=None,
                    error=str(e),
                    metadata={"tool_call_id": tool_call.id}
                )
                results.append(error_result)

        return results

    def _get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions available to this agent.

        Returns JSON schema for tools based on agent permissions.
        """
        tools = []
        permission = self.config.permission

        # Read tool
        if permission.allows_tool("read"):
            tools.append({
                "name": "read",
                "description": "Read contents of a file",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to file to read"
                        },
                        "offset": {
                            "type": "integer",
                            "description": "Optional line offset to start reading from"
                        },
                        "limit": {
                            "type": "integer",
                            "description": "Optional number of lines to read"
                        }
                    },
                    "required": ["file_path"]
                }
            })

        # Write tool
        if permission.allows_tool("write"):
            tools.append({
                "name": "write",
                "description": "Write content to a file (overwrites existing)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to file to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to file"
                        }
                    },
                    "required": ["file_path", "content"]
                }
            })

        # Edit tool
        if permission.allows_tool("edit"):
            tools.append({
                "name": "edit",
                "description": "Edit file by replacing text",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to file to edit"
                        },
                        "old_string": {
                            "type": "string",
                            "description": "Text to find"
                        },
                        "new_string": {
                            "type": "string",
                            "description": "Text to replace with"
                        },
                        "replace_all": {
                            "type": "boolean",
                            "description": "Replace all occurrences (default: false)"
                        }
                    },
                    "required": ["file_path", "old_string", "new_string"]
                }
            })

        # Glob tool
        if permission.allows_tool("glob"):
            tools.append({
                "name": "glob",
                "description": "Find files matching a glob pattern",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Glob pattern (e.g., '**/*.py')"
                        },
                        "path": {
                            "type": "string",
                            "description": "Optional directory to search in"
                        }
                    },
                    "required": ["pattern"]
                }
            })

        # Grep tool
        if permission.allows_tool("grep"):
            tools.append({
                "name": "grep",
                "description": "Search for pattern in files",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Regex pattern to search for"
                        },
                        "path": {
                            "type": "string",
                            "description": "Optional directory/file to search in"
                        },
                        "output_mode": {
                            "type": "string",
                            "enum": ["files_with_matches", "content", "count"],
                            "description": "Output mode"
                        }
                    },
                    "required": ["pattern"]
                }
            })

        # Bash tool
        if permission.allows_tool("bash"):
            tools.append({
                "name": "bash",
                "description": "Execute bash command",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Command to execute"
                        },
                        "cwd": {
                            "type": "string",
                            "description": "Optional working directory"
                        },
                        "timeout": {
                            "type": "integer",
                            "description": "Timeout in seconds (default: 30)"
                        }
                    },
                    "required": ["command"]
                }
            })

        return tools

    def _save_state(self):
        """Save agent state to disk."""
        if not self.state:
            return

        state_file = self.state_path / f"{self.config.agent_id}_state.json"

        try:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(self.state.to_dict(), f, indent=2)

            logger.debug(
                f"[{self.config.agent_id}] Saved state to {state_file}"
            )
        except Exception as e:
            logger.error(f"Failed to save agent state: {e}")

    def get_final_response(self) -> Optional[str]:
        """Get the final response from the agent."""
        if not self.state or not self.state.conversation:
            return None

        # Find last assistant message
        for msg in reversed(self.state.conversation):
            if msg.role == "assistant" and msg.content:
                return msg.content

        return None

    def get_state(self) -> Optional[AgentState]:
        """Get current agent state."""
        return self.state
