"""
LLM Response Cache for TAC-7

Caches LLM API responses to reduce costs and improve performance.

Performance Impact:
- Before: 500-2000ms per API call, $0.001-0.01 per call
- After: <10ms for cached responses, $0 for cache hits
- Expected savings: 50% cost reduction on repeated queries

Cache Strategy:
- Hash-based cache using query + schema + model as key
- TTL-based expiration (default: 1 hour)
- In-memory cache with optional disk persistence
"""

import hashlib
import json
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional, Tuple
from collections import OrderedDict


class LLMCache:
    """
    Cache for LLM API responses with TTL and size limits.

    Features:
    - Hash-based keys (query + schema + model)
    - Time-to-live (TTL) expiration
    - LRU eviction when max size reached
    - Optional disk persistence
    """

    def __init__(
        self,
        ttl_seconds: int = 3600,
        max_entries: int = 1000,
        persist_path: Optional[Path] = None
    ):
        """
        Initialize the LLM cache.

        Args:
            ttl_seconds: Time-to-live for cache entries (default: 1 hour)
            max_entries: Maximum number of entries (default: 1000)
            persist_path: Path to persist cache to disk (optional)
        """
        self.ttl = timedelta(seconds=ttl_seconds)
        self.max_entries = max_entries
        self.persist_path = persist_path

        # OrderedDict for LRU behavior
        self.cache: OrderedDict[str, Tuple[Any, datetime]] = OrderedDict()

        # Load from disk if persistence enabled
        if persist_path and persist_path.exists():
            self._load_from_disk()

        # Statistics
        self.hits = 0
        self.misses = 0

    def _get_cache_key(self, query: str, schema: Dict[str, Any], model: str) -> str:
        """
        Generate cache key from query, schema, and model.

        Args:
            query: Natural language query
            schema: Database schema dictionary
            model: LLM model identifier

        Returns:
            str: SHA256 hash of inputs
        """
        # Normalize inputs for consistent hashing
        schema_str = json.dumps(schema, sort_keys=True)
        query_normalized = query.strip().lower()

        # Create hash
        cache_input = f"{query_normalized}|{schema_str}|{model}"
        return hashlib.sha256(cache_input.encode()).hexdigest()

    def get(
        self,
        query: str,
        schema: Dict[str, Any],
        model: str
    ) -> Optional[str]:
        """
        Get cached response if available and not expired.

        Args:
            query: Natural language query
            schema: Database schema dictionary
            model: LLM model identifier

        Returns:
            Optional[str]: Cached response or None if not found/expired
        """
        key = self._get_cache_key(query, schema, model)

        if key in self.cache:
            result, timestamp = self.cache[key]

            # Check if expired
            if datetime.now() - timestamp < self.ttl:
                # Move to end (LRU)
                self.cache.move_to_end(key)
                self.hits += 1
                return result
            else:
                # Expired - remove
                del self.cache[key]

        self.misses += 1
        return None

    def set(
        self,
        query: str,
        schema: Dict[str, Any],
        model: str,
        result: str
    ) -> None:
        """
        Cache an LLM response.

        Args:
            query: Natural language query
            schema: Database schema dictionary
            model: LLM model identifier
            result: LLM response to cache
        """
        key = self._get_cache_key(query, schema, model)

        # Add to cache
        self.cache[key] = (result, datetime.now())
        self.cache.move_to_end(key)

        # Evict oldest if over limit (LRU)
        if len(self.cache) > self.max_entries:
            self.cache.popitem(last=False)

        # Persist if enabled
        if self.persist_path:
            self._save_to_disk()

    def clear(self) -> None:
        """Clear all cache entries."""
        self.cache.clear()
        self.hits = 0
        self.misses = 0

        if self.persist_path and self.persist_path.exists():
            self.persist_path.unlink()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics.

        Returns:
            Dict with hits, misses, hit_rate, size
        """
        total_requests = self.hits + self.misses
        hit_rate = self.hits / total_requests if total_requests > 0 else 0.0

        return {
            "hits": self.hits,
            "misses": self.misses,
            "total_requests": total_requests,
            "hit_rate": hit_rate,
            "cache_size": len(self.cache),
            "max_entries": self.max_entries,
            "ttl_seconds": self.ttl.total_seconds()
        }

    def _save_to_disk(self) -> None:
        """Save cache to disk."""
        if not self.persist_path:
            return

        # Ensure directory exists
        self.persist_path.parent.mkdir(parents=True, exist_ok=True)

        # Save cache data
        data = {
            "cache": dict(self.cache),
            "hits": self.hits,
            "misses": self.misses
        }

        with open(self.persist_path, 'wb') as f:
            pickle.dump(data, f)

    def _load_from_disk(self) -> None:
        """Load cache from disk."""
        if not self.persist_path or not self.persist_path.exists():
            return

        try:
            with open(self.persist_path, 'rb') as f:
                data = pickle.load(f)

            self.cache = OrderedDict(data.get("cache", {}))
            self.hits = data.get("hits", 0)
            self.misses = data.get("misses", 0)

            # Clean expired entries
            now = datetime.now()
            expired_keys = [
                k for k, (_, ts) in self.cache.items()
                if now - ts >= self.ttl
            ]
            for k in expired_keys:
                del self.cache[k]

        except Exception as e:
            print(f"Warning: Failed to load cache from disk: {e}")
            self.cache.clear()


# Global cache instance
llm_cache: Optional[LLMCache] = None


def initialize_cache(
    ttl_seconds: int = 3600,
    max_entries: int = 1000,
    persist_path: Optional[str] = None
) -> LLMCache:
    """
    Initialize the global LLM cache.

    Call this once during application startup.

    Args:
        ttl_seconds: Time-to-live for cache entries
        max_entries: Maximum number of entries
        persist_path: Path to persist cache to disk

    Returns:
        LLMCache: The global cache instance
    """
    global llm_cache

    persist = Path(persist_path) if persist_path else None
    llm_cache = LLMCache(ttl_seconds, max_entries, persist)
    return llm_cache


def get_cache() -> LLMCache:
    """
    Get the global LLM cache instance.

    Returns:
        LLMCache: The global cache instance

    Raises:
        RuntimeError: If cache hasn't been initialized
    """
    global llm_cache
    if llm_cache is None:
        # Auto-initialize with defaults
        llm_cache = initialize_cache()
    return llm_cache


def shutdown_cache():
    """
    Shutdown the LLM cache.

    Call this during application shutdown to persist cache.
    """
    global llm_cache
    if llm_cache is not None:
        if llm_cache.persist_path:
            llm_cache._save_to_disk()
        llm_cache = None


# Decorator for automatic caching
def cached_llm_call(model: str):
    """
    Decorator to automatically cache LLM API calls.

    Usage:
        @cached_llm_call(model="gpt-4")
        def generate_sql(query: str, schema: dict) -> str:
            # ... call LLM API
            return sql

    Args:
        model: LLM model identifier
    """
    def decorator(func):
        def wrapper(query: str, schema: Dict[str, Any], *args, **kwargs):
            cache = get_cache()

            # Try cache first
            cached_result = cache.get(query, schema, model)
            if cached_result is not None:
                return cached_result

            # Cache miss - call function
            result = func(query, schema, *args, **kwargs)

            # Cache result
            cache.set(query, schema, model, result)

            return result

        return wrapper
    return decorator
