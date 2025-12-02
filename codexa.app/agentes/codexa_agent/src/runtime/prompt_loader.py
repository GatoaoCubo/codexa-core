"""
Prompt Loader
Loads and composes prompts from the layer system.
"""

from pathlib import Path
from typing import List, Optional
import logging
import sys

logger = logging.getLogger(__name__)


class PromptLoader:
    """
    Loads prompts from the layer composition system.

    Integrates with the prompt layer composer to generate
    complete agent system prompts.
    """

    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize prompt loader.

        Args:
            project_root: Project root directory (will auto-detect if not provided)
        """
        self.project_root = project_root or self._find_project_root()
        self.prompts_path = self.project_root / "prompts"
        self.layers_path = self.prompts_path / "layers"
        self.composer_path = self.layers_path / "composer.py"

        # Verify structure exists
        if not self.composer_path.exists():
            raise RuntimeError(
                f"Prompt composer not found at: {self.composer_path}"
            )

        # Import composer
        self._composer = None

        logger.info(f"Initialized prompt loader: {self.project_root}")

    def compose_prompt(
        self,
        layer_ids: List[str],
        agent_name: Optional[str] = None,
        output_path: Optional[Path] = None
    ) -> str:
        """
        Compose prompt from layers.

        Args:
            layer_ids: List of layer IDs to compose
            agent_name: Optional agent name (for metadata)
            output_path: Optional path to save generated prompt

        Returns:
            Composed prompt text

        Raises:
            RuntimeError: If composition fails
        """
        try:
            # Get composer
            composer = self._get_composer()

            # Compose prompt
            logger.info(f"Composing prompt from layers: {layer_ids}")

            prompt_content = composer.compose_from_layers(
                layer_ids=layer_ids,
                output_file=str(output_path) if output_path else None
            )

            logger.info(
                f"Composed prompt: {len(prompt_content)} chars, "
                f"{len(layer_ids)} layers"
            )

            return prompt_content

        except Exception as e:
            logger.error(f"Failed to compose prompt: {e}")
            raise RuntimeError(f"Prompt composition failed: {e}") from e

    def load_agent_prompt(self, agent_type: str) -> str:
        """
        Load pre-generated agent prompt.

        Args:
            agent_type: Agent type (e.g., "planning", "execution")

        Returns:
            Agent system prompt

        Raises:
            RuntimeError: If agent prompt not found
        """
        # Look for generated agent file
        agent_file = self.project_root / "agents" / "generated" / f"{agent_type}_agent.md"

        if not agent_file.exists():
            raise RuntimeError(f"Agent prompt not found: {agent_file}")

        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()

            logger.info(f"Loaded agent prompt: {agent_type} ({len(content)} chars)")

            return content

        except Exception as e:
            logger.error(f"Failed to load agent prompt: {e}")
            raise RuntimeError(f"Failed to load agent prompt: {e}") from e

    def list_available_layers(self) -> List[str]:
        """
        List available prompt layers.

        Returns:
            List of layer IDs
        """
        try:
            composer = self._get_composer()
            config = composer._load_config()

            layers = []
            for layer_config in config.get("layers", {}).values():
                layer_id = layer_config.get("id")
                if layer_id:
                    layers.append(layer_id)

            return sorted(layers)

        except Exception as e:
            logger.error(f"Failed to list layers: {e}")
            return []

    def get_layer_info(self, layer_id: str) -> Optional[dict]:
        """
        Get information about a layer.

        Args:
            layer_id: Layer ID

        Returns:
            Layer metadata or None if not found
        """
        try:
            composer = self._get_composer()
            config = composer._load_config()

            for layer_config in config.get("layers", {}).values():
                if layer_config.get("id") == layer_id:
                    return {
                        "id": layer_config.get("id"),
                        "name": layer_config.get("name"),
                        "description": layer_config.get("description"),
                        "dependencies": layer_config.get("dependencies", []),
                        "file": layer_config.get("file"),
                    }

            return None

        except Exception as e:
            logger.error(f"Failed to get layer info: {e}")
            return None

    def _get_composer(self):
        """Get or create composer instance."""
        if self._composer:
            return self._composer

        try:
            # Add composer directory to path
            composer_dir = str(self.layers_path)
            if composer_dir not in sys.path:
                sys.path.insert(0, composer_dir)

            # Import composer module
            import composer as composer_module

            # Create composer instance
            self._composer = composer_module.PromptLayerComposer(
                layers_dir=str(self.layers_path)
            )

            return self._composer

        except Exception as e:
            logger.error(f"Failed to import composer: {e}")
            raise RuntimeError(f"Failed to load prompt composer: {e}") from e

    def _find_project_root(self) -> Path:
        """
        Find project root by looking for key markers.

        Returns:
            Project root path

        Raises:
            RuntimeError: If project root not found
        """
        current = Path.cwd()

        # Look for prompts/layers directory
        while current != current.parent:
            prompts_layers = current / "prompts" / "layers"
            if prompts_layers.exists():
                return current

            current = current.parent

        raise RuntimeError(
            "Could not find project root (no prompts/layers directory found)"
        )


# Predefined agent compositions

AGENT_COMPOSITIONS = {
    "planning": [
        "01_identity_layer",
        "02_core_instructions",
        "03_workflow_manager",
        "04_tool_definitions_readonly",
        "05_artifact_protocol",
        "07_output_format",
    ],
    "execution": [
        "01_identity_layer",
        "02_core_instructions",
        "03_workflow_manager",
        "06_tool_definitions_full",
        "05_artifact_protocol",
        "07_output_format",
    ],
    "verification": [
        "01_identity_layer",
        "02_core_instructions",
        "03_workflow_manager",
        "04_tool_definitions_readonly",
        "08_verification_protocol",
        "07_output_format",
    ],
    "orchestrator": [
        "01_identity_layer",
        "02_core_instructions",
        "03_workflow_manager",
        "04_tool_definitions_readonly",
        "05_artifact_protocol",
        "07_output_format",
    ],
    "full": [
        "01_identity_layer",
        "02_core_instructions",
        "03_workflow_manager",
        "06_tool_definitions_full",
        "05_artifact_protocol",
        "08_verification_protocol",
        "07_output_format",
    ],
}


def get_standard_composition(agent_type: str) -> List[str]:
    """
    Get standard layer composition for an agent type.

    Args:
        agent_type: Agent type (planning, execution, verification, orchestrator, full)

    Returns:
        List of layer IDs

    Raises:
        ValueError: If agent type not recognized
    """
    if agent_type not in AGENT_COMPOSITIONS:
        raise ValueError(
            f"Unknown agent type: {agent_type}. "
            f"Available: {list(AGENT_COMPOSITIONS.keys())}"
        )

    return AGENT_COMPOSITIONS[agent_type]
