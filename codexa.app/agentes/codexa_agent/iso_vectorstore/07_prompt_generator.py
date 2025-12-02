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
Run an adhoc Claude Code prompt from the command line.

Usage:
    # Method 1: Direct execution (requires uv)
    ./adw_prompt.py "Write a hello world Python script"

    # Method 2: Using uv run
    uv run adw_prompt.py "Write a hello world Python script"

    # Method 3: Using Python directly (requires dependencies installed)
    python adw_prompt.py "Write a hello world Python script"

Examples:
    # Run with specific model
    ./adw_prompt.py "Explain this code" --model opus

    # Run with custom output file
    ./adw_prompt.py "Create a FastAPI app" --output my_result.jsonl

    # Run from a different working directory
    ./adw_prompt.py "List files here" --working-dir /path/to/project

    # Disable retry on failure
    ./adw_prompt.py "Quick test" --no-retry

    # Use custom agent name
    ./adw_prompt.py "Debug this" --agent-name debugger
"""

import os
import sys
import json
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.syntax import Syntax
from rich.text import Text

# Add the adw_modules directory to the path so we can import agent
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "adw_modules"))

from agent import (
    prompt_claude_code,
    AgentPromptRequest,
    AgentPromptResponse,
    prompt_claude_code_with_retry,
    generate_short_id,
)

# Output file name constants
OUTPUT_JSONL = "cc_raw_output.jsonl"
OUTPUT_JSON = "cc_raw_output.json"
FINAL_OBJECT_JSON = "cc_final_object.json"
SUMMARY_JSON = "custom_summary_output.json"

# Platform-aware emoji support (Windows cp1252 doesn't support emojis)
def get_emoji(name: str) -> str:
    """Get emoji if platform supports it, otherwise return empty string."""
    if sys.platform == "win32":
        return ""  # Windows terminals often don't support emojis

    emoji_map = {
        "rocket": "🚀 ",
        "success": "✅ ",
        "fail": "❌ ",
        "warning": "⚠️ ",
        "files": "📄 ",
    }
    return emoji_map.get(name, "")


def sanitize_for_windows(text: str) -> str:
    """Remove characters that Windows cp1252 encoding can't handle."""
    if sys.platform != "win32":
        return text

    # Remove emoji and other Unicode characters that cp1252 can't encode
    # Keep only ASCII and common Windows-1252 characters
    import re
    # Remove emoji and other problematic Unicode
    sanitized = re.sub(r'[^\x00-\xff]', '', text)
    return sanitized


@click.command()
@click.argument("prompt", required=True)
@click.option(
    "--model",
    type=click.Choice(["sonnet", "opus"]),
    default="sonnet",
    help="Claude model to use",
)
@click.option(
    "--output",
    type=click.Path(),
    help="Output file path (default: ./output/oneoff_<id>_output.jsonl)",
)
@click.option(
    "--working-dir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, resolve_path=True),
    help="Working directory for the prompt execution (default: current directory)",
)
@click.option("--no-retry", is_flag=True, help="Disable automatic retry on failure")
@click.option(
    "--agent-name", default="oneoff", help="Agent name for tracking (default: oneoff)"
)
def main(
    prompt: str,
    model: str,
    output: str | None,
    working_dir: str | None,
    no_retry: bool,
    agent_name: str,
) -> None:
    """Run an adhoc Claude Code prompt from the command line.

    Executes a single prompt using the adw_modules agent execution system with
    automatic retry logic (unless --no-retry is specified) and structured output.

    Args:
        prompt: The prompt text to execute
        model: Claude model to use (sonnet or opus)
        output: Optional custom output file path
        working_dir: Optional working directory for execution context
        no_retry: If True, disable automatic retry on failure
        agent_name: Agent identifier for tracking and organization

    Raises:
        SystemExit: Exit code 0 on success, 1 on prompt failure, 2 on unexpected error
    """
    console = Console()

    # Validate prompt
    if not prompt or len(prompt.strip()) == 0:
        console.print("[bold red]Error:[/bold red] Prompt cannot be empty")
        sys.exit(1)

    if len(prompt) > 50000:  # Reasonable limit
        console.print("[bold yellow]Warning:[/bold yellow] Prompt is very long (>50k chars). This may cause issues.")


    # Generate a unique ID for this execution
    adw_id = generate_short_id()

    # Set up output file path
    if not output:
        # Default: write to agents/<adw_id>/<agent_name>/
        output_dir = Path(f"./agents/{adw_id}/{agent_name}")
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except (PermissionError, OSError) as e:
            console.print(f"[bold red]Error:[/bold red] Cannot create output directory: {e}")
            sys.exit(1)
        output = str(output_dir / OUTPUT_JSONL)

    # Use current directory if no working directory specified
    if not working_dir:
        working_dir = os.getcwd()

    # Validate working directory exists and is accessible
    if not os.path.isdir(working_dir):
        console.print(f"[bold red]Error:[/bold red] Working directory does not exist: {working_dir}")
        sys.exit(1)

    # Create the prompt request
    try:
        request = AgentPromptRequest(
            prompt=prompt,
            adw_id=adw_id,
            agent_name=agent_name,
            model=model,
            working_dir=working_dir,
        )
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Failed to create prompt request: {e}")
        sys.exit(1)

    # Create execution info table
    info_table = Table(show_header=False, box=None, padding=(0, 1))
    info_table.add_column(style="bold cyan")
    info_table.add_column()

    info_table.add_row("ADW ID", adw_id)
    info_table.add_row("ADW Name", "adw_prompt")
    info_table.add_row("Prompt", prompt)
    info_table.add_row("Model", model)
    info_table.add_row("Working Dir", working_dir)
    info_table.add_row("Output", output)

    console.print(
        Panel(
            info_table,
            title=f"[bold blue]{get_emoji('rocket')}Inputs[/bold blue]",
            border_style="blue",
        )
    )
    console.print()

    response: AgentPromptResponse | None = None

    try:
        # Execute the prompt
        with console.status("[bold yellow]Executing prompt...[/bold yellow]"):
            if no_retry:
                # Direct execution without retry
                response = prompt_claude_code(request)
            else:
                # Execute with retry logic (exponential backoff: 1s → 2s → 4s)
                response = prompt_claude_code_with_retry(request, max_retries=3)

        # Validate response
        if response is None:
            raise ValueError("Execution returned None response")

        # Display the result
        if response.success:
            # Success panel
            result_panel = Panel(
                sanitize_for_windows(response.output),
                title=f"[bold green]{get_emoji('success')}Success[/bold green]",
                border_style="green",
                padding=(1, 2),
            )
            console.print(result_panel)

            if response.session_id:
                console.print(
                    f"\n[bold cyan]Session ID:[/bold cyan] {response.session_id}"
                )
        else:
            # Error panel
            error_panel = Panel(
                sanitize_for_windows(response.output),
                title=f"[bold red]{get_emoji('fail')}Failed[/bold red]",
                border_style="red",
                padding=(1, 2),
            )
            console.print(error_panel)

            if response.retry_code != "none":
                console.print(
                    f"\n[bold yellow]Retry code:[/bold yellow] {response.retry_code}"
                )

        # Show output file info
        console.print()

        # Also create a JSON summary file
        if output.endswith(f"/{OUTPUT_JSONL}"):
            # Default path: save as custom_summary_output.json in same directory
            simple_json_output = output.replace(f"/{OUTPUT_JSONL}", f"/{SUMMARY_JSON}")
        else:
            # Custom path: replace .jsonl with _summary.json
            simple_json_output = output.replace(".jsonl", "_summary.json")

        try:
            with open(simple_json_output, "w", encoding='utf-8') as f:
                json.dump(
                    {
                        "adw_id": adw_id,
                        "prompt": prompt[:1000],  # Truncate long prompts in summary
                        "prompt_length": len(prompt),
                        "model": model,
                        "working_dir": working_dir,
                        "success": response.success,
                        "session_id": response.session_id,
                        "retry_code": response.retry_code,
                        "execution_time": getattr(response, 'execution_time', 0.0),
                        "output_preview": response.output[:500] if response.output else None,
                        "output_length": len(response.output) if response.output else 0,
                    },
                    f,
                    indent=2,
                )
        except (IOError, OSError) as e:
            console.print(f"[bold yellow]Warning:[/bold yellow] Could not save summary file: {e}")
            # Continue execution - this is not critical

        # Files saved panel with descriptions
        files_table = Table(show_header=True, box=None)
        files_table.add_column("File Type", style="bold cyan")
        files_table.add_column("Path", style="dim")
        files_table.add_column("Description", style="italic")

        # Determine paths for all files
        output_dir = os.path.dirname(output)
        json_array_path = os.path.join(output_dir, OUTPUT_JSON)
        final_object_path = os.path.join(output_dir, FINAL_OBJECT_JSON)

        files_table.add_row(
            "JSONL Stream", output, "Raw streaming output from Claude Code"
        )
        files_table.add_row(
            "JSON Array", json_array_path, "All messages as a JSON array"
        )
        files_table.add_row(
            "Final Object", final_object_path, "Last message entry (final result)"
        )
        files_table.add_row(
            "Summary", simple_json_output, "High-level execution summary with metadata"
        )

        console.print(
            Panel(
                files_table,
                title=f"[bold blue]{get_emoji('files')}Output Files[/bold blue]",
                border_style="blue",
            )
        )

        # Exit with appropriate code
        sys.exit(0 if response.success else 1)

    except KeyboardInterrupt:
        console.print(f"\n[bold yellow]{get_emoji('warning')}Execution interrupted by user[/bold yellow]")
        sys.exit(130)  # Standard exit code for SIGINT

    except ValueError as e:
        console.print(
            Panel(
                f"[bold red]Validation Error:[/bold red] {str(e)}",
                title=f"[bold red]{get_emoji('fail')}Invalid Input/Output[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)

    except (IOError, OSError) as e:
        console.print(
            Panel(
                f"[bold red]File System Error:[/bold red] {str(e)}",
                title=f"[bold red]{get_emoji('fail')}I/O Error[/bold red]",
                border_style="red",
            )
        )
        sys.exit(1)

    except Exception as e:
        console.print(
            Panel(
                f"[bold red]Unexpected Error:[/bold red] {type(e).__name__}: {str(e)}",
                title=f"[bold red]{get_emoji('fail')}Fatal Error[/bold red]",
                border_style="red",
            )
        )
        import traceback
        if os.getenv("DEBUG"):
            console.print("\n[dim]Stack trace:[/dim]")
            traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
