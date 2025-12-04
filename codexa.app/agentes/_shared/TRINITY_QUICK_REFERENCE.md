# Trinity Quick Reference Card

**Quick Link**: `agentes/_shared/trinity_output.md` (full documentation)

---

## The Trinity Pattern at a Glance

Every ADW workflow completion produces 3 files:

```
product_name_output_type.md          (Human-readable narrative)
product_name_output_type.llm.json    (Structured data for LLMs/APIs)
product_name_output_type.meta.json   (Workflow execution metadata)
```

**Why 3 files?**
- `.md`: Humans review, edit, share
- `.llm.json`: Systems parse, process, integrate
- `.meta.json`: Monitoring, auditing, chaining workflows

---

## File Size Guidelines

| File | Min | Typical | Max | Reason |
|------|-----|---------|-----|--------|
| `.md` | 5 KB | 25 KB | 100 KB | Self-contained narrative |
| `.llm.json` | 2 KB | 15 KB | 50 KB | Structured arrays only |
| `.meta.json` | 1 KB | 4 KB | 10 KB | Lightweight summary |

---

## FILE 1: .md (Markdown) - Human-Readable

### Standard Sections

```markdown
# [Product] - [Type] Package

**Generated**: ISO 8601 timestamp
**Quality Score**: X.XX/1.00

## SECTION 1: Primary Content
[Main deliverable]

## SECTION 2: Secondary Content
[Supporting material]

## SECTION 3: Variants
Variant A, B, C...

## QUALITY REPORT
Scores + issues + improvements

## METADATA
Product, type, compliance, time, phases
```

### Do's and Don'ts

✅ **DO**:
- Use code blocks for structured data
- Include examples
- Make it self-contained
- Use headers to organize
- Include metrics with units

❌ **DON'T**:
- Reference external files
- Use excessive nesting (>3 levels)
- Leave TODO placeholders
- Mix file formats in .md
- Make files >100 KB

---

## FILE 2: .llm.json (Structured Data)

### Core Structure

```json
{
  "metadata": {
    "workflow_id": "...",
    "agent": "...",
    "generated_at": "2025-11-17T14:30:45Z"
  },
  "context": {
    "product_name": "string",
    "product_type": "B2B_SAAS|PHYSICAL_PRODUCT|SERVICE",
    "marketplace_type": "GITHUB|MERCADO_LIVRE|SHOPEE|TIKTOK_SHOP"
  },
  "content": {
    "primary": {...},
    "secondary": {...},
    "variants": [...]
  },
  "quality": {
    "aggregate_score": 0.XX,
    "component_scores": {...},
    "validation_checks": {...}
  },
  "execution": {
    "duration_minutes": XX,
    "phases_completed": X,
    "phase_breakdown": [...]
  }
}
```

### Data Type Rules

✅ **USE**:
- `string`, `number`, `boolean`, `null` (primitives)
- `array` (for lists of similar items)
- `object` (for related fields)
- Timestamps: ISO 8601 (2025-11-17T14:30:45Z)
- Scores: 0.00-1.00 range (not percentages)
- camelCase for field names

❌ **DON'T**:
- Object keys with numbers (`{"1": "a", "2": "b"}`)
- Empty strings (use `null`)
- Timestamps: Unix time or MM/DD/YYYY
- Scores: Percentages (0-100) or fractions
- snake_case or kebab-case

### Validation

```bash
# Is it valid JSON?
jq . file.llm.json > /dev/null && echo "Valid"

# Extract specific field
jq '.quality.aggregate_score' file.llm.json

# Count items in array
jq '.content.variants | length' file.llm.json
```

---

## FILE 3: .meta.json (Metadata)

### Core Structure

```json
{
  "workflow_version": "1.0.0",
  "generator": "CODEXA ADW Intelligent Constructor v1.0.0",
  "generated_at": "2025-11-17T14:30:45Z",
  "execution_id": "adw_run_agent_timestamp",

  "execution": {
    "phases_executed": 7,
    "total_duration_minutes": 24,
    "phase_breakdown": [
      {
        "phase_id": "phase_1",
        "phase_name": "Input Validation",
        "duration_minutes": 3,
        "status": "completed"
      }
    ]
  },

  "quality": {
    "final_output_quality": 0.92,
    "validation_checks_passed": 11,
    "validation_checks_total": 11,
    "completeness_percent": 100
  },

  "output": {
    "files_generated": [".md", ".llm.json", ".meta.json"],
    "output_location": "USER_DOCS/agent/product_name/",
    "ready_for_use": true
  },

  "chain_info": {
    "source_workflow": "pesquisa_agent",
    "next_recommended_workflow": "anuncio_agent",
    "can_chain_forward": true
  }
}
```

### Purpose by Field

- `workflow_version`: Schema version (for compatibility)
- `generator`: Tool/version that created this
- `generated_at`: When it was created
- `execution_id`: Unique identifier (for auditing)
- `execution`: Timing and phase breakdown (track what took how long)
- `quality`: Summary metrics (high-level overview)
- `output`: Files generated and location (what was produced)
- `chain_info`: Integration with other workflows (for multi-agent pipelines)

---

## ASSEMBLY WORKFLOW

### Quick Checklist

- [ ] **Phase 1**: Complete all ADW phases → collect outputs
- [ ] **Phase 2**: Generate .md file
  - Fill template
  - Include all sections
  - Add metrics
  - Validate syntax
- [ ] **Phase 3**: Generate .llm.json file
  - Extract structured data
  - Use arrays for lists
  - Validate JSON syntax
- [ ] **Phase 4**: Generate .meta.json file
  - Record execution times
  - Calculate quality scores
  - Include chain info
- [ ] **Phase 5**: Validate all files (use checklist below)
- [ ] **Phase 6**: Save to output directory

---

## VALIDATION CHECKLIST (30 seconds)

### .md File
- [ ] Has H1, H2, H3 headers
- [ ] No "TODO" placeholders
- [ ] Code blocks formatted (triple backticks)
- [ ] Self-contained (no external references)
- [ ] Size: 10-100 KB
- [ ] Renders in GitHub

### .llm.json File
- [ ] Valid JSON (passes `jq .`)
- [ ] Has metadata, context, content, quality, execution
- [ ] Scores in 0.00-1.00 range
- [ ] Uses arrays (not numbered object keys)
- [ ] ISO 8601 timestamps
- [ ] Size: 5-50 KB

### .meta.json File
- [ ] Valid JSON (passes `jq .`)
- [ ] Has workflow_version, generator, generated_at
- [ ] Total duration = sum of phases (±2min)
- [ ] All phases listed in phase_breakdown
- [ ] Files generated match actual files
- [ ] Size: 2-10 KB

### Cross-File
- [ ] Product name matches across all 3 files
- [ ] Quality scores consistent (within 0.05 margin)
- [ ] Timestamps make sense (generated_at after execution end)
- [ ] Output location exists and matches .meta.json

---

## Common Patterns

### Pattern: Anuncio (Ad Copy) Trinity

```
INPUT: Research notes (from pesquisa_agent)
  ↓
PHASES:
  1. Input Validation
  2. Title Generation (3 variations)
  3. Keywords Expansion (4 blocks)
  4. Description Building
  5. Visual Assets (images + video)
  6. QA & Variants
  7. Output Assembly (Trinity)
  ↓
OUTPUT:
  └─ {product}_ad_copy.md          (titles, keywords, description, variants)
  └─ {product}_ad_copy.llm.json    (structured arrays + scores)
  └─ {product}_ad_copy.meta.json   (8 phases, ~32min, quality 0.88)
```

### Pattern: Photo (Prompts) Trinity

```
INPUT: Product description + style
  ↓
PHASES:
  1. Input Processing & Scene Planning (9-scene grid)
  2. Camera & Lighting Design
  3. Prompt Generation (9 scenes)
  4. Brand & Compliance Validation
  5. Batch Assembly & QA (Trinity)
  ↓
OUTPUT:
  └─ {product}_photo_prompts.md      (9 scenes + batch block)
  └─ {product}_photo_prompts.llm.json (scene array + quality scores)
  └─ {product}_photo_prompts.meta.json (5 phases, ~18min, quality 0.85)
```

### Pattern: Pesquisa (Research) Trinity

```
INPUT: Product brief
  ↓
PHASES:
  1-2. Discovery & Query Bank
  3-4. Web Search (inbound + outbound)
  5. Competitor Analysis
  6. SEO Taxonomy
  7-8. Compliance & Synthesis
  9. Output Assembly (Trinity)
  ↓
OUTPUT:
  └─ {product}_research_notes.md     (22 blocks of research data)
  └─ {product}_research_notes.llm.json (structured research blocks)
  └─ {product}_research_notes.meta.json (9 phases, ~25min, quality 0.82)
```

---

## Quality Scoring

### Aggregate Score Formula

```
Quality = (Completeness * 0.40) +
          (Structure * 0.30) +
          (Content * 0.20) +
          (Compliance * 0.10)
```

Where:
- **Completeness**: Sections filled / Total sections
- **Structure**: File format + organization + validation passed
- **Content**: Data quality, metrics, examples
- **Compliance**: Marketplace rules, regulatory requirements

### Score Interpretation

| Range | Status | Action |
|-------|--------|--------|
| 0.90-1.00 | Excellent | Ready to use |
| 0.80-0.89 | Good | Use with minor review |
| 0.70-0.79 | Acceptable | Use with full review |
| <0.70 | Poor | Redo phase(s) |

---

## Troubleshooting

### .llm.json Won't Parse

```bash
# Find the error
jq . file.llm.json

# Fix:
# - Check for trailing commas
# - Ensure all strings in quotes
# - Verify nested braces/brackets match
```

### Quality Score Mismatch

**Problem**: .md says 0.92, .llm.json says 0.85

**Fix**: Use same calculation method everywhere
1. Decide formula once
2. Document in .meta.json
3. Apply consistently

### Files Too Large

**Problem**: .md > 100 KB

**Fix**:
- Move data arrays to .llm.json
- Keep .md to summary + examples
- Reference .llm.json for details

### Missing Validation Checks

**Problem**: QA Report incomplete

**Fix**: Complete all checks before assembly
- Document pass/fail for each
- List specific issues
- Suggest improvements

---

## Output Directory Structure

```
USER_DOCS/
├── anuncios/
│   └── {product_name}/
│       ├── {product_name}_ad_copy.md
│       ├── {product_name}_ad_copy.llm.json
│       └── {product_name}_ad_copy.meta.json
│
├── photos/
│   └── {product_name}/
│       ├── {product_name}_photo_prompts.md
│       ├── {product_name}_photo_prompts.llm.json
│       └── {product_name}_photo_prompts.meta.json
│
└── research/
    └── {product_name}/
        ├── {product_name}_research_notes.md
        ├── {product_name}_research_notes.llm.json
        └── {product_name}_research_notes.meta.json
```

---

## Next Steps

1. **Read full module**: `agentes/_shared/trinity_output.md`
2. **Find your ADW**: `agentes/{agent}/workflows/100_ADW_RUN_{NAME}.md`
3. **Execute workflow**: Follow phases 1 through N
4. **Collect outputs**: Save results from each phase
5. **Assemble Trinity**: Use templates and checklist above
6. **Validate**: Run 30-second checklist
7. **Save**: To correct output directory

---

**Quick Links**:
- Full module: `/agentes/_shared/trinity_output.md`
- Example: `/agentes/anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md`
- Reference: `PRIME.md` (in each agent directory)

**Last Updated**: 2025-12-04
