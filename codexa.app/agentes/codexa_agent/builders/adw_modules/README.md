# ADW Modules - Agent Development Workflow Utilities

> **Purpose**: Production-ready shared utilities for CODEXA builder scripts
> **Version**: 1.2.0
> **Status**: ✅ FUNCTIONAL

---

## Overview

This package provides production-ready functionality for all CODEXA builder scripts including:
- Agent execution with structured output and retry logic
- Repository scanning with caching and code analysis
- Formatting utilities for workflow displays

## Modules

### agent.py
Core agent execution and workflow management with production-ready implementations.

**Key Components**:
- `AgentTemplateRequest` - Request model for slash command execution
- `AgentPromptRequest` - Request model for direct prompts
- `AgentPromptResponse` - Response model with execution results and metadata
- `execute_template()` - Execute commands with structured output and metadata
- `prompt_claude_code()` - Execute prompts with validation and context files
- `prompt_claude_code_with_retry()` - Execute with exponential backoff retry logic
- `generate_short_id()` - Generate unique workflow IDs
- `save_workflow_state()` / `load_workflow_state()` - State persistence

**Status**: ✅ FUNCTIONAL
- ✅ Structured output with JSON metadata for $argument chaining
- ✅ Input validation and error handling
- ✅ Exponential backoff retry (1s → 2s → 4s)
- ✅ Execution timing and traceability

### scout_integration.py
Repository navigation and code analysis with real scanning and caching.

**Key Components**:
- `prepare_scout_context_sync()` - Scan repository and build index with caching
- `extract_related_files()` - Pattern matching with relevance scoring
- `find_files_by_pattern()` - Multi-pattern search with exclusions
- `get_repository_stats()` - Repository statistics
- `analyze_code_structure()` - Extract functions/classes/imports from Python files
- `find_similar_files()` - Multi-metric similarity analysis

**Status**: ✅ FUNCTIONAL
- ✅ Global in-memory cache for fast access
- ✅ Excludes common non-source directories (.git, node_modules, etc.)
- ✅ Relevance scoring for search results
- ✅ Regex-based code parsing for Python
- ✅ Similarity detection by size, depth, keywords

### utils.py
Formatting and helper utilities.

**Key Components**:
- `format_agent_status()` - Format agent status messages
- `format_worktree_status()` - Format git worktree info
- `format_phase_summary()` - Format workflow phase summaries
- `format_duration()` - Human-readable time formatting
- `validate_adw_id()` - Validate workflow IDs
- `create_status_emoji()` - Get status emojis
- `color_by_status()` - Rich console colors

**Status**: ✅ FUNCTIONAL

---

## Installation

These modules are automatically available to builder scripts through Python path manipulation:

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "adw_modules"))

from agent import execute_template, AgentTemplateRequest
from scout_integration import prepare_scout_context_sync
from utils import format_agent_status
```

---

## Usage Examples

### Executing a Template Command

```python
from agent import AgentTemplateRequest, execute_template

request = AgentTemplateRequest(
    command="/plan",
    agent_name="planner-abc123",
    adw_id="abc123",
    model="opus",
    working_dir="/path/to/project"
)

response = execute_template(request)

if response.success:
    print(f"Output: {response.output}")
else:
    print(f"Error: {response.error}")
```

### Repository Analysis

```python
from scout_integration import (
    prepare_scout_context_sync,
    extract_related_files,
    get_repository_stats
)

# Prepare context
context = prepare_scout_context_sync(working_dir=".")

# Get stats
stats = get_repository_stats(context)
print(f"Total files: {stats['total_files']}")

# Find related files
agent_files = extract_related_files(context, pattern="*agent*.py")
print(f"Found {len(agent_files)} agent files")
```

### Status Formatting

```python
from utils import format_agent_status, format_duration

status = format_agent_status(
    agent_name="builder-xyz",
    status="running",
    phase="construction",
    details="Building artifacts..."
)
print(status)

duration = format_duration(125.5)
print(f"Completed in {duration}")  # "2m 5s"
```

---

## Features & Capabilities

### agent.py
- ✅ **Structured Output** - JSON metadata for $argument chaining between phases
- ✅ **Input Validation** - Validates prompts and parameters before execution
- ✅ **Context Management** - Handles working directories and context files
- ✅ **Retry Logic** - Exponential backoff (1s → 2s → 4s) for transient failures
- ✅ **Execution Tracking** - Timing, session IDs, and retry counts
- ✅ **State Persistence** - Save/load workflow state to disk

### scout_integration.py
- ✅ **Real Repository Scanning** - Indexes files with metadata (size, modified date)
- ✅ **Memory Cache** - Fast repeated access with global cache
- ✅ **Smart Filtering** - Excludes .git, node_modules, __pycache__, etc.
- ✅ **Relevance Scoring** - Ranks search results by name match, size, recency
- ✅ **Code Analysis** - Extracts functions, classes, imports from Python files
- ✅ **Similarity Detection** - Multi-metric similarity (size, depth, keywords, directory)

### Known Limitations

1. **Language Support**: Code analysis currently Python-only (regex-based)
   - Enhancement: Add full AST parsing with Python `ast` module
   - Enhancement: Add support for JavaScript, TypeScript, Go, etc.

2. **Execution Model**: Provides structured output for workflow chaining
   - Enhancement: Direct Claude Code CLI subprocess integration
   - Current: Works independently without CLI dependency

3. **Cache Invalidation**: In-memory cache persists for session
   - Enhancement: Add TTL and automatic invalidation on file changes
   - Current: Cache clears on process restart

---

## Dependencies

These modules use only standard library by default, but require additional packages when used by builder scripts:

- `pydantic` - Data validation (used by builders via PEP 723)
- `python-dotenv` - Environment configuration (optional)
- `click` - CLI framework (used by builders)
- `rich` - Terminal formatting (used by builders)

Builder scripts manage their own dependencies via PEP 723 inline metadata.

---

## Development

### Adding New Utilities

1. Add function to appropriate module (`agent.py`, `scout_integration.py`, or `utils.py`)
2. Export in `__init__.py`
3. Add to `__all__` list
4. Update this README with usage example

### Testing

```bash
# Test imports
python -c "from adw_modules import *; print('All imports successful')"

# Test builder scripts
python builders/02_agent_meta_constructor.py --help
python builders/08_prompt_generator.py --help
```

---

## Roadmap

### Completed (v1.2.0)
- [x] Implement structured output for $argument chaining
- [x] Add real repository scanning with caching
- [x] Implement regex-based code analysis for Python
- [x] Add relevance scoring for file search
- [x] Implement exponential backoff retry logic
- [x] Add execution timing and metadata

### Planned Enhancements
- [ ] Full AST parsing for Python (use `ast` module)
- [ ] Multi-language support (JavaScript, TypeScript, Go)
- [ ] Direct Claude Code CLI subprocess integration
- [ ] Cache TTL and automatic invalidation
- [ ] Comprehensive test suite
- [ ] Performance optimization for large repositories

---

**Version**: 1.2.0
**Created**: 2025-11-13
**Last Updated**: 2025-11-13
**Status**: ✅ FUNCTIONAL - Production-ready implementations for all core functionality
