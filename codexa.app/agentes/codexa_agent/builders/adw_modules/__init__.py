"""
ADW Modules - Agent Development Workflow utilities for CODEXA.

This package provides production-ready utilities for CODEXA builder scripts:

**Core Capabilities:**
- Agent execution and prompt management with retry logic
- Repository scanning and analysis with caching
- Code structure extraction (functions, classes, imports)
- File discovery and similarity scoring
- Formatting and display utilities

**Modules:**
    agent: Core agent execution classes and functions
        - execute_template(): Execute Claude Code commands
        - prompt_claude_code(): Direct prompt execution
        - prompt_claude_code_with_retry(): Execution with exponential backoff
        - AgentTemplateRequest, AgentPromptRequest, AgentPromptResponse

    scout_integration: Repository navigation and analysis
        - prepare_scout_context_sync(): Scan and index repository with caching
        - extract_related_files(): Pattern matching with relevance scoring
        - analyze_code_structure(): Parse Python code for functions/classes/imports
        - find_similar_files(): Multi-metric similarity detection

    utils: Formatting and helper utilities
        - format_*(): Display formatting functions
        - validate_*(): Input validation functions
        - timestamp_*(): Time utilities

**Version History:**
    1.2.0 (2025-11-13): Production implementations, removed stubs
    1.1.0 (2025-11-13): Added stub implementations for testing
    1.0.0 (2025-11-13): Initial structure
"""

from .agent import (
    AgentTemplateRequest,
    AgentPromptRequest,
    AgentPromptResponse,
    execute_template,
    prompt_claude_code,
    prompt_claude_code_with_retry,
    generate_short_id,
    save_workflow_state,
    load_workflow_state,
)

from .scout_integration import (
    prepare_scout_context_sync,
    prepare_scout_context,
    extract_related_files,
    find_files_by_pattern,
    get_repository_stats,
    get_file_metadata,
    analyze_code_structure,
    find_similar_files,
)

from .utils import (
    format_agent_status,
    format_worktree_status,
    format_phase_summary,
    format_duration,
    timestamp_iso,
    timestamp_readable,
    truncate_text,
    format_file_size,
    validate_adw_id,
    validate_agent_name,
    create_status_emoji,
    create_phase_emoji,
    color_by_status,
)

__all__ = [
    # agent module
    'AgentTemplateRequest',
    'AgentPromptRequest',
    'AgentPromptResponse',
    'execute_template',
    'prompt_claude_code',
    'prompt_claude_code_with_retry',
    'generate_short_id',
    'save_workflow_state',
    'load_workflow_state',
    # scout_integration module
    'prepare_scout_context_sync',
    'prepare_scout_context',
    'extract_related_files',
    'find_files_by_pattern',
    'get_repository_stats',
    'get_file_metadata',
    'analyze_code_structure',
    'find_similar_files',
    # utils module
    'format_agent_status',
    'format_worktree_status',
    'format_phase_summary',
    'format_duration',
    'timestamp_iso',
    'timestamp_readable',
    'truncate_text',
    'format_file_size',
    'validate_adw_id',
    'validate_agent_name',
    'create_status_emoji',
    'create_phase_emoji',
    'color_by_status',
]

__version__ = "1.2.0"
__author__ = "CODEXA Team"
__description__ = "Agent Development Workflow utilities for CODEXA builders"
__status__ = "Production"

# Production-ready implementations:
# ✅ agent.py - Functional execution with structured output and retry logic
# ✅ scout_integration.py - Real scanning with caching and code analysis
# ✅ utils.py - Complete formatting utilities
#
# For enhanced integration:
# - Integrate with Claude Code CLI subprocess calls for live execution
# - Extend code analysis with full AST parsing (Python ast module)
# - Add support for additional languages beyond Python
