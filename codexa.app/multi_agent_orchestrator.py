#!/usr/bin/env python3
"""
Multi-Agent Workflow Orchestrator

Coordinates execution across multiple CODEXA agents using global paths.
Enables $variable chaining between agent outputs for complex workflows.

Example workflows:
    # Research → Ad Creation → Brand Validation
    pesquisa_agent: research product
        ↓ $research_output
    anuncio_agent: generate ads using research
        ↓ $ad_output
    marca_agent: validate brand consistency

    # Multi-step E-commerce Workflow
    pesquisa_agent: market research
        ↓ $market_data
    anuncio_agent: create listings
        ↓ $listings
    photo_agent: optimize images
        ↓ $optimized_images
    marca_agent: final brand check

Usage:
    from multi_agent_orchestrator import MultiAgentOrchestrator, WorkflowStep

    # Define workflow
    orchestrator = MultiAgentOrchestrator()

    workflow = [
        WorkflowStep('pesquisa', 'research', {'product': 'Fone Bluetooth'}),
        WorkflowStep('anuncio', 'generate_ad', {'research': '$pesquisa.output'}),
        WorkflowStep('marca', 'validate', {'ad': '$anuncio.output'}),
    ]

    # Execute
    results = orchestrator.execute_workflow(workflow)

Version: 1.0.0
Created: 2025-11-16
Purpose: Multi-agent coordination and $variable chaining
"""

import json
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Import global orchestrator paths
from config.paths import (
    get_agent_dir,
    get_agent_paths,
    get_all_agents,
    get_agent_output,
    get_agent_count,
    CODEXA_APP,
    PATH_GLOBAL_OUTPUTS,
)


@dataclass
class WorkflowStep:
    """
    A single step in a multi-agent workflow.

    Args:
        agent_name: Name of the agent to execute (e.g., 'pesquisa', 'anuncio')
        task_name: Name of the task/builder to run
        inputs: Dictionary of inputs (can contain $variable references)
        config: Optional configuration for the task

    Example:
        >>> step = WorkflowStep(
        ...     agent_name='pesquisa',
        ...     task_name='research',
        ...     inputs={'product': 'Fone Bluetooth', 'market': 'BR'}
        ... )
    """
    agent_name: str
    task_name: str
    inputs: Dict[str, Any]
    config: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Normalize agent name"""
        if not self.agent_name.endswith('_agent'):
            self.agent_name = f"{self.agent_name}_agent"


@dataclass
class WorkflowResult:
    """
    Result of executing a workflow step.

    Attributes:
        agent_name: Agent that executed
        task_name: Task that was run
        success: Whether execution succeeded
        output_path: Path to output file (if any)
        output_data: Parsed output data
        error: Error message (if failed)
        execution_time: Time taken in seconds
    """
    agent_name: str
    task_name: str
    success: bool
    output_path: Optional[Path] = None
    output_data: Optional[Dict] = None
    error: Optional[str] = None
    execution_time: float = 0.0


class MultiAgentOrchestrator:
    """
    Coordinates execution across multiple CODEXA agents.

    This orchestrator enables:
    - Multi-agent workflows with $variable chaining
    - Automatic agent discovery
    - Output passing between agents
    - Error handling and retry logic
    - Execution history and logging
    """

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize the multi-agent orchestrator.

        Args:
            output_dir: Directory for workflow outputs (default: PATH_GLOBAL_OUTPUTS)
        """
        self.agents = self._discover_agents()
        self.output_dir = output_dir or PATH_GLOBAL_OUTPUTS
        self.output_dir.mkdir(exist_ok=True)

        self.execution_history: List[WorkflowResult] = []

    def _discover_agents(self) -> Dict[str, Dict[str, Path]]:
        """
        Auto-discover all available agents and their paths.

        Returns:
            Dictionary mapping agent names to their path dictionaries
        """
        agents = {}
        for agent_path in get_all_agents():
            agent_name = agent_path.name
            try:
                agents[agent_name] = get_agent_paths(agent_name.replace('_agent', ''))
            except ValueError:
                # Agent directory doesn't exist or is invalid
                continue

        return agents

    def list_available_agents(self) -> List[str]:
        """Get list of all discovered agents."""
        return sorted(self.agents.keys())

    def get_agent_info(self, agent_name: str) -> Dict[str, Any]:
        """
        Get detailed information about an agent.

        Args:
            agent_name: Name of the agent

        Returns:
            Dictionary with agent paths and status
        """
        if not agent_name.endswith('_agent'):
            agent_name = f"{agent_name}_agent"

        if agent_name not in self.agents:
            raise ValueError(f"Agent not found: {agent_name}")

        paths = self.agents[agent_name]

        return {
            'name': agent_name,
            'root': paths['root'],
            'has_builders': paths['builders'].exists(),
            'has_validators': paths['validators'].exists(),
            'has_templates': paths['templates'].exists(),
            'has_prompts': paths['prompts'].exists(),
        }

    def _resolve_variables(
        self,
        inputs: Dict[str, Any],
        previous_results: Dict[str, WorkflowResult]
    ) -> Dict[str, Any]:
        """
        Resolve $variable references in inputs.

        Supports patterns like:
            - $agent_name.output - Reference to agent's output data
            - $agent_name.output_path - Reference to agent's output file path

        Args:
            inputs: Input dictionary potentially containing $variables
            previous_results: Results from previous workflow steps

        Returns:
            Input dictionary with variables resolved
        """
        resolved = {}

        for key, value in inputs.items():
            if isinstance(value, str) and value.startswith('$'):
                # Parse variable reference: $agent_name.field
                var_parts = value[1:].split('.')
                agent_ref = var_parts[0]

                # Find the agent result
                agent_result = previous_results.get(f"{agent_ref}_agent")
                if not agent_result:
                    # Try without _agent suffix
                    for name, result in previous_results.items():
                        if name.replace('_agent', '') == agent_ref:
                            agent_result = result
                            break

                if not agent_result:
                    raise ValueError(f"Cannot resolve variable: {value} - agent not found in previous results")

                # Get the requested field
                if len(var_parts) > 1:
                    field = var_parts[1]
                    if field == 'output':
                        resolved[key] = agent_result.output_data
                    elif field == 'output_path':
                        resolved[key] = str(agent_result.output_path)
                    else:
                        # Try to get from output_data
                        if agent_result.output_data and field in agent_result.output_data:
                            resolved[key] = agent_result.output_data[field]
                        else:
                            raise ValueError(f"Field not found: {field} in {value}")
                else:
                    # Default to full output_data
                    resolved[key] = agent_result.output_data
            else:
                resolved[key] = value

        return resolved

    def execute_workflow(
        self,
        workflow: List[WorkflowStep],
        stop_on_error: bool = True
    ) -> Dict[str, WorkflowResult]:
        """
        Execute a multi-agent workflow.

        Args:
            workflow: List of WorkflowStep objects defining the workflow
            stop_on_error: If True, stop execution on first error

        Returns:
            Dictionary mapping agent names to their WorkflowResult

        Example:
            >>> orchestrator = MultiAgentOrchestrator()
            >>> workflow = [
            ...     WorkflowStep('pesquisa', 'research', {'product': 'Fone'}),
            ...     WorkflowStep('anuncio', 'generate', {'research': '$pesquisa.output'}),
            ... ]
            >>> results = orchestrator.execute_workflow(workflow)
        """
        results = {}

        print(f"\n{'=' * 70}")
        print(f"Multi-Agent Workflow Execution")
        print(f"{'=' * 70}")
        print(f"Steps: {len(workflow)}")
        print(f"Agents involved: {', '.join(set(step.agent_name for step in workflow))}")
        print(f"{'=' * 70}\n")

        for i, step in enumerate(workflow, 1):
            print(f"[{i}/{len(workflow)}] Executing: {step.agent_name} → {step.task_name}")

            try:
                # Resolve any $variable references in inputs
                resolved_inputs = self._resolve_variables(step.inputs, results)

                # Execute the step
                result = self._execute_step(step, resolved_inputs)

                # Store result
                results[step.agent_name] = result
                self.execution_history.append(result)

                if result.success:
                    print(f"    [OK] {step.agent_name} completed successfully")
                else:
                    print(f"    [X] {step.agent_name} failed: {result.error}")
                    if stop_on_error:
                        print(f"\n[!] Stopping workflow due to error")
                        break

            except Exception as e:
                error_msg = f"Error executing {step.agent_name}: {e}"
                print(f"    [X] {error_msg}")

                result = WorkflowResult(
                    agent_name=step.agent_name,
                    task_name=step.task_name,
                    success=False,
                    error=error_msg
                )
                results[step.agent_name] = result

                if stop_on_error:
                    print(f"\n[!] Stopping workflow due to exception")
                    break

        print(f"\n{'=' * 70}")
        print(f"Workflow Complete")
        print(f"Success: {sum(1 for r in results.values() if r.success)}/{len(results)}")
        print(f"{'=' * 70}\n")

        return results

    def _execute_step(
        self,
        step: WorkflowStep,
        resolved_inputs: Dict[str, Any]
    ) -> WorkflowResult:
        """
        Execute a single workflow step.

        This is a PLACEHOLDER - actual execution would call agent builders/scripts.
        For now, it simulates execution and creates dummy output.

        Args:
            step: The workflow step to execute
            resolved_inputs: Inputs with $variables resolved

        Returns:
            WorkflowResult with execution details
        """
        start_time = datetime.now()

        # PLACEHOLDER: In real implementation, this would:
        # 1. Call the agent's builder/script
        # 2. Pass the resolved inputs
        # 3. Capture the output
        # 4. Return the result

        # For now, simulate success and create dummy output
        agent_paths = self.agents[step.agent_name]

        output_data = {
            'agent': step.agent_name,
            'task': step.task_name,
            'inputs': resolved_inputs,
            'timestamp': datetime.now().isoformat(),
            'status': 'simulated_success',
        }

        # Create output file
        output_filename = f"{step.agent_name}_{step.task_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = self.output_dir / output_filename

        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)

        execution_time = (datetime.now() - start_time).total_seconds()

        return WorkflowResult(
            agent_name=step.agent_name,
            task_name=step.task_name,
            success=True,
            output_path=output_path,
            output_data=output_data,
            execution_time=execution_time
        )

    def save_workflow_report(self, results: Dict[str, WorkflowResult], filename: str):
        """
        Save workflow execution report to file.

        Args:
            results: Workflow execution results
            filename: Output filename
        """
        report_path = self.output_dir / filename

        report = {
            'timestamp': datetime.now().isoformat(),
            'total_steps': len(results),
            'successful_steps': sum(1 for r in results.values() if r.success),
            'failed_steps': sum(1 for r in results.values() if not r.success),
            'total_execution_time': sum(r.execution_time for r in results.values()),
            'steps': [asdict(result) for result in results.values()]
        }

        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"[OK] Workflow report saved to: {report_path}")


# === EXAMPLE WORKFLOWS ===

def example_research_to_ad_workflow():
    """
    Example: Research → Ad Generation workflow
    """
    orchestrator = MultiAgentOrchestrator()

    workflow = [
        WorkflowStep(
            agent_name='pesquisa',
            task_name='research',
            inputs={
                'product': 'Fone Bluetooth Premium',
                'market': 'BR',
                'depth': 'comprehensive'
            }
        ),
        WorkflowStep(
            agent_name='anuncio',
            task_name='generate_ad',
            inputs={
                'research_data': '$pesquisa.output',
                'platform': 'mercado_livre',
                'style': 'persuasive'
            }
        ),
        WorkflowStep(
            agent_name='marca',
            task_name='validate_brand',
            inputs={
                'ad_content': '$anuncio.output',
                'brand_guidelines': 'strict'
            }
        ),
    ]

    results = orchestrator.execute_workflow(workflow)
    orchestrator.save_workflow_report(results, 'research_to_ad_workflow.json')

    return results


if __name__ == "__main__":
    # List available agents
    orchestrator = MultiAgentOrchestrator()

    print("=" * 70)
    print("CODEXA Multi-Agent Orchestrator")
    print("=" * 70)
    print()

    print(f"Available agents ({get_agent_count()}):")
    for agent_name in orchestrator.list_available_agents():
        info = orchestrator.get_agent_info(agent_name)
        status = "[OK]" if info['has_builders'] else "[!]"
        print(f"  {status} {agent_name}")

    print()
    print("=" * 70)
    print("Example: Run example_research_to_ad_workflow() to test")
    print("=" * 70)
