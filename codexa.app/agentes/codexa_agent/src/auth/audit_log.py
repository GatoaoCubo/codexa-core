"""
Audit Logging System for CODEXA Agent
Comprehensive logging for security, compliance, and debugging.
"""

import json
import logging
import asyncio
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from enum import Enum
from collections import deque
import hashlib
import uuid

logger = logging.getLogger(__name__)


class AuditEventType(Enum):
    """Types of audit events."""
    # Authentication events
    AUTH_SUCCESS = "auth.success"
    AUTH_FAILURE = "auth.failure"
    AUTH_LOGOUT = "auth.logout"

    # API events
    API_CALL = "api.call"
    API_SUCCESS = "api.success"
    API_ERROR = "api.error"

    # Tool events
    TOOL_EXECUTE = "tool.execute"
    TOOL_SUCCESS = "tool.success"
    TOOL_FAILURE = "tool.failure"
    TOOL_BLOCKED = "tool.blocked"

    # File operations
    FILE_READ = "file.read"
    FILE_WRITE = "file.write"
    FILE_DELETE = "file.delete"

    # Agent events
    AGENT_START = "agent.start"
    AGENT_COMPLETE = "agent.complete"
    AGENT_ERROR = "agent.error"

    # Workflow events
    WORKFLOW_START = "workflow.start"
    WORKFLOW_STEP = "workflow.step"
    WORKFLOW_COMPLETE = "workflow.complete"
    WORKFLOW_ERROR = "workflow.error"

    # Security events
    SECURITY_VIOLATION = "security.violation"
    PERMISSION_DENIED = "security.permission_denied"
    RATE_LIMITED = "security.rate_limited"

    # System events
    SYSTEM_START = "system.start"
    SYSTEM_SHUTDOWN = "system.shutdown"
    SYSTEM_ERROR = "system.error"


class AuditSeverity(Enum):
    """Severity levels for audit events."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """Represents a single audit event."""
    event_id: str
    event_type: AuditEventType
    severity: AuditSeverity
    timestamp: datetime
    user_id: Optional[str]
    session_id: Optional[str]
    workflow_id: Optional[str]
    agent_id: Optional[str]
    action: str
    resource: Optional[str]
    details: Dict[str, Any]
    result: Optional[str]
    duration_ms: Optional[int]
    ip_address: Optional[str]
    user_agent: Optional[str]

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        data = asdict(self)
        data["event_type"] = self.event_type.value
        data["severity"] = self.severity.value
        data["timestamp"] = self.timestamp.isoformat()
        return data

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_dict(cls, data: Dict) -> "AuditEvent":
        """Create from dictionary."""
        data["event_type"] = AuditEventType(data["event_type"])
        data["severity"] = AuditSeverity(data["severity"])
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


@dataclass
class AuditContext:
    """Context for tracking audit trail."""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    workflow_id: Optional[str] = None
    agent_id: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

    def with_workflow(self, workflow_id: str) -> "AuditContext":
        """Create new context with workflow ID."""
        return AuditContext(
            user_id=self.user_id,
            session_id=self.session_id,
            workflow_id=workflow_id,
            agent_id=self.agent_id,
            ip_address=self.ip_address,
            user_agent=self.user_agent,
        )

    def with_agent(self, agent_id: str) -> "AuditContext":
        """Create new context with agent ID."""
        return AuditContext(
            user_id=self.user_id,
            session_id=self.session_id,
            workflow_id=self.workflow_id,
            agent_id=agent_id,
            ip_address=self.ip_address,
            user_agent=self.user_agent,
        )


class AuditLogHandler:
    """
    Handler for audit log storage.

    Supports multiple backends:
    - File-based (JSON lines)
    - In-memory (for testing)
    - Future: Database, cloud storage
    """

    def __init__(self, log_dir: Optional[Path] = None, max_memory_events: int = 10000):
        """
        Initialize audit log handler.

        Args:
            log_dir: Directory for log files (None for memory-only)
            max_memory_events: Maximum events to keep in memory
        """
        self.log_dir = Path(log_dir) if log_dir else None
        self.max_memory_events = max_memory_events

        # In-memory event store (circular buffer)
        self.events: deque = deque(maxlen=max_memory_events)

        # Statistics
        self.stats = {
            "total_events": 0,
            "events_by_type": {},
            "events_by_severity": {},
            "errors_count": 0,
        }

        # Create log directory if needed
        if self.log_dir:
            self.log_dir.mkdir(parents=True, exist_ok=True)

        self._lock = asyncio.Lock()
        logger.info(f"Initialized audit log handler (dir: {log_dir})")

    def _get_log_file(self, timestamp: datetime) -> Path:
        """Get log file path for timestamp."""
        if not self.log_dir:
            return None
        date_str = timestamp.strftime("%Y-%m-%d")
        return self.log_dir / f"audit_{date_str}.jsonl"

    async def write(self, event: AuditEvent):
        """
        Write audit event.

        Args:
            event: Audit event to write
        """
        async with self._lock:
            # Add to memory store
            self.events.append(event)

            # Update statistics
            self.stats["total_events"] += 1
            event_type = event.event_type.value
            self.stats["events_by_type"][event_type] = (
                self.stats["events_by_type"].get(event_type, 0) + 1
            )
            severity = event.severity.value
            self.stats["events_by_severity"][severity] = (
                self.stats["events_by_severity"].get(severity, 0) + 1
            )
            if event.severity in (AuditSeverity.ERROR, AuditSeverity.CRITICAL):
                self.stats["errors_count"] += 1

            # Write to file if configured
            if self.log_dir:
                log_file = self._get_log_file(event.timestamp)
                try:
                    with open(log_file, "a", encoding="utf-8") as f:
                        f.write(event.to_json() + "\n")
                except Exception as e:
                    logger.error(f"Failed to write audit log: {e}")

    def write_sync(self, event: AuditEvent):
        """Synchronous version of write."""
        # Add to memory store
        self.events.append(event)

        # Update statistics
        self.stats["total_events"] += 1
        event_type = event.event_type.value
        self.stats["events_by_type"][event_type] = (
            self.stats["events_by_type"].get(event_type, 0) + 1
        )
        severity = event.severity.value
        self.stats["events_by_severity"][severity] = (
            self.stats["events_by_severity"].get(severity, 0) + 1
        )
        if event.severity in (AuditSeverity.ERROR, AuditSeverity.CRITICAL):
            self.stats["errors_count"] += 1

        # Write to file if configured
        if self.log_dir:
            log_file = self._get_log_file(event.timestamp)
            try:
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(event.to_json() + "\n")
            except Exception as e:
                logger.error(f"Failed to write audit log: {e}")

    def query(
        self,
        event_type: Optional[AuditEventType] = None,
        severity: Optional[AuditSeverity] = None,
        user_id: Optional[str] = None,
        workflow_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[AuditEvent]:
        """
        Query audit events from memory.

        Args:
            event_type: Filter by event type
            severity: Filter by severity
            user_id: Filter by user ID
            workflow_id: Filter by workflow ID
            start_time: Filter by start time
            end_time: Filter by end time
            limit: Maximum events to return

        Returns:
            List of matching audit events
        """
        results = []

        for event in reversed(self.events):
            if len(results) >= limit:
                break

            if event_type and event.event_type != event_type:
                continue
            if severity and event.severity != severity:
                continue
            if user_id and event.user_id != user_id:
                continue
            if workflow_id and event.workflow_id != workflow_id:
                continue
            if start_time and event.timestamp < start_time:
                continue
            if end_time and event.timestamp > end_time:
                continue

            results.append(event)

        return results

    def get_stats(self) -> Dict:
        """Get audit log statistics."""
        return {
            **self.stats,
            "memory_events": len(self.events),
        }


class AuditLogger:
    """
    Main audit logger for CODEXA Agent.

    Usage:
        audit = AuditLogger()
        ctx = AuditContext(user_id="user123")

        # Log API call
        audit.log_api_call(ctx, "claude", "completion", {"model": "sonnet"})

        # Log tool execution
        audit.log_tool_execute(ctx, "file_read", "/path/to/file")
    """

    def __init__(self, handler: Optional[AuditLogHandler] = None):
        """
        Initialize audit logger.

        Args:
            handler: Audit log handler (creates default if None)
        """
        self.handler = handler or AuditLogHandler()
        self.default_context = AuditContext()

    def _generate_event_id(self) -> str:
        """Generate unique event ID."""
        return str(uuid.uuid4())[:12]

    def _create_event(
        self,
        event_type: AuditEventType,
        severity: AuditSeverity,
        context: Optional[AuditContext],
        action: str,
        resource: Optional[str] = None,
        details: Optional[Dict] = None,
        result: Optional[str] = None,
        duration_ms: Optional[int] = None,
    ) -> AuditEvent:
        """Create audit event."""
        ctx = context or self.default_context
        return AuditEvent(
            event_id=self._generate_event_id(),
            event_type=event_type,
            severity=severity,
            timestamp=datetime.now(),
            user_id=ctx.user_id,
            session_id=ctx.session_id,
            workflow_id=ctx.workflow_id,
            agent_id=ctx.agent_id,
            action=action,
            resource=resource,
            details=details or {},
            result=result,
            duration_ms=duration_ms,
            ip_address=ctx.ip_address,
            user_agent=ctx.user_agent,
        )

    def log(
        self,
        event_type: AuditEventType,
        severity: AuditSeverity,
        context: Optional[AuditContext],
        action: str,
        resource: Optional[str] = None,
        details: Optional[Dict] = None,
        result: Optional[str] = None,
        duration_ms: Optional[int] = None,
    ):
        """
        Log an audit event (synchronous).

        Args:
            event_type: Type of event
            severity: Severity level
            context: Audit context
            action: Action performed
            resource: Resource affected
            details: Additional details
            result: Result of action
            duration_ms: Duration in milliseconds
        """
        event = self._create_event(
            event_type, severity, context, action, resource, details, result, duration_ms
        )
        self.handler.write_sync(event)

    async def log_async(
        self,
        event_type: AuditEventType,
        severity: AuditSeverity,
        context: Optional[AuditContext],
        action: str,
        resource: Optional[str] = None,
        details: Optional[Dict] = None,
        result: Optional[str] = None,
        duration_ms: Optional[int] = None,
    ):
        """Async version of log."""
        event = self._create_event(
            event_type, severity, context, action, resource, details, result, duration_ms
        )
        await self.handler.write(event)

    # Convenience methods for common events

    def log_api_call(
        self,
        context: Optional[AuditContext],
        provider: str,
        endpoint: str,
        details: Optional[Dict] = None,
    ):
        """Log API call."""
        self.log(
            AuditEventType.API_CALL,
            AuditSeverity.INFO,
            context,
            f"api_call:{provider}:{endpoint}",
            resource=f"{provider}/{endpoint}",
            details=details,
        )

    def log_api_success(
        self,
        context: Optional[AuditContext],
        provider: str,
        endpoint: str,
        duration_ms: int,
        details: Optional[Dict] = None,
    ):
        """Log successful API call."""
        self.log(
            AuditEventType.API_SUCCESS,
            AuditSeverity.INFO,
            context,
            f"api_success:{provider}:{endpoint}",
            resource=f"{provider}/{endpoint}",
            details=details,
            result="success",
            duration_ms=duration_ms,
        )

    def log_api_error(
        self,
        context: Optional[AuditContext],
        provider: str,
        endpoint: str,
        error: str,
        details: Optional[Dict] = None,
    ):
        """Log API error."""
        self.log(
            AuditEventType.API_ERROR,
            AuditSeverity.ERROR,
            context,
            f"api_error:{provider}:{endpoint}",
            resource=f"{provider}/{endpoint}",
            details={**(details or {}), "error": error},
            result="error",
        )

    def log_tool_execute(
        self,
        context: Optional[AuditContext],
        tool_name: str,
        resource: str,
        params: Optional[Dict] = None,
    ):
        """Log tool execution."""
        # Hash sensitive parameters
        safe_params = self._sanitize_params(params) if params else {}
        self.log(
            AuditEventType.TOOL_EXECUTE,
            AuditSeverity.INFO,
            context,
            f"tool_execute:{tool_name}",
            resource=resource,
            details={"params": safe_params},
        )

    def log_tool_success(
        self,
        context: Optional[AuditContext],
        tool_name: str,
        resource: str,
        duration_ms: int,
    ):
        """Log successful tool execution."""
        self.log(
            AuditEventType.TOOL_SUCCESS,
            AuditSeverity.INFO,
            context,
            f"tool_success:{tool_name}",
            resource=resource,
            result="success",
            duration_ms=duration_ms,
        )

    def log_tool_failure(
        self,
        context: Optional[AuditContext],
        tool_name: str,
        resource: str,
        error: str,
    ):
        """Log tool failure."""
        self.log(
            AuditEventType.TOOL_FAILURE,
            AuditSeverity.ERROR,
            context,
            f"tool_failure:{tool_name}",
            resource=resource,
            details={"error": error},
            result="failure",
        )

    def log_tool_blocked(
        self,
        context: Optional[AuditContext],
        tool_name: str,
        resource: str,
        reason: str,
    ):
        """Log blocked tool execution."""
        self.log(
            AuditEventType.TOOL_BLOCKED,
            AuditSeverity.WARNING,
            context,
            f"tool_blocked:{tool_name}",
            resource=resource,
            details={"reason": reason},
            result="blocked",
        )

    def log_file_operation(
        self,
        context: Optional[AuditContext],
        operation: str,
        file_path: str,
        details: Optional[Dict] = None,
    ):
        """Log file operation."""
        event_type = {
            "read": AuditEventType.FILE_READ,
            "write": AuditEventType.FILE_WRITE,
            "delete": AuditEventType.FILE_DELETE,
        }.get(operation, AuditEventType.FILE_READ)

        self.log(
            event_type,
            AuditSeverity.INFO,
            context,
            f"file_{operation}",
            resource=file_path,
            details=details,
        )

    def log_security_violation(
        self,
        context: Optional[AuditContext],
        violation_type: str,
        resource: str,
        details: Optional[Dict] = None,
    ):
        """Log security violation."""
        self.log(
            AuditEventType.SECURITY_VIOLATION,
            AuditSeverity.CRITICAL,
            context,
            f"security_violation:{violation_type}",
            resource=resource,
            details=details,
        )

    def log_permission_denied(
        self,
        context: Optional[AuditContext],
        action: str,
        resource: str,
        required_permission: str,
    ):
        """Log permission denied."""
        self.log(
            AuditEventType.PERMISSION_DENIED,
            AuditSeverity.WARNING,
            context,
            f"permission_denied:{action}",
            resource=resource,
            details={"required_permission": required_permission},
        )

    def log_workflow_start(
        self,
        context: Optional[AuditContext],
        workflow_name: str,
        details: Optional[Dict] = None,
    ):
        """Log workflow start."""
        self.log(
            AuditEventType.WORKFLOW_START,
            AuditSeverity.INFO,
            context,
            f"workflow_start:{workflow_name}",
            details=details,
        )

    def log_workflow_complete(
        self,
        context: Optional[AuditContext],
        workflow_name: str,
        duration_ms: int,
        details: Optional[Dict] = None,
    ):
        """Log workflow completion."""
        self.log(
            AuditEventType.WORKFLOW_COMPLETE,
            AuditSeverity.INFO,
            context,
            f"workflow_complete:{workflow_name}",
            result="success",
            duration_ms=duration_ms,
            details=details,
        )

    def _sanitize_params(self, params: Dict) -> Dict:
        """Sanitize parameters for logging (remove/hash sensitive data)."""
        sensitive_keys = {"password", "token", "key", "secret", "credential", "api_key"}
        sanitized = {}

        for key, value in params.items():
            key_lower = key.lower()
            if any(s in key_lower for s in sensitive_keys):
                if isinstance(value, str):
                    sanitized[key] = hashlib.sha256(value.encode()).hexdigest()[:8] + "..."
                else:
                    sanitized[key] = "[REDACTED]"
            elif isinstance(value, dict):
                sanitized[key] = self._sanitize_params(value)
            else:
                sanitized[key] = value

        return sanitized

    def query(self, **kwargs) -> List[AuditEvent]:
        """Query audit events."""
        return self.handler.query(**kwargs)

    def get_stats(self) -> Dict:
        """Get audit statistics."""
        return self.handler.get_stats()


# Global audit logger instance
_audit_logger: Optional[AuditLogger] = None


def get_audit_logger(log_dir: Optional[Path] = None) -> AuditLogger:
    """Get global audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        handler = AuditLogHandler(log_dir=log_dir)
        _audit_logger = AuditLogger(handler=handler)
    return _audit_logger


def audit_log(
    event_type: AuditEventType,
    action: str,
    context: Optional[AuditContext] = None,
    **kwargs,
):
    """
    Convenience function for audit logging.

    Args:
        event_type: Type of event
        action: Action performed
        context: Audit context
        **kwargs: Additional event parameters
    """
    logger = get_audit_logger()
    logger.log(
        event_type=event_type,
        severity=kwargs.pop("severity", AuditSeverity.INFO),
        context=context,
        action=action,
        **kwargs,
    )
