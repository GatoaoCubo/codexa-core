#!/usr/bin/env python3
"""
CODEXA Agent - Single Entry Point
=================================

Unified CLI for all CODEXA operations.

Usage:
    python codexa.py <command> [options]

Commands:
    # Agent Operations
    python codexa.py agent run "task description"
    python codexa.py agent create "agent description"

    # Builder Operations
    python codexa.py build agent "Agent description"
    python codexa.py build prompt "HOP description"
    python codexa.py build command "Command description"

    # Validation
    python codexa.py validate hop prompts/91_meta_build_agent_HOP.md
    python codexa.py validate readme README.md
    python codexa.py validate all

    # Information
    python codexa.py info
    python codexa.py status

Version: 2.5.0
"""

import sys
import asyncio
import os
from pathlib import Path
from typing import Optional
import argparse

# Fix Windows console encoding
if sys.platform == "win32":
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))


def print_banner():
    """Print CODEXA banner."""
    print("""
+---------------------------------------------------------------+
|                    CODEXA Agent System                        |
|           Meta-Constructor & Multi-Agent Orchestrator         |
|                        Version 2.5.0                          |
+---------------------------------------------------------------+
""")


def cmd_info():
    """Show system information."""
    print_banner()

    print("[STRUCTURE]")
    print("=" * 50)
    print("""
codexa_agent/
+-- src/                 # Core runtime
|   +-- llm/            # LLM providers (Claude, OpenAI, Gemini)
|   +-- tools/          # Tool execution (File, Bash)
|   +-- runtime/        # Agent runtime loop
|   +-- auth/           # Auth, rate limiting, audit
|
+-- builders/           # Construction tools
|   +-- 02_agent_meta_constructor.py  # 5-phase agent builder
|
+-- validators/         # Quality gates
|   +-- 07_hop_sync_validator.py      # TAC-7 compliance
|
+-- prompts/            # HOPs & Layers
|   +-- layers/         # 8 composable prompt layers
|   +-- 9*_meta_*_HOP.md              # Higher-Order Prompts
|
+-- agents/             # Agent definitions
|   +-- planning_agent.md
|   +-- execution_agent.md
|   +-- orchestrator.md
|
+-- config/             # Configuration
|   +-- paths.py        # Centralized paths
|   +-- agent_modes.yml # Operating modes
|   +-- prompt_layers.yml
|
+-- deployment/         # Production deployment
    +-- docker/
""")

    # Show versions
    print("\n[VERSIONS]")
    print("=" * 50)
    try:
        from src import __version__ as src_version
        print(f"  src/: {src_version}")
    except Exception:
        print("  src/: N/A")

    # Show available providers
    print("\n[LLM PROVIDERS]")
    print("=" * 50)
    try:
        from src.llm import ProviderFactory
        print("  - Claude (Anthropic): claude-opus, claude-sonnet, claude-haiku")
        print("  - OpenAI: gpt-4, gpt-4-turbo, gpt-5")
        print("  - Gemini (Google): gemini-pro, gemini-2.0")
    except Exception as e:
        print(f"  Error loading providers: {e}")

    # Show tools
    print("\n[TOOLS]")
    print("=" * 50)
    print("  - Read: Read file contents")
    print("  - Write: Write to files")
    print("  - Edit: Edit file contents")
    print("  - Glob: Find files by pattern")
    print("  - Grep: Search file contents")
    print("  - Bash: Execute commands")


def cmd_status():
    """Show system status."""
    print_banner()
    print("[SYSTEM STATUS]")
    print("=" * 50)

    # Check directories
    dirs_to_check = [
        ("src/", "Core runtime"),
        ("builders/", "Builders"),
        ("validators/", "Validators"),
        ("prompts/", "Prompts/HOPs"),
        ("agents/", "Agent definitions"),
        ("config/", "Configuration"),
        ("deployment/", "Deployment"),
    ]

    for dir_path, description in dirs_to_check:
        full_path = PROJECT_ROOT / dir_path
        if full_path.exists():
            file_count = len(list(full_path.glob("**/*")))
            print(f"  [OK] {dir_path:<20} ({description}) - {file_count} files")
        else:
            print(f"  [!!] {dir_path:<20} ({description}) - MISSING")

    # Check key files
    print("\n[KEY FILES]")
    print("=" * 50)
    key_files = [
        "PRIME.md",
        "README.md",
        "INSTRUCTIONS.md",
        "requirements.txt",
    ]

    for file_name in key_files:
        file_path = PROJECT_ROOT / file_name
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"  [OK] {file_name:<25} ({size:,} bytes)")
        else:
            print(f"  [!!] {file_name:<25} MISSING")

    # Check API keys
    print("\n[API KEYS]")
    print("=" * 50)
    try:
        from src.auth import get_default_key_manager
        manager = get_default_key_manager()
        for provider in ["claude", "openai", "gemini"]:
            if manager.has_key(provider):
                print(f"  [OK] {provider.upper()}: {manager.get_masked_key(provider)}")
            else:
                print(f"  [--] {provider.upper()}: Not configured")
    except Exception as e:
        print(f"  Error checking keys: {e}")


async def cmd_agent_run(task: str, provider: str = "claude"):
    """Run an agent with a task."""
    print_banner()
    print(f"[AGENT] Running with task: {task[:50]}...")
    print("=" * 50)

    try:
        from src import create_agent

        agent = create_agent(
            agent_id="cli_agent",
            system_prompt="You are CODEXA, a helpful AI assistant.",
            provider=provider,
        )

        result = await agent.run(task, workflow_id="cli")
        print("\n[RESULT]")
        print("=" * 50)
        print(result.final_response)

    except Exception as e:
        print(f"[ERROR] {e}")
        raise


def cmd_build_agent(description: str):
    """Build a new agent."""
    print_banner()
    print(f"[BUILD] Creating agent: {description[:50]}...")

    import subprocess
    builder_path = PROJECT_ROOT / "builders" / "02_agent_meta_constructor.py"

    if builder_path.exists():
        result = subprocess.run(
            [sys.executable, str(builder_path), description],
            cwd=PROJECT_ROOT,
        )
        return result.returncode
    else:
        print(f"[ERROR] Builder not found: {builder_path}")
        return 1


def cmd_validate(validator: str, target: Optional[str] = None):
    """Run a validator."""
    print_banner()

    validators_map = {
        "hop": "07_hop_sync_validator.py",
        "readme": "09_readme_validator.py",
        "taxonomy": "10_taxonomy_validator.py",
        "doc-sync": "12_doc_sync_validator.py",
        "path": "16_path_consistency_validator.py",
    }

    if validator == "all":
        for name, script in validators_map.items():
            print(f"\n[VALIDATE] Running {name} validator...")
            cmd_validate(name, target)
        return

    script_name = validators_map.get(validator)
    if not script_name:
        print(f"[ERROR] Unknown validator: {validator}")
        print(f"Available: {', '.join(validators_map.keys())}")
        return

    import subprocess
    validator_path = PROJECT_ROOT / "validators" / script_name

    if validator_path.exists():
        args = [sys.executable, str(validator_path)]
        if target:
            args.append(target)

        result = subprocess.run(args, cwd=PROJECT_ROOT)
        return result.returncode
    else:
        print(f"[ERROR] Validator not found: {validator_path}")
        return 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="CODEXA Agent System - Unified CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python codexa.py info                    # Show system info
  python codexa.py status                  # Show system status
  python codexa.py agent run "task"        # Run agent with task
  python codexa.py build agent "desc"      # Build new agent
  python codexa.py validate hop file.md    # Validate HOP
  python codexa.py validate all            # Run all validators
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Info command
    subparsers.add_parser("info", help="Show system information")

    # Status command
    subparsers.add_parser("status", help="Show system status")

    # Agent commands
    agent_parser = subparsers.add_parser("agent", help="Agent operations")
    agent_sub = agent_parser.add_subparsers(dest="agent_cmd")

    run_parser = agent_sub.add_parser("run", help="Run agent with task")
    run_parser.add_argument("task", help="Task description")
    run_parser.add_argument("--provider", default="claude", help="LLM provider")

    # Build commands
    build_parser = subparsers.add_parser("build", help="Build operations")
    build_sub = build_parser.add_subparsers(dest="build_cmd")

    build_agent = build_sub.add_parser("agent", help="Build new agent")
    build_agent.add_argument("description", help="Agent description")

    # Validate commands
    validate_parser = subparsers.add_parser("validate", help="Validation operations")
    validate_parser.add_argument(
        "validator",
        choices=["hop", "readme", "taxonomy", "doc-sync", "path", "all"],
        help="Validator to run",
    )
    validate_parser.add_argument("target", nargs="?", help="Target file/directory")

    # Parse args
    args = parser.parse_args()

    if not args.command:
        print_banner()
        parser.print_help()
        return

    # Execute command
    if args.command == "info":
        cmd_info()
    elif args.command == "status":
        cmd_status()
    elif args.command == "agent":
        if args.agent_cmd == "run":
            asyncio.run(cmd_agent_run(args.task, args.provider))
    elif args.command == "build":
        if args.build_cmd == "agent":
            cmd_build_agent(args.description)
    elif args.command == "validate":
        cmd_validate(args.validator, args.target)


if __name__ == "__main__":
    main()
