# LIVRO: Marketplace
## CAPÍTULO 8

**Versículos consolidados**: 23
**Linhas totais**: 1162
**Gerado em**: 2025-11-13 18:45:49

---


<!-- VERSÍCULO 1/23 - marketplace_optimization__checklist_para_começar_20251113.md (42 linhas) -->

# 📋 Checklist para Começar

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

- [ ] Leia README_LEM_ECOMMERCE.md (10 min)
- [ ] Entenda os 6 LIVROS
- [ ] Entenda ENTROPIA e DEUS-VS-TODO
- [ ] Abra novo terminal
- [ ] Copie PROMPT_NOVO_TERMINAL_FINAL.md
- [ ] Cole como prompt
- [ ] Siga passo 1: Encontre documentos
- [ ] Siga passo 2: Copie para RAW/
- [ ] Siga passo 3: Processe com distiller
- [ ] Siga passo 4: Revise chunks
- [ ] Siga passo 5: Organize VERSÍCULOS
- [ ] Siga passo 6: Gere relatório
- [ ] Siga passo 7: Faça commit

---

**Status:** 🟢 **PRONTO PARA USAR**

**Próximo:** Abra novo terminal e copie `PROMPT_NOVO_TERMINAL_FINAL.md`

---

*Created: 2025-11-02*
*LEM v2.1.0 - Large E-Commerce Model*


======================================================================

**Tags**: general, implementation

**Palavras-chave**: Checklist, Começar

**Origem**: unknown


---


<!-- VERSÍCULO 2/23 - marketplace_optimization__checklist_pré_uso_20251113.md (25 linhas) -->

# ✅ CHECKLIST PRÉ-USO

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

Antes de executar a pesquisa, verifique:

- [ ] **Product Name**: Claro e específico
- [ ] **Category**: Classificado corretamente
- [ ] **Marketplace**: Selecionado (amazon, mercado_livre, ebay, generic)
- [ ] **Competitor URLs**: 3-5 URLs válidas (se análise competitiva)
- [ ] **Research Type**: Definido (quick, deep, keywords_only, competitors, ai_assisted)
- [ ] **AI Composition**: Marcado como true se precisa dos chunks

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: CHECKLIST

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 3/23 - marketplace_optimization__checklist_você_está_pronto_para_começar_20251113.md (26 linhas) -->

# 📋 Checklist: Você Está Pronto Para Começar?

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

```
☐ Abri HTML, entendi a visão geral
☐ Li Markdown, validei a lógica
☐ Escaneei estructura-pratica.md (pelo menos 2 seções)
☐ Salvei cheat-sheet.txt numa aba sempre aberta
☐ Tenho espaço em disco: /lcm-ai/ (comece com 5 GB)
☐ Tenho Python 3.8+ (para core.py)
☐ Escolhi: OPÇÃO A (code), B (design) ou C (híbrido)?
```

---

**Tags**: concrete, general

**Palavras-chave**: Pronto, Checklist, Você, Começar, Está

**Origem**: unknown


---


<!-- VERSÍCULO 4/23 - marketplace_optimization__classes_principais_20251113.md (66 linhas) -->

# 🔑 Classes Principais

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### `AgenteEcommerce`

**Métodos principais**:

| Método | Descrição | Fase |
|--------|-----------|------|
| `iniciar_decisao_compra()` | Inicia fluxo | 1 |
| `processar_implementacao()` | Valida ética | 2 |
| `processar_compra()` | Completa transação | 3 |
| `calcular_iec()` | Calcula métrica | 4 |
| `gerar_relatorio()` | Exporta resultados | - |

### `Produto`

Representa item no e-commerce.

**Atributos**:
- `id`: Identificador único
- `nome`: Nome do produto
- `descricao`: Descrição (>50 chars = ética alta)
- `preco`: Preço em reais
- `categoria`: Categoria
- `ética_score`: 0.0-1.0 (manutenção manual)
- `em_estoque`: Disponibilidade

### `Cliente`

Representa cliente e seu estado na jornada.

**Atributos**:
- `id`: Identificador único
- `nome`: Nome
- `email`: Email
- `estagio_jornada`: Seu estado (DESCOBERTA → COMPRA)
- `carrinho`: Produtos no carrinho
- `historico_compras`: Compras anteriores
- `iec_score_percebido`: Satisfação de ética

### `DecisaoCompra`

Representa uma decisão em progresso.

**Atributos**:
- `cliente_id`: Qual cliente
- `produto_id`: Qual produto
- `estagio`: Fase atual (IDENTIFICAÇÃO → MEDIÇÃO)
- `confianca`: Score de ética (0.0-1.0)
- `objecoes`: Problemas encontrados
- `recomendacoes`: Sugestões de melhoria

---

**Tags**: ecommerce, general, implementation

**Palavras-chave**: Classes, Principais

**Origem**: unknown


---


<!-- VERSÍCULO 5/23 - marketplace_optimization__claude_code_commands_20251113.md (26 linhas) -->

# 🎯 Claude Code Commands

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

Five CLI commands for easy access:

```bash
/research                    - Full research workflow
/analyze_market             - Market research phase
/analyze_competitors        - Competitive analysis phase
/extract_keywords           - Keyword extraction phase
/compose_prompts            - AI prompt composition
```

---

**Tags**: general, intermediate

**Palavras-chave**: Claude, Commands, Code

**Origem**: unknown


---


<!-- VERSÍCULO 6/23 - marketplace_optimization__cli_commands_execução_20251113.md (112 linhas) -->

# 💻 CLI Commands (Execução)

**Categoria**: marketplace_optimization
**Qualidade**: 0.95/1.00
**Data**: 20251113

## Conteúdo

### Command: /research (Main Orchestrator)

**Localização**: `.claude/commands/research.md`
**Linhas**: 700+
**Steps**: 8 steps com 0-level prompts

**Uso**:
```bash
/research
  Product Name: [seu produto]
  Category: [categoria]
  Marketplace: [marketplace]
  Research Type: [quick|deep|custom]
```

**Output**:
- Relatório Markdown (6 pilares)
- JSON estruturado
- 5 chunks de prompts
- Métricas de qualidade

**Fluxo**:
```
Input Parsing → Pilar 1 (Market) → Pilar 2 (Competitors) →
Pilar 3 (Product) → Pilar 4 (Keywords) → Pilar 5+6 (Trends+FAQ) →
Validation → 5-Chunk Composition → Meta-Research → Final Report
```

---

### Command: /analyze_market (Pilar 1)

**Localização**: `.claude/commands/analyze_market.md`
**Linhas**: 430+
**Steps**: 7 steps

**Uso**:
```bash
/analyze_market
  Product Name: [seu produto]
  Marketplace: [marketplace]
```

**Output**: Market research com size, growth, pricing, channels

---

### Command: /analyze_competitors (Pilar 2)

**Localização**: `.claude/commands/analyze_competitors.md`
**Linhas**: 430+
**Steps**: 8 steps

**Uso**:
```bash
/analyze_competitors
  Product Name: [seu produto]
  Competitor URLs: [url1, url2, url3]
```

**Output**: Competitive analysis com gaps e positioning

---

### Command: /extract_keywords (Pilar 4)

**Localização**: `.claude/commands/extract_keywords.md`
**Linhas**: 440+
**Steps**: 8 steps

**Uso**:
```bash
/extract_keywords
  Product Name: [seu produto]
  Category: [categoria]
```

**Output**: Keywords em 4 níveis (50-200 keywords total)

---

### Command: /compose_prompts (5-Chunk Library)

**Localização**: `.claude/commands/compose_prompts.md`
**Linhas**: 710+
**Steps**: 9 steps

**Uso**:
```bash
/compose_prompts
  Use Research Report: [request_id]
  Output Format: [markdown|json|both]
```

**Output**: 5 chunks prontos para copiar-colar em Claude/ChatGPT

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Commands, Execução

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 7/23 - marketplace_optimization__coleta_organizada_20251113.md (80 linhas) -->

# 🗂️ Coleta Organizada

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Exemplo Prático Completo

**Produto**: Notebook Gamer Intel i7 16GB para Desenvolvimento

#### KEYWORDS COLETADAS (do Mercado Livre):
```
Head Keywords (da barra de sugestões):
- notebook gamer
- notebook i7
- notebook 16gb
- notebook barato

Mid-tail (dos títulos dos top 5):
- notebook gamer i7 16gb
- notebook intel i7 16gb ssd
- notebook gamer 16gb promo
- notebook i7 novo promocao

Long-tail (combinações específicas):
- notebook gamer intel i7 16gb ssd 512gb rtx
- notebook para desenvolvimento webcom i7
- notebook gamer barato sem superaquecimento
```

#### FAIXA DE PREÇO:
```
Mínimo: R$ 2.800 (marca desconhecida)
Máximo: R$ 6.900 (marca premium)
Modal: R$ 4.200-4.800
Sugestão para seu produto: R$ 4.499
```

#### TOP 5 CONCORRENTES:
```
1. Samsung Galaxy Book (4.8⭐, 1.2k reviews)
   - Preço: R$ 5.200
   - Diferencial: Design + bateria

2. ASUS Vivobook (4.7⭐, 980 reviews)
   - Preço: R$ 4.500
   - Diferencial: Preço + performance

3. Dell G15 (4.6⭐, 850 reviews)
   - Preço: R$ 5.800
   - Diferencial: Suporte Dell

4. Positivo Intel Core (4.5⭐, 650 reviews)
   - Preço: R$ 3.900
   - Diferencial: Preço super baixo

5. [Your Future Position]
   - Preço: R$ 4.499
   - Diferencial: Suporte em português + ventilação
```

#### PERGUNTAS FREQUENTES (coletadas):
```
1. "Roda Fortnite/PUBG em 60 FPS?" (menção 45x)
2. "Qual é a melhor marca?" (menção 32x)
3. "Aquece muito?" (menção 28x)
4. "Devolve em 30 dias?" (menção 25x)
5. "Bateria dura quantas horas?" (menção 18x)
```

---

**Tags**: architectural, general

**Palavras-chave**: Coleta, Organizada

**Origem**: unknown


---


<!-- VERSÍCULO 8/23 - marketplace_optimization__comando_único_para_começar_20251113.md (40 linhas) -->

# 🚀 COMANDO ÚNICO PARA COMEÇAR

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```bash
# Tudo em uma linha (vai levar ~4-6 horas)

python orchestrator_scaled.py \
  --input "C:\Users\Dell\Desktop\PaddleOCR-main\BIBLIA_REORGANIZADA" \
  --output "knowledge_artifacts/v1" \
  --version "1.0.0" \
  --batch-size 500 \
  --workers 8
```

**Então:**
```bash
# Depois de completo, versionar
cd seu-repo

git add knowledge-artifacts/v1/
git tag -a "kb-v1.0.0" -m "36k files processed, 200k facts, 200 clusters"
git push origin kb-v1.0.0

# Para baixar depois
git clone --depth 1 --branch kb-v1.0.0 seu-repo knowledge-v1
```

---

**Tags**: general, implementation

**Palavras-chave**: COMEÇAR, ÚNICO, COMANDO

**Origem**: unknown


---


<!-- VERSÍCULO 9/23 - marketplace_optimization__comandos_úteis_do_git_20251113.md (56 linhas) -->

# 🛠️ Comandos Úteis do Git

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Para Desfazer Mudanças

```bash
# Remover arquivo de staging (não commitou ainda)
git restore --staged nome_arquivo

# Descartar mudanças de um arquivo
git restore nome_arquivo

# Voltar último commit (mantém mudanças)
git reset HEAD~1
```

### Para Corrigir Último Commit

```bash
# Adicionar arquivo faltante ao último commit
git add arquivo_faltante
git commit --amend --no-edit

# Mudar mensagem do último commit
git commit --amend -m "Nova mensagem"
```

### Ver Status

```bash
# Status completo
git status

# Status resumido
git status -s

# Log simples
git log --oneline

# Log com mais detalhes
git log --oneline --graph --all
```

---

**Tags**: general, intermediate

**Palavras-chave**: Úteis, Comandos

**Origem**: unknown


---


<!-- VERSÍCULO 10/23 - marketplace_optimization__comece_agora_20251113.md (65 linhas) -->

# 🎬 COMECE AGORA

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Passo 1: Entender (5 min)
```
Leia este arquivo até aqui
```

### Passo 2: Preparar (20 min)
```bash
cd seu-repo
# Run os 3 comandos Git LFS
# Copy orchestrator_scaled.py para scripts/
git commit -m "chore: setup knowledge distillation"
```

### Passo 3: Validar (2 min)
```bash
python orchestrator_scaled.py \
  --input "BIBLIA_REORGANIZADA" \
  --output "knowledge-artifacts/v1" \
  --phase 1
# Deve mostrar: 36,377 arquivos
```

### Passo 4: Executar (4-6 horas)
```bash
python orchestrator_scaled.py \
  --input "BIBLIA_REORGANIZADA" \
  --output "knowledge-artifacts/v1" \
  --version "1.0.0"
# Deixa rodar overnight
```

### Passo 5: Versionar (5 min)
```bash
git add knowledge-base/v1/
git tag -a "kb-v1.0.0" -m "36k files, 200k facts, 200 clusters"
git push origin kb-v1.0.0
```

---

**Pronto para começar?** 🚀

Você quer que eu:
1. Prepare o setup completo no seu repo?
2. Crie scripts auxiliares para monitoring?
3. Configure CI/CD para atualização automática?
4. Começar agora mesmo com o orchestrador?


======================================================================

**Tags**: concrete, general

**Palavras-chave**: COMECE, AGORA

**Origem**: unknown


---


<!-- VERSÍCULO 11/23 - marketplace_optimization__começo_real_segunda_feira_20251113.md (54 linhas) -->

# 🚀 Começo REAL (Segunda-Feira)

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### MANHÃ
```
09:00 - Abrir lcm-ai-visual-didatica.html
        Ler com calma, anotar insights
        [15 min]

09:15 - Abrir lcm-ai-visual-didatica.md
        Validar conceitos no seu próprio ritmo
        [30 min]

09:45 - Decidir: OPÇÃO A, B ou C?
        (Me chamar para confirmar)
        [5 min]
```

### TARDE
```
14:00 - Se OPÇÃO A ou C:
        Abrir lcm-ai-estructura-pratica.md
        Entender config.yaml + estrutura -02_build/
        [30 min]

14:30 - Terminal:
        mkdir -p lcm-ai/{...}
        touch config.yaml
        [5 min]

14:35 - Copiar estrutura básica de lcm-ai-estructura-pratica.md
        config.yaml preenchido com valores iniciais
        [15 min]

14:50 - Criar stubs de Skills (funções vazias em Python)
        [30 min]

15:20 - FIM DO DIA 1
        Você tem: Árvore estruturada + pesos iniciais + Skills vazios
```

---

**Tags**: general, intermediate

**Palavras-chave**: Segunda, REAL, Começo, Feira

**Origem**: unknown


---


<!-- VERSÍCULO 12/23 - marketplace_optimization__command_matrix_20251113.md (32 linhas) -->

# 📊 COMMAND MATRIX

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

| Command | Phases | Time | Requires ID | Auto-Ship | Use Case |
|---------|--------|------|-------------|-----------|----------|
| `/adw_plan_iso` | Plan | 5-10 min | ❌ | ❌ | Planning only |
| `/adw_build_iso` | Build | 5-10 min | ✅ | ❌ | Build only |
| `/adw_test_iso` | Test | 5 min | ✅ | ❌ | Test only |
| `/adw_review_iso` | Review | 5 min | ✅ | ❌ | Review only |
| `/adw_document_iso` | Doc | 5 min | ✅ | ❌ | Doc only |
| `/adw_ship_iso` | Ship | 2 min | ✅ | ✅ | Deploy only |
| `/adw_plan_build_iso` | Plan+Build | 10-15 min | ❌ | ❌ | Quick implementation |
| `/adw_plan_build_test_iso` | P+B+T | 15-20 min | ❌ | ❌ | Tested impl |
| `/adw_plan_build_review_iso` | P+B+R | 12-18 min | ❌ | ❌ | Reviewed (skip test) |
| `/adw_plan_build_test_review_iso` | P+B+T+R | 20-25 min | ❌ | ❌ | Tested+Reviewed |
| `/adw_sdlc_iso` | All | 30-45 min | ❌ | ❌ | Complete workflow |
| `/adw_sdlc_zte_iso` | All+Ship | 35-50 min | ❌ | ✅ | Full automation |
| `/adw_patch_iso` | Patch | 5-10 min | ❌ | ❌ | Quick patch |

---

**Tags**: general, implementation

**Palavras-chave**: MATRIX, COMMAND

**Origem**: unknown


---


<!-- VERSÍCULO 13/23 - marketplace_optimization__commands_for_each_enhancement_type_20251113.md (61 linhas) -->

# 🛠️ Commands for Each Enhancement Type

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### For Tier 1 (Quick Win) Enhancements:
```bash
# Fastest path (15-20 min)
/adw_plan_build_test_iso
[Enhancement description]
```

### For Tier 2 (Medium) Enhancements:
```bash
# Full cycle with review (20-30 min)
/adw_plan_build_test_review_iso
[Enhancement description]

# Then
/pull_request
```

### For Tier 3 (Advanced) Enhancements:
```bash
# Full SDLC without auto-merge (35-50 min)
/adw_sdlc_iso
[Enhancement description]

# Then manual review and deployment
/pull_request
```

### For Parallel Execution:
```bash
# Start 3 independent enhancements in parallel
/adw_plan_build_test_iso
Enhancement 1: [Description]

# In another instance:
/adw_plan_build_test_iso
Enhancement 2: [Description]

# In another instance:
/adw_plan_build_test_iso
Enhancement 3: [Description]

# Track all with:
/track_agentic_kpis
```

---

**Tags**: ecommerce, concrete

**Palavras-chave**: Commands, Each, Enhancement, Type

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 14/23 - marketplace_optimization__commit_message_20251113.md (51 linhas) -->

# 🔐 Commit Message

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

```
feat: Implement complete Research Agent System with 7 specialized agents

Add comprehensive multi-agent research framework with:

Core System (3,550+ lines production-ready code):
- research_agent_models.py: 15+ Pydantic models with enums and validation
- research_agent_config.py: Central configuration for all agents and workflows
- research_agent_orchestrator.py: Master coordinator for research workflows
- research_agents.py: 7 specialized agents
- research_agent_routes.py: 7 FastAPI endpoints for REST API access
- research_agent_meta.py: Self-improving meta-research system with KPI tracking

Commands (5 Claude Code CLI commands):
- /research: Full research workflow (all phases)
- /analyze_market: Market research phase only
- /analyze_competitors: Competitive analysis phase only
- /extract_keywords: Keyword extraction phase only
- /compose_prompts: AI prompt composition using 5-chunk library

Documentation (6,000+ lines):
- RESEARCH_AGENT_SYSTEM.md: Complete system documentation and architecture
- INTEGRATION_GUIDE.md: How to integrate into existing FastAPI app
- RESEARCH_AGENT_INDEX.md: Master navigation and quick reference

Architecture:
- 1 prompt = 1 agent = 1 reason (single responsibility principle)
- 8 research phases with structured workflow
- 5 types of research (quick, deep, keywords_only, competitors, ai_assisted)
- Inter-agent communication via AgentMessage protocol
- Dense keywords system for file-based communication
- Quality scoring (0-100) on all research phases
- Meta-research system for continuous optimization
```

---

**Tags**: abstract, general

**Palavras-chave**: Commit, Message

**Origem**: unknown


---


<!-- VERSÍCULO 15/23 - marketplace_optimization__commits_principais_20251113.md (23 linhas) -->

# 📝 Commits Principais

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

| Hash | Mensagem |
|------|----------|
| 2feb84e | Merge consolidate-features: integrate paddleocr and genesis features into main |
| 5123df3 | s |
| 171bf4b | docs: Consolidate all research artifacts into unified MASTER reference document |
| 4489cf0 | docs: Add strategic planning and tracking documents for Phase 4 |

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Commits, Principais

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 16/23 - marketplace_optimization__common_issues_fixes_20251113.md (24 linhas) -->

# 🚨 Common Issues & Fixes

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

| Issue | Fix |
|-------|-----|
| Slow research (>10 min) | Use `Research Type: quick` |
| Low quality score (<60%) | Add competitor URLs |
| Chunks not appearing | Ensure `Include AI Composition: true` |
| JSON format issues | Re-run `/research` |
| Keywords are generic | Adjust `Research Type` to `deep` |

---

**Tags**: general, intermediate

**Palavras-chave**: Common, Issues, Fixes

**Origem**: unknown


---


<!-- VERSÍCULO 17/23 - marketplace_optimization__common_workflows_20251113.md (52 linhas) -->

# 🎯 Common Workflows

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Workflow 1: New Product Launch
1. Read: [COMO_USAR_RESEARCH_AGENT_SYSTEM.md](COMO_USAR_RESEARCH_AGENT_SYSTEM.md)
2. Execute: `/research` (deep mode)
3. Review: All 6 pillars in markdown report
4. Use: 5 chunks for ad creation
5. Reference: [research_framework.md](app/como_pesquisa/01_framework/research_framework.md)

**Time**: 10-15 minutes

### Workflow 2: Competitive Analysis
1. Read: [analyze_competitors.md](.claude/commands/analyze_competitors.md)
2. Execute: `/analyze_competitors`
3. Review: Gaps and differentiation
4. Use: Chunk 3 for positioning strategy
5. Reference: [competitive_analysis.md](app/como_pesquisa/03_research_methodology/competitive_analysis.md)

**Time**: 5-10 minutes

### Workflow 3: SEO/SEM Campaign
1. Read: [extract_keywords.md](.claude/commands/extract_keywords.md)
2. Execute: `/extract_keywords`
3. Review: 4-level keyword hierarchy
4. Use: High-priority keywords for campaigns
5. Reference: [keyword_hierarchy.md](app/como_pesquisa/01_framework/keyword_hierarchy.md)

**Time**: 3-5 minutes

### Workflow 4: AI-Powered Copywriting
1. Read: [COMO_USAR_RESEARCH_AGENT_SYSTEM.md](COMO_USAR_RESEARCH_AGENT_SYSTEM.md)
2. Execute: `/research` (deep mode)
3. Get: 5 AI-ready prompts
4. Copy: Chunk 4 + 5 to Claude/ChatGPT
5. Reference: [prompt_chunks_guide.md](app/como_pesquisa/02_prompt_composition/prompt_chunks_guide.md)

**Time**: 15-20 minutes

---

**Tags**: abstract, general

**Palavras-chave**: Workflows, Common

**Origem**: unknown


---


<!-- VERSÍCULO 18/23 - marketplace_optimization__como_executar_20251113.md (42 linhas) -->

# 🎬 Como Executar

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Automático (Recomendado)
```bash
cd C:\Users\Dell\tac-7
python run_complete_lem_enrichment.py
```
⏱️ Tempo: 30-60 minutos
✅ Inclui validação automática

### Manual (Controle Total)
```bash
# 1. Destilação (atual - em progresso)
python distill_paddleocr_knowledge.py

# 2. Deduplicação
python select_master_files.py "RAW_LEM_v1.1_PADDLEOCR/duplicates_report.json" "C:\Users\Dell\Desktop\PaddleOCR-main"

# 3. Otimização
python optimize_lem_leverage.py

# 4. Integração
python integrate_paddleocr_to_lem.py

# 5. Enriquecimento
python enrich_lem_v1_1.py
```

---

**Tags**: general, intermediate

**Palavras-chave**: Executar, Como

**Origem**: unknown


---


<!-- VERSÍCULO 19/23 - marketplace_optimization__como_fazer_commits_4_passos_20251113.md (37 linhas) -->

# 🎓 Como Fazer Commits (4 Passos)

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

Sempre que precisar fazer mudanças:

```bash
# 1. Verificar status
git status

# 2. Preparar arquivos
git add .

# 3. Fazer commit
git commit -m "🚀 Descrição da mudança"

# 4. Enviar para GitHub
git push origin main
```

**Ou em uma linha:**
```bash
git add . && git commit -m "🚀 Descrição" && git push origin main
```

---

**Tags**: general, intermediate

**Palavras-chave**: Commits, Passos, Como, Fazer

**Origem**: unknown


---


<!-- VERSÍCULO 20/23 - marketplace_optimization__como_integrar_o_lem_20251113.md (116 linhas) -->

# 🚀 Como Integrar o LEM

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Opção 1: Usar Dataset para Fine-tuning

```python
import json
from pathlib import Path

# Carregar dataset
dataset = json.load(open("LEM_knowledge_base/LEM_dataset.json"))

# Extrair training pairs
training_pairs = dataset["training_pairs"]

# Preparar para fine-tuning
training_data = []
for pair in training_pairs:
    training_data.append({
        "prompt": pair["input"],
        "completion": f" {pair.get('expected_output', '')}",
        "agent": pair["agent"]
    })

# Usar com OpenAI Fine-tuning API ou similar
# ...
```

### Opção 2: Use IDK Index para Retrieval-Augmented Generation (RAG)

```python
from sentence_transformers import SentenceTransformer
import json

# Carregar índice
idk_index = json.load(open("LEM_knowledge_base/LEM_IDK_index.json"))

# Inicializar embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Query do usuário
user_query = "Como gerar imagens de anúncios de e-commerce?"

# Buscar keywords relevantes
query_embedding = model.encode(user_query)

# Encontrar contextos relevantes
relevant_contexts = []
for keyword, occurrences in idk_index["keywords"].items():
    keyword_embedding = model.encode(keyword)
    similarity = cosine_similarity([query_embedding], [keyword_embedding])[0][0]

    if similarity > 0.7:
        relevant_contexts.extend(occurrences)

# Passar contextos para o modelo
context_text = "\n".join([c["context"] for c in relevant_contexts])
prompt = f"Context:\n{context_text}\n\nQuestion: {user_query}"

# Usar com seu modelo LLM
response = llm.generate(prompt)
```

### Opção 3: Roteamento Automático de Agentes

```python
import json

# Carregar dataset
dataset = json.load(open("LEM_knowledge_base/LEM_dataset.json"))
idk_index = json.load(open("LEM_knowledge_base/LEM_IDK_index.json"))

def route_to_agent(user_request):
    """Roteia um request ao agente apropriado"""

    # Extrair keywords do request
    request_keywords = extract_keywords(user_request)

    # Encontrar cluster semântico mais relevante
    best_cluster = None
    best_score = 0

    for cluster_name, cluster in idk_index["semantic_clusters"].items():
        cluster_keywords = set(cluster["keywords"])
        request_set = set(request_keywords)

        overlap = len(cluster_keywords & request_set)
        if overlap > best_score:
            best_score = overlap
            best_cluster = cluster

    # Retornar agente mais relevante
    if best_cluster:
        return best_cluster["agents"][0]
    else:
        return "general_agent"

# Exemplo
request = "Preciso gerar imagens para anúncios de produtos em marketplace"
agent = route_to_agent(request)
print(f"Routed to: {agent}")
```

---

**Tags**: concrete, general

**Palavras-chave**: Integrar, Como

**Origem**: unknown


---


<!-- VERSÍCULO 21/23 - marketplace_optimization__como_navegar_20251113.md (51 linhas) -->

# 🔍 Como Navegar

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Para encontrar Quick Starts

```
START_HERE.md                          (Geral)
docs/guides/QUICK_START_REFERENCE.md   (Referência rápida)
```

### Para encontrar Guides

```
docs/guides/                           (Todos os guias)
```

### Para encontrar Documentação Técnica

```
docs/technical/                        (Specs técnicas)
docs/frameworks/                       (LEM framework)
```

### Para encontrar Histórico

```
_archived/delivery_reports/            (Entregas finalizadas)
_archived/phase_reports/               (Fases completas)
```

### Para encontrar Referência de Código

```
docs/scripts/                          (Python scripts)
docs/adw/                              (ADW automation)
docs/paddleocr/                        (Vision ML)
```

---

**Tags**: abstract, general

**Palavras-chave**: Navegar, Como

**Origem**: unknown


---


<!-- VERSÍCULO 22/23 - marketplace_optimization__como_pesquisa_integration_20251113.md (40 linhas) -->

# 🔗 COMO PESQUISA INTEGRATION

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Framework Foundation Files
- `app/como_pesquisa/README.md`
- `app/como_pesquisa/01_framework/research_framework.md` (6 PILLARS)
- `app/como_pesquisa/01_framework/keyword_hierarchy.md` (4-LEVEL KEYWORDS)
- `app/como_pesquisa/02_prompt_composition/prompt_chunks_guide.md` (5-CHUNKS)
- `app/como_pesquisa/02_prompt_composition/prompt_templates.md` (TEMPLATES)
- `app/como_pesquisa/03_research_methodology/competitive_analysis.md`
- `app/como_pesquisa/07_templates/research_report_template.md`

### Research Agents Mapping
- Pilar 1 → `/analyze_market` → Market Research
- Pilar 2 → `/analyze_competitors` → Competitive Analysis
- Pilar 3 → [Internal] → Product Research
- Pilar 4 → `/extract_keywords` → Keywords (4-level)
- Pilar 5 → [Internal] → Trends & Insights
- Pilar 6 → [Internal] → FAQ Collection

### Chunk Library Mapping
- Chunk 1: Research Consolidation ← ALL PILLARS
- Chunk 2: Keyword Analysis ← PILAR 4 + 3
- Chunk 3: Competitive Gaps ← PILAR 2 + 1
- Chunk 4: Ad Structure ← ALL PILLARS
- Chunk 5: Validation & Optimization ← CHUNK 4

---

**Tags**: abstract, ecommerce, general

**Palavras-chave**: INTEGRATION, COMO, PESQUISA

**Origem**: unknown


---


<!-- VERSÍCULO 23/23 - marketplace_optimization__como_tudo_se_conecta_20251113.md (41 linhas) -->

# 🎯 Como Tudo Se Conecta

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```
USER INPUT
  ↓
RESEARCH_AGENT_INDEX.md (onde começar)
  ↓
COMO_USAR_RESEARCH_AGENT_SYSTEM.md (como usar)
  ├─ /research (main HOP)
  │  ├─ /analyze_market (Pilar 1)
  │  ├─ /analyze_competitors (Pilar 2)
  │  ├─ /extract_keywords (Pilar 4)
  │  └─ /compose_prompts (5-chunks)
  │
  └─ RESEARCH_AGENT_ENRICHMENT_SUMMARY.md (entender)
       └─ Referências para:
          - app/como_pesquisa/ (framework)
          - ADW_COMMANDS_COMPLETE_INDEX.md (automação)
          └─ USAR_ADW_PARA_DESTILACAO.md (próximas melhorias)

OUTPUT
  ├─ Markdown Report (human-readable)
  ├─ JSON Structured Data (API-ready)
  ├─ 5 AI-Ready Prompts (Claude/ChatGPT-ready)
  └─ Meta-Analysis Report (optimization tips)
```

---

**Tags**: abstract, general

**Palavras-chave**: Tudo, Como, Conecta

**Origem**: unknown


---


<!-- FIM DO CAPÍTULO 8 -->
<!-- Total: 23 versículos, 1162 linhas -->
