# /curso_workbook | Generate Workbook

## Purpose
Generate 8-15 page workbook with theory, exercises, and reflection questions.

## Usage
```
/curso_workbook [module_id]
```

## Parameters
- **module_id**: Module number (01-06)

## Workflow

### Step 1: Execute Builder
```bash
python builders/03_workbook_builder.py --module [ID] --verbose
```

### Step 2: Validate
```bash
python validators/03_pedagogical_validator.py --file outputs/workbooks/[ID]_workbook.md
```

## Output
Trinity format in outputs/workbooks/:
- [ID]_workbook.md
- [ID]_workbook.llm.json
- [ID]_workbook.meta.json

## Structure
Generated workbook includes:
1. Cover Page (title, objectives, time)
2. Theory Section (2-3 pages)
3. Guided Exercises (3-4 pages)
4. Hands-On Practice (2-3 pages)
5. Reflection Questions (1 page)
6. Resources & Next Steps (1 page)

## Example
```
User: /curso_workbook 02
Agent: Generating workbook for Module 02: Anúncios...
Agent: [OK] Workbook generated (8-15 pages)
Agent: [OK] Validation: Score 8.0/10.0 PASSED
Agent: Output: outputs/workbooks/02_workbook.md
```

---
**Version**: 2.0.0 | **Builder**: 03_workbook_builder.py
