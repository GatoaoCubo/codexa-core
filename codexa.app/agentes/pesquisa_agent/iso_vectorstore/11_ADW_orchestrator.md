# ADW ORCHESTRATOR | pesquisa_agent v3.0.0

**Purpose**: 9-phase market research workflow (brief → research_notes.md)
**Duration**: 20-30 min | **Output**: research_notes.md (22 blocks)

---

## WORKFLOW (9 Phases)

### Phase 1: DISCOVERY (2min)
**Doc**: `14_HOP_intake_validation.md`
- Auto-detect capabilities (web_search required)
- Validate brief (product, category, audience, price)
- Output: `{validated_brief, capabilities}`

### Phase 2: QUERY BANK (3min)
**Doc**: `13_HOP_main_agent.md`
- Generate head terms (10-15)
- Derive longtails (30-50)
- Map synonyms + variations
- Output: `{query_bank}`

### Phase 3: INBOUND SEARCH (8min)
**Doc**: `15_HOP_competitor_analysis.md`
- Search 9 BR marketplaces
- Extract: titles, prices, ratings, badges
- Log all queries with URLs
- Output: `{marketplace_data, seo_inbound}`

### Phase 4: OUTBOUND SEARCH (8min)
**Doc**: `19_HOP_sentiment_analysis.md`
- Search: Google, YouTube, TikTok, Instagram
- Reclame Aqui (required)
- Extract: pain points, gains, objections
- Output: `{sentiment_data, seo_outbound}`

### Phase 5: COMPETITOR ANALYSIS (6min)
**Doc**: `15_HOP_competitor_analysis.md`
- Analyze top 3-5 competitors
- Quantitative benchmark
- Gap identification
- Output: `{competitor_profiles, benchmark}`

### Phase 6: SEO TAXONOMY (4min)
**Doc**: `16_HOP_gap_identification.md`
- Cluster keywords
- Separate inbound vs outbound
- Category positioning
- Output: `{seo_taxonomy}`

### Phase 7: COMPLIANCE (3min)
**Doc**: `17_HOP_image_analysis.md`
- ANVISA, INMETRO, CONAR checks
- Risk analysis
- Output: `{compliance_risks}`

### Phase 8: SYNTHESIS (3min)
**Doc**: `18_HOP_price_comparison.md`
- Consolidate findings
- Generate insights
- Priority opportunities
- Output: `{insights, opportunities}`

### Phase 9: VALIDATION (2min)
**Doc**: `20_HOP_qa_validation.md`
- Verify 22 blocks present
- Check quality gates
- Calculate confidence
- Output: `{research_notes.md, metadata.json}`

---

## QUALITY GATES

| Gate | Target |
|------|--------|
| Blocks present | 22/22 |
| Competitors analyzed | >= 3 |
| Queries logged | >= 15 |
| Confidence score | >= 0.75 |
| Placeholders | <= 10% |

---

## CHAINING

```
Phase 1 output → Phase 2 input
Phase 2 output → Phase 3, 4 input
Phase 3, 4 output → Phase 5 input
Phase 5 output → Phase 6 input
Phase 6 output → Phase 7 input
Phase 7 output → Phase 8 input
All outputs → Phase 9 input
```

---

**ADW**: 11 | **Agent**: pesquisa_agent | **Version**: 3.0.0
**Tokens**: ~800 (optimized from 8,500)
