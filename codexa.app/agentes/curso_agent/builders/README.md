# Builders | curso_agent

**Purpose**: Automated content generation tools for course creation

## Planned Builders (Sprint 2)

1. **01_course_outline_builder.py** - Generate module outlines (objectives, timing, prerequisites)
2. **02_video_script_builder.py** - Create 15-30min scripts with timing marks and [OPEN_VARIABLES]
3. **03_workbook_builder.py** - Generate 8-15 page workbooks (theory + exercises)
4. **04_sales_collateral_builder.py** - Create landing pages, email sequences, ad copy
5. **05_hotmart_package_builder.py** - Package content for Hotmart deployment

## Usage Pattern

```python
# Import centralized paths
from config.paths import PATH_CONTEXT, PATH_OUTPUTS, CONTEXT_FILES

# Use paths for file operations
context_data = PATH_CONTEXT / "01_MODULO_INTRODUCAO.md"
output_file = PATH_OUTPUTS / "video_script_01.md"
```

## Status

- **Sprint 1**: Directory created, structure ready
- **Sprint 2**: Builders implementation
- **Sprint 3**: Integration testing
