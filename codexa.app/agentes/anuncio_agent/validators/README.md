# Anúncio Validator Module

**Version**: 1.0.0
**Scope**: TEXT-ONLY (títulos, descricao, keywords, bullets)
**Language**: Python 3.8+

Production-ready quality validation module for e-commerce product listings (anúncios).

## Overview

The `anuncio_validator` module provides comprehensive quality scoring and validation for product descriptions across all critical dimensions:

- **Títulos**: Title optimization (58-60 chars ML algorithm)
- **Keywords**: SEO keyword validation (60+ unique terms)
- **Descrição**: Long-form description quality (3300+ chars)
- **Bullets**: Feature/benefit bullets (10 items, 250-299 chars each)
- **Compliance**: Platform policy compliance (no HTML, emojis, prohibited claims)

## Quick Start

### Basic Usage

```python
from validators.anuncio_validator import AnuncioValidator

validator = AnuncioValidator()

report = validator.validate(
    titulos=[
        "Whey Protein Premium 1kg - Ganho Muscular Rápido",
        "Proteína Concentrada - Potência Máxima para Atletas",
        "Whey Isolado 1kg - Absorção Rápida Pós-Treino"
    ],
    descricao="Nossa proteína whey premium é a escolha definitiva...",
    keywords_block_1="protein, whey, suplemento, musculação, ...",
    keywords_block_2="treino, força, performance, ganho muscular, ...",
    bullets=[
        "Bullet 1 with 250+ characters...",
        "Bullet 2 with 250+ characters...",
        # ... 10 bullets total
    ]
)

# Get results
print(report.overall_score)  # 0-10 scale
print(report.status)         # "PASS" | "WARN" | "FAIL"
print(report.to_json())      # Full report as JSON string
```

### Using the Convenience Function

```python
from validators.anuncio_validator import validate_anuncio

result = validate_anuncio(
    titulos=[...],
    descricao="...",
    keywords_block_1="...",
    keywords_block_2="...",
    bullets=[...]
)

# Returns JSON-serializable dictionary
print(result['overall_score'])
print(result['status'])
```

## Validation Dimensions

### 1. Títulos (25% weight)

**Requirements**:
- Exactly 3 title variations
- Each title: 58-60 characters (optimized for marketplace ML algorithms)
- Distinct angles/approaches

**Scoring**:
- Character compliance: 0-5 points
- Count validation: 0-5 points

**Issues Detected**:
- Incorrect character count (too short or too long)
- Wrong number of titles

---

### 2. Keywords (20% weight)

**Requirements**:
- 2 keyword blocks (separated for multi-field listings)
- 115-120 terms per block (230-240 total)
- 60+ unique keywords minimum
- Comma-separated format

**Scoring**:
- Block validity: 0-5 points (both blocks in range)
- Unique keyword count: 0-5 points

**Issues Detected**:
- Block has too few terms (< 115)
- Block has too many terms (> 120)
- Insufficient unique keywords
- Duplicate keywords across blocks

---

### 3. Descrição (30% weight)

**Requirements**:
- Minimum 3300 characters (long-form persuasive copy)
- StoryBrand framework elements:
  - Problem: mentions customer pain/difficulty
  - Solution: describes how product resolves issue
  - Success: highlights results/achievements
  - CTA: includes call-to-action

**Scoring**:
- Length compliance: 0-5 points
- StoryBrand elements: 0-5 points (4 elements possible)

**Issues Detected**:
- Insufficient character count
- Missing StoryBrand narrative elements

---

### 4. Bullets (15% weight)

**Requirements**:
- Exactly 10 bullet points
- Each bullet: 250-299 characters (detailed feature/benefit)
- Clear, scannable format

**Scoring**:
- Count validation: 0-5 points
- Character compliance: 0-5 points

**Issues Detected**:
- Wrong number of bullets
- Bullet too short (< 250 chars)
- Bullet too long (> 299 chars)

---

### 5. Compliance (10% weight)

**Requirements**:
- No HTML/CSS/JavaScript tags
- No decorative emojis
- No prohibited marketing claims
- No external links (must use marketplace CTAs)

**Prohibited Patterns**:
- "#1" / "número 1" (unsubstantiated claim)
- "melhor do brasil" (superlative)
- "líder de mercado" (unproven claim)
- "cura" (medical claim)
- "milagre" (miracle claim)

**Scoring**:
- 2.5 points per compliance check passed (4 checks total)

**Issues Detected**:
- HTML tags detected
- Emoji characters present
- Prohibited claims found
- External links detected

---

## Scoring System

### Overall Score: 0-10 Scale

```
Score Range  | Status | Action
0.0 - 6.0    | FAIL   | Requires substantial revision
6.0 - 8.0    | WARN   | Needs minor improvements
8.0 - 10.0   | PASS   | Publication-ready
```

### Weighted Calculation

```
Overall Score =
  (Titulos Score / 10) × 0.25 +
  (Keywords Score / 10) × 0.20 +
  (Descrição Score / 10) × 0.30 +
  (Bullets Score / 10) × 0.15 +
  (Compliance Score / 10) × 0.10

Result: 0-10 scale
```

## Output Format

### JSON Report Structure

```json
{
  "timestamp": "2025-12-04T17:51:30.518991",
  "version": "1.0.0",
  "overall_score": 7.5,
  "status": "WARN",
  "total_issues": 3,
  "components": {
    "titulos": {
      "score": 7.5,
      "max_score": 10.0,
      "status": "WARN",
      "details": {
        "titles": [
          {"number": 1, "chars": 58, "valid": true},
          {"number": 2, "chars": 59, "valid": true},
          {"number": 3, "chars": 60, "valid": true}
        ],
        "valid_count": 3,
        "total_count": 3
      },
      "issues": []
    },
    "keywords": {
      "score": 10.0,
      "max_score": 10.0,
      "status": "PASS",
      "details": {...},
      "issues": []
    },
    "descricao": {
      "score": 5.0,
      "max_score": 10.0,
      "status": "WARN",
      "details": {...},
      "issues": ["Missing StoryBrand elements: problem, solution, success, cta"]
    },
    "bullets": {
      "score": 8.0,
      "max_score": 10.0,
      "status": "PASS",
      "details": {...},
      "issues": []
    },
    "compliance": {
      "score": 10.0,
      "max_score": 10.0,
      "status": "PASS",
      "details": {...},
      "issues": []
    }
  },
  "recommendations": [
    "Expand description to include all StoryBrand narrative elements"
  ]
}
```

## API Reference

### AnuncioValidator Class

#### `validate()`

```python
def validate(
    titulos: List[str],
    descricao: str,
    keywords_block_1: str,
    keywords_block_2: str,
    bullets: List[str],
    strict_mode: bool = False
) -> ValidationReport
```

**Parameters**:
- `titulos`: List of 3 title variations
- `descricao`: Long-form description text (3300+ chars)
- `keywords_block_1`: Comma-separated keywords (115-120 terms)
- `keywords_block_2`: Comma-separated keywords (115-120 terms)
- `bullets`: List of 10 bullet points (250-299 chars each)
- `strict_mode`: If True, any issue causes FAIL status (default: False)

**Returns**: `ValidationReport` object

**Example**:
```python
validator = AnuncioValidator()
report = validator.validate(
    titulos=[...],
    descricao="...",
    keywords_block_1="...",
    keywords_block_2="...",
    bullets=[...]
)
```

---

### ValidationReport Class

Dataclass containing validation results.

**Key Attributes**:
- `timestamp`: ISO format timestamp
- `version`: Validator version
- `overall_score`: 0-10 scale
- `status`: "PASS" | "WARN" | "FAIL"
- `component_scores`: Dict of dimension scores
- `total_issues`: Count of detected issues
- `recommendations`: List of improvement suggestions

**Methods**:
- `to_dict()`: Returns JSON-serializable dictionary
- `to_json()`: Returns formatted JSON string

---

### ComponentScore Class

Dataclass for individual dimension scores.

**Attributes**:
- `name`: Dimension name (titulos, keywords, etc.)
- `score`: Component score (0-10)
- `max_score`: Maximum possible score (always 10)
- `status`: "PASS" | "WARN" | "FAIL"
- `details`: Dict with dimension-specific metrics
- `issues`: List of detected issues

---

### Utility Functions

#### `validate_anuncio()`

Convenience function returning JSON-serializable dictionary:

```python
def validate_anuncio(
    titulos: List[str],
    descricao: str,
    keywords_block_1: str,
    keywords_block_2: str,
    bullets: List[str],
    strict_mode: bool = False
) -> Dict[str, Any]
```

**Example**:
```python
result = validate_anuncio(titulos=[...], descricao="...", ...)
print(json.dumps(result, indent=2))
```

---

## Configuration Constants

### Dimension Requirements

```python
# Títulos
TITLE_COUNT = 3
TITLE_MIN_CHARS = 58
TITLE_MAX_CHARS = 60

# Keywords
KEYWORDS_MIN_UNIQUE = 60
KEYWORDS_BLOCK_MIN = 115
KEYWORDS_BLOCK_MAX = 120

# Descrição
DESCRIPTION_MIN_CHARS = 3300

# Bullets
BULLET_COUNT = 10
BULLET_MIN_CHARS = 250
BULLET_MAX_CHARS = 299
```

### Scoring Weights

```python
WEIGHTS = {
    "titulos": 0.25,      # Title optimization
    "keywords": 0.20,     # SEO discovery
    "descricao": 0.30,    # Persuasive copy
    "bullets": 0.15,      # Feature benefits
    "compliance": 0.10    # Policy compliance
}
```

### Status Thresholds

```python
PASS_THRESHOLD = 8.0   # Score ≥ 8.0 = PASS
WARN_THRESHOLD = 6.0   # Score 6.0-8.0 = WARN
# Score < 6.0 = FAIL
```

---

## Strict Mode

By default, the validator uses **lenient** mode:
- Issues are counted but don't automatically fail the report
- Status determined by overall score
- Allows for flexibility in edge cases

Enable **strict mode** for rigid validation:
```python
report = validator.validate(..., strict_mode=True)
```

In strict mode:
- Any detected issue → status = "FAIL"
- Perfect validation required for "PASS" status
- Use for compliance/QA gates

---

## Integration Examples

### With FastAPI

```python
from fastapi import FastAPI
from validators.anuncio_validator import validate_anuncio

app = FastAPI()

@app.post("/validate-anuncio")
async def validate_endpoint(request: dict):
    result = validate_anuncio(
        titulos=request['titulos'],
        descricao=request['descricao'],
        keywords_block_1=request['keywords_1'],
        keywords_block_2=request['keywords_2'],
        bullets=request['bullets']
    )
    return result
```

### With Pydantic Models

```python
from pydantic import BaseModel
from validators.anuncio_validator import validate_anuncio

class AnuncioValidationRequest(BaseModel):
    titulos: list[str]
    descricao: str
    keywords_block_1: str
    keywords_block_2: str
    bullets: list[str]

def validate_request(data: AnuncioValidationRequest):
    return validate_anuncio(
        titulos=data.titulos,
        descricao=data.descricao,
        keywords_block_1=data.keywords_block_1,
        keywords_block_2=data.keywords_block_2,
        bullets=data.bullets
    )
```

### Batch Processing

```python
from validators.anuncio_validator import validate_anuncio
import json

# Validate multiple anúncios
anuncios = load_anuncios_from_db()
results = []

for anuncio in anuncios:
    report = validate_anuncio(
        titulos=anuncio['titulos'],
        descricao=anuncio['descricao'],
        keywords_block_1=anuncio['keywords_1'],
        keywords_block_2=anuncio['keywords_2'],
        bullets=anuncio['bullets']
    )
    results.append({
        'product_id': anuncio['id'],
        'validation': report
    })

# Export results
with open('validation_results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

---

## Quality Gates

### Pre-Publication Gate

```python
validator = AnuncioValidator()
report = validator.validate(...)

if report.overall_score >= 8.0:
    # Publish to marketplace
    publish_anuncio(data)
else:
    # Hold for review
    send_for_human_review(data, report)
```

### Multi-Stage Gate

```python
# Stage 1: Content completeness
if report.component_scores['descricao'].score < 5.0:
    return "REJECT - Description incomplete"

# Stage 2: Compliance
if report.component_scores['compliance'].status != "PASS":
    return "REJECT - Compliance issues"

# Stage 3: Overall quality
if report.overall_score < 7.0:
    return "FLAG - Needs improvement"

# All passed
return "APPROVE - Ready for publication"
```

---

## Troubleshooting

### Low Keywords Score

**Issue**: Keywords block count is slightly off (e.g., 114 or 121 terms)

**Solution**:
- Keywords must be 115-120 per block for marketplace algorithms
- Count terms carefully: split by comma, trim whitespace
- Use `validate_anuncio().to_dict()` to see exact counts

### Low Description Score

**Issue**: StoryBrand elements not detected despite being present

**Solution**:
- The validator uses Portuguese keyword matching
- Ensure text includes: problem, solution, success, CTA language
- Check exact keywords: "problema", "dor", "sofre", "solução", "resultado", "compre", "adquira"

### Low Bullet Score

**Issue**: Some bullets fall just under 250 or just over 299 characters

**Solution**:
- Each bullet must be 250-299 characters exactly
- Count characters carefully (spaces count)
- Add/remove content to hit the range

### Compliance Failures

**Issue**: Prohibited patterns detected unexpectedly

**Solution**:
- The validator catches patterns case-insensitively
- Avoid even partial matches ("Milagre" would match "milagr" pattern)
- Use marketplace-approved language for claims

---

## Version History

### v1.0.0 (2025-12-04)
- Initial release
- 5-dimension scoring system
- JSON report export
- Compliance validation
- StoryBrand framework detection
- Batch processing support

---

## Contributing

To suggest improvements:
1. Test the validator against real anúncios
2. Document edge cases discovered
3. Create issue with validation example
4. Propose threshold adjustments if needed

---

## License

Part of codexa-core project framework.
