# 101_ADW_{{SOURCE}}_BRIDGE

**ID**: 101_ADW_{{SOURCE}}_BRIDGE
**Version**: 1.0.0
**Type**: ADW (Bridge Workflow)
**Chain**: {{SOURCE}}_agent → {{TARGET}}_agent

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_{{source_lower}}_bridge",
  "workflow_name": "{{source_title}} to {{target_title}} Bridge",
  "agent": "{{target_agent}}",
  "version": "1.0.0",
  "type": "bridge",
  "chain": "{{source_agent}} → {{target_agent}}",
  "context_strategy": "isolated",
  "failure_handling": "stop_and_report",
  "min_llm_model": "claude-sonnet-4-20250514",
  "required_capabilities": {{REQUIRED_CAPABILITIES}},
  "quality_threshold": 7.0,
  "estimated_duration": "2-3 minutes",
  "phases": ["LOCATE", "EXTRACT", "VALIDATE", "HANDOFF"]
}
```

---

## PURPOSE

Bridges {{source}} output from `{{source_agent}}` to `{{target_agent}}` input.

**Key Insight**: {{TRANSFORMATION_INSIGHT}}

---

## INPUT_CONTRACT

From `{{source_agent}}`:
- `${{source_lowercase}}_file`: Path to {{source}} output ({{SOURCE_PATH_PATTERN}})

Expected {{source}} data:
```{{SOURCE_DATA_FORMAT}}
{{SOURCE_DATA_STRUCTURE}}
```

---

## PHASES

### Phase 1: LOCATE (30s)

**Objective**: Discover {{source}} outputs for target {{source_lowercase}}.

```bash
# Using Scout
mcp__scout__discover("{{source_lowercase}} output for [product/content_name]")

# OR direct glob
Glob: {{SOURCE_PATH_PATTERN}}
```

**Output**: `${{source}}_paths` (list of matching files)

**Validation**:
- [ ] At least 1 file found
- [ ] File is readable (format: {{SOURCE_DATA_FORMAT}})
- [ ] File size ≥{{MIN_FILE_SIZE}}
- [ ] Contains required fields: {{REQUIRED_SOURCE_FIELDS}}

**Error Handling**:
- If no files found → HALT: "No {{source}} found for [target]. Run {{source_agent}} first or specify file path."
- If multiple files → SELECT: Most recent (by timestamp) or prompt user

---

### Phase 2: EXTRACT (1min)

**Objective**: Parse {{source}} and transform to {{target}} production context.

#### 2.1: Extract Core Data

**Extraction Mapping**:
```
{{SOURCE_FIELD}} → {{TARGET_FIELD}}
{{MAPPING_RULES}}
```

#### 2.2: Transform Context

**Translation Logic**:

| {{Source}} Element | {{Target}} Element | Transformation |
|-------------------|-------------------|----------------|
{{TRANSFORMATION_TABLE}}

#### 2.3: Add Production Hints

{{ADDITIONAL_EXTRACTION_LOGIC}}

**Output**: `${{target}}_context` (structured JSON with all required fields)

**Quality Gate**:
- [ ] All core fields extracted
- [ ] {{FIELD_1}} has required content ({{VALIDATION_RULE_1}})
- [ ] {{FIELD_2}} defined ({{VALIDATION_RULE_2}})
- [ ] {{FIELD_3}} complete ({{VALIDATION_RULE_3}})
- [ ] Transformation rules applied correctly

---

### Phase 3: VALIDATE (30s)

**Objective**: Ensure {{target}} specs meet production requirements.

**Validation Checklist**:

1. **Structural Validation**
   - [ ] {{STRUCTURAL_CHECK_1}}
   - [ ] {{STRUCTURAL_CHECK_2}}
   - [ ] {{STRUCTURAL_CHECK_3}}

2. **Content Validation**
   - [ ] {{CONTENT_CHECK_1}}
   - [ ] {{CONTENT_CHECK_2}}
   - [ ] {{CONTENT_CHECK_3}}

3. **Brand/Format Validation**
   - [ ] {{BRAND_CHECK_1}}
   - [ ] {{BRAND_CHECK_2}}

4. **Production Feasibility**
   - [ ] {{FEASIBILITY_CHECK_1}}
   - [ ] {{FEASIBILITY_CHECK_2}}

**Scoring**:
```
Pass all checks → quality_score = 10.0
Fail 1-2 checks → quality_score = 8.0 (acceptable)
Fail 3+ checks → quality_score = 6.0 (needs revision)
```

**Quality Gate**: quality_score ≥7.0 to proceed

**Output**: `$validation_result` (pass/fail + score with detailed report)

**Error Handling**:
- If quality_score <7.0 → RETRY: "Quality too low ([X]/10). Missing: [list deficiencies]"
- If {{CRITICAL_FIELD}} missing → HALT: "{{HALT_MESSAGE}}"
- If {{WARNING_CONDITION}} → WARN: "{{WARNING_MESSAGE}}"

---

### Phase 4: HANDOFF (30s)

**Objective**: Prepare structured context for {{target_agent}} ingestion.

**Handoff Format**:

```handoff
contexto: {{source}} complete for [{{source_lowercase}}_name]
arquivos_gerados:
  - {{OUTPUT_FILE_PATH}}/[{{source_lowercase}}]_{{source_lowercase}}.{{OUTPUT_FORMAT}}
proximo: Run {{target_agent}} with {{source}} context
dados:
  {{HANDOFF_FIELD_1}}: ${{target}}_context.{{FIELD_MAPPING_1}}
  {{HANDOFF_FIELD_2}}: ${{target}}_context.{{FIELD_MAPPING_2}}
  {{HANDOFF_FIELD_3}}: ${{target}}_context.{{FIELD_MAPPING_3}}
  {{HANDOFF_ADDITIONAL_FIELDS}}
qualidade: $validation_result.score/10
```

**Handoff Block Structure**:

```json
{
  "handoff": {
    "from_agent": "{{source_agent}}",
    "to_agent": "{{target_agent}}",
    "timestamp": "{{TIMESTAMP}}",
    "{{source_lowercase}}_source": "{{BRIDGE_INPUT_PATH}}"
  },
  "{{target}}_context": {
    {{HANDOFF_JSON_STRUCTURE}}
  },
  "metadata": {
    "total_{{UNIT}}": {{TOTAL_COUNT}},
    "language": "pt-BR",
    "quality_score": {{QUALITY_SCORE}}
  }
}
```

**Output**:
- `$handoff_block`: Formatted markdown context (ready to paste into {{target_agent}})
- `${{target}}_context_file`: Absolute path to saved context file
- `$bridge_log`: JSON log entry

**Quality Gate**:
- [ ] Handoff block ≥500 chars
- [ ] Context file saved successfully
- [ ] All required sections present ({{HANDOFF_SECTIONS}})

---

## OUTPUT_CONTRACT

### For {{target_agent}}

**Delivered**:

1. **{{target}}_context.json** (machine-readable)
   - Structured JSON with all extracted data
   - Ready for {{target_agent}} builders to parse

2. **[{{source_lowercase}}]_{{target}}_context.md** (human-readable)
   - Formatted markdown handoff block
   - LLM-optimized for prompt injection

3. **bridge_log.json** (audit trail)
   - Bridge execution details
   - Quality score and validation results

---

## TRIGGERS

### Manual

```bash
/flow do "bridge {{source_lowercase}} to {{target_lowercase}} for [{{source_lowercase}}_name]"
```

### Automatic

Triggered when:
1. {{source_agent}} completes {{SOURCE_COMPLETION_FILE}}
2. File detected in {{SOURCE_WATCH_PATH}}
3. File age <1 hour (recent)

### Via Spawn

```bash
/spawn
1. explore: find {{source_lowercase}} output for [{{source_lowercase}}_name]
2. review: validate {{source_lowercase}} quality
3. build: execute 101_ADW_{{SOURCE}}_BRIDGE
```

---

## EXAMPLE

### Input ({{source}} output excerpt)

```{{SOURCE_DATA_FORMAT}}
{{EXAMPLE_SOURCE_DATA}}
```

### Output ({{target}} context)

```json
{{EXAMPLE_TARGET_CONTEXT}}
```

### Generated Handoff

```handoff
{{EXAMPLE_HANDOFF_BLOCK}}
```

---

## INTEGRATION

### With /flow

```bash
/flow plan "create {{target_lowercase}} with {{source_lowercase}} for [{{source_lowercase}}_name]"
# Automatically includes bridge phase
```

### With /spawn

```bash
/spawn
1. build: {{source_lowercase}} for [{{source_lowercase}}_name]
2. build: bridge {{source_lowercase}}→{{target_lowercase}}
3. build: {{target_lowercase}} with context
```

### With {{target_agent}} Production

```bash
# Direct context injection
python codexa.app/agentes/{{target_agent}}/src/{{target_agent}}.py \
  --context {{target}}_bridge/[{{source_lowercase}}]_{{target}}_context.md \
  --workflow 100_ADW_RUN_{{TARGET_UPPERCASE}}
```

---

## VALIDATION

### Quality Gate Checklist

**Phase 1: Locate**
- [ ] {{source}} file found
- [ ] File readable and valid {{SOURCE_DATA_FORMAT}}
- [ ] File size ≥{{MIN_FILE_SIZE}}
- [ ] Contains required sections: {{REQUIRED_SOURCE_SECTIONS}}

**Phase 2: Extract**
- [ ] All core fields parsed (count ≥{{MIN_EXTRACTED_FIELDS}})
- [ ] Transformation rules applied successfully
- [ ] All {{TARGET}} elements defined
- [ ] {{ADDITIONAL_CHECKS}}

**Phase 3: Validate**
- [ ] Structural checks passed (≥{{MIN_PASSING_CHECKS}}/{{TOTAL_CHECKS}})
- [ ] Quality score ≥7.0
- [ ] No blocking issues
- [ ] Production feasibility confirmed

**Phase 4: Handoff**
- [ ] Handoff block generated (≥500 chars)
- [ ] Context file saved successfully
- [ ] Bridge log created
- [ ] Ready for {{target_agent}} ingestion

**Overall Success Criteria**:
- [ ] All 4 phases completed
- [ ] Quality score ≥7.0
- [ ] {{Target}} context file saved
- [ ] No errors logged

---

## ERROR HANDLING

### Phase 1 Errors

**Error**: {{source}} file not found
**Cause**: {{source_agent}} hasn't generated output yet, or wrong path
**Action**:
1. Search recursively in {{source_agent}}/outputs/
2. If not found, return error: "No {{source}} found. Run {{source_agent}} workflow first."

**Error**: File unreadable or corrupt
**Cause**: Incomplete generation or encoding issue
**Action**:
1. Check file size (must be >{{MIN_FILE_SIZE}})
2. Try UTF-8 decoding
3. If fails, return error with file path for manual inspection

---

### Phase 2 Errors

**Error**: Required fields missing
**Cause**: Unexpected {{source}} format or incomplete generation
**Action**:
1. Search for alternative field names
2. If not found, use fallback extraction
3. Log warning: "Missing optional fields, using defaults"

**Error**: Transformation mapping failed
**Cause**: Unexpected data format or incompatible types
**Action**:
1. Attempt manual type conversion
2. Use placeholder values for missing fields
3. Flag for manual review

---

### Phase 3 Errors

**Error**: Quality score <7.0
**Cause**: Missing data or invalid structure
**Action**:
1. List all failed checks
2. Provide recommendations for fixes
3. Allow manual override with `--force` flag
4. Log warning: "Low quality score, review recommended"

---

### Phase 4 Errors

**Error**: Context file save failed
**Cause**: Permission issue or disk full
**Action**:
1. Check write permissions on {{target_agent}}/context/
2. Create directory if missing
3. Retry save
4. If still fails, return context in stdout instead

---

## CONFIGURATION

### File Paths

```json
{
  "input_paths": {
    "{{source}}_outputs": "codexa.app/agentes/{{source_agent}}/outputs/",
    "{{source}}_pattern": "{{SOURCE_FILENAME_PATTERN}}"
  },
  "output_paths": {
    "{{target}}_context": "codexa.app/agentes/{{target_agent}}/context/{{source_lower}}_bridge/",
    "bridge_logs": "codexa.app/agentes/{{target_agent}}/logs/bridges/"
  }
}
```

### Mapping Rules

```json
{
  {{MAPPING_CONFIG}}
}
```

---

## KEY PRINCIPLES

### Isolation Strategy
- Bridge operates in isolated context (no global state pollution)
- Each phase produces intermediate JSON for resumability
- Failure in any phase logs detailed diagnostics

### Quality Assurance
- Quality gate ≥7.0 prevents propagation of degraded data
- All validation checks must pass before handoff
- Retry logic for recoverable errors (Phase 2/3)
- Halt + manual review for unrecoverable errors (Phase 1)

### Handoff Format
- Standardized structure across all bridges
- Human-readable markdown for team visibility
- Machine-readable JSON for automated ingestion
- Includes source provenance and quality metrics

### Data Transformation
- Explicit mapping rules (no magic)
- Lossy transformation acceptable (document what's dropped)
- Additive enrichment (bridge adds production hints)
- Traceability (original source always accessible)

---

## NOTES

**Why Bridges Matter**:
- **Consistency**: {{source}} outputs are optimized for {{source_agent}} format; bridges translate to {{target_agent}} requirements
- **Quality Control**: Validation gate prevents garbage-in/garbage-out
- **Composability**: Agent chains work reliably because bridges guarantee contract compliance
- **Auditability**: Bridge logs provide full traceability from source through production

**Common Pitfalls**:
- Skipping validation (leads to cascading failures downstream)
- Over-transforming (losing nuance from source)
- Under-documenting transformations (team confusion)
- Ignoring edge cases (brittle on unusual inputs)

**Best Practices**:
- Always validate before handoff (never skip Phase 3)
- Document transformation rationale (not just the mapping)
- Test with real data from source agent
- Version mapping rules (changes need review)
- Log all failures with context

---

## RELATED WORKFLOWS

- **{{source_agent}}/workflows/100_ADW_RUN_{{SOURCE_UPPERCASE}}.md** - Produces input for this bridge
- **{{target_agent}}/workflows/100_ADW_RUN_{{TARGET_UPPERCASE}}.md** - Consumes output from this bridge
- **{{source_agent}}/prompts/10_*_HOP.md** - Context for {{source}} generation
- **{{target_agent}}/prompts/10_*_HOP.md** - Uses context from this bridge

---

**Type**: Bridge Workflow Template ({{source_agent}} → {{target_agent}})
**Maintainer**: CODEXA Meta-Constructor
**Template Version**: 1.0.0
**Created**: 2025-12-04

---

## IMPLEMENTATION GUIDE

To create a new bridge from this template:

1. **Define Variables**:
   - {{SOURCE}} = source agent name (e.g., "PESQUISA")
   - {{TARGET}} = target agent name (e.g., "ANUNCIO")
   - {{source_agent}} = source agent slug (e.g., "pesquisa_agent")
   - {{target_agent}} = target agent slug (e.g., "anuncio_agent")

2. **Fill Transformation Table**: Map source fields → target fields with transformation logic

3. **Define Extraction Logic**: Implement Phase 2 transformation rules specific to your bridge

4. **Define Validation Checklist**: Create quality checks specific to {{target}} requirements

5. **Complete Example Section**: Provide real input/output example

6. **Test Bridge**: Execute all 4 phases with sample data, verify quality_score ≥7.0

7. **Document Integration**: Show how bridge fits into agent workflow orchestration

---

**Reference Implementations**:
- `codexa.app/agentes/anuncio_agent/workflows/101_ADW_PESQUISA_BRIDGE.md`
- `codexa.app/agentes/photo_agent/workflows/101_ADW_ANUNCIO_BRIDGE.md`
- `codexa.app/agentes/video_agent/workflows/101_ADW_CURSO_BRIDGE.md`
- `codexa.app/agentes/voice_agent/workflows/101_ADW_VIDEO_BRIDGE.md`
