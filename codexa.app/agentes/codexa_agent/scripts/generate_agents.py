#!/usr/bin/env python3
"""
Generate specialized agents using the layer composer.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "prompts" / "layers"))

from composer import LayerComposer

def main():
    """Generate all specialized agents."""
    # Initialize composer
    config_path = Path("config/prompt_layers.yml")
    composer = LayerComposer(config_path)

    # Output directory
    output_dir = Path("agents/generated")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Agents to generate
    agents = [
        ("planning", "planning_agent.md"),
        ("execution", "execution_agent.md"),
        ("verification", "verification_agent.md"),
        ("orchestrator", "orchestrator_agent.md"),
        ("full", "full_agent.md"),
    ]

    print("Generating specialized agents...\n")

    for preset_name, output_file in agents:
        print(f"Generating {preset_name} agent...")

        try:
            # Compose agent from preset
            composed_prompt = composer.compose_preset(preset_name)

            # Write to file
            output_path = output_dir / output_file
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(composed_prompt)

            # Get stats
            lines = len(composed_prompt.split('\n'))
            chars = len(composed_prompt)

            print(f"  SUCCESS: {output_path}")
            print(f"  Size: {lines} lines, {chars:,} characters\n")

        except Exception as e:
            print(f"  ERROR: {e}\n")
            continue

    print("Agent generation complete!")

if __name__ == "__main__":
    main()
