"""
CODEXA Authentication & Security System
Version: 3.1.0

Production-grade authentication for LLM providers:
- API key management
- Rate limiting (token bucket algorithm)
- Audit logging
- Secrets management
"""

from .api_keys import APIKeyManager, APIKeyError, get_default_key_manager
from .rate_limiter import (
    RateLimiter,
    RateLimitConfig,
    RateLimitExceeded,
    get_rate_limiter,
    check_rate_limit,
)
from .audit_log import (
    AuditLogger,
    AuditLogHandler,
    AuditEvent,
    AuditContext,
    AuditEventType,
    AuditSeverity,
    get_audit_logger,
    audit_log,
)
from .secrets import (
    SecretsManager,
    SecretsError,
    get_secrets_manager,
    get_secret,
    require_secret,
)

__all__ = [
    # API Keys
    'APIKeyManager',
    'APIKeyError',
    'get_default_key_manager',
    # Rate Limiting
    'RateLimiter',
    'RateLimitConfig',
    'RateLimitExceeded',
    'get_rate_limiter',
    'check_rate_limit',
    # Audit Logging
    'AuditLogger',
    'AuditLogHandler',
    'AuditEvent',
    'AuditContext',
    'AuditEventType',
    'AuditSeverity',
    'get_audit_logger',
    'audit_log',
    # Secrets
    'SecretsManager',
    'SecretsError',
    'get_secrets_manager',
    'get_secret',
    'require_secret',
]
