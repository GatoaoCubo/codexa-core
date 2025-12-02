# LIVRO: Marketplace
## CAPÍTULO 19

**Versículos consolidados**: 27
**Linhas totais**: 1179
**Gerado em**: 2025-11-13 18:45:49

---


<!-- VERSÍCULO 1/27 - marketplace_optimization__python_implementation_código_20251113.md (133 linhas) -->

# 🐍 Python Implementation (Código)

**Categoria**: marketplace_optimization
**Qualidade**: 0.95/1.00
**Data**: 20251113

## Conteúdo

### Localização: `app/server/`

#### 1. research_agent_models.py (700+ linhas)

**Conteúdo**:
- Data models para todos os agentes
- Enums para tipos de pesquisa
- Schemas JSON para inputs/outputs
- Validação Pydantic

**Classes**:
```
- ResearchRequest
- MarketResearchResult
- CompetitiveAnalysisResult
- KeywordResult
- FAQItem
- ChunkOutput
- ValidationMetrics
- MetaAnalysisResult
```

---

#### 2. research_agent_config.py (400+ linhas)

**Conteúdo**:
- Configurações centralizadas de agentes
- Timeouts e limites
- Prompt templates
- Integração com Como Pesquisa framework

**Configurações**:
```python
AGENT_CONFIGS = {
    'market_researcher': {...},
    'competitor_analyst': {...},
    'keyword_extractor': {...},
    ...
}
```

---

#### 3. research_agent_orchestrator.py (500+ linhas)

**Conteúdo**:
- Orquestração principal do pipeline
- Coordenação de agentes
- Agregação de resultados
- Error handling

**Métodos**:
```
- orchestrate_research()
- run_parallel_agents()
- aggregate_results()
- generate_report()
```

---

#### 4. research_agents.py (1000+ linhas)

**Conteúdo**:
- Implementação dos 7 agentes
- Lógica de cada pilar
- Integration com external APIs

**Classes**:
```
- MarketResearchAgent
- CompetitorAnalystAgent
- KeywordExtractorAgent
- FAQCollectorAgent
- DataValidatorAgent
- PromptComposerAgent
```

---

#### 5. research_agent_routes.py (450+ linhas)

**Conteúdo**:
- FastAPI endpoints
- REST API para research
- Request validation
- Response formatting

**Endpoints**:
```
POST /api/research/orchestrate
POST /api/research/analyze-market
POST /api/research/analyze-competitors
POST /api/research/extract-keywords
POST /api/research/compose-prompts
GET /api/research/status/{request_id}
```

---

#### 6. research_agent_meta.py (500+ linhas)

**Conteúdo**:
- Meta-research system
- Quality scoring
- Performance tracking
- Optimization engine

**Funcionalidades**:
```
- Quality scoring (0-100)
- Efficiency analysis
- Bottleneck detection
- Recommendations generation
```

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Python, Implementation, Código

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 2/27 - marketplace_optimization__qual_usar_20251113.md (41 linhas) -->

# 📍 QUAL USAR?

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Se você quer **MÁXIMO detalhe com exemplos**
👉 **`PROMPT_NOVO_TERMINAL_FINAL.md`**
- Explicação completa de cada passo
- Scripts Python inclusos
- Exemplos de comandos
- Estrutura esperada mostrada

### Se você quer **detalhes sem ser longo**
👉 **`PROMPT_ESCALAR_LEM_NOVO_TERMINAL.txt`**
- Descrição clara de cada etapa
- Requisitos bem definidos
- Estrutura do output esperada

### Se você quer **simples e direto**
👉 **`PROMPT_DISTILLACAO_SIMPLES.txt`**
- Passos principais
- Sem muitos detalhes
- Rápido de ler

### Se você quer **ULTRA conciso**
👉 **`PROMPT_ULTRA_CONCISO.txt`**
- Uma página
- Essencial apenas
- Máxima velocidade

---

**Tags**: concrete, general

**Palavras-chave**: USAR, QUAL

**Origem**: unknown


---


<!-- VERSÍCULO 3/27 - marketplace_optimization__qualidade_do_knowledge_distillation_20251113.md (37 linhas) -->

# 📊 Qualidade do Knowledge Distillation

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Métricas

| Métrica | Valor |
|---------|-------|
| **Total Agents** | 3 |
| **Prompts Extraídos** | 12 |
| **Comportamentos** | 3 |
| **Facts from Docs** | 305 |
| **Training Pairs** | 13 |
| **Keywords Únicos** | 91 |
| **Semantic Clusters** | 3 |
| **Completeness** | 100% |
| **Coverage** | 100% |

### Validação

✅ Todos os agentes têm prompts associados
✅ Todos os comportamentos têm exemplos
✅ Keywords organizadas em clusters semânticos
✅ Dataset estruturado e pronto para treinamento

---

**Tags**: general, intermediate

**Palavras-chave**: Distillation, Knowledge, Qualidade

**Origem**: unknown


---


<!-- VERSÍCULO 4/27 - marketplace_optimization__qualidade_e_validação_20251113.md (34 linhas) -->

# 📊 Qualidade e Validação

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### ✅ Validações Implementadas

- [x] Todos os agentes têm prompts associados (100% coverage)
- [x] Todos os comportamentos têm exemplos
- [x] Keywords organizadas em clusters semânticos
- [x] Dataset estruturado e pronto para treinamento
- [x] Pares entrada/saída validados
- [x] Documentação completa

### 📈 Métricas de Qualidade

| Métrica | Valor | Status |
|---------|-------|--------|
| Completeness | 100% | ✅ |
| Coverage | 100% | ✅ |
| Validation Rules | 26 | ✅ |
| Examples | 2+ per agent | ✅ |

---

**Tags**: concrete, general

**Palavras-chave**: Validação, Qualidade

**Origem**: unknown


---


<!-- VERSÍCULO 5/27 - marketplace_optimization__quality_baseline_20251113.md (28 linhas) -->

# 📈 Quality Baseline

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

### Research Quality Metrics

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Quality Score | 85+ / 100 | 82 / 100 | ✅ Near target |
| Data Completeness | 95%+ | 92% | ✅ Good |
| Pillar Coverage | 6/6 | 6/6 | ✅ Complete |
| Keyword Hierarchy | 4 levels | 4 levels | ✅ Complete |
| FAQ Collection | 10+ items | 15+ items | ✅ Exceeds |
| Chunk Generation | 5/5 | 5/5 | ✅ Complete |
| Test Coverage | 80%+ | 65% | ⚠️ Needs improvement |

---

**Tags**: general, intermediate

**Palavras-chave**: Quality, Baseline

**Origem**: unknown


---


<!-- VERSÍCULO 6/27 - marketplace_optimization__quality_metrics_20251113.md (27 linhas) -->

# 📊 Quality Metrics

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Agents Documented | 100% | 3/3 | ✅ |
| Behaviors Captured | 100% | 3/3 | ✅ |
| Prompts Extracted | 100% | 12/12 | ✅ |
| Training Pairs | >10 | 13 | ✅ |
| Keywords (IDK) | >50 | 91 | ✅ |
| Clusters | >2 | 3 | ✅ |
| Completeness | 95%+ | 100% | ✅ |
| Coverage | 95%+ | 100% | ✅ |

---

**Tags**: general, intermediate

**Palavras-chave**: Quality, Metrics

**Origem**: unknown


---


<!-- VERSÍCULO 7/27 - marketplace_optimization__quando_me_chamar_próximos_passos_20251113.md (32 linhas) -->

# 📞 Quando Me Chamar (Próximos Passos)

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

**Depois que ler os 4 documentos, me fale:**

```
1. "Entendi a visão, quero começar"
   → Dou você os scripts prontos (OPÇÃO A)

2. "Quero validar minha versão do plano"
   → Refinamos o YAML juntos (OPÇÃO B)

3. "Estou preso em [seção específica]"
   → Ajudo com esse conceito

4. "Pronto dia 1, qual é dia 2?"
   → Guio você pelo fluxo
```

---

**Tags**: concrete, general

**Palavras-chave**: Quando, Próximos, Chamar, Passos

**Origem**: unknown


---


<!-- VERSÍCULO 8/27 - marketplace_optimization__questions_answered_by_this_index_20251113.md (37 linhas) -->

# 📞 Questions Answered by This Index

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

**Q: Where are the agents defined?**
A: `knowledge_base/agents.json`

**Q: How do I fine-tune a model?**
A: Use `knowledge_base/training_data.jsonl` with OpenAI API

**Q: What keywords should I index on?**
A: See `knowledge_base/idk_index.json` (91 keywords, organized by cluster)

**Q: How do I route a request?**
A: Use `knowledge_base/semantic_clusters.json` to classify, then route

**Q: Is all data validated?**
A: Yes. Run `python scripts/validate_structure.py`

**Q: Where did this knowledge come from?**
A: See `metadata/sources.json` for full traceability

**Q: How often is this updated?**
A: See `metadata/versioning.json` for update history

---

**Tags**: concrete, general

**Palavras-chave**: Questions, Index, Answered

**Origem**: unknown


---


<!-- VERSÍCULO 9/27 - marketplace_optimization__quick_decision_tree_20251113.md (45 linhas) -->

# 🎯 QUICK DECISION TREE

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### I want to implement a feature:
```
/feature → (creates plan) → /implement → /test → /review → /ship
Or use directly: /adw_sdlc_iso
```

### I want to fix a bug:
```
/bug → (creates plan) → /implement → /test → /review → /ship
Or use directly: /adw_plan_build_test_review_iso
```

### I want to do maintenance:
```
/chore → (creates plan) → /implement → /test
Or use directly: /adw_plan_build_test_iso
```

### I want quick patch:
```
/adw_patch_iso (direct patch, no plan)
```

### I want full automation:
```
/adw_sdlc_zte_iso (complete automation + auto-merge)
⚠️ USE WITH CAUTION
```

---

**Tags**: general, intermediate

**Palavras-chave**: TREE, QUICK, DECISION

**Origem**: unknown


---


<!-- VERSÍCULO 10/27 - marketplace_optimization__quick_navigation_20251113.md (46 linhas) -->

# 🚀 Quick Navigation

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### For Quick Research (5-10 min)
→ **[COMO_USAR_RESEARCH_AGENT_SYSTEM.md](COMO_USAR_RESEARCH_AGENT_SYSTEM.md)**
- Use `/research` with quick research type
- Get keywords + basic insights
- Use Chunk 1 + 5 for ad copy

### For Deep Market Analysis (20-30 min)
→ **[.claude/commands/research.md](.claude/commands/research.md)**
- Execute complete workflow
- Review all 6 pillars
- Use all 5 chunks

### For Competitive Intelligence
→ **[.claude/commands/analyze_competitors.md](.claude/commands/analyze_competitors.md)**
- Execute `/analyze_competitors`
- Review gaps and positioning
- Use Chunk 3 for differentiation

### For Keyword Strategy
→ **[.claude/commands/extract_keywords.md](.claude/commands/extract_keywords.md)**
- Execute `/extract_keywords`
- Get 4-level keyword hierarchy
- Use for SEO/SEM campaigns

### For AI Prompt Generation
→ **[.claude/commands/compose_prompts.md](.claude/commands/compose_prompts.md)**
- Execute `/compose_prompts`
- Get 5 ready-to-use prompts
- Copy-paste into Claude/ChatGPT

---

**Tags**: architectural, general

**Palavras-chave**: Navigation, Quick

**Origem**: unknown


---


<!-- VERSÍCULO 11/27 - marketplace_optimization__quick_reference_20251113.md (36 linhas) -->

# ⚡ Quick Reference

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

```bash
# Verificar status
cat knowledge-artifacts/v1/state.json

# Ver estatísticas
cat knowledge-artifacts/v1/orchestrator.log | grep "Estatísticas" -A 10

# Retomar onde parou
python orchestrator_scaled.py \
  --input "BIBLIA_REORGANIZADA" \
  --output "knowledge-artifacts/v1" \
  --resume

# Gerar próxima versão
python orchestrator_scaled.py \
  --input "BIBLIA_REORGANIZADA" \
  --output "knowledge-artifacts/v2" \
  --version "2.0.0"
```

---

**Tags**: general, intermediate

**Palavras-chave**: Reference, Quick

**Origem**: unknown


---


<!-- VERSÍCULO 12/27 - marketplace_optimization__quick_start_20251113.md (84 linhas) -->

# 🚀 Quick Start

**Categoria**: marketplace_optimization
**Qualidade**: 0.95/1.00
**Data**: 20251113

## Conteúdo

### Opção 1: Pesquisa Completa (6 Pilares + 5 Chunks)

```bash
/research
Product Name: Notebook Gamer
Category: Electronics/Computers
Research Type: deep
Marketplace: amazon
Competitor URLs: https://competitor1.com, https://competitor2.com
Include AI Composition: true
```

**Tempo estimado**: 3-5 minutos
**Output**: Complete report + JSON + 5 AI-ready prompts

### Opção 2: Apenas Market Research (Pilar 1)

```bash
/analyze_market
Product Name: Notebook Gamer
Category: Electronics/Computers
Marketplace: amazon
```

**Tempo estimado**: 1-2 minutos
**Output**: Market insights + trends + seasonality

### Opção 3: Apenas Keywords (Pilar 4)

```bash
/extract_keywords
Product Name: Notebook Gamer
Category: Electronics/Computers
Target Marketplace: amazon
Custom Keywords: gaming, development, budget
```

**Tempo estimado**: 1-2 minutos
**Output**: 4-level keyword hierarchy + quality score

### Opção 4: Análise Competitiva (Pilar 2)

```bash
/analyze_competitors
Product Name: Notebook Gamer
Competitor URLs:
- https://samsung.com/notebooks
- https://asus.com/gaming
- https://dell.com/gaming
Our Strengths: price, support, warranty
```

**Tempo estimado**: 2-3 minutos
**Output**: Competitive positioning + gaps + differentiation

### Opção 5: Composição de Prompts (5-Chunk Library)

```bash
/compose_prompts
Use Research Report: (from previous /research execution)
Focus Areas: market, keywords, competitors, ads, copy
Output Format: markdown
Include Context: true
```

**Tempo estimado**: 1-2 minutos
**Output**: 5 AI-ready prompts ready for Claude/ChatGPT

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Quick, Start

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 13/27 - marketplace_optimization__quick_start_2_minutos_20251113.md (40 linhas) -->

# 🎯 Quick Start (2 Minutos)

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Opção A: Usar Baseline LEM Agora
```python
import json

# Carregar dataset pronto
dataset = json.load(open("LEM_knowledge_base/LEM_dataset.json"))

# 3 agentes, 12 prompts, 13 training pairs
print(f"Agentes: {len(dataset['agent_behaviors'])}")
print(f"Prompts: {len(dataset['prompt_examples'])}")
print(f"Training Pairs: {len(dataset['training_pairs'])}")
```

### Opção B: Escalar para 36k Files Agora
```bash
python orchestrator_scaled.py \
  --input "BIBLIA_REORGANIZADA" \
  --output "knowledge_artifacts/v1" \
  --version "1.0.0"

# Deixa rodar overnight ~4-6 horas
# Sai com v1.0.0 completo (200k+ facts)
```

---

**Tags**: concrete, general

**Palavras-chave**: Minutos, Start, Quick

**Origem**: unknown


---


<!-- VERSÍCULO 14/27 - marketplace_optimization__quick_start_5_minutos_20251113.md (42 linhas) -->

# ⚡ Quick Start (5 Minutos)

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### 1. Adicione um documento

```bash
cp your_ecommerce_guide.md ecommerce-canon/GENESIS/RAW/
```

### 2. Processe com distiller

```bash
cd ecommerce-canon
python AGENTS/distiller.py GENESIS/RAW/your_ecommerce_guide.md GENESIS/PROCESSING
```

### 3. Organize chunks

Chunks aparecem em `GENESIS/PROCESSING/chunks_000.json`:
- Cada um tem entropy (0-100), deus-vs-todo, livro/capítulo sugerido
- Crie VERSÍCULOS em `LIVRO_XX/CAPÍTULO_YY/VERSÍCULO_ZZ.md`

### 4. Versione

```bash
git add ecommerce-canon/
git commit -m "CANON_ADD: LIVRO_03 - Inventory Knowledge"
```

---

**Tags**: ecommerce, implementation

**Palavras-chave**: Quick, Start, Minutos

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 15/27 - marketplace_optimization__quick_start_paths_20251113.md (47 linhas) -->

# 🚀 Quick Start Paths

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Path 1: Command Line (Fastest)
```bash
/research \
  Product Name: Wireless Speaker \
  Category: Electronics \
  Research Type: quick
```
**Time to results**: 5-10 min

### Path 2: REST API (Integration)
```bash
curl -X POST http://localhost:8000/api/research/start \
  -H "Content-Type: application/json" \
  -d '{"product_name":"...",...}'
```
**Time to results**: 20-30 min

### Path 3: Python API (Programmatic)
```python
orchestrator = ResearchAgentOrchestrator()
report = await orchestrator.process_research_request(request)
```
**Time to results**: 20-30 min

### Path 4: Individual Agents (Granular)
```python
agent = MarketResearchAgent()
result = await agent.execute(request, report)
```
**Time to results**: 5 min per agent

---

**Tags**: ecommerce, general, implementation

**Palavras-chave**: Start, Paths, Quick

**Origem**: unknown


---


<!-- VERSÍCULO 16/27 - marketplace_optimization__quick_start_workflows_20251113.md (89 linhas) -->

# 🚀 Quick Start Workflows

**Categoria**: marketplace_optimization
**Qualidade**: 0.95/1.00
**Data**: 20251113

## Conteúdo

### Workflow 1: Nova Pesquisa (5-10 min)

```
1. Execute: /research (quick mode)
   Input: Product name + Category + Marketplace

2. Review: Markdown report (all 6 pillars)

3. Use: Chunk 1 + Chunk 5 para ad copy rápida

4. Output: Relatório + 5 chunks prontos
```

---

### Workflow 2: Análise Competitiva (10-15 min)

```
1. Execute: /analyze_competitors
   Input: Product + Competitor URLs

2. Review: Gaps and positioning (Pilar 2)

3. Use: Chunk 3 para diferenciação

4. Output: Strategic positioning insights
```

---

### Workflow 3: Keywords para SEM/SEO (3-5 min)

```
1. Execute: /extract_keywords
   Input: Product + Category

2. Review: 4-level keyword hierarchy

3. Use: Head + Mid-tail para campaigns

4. Output: 50-200 keywords estruturadas
```

---

### Workflow 4: Composição de Prompts (15-20 min)

```
1. Execute: /research (deep mode)
   → Gera completa research + JSON

2. Execute: /compose_prompts
   Input: Research report request_id

3. Copy: 5 chunks para Claude/ChatGPT

4. Use: Para copywriting em escala
```

---

### Workflow 5: Automação com ADW

```
1. Configure: GITHUB_REPO_URL + API keys

2. Execute: adw_plan_build_test_review_iso.py <issue-number>

3. Auto-trigger: /research quando issue criada

4. Auto-commit: Results como PR
```

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Quick, Start, Workflows

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 17/27 - marketplace_optimization__quick_validation_20251113.md (38 linhas) -->

# 🎯 Quick Validation

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

Depois da execução, validar:

```bash
# 1. Ver resumo
cat RAW_LEM_v1.1_PADDLEOCR/DISTILLATION_SUMMARY.json

# 2. Contar resultados
echo "Training pairs:"
wc -l training_pairs_paddleocr.jsonl

echo "Semantic tokens:"
python -c "import json; m=json.load(open('RAW_LEM_v1.1_PADDLEOCR/semantic_map.json')); print(len(m))"

# 3. Inspecionar primeiros tokens
python -c "
import json
m = json.load(open('RAW_LEM_v1.1_PADDLEOCR/semantic_map.json'))
for token in list(m.keys())[:10]:
    print(f'  {token}: {len(m[token])} files')
"
```

---

**Tags**: general, intermediate

**Palavras-chave**: Quick, Validation

**Origem**: unknown


---


<!-- VERSÍCULO 18/27 - marketplace_optimization__recomendação_final_20251113.md (34 linhas) -->

# 🎯 Recomendação Final

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

**Para você, recomendo:**

### ✅ CAMINHO A (Rápido - Recomendado)

**Hoje:**
1. Setup repo (20 min) - Rodar os 3 comandos Git LFS acima
2. Copiar orchestrator para scripts/
3. Rodar Fase 1 (scan) - 30 segundos, valida tudo funciona

**Tomorrow (noite):**
4. Rodar Fases 2-5 overnight
5. Acordar com v1.0.0 pronto

**Próximo dia:**
6. Testar, fazer deploy, usar em production

**Total: ~1 dia de setup + processamento**

---

**Tags**: concrete, general

**Palavras-chave**: Final, Recomendação

**Origem**: unknown


---


<!-- VERSÍCULO 19/27 - marketplace_optimization__recommended_implementation_order_20251113.md (55 linhas) -->

# 🚀 Recommended Implementation Order

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### Week 1: High Impact (Days 1-4)
```
Day 1: Pilar 5 Expansion (15-20 min)
       ↓
Day 2: Pilar 6 Enhancement (15-20 min)
       ↓
Day 3: Meta-Research V2 (20-30 min)
       ↓
Day 4: E2E Tests (15-20 min)

Cumulative Time: ~75 min | Impact: +40% system capability
```

### Week 2: Marketplace & Performance (Days 5-8)
```
Day 5: Marketplace Optimization (20-30 min)
       ↓
Day 6: Performance - Parallel Execution (20-30 min)
       ↓
Day 7: API Integration (30-45 min)
       ↓
Day 8: Testing & Validation (15 min)

Cumulative Time: ~110 min | Impact: +35% user experience
```

### Week 3: Polish & Advanced (Days 9-12)
```
Day 9:  Visualization Layer (30-45 min)
        ↓
Day 10: Como Pesquisa Templates (15-20 min)
        ↓
Day 11: Advanced HOPs (30-45 min)
        ↓
Day 12: Integration Testing & Docs (30 min)

Cumulative Time: ~150 min | Impact: +25% advanced features
```

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Recommended, Implementation, Order

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 20/27 - marketplace_optimization__recursos_por_tópico_20251113.md (35 linhas) -->

# 🔧 Recursos por Tópico

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Para Iniciantes
- Leia primeiro: `01_framework/research_framework.md`
- Depois: `02_prompt_composition/prompt_templates.md`
- Pratique com: `07_templates/research_report_template.md`

### Para Pesquisadores
- Deep dive: `03_research_methodology/` (todos os arquivos)
- Metodologias avançadas: `04_marketplace_research/`
- Validação: `04_marketplace_research/data_validation.md`

### Para Criadores de Anúncios
- Framework: `05_ad_composition/ad_structure.md`
- Storytelling: `05_ad_composition/storytelling_guide.md`
- Templates: `07_templates/ad_brief_template.md`

### Para Desenvolvedores
- Integração: `06_tools_integration/api_integration.md`
- Automação: `06_tools_integration/automation_scripts.md`

---

**Tags**: abstract, general

**Palavras-chave**: Recursos, Tópico

**Origem**: unknown


---


<!-- VERSÍCULO 21/27 - marketplace_optimization__reexecução_do_pipeline_20251113.md (32 linhas) -->

# 🔧 Reexecução do Pipeline

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

Para atualizar o dataset quando novos agentes forem criados:

```bash
# Adicione novos agentes em:
# C:\Users\Dell\Desktop\PaddleOCR-main\BIBLIA_REORGANIZADA\CODEXA\AGENTE\

# Execute novamente:
python LEM_knowledge_distillation.py

# Isto regenerará:
# - LEM_dataset.json
# - LEM_IDK_index.json
# - LEM_training_data.jsonl
# - Todos os relatórios
```

---

**Tags**: concrete, general

**Palavras-chave**: Reexecução, Pipeline

**Origem**: unknown


---


<!-- VERSÍCULO 22/27 - marketplace_optimization__referência_rápida_20251113.md (28 linhas) -->

# 📞 Referência Rápida

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

| Comando | O que faz |
|---------|-----------|
| `git status` | Ver status do repositório |
| `git add .` | Preparar todas mudanças |
| `git add arquivo` | Preparar um arquivo específico |
| `git commit -m "msg"` | Criar commit |
| `git push` | Enviar para GitHub |
| `git pull` | Baixar de GitHub |
| `git log` | Ver histórico |
| `git diff` | Ver mudanças |
| `git branch` | Ver branches |

---

**Tags**: general, intermediate

**Palavras-chave**: Referência, Rápida

**Origem**: unknown


---


<!-- VERSÍCULO 23/27 - marketplace_optimization__referências_de_scripts_20251113.md (25 linhas) -->

# 📚 Referências de Scripts

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

| Script | Propósito | Tempo |
|--------|-----------|-------|
| `distill_paddleocr_knowledge.py` | Análise + catalogação | 15-30m |
| `select_master_files.py` | Deduplicação | 2-5m |
| `optimize_lem_leverage.py` | Otimização 4 táticas | 5-10m |
| `integrate_paddleocr_to_lem.py` | Integração merge | 3-5m |
| `enrich_lem_v1_1.py` | Enriquecimento final | 2-3m |
| `run_complete_lem_enrichment.py` | Orquestra tudo | 30-60m |

---

**Tags**: concrete, general

**Palavras-chave**: Scripts, Referências

**Origem**: unknown


---


<!-- VERSÍCULO 24/27 - marketplace_optimization__related_documentation_20251113.md (22 linhas) -->

# 📚 Related Documentation

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

- **ADW Complete Index**: `ADW_COMMANDS_COMPLETE_INDEX.md`
- **Research Agents Index**: `RESEARCH_AGENT_INDEX.md`
- **Research Enrichment**: `RESEARCH_AGENT_ENRICHMENT_SUMMARY.md`
- **Research Usage Guide**: `COMO_USAR_RESEARCH_AGENT_SYSTEM.md`
- **Como Pesquisa Framework**: `app/como_pesquisa/`

---

**Tags**: abstract, general

**Palavras-chave**: Documentation, Related

**Origem**: unknown


---


<!-- VERSÍCULO 25/27 - marketplace_optimization__related_resources_20251113.md (28 linhas) -->

# 🔗 RELATED RESOURCES

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

- **ADW System Docs**: `adws/README.md`
- **ADW Quick Start**: `ADW_EXECUTION_QUICK_START.md`
- **Research Agents**: `RESEARCH_AGENT_INDEX.md`
- **Framework**: `app/como_pesquisa/`

---

**Last Updated**: November 2024
**Status**: ✅ Complete reference
**Ready for**: Automation + Research Enhancement


======================================================================

**Tags**: abstract, general

**Palavras-chave**: RELATED, RESOURCES

**Origem**: unknown


---


<!-- VERSÍCULO 26/27 - marketplace_optimization__research_workflow_20251113.md (40 linhas) -->

# 🔄 Research Workflow

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### 8 Phases (Sequential/Parallel)
1. **PLANNING** - Initialization
2. **MARKET_RESEARCH** - Market analysis
3. **COMPETITIVE_ANALYSIS** - Competitor intelligence
4. **KEYWORD_EXTRACTION** - SEO keyword hierarchy
5. **FAQ_COLLECTION** - Objections & answers
6. **DATA_VALIDATION** - Quality assurance
7. **PROMPT_COMPOSITION** - AI prompt generation
8. **REPORT_GENERATION** - Final assembly

### 5 Research Types
- **Quick** (5-10 min) - Market + Keywords + Prompts
- **Deep** (20-30 min) - All phases
- **Keywords Only** (2-5 min) - SEO focused
- **Competitors** (10-15 min) - Competitive analysis
- **AI-Assisted** (5-15 min) - Claude-powered

### 5-Chunk Prompt Library
1. Research Consolidation
2. Keyword Analysis
3. Competitor Insights
4. Ad Brief Generation
5. Copy Optimization

---

**Tags**: general, intermediate

**Palavras-chave**: Workflow, Research

**Origem**: unknown


---


<!-- VERSÍCULO 27/27 - marketplace_optimization__resultados_da_destilação_20251113.md (44 linhas) -->

# 📊 Resultados da Destilação

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

```
INPUT:
  - Caminho: C:\Users\Dell\Desktop\PaddleOCR-main
  - Arquivos: 113.864
  - Tamanho: ~3.5GB
  - Extensões: 139 tipos diferentes

OUTPUT:
  - Tokens semânticos: 17.082
  - Arquivos únicos: 113.863
  - Duplicatas: 1
  - Status: ✅ COMPLETE
```

### Distribuição de Tipos de Arquivo

**Top 10 Extensões**:
- `.pyi` - 17.180 (type stubs)
- `.html` - 11.713 (documentação web)
- `.txt` - 9.968 (texto)
- `.ts` - 8.725 (TypeScript)
- `.md` - 6.994 (Markdown)
- `.js` - 6.701 (JavaScript)
- `.tsx` - 6.153 (React/TypeScript)
- `.png` - 6.616 (imagens)
- `.cpp` - 3.916 (C++ code)
- `.h` - 4.302 (headers)

---

**Tags**: ecommerce, concrete

**Palavras-chave**: Resultados, Destilação

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- FIM DO CAPÍTULO 19 -->
<!-- Total: 27 versículos, 1179 linhas -->
