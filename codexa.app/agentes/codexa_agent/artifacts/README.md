# CODEXA Artifacts

Artifact generation, templates, and validation for agent workflows.

---

## Structure

```
artifacts/
├── generators/          # Generate artifacts
│   ├── plan_generator.py
│   ├── report_generator.py
│   └── walkthrough_generator.py
│
├── templates/           # Jinja2 templates
│   ├── implementation_plan.jinja2
│   ├── execution_report.jinja2
│   ├── verification_report.jinja2
│   └── review_report.jinja2
│
└── validators/          # Validate artifacts
    ├── plan_validator.py
    └── report_validator.py
```

---

## Artifact Types

| Type | Template | Generator |
|------|----------|-----------|
| Implementation Plan | `implementation_plan.jinja2` | `plan_generator.py` |
| Execution Report | `execution_report.jinja2` | `report_generator.py` |
| Verification Report | `verification_report.jinja2` | `report_generator.py` |
| Review Report | `review_report.jinja2` | `report_generator.py` |
| Walkthrough | - | `walkthrough_generator.py` |

---

## Usage

```python
from artifacts.generators.plan_generator import generate_plan

plan = generate_plan(
    task="Add dark mode",
    spec_file="specs/dark_mode.md"
)
```

---

**See**: [config/artifact_schemas.yml](../config/artifact_schemas.yml)
