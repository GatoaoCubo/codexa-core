# Workflows Documentation | pesquisa_agent

**Agent**: pesquisa_agent
**Version**: 2.1.0
**Workflows Available**: 1 (Phase A complete)
**Status**: Production-Ready

---

## AVAILABLE WORKFLOWS

### 100_ADW_RUN_PESQUISA.md ⭐ PRIMARY

**Purpose**: Complete Brazilian e-commerce market research execution
**Duration**: 20-30 minutes
**Input**: Research brief (product, category, audience, price)
**Output**: research_notes.md (22 blocks) + metadata.json + queries.json
**Status**: ✅ Production-Ready (Phase A - Conversational)

**When to use**:
- Pre-launch product research (understand market before launch)
- Competitor monitoring (track competition strategies)
- Ad optimization (improve low-conversion ads with research insights)
- SEO planning (extract keywords for content strategy)
- New marketplace entry (adapt product for new sales channel)

**How to execute**:
```
1. Load PRIME.md + 100_ADW_RUN_PESQUISA.md
2. Provide research brief (min: product, category, audience, price)
3. Follow 9 phases sequentially
4. Validate outputs (quality score ≥0.75)
5. Review research_notes.md in user_research/
```

**Capabilities required**:
- web_search: ✅ REQUIRED (abort if not available)
- vision: 📄 Optional (screenshot analysis)
- file_search: 📄 Optional (compliance rules)
- code_interpreter: 📄 Optional (advanced metrics)

---

## WORKFLOW PATTERN

**Type**: Sequential Execution (9 Phases)

**Phases**:
1. **Phase 1**: Capability Discovery & Brief Validation (2min)
2. **Phase 2**: Query Bank Generation (3min)
3. **Phase 3**: Web Search INBOUND - Marketplaces (8min)
4. **Phase 4**: Web Search OUTBOUND - SERP & Social (8min)
5. **Phase 5**: Competitor Analysis & Benchmark (6min)
6. **Phase 6**: SEO Taxonomy & Strategy (4min)
7. **Phase 7**: Compliance & Risk Analysis (3min)
8. **Phase 8**: Synthesis & Insights (3min)
9. **Phase 9**: Output Assembly & Validation (2min)

**Total Duration**: ~40 minutes (target: 20-30 min with optimizations)

**Data Flow**:
```
User Brief
  → Phase 1: Validate + detect capabilities
  → Phase 2: Generate keyword bank
  → Phase 3: Search marketplaces (9 BR platforms)
  → Phase 4: Search SERP + social (Google, YouTube, TikTok, Instagram, Reclame Aqui)
  → Phase 5: Analyze competitors (≥3) + benchmark
  → Phase 6: Consolidate SEO taxonomy
  → Phase 7: Check compliance (ANVISA, INMETRO) + risks
  → Phase 8: Synthesize insights + prioritize opportunities
  → Phase 9: Assemble outputs (22 blocks) + validate
  → user_research/{product}_research_notes.md + metadata + queries
```

---

## QUALITY GATES

All workflows include validation at each phase:

**Phase-Level Validation**:
- ✅ Each phase validates inputs before execution
- ✅ Each phase validates outputs before moving to next
- ✅ Error handling with clear messages + suggested fixes

**Workflow-Level Validation** (Phase 9):
- ✅ All 22 blocks present in research_notes.md
- ✅ ≥3 competitors analyzed with quantitative data
- ✅ ≥15 web queries logged (date, source, URL, insight)
- ✅ Metrics in BRL and % (not just qualitative)
- ✅ Completeness ≥75% (≤10% [SUGESTÃO] placeholders)
- ✅ Confidence score ≥0.75/1.0

**Quality Scoring**:
```python
completeness = (filled_blocks / 22) * 100  # Target: ≥75%
suggestions_ratio = suggestion_count / total_fields  # Target: ≤10%
confidence_score = avg(block_confidence_scores)  # Target: ≥0.75
quality_score = (completeness * 0.4 + (1 - suggestions_ratio) * 0.3 + confidence_score * 0.3)
```

**Minimum Quality Score**: 0.75/1.0

---

## OUTPUT STRUCTURE

**Primary Output**: `user_research/{product}_research_notes.md`

**22 Blocks**:
1. Lacunas do Brief
2. Head Terms Prioritários
3. Longtails
4. Sinônimos e Variações
5. Termo Contextual e Ocasião
6. Dores do Público
7. Ganhos Desejados
8. Objeções e Respostas
9. Provas e Evidências
10. Diferenciais Competitivos
11. Riscos ou Alertas
12. Análise de Concorrentes (≥3)
13. Benchmark de Concorrentes
14. Estratégias e Gaps
15. Padrões de Linguagem
16. SEO Outbound
17. SEO Inbound
18. Regras Críticas de Marketplace
19. Decisões de Copy Iniciais
20. Consultas Web (≥15 logged)
21. Imagens Analisadas (if applicable)
22. Resumo Executivo

**Secondary Outputs**:
- `{product}_metadata.json` - Execution metadata, quality scores, duration
- `{product}_queries.json` - All web queries traced (date, source, URL, insight)

---

## FUTURE WORKFLOWS (Planned)

### 101_ADW_QUICK_PESQUISA.md
**Status**: Planned
**Purpose**: Abbreviated research (main competitors + SEO only)
**Duration**: 10-15 minutes
**Use case**: Quick competitive checks, ad refresh research
**Phases**: 5 (discovery, query bank, marketplace search, competitor analysis, output)

### 102_ADW_COMPLIANCE_PESQUISA.md
**Status**: Planned
**Purpose**: Deep compliance validation (health, kids, electronics)
**Duration**: 15-20 minutes
**Use case**: High-risk categories requiring detailed regulatory analysis
**Phases**: 7 (focus on ANVISA, INMETRO, ANATEL, CONAR rules)

### 103_ADW_REVALIDATE_PESQUISA.md
**Status**: Planned
**Purpose**: Re-run research for existing product (update stale data)
**Duration**: 15-20 minutes
**Use case**: Monthly/quarterly research updates, competitive monitoring
**Phases**: 6 (load previous research, re-search changed areas, compare, report deltas)

---

## PHASE B: PYTHON AUTOMATION

**Status**: ⏳ Planned (after Phase A validation complete)
**Script**: `run_pesquisa_agent.py`

**Features** (to be implemented):
- LLM API integration (Anthropic Claude / OpenAI GPT)
- CLI arguments for batch processing
- JSON brief input support
- Quality reporting (PDF/JSON)
- CI/CD integration hooks
- Parallel web searches (performance optimization)
- Caching layer (avoid redundant searches)

**Planned Usage**:
```bash
# Single research
python run_pesquisa_agent.py \
  --brief "Product: X, Category: Y, Audience: Z, Price: R$ A-B" \
  --output user_research/ \
  --model claude-sonnet-3.5

# Batch processing
python run_pesquisa_agent.py \
  --brief-file briefs.json \
  --output-dir batch_research/ \
  --parallel 3

# CI/CD integration
python run_pesquisa_agent.py \
  --brief-file $BRIEF_JSON \
  --output $OUTPUT_DIR \
  --report-format json \
  --min-quality 0.80
```

---

## INTEGRATION

### Upstream Agents
**None** - pesquisa_agent is independent (does not depend on other agents)

### Downstream Agents
**Consumers of research_notes.md**:

1. **anuncio_agent** (Ad Copy Generation):
   - Uses: Pain points, gains, objections, proofs, language patterns, SEO keywords
   - Workflow: Load research_notes.md → Generate ad copy optimized for marketplace

2. **marca_agent** (Brand Strategy):
   - Uses: Competitor analysis, gaps, positioning opportunities, audience insights
   - Workflow: Load research_notes.md → Develop brand positioning

3. **USER_DOCS/produtos/** (Product Documentation):
   - Uses: Complete research as product knowledge base
   - Workflow: Archive research_notes.md for future reference

### Integration with iso_vectorstore
- Workflow files synced to `iso_vectorstore/` for portability
- Enables drag-and-drop to other LLM platforms
- File: `17_pesquisa_workflow_adw.md` (or similar numbering)

---

## RELATED FILES

**Core Workflow Files**:
- `100_ADW_RUN_PESQUISA.md` - Complete execution workflow ⭐
- `ADW_TEMPLATE.md` - Template for creating new workflows
- `IMPLEMENTATION_GUIDE.md` - Guide for replicating to other agents
- `README_WORKFLOWS.md` - This file

**Agent Documentation**:
- `../PRIME.md` - Agent instructions (source of workflow steps)
- `../README.md` - Agent structure and navigation
- `../INSTRUCTIONS.md` - Operational instructions
- `../SETUP.md` - Platform-specific setup

**Configuration**:
- `../config/agent.json` - Agent configuration
- `../config/marketplaces.json` - 9 BR marketplace database
- `../config/plans/standard_research.json` - Default execution plan

**Templates**:
- `../templates/research_notes.md` - 22-block output template

**Output Directory**:
- `../user_research/` - All research outputs saved here

---

## REPLICATION TO OTHER AGENTS

**This workflow pattern can be replicated to**:
- anuncio_agent (ad copy generation workflow)
- marca_agent (brand strategy workflow)
- mentor_agent (mentoring workflow)
- photo_agent (photo generation workflow)
- Any new agent created with `/codexa-build_agent`

**How to replicate**:
1. Read `IMPLEMENTATION_GUIDE.md` (complete step-by-step)
2. Copy `ADW_TEMPLATE.md` to target agent
3. Map target agent's PRIME.md steps to ADW phases
4. Follow 7-phase implementation process
5. Test and validate
6. Sync to iso_vectorstore

**Estimated Time**: 30-45 minutes per agent

---

## TROUBLESHOOTING

### "Workflow takes >35 minutes"
**Solution**:
- Reduce number of marketplaces searched (focus on top 3)
- Reduce number of head terms (focus on top 5)
- Skip optional phases if time-constrained (Phase 7 compliance can be quick-checked)

### "Quality score <0.75"
**Solution**:
- Provide more detailed brief (reduce assumptions)
- Extend search to more channels (increase query count)
- Re-run weak phases (check lowest confidence blocks)

### "Missing [SUGESTÃO] placeholders >10%"
**Solution**:
- Niche product or limited public data - flag in executive summary
- Supplement with manual research
- User interview to fill gaps

### "Capabilities: web_search not available"
**Solution**:
- See `../SETUP.md` for platform-specific web_search enablement
- OpenAI: Use Assistants API with web_search tool
- Claude: Use Claude Code with MCP web search
- Gemini: Use Gemini AI Studio with Grounding

---

## CHANGELOG

**v1.0.0** (2025-11-17):
- Initial workflow creation
- 100_ADW_RUN_PESQUISA.md complete (9 phases)
- Documentation suite (TEMPLATE, GUIDE, README)
- Phase A (Conversational) ready for testing
- Phase B (Python automation) planned

---

## NEXT STEPS

**Immediate**:
1. Test 100_ADW_RUN_PESQUISA.md with sample brief
2. Validate outputs against quality gates
3. Document any issues or improvements
4. Update sync_iso_vectorstore.py with workflow files
5. Sync to iso_vectorstore/

**Phase B** (Python Automation):
1. Create `run_pesquisa_agent.py` script
2. Implement LLM API integration
3. Add batch processing
4. Add quality reporting

**Replication**:
1. Apply pattern to anuncio_agent (next target)
2. Apply pattern to marca_agent
3. Apply pattern to mentor_agent
4. Apply pattern to photo_agent

---

**Version**: 1.0.0
**Created**: 2025-11-17
**Maintainer**: CODEXA Meta-Constructor
**Status**: ✅ Production-Ready (Phase A)
**License**: Internal use only (EcomLM Codexa system)

---

> 🎯 **Goal**: Enable complete market research execution with 1 command
> 📚 **Principle**: Workflows that LLMs can follow conversationally OR scripts can automate
> ✅ **Success**: Quality research in 20-30 minutes with ≥0.75 quality score
