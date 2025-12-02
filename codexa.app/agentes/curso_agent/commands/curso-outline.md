# /curso_outline | Generate Course Outline

## Purpose
Generate complete course outline with modules, objectives, timing, prerequisites.

## Usage
```
/curso_outline
```

## Parameters (Interactive)
- **Scope**: Layer coverage (1, 1-2, 1-2-3)
- **Duration**: Target hours (10-50h)
- **Priority**: Output format priority (scripts, workbooks, exercises, all)

## Workflow

### Step 1: Gather Parameters
Ask user for:
1. Scope: Which CODEXA layers to cover?
2. Duration: How many hours total?
3. Timeline: Hard deadline or flexible?

### Step 2: Execute Builder
```bash
python builders/01_course_outline_builder.py --scope [SCOPE] --duration [HOURS] --verbose
```

### Step 3: Review Output
- Check outputs/outlines/*.md
- Verify module count appropriate for duration
- Confirm objectives measurable (Bloom's Taxonomy)

### Step 4: Validate (Optional)
```bash
python validators/03_pedagogical_validator.py --file outputs/outlines/*.md
```

## Output
Trinity format in outputs/outlines/:
- outline_layer_[SCOPE]_[HOURS]h.md
- outline_layer_[SCOPE]_[HOURS]h.llm.json
- outline_layer_[SCOPE]_[HOURS]h.meta.json

## Example
```
User: /curso_outline
Agent: What scope? (1, 1-2, 1-2-3)
User: 1-2
Agent: Duration in hours? (10-50)
User: 20
Agent: [Executes builder, generates outline]
Agent: Course outline generated! 6 modules, 20h total. Review: outputs/outlines/outline_layer_1_2_20h.md
```

## Next Steps
After outline approval:
- `/curso_script` - Generate video scripts for each module
- `/curso_workbook` - Generate workbooks for each module

---
**Version**: 2.0.0 | **Builder**: 01_course_outline_builder.py
