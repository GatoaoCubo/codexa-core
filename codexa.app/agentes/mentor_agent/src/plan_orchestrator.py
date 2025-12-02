"""
Mentor Orchestrator - Strategic Plan Generation and Execution Logic

This module contains the core orchestration logic for the Mentor Agent.
It handles:
- Strategic plan generation from business objectives
- Agent delegation for research, ad creation, tracking
- Result consolidation from multiple agents
- KPI evaluation and tactical recommendations
- Knowledge base integration
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Tuple
from datetime import datetime, date, timedelta
import re

# Import agent execution module
from agent import (
    AgentTemplateRequest,
    execute_template,
    generate_short_id,
)

# Import strategic plan models
from strategic_plan_models import (
    StrategicPlan,
    Tactic,
    KPI,
    Milestone,
    Deliverable,
    AgentDelegation,
    CompetitiveInsight,
    KnowledgeInsight,
    DecisionPoint,
    TacticStatus,
    Priority,
    PlanStatus,
)

# Import utility functions
from utils import parse_json


class MentorOrchestrator:
    """
    High-level orchestrator for strategic e-commerce planning.

    This class handles the tactical intelligence and agent coordination
    for the Mentor Agent system.
    """

    def __init__(self, working_dir: Optional[str] = None):
        """Initialize the orchestrator.

        Args:
            working_dir: Working directory for agent execution (defaults to cwd)
        """
        self.working_dir = working_dir or os.getcwd()
        self.knowledge_base_path = Path(self.working_dir) / "knowledge_base"
        self.user_docs_path = Path(self.working_dir) / "USER_DOCS"
        self.agents_output_path = Path(self.working_dir) / "agents"

    # ===================================================================
    # STRATEGIC PLAN GENERATION
    # ===================================================================

    def analyze_objective(self, objective_text: str) -> Dict[str, Any]:
        """Parse and analyze a business objective.

        Extracts key information like:
        - Primary goal
        - Target market/product
        - Competitive context
        - Implied KPIs

        Args:
            objective_text: The business objective statement

        Returns:
            Dictionary with analyzed components
        """
        analysis = {
            "raw_objective": objective_text,
            "primary_goal": "",
            "target_market": None,
            "target_product": None,
            "competitors": [],
            "implied_kpis": [],
            "urgency": "medium"
        }

        # Extract primary goal (verbs like: outrank, launch, increase, optimize, etc.)
        goal_verbs = ["outrank", "launch", "increase", "optimize", "improve", "achieve", "reach", "grow"]
        for verb in goal_verbs:
            if verb.lower() in objective_text.lower():
                analysis["primary_goal"] = verb
                break

        # Extract competitor mentions
        competitor_patterns = [
            r"outrank\s+([A-Za-z0-9\s]+?)(?:\s+on|\s+in|$)",
            r"compete\s+with\s+([A-Za-z0-9\s]+?)(?:\s+on|\s+in|$)",
            r"vs\.?\s+([A-Za-z0-9\s]+?)(?:\s+on|\s+in|$)"
        ]
        for pattern in competitor_patterns:
            match = re.search(pattern, objective_text, re.IGNORECASE)
            if match:
                analysis["competitors"].append(match.group(1).strip())

        # Extract urgency indicators
        if any(word in objective_text.lower() for word in ["urgent", "asap", "immediately", "critical"]):
            analysis["urgency"] = "high"
        elif any(word in objective_text.lower() for word in ["eventually", "long-term", "future"]):
            analysis["urgency"] = "low"

        return analysis

    def generate_tactical_plan(
        self,
        objective: str,
        market_context: Optional[str] = None,
        suggested_kpis: Optional[List[KPI]] = None
    ) -> StrategicPlan:
        """Generate a comprehensive tactical plan from a business objective.

        Args:
            objective: Business objective statement
            market_context: Optional market context/background
            suggested_kpis: Optional pre-defined KPIs (otherwise inferred)

        Returns:
            A StrategicPlan with generated tactics, KPIs, and milestones
        """
        # Analyze the objective
        analysis = self.analyze_objective(objective)

        # Generate title from objective
        title = objective[:50] if len(objective) <= 50 else objective[:47] + "..."

        # Infer KPIs if not provided
        if not suggested_kpis:
            suggested_kpis = self._infer_kpis_from_objective(analysis)

        # Generate tactical sequence
        tactics = self._generate_tactics_sequence(analysis, market_context)

        # Generate milestones
        milestones = self._generate_milestones(tactics)

        # Determine priority
        priority = Priority.HIGH if analysis["urgency"] == "high" else Priority.MEDIUM

        # Create the strategic plan
        plan = StrategicPlan(
            title=title,
            objective=objective,
            kpis=suggested_kpis,
            tactics=tactics,
            milestones=milestones,
            priority=priority,
            status=PlanStatus.DRAFT
        )

        return plan

    def _infer_kpis_from_objective(self, analysis: Dict[str, Any]) -> List[KPI]:
        """Infer appropriate KPIs based on objective analysis."""
        kpis = []

        goal = analysis["primary_goal"]

        # Common KPI templates by goal type
        if goal == "outrank":
            kpis.append(KPI(name="Marketplace Ranking", target=3, unit="position"))
            kpis.append(KPI(name="Organic Traffic", target=1000, unit="visits/month"))

        elif goal == "launch":
            kpis.append(KPI(name="Sales", target=500, unit="units/month"))
            kpis.append(KPI(name="Conversion Rate", target=3.0, unit="%"))

        elif goal in ["increase", "grow"]:
            kpis.append(KPI(name="Revenue Growth", target=20, unit="%"))
            kpis.append(KPI(name="Sales Volume", target=1000, unit="units"))

        elif goal == "optimize":
            kpis.append(KPI(name="Conversion Rate", target=5.0, unit="%"))
            kpis.append(KPI(name="ROI", target=150, unit="%"))

        # Default fallback KPIs
        if not kpis:
            kpis.append(KPI(name="Sales", target=500, unit="units"))
            kpis.append(KPI(name="Revenue", target=50000, unit="BRL"))

        return kpis

    def _generate_tactics_sequence(
        self,
        analysis: Dict[str, Any],
        market_context: Optional[str]
    ) -> List[Tactic]:
        """Generate a sequenced list of tactics based on objective analysis."""
        tactics = []

        # Tactic 1: Market Research (always first, no dependencies)
        research_desc = "Conduct comprehensive market research"
        if analysis["competitors"]:
            research_desc += f" focusing on competitors: {', '.join(analysis['competitors'])}"

        tactics.append(Tactic(
            description=research_desc,
            rationale="Understanding the market landscape is critical before taking action",
            agent_delegation=AgentDelegation(
                agent_name="pesquisa",
                slash_command="/pesquisa",
                args=[analysis["raw_objective"]]
            ),
            priority=Priority.HIGH,
            dependencies=[]
        ))

        # Tactic 2: Competitive Analysis (depends on research)
        if analysis["competitors"]:
            tactics.append(Tactic(
                description=f"Analyze competitor strategies and weaknesses",
                rationale="Identify gaps and opportunities in competitor approaches",
                agent_delegation=AgentDelegation(
                    agent_name="pesquisa",
                    slash_command="/pesquisa",
                    args=[f"competitive analysis {analysis['competitors'][0]}"]
                ),
                priority=Priority.HIGH,
                dependencies=[tactics[0].id]
            ))

        # Tactic 3: Content/Ad Generation (depends on research)
        if analysis["primary_goal"] in ["launch", "outrank", "increase"]:
            research_dep_id = tactics[0].id
            tactics.append(Tactic(
                description="Generate optimized ad copy and product listings",
                rationale="High-quality content is essential for conversion and ranking",
                agent_delegation=AgentDelegation(
                    agent_name="codex_anuncio",
                    slash_command="/codex_anuncio",
                    args=["generate listings based on research"]
                ),
                priority=Priority.MEDIUM,
                dependencies=[research_dep_id]
            ))

        # Tactic 4: Implementation/Launch (depends on content)
        if len(tactics) >= 3:
            tactics.append(Tactic(
                description="Deploy optimized listings to marketplace",
                rationale="Execute the strategy with optimized content",
                priority=Priority.MEDIUM,
                dependencies=[tactics[-1].id]
            ))

        # Tactic 5: Monitoring and Optimization (depends on launch)
        tactics.append(Tactic(
            description="Monitor performance and iterate on strategy",
            rationale="Continuous optimization is key to sustained success",
            agent_delegation=AgentDelegation(
                agent_name="orchestrator",
                slash_command="/orchestrator",
                args=["track performance metrics"]
            ),
            priority=Priority.MEDIUM,
            dependencies=[tactics[-1].id] if len(tactics) > 1 else []
        ))

        return tactics

    def _generate_milestones(self, tactics: List[Tactic]) -> List[Milestone]:
        """Generate milestones based on tactical sequence."""
        milestones = []

        # Milestone 1: Research Complete (first 2-3 tactics)
        research_tactics = [t for t in tactics[:3] if "research" in t.description.lower() or "analyz" in t.description.lower()]
        if research_tactics:
            deliverables = [Deliverable(description=t.description) for t in research_tactics]
            milestones.append(Milestone(
                title="Market Research Complete",
                description="Comprehensive understanding of market and competitors",
                deadline=date.today() + timedelta(days=7),
                deliverables=deliverables
            ))

        # Milestone 2: Content Ready (content/ad generation tactics)
        content_tactics = [t for t in tactics if any(word in t.description.lower() for word in ["content", "ad", "listing", "copy"])]
        if content_tactics:
            deliverables = [Deliverable(description=t.description) for t in content_tactics]
            milestones.append(Milestone(
                title="Content Assets Ready",
                description="All content and ad copy generated and approved",
                deadline=date.today() + timedelta(days=14),
                deliverables=deliverables
            ))

        # Milestone 3: Launch/Implementation (implementation tactics)
        impl_tactics = [t for t in tactics if any(word in t.description.lower() for word in ["deploy", "launch", "implement", "execute"])]
        if impl_tactics:
            deliverables = [Deliverable(description=t.description) for t in impl_tactics]
            milestones.append(Milestone(
                title="Strategy Deployed",
                description="All tactics implemented in marketplace",
                deadline=date.today() + timedelta(days=21),
                deliverables=deliverables
            ))

        # Milestone 4: Results Measured (monitoring tactics)
        monitor_tactics = [t for t in tactics if any(word in t.description.lower() for word in ["monitor", "track", "optimize", "measure"])]
        if monitor_tactics:
            deliverables = [Deliverable(description=t.description) for t in monitor_tactics]
            milestones.append(Milestone(
                title="Initial Results Measured",
                description="Performance data collected and analyzed",
                deadline=date.today() + timedelta(days=30),
                deliverables=deliverables
            ))

        return milestones

    # ===================================================================
    # AGENT DELEGATION
    # ===================================================================

    def delegate_research(self, research_query: str, tactic_id: Optional[str] = None) -> Dict[str, Any]:
        """Delegate research to the pesquisa agent.

        Args:
            research_query: The research query/objective
            tactic_id: Optional tactic ID for tracking

        Returns:
            Dictionary with research results and metadata
        """
        adw_id = generate_short_id()

        request = AgentTemplateRequest(
            agent_name="research-delegated",
            slash_command="/pesquisa",
            args=[research_query],
            adw_id=adw_id,
            model="sonnet",
            working_dir=self.working_dir
        )

        response = execute_template(request)

        result = {
            "success": response.success,
            "adw_id": adw_id,
            "tactic_id": tactic_id,
            "output_raw": response.output,
            "insights": [],
            "error": None
        }

        if response.success:
            # Parse research results
            result["insights"] = self._parse_research_output(response.output)
        else:
            result["error"] = f"Research delegation failed: {response.output[:200]}"

        return result

    def delegate_ad_creation(self, product_info: str, tactic_id: Optional[str] = None) -> Dict[str, Any]:
        """Delegate ad creation to the codex_anuncio agent.

        Args:
            product_info: Product information for ad generation
            tactic_id: Optional tactic ID for tracking

        Returns:
            Dictionary with ad generation results
        """
        adw_id = generate_short_id()

        request = AgentTemplateRequest(
            agent_name="adgen-delegated",
            slash_command="/codex_anuncio",
            args=[product_info],
            adw_id=adw_id,
            model="sonnet",
            working_dir=self.working_dir
        )

        response = execute_template(request)

        result = {
            "success": response.success,
            "adw_id": adw_id,
            "tactic_id": tactic_id,
            "output_raw": response.output,
            "ads_generated": [],
            "error": None
        }

        if response.success:
            # Parse ad generation results
            result["ads_generated"] = self._parse_ad_output(response.output)
        else:
            result["error"] = f"Ad generation failed: {response.output[:200]}"

        return result

    def delegate_tracking(self, tracking_query: str, tactic_id: Optional[str] = None) -> Dict[str, Any]:
        """Delegate tracking to the orchestrator agent.

        Args:
            tracking_query: Tracking query/objective
            tactic_id: Optional tactic ID for tracking

        Returns:
            Dictionary with tracking results
        """
        adw_id = generate_short_id()

        request = AgentTemplateRequest(
            agent_name="tracking-delegated",
            slash_command="/orchestrator",
            args=[tracking_query],
            adw_id=adw_id,
            model="sonnet",
            working_dir=self.working_dir
        )

        response = execute_template(request)

        result = {
            "success": response.success,
            "adw_id": adw_id,
            "tactic_id": tactic_id,
            "output_raw": response.output,
            "metrics": {},
            "error": None
        }

        if response.success:
            # Parse tracking results
            result["metrics"] = self._parse_tracking_output(response.output)
        else:
            result["error"] = f"Tracking failed: {response.output[:200]}"

        return result

    # ===================================================================
    # RESULT PARSING AND CONSOLIDATION
    # ===================================================================

    def _parse_research_output(self, output: str) -> List[str]:
        """Parse research agent output to extract key insights."""
        insights = []

        # Try to parse as JSON first
        try:
            data = parse_json(output, dict)
            if isinstance(data, dict):
                if "insights" in data:
                    insights = data["insights"]
                elif "findings" in data:
                    insights = data["findings"]
                elif "results" in data:
                    insights = data["results"]
        except:
            # Fallback: extract bullet points or numbered lists
            lines = output.split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith("-") or line.startswith("*") or re.match(r"^\d+\.", line):
                    # Remove list markers
                    insight = re.sub(r"^[-*\d.]+\s*", "", line).strip()
                    if len(insight) > 20:  # Meaningful insights only
                        insights.append(insight)

        return insights[:10]  # Limit to top 10 insights

    def _parse_ad_output(self, output: str) -> List[Dict[str, str]]:
        """Parse ad generation output to extract generated ads."""
        ads = []

        # Try JSON parsing first
        try:
            data = parse_json(output, dict)
            if isinstance(data, dict) and "ads" in data:
                ads = data["ads"]
        except:
            # Fallback: look for structured ad content
            # This is a simplified parser; real implementation would be more robust
            pass

        return ads

    def _parse_tracking_output(self, output: str) -> Dict[str, Any]:
        """Parse tracking output to extract metrics."""
        metrics = {}

        try:
            data = parse_json(output, dict)
            if isinstance(data, dict):
                metrics = data.get("metrics", {})
        except:
            pass

        return metrics

    def consolidate_results(self, agent_outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Consolidate results from multiple agent executions.

        Args:
            agent_outputs: List of agent output dictionaries

        Returns:
            Consolidated results with key findings
        """
        consolidated = {
            "total_executions": len(agent_outputs),
            "successful_executions": sum(1 for out in agent_outputs if out.get("success")),
            "failed_executions": sum(1 for out in agent_outputs if not out.get("success")),
            "all_insights": [],
            "key_findings": [],
            "errors": []
        }

        for output in agent_outputs:
            if output.get("success"):
                if "insights" in output:
                    consolidated["all_insights"].extend(output["insights"])
            else:
                if "error" in output:
                    consolidated["errors"].append(output["error"])

        # Extract top key findings (most frequent or highest confidence)
        # For v1, just take the first 5 unique insights
        seen = set()
        for insight in consolidated["all_insights"]:
            if insight not in seen and len(consolidated["key_findings"]) < 5:
                consolidated["key_findings"].append(insight)
                seen.add(insight)

        return consolidated

    # ===================================================================
    # KPI EVALUATION
    # ===================================================================

    def evaluate_kpis(self, plan_id: str, plan: StrategicPlan) -> Dict[str, Any]:
        """Evaluate KPI performance for a strategic plan.

        Args:
            plan_id: Plan identifier
            plan: The strategic plan to evaluate

        Returns:
            Evaluation results with recommendations
        """
        evaluation = {
            "plan_id": plan_id,
            "overall_achievement": plan.get_overall_kpi_achievement(),
            "kpi_details": [],
            "status": "on_track",
            "recommendations": []
        }

        for kpi in plan.kpis:
            achievement = kpi.calculate_achievement_percentage()
            kpi_eval = {
                "name": kpi.name,
                "target": kpi.target,
                "current": kpi.current,
                "achievement": achievement,
                "status": kpi.status.value
            }

            # Generate recommendations based on performance
            if achievement < 50:
                kpi_eval["recommendation"] = f"URGENT: {kpi.name} significantly below target. Reassess strategy."
            elif achievement < 80:
                kpi_eval["recommendation"] = f"ATTENTION: {kpi.name} needs improvement. Review tactics."
            elif achievement >= 100:
                kpi_eval["recommendation"] = f"SUCCESS: {kpi.name} target achieved. Consider raising target."
            else:
                kpi_eval["recommendation"] = f"ON TRACK: {kpi.name} progressing well."

            evaluation["kpi_details"].append(kpi_eval)

        # Overall status
        avg_achievement = evaluation["overall_achievement"]
        if avg_achievement < 50:
            evaluation["status"] = "critical"
        elif avg_achievement < 80:
            evaluation["status"] = "needs_attention"
        elif avg_achievement >= 100:
            evaluation["status"] = "exceeding"
        else:
            evaluation["status"] = "on_track"

        # Generate high-level recommendations
        if evaluation["status"] == "critical":
            evaluation["recommendations"].append("Consider pivot or major strategy adjustment")
        elif evaluation["status"] == "needs_attention":
            evaluation["recommendations"].append("Review and adjust underperforming tactics")

        return evaluation

    # ===================================================================
    # TACTICAL RECOMMENDATIONS
    # ===================================================================

    def recommend_next_actions(self, plan: StrategicPlan) -> List[str]:
        """Generate recommended next actions for a strategic plan.

        Args:
            plan: The strategic plan

        Returns:
            List of recommended action strings
        """
        recommendations = []

        # Check for pending tactics that can be started
        pending_tactics = plan.get_pending_tactics()
        if pending_tactics:
            for tactic in pending_tactics[:3]:  # Top 3
                recommendations.append(f"START: {tactic.description}")

        # Check for overdue milestones
        for milestone in plan.milestones:
            if milestone.is_overdue():
                recommendations.append(f"URGENT: Address overdue milestone '{milestone.title}'")

        # Check for pending decisions
        pending_decisions = plan.get_pending_decisions()
        if pending_decisions:
            for decision in pending_decisions[:2]:  # Top 2
                recommendations.append(f"DECIDE: {decision.question}")

        # Check KPI performance
        for kpi in plan.kpis:
            achievement = kpi.calculate_achievement_percentage()
            if achievement < 50:
                recommendations.append(f"REASSESS: {kpi.name} strategy - significantly below target")

        # If no specific recommendations, provide general guidance
        if not recommendations:
            if plan.status == PlanStatus.DRAFT:
                recommendations.append("ACTIVATE: Mark plan as active and begin execution")
            elif plan.status == PlanStatus.ACTIVE:
                recommendations.append("EXECUTE: Start with research tactics to gather market intelligence")
            else:
                recommendations.append("MONITOR: Continue tracking KPIs and adjust as needed")

        return recommendations[:5]  # Limit to top 5

    # ===================================================================
    # KNOWLEDGE BASE INTEGRATION
    # ===================================================================

    def retrieve_knowledge(self, query: str, domain: str = "ecommerce") -> List[Dict[str, Any]]:
        """Retrieve relevant knowledge from the knowledge base.

        Args:
            query: Search query
            domain: Knowledge domain (e.g., 'ecommerce', 'marketing', 'product')

        Returns:
            List of relevant knowledge cards
        """
        knowledge_cards = []

        # Search in knowledge base directory
        knowledge_cards_dir = self.knowledge_base_path / "app_documentation" / "RAW_LCM" / "KNOWLEDGE_CARDS"

        if not knowledge_cards_dir.exists():
            return []

        # Simple search: look for markdown files containing query keywords
        query_terms = query.lower().split()

        for card_file in knowledge_cards_dir.glob("*.md"):
            try:
                content = card_file.read_text(encoding='utf-8')
                content_lower = content.lower()

                # Check if any query term appears in the content
                relevance = sum(1 for term in query_terms if term in content_lower)

                if relevance > 0:
                    knowledge_cards.append({
                        "file": str(card_file),
                        "title": card_file.stem,
                        "relevance_score": min(relevance / len(query_terms), 1.0),
                        "content_preview": content[:300]
                    })
            except Exception:
                continue

        # Sort by relevance and return top results
        knowledge_cards.sort(key=lambda x: x["relevance_score"], reverse=True)
        return knowledge_cards[:5]
