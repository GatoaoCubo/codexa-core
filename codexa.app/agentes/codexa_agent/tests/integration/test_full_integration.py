"""
Full Integration Test
Tests the complete CODEXA system end-to-end.
"""

import pytest
import asyncio
from pathlib import Path
import tempfile
import shutil

from src.llm.provider_factory import ProviderFactory
from src.llm.provider import ModelType
from src.llm.cost_tracker import CostTracker
from src.tools.executor import ToolExecutor
from src.tools.file_tools import FileTools
from src.tools.bash_tools import BashTools
from src.tools.permissions import (
    PermissionManager,
    create_full_access_permission,
    create_read_only_permission,
)
from src.runtime.agent_runtime import AgentRuntime, AgentConfig
from src.runtime.prompt_loader import PromptLoader, get_standard_composition
from src.auth.api_keys import APIKeyManager


class TestFullIntegration:
    """End-to-end integration tests."""

    @pytest.fixture
    def temp_workspace(self):
        """Create temporary workspace for tests."""
        workspace = Path(tempfile.mkdtemp())
        yield workspace
        shutil.rmtree(workspace)

    @pytest.fixture
    def api_key_manager(self):
        """Create API key manager."""
        return APIKeyManager(auto_load=True)

    @pytest.fixture
    def cost_tracker(self, temp_workspace):
        """Create cost tracker."""
        return CostTracker(storage_path=temp_workspace / "costs")

    @pytest.fixture
    def tool_executor(self, temp_workspace):
        """Create tool executor with file and bash tools."""
        # Create permission manager
        permission_manager = PermissionManager(workspace_path=temp_workspace)

        # Register test agent with full access
        permission_manager.register_agent(
            agent_id="test_agent",
            permission=create_full_access_permission("test_agent")
        )

        # Create tool executor
        executor = ToolExecutor(permission_manager=permission_manager)

        # Register file tools
        file_tools = FileTools(base_path=temp_workspace)
        executor.register_tool("read", file_tools.read)
        executor.register_tool("write", file_tools.write)
        executor.register_tool("edit", file_tools.edit)
        executor.register_tool("glob", file_tools.glob)
        executor.register_tool("grep", file_tools.grep)

        # Register bash tools
        bash_tools = BashTools(base_path=temp_workspace)
        executor.register_tool("bash", bash_tools.execute)

        return executor

    @pytest.mark.asyncio
    async def test_tool_execution(self, tool_executor, temp_workspace):
        """Test basic tool execution."""
        # Test write
        result = await tool_executor.execute(
            tool_name="write",
            arguments={
                "file_path": "test.txt",
                "content": "Hello World"
            },
            agent_id="test_agent"
        )
        assert result.success
        assert (temp_workspace / "test.txt").exists()

        # Test read
        result = await tool_executor.execute(
            tool_name="read",
            arguments={"file_path": "test.txt"},
            agent_id="test_agent"
        )
        assert result.success
        assert "Hello World" in result.output

        # Test glob
        result = await tool_executor.execute(
            tool_name="glob",
            arguments={"pattern": "*.txt"},
            agent_id="test_agent"
        )
        assert result.success
        assert "test.txt" in result.output

    @pytest.mark.asyncio
    async def test_permission_system(self, temp_workspace):
        """Test permission enforcement."""
        # Create permission manager with read-only agent
        permission_manager = PermissionManager(workspace_path=temp_workspace)
        permission_manager.register_agent(
            agent_id="readonly_agent",
            permission=create_read_only_permission("readonly_agent")
        )

        # Create executor
        executor = ToolExecutor(permission_manager=permission_manager)
        file_tools = FileTools(base_path=temp_workspace)
        executor.register_tool("read", file_tools.read)
        executor.register_tool("write", file_tools.write)

        # Create test file first
        test_file = temp_workspace / "test.txt"
        test_file.write_text("test")

        # Read should succeed
        result = await executor.execute(
            tool_name="read",
            arguments={"file_path": "test.txt"},
            agent_id="readonly_agent"
        )
        assert result.success

        # Write should fail (permission denied)
        result = await executor.execute(
            tool_name="write",
            arguments={
                "file_path": "test2.txt",
                "content": "test"
            },
            agent_id="readonly_agent"
        )
        assert not result.success
        assert "Permission denied" in result.error

    @pytest.mark.asyncio
    async def test_llm_providers(self, api_key_manager):
        """Test LLM provider creation and basic functionality."""
        providers_to_test = []

        # Test Claude if API key available
        if api_key_manager.has_key("claude"):
            providers_to_test.append(("claude", ModelType.CLAUDE_HAIKU))

        # Test OpenAI if API key available
        if api_key_manager.has_key("openai"):
            providers_to_test.append(("openai", ModelType.GPT4_TURBO))

        # Test Gemini if API key available
        if api_key_manager.has_key("gemini"):
            providers_to_test.append(("gemini", ModelType.GEMINI_PRO))

        if not providers_to_test:
            pytest.skip("No API keys available for testing")

        for provider_name, model in providers_to_test:
            # Create provider
            api_key = api_key_manager.get_key(provider_name)
            provider = ProviderFactory.create_provider(
                model=model,
                api_key=api_key
            )

            # Test simple completion
            response = await provider.complete(
                messages=[{"role": "user", "content": "Say 'test successful'"}],
                system="You are a test assistant."
            )

            assert response.success
            assert len(response.content) > 0
            assert response.cost_usd >= 0

    @pytest.mark.asyncio
    @pytest.mark.slow
    async def test_agent_runtime_simple_task(
        self,
        api_key_manager,
        cost_tracker,
        tool_executor,
        temp_workspace
    ):
        """Test agent runtime with a simple task."""
        # Skip if no API keys
        if not api_key_manager.has_key("claude"):
            pytest.skip("Claude API key not available")

        # Create LLM provider (using fast/cheap model for testing)
        provider = ProviderFactory.create_provider(
            model=ModelType.CLAUDE_HAIKU,
            api_key=api_key_manager.get_key("claude")
        )

        # Create simple system prompt
        system_prompt = """You are a helpful assistant that can use tools.

Your task is to help the user with file operations.

Available tools:
- read: Read file contents
- write: Write content to a file
- glob: Find files by pattern
- grep: Search for text in files

When given a task, think step by step and use the appropriate tools."""

        # Create agent config
        config = AgentConfig(
            agent_id="test_agent",
            agent_type="test",
            system_prompt=system_prompt,
            llm_provider=provider,
            tool_executor=tool_executor,
            permission=create_full_access_permission("test_agent"),
            max_iterations=10,
            workspace_path=temp_workspace
        )

        # Create runtime
        runtime = AgentRuntime(
            config=config,
            cost_tracker=cost_tracker
        )

        # Run simple task
        task = "Create a file called 'hello.txt' with the content 'Hello from CODEXA!'"

        state = await runtime.run(
            task=task,
            workflow_id="test_workflow_001"
        )

        # Verify completion
        assert state.status.value in ["completed", "blocked"]
        assert state.iteration > 0
        assert state.total_tool_calls > 0

        # Verify file was created
        assert (temp_workspace / "hello.txt").exists()
        content = (temp_workspace / "hello.txt").read_text()
        assert "Hello from CODEXA" in content

        # Verify cost tracking
        workflow_cost = cost_tracker.get_workflow_cost("test_workflow_001")
        assert workflow_cost is not None
        assert workflow_cost.total_cost > 0
        assert workflow_cost.llm_calls > 0

    @pytest.mark.asyncio
    async def test_cost_tracking(self, cost_tracker, api_key_manager):
        """Test cost tracking functionality."""
        if not api_key_manager.has_key("claude"):
            pytest.skip("Claude API key not available")

        workflow_id = "test_cost_workflow"
        cost_tracker.start_workflow(workflow_id)

        # Create provider and make a call
        provider = ProviderFactory.create_provider(
            model=ModelType.CLAUDE_HAIKU,
            api_key=api_key_manager.get_key("claude")
        )

        response = await provider.complete(
            messages=[{"role": "user", "content": "Hello"}],
            system="You are a test assistant."
        )

        # Track the call
        cost_tracker.track_llm_call(
            workflow_id=workflow_id,
            agent_id="test_agent",
            response=response
        )

        # Verify tracking
        workflow_cost = cost_tracker.get_workflow_cost(workflow_id)
        assert workflow_cost is not None
        assert workflow_cost.total_cost > 0
        assert workflow_cost.total_tokens > 0
        assert workflow_cost.llm_calls == 1
        assert "test_agent" in workflow_cost.agent_costs

    def test_prompt_loader(self):
        """Test prompt loader functionality."""
        try:
            loader = PromptLoader()

            # Test listing layers
            layers = loader.list_available_layers()
            assert len(layers) > 0
            assert "01_identity_layer" in layers

            # Test getting layer info
            info = loader.get_layer_info("01_identity_layer")
            assert info is not None
            assert info["id"] == "01_identity_layer"

            # Test standard compositions
            planning_layers = get_standard_composition("planning")
            assert len(planning_layers) > 0
            assert "01_identity_layer" in planning_layers

        except RuntimeError as e:
            pytest.skip(f"Prompt loader not available: {e}")


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
