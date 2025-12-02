"""
Permission System
Manages tool access permissions for agents.
"""

from dataclasses import dataclass, field
from typing import Dict, Set, List, Any, Optional, Callable
from pathlib import Path
from enum import Enum
import fnmatch
import logging

logger = logging.getLogger(__name__)


class PermissionLevel(Enum):
    """Permission levels for agents."""
    NONE = "none"           # No access
    READ_ONLY = "read_only"  # Can read but not modify
    WRITE = "write"          # Can read and write
    EXECUTE = "execute"      # Can execute commands
    ADMIN = "admin"          # Full access


@dataclass
class Permission:
    """
    Permission definition for an agent.

    Defines what tools an agent can use and under what constraints.
    """
    agent_id: str
    allowed_tools: Set[str] = field(default_factory=set)
    denied_tools: Set[str] = field(default_factory=set)
    allowed_paths: List[str] = field(default_factory=list)  # Glob patterns
    denied_paths: List[str] = field(default_factory=list)   # Glob patterns
    max_file_size: int = 10_000_000  # 10MB default
    permission_level: PermissionLevel = PermissionLevel.READ_ONLY
    custom_validators: Dict[str, Callable] = field(default_factory=dict)

    def allows_tool(self, tool_name: str) -> bool:
        """Check if tool is allowed."""
        # Explicit denial takes precedence
        if tool_name in self.denied_tools:
            return False

        # If allowed list is empty, allow all (except denied)
        if not self.allowed_tools:
            return True

        return tool_name in self.allowed_tools

    def allows_path(self, path: str) -> bool:
        """
        Check if path is allowed.

        Args:
            path: File path to check

        Returns:
            True if path is allowed
        """
        path_obj = Path(path)
        path_str = str(path_obj)

        # Check denied paths first
        for denied_pattern in self.denied_paths:
            if fnmatch.fnmatch(path_str, denied_pattern):
                return False

        # If no allowed patterns, allow all (except denied)
        if not self.allowed_paths:
            return True

        # Check allowed paths
        for allowed_pattern in self.allowed_paths:
            if fnmatch.fnmatch(path_str, allowed_pattern):
                return True

        return False


class PermissionManager:
    """
    Manages permissions for all agents.

    Features:
    - Per-agent tool access control
    - Path-based restrictions (glob patterns)
    - File size limits
    - Permission levels
    - Custom validators
    """

    def __init__(self, workspace_path: Optional[Path] = None):
        """
        Initialize permission manager.

        Args:
            workspace_path: Workspace root for path restrictions
        """
        self.workspace_path = workspace_path or Path.cwd()
        self.permissions: Dict[str, Permission] = {}
        self.default_permission: Optional[Permission] = None

    def register_agent(
        self,
        agent_id: str,
        permission: Permission
    ):
        """
        Register permissions for an agent.

        Args:
            agent_id: Agent identifier
            permission: Permission configuration
        """
        self.permissions[agent_id] = permission
        logger.info(
            f"Registered permissions for agent {agent_id}: "
            f"level={permission.permission_level.value}, "
            f"tools={len(permission.allowed_tools)}"
        )

    def set_default_permission(self, permission: Permission):
        """Set default permission for unregistered agents."""
        self.default_permission = permission
        logger.info("Set default permission policy")

    def check_permission(
        self,
        agent_id: Optional[str],
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> bool:
        """
        Check if agent has permission to execute tool.

        Args:
            agent_id: Agent identifier (None = anonymous)
            tool_name: Tool to execute
            arguments: Tool arguments

        Returns:
            True if allowed, False otherwise
        """
        # Get agent permission
        if agent_id and agent_id in self.permissions:
            permission = self.permissions[agent_id]
        elif self.default_permission:
            permission = self.default_permission
        else:
            # No permission defined = deny by default
            logger.warning(
                f"No permission defined for agent {agent_id}, denying {tool_name}"
            )
            return False

        # Check tool access
        if not permission.allows_tool(tool_name):
            logger.warning(
                f"Agent {agent_id} denied tool access: {tool_name}"
            )
            return False

        # Check permission level vs tool type
        if not self._check_tool_permission_level(tool_name, permission):
            logger.warning(
                f"Agent {agent_id} permission level insufficient for {tool_name}"
            )
            return False

        # Check path-based restrictions for file tools
        if tool_name in ['read', 'write', 'edit', 'glob', 'grep']:
            if not self._check_file_tool_permission(
                tool_name, arguments, permission
            ):
                return False

        # Check bash command restrictions
        if tool_name == 'bash':
            if not self._check_bash_permission(arguments, permission):
                return False

        # Run custom validators if defined
        if tool_name in permission.custom_validators:
            validator = permission.custom_validators[tool_name]
            try:
                if not validator(arguments):
                    logger.warning(
                        f"Custom validator denied {tool_name} for {agent_id}"
                    )
                    return False
            except Exception as e:
                logger.error(f"Custom validator error: {e}")
                return False

        return True

    def _check_tool_permission_level(
        self,
        tool_name: str,
        permission: Permission
    ) -> bool:
        """Check if permission level allows tool."""
        level = permission.permission_level

        # Read-only tools
        if tool_name in ['read', 'glob', 'grep']:
            return level != PermissionLevel.NONE

        # Write tools
        if tool_name in ['write', 'edit']:
            return level in [
                PermissionLevel.WRITE,
                PermissionLevel.EXECUTE,
                PermissionLevel.ADMIN
            ]

        # Execute tools
        if tool_name == 'bash':
            return level in [
                PermissionLevel.EXECUTE,
                PermissionLevel.ADMIN
            ]

        # Unknown tools require admin
        return level == PermissionLevel.ADMIN

    def _check_file_tool_permission(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        permission: Permission
    ) -> bool:
        """Check file tool path restrictions."""
        # Extract file path from arguments
        file_path = arguments.get('file_path') or arguments.get('path')

        if not file_path:
            # No path specified, allow
            return True

        # Resolve path
        path_obj = Path(file_path)
        if not path_obj.is_absolute():
            path_obj = self.workspace_path / path_obj

        path_str = str(path_obj)

        # Check if path is allowed
        if not permission.allows_path(path_str):
            logger.warning(
                f"Path denied: {path_str} (agent={permission.agent_id})"
            )
            return False

        # Check file size limits for write operations
        if tool_name in ['write', 'edit']:
            content = arguments.get('content', '')
            if isinstance(content, str):
                content_size = len(content.encode('utf-8'))
                if content_size > permission.max_file_size:
                    logger.warning(
                        f"File size {content_size} exceeds limit "
                        f"{permission.max_file_size}"
                    )
                    return False

        return True

    def _check_bash_permission(
        self,
        arguments: Dict[str, Any],
        permission: Permission
    ) -> bool:
        """Check bash command restrictions."""
        command = arguments.get('command', '')

        # Check working directory
        cwd = arguments.get('cwd')
        if cwd:
            if not permission.allows_path(str(Path(cwd))):
                logger.warning(f"Bash cwd denied: {cwd}")
                return False

        # Add more bash-specific checks here if needed
        # e.g., dangerous commands, network access, etc.

        return True

    def get_agent_permission(self, agent_id: str) -> Optional[Permission]:
        """Get permission for an agent."""
        return self.permissions.get(agent_id)

    def list_agents(self) -> List[str]:
        """List all registered agents."""
        return list(self.permissions.keys())

    def revoke_agent(self, agent_id: str):
        """Revoke all permissions for an agent."""
        if agent_id in self.permissions:
            del self.permissions[agent_id]
            logger.info(f"Revoked permissions for agent: {agent_id}")


# Predefined permission presets

def create_read_only_permission(agent_id: str, allowed_paths: List[str] = None) -> Permission:
    """Create read-only permission preset."""
    return Permission(
        agent_id=agent_id,
        allowed_tools={'read', 'glob', 'grep'},
        allowed_paths=allowed_paths or ['**/*'],
        permission_level=PermissionLevel.READ_ONLY
    )


def create_full_access_permission(agent_id: str) -> Permission:
    """Create full access permission preset."""
    return Permission(
        agent_id=agent_id,
        allowed_tools={'read', 'write', 'edit', 'glob', 'grep', 'bash'},
        allowed_paths=['**/*'],
        permission_level=PermissionLevel.ADMIN
    )


def create_sandboxed_permission(
    agent_id: str,
    sandbox_path: str
) -> Permission:
    """Create sandboxed permission (restricted to specific directory)."""
    return Permission(
        agent_id=agent_id,
        allowed_tools={'read', 'write', 'edit', 'glob', 'grep'},
        allowed_paths=[f"{sandbox_path}/**/*"],
        denied_paths=[
            "**/.git/**",
            "**/.env",
            "**/secrets/**",
            "**/*.key",
            "**/*.pem"
        ],
        permission_level=PermissionLevel.WRITE
    )
