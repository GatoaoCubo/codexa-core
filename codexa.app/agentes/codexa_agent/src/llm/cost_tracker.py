"""
Cost Tracker
Tracks LLM API costs across workflows and agents.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from datetime import datetime
import json
from pathlib import Path
import logging

from .provider import LLMResponse

logger = logging.getLogger(__name__)


@dataclass
class WorkflowCost:
    """Cost tracking for a workflow."""
    workflow_id: str
    started_at: datetime
    completed_at: datetime | None = None
    total_cost: float = 0.0
    total_tokens: int = 0
    llm_calls: int = 0
    agent_costs: Dict[str, float] = field(default_factory=dict)
    provider_costs: Dict[str, float] = field(default_factory=dict)
    model_costs: Dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "workflow_id": self.workflow_id,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "total_cost": self.total_cost,
            "total_tokens": self.total_tokens,
            "llm_calls": self.llm_calls,
            "agent_costs": self.agent_costs,
            "provider_costs": self.provider_costs,
            "model_costs": self.model_costs,
        }


class CostTracker:
    """
    Tracks LLM API costs for workflows and agents.

    Features:
    - Per-workflow cost tracking
    - Per-agent cost tracking
    - Per-provider cost tracking
    - Per-model cost tracking
    - Historical cost analysis
    """

    def __init__(self, storage_path: Path | None = None):
        """
        Initialize cost tracker.

        Args:
            storage_path: Path to store cost data (default: .codexa/costs/)
        """
        self.storage_path = storage_path or Path(".codexa/costs")
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.workflows: Dict[str, WorkflowCost] = {}
        self.total_cost = 0.0
        self.total_tokens = 0
        self.total_calls = 0

    def start_workflow(self, workflow_id: str):
        """Start tracking a workflow."""
        self.workflows[workflow_id] = WorkflowCost(
            workflow_id=workflow_id,
            started_at=datetime.now()
        )
        logger.info(f"Started cost tracking for workflow: {workflow_id}")

    def track_llm_call(
        self,
        workflow_id: str,
        agent_id: str,
        response: LLMResponse
    ):
        """
        Track an LLM API call.

        Args:
            workflow_id: Workflow ID
            agent_id: Agent ID that made the call
            response: LLM response
        """
        if workflow_id not in self.workflows:
            logger.warning(f"Workflow {workflow_id} not started, starting now")
            self.start_workflow(workflow_id)

        workflow = self.workflows[workflow_id]

        # Update workflow totals
        workflow.total_cost += response.cost_usd
        workflow.total_tokens += response.tokens_used
        workflow.llm_calls += 1

        # Track per-agent cost
        if agent_id not in workflow.agent_costs:
            workflow.agent_costs[agent_id] = 0.0
        workflow.agent_costs[agent_id] += response.cost_usd

        # Track per-provider cost
        provider = response.provider
        if provider not in workflow.provider_costs:
            workflow.provider_costs[provider] = 0.0
        workflow.provider_costs[provider] += response.cost_usd

        # Track per-model cost
        model = response.model
        if model not in workflow.model_costs:
            workflow.model_costs[model] = 0.0
        workflow.model_costs[model] += response.cost_usd

        # Update global totals
        self.total_cost += response.cost_usd
        self.total_tokens += response.tokens_used
        self.total_calls += 1

        logger.debug(
            f"Tracked LLM call: workflow={workflow_id}, agent={agent_id}, "
            f"cost=${response.cost_usd:.4f}, tokens={response.tokens_used}"
        )

    def complete_workflow(self, workflow_id: str):
        """Mark workflow as completed."""
        if workflow_id in self.workflows:
            self.workflows[workflow_id].completed_at = datetime.now()
            self._save_workflow(workflow_id)
            logger.info(
                f"Completed workflow {workflow_id}: "
                f"${self.workflows[workflow_id].total_cost:.4f}, "
                f"{self.workflows[workflow_id].llm_calls} calls"
            )

    def get_workflow_cost(self, workflow_id: str) -> WorkflowCost | None:
        """Get cost data for a workflow."""
        return self.workflows.get(workflow_id)

    def get_total_cost(self) -> float:
        """Get total cost across all workflows."""
        return self.total_cost

    def get_stats(self) -> Dict[str, Any]:
        """Get overall cost statistics."""
        return {
            "total_cost": self.total_cost,
            "total_tokens": self.total_tokens,
            "total_calls": self.total_calls,
            "avg_cost_per_call": self.total_cost / self.total_calls if self.total_calls > 0 else 0,
            "avg_tokens_per_call": self.total_tokens / self.total_calls if self.total_calls > 0 else 0,
            "workflows_tracked": len(self.workflows),
        }

    def _save_workflow(self, workflow_id: str):
        """Save workflow cost data to disk."""
        if workflow_id not in self.workflows:
            return

        workflow = self.workflows[workflow_id]
        cost_file = self.storage_path / f"{workflow_id}_cost.json"

        try:
            with open(cost_file, 'w', encoding='utf-8') as f:
                json.dump(workflow.to_dict(), f, indent=2)
            logger.debug(f"Saved cost data for workflow: {workflow_id}")
        except Exception as e:
            logger.error(f"Failed to save cost data: {e}")

    def get_workflow_summary(self, workflow_id: str) -> str:
        """Get human-readable cost summary for workflow."""
        workflow = self.get_workflow_cost(workflow_id)
        if not workflow:
            return f"Workflow {workflow_id} not found"

        summary = f"""
Workflow Cost Summary: {workflow_id}
================================================================================
Total Cost: ${workflow.total_cost:.4f}
Total Tokens: {workflow.total_tokens:,}
LLM Calls: {workflow.llm_calls}
Duration: {(workflow.completed_at - workflow.started_at).total_seconds():.1f}s

Per-Agent Costs:
"""
        for agent, cost in sorted(workflow.agent_costs.items(), key=lambda x: x[1], reverse=True):
            summary += f"  {agent}: ${cost:.4f}\n"

        summary += "\nPer-Provider Costs:\n"
        for provider, cost in sorted(workflow.provider_costs.items(), key=lambda x: x[1], reverse=True):
            summary += f"  {provider}: ${cost:.4f}\n"

        summary += "\nPer-Model Costs:\n"
        for model, cost in sorted(workflow.model_costs.items(), key=lambda x: x[1], reverse=True):
            summary += f"  {model}: ${cost:.4f}\n"

        return summary
