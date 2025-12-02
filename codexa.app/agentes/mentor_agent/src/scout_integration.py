"""
SCOUT Integration Module - Pre-Task Repository Context.

• PURPOSE ▸ Enable all agents to auto-consult SCOUT for repository context before executing tasks, creating verticalized knowledge navigation through entropic annotation discovery → Reference adw_scout.py for annotation semantics and query_organization patterns

This module provides utilities for agents to automatically leverage SCOUT
as a pre-preparation step before executing any task.

INTEGRATION PHILOSOPHY:
- Every agent should "know the territory" before acting
- SCOUT provides entropic guidance system for code navigation
- Vertical consultation chains through PURPOSE annotations
- Zero-cost cache-based lookups for performance

USAGE PATTERNS:

1. **Pre-Task Scan** (Recommended for all agents):
   ```python
   from adw_modules.scout_integration import prepare_scout_context

   # At the beginning of any agent task
   scout_context = await prepare_scout_context(working_dir=".")
   # Now you have repository structure and annotations
   ```

2. **Query-Driven Navigation**:
   ```python
   from adw_modules.scout_integration import query_scout

   # Ask SCOUT where to find or place something
   result = await query_scout(
       "Where should I implement authentication handlers?",
       working_dir="."
   )
   ```

3. **Automatic Integration** (For new agents):
   ```python
   from adw_modules.scout_integration import with_scout_context

   @with_scout_context
   async def my_agent_function(task_input, scout_context=None):
       # scout_context automatically populated
       related_files = scout_context.get('related_files', [])
       # ... your agent logic
   ```
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta
from functools import wraps

# Import SCOUT components
# Add parent directory to path to import scout modules
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from adw_scout import ScoutRepository, query_organization, SCAN_CACHE
except ImportError:
    # Fallback if running from different context
    ScoutRepository = None
    query_organization = None
    SCAN_CACHE = ".scout_cache.json"


# ============================================================================
# CONFIGURATION
# ============================================================================

class ScoutIntegrationConfig:
    """Configuration for SCOUT integration."""

    # Cache settings
    CACHE_EXPIRY_HOURS = 24  # Re-scan if cache older than 24 hours
    AUTO_SCAN_ON_MISS = True  # Automatically scan if no cache exists

    # Performance settings
    ASYNC_SCAN = True  # Run scans asynchronously
    TIMEOUT_SECONDS = 30  # Timeout for SCOUT operations

    # Integration behavior
    ENABLE_AUTO_CONTEXT = True  # Enable automatic context injection
    VERBOSE_LOGGING = False  # Log SCOUT operations


# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def is_cache_fresh(cache_path: str, max_age_hours: int = 24) -> bool:
    """Check if SCOUT cache exists and is fresh enough to use.

    Args:
        cache_path: Path to the cache file
        max_age_hours: Maximum age in hours before cache is stale

    Returns:
        True if cache exists and is fresh, False otherwise
    """
    if not os.path.exists(cache_path):
        return False

    try:
        # Check file modification time
        cache_time = datetime.fromtimestamp(os.path.getmtime(cache_path))
        age = datetime.now() - cache_time

        return age < timedelta(hours=max_age_hours)
    except Exception:
        return False


async def run_scout_scan(
    working_dir: str = ".",
    use_cache: bool = True,
    timeout: int = 30
) -> Dict[str, Any]:
    """Run SCOUT scan to build repository structure map.

    Args:
        working_dir: Working directory to scan
        use_cache: Whether to use cached results if available
        timeout: Timeout in seconds

    Returns:
        Dictionary with scan results or error information
    """
    cache_path = os.path.join(working_dir, SCAN_CACHE)

    # Check if we can use cache
    if use_cache and is_cache_fresh(cache_path, ScoutIntegrationConfig.CACHE_EXPIRY_HOURS):
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
                return {
                    'success': True,
                    'from_cache': True,
                    'structure': cache_data.get('structure', {}),
                    'annotations': cache_data.get('annotations', {}),
                    'timestamp': cache_data.get('timestamp'),
                }
        except Exception as e:
            # Cache read failed, fall through to scan
            pass

    # Run SCOUT scan command
    scout_script = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "adw_scout.py"
    )

    if not os.path.exists(scout_script):
        return {
            'success': False,
            'error': 'SCOUT script not found',
            'from_cache': False
        }

    try:
        # Run scan via subprocess
        cmd = [
            sys.executable,
            scout_script,
            "scan",
            "--target", working_dir,
            "--cache"
        ]

        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            return {
                'success': False,
                'error': 'SCOUT scan timed out',
                'from_cache': False
            }

        if process.returncode == 0:
            # Load the cache that was just created
            try:
                with open(cache_path, 'r') as f:
                    cache_data = json.load(f)
                    return {
                        'success': True,
                        'from_cache': False,
                        'structure': cache_data.get('structure', {}),
                        'annotations': cache_data.get('annotations', {}),
                        'timestamp': cache_data.get('timestamp'),
                    }
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Failed to read scan results: {str(e)}',
                    'from_cache': False
                }
        else:
            error_msg = stderr.decode() if stderr else 'Unknown error'
            return {
                'success': False,
                'error': f'SCOUT scan failed: {error_msg}',
                'from_cache': False
            }

    except Exception as e:
        return {
            'success': False,
            'error': f'Failed to run SCOUT: {str(e)}',
            'from_cache': False
        }


async def query_scout(
    query_text: str,
    working_dir: str = ".",
    model: str = "sonnet"
) -> Dict[str, Any]:
    """Query SCOUT about repository organization.

    Args:
        query_text: Question to ask SCOUT
        working_dir: Working directory
        model: Model to use (sonnet or opus)

    Returns:
        Query result dictionary
    """
    # Ensure we have a fresh scan
    scan_result = await run_scout_scan(working_dir=working_dir)

    if not scan_result.get('success'):
        return {
            'success': False,
            'error': 'Failed to scan repository before query'
        }

    # Use the imported function if available
    if query_organization:
        try:
            repo = ScoutRepository(working_dir)
            repo.load_cache()

            result = query_organization(query_text, repo, model=model)
            return {
                'success': True,
                'result': result
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Query failed: {str(e)}'
            }
    else:
        # Fallback: run via subprocess
        scout_script = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "adw_scout.py"
        )

        try:
            cmd = [
                sys.executable,
                scout_script,
                "query",
                query_text,
                "--target", working_dir,
                "--model", model
            ]

            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=ScoutIntegrationConfig.TIMEOUT_SECONDS
            )

            if process.returncode == 0:
                return {
                    'success': True,
                    'result': stdout.decode()
                }
            else:
                return {
                    'success': False,
                    'error': stderr.decode()
                }

        except Exception as e:
            return {
                'success': False,
                'error': f'Query execution failed: {str(e)}'
            }


async def prepare_scout_context(
    working_dir: str = ".",
    auto_scan: bool = True
) -> Dict[str, Any]:
    """Prepare SCOUT context for agent execution.

    This is the main function agents should call at the beginning of tasks.

    Args:
        working_dir: Working directory to analyze
        auto_scan: Automatically scan if no cache exists

    Returns:
        Dictionary with repository context including:
        - structure: Repository structure
        - annotations: PURPOSE annotations
        - stats: Repository statistics
        - from_cache: Whether loaded from cache
    """
    if not ScoutIntegrationConfig.ENABLE_AUTO_CONTEXT:
        return {'enabled': False}

    scan_result = await run_scout_scan(
        working_dir=working_dir,
        use_cache=True
    )

    if not scan_result.get('success'):
        if auto_scan and ScoutIntegrationConfig.AUTO_SCAN_ON_MISS:
            # Try one more time without cache
            scan_result = await run_scout_scan(
                working_dir=working_dir,
                use_cache=False
            )

    return {
        'enabled': True,
        'success': scan_result.get('success', False),
        'structure': scan_result.get('structure', {}),
        'annotations': scan_result.get('annotations', {}),
        'stats': scan_result.get('structure', {}).get('stats', {}),
        'from_cache': scan_result.get('from_cache', False),
        'timestamp': scan_result.get('timestamp'),
    }


def with_scout_context(func):
    """Decorator to automatically inject SCOUT context into agent functions.

    Usage:
        @with_scout_context
        async def my_agent(task_input, scout_context=None):
            # scout_context is automatically populated
            files = scout_context.get('structure', {}).get('files', [])
            ...
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Determine working directory
        working_dir = kwargs.get('working_dir', '.')

        # Prepare SCOUT context
        scout_context = await prepare_scout_context(working_dir=working_dir)

        # Inject into kwargs
        kwargs['scout_context'] = scout_context

        # Call original function
        return await func(*args, **kwargs)

    return wrapper


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def extract_related_files(
    scout_context: Dict[str, Any],
    pattern: Optional[str] = None,
    extension: Optional[str] = None
) -> List[str]:
    """Extract related files from SCOUT context based on criteria.

    Args:
        scout_context: SCOUT context from prepare_scout_context()
        pattern: File pattern to match (e.g., "*agent*")
        extension: File extension to filter (e.g., ".py")

    Returns:
        List of matching file paths
    """
    if not scout_context.get('success'):
        return []

    files = scout_context.get('structure', {}).get('files', [])

    if pattern:
        from fnmatch import fnmatch
        files = [f for f in files if fnmatch(f, pattern)]

    if extension:
        files = [f for f in files if f.endswith(extension)]

    return files


def get_repository_stats(scout_context: Dict[str, Any]) -> Dict[str, Any]:
    """Get repository statistics from SCOUT context.

    Args:
        scout_context: SCOUT context from prepare_scout_context()

    Returns:
        Dictionary with statistics
    """
    return scout_context.get('stats', {})


# ============================================================================
# SYNCHRONOUS WRAPPERS (for non-async code)
# ============================================================================

def prepare_scout_context_sync(working_dir: str = ".") -> Dict[str, Any]:
    """Synchronous version of prepare_scout_context.

    For use in non-async code. Uses asyncio.run() internally.
    """
    return asyncio.run(prepare_scout_context(working_dir=working_dir))


def query_scout_sync(
    query_text: str,
    working_dir: str = ".",
    model: str = "sonnet"
) -> Dict[str, Any]:
    """Synchronous version of query_scout.

    For use in non-async code. Uses asyncio.run() internally.
    """
    return asyncio.run(query_scout(query_text, working_dir=working_dir, model=model))
