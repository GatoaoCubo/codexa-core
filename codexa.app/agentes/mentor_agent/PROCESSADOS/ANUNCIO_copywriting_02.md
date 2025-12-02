# LIVRO: Copywriting
## CAPÍTULO 2

**Versículos consolidados**: 40
**Linhas totais**: 1179
**Gerado em**: 2025-11-13 18:45:48

---


<!-- VERSÍCULO 1/40 - copywriting_conceito_core_28_20251113.md (30 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.66/1.00
**Data**: 20251113

## Conteúdo

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

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 2/40 - copywriting_conceito_core_29_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.60/1.00
**Data**: 20251113

## Conteúdo

### Problema: Keywords incompletas

**Causa**: Falta de dados para o produto
**Solução**: Forneça descrição mais detalhada do produto

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 3/40 - copywriting_conceito_core_2_20251113.md (31 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

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
    capitulo = classif

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 4/40 - copywriting_conceito_core_30_20251113.md (25 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.68/1.00
**Data**: 20251113

## Conteúdo

### 3.4 FASE 4: VALIDAÇÃO (Quality Gates)

```
validator.py verifica:
  ✓ Completude: Tem title, content, keywords?
  ✓ Singularidade: Não é duplicado em outro VERSÍCULO?
  ✓ Relevância: Entropia > threshold mínimo?
  ✓ Coerência: Faz sentido no contexto do LIVRO/CAP?
  ✓ Formato: Markdown válido? Links corretos?
```

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 5/40 - copywriting_conceito_core_31_20251113.md (22 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.65/1.00
**Data**: 20251113

## Conteúdo

dumps(results, indent=2)
        )
        
        # Copy approved cards if quality is good
        if results['overall_score'] >= 0.8:
            import shutil
            shutil.copytree('05_cards', '07_validated/approved_knowledge')

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 6/40 - copywriting_conceito_core_32_20251113.md (19 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

### Chunk 4: Ad Structure Builder
- **Source**: All pillars + outputs from Chunks 1-3
- **Purpose**: Transform research into ad structure (headlines, bullets, FAQ)
- **Output**: Advertisement structure ready for copywriting

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 7/40 - copywriting_conceito_core_33_20251113.md (18 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

### 3) Fallbacks e etiquetas
- Ao inferir conteúdo, marque com **[SUGESTÃO]** e registre a suposição em `meta.assumptions`.
- Pergunte **apenas o mínimo necessário** quando o bloqueio for crítico (ex.: nome da marca inexistente).

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 8/40 - copywriting_conceito_core_34_20251113.md (18 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

### 4) Acessibilidade
- Ao sugerir cores, informe quais pares “texto/fundo” atendem **WCAG 2.2** (4,5:1 texto normal; 3:1 texto grande).  
- Gere **contrast_pairs** (ex.: `#111111` sobre `#FFFFFF` → **OK 21:1**).

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 9/40 - copywriting_conceito_core_35_20251113.md (33 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
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

    # 2. Token entropy (info

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 10/40 - copywriting_conceito_core_36_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Overview

A 5-Chunk Library é um sistema modular para compor prompts inteligentes que transformam dados de pesquisa em insumos para criação de conteúdo.

**Localização**: `.claude/commands/compose_prompts.md`
**Framework**: `app/como_pesquisa/02_prompt_composition/prompt_chunks_guide.md`

**Tags**: ecommerce, abstract

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 11/40 - copywriting_conceito_core_37_20251113.md (26 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.71/1.00
**Data**: 20251113

## Conteúdo

conceito, contextual, abstract, conhecimento, unidade, hierarquia, entropia, 
livro (6 domínios de e-commerce)
  ↓
capítulo (subtemas)
  ↓
versículo (unidade atômica de conhecimento)
  ├─ título + conceito
  ├─ entropia: 0-100 (densidade informacional)
  ├─ deus-vs-todo: abstract ↔ contextual
  └─ relações com outros versículos
, subtemas

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core, Keywords

**Origem**: desconhecida


---


<!-- VERSÍCULO 12/40 - copywriting_conceito_core_38_20251113.md (32 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

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

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 13/40 - copywriting_conceito_core_39_20251113.md (30 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.66/1.00
**Data**: 20251113

## Conteúdo

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

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 14/40 - copywriting_conceito_core_3_20251113.md (23 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### 1) Montar/atualizar `brand_guidelines` (Structured Output)
Validações (máx.): missão/visão ≤ 2 frases; valores 3–5; paleta 2–4 cores; tom 3–5 adjetivos.  
Se algo faltar, gere 2–3 opções com etiqueta **[SUGESTÃO]**.

**Campos-chave**  
- **brand_name**, **segment**, **positioning** (frame of reference, target, promise, RTBs).  
- **mission**, **vision**, **values**, **slogan** (opcional).  
- **tone_of_voice**: diferenças entre **voz** (estável) e **tom** (varia por contexto). Construa a mat

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 15/40 - copywriting_conceito_core_40_20251113.md (21 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.60/1.00
**Data**: 20251113

## Conteúdo

### Problema: Keywords incompletas

**Causa**: Falta de dados para o produto
**Solução**: Forneça descrição mais detalhada do produto

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 16/40 - copywriting_conceito_core_41_20251113.md (19 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

### Chunk 4: Ad Structure Builder
- **Source**: All pillars + outputs from Chunks 1-3
- **Purpose**: Transform research into ad structure (headlines, bullets, FAQ)
- **Output**: Advertisement structure ready for copywriting

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 17/40 - copywriting_conceito_core_42_20251113.md (33 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
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

    # 2. Token entropy (info

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 18/40 - copywriting_conceito_core_43_20251113.md (18 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

# Brand Assistant — MASTER PROMPT (v4)

> Objetivo: transformar qualquer insumo do usuário (texto/imagens) em um **Brandbook** claro e utilizável, com JSON `brand_guidelines` validado + um Markdown humano amigável.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 19/40 - copywriting_conceito_core_44_20251113.md (17 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### S3 — Sistema Visual, Acessibilidade & Governança
Objetivo: definir a identidade visual e garantir governança dos ativos.  Descreva o logotipo primário e variantes (símbolo, lock‑ups), regras de clear space e tamanhos mínimos; especifique usos incorretos.  Defina a paleta oficial (até 4 cores), indicando função de cada cor e pares de contraste; teste combinações “texto/fundo” e liste as que cumprem WCAG 2.2 (≥ 4,5:1 para texto normal).  Documente tipografia (display e texto, pesos, escalas e

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 20/40 - copywriting_conceito_core_45_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

### 2. PADDLEOCR Knowledge
- **Análise Técnica:** OCR, detecção de texto, processamento de imagem
- **Métricas:** Acurácia, velocidade, suporte a 80+ idiomas
- **Aplicações:** Documentos, cartazes, material impresso
- **Performance:** Otimizado para tempo real

**Tags**: ecommerce, general, implementation

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 21/40 - copywriting_conceito_core_46_20251113.md (32 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.66/1.00
**Data**: 20251113

## Conteúdo

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

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 22/40 - copywriting_conceito_core_47_20251113.md (19 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

### Tipografia
- **Poppins** (títulos/CTAs 600–800)  
- **Roboto** (corpo/UI 400–500)  
Boas práticas: desativar ligaturas; tracking +2 a +4 em títulos longos; LH 120–140%.

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 23/40 - copywriting_conceito_core_48_20251113.md (31 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

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
    capitulo = classif

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 24/40 - copywriting_conceito_core_4_20251113.md (33 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

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

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 25/40 - copywriting_conceito_core_5_20251113.md (34 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

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

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core, Keywords

**Origem**: desconhecida


---


<!-- VERSÍCULO 26/40 - copywriting_conceito_core_6_20251113.md (20 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

### Chunk 4: Ad Brief Generation
**Purpose**: Create advertising briefs

**Input**: Research consolidated data
**Output**: Ad copy variations, CTAs, value props

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 27/40 - copywriting_conceito_core_7_20251113.md (22 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.61/1.00
**Data**: 20251113

## Conteúdo

### Chunk 5: Copy Optimization
**Purpose**: Optimize ad copy for conversion

**Input**: Ad copy + research context
**Output**: Optimized variations by element

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---


<!-- VERSÍCULO 28/40 - copywriting_conceito_core_8_20251113.md (26 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.65/1.00
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

**Tags**: ecommerce, implementation

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 29/40 - copywriting_conceito_core_9_20251113.md (27 linhas) -->

# Conceito Core

**Categoria**: copywriting
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

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

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 30/40 - copywriting_conte_do_proibido_20251113.md (19 linhas) -->

# Conteúdo proibido

**Categoria**: copywriting
**Qualidade**: 0.65/1.00
**Data**: 20251113

## Conteúdo

- Promessas absolutas: "o melhor do mundo", "cura garantida", "nunca falha".
- Dados médicos ou terapêuticos sem comprovação regulatória.
- Uso de CAPS LOCK contínuo ou excesso de pontuação (!!!).
- Links externos que desviem a compra da plataforma.

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conteúdo, proibido

**Origem**: desconhecida


---


<!-- VERSÍCULO 31/40 - copywriting_descri_o_20251113.md (19 linhas) -->

# Descrição

**Categoria**: copywriting
**Qualidade**: 0.62/1.00
**Data**: 20251113

## Conteúdo

- Deve ser texto plano, sem HTML, emojis ou tabelas.
- Estruture em blocos curtos com cabeçalhos claros.
- Inclua políticas de devolução e garantia quando existirem.
- Não copie conteúdo de concorrentes; gere texto original.

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Descrição

**Origem**: desconhecida


---


<!-- VERSÍCULO 32/40 - copywriting_documentation_index_20251113.md (58 linhas) -->

# Documentation Index | copywriting

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
**Categoria**: copywriting
**Nível**: intermediário
**Tags**: python
**Aplicação**: quando_automatizar_processos
**Fonte**: RASCUNHO/DOCUMENTATION_INDEX.md
**Processado**: 20251113


---


<!-- VERSÍCULO 33/40 - copywriting_e_commerce_marketplace_20251113.md (33 linhas) -->

# E-Commerce & Marketplace

**Categoria**: copywriting
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

### Mercado Líder
**English:** "Market Leader" badge on Mercado Livre achieved when seller meets: 230+ sales in 60 days, R$37,000+ revenue, high reputation, low chargeback rate.

**Portuguese:** Badge "Mercado Líder" no Mercado Livre conquistado quando vendedor atinge: 230+ vendas em 60 dias, R$37.000+ em receita, boa reputação, taxa baixa de chargebacks.

**Significance:** Increases visibility, customer trust, and access to promotional tools.

**See:** KNOWLEDGE_BASE_GUIDE.md, section on E-Commerce Growth Strategy (30-Day Framework)

---

### E-COM QUEST (E-COM QUEST 0-30)
**English:** Framework for launching new e-commerce seller account to "Mercado Líder" status in 30 days through phase-based strategy: Setup → Traction → Scaling → Achievement.

**Portuguese:** Framework para lançamento de nova conta de vendedor e-commerce a status "Mercado Líder" em 30 dias através de estratégia em fases: Setup → Tração → Escalabilidade → Conquista.

**4-Phase Structure:**
- **Days 1-5:** Account cr

**Tags**: ecommerce, abstract

**Palavras-chave**: Commerce, Marketplace

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 34/40 - copywriting_fun_es_personalizadas_1_20251113.md (47 linhas) -->

# Funções Personalizadas

**Categoria**: copywriting
**Qualidade**: 0.69/1.00
**Data**: 20251113

## Conteúdo

retorna, json
{
  "name": "gerar_ean",
  "description": "retorna um ean-13 válido com base em categoria, marca e modelo.",
  "parameters": {
    "type": "object",
    "properties": {
      "categoria": {"type": "string", "description": "categoria do produto"},
      "marca": {"type": "string", "description": "marca do produto"},
      "modelo": {"type": "string", "description": "modelo/nome do produto"}
    },
    "required": ["categoria"]
  }
}
{
  "name": "pesquisa_seo",
  "description": "busca palavras-chave relevantes e dados de concorrentes.",
  "parameters": {
    "type": "object",
    "properties": {
      "produto": {"type": "string", "description": "nome/descrição do produto"},
      "categoria": {"type": "string", "description": "categoria do produto"},
      "marca": {"type": "string", "description": "marca do produto"}
    },
    "required": ["produto"]
  }
}
{
  "name": "valida_output",
  "description": "verifica limites de caracteres e formato final.",
  "parameters": {
 

**Tags**: concrete, ecommerce, general

**Palavras-chave**: Personalizadas, Keywords, Funções

**Origem**: desconhecida


---


<!-- VERSÍCULO 35/40 - copywriting_fun_es_personalizadas_20251113.md (47 linhas) -->

# Funções Personalizadas

**Categoria**: copywriting
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

```json
{
  "name": "gerar_ean",
  "description": "Retorna um EAN-13 válido com base em categoria, marca e modelo.",
  "parameters": {
    "type": "object",
    "properties": {
      "categoria": {"type": "string", "description": "Categoria do produto"},
      "marca": {"type": "string", "description": "Marca do produto"},
      "modelo": {"type": "string", "description": "Modelo/nome do produto"}
    },
    "required": ["categoria"]
  }
}
{
  "name": "pesquisa_seo",
  "description": "Busca palavras-chave relevantes e dados de concorrentes.",
  "parameters": {
    "type": "object",
    "properties": {
      "produto": {"type": "string", "description": "Nome/descrição do produto"},
      "categoria": {"type": "string", "description": "Categoria do produto"},
      "marca": {"type": "string", "description": "Marca do produto"}
    },
    "required": ["produto"]
  }
}
{
  "name": "valida_output",
  "description": "Verifica limites de caracteres e formato final.",
  "parameters": {
    "ty

**Tags**: ecommerce, concrete

**Palavras-chave**: Funções, Personalizadas

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 36/40 - copywriting_integra_es_1_20251113.md (61 linhas) -->

# 🔗 INTEGRAÇÕES

**Categoria**: copywriting
**Qualidade**: 0.69/1.00
**Data**: 20251113

## Conteúdo

### Com Claude/ChatGPT

```
1. Execute /research
2. Copie Chunk 1 (Research Consolidation)
3. Cole no Claude/ChatGPT
4. Substitua variáveis pelo seu contexto
5. Execute o prompt
```

### Com Sistema API

```bash
POST /api/research/start
{
  "product_name": "Notebook Gamer",
  "category": "Electronics",
  "research_type": "deep"
}

Response:
{
  "request_id": "req_xyz",
  "status": "processing"
}

# Após 2-5 minutos:
GET /api/research/req_xyz/report
→ Retorna JSON com todos os dados + chunks
```

### Com Automação (ADW)

```bash
# Trigger automático via GitHub issue
Title: Research Notebook Gamer
Body: Please analyze this product for marketing

# Sistema:
1. Detecta issue
2. Executa /research automaticamente
3. Comenta com resultado
4. Cria PR com dados estruturados
```

---

**Tags**: ecommerce, implementation

**Palavras-chave**: INTEGRAÇÕES

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 37/40 - copywriting_integra_es_20251113.md (61 linhas) -->

# 🔗 INTEGRAÇÕES

**Categoria**: copywriting
**Qualidade**: 0.69/1.00
**Data**: 20251113

## Conteúdo

### Com Claude/ChatGPT

```
1. Execute /research
2. Copie Chunk 1 (Research Consolidation)
3. Cole no Claude/ChatGPT
4. Substitua variáveis pelo seu contexto
5. Execute o prompt
```

### Com Sistema API

```bash
POST /api/research/start
{
  "product_name": "Notebook Gamer",
  "category": "Electronics",
  "research_type": "deep"
}

Response:
{
  "request_id": "req_xyz",
  "status": "processing"
}

# Após 2-5 minutos:
GET /api/research/req_xyz/report
→ Retorna JSON com todos os dados + chunks
```

### Com Automação (ADW)

```bash
# Trigger automático via GitHub issue
Title: Research Notebook Gamer
Body: Please analyze this product for marketing

# Sistema:
1. Detecta issue
2. Executa /research automaticamente
3. Comenta com resultado
4. Cria PR com dados estruturados
```

---

**Tags**: ecommerce, general, implementation

**Palavras-chave**: INTEGRAÇÕES

**Origem**: desconhecida


---


<!-- VERSÍCULO 38/40 - copywriting_keywords_10_20251113.md (25 linhas) -->

# Keywords

**Categoria**: copywriting
**Qualidade**: 0.64/1.00
**Data**: 20251113

## Conteúdo

workflow, research, prompts, execute, input, claude, 
1. execute: /research (deep mode)
   → gera completa research + json

2. execute: /compose_prompts
   input: research report request_id

3. copy: 5 chunks para claude/chatgpt

4. use: para copywriting em escala

**Tags**: ecommerce, intermediate

**Palavras-chave**: Keywords

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 39/40 - copywriting_keywords_11_20251113.md (44 linhas) -->

# Keywords

**Categoria**: copywriting
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

muito, semantic, domain, character, token,  log₂(p(x))

    alto (80-100) = muito específico, denso, novo
    médio (50-79) = bom para contexto, prático
    baixo (0-49) = informação óbvia, genérica
    """

    # 1. character entropy (probabilidade de caracteres)
    char_entropy = shannon_entropy(text)

    # 2. token entropy (informação por token)
    token_entropy = token_information_content(text)

    # 3. semantic novelty (quanto é novo para o corpus)
    semantic_entropy = semantic_novelty_score(text, canon_texts)

    # 4. domain specificity (quanto é específico de e-commerce)
    domain_entropy = domain_specificity(text, "ecommerce")

    # weighted average
    total = (char_entropy , commerce, shannon-entropy, baixo, weighted, python
def calculate_entropy(text, domain="ecommerce"):
    """
    mede quantidade de informação nova em relação ao corpus existente

    fórmula: h(x) = -∑ p(x) * log₂(p(x))

    alto (80-100) = muito específico, denso, novo
    médio (50-79) = bom pa

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Keywords

**Origem**: desconhecida


---


<!-- VERSÍCULO 40/40 - copywriting_keywords_12_20251113.md (44 linhas) -->

# Keywords

**Categoria**: copywriting
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

muito, semantic, domain, character, token,  log₂(p(x))

    alto (80-100) = muito específico, denso, novo
    médio (50-79) = bom para contexto, prático
    baixo (0-49) = informação óbvia, genérica
    """

    # 1. character entropy (probabilidade de caracteres)
    char_entropy = shannon_entropy(text)

    # 2. token entropy (informação por token)
    token_entropy = token_information_content(text)

    # 3. semantic novelty (quanto é novo para o corpus)
    semantic_entropy = semantic_novelty_score(text, canon_texts)

    # 4. domain specificity (quanto é específico de e-commerce)
    domain_entropy = domain_specificity(text, "ecommerce")

    # weighted average
    total = (char_entropy , commerce, shannon-entropy, baixo, weighted, python
def calculate_entropy(text, domain="ecommerce"):
    """
    mede quantidade de informação nova em relação ao corpus existente

    fórmula: h(x) = -∑ p(x) * log₂(p(x))

    alto (80-100) = muito específico, denso, novo
    médio (50-79) = bom pa

**Tags**: ecommerce, intermediate

**Palavras-chave**: Keywords

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- FIM DO CAPÍTULO 2 -->
<!-- Total: 40 versículos, 1179 linhas -->
