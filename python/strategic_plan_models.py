"""
Data models for the Mentor Agent strategic planning system.

These models define the structure for strategic plans, tactics, KPIs, and milestones
used throughout the Mentor Agent orchestration system.
"""

from typing import List, Optional, Literal, Dict, Any
from datetime import datetime, date
from enum import Enum
from pydantic import BaseModel, Field, field_validator
import uuid


class PlanStatus(str, Enum):
    """Status of a strategic plan."""

    DRAFT = "draft"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TacticStatus(str, Enum):
    """Status of a tactical action."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DELEGATED = "delegated"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class KPIStatus(str, Enum):
    """Status of a KPI based on target achievement."""

    NOT_STARTED = "not_started"
    BELOW_TARGET = "below_target"
    ON_TRACK = "on_track"
    ACHIEVED = "achieved"
    EXCEEDED = "exceeded"


class MilestoneStatus(str, Enum):
    """Status of a milestone."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    BLOCKED = "blocked"


class Priority(str, Enum):
    """Priority level for plans and tactics."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class KPI(BaseModel):
    """Key Performance Indicator for a strategic plan."""

    name: str = Field(..., description="Name of the KPI (e.g., 'Sales', 'Conversion Rate')")
    target: float = Field(..., description="Target value for the KPI")
    current: float = Field(default=0.0, description="Current value of the KPI")
    unit: str = Field(..., description="Unit of measurement (e.g., 'units', '%', 'BRL')")
    status: KPIStatus = Field(default=KPIStatus.NOT_STARTED, description="Current status")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update time")

    def calculate_achievement_percentage(self) -> float:
        """Calculate achievement percentage (0-100+)."""
        if self.target == 0:
            return 0.0
        return (self.current / self.target) * 100

    def update_status(self) -> None:
        """Update status based on current vs target."""
        if self.current == 0:
            self.status = KPIStatus.NOT_STARTED
        elif self.current < self.target * 0.5:
            self.status = KPIStatus.BELOW_TARGET
        elif self.current < self.target * 0.9:
            self.status = KPIStatus.ON_TRACK
        elif self.current >= self.target:
            if self.current > self.target * 1.2:
                self.status = KPIStatus.EXCEEDED
            else:
                self.status = KPIStatus.ACHIEVED
        self.updated_at = datetime.now()

    def update_current(self, value: float) -> None:
        """Update current value and recalculate status."""
        self.current = value
        self.update_status()


class AgentDelegation(BaseModel):
    """Information about delegation to a specialized agent."""

    agent_name: str = Field(..., description="Name of the delegated agent (e.g., 'pesquisa', 'codex_anuncio')")
    slash_command: str = Field(..., description="Slash command to invoke (e.g., '/pesquisa', '/codex_anuncio')")
    args: List[str] = Field(default_factory=list, description="Arguments for the command")
    adw_id: Optional[str] = Field(None, description="ADW ID assigned for tracking")
    delegated_at: Optional[datetime] = Field(None, description="Time of delegation")
    completed_at: Optional[datetime] = Field(None, description="Time of completion")
    output_path: Optional[str] = Field(None, description="Path to agent output file")
    success: Optional[bool] = Field(None, description="Whether delegation succeeded")
    error_message: Optional[str] = Field(None, description="Error message if failed")

    def mark_delegated(self, adw_id: str) -> None:
        """Mark as delegated with tracking ID."""
        self.adw_id = adw_id
        self.delegated_at = datetime.now()

    def mark_completed(self, success: bool, output_path: Optional[str] = None, error_message: Optional[str] = None) -> None:
        """Mark delegation as completed."""
        self.completed_at = datetime.now()
        self.success = success
        self.output_path = output_path
        self.error_message = error_message


class Tactic(BaseModel):
    """A tactical action within a strategic plan."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8], description="Unique tactic ID")
    description: str = Field(..., description="Description of the tactical action")
    rationale: Optional[str] = Field(None, description="Why this tactic is important")
    agent_delegation: Optional[AgentDelegation] = Field(None, description="Agent delegation details")
    status: TacticStatus = Field(default=TacticStatus.PENDING, description="Current status")
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level")
    dependencies: List[str] = Field(default_factory=list, description="IDs of tactics this depends on")
    results: Optional[Dict[str, Any]] = Field(None, description="Results/outputs from execution")
    created_at: datetime = Field(default_factory=datetime.now, description="Creation time")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update time")

    def can_start(self, completed_tactic_ids: List[str]) -> bool:
        """Check if all dependencies are met."""
        return all(dep_id in completed_tactic_ids for dep_id in self.dependencies)

    def update_status(self, new_status: TacticStatus, results: Optional[Dict[str, Any]] = None) -> None:
        """Update tactic status and results."""
        self.status = new_status
        if results:
            self.results = results
        self.updated_at = datetime.now()


class Deliverable(BaseModel):
    """A deliverable within a milestone."""

    description: str = Field(..., description="Description of the deliverable")
    completed: bool = Field(default=False, description="Whether completed")
    completed_at: Optional[datetime] = Field(None, description="Completion time")

    def mark_completed(self) -> None:
        """Mark deliverable as completed."""
        self.completed = True
        self.completed_at = datetime.now()


class Milestone(BaseModel):
    """A milestone within a strategic plan."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8], description="Unique milestone ID")
    title: str = Field(..., description="Title of the milestone")
    description: Optional[str] = Field(None, description="Detailed description")
    deadline: Optional[date] = Field(None, description="Target deadline")
    status: MilestoneStatus = Field(default=MilestoneStatus.PENDING, description="Current status")
    deliverables: List[Deliverable] = Field(default_factory=list, description="List of deliverables")
    completed_at: Optional[datetime] = Field(None, description="Completion time")

    def calculate_completion_percentage(self) -> float:
        """Calculate percentage of deliverables completed."""
        if not self.deliverables:
            return 0.0
        completed_count = sum(1 for d in self.deliverables if d.completed)
        return (completed_count / len(self.deliverables)) * 100

    def is_overdue(self) -> bool:
        """Check if milestone is overdue."""
        if not self.deadline:
            return False
        return date.today() > self.deadline and self.status != MilestoneStatus.COMPLETED

    def update_status(self) -> None:
        """Update status based on deliverables and deadline."""
        completion_pct = self.calculate_completion_percentage()

        if completion_pct == 100:
            self.status = MilestoneStatus.COMPLETED
            if not self.completed_at:
                self.completed_at = datetime.now()
        elif self.is_overdue():
            self.status = MilestoneStatus.DELAYED
        elif completion_pct > 0:
            self.status = MilestoneStatus.IN_PROGRESS
        else:
            self.status = MilestoneStatus.PENDING


class CompetitiveInsight(BaseModel):
    """Competitive intelligence insight."""

    competitor_name: str = Field(..., description="Name of competitor")
    insight: str = Field(..., description="The competitive insight")
    source: Optional[str] = Field(None, description="Source of the insight (e.g., research agent output)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")
    identified_at: datetime = Field(default_factory=datetime.now, description="When insight was identified")

    def is_high_confidence(self) -> bool:
        """Check if this is a high-confidence insight."""
        return self.confidence >= 0.7


class KnowledgeInsight(BaseModel):
    """Insight from the knowledge base."""

    title: str = Field(..., description="Title of the insight")
    content: str = Field(..., description="Content/description of the insight")
    source_file: Optional[str] = Field(None, description="Source knowledge base file")
    tags: List[str] = Field(default_factory=list, description="Relevant tags")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance to current plan (0-1)")

    def is_highly_relevant(self) -> bool:
        """Check if this insight is highly relevant."""
        return self.relevance_score >= 0.7


class DecisionPoint(BaseModel):
    """A decision point requiring user input."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8], description="Unique decision ID")
    question: str = Field(..., description="The decision question")
    context: str = Field(..., description="Context for the decision")
    options: List[str] = Field(..., description="Available options")
    recommendation: Optional[str] = Field(None, description="Mentor's recommended option")
    rationale: Optional[str] = Field(None, description="Rationale for recommendation")
    user_decision: Optional[str] = Field(None, description="User's chosen option")
    decided_at: Optional[datetime] = Field(None, description="Time of decision")
    created_at: datetime = Field(default_factory=datetime.now, description="When question was posed")

    def record_decision(self, decision: str) -> None:
        """Record user's decision."""
        self.user_decision = decision
        self.decided_at = datetime.now()


class StrategicPlan(BaseModel):
    """A strategic e-commerce plan managed by the Mentor Agent."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8], description="Unique plan ID")
    title: str = Field(..., description="Title of the strategic plan")
    objective: str = Field(..., description="Clear business objective")
    status: PlanStatus = Field(default=PlanStatus.DRAFT, description="Current status")
    priority: Priority = Field(default=Priority.MEDIUM, description="Priority level")

    # Core plan elements
    kpis: List[KPI] = Field(default_factory=list, description="Target KPIs")
    tactics: List[Tactic] = Field(default_factory=list, description="Tactical actions")
    milestones: List[Milestone] = Field(default_factory=list, description="Milestones")

    # Intelligence and insights
    competitive_insights: List[CompetitiveInsight] = Field(default_factory=list, description="Competitive intelligence")
    knowledge_insights: List[KnowledgeInsight] = Field(default_factory=list, description="Knowledge base insights")

    # Decision tracking
    decision_points: List[DecisionPoint] = Field(default_factory=list, description="Decision history")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.now, description="Creation time")
    updated_at: datetime = Field(default_factory=datetime.now, description="Last update time")
    archived_at: Optional[datetime] = Field(None, description="Archival time")
    archive_reason: Optional[str] = Field(None, description="Reason for archival")

    # File references
    file_path: Optional[str] = Field(None, description="Path to the plan markdown file")
    report_paths: List[str] = Field(default_factory=list, description="Paths to generated reports")

    @field_validator("kpis")
    @classmethod
    def validate_kpis(cls, v):
        """Ensure at least one KPI is defined."""
        if not v:
            raise ValueError("Strategic plan must have at least one KPI")
        return v

    def get_overall_kpi_achievement(self) -> float:
        """Calculate average KPI achievement percentage."""
        if not self.kpis:
            return 0.0
        total = sum(kpi.calculate_achievement_percentage() for kpi in self.kpis)
        return total / len(self.kpis)

    def get_tactics_by_status(self, status: TacticStatus) -> List[Tactic]:
        """Get all tactics with a specific status."""
        return [t for t in self.tactics if t.status == status]

    def get_pending_tactics(self) -> List[Tactic]:
        """Get tactics ready to start (pending with no dependencies or dependencies met)."""
        completed_ids = [t.id for t in self.tactics if t.status == TacticStatus.COMPLETED]
        return [
            t for t in self.tactics
            if t.status == TacticStatus.PENDING and t.can_start(completed_ids)
        ]

    def get_high_confidence_competitive_insights(self) -> List[CompetitiveInsight]:
        """Get high-confidence competitive insights."""
        return [ci for ci in self.competitive_insights if ci.is_high_confidence()]

    def get_highly_relevant_knowledge_insights(self) -> List[KnowledgeInsight]:
        """Get highly relevant knowledge insights."""
        return [ki for ki in self.knowledge_insights if ki.is_highly_relevant()]

    def get_pending_decisions(self) -> List[DecisionPoint]:
        """Get decision points awaiting user input."""
        return [dp for dp in self.decision_points if dp.user_decision is None]

    def mark_active(self) -> None:
        """Mark plan as active."""
        self.status = PlanStatus.ACTIVE
        self.updated_at = datetime.now()

    def mark_in_progress(self) -> None:
        """Mark plan as in progress."""
        self.status = PlanStatus.IN_PROGRESS
        self.updated_at = datetime.now()

    def mark_completed(self) -> None:
        """Mark plan as completed."""
        self.status = PlanStatus.COMPLETED
        self.updated_at = datetime.now()

    def archive(self, reason: str) -> None:
        """Archive the plan."""
        self.status = PlanStatus.ARCHIVED
        self.archived_at = datetime.now()
        self.archive_reason = reason
        self.updated_at = datetime.now()

    def add_decision_point(self, question: str, context: str, options: List[str],
                          recommendation: Optional[str] = None, rationale: Optional[str] = None) -> DecisionPoint:
        """Add a new decision point."""
        decision = DecisionPoint(
            question=question,
            context=context,
            options=options,
            recommendation=recommendation,
            rationale=rationale
        )
        self.decision_points.append(decision)
        self.updated_at = datetime.now()
        return decision

    def update_kpi_values(self, kpi_updates: Dict[str, float]) -> None:
        """Update multiple KPI values at once."""
        for kpi in self.kpis:
            if kpi.name in kpi_updates:
                kpi.update_current(kpi_updates[kpi.name])
        self.updated_at = datetime.now()

    def add_competitive_insight(self, competitor_name: str, insight: str,
                               confidence: float, source: Optional[str] = None) -> None:
        """Add a competitive insight."""
        ci = CompetitiveInsight(
            competitor_name=competitor_name,
            insight=insight,
            confidence=confidence,
            source=source
        )
        self.competitive_insights.append(ci)
        self.updated_at = datetime.now()

    def add_knowledge_insight(self, title: str, content: str, relevance_score: float,
                             source_file: Optional[str] = None, tags: Optional[List[str]] = None) -> None:
        """Add a knowledge insight."""
        ki = KnowledgeInsight(
            title=title,
            content=content,
            relevance_score=relevance_score,
            source_file=source_file,
            tags=tags or []
        )
        self.knowledge_insights.append(ki)
        self.updated_at = datetime.now()


class TacticalReport(BaseModel):
    """A comprehensive tactical report across all plans."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8], description="Unique report ID")
    title: str = Field(..., description="Report title")
    generated_at: datetime = Field(default_factory=datetime.now, description="Generation time")

    # Plans summary
    active_plans_count: int = Field(..., description="Number of active plans")
    total_kpis: int = Field(..., description="Total number of KPIs across plans")
    avg_kpi_achievement: float = Field(..., description="Average KPI achievement percentage")

    # Tactical status
    pending_tactics_count: int = Field(..., description="Number of pending tactics")
    in_progress_tactics_count: int = Field(..., description="Number of in-progress tactics")
    completed_tactics_count: int = Field(..., description="Number of completed tactics")

    # Insights
    top_competitive_insights: List[CompetitiveInsight] = Field(default_factory=list, description="Top competitive insights")
    key_opportunities: List[str] = Field(default_factory=list, description="Key opportunities identified")

    # Recommendations
    recommended_actions: List[str] = Field(default_factory=list, description="Recommended next actions")

    # References
    plan_summaries: List[Dict[str, Any]] = Field(default_factory=list, description="Summary of each plan")
    file_path: Optional[str] = Field(None, description="Path to report markdown file")
