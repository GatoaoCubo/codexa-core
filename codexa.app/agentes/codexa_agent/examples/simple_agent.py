"""
Simple Agent Example
Demonstrates basic usage of the CODEXA agent system.
"""

import asyncio
from pathlib import Path

from src.llm.provider_factory import ProviderFactory
from src.llm.provider import ModelType
from src.llm.cost_tracker import CostTracker
from src.tools.executor import ToolExecutor
from src.tools.file_tools import FileTools
from src.tools.bash_tools import BashTools
from src.tools.permissions import (
    PermissionManager,
    create_full_access_permission,
)
from src.runtime.agent_runtime import AgentRuntime, AgentConfig
from src.auth.api_keys import APIKeyManager


async def main():
    """Run a simple agent task."""

    print("=" * 80)
    print("CODEXA Agent System - Simple Example")
    print("=" * 80)
    print()

    # 1. Setup workspace
    workspace = Path.cwd() / "workspace"
    workspace.mkdir(exist_ok=True)
    print(f"[1/6] Workspace: {workspace}")

    # 2. Load API keys
    api_keys = APIKeyManager()

    if not api_keys.has_key("claude"):
        print("\n[ERROR] Claude API key not found!")
        print("Set ANTHROPIC_API_KEY environment variable")
        return

    print(f"[2/6] API Keys loaded: {api_keys.list_providers()}")

    # 3. Create LLM provider (using Claude Haiku for speed/cost)
    provider = ProviderFactory.create_provider(
        model=ModelType.CLAUDE_HAIKU,
        api_key=api_keys.get_key("claude")
    )
    print(f"[3/6] LLM Provider: {provider.config.model.value}")

    # 4. Setup tools with permissions
    permission_manager = PermissionManager(workspace_path=workspace)
    permission_manager.register_agent(
        agent_id="demo_agent",
        permission=create_full_access_permission("demo_agent")
    )

    tool_executor = ToolExecutor(permission_manager=permission_manager)

    # Register file tools
    file_tools = FileTools(base_path=workspace)
    tool_executor.register_tool("read", file_tools.read)
    tool_executor.register_tool("write", file_tools.write)
    tool_executor.register_tool("edit", file_tools.edit)
    tool_executor.register_tool("glob", file_tools.glob)
    tool_executor.register_tool("grep", file_tools.grep)

    # Register bash tools
    bash_tools = BashTools(base_path=workspace)
    tool_executor.register_tool("bash", bash_tools.execute)

    print("[4/6] Tools registered: read, write, edit, glob, grep, bash")

    # 5. Create cost tracker
    cost_tracker = CostTracker()
    cost_tracker.start_workflow("demo_workflow")
    print("[5/6] Cost tracker initialized")

    # 6. Create agent
    system_prompt = """You are a helpful coding assistant with access to file tools.

Your task is to help the user with file operations and simple coding tasks.

Available tools:
- read: Read file contents
- write: Write content to a file
- edit: Edit file by replacing text
- glob: Find files by pattern
- grep: Search for text in files
- bash: Execute bash commands

When given a task:
1. Think step by step about what needs to be done
2. Use the appropriate tools to complete the task
3. Verify your work when possible
4. Respond to the user with a clear summary

Be efficient and use tools effectively."""

    config = AgentConfig(
        agent_id="demo_agent",
        agent_type="assistant",
        system_prompt=system_prompt,
        llm_provider=provider,
        tool_executor=tool_executor,
        permission=create_full_access_permission("demo_agent"),
        max_iterations=20,
        workspace_path=workspace
    )

    runtime = AgentRuntime(
        config=config,
        cost_tracker=cost_tracker
    )

    print("[6/6] Agent runtime created")
    print()

    # Run task
    print("=" * 80)
    print("TASK")
    print("=" * 80)

    task = """Create a Python script called 'hello.py' that:
1. Prints 'Hello from CODEXA!'
2. Calculates the sum of numbers 1 to 10
3. Prints the result

After creating the file, verify it was created successfully."""

    print(task)
    print()
    print("=" * 80)
    print("EXECUTION")
    print("=" * 80)
    print()

    state = await runtime.run(
        task=task,
        workflow_id="demo_workflow"
    )

    # Show results
    print()
    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()
    print(f"Status: {state.status.value}")
    print(f"Iterations: {state.iteration}")
    print(f"Tool calls: {state.total_tool_calls}")
    print(f"Cost: ${state.total_cost:.4f}")
    print()

    # Show final response
    final_response = runtime.get_final_response()
    if final_response:
        print("Agent Response:")
        print("-" * 80)
        print(final_response)
        print("-" * 80)
        print()

    # Show created file
    if (workspace / "hello.py").exists():
        print("Created file (hello.py):")
        print("-" * 80)
        print((workspace / "hello.py").read_text())
        print("-" * 80)
        print()

    # Show cost summary
    cost_tracker.complete_workflow("demo_workflow")
    summary = cost_tracker.get_workflow_summary("demo_workflow")
    print(summary)


if __name__ == "__main__":
    asyncio.run(main())
