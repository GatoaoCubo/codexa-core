"""
Intelligent Fallback - History Module
======================================

Tracks fallback attempts and outcomes to enable learning and optimization.
The history is used to:
1. Skip strategies that consistently fail
2. Prefer strategies that consistently succeed
3. Identify patterns in failures
4. Generate analytics for improvement

Version: 1.0.0
"""

import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Any, Optional
from pathlib import Path
from collections import defaultdict

from .actions import FallbackAction, CorrectionResult


@dataclass
class FallbackAttempt:
    """Record of a single fallback attempt."""

    timestamp: str  # ISO format
    session_id: str
    checkpoint_name: str
    initial_confidence: float
    action_taken: str  # FallbackAction name
    strategy_used: Optional[str]
    final_confidence: float
    success: bool
    duration_ms: int
    context: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None

    @classmethod
    def create(
        cls,
        session_id: str,
        checkpoint_name: str,
        initial_confidence: float,
        action: FallbackAction,
        strategy: Optional[str],
        final_confidence: float,
        success: bool,
        duration_ms: int,
        context: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None
    ) -> "FallbackAttempt":
        return cls(
            timestamp=datetime.now().isoformat(),
            session_id=session_id,
            checkpoint_name=checkpoint_name,
            initial_confidence=initial_confidence,
            action_taken=action.name,
            strategy_used=strategy,
            final_confidence=final_confidence,
            success=success,
            duration_ms=duration_ms,
            context=context or {},
            error=error
        )

    @property
    def improvement(self) -> float:
        """Confidence improvement from this attempt."""
        return self.final_confidence - self.initial_confidence

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StrategyStats:
    """Statistics for a single strategy."""

    strategy_name: str
    total_attempts: int = 0
    successes: int = 0
    failures: int = 0
    total_improvement: float = 0.0
    total_duration_ms: int = 0
    last_used: Optional[str] = None
    consecutive_failures: int = 0

    @property
    def success_rate(self) -> float:
        if self.total_attempts == 0:
            return 0.0
        return self.successes / self.total_attempts

    @property
    def avg_improvement(self) -> float:
        if self.total_attempts == 0:
            return 0.0
        return self.total_improvement / self.total_attempts

    @property
    def avg_duration_ms(self) -> int:
        if self.total_attempts == 0:
            return 0
        return self.total_duration_ms // self.total_attempts

    def record_attempt(self, attempt: FallbackAttempt) -> None:
        """Record a new attempt for this strategy."""
        self.total_attempts += 1
        self.total_duration_ms += attempt.duration_ms
        self.total_improvement += attempt.improvement
        self.last_used = attempt.timestamp

        if attempt.success:
            self.successes += 1
            self.consecutive_failures = 0
        else:
            self.failures += 1
            self.consecutive_failures += 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "strategy": self.strategy_name,
            "attempts": self.total_attempts,
            "successes": self.successes,
            "failures": self.failures,
            "success_rate": round(self.success_rate, 3),
            "avg_improvement": round(self.avg_improvement, 3),
            "avg_duration_ms": self.avg_duration_ms,
            "last_used": self.last_used,
            "consecutive_failures": self.consecutive_failures
        }


class FallbackHistory:
    """
    Manages fallback attempt history and provides learning insights.

    The history is persisted to a JSON file and loaded on initialization.
    """

    DEFAULT_HISTORY_PATH = ".fallback_history.json"
    MAX_HISTORY_SIZE = 1000  # Keep last N attempts
    CONSECUTIVE_FAILURE_THRESHOLD = 3  # Skip after N consecutive failures

    def __init__(self, history_path: Optional[str] = None):
        self.history_path = Path(history_path or self.DEFAULT_HISTORY_PATH)
        self.attempts: List[FallbackAttempt] = []
        self.strategy_stats: Dict[str, StrategyStats] = {}
        self.checkpoint_stats: Dict[str, Dict[str, StrategyStats]] = defaultdict(dict)
        self._load()

    def _load(self) -> None:
        """Load history from file."""
        if self.history_path.exists():
            try:
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.attempts = [
                        FallbackAttempt(**a) for a in data.get("attempts", [])
                    ]
                    self._rebuild_stats()
            except (json.JSONDecodeError, TypeError, KeyError) as e:
                # Corrupted history, start fresh
                self.attempts = []
                self.strategy_stats = {}

    def _save(self) -> None:
        """Save history to file."""
        # Trim to max size
        if len(self.attempts) > self.MAX_HISTORY_SIZE:
            self.attempts = self.attempts[-self.MAX_HISTORY_SIZE:]

        data = {
            "version": "1.0.0",
            "updated": datetime.now().isoformat(),
            "attempts": [a.to_dict() for a in self.attempts],
            "stats": {
                "strategies": {
                    name: stats.to_dict()
                    for name, stats in self.strategy_stats.items()
                }
            }
        }

        # Ensure directory exists
        self.history_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.history_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _rebuild_stats(self) -> None:
        """Rebuild statistics from attempts."""
        self.strategy_stats = {}
        self.checkpoint_stats = defaultdict(dict)

        for attempt in self.attempts:
            if attempt.strategy_used:
                # Global strategy stats
                if attempt.strategy_used not in self.strategy_stats:
                    self.strategy_stats[attempt.strategy_used] = StrategyStats(
                        strategy_name=attempt.strategy_used
                    )
                self.strategy_stats[attempt.strategy_used].record_attempt(attempt)

                # Per-checkpoint strategy stats
                checkpoint = attempt.checkpoint_name
                if attempt.strategy_used not in self.checkpoint_stats[checkpoint]:
                    self.checkpoint_stats[checkpoint][attempt.strategy_used] = StrategyStats(
                        strategy_name=attempt.strategy_used
                    )
                self.checkpoint_stats[checkpoint][attempt.strategy_used].record_attempt(attempt)

    def record(self, attempt: FallbackAttempt) -> None:
        """Record a new fallback attempt."""
        self.attempts.append(attempt)

        if attempt.strategy_used:
            if attempt.strategy_used not in self.strategy_stats:
                self.strategy_stats[attempt.strategy_used] = StrategyStats(
                    strategy_name=attempt.strategy_used
                )
            self.strategy_stats[attempt.strategy_used].record_attempt(attempt)

            # Per-checkpoint stats
            checkpoint = attempt.checkpoint_name
            if attempt.strategy_used not in self.checkpoint_stats[checkpoint]:
                self.checkpoint_stats[checkpoint][attempt.strategy_used] = StrategyStats(
                    strategy_name=attempt.strategy_used
                )
            self.checkpoint_stats[checkpoint][attempt.strategy_used].record_attempt(attempt)

        self._save()

    def success_rate(self, strategy: str) -> float:
        """Get the overall success rate for a strategy."""
        if strategy not in self.strategy_stats:
            return 0.5  # Default: unknown strategy, assume 50%
        return self.strategy_stats[strategy].success_rate

    def success_rate_for_checkpoint(
        self,
        strategy: str,
        checkpoint: str
    ) -> float:
        """Get success rate for a strategy on a specific checkpoint."""
        if checkpoint not in self.checkpoint_stats:
            return self.success_rate(strategy)
        if strategy not in self.checkpoint_stats[checkpoint]:
            return self.success_rate(strategy)
        return self.checkpoint_stats[checkpoint][strategy].success_rate

    def best_strategy_for(self, checkpoint: str) -> Optional[str]:
        """Find the best performing strategy for a checkpoint."""
        if checkpoint not in self.checkpoint_stats:
            return None

        stats = self.checkpoint_stats[checkpoint]
        if not stats:
            return None

        # Filter strategies with enough attempts
        viable = [
            (name, s) for name, s in stats.items()
            if s.total_attempts >= 3 and s.consecutive_failures < self.CONSECUTIVE_FAILURE_THRESHOLD
        ]

        if not viable:
            return None

        # Sort by success rate, then by improvement
        viable.sort(key=lambda x: (x[1].success_rate, x[1].avg_improvement), reverse=True)
        return viable[0][0]

    def should_skip(self, strategy: str, checkpoint: Optional[str] = None) -> bool:
        """
        Determine if a strategy should be skipped based on history.

        Returns True if:
        - Strategy has had too many consecutive failures
        - Strategy has very low success rate with enough data
        """
        stats = None

        if checkpoint and checkpoint in self.checkpoint_stats:
            stats = self.checkpoint_stats[checkpoint].get(strategy)

        if stats is None:
            stats = self.strategy_stats.get(strategy)

        if stats is None:
            return False  # Unknown strategy, don't skip

        # Skip if too many consecutive failures
        if stats.consecutive_failures >= self.CONSECUTIVE_FAILURE_THRESHOLD:
            return True

        # Skip if low success rate with significant data
        if stats.total_attempts >= 5 and stats.success_rate < 0.2:
            return True

        return False

    def get_recommended_strategies(
        self,
        checkpoint: str,
        available_strategies: List[str]
    ) -> List[str]:
        """
        Get strategies ordered by likelihood of success.

        Filters out strategies that should be skipped and orders
        remaining by historical success rate.
        """
        viable = [s for s in available_strategies if not self.should_skip(s, checkpoint)]

        # Sort by success rate for this checkpoint
        def sort_key(strategy: str) -> float:
            rate = self.success_rate_for_checkpoint(strategy, checkpoint)
            return rate

        viable.sort(key=sort_key, reverse=True)
        return viable

    def get_analytics(self) -> Dict[str, Any]:
        """Generate analytics summary."""
        total_attempts = len(self.attempts)
        successful = sum(1 for a in self.attempts if a.success)

        return {
            "total_attempts": total_attempts,
            "successful": successful,
            "overall_success_rate": successful / total_attempts if total_attempts > 0 else 0,
            "strategies": {
                name: stats.to_dict()
                for name, stats in sorted(
                    self.strategy_stats.items(),
                    key=lambda x: x[1].success_rate,
                    reverse=True
                )
            },
            "checkpoints": {
                cp: {
                    name: stats.to_dict()
                    for name, stats in checkpoint_stats.items()
                }
                for cp, checkpoint_stats in self.checkpoint_stats.items()
            }
        }

    def clear_history(self) -> None:
        """Clear all history (for testing or reset)."""
        self.attempts = []
        self.strategy_stats = {}
        self.checkpoint_stats = defaultdict(dict)
        if self.history_path.exists():
            self.history_path.unlink()

    def get_recent_attempts(
        self,
        limit: int = 10,
        checkpoint: Optional[str] = None
    ) -> List[FallbackAttempt]:
        """Get recent attempts, optionally filtered by checkpoint."""
        attempts = self.attempts
        if checkpoint:
            attempts = [a for a in attempts if a.checkpoint_name == checkpoint]
        return attempts[-limit:]
