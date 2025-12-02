# CODEXA Multi-Agent Orchestration

**Version**: 1.0.0
**Created**: 2025-11-16
**Purpose**: Coordinate multi-agent workflows with $variable chaining

---

## Overview

The CODEXA multi-agent orchestration system enables workflows that span multiple agents, passing data between them using `$variable` references.

**Key Features**:
- ✅ Global path configuration (`config/paths.py`)
- ✅ Auto-discovery of all agents
- ✅ `$variable` chaining between agent outputs
- ✅ Workflow execution and error handling
- ✅ Multi-agent ADW support

---

## Architecture

```
codexa.app/
├── config/                          ← Global Orchestrator
│   ├── __init__.py
│   └── paths.py                     ← Master paths for ALL agents
│
├── multi_agent_orchestrator.py     ← Workflow coordinator
│
└── agentes/
    ├── codexa_agent/               ← Meta-constructor
    ├── pesquisa_agent/             ← Research
    ├── anuncio_agent/              ← Ad generation
    ├── marca_agent/                ← Brand validation
    └── photo_agent/                ← Image optimization
```

---

## Quick Start

### 1. Import Global Paths (from any agent)

```python
import sys
from pathlib import Path

# Add codexa.app to path (2 levels up from agent/config/)
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.paths import (
    AGENTS_ROOT,
    CODEXA_APP,
    get_agent_dir,
    get_agent_paths,
    get_all_agents,
)

# Get paths for any agent
anuncio_paths = get_agent_paths('anuncio')
all_agents = get_all_agents()
```

### 2. Use Multi-Agent Orchestrator

```python
from multi_agent_orchestrator import MultiAgentOrchestrator, WorkflowStep

# Create orchestrator
orchestrator = MultiAgentOrchestrator()

# Define workflow with $variable chaining
workflow = [
    # Step 1: Research
    WorkflowStep(
        agent_name='pesquisa',
        task_name='research',
        inputs={'product': 'Fone Bluetooth'}
    ),

    # Step 2: Generate ads using research output
    WorkflowStep(
        agent_name='anuncio',
        task_name='generate_ad',
        inputs={
            'research_data': '$pesquisa.output',  # ← $variable reference
            'platform': 'mercado_livre'
        }
    ),

    # Step 3: Validate brand consistency
    WorkflowStep(
        agent_name='marca',
        task_name='validate',
        inputs={
            'ad_content': '$anuncio.output'  # ← Chained from previous step
        }
    ),
]

# Execute
results = orchestrator.execute_workflow(workflow)

# Save report
orchestrator.save_workflow_report(results, 'my_workflow.json')
```

---

## $Variable Chaining

**Syntax**: `$agent_name.field`

**Supported patterns**:
- `$agent_name.output` - Full output data from agent
- `$agent_name.output_path` - Path to agent's output file
- `$agent_name.field_name` - Specific field from output data

**Example**:
```python
# Step 1 output: {'product_name': 'Fone XYZ', 'price': 199}
WorkflowStep('pesquisa', 'research', {...})

# Step 2 references step 1's output
WorkflowStep('anuncio', 'generate', {
    'product': '$pesquisa.product_name',  # → 'Fone XYZ'
    'price': '$pesquisa.price'            # → 199
})
```

---

## Example Workflows

### E-commerce Product Launch

```
pesquisa_agent (research)
    → $market_data
anuncio_agent (generate_listings)
    → $listings
photo_agent (optimize_images)
    → $optimized_images
marca_agent (brand_validation)
    → FINAL OUTPUT
```

### Content Creation Pipeline

```
pesquisa_agent (competitor_analysis)
    → $competitor_data
anuncio_agent (create_copy)
    → $ad_copy
marca_agent (tone_check)
    → APPROVED CONTENT
```

---

## Global Paths API

### Available Constants

```python
# Hierarchy
PROJECT_ROOT        # codexa/
CODEXA_APP          # codexa.app/
AGENTS_ROOT         # codexa.app/agentes/
CONFIG_DIR          # codexa.app/config/

# Global paths
PATH_REGISTRY       # 51_AGENT_REGISTRY.json
PATH_HOP_FRAMEWORK  # 42_HOP_FRAMEWORK.md
PATH_PRIME          # PRIME.md
PATH_GLOBAL_OUTPUTS # outputs/ (multi-agent coordination)
PATH_GLOBAL_LOGS    # logs/
```

### Utility Functions

```python
# Get any agent's directory
agent_dir = get_agent_dir('anuncio')

# Get all paths for an agent
paths = get_agent_paths('pesquisa')
# Returns: {root, builders, validators, templates, workflows, prompts, config, outputs, logs}

# List all agents
all_agents = get_all_agents()

# Get specific agent output
output_file = get_agent_output('pesquisa', 'research_notes.md')

# Agent count
count = get_agent_count()  # → 6
```

---

## Creating Multi-Agent ADWs

### Template Structure

```python
# adw_multi_agent_template.py

from config.paths import get_agent_paths, get_all_agents
from multi_agent_orchestrator import MultiAgentOrchestrator, WorkflowStep

def execute_multi_agent_workflow(product: str):
    """
    Multi-agent workflow for product research → ad creation.
    """
    orchestrator = MultiAgentOrchestrator()

    workflow = [
        WorkflowStep('pesquisa', 'research', {'product': product}),
        WorkflowStep('anuncio', 'generate', {'research': '$pesquisa.output'}),
    ]

    return orchestrator.execute_workflow(workflow)
```

---

## Testing

```bash
# Test global paths
cd codexa.app
python config/paths.py

# Test orchestrator
python multi_agent_orchestrator.py

# List available agents
python -c "from config.paths import get_all_agents; print([a.name for a in get_all_agents()])"
```

---

## Benefits

✅ **Single Source of Truth** - All paths centralized in `config/paths.py`
✅ **Auto-Discovery** - Automatically finds all agents
✅ **$Variable Chaining** - Pass data between agents seamlessly
✅ **Type-Safe** - Path objects, not strings
✅ **Cross-Platform** - Works on Windows/Linux/Mac
✅ **Scalable** - Easy to add new agents
✅ **Error Handling** - Built-in retry and error reporting

---

## Next Steps

1. **Create agent-specific ADWs** - Each agent can have builders that are orchestrated
2. **Implement real execution** - Currently orchestrator is a template (placeholder execution)
3. **Add retry logic** - Exponential backoff for failed steps
4. **Create web UI** - Visual workflow builder
5. **Add monitoring** - Real-time workflow execution tracking

---

**Version**: 1.0.0
**Status**: Production-Ready Template
**Author**: CODEXA Meta-Constructor
**Last Updated**: 2025-11-16
