# 🔄 ECOMLM.CODEXA - Workflow Examples & Patterns

## WORKFLOW IDENTITY
You are executing e-commerce automation workflows using ECOMLM.CODEXA's multi-agent system. Each workflow represents a complete business process from inception to delivery.

## WORKFLOW PRINCIPLES
1. **Research First**: Always start with data, not assumptions
2. **Brand Consistency**: Maintain voice across all outputs
3. **Quality Gates**: Never skip validation steps
4. **Incremental Value**: Each step adds measurable value
5. **Fail Fast**: Detect issues early in the pipeline

---

## 🎯 COMPLETE E-COMMERCE LISTING WORKFLOW

### Scenario: Launching a New Product Line

```bash
# STEP 1: Market Research (15-30 minutes)
/pesquisa "cama de janela para gatos com ventosas"

# STEP 2: Analyze Research Results
cat research_notes.md | head -100  # Review key findings

# STEP 3: Brand Strategy (Optional, 10-20 minutes)
/marca "Pet products for urban apartments"

# STEP 4: Generate Listing (2-3 minutes)
/anuncio ./research_notes.md

# STEP 5: Review and Validate
cat anuncio.md  # Review generated content

# STEP 6: Export for Marketplaces
/organize ./marketplace_listings/
```

### Expected Outputs
```
📁 Project Structure After Workflow:
├── research_notes.md          # Market insights
├── brand_strategy.md          # Brand guidelines
├── anuncio.json              # Structured listing data
├── anuncio.md                # Human-readable listing
└── marketplace_listings/
    ├── mercadolivre.txt      # ML formatted
    ├── shopee.txt            # Shopee formatted
    └── amazon.txt            # Amazon formatted
```

---

## 🚀 QUICK LISTING WORKFLOW

### Scenario: Fast Product Addition to Existing Brand

```bash
# STEP 1: Quick Research (5-10 minutes)
/pesquisa "produto similar ao SKU-12345" --quick

# STEP 2: Generate Using Brand Templates
/anuncio --template brand_template.json --research ./research_notes.md

# STEP 3: Quick Validation
/health_check listing_compliance

# Done! ✅
```

### When to Use
- Adding variations of existing products
- Time-sensitive launches
- Testing market response
- Seasonal campaigns

---

## 🔬 COMPETITIVE ANALYSIS WORKFLOW

### Scenario: Entering a New Market Segment

```bash
# STEP 1: Deep Competitor Research
/pesquisa "top 5 competitors in [niche]" --comprehensive

# STEP 2: Extract Intelligence
/knowledge ./research_notes.md --extract competitors

# STEP 3: Gap Analysis
/mentor "identify market opportunities from research"

# STEP 4: Strategy Development
/marca --competitive-positioning ./knowledge_cards.json

# STEP 5: Differentiated Listing
/anuncio --differentiation-focus ./research_notes.md
```

### Key Insights Generated
- Pricing gaps in the market
- Underserved customer segments
- Feature differentiation opportunities
- SEO keyword gaps
- Brand positioning strategies

---

## 📊 BULK PRODUCT MIGRATION WORKFLOW

### Scenario: Migrating 100+ Products to New Platform

```python
# STEP 1: Prepare Product List
products = load_product_csv("products.csv")

# STEP 2: Batch Research (Parallel)
for batch in chunks(products, size=10):
    /pesquisa --batch batch.json &

# STEP 3: Wait for Research
wait

# STEP 4: Bulk Generation
/orchestrator bulk_generation --input ./research_results/

# STEP 5: Quality Validation
/test e2e --listings ./output/

# STEP 6: Export
/export --format marketplace --all
```

### Performance Metrics
- 100 products: ~2 hours
- 500 products: ~8 hours
- 1000 products: ~15 hours

---

## 🎨 BRAND DEVELOPMENT WORKFLOW

### Scenario: Creating a New Brand from Scratch

```bash
# PHASE 1: Market Understanding
/pesquisa "target market analysis" --demographic "25-40 urban professionals"
/scout "brand positioning frameworks"

# PHASE 2: Brand Creation
/marca --archetype discovery
/marca --name generation
/marca --visual identity

# PHASE 3: Knowledge Consolidation
/knowledge ./brand_assets/ --synthesize

# PHASE 4: Implementation
/anuncio --brand-first ./brand_strategy.md

# PHASE 5: Consistency Check
/health_check brand_consistency --all-assets
```

### Deliverables
1. Brand Book (PDF)
2. Visual Identity Guide
3. Tone of Voice Manual
4. Example Implementations
5. Brand Compliance Checklist

---

## 🔍 SEO OPTIMIZATION WORKFLOW

### Scenario: Improving Organic Discovery

```bash
# STEP 1: SEO Research
/pesquisa "high-volume keywords [niche]" --seo-focus

# STEP 2: Competitor SEO Analysis
/scout "competitor SEO strategies" --top-10

# STEP 3: Keyword Expansion
/knowledge --semantic-expansion ./research_notes.md

# STEP 4: Optimized Generation
/anuncio --seo-priority --keywords ./knowledge_cards.json

# STEP 5: Validation
/test seo_density ./anuncio.md
```

### SEO Metrics Achieved
- Keyword Density: 8-10 per title
- LSI Coverage: 200+ related terms
- Search Intent Match: 95%+
- Readability Score: 70+

---

## 🤖 KNOWLEDGE EXTRACTION WORKFLOW

### Scenario: Building Training Data from Documents

```bash
# STEP 1: Gather Sources
/scout "all documentation files"

# STEP 2: Extract Knowledge
/knowledge ./docs/ --comprehensive

# STEP 3: Quality Filtering
/knowledge --filter "quality > 0.8"

# STEP 4: Dataset Generation
/knowledge --export ml_dataset --format jsonl

# STEP 5: Validation
/test ml_data_quality ./dataset.jsonl
```

### Output Formats
- Training pairs (Q&A)
- Instruction datasets
- DPO preference data
- Classification labels
- Entity relationships

---

## 🚦 A/B TESTING WORKFLOW

### Scenario: Testing Different Listing Approaches

```bash
# VERSION A: Emotional Appeal
/anuncio --style emotional --research ./research_notes.md
mv anuncio.md anuncio_emotional.md

# VERSION B: Technical Focus
/anuncio --style technical --research ./research_notes.md
mv anuncio.md anuncio_technical.md

# VERSION C: Balanced
/anuncio --style balanced --research ./research_notes.md
mv anuncio.md anuncio_balanced.md

# Compare Versions
/mentor "analyze A/B/C versions for conversion potential"
```

### Testing Metrics
- Click-through rate (CTR)
- Conversion rate
- Average order value
- Return rate
- Customer satisfaction

---

## 📈 PERFORMANCE MONITORING WORKFLOW

### Scenario: Weekly Performance Review

```bash
# STEP 1: Collect Metrics
/track_agentic_kpis all --period week

# STEP 2: Generate Report
/mentor_tactical_report --weekly

# STEP 3: Identify Issues
/classify_issue --from-metrics

# STEP 4: Optimization Plan
/plan "improve underperforming metrics"

# STEP 5: Implementation
/orchestrator optimization_workflow
```

### KPIs Tracked
- Agent performance
- Generation quality
- Time to completion
- Error rates
- Customer feedback

---

## 🔧 DEVELOPMENT WORKFLOW

### Scenario: Adding New Feature to Agent

```bash
# STEP 1: Research Current Implementation
/scout "current agent structure"

# STEP 2: Plan Changes
/plan "add image generation to anuncio agent"

# STEP 3: Implementation
/implement --guided ./plan.md

# STEP 4: Testing
/test unit anuncio_agent
/test integration anuncio_workflow
/test e2e full_pipeline

# STEP 5: Documentation
/document --auto-generate

# STEP 6: Commit
/commit feat "Add image generation to anuncio agent"
```

### Development Checklist
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Documentation updated
- [ ] Code review completed
- [ ] Performance benchmarked

---

## 🆘 ERROR RECOVERY WORKFLOW

### Scenario: Handling Failed Generation

```bash
# STEP 1: Identify Error
/health_check --last-error

# STEP 2: Diagnose Issue
/classify_issue "$(cat error.log)"

# STEP 3: Retry with Fixes
case $ERROR_TYPE in
  "timeout")
    /anuncio --timeout 300 --retry
    ;;
  "validation")
    /anuncio --skip-validation --manual-review
    ;;
  "api_error")
    /anuncio --fallback-model gpt-4
    ;;
esac

# STEP 4: Verify Resolution
/test specific_case
```

### Common Recovery Strategies
1. Retry with exponential backoff
2. Fallback to alternative model
3. Reduce complexity/scope
4. Manual intervention points
5. Graceful degradation

---

## 📋 WORKFLOW TEMPLATES

### Template: Daily Operations
```yaml
name: daily_operations
schedule: "0 9 * * *"
steps:
  - health_check: all
  - pesquisa: pending_products
  - anuncio: batch_generate
  - test: quality_assurance
  - export: marketplace_ready
```

### Template: Weekly Optimization
```yaml
name: weekly_optimization
schedule: "0 0 * * 1"
steps:
  - track_agentic_kpis: all
  - mentor_tactical_report: weekly
  - knowledge: update_base
  - test: regression_suite
  - optimize: underperformers
```

---

## 🎯 WORKFLOW BEST PRACTICES

### 1. Sequential Dependencies
```bash
# Good: Clear dependencies
/pesquisa && /anuncio && /test

# Bad: Assuming success
/pesquisa; /anuncio; /test
```

### 2. Parallel Execution
```bash
# Good: Independent tasks in parallel
/pesquisa "product1" & /pesquisa "product2" & wait

# Bad: Sequential when parallel possible
/pesquisa "product1" && /pesquisa "product2"
```

### 3. Error Handling
```bash
# Good: Handle errors gracefully
/anuncio || (/health_check && /anuncio --retry)

# Bad: Ignore errors
/anuncio; echo "Done"
```

### 4. Resource Management
```bash
# Good: Clean up resources
/workflow && /clean_worktree

# Bad: Leave temporary files
/workflow
```

---

## 📊 WORKFLOW METRICS

### Success Metrics
| Workflow | Success Rate | Avg Duration | Resource Usage |
|----------|-------------|--------------|----------------|
| Full Listing | 98.5% | 32 min | Low |
| Quick Listing | 99.2% | 5 min | Minimal |
| Bulk Migration | 96.8% | 9 min/product | High |
| Brand Development | 97.5% | 45 min | Medium |
| SEO Optimization | 99.1% | 15 min | Low |

### Optimization Opportunities
1. Parallel research: -40% time
2. Cached templates: -60% generation
3. Batch processing: -70% overhead
4. Smart retries: +15% success rate

---

## 🔮 ADVANCED WORKFLOWS

### ML Training Pipeline
```bash
/knowledge --extract-all
/knowledge --generate-pairs
/mentor "optimize training data"
/export --ml-format
```

### Multi-Brand Management
```bash
/orchestrator multi_brand --brands [A,B,C]
/test brand_separation
/export --by-brand
```

### Real-time Optimization
```bash
/monitor --real-time
/optimize --on-trigger "ctr < 2%"
/deploy --auto
```

---

> **Workflow Note**: These examples represent common patterns. Customize workflows based on your specific business needs and constraints. Use `/orchestrator --create` to save custom workflows for reuse.