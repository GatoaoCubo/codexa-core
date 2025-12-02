"""
Tool Executor
Main engine for executing agent tools.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, Callable
from datetime import datetime
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ToolType(Enum):
    """Available tool types."""
    READ = "read"
    WRITE = "write"
    EDIT = "edit"
    GLOB = "glob"
    GREP = "grep"
    BASH = "bash"
    TASK = "task"
    WEBSEARCH = "websearch"
    WEBFETCH = "webfetch"


@dataclass
class ToolResult:
    """Result from tool execution."""
    tool_name: str
    success: bool
    output: Any
    error: Optional[str] = None
    duration_ms: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "tool_name": self.tool_name,
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata,
        }


class ToolError(Exception):
    """Base exception for tool errors."""
    pass


class PermissionError(ToolError):
    """Permission denied for tool operation."""
    pass


class ToolExecutor:
    """
    Main tool executor.

    Coordinates execution of all tools and enforces permissions.
    """

    def __init__(self, permission_manager=None):
        """
        Initialize tool executor.

        Args:
            permission_manager: Optional permission manager
        """
        self.permission_manager = permission_manager
        self.tools: Dict[str, Callable] = {}
        self.call_count = 0
        self.success_count = 0
        self.error_count = 0

    def register_tool(self, name: str, handler: Callable):
        """
        Register a tool handler.

        Args:
            name: Tool name
            handler: Tool handler function
        """
        self.tools[name] = handler
        logger.info(f"Registered tool: {name}")

    async def execute(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        agent_id: Optional[str] = None
    ) -> ToolResult:
        """
        Execute a tool.

        Args:
            tool_name: Tool to execute
            arguments: Tool arguments
            agent_id: Optional agent ID for permission checks

        Returns:
            Tool result

        Raises:
            PermissionError: If permission denied
            ToolError: If tool execution fails
        """
        import time
        start_time = time.time()

        self.call_count += 1

        try:
            # Check permissions
            if self.permission_manager:
                if not self.permission_manager.check_permission(agent_id, tool_name, arguments):
                    raise PermissionError(
                        f"Permission denied: {agent_id} cannot execute {tool_name}"
                    )

            # Get tool handler
            if tool_name not in self.tools:
                raise ToolError(f"Unknown tool: {tool_name}")

            handler = self.tools[tool_name]

            # Execute tool
            logger.info(f"Executing tool: {tool_name} with args: {list(arguments.keys())}")
            output = await handler(**arguments)

            # Calculate duration
            duration_ms = (time.time() - start_time) * 1000

            # Create result
            result = ToolResult(
                tool_name=tool_name,
                success=True,
                output=output,
                duration_ms=duration_ms,
                metadata={
                    "agent_id": agent_id,
                    "arguments": arguments,
                }
            )

            self.success_count += 1
            logger.info(f"Tool {tool_name} succeeded in {duration_ms:.0f}ms")

            return result

        except PermissionError as e:
            duration_ms = (time.time() - start_time) * 1000
            self.error_count += 1

            result = ToolResult(
                tool_name=tool_name,
                success=False,
                output=None,
                error=str(e),
                duration_ms=duration_ms,
            )

            logger.error(f"Permission denied for {tool_name}: {e}")
            return result

        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            self.error_count += 1

            result = ToolResult(
                tool_name=tool_name,
                success=False,
                output=None,
                error=str(e),
                duration_ms=duration_ms,
            )

            logger.error(f"Tool {tool_name} failed: {e}")
            return result

    def get_stats(self) -> Dict[str, Any]:
        """Get executor statistics."""
        return {
            "total_calls": self.call_count,
            "successful_calls": self.success_count,
            "failed_calls": self.error_count,
            "success_rate": self.success_count / self.call_count if self.call_count > 0 else 0,
            "tools_registered": len(self.tools),
        }
