# Trinity Output Module | Shared Pattern Library

**Version**: 1.0.0 | **Type**: Reusable Module | **Status**: Production-Ready
**Created**: 2025-12-04 | **Maintainer**: CODEXA Meta-Constructor
**Pattern Source**: Analyzed from anuncio_agent, photo_agent, pesquisa_agent workflows

---

## PURPOSE

This module defines the **Trinity Output Pattern** - a standardized format for multi-phase ADW (Agentic Developer Workflow) completions that output three complementary file formats:

1. **`.md` (Markdown)** - Human-readable, comprehensive documentation
2. **`.llm.json` (Structured Data)** - Machine-readable, LLM-optimized schema
3. **`.meta.json` (Workflow Metadata)** - Execution tracking and quality metrics

**Use Case**: Any ADW workflow that needs to package outputs for human review, programmatic access, and audit trails.

---

## TRINITY STRUCTURE OVERVIEW

### Trinity = 3 Files with Clear Separation of Concerns

| File | Purpose | Audience | Format | Size |
|------|---------|----------|--------|------|
| **`{name}.md`** | Full content + context + narrative | Humans | Markdown | 10-100 KB |
| **`{name}.llm.json`** | Structured data arrays, objects, metrics | LLMs, APIs | JSON | 5-50 KB |
| **`{name}.meta.json`** | Workflow execution metadata | Monitoring, Auditing | JSON | 2-10 KB |

### Naming Convention

```
{product_name}_{output_type}.md              # e.g., product_ad_copy.md
{product_name}_{output_type}.llm.json        # e.g., product_ad_copy.llm.json
{product_name}_{output_type}.meta.json       # e.g., product_ad_copy.meta.json
```

**Valid output_type values**:
- `ad_copy` (anuncio_agent)
- `photo_prompts` (photo_agent)
- `research_notes` (pesquisa_agent)
- `brand_strategy` (marca_agent)
- `video_script` (video_agent)

---

## FILE 1: MARKDOWN (.md) - HUMAN-READABLE

### Purpose
Comprehensive, narrative-driven output optimized for human review, editing, and sharing.

### Standard Structure

```markdown
# [Product Name] - [Output Type] Package

**Generated**: [ISO 8601 timestamp]
**Marketplace**: [if applicable]
**Product Type**: [if applicable]
**Quality Score**: [X.XX]/1.00

---

## SECTION 1: Primary Content

[Main deliverable - specific to output type]

**Metrics**:
- Metric 1: [value]
- Metric 2: [value]
- Metric 3: [value]

---

## SECTION 2: Secondary Content

[Supporting deliverable]

---

## SECTION 3: Variants / Alternatives

[2-3 variations for testing/comparison]

### Variant A: [Strategy]
[content]

### Variant B: [Strategy]
[content]

---

## QUALITY REPORT

**Aggregate Score**: [X.XX]/1.00

**Breakdown**:
- Component 1: [X.XX]/1.00
- Component 2: [X.XX]/1.00
- Component 3: [X.XX]/1.00
- Component 4: [X.XX]/1.00

**Issues Found**: [X]
- [List if any]

**Improvement Suggestions**: [X]
- [List if score <0.95]

---

## METADATA

- Product: [name]
- Type: [category]
- Compliance: [ANVISA|INMETRO|Anatel|NONE]
- Quality Score: [X.XX]/1.00
- Total Execution Time: [XX]min
- Phases Completed: [X/X]
```

### Markdown Formatting Rules

1. **Headers**: H1 (#) for title, H2 (##) for sections, H3 (###) for subsections
2. **Code blocks**: Use triple backticks with language hint (```json, ```markdown)
3. **Tables**: Use pipe delimiters (|) for structured data
4. **Lists**: Use `-` for unordered, `1.` for ordered
5. **Emphasis**: Use **bold** for highlights, *italic* for context
6. **Line breaks**: Use `---` for visual separation between major sections

### Content Guidelines

- **Readability first**: Assume reader has limited context
- **Examples included**: Provide concrete examples for each section
- **Self-contained**: Don't reference external files (embed data in .md)
- **Editable format**: Use plain text (not HTML), markdown-compatible
- **Version control friendly**: Works well with git diffs

---

## FILE 2: JSON STRUCTURED DATA (.llm.json)

### Purpose
Structured, machine-readable schema optimized for programmatic access and LLM processing.

### JSON Schema Template

```json
{
  "metadata": {
    "workflow_id": "adw_run_{agent}_{timestamp}",
    "agent": "anuncio_agent|photo_agent|pesquisa_agent|...",
    "output_type": "ad_copy|photo_prompts|research_notes|...",
    "version": "1.0.0",
    "generated_at": "2025-11-17T14:30:45Z"
  },

  "context": {
    "product_name": "string",
    "product_type": "B2B_SAAS|PHYSICAL_PRODUCT|SERVICE",
    "marketplace_type": "GITHUB|MERCADO_LIVRE|SHOPEE|TIKTOK_SHOP",
    "target_audience": "string",
    "compliance_requirements": ["ANVISA", "INMETRO"] | []
  },

  "content": {
    "primary": {
      "type": "string (matches section type)",
      "value": "string|object|array",
      "metrics": {
        "metric_1": "value",
        "metric_2": "value"
      }
    },
    "secondary": {
      "type": "string",
      "value": "string|object|array"
    },
    "variants": [
      {
        "name": "Variant A",
        "strategy": "string",
        "content": "string|object"
      },
      {
        "name": "Variant B",
        "strategy": "string",
        "content": "string|object"
      }
    ]
  },

  "quality": {
    "aggregate_score": 0.XX,
    "component_scores": {
      "component_1": 0.XX,
      "component_2": 0.XX,
      "component_3": 0.XX,
      "component_4": 0.XX
    },
    "validation_checks": {
      "check_1": {"status": "passed|failed|warning", "details": "string"},
      "check_2": {"status": "passed|failed|warning", "details": "string"}
    },
    "issues": [
      {"severity": "critical|important|minor", "issue": "string", "suggestion": "string"}
    ],
    "improvements": [
      "improvement_1",
      "improvement_2"
    ]
  },

  "execution": {
    "duration_minutes": 15,
    "phases_completed": 5,
    "phases_total": 5,
    "phase_breakdown": {
      "phase_1": {"name": "Phase Name", "duration_min": X, "status": "completed"},
      "phase_2": {"name": "Phase Name", "duration_min": X, "status": "completed"}
    }
  }
}
```

### JSON Formatting Rules

1. **Data Types**: Use strict JSON types (string, number, boolean, null, array, object)
2. **Timestamps**: ISO 8601 format (2025-11-17T14:30:45Z)
3. **Scores**: 0.00-1.00 range (not percentages)
4. **Null handling**: Use `null` for missing values (not empty strings)
5. **Nesting**: Maximum 4 levels (for readability)
6. **Arrays**: Use for lists of similar items (not mixed types)
7. **Field naming**: camelCase (not snake_case or kebab-case)

### JSON Validation

```bash
# Validate JSON syntax
jq empty {file}.llm.json

# Pretty-print for review
jq . {file}.llm.json

# Extract specific field
jq '.quality.aggregate_score' {file}.llm.json
```

---

## FILE 3: METADATA (.meta.json)

### Purpose
Lightweight metadata about workflow execution, used for monitoring, auditing, and chaining workflows.

### Meta JSON Schema

```json
{
  "workflow_version": "1.0.0",
  "generator": "CODEXA ADW Intelligent Constructor v1.0.0",
  "generator_agent": "anuncio_agent|photo_agent|pesquisa_agent",
  "generated_at": "2025-11-17T14:30:45Z",
  "execution_id": "adw_run_{agent}_{timestamp}",

  "input": {
    "user_data": {
      "product_name": "string",
      "brief_completeness": 0.85,
      "required_fields_present": true
    }
  },

  "execution": {
    "phases_executed": 7,
    "phases_total": 7,
    "total_duration_minutes": 24,
    "start_time": "2025-11-17T14:06:45Z",
    "end_time": "2025-11-17T14:30:45Z",

    "phase_breakdown": [
      {
        "phase_id": "phase_0",
        "phase_name": "Knowledge Loading",
        "duration_minutes": 2,
        "status": "completed",
        "checkpoint": "knowledge_context loaded"
      },
      {
        "phase_id": "phase_1",
        "phase_name": "Input Validation",
        "duration_minutes": 3,
        "status": "completed",
        "checkpoint": "strategic_brief created"
      }
    ]
  },

  "quality": {
    "research_quality": 0.85,
    "final_output_quality": 0.92,
    "validation_checks_passed": 11,
    "validation_checks_total": 11,
    "completeness_percent": 100,
    "confidence_level": "HIGH"
  },

  "output": {
    "files_generated": ["ad_copy.md", "ad_copy.llm.json", "ad_copy.meta.json"],
    "file_sizes_bytes": {"ad_copy.md": 45000, "ad_copy.llm.json": 22000, "ad_copy.meta.json": 5000},
    "output_location": "USER_DOCS/anuncios/product_name/",
    "ready_for_use": true
  },

  "context": {
    "product_type": "B2B_SAAS",
    "marketplace_type": "GITHUB",
    "compliance": {
      "requirements": [],
      "validated": true,
      "risks": []
    }
  },

  "chain_info": {
    "source_workflow": "pesquisa_agent",
    "source_output": "research_notes.md",
    "next_recommended_workflow": "anuncio_agent",
    "can_chain_forward": true
  }
}
```

### Meta JSON Guidelines

1. **Lightweight**: Keep under 10 KB (summary only)
2. **Execution tracking**: Focus on timing, status, checkpoints
3. **Quality snapshot**: Summary metrics (not detailed scores)
4. **Chaining support**: Include info for workflow handoff
5. **Auditability**: Track execution ID, timestamps, user input

---

## ASSEMBLY INSTRUCTIONS

### Step 1: Prepare Phase Outputs

Before assembly, ensure all ADW phases have completed and produced outputs:

```
Phase 1 → $output_1
Phase 2 → $output_2
Phase 3 → $output_3
...
Phase N → $output_N
```

### Step 2: Generate .md File

**Process**:

1. Start with `.md` template above
2. Fill in metadata (product, type, timestamp, quality score)
3. Populate sections with phase outputs
4. Add metrics and breakdowns
5. Include variants (if generated)
6. Add QA report with validation results

**Tips**:
- Use code blocks for structured data (JSON, arrays)
- Include examples within the text
- Make it self-contained (don't rely on .json files)
- Use headers to organize content

**Validation**:
```bash
# Check markdown syntax
mdl {file}.md

# Count headers (should have structure)
grep "^#" {file}.md | wc -l

# Verify no broken links
grep "^\[" {file}.md
```

### Step 3: Generate .llm.json File

**Process**:

1. Start with `.llm.json` schema above
2. Extract structured data from phase outputs
3. Create arrays for lists (titles, keywords, variants)
4. Map phase outputs to content sections
5. Add quality scores and validation results
6. Ensure JSON is valid

**Tips**:
- Use arrays for repeated items (not nested objects with number keys)
- Normalize numeric values (use 0.XX, not percentages)
- Include both raw data and computed metrics
- Ensure all keys are in camelCase

**Validation**:
```bash
# Validate JSON structure
jq . {file}.llm.json > /dev/null && echo "Valid JSON"

# Check required fields
jq '.metadata, .context, .quality' {file}.llm.json

# Count items in arrays
jq '.content.variants | length' {file}.llm.json
```

### Step 4: Generate .meta.json File

**Process**:

1. Start with `.meta.json` schema above
2. Record execution timeline (start → end time)
3. Document all phases executed (with duration)
4. Add quality metrics (aggregate score, completeness %)
5. List output files generated
6. Note next recommended workflow

**Tips**:
- Keep execution times accurate (track during workflow)
- Calculate completeness as (sections_filled / total_sections) * 100
- Use ISO 8601 timestamps (2025-11-17T14:30:45Z)
- Include chaining info for multi-agent workflows

**Validation**:
```bash
# Validate JSON
jq . {file}.meta.json > /dev/null && echo "Valid JSON"

# Check required metadata fields
jq '.generator, .generated_at, .execution.total_duration_minutes' {file}.meta.json
```

### Step 5: File Organization

Save all three files in the same directory:

```
USER_DOCS/
├── anuncios/
│   └── product_name/
│       ├── product_name_ad_copy.md
│       ├── product_name_ad_copy.llm.json
│       └── product_name_ad_copy.meta.json
│
├── photos/
│   └── product_name/
│       ├── product_name_photo_prompts.md
│       ├── product_name_photo_prompts.llm.json
│       └── product_name_photo_prompts.meta.json
│
└── research/
    └── product_name/
        ├── product_name_research_notes.md
        ├── product_name_research_notes.llm.json
        └── product_name_research_notes.meta.json
```

---

## QUALITY VALIDATION CHECKLIST

### Pre-Assembly Validation

- [ ] All phase outputs generated successfully
- [ ] No phase failures or errors
- [ ] Execution times recorded for all phases
- [ ] Quality scores calculated for all components
- [ ] All validation checks documented

### .md File Validation

- [ ] File size: 10-100 KB (proportional to complexity)
- [ ] Header structure present (H1, H2, H3)
- [ ] All sections completed (no "TODO" placeholders)
- [ ] Code blocks formatted correctly (triple backticks)
- [ ] Metrics included with units
- [ ] QA report present with scores ≥0.70
- [ ] No external file references (self-contained)
- [ ] Markdown renders without errors (can preview in GitHub)

### .llm.json File Validation

- [ ] File size: 5-50 KB
- [ ] Valid JSON (parseable with jq or JSON validators)
- [ ] All metadata fields present
- [ ] Context fields accurately mapped
- [ ] Content structure matches output type
- [ ] All scores in 0.00-1.00 range
- [ ] Arrays used for lists (not object keys with numbers)
- [ ] No empty strings (use null for missing values)
- [ ] Can be parsed by LLMs without errors

### .meta.json File Validation

- [ ] File size: 2-10 KB
- [ ] Valid JSON (parseable)
- [ ] Timestamps in ISO 8601 format
- [ ] Phase breakdown includes all executed phases
- [ ] Total duration = sum of phase durations (±2min margin)
- [ ] Output files list matches actual generated files
- [ ] Quality scores present (research_quality, output_quality)
- [ ] Chain info populated (if multi-agent workflow)

### Content Quality Validation

- [ ] Aggregate quality score ≥0.70 (minimum threshold)
- [ ] Completeness ≥75% (sections filled / total sections)
- [ ] All validation checks passed (or documented failures)
- [ ] Compliance requirements met (if applicable)
- [ ] Marketplace-specific rules followed (if applicable)
- [ ] No superlatives without proof (marketplace compliance)
- [ ] All data in Brazilian Portuguese (if regional content)
- [ ] All URLs valid (if included)

### Cross-File Consistency Validation

- [ ] Product name matches across all three files
- [ ] Quality scores consistent (.md ≈ .llm.json aggregate)
- [ ] Execution time matches .meta.json
- [ ] Content sections in .md correspond to .llm.json structures
- [ ] Output location in .meta.json matches actual save path

---

## VALIDATION SCORING MATRIX

Use this matrix to assess trinity output quality:

| Metric | Excellent (0.90-1.00) | Good (0.75-0.89) | Acceptable (0.70-0.74) | Poor (<0.70) |
|--------|----------------------|------------------|------------------------|--------------|
| **Completeness** | 100% sections | 90-99% sections | 75-89% sections | <75% sections |
| **Structure** | All files perfect | 1 minor issue | 2-3 minor issues | Missing sections/files |
| **Content Quality** | All content ≥0.85 | Most content ≥0.80 | Some content ≥0.70 | Content <0.70 |
| **Marketplace Compliance** | 100% compliant | 1-2 warnings | 3-4 warnings | Multiple failures |
| **Validation Checks** | 100% passed | 95-99% passed | 85-94% passed | <85% passed |

**Overall Quality Score** = Average of 5 metrics above

---

## EXAMPLES BY OUTPUT TYPE

### Example 1: Anuncio (Ad Copy) Trinity

**Workflow**: 100_ADW_RUN_ANUNCIO
**Phases**: 8 (including knowledge loading)
**Duration**: 24-40 min

**.md Structure**:
- Titles (3 variations with scores)
- Keywords (4 semantic blocks)
- Description (main + metrics)
- Visual Assets (image prompts + video script)
- A/B Variants
- QA Report

**.llm.json Structure**:
```json
{
  "metadata": {"workflow_id": "...", "agent": "anuncio_agent"},
  "content": {
    "titles": [{"text": "...", "score": 0.92}],
    "keywords": {"block_a": {...}, "block_b": {...}},
    "description": {"text": "...", "word_count": 450},
    "visual_assets": {"image_prompts": [...], "video_script": "..."},
    "ab_variants": [...]
  },
  "quality": {"aggregate_score": 0.88, ...}
}
```

**.meta.json Structure**:
```json
{
  "generator_agent": "anuncio_agent",
  "execution": {
    "phases_executed": 8,
    "total_duration_minutes": 32,
    "phase_breakdown": [
      {"phase_id": "phase_0", "phase_name": "Knowledge Loading", ...},
      {"phase_id": "phase_1", "phase_name": "Input Validation", ...}
    ]
  }
}
```

### Example 2: Photo (Prompts) Trinity

**Workflow**: 100_ADW_RUN_PHOTO
**Phases**: 5 (including knowledge loading)
**Duration**: 15-30 min

**.md Structure**:
- 9-Scene Grid Overview (table)
- Individual Prompts (9 scenes with specs)
- Batch Block (all concatenated)
- QA Report

**.llm.json Structure**:
```json
{
  "content": {
    "scene_grid": {"rows": 3, "cols": 3},
    "prompts": [
      {"scene": 1, "subject": "...", "camera": {...}, "lighting": {...}},
      {"scene": 2, ...}
    ],
    "batch_block": "---Scene 1--- ... ---Scene 9---"
  }
}
```

**.meta.json Structure**:
```json
{
  "generator_agent": "photo_agent",
  "execution": {"phases_executed": 5, "total_duration_minutes": 18}
}
```

### Example 3: Pesquisa (Research) Trinity

**Workflow**: 100_ADW_RUN_PESQUISA
**Phases**: 9 (including knowledge loading)
**Duration**: 20-30 min

**.md Structure**:
- 22 Research Blocks (filled template)
- Executive Summary
- Opportunities & Recommendations
- QA Report

**.llm.json Structure**:
```json
{
  "content": {
    "research_blocks": [
      {"block_name": "HEAD TERMS", "content": "..."},
      {"block_name": "LONGTAILS", "content": "..."}
    ],
    "competitors": [{"name": "...", "price": "...", "rating": 4.5}],
    "queries_logged": 45
  }
}
```

**.meta.json Structure**:
```json
{
  "generator_agent": "pesquisa_agent",
  "execution": {"phases_executed": 9, "total_duration_minutes": 25},
  "output": {"files_generated": ["research_notes.md", "research_notes.llm.json", "research_notes.meta.json"]}
}
```

---

## COMMON ISSUES & FIXES

### Issue: .llm.json contains object keys with numbers

**Problem**: `{ "1": {...}, "2": {...} }` instead of `[{...}, {...}]`

**Fix**: Use arrays for lists of similar items
```json
// ❌ BAD
{"titles": {"1": "Title A", "2": "Title B"}}

// ✅ GOOD
{"titles": [{"order": 1, "text": "Title A"}, {"order": 2, "text": "Title B"}]}
```

### Issue: Quality score mismatch between .md and .llm.json

**Problem**: .md shows 0.92, .llm.json shows 0.85

**Fix**: Ensure both files use same calculation method
- Decide on single calculation formula
- Apply consistently before assembly
- Document formula in .meta.json

### Issue: .md file too large (>100 KB)

**Problem**: File size exceeds readable limit

**Fix**: Move detailed data to .llm.json, summarize in .md
- Keep .md to 10-50 KB
- Put raw data arrays in .llm.json
- Reference .llm.json for drill-down

### Issue: .meta.json timestamps don't match

**Problem**: generated_at ≠ actual generation time

**Fix**: Record timestamps during phase execution
- Set start_time at workflow beginning
- Set end_time at workflow completion
- Calculate duration programmatically

### Issue: Missing validation checks in .md

**Problem**: QA Report section incomplete

**Fix**: Complete all validation checks before assembly
- Document pass/fail for each check
- List specific issues found (if any)
- Suggest improvements if score <0.95

---

## INTEGRATION PATTERNS

### Pattern 1: Single-Agent Output (Linear ADW)

```
ADW Phases 1-N → Collect Outputs → Assemble Trinity → Save 3 Files
                                         ↓
                                    .md (human review)
                                    .llm.json (data access)
                                    .meta.json (audit trail)
```

### Pattern 2: Multi-Agent Chaining (Workflow → Workflow)

```
Pesquisa ADW (9 phases)
        ↓
    research_notes trinity
        ↓
  Pass to Anuncio ADW
        ↓
    ad_copy trinity
        ↓
  Pass to Photo ADW
        ↓
    photo_prompts trinity
```

**Chain Info in .meta.json**:
```json
{
  "chain_info": {
    "source_workflow": "pesquisa_agent",
    "source_output": "research_notes.md",
    "next_recommended_workflow": "anuncio_agent",
    "can_chain_forward": true
  }
}
```

### Pattern 3: Parallel Execution (Multiple Agents)

```
User Brief
    ↓
    ├─→ Pesquisa ADW (research) → research_notes trinity
    ├─→ Marca ADW (brand) → brand_strategy trinity
    └─→ Mentor ADW (guidance) → mentor_advice trinity
    ↓
    Consolidate all trinities into unified output
```

### Pattern 4: Reusable Module Access

```
ADW Phase X needs Trinity format
    ↓
Read this module (trinity_output.md)
    ↓
Use templates (schemas, checklists)
    ↓
Apply to specific ADW context
    ↓
Generate agent-specific trinity
```

---

## MAINTENANCE & VERSIONING

### Version History

- **v1.0.0** (2025-12-04): Initial module
  - Analyzed 3 ADW workflows (anuncio, photo, pesquisa)
  - Extracted common Trinity pattern
  - Created reusable schemas and guidelines
  - Documented assembly instructions
  - Provided validation checklist

### Future Enhancements

- [ ] **v1.1.0**: Add XML schema definitions (.xsd) for validation
- [ ] **v1.2.0**: Create automated Trinity validator (Python script)
- [ ] **v1.3.0**: Add Trinity comparison tool (diff between versions)
- [ ] **v2.0.0**: Support nested variants and parameterized templates

### Contributing

To update this module:

1. Document any new Trinity usage patterns
2. Add examples from new ADW workflows
3. Update validation checklist if needed
4. Test schemas with actual outputs
5. Submit PR with changelog entry

---

## REFERENCES

### Related Workflows

- `100_ADW_RUN_ANUNCIO.md` - Ad copy generation (8 phases)
- `100_ADW_RUN_PHOTO.md` - Photo prompts (5 phases)
- `100_ADW_RUN_PESQUISA.md` - Market research (9 phases)

### Related Modules

- `PHASE_0_KNOWLEDGE_LOADING.md` - Cross-agent knowledge prep
- `PRIME.md` - Agent instructions (in each agent)
- `README.md` - Agent structure (in each agent)

### External Tools

- **JSON Validation**: `jq` (JSON query tool)
- **Markdown Linting**: `mdl` (markdown linter)
- **Git**: Track Trinity output versions in version control

---

## QUICK START

### To Create a Trinity Output:

```bash
# 1. Complete all ADW phases (generate $output_1, $output_2, ..., $output_N)

# 2. Create .md file (human-readable)
# → Use template from "FILE 1: MARKDOWN" section
# → Fill with phase outputs and metrics

# 3. Create .llm.json file (structured data)
# → Use schema from "FILE 2: JSON STRUCTURED DATA" section
# → Extract structured data from all outputs
# → Validate with: jq . file.llm.json

# 4. Create .meta.json file (metadata)
# → Use schema from "FILE 3: METADATA" section
# → Record execution timeline and quality metrics

# 5. Validate all files
# → Use checklist from "QUALITY VALIDATION CHECKLIST" section
# → Ensure consistency across all three files
# → Check aggregate quality score ≥0.70

# 6. Save to output directory
# → /USER_DOCS/{agent}/{product_name}/
# → Trinity ready for use!
```

### To Validate a Completed Trinity:

```bash
# Check .md syntax
mdl product_name.md

# Validate .llm.json
jq . product_name.llm.json > /dev/null && echo "Valid JSON"

# Validate .meta.json
jq . product_name.meta.json > /dev/null && echo "Valid JSON"

# Check file sizes
ls -lh product_name.*

# Verify Trinity completeness
[ -f product_name.md ] && [ -f product_name.llm.json ] && [ -f product_name.meta.json ] && echo "Trinity complete!"
```

---

**Type**: Module
**Audience**: ADW Developers, LLM Engineers
**Status**: Production-Ready
**Last Updated**: 2025-12-04
