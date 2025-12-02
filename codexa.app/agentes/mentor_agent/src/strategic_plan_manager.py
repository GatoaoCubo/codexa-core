#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "pydantic",
#   "python-dotenv",
#   "click",
#   "rich",
# ]
# ///
"""
Mentor Agent - High-Level Strategic E-Commerce Advisor

This is a strategic orchestration agent that manages e-commerce strategic plans
through a CRUD system. It doesn't execute tasks directly but orchestrates specialized
agents (research, ad generation, brand) to achieve business objectives.

Versioned from: adw_trigger_cron_todone.py
Adapted for: Strategic business planning and tactical orchestration

Usage:
    # Create a new strategic plan
    uv run adws/adw_mentor_agent.py create-plan --objective "Outrank competitor X"

    # List active plans
    uv run adws/adw_mentor_agent.py list-plans

    # Get plan details
    uv run adws/adw_mentor_agent.py read-plan <plan_id>

    # Update a plan
    uv run adws/adw_mentor_agent.py update-plan <plan_id>

    # Archive a plan
    uv run adws/adw_mentor_agent.py archive-plan <plan_id> --reason "Completed"

    # Generate tactical report
    uv run adws/adw_mentor_agent.py tactical-report

Examples:
    # Create strategic plan for product launch
    uv run adws/adw_mentor_agent.py create-plan \\
        --objective "Launch smartwatch product line in Brazil" \\
        --kpi "Sales:500:units/month" \\
        --kpi "Ranking:Top 3:position" \\
        --priority high

    # Generate comprehensive tactical report
    uv run adws/adw_mentor_agent.py tactical-report --output strategic_plans/reports/

    # Dry run mode (no changes made)
    uv run adws/adw_mentor_agent.py create-plan --objective "Test" --dry-run
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime
import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown

# Add the parent directory to the path so we can import modules
parent_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, parent_dir)
sys.path.insert(0, os.path.join(parent_dir, "adw_modules"))

from agent import (
    AgentTemplateRequest,
    execute_template,
    generate_short_id,
)

# Import strategic plan data models
from strategic_plan_models import (
    StrategicPlan,
    Tactic,
    KPI,
    Milestone,
    AgentDelegation,
    CompetitiveInsight,
    KnowledgeInsight,
    DecisionPoint,
    TacticalReport,
    PlanStatus,
    TacticStatus,
    Priority,
)

# Configuration constants
STRATEGIC_PLANS_DIR = Path("strategic_plans")
ACTIVE_PLANS_DIR = STRATEGIC_PLANS_DIR / "active"
ARCHIVED_PLANS_DIR = STRATEGIC_PLANS_DIR / "archived"
TEMPLATES_DIR = STRATEGIC_PLANS_DIR / "templates"
REPORTS_DIR = STRATEGIC_PLANS_DIR / "reports"


class StrategicPlanManager:
    """Manages CRUD operations for strategic plans."""

    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()
        self.ensure_directories()

    def ensure_directories(self):
        """Ensure all required directories exist."""
        for directory in [ACTIVE_PLANS_DIR, ARCHIVED_PLANS_DIR, TEMPLATES_DIR, REPORTS_DIR]:
            directory.mkdir(parents=True, exist_ok=True)

    def sanitize_filename(self, text: str) -> str:
        """Sanitize text for use in filenames."""
        # Remove or replace invalid filename characters
        sanitized = "".join(c if c.isalnum() or c in (' ', '-', '_') else '_' for c in text)
        # Replace spaces with underscores and convert to lowercase
        sanitized = sanitized.replace(' ', '_').lower()
        # Limit length
        return sanitized[:50]

    def get_plan_filename(self, plan: StrategicPlan) -> str:
        """Generate filename for a strategic plan."""
        sanitized_title = self.sanitize_filename(plan.title)
        return f"{plan.id}_{sanitized_title}.md"

    def get_plan_path(self, plan: StrategicPlan, archived: bool = False) -> Path:
        """Get the full path for a plan file."""
        directory = ARCHIVED_PLANS_DIR if archived else ACTIVE_PLANS_DIR
        return directory / self.get_plan_filename(plan)

    def list_plans(self, status: Optional[PlanStatus] = None) -> List[StrategicPlan]:
        """List all strategic plans, optionally filtered by status."""
        plans = []

        # Load active plans
        for plan_file in ACTIVE_PLANS_DIR.glob("*.md"):
            try:
                plan = self.load_plan_from_markdown(plan_file)
                if status is None or plan.status == status:
                    plans.append(plan)
            except Exception as e:
                self.console.print(f"[yellow]Warning: Could not load {plan_file.name}: {e}[/yellow]")

        # Load archived plans
        for plan_file in ARCHIVED_PLANS_DIR.glob("*.md"):
            try:
                plan = self.load_plan_from_markdown(plan_file)
                if status is None or plan.status == status:
                    plans.append(plan)
            except Exception as e:
                self.console.print(f"[yellow]Warning: Could not load {plan_file.name}: {e}[/yellow]")

        # Sort by creation date (newest first)
        plans.sort(key=lambda p: p.created_at, reverse=True)
        return plans

    def load_plan_from_markdown(self, file_path: Path) -> StrategicPlan:
        """Load a strategic plan from a markdown file.

        Note: For v1, we'll store the plan data as JSON in a code block within the markdown.
        This allows human-readable markdown with machine-parseable data.
        """
        content = file_path.read_text(encoding='utf-8')

        # Extract JSON data from code block (enclosed in ```json ... ```)
        import re
        json_match = re.search(r'```json\s*\n(.*?)\n```', content, re.DOTALL)
        if not json_match:
            raise ValueError(f"No JSON data block found in {file_path}")

        json_data = json_match.group(1)
        plan_dict = json.loads(json_data)

        # Reconstruct the plan object
        plan = StrategicPlan(**plan_dict)
        plan.file_path = str(file_path)
        return plan

    def save_plan_to_markdown(self, plan: StrategicPlan, archived: bool = False) -> Path:
        """Save a strategic plan to a markdown file."""
        file_path = self.get_plan_path(plan, archived=archived)
        plan.file_path = str(file_path)
        plan.updated_at = datetime.now()

        # Load template
        template_path = TEMPLATES_DIR / "strategic_plan_template.md"
        if template_path.exists():
            template = template_path.read_text(encoding='utf-8')
        else:
            template = self._get_default_template()

        # Render the markdown with plan data
        rendered_md = self._render_plan_markdown(plan, template)

        # Write to file
        file_path.write_text(rendered_md, encoding='utf-8')

        return file_path

    def _get_default_template(self) -> str:
        """Get a basic default template if file doesn't exist."""
        return """# Strategic Plan: {TITLE}

**Plan ID**: `{PLAN_ID}`
**Status**: {STATUS}
**Created**: {CREATED_AT}

## Objective

{OBJECTIVE}

## KPIs

{KPIS_TABLE}

## Tactics

{TACTICS_LIST}

## Plan Data (Machine-Readable)

```json
{JSON_DATA}
```
"""

    def _render_plan_markdown(self, plan: StrategicPlan, template: str) -> str:
        """Render a plan into markdown using the template."""
        # Build KPIs table
        kpis_table = "| KPI | Target | Current | Unit | Status | Achievement |\n"
        kpis_table += "|-----|--------|---------|------|--------|-------------|\n"
        for kpi in plan.kpis:
            achievement = kpi.calculate_achievement_percentage()
            kpis_table += f"| {kpi.name} | {kpi.target} | {kpi.current} | {kpi.unit} | {kpi.status.value} | {achievement:.1f}% |\n"

        # Build tactics list
        tactics_list = ""
        for idx, tactic in enumerate(plan.tactics, 1):
            tactics_list += f"### {idx}. {tactic.description}\n\n"
            tactics_list += f"**ID**: `{tactic.id}`\n"
            tactics_list += f"**Status**: {tactic.status.value}\n"
            tactics_list += f"**Priority**: {tactic.priority.value}\n\n"
            if tactic.agent_delegation:
                tactics_list += f"**Agent Delegation**: {tactic.agent_delegation.agent_name} (`{tactic.agent_delegation.slash_command}`)\n\n"
            tactics_list += "---\n\n"

        # Build milestones section
        milestones_list = ""
        for milestone in plan.milestones:
            completion = milestone.calculate_completion_percentage()
            milestones_list += f"### {milestone.title}\n\n"
            milestones_list += f"**Status**: {milestone.status.value} | **Completion**: {completion:.0f}%\n\n"
            if milestone.deadline:
                milestones_list += f"**Deadline**: {milestone.deadline}\n\n"
            for deliv in milestone.deliverables:
                check = "x" if deliv.completed else " "
                milestones_list += f"- [{check}] {deliv.description}\n"
            milestones_list += "\n---\n\n"

        # Serialize plan to JSON for machine readability
        json_data = plan.model_dump_json(indent=2)

        # Replace template variables (simple version - can be enhanced)
        rendered = template
        replacements = {
            "{TITLE}": plan.title,
            "{PLAN_ID}": plan.id,
            "{STATUS}": plan.status.value,
            "{PRIORITY}": plan.priority.value,
            "{CREATED_AT}": plan.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "{UPDATED_AT}": plan.updated_at.strftime("%Y-%m-%d %H:%M:%S"),
            "{OBJECTIVE}": plan.objective,
            "{KPIS_TABLE}": kpis_table,
            "{TACTICS_LIST}": tactics_list,
            "{MILESTONES_LIST}": milestones_list if plan.milestones else "*No milestones defined*",
            "{AVG_PERCENTAGE}": f"{plan.get_overall_kpi_achievement():.1f}",
            "{JSON_DATA}": json_data,
        }

        for key, value in replacements.items():
            rendered = rendered.replace(key, value)

        return rendered

    def create_plan(self, title: str, objective: str, kpis: List[KPI],
                   priority: Priority = Priority.MEDIUM) -> StrategicPlan:
        """Create a new strategic plan."""
        plan = StrategicPlan(
            title=title,
            objective=objective,
            kpis=kpis,
            priority=priority,
            status=PlanStatus.DRAFT
        )

        # Save to file
        file_path = self.save_plan_to_markdown(plan)

        return plan

    def read_plan(self, plan_id: str) -> Optional[StrategicPlan]:
        """Read a strategic plan by ID."""
        # Search in active plans
        for plan_file in ACTIVE_PLANS_DIR.glob(f"{plan_id}_*.md"):
            return self.load_plan_from_markdown(plan_file)

        # Search in archived plans
        for plan_file in ARCHIVED_PLANS_DIR.glob(f"{plan_id}_*.md"):
            return self.load_plan_from_markdown(plan_file)

        return None

    def update_plan(self, plan: StrategicPlan) -> Path:
        """Update an existing strategic plan."""
        archived = plan.status == PlanStatus.ARCHIVED
        return self.save_plan_to_markdown(plan, archived=archived)

    def archive_plan(self, plan_id: str, reason: str) -> bool:
        """Archive a strategic plan."""
        plan = self.read_plan(plan_id)
        if not plan:
            return False

        # Mark as archived
        plan.archive(reason)

        # Move from active to archived
        old_path = self.get_plan_path(plan, archived=False)
        if old_path.exists():
            old_path.unlink()

        # Save to archived directory
        self.save_plan_to_markdown(plan, archived=True)

        return True


class MentorAgent:
    """Main Mentor Agent orchestrator."""

    def __init__(self, dry_run: bool = False):
        self.console = Console()
        self.plan_manager = StrategicPlanManager(self.console)
        self.dry_run = dry_run

    def display_plan_summary(self, plan: StrategicPlan):
        """Display a summary of a strategic plan."""
        # Create a rich table for KPIs
        kpi_table = Table(title=f"📊 KPIs - {plan.title}")
        kpi_table.add_column("KPI", style="cyan")
        kpi_table.add_column("Target", justify="right", style="green")
        kpi_table.add_column("Current", justify="right", style="yellow")
        kpi_table.add_column("Achievement", justify="right", style="magenta")

        for kpi in plan.kpis:
            achievement = kpi.calculate_achievement_percentage()
            kpi_table.add_row(
                kpi.name,
                f"{kpi.target} {kpi.unit}",
                f"{kpi.current} {kpi.unit}",
                f"{achievement:.1f}%"
            )

        self.console.print(kpi_table)

        # Display tactics summary
        pending = len(plan.get_tactics_by_status(TacticStatus.PENDING))
        in_progress = len(plan.get_tactics_by_status(TacticStatus.IN_PROGRESS))
        completed = len(plan.get_tactics_by_status(TacticStatus.COMPLETED))

        tactics_panel = Panel(
            f"Pending: {pending} | In Progress: {in_progress} | Completed: {completed}",
            title="📋 Tactics Status",
            border_style="blue"
        )
        self.console.print(tactics_panel)

    def create_plan_interactive(self, objective: str, kpi_specs: List[str],
                               priority: str = "medium") -> StrategicPlan:
        """Create a strategic plan interactively."""
        if self.dry_run:
            self.console.print("[yellow]DRY RUN: Would create strategic plan[/yellow]")
            return None

        # Generate title from objective (first 50 chars)
        title = objective[:50] if len(objective) <= 50 else objective[:47] + "..."

        # Parse KPI specifications (format: "name:target:unit")
        kpis = []
        for kpi_spec in kpi_specs:
            parts = kpi_spec.split(":")
            if len(parts) != 3:
                self.console.print(f"[red]Invalid KPI format: {kpi_spec}. Use 'name:target:unit'[/red]")
                continue

            name, target, unit = parts
            try:
                target_value = float(target) if '.' in target else int(target)
                kpis.append(KPI(name=name, target=target_value, unit=unit))
            except ValueError:
                self.console.print(f"[red]Invalid target value in KPI: {kpi_spec}[/red]")

        if not kpis:
            self.console.print("[red]No valid KPIs provided. At least one KPI is required.[/red]")
            return None

        # Parse priority
        priority_enum = Priority(priority.lower())

        # Create the plan
        plan = self.plan_manager.create_plan(
            title=title,
            objective=objective,
            kpis=kpis,
            priority=priority_enum
        )

        # Display success
        success_panel = Panel(
            f"✅ Strategic plan created successfully!\n\n"
            f"**Plan ID**: `{plan.id}`\n"
            f"**Title**: {plan.title}\n"
            f"**KPIs**: {len(plan.kpis)} defined\n"
            f"**File**: {plan.file_path}",
            title="[bold green]Plan Created[/bold green]",
            border_style="green"
        )
        self.console.print(success_panel)

        return plan


# CLI Commands

@click.group()
@click.option('--dry-run', is_flag=True, help='Run in dry-run mode (no changes)')
@click.pass_context
def cli(ctx, dry_run):
    """Mentor Agent - Strategic E-Commerce Advisor

    High-level orchestration agent for managing e-commerce strategic plans.
    """
    ctx.ensure_object(dict)
    ctx.obj['dry_run'] = dry_run
    ctx.obj['agent'] = MentorAgent(dry_run=dry_run)


@cli.command()
@click.option('--objective', required=True, help='Business objective for the plan')
@click.option('--kpi', 'kpis', multiple=True, required=True, help='KPI in format "name:target:unit"')
@click.option('--priority', default='medium', type=click.Choice(['low', 'medium', 'high', 'critical']), help='Plan priority')
@click.pass_context
def create_plan(ctx, objective, kpis, priority):
    """Create a new strategic plan."""
    agent = ctx.obj['agent']
    plan = agent.create_plan_interactive(objective, list(kpis), priority)

    if plan:
        agent.display_plan_summary(plan)


@cli.command()
@click.option('--status', type=click.Choice(['draft', 'active', 'in_progress', 'on_hold', 'completed', 'archived']), help='Filter by status')
@click.pass_context
def list_plans(ctx, status):
    """List all strategic plans."""
    agent = ctx.obj['agent']
    status_filter = PlanStatus(status) if status else None
    plans = agent.plan_manager.list_plans(status=status_filter)

    if not plans:
        agent.console.print("[yellow]No strategic plans found.[/yellow]")
        return

    # Create a table
    table = Table(title="📋 Strategic Plans")
    table.add_column("ID", style="cyan")
    table.add_column("Title", style="bold")
    table.add_column("Status", style="magenta")
    table.add_column("Priority", style="yellow")
    table.add_column("KPI Achievement", justify="right", style="green")
    table.add_column("Created", style="dim")

    for plan in plans:
        avg_achievement = plan.get_overall_kpi_achievement()
        table.add_row(
            plan.id,
            plan.title[:40],
            plan.status.value,
            plan.priority.value,
            f"{avg_achievement:.1f}%",
            plan.created_at.strftime("%Y-%m-%d")
        )

    agent.console.print(table)


@cli.command()
@click.argument('plan_id')
@click.pass_context
def read_plan(ctx, plan_id):
    """Read and display a strategic plan."""
    agent = ctx.obj['agent']
    plan = agent.plan_manager.read_plan(plan_id)

    if not plan:
        agent.console.print(f"[red]Plan not found: {plan_id}[/red]")
        return

    # Display detailed plan information
    header_panel = Panel(
        f"**Title**: {plan.title}\n"
        f"**ID**: `{plan.id}`\n"
        f"**Status**: {plan.status.value}\n"
        f"**Priority**: {plan.priority.value}\n"
        f"**Created**: {plan.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"**Updated**: {plan.updated_at.strftime('%Y-%m-%d %H:%M:%S')}",
        title="[bold cyan]📋 Strategic Plan[/bold cyan]",
        border_style="cyan"
    )
    agent.console.print(header_panel)

    # Display objective
    obj_panel = Panel(plan.objective, title="[bold]🎯 Objective[/bold]", border_style="blue")
    agent.console.print(obj_panel)

    # Display KPIs and tactics
    agent.display_plan_summary(plan)

    # File path
    agent.console.print(f"\n📄 File: {plan.file_path}")


@cli.command()
@click.argument('plan_id')
@click.option('--reason', required=True, help='Reason for archiving')
@click.pass_context
def archive_plan(ctx, plan_id, reason):
    """Archive a strategic plan."""
    agent = ctx.obj['agent']

    if agent.dry_run:
        agent.console.print(f"[yellow]DRY RUN: Would archive plan {plan_id}[/yellow]")
        return

    success = agent.plan_manager.archive_plan(plan_id, reason)

    if success:
        agent.console.print(f"[green]✅ Plan {plan_id} archived successfully.[/green]")
    else:
        agent.console.print(f"[red]❌ Failed to archive plan {plan_id}. Plan not found.[/red]")


@cli.command()
@click.pass_context
def tactical_report(ctx):
    """Generate a comprehensive tactical report."""
    agent = ctx.obj['agent']
    plans = agent.plan_manager.list_plans()

    # Calculate statistics
    active_count = len([p for p in plans if p.status in [PlanStatus.ACTIVE, PlanStatus.IN_PROGRESS]])
    total_kpis = sum(len(p.kpis) for p in plans)
    avg_achievement = sum(p.get_overall_kpi_achievement() for p in plans) / len(plans) if plans else 0

    # Count tactics by status
    all_pending = sum(len(p.get_tactics_by_status(TacticStatus.PENDING)) for p in plans)
    all_in_progress = sum(len(p.get_tactics_by_status(TacticStatus.IN_PROGRESS)) for p in plans)
    all_completed = sum(len(p.get_tactics_by_status(TacticStatus.COMPLETED)) for p in plans)

    # Display report
    report_panel = Panel(
        f"**Active Plans**: {active_count}\n"
        f"**Total KPIs**: {total_kpis}\n"
        f"**Average KPI Achievement**: {avg_achievement:.1f}%\n\n"
        f"**Tactics Status**:\n"
        f"  • Pending: {all_pending}\n"
        f"  • In Progress: {all_in_progress}\n"
        f"  • Completed: {all_completed}",
        title="[bold cyan]📊 Tactical Report[/bold cyan]",
        border_style="cyan"
    )
    agent.console.print(report_panel)


if __name__ == "__main__":
    cli()
