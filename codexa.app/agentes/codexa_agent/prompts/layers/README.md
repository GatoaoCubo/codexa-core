# CODEXA Prompt Layers

**Phase 1 Deliverable**: 8 composable prompt layers for agent construction.

---

## Layers

| Layer | Purpose | Lines |
|-------|---------|-------|
| `01_identity_layer.md` | Agent identity & role | ~400 |
| `02_operating_modes.md` | 7 operating modes | ~600 |
| `03_tool_usage_layer.md` | Tool definitions | ~600 |
| `04_communication_layer.md` | User interaction | ~450 |
| `05_code_conventions.md` | Code style guide | ~550 |
| `06_design_system.md` | Design tokens | ~470 |
| `07_steering_hooks.md` | Behavior steering | ~420 |
| `08_workflows.md` | Workflow patterns | ~440 |

---

## Usage

### With Composer

```python
from prompts.layers.composer import PromptComposer

composer = PromptComposer()
prompt = composer.compose(
    mode="planning",
    agent_type="meta-constructor"
)
```

### With Runtime

```python
from src.runtime import PromptLoader, CompositionType

loader = PromptLoader()
prompt = loader.load_composition(CompositionType.PLANNING_AGENT)
```

---

## Composition Types

- `PLANNING_AGENT`: Identity + Modes + Tools + Communication
- `EXECUTION_AGENT`: Identity + Modes + Tools + Code + Workflows
- `VERIFICATION_AGENT`: Identity + Modes + Tools + Steering

---

**See**: [config/prompt_layers.yml](../../config/prompt_layers.yml)
