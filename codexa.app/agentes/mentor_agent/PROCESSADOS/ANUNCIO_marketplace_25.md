# LIVRO: Marketplace
## CAPÍTULO 25

**Versículos consolidados**: 16
**Linhas totais**: 1181
**Gerado em**: 2025-11-13 18:45:49

---


<!-- VERSÍCULO 1/16 - marketplace_optimization_agent_architecture_patterns_20251113.md (156 linhas) -->

# Agent Architecture Patterns

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### CARD-030: Blueprint de Prompt (6 Camadas)
**KEYWORDS:** `prompt-engineering|agent-architecture|layered-prompts`

**Estrutura em Camadas:**

```
[LAYER 1: SYSTEM]
├─ Identidade do agente
├─ Objetivo da tarefa
└─ Guardrails (sempre incluído)

[LAYER 2: KNOWLEDGE CONTEXT]
├─ Top-K cards relevantes (RAG)
├─ Namespace prioritário
└─ Glossário específico do domínio

[LAYER 3: TASK DEFINITION]
├─ Input esperado
├─ Output esperado
├─ Formato estruturado (JSON/Markdown)
└─ Exemplos (few-shot)

[LAYER 4: CONSTRAINTS]
├─ Tempo limite
├─ Tamanho máximo de output
├─ Políticas de compliance
└─ Regras de negócio

[LAYER 5: REASONING GUIDANCE]
├─ Chain-of-thought prompting
├─ Step-by-step decomposition
└─ Self-verification

[LAYER 6: OUTPUT FORMATTING]
├─ Template de saída
├─ Validation schema
└─ Error handling
```

**Como Aplicar:**
1. Sempre começar com System + Guardrails
2. Injetar Knowledge Context via RAG
3. Definir Task com exemplos
4. Especificar Constraints claros
5. Guiar raciocínio passo-a-passo
6. Formatar output estruturado

**Confidence:** 96% | **Weight:** 5 | **Source:** biblia_lcm_large_commerce_model_playbook_de_destilacao_v_0.md

---

### CARD-031: Mapeamento de Temperatura e Pesos
**KEYWORDS:** `temperature|weights|model-config`

**Configurações de Temperatura:**

| Uso | Temperatura | Quando Usar |
|-----|-------------|-------------|
| Determinístico | 0.0 - 0.3 | Análise, classificação, extração |
| Balanceado | 0.4 - 0.7 | Research, síntese, recomendações |
| Criativo | 0.8 - 1.2 | Copywriting, brainstorming, variações |
| Experimental | 1.3 - 1.5 | Exploração de ideias, art direction |

**Fórmula de Conversão (0-100 → 0-1.5):**
```python
temp_model = min(1.5, round(temperatura_criativa / 100 * 1.5, 2))
```

**Pesos por Namespace (1-5):**

| Namespace | Peso | Uso |
|-----------|------|-----|
| `guardrails` | 999 | Sempre incluído |
| `core` | 5 | Fundamentos sempre relevantes |
| `meli-br` | 4 | Marketplace específico |
| `marketing` | 3 | Domínio geral |
| `contabilidade` | 2 | Especializado |
| `websearch` | 1 | Dados externos |

**Como Aplicar:**
1. Escolher temperatura baseada no tipo de tarefa
2. Atribuir pesos aos namespaces por relevância
3. Ajustar dinamicamente com feedback
4. Monitorar performance e recalibrar

**Confidence:** 95% | **Weight:** 4 | **Source:** biblia_lcm_large_commerce_model_playbook_de_destilacao_v_0.md

---

### CARD-032: Fusão de Resultados (Hybrid Search)
**KEYWORDS:** `rag|hybrid-search|retrieval|fusion`

**Estratégia de Fusão (RRF - Reciprocal Rank Fusion):**

```
1. BM25 (Full-Text Search)
   ├─ Busca por keywords exatas
   ├─ Scoring baseado em TF-IDF
   └─ Retorna top-K resultados

2. Vector Search (Embeddings)
   ├─ Busca por similaridade semântica
   ├─ Scoring baseado em cosine similarity
   └─ Retorna top-K resultados

3. RRF Fusion
   ├─ score_rrf = Σ (1 / (rank + k))
   ├─ k = 60 (constante padrão)
   └─ Multiplicadores por namespace

4. Reranker (Opcional)
   ├─ Cross-encoder para relevância final
   └─ Top-N resultados finais
```

**Fórmula RRF com Pesos:**
```python
def rrf_score(rank_bm25, rank_vector, namespace_weight, k=60):
    score_bm25 = 1 / (rank_bm25 + k)
    score_vector = 1 / (rank_vector + k)
    return (score_bm25 + score_vector) * namespace_weight
```

**Configurações Recomendadas:**

| Parâmetro | Valor | Descrição |
|-----------|-------|-----------|
| k_vector | 8 | Top-8 similaridade semântica |
| k_bm25 | 8 | Top-8 keyword match |
| k_constant | 60 | Constante RRF |
| rerank_top_n | 5 | Resultados finais |

**Como Aplicar:**
1. Executar BM25 e Vector search em paralelo
2. Aplicar RRF com multiplicadores de namespace
3. Opcional: Reranker para top-N final
4. Retornar cards ordenados por relevância

**Confidence:** 94% | **Weight:** 4 | **Source:** biblia_lcm_large_commerce_model_playbook_de_destilacao_v_0.md

---

**Tags**: lem, concrete

**Palavras-chave**: Architecture, Agent, Patterns

**Origem**: unknown


---


<!-- VERSÍCULO 2/16 - marketplace_optimization_agent_isolation_20251112_112210_20251113.md (58 linhas) -->

# Agent Isolation 20251112 112210 | marketplace_optimization

## CONCEITOS-CHAVE

• **Fundamentos**: Este conhecimento aborda conceitos essenciais para vendedores que querem crescer no e-commerce brasileiro
• **Aplicação Prática**: Técnicas e estratégias que você pode aplicar hoje mesmo nos seus produtos
• **Resultados Mensuráveis**: Foco em ações que geram impacto direto nas suas vendas
• **Marketplaces**: Conhecimento aplicável ao Mercado Livre, Shopee, Magalu e outros canais

## POR QUE IMPORTA

Se você vende online no Brasil, sabe que a concorrência está cada vez maior. Este conhecimento foi criado para te ajudar a se destacar da multidão e vender mais.

No cenário atual dos marketplaces brasileiros, quem domina as técnicas certas consegue resultados até 3x melhores que a média. Seja otimizando títulos para o algoritmo do Mercado Livre, criando descrições que convencem, ou automatizando processos repetitivos - cada detalhe conta.

## COMO FAZER

1. **Comece pelo básico**: Analise sua situação atual e identifique onde você pode melhorar
2. **Aplique as técnicas**: Implemente as estratégias de forma gradual, começando pelos produtos mais importantes
3. **Teste e ajuste**: Monitore os resultados e faça ajustes conforme necessário
4. **Escale o que funciona**: Quando encontrar uma estratégia vencedora, replique para todos os produtos
5. **Automatize processos**: Use ferramentas e scripts para economizar tempo nas tarefas repetitivas
6. **Acompanhe métricas**: Fique de olho em conversão, visualizações e posição nos resultados de busca
7. **Mantenha-se atualizado**: Os marketplaces mudam constantemente - adapte suas estratégias

## EXEMPLO REAL

**Antes**: Vendedor com 50 produtos no Mercado Livre, títulos genéricos, fotos padrão do fornecedor, descrições copiadas. Taxa de conversão: 1.2%, aparecendo na 5ª página de resultados.

**Depois**: Após aplicar as técnicas de otimização - títulos com palavras-chave estratégicas, fotos profissionais com fundo branco, descrições persuasivas com gatilhos mentais, uso de ferramentas de automação para atualizar preços.

**Resultado**: Taxa de conversão subiu para 3.8% (+217%), produtos aparecendo na primeira página, vendas aumentaram de 15 para 42 unidades/mês por produto (+180%). Tempo gasto em gestão reduziu de 4h para 1h por dia graças à automação.

## BOAS PRÁTICAS

• **Seja consistente**: Aplique as técnicas em todos os seus produtos, não apenas em alguns
• **Teste sempre**: O que funciona para um vendedor pode não funcionar para outro - teste e descubra o que dá certo no seu nicho
• **Foque no cliente**: Pense sempre em como facilitar a decisão de compra do seu cliente
• **Use dados**: Baseie suas decisões em números reais, não em achismos
• **Automatize o repetitivo**: Use ferramentas para economizar tempo e focar no estratégico

## PRÓXIMOS PASSOS

Depois de dominar este conteúdo, explore:
• Técnicas avançadas de SEO para marketplaces
• Estratégias de precificação dinâmica
• Automação de processos com Python
• Análise de concorrência e benchmarking
• Gatilhos mentais aplicados ao e-commerce

---
**Categoria**: marketplace_optimization
**Nível**: intermediário
**Tags**: mercadolivre, api
**Aplicação**: quando_otimizar_operacoes
**Fonte**: RASCUNHO/agent-isolation_20251112_112210.md
**Processado**: 20251113


---


<!-- VERSÍCULO 3/16 - marketplace_optimization_agent_isolation_20251113.md (58 linhas) -->

# Agent Isolation | marketplace_optimization

## CONCEITOS-CHAVE

• **Fundamentos**: Este conhecimento aborda conceitos essenciais para vendedores que querem crescer no e-commerce brasileiro
• **Aplicação Prática**: Técnicas e estratégias que você pode aplicar hoje mesmo nos seus produtos
• **Resultados Mensuráveis**: Foco em ações que geram impacto direto nas suas vendas
• **Marketplaces**: Conhecimento aplicável ao Mercado Livre, Shopee, Magalu e outros canais

## POR QUE IMPORTA

Se você vende online no Brasil, sabe que a concorrência está cada vez maior. Este conhecimento foi criado para te ajudar a se destacar da multidão e vender mais.

No cenário atual dos marketplaces brasileiros, quem domina as técnicas certas consegue resultados até 3x melhores que a média. Seja otimizando títulos para o algoritmo do Mercado Livre, criando descrições que convencem, ou automatizando processos repetitivos - cada detalhe conta.

## COMO FAZER

1. **Comece pelo básico**: Analise sua situação atual e identifique onde você pode melhorar
2. **Aplique as técnicas**: Implemente as estratégias de forma gradual, começando pelos produtos mais importantes
3. **Teste e ajuste**: Monitore os resultados e faça ajustes conforme necessário
4. **Escale o que funciona**: Quando encontrar uma estratégia vencedora, replique para todos os produtos
5. **Automatize processos**: Use ferramentas e scripts para economizar tempo nas tarefas repetitivas
6. **Acompanhe métricas**: Fique de olho em conversão, visualizações e posição nos resultados de busca
7. **Mantenha-se atualizado**: Os marketplaces mudam constantemente - adapte suas estratégias

## EXEMPLO REAL

**Antes**: Vendedor com 50 produtos no Mercado Livre, títulos genéricos, fotos padrão do fornecedor, descrições copiadas. Taxa de conversão: 1.2%, aparecendo na 5ª página de resultados.

**Depois**: Após aplicar as técnicas de otimização - títulos com palavras-chave estratégicas, fotos profissionais com fundo branco, descrições persuasivas com gatilhos mentais, uso de ferramentas de automação para atualizar preços.

**Resultado**: Taxa de conversão subiu para 3.8% (+217%), produtos aparecendo na primeira página, vendas aumentaram de 15 para 42 unidades/mês por produto (+180%). Tempo gasto em gestão reduziu de 4h para 1h por dia graças à automação.

## BOAS PRÁTICAS

• **Seja consistente**: Aplique as técnicas em todos os seus produtos, não apenas em alguns
• **Teste sempre**: O que funciona para um vendedor pode não funcionar para outro - teste e descubra o que dá certo no seu nicho
• **Foque no cliente**: Pense sempre em como facilitar a decisão de compra do seu cliente
• **Use dados**: Baseie suas decisões em números reais, não em achismos
• **Automatize o repetitivo**: Use ferramentas para economizar tempo e focar no estratégico

## PRÓXIMOS PASSOS

Depois de dominar este conteúdo, explore:
• Técnicas avançadas de SEO para marketplaces
• Estratégias de precificação dinâmica
• Automação de processos com Python
• Análise de concorrência e benchmarking
• Gatilhos mentais aplicados ao e-commerce

---
**Categoria**: marketplace_optimization
**Nível**: intermediário
**Tags**: mercadolivre, seo, python
**Aplicação**: quando_criar_anuncios
**Fonte**: RASCUNHO/agent-isolation.md
**Processado**: 20251113


---


<!-- VERSÍCULO 4/16 - marketplace_optimization_agentic_kpis_20251113.md (26 linhas) -->

# Agentic KPIs

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

Summary metrics across all ADW runs.

| Metric            | Value          | Last Updated             |
| ----------------- | -------------- | ------------------------ |
| Current Streak    | 1              | Thu Jul 31 12:06:52 CDT 2025 |
| Longest Streak    | 1              | Thu Jul 31 12:06:52 CDT 2025 |
| Total Plan Size   | 39 lines       | Thu Jul 31 12:06:52 CDT 2025 |
| Largest Plan Size | 39 lines       | Thu Jul 31 12:06:52 CDT 2025 |
| Total Diff Size   | 279 lines      | Thu Jul 31 12:06:52 CDT 2025 |
| Largest Diff Size | 279 lines      | Thu Jul 31 12:06:52 CDT 2025 |
| Average Presence  | 1.0            | Thu Jul 31 12:06:52 CDT 2025 |

**Tags**: general, intermediate

**Palavras-chave**: Agentic, KPIs

**Origem**: unknown


---


<!-- VERSÍCULO 5/16 - marketplace_optimization_agentic_success_metrics_20251113.md (60 linhas) -->

# Agentic Success Metrics

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```yaml
attempts_metric:
  name: "Attempts to Success"
  goal: MINIMIZE
  target: "<3 iterations"
  meaning: "Fewer retries = better understanding"
  
streak_metric:
  name: "Success Streak"
  goal: MAXIMIZE
  target: ">100 consecutive successes"
  meaning: "Consistency and reliability"
  
size_metric:
  name: "Problem Size"
  goal: MAXIMIZE
  target: "Larger, more complex problems"
  meaning: "Growing capability"
  
presence_metric:
  name: "Human Intervention"
  goal: MINIMIZE
  target: "<10% touchpoints"
  meaning: "Moving toward autonomy"

progression_stages:
  IN_LOOP:
    presence: high
    control: manual
    touchpoints: many
    
  OUT_LOOP:
    presence: medium
    control: automated_with_review
    touchpoints: 2 (prompt + review)
    
  ZERO_TOUCH:
    presence: minimal
    control: fully_automated
    touchpoints: 1 (prompt only)
```

---

# PART VIII: THE AGENTIC LAYER

**Tags**: general, intermediate

**Palavras-chave**: Success, Metrics, Agentic

**Origem**: unknown


---


<!-- VERSÍCULO 6/16 - marketplace_optimization_ai_developer_workflow_adw_20251113.md (74 linhas) -->

# AI Developer Workflow (ADW)

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

The ADW system is a comprehensive automation framework that integrates GitHub issues with Claude Code CLI to classify issues, generate implementation plans, and automatically create pull requests. ADW processes GitHub issues by classifying them as `/chore`, `/bug`, or `/feature` commands and then implementing solutions autonomously.

**For complete Python scripts documentation, see: [PYTHON_SCRIPTS_GUIDE.md](PYTHON_SCRIPTS_GUIDE.md)**

### Prerequisites

Before using ADW, ensure you have the following installed and configured:

- **GitHub CLI**: `brew install gh` (macOS) or equivalent for your OS
- **Claude Code CLI**: Install from [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)
- **Python with uv**: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **GitHub authentication**: `gh auth login`

### Environment Variables

Set these environment variables before running ADW:

```bash
export GITHUB_REPO_URL="https://github.com/owner/repository"
export ANTHROPIC_API_KEY="sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export CLAUDE_CODE_PATH="/path/to/claude"  # Optional, defaults to "claude"
export GITHUB_PAT="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Optional, only if using different account than 'gh auth login'
```

### Usage Modes

ADW supports three main operation modes:

#### 1. Manual Processing
Process a single GitHub issue manually (in isolated worktree):
```bash
cd adws/
uv run adw_plan_build_iso.py <issue-number>
```

#### 2. Automated Monitoring
Continuously monitor GitHub for new issues (polls every 20 seconds):
```bash
cd adws/
uv run trigger_cron.py
```

#### 3. Webhook Server
Start a webhook server for real-time GitHub event processing:
```bash
cd adws/
uv run trigger_webhook.py
```

### How ADW Works

1. **Issue Classification**: Analyzes GitHub issues and determines type (`/chore`, `/bug`, `/feature`)
2. **Planning**: Generates detailed implementation plans using Claude Code CLI
3. **Implementation**: Executes the plan by making code changes, running tests, and ensuring quality
4. **Integration**: Creates git commits and pull requests with semantic commit messages

### For More Information

For detailed technical documentation, configuration options, and troubleshooting, see [`adws/README.md`](adws/README.md).

**Tags**: abstract, general

**Palavras-chave**: Developer, Workflow

**Origem**: unknown


---


<!-- VERSÍCULO 7/16 - marketplace_optimization_analyze_image_inputs_20251113.md (94 linhas) -->

# Analyze image inputs

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

You can provide image inputs to the model as well. Scan receipts, analyze screenshots, or find objects in the real world with [computer vision](https://platform.openai.com/docs/guides/images).

### Analyze the content of an image

#### JavaScript

```javascript
import OpenAI from "openai";
const client = new OpenAI();

const response = await client.responses.create({
    model: "gpt-4.1",
    input: [
        { role: "user", content: "What two teams are playing in this photo?" },
        {
            role: "user",
            content: [
                {
                    type: "input_image",
                    image_url: "https://upload.wikimedia.org/wikipedia/commons/3/3b/LeBron_James_Layup_%28Cleveland_vs_Brooklyn_2018%29.jpg",
                }
            ],
        },
    ],
});

console.log(response.output_text);
```

#### Python

```python
from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-4.1",
    input=[
        {"role": "user", "content": "what teams are playing in this image?"},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3b/LeBron_James_Layup_%28Cleveland_vs_Brooklyn_2018%29.jpg"
                }
            ]
        }
    ]
)

print(response.output_text)
```

#### cURL

```bash
curl "https://api.openai.com/v1/responses" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-4.1",
        "input": [
            {
                "role": "user",
                "content": "What two teams are playing in this photo?"
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3b/LeBron_James_Layup_%28Cleveland_vs_Brooklyn_2018%29.jpg"
                    }
                ]
            }
        ]
    }'
```

**Tags**: concrete, general

**Palavras-chave**: inputs, image, Analyze

**Origem**: unknown


---


<!-- VERSÍCULO 8/16 - marketplace_optimization_antes_e_depois_do_push_20251113.md (50 linhas) -->

# ANTES E DEPOIS DO PUSH

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

ANTES:
┌──────────────────────────────────────────────────────────┐
│  Seu Repositório Local                                   │
│  main                                                    │
│  ├── ...anterior                                         │
│  ├── aa7a9c2 - docs: Add Biblia LEM summary            │
│  └── 31dfa6d - feat: Consolidate LEM (NÃO ENVIADO)      │
│                                                          │
│  ⚠️ Seu código local tem commits não enviados!           │
│  💾 Se seu PC quebrar, perde esses commits!              │
└──────────────────────────────────────────────────────────┘

                   git push origin main
                          ↓

DEPOIS:
┌──────────────────────────────────────────────────────────┐
│  Seu Repositório Local                                   │
│  main (atualizado com origin/main)                       │
│  ├── ...anterior                                         │
│  ├── aa7a9c2 - docs: Add Biblia LEM summary            │
│  └── 31dfa6d - feat: Consolidate LEM ✓ ENVIADO         │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│  GitHub Repository (origin/main)                         │
│  main                                                    │
│  ├── ...anterior                                         │
│  ├── aa7a9c2 - docs: Add Biblia LEM summary            │
│  └── 31dfa6d - feat: Consolidate LEM ✓ SINCRONIZADO    │
└──────────────────────────────────────────────────────────┘

✅ Local e remoto estão sincronizados!
✅ Seus commits estão seguros no GitHub!
✅ Outros podem acessar seu código!

**Tags**: general, intermediate

**Palavras-chave**: PUSH, ANTES, DEPOIS

**Origem**: unknown


---


<!-- VERSÍCULO 9/16 - marketplace_optimization_antipatterns_avoid_20251113.md (42 linhas) -->

# ANTIPATTERNS (Avoid)

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```yaml
duplicated_logic:
  problem: same_action_in_multiple_places
  solution: one_slash_command_multiple_callers
  
ad_hoc_prompts:
  problem: unversioned_unreproducible
  solution: commit_all_prompts_to_codebase
  
god_model:
  problem: one_agent_does_everything
  solution: specialized_agents_per_purpose
  
manual_testing:
  problem: human_bottleneck
  solution: automated_validation_loops
  
context_pollution:
  problem: overloaded_context_window
  solution: minimum_context_principle
  
no_feedback_loops:
  problem: brittle_agents
  solution: closed_loop_validation
```

---

**Tags**: abstract, general

**Palavras-chave**: ANTIPATTERNS, Avoid

**Origem**: unknown


---


<!-- VERSÍCULO 10/16 - marketplace_optimization_análise_de_concorrentes_20251113.md (151 linhas) -->

# [ANÁLISE DE CONCORRENTES]

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Mapa de Posicionamento
```
Qualidade
    ^
 1.0|        [Premium Zone]
    |    ● Produto C (R$ 450)
 0.7|  [Value Zone]
    | ● Produto A (R$ 299)
 0.5|     ● Nosso Produto [OPORTUNIDADE]
    |   ● Produto B (R$ 189)
 0.3|    [Budget Zone]
    |
 0.0+-------------------------->
    0    0.3   0.5   0.7   1.0  Preço
```

### Análise Individual

#### Concorrente 1: "Mochila Exec Couro Notebook 15.6"
- **Preço:** R$ 299
- **Rating:** 4.8/5 (2.341 reviews)
- **Marketplace:** Mercado Livre
- **Forças:**
  - Prova social excepcional (volume alto de reviews)
  - Título SEO-otimizado completo
  - Imagens profissionais (8 fotos)
  - Frete grátis destacado
  - Badge MercadoLíder
- **Fraquezas:**
  - Descrição genérica e curta (180 palavras)
  - Sem storytelling ou conexão emocional
  - Características listadas sem benefícios
  - Imagens sem contexto lifestyle
- **Oportunidade:**
  - Superá-lo com descrição rica + lifestyle images
  - Adicionar prova social de autoridade (certificações)
  - Novelty Score: 3/5

#### Concorrente 2: "Mochila Couro Sintético Trabalho"
[Análise similar]

### Feature Gap Analysis
**Must-Have (70%+ presença):**
- Compartimento notebook
- Múltiplos bolsos
- Alças ajustáveis
- Zíper resistente

**Differentiators (< 30% presença):**
- Porta USB integrada ⭐ OPORTUNIDADE
- Bolso anti-furto ⭐ OPORTUNIDADE
- Material impermeável ⭐ OPORTUNIDADE
- Garantia estendida

### Estratégias Vencedoras Identificadas
1. Título longo com 3+ atributos (conversão 23% maior)
2. Primeira imagem: fundo branco, produto 80%+ (CTR 34% maior)
3. Frete grátis destacado no título (conversão 18% maior)
4. Badge de garantia visível (confiança +12%)

### Gaps Exploráveis
1. **Nenhum concorrente enfatiza sustentabilidade do couro**
2. **Poucos mostram produto em uso real (lifestyle)**
3. **Descrições não endereçam objeções comuns**
4. **Imagens não demonstram capacidade/organização interna**
```

#### Fase 7: Compliance e Risk Assessment

```python
def check_compliance(product, category, marketplace):
    """
    Verifica compliance com regras do marketplace e regulamentações
    """
    issues = {
        'blocked_terms': [],
        'required_disclaimers': [],
        'prohibited_claims': [],
        'category_requirements': [],
        'legal_requirements': []
    }
    
    # 1. Termos proibidos por marketplace
    prohibited = get_prohibited_terms(marketplace, category)
    for term in prohibited:
        if term in product['description'].lower():
            issues['blocked_terms'].append(term)
    
    # 2. Claims que requerem prova
    regulated_claims = [
        'hipoalergênico', 'dermatologicamente testado',
        'aprovado pela ANVISA', 'certificado INMETRO',
        'made in', 'original', 'genuíno'
    ]
    for claim in regulated_claims:
        if claim in product['description'].lower():
            issues['required_disclaimers'].append(
                f"Claim '{claim}' requer prova/certificação"
            )
    
    # 3. Requisitos por categoria
    category_rules = get_category_rules(marketplace, category)
    for rule in category_rules:
        if not check_rule(product, rule):
            issues['category_requirements'].append(rule)
    
    # 4. Regulamentações legais (Brasil)
    if category in ['eletrônicos', 'brinquedos', 'alimentos']:
        legal = check_legal_requirements(product, category)
        issues['legal_requirements'].extend(legal)
    
    return issues

def get_prohibited_terms(marketplace, category):
    """
    Base de dados de termos proibidos por marketplace
    """
    prohibited_db = {
        'mercadolivre': {
            'all': ['melhor', 'número 1', 'clique aqui', 'WhatsApp', 'contato'],
            'saude': ['cura', 'tratamento', 'emagrece', 'medicamento']
        },
        'amazon': {
            'all': ['Amazon choice', 'prime exclusivo', 'melhor vendido'],
        },
        # ...
    }
    
    general = prohibited_db.get(marketplace, {}).get('all', [])
    category_specific = prohibited_db.get(marketplace, {}).get(category, [])
    
    return general + category_specific
```

**Output Esperado:**
```markdown

**Tags**: concrete, general

**Palavras-chave**: ANÁLISE, CONCORRENTES

**Origem**: unknown


---


<!-- VERSÍCULO 11/16 - marketplace_optimization_api_issues_20251113.md (122 linhas) -->

# API Issues

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Problem: Rate Limiting / Too Many Requests

**Symptoms:**
```
RateLimitError: Rate limit exceeded
Error 429: Too Many Requests
```

**Decision Tree:**

```
How frequently are requests?
├─ <100 requests/min → Check quota usage:
│                      https://console.anthropic.com/account/usage
│
└─ 100+ requests/min → Implement backoff:
                       ├─ Add delay between requests
                       ├─ Queue requests
                       └─ Use batch processing
```

**Solution:**
```python
# 1. Check API usage
# Visit: https://console.anthropic.com/account/usage

# 2. Implement exponential backoff
import time
from anthropic import Anthropic, RateLimitError

client = Anthropic()
max_retries = 3
base_delay = 1

for attempt in range(max_retries):
    try:
        response = client.messages.create(...)
        break
    except RateLimitError:
        delay = base_delay * (2 ** attempt)
        print(f"Rate limited. Retrying in {delay}s...")
        time.sleep(delay)

# 3. Configure in .env
# API_RATE_LIMIT_REQUESTS_PER_MINUTE=100
# API_RETRY_DELAY_SECONDS=5
```

---

### Problem: Connection Refused / Timeout

**Symptoms:**
```
ConnectionError: Failed to establish connection
Timeout: Request timed out
```

**Decision Tree:**

```
Is network working?
├─ NO → Check internet connection:
│       ping 8.8.8.8
│       ping api.anthropic.com
│
└─ YES → Is firewall blocking?
    ├─ YES → Allow HTTPS (443) to api.anthropic.com
    │
    └─ NO → Are you behind proxy?
            ├─ YES → Configure proxy in .env
            │        HTTP_PROXY=...
            │        HTTPS_PROXY=...
            │
            └─ NO → API server down?
                    Check: status.anthropic.com
```

**Solution:**
```bash
# 1. Test connectivity
ping api.anthropic.com
curl -I https://api.anthropic.com/v1/messages

# 2. Configure proxy (if needed)
# Edit .env:
# HTTP_PROXY=http://proxy.company.com:8080
# HTTPS_PROXY=http://proxy.company.com:8080

# 3. Test with timeout adjustment
python3 << 'EOF'
from anthropic import Anthropic

client = Anthropic(timeout=60.0)  # 60 second timeout
try:
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=10,
        messages=[{"role": "user", "content": "test"}]
    )
    print("✓ Connection successful")
except Exception as e:
    print(f"✗ Connection failed: {e}")
EOF
```

---

**Tags**: general, implementation

**Palavras-chave**: Issues

**Origem**: unknown


---


<!-- VERSÍCULO 12/16 - marketplace_optimization_api_reference_20251113.md (53 linhas) -->

# API Reference

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Classe/Função: nome()

**Assinatura:**
```python
def nome(
    param1: Type,
    param2: Type = default
) -> ReturnType:
```

**Parâmetros:**
- `param1` (Type): [Descrição clara, range/constraints]
- `param2` (Type, default=default): [Descrição]

**Retorna:**
- Type: [O que retorna, formato]

**Raises:**
- `ErrorType`: [Quando ocorre]

**Exemplos:**

```python
# Exemplo 1: Uso básico
result = nome(arg1, arg2)

# Exemplo 2: Com todos parâmetros
result = nome(
    param1=valor,
    param2=outro_valor
)

# Exemplo 3: Edge case
try:
    result = nome(None)  # Erro esperado
except ValueError as e:
    print(f"Capturado: {e}")
```

**Tags**: general, intermediate

**Palavras-chave**: Reference

**Origem**: unknown


---


<!-- VERSÍCULO 13/16 - marketplace_optimization_api_reference_completo_20251113.md (98 linhas) -->

# API Reference (Completo)

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

[... documentação exaustiva ...]
```

**Por que funciona:**

- **Respeita níveis de expertise**: Usuário novato lê TL;DR, expert pula para API Reference
- **Fácil scanning**: LLM pode identificar qual seção precisa
- **Não polui context**: Iniciante não é forçado a consumir 50 parágrafos

### 2.4 Taxonomia e Categorização

**Sistema de Tags Semântico:**

```markdown
# Função: calculate_loss()

**Categoria:** Training / Loss Functions  
**Complexidade:** ⭐⭐⭐ (Intermediário)  
**Tipo:** Utility Function  
**Domínio:** Deep Learning > Optimization  
**Keywords:** loss, training, backpropagation, gradient  
**Related:** [optimizer.step()](#optimizer), [backward()](#backward)  
**Version Added:** 1.0  
**Stability:** Stable  

---

[Documentação da função...]
```

**Benefícios para LLM:**

1. **Classificação multi-dimensional**: LLM pode filtrar por categoria, complexidade, domínio
2. **Keywords explícitas**: Melhoram retrieval semântico
3. **Relações explicitadas**: "Related" cria grafo de conhecimento
4. **Metadados úteis**: Version/Stability informam confiabilidade

**Sistema de Categorização Hierárquico:**

```
Sistema de IA
├── Pretraining
│   ├── Datasets
│   │   ├── Web Data (FineWeb, DCLM)
│   │   ├── Code Data (StarCoder)
│   │   └── Math Data (FineMath)
│   ├── Architecture
│   │   └── Transformer
│   └── Training
│       ├── Distributed Training
│       └── Mixed Precision
├── Fine-tuning
│   ├── Supervised Fine-Tuning (SFT)
│   │   ├── SFTTrainer
│   │   └── Dataset Formatting
│   └── Preference Alignment
│       ├── DPO (Direct Preference Optimization)
│       ├── RLHF (Reinforcement Learning from Human Feedback)
│       └── IPO (Identity Preference Optimization)
└── Deployment
    ├── Quantization
    ├── Inference Optimization
    └── Model Serving
```

**Como embedar taxonomia em docs:**

```markdown
# SFTTrainer

**Caminho na Taxonomia:**  
`Sistema de IA > Fine-tuning > Supervised Fine-Tuning (SFT) > SFTTrainer`

**Conceito Pai:** [Supervised Fine-Tuning](#sft)  
**Conceitos Irmãos:** [DatasetFormatting](#dataset-formatting)  
**Conceitos Filhos:** [TrainingArguments](#training-arguments), [Callbacks](#callbacks)

---

[Documentação...]
```

---

**Tags**: concrete, general

**Palavras-chave**: Reference, Completo

**Origem**: unknown


---


<!-- VERSÍCULO 14/16 - marketplace_optimization_api_reference_integra_o_20251113.md (88 linhas) -->

# 📊 API Reference (Integração)

**Categoria**: marketplace_optimization
**Qualidade**: 0.71/1.00
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
  "differentiation_angles": [...

**Tags**: ecommerce, general, implementation

**Palavras-chave**: Reference, Integração

**Origem**: desconhecida


---


<!-- VERSÍCULO 15/16 - marketplace_optimization_app_docs_master_backup_ecommerce_canon_1_20251113.md (25 linhas) -->

# [app_docs\_MASTER_BACKUP\ecommerce-canon\GENESIS\RAW\RAW_006_StoryBrand_Marketplaces.md]

**Categoria**: marketplace_optimization
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

Lines: 62

# Arquivo: Referencias_StoryBrand_Marketplaces.md
# Versão: 1.1
# Data: 12/08/2025
# Escopo: Repositório de fontes (dos ficheiros carregados) com links e notas de uso

> Todas as fontes abaixo foram extraídas dos documentos que você subiu (“Base de Conhecimento StoryBrand…”, “Pesquisa StoryBrand – Donald Miller”). Organizei por tema e acrescentei “Como usar” para acelerar pesquisa e citação.

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: app_docs, canon, Core, ecommerce, Conceito, GENESIS, RAW_006_StoryBrand_Marketplaces, _MASTER_BACKUP

**Origem**: desconhecida


---


<!-- VERSÍCULO 16/16 - marketplace_optimization_app_docs_master_backup_ecommerce_canon_20251113.md (26 linhas) -->

# [app_docs\_MASTER_BACKUP\ecommerce-canon\GENESIS\RAW\RAW_005_Products_Marketplaces.md]

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

- Destacar prazos reais de envio e políticas de devolução de acordo com o Fulfillment.
- Garantir preenchimento completo da ficha técnica (GTIN, modelo, variações) para melhorar rankeamento.
- Monitorar reputação do vendedor (medalha, tempo de resposta) e refletir em metadados quando impactar estratégia.


---

### RAW_005_Products_Marketplaces.md

| Sku    | Descrição                                          |   Custo Final |   Simples | Mercado Livre   | nan                | nan                  | Shopee   | nan                | nan                  | B2W   | nan                | nan                  | Magalu   | nan                | nan                  | Olist   | nan                | nan                  | SHEIN   | nan                | nan                  | AMAZON DBA   | nan                | nan                  | Marketplace 10   | nan   | nan    |
|:-------|:---------------------------------------------------|--------------:|----------:|:----------------|:-------------------|

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Operação, app_docs, canon, Core, ecommerce, Conceito, RAW_005_Products_Marketplaces, GENESIS, _MASTER_BACKUP

**Origem**: desconhecida


---


<!-- FIM DO CAPÍTULO 25 -->
<!-- Total: 16 versículos, 1181 linhas -->
