# LIVRO: Marketplace
## CAPÍTULO 48

**Versículos consolidados**: 12
**Linhas totais**: 1181
**Gerado em**: 2025-11-13 18:45:49

---


<!-- VERSÍCULO 1/12 - marketplace_optimization_part_6_claude_code_hooks_20251113.md (44 linhas) -->

# PART 6: CLAUDE CODE HOOKS

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### CARD-015: Claude Code Integration Hooks
**Location:** `.claude/hooks/`

**Hook Types:**
1. **Pre-Tool Hooks:** `pre_tool_use.py`
   - Request validation
   - Security checks
   - Resource validation

2. **Post-Tool Hooks:** `post_tool_use.py`
   - Result validation
   - Knowledge extraction
   - Logging

3. **Notification System:** `notification.py`
   - Event notification
   - Alert generation
   - Status reporting

4. **LLM Integration:** `utils/llm/`
   - `anth.py` - Anthropic API integration
   - `oai.py` - OpenAI API fallback

5. **User Prompt Handling:** `user_prompt_submit.py`
   - Prompt validation
   - Context enrichment
   - Knowledge injection

---

**Tags**: python, concrete

**Palavras-chave**: HOOKS, CLAUDE, PART, CODE

**Origem**: unknown


---


<!-- VERSÍCULO 2/12 - marketplace_optimization_part_7_detailed_script_reference_cards_20251113.md (162 linhas) -->

# PART 7: DETAILED SCRIPT REFERENCE CARDS

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### CARD-016: ADWS Core Modules (adw_modules/)
**Contained Scripts:**
- `agent.py` - Agent execution logic, state management
- `git_ops.py` - Git operations (commit, push, worktree)
- `github.py` - GitHub API integration, PR management
- `github_api_direct.py` - Direct GitHub REST API calls
- `gh_wrapper.py` - GitHub CLI wrapper utilities
- `workflow_ops.py` - Workflow orchestration and sequencing
- `worktree_ops.py` - Git worktree management for parallel builds
- `r2_uploader.py` - Cloudflare R2 storage integration
- `data_types.py` - Shared data structures and models
- `state.py` - Workflow state management
- `utils.py` - Utility functions and helpers

**Key Patterns:**
- Each module encapsulates specific domain (git, github, workflow, storage)
- State management through dataclasses and configuration objects
- Error handling with retry logic and fallbacks
- Logging at critical decision points
- Integration with external APIs (GitHub, Cloudflare R2)

---

### CARD-017: ADWS Workflow Orchestration Scripts
**Core Workflow Files:**
- `adw_plan_iso.py` - Planning phase (task decomposition)
- `adw_plan_build_iso.py` - Plan+Build combined workflow
- `adw_plan_build_test_iso.py` - Plan+Build+Test full SDLC
- `adw_build_iso.py` - Building phase (compilation, deployment)
- `adw_test_iso.py` - Testing phase (validation, assertions)
- `adw_review_iso.py` - Code review phase (quality gates)
- `adw_ship_iso.py` - Shipping phase (release, deployment)
- `adw_document_iso.py` - Documentation generation
- `adw_patch_iso.py` - Hot patch workflow
- `adw_sdlc_iso.py` - Full SDLC pipeline orchestrator
- `adw_sdlc_zte_iso.py` - SDLC with zero-trust enforcement

**Orchestration Pattern:**
```
1. Parse user request/trigger
2. Load workflow configuration
3. Initialize git worktree for isolation
4. Execute workflow stages sequentially
5. Aggregate results from each stage
6. Generate comprehensive report
7. Update remote state
8. Commit to git with audit trail
```

---

### CARD-018: ADWS Testing Framework (adw_tests/)
**Test Scripts:**
- `test_agents.py` - Agent capability validation
- `test_model_selection.py` - Model selection logic tests
- `test_r2_uploader.py` - R2 upload functionality tests
- `test_webhook_simplified.py` - Webhook handling tests
- `health_check.py` - System health validation
- `sandbox_poc.py` - Proof-of-concept sandbox testing

**Testing Strategy:**
- Unit tests for individual components
- Integration tests for multi-module workflows
- Health checks for deployment readiness
- Sandbox environment for safe experimentation
- Automated test suite execution

---

### CARD-019: ADWS Trigger System (adw_triggers/)
**Trigger Implementations:**
- `trigger_webhook.py` - GitHub webhook listener
  - Event types: push, pull_request, workflow_dispatch
  - Payload parsing and validation
  - Automatic workflow invocation
  - Event filtering and routing

- `trigger_cron.py` - Scheduled execution
  - Cron expression parsing
  - Scheduled task execution
  - Result aggregation
  - Error notification

**Trigger Pattern:**
```
Event → Validate → Route → Invoke Workflow → Report Result
```

---

### CARD-020: LEM Knowledge Distillation Ecosystem
**Core Distillation Files:**
- `LEM_knowledge_distillation.py` (root) - Main distillation engine
- `knowledge_artifacts_v1/LEM/LEM_knowledge_distillation.py` - Versioned engine
- `LEM_usage_examples.py` - Usage patterns and examples
- `knowledge_artifacts_v1/LEM/LEM_usage_examples.py` - Versioned examples

**Distillation Process:**
1. Load consolidated knowledge base
2. Parse e-commerce domain concepts
3. Extract semantic relationships
4. Generate embeddings for each concept
5. Create training pairs (query → answer)
6. Build knowledge graph connections
7. Index for semantic search
8. Validate quality metrics
9. Export to trainable format

**Output Artifacts:**
- Embedding vectors for semantic search
- Training pairs for model fine-tuning
- Knowledge graph for relationship mapping
- Domain-specific entity catalogs

---

### CARD-021: Knowledge Enrichment Pipeline
**Enrichment Scripts:**
- `enrich_genesis_advanced.py` - Advanced GENESIS enrichment
- `enrich_lem_v1_1.py` - LEM v1.1 enrichment
- `enrich_with_genesis_knowledge.py` - GENESIS knowledge injection
- `build_genesis_lem_complete.py` - Complete LEM building from GENESIS
- `run_complete_lem_enrichment.py` - Full enrichment orchestration

**Enrichment Pattern:**
```
Base LEM → Load GENESIS → Extract Topics →
Build Relationships → Generate Embeddings →
Create Training Data → Validate → Export
```

**Integration Points:**
- GENESIS as knowledge foundation
- LIVRO books for structured knowledge
- RAW files for research grounding
- PaddleOCR for document extraction

---

### CARD-022: Training Data Generation
**Generation Scripts:**
- `generate_training_pairs.py` - Query-answer pair generation
- `run_full_distillation.py` - Complete distillation run
- `distill_fast.py` - Optimized fast distillation
- `distill_paddleocr_knowledge.py` - OCR kn

[... content truncated ...]

**Tags**: python, abstract

**Palavras-chave**: SCRIPT, CARDS, REFERENCE, PART, DETAILED

**Origem**: unknown


---


<!-- VERSÍCULO 3/12 - marketplace_optimization_parte_10_pr_ximos_passos_20251113.md (38 linhas) -->

# PARTE 10: PRÓXIMOS PASSOS

**Categoria**: marketplace_optimization
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

### Implementação Imediata
1. ✅ Mapear estrutura de LIVROS/CAPÍTULOS
2. ⬜ Desenvolver `distiller.py` (Fase 1)
3. ⬜ Desenvolver `organizer.py` (Fase 3)
4. ⬜ Implementar validação automática
5. ⬜ Setup CI/CD para processamento automático

### Integração
- [ ] Integrar com ADW para processamento em massa
- [ ] Setup API para consumir conhecimento
- [ ] Fine-tuning LLM com corpus
- [ ] RAG system para Q&A

---

**Próximo Passo:** Quer que eu comece com o desenvolvimento do `distiller.py` ou prefere mapear os LIVROS/CAPÍTULOS primeiro?


---

### RAW_001_ECOM_QUEST_Integration.md

# Integração Mentor ML ↔ Ecom Quest

**Tags**: ecommerce, general, implementation

**Palavras-chave**: PARTE, PRÓXIMOS, PASSOS

**Origem**: desconhecida


---


<!-- VERSÍCULO 4/12 - marketplace_optimization_parte_10_próximos_passos_20251113.md (34 linhas) -->

# PARTE 10: PRÓXIMOS PASSOS

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### Implementação Imediata
1. ✅ Mapear estrutura de LIVROS/CAPÍTULOS
2. ⬜ Desenvolver `distiller.py` (Fase 1)
3. ⬜ Desenvolver `organizer.py` (Fase 3)
4. ⬜ Implementar validação automática
5. ⬜ Setup CI/CD para processamento automático

### Integração
- [ ] Integrar com ADW para processamento em massa
- [ ] Setup API para consumir conhecimento
- [ ] Fine-tuning LLM com corpus
- [ ] RAG system para Q&A

---

**Próximo Passo:** Quer que eu comece com o desenvolvimento do `distiller.py` ou prefere mapear os LIVROS/CAPÍTULOS primeiro?


======================================================================

**Tags**: ecommerce, implementation

**Palavras-chave**: PARTE, PRÓXIMOS, PASSOS

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 5/12 - marketplace_optimization_parte_1_arquitetura_geral_20251113.md (100 linhas) -->

# PARTE 1: ARQUITETURA GERAL

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### 1.1 Estrutura de Ficheiros (Hierarquia Bíblica)

```
ecommerce-canon/
├── 📖 LIVRO_01_FUNDAMENTALS/          [Conceitos base de e-commerce]
│   ├── CAPITULO_01_BUSINESS_MODEL/
│   │   ├── VERSÍCULO_001_B2C.md
│   │   ├── VERSÍCULO_002_B2B.md
│   │   ├── VERSÍCULO_003_MARKETPLACE.md
│   │   ├── VERSÍCULO_004_SAAS.md
│   │   └── _CHAPTER_METADATA.json
│   ├── CAPITULO_02_CUSTOMER_JOURNEY/
│   │   ├── VERSÍCULO_001_AWARENESS.md
│   │   ├── VERSÍCULO_002_CONSIDERATION.md
│   │   ├── VERSÍCULO_003_PURCHASE.md
│   │   ├── VERSÍCULO_004_RETENTION.md
│   │   └── _CHAPTER_METADATA.json
│   └── _LIVRO_INDEX.md
│
├── 📖 LIVRO_02_PRODUCT_MANAGEMENT/    [Gestão de catálogo e dados]
│   ├── CAPITULO_01_CATALOG_ARCHITECTURE/
│   │   ├── VERSÍCULO_001_TAXONOMY.md
│   │   ├── VERSÍCULO_002_ATTRIBUTES.md
│   │   ├── VERSÍCULO_003_VARIANTS.md
│   │   ├── VERSÍCULO_004_HIERARCHY.md
│   │   └── _CHAPTER_METADATA.json
│   ├── CAPITULO_02_DATA_ENRICHMENT/
│   │   ├── VERSÍCULO_001_DESCRIPTIONS.md
│   │   ├── VERSÍCULO_002_IMAGES.md
│   │   ├── VERSÍCULO_003_PRICING_RULES.md
│   │   └── _CHAPTER_METADATA.json
│   └── _LIVRO_INDEX.md
│
├── 📖 LIVRO_03_OPERATIONS/            [Processos operacionais]
│   ├── CAPITULO_01_INVENTORY/
│   ├── CAPITULO_02_ORDERS/
│   ├── CAPITULO_03_FULFILLMENT/
│   └── _LIVRO_INDEX.md
│
├── 📖 LIVRO_04_TECHNOLOGY/            [Stack técnico]
│   ├── CAPITULO_01_ARCHITECTURE/
│   ├── CAPITULO_02_DATABASE_DESIGN/
│   ├── CAPITULO_03_INTEGRATIONS/
│   └── _LIVRO_INDEX.md
│
├── 📖 LIVRO_05_MARKETING/             [Marketing & Growth]
│   ├── CAPITULO_01_CUSTOMER_ACQUISITION/
│   ├── CAPITULO_02_RETENTION/
│   ├── CAPITULO_03_ANALYTICS/
│   └── _LIVRO_INDEX.md
│
├── 📖 LIVRO_06_PAYMENTS/              [Processamento de pagamentos]
│   ├── CAPITULO_01_PAYMENT_METHODS/
│   ├── CAPITULO_02_FRAUD_PREVENTION/
│   ├── CAPITULO_03_COMPLIANCE/
│   └── _LIVRO_INDEX.md
│
├── 🔬 GENESIS/                        [Raw → Structured]
│   ├── RAW/                          [Input não processado]
│   │   └── *.md, *.txt, *.json
│   ├── PROCESSING/                   [Processamento em andamento]
│   │   ├── chunks/
│   │   ├── semantic_graphs/
│   │   └── entropy_reports/
│   └── VALIDATION/                   [Esperando aprovação]
│       └── *.pending.md
│
├── 🎯 AGENTS/                        [Agentes de Destilação]
│   ├── distiller.py               [RAW → Semantic Chunks]
│   ├── organizer.py               [Chunks → Canon Structure]
│   ├── validator.py               [Quality Assurance]
│   ├── versioner.py               [Git + Changelog]
│   └── indexer.py                 [Build Indices]
│
└── 📊 METADATA/                       [Índices & Tracking]
    ├── canon_registry.json          [All versículos]
    ├── entropy_scores.json          [Info density]
    ├── keywords_taxonomy.json       [Searchable keywords]
    ├── deus_vs_todo.json            [Absolute vs Contextual]
    ├── version_history.json         [Evolution tracking]
    ├── cross_references.json        [Relations between versículos]
    └── search_index.json            [Full-text search]
```

---

**Tags**: concrete, ecommerce, general

**Palavras-chave**: GERAL, ARQUITETURA, PARTE

**Origem**: unknown


---


<!-- VERSÍCULO 6/12 - marketplace_optimization_parte_1_introdução_e_primeiros_passos_20251113.md (149 linhas) -->

# PARTE 1: INTRODUÇÃO E PRIMEIROS PASSOS

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Introdução ao Claude

Claude é uma plataforma de IA altamente performática, confiável e inteligente construída pela Anthropic. Claude se destaca em tarefas envolvendo linguagem, raciocínio, análise, codificação e muito mais. A plataforma é projetada para ser segura, confiável e resistente a jailbreaks, tornando-a ideal para clientes empresariais construindo aplicações alimentadas por IA em escala.

#### Modelos Claude Mais Recentes

- **Claude Sonnet 4.5** - O modelo mais inteligente, melhor para agentes complexos, codificação e tarefas mais avançadas
- **Claude Haiku 4.5** - O modelo mais rápido com inteligência próxima à fronteira
- **Claude Opus 4.1** - Modelo excepcional para tarefas especializadas que requerem raciocínio avançado

**Nota:** Se você está procurando conversar com Claude, visite claude.ai. Este guia é para desenvolvedores usando a API Claude.

### Pré-requisitos

Antes de começar com Claude, você precisa:

1. **Uma Conta Anthropic Console** - Inscreva-se em console.anthropic.com
2. **Uma Chave API** - Gere a partir do Claude Console
3. **Um ambiente de desenvolvimento** com uma das seguintes opções:
   - cURL (para testes rápidos)
   - Python 3.7+
   - Node.js 14+
   - Java 8+
   - Go 1.18+
   - .NET, Ruby, PHP

### Obtendo Sua Chave API

**Passo 1: Acesse o Console**
1. Navegue até Claude Console (console.anthropic.com)
2. Faça login com suas credenciais
3. Vá para Account Settings → API Keys

**Passo 2: Gere uma Chave API**
1. Clique em Create Key
2. Dê um nome descritivo à chave
3. Copie a chave imediatamente (você não poderá vê-la novamente)
4. Armazene-a com segurança

**Importante:** Cada chave API tem escopo para um Workspace específico.

### Configurando Seu Ambiente

#### Configuração de Variável de Ambiente

**macOS/Linux:**
```bash
export ANTHROPIC_API_KEY='sua-chave-api-aqui'
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY='sua-chave-api-aqui'
```

**Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sua-chave-api-aqui
```

### Fazendo Sua Primeira Chamada API

#### Usando cURL

```bash
curl https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-sonnet-4-5",
    "max_tokens": 1000,
    "messages": [
      {
        "role": "user",
        "content": "Quais são os últimos desenvolvimentos em energia renovável?"
      }
    ]
  }'
```

### Instalando SDKs Cliente

#### Python SDK

**Instalação:**
```bash
pip install anthropic
```

**Uso Básico:**
```python
import anthropic

client = anthropic.Anthropic(
    api_key="minha_chave_api"
)

message = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Olá, Claude"}
    ]
)

print(message.content)
```

#### TypeScript SDK

**Instalação:**
```bash
npm install @anthropic-ai/sdk
```

**Uso Básico:**
```typescript
import Anthropic from '@anthropic-ai/sdk';

const anthropic = new Anthropic({
  apiKey: 'minha_chave_api'
});

const msg = await anthropic.messages.create({
  model: "claude-sonnet-4-5",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Olá, Claude" }],
});

console.log(msg);
```

---

**Tags**: concrete, general

**Palavras-chave**: PARTE, PRIMEIROS, INTRODUÇÃO, PASSOS

**Origem**: unknown


---


<!-- VERSÍCULO 7/12 - marketplace_optimization_parte_2_definição_de_termos_bíblia_do_e_commerce_20251113.md (35 linhas) -->

# PARTE 2: DEFINIÇÃO DE TERMOS (Bíblia do E-Commerce)

**Categoria**: marketplace_optimization
**Qualidade**: 0.91/1.00
**Data**: 20251113

## Conteúdo

### 2.1 Hierarquia de Conhecimento

| Nível | Termo | Descrição | Exemplo |
|-------|-------|-----------|---------|
| **Livro** | LIVRO_01 | Domínio temático principal | PRODUCT_MANAGEMENT |
| **Capítulo** | CAP_01 | Subdivisão de domínio | CATALOG_ARCHITECTURE |
| **Versículo** | VERS_001 | Unidade atômica de conhecimento | TAXONOMY.md |
| **Entropia** | 0-100 | Densidade informacional (quanto "novo" contém) | 85 = muito denso |
| **Deus vs Todo** | Abstract ↔ Contextual | Absoluto (universal) vs Relativo (caso-específico) | Absoluto: "ACID properties"; Relativo: "PostgreSQL em produção" |

### 2.2 Estrutura de um VERSÍCULO

```markdown
# VERSÍCULO_001_TAXONOMY

**Entropia:** 78/100
**Status:** [Stable|Experimental|Deprecated]
**Last Updated:** 2025-11-02
**Version:** 1.2.3
**Deus-vs-Todo:** 70% Absoluto / 30% Contextual

**Tags**: ecommerce, architectural

**Palavras-chave**: PARTE, DEFINIÇÃO, TERMOS, Bíblia, Commerce

**Origem**: _CONSOLIDATED_ECOMMERCE_RAW_FROM_GIT.md


---


<!-- VERSÍCULO 8/12 - marketplace_optimization_parte_2_modelos_e_especificações_completas_20251113.md (111 linhas) -->

# PARTE 2: MODELOS E ESPECIFICAÇÕES COMPLETAS

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Modelos Atuais do Claude

#### Claude Sonnet 4.5 (Mais Inteligente)

**IDs do Modelo:**
- API Claude: `claude-sonnet-4-5-20250929`
- Alias API: `claude-sonnet-4-5`
- AWS Bedrock: `anthropic.claude-sonnet-4-5-20250929-v1:0`
- GCP Vertex AI: `claude-sonnet-4-5@20250929`

**Especificações:**
- **Janela de Contexto:** 200K tokens (padrão), 1M tokens (beta com cabeçalho `context-1m-2025-08-07`)
- **Saída Máxima:** 64K tokens
- **Corte de Conhecimento:** Janeiro 2025 (confiável), Julho 2025 (dados de treinamento)
- **Preços:** $3/MTok entrada, $15/MTok saída

**Principais Recursos:**
- Melhor modelo de codificação até hoje
- Operação autônoma estendida para tarefas de horas
- Consciência de contexto
- Uso aprimorado de ferramentas com chamadas paralelas
- Geração de conteúdo criativo excepcional
- Planejamento avançado e design de sistemas

#### Claude Haiku 4.5 (Mais Rápido)

**IDs do Modelo:**
- API Claude: `claude-haiku-4-5-20251001`
- Alias API: `claude-haiku-4-5`
- AWS Bedrock: `anthropic.claude-haiku-4-5-20251001-v1:0`
- GCP Vertex AI: `claude-haiku-4-5@20251001`

**Especificações:**
- **Janela de Contexto:** 200K tokens
- **Saída Máxima:** 64K tokens
- **Corte de Conhecimento:** Janeiro 2025
- **Preços:** $1/MTok entrada, $5/MTok saída

**Principais Recursos:**
- Inteligência próxima à fronteira igualando Sonnet 4
- Mais de 2x mais rápido que Sonnet 4
- Primeiro modelo Haiku com pensamento estendido
- Ótima relação custo-desempenho

#### Claude Opus 4.1

**IDs do Modelo:**
- API Claude: `claude-opus-4-1-20250805`
- Alias API: `claude-opus-4-1`
- AWS Bedrock: `anthropic.claude-opus-4-1-20250805-v1:0`
- GCP Vertex AI: `claude-opus-4-1@20250805`

**Especificações:**
- **Janela de Contexto:** 200K tokens
- **Saída Máxima:** 64K tokens
- **Corte de Conhecimento:** Janeiro 2025
- **Preços:** $15/MTok entrada, $75/MTok saída

### Tabela Completa de Preços

#### Preços da API Padrão

| Modelo | Entrada Base | Cache Write 5m | Cache Write 1h | Cache Hits | Saída |
|--------|--------------|----------------|----------------|------------|-------|
| Sonnet 4.5 | $3/MTok | $3.75/MTok | $6/MTok | $0.30/MTok | $15/MTok |
| Haiku 4.5 | $1/MTok | $1.25/MTok | $2/MTok | $0.10/MTok | $5/MTok |
| Opus 4.1 | $15/MTok | $18.75/MTok | $30/MTok | $1.50/MTok | $75/MTok |

#### Preços da API em Lote (50% de Desconto)

| Modelo | Entrada em Lote | Saída em Lote |
|--------|-----------------|---------------|
| Opus 4.1 | $7.50/MTok | $37.50/MTok |
| Sonnet 4.5 | $1.50/MTok | $7.50/MTok |
| Haiku 4.5 | $0.50/MTok | $2.50/MTok |

#### Preços de Contexto Longo (Janela 1M Token)

**Aplica-se a:** Claude Sonnet 4, Sonnet 4.5 (com cabeçalho beta `context-1m-2025-08-07`)

**Para solicitações excedendo 200K tokens de entrada:**

| Tokens | Entrada | Saída |
|--------|---------|-------|
| ≤ 200K | $3/MTok | $15/MTok |
| \u003e 200K | $6/MTok | $22.50/MTok |

### Orientação de Seleção de Modelo

| Caso de Uso | Modelo Recomendado | Raciocínio |
|-------------|-------------------|------------|
| Maior inteligência e raciocínio | Claude Opus 4.1 | Frameworks multi-agente, refatoração complexa |
| Equilíbrio de inteligência e velocidade | Claude Sonnet 4.5 | Chatbots complexos, geração de código, agentes |
| Respostas rápidas, menor custo | Claude Haiku 4.5 | Geração de conteúdo em alto volume, aplicações em tempo real |

---

**Tags**: abstract, general

**Palavras-chave**: ESPECIFICAÇÕES, PARTE, MODELOS, COMPLETAS

**Origem**: unknown


---


<!-- VERSÍCULO 9/12 - marketplace_optimization_parte_3_engenharia_de_prompts_e_melhores_práticas_20251113.md (168 linhas) -->

# PARTE 3: ENGENHARIA DE PROMPTS E MELHORES PRÁTICAS

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Princípios Fundamentais

#### 1. Seja Claro, Direto e Detalhado

**Regra de Ouro:** Mostre seu prompt a um colega com contexto mínimo. Se eles ficarem confusos, Claude também ficará.

**Melhores Práticas:**

- Forneça informações contextuais ao Claude
- Seja específico sobre o que você deseja
- Forneça instruções como etapas sequenciais

**Exemplo: Anonimizando feedback de clientes**

❌ **Prompt Não Claro:**
```
Por favor, remova todas as informações pessoalmente identificáveis destas mensagens de feedback de clientes: {{FEEDBACK_DATA}}
```

✅ **Prompt Claro:**
```
Sua tarefa é anonimizar feedback de clientes para nossa revisão trimestral.

Instruções:
1. Substitua todos os nomes de clientes por "CUSTOMER_[ID]" (ex: "Jane Doe" → "CUSTOMER_001")
2. Substitua endereços de e-mail por "EMAIL_[ID]@example.com"
3. Redija números de telefone como "PHONE_[ID]"
4. Se uma mensagem mencionar um produto específico, deixe intacto
5. Se nenhuma PII for encontrada, copie a mensagem literal
6. Produza apenas as mensagens processadas, separadas por "---"

Dados para processar: {{FEEDBACK_DATA}}
```

#### 2. Use Exemplos (Prompting Multishot)

Exemplos são sua arma secreta para fazer Claude gerar exatamente o que você precisa. Ao fornecer 3-5 exemplos bem elaborados, você pode melhorar dramaticamente a precisão, consistência e qualidade.

**Estrutura de Exemplo:**
```xml
<examples>
  <example>
    <input>{{INPUT_1}}</input>
    <output>{{OUTPUT_1}}</output>
  </example>
  
  <example>
    <input>{{INPUT_2}}</input>
    <output>{{OUTPUT_2}}</output>
  </example>
</examples>
```

#### 3. Deixe Claude Pensar (Chain of Thought)

Quando tarefas requerem pensar através de problemas complexos, peça explicitamente a Claude para pensar passo a passo antes de responder.

**Técnicas CoT (Menos ao Mais Complexo):**

**1. Prompt Básico: "Pense passo a passo"**
```
Calcule o juros composto para um investimento de $10.000 a 5% de taxa anual por 3 anos. Pense passo a passo.
```

**2. Prompt Guiado: Descreva etapas específicas**
```
Calcule o juros composto para um investimento de $10.000 a 5% de taxa anual por 3 anos. Siga estas etapas:
1. Identifique o principal, taxa e tempo
2. Aplique a fórmula de juros composto: A = P(1 + r)^t
3. Calcule o valor final
4. Subtraia o principal para obter juros ganhos
5. Mostre seu trabalho para cada etapa
```

**3. Prompt Estruturado: Use tags XML**
```
Calcule o juros composto para um investimento de $10.000 a 5% de taxa anual por 3 anos.

Coloque seu raciocínio passo a passo em tags <thinking>.
Coloque sua resposta final em tags <answer>.
```

#### 4. Use Tags XML para Estruturar Prompts

Quando prompts envolvem múltiplos componentes (contexto, instruções, exemplos), tags XML ajudam Claude a analisar com precisão, levando a saídas de maior qualidade.

**Melhores Práticas:**

- Seja consistente com nomes de tags
- Aninhe tags para conteúdo hierárquico
- Combine com outras técnicas

**Tags XML Comuns:**
- `<instructions>` - Instruções de tarefa
- `<example>` / `<examples>` - Entradas/saídas de exemplo
- `<context>` - Informações de contexto
- `<document>` - Conteúdo de forma longa
- `<thinking>` - Espaço de raciocínio
- `<answer>` - Resposta final
- `<formatting>` - Especificações de formato de saída

#### 5. Dê a Claude um Papel (System Prompts)

Usar o parâmetro system para dar a Claude um papel é a maneira mais poderosa de usar system prompts. O papel certo transforma Claude de um assistente geral em seu especialista de domínio virtual.

**Exemplo: Análise de Contrato Legal**
```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2048,
    system="Você é um advogado corporativo especialista com 20 anos de experiência revisando contratos SaaS. Você se especializa em identificar riscos relacionados a privacidade de dados, responsabilidade e conformidade com SLA.",
    messages=[{
        "role": "user",
        "content": "Revise este contrato: <contract>{{CONTRACT}}</contract>"
    }]
)
```

#### 6. Preencha Previamente a Resposta de Claude

Preencher previamente permite orientar as respostas de Claude fornecendo o texto inicial na mensagem do Assistente. Claude continua de onde o preenchimento prévio termina.

**Exemplo: Controlando Formato de Saída**
```python
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Gere dados JSON de usuário para Alice, idade 30."},
        {"role": "assistant", "content": "{"}
    ]
)
```

Claude continuará com JSON válido sem preâmbulo.

### Melhores Práticas Claude 4

#### Seja Explícito com Instruções

Modelos Claude 4.x respondem bem a instruções claras e explícitas.

**Exemplo: Criando um painel de análise**
```
❌ Em vez de: "Crie um painel de análise"

✅ Use: "Crie um painel de análise. Inclua tantos recursos e interações relevantes quanto possível. Vá além do básico para criar uma 

[... content truncated ...]

**Tags**: concrete, general

**Palavras-chave**: ENGENHARIA, MELHORES, PROMPTS, PRÁTICAS, PARTE

**Origem**: unknown


---


<!-- VERSÍCULO 10/12 - marketplace_optimization_parte_3_processo_de_destilação_5_fases_20251113.md (130 linhas) -->

# PARTE 3: PROCESSO DE DESTILAÇÃO (5 Fases)

**Categoria**: marketplace_optimization
**Qualidade**: 0.95/1.00
**Data**: 20251113

## Conteúdo

### 3.1 FASE 1: EXTRAÇÃO (RAW → Semantic Units)

**Input:** Documentos brutos (PaddleOCR, articles, research, code comments)

**Processo:**
```
distiller.py:
  ├─ read_raw_document()
  ├─ detect_semantic_boundaries()    [Parágrafos temáticos]
  ├─ extract_entities()               [Termos-chave, conceitos]
  ├─ calculate_entropy()              [Shannon Entropy]
  └─ generate_chunk_metadata()
```

**Output:** `GENESIS/PROCESSING/chunks/doc_001.json`
```json
{
  "chunk_id": "chunk_0042",
  "source_doc": "ecommerce_best_practices.md",
  "text": "A taxonomia de produtos deve ser...",
  "entities": ["taxonomy", "classification", "hierarchy"],
  "entropy_score": 78.5,
  "deus_vs_todo": {
    "abstract_ratio": 0.70,
    "contextual_ratio": 0.30,
    "classification": "theoretical-with-practice"
  },
  "suggested_livro": "LIVRO_02_PRODUCT_MANAGEMENT",
  "suggested_capitulo": "CAPITULO_01_CATALOG_ARCHITECTURE",
  "confidence": 0.92,
  "raw_position": "line_234_to_256"
}
```

### 3.2 FASE 2: CLASSIFICAÇÃO (Chunks → Canon Position)

**Algoritmo de Posicionamento:**
```python
def classify_chunk(chunk):
    # 1. NER: Extrai entidades + contexto
    entities = ner_model(chunk.text)

    # 2. Semantic similarity: Compara com corpus existente
    similarity = semantic_similarity(chunk.text, canon_texts)

    # 3. Domain classification: Determina LIVRO
    livro = classify_domain(entities, similarity)

    # 4. Topic classification: Determina CAPÍTULO
    capitulo = classify_topic(entities, livro)

    # 5. Atomic unit: Gera VERSÍCULO
    versiculo = create_atomic_unit(chunk, livro, capitulo)

    return Canon(livro, capitulo, versiculo)
```

### 3.3 FASE 3: ORGANIZAÇÃO (Criar Ficheiros)

```
organizer.py:
  ├─ create_directory_structure()
  ├─ write_versiculo_file()
  ├─ generate_chapter_metadata()
  ├─ generate_livro_index()
  └─ update_canon_registry()
```

**Resultado:**
```
LIVRO_02_PRODUCT_MANAGEMENT/
├── CAPITULO_01_CATALOG_ARCHITECTURE/
│   ├── VERSÍCULO_001_TAXONOMY.md
│   ├── VERSÍCULO_002_ATTRIBUTES.md
│   ├── _CHAPTER_METADATA.json
└── _LIVRO_INDEX.md
```

### 3.4 FASE 4: VALIDAÇÃO (Quality Gates)

```
validator.py verifica:
  ✓ Completude: Tem title, content, keywords?
  ✓ Singularidade: Não é duplicado em outro VERSÍCULO?
  ✓ Relevância: Entropia > threshold mínimo?
  ✓ Coerência: Faz sentido no contexto do LIVRO/CAP?
  ✓ Formato: Markdown válido? Links corretos?
```

### 3.5 FASE 5: VERSIONAMENTO (Git + Changelog)

```
versioner.py:
  ├─ detect_changes()
  ├─ generate_changelog()
  ├─ git_add()
  ├─ git_commit_with_metadata()
  └─ git_tag(version)
```

**Commit Format:**
```
CANON_ADD: LIVRO_02/CAP_01/VERSÍCULO_001_TAXONOMY

- Source: ecommerce_best_practices.md:234-256
- Entropy: 78/100 → Classified as "Core Knowledge"
- Keywords: +3 novo termos
- Relations: Links 2 existing versículos
- Status: [Stable] version 1.0.0

📚 Generated by CanonDistiller v2.1.0
🔗 Refs: #genesis-distill-001
```

---

**Tags**: ecommerce, concrete

**Palavras-chave**: PARTE, PROCESSO, DESTILAÇÃO, Fases

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 11/12 - marketplace_optimization_parte_4_referência_completa_da_api_20251113.md (125 linhas) -->

# PARTE 4: REFERÊNCIA COMPLETA DA API

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### URL Base
```
https://api.anthropic.com/v1
```

### Autenticação

Todas as requisições requerem um cabeçalho `x-api-key` com sua chave API.

**Cabeçalhos Obrigatórios:**
- `x-api-key`: Sua chave API (obrigatório)
- `anthropic-version`: Versão da API (obrigatório, ex: "2023-06-01")
- `content-type`: "application/json" (obrigatório)

### API de Mensagens (POST /v1/messages)

**Parâmetros de Requisição:**

| Parâmetro | Tipo | Obrigatório | Descrição |
|-----------|------|-------------|-----------|
| `model` | string | Sim | Identificador do modelo |
| `max_tokens` | integer | Sim | Tokens máximos para gerar |
| `messages` | array | Sim | Array de mensagens com role e content |
| `system` | string | Não | System prompt para contexto |
| `temperature` | float | Não | Temperatura de amostragem (0-1) |
| `top_p` | float | Não | Parâmetro de amostragem nucleus |
| `stop_sequences` | array | Não | Sequências personalizadas que param geração |
| `stream` | boolean | Não | Habilitar respostas streaming |
| `tools` | array | Não | Definições de ferramentas |

**Formato de Mensagens:**
```json
{
  "model": "claude-sonnet-4-5",
  "max_tokens": 1024,
  "messages": [
    {
      "role": "user",
      "content": "Olá, Claude"
    }
  ]
}
```

**Formato de Resposta:**
```json
{
  "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Olá! Meu nome é Claude."
    }
  ],
  "model": "claude-sonnet-4-5",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 2095,
    "output_tokens": 503
  }
}
```

### API de Lotes de Mensagens

#### Criar Lote de Mensagens (POST /v1/messages/batches)

Processe múltiplas requisições da API Messages de forma assíncrona.

**Limites de Lote:**
- Máximo: 100.000 requisições OU 256 MB por lote
- Tempo de processamento: Até 24 horas
- Resultados disponíveis por: 29 dias
- Custo: 50% de desconto em todo uso

### API de Modelos

#### Listar Modelos (GET /v1/models)
Lista modelos disponíveis (mais recentes primeiro).

#### Obter Modelo (GET /v1/models/{model_id})
Obter informações sobre um modelo específico.

### Contagem de Tokens (POST /v1/messages/count_tokens)

Conte tokens em uma mensagem sem criá-la.

### API de Arquivos

#### Criar Arquivo (POST /v1/files)
Enviar um arquivo (recurso beta).

#### Listar Arquivos (GET /v1/files)
Listar arquivos no workspace.

### Códigos de Status HTTP

| Código | Tipo de Erro | Descrição |
|--------|-------------|-----------|
| 400 | `invalid_request_error` | Problema de formato/conteúdo da requisição |
| 401 | `authentication_error` | Problema com chave API |
| 403 | `permission_error` | Sem permissão para recurso |
| 404 | `not_found_error` | Recurso não encontrado |
| 429 | `rate_limit_error` | Limite de taxa excedido |
| 500 | `api_error` | Erro interno do servidor |
| 529 | `overloaded_error` | API temporariamente sobrecarregada |

---

**Tags**: general, implementation

**Palavras-chave**: PARTE, COMPLETA, REFERÊNCIA

**Origem**: unknown


---


<!-- VERSÍCULO 12/12 - marketplace_optimization_parte_4_sistema_de_entropia_medindo_densidade_de_i_20251113.md (85 linhas) -->

# PARTE 4: SISTEMA DE ENTROPIA (Medindo Densidade de Info)

**Categoria**: marketplace_optimization
**Qualidade**: 0.95/1.00
**Data**: 20251113

## Conteúdo

### 4.1 Shannon Entropy para E-Commerce

```python
def calculate_entropy(text, domain="ecommerce"):
    """
    Mede quantidade de informação nova em relação ao corpus existente

    Fórmula: H(X) = -∑ P(x) * log₂(P(x))

    Alto (80-100) = Muito específico, denso, novo
    Médio (50-79) = Bom para contexto, prático
    Baixo (0-49) = Informação óbvia, genérica
    """

    # 1. Character entropy (probabilidade de caracteres)
    char_entropy = shannon_entropy(text)

    # 2. Token entropy (informação por token)
    token_entropy = token_information_content(text)

    # 3. Semantic novelty (quanto é novo para o corpus)
    semantic_entropy = semantic_novelty_score(text, canon_texts)

    # 4. Domain specificity (quanto é específico de e-commerce)
    domain_entropy = domain_specificity(text, "ecommerce")

    # Weighted average
    total = (char_entropy * 0.2 +
             token_entropy * 0.2 +
             semantic_entropy * 0.3 +
             domain_entropy * 0.3)

    return normalize(total, 0, 100)
```

### 4.2 Deus vs Todo (Abstração vs Contextualidade)

```python
def classify_abstraction_level(text):
    """
    DEUS (0%):     Puramente teórico, universal, atemporalmente válido
    MIXED (50%):   Conceitos universais com aplicações específicas
    TODO (100%):   Totalmente contextual, case-specific, temporal

    Exemplo:
    - DEUS (95%): "ACID properties are fundamental to transactional integrity"
    - MIXED (50%): "PostgreSQL provides ACID guarantees; MySQL with InnoDB also does"
    - TODO (15%): "Our production uses PostgreSQL 14.2 in us-east-1"
    """

    # Analyze temporal references
    temporal_score = detect_temporal_references(text)

    # Analyze context-specific terms
    context_score = detect_context_specifics(text)

    # Analyze universal concepts
    universal_score = detect_universal_concepts(text)

    deus_ratio = universal_score / (universal_score + context_score)
    todo_ratio = 1 - deus_ratio

    return {
        "deus": deus_ratio * 100,
        "todo": todo_ratio * 100,
        "classification": classify_type(deus_ratio)
    }
```

---

**Tags**: ecommerce, abstract

**Palavras-chave**: PARTE, SISTEMA, ENTROPIA, Medindo, Densidade, Info

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- FIM DO CAPÍTULO 48 -->
<!-- Total: 12 versículos, 1181 linhas -->
