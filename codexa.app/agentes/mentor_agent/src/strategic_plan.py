"""
CODEXA Strategy Mentor Module

High-level strategic e-commerce planning and orchestration system.

Manages strategic business plans with KPIs, tactics, milestones, and agent delegations.
Consolidated from adw_mentor_agent.py with enhanced CRUD integration.

Core Capabilities:
- Strategic plan creation and management
- KPI tracking and achievement monitoring
- Tactical action planning and delegation
- Milestone tracking and progress monitoring
- Competitive and knowledge insights integration
"""

from typing import Optional, List, Dict, Any, Tuple
from pathlib import Path
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field
import json

from ..utils.logger import get_logger
from ..crud_ops import get_crud_ops, CRUDOperations

logger = get_logger()


# ==================== ENUMERATIONS ====================


class PlanStatus(str, Enum):
    """Strategic plan status."""

    DRAFT = "draft"
    ACTIVE = "active"
    IN_PROGRESS = "in_progress"
    ON_HOLD = "on_hold"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class TacticStatus(str, Enum):
    """Tactical action status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DELEGATED = "delegated"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class KPIStatus(str, Enum):
    """KPI achievement status."""

    NOT_STARTED = "not_started"
    BELOW_TARGET = "below_target"
    ON_TRACK = "on_track"
    ACHIEVED = "achieved"
    EXCEEDED = "exceeded"


class MilestoneStatus(str, Enum):
    """Milestone status."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    BLOCKED = "blocked"


class Priority(str, Enum):
    """Priority level."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


# ==================== DATA MODELS ====================


class KPI(BaseModel):
    """Key Performance Indicator."""

    name: str = Field(..., description="KPI name (e.g., 'Sales', 'Conversion Rate')")
    target: float = Field(..., description="Target value")
    current: float = Field(default=0.0, description="Current value")
    unit: str = Field(..., description="Unit of measurement")
    status: KPIStatus = Field(default=KPIStatus.NOT_STARTED)
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def calculate_achievement_percentage(self) -> float:
        """Calculate achievement percentage (0-100+)."""
        if self.target == 0:
            return 0.0
        return (self.current / self.target) * 100

    def update_status(self):
        """Update status based on current vs target."""
        if self.current == 0:
            self.status = KPIStatus.NOT_STARTED
        elif self.current < self.target * 0.5:
            self.status = KPIStatus.BELOW_TARGET
        elif self.current < self.target * 0.9:
            self.status = KPIStatus.ON_TRACK
        elif self.current >= self.target:
            self.status = (
                KPIStatus.EXCEEDED
                if self.current > self.target * 1.2
                else KPIStatus.ACHIEVED
            )
        self.updated_at = datetime.now().isoformat()

    def update_current(self, value: float):
        """Update current value and recalculate status."""
        self.current = value
        self.update_status()


class AgentDelegation(BaseModel):
    """Agent delegation information."""

    agent_name: str = Field(..., description="Delegated agent name")
    task_description: str = Field(..., description="Task description")
    args: List[str] = Field(default_factory=list, description="Task arguments")
    delegated_at: Optional[str] = Field(None, description="Delegation timestamp")
    completed_at: Optional[str] = Field(None, description="Completion timestamp")
    success: Optional[bool] = Field(None, description="Success status")
    output: Optional[Dict[str, Any]] = Field(None, description="Agent output")
    error_message: Optional[str] = Field(None, description="Error if failed")


class Tactic(BaseModel):
    """Tactical action within a strategic plan."""

    id: str = Field(..., description="Unique tactic ID")
    description: str = Field(..., description="Tactic description")
    rationale: Optional[str] = Field(None, description="Why this tactic is important")
    status: TacticStatus = Field(default=TacticStatus.PENDING)
    priority: Priority = Field(default=Priority.MEDIUM)
    agent_delegation: Optional[AgentDelegation] = Field(
        None, description="Agent delegation details"
    )
    dependencies: List[str] = Field(
        default_factory=list, description="Dependent tactic IDs"
    )
    results: Optional[Dict[str, Any]] = Field(None, description="Execution results")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def can_start(self, completed_tactic_ids: List[str]) -> bool:
        """Check if all dependencies are met."""
        return all(dep_id in completed_tactic_ids for dep_id in self.dependencies)


class Milestone(BaseModel):
    """Project milestone."""

    title: str = Field(..., description="Milestone title")
    description: Optional[str] = Field(None, description="Milestone description")
    status: MilestoneStatus = Field(default=MilestoneStatus.PENDING)
    deadline: Optional[str] = Field(None, description="Deadline date")
    deliverables: List[str] = Field(
        default_factory=list, description="Milestone deliverables"
    )
    completion_percentage: float = Field(default=0.0, description="Completion %")
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class StrategicPlan(BaseModel):
    """Strategic business plan."""

    id: str = Field(..., description="Unique plan ID")
    title: str = Field(..., description="Plan title")
    objective: str = Field(..., description="Business objective")

    # Planning elements
    kpis: List[KPI] = Field(default_factory=list, description="Key performance indicators")
    tactics: List[Tactic] = Field(default_factory=list, description="Tactical actions")
    milestones: List[Milestone] = Field(default_factory=list, description="Project milestones")

    # Status and priority
    status: PlanStatus = Field(default=PlanStatus.DRAFT)
    priority: Priority = Field(default=Priority.MEDIUM)

    # Intelligence integration
    competitive_insights: List[str] = Field(
        default_factory=list, description="Competitive insights"
    )
    knowledge_insights: List[str] = Field(
        default_factory=list, description="Knowledge base insights"
    )

    # Metadata
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    archive_reason: Optional[str] = Field(None, description="Archive reason")

    def get_overall_kpi_achievement(self) -> float:
        """Calculate overall KPI achievement percentage."""
        if not self.kpis:
            return 0.0
        achievements = [kpi.calculate_achievement_percentage() for kpi in self.kpis]
        return sum(achievements) / len(achievements)

    def get_tactics_by_status(self, status: TacticStatus) -> List[Tactic]:
        """Get tactics filtered by status."""
        return [t for t in self.tactics if t.status == status]

    def get_completed_tactic_ids(self) -> List[str]:
        """Get IDs of completed tactics."""
        return [t.id for t in self.tactics if t.status == TacticStatus.COMPLETED]

    def get_next_actionable_tactics(self) -> List[Tactic]:
        """Get tactics that can be started now (dependencies met)."""
        completed_ids = self.get_completed_tactic_ids()
        pending_tactics = self.get_tactics_by_status(TacticStatus.PENDING)
        return [t for t in pending_tactics if t.can_start(completed_ids)]


# ==================== STRATEGY MENTOR ====================


class StrategyMentor:
    """
    Strategic planning and orchestration system.

    Capabilities:
    - Create and manage strategic plans
    - Track KPIs and milestones
    - Coordinate tactical actions
    - Generate strategic insights
    """

    def __init__(
        self,
        data_dir: Path = Path("./strategic_plans"),
        auto_backup: bool = True,
        auto_git: bool = True,
        dry_run: bool = False,
    ):
        """
        Initialize Strategy Mentor.

        Args:
            data_dir: Directory for strategic plans
            auto_backup: Enable automatic backups
            auto_git: Enable automatic git commits
            dry_run: Preview mode
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self.crud = get_crud_ops(
            auto_backup=auto_backup, auto_git=auto_git, dry_run=dry_run
        )
        self.dry_run = dry_run

        logger.module_loaded(
            "StrategyMentor",
            capabilities=[
                "strategic_planning",
                "kpi_tracking",
                "tactical_orchestration",
                "milestone_management",
            ],
        )

    # ==================== PLAN MANAGEMENT ====================

    def create_plan(self, plan: StrategicPlan) -> Tuple[bool, str]:
        """
        Create a new strategic plan.

        Args:
            plan: StrategicPlan object

        Returns:
            Tuple of (success, plan_id_or_error)
        """
        logger.operation_start("create_plan", title=plan.title)

        try:
            # Generate plan document
            plan_md = self._generate_plan_markdown(plan)

            # Save as markdown document with metadata
            success, message = self.crud.create_document(
                path=self.data_dir / f"{plan.id}_{plan.title[:30]}.md",
                content=plan_md,
                doc_type="markdown",
                metadata={
                    "plan_id": plan.id,
                    "status": plan.status.value,
                    "priority": plan.priority.value,
                    "created_at": plan.created_at,
                },
            )

            if success:
                # Also save as JSON for easy programmatic access
                self.crud.create_data_record(
                    collection="strategic_plans",
                    record=plan.model_dump(),
                    record_id=plan.id,
                    data_dir=self.data_dir,
                )
                logger.operation_success("create_plan", id=plan.id)
                return True, plan.id
            else:
                logger.operation_failure("create_plan", message, title=plan.title)
                return False, message

        except Exception as e:
            logger.operation_failure("create_plan", str(e), title=plan.title)
            return False, str(e)

    def get_plan(self, plan_id: str) -> Tuple[bool, Union[StrategicPlan, str]]:
        """
        Retrieve a strategic plan.

        Args:
            plan_id: Plan ID

        Returns:
            Tuple of (success, plan_or_error)
        """
        logger.operation_start("get_plan", id=plan_id)

        try:
            success, result = self.crud.read_data_record(
                collection="strategic_plans",
                record_id=plan_id,
                data_dir=self.data_dir,
            )

            if success:
                plan = StrategicPlan(**result)
                logger.operation_success("get_plan", id=plan_id)
                return True, plan
            else:
                logger.operation_failure("get_plan", result, id=plan_id)
                return False, result

        except Exception as e:
            logger.operation_failure("get_plan", str(e), id=plan_id)
            return False, str(e)

    def update_plan(
        self, plan_id: str, updates: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Update a strategic plan.

        Args:
            plan_id: Plan ID
            updates: Dictionary of updates

        Returns:
            Tuple of (success, message)
        """
        logger.operation_start("update_plan", id=plan_id)

        try:
            # Get current plan
            success, plan = self.get_plan(plan_id)
            if not success:
                return False, plan

            # Apply updates
            updates["updated_at"] = datetime.now().isoformat()

            success, result = self.crud.update_data_record(
                collection="strategic_plans",
                record_id=plan_id,
                updates=updates,
                data_dir=self.data_dir,
            )

            if success:
                # Regenerate markdown
                updated_success, updated_plan = self.get_plan(plan_id)
                if updated_success:
                    plan_md = self._generate_plan_markdown(updated_plan)
                    self.crud.update_document(
                        path=self.data_dir / f"{plan_id}_{plan.title[:30]}.md",
                        content=plan_md,
                    )

                logger.operation_success("update_plan", id=plan_id)
            else:
                logger.operation_failure("update_plan", result, id=plan_id)

            return success, result

        except Exception as e:
            logger.operation_failure("update_plan", str(e), id=plan_id)
            return False, str(e)

    def list_plans(
        self, status: Optional[PlanStatus] = None
    ) -> Tuple[bool, Union[List[StrategicPlan], str]]:
        """
        List all strategic plans.

        Args:
            status: Filter by status

        Returns:
            Tuple of (success, plans_or_error)
        """
        logger.operation_start("list_plans", status=status)

        try:
            success, result = self.crud.list_data_records(
                collection="strategic_plans", data_dir=self.data_dir
            )

            if not success:
                return False, result

            plans = [StrategicPlan(**record) for record in result]

            if status:
                plans = [p for p in plans if p.status == status]

            # Sort by priority and creation date
            priority_order = {
                Priority.CRITICAL: 0,
                Priority.HIGH: 1,
                Priority.MEDIUM: 2,
                Priority.LOW: 3,
            }
            plans.sort(key=lambda p: (priority_order.get(p.priority, 99), p.created_at))

            logger.operation_success("list_plans", count=len(plans))
            return True, plans

        except Exception as e:
            logger.operation_failure("list_plans", str(e))
            return False, str(e)

    # ==================== KPI MANAGEMENT ====================

    def update_kpi(
        self, plan_id: str, kpi_name: str, new_value: float
    ) -> Tuple[bool, str]:
        """
        Update KPI value in a plan.

        Args:
            plan_id: Plan ID
            kpi_name: KPI name
            new_value: New current value

        Returns:
            Tuple of (success, message)
        """
        logger.operation_start("update_kpi", plan=plan_id, kpi=kpi_name)

        try:
            success, plan = self.get_plan(plan_id)
            if not success:
                return False, plan

            # Find and update KPI
            kpi_found = False
            for kpi in plan.kpis:
                if kpi.name == kpi_name:
                    kpi.update_current(new_value)
                    kpi_found = True
                    break

            if not kpi_found:
                msg = f"KPI '{kpi_name}' not found in plan {plan_id}"
                logger.warning(msg)
                return False, msg

            # Update plan
            success, result = self.update_plan(
                plan_id, {"kpis": [kpi.model_dump() for kpi in plan.kpis]}
            )

            if success:
                logger.operation_success(
                    "update_kpi", plan=plan_id, kpi=kpi_name, value=new_value
                )

            return success, result

        except Exception as e:
            logger.operation_failure("update_kpi", str(e), plan=plan_id, kpi=kpi_name)
            return False, str(e)

    # ==================== HELPER METHODS ====================

    def _generate_plan_markdown(self, plan: StrategicPlan) -> str:
        """Generate markdown representation of a strategic plan."""
        lines = [
            f"# Strategic Plan: {plan.title}",
            "",
            f"**Plan ID**: `{plan.id}`",
            f"**Status**: {plan.status.value}",
            f"**Priority**: {plan.priority.value}",
            f"**Created**: {plan.created_at}",
            "",
            "## Objective",
            "",
            plan.objective,
            "",
            "## Key Performance Indicators",
            "",
            "| KPI | Target | Current | Achievement | Status |",
            "|-----|--------|---------|-------------|--------|",
        ]

        for kpi in plan.kpis:
            achievement = kpi.calculate_achievement_percentage()
            lines.append(
                f"| {kpi.name} | {kpi.target} {kpi.unit} | {kpi.current} {kpi.unit} | {achievement:.1f}% | {kpi.status.value} |"
            )

        lines.extend(["", "## Tactics", ""])

        for idx, tactic in enumerate(plan.tactics, 1):
            lines.extend(
                [
                    f"### {idx}. {tactic.description}",
                    "",
                    f"- **Status**: {tactic.status.value}",
                    f"- **Priority**: {tactic.priority.value}",
                ]
            )

            if tactic.rationale:
                lines.append(f"- **Rationale**: {tactic.rationale}")

            if tactic.agent_delegation:
                lines.append(
                    f"- **Delegated to**: {tactic.agent_delegation.agent_name}"
                )

            lines.append("")

        if plan.milestones:
            lines.extend(["## Milestones", ""])
            for milestone in plan.milestones:
                lines.extend(
                    [
                        f"### {milestone.title}",
                        "",
                        f"- **Status**: {milestone.status.value}",
                        f"- **Completion**: {milestone.completion_percentage:.0f}%",
                        "",
                    ]
                )

        # Add JSON data block for machine readability
        lines.extend(
            [
                "---",
                "",
                "## Plan Data (Machine-Readable)",
                "",
                "```json",
                json.dumps(plan.model_dump(), indent=2),
                "```",
            ]
        )

        return "\n".join(lines)

    def get_capabilities(self) -> List[str]:
        """Get list of available capabilities."""
        return [
            "create_plan",
            "get_plan",
            "update_plan",
            "list_plans",
            "update_kpi",
        ]


# Global Strategy Mentor instance
_global_strategy_mentor: Optional[StrategyMentor] = None


def get_strategy_mentor(
    data_dir: Path = Path("./strategic_plans"),
    auto_backup: bool = True,
    auto_git: bool = True,
    dry_run: bool = False,
) -> StrategyMentor:
    """
    Get or create the global Strategy Mentor instance.

    Args:
        data_dir: Directory for strategic plans
        auto_backup: Enable automatic backups
        auto_git: Enable automatic git commits
        dry_run: Preview mode

    Returns:
        StrategyMentor instance
    """
    global _global_strategy_mentor

    if _global_strategy_mentor is None:
        _global_strategy_mentor = StrategyMentor(
            data_dir=data_dir,
            auto_backup=auto_backup,
            auto_git=auto_git,
            dry_run=dry_run,
        )

    return _global_strategy_mentor
