# LIVRO: Marketplace
## CAPÍTULO 6

**Versículos consolidados**: 22
**Linhas totais**: 1147
**Gerado em**: 2025-11-13 18:45:49

---


<!-- VERSÍCULO 1/22 - marketplace_optimization__adw_integration_path_20251113.md (37 linhas) -->

# 🚀 ADW Integration Path

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

```
RESEARCH ENHANCEMENT IDEA
  ↓
USAR_ADW_PARA_DESTILACAO.md
  ├─ Choose workflow (Quick/Detailed/Full)
  ├─ Run: /adw_plan_iso
  ├─ Run: /adw_plan_build_test_iso
  ├─ Run: /adw_review_iso
  ├─ Run: /adw_document_iso
  └─ Run: /adw_ship_iso
  ↓
ENHANCED RESEARCH SYSTEM
  ↓
Updated documentation in:
  - RESEARCH_AGENT_ENRICHMENT_SUMMARY.md
  - COMO_USAR_RESEARCH_AGENT_SYSTEM.md
  - RESEARCH_AGENT_INDEX.md
  ↓
NEW CAPABILITIES READY
```

---

**Tags**: general, intermediate

**Palavras-chave**: Integration, Path

**Origem**: unknown


---


<!-- VERSÍCULO 2/22 - marketplace_optimization__adw_workflow_commands_20251113.md (84 linhas) -->

# 📋 ADW WORKFLOW COMMANDS

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Core SDLC Commands

#### 1. **`/adw_plan_iso`** - Planning Phase Only
- **Purpose**: Create implementation specification
- **Input**: Feature/Bug/Chore description
- **Output**: Detailed plan file in `specs/` directory
- **Usage**:
  ```
  /adw_plan_iso
  [Provide feature description, bug details, or chore]
  ```
- **Output File**: `specs/issue-{issue_number}-adw-{adw_id}-sdlc_planner-{descriptive-name}.md`

#### 2. **`/adw_build_iso`** - Building Phase Only
- **Purpose**: Implement the planned solution
- **Input**: `adw_id` (required), implementation plan
- **Output**: Modified files + commits
- **Requirements**: Plan must already exist
- **Usage**:
  ```
  /adw_build_iso
  adw_id: abc12345
  ```

#### 3. **`/adw_test_iso`** - Testing Phase Only
- **Purpose**: Run validation tests on implementation
- **Input**: `adw_id` (required), worktree with implementation
- **Output**: Test results + validation report
- **Requirements**: Implementation must exist
- **Usage**:
  ```
  /adw_test_iso
  adw_id: abc12345
  ```

#### 4. **`/adw_review_iso`** - Review Phase Only
- **Purpose**: Validate implementation against plan
- **Input**: `adw_id` (required), plan + implementation
- **Output**: Review report + validation metrics
- **Requirements**: Plan and implementation must exist
- **Usage**:
  ```
  /adw_review_iso
  adw_id: abc12345
  ```

#### 5. **`/adw_document_iso`** - Documentation Phase Only
- **Purpose**: Generate documentation for the changes
- **Input**: `adw_id` (required), implementation files
- **Output**: Generated documentation
- **Requirements**: Implementation must exist
- **Usage**:
  ```
  /adw_document_iso
  adw_id: abc12345
  ```

#### 6. **`/adw_ship_iso`** - Shipping Phase Only
- **Purpose**: Approve implementation and merge to main
- **Input**: `adw_id` (required), reviewed implementation
- **Output**: Merged PR + updated main branch
- **Requirements**: Implementation must be reviewed
- **Usage**:
  ```
  /adw_ship_iso
  adw_id: abc12345
  ```

---

**Tags**: concrete, general

**Palavras-chave**: COMMANDS, WORKFLOW

**Origem**: unknown


---


<!-- VERSÍCULO 3/22 - marketplace_optimization__alternativa_execução_passo_a_passo_20251113.md (42 linhas) -->

# 🔧 Alternativa: Execução Passo-a-Passo

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

Se quiser mais controle ou debug entre fases:

```bash
cd C:\Users\Dell\tac-7\adws

# Fase 1: PLAN (4h)
uv run adw_plan_iso.py 1 c45aa7b8
# Output: agents/c45aa7b8/adw_state.json (UPDATED com plano)

# Fase 2: BUILD (8h)
uv run adw_build_iso.py 1 c45aa7b8
# Output: RAW_LEM_v1/knowledge_base/ (com novos agentes + keywords + pairs)

# Fase 3: TEST (4h)
uv run adw_test_iso.py 1 c45aa7b8
# Output: Test report com pass/fail

# Fase 4: DOCUMENT (4h)
uv run adw_document_iso.py 1 c45aa7b8
# Output: RAW_LEM_v1/docs/ com README, API docs, etc.

# Fase 5: REVIEW (2h)
uv run adw_review_iso.py 1 c45aa7b8
# Output: Review report com sign-off
```

---

**Tags**: general, intermediate

**Palavras-chave**: Execução, Passo, Alternativa

**Origem**: unknown


---


<!-- VERSÍCULO 4/22 - marketplace_optimization__anatomia_de_um_anúncio_estruturado_20251113.md (62 linhas) -->

# 🏗️ Anatomia de um Anúncio Estruturado

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

```
┌─────────────────────────────────────┐
│   TÍTULO PRINCIPAL (Headline 1)     │
│   (60 caracteres, keywords + benefit)
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   SUBTÍTULO SECUNDÁRIO (Headline 2) │
│   (opcional, feature ou diferencial)
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   BULLETS (3-5 benefícios)          │
│   ✓ Benefício 1 + prova             │
│   ✓ Benefício 2 + prova             │
│   ✓ Benefício 3 + prova             │
│   ✓ Diferencial único               │
│   ✓ Urgência/Oferta                 │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   BODY COPY (200-300 palavras)      │
│   Narrativa completa usando         │
│   StoryBrand: problema → solução →  │
│   benefício → prova social → ação   │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   SEÇÃO FAQ (5-8 perguntas)         │
│   P: Objeção comum                  │
│   R: Resposta com benefício         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   CALL-TO-ACTION (CTA)              │
│   Texto claro: "Compre Agora"       │
│   ou "Aproveite a Promoção"         │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│   EXTRAS (itens inclusos, dicas)    │
│   O que vem na compra               │
│   Dicas de uso                      │
└─────────────────────────────────────┘
```

---

**Tags**: general, intermediate

**Palavras-chave**: Anatomia, Estruturado, Anúncio

**Origem**: unknown


---


<!-- VERSÍCULO 5/22 - marketplace_optimization__anatomia_de_um_prompt_chunk_20251113.md (47 linhas) -->

# 🏗️ Anatomia de um Prompt-Chunk

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

Cada chunk possui:

```
CHUNK_NAME: [Nome descritivo]

ROLE: [Papel/Identidade do agente]
"Você é um especialista em [área]. Seu objetivo é [meta]."

CONTEXT: [Informações contextuais]
"Você está criando um anúncio para [produto] no [canal]."

INPUTS: [Variáveis esperadas / $ARGUMENTS]
- $PRODUTO: Nome e descrição do produto
- $MERCADO: Tipo de mercado (e-commerce, marketplace, etc)
- $KEYWORDS: Lista de keywords em JSON

INSTRUCTIONS: [Passos específicos]
1. Passo um
2. Passo dois
3. Passo três

OUTPUT_STRUCTURE: [Formato esperado]
{
  "field1": "descrição",
  "field2": "descrição"
}

EXAMPLE: [Exemplo real de aplicação]
[Input → Output exemplo]
```

---

**Tags**: concrete, general

**Palavras-chave**: Anatomia, Chunk, Prompt

**Origem**: unknown


---


<!-- VERSÍCULO 6/22 - marketplace_optimization__antes_vs_depois_20251113.md (64 linhas) -->

# 📊 ANTES vs DEPOIS

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### ❌ AGORA (32k arquivos caóticos)

```
32.671 arquivos
├─ /docs/
├─ /backup/
├─ /old/
├─ /Desktop/
│  ├─ doc1.pdf
│  ├─ doc1_v2.pdf
│  ├─ doc1_FINAL.pdf
│  ├─ doc1_FINAL_FINAL.pdf ← Qual é o real?
│  └─ (30 mais similares)

Problemas:
✗ Onde está "Prompt Engineering"?
✗ Duplicatas? Não sabe
✗ 10 clicks para achar algo
✗ Sem rastreabilidade
✗ Precisa copy-paste para cada LLM
✗ Quando quebra, tudo quebra
```

### ✅ DEPOIS (Árvore em Pé)

```
~8.000 artefatos únicos
├─ /lcm-ai/
│  ├─ 00_∞_hub/ ← Coração
│  ├─ −01_capture/ ← Histórico bruto
│  ├─ −02_build/ ← Artefatos
│  ├─ −03_index/ ← Catálogo
│  ├─ +01_intake/ ← Entrada
│  ├─ +05_delivery/ ← Saída
│  └─ views/ ← Symlinks semânticos
│     ├─ by-domain/
│     ├─ by-entity/
│     └─ by-purpose/

Ganhos:
✓ Busca "Prompt Engineering" → 0.2s, 50 resultados
✓ Duplicatas eliminadas via SHA256
✓ 1 clique: .md abre, .llm.json pronto
✓ Auditoria completa: quem? quando? por quê?
✓ Novo LLM amanhã? Seu .llm.json já funciona
✓ Escalável: adiciona Skills conforme precisa
```

---

**Tags**: general, intermediate

**Palavras-chave**: ANTES, DEPOIS

**Origem**: unknown


---


<!-- VERSÍCULO 7/22 - marketplace_optimization__api_endpoints_20251113.md (46 linhas) -->

# 🌐 API Endpoints

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Research Management

```
POST   /api/research/start
       Request: ResearchRequestDTO
       Response: ResearchStatusResponse
       Example: See INTEGRATION_GUIDE.md

GET    /api/research/{request_id}/status
       Response: ResearchStatusResponse

GET    /api/research/{request_id}/report
       Response: ResearchReportResponse

GET    /api/research/{request_id}/report/markdown
       Response: {markdown: str}

GET    /api/research
       Query: skip=0, limit=10
       Response: List[Dict]

GET    /api/research/{request_id}/messages
       Response: {messages: List[AgentMessage]}

GET    /api/research/health
       Response: {status: str, version: str}
```

All defined in `research_agent_routes.py`.

---

**Tags**: concrete, ecommerce, general

**Palavras-chave**: Endpoints, Conceito, Core, Keywords

**Origem**: unknown


---


<!-- VERSÍCULO 8/22 - marketplace_optimization__api_reference_integração_20251113.md (136 linhas) -->

# 📊 API Reference (Integração)

**Categoria**: marketplace_optimization
**Qualidade**: 0.95/1.00
**Data**: 20251113

## Conteúdo

### Base URL
```
http://localhost:8000/api/research
```

### Endpoint 1: POST /orchestrate

**Request**:
```json
{
  "product_name": "string",
  "category": "string",
  "marketplace": "string",
  "research_type": "quick|deep|custom"
}
```

**Response**:
```json
{
  "request_id": "uuid",
  "status": "processing|completed",
  "result": {
    "markdown_report": "...",
    "structured_data": {...},
    "chunks": [...],
    "metrics": {...}
  }
}
```

---

### Endpoint 2: POST /analyze-market

**Request**:
```json
{
  "product_name": "string",
  "marketplace": "string"
}
```

**Response**:
```json
{
  "market_size": "...",
  "growth_rate": 0.15,
  "seasonality": {...},
  "pricing_strategies": [...],
  "channels": [...]
}
```

---

### Endpoint 3: POST /analyze-competitors

**Request**:
```json
{
  "product_name": "string",
  "competitor_urls": ["url1", "url2"]
}
```

**Response**:
```json
{
  "competitors": [...],
  "positioning_map": {...},
  "gaps": [...],
  "differentiation_angles": [...]
}
```

---

### Endpoint 4: POST /extract-keywords

**Request**:
```json
{
  "product_name": "string",
  "category": "string"
}
```

**Response**:
```json
{
  "head_keywords": [...],
  "mid_tail_keywords": [...],
  "long_tail_keywords": [...],
  "question_keywords": [...]
}
```

---

### Endpoint 5: POST /compose-prompts

**Request**:
```json
{
  "research_request_id": "uuid"
}
```

**Response**:
```json
{
  "chunk_1": "Research Consolidation prompt...",
  "chunk_2": "Keyword Analysis prompt...",
  "chunk_3": "Competitive Gaps prompt...",
  "chunk_4": "Ad Structure prompt...",
  "chunk_5": "Validation & Optimization prompt..."
}
```

---

**Tags**: ecommerce, implementation

**Palavras-chave**: Reference, Integração

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 9/22 - marketplace_optimization__aplicação_em_seu_anúncio_20251113.md (56 linhas) -->

# 🎯 Aplicação em Seu Anúncio

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

Após análise completa, use os insights para:

### 1. Posicionamento Diferente
```
Se todos falam "melhor preço":
→ Você fala "melhor suporte"

Se todos falam "performance":
→ Você fala "custo-benefício + confiabilidade"
```

### 2. Headlines Baseadas em Gaps
```
Gap encontrado: Ninguém fala sobre suporte em português
Seu headline: "Suporte Técnico 24/7 em Português - Resolvemos em 1 hora"

Gap encontrado: Reclamação sobre superaquecimento
Seu headline: "Notebook Gamer Sem Superaquecimento - Ventilação Otimizada"
```

### 3. Bullets Respondendo Objeções
```
Reclamação comum: "Bate o preço vs novos?"
Seu bullet: "✓ Preço 18% menor que novo + garantia igual"

Reclamação comum: "Dura a bateria o dia todo?"
Seu bullet: "✓ 11h de bateria = trabalha o dia inteiro"
```

### 4. FAQ Antecipando Dúvidas
```
P: "Vale mais a pena comprar recondicionado?"
R: "Não neste caso. Bateria nova tem [X] ciclos. A nossa custa [Y].
    Diferença: R$ [Z]. Vale a pena esperar 1-2 anos para economizar?"

P: "É tão bom quanto as marcas famosas?"
R: "Sim! Mesma fabricante, mesmos componentes. A diferença é no
    branding. Você economiza no marketing da marca e ganha em funcionalidade."
```

---

**Tags**: general, intermediate

**Palavras-chave**: Aplicação, Anúncio

**Origem**: unknown


---


<!-- VERSÍCULO 10/22 - marketplace_optimization__aplicação_por_canal_20251113.md (40 linhas) -->

# 📱 Aplicação por Canal

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Mercado Livre
- **Título**: Head + 1 Mid-tail (máx 100 caracteres)
- **Descrição**: Misture Nível 1, 2 e 3
- **Seção FAQ**: Nível 4 (Question-based)

### Google Shopping/Ads
- **Headline 1**: Head keyword
- **Headline 2**: Mid-tail keyword
- **Headline 3**: Benefício ou long-tail
- **Description**: Nível 3 + 4

### Social Media (Instagram, TikTok)
- **Caption**: Mid-tail + Nível 3
- **Hashtags**: Misture níveis (alcance + segmentação)
- **CTA**: Question-based (converse)

### Site/E-commerce
- **URL**: Head keyword (ex: /notebook-gamer)
- **Title Tag**: Head + Mid-tail
- **Meta Description**: Mid-tail + Nível 3
- **H1**: Mid-tail
- **Body**: Nível 3 + 4
- **FAQ**: Nível 4

---

**Tags**: concrete, general

**Palavras-chave**: Aplicação, Canal

**Origem**: unknown


---


<!-- VERSÍCULO 11/22 - marketplace_optimization__aprendizados_aplicados_20251113.md (39 linhas) -->

# 🎓 Aprendizados Aplicados

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### Do PaddleOCR Knowledge Base

1. **Domínios Identificados**:
   - Document Processing (layout, structure)
   - Image Optimization (preprocessing, quality)
   - Model Management (inference, deployment)
   - Multilingual Support (language, character)
   - Quality Assurance (validation, testing)

2. **5 Novos Agentes Criados**:
   - DocumentProcessingAgent
   - ImageOptimizationAgent
   - ModelManagementAgent
   - MultilingualSupportAgent
   - QualityAssuranceAgent

3. **10 Training Pairs Gerados**:
   - 2 × Document Processing
   - 2 × Image Optimization
   - 2 × Model Management
   - 2 × Multilingual Support
   - 2 × Quality Assurance

---

**Tags**: ecommerce, implementation

**Palavras-chave**: Aprendizados, Aplicados

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 12/22 - marketplace_optimization__após_tudo_completar_20251113.md (63 linhas) -->

# 🎁 Após Tudo Completar

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### **1. Fazer o Commit do Novo Knowledge**
```bash
cd C:\Users\Dell\tac-7
git add RAW_LEM_v1/
git commit -m "🚀 Implement RAW_LEM_v1.1: Add 3 new agents with distilled knowledge

- Added PaymentProcessingAgent (20 keywords, 4 training pairs)
- Added OrderManagementAgent (20 keywords, 4 training pairs)
- Added CustomerServiceAgent (19 keywords, 4 training pairs)
- Expanded keywords: 91 → 150+
- Expanded training pairs: 13 → 25+
- Quality score: 100/100 (maintained)

Generated with ADW SDLC workflow"

git push
```

### **2. Usar o Knowledge para Fine-Tuning**
```bash
# Training data já está em formato OpenAI JSONL:
openai.FineTuningJob.create(
    training_file="RAW_LEM_v1/knowledge_base/training_data.jsonl",
    model="gpt-3.5-turbo"
)
```

### **3. Usar para RAG System**
```python
from lem_rag import LEM_RAG

rag = LEM_RAG.load("RAW_LEM_v1/knowledge_base/idk_index.json")
context = rag.retrieve("How do I process a payment?")
# Returns context from PaymentProcessingAgent's knowledge
```

### **4. Próximo Passo: v1.1.1 ou v2.0**
```bash
# Para adicionar mais agentes, use o mesmo workflow:
# 1. Adicione domínio novo em plan_input.json
# 2. Rodar ADW SDLC novamente
# 3. v1.1.1 será incremento automático

cd adws
uv run adw_sdlc_iso.py 2 c45aa7b8  # Nova issue para v1.1.1
```

---

**Tags**: general, implementation

**Palavras-chave**: Tudo, Completar, Após

**Origem**: unknown


---


<!-- VERSÍCULO 13/22 - marketplace_optimization__arquitetura_20251113.md (52 linhas) -->

# 🏗️ Arquitetura

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Hierarquia de Conhecimento

```
LIVRO (6 domínios de e-commerce)
  ↓
CAPÍTULO (Subtemas)
  ↓
VERSÍCULO (Unidade atômica de conhecimento)
  ├─ Título + Conceito
  ├─ Entropia: 0-100 (densidade informacional)
  ├─ Deus-vs-Todo: Abstract ↔ Contextual
  └─ Relações com outros versículos
```

### Pipeline de Destilação (5 Fases)

```
RAW Doc → [1. Extract] → Chunks
       → [2. Entropy] → Scored
       → [3. Abstraction] → Classified
       → [4. Domain] → Positioned
       → [5. Output] → JSON
```

### Métricas Principais

**Entropia (0-100)**
- 80-100: Denso, novo, importante
- 50-79: Bom, prático, balanceado
- 0-49: Óbvio, repetitivo, descartável

**Deus-vs-Todo**
- 100% Deus: "ACID properties..." (universal)
- 50% Mixed: "PostgreSQL has ACID, MySQL too" (geral + exemplos)
- 100% Todo: "Our prod uses PostgreSQL" (contextual)

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Arquitetura

**Origem**: unknown


---


<!-- VERSÍCULO 14/22 - marketplace_optimization__arquitetura_do_sistema_20251113.md (69 linhas) -->

# 🏗️ Arquitetura do Sistema

**Categoria**: marketplace_optimization
**Qualidade**: 0.95/1.00
**Data**: 20251113

## Conteúdo

### Fluxo de Dados Completo

```
INPUT (Product Name + Category + Marketplace)
  ↓
ORCHESTRATOR (/research - Main Agent)
  ↓
┌─────────────────────────────────────────────────────────────┐
│ PIPELINE DE 6 PILARES (em paralelo ou sequencial)          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ Pilar 1: /analyze_market → $market_research_result        │
│ Pilar 2: /analyze_competitors → $competitive_result       │
│ Pilar 3: [Internal] Product Research → $product_result    │
│ Pilar 4: /extract_keywords → $keywords_result             │
│ Pilar 5: [Internal] Trends & Insights → $trends_result    │
│ Pilar 6: [Internal] FAQ Collection → $faq_result          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
  ↓
VALIDATION LAYER (Quality Scoring + Meta-Analysis)
  ↓
┌─────────────────────────────────────────────────────────────┐
│ 5-CHUNK PROMPT COMPOSITION LIBRARY                          │
├─────────────────────────────────────────────────────────────┤
│ Chunk 1: Research Consolidation (All 6 pillars)           │
│ Chunk 2: Keyword Analysis (Pillar 4 + 3)                  │
│ Chunk 3: Competitive Gaps (Pillar 2 + 1)                  │
│ Chunk 4: Ad Structure (All pillars)                       │
│ Chunk 5: Validation & Optimization (Chunk 4 QA)           │
└─────────────────────────────────────────────────────────────┘
  ↓
META-RESEARCH LAYER (Optimization + Improvements)
  ↓
OUTPUT ASSEMBLY
  ├─ 📄 Markdown Report (Human-readable)
  ├─ 📊 JSON Structured Data (API-ready)
  ├─ 🤖 5 AI-Ready Prompts (Copy-paste to Claude/ChatGPT)
  ├─ 📈 Quality Metrics (0-100 scores)
  └─ ✨ Ready-to-use Assets
```

### Componentes Principais

| Componente | Localização | Função |
|-----------|-----------|---------|
| **Orchestrator** | `.claude/commands/research.md` | Coordena todo pipeline |
| **Pillar Agents** | `.claude/commands/{analyze_market,analyze_competitors,extract_keywords}.md` | Executa pesquisas temáticas |
| **Chunk Composer** | `.claude/commands/compose_prompts.md` | Transforma dados em prompts |
| **Python Server** | `app/server/research_agent_*.py` | Backend REST API |
| **Knowledge Base** | `RAW_LEM_v1.1/` + `knowledge_artifacts_v1/` | Dados de treinamento |
| **Framework** | `app/como_pesquisa/` | Metodologia e templates |

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Arquitetura, Sistema

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 15/22 - marketplace_optimization__arquitetura_final_20251113.md (45 linhas) -->

# 🏗️ Arquitetura Final

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```
RESEARCH AGENT SYSTEM (6 PILARES + 5-CHUNKS)
│
├─ Pilar 1: Market Research (/analyze_market)
│  └─ 7 steps com 0-level prompts
│
├─ Pilar 2: Competitive Analysis (/analyze_competitors)
│  └─ 8 steps com 0-level prompts
│
├─ Pilar 3: Product Research (Internal)
│  └─ Features → Benefits → Emotions
│
├─ Pilar 4: Keywords Research (/extract_keywords)
│  └─ 8 steps + 4-level hierarchy
│
├─ Pilar 5: Trends & Insights (Internal)
│  └─ Market dynamics + trends
│
├─ Pilar 6: FAQ Collection (Internal)
│  └─ Customer questions + objections
│
└─ 5-CHUNK PROMPT LIBRARY (/compose_prompts)
   ├─ Chunk 1: Research Consolidation
   ├─ Chunk 2: Keyword Analysis
   ├─ Chunk 3: Competitive Gaps
   ├─ Chunk 4: Ad Structure
   └─ Chunk 5: Ad Validation
```

---

**Tags**: general, intermediate

**Palavras-chave**: Arquitetura, Final

**Origem**: unknown


---


<!-- VERSÍCULO 16/22 - marketplace_optimization__arquitetura_proposta_20251113.md (29 linhas) -->

# 🎯 Arquitetura Proposta

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

```
C:\seu\repo\
├── .git/
├── .gitignore              ← Excluir artifacts grandes
├── knowledge-base/         ← Versionado (apenas índices + metadata)
│   ├── v1/                 ← Snapshots versionados
│   │   ├── index.json      ← Índice completo (comprimido)
│   │   ├── metadata.json   ← Estatísticas
│   │   └── changelog.md
│   ├── current/            ← Symlink para versão latest
│   └── .gitkeep
│
├── knowledge-artifacts/    ← NÃO versionado (Git LFS ou S3)
│   ├

**Tags**: ecommerce, intermediate

**Palavras-chave**: Arquitetura, Proposta

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 17/22 - marketplace_optimization__arquitetura_trinity_20251113.md (48 linhas) -->

# 🏗️ Arquitetura Trinity

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

O agente implementa o padrão **Trinity** com 3 camadas:

### 1. **Narrativa** (Lógica de Negócio)
- Algoritmo de decisão em 3 fases
- Validação de princípios éticos
- Cálculo de confiança

### 2. **Estrutura** (Data Classes)
```python
@dataclass
class Produto:
    id, nome, descricao, preco
    categoria, ética_score

@dataclass
class Cliente:
    id, nome, email
    estagio_jornada, carrinho
    historico_compras, iec_score_percebido

@dataclass
class DecisaoCompra:
    cliente_id, produto_id
    estagio, confianca
    objecoes, recomendacoes
```

### 3. **Propósito** (Governança)
- KPIs de sucesso
- Métricas de medição
- Recomendações de melhoria

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Arquitetura, Trinity

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 18/22 - marketplace_optimization__arquivos_criados_hoje_20251113.md (45 linhas) -->

# ⚙️ ARQUIVOS CRIADOS HOJE

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### 1. Orchestrator (coordena tudo)
```
orchestrator_scaled.py       [Reutilizável, extensível]
```

**Uso:**
```bash
# Executar tudo
python orchestrator_scaled.py \
  --input "BIBLIA_REORGANIZADA/" \
  --output "knowledge_artifacts_v1/" \
  --version "1.0.0"

# Ou executar fase por fase
python orchestrator_scaled.py \
  --input "BIBLIA_REORGANIZADA/" \
  --output "knowledge_artifacts_v1/" \
  --phase 2          # Só extração
  --resume           # Retomar de onde parou
```

### 2. Documentação Estratégica
```
STRATEGY_SCALED_KNOWLEDGE_DISTILLATION.md
└─ Arquitetura completa
└─ 3 camadas de processamento
└─ Versionamento no repo
```

---

**Tags**: architectural, general

**Palavras-chave**: HOJE, ARQUIVOS, CRIADOS

**Origem**: unknown


---


<!-- VERSÍCULO 19/22 - marketplace_optimization__arquivos_de_saída_20251113.md (38 linhas) -->

# 📁 Arquivos de Saída

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Do Passo 1 (Distillation)
```
RAW_LEM_v1.1_PADDLEOCR/
├── DISTILLATION_SUMMARY.json        ⭐ VER PRIMEIRO
├── catalog_index.json               📑 Índice de ficheiros
├── content_catalog.jsonl            📚 Catálogo (33k+ linhas)
├── semantic_map.json                🔗 Mapa keywords
└── duplicates_report.json           🔄 Duplicatas
```

### Do Passo 2 (Master Selection)
```
MASTER_SELECTION.json               🎯 Ficheiros mestres
REMOVABLE_DUPLICATES.jsonl          🗑️  Ficheiros para deletar
dedup_cleanup.sh                    ⚠️  Script cleanup (revisar!)
```

### Do Passo 3 (Training)
```
training_pairs_paddleocr.jsonl      📝 Dados fine-tuning
```

---

**Tags**: concrete, general

**Palavras-chave**: Arquivos, Saída

**Origem**: unknown


---


<!-- VERSÍCULO 20/22 - marketplace_optimization__arquivos_gerados_20251113.md (38 linhas) -->

# 📁 Arquivos Gerados

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### 1. Arquivos de Conhecimento

```
LEM_knowledge_base/
├── LEM_dataset.json               ← Dataset estruturado para treinamento
├── LEM_IDK_index.json             ← Índice de Information Dense Keywords
├── LEM_training_data.jsonl        ← Formato OpenAI para fine-tuning
├── LEM_knowledge_cards.json       ← Knowledge cards estruturados
├── LEM_pipeline_report.json       ← Relatório de qualidade
└── LEM_pipeline.log               ← Logs da execução
```

### 2. Scripts de Integração

```
Raiz do Projeto/
├── LEM_knowledge_distillation.py  ← Pipeline principal (reutilizável)
├── LEM_usage_examples.py          ← 10 exemplos práticos de uso
├── LEM_INTEGRATION_GUIDE.md       ← Guia completo de integração
└── LEM_README.md                  ← Este arquivo
```

---

**Tags**: concrete, general

**Palavras-chave**: Arquivos, Gerados

**Origem**: unknown


---


<!-- VERSÍCULO 21/22 - marketplace_optimization__arquivos_no_github_20251113.md (37 linhas) -->

# 📁 Arquivos no GitHub

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```
RAW_LEM_v1/
├── README.md                      (6.3KB)
├── KNOWLEDGE_INDEX.md             (11KB)
├── knowledge_base/                (120KB)
│   ├── dataset.json              (23KB - 3 agentes)
│   ├── idk_index.json            (78KB - 91 keywords)
│   ├── training_data.jsonl       (9.5KB - 13 pares)
│   └── knowledge_cards.json      (2.9KB)
├── metadata/
│   ├── quality_metrics.json      (100/100 score)
│   ├── versioning.json           (v1→v3 roadmap)
│   └── changelog.md

+ Documentação:
├── RAW_LEM_v1_COMPLETION_REPORT.md
├── RAW_LEM_v1_INDEX.md
├── CONTINUE_WORKFLOW.md
└── GUIA_GIT_COMMITS.md
```

---

**Tags**: general, intermediate

**Palavras-chave**: GitHub, Arquivos

**Origem**: unknown


---


<!-- VERSÍCULO 22/22 - marketplace_optimization__artefatos_consolidados_20251113.md (30 linhas) -->

# 🎯 Artefatos Consolidados

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### Research System (Origem)
- **6 Pilares**: Market, Competitors, Product, Keywords, Trends, FAQ
- **5-Chunk Library**: Consolidation, Keywords, Gaps, Ad Structure, Validation
- **7 Agentes**: Orchestrator, Market, Competitor, Keyword, FAQ, Validator, Meta
- **5 CLI Commands**: /research, /analyze_market, /analyze_competitors, /extract_keywords, /compose_prompts
- **6 Python Modules**: models, config, orchestrator, agents, routes, meta
- **Knowledge Base**: 8 JSON files com semantic maps, inventories, catalogs

### Framework (Como Pesquisa)
- **20+ documentos** sobre metodologia, templates, tools integration
- **4 níveis de keyword hierarchy**
- **5-chunk prompt composition library**
- **Metodologias de pesquisa**: competitive, market, product, trends, FAQ

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Artefatos, Consolidados

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- FIM DO CAPÍTULO 6 -->
<!-- Total: 22 versículos, 1147 linhas -->
