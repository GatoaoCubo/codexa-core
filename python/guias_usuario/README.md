# CODEXA - HOP Meta-Agent

**Version:** 1.0.0
**Last Updated:** 2025-11-11 19:37:13
**Modules:** 6

---

## 🎯 For the Agent: Quick Capability Reference

CODEXA (Create Organize Read Update Delete E-com X-Agent) is a HOP (Hierarchical Orchestration Pattern) meta-agent that consolidates:
- **CRUD operations** for documentation and e-commerce data
- **Scout capabilities** for intelligent repository navigation
- **Strategic planning** (mentor pattern) for business KPIs
- **Self-documentation** through introspection and auto-update

**Read this README to understand your available capabilities before executing operations.**

---

## ⚡ Quick Reference

### CODEXA Commands

| Need to... | Command |
|------------|---------|
| View system status | `python cli.py status` |
| Create document | `python cli.py crud create <path> --content "..."` |
| Read document | `python cli.py crud read <path>` |
| List documents | `python cli.py crud list --type document` |
| Search documents | `python cli.py crud search --keyword "..."` |
| Scan repository | `python cli.py scout scan --cache` |
| Find files | `python cli.py scout find --pattern "*.py"` |
| Repository stats | `python cli.py scout stats` |
| Create product | `python cli.py ecom products create --name "..." --price 99` |
| List products | `python cli.py ecom products list` |
| Create strategic plan | `python cli.py ecom strategy create-plan --title "..."` |
| Update KPI | `python cli.py ecom strategy update-kpi <id> "Metric" 100` |
| Add competitor | `python cli.py ecom competitor add --name "..." --price 99` |
| Search knowledge | `python cli.py ecom knowledge search --keyword "..."` |
| Update README | `python cli.py readme update` |

### TAC-7 ADW Agents (../adws/)

**When to use**: For specialized autonomous development workflows

| Agent | Purpose | Usage |
|-------|---------|-------|
| `adw_scout.py` | Repository navigation & annotation | Import `ScoutRepository` for codebase analysis |
| `adw_mentor_agent.py` | Strategic planning & KPI management | Import `StrategicPlanManager` for business planning |
| `adw_chore_implement.py` | Automated chore task implementation | Use for repetitive maintenance tasks |
| `adw_build_update_task.py` | Build & update task automation | Use for build pipeline tasks |
| `adw_plan_implement_update_task.py` | Complete plan-implement-update cycle | Full workflow automation |
| `adw_agent_meta_constructor.py` | Agent creation & meta-construction | Build new agents dynamically |
| `adw_prompt.py` | Prompt engineering & management | Manage agent prompts |
| `adw_slash_command.py` | Slash command creation | Create custom commands |
| `command_analyzer.py` | Analyze command effectiveness | Evaluate command performance |
| `command_improvement_orchestrator.py` | Improve existing commands | Optimize command workflows |

**Access Pattern**:
```python
# From CODEXA modules
import sys
sys.path.append('../adws')
from adw_scout import ScoutRepository
from adw_mentor_agent import StrategicPlanManager
```

### Claude Code Commands (../.claude/commands/)

**When to use**: Via Claude Code CLI with `/command-name`

**Development Commands**:
- `/plan` - Plan implementation strategies
- `/implement` - Implement features
- `/feature` - Create new features
- `/bug` - Fix bugs with guided workflow
- `/chore` - Handle chore tasks
- `/patch` - Apply quick patches
- `/build` - Build the project

**Git Commands**:
- `/commit` - Create intelligent commits
- `/pull_request` - Create pull requests
- `/git-status` - Enhanced git status
- `/git-review` - Review code changes

**Testing Commands**:
- `/test` - Run unit tests
- `/test_e2e` - Run end-to-end tests
- `/resolve_failed_test` - Debug failing tests

**Research & E-commerce Commands**:
- `/pesquisa` - Market research for Brazilian marketplaces
- `/codex_anuncio` - Generate optimized marketplace ads
- `/research_agent` - Orchestrate research agents
- `/mentor` - Strategic mentoring and planning
- `/hop_pesquisa` - HOP-based research orchestration
- `/hop_anuncio` - HOP-based ad generation
- `/hop_brand` - HOP-based brand strategy

**Documentation Commands**:
- `/document` - Generate documentation
- `/review` - Review code and docs
- `/prime` - Prime system with context

**Infrastructure Commands**:
- `/health_check` - System health verification
- `/install` - Complete system installation

**See**: `../.claude/commands/README.md` for complete list of 51+ commands

---

## 📦 Available Modules

### crud

Unified CRUD operations for documentation and e-commerce data

**Operations:**

- `create`: Create a new document or data entry
- `read`: Read a document or data entry
- `update`: Update an existing document or data entry
- `delete`: Delete a document or data entry
- `list`: List all items of a specific type
- `search`: Search for items by keyword

**Usage Examples:**

```bash
python cli.py crud create test.md --content '# Test' --type document
```

```bash
python cli.py crud read test.md --type document
```

```bash
python cli.py crud update test.md --content '# Updated' --type document
```

```bash
python cli.py crud delete test.md --force
```

```bash
python cli.py crud list --type document
```

```bash
python cli.py crud search --keyword 'test'
```

---

### scout

Intelligent repository navigation and organization

**Operations:**

- `scan`: Scan repository and build structure map
- `annotate`: Add PURPOSE annotation to file
- `query`: Query where files should be located
- `find`: Find files by pattern or extension
- `stats`: Get repository statistics

**Usage Examples:**

```bash
python cli.py scout scan --target . --cache
```

```bash
python cli.py scout annotate file.py --axiom 'Core CRUD operations' --trigger 'See hop_orchestrator.py'
```

```bash
python cli.py scout query 'Where should I put ML training scripts?'
```

```bash
python cli.py scout find --pattern '*.py'
```

```bash
python cli.py scout stats
```

---

### product_manager

E-commerce product catalog management with CRUD operations

**Operations:**

- `create`: Create a new product
- `read`: Read product by ID
- `update`: Update existing product
- `delete`: Delete a product
- `list`: List all products
- `search`: Search products by keyword
- `bulk_import`: Import multiple products from JSON
- `bulk_export`: Export all products to JSON

**Usage Examples:**

```bash
python cli.py ecom products create --name 'Smartwatch X' --price 299.99 --category 'Electronics'
```

```bash
python cli.py ecom products read <product_id>
```

```bash
python cli.py ecom products update <product_id> --price 279.99
```

```bash
python cli.py ecom products delete <product_id>
```

```bash
python cli.py ecom products list --category 'Electronics'
```

```bash
python cli.py ecom products search --keyword 'smart'
```

---

### strategy_mentor

Strategic planning and KPI tracking for e-commerce

**Operations:**

- `create_plan`: Create strategic plan
- `read_plan`: Read strategic plan
- `update_plan`: Update strategic plan
- `list_plans`: List all plans
- `update_kpi`: Update KPI progress

**Usage Examples:**

```bash
python cli.py ecom strategy create-plan --title 'Q4 Growth' --objective 'Increase sales'
```

```bash
python cli.py ecom strategy list-plans
```

```bash
python cli.py ecom strategy read-plan <plan_id>
```

```bash
python cli.py ecom strategy update-kpi <plan_id> <kpi_name> <value>
```

---

### competitor_scout

Competitor analysis and intelligence

**Operations:**

- `add_competitor`: Add competitor product
- `compare`: Compare products
- `list_competitors`: List all competitors

**Usage Examples:**

```bash
python cli.py ecom competitor add --name 'Competitor Watch' --competitor-name 'Competitor X' --price 249.99
```

```bash
python cli.py ecom competitor compare <our_product_id> <competitor_id>
```

```bash
python cli.py ecom competitor list
```

---

### knowledge_base

Documentation and knowledge management

**Operations:**

- `add_entry`: Add knowledge entry
- `search`: Search knowledge base
- `list_entries`: List all entries

**Usage Examples:**

```bash
python cli.py ecom knowledge add --title 'Product Guidelines' --content '...' --category 'docs'
```

```bash
python cli.py ecom knowledge search --keyword 'pricing'
```

```bash
python cli.py ecom knowledge list --category 'docs'
```

---



---

## 🚀 For Humans: Getting Started

### Installation

```bash
cd codexa/
pip install -r requirements.txt
```

### Basic Usage

```bash
# List all modules
python cli.py --help

# CRUD operations
python cli.py crud --help

# Scout operations
python cli.py scout --help

# E-commerce operations
python cli.py ecom --help

# Update this README
python cli.py readme update
```

### Architecture

CODEXA uses the **HOP (Hierarchical Orchestration Pattern)**:

1. **Hierarchical**: Modules organized by domain
2. **Orchestration**: Central coordinator routes requests
3. **Pattern**: Reusable architecture for multi-agent systems

```
codexa/
├── hop_orchestrator.py       # Main coordinator
├── modules/
│   ├── crud_ops.py           # Core CRUD operations
│   ├── scout_ops.py          # Repository navigation
│   └── ecommerce/            # E-commerce modules
└── cli.py                    # Command-line interface
```

---

## 🧬 Meta-Construction Philosophy

CODEXA follows meta-construction principles:

- **Self-Awareness**: Knows its capabilities through introspection
- **Auto-Documentation**: Updates README when modules change
- **Loose Coupling**: Modules are independent and replaceable
- **Intentional Entropy**: Flexibility for creative problem-solving

---

## 📊 System Status

- **Working Directory**: `C:\Users\Dell\Documents\GitHub\tac-7\codexa`
- **Modules Registered**: 6
- **Last Introspection**: 2025-11-11T19:37:13.925830

---

## 📄 License

Generated by CODEXA HOP-001 Meta-Agent
🤖 Part of the TAC-7 (Tactical Agentic Commerce) project

---

*This README is auto-generated and auto-updated. Do not edit manually.*
*Last auto-update: 2025-11-11T19:37:13.925909*
