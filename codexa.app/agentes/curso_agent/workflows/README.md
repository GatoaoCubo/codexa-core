# Workflows | curso_agent

**Purpose**: Multi-phase ADW (Agentic Developer Workflows) for orchestration

## Planned Workflows (Sprint 3)

1. **01_ADW_QUICK_COURSE.md** - Quick course outline (5-10 min)
   - Load context → Generate outline → Validate → Deliver
   - $arguments: $scope → $outline → $validation_results

2. **02_ADW_FULL_MODULE.md** - Full module content (30-45 min)
   - Generate script → Generate workbook → Generate exercise → Validate → Deliver
   - $arguments: $outline → $script → $workbook → $exercise → $validation → $package

3. **03_ADW_SALES_PACKAGE.md** - Sales collateral (20-30 min)
   - Load brand → Generate landing → Generate emails → Generate ads → Validate → Deliver
   - $arguments: $brand_voice → $landing → $emails → $ads → $validation → $package

## ADW Pattern

Each workflow follows CODEXA meta-construction principles:
- **$arguments chaining**: Phase N output → Phase N+1 input
- **[OPEN_VARIABLES]**: Intentional blanks for customization
- **Quality gates**: Validation between phases
- **Trinity Output**: .md + .llm.json + .meta.json

## Status

- **Sprint 1**: Directory created
- **Sprint 3**: ADW files creation
- **Sprint 4**: End-to-end testing
