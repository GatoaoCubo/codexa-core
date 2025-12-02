"""
Rate Limiter for CODEXA Agent System
Token bucket algorithm with per-provider and per-user limits.
"""

import time
import asyncio
from typing import Dict, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import defaultdict
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class RateLimitExceeded(Exception):
    """Raised when rate limit is exceeded."""

    def __init__(self, message: str, retry_after: float):
        super().__init__(message)
        self.retry_after = retry_after


class LimitType(Enum):
    """Types of rate limits."""
    REQUESTS_PER_MINUTE = "rpm"
    REQUESTS_PER_HOUR = "rph"
    TOKENS_PER_MINUTE = "tpm"
    TOKENS_PER_DAY = "tpd"


@dataclass
class RateLimitConfig:
    """Configuration for rate limits."""
    requests_per_minute: int = 60
    requests_per_hour: int = 1000
    tokens_per_minute: int = 100_000
    tokens_per_day: int = 1_000_000
    burst_multiplier: float = 1.5  # Allow burst up to 1.5x limit


@dataclass
class TokenBucket:
    """Token bucket for rate limiting."""
    capacity: float
    tokens: float = field(default=None)
    last_update: float = field(default_factory=time.time)
    refill_rate: float = 1.0  # tokens per second

    def __post_init__(self):
        if self.tokens is None:
            self.tokens = self.capacity

    def consume(self, amount: float = 1.0) -> Tuple[bool, float]:
        """
        Try to consume tokens from bucket.

        Args:
            amount: Number of tokens to consume

        Returns:
            Tuple of (success, wait_time if failed)
        """
        now = time.time()
        elapsed = now - self.last_update

        # Refill tokens
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_update = now

        if self.tokens >= amount:
            self.tokens -= amount
            return True, 0.0
        else:
            wait_time = (amount - self.tokens) / self.refill_rate
            return False, wait_time


@dataclass
class UserLimits:
    """Rate limits for a specific user."""
    user_id: str
    request_bucket: TokenBucket
    token_bucket: TokenBucket
    daily_tokens_used: int = 0
    daily_reset_time: datetime = field(default_factory=datetime.now)

    def reset_daily_if_needed(self):
        """Reset daily limits if needed."""
        now = datetime.now()
        if now.date() > self.daily_reset_time.date():
            self.daily_tokens_used = 0
            self.daily_reset_time = now


class RateLimiter:
    """
    Rate limiter with token bucket algorithm.

    Features:
    - Per-provider rate limits
    - Per-user rate limits
    - Token-based limits (for LLM APIs)
    - Request-based limits
    - Async support
    - Burst allowance
    """

    # Default limits per provider
    DEFAULT_PROVIDER_LIMITS = {
        "claude": RateLimitConfig(
            requests_per_minute=50,
            requests_per_hour=1000,
            tokens_per_minute=100_000,
            tokens_per_day=1_000_000,
        ),
        "openai": RateLimitConfig(
            requests_per_minute=60,
            requests_per_hour=3500,
            tokens_per_minute=150_000,
            tokens_per_day=2_000_000,
        ),
        "gemini": RateLimitConfig(
            requests_per_minute=60,
            requests_per_hour=1500,
            tokens_per_minute=120_000,
            tokens_per_day=1_500_000,
        ),
    }

    def __init__(
        self,
        provider_limits: Optional[Dict[str, RateLimitConfig]] = None,
        default_user_limit: Optional[RateLimitConfig] = None,
    ):
        """
        Initialize rate limiter.

        Args:
            provider_limits: Custom limits per provider
            default_user_limit: Default limit for users
        """
        self.provider_limits = {
            **self.DEFAULT_PROVIDER_LIMITS,
            **(provider_limits or {}),
        }

        self.default_user_limit = default_user_limit or RateLimitConfig(
            requests_per_minute=30,
            requests_per_hour=500,
            tokens_per_minute=50_000,
            tokens_per_day=500_000,
        )

        # Buckets: provider -> TokenBucket
        self.provider_buckets: Dict[str, Dict[str, TokenBucket]] = defaultdict(dict)

        # User limits: user_id -> UserLimits
        self.user_limits: Dict[str, UserLimits] = {}

        # Statistics
        self.stats = {
            "total_requests": 0,
            "total_tokens": 0,
            "rate_limited_count": 0,
            "requests_by_provider": defaultdict(int),
            "tokens_by_provider": defaultdict(int),
        }

        self._lock = asyncio.Lock()
        logger.info("Initialized rate limiter")

    def _get_provider_bucket(self, provider: str, limit_type: str) -> TokenBucket:
        """Get or create token bucket for provider."""
        if limit_type not in self.provider_buckets[provider]:
            config = self.provider_limits.get(provider, self.default_user_limit)

            if limit_type == "rpm":
                capacity = config.requests_per_minute * config.burst_multiplier
                refill_rate = config.requests_per_minute / 60
            elif limit_type == "tpm":
                capacity = config.tokens_per_minute * config.burst_multiplier
                refill_rate = config.tokens_per_minute / 60
            else:
                capacity = 100
                refill_rate = 1.0

            self.provider_buckets[provider][limit_type] = TokenBucket(
                capacity=capacity,
                refill_rate=refill_rate,
            )

        return self.provider_buckets[provider][limit_type]

    def _get_user_limits(self, user_id: str) -> UserLimits:
        """Get or create user limits."""
        if user_id not in self.user_limits:
            config = self.default_user_limit

            self.user_limits[user_id] = UserLimits(
                user_id=user_id,
                request_bucket=TokenBucket(
                    capacity=config.requests_per_minute * config.burst_multiplier,
                    refill_rate=config.requests_per_minute / 60,
                ),
                token_bucket=TokenBucket(
                    capacity=config.tokens_per_minute * config.burst_multiplier,
                    refill_rate=config.tokens_per_minute / 60,
                ),
            )

        return self.user_limits[user_id]

    def check_limit(
        self,
        provider: str,
        user_id: Optional[str] = None,
        token_count: int = 0,
    ) -> Tuple[bool, float]:
        """
        Check if request is within rate limits.

        Args:
            provider: LLM provider name
            user_id: Optional user identifier
            token_count: Estimated token count for request

        Returns:
            Tuple of (allowed, wait_time_if_not_allowed)
        """
        # Check provider request limit
        provider_rpm = self._get_provider_bucket(provider, "rpm")
        allowed, wait_time = provider_rpm.consume(1)
        if not allowed:
            return False, wait_time

        # Check provider token limit if applicable
        if token_count > 0:
            provider_tpm = self._get_provider_bucket(provider, "tpm")
            allowed, wait_time = provider_tpm.consume(token_count)
            if not allowed:
                # Refund the request token
                provider_rpm.tokens += 1
                return False, wait_time

        # Check user limits if user_id provided
        if user_id:
            user_limits = self._get_user_limits(user_id)
            user_limits.reset_daily_if_needed()

            # Check daily token limit
            daily_limit = self.default_user_limit.tokens_per_day
            if user_limits.daily_tokens_used + token_count > daily_limit:
                # Calculate time until midnight reset
                now = datetime.now()
                midnight = (now + timedelta(days=1)).replace(
                    hour=0, minute=0, second=0, microsecond=0
                )
                wait_time = (midnight - now).total_seconds()
                return False, wait_time

            # Check user request limit
            allowed, wait_time = user_limits.request_bucket.consume(1)
            if not allowed:
                return False, wait_time

            # Check user token limit
            if token_count > 0:
                allowed, wait_time = user_limits.token_bucket.consume(token_count)
                if not allowed:
                    user_limits.request_bucket.tokens += 1
                    return False, wait_time

                user_limits.daily_tokens_used += token_count

        return True, 0.0

    async def acquire(
        self,
        provider: str,
        user_id: Optional[str] = None,
        token_count: int = 0,
        max_wait: float = 60.0,
    ):
        """
        Acquire rate limit slot, waiting if necessary.

        Args:
            provider: LLM provider name
            user_id: Optional user identifier
            token_count: Estimated token count
            max_wait: Maximum time to wait (seconds)

        Raises:
            RateLimitExceeded: If wait time exceeds max_wait
        """
        async with self._lock:
            allowed, wait_time = self.check_limit(provider, user_id, token_count)

            if allowed:
                self._record_request(provider, token_count)
                return

            if wait_time > max_wait:
                self.stats["rate_limited_count"] += 1
                raise RateLimitExceeded(
                    f"Rate limit exceeded for {provider}. Retry after {wait_time:.1f}s",
                    retry_after=wait_time,
                )

            logger.info(f"Rate limited, waiting {wait_time:.1f}s for {provider}")

        # Wait outside the lock
        await asyncio.sleep(wait_time)

        # Retry after waiting
        await self.acquire(provider, user_id, token_count, max_wait - wait_time)

    def acquire_sync(
        self,
        provider: str,
        user_id: Optional[str] = None,
        token_count: int = 0,
        max_wait: float = 60.0,
    ):
        """
        Synchronous version of acquire.

        Args:
            provider: LLM provider name
            user_id: Optional user identifier
            token_count: Estimated token count
            max_wait: Maximum time to wait (seconds)

        Raises:
            RateLimitExceeded: If wait time exceeds max_wait
        """
        allowed, wait_time = self.check_limit(provider, user_id, token_count)

        if allowed:
            self._record_request(provider, token_count)
            return

        if wait_time > max_wait:
            self.stats["rate_limited_count"] += 1
            raise RateLimitExceeded(
                f"Rate limit exceeded for {provider}. Retry after {wait_time:.1f}s",
                retry_after=wait_time,
            )

        logger.info(f"Rate limited, waiting {wait_time:.1f}s for {provider}")
        time.sleep(wait_time)

        # Retry after waiting
        self.acquire_sync(provider, user_id, token_count, max_wait - wait_time)

    def _record_request(self, provider: str, token_count: int):
        """Record request statistics."""
        self.stats["total_requests"] += 1
        self.stats["total_tokens"] += token_count
        self.stats["requests_by_provider"][provider] += 1
        self.stats["tokens_by_provider"][provider] += token_count

    def get_stats(self) -> Dict:
        """Get rate limiter statistics."""
        return {
            **self.stats,
            "requests_by_provider": dict(self.stats["requests_by_provider"]),
            "tokens_by_provider": dict(self.stats["tokens_by_provider"]),
        }

    def get_remaining(self, provider: str, user_id: Optional[str] = None) -> Dict:
        """
        Get remaining capacity.

        Args:
            provider: Provider name
            user_id: Optional user ID

        Returns:
            Dict with remaining capacity info
        """
        result = {}

        # Provider limits
        if provider in self.provider_buckets:
            for limit_type, bucket in self.provider_buckets[provider].items():
                result[f"provider_{limit_type}"] = int(bucket.tokens)

        # User limits
        if user_id and user_id in self.user_limits:
            user = self.user_limits[user_id]
            result["user_requests"] = int(user.request_bucket.tokens)
            result["user_tokens"] = int(user.token_bucket.tokens)
            result["user_daily_remaining"] = (
                self.default_user_limit.tokens_per_day - user.daily_tokens_used
            )

        return result

    def reset_provider(self, provider: str):
        """Reset rate limits for a provider."""
        if provider in self.provider_buckets:
            del self.provider_buckets[provider]
            logger.info(f"Reset rate limits for provider: {provider}")

    def reset_user(self, user_id: str):
        """Reset rate limits for a user."""
        if user_id in self.user_limits:
            del self.user_limits[user_id]
            logger.info(f"Reset rate limits for user: {user_id}")


# Global rate limiter instance
_rate_limiter: Optional[RateLimiter] = None


def get_rate_limiter() -> RateLimiter:
    """Get global rate limiter instance."""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter


async def check_rate_limit(
    provider: str,
    user_id: Optional[str] = None,
    token_count: int = 0,
):
    """
    Check rate limit for a request.

    Args:
        provider: LLM provider name
        user_id: Optional user identifier
        token_count: Estimated token count

    Raises:
        RateLimitExceeded: If rate limit exceeded
    """
    limiter = get_rate_limiter()
    await limiter.acquire(provider, user_id, token_count)
