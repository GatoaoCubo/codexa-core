# /curso_validate | Run All Validators

## Purpose
Run complete validation suite on generated content (5 validators).

## Usage
```
/curso_validate [file_path]
/curso_validate --all
```

## Parameters
- **file_path**: Specific file to validate
- **--all**: Validate all outputs

## Validators
1. **Content Quality** (01) - Hook, timing, objectives, structure
2. **Brand Voice** (02) - Seed words, tone, no hype
3. **Pedagogical** (03) - Complexity, prerequisites, exercises
4. **Technical** (04) - [OPEN_VARIABLES], timing, examples
5. **Hotmart Compliance** (05) - DRM, LGPD, claims, specs

## Workflow

### Single File
```bash
python validators/01_content_quality_validator.py --file [PATH] --verbose
python validators/02_brand_voice_validator.py --file [PATH]
python validators/03_pedagogical_validator.py --file [PATH]
python validators/04_technical_validator.py --file [PATH]
```

### All Outputs
```bash
# Video scripts
for f in outputs/video_scripts/*.md; do
  python validators/01_content_quality_validator.py --file "$f"
done

# Workbooks
for f in outputs/workbooks/*.md; do
  python validators/03_pedagogical_validator.py --file "$f"
done

# Sales
for f in outputs/sales/*.md; do
  python validators/02_brand_voice_validator.py --file "$f"
done
```

## Quality Thresholds
- Content Quality: ≥7.0/10.0
- Brand Voice: ≥7.0/10.0
- Pedagogical: ≥7.0/10.0
- Technical: ≥7.0/10.0
- Hotmart Compliance: ≥8.0/10.0 (stricter)

## Output
Validation report with:
- Score for each validator
- Passed/Failed status
- Issues list (if failed)
- Recommendations

## Example
```
User: /curso_validate outputs/video_scripts/01_MODULO_INTRODUCAO.md

Agent: Running validation suite...
  [OK] Content Quality: 7.5/10.0 PASSED
  [OK] Brand Voice: 8.0/10.0 PASSED
  [OK] Technical: 7.0/10.0 PASSED

Overall: 7.5/10.0 PASSED (3/3 validators)
```

---
**Version**: 2.0.0 | **Validators**: 01-05_*_validator.py
