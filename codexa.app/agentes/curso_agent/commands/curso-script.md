# /curso_script | Generate Video Script

## Purpose
Generate 15-30min video script with timing marks, hooks, and [OPEN_VARIABLES].

## Usage
```
/curso_script [module_id]
```

## Parameters
- **module_id**: Module number (01-06) from context/ directory

## Workflow

### Step 1: Select Module
If not provided, show available modules:
- 01: Introdução ao CODEXA
- 02: Anúncios (anuncio_agent)
- 03: Pesquisa (pesquisa_agent)
- 04: Marca (marca_agent)
- 05: Fotos (photo_agent)
- 06: Meta-Construção (codexa_agent)

### Step 2: Execute Builder
```bash
python builders/02_video_script_builder.py --module [ID] --verbose
```

### Step 3: Validate Output
```bash
python validators/01_content_quality_validator.py --file outputs/video_scripts/[ID]_*.md --verbose
```

### Step 4: Review Quality
Check validation results:
- Hook ≤90s? ✓
- [OPEN_VARIABLES] ≥2? ✓
- Timing marks present? ✓
- Brand voice compliant? ✓

## Output
Trinity format in outputs/video_scripts/:
- [ID]_[MODULE_NAME].md (meta-prompt for LLM)
- [ID]_[MODULE_NAME].llm.json (structured data)
- [ID]_[MODULE_NAME].meta.json (metadata)

## Example
```
User: /curso_script 01
Agent: Generating video script for Module 01: Introdução ao CODEXA...
Agent: [OK] Script generated (Trinity Output)
Agent: [OK] Validation: Score 7.5/10.0 PASSED
Agent: Output: outputs/video_scripts/01_MODULO_INTRODUCAO.md
Agent: Next: Execute meta-prompt with LLM to generate final script
```

## Quality Threshold
- Content Quality: ≥7.0/10.0
- Brand Voice: ≥7.0/10.0

---
**Version**: 2.0.0 | **Builder**: 02_video_script_builder.py | **Validator**: 01_content_quality_validator.py
