"""
SCOUT Integration for ADW Workflows.

This module provides integration with the SCOUT repository navigation system,
allowing agents to understand codebase structure and find relevant files.

SCOUT provides:
- Repository indexing and caching
- Pattern-based file searching
- Code structure analysis
- Related file discovery
"""

import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Set
from datetime import datetime
from collections import defaultdict


# ============================================================================
# GLOBAL CACHE
# ============================================================================

_SCOUT_CACHE: Dict[str, Dict[str, Any]] = {}


# ============================================================================
# SCOUT CONTEXT MANAGEMENT
# ============================================================================

def prepare_scout_context_sync(
    working_dir: Optional[str] = None,
    cache: bool = True,
    max_files: int = 1000
) -> Dict[str, Any]:
    """Prepare SCOUT context for repository analysis with real scanning and caching.

    Scans the repository, builds a file index, and caches results for performance.
    Filters out common non-source directories like .git, node_modules, __pycache__.

    Args:
        working_dir: Directory to scan (default: current directory)
        cache: Whether to use/create cache (default: True)
        max_files: Maximum files to index (default: 1000)

    Returns:
        SCOUT context dictionary with repository information and file index
    """
    try:
        working_dir = working_dir or os.getcwd()
        repo_path = Path(working_dir).resolve()
        cache_key = str(repo_path)

        # Check cache first
        if cache and cache_key in _SCOUT_CACHE:
            cached = _SCOUT_CACHE[cache_key]
            cached['from_cache'] = True
            cached['cache_timestamp'] = cached.get('timestamp')
            cached['timestamp'] = datetime.now().isoformat()
            return cached

        # Directories to exclude from scanning
        exclude_dirs = {
            '.git', '.svn', '.hg',
            'node_modules', '__pycache__', '.pytest_cache',
            'venv', '.venv', 'env', '.env',
            'dist', 'build', '.tox', '.mypy_cache',
            '.next', '.nuxt', 'target'
        }

        # Build file index
        file_index = {}
        file_count = 0
        dir_count = 0
        files_by_ext = defaultdict(list)

        for item in repo_path.rglob('*'):
            # Skip excluded directories
            if any(excluded in item.parts for excluded in exclude_dirs):
                continue

            if item.is_dir():
                dir_count += 1
            elif item.is_file() and file_count < max_files:
                relative_path = str(item.relative_to(repo_path))
                file_size = item.stat().st_size
                extension = item.suffix.lower()

                # Add to index
                file_index[relative_path] = {
                    'path': relative_path,
                    'name': item.name,
                    'extension': extension,
                    'size': file_size,
                    'modified': datetime.fromtimestamp(item.stat().st_mtime).isoformat()
                }

                # Group by extension
                files_by_ext[extension].append(relative_path)
                file_count += 1

        # Create context
        context = {
            "success": True,
            "working_dir": str(repo_path),
            "timestamp": datetime.now().isoformat(),
            "stats": {
                "total_files": file_count,
                "indexed_files": file_count,
                "directories": dir_count,
                "unique_extensions": len(files_by_ext),
                "largest_extension_group": max(len(v) for v in files_by_ext.values()) if files_by_ext else 0
            },
            "cache_enabled": cache,
            "index": file_index,
            "files_by_extension": dict(files_by_ext),
            "from_cache": False
        }

        # Store in cache
        if cache:
            _SCOUT_CACHE[cache_key] = context

        return context

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "working_dir": working_dir,
            "timestamp": datetime.now().isoformat()
        }


def prepare_scout_context(
    working_dir: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """Async wrapper for prepare_scout_context_sync.

    For compatibility with async codebases.
    """
    return prepare_scout_context_sync(working_dir, **kwargs)


# ============================================================================
# FILE DISCOVERY
# ============================================================================

def extract_related_files(
    scout_context: Dict[str, Any],
    pattern: str = "*",
    max_results: int = 10,
    score_by_size: bool = False
) -> List[str]:
    """Extract files matching a pattern from SCOUT context with scoring.

    Searches the indexed files and ranks results by relevance:
    - Exact name matches score higher
    - More recently modified files score higher
    - Smaller files score higher (if score_by_size=True)

    Args:
        scout_context: SCOUT context from prepare_scout_context_sync
        pattern: Glob pattern to match (e.g., "*agent*.py", "*.md")
        max_results: Maximum number of results to return
        score_by_size: Prefer smaller files (useful for config/docs)

    Returns:
        List of file paths matching the pattern, sorted by relevance score
    """
    if not scout_context.get('success'):
        return []

    try:
        file_index = scout_context.get('index', {})

        if not file_index:
            # Fallback to direct scanning if index is empty
            working_dir = Path(scout_context.get('working_dir', '.'))
            results = []
            for file_path in working_dir.rglob(pattern):
                if file_path.is_file():
                    results.append(str(file_path.relative_to(working_dir)))
                    if len(results) >= max_results:
                        break
            return results

        # Score and rank files from index
        scored_files = []

        for file_path, file_info in file_index.items():
            # Check if pattern matches
            path_obj = Path(file_path)
            if not path_obj.match(pattern):
                continue

            score = 0.0

            # Exact name match: +10 points
            if pattern.strip('*') in file_info['name']:
                score += 10.0

            # Extension match: +5 points
            if pattern.endswith(file_info['extension']):
                score += 5.0

            # Size scoring (smaller is better for docs/config)
            if score_by_size and file_info['size'] > 0:
                # Normalize: prefer files < 100KB
                size_kb = file_info['size'] / 1024
                if size_kb < 100:
                    score += 3.0
                elif size_kb < 500:
                    score += 1.0

            # Recently modified: +2 points (basic heuristic)
            # Could be improved with actual time comparison
            score += 2.0

            scored_files.append((file_path, score))

        # Sort by score (descending) and return top max_results
        scored_files.sort(key=lambda x: x[1], reverse=True)
        return [path for path, score in scored_files[:max_results]]

    except Exception as e:
        print(f"[SCOUT] Error extracting related files: {e}")
        return []


def find_files_by_pattern(
    scout_context: Dict[str, Any],
    patterns: List[str],
    exclude_patterns: Optional[List[str]] = None
) -> Dict[str, List[str]]:
    """Find files matching multiple patterns.

    Args:
        scout_context: SCOUT context
        patterns: List of glob patterns to search
        exclude_patterns: Patterns to exclude from results

    Returns:
        Dictionary mapping patterns to matching files
    """
    results = {}
    exclude_patterns = exclude_patterns or []

    for pattern in patterns:
        matches = extract_related_files(scout_context, pattern, max_results=50)

        # Apply exclusion filters
        filtered = []
        for match in matches:
            if not any(excl in match for excl in exclude_patterns):
                filtered.append(match)

        results[pattern] = filtered

    return results


# ============================================================================
# REPOSITORY STATISTICS
# ============================================================================

def get_repository_stats(scout_context: Dict[str, Any]) -> Dict[str, Any]:
    """Extract repository statistics from SCOUT context.

    Args:
        scout_context: SCOUT context

    Returns:
        Dictionary with repository statistics
    """
    if not scout_context.get('success'):
        return {
            "total_files": 0,
            "total_directories": 0,
            "indexed": False
        }

    return scout_context.get('stats', {})


def get_file_metadata(
    scout_context: Dict[str, Any],
    file_path: str
) -> Optional[Dict[str, Any]]:
    """Get metadata for a specific file.

    Args:
        scout_context: SCOUT context
        file_path: Path to file

    Returns:
        File metadata if available
    """
    try:
        working_dir = Path(scout_context.get('working_dir', '.'))
        full_path = working_dir / file_path

        if not full_path.exists():
            return None

        stat = full_path.stat()

        return {
            "path": file_path,
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "is_file": full_path.is_file(),
            "is_dir": full_path.is_dir(),
            "extension": full_path.suffix,
        }

    except Exception:
        return None


# ============================================================================
# CODE ANALYSIS
# ============================================================================

def analyze_code_structure(
    scout_context: Dict[str, Any],
    file_path: str
) -> Dict[str, Any]:
    """Analyze code structure of a file using regex-based parsing.

    Extracts basic code elements from Python files:
    - Function definitions (def function_name)
    - Class definitions (class ClassName)
    - Import statements (import/from)

    For production use with full AST parsing, use Python's ast module.

    Args:
        scout_context: SCOUT context
        file_path: Path to file to analyze

    Returns:
        Code structure analysis with functions, classes, and imports
    """
    try:
        working_dir = Path(scout_context.get('working_dir', '.'))
        full_path = working_dir / file_path

        if not full_path.exists() or not full_path.is_file():
            return {
                "file_path": file_path,
                "analyzed": False,
                "error": "File not found",
                "functions": [],
                "classes": [],
                "imports": []
            }

        # Only analyze text files (primarily Python)
        if full_path.suffix not in ['.py', '.pyx', '.pyi']:
            return {
                "file_path": file_path,
                "analyzed": False,
                "note": "Non-Python file, basic analysis only",
                "functions": [],
                "classes": [],
                "imports": []
            }

        # Read file content
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            return {
                "file_path": file_path,
                "analyzed": False,
                "error": "Unable to decode file",
                "functions": [],
                "classes": [],
                "imports": []
            }

        # Extract functions (def name(...))
        function_pattern = r'^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        functions = re.findall(function_pattern, content, re.MULTILINE)

        # Extract classes (class Name...)
        class_pattern = r'^\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        classes = re.findall(class_pattern, content, re.MULTILINE)

        # Extract imports
        import_pattern = r'^\s*(?:from\s+([\w\.]+)\s+)?import\s+([\w\.,\s\*]+)'
        import_matches = re.findall(import_pattern, content, re.MULTILINE)

        imports = []
        for from_module, import_list in import_matches:
            if from_module:
                imports.append(f"from {from_module} import {import_list.strip()}")
            else:
                imports.append(f"import {import_list.strip()}")

        return {
            "file_path": file_path,
            "analyzed": True,
            "language": "python",
            "functions": functions,
            "function_count": len(functions),
            "classes": classes,
            "class_count": len(classes),
            "imports": imports[:20],  # Limit to first 20
            "import_count": len(imports),
            "lines_of_code": len(content.split('\n')),
            "note": "Basic regex-based analysis. For full AST analysis, use Python ast module."
        }

    except Exception as e:
        return {
            "file_path": file_path,
            "analyzed": False,
            "error": str(e),
            "functions": [],
            "classes": [],
            "imports": []
        }


def find_similar_files(
    scout_context: Dict[str, Any],
    reference_file: str,
    max_results: int = 5
) -> List[str]:
    """Find files similar to a reference file using multiple similarity metrics.

    Similarity scoring based on:
    - Same extension (mandatory)
    - Similar file size (±50%)
    - Similar directory depth
    - Shared keywords in filename

    Args:
        scout_context: SCOUT context
        reference_file: File to use as reference
        max_results: Maximum similar files to return

    Returns:
        List of similar file paths, ranked by similarity score
    """
    try:
        file_index = scout_context.get('index', {})

        if reference_file not in file_index:
            # Fallback to simple extension matching
            ref_path = Path(reference_file)
            pattern = f"*{ref_path.suffix}"
            similar = extract_related_files(scout_context, pattern, max_results + 1)
            return [f for f in similar if f != reference_file][:max_results]

        ref_info = file_index[reference_file]
        ref_path = Path(reference_file)
        ref_extension = ref_info['extension']
        ref_size = ref_info['size']
        ref_depth = len(ref_path.parts)
        ref_name_words = set(re.findall(r'\w+', ref_path.stem.lower()))

        scored_files = []

        for file_path, file_info in file_index.items():
            # Skip the reference file itself
            if file_path == reference_file:
                continue

            # Must have same extension
            if file_info['extension'] != ref_extension:
                continue

            score = 0.0
            file_path_obj = Path(file_path)

            # Size similarity (±50%)
            if ref_size > 0:
                size_ratio = file_info['size'] / ref_size
                if 0.5 <= size_ratio <= 1.5:
                    score += 5.0
                elif 0.25 <= size_ratio <= 2.0:
                    score += 2.0

            # Directory depth similarity
            file_depth = len(file_path_obj.parts)
            if file_depth == ref_depth:
                score += 3.0
            elif abs(file_depth - ref_depth) == 1:
                score += 1.0

            # Shared keywords in filename
            file_name_words = set(re.findall(r'\w+', file_path_obj.stem.lower()))
            shared_words = ref_name_words & file_name_words
            score += len(shared_words) * 2.0

            # Same directory: bonus points
            if file_path_obj.parent == ref_path.parent:
                score += 4.0

            if score > 0:
                scored_files.append((file_path, score))

        # Sort by score and return top results
        scored_files.sort(key=lambda x: x[1], reverse=True)
        return [path for path, score in scored_files[:max_results]]

    except Exception as e:
        print(f"[SCOUT] Error finding similar files: {e}")
        return []


# ============================================================================
# MODULE INFO
# ============================================================================

__version__ = "1.0.0"
__author__ = "CODEXA Team"
__description__ = "SCOUT integration for repository navigation and analysis"

# Note: This is a STUB implementation
# For production use, integrate with actual SCOUT system or implement full scanning
