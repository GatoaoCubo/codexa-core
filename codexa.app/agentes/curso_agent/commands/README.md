# Commands | curso_agent

**Purpose**: Slash commands for Claude Code integration

## Planned Commands (Sprint 3)

1. **/curso_outline** - Generate course outline (5-10 min workflow)
2. **/curso_script** - Generate video script for module (30-45 min)
3. **/curso_workbook** - Generate workbook for module (30-45 min)
4. **/curso_sales** - Generate sales collateral (20-30 min)
5. **/curso_validate** - Run all 5 validators
6. **/curso_package** - Package for Hotmart delivery

## Command Pattern

Each command wraps a builder + validator workflow:

```
/curso_script Module 1
  → Load context (01_MODULO_INTRODUCAO.md)
  → Run 02_video_script_builder.py
  → Run 01_content_quality_validator.py
  → Output validated script
```

## Status

- **Sprint 1**: Directory created
- **Sprint 3**: Commands implementation
- **Sprint 4**: Testing and documentation
