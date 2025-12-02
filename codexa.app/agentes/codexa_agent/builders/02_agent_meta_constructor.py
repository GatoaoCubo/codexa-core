#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pydantic",
#   "python-dotenv",
#   "click",
#   "rich",
# ]
# ///
"""
META-CONSTRUCTOR: Build -> Test -> Review -> Document Agent Workflows
Version: 2.0.0
Updated: 2025-11-24

This ADW orchestrates a 5-phase meta-construction workflow for creating ISOLATED
agents that work as single nodes in OpenAI Agent Builder (gpt-4o/gpt-5 minimum).

META-CONSTRUCTION PHILOSOPHY:
- Build the thing that builds the thing
- Intentionally leave [VARIABLES] unspecified for creative entropy
- Use $argument to chain outputs between phases
- Maximize agent autonomy and capability

PHASES:
1. /agent_plan      - Strategic planning with [OPEN_VARIABLES]
2. /agent_build     - Construction with $plan as input
3. /agent_test      - Validation with $artifacts as input
4. /agent_review    - Critical review with $test_results as input
5. /agent_document  - Final documentation with $all_context as input

SRC INTEGRATION (v2.0.0):
- src/llm: LLM provider factory and model types
- src/tools: File operations and tool execution
- src/runtime: Agent runtime and prompt loading
- src/auth: API key management and rate limiting

Usage:
    uv run builders/02_agent_meta_constructor.py "Create a sentiment analysis agent"
    uv run builders/02_agent_meta_constructor.py "Build a code review agent" --model opus
    uv run builders/02_agent_meta_constructor.py "Research agent" --output-dir reports/
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.rule import Rule
from rich.tree import Tree

# Add the adw_modules directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "adw_modules"))

# Add parent directory for src/ imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# src/ integration (v2.0.0)
try:
    from src import ProviderFactory, ModelType, AgentConfig
    from src.runtime import PromptLoader
    SRC_AVAILABLE = True
except ImportError:
    SRC_AVAILABLE = False

# Report generator for ##report standard
try:
    from artifacts.generators.report_generator import ExecutionReportBuilder, ReportGenerator
    REPORT_GENERATOR_AVAILABLE = True
except ImportError:
    REPORT_GENERATOR_AVAILABLE = False

from agent import (
    AgentTemplateRequest,
    AgentPromptRequest,
    AgentPromptResponse,
    execute_template,
    prompt_claude_code_with_retry,
    generate_short_id,
)

# SCOUT Integration
try:
    from scout_integration import prepare_scout_context_sync, extract_related_files, get_repository_stats
    SCOUT_AVAILABLE = True
except ImportError:
    SCOUT_AVAILABLE = False

# Output file name constants
OUTPUT_JSONL = "cc_raw_output.jsonl"
OUTPUT_JSON = "cc_raw_output.json"
FINAL_OBJECT_JSON = "cc_final_object.json"
SUMMARY_JSON = "custom_summary_output.json"


def sanitize_for_windows(text: str) -> str:
    """Remove characters that Windows cp1252 encoding can't handle."""
    if sys.platform != "win32":
        return text

    # Remove emoji and other Unicode characters that cp1252 can't encode
    # Keep only ASCII and common Windows-1252 characters
    sanitized = re.sub(r'[^\x00-\xff]', '', text)
    return sanitized


def extract_variable(output: str, variable_name: str, patterns: list[str]) -> Optional[str]:
    """Extract a variable from agent output using multiple regex patterns.

    Tries each pattern in order until one matches. Returns the first capture group if present,
    otherwise the entire match. Useful for extracting $variables from workflow phase outputs.

    Args:
        output: The agent output text to search
        variable_name: Name of the variable for logging/debugging
        patterns: List of regex patterns to try in order

    Returns:
        The extracted value (stripped of whitespace), or None if no pattern matches

    Example:
        >>> extract_variable("Agent: test-agent", "agent_name", [r'Agent:\\s*(.+)'])
        'test-agent'
    """
    if not output or not patterns:
        return None

    for pattern in patterns:
        try:
            match = re.search(pattern, output, re.IGNORECASE | re.MULTILINE | re.DOTALL)
            if match:
                # Return first capture group if exists, else entire match
                extracted = match.group(1).strip() if match.groups() else match.group(0).strip()
                if extracted:  # Don't return empty strings
                    return extracted
        except re.error as e:
            # Invalid regex pattern - log and continue
            print(f"Warning: Invalid regex pattern for {variable_name}: {e}")
            continue

    return None


def save_phase_summary(
    output_dir: str,
    phase: str,
    adw_id: str,
    agent_name: str,
    command: str,
    args: list[str],
    model: str,
    working_dir: str,
    response: AgentPromptResponse,
    extracted_data: Optional[Dict[str, Any]] = None,
) -> str:
    """Save a standardized summary for a workflow phase with error handling.

    Creates a JSON summary file with phase execution metadata and results.
    Includes error handling to ensure workflow continues even if saving fails.

    Args:
        output_dir: Directory to save the summary file
        phase: Phase name (e.g., "planning", "building")
        adw_id: Workflow ID for tracking
        agent_name: Name of the agent being constructed
        command: Command executed (e.g., "/agent_plan")
        args: Command arguments
        model: Model used for execution
        working_dir: Working directory
        response: Agent response object
        extracted_data: Optional extracted variables from output

    Returns:
        Path to the saved summary file

    Raises:
        IOError: If file cannot be written (will print warning)
    """
    summary_path = Path(output_dir) / SUMMARY_JSON

    summary_data = {
        "phase": phase,
        "adw_id": adw_id,
        "agent_name": agent_name,
        "command": command,
        "args": args,
        "model": model,
        "working_dir": working_dir,
        "success": response.success,
        "session_id": response.session_id,
        "retry_code": response.retry_code,
        "execution_time": getattr(response, 'execution_time', 0.0),
        "timestamp": datetime.now().isoformat(),
        "output_preview": response.output[:500] if response.output else None,
        "output_length": len(response.output) if response.output else 0,
    }

    if extracted_data:
        summary_data["extracted_data"] = extracted_data

    if response.error:
        summary_data["error"] = response.error

    try:
        # Ensure output directory exists
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        with open(summary_path, "w", encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)

        return str(summary_path)

    except (IOError, OSError) as e:
        print(f"Warning: Could not save phase summary to {summary_path}: {e}")
        return ""


def print_phase_header(console: Console, phase_num: int, phase_name: str, icon: str) -> None:
    """Print a consistent phase header with visual separation.

    Args:
        console: Rich console instance for formatted output
        phase_num: Phase number (1-5)
        phase_name: Name of the phase (e.g., "Strategic Planning")
        icon: Emoji icon for visual identification (currently unused)
    """
    console.print()
    console.print(Rule(f"[bold yellow]{icon} Phase {phase_num}: {phase_name}[/bold yellow]"))
    console.print()


@click.command()
@click.argument("agent_description", required=True)
@click.option(
    "--model",
    type=click.Choice(["sonnet", "opus"]),
    default="opus",
    help="Claude model to use (default: opus for complex meta-construction)",
)
@click.option(
    "--target-dir",
    type=str,
    help="Target directory for agent artifacts (default: agents/{adw_id}/agent-artifacts/)",
)
@click.option(
    "--working-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Working directory for execution (default: current directory)",
)
@click.option(
    "--skip-phases",
    type=str,
    help="Comma-separated list of phases to skip (e.g., 'test,review')",
)
@click.option(
    "--verbose",
    is_flag=True,
    help="Show full output from each phase",
)
def main(
    agent_description: str,
    model: str,
    target_dir: str | None,
    working_dir: str | None,
    skip_phases: str | None,
    verbose: bool,
) -> None:
    """META-CONSTRUCTOR: Build AI agents with intentional entropy and creative freedom.

    Creates ISOLATED agents for OpenAI Agent Builder through 5 strategic phases:
    1. /agent_plan - Strategic planning with [OPEN_VARIABLES]
    2. /agent_build - Construction with $plan chaining
    3. /agent_test - Validation with $artifacts
    4. /agent_review - Critical review with $test_results
    5. /agent_document - Final documentation with $all_context

    Philosophy:
        - Build the thing that builds the thing
        - Intentionally leave [VARIABLES] unspecified for creative entropy
        - Use $arguments to chain outputs between phases
        - Maximize agent autonomy and capability

    Args:
        agent_description: Description of the agent to build (required)
        model: Claude model to use (sonnet | opus)
        target_dir: Custom output directory for artifacts
        working_dir: Working directory for execution context
        skip_phases: Comma-separated phases to skip
        verbose: Show full output from each phase

    Raises:
        SystemExit: Exit code 0 on success, 1 on failure

    Example:
        python 02_agent_meta_constructor.py "Build a sentiment analysis agent" --model opus
    """
    console = Console()

    # Validate agent description
    if not agent_description or len(agent_description.strip()) < 10:
        console.print("[bold red]Error:[/bold red] Agent description too short (minimum 10 characters)")
        sys.exit(1)

    # Generate unique ID for this meta-construction workflow
    adw_id = generate_short_id()

    # Set working directory
    if not working_dir:
        working_dir = os.getcwd()

    # Set target directory for agent artifacts
    if not target_dir:
        target_dir = f"agents/{adw_id}/agent-artifacts"

    # Parse skip phases
    skipped_phases = set(skip_phases.split(",")) if skip_phases else set()

    # Agent names for each phase
    planner_name = f"meta-planner-{adw_id[:6]}"
    builder_name = f"meta-builder-{adw_id[:6]}"
    tester_name = f"meta-tester-{adw_id[:6]}"
    reviewer_name = f"meta-reviewer-{adw_id[:6]}"
    documenter_name = f"meta-documenter-{adw_id[:6]}"

    # Welcome banner
    tree = Tree("[META-CONSTRUCTOR WORKFLOW]")
    tree.add("[cyan]Phase 1:[/cyan] Strategic Planning [dim](with open variables)[/dim]")
    tree.add("[cyan]Phase 2:[/cyan] Artifact Construction [dim]($plan -> artifacts)[/dim]")
    tree.add("[cyan]Phase 3:[/cyan] Testing & Validation [dim]($artifacts -> results)[/dim]")
    tree.add("[cyan]Phase 4:[/cyan] Critical Review [dim]($results -> refinements)[/dim]")
    tree.add("[cyan]Phase 5:[/cyan] Documentation [dim]($all_context -> docs)[/dim]")

    console.print(Panel(tree, title="[bold blue]>> Workflow Overview <<[/bold blue]", border_style="blue"))

    # Configuration panel
    config_table = Table(show_header=False, box=None, padding=(0, 1))
    config_table.add_column(style="bold cyan")
    config_table.add_column()

    config_table.add_row("ADW ID", adw_id)
    config_table.add_row("Agent Description", agent_description)
    config_table.add_row("Model", model)
    config_table.add_row("Target Directory", target_dir)
    config_table.add_row("Working Directory", working_dir)
    config_table.add_row("Skipped Phases", ", ".join(skipped_phases) if skipped_phases else "None")

    console.print()
    console.print(Panel(config_table, title="[bold blue]>> Configuration <<[/bold blue]", border_style="blue"))

    # SCOUT Pre-Preparation: Load repository context
    scout_context = None
    if SCOUT_AVAILABLE:
        try:
            console.print("\n[cyan][SCOUT][/cyan] Loading repository context...")
            scout_context = prepare_scout_context_sync(working_dir=working_dir)
            if scout_context.get('success'):
                stats = get_repository_stats(scout_context)
                console.print(f"[green][SCOUT][/green] Indexed {stats.get('total_files', 0)} files")

                # Find existing agent patterns
                agent_files = extract_related_files(scout_context, pattern="*agent*.py")
                if agent_files:
                    console.print(f"[green][SCOUT][/green] Found {len(agent_files)} existing agent files for pattern analysis")

                    # Store agent files in workflow context for later reference
                    workflow_context_temp = {"agent_files": agent_files[:10]}  # Top 10 for context
            else:
                console.print(f"[yellow][SCOUT][/yellow] Context failed: {scout_context.get('error')}")
        except Exception as e:
            console.print(f"[yellow][SCOUT][/yellow] Integration error: {e}")

    # Track workflow state and $arguments
    workflow_context = {
        "adw_id": adw_id,
        "agent_description": agent_description,
        "scout_context": scout_context,
        "model": model,
        "target_dir": target_dir,
        "working_dir": working_dir,
        "timestamp_start": datetime.now().isoformat(),
        "agent_files": workflow_context_temp.get("agent_files", []) if 'workflow_context_temp' in locals() else [],
    }

    workflow_success = True
    phase_results = {}

    try:
        # ==================== PHASE 1: STRATEGIC PLANNING ====================
        if "plan" not in skipped_phases:
            print_phase_header(console, 1, "Strategic Planning (with [OPEN_VARIABLES])", "")

            # Build the planning prompt with meta-construction instructions
            planning_prompt = f"""You are a META-CONSTRUCTOR tasked with planning an ISOLATED agent for OpenAI Agent Builder.

AGENT TO BUILD:
{agent_description}

META-CONSTRUCTION PRINCIPLES:
1. **Intentional Entropy**: Leave [VARIABLES] unspecified to allow creative freedom
2. **$argument Chaining**: Design outputs that flow naturally to next phases
3. **Isolation**: Agent must be self-contained (no external dependencies)
4. **GPT-4o/GPT-5**: Assume access to advanced models
5. **Single Node**: Works as ONE node in Agent Builder workflow

YOUR TASK:
Create a strategic plan with the following structure:

## 1. AGENT SPECIFICATION
- Name: [AGENT_NAME]
- Purpose: [AGENT_PURPOSE]
- Target Model: [MODEL_CHOICE]
- Reasoning Mode: [REASONING_ENABLED]

## 2. CORE CAPABILITIES (with [OPEN_VARIABLES])
- [CAPABILITY_1]
- [CAPABILITY_2]
- [CAPABILITY_3]
- ...

## 3. TOOLS & RESOURCES
- File Search: [FILE_SEARCH_CONFIG]
- Code Interpreter: [CODE_INTERPRETER_CONFIG]
- Custom Tools: [CUSTOM_TOOLS]

## 4. INSTRUCTIONS STRATEGY
- Tone: [TONE_STYLE]
- Output Format: [OUTPUT_FORMAT]
- Key Constraints: [CONSTRAINTS]

## 5. VECTOR STORE KNOWLEDGE
List 5-10 critical knowledge files needed:
- [FILE_1]: [PURPOSE]
- [FILE_2]: [PURPOSE]
...

## 6. OUTPUT SCHEMA
Define expected output structure:
```
[OUTPUT_STRUCTURE]
```

## 7. $ARGUMENTS FOR NEXT PHASE
Prepare these variables for /agent_build:
- $agent_name: [NAME]
- $instructions_summary: [SUMMARY]
- $vector_store_files: [FILE_LIST]
- $tools_config: [TOOLS]

IMPORTANT:
- Use [VARIABLES] liberally for creative freedom
- Be specific where critical, vague where beneficial
- Think "meta" - design for flexibility and evolution
"""

            plan_request = AgentPromptRequest(
                prompt=planning_prompt,
                adw_id=adw_id,
                agent_name=planner_name,
                model=model,
                dangerously_skip_permissions=True,
                output_file=f"./agents/{adw_id}/{planner_name}/{OUTPUT_JSONL}",
                working_dir=working_dir,
            )

            with console.status("[bold yellow]Planning with intentional entropy...[/bold yellow]"):
                plan_response = prompt_claude_code_with_retry(plan_request)

            if plan_response.success:
                console.print(Panel(
                    sanitize_for_windows(plan_response.output) if verbose else "Strategic plan created with [OPEN_VARIABLES]",
                    title="[bold green][+] Phase 1 Success[/bold green]",
                    border_style="green",
                    padding=(1, 2),
                ))

                # Extract $arguments for next phase
                agent_name = extract_variable(
                    plan_response.output,
                    "agent_name",
                    [r"\$agent_name:\s*(.+?)(?:\n|$)", r"Name:\s*(.+?)(?:\n|$)"]
                )

                workflow_context["$plan"] = plan_response.output
                workflow_context["$agent_name"] = agent_name or "[AGENT_NAME]"

                phase_results["plan"] = {
                    "success": True,
                    "output_dir": f"./agents/{adw_id}/{planner_name}/",
                }
            else:
                console.print(Panel(
                    sanitize_for_windows(plan_response.output),
                    title="[bold red][X] Phase 1 Failed[/bold red]",
                    border_style="red",
                    padding=(1, 2),
                ))
                workflow_success = False
                phase_results["plan"] = {"success": False}

            # Save phase summary
            save_phase_summary(
                f"./agents/{adw_id}/{planner_name}",
                "planning",
                adw_id,
                planner_name,
                "direct_prompt",
                [agent_description],
                model,
                working_dir,
                plan_response,
                {"agent_name": workflow_context.get("$agent_name")},
            )

        # ==================== PHASE 2: ARTIFACT CONSTRUCTION ====================
        if workflow_success and "build" not in skipped_phases:
            print_phase_header(console, 2, "Artifact Construction ($plan -> artifacts)", "")

            build_prompt = f"""You are a META-CONSTRUCTOR in the BUILD phase.

PREVIOUS PHASE OUTPUT ($plan):
{workflow_context.get('$plan', '[NO_PLAN_AVAILABLE]')}

YOUR TASK:
Build ALL necessary artifacts for this agent to work in OpenAI Agent Builder:

## ARTIFACTS TO CREATE:

### 1. MASTER_INSTRUCTIONS.md
Write comprehensive instructions (2000-5000 words) that define:
- Agent personality and communication style
- Step-by-step workflow
- Compliance rules and constraints
- Output format requirements
- Tool usage patterns
- Error handling strategies

### 2. AGENT_CONFIGURATION.json
```json
{{
  "model": "[MODEL]",
  "temperature": [TEMP],
  "reasoning_mode": [true/false],
  "tools": {{
    "file_search": {{
      "enabled": [true/false],
      "vector_store": "[NAME]"
    }},
    "code_interpreter": {{
      "enabled": [true/false]
    }}
  }}
}}
```

### 3. VECTOR_STORE_MANIFEST.md
List all files for Vector Store:
- Group A: Core prompts (5-10 files)
- Group B: Configuration files (2-4 files)
- Group C: Documentation (3-5 files)
Include file descriptions, sizes, priorities

### 4. OUTPUT_SCHEMA.md
Define structured output format with:
- Block specifications
- Validation rules
- Example outputs
- Min/max constraints

### 5. [CREATIVE_ARTIFACT]
Create 1-2 additional artifacts that would maximize agent capability.
Use [VARIABLES] creatively here.

## TARGET DIRECTORY:
Save all artifacts to: {target_dir}

## $ARGUMENTS FOR NEXT PHASE:
- $artifacts_created: [LIST]
- $primary_instructions_path: [PATH]
- $config_path: [PATH]
- $vector_store_files: [COUNT]

Create these artifacts now using Write tool.
"""

            build_request = AgentPromptRequest(
                prompt=build_prompt,
                adw_id=adw_id,
                agent_name=builder_name,
                model=model,
                dangerously_skip_permissions=True,
                output_file=f"./agents/{adw_id}/{builder_name}/{OUTPUT_JSONL}",
                working_dir=working_dir,
            )

            with console.status("[bold yellow]Constructing artifacts...[/bold yellow]"):
                build_response = prompt_claude_code_with_retry(build_request)

            if build_response.success:
                console.print(Panel(
                    sanitize_for_windows(build_response.output) if verbose else f"Artifacts created in {target_dir}",
                    title="[bold green][+] Phase 2 Success[/bold green]",
                    border_style="green",
                    padding=(1, 2),
                ))

                workflow_context["$artifacts"] = build_response.output
                workflow_context["$target_dir"] = target_dir

                phase_results["build"] = {
                    "success": True,
                    "output_dir": f"./agents/{adw_id}/{builder_name}/",
                }
            else:
                console.print(Panel(
                    sanitize_for_windows(build_response.output),
                    title="[bold red][X] Phase 2 Failed[/bold red]",
                    border_style="red",
                    padding=(1, 2),
                ))
                workflow_success = False
                phase_results["build"] = {"success": False}

            save_phase_summary(
                f"./agents/{adw_id}/{builder_name}",
                "build",
                adw_id,
                builder_name,
                "direct_prompt",
                [target_dir],
                model,
                working_dir,
                build_response,
            )

        # ==================== PHASE 3: TESTING & VALIDATION ====================
        if workflow_success and "test" not in skipped_phases:
            print_phase_header(console, 3, "Testing & Validation ($artifacts -> results)", "")

            test_prompt = f"""You are a META-CONSTRUCTOR in the TEST phase.

ARTIFACTS CREATED ($artifacts):
{workflow_context.get('$artifacts', '[NO_ARTIFACTS]')}

TARGET DIRECTORY: {target_dir}

YOUR TASK:
Validate ALL created artifacts through comprehensive testing:

## TEST SUITE:

### 1. COMPLETENESS CHECK
- [ ] All required files exist
- [ ] File sizes are reasonable (not empty)
- [ ] All [VARIABLES] were either filled or intentionally left open
- [ ] $arguments are properly documented

### 2. INSTRUCTIONS VALIDATION
Read MASTER_INSTRUCTIONS.md and verify:
- [ ] Clear workflow steps
- [ ] Compliance rules present
- [ ] Tool usage documented
- [ ] Output format specified
- [ ] Length: 2000-5000 words

### 3. CONFIGURATION VALIDATION
Check AGENT_CONFIGURATION.json for:
- [ ] Valid model name
- [ ] Temperature in range 0.0-2.0
- [ ] Tools properly configured
- [ ] All required fields present

### 4. VECTOR STORE VALIDATION
Review VECTOR_STORE_MANIFEST.md:
- [ ] File list complete
- [ ] Priorities assigned
- [ ] Total size reasonable (<50MB)
- [ ] Groups organized logically

### 5. OUTPUT SCHEMA VALIDATION
Inspect OUTPUT_SCHEMA.md for:
- [ ] Clear structure defined
- [ ] Validation rules specified
- [ ] Examples provided
- [ ] Constraints documented

### 6. SIMULATION TEST
Simulate a sample interaction:
- Input: [CREATE_TEST_INPUT]
- Expected Output: [PREDICT_OUTPUT]
- Validation: [PASS/FAIL with reasoning]

## TEST RESULTS FORMAT:
```
OVERALL: [PASS/FAIL]
Score: [X/100]

Passed: [N] tests
Failed: [M] tests
Warnings: [K] issues

Critical Issues:
- [ISSUE_1]
- [ISSUE_2]

Recommendations:
- [REC_1]
- [REC_2]
```

## $ARGUMENTS FOR NEXT PHASE:
- $test_score: [SCORE]
- $critical_issues: [ISSUES]
- $recommendations: [RECS]

Run all tests now using Read tool to inspect artifacts.
"""

            test_request = AgentPromptRequest(
                prompt=test_prompt,
                adw_id=adw_id,
                agent_name=tester_name,
                model=model,
                dangerously_skip_permissions=True,
                output_file=f"./agents/{adw_id}/{tester_name}/{OUTPUT_JSONL}",
                working_dir=working_dir,
            )

            with console.status("[bold yellow]Running test suite...[/bold yellow]"):
                test_response = prompt_claude_code_with_retry(test_request)

            if test_response.success:
                console.print(Panel(
                    sanitize_for_windows(test_response.output) if verbose else "Testing completed with results",
                    title="[bold green][+] Phase 3 Success[/bold green]",
                    border_style="green",
                    padding=(1, 2),
                ))

                # Extract test score
                test_score = extract_variable(
                    test_response.output,
                    "test_score",
                    [r"Score:\s*(\d+)/100", r"\$test_score:\s*(\d+)"]
                )

                workflow_context["$test_results"] = test_response.output
                workflow_context["$test_score"] = test_score or "[UNKNOWN]"

                phase_results["test"] = {
                    "success": True,
                    "output_dir": f"./agents/{adw_id}/{tester_name}/",
                    "score": test_score,
                }
            else:
                console.print(Panel(
                    sanitize_for_windows(test_response.output),
                    title="[bold red][X] Phase 3 Failed[/bold red]",
                    border_style="red",
                    padding=(1, 2),
                ))
                workflow_success = False
                phase_results["test"] = {"success": False}

            save_phase_summary(
                f"./agents/{adw_id}/{tester_name}",
                "test",
                adw_id,
                tester_name,
                "direct_prompt",
                [target_dir],
                model,
                working_dir,
                test_response,
                {"test_score": workflow_context.get("$test_score")},
            )

        # ==================== PHASE 4: CRITICAL REVIEW ====================
        if workflow_success and "review" not in skipped_phases:
            print_phase_header(console, 4, "Critical Review ($test_results -> refinements)", "")

            review_prompt = f"""You are a META-CONSTRUCTOR in the REVIEW phase.

TEST RESULTS ($test_results):
{workflow_context.get('$test_results', '[NO_TEST_RESULTS]')}

AGENT DESCRIPTION: {agent_description}
TARGET DIRECTORY: {target_dir}

YOUR TASK:
Perform a critical review and apply refinements:

## REVIEW CRITERIA:

### 1. STRATEGIC ALIGNMENT
- Does the agent fulfill the original description?
- Are the capabilities appropriate for the use case?
- Is the isolation principle maintained?

### 2. META-CONSTRUCTION QUALITY
- Are [VARIABLES] used effectively for creative freedom?
- Do $arguments flow logically between phases?
- Is there healthy entropy vs structure balance?

### 3. TECHNICAL EXCELLENCE
- Are instructions comprehensive and clear?
- Is configuration optimal for the task?
- Is the Vector Store well-organized?
- Is the output schema practical?

### 4. ROBUSTNESS
- Can the agent handle edge cases?
- Are error conditions addressed?
- Is fallback behavior defined?

### 5. USABILITY
- Is deployment straightforward?
- Is documentation sufficient?
- Are examples helpful?

## REFINEMENT ACTIONS:
Based on critical issues from testing, apply fixes:

1. If test_score < 70: [MAJOR_REFINEMENTS_NEEDED]
2. If test_score 70-85: [MODERATE_IMPROVEMENTS]
3. If test_score > 85: [MINOR_POLISH]

Use Edit tool to refine artifacts as needed.

## REVIEW OUTPUT:
```
REVIEW VERDICT: [EXCELLENT/GOOD/NEEDS_WORK/POOR]
Alignment Score: [X/100]
Technical Score: [Y/100]
Usability Score: [Z/100]

Strengths:
- [STRENGTH_1]
- [STRENGTH_2]

Weaknesses:
- [WEAKNESS_1]
- [WEAKNESS_2]

Refinements Applied:
- [REFINEMENT_1]
- [REFINEMENT_2]

Final Recommendation: [DEPLOY/REVISE/REBUILD]
```

## $ARGUMENTS FOR NEXT PHASE:
- $review_verdict: [VERDICT]
- $final_recommendation: [RECOMMENDATION]
- $refinements_applied: [COUNT]

Perform review and apply refinements now.
"""

            review_request = AgentPromptRequest(
                prompt=review_prompt,
                adw_id=adw_id,
                agent_name=reviewer_name,
                model=model,
                dangerously_skip_permissions=True,
                output_file=f"./agents/{adw_id}/{reviewer_name}/{OUTPUT_JSONL}",
                working_dir=working_dir,
            )

            with console.status("[bold yellow]Conducting critical review...[/bold yellow]"):
                review_response = prompt_claude_code_with_retry(review_request)

            if review_response.success:
                console.print(Panel(
                    sanitize_for_windows(review_response.output) if verbose else "Review completed with refinements",
                    title="[bold green][+] Phase 4 Success[/bold green]",
                    border_style="green",
                    padding=(1, 2),
                ))

                # Extract review verdict
                review_verdict = extract_variable(
                    review_response.output,
                    "review_verdict",
                    [r"REVIEW VERDICT:\s*(\w+)", r"\$review_verdict:\s*(\w+)"]
                )

                workflow_context["$review"] = review_response.output
                workflow_context["$review_verdict"] = review_verdict or "[UNKNOWN]"

                phase_results["review"] = {
                    "success": True,
                    "output_dir": f"./agents/{adw_id}/{reviewer_name}/",
                    "verdict": review_verdict,
                }
            else:
                console.print(Panel(
                    sanitize_for_windows(review_response.output),
                    title="[bold red][X] Phase 4 Failed[/bold red]",
                    border_style="red",
                    padding=(1, 2),
                ))
                workflow_success = False
                phase_results["review"] = {"success": False}

            save_phase_summary(
                f"./agents/{adw_id}/{reviewer_name}",
                "review",
                adw_id,
                reviewer_name,
                "direct_prompt",
                [target_dir],
                model,
                working_dir,
                review_response,
                {"review_verdict": workflow_context.get("$review_verdict")},
            )

        # ==================== PHASE 5: DOCUMENTATION ====================
        if workflow_success and "document" not in skipped_phases:
            print_phase_header(console, 5, "Documentation ($all_context -> docs)", "")

            document_prompt = f"""You are a META-CONSTRUCTOR in the DOCUMENTATION phase.

COMPLETE WORKFLOW CONTEXT:
- Agent Description: {agent_description}
- ADW ID: {adw_id}
- Target Directory: {target_dir}
- Test Score: {workflow_context.get('$test_score', 'N/A')}
- Review Verdict: {workflow_context.get('$review_verdict', 'N/A')}

FULL CONTEXT:
{json.dumps(workflow_context, indent=2)}

YOUR TASK:
Create comprehensive documentation for this agent:

## DOCUMENTS TO CREATE:

### 1. README.md (in {target_dir})
```markdown
# {{agent_name}} - AI Agent for OpenAI Agent Builder

## 🎯 Purpose
[AGENT_PURPOSE]

## 🚀 Quick Start
[DEPLOYMENT_STEPS]

## 📋 Capabilities
[CAPABILITY_LIST]

## ⚙️ Configuration
[CONFIG_DETAILS]

## 📊 Performance
- Test Score: {workflow_context.get('$test_score', 'N/A')}/100
- Review Verdict: {workflow_context.get('$review_verdict', 'N/A')}

## 📁 Files
[FILE_STRUCTURE]

## 🔧 Customization
[CUSTOMIZATION_GUIDE]

## 📄 License & Attribution
```

### 2. DEPLOYMENT_GUIDE.md
Step-by-step instructions for deploying to OpenAI Agent Builder:
- Account setup
- File uploads
- Configuration
- Testing
- Production deployment

### 3. META_CONSTRUCTION_LOG.md
Document the meta-construction process:
- ADW ID and timestamp
- All 5 phases executed
- $arguments used
- [VARIABLES] left open
- Decisions made
- Lessons learned

### 4. EXAMPLES.md
Provide 3-5 example interactions:
- Input examples
- Expected outputs
- Edge cases
- Error handling examples

### 5. CHANGELOG.md
Initial version documentation:
- Version 1.0.0
- Created by META-CONSTRUCTOR
- Features included
- Known limitations

Create all documentation now using Write tool in {target_dir}.

## FINAL OUTPUT:
Summarize the complete meta-construction:
```
🧬 META-CONSTRUCTION COMPLETE

Agent: {workflow_context.get('$agent_name', '[AGENT]')}
ADW ID: {adw_id}
Quality: {workflow_context.get('$review_verdict', 'N/A')}
Test Score: {workflow_context.get('$test_score', 'N/A')}/100

Artifacts: [COUNT] files in {target_dir}
Documentation: 5 guides created
Status: READY FOR DEPLOYMENT

Deployment Command:
  # Upload artifacts to OpenAI Agent Builder
  # Configure with AGENT_CONFIGURATION.json
  # Upload Vector Store files per VECTOR_STORE_MANIFEST.md
  # Copy MASTER_INSTRUCTIONS.md to Instructions field
  # Test with EXAMPLES.md scenarios
  # Deploy!

Meta-Construction Philosophy:
- [OPEN_VARIABLES] preserved for creative freedom
- $arguments chained through 5 phases
- Isolation principle maintained
- Built the thing that builds the thing ✓
```
"""

            document_request = AgentPromptRequest(
                prompt=document_prompt,
                adw_id=adw_id,
                agent_name=documenter_name,
                model=model,
                dangerously_skip_permissions=True,
                output_file=f"./agents/{adw_id}/{documenter_name}/{OUTPUT_JSONL}",
                working_dir=working_dir,
            )

            with console.status("[bold yellow]Generating documentation...[/bold yellow]"):
                document_response = prompt_claude_code_with_retry(document_request)

            if document_response.success:
                console.print(Panel(
                    sanitize_for_windows(document_response.output) if verbose else "Documentation completed",
                    title="[bold green][+] Phase 5 Success[/bold green]",
                    border_style="green",
                    padding=(1, 2),
                ))

                workflow_context["$documentation"] = document_response.output

                phase_results["document"] = {
                    "success": True,
                    "output_dir": f"./agents/{adw_id}/{documenter_name}/",
                }
            else:
                console.print(Panel(
                    sanitize_for_windows(document_response.output),
                    title="[bold red][X] Phase 5 Failed[/bold red]",
                    border_style="red",
                    padding=(1, 2),
                ))
                workflow_success = False
                phase_results["document"] = {"success": False}

            save_phase_summary(
                f"./agents/{adw_id}/{documenter_name}",
                "documentation",
                adw_id,
                documenter_name,
                "direct_prompt",
                [target_dir],
                model,
                working_dir,
                document_response,
            )

        # ==================== WORKFLOW SUMMARY ====================
        console.print()
        console.print(Rule("[bold blue]META-CONSTRUCTION SUMMARY[/bold blue]"))
        console.print()

        summary_table = Table(show_header=True, box=None)
        summary_table.add_column("Phase", style="bold cyan")
        summary_table.add_column("Status", style="bold")
        summary_table.add_column("Details", style="dim")

        phase_info = [
            ("1. Planning", "plan", workflow_context.get("$agent_name", "N/A")),
            ("2. Build", "build", target_dir),
            ("3. Test", "test", f"Score: {workflow_context.get('$test_score', 'N/A')}"),
            ("4. Review", "review", workflow_context.get("$review_verdict", "N/A")),
            ("5. Document", "document", "Docs created"),
        ]

        for phase_name, phase_key, details in phase_info:
            if phase_key in skipped_phases:
                summary_table.add_row(phase_name, "[>>] Skipped", "-")
            elif phase_key in phase_results:
                status = "[+] Success" if phase_results[phase_key]["success"] else "[X] Failed"
                summary_table.add_row(phase_name, status, details)
            else:
                summary_table.add_row(phase_name, "[-] Not Run", "-")

        console.print(summary_table)

        # Save final workflow summary
        workflow_summary_path = f"./agents/{adw_id}/meta_construction_summary.json"
        os.makedirs(f"./agents/{adw_id}", exist_ok=True)

        workflow_context["phases"] = phase_results
        workflow_context["overall_success"] = workflow_success
        workflow_context["timestamp_end"] = datetime.now().isoformat()

        with open(workflow_summary_path, "w") as f:
            json.dump(workflow_context, f, indent=2)

        console.print()
        console.print(f"[bold cyan]Workflow Summary:[/bold cyan] {workflow_summary_path}")
        console.print(f"[bold cyan]Agent Artifacts:[/bold cyan] {target_dir}")
        console.print()

        # Final status
        if workflow_success:
            console.print(Panel(
                f"[bold green]META-CONSTRUCTION COMPLETE![/bold green]\n\n"
                f"Agent: {workflow_context.get('$agent_name', '[AGENT]')}\n"
                f"Quality: {workflow_context.get('$review_verdict', 'N/A')}\n"
                f"Test Score: {workflow_context.get('$test_score', 'N/A')}/100\n\n"
                f"[+] Ready for OpenAI Agent Builder deployment\n"
                f"[+] All artifacts in: {target_dir}",
                title="[bold green][SUCCESS][/bold green]",
                border_style="green",
            ))
            sys.exit(0)
        else:
            console.print(Panel(
                "[bold yellow][WARNING] META-CONSTRUCTION COMPLETED WITH ERRORS[/bold yellow]\n\n"
                "Some phases failed. Review phase outputs for details.",
                title="[bold yellow][PARTIAL SUCCESS][/bold yellow]",
                border_style="yellow",
            ))
            sys.exit(1)

    except Exception as e:
        console.print(Panel(
            f"[bold red]{str(e)}[/bold red]",
            title="[bold red][X] Unexpected Error[/bold red]",
            border_style="red",
        ))
        sys.exit(2)


if __name__ == "__main__":
    main()
