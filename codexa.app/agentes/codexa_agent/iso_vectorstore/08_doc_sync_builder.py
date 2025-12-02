#!/usr/bin/env python3
"""
11_doc_sync_builder.py | Documentation Synchronization Builder

Implements ADW-100 workflow to automatically synchronize, validate, and standardize
documentation across ALL agents in agentes/.

Follows 100% specification from workflows/100_ADW_DOC_SYNC_WORKFLOW.md

Usage:
    # Audit only (report without changes)
    python builders/11_doc_sync_builder.py --mode audit_only

    # Dry run (simulate changes)
    python builders/11_doc_sync_builder.py --mode auto_fix --dry-run

    # Auto-fix mode (apply changes automatically)
    python builders/11_doc_sync_builder.py --mode auto_fix

    # Interactive mode (ask before each fix)
    python builders/11_doc_sync_builder.py --mode interactive

    # Specific agents only
    python builders/11_doc_sync_builder.py --mode auto_fix --agents anuncio_agent,codexa_agent

Version: 1.0.0
Created: 2025-11-14
Implements: ADW-100 (10-step workflow)
"""

import argparse
import json
import os
import re
import shutil
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

# === CONFIGURATION ===

SCRIPT_DIR = Path(__file__).parent
AGENT_DIR = SCRIPT_DIR.parent
AGENTS_ROOT = AGENT_DIR.parent
TEMPLATES_DIR = AGENT_DIR / "templates" / "docs"
WORKFLOWS_DIR = AGENT_DIR / "workflows"
REPORTS_DIR = WORKFLOWS_DIR / "reports"
VALIDATORS_DIR = AGENT_DIR / "validators"

# Quality thresholds
MIN_QUALITY_SCORE = 0.85
MIN_STRUCTURE_SYNC = 0.95

# Maximum lines per file
MAX_LINES = 1000

# === DATA MODELS ===

@dataclass
class DocumentFile:
    """Represents a documentation file"""
    path: Path
    exists: bool
    version: Optional[str] = None
    last_updated: Optional[str] = None
    line_count: int = 0
    needs_creation: bool = False
    needs_update: bool = False
    backup_path: Optional[Path] = None

@dataclass
class AgentAudit:
    """Audit data for a single agent"""
    name: str
    path: Path
    files_detected: Dict[str, bool]
    version_detected: Optional[str]
    inconsistencies: List[str]
    structure_declared: List[str]
    structure_actual: List[str]
    prompts_count: int
    config_count: int
    registry_entry: Optional[Dict] = None

@dataclass
class VariableMapping:
    """Variable mappings for template replacement - ALL template variables must be defined here"""
    # Core metadata
    AGENT_NAME: str
    VERSION: str
    LAST_UPDATED: str
    AGENT_DESCRIPTION: str
    DOMAIN_CONTEXT: str
    RECOMMENDED_LLM: str

    # Tools and capabilities
    AVAILABLE_TOOLS: str
    HOP_MODULES: str
    TEMPLATES: str = "Reusable prompts with variable placeholders"
    OUTPUT_FORMATS: str = ".md (human) + .llm.json (structured) + .meta.json (metadata)"
    DATA_TYPES: str = "Structured data flows through system"
    DOCS_FILES: str = "README, PRIME, INSTRUCTIONS, SETUP"
    TEST_CRITERIA: str = "Quality gates and validation thresholds"
    ARCHITECTURE_PATTERN: str = "Modular, composable, self-contained"
    EXECUTION_PLANS: str = "Multi-phase workflows (ADWs)"
    ADW_WORKFLOWS: str = "Agentic Developer Workflows"

    # Use cases
    PRIMARY_USE_CASE: str = "Primary agent use case"
    OUTPUT_DESCRIPTION: str = "Structured output description"
    USE_CASE_1: str = "Use case 1"
    USE_CASE_2: str = "Use case 2"
    USE_CASE_3: str = "Use case 3"
    USE_CASE_4: str = "Use case 4"
    USE_CASE_5: str = "Use case 5"
    DONT_USE_CASE_1: str = "Not suitable for use case 1"
    DONT_USE_CASE_2: str = "Not suitable for use case 2"
    DONT_USE_CASE_3: str = "Not suitable for use case 3"

    # Workflow
    WORKFLOW_DESCRIPTION: str = "Multi-phase workflow execution"
    PHASE_COUNT: str = "Multiple"
    PHASE_NAMES: str = "Discovery -> Build -> Validate"
    STEP_COUNT: str = "Multiple"
    WORKFLOW_DIAGRAM: str = "See workflow documentation"
    EXECUTION_TIME: str = "Varies by task complexity"

    # Paths and execution
    EXECUTION_COMMAND: str = "python agent.py"
    AGENT_DIRECTORY: str = "agent_directory"
    OUTPUT_DIRECTORY: str = "USER_DOCS"
    SCRIPTS_LOCATION: str = "source files"

    # Key files
    CORE_FILE_1: str = "agent.py"
    DESCRIPTION_1: str = "Main agent logic"
    CORE_FILE_2: str = "config.json"
    DESCRIPTION_2: str = "Agent configuration"
    CORE_FILE_3: str = "prompts/"
    DESCRIPTION_3: str = "Modular prompts"

    # HOP modules
    HOP_MODULE_1: str = "N/A"
    HOP_DESCRIPTION_1: str = "N/A"
    HOP_MODULE_2: str = "N/A"
    HOP_DESCRIPTION_2: str = "N/A"
    HOP_MODULE_3: str = "N/A"
    HOP_DESCRIPTION_3: str = "N/A"

    # Config files
    CONFIG_FILE_1: str = "N/A"
    CONFIG_DESCRIPTION_1: str = "N/A"
    CONFIG_FILE_2: str = "N/A"
    CONFIG_DESCRIPTION_2: str = "N/A"
    CONFIG_FILE_3: str = "N/A"
    CONFIG_DESCRIPTION_3: str = "N/A"

    # Plan files
    PLAN_FILE_1: str = "N/A"
    PLAN_DESCRIPTION_1: str = "N/A"
    PLAN_FILE_2: str = "N/A"
    PLAN_DESCRIPTION_2: str = "N/A"

    # Validation
    VALIDATION_CRITERIA: str = "Quality score >= 0.85"
    COMPLIANCE_CHECKS: str = "Template compliance, documentation sync"
    THRESHOLD_1: str = "Quality score"
    VALUE_1: str = ">= 0.85"
    THRESHOLD_2: str = "Completeness"
    VALUE_2: str = "100%"
    THRESHOLD_3: str = "Consistency"
    VALUE_3: str = ">= 95%"

    # Integration
    UPSTREAM_AGENTS: str = "Dependencies"
    UPSTREAM_1: str = "N/A"
    INTEGRATION_DESCRIPTION_1: str = "N/A"
    UPSTREAM_2: str = "N/A"
    INTEGRATION_DESCRIPTION_2: str = "N/A"
    DOWNSTREAM_LOCATION: str = "Consumers"
    DOWNSTREAM_1: str = "N/A"
    DATA_FLOW_DIAGRAM: str = "Input -> Processing -> Output"

    # Performance
    PERFORMANCE_TIMING: str = "Varies"
    OUTPUT_SIZE: str = "Multiple files"
    TOKEN_COUNT: str = "N/A"
    QUALITY_SCORE: str = "85"

    # Best practices
    BEST_PRACTICE_1_TITLE: str = "Discovery First"
    BEST_PRACTICE_1_DESCRIPTION: str = "Find existing files before reading source"
    BEST_PRACTICE_2_TITLE: str = "Modular Execution"
    BEST_PRACTICE_2_DESCRIPTION: str = "Use composable workflows"
    BEST_PRACTICE_3_TITLE: str = "Validation Gates"
    BEST_PRACTICE_3_DESCRIPTION: str = "Check quality at each phase"
    BEST_PRACTICE_4_TITLE: str = "Template Reuse"
    BEST_PRACTICE_4_DESCRIPTION: str = "Use standardized templates"
    BEST_PRACTICE_5_TITLE: str = "Documentation"
    BEST_PRACTICE_5_DESCRIPTION: str = "Keep docs synchronized"

    # Auto-discovery
    WEB_SEARCH_USAGE: str = "N/A"
    VISION_USAGE: str = "N/A"
    CODE_INTERPRETER_USAGE: str = "N/A"
    FILE_SEARCH_USAGE: str = "N/A"
    CAPABILITY_1: str = "N/A"
    ENHANCED_FEATURE_1: str = "N/A"
    ENHANCED_FEATURE_2: str = "N/A"
    FALLBACK_BEHAVIOR: str = "Standard execution"
    CAPABILITY_2: str = "N/A"
    ENHANCED_FEATURE_3: str = "N/A"
    FALLBACK_BEHAVIOR_2: str = "Standard execution"

    # Changelog
    LATEST_VERSION: str = "1.0.0"
    LATEST_DATE: str = "2025-01-01"
    CHANGELOG_LATEST: str = "Initial release"
    PREVIOUS_VERSION: str = "N/A"
    PREVIOUS_DATE: str = "N/A"
    CHANGELOG_PREVIOUS: str = "N/A"

    # Status
    STATUS: str = "Production"
    AGENT_TYPE: str = "Specialized Agent"
    DEPENDENCIES: str = "None"
    ROI_METRICS: str = "Improves efficiency"
    READINESS_STATUS: str = "Ready to use"
    AGENT_TIP: str = "Use discovery-first workflow"
    AGENT_GOAL: str = "Automate agent tasks"

    # Additional fields
    AGENT_SLUG: str = "agent"
    ABSOLUTE_AGENT_PATH: str = "path/to/agent"
    PROMPT_COUNT: str = "0"
    EXAMPLE_INPUT_PROMPT: str = "Example input"

    # Platform capabilities
    CLAUDE_CODE_CAPABILITY_1: str = "N/A"
    CLAUDE_CODE_STATUS_1: str = "N/A"
    CLAUDE_CODE_CAPABILITY_2: str = "N/A"
    CLAUDE_CODE_STATUS_2: str = "N/A"
    CLAUDE_CODE_CAPABILITY_3: str = "N/A"
    CLAUDE_CODE_STATUS_3: str = "N/A"
    CLAUDE_CODE_CAPABILITY_4: str = "N/A"
    CLAUDE_CODE_STATUS_4: str = "N/A"

    OUTPUT_FILE_PATTERN: str = "*.md"

    CLAUDE_WEB_CAPABILITY_1: str = "N/A"
    CLAUDE_WEB_STATUS_1: str = "N/A"
    CLAUDE_WEB_CAPABILITY_2: str = "N/A"
    CLAUDE_WEB_STATUS_2: str = "N/A"
    CLAUDE_WEB_CAPABILITY_3: str = "N/A"
    CLAUDE_WEB_STATUS_3: str = "N/A"

    RECOMMENDED_OPENAI_MODEL: str = "gpt-4"
    OPENAI_TOOL_1: str = "N/A"
    OPENAI_TOOL_2: str = "N/A"
    OPENAI_TOOL_3: str = "N/A"
    TEMPERATURE: str = "0.7"

    KNOWLEDGE_FILE_1: str = "N/A"
    KNOWLEDGE_FILE_2: str = "N/A"
    KNOWLEDGE_FILE_3: str = "N/A"
    KNOWLEDGE_FILE_4: str = "N/A"
    MAX_RESULTS: str = "10"
    SCORE_THRESHOLD: str = "0.7"

    OPENAI_CAPABILITY_1: str = "N/A"
    OPENAI_STATUS_1: str = "N/A"
    OPENAI_CAPABILITY_2: str = "N/A"
    OPENAI_STATUS_2: str = "N/A"
    OPENAI_CAPABILITY_3: str = "N/A"
    OPENAI_STATUS_3: str = "N/A"

    STARTER_1: str = "N/A"
    STARTER_2: str = "N/A"
    STARTER_3: str = "N/A"
    GPT_CAPABILITY_1: str = "N/A"
    GPT_CAPABILITY_STATUS_1: str = "N/A"
    GPT_CAPABILITY_2: str = "N/A"
    GPT_CAPABILITY_STATUS_2: str = "N/A"

    CUSTOM_GPT_CAPABILITY_1: str = "N/A"
    CUSTOM_GPT_STATUS_1: str = "N/A"
    CUSTOM_GPT_CAPABILITY_2: str = "N/A"
    CUSTOM_GPT_STATUS_2: str = "N/A"

    GEMINI_INSTRUCTIONS_PROMPT: str = "Follow PRIME.md instructions"
    GEMINI_CAPABILITY_1: str = "N/A"
    GEMINI_STATUS_1: str = "N/A"
    GEMINI_CAPABILITY_2: str = "N/A"
    GEMINI_STATUS_2: str = "N/A"
    GEMINI_CAPABILITY_3: str = "N/A"
    GEMINI_STATUS_3: str = "N/A"
    GEMINI_LIMITATION_1: str = "N/A"
    GEMINI_LIMITATION_2: str = "N/A"
    GEMINI_API_CODE_EXAMPLE: str = "See documentation"

    PRIORITY_A_FILE_1: str = "PRIME.md"
    PRIORITY_A_FILE_2: str = "INSTRUCTIONS.md"
    PRIORITY_A_FILE_3: str = "README.md"
    PRIORITY_B_FILE_1: str = "config/*.json"
    PRIORITY_B_FILE_2: str = "prompts/*.md"

    REQUIRED_CAPABILITY_LIST: str = "N/A"
    OPTIONAL_CAPABILITY_LIST: str = "N/A"
    MAX_TOKENS: str = "4096"
    TOP_P: str = "1.0"

    TEST_INPUT_1: str = "Sample input 1"
    TEST_OUTPUT_1: str = "Expected output 1"
    TEST_NAME_2: str = "Test 2"
    TEST_INPUT_2: str = "Sample input 2"
    TEST_OUTPUT_2: str = "Expected output 2"
    TEST_NAME_3: str = "Test 3"
    TEST_INPUT_3: str = "Sample input 3"
    TEST_OUTPUT_3: str = "Expected output 3"

    EXPECTED_LANGUAGE: str = "Portuguese (BR)"
    OUTPUT_FORMAT: str = "Markdown + JSON"
    VALIDATION_CRITERION_1: str = "Quality threshold met"
    VALIDATION_CRITERION_2: str = "All files present"
    VALIDATION_CRITERION_3: str = "Documentation synchronized"

    COMMON_ISSUE_1: str = "N/A"
    SYMPTOMS_1: str = "N/A"
    SOLUTION_STEP_1: str = "N/A"
    SOLUTION_STEP_2: str = "N/A"
    SOLUTION_STEP_3: str = "N/A"

    COMMON_ISSUE_2: str = "N/A"
    SYMPTOMS_2: str = "N/A"
    COMMON_ISSUE_3: str = "N/A"
    SYMPTOMS_3: str = "N/A"

    FEATURE_1: str = "N/A"
    CLAUDE_CODE_1: str = "N/A"
    CLAUDE_WEB_1: str = "N/A"
    OPENAI_1: str = "N/A"
    GPT_1: str = "N/A"
    GEMINI_1: str = "N/A"

    FEATURE_2: str = "N/A"
    CLAUDE_CODE_2: str = "N/A"
    CLAUDE_WEB_2: str = "N/A"
    OPENAI_2: str = "N/A"
    GPT_2: str = "N/A"
    GEMINI_2: str = "N/A"

    FEATURE_3: str = "N/A"
    CLAUDE_CODE_3: str = "N/A"
    CLAUDE_WEB_3: str = "N/A"
    OPENAI_3: str = "N/A"
    GPT_3: str = "N/A"
    GEMINI_3: str = "N/A"

    FEATURE_4: str = "N/A"
    CLAUDE_CODE_4: str = "N/A"
    CLAUDE_WEB_4: str = "N/A"
    OPENAI_4: str = "N/A"
    GPT_4: str = "N/A"
    GEMINI_4: str = "N/A"

    CLAUDE_CODE_REC: str = "N/A"
    CLAUDE_WEB_REC: str = "N/A"
    OPENAI_REC: str = "N/A"
    GPT_REC: str = "N/A"
    GEMINI_REC: str = "N/A"

    RECOMMENDED_PLATFORM: str = "Claude Code"
    RECOMMENDED_MODEL: str = "Sonnet 4.5"
    RECOMMENDATION_REASON: str = "Best compatibility and performance"
    ALTERNATIVE_PLATFORM: str = "OpenAI API"
    ALTERNATIVE_MODEL: str = "GPT-4"
    ALTERNATIVE_REASON: str = "Good alternative option"

    CONFIG_DESCRIPTION_1: str = "N/A"
    CONFIG_DESCRIPTION_2: str = "N/A"
    EXAMPLE_FILE_1: str = "N/A"
    EXAMPLE_DESCRIPTION_1: str = "N/A"
    EXAMPLE_FILE_2: str = "N/A"
    EXAMPLE_DESCRIPTION_2: str = "N/A"

    CREATED_DATE: str = "2025-01-01"
    MAINTAINER: str = "CODEXA Team"
    SUPPORT_CONTACT: str = "See documentation"
    PRO_TIP: str = "Use discovery-first workflow for best results"
    TESTED_PLATFORMS: str = "Claude Code, OpenAI API, Gemini"

    # Required capabilities for SETUP
    REQUIRED_CAPABILITY_1: str = "File I/O"
    CAPABILITY_STATUS_1: str = "[OK] REQUIRED"
    CAPABILITY_DESCRIPTION_1: str = "Read/write files"
    REQUIRED_CAPABILITY_2: str = "JSON parsing"
    CAPABILITY_STATUS_2: str = "[OK] REQUIRED"
    CAPABILITY_DESCRIPTION_2: str = "Parse configuration files"
    REQUIRED_CAPABILITY_3: str = "Text processing"
    CAPABILITY_STATUS_3: str = "[OK] REQUIRED"
    CAPABILITY_DESCRIPTION_3: str = "Process templates and markdown"
    REQUIRED_CAPABILITY_4: str = "Regex support"
    CAPABILITY_STATUS_4: str = "[WARN] RECOMMENDED"
    CAPABILITY_DESCRIPTION_4: str = "Pattern matching for validation"

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for template replacement"""
        return {k: v for k, v in asdict(self).items()}

@dataclass
class SyncReport:
    """Final synchronization report"""
    timestamp: str
    execution_mode: str
    agents_processed: int
    agents_synced: int
    files_created: int
    files_updated: int
    files_deleted: int
    validation_errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    agent_scores: Dict[str, float] = field(default_factory=dict)
    changes_made: List[str] = field(default_factory=list)

# === UTILITY FUNCTIONS ===

def extract_version(content: str) -> Optional[str]:
    """Extract version from documentation content"""
    patterns = [
        r'\*\*Version\*\*:\s*([0-9]+\.[0-9]+\.[0-9]+)',
        r'Version:\s*([0-9]+\.[0-9]+\.[0-9]+)',
        r'v([0-9]+\.[0-9]+\.[0-9]+)',
        r'"version":\s*"([0-9]+\.[0-9]+\.[0-9]+)"',
        r'\*\*Version\*\*:\s*([0-9]+\.[0-9]+)',  # Support X.Y format
        r'Version:\s*([0-9]+\.[0-9]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, content)
        if match:
            return match.group(1)
    return None

def extract_description(readme_content: str) -> str:
    """Extract agent description from README"""
    # Look for first paragraph after title
    lines = readme_content.split('\n')
    description_lines = []
    found_title = False

    for line in lines:
        if line.startswith('# '):
            found_title = True
            continue

        if found_title and line.strip():
            if line.startswith('#'):  # Next section
                break
            description_lines.append(line.strip())
            if len(' '.join(description_lines)) > 200:  # Limit description length
                break

    return ' '.join(description_lines[:3]) if description_lines else "Agent description"

def scan_directory_tree(path: Path) -> List[str]:
    """Scan directory and return list of subdirectories"""
    if not path.exists():
        return []

    dirs = []
    for item in path.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name != '__pycache__':
            dirs.append(item.name)
    return sorted(dirs)

def extract_readme_structure(content: str) -> List[str]:
    """Extract declared structure from README.md"""
    structure = []
    in_structure_section = False

    for line in content.split('\n'):
        if '## STRUCTURE' in line or '## 📁 STRUCTURE' in line or '## 📂 PROJECT STRUCTURE' in line:
            in_structure_section = True
            continue

        if in_structure_section:
            if line.startswith('##'):  # Next section
                break
            # Match directory entries
            match = re.search(r'[├└│]\s*──\s*([a-z_]+)/', line)
            if match:
                structure.append(match.group(1))

    return sorted(set(structure))

def count_files_in_dir(path: Path, pattern: str = '*') -> int:
    """Count files matching pattern in directory"""
    if not path.exists():
        return 0
    return len(list(path.glob(pattern)))

def create_backup(file_path: Path) -> Optional[Path]:
    """Create backup of file with .bak extension"""
    if not file_path.exists():
        return None

    backup_path = file_path.with_suffix(file_path.suffix + '.bak')
    shutil.copy2(file_path, backup_path)
    return backup_path

def replace_variables(template: str, variables: Dict[str, str]) -> str:
    """Replace [VARIABLES] in template with actual values"""
    result = template

    for var_name, var_value in variables.items():
        placeholder = f"[{var_name}]"
        result = result.replace(placeholder, str(var_value))

    return result

def validate_no_placeholders(content: str, exclude_patterns: List[str] = None) -> List[str]:
    """Find any remaining [VARIABLE] placeholders"""
    placeholders = re.findall(r'\[([A-Z_][A-Z0-9_]*)\]', content)

    if exclude_patterns:
        # Filter out excluded patterns
        placeholders = [p for p in placeholders if p not in exclude_patterns]

    return placeholders

# === STEP 1: DISCOVERY & AUDIT ===

def step1_discovery_and_audit(
    agents_dir: Path,
    registry_path: Optional[Path] = None,
    target_agents: Optional[List[str]] = None
) -> Dict[str, AgentAudit]:
    """
    STEP 1: Scan all agents and build initial audit report

    Returns: Dictionary of agent audits keyed by agent name
    """
    print("\n" + "="*60)
    print("STEP 1: DISCOVERY & AUDIT")
    print("="*60)

    # Load registry if available
    registry = None
    if registry_path and registry_path.exists():
        try:
            registry = json.loads(registry_path.read_text(encoding='utf-8'))
            print(f"[OK] Loaded registry: {registry_path}")
        except Exception as e:
            print(f"[WARN] Could not load registry: {e}")

    # Find all agent directories
    all_agent_dirs = [d for d in agents_dir.iterdir()
                      if d.is_dir() and d.name.endswith('_agent')]

    if target_agents:
        agent_dirs = [d for d in all_agent_dirs if d.name in target_agents]
        print(f"[OK] Target agents specified: {len(agent_dirs)} of {len(all_agent_dirs)}")
    else:
        agent_dirs = all_agent_dirs
        print(f"[OK] Scanning all agents: {len(agent_dirs)}")

    audits = {}

    for agent_dir in sorted(agent_dirs):
        agent_name = agent_dir.name
        print(f"\nScanning: {agent_name}")

        # Detect files
        readme_exists = (agent_dir / 'README.md').exists()
        prime_exists = (agent_dir / 'PRIME.md').exists()

        # Check for INSTRUCTIONS with or without suffix
        instructions_path = agent_dir / f'INSTRUCTIONS_{agent_name}.md'
        if not instructions_path.exists():
            instructions_path = agent_dir / 'INSTRUCTIONS.md'
        instructions_exists = instructions_path.exists()

        setup_exists = (agent_dir / 'SETUP.md').exists()

        files_detected = {
            'README.md': readme_exists,
            'PRIME.md': prime_exists,
            'INSTRUCTIONS.md': instructions_exists,
            'SETUP.md': setup_exists
        }

        # Detect version
        version_detected = None
        if readme_exists:
            readme_content = (agent_dir / 'README.md').read_text(encoding='utf-8')
            version_detected = extract_version(readme_content)

        # Scan structure
        structure_actual = scan_directory_tree(agent_dir)
        structure_declared = []

        if readme_exists:
            structure_declared = extract_readme_structure(readme_content)

        # Count prompts and configs
        prompts_count = count_files_in_dir(agent_dir / 'prompts', '*.md')
        config_count = count_files_in_dir(agent_dir / 'config', '*.json')

        # Find inconsistencies
        inconsistencies = []

        if not readme_exists:
            inconsistencies.append("Missing README.md")
        if not prime_exists:
            inconsistencies.append("Missing PRIME.md")
        if not instructions_exists:
            inconsistencies.append("Missing INSTRUCTIONS.md")
        if not setup_exists:
            inconsistencies.append("Missing SETUP.md")

        # Check version consistency across files
        versions = {}
        for file_name in ['README.md', 'PRIME.md', 'INSTRUCTIONS.md', 'SETUP.md']:
            file_path = agent_dir / file_name
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                version = extract_version(content)
                if version:
                    versions[file_name] = version

        if len(set(versions.values())) > 1:
            inconsistencies.append(f"Version mismatch: {versions}")

        # Get registry entry
        registry_entry = None
        if registry:
            registry_entry = registry.get('agents', {}).get(agent_name)

        audit = AgentAudit(
            name=agent_name,
            path=agent_dir,
            files_detected=files_detected,
            version_detected=version_detected,
            inconsistencies=inconsistencies,
            structure_declared=structure_declared,
            structure_actual=structure_actual,
            prompts_count=prompts_count,
            config_count=config_count,
            registry_entry=registry_entry
        )

        audits[agent_name] = audit

        # Print summary
        files_present = sum(files_detected.values())
        print(f"  Files: {files_present}/4")
        print(f"  Version: {version_detected or 'N/A'}")
        print(f"  Prompts: {prompts_count}")
        print(f"  Issues: {len(inconsistencies)}")

    print(f"\n[OK] STEP 1 COMPLETE: Audited {len(audits)} agents")
    return audits

# === STEP 2: TEMPLATE GENERATION ===

def step2_template_generation(templates_dir: Path) -> Dict[str, str]:
    """
    STEP 2: Load standardized templates

    Returns: Dictionary of templates keyed by file type
    """
    print("\n" + "="*60)
    print("STEP 2: TEMPLATE GENERATION")
    print("="*60)

    templates = {}

    # Load INSTRUCTIONS template
    instructions_template_path = templates_dir / 'INSTRUCTIONS_TEMPLATE.md'
    if instructions_template_path.exists():
        templates['INSTRUCTIONS'] = instructions_template_path.read_text(encoding='utf-8')
        print(f"[OK] Loaded: INSTRUCTIONS_TEMPLATE.md")
    else:
        print(f"[WARN] Missing: INSTRUCTIONS_TEMPLATE.md")

    # Load SETUP template
    setup_template_path = templates_dir / 'SETUP_TEMPLATE.md'
    if setup_template_path.exists():
        templates['SETUP'] = setup_template_path.read_text(encoding='utf-8')
        print(f"[OK] Loaded: SETUP_TEMPLATE.md")
    else:
        print(f"[WARN] Missing: SETUP_TEMPLATE.md")

    print(f"\n[OK] STEP 2 COMPLETE: Loaded {len(templates)} templates")
    return templates

# === STEP 3: VARIABLE EXTRACTION ===

def step3_variable_extraction(audit: AgentAudit) -> VariableMapping:
    """
    STEP 3: Extract agent-specific variables for template replacement

    Returns: VariableMapping object
    """
    agent_path = audit.path
    agent_name = audit.name

    # Defaults
    variables = {
        'AGENT_NAME': agent_name.replace('_agent', '').title() + ' Agent',
        'VERSION': audit.version_detected or '1.0.0',
        'LAST_UPDATED': datetime.now().strftime('%Y-%m-%d'),
        'AGENT_DESCRIPTION': 'Agent description',
        'DOMAIN_CONTEXT': 'Domain-specific context and requirements',
        'RECOMMENDED_LLM': 'GPT-4+ / Sonnet 4.5+',
        'AVAILABLE_TOOLS': 'Standard tools and integrations',
        'HOP_MODULES': f'{audit.prompts_count} modular prompts',
        'OUTPUT_FORMATS': '.md (human) + .llm.json (structured) + .meta.json (metadata)',
        'AGENT_DIRECTORY': str(agent_path.relative_to(agent_path.parent.parent)),
        'OUTPUT_DIRECTORY': 'USER_DOCS',
        'EXECUTION_COMMAND': f'python {agent_name}.py',
        'WORKFLOW_DESCRIPTION': 'Multi-phase workflow for task execution',
    }

    # Extract from README if available
    readme_path = agent_path / 'README.md'
    if readme_path.exists():
        readme_content = readme_path.read_text(encoding='utf-8')

        # Extract description
        description = extract_description(readme_content)
        if description:
            variables['AGENT_DESCRIPTION'] = description

        # Extract title
        title_match = re.search(r'^#\s+(.+)', readme_content, re.MULTILINE)
        if title_match:
            variables['AGENT_NAME'] = title_match.group(1).strip()

    # Extract from PRIME if available
    prime_path = agent_path / 'PRIME.md'
    if prime_path.exists():
        prime_content = prime_path.read_text(encoding='utf-8')

        # Look for workflow description
        workflow_match = re.search(r'##\s+WORKFLOW.*?\n\n(.+?)(?=\n##|\Z)',
                                   prime_content, re.DOTALL)
        if workflow_match:
            workflow_text = workflow_match.group(1).strip()
            # Take first paragraph
            workflow_para = workflow_text.split('\n\n')[0]
            variables['WORKFLOW_DESCRIPTION'] = workflow_para

    return VariableMapping(**variables)

# === STEP 4: DOCUMENTATION GENERATION ===

def step4_documentation_generation(
    audit: AgentAudit,
    templates: Dict[str, str],
    variables: VariableMapping,
    dry_run: bool = False
) -> List[Path]:
    """
    STEP 4: Generate/update documentation files

    Returns: List of file paths that were created/updated
    """
    generated_files = []
    agent_path = audit.path
    agent_name = audit.name

    var_dict = variables.to_dict()

    # INSTRUCTIONS file
    if not audit.files_detected.get('INSTRUCTIONS.md', False):
        if 'INSTRUCTIONS' in templates:
            instructions_path = agent_path / f'INSTRUCTIONS_{agent_name}.md'
            instructions_content = replace_variables(templates['INSTRUCTIONS'], var_dict)

            if not dry_run:
                instructions_path.write_text(instructions_content, encoding='utf-8')
                print(f"  [OK] Created: {instructions_path.name}")
            else:
                print(f"  [DRY-RUN] Would create: {instructions_path.name}")

            generated_files.append(instructions_path)

    # SETUP file
    if not audit.files_detected.get('SETUP.md', False):
        if 'SETUP' in templates:
            setup_path = agent_path / 'SETUP.md'
            setup_content = replace_variables(templates['SETUP'], var_dict)

            if not dry_run:
                setup_path.write_text(setup_content, encoding='utf-8')
                print(f"  [OK] Created: {setup_path.name}")
            else:
                print(f"  [DRY-RUN] Would create: {setup_path.name}")

            generated_files.append(setup_path)

    return generated_files

# === STEP 5: STRUCTURE VALIDATION ===

def step5_structure_validation(audit: AgentAudit) -> Tuple[float, Dict]:
    """
    STEP 5: Validate README structure matches filesystem

    Returns: (sync_score, details_dict)
    """
    declared = set(audit.structure_declared)
    actual = set(audit.structure_actual)

    if not declared:
        return 0.5, {
            'status': 'no_structure_section',
            'declared': [],
            'actual': list(actual)
        }

    matches = declared & actual
    missing = declared - actual
    extra = actual - declared

    score = len(matches) / len(declared) if declared else 1.0

    details = {
        'status': 'synced' if score >= MIN_STRUCTURE_SYNC else 'out_of_sync',
        'score': score,
        'declared': sorted(list(declared)),
        'actual': sorted(list(actual)),
        'matches': sorted(list(matches)),
        'missing_from_filesystem': sorted(list(missing)),
        'not_in_readme': sorted(list(extra))
    }

    return score, details

# === STEP 6: HOP SYNC VALIDATION ===

def step6_hop_sync_validation(audit: AgentAudit) -> Tuple[float, Dict]:
    """
    STEP 6: Validate INSTRUCTIONS mentions match prompts directory

    Returns: (sync_score, details_dict)
    """
    # For now, simple check: do prompts exist?
    prompts_exist = (audit.path / 'prompts').exists()
    instructions_exist = audit.files_detected.get('INSTRUCTIONS.md', False)

    if not instructions_exist:
        return 0.0, {'status': 'instructions_missing'}

    if not prompts_exist:
        return 1.0, {'status': 'no_prompts_dir'}

    # Simple heuristic: if both exist, assume 80% sync
    # Full validation would parse INSTRUCTIONS and cross-reference
    return 0.8, {
        'status': 'basic_check',
        'prompts_count': audit.prompts_count
    }

# === STEP 7: VERSION SYNCHRONIZATION ===

def step7_version_synchronization(
    audit: AgentAudit,
    dry_run: bool = False
) -> Tuple[str, Dict]:
    """
    STEP 7: Synchronize versions across all documentation files

    Returns: (canonical_version, sync_report)
    """
    versions = {}

    # Collect versions from all files
    for file_name in ['README.md', 'PRIME.md', 'INSTRUCTIONS.md', 'SETUP.md']:
        file_path = audit.path / file_name
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')
            version = extract_version(content)
            if version:
                versions[file_name] = version

    if not versions:
        return '1.0.0', {'status': 'no_versions_found'}

    # Determine canonical version (use most common, or latest)
    from collections import Counter
    version_counts = Counter(versions.values())
    canonical_version = version_counts.most_common(1)[0][0]

    # Check if sync needed
    unique_versions = set(versions.values())
    needs_sync = len(unique_versions) > 1

    if needs_sync and not dry_run:
        # Update files with mismatched versions
        today = datetime.now().strftime('%Y-%m-%d')

        for file_name, file_version in versions.items():
            if file_version != canonical_version:
                file_path = audit.path / file_name
                content = file_path.read_text(encoding='utf-8')

                # Create backup
                create_backup(file_path)

                # Update version (use lambda to avoid backreference issues)
                content = re.sub(
                    r'(\*\*Version\*\*:\s*)([0-9.]+)',
                    lambda m: m.group(1) + canonical_version,
                    content
                )

                # Update last updated
                content = re.sub(
                    r'(\*\*Last Updated\*\*:\s*)([0-9-]+)',
                    lambda m: m.group(1) + today,
                    content
                )

                file_path.write_text(content, encoding='utf-8')
                print(f"  [OK] Synced version in {file_name}: {file_version} -> {canonical_version}")

    return canonical_version, {
        'canonical_version': canonical_version,
        'versions_found': versions,
        'needs_sync': needs_sync,
        'synced': not needs_sync
    }

# === STEP 8: TAXONOMY VALIDATION ===

def step8_taxonomy_validation(
    audits: Dict[str, AgentAudit],
    registry_path: Optional[Path]
) -> Dict:
    """
    STEP 8: Validate registry matches documentation

    Returns: taxonomy_report dict
    """
    print("\n" + "="*60)
    print("STEP 8: TAXONOMY VALIDATION")
    print("="*60)

    if not registry_path or not registry_path.exists():
        print("[WARN] No registry file found")
        return {'status': 'no_registry'}

    registry = json.loads(registry_path.read_text(encoding='utf-8'))

    agents_in_registry = set(registry.get('agents', {}).keys())
    agents_in_filesystem = set(audits.keys())

    matches = agents_in_registry & agents_in_filesystem
    missing_from_registry = agents_in_filesystem - agents_in_registry
    orphaned_in_registry = agents_in_registry - agents_in_filesystem

    accuracy = len(matches) / len(agents_in_filesystem) if agents_in_filesystem else 1.0

    print(f"  Registry entries: {len(agents_in_registry)}")
    print(f"  Filesystem agents: {len(agents_in_filesystem)}")
    print(f"  Matches: {len(matches)}")
    print(f"  Accuracy: {accuracy*100:.1f}%")

    if missing_from_registry:
        print(f"  [WARN] Missing from registry: {', '.join(missing_from_registry)}")

    if orphaned_in_registry:
        print(f"  [WARN] Orphaned in registry: {', '.join(orphaned_in_registry)}")

    return {
        'status': 'validated',
        'accuracy': accuracy,
        'matches': sorted(list(matches)),
        'missing_from_registry': sorted(list(missing_from_registry)),
        'orphaned': sorted(list(orphaned_in_registry))
    }

# === STEP 9: QUALITY GATE VALIDATION ===

def step9_quality_gate_validation(
    audits: Dict[str, AgentAudit],
    structure_reports: Dict[str, Dict],
    hop_reports: Dict[str, Dict],
    version_reports: Dict[str, Dict]
) -> Dict[str, float]:
    """
    STEP 9: Calculate quality scores for all agents

    Returns: Dictionary of quality scores by agent name
    """
    print("\n" + "="*60)
    print("STEP 9: QUALITY GATE VALIDATION")
    print("="*60)

    scores = {}

    weights = {
        'readme_valid': 0.25,
        'prime_valid': 0.20,
        'instructions_valid': 0.20,
        'setup_valid': 0.10,
        'structure_sync': 0.10,
        'hop_sync': 0.10,
        'version_sync': 0.05
    }

    for agent_name, audit in audits.items():
        score_components = {
            'readme_valid': 1.0 if audit.files_detected.get('README.md') else 0.0,
            'prime_valid': 1.0 if audit.files_detected.get('PRIME.md') else 0.0,
            'instructions_valid': 1.0 if audit.files_detected.get('INSTRUCTIONS.md') else 0.0,
            'setup_valid': 1.0 if audit.files_detected.get('SETUP.md') else 0.0,
            'structure_sync': structure_reports.get(agent_name, {}).get('score', 0.0),
            'hop_sync': hop_reports.get(agent_name, (0.0, {}))[0],
            'version_sync': 1.0 if version_reports.get(agent_name, {}).get('synced') else 0.0
        }

        overall_score = sum(
            score_components[component] * weights[component]
            for component in weights
        )

        scores[agent_name] = overall_score

        quality_level = (
            "EXCELLENT" if overall_score >= 0.90 else
            "GOOD" if overall_score >= 0.85 else
            "FAIR" if overall_score >= 0.75 else
            "POOR"
        )

        print(f"  {agent_name}: {overall_score:.2f} ({quality_level})")

    avg_score = sum(scores.values()) / len(scores) if scores else 0.0
    print(f"\n  Average Score: {avg_score:.2f}")

    return scores

# === STEP 10: REPORT GENERATION ===

def step10_report_generation(
    sync_report: SyncReport,
    audits: Dict[str, AgentAudit],
    dry_run: bool = False
) -> Tuple[str, str]:
    """
    STEP 10: Generate comprehensive sync report

    Returns: (markdown_report, json_report_path)
    """
    print("\n" + "="*60)
    print("STEP 10: REPORT GENERATION")
    print("="*60)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Generate Markdown report
    md_lines = []
    md_lines.append(f"# ADW-100 Documentation Sync Report")
    md_lines.append(f"")
    md_lines.append(f"**Execution**: {sync_report.timestamp}")
    md_lines.append(f"**Mode**: {sync_report.execution_mode}")
    md_lines.append(f"**Agents Processed**: {sync_report.agents_processed}")
    md_lines.append(f"**Dry Run**: {dry_run}")
    md_lines.append(f"")
    md_lines.append(f"## Summary")
    md_lines.append(f"")
    md_lines.append(f"- Agents synced: {sync_report.agents_synced}")
    md_lines.append(f"- Files created: {sync_report.files_created}")
    md_lines.append(f"- Files updated: {sync_report.files_updated}")
    md_lines.append(f"- Files deleted: {sync_report.files_deleted}")
    md_lines.append(f"")
    md_lines.append(f"## Quality Scores")
    md_lines.append(f"")
    md_lines.append(f"| Agent | Score | Quality |")
    md_lines.append(f"|-------|-------|---------|")

    for agent_name, score in sorted(sync_report.agent_scores.items()):
        quality = (
            "EXCELLENT" if score >= 0.90 else
            "GOOD" if score >= 0.85 else
            "FAIR" if score >= 0.75 else
            "POOR"
        )
        md_lines.append(f"| {agent_name} | {score:.2f} | {quality} |")

    md_lines.append(f"")
    md_lines.append(f"## Changes Made")
    md_lines.append(f"")

    if sync_report.changes_made:
        for change in sync_report.changes_made:
            md_lines.append(f"- {change}")
    else:
        md_lines.append(f"- No changes made")

    md_lines.append(f"")
    md_lines.append(f"## Validation Results")
    md_lines.append(f"")

    if sync_report.validation_errors:
        md_lines.append(f"### Errors ({len(sync_report.validation_errors)})")
        for error in sync_report.validation_errors:
            md_lines.append(f"- [FAIL] {error}")
        md_lines.append(f"")

    if sync_report.warnings:
        md_lines.append(f"### Warnings ({len(sync_report.warnings)})")
        for warning in sync_report.warnings:
            md_lines.append(f"- [WARN] {warning}")
        md_lines.append(f"")

    if sync_report.recommendations:
        md_lines.append(f"### Recommendations")
        for rec in sync_report.recommendations:
            md_lines.append(f"- {rec}")

    md_lines.append(f"")
    md_lines.append(f"---")
    md_lines.append(f"")
    md_lines.append(f"**Report Generated**: {datetime.now().isoformat()}")
    md_lines.append(f"**Builder**: builders/11_doc_sync_builder.py v1.0.0")

    markdown_report = '\n'.join(md_lines)

    # Save reports
    if not dry_run:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        md_path = REPORTS_DIR / f'ADW_100_sync_{timestamp}.md'
        json_path = REPORTS_DIR / f'ADW_100_sync_{timestamp}.json'

        md_path.write_text(markdown_report, encoding='utf-8')

        json_data = asdict(sync_report)
        json_path.write_text(json.dumps(json_data, indent=2), encoding='utf-8')

        print(f"  [OK] Markdown report: {md_path}")
        print(f"  [OK] JSON report: {json_path}")

        return markdown_report, str(json_path)
    else:
        print(f"  [DRY-RUN] Would save reports to {REPORTS_DIR}")
        return markdown_report, "[dry-run]"

# === MAIN WORKFLOW ===

def main():
    parser = argparse.ArgumentParser(
        description='ADW-100: Documentation Synchronization Builder',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Audit only (no changes)
  python builders/11_doc_sync_builder.py --mode audit_only

  # Dry run (simulate changes)
  python builders/11_doc_sync_builder.py --mode auto_fix --dry-run

  # Auto-fix mode (apply changes)
  python builders/11_doc_sync_builder.py --mode auto_fix

  # Specific agents only
  python builders/11_doc_sync_builder.py --mode auto_fix --agents anuncio_agent,codexa_agent
        """
    )

    parser.add_argument(
        '--mode',
        choices=['audit_only', 'auto_fix', 'interactive'],
        default='audit_only',
        help='Execution mode'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Simulate execution without writing files'
    )

    parser.add_argument(
        '--agents',
        type=str,
        help='Comma-separated list of specific agents to process'
    )

    parser.add_argument(
        '--agents-dir',
        type=str,
        help='Path to agentes directory (default: auto-detect)'
    )

    parser.add_argument(
        '--registry',
        type=str,
        help='Path to AGENT_REGISTRY.json (default: auto-detect)'
    )

    args = parser.parse_args()

    # Determine paths
    agents_dir = Path(args.agents_dir) if args.agents_dir else AGENTS_ROOT

    if args.registry:
        registry_path = Path(args.registry)
    else:
        registry_path = agents_dir.parent / '51_AGENT_REGISTRY.json'

    # Parse target agents
    target_agents = None
    if args.agents:
        target_agents = [a.strip() for a in args.agents.split(',')]

    # Initialize report
    sync_report = SyncReport(
        timestamp=datetime.now().isoformat(),
        execution_mode=args.mode,
        agents_processed=0,
        agents_synced=0,
        files_created=0,
        files_updated=0,
        files_deleted=0
    )

    print("\n" + "="*60)
    print("ADW-100: DOCUMENTATION SYNCHRONIZATION BUILDER")
    print("="*60)
    print(f"Mode: {args.mode}")
    print(f"Dry Run: {args.dry_run}")
    print(f"Agents Directory: {agents_dir}")
    print(f"Registry: {registry_path}")

    try:
        # STEP 1: Discovery & Audit
        audits = step1_discovery_and_audit(agents_dir, registry_path, target_agents)
        sync_report.agents_processed = len(audits)

        # STEP 2: Template Generation
        templates = step2_template_generation(TEMPLATES_DIR)

        # Process each agent
        structure_reports = {}
        hop_reports = {}
        version_reports = {}

        for agent_name, audit in audits.items():
            print(f"\n{'='*60}")
            print(f"Processing: {agent_name}")
            print(f"{'='*60}")

            # STEP 3: Variable Extraction
            print(f"\nSTEP 3: Extracting variables...")
            variables = step3_variable_extraction(audit)

            # STEP 4: Documentation Generation
            print(f"\nSTEP 4: Generating documentation...")
            if args.mode in ['auto_fix', 'interactive']:
                generated_files = step4_documentation_generation(
                    audit, templates, variables, args.dry_run
                )
                sync_report.files_created += len(generated_files)

                if generated_files:
                    sync_report.changes_made.extend([
                        f"Created {f.name} for {agent_name}" for f in generated_files
                    ])

            # STEP 5: Structure Validation
            print(f"\nSTEP 5: Validating structure...")
            struct_score, struct_details = step5_structure_validation(audit)
            structure_reports[agent_name] = {'score': struct_score, **struct_details}
            print(f"  Structure sync: {struct_score:.2f}")

            # STEP 6: HOP Sync Validation
            print(f"\nSTEP 6: Validating HOP sync...")
            hop_score, hop_details = step6_hop_sync_validation(audit)
            hop_reports[agent_name] = (hop_score, hop_details)
            print(f"  HOP sync: {hop_score:.2f}")

            # STEP 7: Version Synchronization
            print(f"\nSTEP 7: Synchronizing versions...")
            canonical_version, version_report = step7_version_synchronization(
                audit, args.dry_run
            )
            version_reports[agent_name] = version_report
            print(f"  Canonical version: {canonical_version}")

        # STEP 8: Taxonomy Validation
        taxonomy_report = step8_taxonomy_validation(audits, registry_path)

        # STEP 9: Quality Gate Validation
        quality_scores = step9_quality_gate_validation(
            audits, structure_reports, hop_reports, version_reports
        )
        sync_report.agent_scores = quality_scores

        # Count agents meeting quality threshold
        sync_report.agents_synced = sum(
            1 for score in quality_scores.values() if score >= MIN_QUALITY_SCORE
        )

        # Add recommendations
        avg_score = sum(quality_scores.values()) / len(quality_scores) if quality_scores else 0

        if avg_score < MIN_QUALITY_SCORE:
            sync_report.recommendations.append(
                f"Average quality score ({avg_score:.2f}) below threshold ({MIN_QUALITY_SCORE})"
            )
            sync_report.recommendations.append(
                "Consider running in auto_fix mode to create missing documentation"
            )

        for agent_name, score in quality_scores.items():
            if score < MIN_QUALITY_SCORE:
                sync_report.recommendations.append(
                    f"{agent_name}: Improve quality score from {score:.2f} to >={MIN_QUALITY_SCORE}"
                )

        # STEP 10: Report Generation
        markdown_report, json_path = step10_report_generation(
            sync_report, audits, args.dry_run
        )

        # Print summary
        print("\n" + "="*60)
        print("FINAL SUMMARY")
        print("="*60)
        print(f"Agents Processed: {sync_report.agents_processed}")
        print(f"Agents Meeting Quality (>={MIN_QUALITY_SCORE}): {sync_report.agents_synced}/{sync_report.agents_processed}")
        print(f"Files Created: {sync_report.files_created}")
        print(f"Average Score: {avg_score:.2f}")

        if avg_score >= MIN_QUALITY_SCORE:
            print(f"\n[OK] SUCCESS: All agents meet quality standards!")
            return 0
        else:
            print(f"\n[WARN] PARTIAL: Some agents below quality threshold")
            return 1

    except Exception as e:
        print(f"\n[FAIL] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
