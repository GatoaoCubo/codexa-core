# E2E Test: HOP Anúncio Flow - Full Workflow Execution

Test the complete Higher-Order Prompt orchestration for Codex-Anúncio agent, validating all steps from research ingestion to final ad generation.

## User Story

As a marketplace seller
I want to generate complete optimized ads from research notes using the HOP system
So that I can create production-ready listings with quality gates and compliance validation

## Prerequisites

1. **Research Notes Available**:
   - Path: `USER_DOCS/produtos/research_test_produto.md`
   - Must contain all 22 structured blocks
   - Confidence score ≥0.60

2. **Execution Plan**:
   - File: `anuncio-agent/config/plans/full_anuncio.json`
   - Validated against `execution_plan_schema.json`

3. **Prompt Modules**:
   - All modules referenced in plan must exist
   - Located in `anuncio-agent/prompts/`

4. **Marketplace Config**:
   - `config/marketplace_specs.json` loaded
   - Compliance rules for target marketplace

## Test Steps

### Phase 1: Plan Validation (Steps 1-5)

1. Load execution plan from `anuncio-agent/config/plans/full_anuncio.json`
2. **Verify** plan JSON is valid and parseable
3. **Verify** all required fields present:
   - `plan_id`, `plan_name`, `agent_type`, `execution_steps`
4. **Verify** plan validates against schema:
   - Run: `config/hop_framework/execution_plan_schema.json` validation
5. **Verify** all prompt modules exist:
   - For each step, check `prompts/{prompt_module}` exists
   - Expected modules: `titulo_generator_REFINED.md`, `keywords_expander_HOP.md`, etc.

### Phase 2: Research Notes Ingestion (Steps 6-10)

6. Load research notes from test file
7. **Verify** research_notes contains 22 blocks:
   - [LACUNAS_DO_BRIEF]
   - [HEAD_TERMS_PRIORITARIOS]
   - [LONGTAILS]
   - ... (all 22 blocks)
8. **Verify** confidence_score extracted and ≥0.60
9. Parse Strategic Brief:
   - **Verify** top 3 head_terms extracted
   - **Verify** top 3 diferenciais extracted
   - **Verify** top 3 dores extracted
   - **Verify** top 3 ganhos extracted
10. **Verify** marketplace rules loaded for specified marketplace

### Phase 3: Sequential Step Execution (Steps 11-55)

#### STEP 1: Parse Input Research
11. Execute step_1: `input_parser.md`
12. **Verify** input mapping successful:
    - `research_notes_path` → research content
    - `marketplace` → compliance rules
13. **Verify** outputs generated:
    - [IDENTIDADE_DO_PRODUTO] block populated
    - [PROPOSTA_DE_VALOR] block populated
14. **Verify** export variables created:
    - `head_terms` (array[string])
    - `diferenciais` (array[object])
    - `dores` (array[string])
    - `ganhos` (array[string])
15. **Verify** quality gate PASS:
    - completeness_threshold ≥75%

#### STEP 2: Generate Titles
16. Execute step_2: `titulo_generator_REFINED.md`
17. **Verify** inputs mapped from step_1:
    - `head_terms` received
    - `diferenciais` received
18. **Verify** 3 títulos generated
19. **Verify** each título is 58-60 chars
20. **Verify** [BLOCOS_DE_TITULOS] block populated
21. **Verify** export: `titulos_list` (array[3])
22. **Verify** quality gate PASS:
    - 3 titles, correct length range

#### STEP 3: Expand Keywords
23. Execute step_3: `keywords_expander_HOP.md`
24. **Verify** inputs mapped:
    - `head_terms` from step_1
    - `titulos_list` from step_2
25. **Verify** [BLOCO_PALAVRAS_1] generated (115-120 keywords)
26. **Verify** [BLOCO_PALAVRAS_2] generated (115-120 keywords)
27. **Verify** no duplicates between blocks
28. **Verify** export: `keywords_blocks` (array[2])
29. **Verify** quality gate PASS:
    - 2 blocks, 115-120 each

#### STEP 4: Generate Bullet Points
30. Execute step_4: `bullet_points_estrategicos_HOP.md`
31. **Verify** inputs mapped:
    - `diferenciais`, `dores`, `ganhos` from step_1
32. **Verify** 10 bullet points generated
33. **Verify** each bullet is 250-299 chars
34. **Verify** [BULLET_POINTS_ESTRATEGICOS] populated
35. **Verify** mental triggers applied
36. **Verify** quality gate PASS

#### STEP 5: Build Long Description
37. Execute step_5: `descricao_builder_HOP.md`
38. **Verify** inputs mapped:
    - `bullets_list` from step_4
    - `keywords_blocks` from step_3
    - `dores`, `ganhos` from step_1
39. **Verify** [DESCRICAO_LONGA] generated
40. **Verify** description ≥3,300 chars
41. **Verify** StoryBrand framework applied
42. **Verify** 12 blocks present in description
43. **Verify** quality gate PASS

#### STEPS 6-8: Parallel Execution
44. Execute parallel steps:
    - step_6: `image_prompts_generator_HOP.md`
    - step_7: `video_script_veo3_HOP.md`
    - step_8: `seo_metadata.md`
45. **Verify** all 3 execute concurrently
46. **Verify** step_6 outputs 9 image prompts
47. **Verify** step_7 outputs video script (6-9 scenes)
48. **Verify** step_8 outputs SEO metadata JSON
49. **Verify** all parallel steps complete before step_9

#### STEP 9: Generate Variations
50. Execute step_9: `variacoes_s5.md`
51. **Verify** 3 variations generated:
    - Variação A: Equilibrada
    - Variação B: Emocional
    - Variação C: Técnica
52. **Verify** [VARIACOES_S5] populated

#### STEP 10: QA Validation
53. Execute step_10: `qa_validation_HOP.md`
54. **Verify** compliance check runs:
    - Zero HTML tags detected
    - Zero emojis detected
    - Zero prohibited claims
55. **Verify** [AUDITORIA_QA] populated with scores:
    - compliance_score: 100
    - persuasion_score ≥0.75
    - quality_score ≥90

### Phase 4: Output Assembly (Steps 56-65)

56. Execute step_11: `output_assembly.md`
57. **Verify** all outputs consolidated:
    - Count populated blocks (should be ≥9)
58. **Verify** required blocks present:
    - IDENTIDADE_DO_PRODUTO ✓
    - PROPOSTA_DE_VALOR ✓
    - BLOCOS_DE_TITULOS ✓
    - BLOCO_PALAVRAS_1 ✓
    - BLOCO_PALAVRAS_2 ✓
    - BULLET_POINTS_ESTRATEGICOS ✓
    - DESCRICAO_LONGA ✓
    - VARIACOES_S5 ✓
    - AUDITORIA_QA ✓
59. **Verify** execution metadata added:
    - execution_plan: "full_anuncio"
    - plan_version: "1.0.0"
    - execution_date (ISO8601)
    - duration_minutes (numeric)
    - quality_score (0-100)
    - compliance_score (0-100)
    - steps_executed: 11/11
    - steps_failed: 0
60. **Verify** research utilization calculated:
    - overall_utilization ≥90%
61. **Verify** final quality thresholds met:
    - completeness ≥90%
    - compliance_score = 100
62. **Verify** output file written:
    - Path: `USER_DOCS/produtos/anuncio_test_produto_{timestamp}.md`
    - File exists and is readable
63. **Verify** output follows `anuncio_output.md` schema
64. **Verify** [NOTAS_DE_FALLBACK] contains warnings if any
65. **Verify** execution time ≤15 minutes

### Phase 5: Validation Mode Testing (Steps 66-70)

#### Test: Flexible Mode (Default)
66. Re-run with `validation_mode=flexible`
67. Introduce minor quality gate failure (e.g., 89% completeness)
68. **Verify** execution continues (does not abort)
69. **Verify** warning logged in [NOTAS_DE_FALLBACK]
70. **Verify** output still generated with quality score < 100

#### Test: Strict Mode
71. Re-run with `validation_mode=strict`
72. Introduce same quality gate failure
73. **Verify** execution aborts immediately
74. **Verify** error message returned
75. **Verify** no output file written

### Phase 6: Error Handling (Steps 76-80)

76. Test missing prompt module:
    - Remove one prompt module temporarily
    - **Verify** pre-flight check fails
    - **Verify** error message indicates missing module
77. Test low research confidence:
    - Set confidence_score = 0.55 (below threshold)
    - **Verify** warning displayed
    - **Verify** can proceed with `force=true`
78. Test timeout handling:
    - Simulate step timeout (if possible)
    - **Verify** graceful handling per `error_handling` policy
79. Test compliance violation:
    - Inject prohibited claim in research
    - **Verify** QA validation detects it
    - **Verify** compliance_score < 100
80. Test plan schema violation:
    - Load invalid plan JSON
    - **Verify** schema validation fails
    - **Verify** clear error message

## Success Criteria

### Functional Requirements
- ✅ All 11 steps execute successfully
- ✅ All required blocks populated
- ✅ Quality gates applied correctly
- ✅ Parallel execution works (steps 6-8)
- ✅ Output file written to correct path
- ✅ Execution metadata accurate

### Quality Requirements
- ✅ Quality score ≥90 (flexible mode)
- ✅ Compliance score = 100 (zero violations)
- ✅ Research utilization ≥90%
- ✅ Execution time ≤15 minutes
- ✅ All titles 58-60 chars
- ✅ All bullets 250-299 chars
- ✅ Description ≥3,300 chars

### Validation Requirements
- ✅ Flexible mode generates warnings, continues
- ✅ Strict mode aborts on failures
- ✅ Error handling graceful
- ✅ Missing modules detected pre-flight
- ✅ Low confidence warnings shown

### Output Requirements
- ✅ Output follows schema exactly
- ✅ All blocks properly formatted
- ✅ Metadata complete and accurate
- ✅ Warnings logged in NOTAS_DE_FALLBACK
- ✅ File path follows naming convention

## Performance Benchmarks

- **Full workflow**: ≤15 minutes
- **Per-step average**: ≤90 seconds
- **Parallel steps**: Complete within 3 minutes (vs 6+ sequential)
- **Memory usage**: Reasonable (context_strategy=minimal)

## Test Data

### Sample research_notes.md
```markdown
# research_test_produto

## VERSAO_SCHEMA: 1.1

[... 22 blocos estruturados ...]

## CONFIDENCE_SCORE
0.87

## HEAD_TERMS
- fone bluetooth
- headphone sem fio
- fone ANC
```

### Sample marketplace
```
marketplace: "mercadolivre"
```

## Expected Output Structure

```markdown
# anuncio_test_produto_20251110

## VERSAO_SCHEMA: 1.1

[... all blocks populated ...]

## EXECUTION_METADATA
execution_plan: full_anuncio.json
plan_version: 1.0.0
execution_date: 2025-11-10T...
duration_minutes: 12.3
quality_score: 98/100
compliance_score: 100/100
persuasion_score: 0.89

steps_executed: 11/11
steps_skipped: 0
steps_failed: 0

research_utilization: 94%
```

## Regression Testing

Run this E2E test on every:
- HOP framework update
- Execution plan schema change
- New prompt module addition
- Quality gate threshold adjustment
- Marketplace rules update

## Notes

- This test validates the **entire HOP orchestration system**
- Tests both happy path and error scenarios
- Validates quality gates, compliance, and metadata
- Ensures production readiness of generated ads

**Test ID**: E2E_HOP_ANUNCIO_001
**Version**: 1.0.0
**Last Updated**: 2025-11-10
**Estimated Duration**: 20-25 minutes (including all phases)
