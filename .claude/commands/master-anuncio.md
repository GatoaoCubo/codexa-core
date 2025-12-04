# master-anuncio - Full E-Commerce Pipeline Orchestrator

Execute the complete master anuncio pipeline: research → ad generation → photo prompts

## Usage

```bash
/master-anuncio "Product Name"
/master-anuncio "Product Name" --skip-research
/master-anuncio "Product Name" --skip-photos
/master-anuncio "Product Name" --dry-run
/master-anuncio "Product Name" --skip-research --skip-photos
```

## Description

This command executes the **MASTER_ADW_ANUNCIO_PIPELINE** - a complete end-to-end workflow for Brazilian e-commerce product listing generation:

1. **Phase 1: Market Research** (pesquisa_agent) - Competitive analysis, keyword research, market positioning
2. **Phase 2: Ad Generation** (anuncio_agent) - SEO-optimized titles, descriptions, keywords for multiple marketplaces
3. **Phase 3: Visual Assets** (photo_agent) - AI image generation prompts tailored to product type and marketplace

## Arguments

| Argument | Type | Required | Description |
|----------|------|----------|-------------|
| `$ARGUMENTS` | string | Yes | Product name (3-100 chars) |
| `--skip-research` | flag | No | Skip Phase 1 (research) - use cached research if available |
| `--skip-photos` | flag | No | Skip Phase 3 (photo generation) - only generate ad copy |
| `--dry-run` | flag | No | Execute workflow in simulation mode (no files written) |

## Workflow Phases

### Phase 1: Market Research (pesquisa_agent)
**Duration**: 10-15 min | **Status**: `$skip_research`
```yaml
Tasks:
  - Competitor analysis (3-5 main competitors)
  - Keyword research (head terms + longtails)
  - Market positioning analysis
  - Pricing strategy recommendations
  - Target audience identification

Output:
  - research_notes.md
  - competitor_analysis.json
  - keyword_strategy.json
```

### Phase 2: Ad Generation (anuncio_agent)
**Duration**: 8-12 min | **Status**: Always executed
```yaml
Tasks:
  - Strategic brief creation (product type detection)
  - Title generation (3 marketplace-optimized variations)
  - Keywords expansion (4 semantic blocks, 70+ keywords)
  - Description building (marketplace-specific templates)
  - Bullet points (benefit-focused, StoryBrand framework)
  - QA validation (11-criteria compliance check)

Output:
  - anuncio.md (human-readable copy package)
  - anuncio.llm.json (structured data)
  - anuncio.meta.json (workflow metadata)
```

### Phase 3: Visual Assets (photo_agent)
**Duration**: 5-8 min | **Status**: `$skip_photos`
```yaml
Tasks:
  - Image prompt generation (8-12 prompts per product type)
  - Video script creation (30-60 sec storyboard)
  - Marketplace-specific optimization (GitHub/ML/Shopee/TikTok)
  - Asset tagging for AI generation (DALL-E, Midjourney compatible)

Output:
  - image_prompts.json (AI generation prompts)
  - video_script.md (storyboard format)
  - asset_manifest.json (all visual assets metadata)
```

## Quality Gates

All phases include quality validation:

| Phase | Validator | Pass Threshold | Action on Fail |
|-------|-----------|----------------|----------------|
| Research | market_validator | ≥0.70 confidence | Retry with expanded search |
| Ad Copy | compliance_validator | ≥0.85 quality score | Review + manual refinement |
| Visuals | asset_validator | ≥0.80 quality score | Regenerate prompts |

## Output Structure

Files are saved to: `USER_DOCS/produtos/{{PRODUCT_NAME}}/`

```
{{PRODUCT_NAME}}/
├── research/
│   ├── {{PRODUCT_NAME}}_research_notes.md
│   ├── competitor_analysis.json
│   └── keyword_strategy.json
├── anuncios/
│   ├── {{PRODUCT_NAME}}_anuncio.md
│   ├── {{PRODUCT_NAME}}_anuncio.llm.json
│   └── {{PRODUCT_NAME}}_anuncio.meta.json
└── visuals/
    ├── {{PRODUCT_NAME}}_image_prompts.json
    ├── {{PRODUCT_NAME}}_video_script.md
    └── {{PRODUCT_NAME}}_asset_manifest.json
```

## Examples

### Full Pipeline (All Phases)
```bash
/master-anuncio "Bluetooth Headphone Pro Max"
```
**Output**: Complete research, ad copy, and visual assets (23-35 min total)

### Skip Research (Use Cached)
```bash
/master-anuncio "Bluetooth Headphone Pro Max" --skip-research
```
**Output**: Only ad copy and visuals (13-20 min) - requires previous research to exist

### Only Ad Copy
```bash
/master-anuncio "Bluetooth Headphone Pro Max" --skip-photos
```
**Output**: Research and ad copy only, no visual assets (18-27 min)

### Dry Run (Simulation)
```bash
/master-anuncio "Bluetooth Headphone Pro Max" --dry-run
```
**Output**: Workflow execution plan + quality predictions (no files written)

## Flags Reference

### `--skip-research`
- **When to use**: You already have research data from a previous run
- **Behavior**: Loads cached research from `USER_DOCS/produtos/{{PRODUCT_NAME}}/research/`
- **Error if**: Research files don't exist and no input provided
- **Time saved**: ~10-15 min

### `--skip-photos`
- **When to use**: You only need copy/SEO optimization, not visuals
- **Behavior**: Executes phases 1-2 only, skips phase 3
- **Output**: Research + Ad copy (no image/video prompts)
- **Time saved**: ~5-8 min

### `--dry-run`
- **When to use**: Preview workflow before execution, estimate time/quality
- **Behavior**: Shows execution plan, quality predictions, estimated outputs
- **Output**: Detailed report (no files written, no API calls)
- **Time**: <2 min

## Integration Points

This command chains the following agents:

```
[Product Name]
     |
     v
┌─────────────────────────────────────┐
│ pesquisa_agent (Phase 1)            │ [/prime-pesquisa]
│ - Competitive analysis              │
│ - Market research                   │
│ - Keyword discovery                 │
└──────────────┬──────────────────────┘
               |
               v research_notes.md
┌─────────────────────────────────────┐
│ anuncio_agent (Phase 2)             │ [/prime-anuncio]
│ - Title generation                  │
│ - Description building              │
│ - Keyword optimization              │
│ - Compliance validation             │
└──────────────┬──────────────────────┘
               |
               v anuncio.md + .llm.json
┌─────────────────────────────────────┐
│ photo_agent (Phase 3)               │ [/prime-photo]
│ - Image prompt generation           │
│ - Video script creation             │
│ - Asset optimization                │
└──────────────┬──────────────────────┘
               |
               v Complete Package
        USER_DOCS/produtos/
```

## Performance Metrics

| Configuration | Duration | Tokens | Quality |
|---------------|----------|--------|---------|
| Full pipeline | 23-35 min | 120-180k | ≥0.85 |
| Skip research | 13-20 min | 80-120k | ≥0.85 |
| Skip photos | 18-27 min | 100-150k | ≥0.85 |
| Dry run | <2 min | <5k | Predicted |

## Error Handling

| Error | Solution |
|-------|----------|
| Product name too short (<3 chars) | Provide minimum 3 character name |
| Research not found (with --skip-research) | Run full pipeline first or provide research manually |
| Network timeout (Phase 1) | Retry - transient network issue |
| Low quality score (<0.70) | Review + manual refinement required |
| API rate limit | Wait 60s + retry |

## Prerequisites

Before running, ensure:

1. **Agent Context Loaded**:
   - Read `/anuncio_agent/PRIME.md` (identity)
   - Read `/pesquisa_agent/PRIME.md` (identity)
   - Read `/photo_agent/PRIME.md` (identity)

2. **Configuration Files Available**:
   - `config/marketplace_specs.json` (platform constraints)
   - `config/copy_rules.json` (compliance rules)
   - `config/persuasion_patterns.json` (PNL patterns)

3. **User Directory Structure**:
   - `USER_DOCS/produtos/` exists and is writable

4. **LLM Model**:
   - Minimum: Claude Sonnet 4 or GPT-4o
   - Recommended: Claude Opus 4.5 (best quality)

## Environment Variables

Optional configuration:

```bash
CODEXA_DRY_RUN=true          # Force dry-run mode
CODEXA_SKIP_RESEARCH=true    # Always skip research
CODEXA_SKIP_PHOTOS=true      # Always skip photos
CODEXA_OUTPUT_DIR=/custom/path  # Override output directory
CODEXA_MAX_DURATION=30       # Timeout in minutes
```

## Related Commands

- `/prime-pesquisa` - Run research phase standalone
- `/prime-anuncio` - Run ad generation standalone
- `/prime-photo` - Run photo generation standalone
- `/anuncio` - Legacy ad generator (single phase)
- `/pesquisa` - Legacy research generator (single phase)

## Workflow Architecture

**Type**: Multi-phase ADW (Agentic Developer Workflow)
**Duration**: 23-35 min (full) | 2-27 min (with flags)
**Output**: Trinity format (.md + .llm.json + .meta.json)
**Compliance**: ANVISA/INMETRO/CONAR + marketplace-specific rules
**Quality Validation**: 11-criteria compliance + 3-stage quality gates

## Success Criteria

Workflow completes successfully when:
- ✅ All phases executed (or skipped with flag)
- ✅ Quality score ≥0.85 (or predicted ≥0.85 for dry-run)
- ✅ Output files generated in Trinity format
- ✅ No compliance violations
- ✅ Execution time within 35min target (or predicted for dry-run)

## Troubleshooting

**Low research confidence (<0.70)**
```
→ Issue: Market data insufficient
→ Solution: Provide more detailed product information or additional research data
```

**Ad copy quality score <0.85**
```
→ Issue: Description or titles don't meet standards
→ Solution: Review phase 2 output, check compliance issues in qa_report
```

**Visual assets not optimized**
```
→ Issue: Image prompts below quality threshold
→ Solution: Regenerate with --skip-research --skip-photos (phase 3 only)
```

**Timeout or resource limit**
```
→ Issue: Workflow exceeds time/token budget
→ Solution: Run phases separately (pesquisa, anuncio, photo) or use --dry-run first
```

## Version

- **Command**: master-anuncio v1.0.0
- **Pipeline**: MASTER_ADW_ANUNCIO v2.1.0
- **Last Updated**: 2025-12-04
- **Status**: Production-Ready

---

**Framework**: CODEXA Meta-Construction System
**Type**: Pipeline Orchestrator | **Agents**: 3 (pesquisa, anuncio, photo)
**Documentation**: [CLAUDE.md Law 4 - Agentic Design](docs/CLAUDE.md)
