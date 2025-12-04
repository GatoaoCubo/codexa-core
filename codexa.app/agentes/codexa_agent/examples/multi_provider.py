"""
Multi-Provider Example
Demonstrates using multiple LLM providers with the same task.
"""

import asyncio
from pathlib import Path

from src.llm.provider_factory import ProviderFactory
from src.llm.provider import ModelType
from src.llm.cost_tracker import CostTracker
from src.tools.executor import ToolExecutor
from src.tools.file_tools import FileTools
from src.tools.permissions import (
    PermissionManager,
    create_full_access_permission,
)
from src.runtime.agent_runtime import AgentRuntime, AgentConfig
from src.auth.api_keys import APIKeyManager


async def run_with_provider(
    provider_name: str,
    model: ModelType,
    api_key: str,
    workspace: Path,
    cost_tracker: CostTracker
):
    """Run the same task with different providers."""

    print(f"\n{'=' * 80}")
    print(f"Testing with: {provider_name} ({model.value})")
    print("=" * 80)

    # Create provider
    provider = ProviderFactory.create_provider(
        model=model,
        api_key=api_key
    )

    # Setup tools
    permission_manager = PermissionManager(workspace_path=workspace)
    agent_id = f"{provider_name}_agent"
    permission_manager.register_agent(
        agent_id=agent_id,
        permission=create_full_access_permission(agent_id)
    )

    tool_executor = ToolExecutor(permission_manager=permission_manager)
    file_tools = FileTools(base_path=workspace)
    tool_executor.register_tool("write", file_tools.write)
    tool_executor.register_tool("read", file_tools.read)

    # Create agent
    system_prompt = """You are a helpful assistant. Use the available tools to complete tasks efficiently."""

    config = AgentConfig(
        agent_id=agent_id,
        agent_type="test",
        system_prompt=system_prompt,
        llm_provider=provider,
        tool_executor=tool_executor,
        permission=create_full_access_permission(agent_id),
        max_iterations=10,
        workspace_path=workspace
    )

    runtime = AgentRuntime(
        config=config,
        cost_tracker=cost_tracker
    )

    # Run task
    workflow_id = f"{provider_name}_workflow"
    cost_tracker.start_workflow(workflow_id)

    task = f"Create a file called '{provider_name}_test.txt' with content 'Hello from {provider_name}!'"

    print(f"Task: {task}")
    print()

    try:
        state = await runtime.run(
            task=task,
            workflow_id=workflow_id
        )

        print(f"[SUCCESS] Status: {state.status.value}")
        print(f"          Iterations: {state.iteration}")
        print(f"          Tool calls: {state.total_tool_calls}")
        print(f"          Cost: ${state.total_cost:.4f}")

        # Verify file
        test_file = workspace / f"{provider_name}_test.txt"
        if test_file.exists():
            print(f"          File created: {test_file.name}")

        cost_tracker.complete_workflow(workflow_id)

        return {
            "provider": provider_name,
            "success": True,
            "cost": state.total_cost,
            "iterations": state.iteration,
            "tool_calls": state.total_tool_calls
        }

    except Exception as e:
        print(f"[ERROR] {provider_name} failed: {e}")
        return {
            "provider": provider_name,
            "success": False,
            "error": str(e)
        }


async def main():
    """Test all available providers."""

    print("=" * 80)
    print("CODEXA Multi-Provider Test")
    print("=" * 80)

    # Setup workspace
    workspace = Path.cwd() / "workspace_multitest"
    workspace.mkdir(exist_ok=True)

    # Load API keys
    api_keys = APIKeyManager()
    cost_tracker = CostTracker()

    # Configure providers to test
    providers_to_test = []

    if api_keys.has_key("claude"):
        providers_to_test.append(("Claude", ModelType.CLAUDE_HAIKU, "claude"))

    if api_keys.has_key("openai"):
        providers_to_test.append(("OpenAI", ModelType.GPT_4_TURBO, "openai"))

    if api_keys.has_key("gemini"):
        providers_to_test.append(("Gemini", ModelType.GEMINI_PRO, "gemini"))

    if not providers_to_test:
        print("\n[ERROR] No API keys found!")
        print("Set at least one of: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY")
        return

    print(f"\nTesting with {len(providers_to_test)} provider(s):")
    for name, model, _ in providers_to_test:
        print(f"  - {name} ({model.value})")

    # Run tests
    results = []

    for name, model, key_name in providers_to_test:
        result = await run_with_provider(
            provider_name=name.lower(),
            model=model,
            api_key=api_keys.get_key(key_name),
            workspace=workspace,
            cost_tracker=cost_tracker
        )
        results.append(result)

    # Show summary
    print(f"\n{'=' * 80}")
    print("SUMMARY")
    print("=" * 80)
    print()

    for result in results:
        if result["success"]:
            print(f"{result['provider']:10} | "
                  f"Cost: ${result['cost']:.4f} | "
                  f"Iterations: {result['iterations']:2} | "
                  f"Tools: {result['tool_calls']:2} | "
                  f"[SUCCESS]")
        else:
            print(f"{result['provider']:10} | [FAILED] {result.get('error', 'Unknown error')}")

    print()

    # Overall stats
    stats = cost_tracker.get_stats()
    print("Overall Statistics:")
    print(f"  Total cost: ${stats['total_cost']:.4f}")
    print(f"  Total calls: {stats['total_calls']}")
    print(f"  Avg cost/call: ${stats['avg_cost_per_call']:.4f}")
    print()


if __name__ == "__main__":
    asyncio.run(main())
