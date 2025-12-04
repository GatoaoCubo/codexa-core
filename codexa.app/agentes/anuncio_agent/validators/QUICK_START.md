# Anúncio Validator - Quick Start Guide

## Installation

The module is already installed in:
```
codexa.app/agentes/anuncio_agent/validators/
```

## Basic Import

```python
from validators.anuncio_validator import AnuncioValidator, validate_anuncio
```

## 30-Second Example

```python
from validators.anuncio_validator import validate_anuncio
import json

result = validate_anuncio(
    titulos=[
        "Whey Protein Premium 1kg - Ganho Muscular Rápido",
        "Proteína Isolada 1kg - Absorção Máxima Pós-Treino",
        "Whey Concentrado 1kg - Força para Atletas Sérios"
    ],
    descricao="Nossa proteína premium é a melhor. " * 100,  # 3300+ chars
    keywords_block_1="protein, whey, " + ", ".join([f"term{i}" for i in range(115)]),
    keywords_block_2="treino, " + ", ".join([f"word{i}" for i in range(114)]),
    bullets=["Benefit point with 270+ characters... " * 8 for _ in range(10)]
)

print(json.dumps(result, indent=2))
# Output: JSON report with overall_score (0-10), status, components, issues
```

## Results Explained

```json
{
  "overall_score": 7.5,           # 0-10 scale
  "status": "WARN",               # PASS | WARN | FAIL
  "total_issues": 2,
  "components": {
    "titulos": {
      "score": 8.0,               # Individual dimension score
      "status": "PASS",
      "issues": []                # What needs fixing
    },
    "keywords": {"score": 7.0, ...},
    "descricao": {"score": 8.5, ...},
    "bullets": {"score": 6.0, ...},
    "compliance": {"score": 10.0, ...}
  },
  "recommendations": [            # Suggested improvements
    "Adjust titles to exactly 58-60 characters..."
  ]
}
```

## Key Requirements

| Dimension | Requirement | Max Points |
|-----------|-------------|-----------|
| **Titles** | 3x exactly 58-60 chars | 2.5/10 |
| **Keywords** | 60+ unique, 115-120 per block | 2.0/10 |
| **Description** | 3300+ chars, StoryBrand elements | 3.0/10 |
| **Bullets** | 10x exactly 250-299 chars | 1.5/10 |
| **Compliance** | No HTML, emojis, prohibited claims | 1.0/10 |

## Scoring Scale

- **8.0-10.0**: PASS → Ready to publish
- **6.0-8.0**: WARN → Minor fixes needed
- **0.0-6.0**: FAIL → Major revision required

## Common Issues

### Low Title Score
✗ "Short Title" (11 chars)
✓ "Whey Protein Premium 1kg - Ganho Muscular Rápido" (58 chars)

### Low Keywords Score
✗ Only 50 unique terms
✓ Ensure 60+ unique keywords across both blocks

### Low Description Score
✗ Only 1500 chars (too short)
✓ Expand to 3300+ with problem-solution-success-CTA

### Low Bullet Score
✗ "Short benefit" (14 chars)
✓ "Comprehensive benefit statement with detailed explanation..." (270+ chars)

## Validation Modes

### Lenient (Default)
```python
report = validator.validate(..., strict_mode=False)
# Score-based status (8.0+ = PASS, 6.0+ = WARN)
```

### Strict (Compliance)
```python
report = validator.validate(..., strict_mode=True)
# Any issue = FAIL (use for publication gates)
```

## Running Examples

```bash
cd codexa.app/agentes/anuncio_agent/

# Run built-in tests
python validators/anuncio_validator.py

# Run 5 example scenarios
python validators/example_usage.py
```

## Integration Example

```python
# FastAPI integration
from fastapi import FastAPI
from validators.anuncio_validator import validate_anuncio

app = FastAPI()

@app.post("/validate-anuncio")
async def validate(request: dict):
    return validate_anuncio(
        titulos=request['titulos'],
        descricao=request['descricao'],
        keywords_block_1=request['keywords_1'],
        keywords_block_2=request['keywords_2'],
        bullets=request['bullets']
    )
```

## Quality Gate Pattern

```python
from validators.anuncio_validator import AnuncioValidator

validator = AnuncioValidator()
report = validator.validate(...)

# Check if ready for publication
if report.overall_score >= 8.0:
    publish_to_marketplace()
elif report.overall_score >= 6.0:
    request_human_review()
else:
    reject_and_ask_for_revision()
```

## Full Documentation

- **README.md**: 380 lines, complete API reference
- **IMPLEMENTATION_SUMMARY.md**: Technical details and design
- **example_usage.py**: 5 runnable scenarios
- **anuncio_validator.py**: 728 lines with docstrings

## API Cheat Sheet

```python
# Method 1: Class-based (full control)
from validators.anuncio_validator import AnuncioValidator

validator = AnuncioValidator()
report = validator.validate(
    titulos=[...],
    descricao="...",
    keywords_block_1="...",
    keywords_block_2="...",
    bullets=[...],
    strict_mode=False
)

# Access results
print(report.overall_score)              # 0-10 float
print(report.status)                     # "PASS" | "WARN" | "FAIL"
print(report.component_scores['titulos']) # Individual component
print(report.to_json())                  # JSON string
print(report.to_dict())                  # Python dict

# Method 2: Simple function
from validators.anuncio_validator import validate_anuncio

result = validate_anuncio(titulos=[...], ...)  # Returns dict
```

## Constants (Easily Customizable)

```python
# In AnuncioValidator class:
TITLE_MIN_CHARS = 58
TITLE_MAX_CHARS = 60
KEYWORDS_MIN_UNIQUE = 60
DESCRIPTION_MIN_CHARS = 3300
BULLET_MIN_CHARS = 250
BULLET_MAX_CHARS = 299

PASS_THRESHOLD = 8.0
WARN_THRESHOLD = 6.0
```

## Questions?

1. **How do I validate?** → Use `validator.validate()` or `validate_anuncio()`
2. **What's a good score?** → 8.0+ is PASS, 6.0+ is WARN
3. **What's required?** → Titles (58-60 chars), Keywords (60+ unique), Description (3300+ chars), Bullets (10x 250-299 chars)
4. **How do I use results?** → Check `report.overall_score` and `report.status` for decisions
5. **Can I integrate it?** → Yes! It's JSON-serializable and has no dependencies

---

**Version**: 1.0.0 | **Status**: Production-Ready
