# Mentor Agent - Strategic E-Commerce Advisor

Launch the Mentor Agent interface - a high-level strategic orchestrator for e-commerce business planning and tactical execution.

## Overview

The Mentor Agent is a CRUD-based strategic planning system that:
- Creates comprehensive e-commerce strategic plans from business objectives
- Orchestrates specialized agents (research, ad generation, tracking) to execute tactics
- Provides tactical insights and competitive intelligence
- Reports to the user for critical decision-making
- Maintains strategic plan lifecycle (Draft → Active → In Progress → Completed → Archived)

**Philosophy**: The Mentor Agent **never executes tasks directly**. It is a high-level advisor that delegates to specialized agents and consolidates results for strategic decision-making.

## Interactive Menu

This command launches an interactive menu with the following options:

1. **Create Strategic Plan** - Generate a new plan from a business objective
2. **List Active Plans** - View all active strategic plans
3. **Read Plan Details** - Inspect a specific plan
4. **Update Plan** - Refine a plan based on new results
5. **Archive Plan** - Move completed/obsolete plans to archive
6. **Generate Tactical Report** - Comprehensive report across all plans
7. **Help** - View Mentor Agent documentation

## Quick Actions

### Create a Plan
```bash
/mentor_create_plan "Outrank competitor X on MercadoLivre for smartwatches"
```

### View Plans
```bash
/mentor_read_plan <plan_id>
```

### Generate Report
```bash
/mentor_tactical_report
```

## Integration Points

The Mentor Agent integrates with:
- **Research Agent** (`/pesquisa`) - Market research and competitive intelligence
- **Codex Anuncio** (`/codex_anuncio`) - Ad copy and listing generation
- **Orchestrator** (`/orchestrator`) - Consumption/creation tracking
- **Knowledge Base** (`knowledge_base/`) - Best practices and insights

## Instructions

1. Display welcome message with Mentor Agent logo and description
2. Show interactive menu with numbered options (1-7)
3. Prompt user for selection
4. Execute the corresponding command based on user choice:
   - Option 1: Prompt for objective and KPIs, then call `/mentor_create_plan`
   - Option 2: Call `uv run adws/adw_mentor_agent.py list-plans`
   - Option 3: Prompt for plan ID, then call `/mentor_read_plan <id>`
   - Option 4: Prompt for plan ID, then call `/mentor_update_plan <id>`
   - Option 5: Prompt for plan ID and reason, then call `/mentor_archive_plan <id> --reason <reason>`
   - Option 6: Call `/mentor_tactical_report`
   - Option 7: Display help documentation

## Step by Step Tasks

### Step 1: Display Welcome Screen
Show a welcome panel with:
```
╔══════════════════════════════════════════════════════════════╗
║                    🎯 MENTOR AGENT 🎯                        ║
║          Strategic E-Commerce Tactical Advisor               ║
╚══════════════════════════════════════════════════════════════╝

Your high-level orchestrator for winning e-commerce strategies.

The Mentor Agent helps you:
✓ Create data-driven strategic plans
✓ Orchestrate specialized agents
✓ Track KPIs and milestones
✓ Make informed tactical decisions
✓ Outmaneuver competitors
```

### Step 2: Show Interactive Menu
Display numbered menu:
```
┌─────────────────────────────────────────────────────────────┐
│ MAIN MENU                                                   │
├─────────────────────────────────────────────────────────────┤
│ 1. 📝 Create Strategic Plan                                 │
│ 2. 📋 List Active Plans                                     │
│ 3. 🔍 Read Plan Details                                     │
│ 4. ✏️  Update Plan                                          │
│ 5. 📦 Archive Plan                                          │
│ 6. 📊 Generate Tactical Report                              │
│ 7. ❓ Help & Documentation                                  │
│ 0. 🚪 Exit                                                   │
└─────────────────────────────────────────────────────────────┘

Select an option (0-7):
```

### Step 3: Handle User Selection

#### Option 1: Create Strategic Plan
1. Prompt user: "What is your business objective?"
2. Prompt user: "Enter KPIs (format: name:target:unit, comma-separated)"
   - Example: "Sales:500:units, Ranking:Top 3:position, Revenue:50000:BRL"
3. Prompt user: "Priority level (low/medium/high/critical)?" [Default: medium]
4. Call `/mentor_create_plan` with provided parameters
5. Display created plan summary
6. Ask: "Would you like to activate this plan now?" (y/n)
7. If yes, mark plan as active and display next steps

#### Option 2: List Active Plans
1. Execute: `uv run adws/adw_mentor_agent.py list-plans --status active`
2. Display results in formatted table
3. Show summary: "Total active plans: X | Average KPI achievement: Y%"
4. Prompt: "Enter plan ID to view details, or press Enter to return to menu"

#### Option 3: Read Plan Details
1. Execute: `uv run adws/adw_mentor_agent.py list-plans`
2. Display available plans with IDs
3. Prompt user: "Enter plan ID to inspect:"
4. Call `/mentor_read_plan <plan_id>`
5. Display comprehensive plan details
6. Offer actions: "Update (u) | Archive (a) | Back to menu (m)"

#### Option 4: Update Plan
1. List available plans
2. Prompt for plan ID
3. Call `/mentor_update_plan <plan_id>`
4. This will:
   - Load current plan
   - Show pending tactics
   - Show KPI status
   - Prompt for updates (new tactics, KPI values, decisions)
   - Save updated plan

#### Option 5: Archive Plan
1. List active/completed plans
2. Prompt for plan ID
3. Prompt for archive reason (completed/obsolete/superseded/deprioritized)
4. Confirm: "Archive plan <id>? This will move it to archived/ (y/n)"
5. Execute: `uv run adws/adw_mentor_agent.py archive-plan <plan_id> --reason "<reason>"`
6. Display success message

#### Option 6: Generate Tactical Report
1. Execute: `/mentor_tactical_report`
2. This generates a comprehensive report including:
   - Active plans status
   - KPI performance across all plans
   - Tactical actions status (pending/in-progress/completed)
   - Competitive intelligence insights
   - Market opportunities identified
   - Recommended next actions (prioritized)
3. Save report to `strategic_plans/reports/tactical_report_<timestamp>.md`
4. Display executive summary
5. Prompt: "View full report? (y/n)"

#### Option 7: Help & Documentation
1. Display help text explaining:
   - Mentor Agent architecture
   - Strategic plan components (Objective, KPIs, Tactics, Milestones)
   - Agent delegation model
   - Decision points and user interaction
   - Best practices for strategic planning
2. Show links to documentation files:
   - `strategic_plans/README.md`
   - `strategic_plans/templates/strategic_plan_template.md`
3. Show example commands and workflows

### Step 4: Loop or Exit
- After each operation, ask: "Return to main menu? (y/n)"
- If yes, show menu again (Step 2)
- If no, display exit message and terminate

## Exit Message

```
╔══════════════════════════════════════════════════════════════╗
║           Thank you for using Mentor Agent! 🎯               ║
╚══════════════════════════════════════════════════════════════╝

Your strategic plans are saved in: strategic_plans/active/

To resume, run: /mentor

To create a plan directly: /mentor_create_plan "<objective>"
To view reports: ls strategic_plans/reports/

Keep winning in e-commerce! 🚀
```

## Error Handling

- If plan ID not found: Display error with list of available IDs
- If invalid KPI format: Show example and prompt again
- If agent delegation fails: Display error and suggest manual execution
- If file not found: Check directory structure and suggest running setup

## Notes

- The Mentor Agent is **non-executing** - it orchestrates but doesn't implement directly
- All tactical actions are delegated to specialized agents
- User is prompted for critical decisions (never assumed)
- Plans persist as both markdown (human-readable) and JSON (machine-parseable)
- The system supports multiple concurrent plans with independent tracking

---

**Versioned from**: `adw_trigger_cron_todone.py`
**Adapted for**: High-level strategic orchestration
