# CODEXA Configuration

Central configuration for the CODEXA agent system.

---

## Files

| File | Purpose |
|------|---------|
| `paths.py` | Centralized path constants |
| `agent_modes.yml` | 7 operating modes |
| `prompt_layers.yml` | Layer composition config |
| `artifact_schemas.yml` | Artifact type definitions |

---

## Usage

### Path Constants

```python
from config.paths import (
    PROJECT_ROOT,
    CODEXA_AGENT_DIR,
    PATH_PROMPTS,
    PATH_BUILDERS,
)
```

### Agent Modes

```yaml
# 7 modes available:
# PLANNING, EXECUTION, VERIFICATION, FIX, RESEARCH, ORCHESTRATION, REVIEW
```

---

**See**: [STRUCTURE.md](../STRUCTURE.md)
