# Validators | curso_agent

**Purpose**: Automated quality gates for course content validation

## Planned Validators (Sprint 2)

1. **01_content_quality_validator.py** - Hook ≤90s, Objectives measurable, Demos real, [OPEN_VARIABLES] ≥2
2. **02_brand_voice_validator.py** - Seed words ≥3, Tone disruptivo-sofisticado, No hype words
3. **03_pedagogical_validator.py** - Progressive complexity, Prerequisites clear, Outcomes actionable
4. **04_technical_validator.py** - [OPEN_VARIABLES] ≥2, Timing feasible, Examples Brazilian
5. **05_hotmart_compliance_validator.py** - DRM, LGPD, Claims sensíveis, Video specs

## Quality Thresholds

- Minimum score: **7.0/10.0**
- Hotmart compliance: **8.0/10.0** (stricter due to legal requirements)

## Usage Pattern

```python
from validators.content_quality_validator import validate_content

result = validate_content(script_file)
if result.score >= 7.0:
    print("[OK] Content quality validated")
else:
    print(f"[FAIL] Score {result.score}: {result.issues}")
```

## Status

- **Sprint 1**: Directory created, structure ready
- **Sprint 2**: Validators implementation
- **Sprint 3**: Integration with builders
