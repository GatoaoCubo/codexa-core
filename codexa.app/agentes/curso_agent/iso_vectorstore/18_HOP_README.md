<!-- iso_vectorstore -->
<!--
  Source: README.md
  Agent: curso_agent
  Synced: 2025-11-30
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# Prompts | curso_agent

**Purpose**: Higher-Order Prompts (HOPs) following TAC-7 framework

## Planned HOPs (Sprint 4)

1. **91_curso_outline_HOP.md** - Course outline generation workflow
2. **92_curso_script_HOP.md** - Video script generation workflow
3. **93_curso_workbook_HOP.md** - Workbook generation workflow
4. **94_curso_sales_HOP.md** - Sales collateral generation workflow
5. **95_curso_validate_HOP.md** - Quality validation workflow

## TAC-7 Structure

Each HOP must include:
- **MODULE_METADATA**: id, version, purpose, dependencies, category
- **INPUT_CONTRACT**: $variables (type, validation, example)
- **OUTPUT_CONTRACT**: structure, format, validation
- **TASK**: role, objective, standards, constraints
- **STEPS**: 3-7 actionable steps (H3 headers)
- **VALIDATION**: Quality gates (≥7.0/10.0)
- **CONTEXT**: Usage, $arguments chaining, assumptions

## Migration Plan

HOPs currently in `iso_vectorstore/` will be migrated to TAC-7 format:
- Source: `iso_vectorstore/09_HOP_main.md`, `10_HOP_secondary.md`
- Target: `prompts/91-95_curso_*_HOP.md`
- Validation: `validators/07_hop_sync_validator.py`

## Status

- **Sprint 1**: Directory created
- **Sprint 4**: HOP migration and TAC-7 compliance
- **Sprint 5**: Full validation
