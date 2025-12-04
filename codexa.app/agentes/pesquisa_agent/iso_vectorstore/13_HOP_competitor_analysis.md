<!-- iso_vectorstore -->
<!--
  Source: competitor_analysis.md
  Agent: pesquisa_agent
  Synced: 2025-12-02
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# MÓDULO: ANÁLISE E BENCHMARK DE CONCORRENTES

## 📋 MODULE_METADATA (TAC-7 Header)

```yaml
id: competitor_analysis_v1
version: 1.0.0
purpose: "Deep dive into top 3-5 competitors with quantitative benchmarking"
category: competitive_intelligence
dependencies:
  - config/accessible_urls.md (relevant sections)
  - web_search capability (required for most modules)
execution_time: 6-8 min
isolation: module
portability: llm_agnostic
```

## 📥 INPUT_CONTRACT

**Required Inputs**:
- `$competitors` - Input parameter
- `$validated_brief` - Input parameter

**Optional Inputs**: (see original content below)

## 📤 OUTPUT_CONTRACT

**Primary Outputs**: `[ANÁLISE DE CONCORRENTES]`, `[BENCHMARK DE CONCORRENTES]`, `[DIFERENCIAIS COMPETITIVOS]`

**Export Variables**:
```yaml
competitor_list: "Detailed competitor profiles"
benchmark_data: "Aggregated metrics (price, rating, review count)"
```

## 🎯 TASK

**Role**: Competitive Intelligence Analyst
**Objective**: Deep dive into top 3-5 competitors with quantitative benchmarking
**Standards**: (see original content below)
**Constraints**: Max execution time: 6-8 min, All queries logged

## ✅ VALIDATION (Quality Gates)

(See original content for specific validation criteria)

## 🔗 CONTEXT (Usage & Integration)

**Upstream Dependencies**: Previous steps in execution plan
**Downstream Consumers**: Subsequent steps + output blocks
**Data Flow**: (see original content)

---



## Objetivo
Consolidar análise estruturada de concorrentes identificados durante web searches inbound/outbound, com métricas quantitativas e qualitativas.

## Entradas
- Concorrentes identificados durante web search inbound (marketplaces)
- Concorrentes mencionados em reviews e SERP (web search outbound)
- Concorrentes declarados no brief
- Histórico de benchmarks similares (file search)

## Definição de Concorrente Relevante

Incluir se:
- Produto/marca aparece em top 10 de marketplace para head term prioritário
- Mencionado em ≥3 reviews ou comparativos
- Declarado no brief
- Volume significativo de avaliações (>50 para marketplaces grandes)
- Posicionamento similar (categoria, preço, público)

Excluir se:
- Produto descontinuado ou indisponível
- Marca sem presença digital verificável
- Produto de categoria muito distante
- Outliers extremos de preço (>5x ou <20% da média)

## Estrutura de Análise por Concorrente

### Bloco [ANÁLISE DE CONCORRENTES]

Para cada concorrente, coletar:

```
nome: [marca + modelo ou descrição curta]

forças:
- [força 1: claim, diferencial, prova específica]
- [força 2]
- [força 3]
máximo 5 forças

fraquezas:
- [fraqueza 1: gap, objeção recorrente, limitação]
- [fraqueza 2]
- [fraqueza 3]
máximo 5 fraquezas

preço médio ou faixa:
[valor BRL ou range] ou [SUGESTÃO]
contexto: [marketplace onde foi observado]

principais claims:
- [claim 1 + se é verificável]
- [claim 2 + se é verificável]
máximo 5 claims

provas e avaliações:
rating: [X.X de 5]
volume avaliações: [número ou range]
comentários típicos: [síntese de feedback recorrente]

políticas e alertas:
- [política de destaque: garantia, devolução, frete]
- [alertas: reclamações, riscos, compliance]

oportunidades:
- [oportunidade 1: gap explorável, weakness endereçável]
- [oportunidade 2]
máximo 3 oportunidades

novelty:
[score 1-5]
justificativa: [breve explicação do score]
```

### Critérios de Novelty Score

- **1 - Commodity**: produto genérico sem diferenciação aparente
  - Ex: cabo USB básico sem marca

- **2 - Padronizado com variação leve**: produto comum com pequena variação estética ou de marca
  - Ex: mouse sem fio padrão de marca conhecida

- **3 - Diferenciação moderada**: produto com feature, design ou benefício distintivo
  - Ex: fone com cancelamento de ruído ativo (quando não é padrão da categoria)

- **4 - Inovação relevante**: produto com inovação significativa no segmento
  - Ex: fone com tradução simultânea integrada

- **5 - Disruptivo ou pioneiro**: produto que cria nova categoria ou muda paradigma
  - Ex: primeiro dispositivo wearable de determinado tipo no mercado BR

## Benchmark Consolidado

### Bloco [BENCHMARK DE CONCORRENTES]

Após analisar todos concorrentes, consolidar métricas agregadas:

```
número de concorrentes analisados: [N]

faixa de preço por marketplace:
- [marketplace 1]: [min-max BRL] | modal: [range mais frequente]
- [marketplace 2]: [min-max BRL] | modal: [range mais frequente]

rating médio do segmento:
- média geral: [X.X de 5]
- range: [min-max]
- referência de excelência: [≥X.X para ser competitivo]

volume de avaliações típico:
- low: [<N avaliações]
- medium: [N-M avaliações]
- high: [>M avaliações]
- insight: [volume mínimo para credibilidade]

padrão visual predominante:
- [fundo branco | lifestyle | técnico]: [% de concorrentes]
- número de imagens: [range típico]
- presença de vídeo: [% de concorrentes]
- insight: [padrão vencedor ou oportunidade de diferenciação]

claims mais frequentes:
1. [claim A]: presente em [X%] dos concorrentes | verificável: [sim/não]
2. [claim B]: presente em [Y%] dos concorrentes | verificável: [sim/não]
3. [claim C]: presente em [Z%] dos concorrentes | verificável: [sim/não]
máximo 10 claims

provas mais utilizadas:
- [tipo de prova 1]: [% de uso] | efetividade: [alta/média/baixa]
- [tipo de prova 2]: [% de uso] | efetividade: [alta/média/baixa]
ex: certificação Anatel, garantia estendida, rating >4.5, número de vendas

políticas recorrentes:
- frete: [padrão observado - grátis, prazo típico]
- devolução: [padrão - dias, condições]
- garantia: [padrão - prazo, tipo]
- parcelamento: [padrão - número de vezes]

selos e certificações frequentes:
- [selo/certificação 1]: [% de presença]
- [selo/certificação 2]: [% de presença]

share aparente de prateleira:
- [concorrente líder]: [estimativa de presença relativa]
- [concorrente 2]: [estimativa]
insight: [dominância ou fragmentação do segmento]

estratégias de diferenciação observadas:
1. [estratégia A e quem usa]
2. [estratégia B e quem usa]
3. [estratégia C e quem usa]

novelty médio do segmento: [score médio 1-5]
insight: [segmento commoditizado ou com inovação]
```

## Análise Comparativa

### Matriz de Forças vs Fraquezas

Identificar padrões:
- **Forças comuns**: compartilhadas por ≥50% dos concorrentes → tabela stakes do segmento
- **Forças raras**: compartilhadas por <20% → possíveis diferenciais
- **Fraquezas comuns**: gaps do segmento → oportunidades
- **Fraquezas específicas**: de líder ou player relevante → abertura para ataque

### Análise de Preço-Valor

Mapear posicionamento:
- **Premium** (top 20% de preço): forças que justificam, público-alvo
- **Mid-tier** (20-80% de preço): balanceamento, maior volume
- **Econômico** (bottom 20%): trade-offs, objeções típicas

### Análise de Prova Social

Correlações:
- Rating vs volume de avaliações
- Rating vs preço
- Volume de perguntas vs conversão (quando observável)
- Presença de vídeo vs engajamento

## Exemplo Completo

**Categoria**: Fone Bluetooth
**Concorrentes analisados**: 5

### [ANÁLISE DE CONCORRENTES]

```
nome: JBL Tune 510BT

forças:
- Marca consolidada com reconhecimento alto
- Bateria 40h (acima da média)
- Certificação Anatel visível
- Rating 4.6 com 3200 avaliações no ML
- Preço competitivo para marca premium

fraquezas:
- Não possui cancelamento de ruído ativo
- Design básico sem inovação
- Reclamações sobre conforto para uso prolongado (>2h)
- Embalagem simples (percepção de valor menor)

preço médio: 180-220 BRL
contexto: Mercado Livre e Amazon BR

principais claims:
- Original JBL com garantia (verificável via selo)
- 40h de bateria (especificação técnica)
- Som Pure Bass (claim de marca, subjetivo)
- Conexão Bluetooth 5.0 (verificável)

provas e avaliações:
rating: 4.6 de 5
volume avaliações: 3200 no ML
comentários típicos: elogios a bateria e som; críticas a conforto e falta de case

políticas e alertas:
- Garantia 12 meses via fabricante
- Frete grátis em 80% dos anúncios
- Sem reclamações significativas no Reclame Aqui sobre produto

oportunidades:
- Adicionar case ou acessórios para melhorar valor percebido
- Destacar conforto melhorado se aplicável
- Explorar gap de cancelamento de ruído ativo

novelty: 2
justificativa: produto estabelecido sem features inovadoras mas marca forte
```

```
nome: Edifier W800BT

forças:
- Melhor custo-benefício (rating alto, preço baixo)
- Design mais moderno que concorrentes da faixa
- Almofadas macias (comentários recorrentes)
- 50h de bateria (líder do segmento)
- Cabo auxiliar incluso (uso com e sem bateria)

fraquezas:
- Marca menos conhecida no Brasil
- Sem certificação Anatel aparente em alguns anúncios
- Volume de avaliações menor (850)
- Disponibilidade limitada (menos vendedores)

preço médio: 150-180 BRL
contexto: Mercado Livre e Shopee

principais claims:
- 50h de bateria (verificável)
- Conforto superior (baseado em reviews)
- Som Hi-Fi (claim subjetivo)
- Dobrável e leve (verificável)

provas e avaliações:
rating: 4.7 de 5
volume avaliações: 850 no ML
comentários típicos: surpresa positiva com qualidade; dúvidas sobre originalidade

políticas e alertas:
- Garantia varia (6-12 meses conforme vendedor)
- Alerta: alguns vendedores sem certificação clara

oportunidades:
- Fortalecer prova de originalidade (selo, vendedor oficial)
- Ampliar disponibilidade (mais vendedores)
- Marketing de marca para reconhecimento

novelty: 2
justificativa: produto bom mas sem inovação; diferencial está em custo-benefício
```

[... mais 3 concorrentes]

### [BENCHMARK DE CONCORRENTES]

```
número de concorrentes analisados: 5

faixa de preço por marketplace:
- Mercado Livre: 80-350 BRL | modal: 150-200 BRL
- Shopee: 60-300 BRL | modal: 100-180 BRL
- Amazon BR: 100-400 BRL | modal: 180-250 BRL

rating médio do segmento: 4.5 de 5
range: 4.2-4.8
referência de excelência: ≥4.5 para competir em top 10

volume de avaliações típico:
- low: <500 avaliações (novos no mercado)
- medium: 500-2000 avaliações (estabelecidos)
- high: >2000 avaliações (líderes)
insight: mínimo 200 avaliações para credibilidade inicial

padrão visual predominante:
- fundo branco: 80% dos concorrentes
- lifestyle: 40% (como imagem secundária)
- close técnico: 60%
- número de imagens: 6-10 típico
- presença de vídeo: 30%
insight: fundo branco é padrão; vídeo ainda é diferencial

claims mais frequentes:
1. Bateria longa duração (30-50h): 100% | verificável: sim
2. Original com garantia: 90% | verificável: depende do vendedor
3. Bluetooth 5.0+: 80% | verificável: sim
4. Som de qualidade (bass, hi-fi): 70% | verificável: não (subjetivo)
5. Conforto: 60% | verificável: parcial (via reviews)
6. Certificação Anatel: 50% visível | verificável: sim (crítico)

provas mais utilizadas:
- Rating >4.5: 80% | efetividade: alta (crítico para conversão)
- Volume avaliações >500: 60% | efetividade: alta
- Selo vendedor oficial: 40% | efetividade: alta
- Vídeo de demonstração: 30% | efetividade: média-alta

políticas recorrentes:
- frete: grátis em 70% (ML), 90% (Shopee), prazo 5-12 dias
- devolução: 7 dias padrão, 30 dias em 20% dos casos
- garantia: 12 meses (fabricante ou vendedor)
- parcelamento: 6-12x sem juros

share aparente de prateleira:
- JBL: dominante (~30% dos resultados top 10)
- Sony: forte (~20%)
- Philips: moderado (~15%)
- Edifier, QCY: emergentes (~10% cada)
insight: segmento concentrado em marcas estabelecidas, mas com espaço para custo-benefício

estratégias de diferenciação observadas:
1. Marca premium + preço acessível (JBL, Sony)
2. Custo-benefício com features superiores (Edifier, QCY)
3. Design diferenciado + cores (Philips)

novelty médio do segmento: 2.2 de 5
insight: segmento maduro e commoditizado; diferenciação vem de marca, preço e pequenas features
```

## Output: Integração com Estratégias

Usar benchmark para alimentar:

### [ESTRATÉGIAS E GAPS]
```
estratégia vencedora: marcas consolidadas dominam com preço competitivo e prova social alta
gap explorável: certificação Anatel não é destacada por todos (oportunidade de compliance como diferencial)
risco frequente: claims de qualidade de som sem prova objetiva
oportunidade KW: termos de conforto e uso prolongado são pouco explorados
```

### [DIFERENCIAIS COMPETITIVOS]
```
diferencial real: [se o produto tem feature ausente em >70% dos concorrentes]
diferencial de prova: [se tem certificação/selo que <50% exibem]
diferencial de experiência: [se políticas são superiores - devolução 30d vs 7d]
```

## Quando Usar [SUGESTÃO]

Usar [SUGESTÃO] para:
- Preço não encontrado após pesquisas (produto descontinuado, regional)
- Dados de volume não públicos (estimativas)
- Certificações não verificáveis online

Sempre registrar em [NOTAS DE FALLBACK].

## Checklist de Execução

- [ ] Mínimo 3 concorrentes analisados (ideal 5-8)
- [ ] Cada concorrente com ≥4 blocos preenchidos (forças, fraquezas, preço, provas)
- [ ] Novelty score justificado
- [ ] Benchmark consolidado com métricas agregadas
- [ ] Claims frequentes quantificados (%)
- [ ] Padrões visuais mapeados
- [ ] Oportunidades de diferenciação identificadas

---

**Execução**: Após web searches inbound e outbound
**Integração**: Alimenta [ESTRATÉGIAS E GAPS], [DIFERENCIAIS COMPETITIVOS], [PADRÕES DE LINGUAGEM]
**Output**: [ANÁLISE DE CONCORRENTES], [BENCHMARK DE CONCORRENTES]



## 🔍 Enriquecimento: Pesquisa & SEO

### Técnicas e Algoritmos
**Algoritmos/Métodos:** PACIF).md](#engenheiro-de-prompt-(método-pacif)-md)

### Táticas e Metodologias
**Processo/Metodologia:**
- [RESUMO_EXECUTIVO_SESSION_20251027.md](#resumo_executivo_session_20251027-md)
- [SUMARIO_FINAL_SESSAO.md](#sumario_final_sessao-md)
- [test_serving.md](#test_serving-md)
- [CARD_001.human.md](#card_001-human-md)
- [etica_comercial.yml.human.md](#etica_comercial-yml-human-md)
- [Engenheiro de Prompt (Método PACIF).md](#engenheiro-de-prompt-(método-pacif)-md)
- [Market Idea Expander.md](#market-idea-expander-md)

### Estratégias de Mercado
*Nenhuma estratégia específica encontrada*

### Meta-Instruções
*Nenhuma meta-instrução específica encontrada*

---
*Enriquecido em: 2025-11-03T16:21:52.272331*
*Fonte: PaddleOCR Organized Knowledge Base*

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

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Consolidados, Artefatos

**Origem**: desconhecida


---

### Pesquisa de Mercado em Marketplaces
*Relevância: 0.92 | Tags: pesquisa, mercado, marketplace*

# 2. Análise Competitiva

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Top 5 Concorrentes

#### Concorrente 1: ASUS Vivobook

- URL: [mercadolivre.com.br/...]
- Preço: R$ 4.500
- Rating: 4.7/5 (980 reviews)
- Mensagem: "Melhor custo-benefício em performance"
- Diferenciais: Preço competitivo, bateria boa
- Principais reclamações: Superaquecimento (45x), bateria (30x)

#### Concorrente 2: Samsung Galaxy Book

- Preço: R$ 5.200
- Rating: 4.8/5 (1.200 reviews)
- Mensagem: "Design fino + Performance"
- Principais reclamações: Preço alto (60x), porta USB limitada (25x)

### Gaps Identificados

```
GAP 1: Suporte técnico em português
Ninguém fala sobre suporte após venda
Seu diferencial: Suporte 24/7 em PT-BR
Aplicação: Headline "Suporte Técnico em Português 24/7"

GAP 2: Ventilação otimizada
Reclamação comum: "Aquece muito"
Seu diferencial: Ventilação otimizada, zero super aquecimento
Aplicação: Bullet "❄️ Zero superaquecimento mesmo 8h ligado"
```

**Tags**: architectural, general

**Palavras-chave**: Análise, Competitiva

**Origem**: unknown


---

### Identificação de Gaps Competitivos
*Relevância: 0.88 | Tags: gaps, oportunidades, diferenciacao*

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Componentes Principais

| Componente | Localização | Função |
|-----------|-----------|---------|
| **Orchestrator** | `.claude/commands/research.md` | Coordena todo pipeline |
| **Pillar Agents** | `.claude/commands/{analyze_market,analyze_competitors,extract_keywords}.md` | Executa pesquisas temáticas |
| **Chunk Composer** | `.claude/commands/compose_prompts.md` | Transforma dados em prompts |
| **Python Server** | `app/server/research_agent_*.py` | Backend REST API |
| **Knowledge Base**

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---

---

**Metadados da Injeção:**
- **Versículos injetados**: 3
- **Fonte**: mentor_agent/PROCESSADOS/
- **Última atualização**: 2025-11-14 07:44:46
- **Versão do schema**: 1.0.0

**Referências**: `CAPITULO_analise_01:versiculo_7, CAPITULO_marketplace_01:versiculo_22, CAPITULO_analise_02:versiculo_12`

## Conteúdo

### Workflow 2: Análise Competitiva (10-15 min)

```
1. Execute: /analyze_competitors
   Input: Product + Competitor URLs

2. Review: Gaps and positioning (Pilar 2)

3. Use: Chunk 3 para diferenciação

4. Output: Strategic positioning insights
```

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---

### Conceito Core
*Relevância: 0.57 | Tags: ecommerce, general, intermediate*

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Research System (Origem)
- **6 Pilares**: Market, Competitors, Product, Keywords, Trends, FAQ
- **5-Chunk Library**: Consolidation, Keywords, Gaps, Ad Structure, Validation
- **7 Agentes**: Orchestrator, Market, Competitor, Keyword, FAQ, Validator, Meta
- **5 CLI Commands**: /research, /analyze_market, /analyze_competitors, /extract_keywords, /compose_prompts
- **6 Python Modules**: models, config, orchestrator, agents, routes, meta
- **Knowledge Base**: 8 JSON files com semantic maps, inven

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---

### Conceito Core
*Relevância: 0.57 | Tags: ecommerce, general, intermediate*

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### 3. CompetitorAnalystAgent
**Role**: Competitive intelligence expert
**Keywords**: competitor|analysis|positioning|messaging|gap
**File**: `research_agents.py:CompetitorAnalystAgent`

Responsibilities:
- Analyze competitor products
- Extract strengths/weaknesses
- Identify market gaps
- Extract messaging themes
- Find differentiation opportunities

**Returns**: `CompetitiveAnalysisResult`

**Interface**:
```python
agent = CompetitorAnalystAgent()
result = await agent.execute(request, report)

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---

### Keywords
*Relevância: 0.67 | Tags: ecommerce, general, intermediate*

# Keywords

**Categoria**: analise_concorrencia
**Qualidade**: 0.65/1.00
**Data**: 20251113

## Conteúdo

output, strategic, workflow, product, competitor, execute, chunk, pilar, 
1. execute: /analyze_competitors
   input: product + competitor urls

2. review: gaps and positioning (pilar 2)

3. use: chunk 3 para diferenciação

4. output: strategic positioning insights
, input, review, competitiva

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Keywords

**Origem**: desconhecida


---

### 📚 Knowledge Base (Dados)
*Relevância: 0.58 | Tags: ecommerce, general, intermediate*

# 📚 Knowledge Base (Dados)

**Categoria**: analise_concorrencia
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

### Localização: `RAW_LEM_v1.1/` + `knowledge_artifacts_v1/`

#### Arquivos Principais

| Arquivo | Tipo | Função |
|---------|------|---------|
| `knowledge_base_consolidated.json` | JSON | KB consolidada com 1000+ entries |
| `genesis_knowledge_cards.json` | JSON | Cartões de conhecimento Genesis |
| `knowledge_cards_paddleocr.json` | JSON | Cartões enriquecidos |
| `semantic_paddleocr.json` | JSON | Estruturas semânticas |
| `semantic_map.json` | JSON | Mapa semântico de conceitos |
| `catalog_index.json` | JSON | Índice de catálogo |
| `inventory.json` | JSON | Inventário de artefatos |

#### Estrutura JSON Padrão

```json
{
  "metadata": {
    "research_date": "YYYY-MM-DD",
    "product_name": "...",
    "research_type": "competitive|market|product|trend|faq"
  },
  "findings": {
    "primary_insights": [],
    "secondary_insights": [],
    "gaps": []
  },
  "structured_data": {
    "keywords": [],
    "competitors": [],
    "trends": [],
    "faq": []
  }
}
```

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Keywords, Core, Base, Knowledge, Conceito, Dados

**Origem**: desconhecida


---

### 📈 Métricas & Estatísticas
*Relevância: 0.58 | Tags: ecommerce, abstract*

# 📈 Métricas & Estatísticas

**Categoria**: analise_concorrencia
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

### Cobertura

- **Total Ficheiros**: 41 markdown docs + 6 Python modules + 8 JSON configs
- **Total Linhas**: 3,550+ lines código + 2,700+ lines documentação
- **CLI Commands**: 5 (research, analyze_market, analyze_competitors, extract_keywords, compose_prompts)
- **Python Modules**: 6 (models, config, orchestrator, agents, routes, meta)
- **Framework Files**: 20+

### Capacidades

- **Agentes**: 7 (orchestrator, market, competitor, keyword, faq, validator, meta)
- **Pilares**: 6 (market, competitors, product, keywords, trends, faq)
- **Chunks**: 5 (consolidation, keywords, gaps, structure, validation)
- **Steps**: 40+ (cada um com 0-level prompt)
- **Variáveis**: 25+ ($product_name, $category, etc)

### Performance

- **Pesquisa Rápida**: 5-10 minutos
- **Pesquisa Profunda**: 20-30 minutos
- **Keywords Only**: 2-5 minutos
- **Concurrent Jobs**: Até 15+ simultâneos
- **Quality Score**: 75-95%

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Métricas, Estatísticas

**Origem**: _CONSOLIDATED_ecommerce_other.md


---

### 🚀 Quick Start Workflows
*Relevância: 0.68 | Tags: ecommerce, general, intermediate*

# 🚀 Quick Start Workflows

**Categoria**: analise_concorrencia
**Qualidade**: 0.77/1.00
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

4. 

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Workflows, Start, Quick

**Origem**: desconhecida


---

*... (conteúdo truncado por limite de 1500 tokens)*
---

**Metadados da Injeção:**
- **Versículos injetados**: 194
- **Fonte**: mentor_agent/PROCESSADOS/
- **Última atualização**: 2025-11-14 07:44:46
- **Versão do schema**: 1.0.0

**Referências**: `CAPITULO_analise_03:versiculo_1, CAPITULO_analise_03:versiculo_5, CAPITULO_analise_03:versiculo_6, CAPITULO_analise_04:versiculo_37, CAPITULO_analise_04:versiculo_47, CAPITULO_analise_04:versiculo_50, CAPITULO_analise_05:versiculo_18, CAPITULO_analise_05:versiculo_21, CAPITULO_analise_05:versiculo_16, CAPITULO_analise_06:versiculo_3, CAPITULO_analise_06:versiculo_4, CAPITULO_analise_06:versiculo_2, CAPITULO_estrategia_01:versiculo_4, CAPITULO_general_01:versiculo_7, CAPITULO_marketplace_03:versiculo_1, CAPITULO_marketplace_03:versiculo_12, CAPITULO_marketplace_03:versiculo_5, CAPITULO_marketplace_04:versiculo_5, CAPITULO_marketplace_04:versiculo_17, CAPITULO_marketplace_04:versiculo_9, CAPITULO_marketplace_05:versiculo_10, CAPITULO_marketplace_05:versiculo_13, CAPITULO_marketplace_05:versiculo_11, CAPITULO_marketplace_06:versiculo_8, CAPITULO_marketplace_06:versiculo_14, CAPITULO_marketplace_06:versiculo_22, CAPITULO_marketplace_07:versiculo_15, CAPITULO_marketplace_07:versiculo_8, CAPITULO_marketplace_07:versiculo_19, CAPITULO_marketplace_08:versiculo_7, CAPITULO_marketplace_08:versiculo_2, CAPITULO_marketplace_08:versiculo_6, CAPITULO_marketplace_09:versiculo_5, CAPITULO_marketplace_09:versiculo_4, CAPITULO_marketplace_09:versiculo_10, CAPITULO_marketplace_10:versiculo_16, CAPITULO_marketplace_10:versiculo_4, CAPITULO_marketplace_10:versiculo_11, CAPITULO_marketplace_11:versiculo_21, CAPITULO_marketplace_11:versiculo_6, CAPITULO_marketplace_11:versiculo_7, CAPITULO_marketplace_12:versiculo_1, CAPITULO_marketplace_12:versiculo_6, CAPITULO_marketplace_12:versiculo_7, CAPITULO_marketplace_13:versiculo_23, CAPITULO_marketplace_13:versiculo_21, CAPITULO_marketplace_13:versiculo_20, CAPITULO_marketplace_14:versiculo_16, CAPITULO_marketplace_14:versiculo_5, CAPITULO_marketplace_14:versiculo_8, CAPITULO_marketplace_15:versiculo_16, CAPITULO_marketplace_15:versiculo_4, CAPITULO_marketplace_15:versiculo_10, CAPITULO_marketplace_16:versiculo_23, CAPITULO_marketplace_16:versiculo_2, CAPITULO_marketplace_16:versiculo_1, CAPITULO_marketplace_17:versiculo_3, CAPITULO_marketplace_17:versiculo_14, CAPITULO_marketplace_17:versiculo_2, CAPITULO_marketplace_18:versiculo_4, CAPITULO_marketplace_18:versiculo_11, CAPITULO_marketplace_18:versiculo_1, CAPITULO_marketplace_19:versiculo_12, CAPITULO_marketplace_19:versiculo_16, CAPITULO_marketplace_19:versiculo_10, CAPITULO_marketplace_20:versiculo_8, CAPITULO_marketplace_20:versiculo_6, CAPITULO_marketplace_20:versiculo_9, CAPITULO_marketplace_21:versiculo_14, CAPITULO_marketplace_21:versiculo_18, CAPITULO_marketplace_21:versiculo_8, CAPITULO_marketplace_22:versiculo_16, CAPITULO_marketplace_22:versiculo_1, CAPITULO_marketplace_22:versiculo_14, CAPITULO_marketplace_23:versiculo_15, CAPITULO_marketplace_23:versiculo_19, CAPITULO_marketplace_23:versiculo_22, CAPITULO_marketplace_24:versiculo_5, CAPITULO_marketplace_24:versiculo_13, CAPITULO_marketplace_24:versiculo_17, CAPITULO_marketplace_25:versiculo_10, CAPITULO_marketplace_25:versiculo_2, CAPITULO_marketplace_25:versiculo_3, CAPITULO_marketplace_26:versiculo_4, CAPITULO_marketplace_26:versiculo_5, CAPITULO_marketplace_26:versiculo_6, CAPITULO_marketplace_27:versiculo_15, CAPITULO_marketplace_27:versiculo_13, CAPITULO_marketplace_27:versiculo_12, CAPITULO_marketplace_28:versiculo_1, CAPITULO_marketplace_28:versiculo_5, CAPITULO_marketplace_28:versiculo_8, CAPITULO_marketplace_29:versiculo_6, CAPITULO_marketplace_29:versiculo_7, CAPITULO_marketplace_29:versiculo_1, CAPITULO_marketplace_30:versiculo_34, CAPITULO_marketplace_30:versiculo_9, CAPITULO_marketplace_30:versiculo_13, CAPITULO_marketplace_31:versiculo_22, CAPITULO_marketplace_31:versiculo_38, CAPITULO_marketplace_31:versiculo_37, CAPITULO_marketplace_32:versiculo_6, CAPITULO_marketplace_32:versiculo_10, CAPITULO_marketplace_32:versiculo_13, CAPITULO_marketplace_33:versiculo_8, CAPITULO_marketplace_33:versiculo_12, CAPITULO_marketplace_33:versiculo_1, CAPITULO_marketplace_34:versiculo_17, CAPITULO_marketplace_34:versiculo_2, CAPITULO_marketplace_34:versiculo_8, CAPITULO_marketplace_35:versiculo_4, CAPITULO_marketplace_35:versiculo_6, CAPITULO_marketplace_35:versiculo_9, CAPITULO_marketplace_36:versiculo_7, CAPITULO_marketplace_36:versiculo_11, CAPITULO_marketplace_36:versiculo_13, CAPITULO_marketplace_37:versiculo_23, CAPITULO_marketplace_37:versiculo_24, CAPITULO_marketplace_37:versiculo_15, CAPITULO_marketplace_38:versiculo_4, CAPITULO_marketplace_38:versiculo_1, CAPITULO_marketplace_38:versiculo_2, CAPITULO_marketplace_39:versiculo_13, CAPITULO_marketplace_39:versiculo_14, CAPITULO_marketplace_39:versiculo_18, CAPITULO_marketplace_40:versiculo_1, CAPITULO_marketplace_40:versiculo_3, CAPITULO_marketplace_40:versiculo_4, CAPITULO_marketplace_41:versiculo_7, CAPITULO_marketplace_41:versiculo_3, CAPITULO_marketplace_41:versiculo_4, CAPITULO_marketplace_42:versiculo_27, CAPITULO_marketplace_42:versiculo_8, CAPITULO_marketplace_42:versiculo_2, CAPITULO_marketplace_43:versiculo_2, CAPITULO_marketplace_43:versiculo_23, CAPITULO_marketplace_43:versiculo_18, CAPITULO_marketplace_44:versiculo_8, CAPITULO_marketplace_44:versiculo_9, CAPITULO_marketplace_44:versiculo_11, CAPITULO_marketplace_45:versiculo_2, CAPITULO_marketplace_45:versiculo_3, CAPITULO_marketplace_45:versiculo_4, CAPITULO_marketplace_46:versiculo_13, CAPITULO_marketplace_46:versiculo_2, CAPITULO_marketplace_46:versiculo_11, CAPITULO_marketplace_47:versiculo_1, CAPITULO_marketplace_47:versiculo_10, CAPITULO_marketplace_47:versiculo_13, CAPITULO_marketplace_48:versiculo_10, CAPITULO_marketplace_48:versiculo_12, CAPITULO_marketplace_48:versiculo_4, CAPITULO_marketplace_49:versiculo_2, CAPITULO_marketplace_49:versiculo_5, CAPITULO_marketplace_49:versiculo_6, CAPITULO_marketplace_50:versiculo_2, CAPITULO_marketplace_50:versiculo_6, CAPITULO_marketplace_50:versiculo_1, CAPITULO_marketplace_51:versiculo_16, CAPITULO_marketplace_51:versiculo_8, CAPITULO_marketplace_51:versiculo_3, CAPITULO_marketplace_52:versiculo_2, CAPITULO_marketplace_52:versiculo_10, CAPITULO_marketplace_52:versiculo_12, CAPITULO_marketplace_53:versiculo_13, CAPITULO_marketplace_53:versiculo_2, CAPITULO_marketplace_53:versiculo_8, CAPITULO_marketplace_54:versiculo_13, CAPITULO_marketplace_54:versiculo_14, CAPITULO_marketplace_54:versiculo_15, CAPITULO_marketplace_55:versiculo_9, CAPITULO_marketplace_55:versiculo_13, CAPITULO_marketplace_55:versiculo_3, CAPITULO_marketplace_56:versiculo_5, CAPITULO_marketplace_56:versiculo_8, CAPITULO_marketplace_56:versiculo_16, CAPITULO_marketplace_57:versiculo_2, CAPITULO_marketplace_57:versiculo_20, CAPITULO_marketplace_57:versiculo_3, CAPITULO_marketplace_58:versiculo_2, CAPITULO_marketplace_58:versiculo_1, CAPITULO_marketplace_58:versiculo_3, CAPITULO_marketplace_59:versiculo_9, CAPITULO_marketplace_59:versiculo_1, CAPITULO_marketplace_59:versiculo_2, CAPITULO_marketplace_60:versiculo_15, CAPITULO_marketplace_60:versiculo_12, CAPITULO_marketplace_60:versiculo_1, CAPITULO_marketplace_61:versiculo_11, CAPITULO_marketplace_61:versiculo_2, CAPITULO_marketplace_61:versiculo_7, CAPITULO_marketplace_62:versiculo_7, CAPITULO_marketplace_62:versiculo_1, CAPITULO_marketplace_62:versiculo_2`

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

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Consolidados, Artefatos

**Origem**: desconhecida


---

### Pesquisa de Mercado em Marketplaces
*Relevância: 0.92 | Tags: pesquisa, mercado, marketplace*

# 2. Análise Competitiva

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Top 5 Concorrentes

#### Concorrente 1: ASUS Vivobook

- URL: [mercadolivre.com.br/...]
- Preço: R$ 4.500
- Rating: 4.7/5 (980 reviews)
- Mensagem: "Melhor custo-benefício em performance"
- Diferenciais: Preço competitivo, bateria boa
- Principais reclamações: Superaquecimento (45x), bateria (30x)

#### Concorrente 2: Samsung Galaxy Book

- Preço: R$ 5.200
- Rating: 4.8/5 (1.200 reviews)
- Mensagem: "Design fino + Performance"
- Principais reclamações: Preço alto (60x), porta USB limitada (25x)

### Gaps Identificados

```
GAP 1: Suporte técnico em português
Ninguém fala sobre suporte após venda
Seu diferencial: Suporte 24/7 em PT-BR
Aplicação: Headline "Suporte Técnico em Português 24/7"

GAP 2: Ventilação otimizada
Reclamação comum: "Aquece muito"
Seu diferencial: Ventilação otimizada, zero super aquecimento
Aplicação: Bullet "❄️ Zero superaquecimento mesmo 8h ligado"
```

**Tags**: architectural, general

**Palavras-chave**: Análise, Competitiva

**Origem**: unknown


---

### Identificação de Gaps Competitivos
*Relevância: 0.88 | Tags: gaps, oportunidades, diferenciacao*

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Componentes Principais

| Componente | Localização | Função |
|-----------|-----------|---------|
| **Orchestrator** | `.claude/commands/research.md` | Coordena todo pipeline |
| **Pillar Agents** | `.claude/commands/{analyze_market,analyze_competitors,extract_keywords}.md` | Executa pesquisas temáticas |
| **Chunk Composer** | `.claude/commands/compose_prompts.md` | Transforma dados em prompts |
| **Python Server** | `app/server/research_agent_*.py` | Backend REST API |
| **Knowledge Base**

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---

---

**Metadados da Injeção:**
- **Versículos injetados**: 3
- **Fonte**: mentor_agent/PROCESSADOS/
- **Última atualização**: 2025-11-14 08:11:52
- **Versão do schema**: 1.0.0

**Referências**: `CAPITULO_analise_01:versiculo_7, CAPITULO_marketplace_01:versiculo_22, CAPITULO_analise_02:versiculo_12`

## Conteúdo

### Workflow 2: Análise Competitiva (10-15 min)

```
1. Execute: /analyze_competitors
   Input: Product + Competitor URLs

2. Review: Gaps and positioning (Pilar 2)

3. Use: Chunk 3 para diferenciação

4. Output: Strategic positioning insights
```

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---

### Conceito Core
*Relevância: 0.57 | Tags: ecommerce, general, intermediate*

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Research System (Origem)
- **6 Pilares**: Market, Competitors, Product, Keywords, Trends, FAQ
- **5-Chunk Library**: Consolidation, Keywords, Gaps, Ad Structure, Validation
- **7 Agentes**: Orchestrator, Market, Competitor, Keyword, FAQ, Validator, Meta
- **5 CLI Commands**: /research, /analyze_market, /analyze_competitors, /extract_keywords, /compose_prompts
- **6 Python Modules**: models, config, orchestrator, agents, routes, meta
- **Knowledge Base**: 8 JSON files com semantic maps, inven

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---

### Conceito Core
*Relevância: 0.57 | Tags: ecommerce, general, intermediate*

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### 3. CompetitorAnalystAgent
**Role**: Competitive intelligence expert
**Keywords**: competitor|analysis|positioning|messaging|gap
**File**: `research_agents.py:CompetitorAnalystAgent`

Responsibilities:
- Analyze competitor products
- Extract strengths/weaknesses
- Identify market gaps
- Extract messaging themes
- Find differentiation opportunities

**Returns**: `CompetitiveAnalysisResult`

**Interface**:
```python
agent = CompetitorAnalystAgent()
result = await agent.execute(request, report)

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---

### Keywords
*Relevância: 0.67 | Tags: ecommerce, general, intermediate*

# Keywords

**Categoria**: analise_concorrencia
**Qualidade**: 0.65/1.00
**Data**: 20251113

## Conteúdo

output, strategic, workflow, product, competitor, execute, chunk, pilar, 
1. execute: /analyze_competitors
   input: product + competitor urls

2. review: gaps and positioning (pilar 2)

3. use: chunk 3 para diferenciação

4. output: strategic positioning insights
, input, review, competitiva

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Keywords

**Origem**: desconhecida


---

### 📚 Knowledge Base (Dados)
*Relevância: 0.58 | Tags: ecommerce, general, intermediate*

# 📚 Knowledge Base (Dados)

**Categoria**: analise_concorrencia
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

### Localização: `RAW_LEM_v1.1/` + `knowledge_artifacts_v1/`

#### Arquivos Principais

| Arquivo | Tipo | Função |
|---------|------|---------|
| `knowledge_base_consolidated.json` | JSON | KB consolidada com 1000+ entries |
| `genesis_knowledge_cards.json` | JSON | Cartões de conhecimento Genesis |
| `knowledge_cards_paddleocr.json` | JSON | Cartões enriquecidos |
| `semantic_paddleocr.json` | JSON | Estruturas semânticas |
| `semantic_map.json` | JSON | Mapa semântico de conceitos |
| `catalog_index.json` | JSON | Índice de catálogo |
| `inventory.json` | JSON | Inventário de artefatos |

#### Estrutura JSON Padrão

```json
{
  "metadata": {
    "research_date": "YYYY-MM-DD",
    "product_name": "...",
    "research_type": "competitive|market|product|trend|faq"
  },
  "findings": {
    "primary_insights": [],
    "secondary_insights": [],
    "gaps": []
  },
  "structured_data": {
    "keywords": [],
    "competitors": [],
    "trends": [],
    "faq": []
  }
}
```

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Keywords, Core, Base, Knowledge, Conceito, Dados

**Origem**: desconhecida


---

### 📈 Métricas & Estatísticas
*Relevância: 0.58 | Tags: ecommerce, abstract*

# 📈 Métricas & Estatísticas

**Categoria**: analise_concorrencia
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

### Cobertura

- **Total Ficheiros**: 41 markdown docs + 6 Python modules + 8 JSON configs
- **Total Linhas**: 3,550+ lines código + 2,700+ lines documentação
- **CLI Commands**: 5 (research, analyze_market, analyze_competitors, extract_keywords, compose_prompts)
- **Python Modules**: 6 (models, config, orchestrator, agents, routes, meta)
- **Framework Files**: 20+

### Capacidades

- **Agentes**: 7 (orchestrator, market, competitor, keyword, faq, validator, meta)
- **Pilares**: 6 (market, competitors, product, keywords, trends, faq)
- **Chunks**: 5 (consolidation, keywords, gaps, structure, validation)
- **Steps**: 40+ (cada um com 0-level prompt)
- **Variáveis**: 25+ ($product_name, $category, etc)

### Performance

- **Pesquisa Rápida**: 5-10 minutos
- **Pesquisa Profunda**: 20-30 minutos
- **Keywords Only**: 2-5 minutos
- **Concurrent Jobs**: Até 15+ simultâneos
- **Quality Score**: 75-95%

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Métricas, Estatísticas

**Origem**: _CONSOLIDATED_ecommerce_other.md


---

### 🚀 Quick Start Workflows
*Relevância: 0.68 | Tags: ecommerce, general, intermediate*

# 🚀 Quick Start Workflows

**Categoria**: analise_concorrencia
**Qualidade**: 0.77/1.00
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

4. 

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Workflows, Start, Quick

**Origem**: desconhecida


---

*... (conteúdo truncado por limite de 1500 tokens)*
---

**Metadados da Injeção:**
- **Versículos injetados**: 194
- **Fonte**: mentor_agent/PROCESSADOS/
- **Última atualização**: 2025-11-14 08:11:52
- **Versão do schema**: 1.0.0

**Referências**: `CAPITULO_analise_03:versiculo_1, CAPITULO_analise_03:versiculo_5, CAPITULO_analise_03:versiculo_6, CAPITULO_analise_04:versiculo_37, CAPITULO_analise_04:versiculo_47, CAPITULO_analise_04:versiculo_50, CAPITULO_analise_05:versiculo_18, CAPITULO_analise_05:versiculo_21, CAPITULO_analise_05:versiculo_16, CAPITULO_analise_06:versiculo_3, CAPITULO_analise_06:versiculo_4, CAPITULO_analise_06:versiculo_2, CAPITULO_estrategia_01:versiculo_4, CAPITULO_general_01:versiculo_7, CAPITULO_marketplace_03:versiculo_1, CAPITULO_marketplace_03:versiculo_12, CAPITULO_marketplace_03:versiculo_5, CAPITULO_marketplace_04:versiculo_5, CAPITULO_marketplace_04:versiculo_17, CAPITULO_marketplace_04:versiculo_9, CAPITULO_marketplace_05:versiculo_10, CAPITULO_marketplace_05:versiculo_13, CAPITULO_marketplace_05:versiculo_11, CAPITULO_marketplace_06:versiculo_8, CAPITULO_marketplace_06:versiculo_14, CAPITULO_marketplace_06:versiculo_22, CAPITULO_marketplace_07:versiculo_15, CAPITULO_marketplace_07:versiculo_8, CAPITULO_marketplace_07:versiculo_19, CAPITULO_marketplace_08:versiculo_7, CAPITULO_marketplace_08:versiculo_2, CAPITULO_marketplace_08:versiculo_6, CAPITULO_marketplace_09:versiculo_5, CAPITULO_marketplace_09:versiculo_4, CAPITULO_marketplace_09:versiculo_10, CAPITULO_marketplace_10:versiculo_16, CAPITULO_marketplace_10:versiculo_4, CAPITULO_marketplace_10:versiculo_11, CAPITULO_marketplace_11:versiculo_21, CAPITULO_marketplace_11:versiculo_6, CAPITULO_marketplace_11:versiculo_7, CAPITULO_marketplace_12:versiculo_1, CAPITULO_marketplace_12:versiculo_6, CAPITULO_marketplace_12:versiculo_7, CAPITULO_marketplace_13:versiculo_23, CAPITULO_marketplace_13:versiculo_21, CAPITULO_marketplace_13:versiculo_20, CAPITULO_marketplace_14:versiculo_16, CAPITULO_marketplace_14:versiculo_5, CAPITULO_marketplace_14:versiculo_8, CAPITULO_marketplace_15:versiculo_16, CAPITULO_marketplace_15:versiculo_4, CAPITULO_marketplace_15:versiculo_10, CAPITULO_marketplace_16:versiculo_23, CAPITULO_marketplace_16:versiculo_2, CAPITULO_marketplace_16:versiculo_1, CAPITULO_marketplace_17:versiculo_3, CAPITULO_marketplace_17:versiculo_14, CAPITULO_marketplace_17:versiculo_2, CAPITULO_marketplace_18:versiculo_4, CAPITULO_marketplace_18:versiculo_11, CAPITULO_marketplace_18:versiculo_1, CAPITULO_marketplace_19:versiculo_12, CAPITULO_marketplace_19:versiculo_16, CAPITULO_marketplace_19:versiculo_10, CAPITULO_marketplace_20:versiculo_8, CAPITULO_marketplace_20:versiculo_6, CAPITULO_marketplace_20:versiculo_9, CAPITULO_marketplace_21:versiculo_14, CAPITULO_marketplace_21:versiculo_18, CAPITULO_marketplace_21:versiculo_8, CAPITULO_marketplace_22:versiculo_16, CAPITULO_marketplace_22:versiculo_1, CAPITULO_marketplace_22:versiculo_14, CAPITULO_marketplace_23:versiculo_15, CAPITULO_marketplace_23:versiculo_19, CAPITULO_marketplace_23:versiculo_22, CAPITULO_marketplace_24:versiculo_5, CAPITULO_marketplace_24:versiculo_13, CAPITULO_marketplace_24:versiculo_17, CAPITULO_marketplace_25:versiculo_10, CAPITULO_marketplace_25:versiculo_2, CAPITULO_marketplace_25:versiculo_3, CAPITULO_marketplace_26:versiculo_4, CAPITULO_marketplace_26:versiculo_5, CAPITULO_marketplace_26:versiculo_6, CAPITULO_marketplace_27:versiculo_15, CAPITULO_marketplace_27:versiculo_13, CAPITULO_marketplace_27:versiculo_12, CAPITULO_marketplace_28:versiculo_1, CAPITULO_marketplace_28:versiculo_5, CAPITULO_marketplace_28:versiculo_8, CAPITULO_marketplace_29:versiculo_6, CAPITULO_marketplace_29:versiculo_7, CAPITULO_marketplace_29:versiculo_1, CAPITULO_marketplace_30:versiculo_34, CAPITULO_marketplace_30:versiculo_9, CAPITULO_marketplace_30:versiculo_13, CAPITULO_marketplace_31:versiculo_22, CAPITULO_marketplace_31:versiculo_38, CAPITULO_marketplace_31:versiculo_37, CAPITULO_marketplace_32:versiculo_6, CAPITULO_marketplace_32:versiculo_10, CAPITULO_marketplace_32:versiculo_13, CAPITULO_marketplace_33:versiculo_8, CAPITULO_marketplace_33:versiculo_12, CAPITULO_marketplace_33:versiculo_1, CAPITULO_marketplace_34:versiculo_17, CAPITULO_marketplace_34:versiculo_2, CAPITULO_marketplace_34:versiculo_8, CAPITULO_marketplace_35:versiculo_4, CAPITULO_marketplace_35:versiculo_6, CAPITULO_marketplace_35:versiculo_9, CAPITULO_marketplace_36:versiculo_7, CAPITULO_marketplace_36:versiculo_11, CAPITULO_marketplace_36:versiculo_13, CAPITULO_marketplace_37:versiculo_23, CAPITULO_marketplace_37:versiculo_24, CAPITULO_marketplace_37:versiculo_15, CAPITULO_marketplace_38:versiculo_4, CAPITULO_marketplace_38:versiculo_1, CAPITULO_marketplace_38:versiculo_2, CAPITULO_marketplace_39:versiculo_13, CAPITULO_marketplace_39:versiculo_14, CAPITULO_marketplace_39:versiculo_18, CAPITULO_marketplace_40:versiculo_1, CAPITULO_marketplace_40:versiculo_3, CAPITULO_marketplace_40:versiculo_4, CAPITULO_marketplace_41:versiculo_7, CAPITULO_marketplace_41:versiculo_3, CAPITULO_marketplace_41:versiculo_4, CAPITULO_marketplace_42:versiculo_27, CAPITULO_marketplace_42:versiculo_8, CAPITULO_marketplace_42:versiculo_2, CAPITULO_marketplace_43:versiculo_2, CAPITULO_marketplace_43:versiculo_23, CAPITULO_marketplace_43:versiculo_18, CAPITULO_marketplace_44:versiculo_8, CAPITULO_marketplace_44:versiculo_9, CAPITULO_marketplace_44:versiculo_11, CAPITULO_marketplace_45:versiculo_2, CAPITULO_marketplace_45:versiculo_3, CAPITULO_marketplace_45:versiculo_4, CAPITULO_marketplace_46:versiculo_13, CAPITULO_marketplace_46:versiculo_2, CAPITULO_marketplace_46:versiculo_11, CAPITULO_marketplace_47:versiculo_1, CAPITULO_marketplace_47:versiculo_10, CAPITULO_marketplace_47:versiculo_13, CAPITULO_marketplace_48:versiculo_10, CAPITULO_marketplace_48:versiculo_12, CAPITULO_marketplace_48:versiculo_4, CAPITULO_marketplace_49:versiculo_2, CAPITULO_marketplace_49:versiculo_5, CAPITULO_marketplace_49:versiculo_6, CAPITULO_marketplace_50:versiculo_2, CAPITULO_marketplace_50:versiculo_6, CAPITULO_marketplace_50:versiculo_1, CAPITULO_marketplace_51:versiculo_16, CAPITULO_marketplace_51:versiculo_8, CAPITULO_marketplace_51:versiculo_3, CAPITULO_marketplace_52:versiculo_2, CAPITULO_marketplace_52:versiculo_10, CAPITULO_marketplace_52:versiculo_12, CAPITULO_marketplace_53:versiculo_13, CAPITULO_marketplace_53:versiculo_2, CAPITULO_marketplace_53:versiculo_8, CAPITULO_marketplace_54:versiculo_13, CAPITULO_marketplace_54:versiculo_14, CAPITULO_marketplace_54:versiculo_15, CAPITULO_marketplace_55:versiculo_9, CAPITULO_marketplace_55:versiculo_13, CAPITULO_marketplace_55:versiculo_3, CAPITULO_marketplace_56:versiculo_5, CAPITULO_marketplace_56:versiculo_8, CAPITULO_marketplace_56:versiculo_16, CAPITULO_marketplace_57:versiculo_2, CAPITULO_marketplace_57:versiculo_20, CAPITULO_marketplace_57:versiculo_3, CAPITULO_marketplace_58:versiculo_2, CAPITULO_marketplace_58:versiculo_1, CAPITULO_marketplace_58:versiculo_3, CAPITULO_marketplace_59:versiculo_9, CAPITULO_marketplace_59:versiculo_1, CAPITULO_marketplace_59:versiculo_2, CAPITULO_marketplace_60:versiculo_15, CAPITULO_marketplace_60:versiculo_12, CAPITULO_marketplace_60:versiculo_1, CAPITULO_marketplace_61:versiculo_11, CAPITULO_marketplace_61:versiculo_2, CAPITULO_marketplace_61:versiculo_7, CAPITULO_marketplace_62:versiculo_7, CAPITULO_marketplace_62:versiculo_1, CAPITULO_marketplace_62:versiculo_2`

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

**Tags**: abstract, ecommerce, general

**Palavras-chave**: Consolidados, Artefatos

**Origem**: desconhecida


---

### Pesquisa de Mercado em Marketplaces
*Relevância: 0.92 | Tags: pesquisa, mercado, marketplace*

# 2. Análise Competitiva

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

### Top 5 Concorrentes

#### Concorrente 1: ASUS Vivobook

- URL: [mercadolivre.com.br/...]
- Preço: R$ 4.500
- Rating: 4.7/5 (980 reviews)
- Mensagem: "Melhor custo-benefício em performance"
- Diferenciais: Preço competitivo, bateria boa
- Principais reclamações: Superaquecimento (45x), bateria (30x)

#### Concorrente 2: Samsung Galaxy Book

- Preço: R$ 5.200
- Rating: 4.8/5 (1.200 reviews)
- Mensagem: "Design fino + Performance"
- Principais reclamações: Preço alto (60x), porta USB limitada (25x)

### Gaps Identificados

```
GAP 1: Suporte técnico em português
Ninguém fala sobre suporte após venda
Seu diferencial: Suporte 24/7 em PT-BR
Aplicação: Headline "Suporte Técnico em Português 24/7"

GAP 2: Ventilação otimizada
Reclamação comum: "Aquece muito"
Seu diferencial: Ventilação otimizada, zero super aquecimento
Aplicação: Bullet "❄️ Zero superaquecimento mesmo 8h ligado"
```

**Tags**: architectural, general

**Palavras-chave**: Análise, Competitiva

**Origem**: unknown


---

### Identificação de Gaps Competitivos
*Relevância: 0.88 | Tags: gaps, oportunidades, diferenciacao*

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Componentes Principais

| Componente | Localização | Função |
|-----------|-----------|---------|
| **Orchestrator** | `.claude/commands/research.md` | Coordena todo pipeline |
| **Pillar Agents** | `.claude/commands/{analyze_market,analyze_competitors,extract_keywords}.md` | Executa pesquisas temáticas |
| **Chunk Composer** | `.claude/commands/compose_prompts.md` | Transforma dados em prompts |
| **Python Server** | `app/server/research_agent_*.py` | Backend REST API |
| **Knowledge Base**

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---

---

**Metadados da Injeção:**
- **Versículos injetados**: 3
- **Fonte**: mentor_agent/PROCESSADOS/
- **Última atualização**: 2025-11-14 08:19:53
- **Versão do schema**: 1.0.0

**Referências**: `CAPITULO_analise_01:versiculo_7, CAPITULO_marketplace_01:versiculo_22, CAPITULO_analise_02:versiculo_12`




## 📚 CONHECIMENTO TÉCNICO

*Este conhecimento foi injetado automaticamente do mentor_agent para enriquecer este prompt com expertise técnica validada.*

### Conceito Core
*Relevância: 0.67 | Tags: ecommerce, general, intermediate*

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.65/1.00
**Data**: 20251113

## Conteúdo

### Workflow 2: Análise Competitiva (10-15 min)

```
1. Execute: /analyze_competitors
   Input: Product + Competitor URLs

2. Review: Gaps and positioning (Pilar 2)

3. Use: Chunk 3 para diferenciação

4. Output: Strategic positioning insights
```

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---

### Conceito Core
*Relevância: 0.57 | Tags: ecommerce, general, intermediate*

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### Research System (Origem)
- **6 Pilares**: Market, Competitors, Product, Keywords, Trends, FAQ
- **5-Chunk Library**: Consolidation, Keywords, Gaps, Ad Structure, Validation
- **7 Agentes**: Orchestrator, Market, Competitor, Keyword, FAQ, Validator, Meta
- **5 CLI Commands**: /research, /analyze_market, /analyze_competitors, /extract_keywords, /compose_prompts
- **6 Python Modules**: models, config, orchestrator, agents, routes, meta
- **Knowledge Base**: 8 JSON files com semantic maps, inven

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---

### Conceito Core
*Relevância: 0.57 | Tags: ecommerce, general, intermediate*

# Conceito Core

**Categoria**: analise_concorrencia
**Qualidade**: 0.75/1.00
**Data**: 20251113

## Conteúdo

### 3. CompetitorAnalystAgent
**Role**: Competitive intelligence expert
**Keywords**: competitor|analysis|positioning|messaging|gap
**File**: `research_agents.py:CompetitorAnalystAgent`

Responsibilities:
- Analyze competitor products
- Extract strengths/weaknesses
- Identify market gaps
- Extract messaging themes
- Find differentiation opportunities

**Returns**: `CompetitiveAnalysisResult`

**Interface**:
```python
agent = CompetitorAnalystAgent()
result = await agent.execute(request, report)

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Conceito, Core

**Origem**: desconhecida


---

### Keywords
*Relevância: 0.67 | Tags: ecommerce, general, intermediate*

# Keywords

**Categoria**: analise_concorrencia
**Qualidade**: 0.65/1.00
**Data**: 20251113

## Conteúdo

output, strategic, workflow, product, competitor, execute, chunk, pilar, 
1. execute: /analyze_competitors
   input: product + competitor urls

2. review: gaps and positioning (pilar 2)

3. use: chunk 3 para diferenciação

4. output: strategic positioning insights
, input, review, competitiva

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Keywords

**Origem**: desconhecida


---

### 📚 Knowledge Base (Dados)
*Relevância: 0.58 | Tags: ecommerce, general, intermediate*

# 📚 Knowledge Base (Dados)

**Categoria**: analise_concorrencia
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

### Localização: `RAW_LEM_v1.1/` + `knowledge_artifacts_v1/`

#### Arquivos Principais

| Arquivo | Tipo | Função |
|---------|------|---------|
| `knowledge_base_consolidated.json` | JSON | KB consolidada com 1000+ entries |
| `genesis_knowledge_cards.json` | JSON | Cartões de conhecimento Genesis |
| `knowledge_cards_paddleocr.json` | JSON | Cartões enriquecidos |
| `semantic_paddleocr.json` | JSON | Estruturas semânticas |
| `semantic_map.json` | JSON | Mapa semântico de conceitos |
| `catalog_index.json` | JSON | Índice de catálogo |
| `inventory.json` | JSON | Inventário de artefatos |

#### Estrutura JSON Padrão

```json
{
  "metadata": {
    "research_date": "YYYY-MM-DD",
    "product_name": "...",
    "research_type": "competitive|market|product|trend|faq"
  },
  "findings": {
    "primary_insights": [],
    "secondary_insights": [],
    "gaps": []
  },
  "structured_data": {
    "keywords": [],
    "competitors": [],
    "trends": [],
    "faq": []
  }
}
```

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Keywords, Core, Base, Knowledge, Conceito, Dados

**Origem**: desconhecida


---

### 📈 Métricas & Estatísticas
*Relevância: 0.58 | Tags: ecommerce, abstract*

# 📈 Métricas & Estatísticas

**Categoria**: analise_concorrencia
**Qualidade**: 0.83/1.00
**Data**: 20251113

## Conteúdo

### Cobertura

- **Total Ficheiros**: 41 markdown docs + 6 Python modules + 8 JSON configs
- **Total Linhas**: 3,550+ lines código + 2,700+ lines documentação
- **CLI Commands**: 5 (research, analyze_market, analyze_competitors, extract_keywords, compose_prompts)
- **Python Modules**: 6 (models, config, orchestrator, agents, routes, meta)
- **Framework Files**: 20+

### Capacidades

- **Agentes**: 7 (orchestrator, market, competitor, keyword, faq, validator, meta)
- **Pilares**: 6 (market, competitors, product, keywords, trends, faq)
- **Chunks**: 5 (consolidation, keywords, gaps, structure, validation)
- **Steps**: 40+ (cada um com 0-level prompt)
- **Variáveis**: 25+ ($product_name, $category, etc)

### Performance

- **Pesquisa Rápida**: 5-10 minutos
- **Pesquisa Profunda**: 20-30 minutos
- **Keywords Only**: 2-5 minutos
- **Concurrent Jobs**: Até 15+ simultâneos
- **Quality Score**: 75-95%

---

**Tags**: ecommerce, abstract

**Palavras-chave**: Métricas, Estatísticas

**Origem**: _CONSOLIDATED_ecommerce_other.md


---

### 🚀 Quick Start Workflows
*Relevância: 0.68 | Tags: ecommerce, general, intermediate*

# 🚀 Quick Start Workflows

**Categoria**: analise_concorrencia
**Qualidade**: 0.77/1.00
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

4. 

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Workflows, Start, Quick

**Origem**: desconhecida


---

*... (conteúdo truncado por limite de 1500 tokens)*
---

**Metadados da Injeção:**
- **Versículos injetados**: 194
- **Fonte**: mentor_agent/PROCESSADOS/
- **Última atualização**: 2025-11-14 08:19:53
- **Versão do schema**: 1.0.0

**Referências**: `CAPITULO_analise_03:versiculo_1, CAPITULO_analise_03:versiculo_5, CAPITULO_analise_03:versiculo_6, CAPITULO_analise_04:versiculo_37, CAPITULO_analise_04:versiculo_47, CAPITULO_analise_04:versiculo_50, CAPITULO_analise_05:versiculo_18, CAPITULO_analise_05:versiculo_21, CAPITULO_analise_05:versiculo_16, CAPITULO_analise_06:versiculo_3, CAPITULO_analise_06:versiculo_4, CAPITULO_analise_06:versiculo_2, CAPITULO_estrategia_01:versiculo_4, CAPITULO_general_01:versiculo_7, CAPITULO_marketplace_03:versiculo_1, CAPITULO_marketplace_03:versiculo_12, CAPITULO_marketplace_03:versiculo_5, CAPITULO_marketplace_04:versiculo_5, CAPITULO_marketplace_04:versiculo_17, CAPITULO_marketplace_04:versiculo_9, CAPITULO_marketplace_05:versiculo_10, CAPITULO_marketplace_05:versiculo_13, CAPITULO_marketplace_05:versiculo_11, CAPITULO_marketplace_06:versiculo_8, CAPITULO_marketplace_06:versiculo_14, CAPITULO_marketplace_06:versiculo_22, CAPITULO_marketplace_07:versiculo_15, CAPITULO_marketplace_07:versiculo_8, CAPITULO_marketplace_07:versiculo_19, CAPITULO_marketplace_08:versiculo_7, CAPITULO_marketplace_08:versiculo_2, CAPITULO_marketplace_08:versiculo_6, CAPITULO_marketplace_09:versiculo_5, CAPITULO_marketplace_09:versiculo_4, CAPITULO_marketplace_09:versiculo_10, CAPITULO_marketplace_10:versiculo_16, CAPITULO_marketplace_10:versiculo_4, CAPITULO_marketplace_10:versiculo_11, CAPITULO_marketplace_11:versiculo_21, CAPITULO_marketplace_11:versiculo_6, CAPITULO_marketplace_11:versiculo_7, CAPITULO_marketplace_12:versiculo_1, CAPITULO_marketplace_12:versiculo_6, CAPITULO_marketplace_12:versiculo_7, CAPITULO_marketplace_13:versiculo_23, CAPITULO_marketplace_13:versiculo_21, CAPITULO_marketplace_13:versiculo_20, CAPITULO_marketplace_14:versiculo_16, CAPITULO_marketplace_14:versiculo_5, CAPITULO_marketplace_14:versiculo_8, CAPITULO_marketplace_15:versiculo_16, CAPITULO_marketplace_15:versiculo_4, CAPITULO_marketplace_15:versiculo_10, CAPITULO_marketplace_16:versiculo_23, CAPITULO_marketplace_16:versiculo_2, CAPITULO_marketplace_16:versiculo_1, CAPITULO_marketplace_17:versiculo_3, CAPITULO_marketplace_17:versiculo_14, CAPITULO_marketplace_17:versiculo_2, CAPITULO_marketplace_18:versiculo_4, CAPITULO_marketplace_18:versiculo_11, CAPITULO_marketplace_18:versiculo_1, CAPITULO_marketplace_19:versiculo_12, CAPITULO_marketplace_19:versiculo_16, CAPITULO_marketplace_19:versiculo_10, CAPITULO_marketplace_20:versiculo_8, CAPITULO_marketplace_20:versiculo_6, CAPITULO_marketplace_20:versiculo_9, CAPITULO_marketplace_21:versiculo_14, CAPITULO_marketplace_21:versiculo_18, CAPITULO_marketplace_21:versiculo_8, CAPITULO_marketplace_22:versiculo_16, CAPITULO_marketplace_22:versiculo_1, CAPITULO_marketplace_22:versiculo_14, CAPITULO_marketplace_23:versiculo_15, CAPITULO_marketplace_23:versiculo_19, CAPITULO_marketplace_23:versiculo_22, CAPITULO_marketplace_24:versiculo_5, CAPITULO_marketplace_24:versiculo_13, CAPITULO_marketplace_24:versiculo_17, CAPITULO_marketplace_25:versiculo_10, CAPITULO_marketplace_25:versiculo_2, CAPITULO_marketplace_25:versiculo_3, CAPITULO_marketplace_26:versiculo_4, CAPITULO_marketplace_26:versiculo_5, CAPITULO_marketplace_26:versiculo_6, CAPITULO_marketplace_27:versiculo_15, CAPITULO_marketplace_27:versiculo_13, CAPITULO_marketplace_27:versiculo_12, CAPITULO_marketplace_28:versiculo_1, CAPITULO_marketplace_28:versiculo_5, CAPITULO_marketplace_28:versiculo_8, CAPITULO_marketplace_29:versiculo_6, CAPITULO_marketplace_29:versiculo_7, CAPITULO_marketplace_29:versiculo_1, CAPITULO_marketplace_30:versiculo_34, CAPITULO_marketplace_30:versiculo_9, CAPITULO_marketplace_30:versiculo_13, CAPITULO_marketplace_31:versiculo_22, CAPITULO_marketplace_31:versiculo_38, CAPITULO_marketplace_31:versiculo_37, CAPITULO_marketplace_32:versiculo_6, CAPITULO_marketplace_32:versiculo_10, CAPITULO_marketplace_32:versiculo_13, CAPITULO_marketplace_33:versiculo_8, CAPITULO_marketplace_33:versiculo_12, CAPITULO_marketplace_33:versiculo_1, CAPITULO_marketplace_34:versiculo_17, CAPITULO_marketplace_34:versiculo_2, CAPITULO_marketplace_34:versiculo_8, CAPITULO_marketplace_35:versiculo_4, CAPITULO_marketplace_35:versiculo_6, CAPITULO_marketplace_35:versiculo_9, CAPITULO_marketplace_36:versiculo_7, CAPITULO_marketplace_36:versiculo_11, CAPITULO_marketplace_36:versiculo_13, CAPITULO_marketplace_37:versiculo_23, CAPITULO_marketplace_37:versiculo_24, CAPITULO_marketplace_37:versiculo_15, CAPITULO_marketplace_38:versiculo_4, CAPITULO_marketplace_38:versiculo_1, CAPITULO_marketplace_38:versiculo_2, CAPITULO_marketplace_39:versiculo_13, CAPITULO_marketplace_39:versiculo_14, CAPITULO_marketplace_39:versiculo_18, CAPITULO_marketplace_40:versiculo_1, CAPITULO_marketplace_40:versiculo_3, CAPITULO_marketplace_40:versiculo_4, CAPITULO_marketplace_41:versiculo_7, CAPITULO_marketplace_41:versiculo_3, CAPITULO_marketplace_41:versiculo_4, CAPITULO_marketplace_42:versiculo_27, CAPITULO_marketplace_42:versiculo_8, CAPITULO_marketplace_42:versiculo_2, CAPITULO_marketplace_43:versiculo_2, CAPITULO_marketplace_43:versiculo_23, CAPITULO_marketplace_43:versiculo_18, CAPITULO_marketplace_44:versiculo_8, CAPITULO_marketplace_44:versiculo_9, CAPITULO_marketplace_44:versiculo_11, CAPITULO_marketplace_45:versiculo_2, CAPITULO_marketplace_45:versiculo_3, CAPITULO_marketplace_45:versiculo_4, CAPITULO_marketplace_46:versiculo_13, CAPITULO_marketplace_46:versiculo_2, CAPITULO_marketplace_46:versiculo_11, CAPITULO_marketplace_47:versiculo_1, CAPITULO_marketplace_47:versiculo_10, CAPITULO_marketplace_47:versiculo_13, CAPITULO_marketplace_48:versiculo_10, CAPITULO_marketplace_48:versiculo_12, CAPITULO_marketplace_48:versiculo_4, CAPITULO_marketplace_49:versiculo_2, CAPITULO_marketplace_49:versiculo_5, CAPITULO_marketplace_49:versiculo_6, CAPITULO_marketplace_50:versiculo_2, CAPITULO_marketplace_50:versiculo_6, CAPITULO_marketplace_50:versiculo_1, CAPITULO_marketplace_51:versiculo_16, CAPITULO_marketplace_51:versiculo_8, CAPITULO_marketplace_51:versiculo_3, CAPITULO_marketplace_52:versiculo_2, CAPITULO_marketplace_52:versiculo_10, CAPITULO_marketplace_52:versiculo_12, CAPITULO_marketplace_53:versiculo_13, CAPITULO_marketplace_53:versiculo_2, CAPITULO_marketplace_53:versiculo_8, CAPITULO_marketplace_54:versiculo_13, CAPITULO_marketplace_54:versiculo_14, CAPITULO_marketplace_54:versiculo_15, CAPITULO_marketplace_55:versiculo_9, CAPITULO_marketplace_55:versiculo_13, CAPITULO_marketplace_55:versiculo_3, CAPITULO_marketplace_56:versiculo_5, CAPITULO_marketplace_56:versiculo_8, CAPITULO_marketplace_56:versiculo_16, CAPITULO_marketplace_57:versiculo_2, CAPITULO_marketplace_57:versiculo_20, CAPITULO_marketplace_57:versiculo_3, CAPITULO_marketplace_58:versiculo_2, CAPITULO_marketplace_58:versiculo_1, CAPITULO_marketplace_58:versiculo_3, CAPITULO_marketplace_59:versiculo_9, CAPITULO_marketplace_59:versiculo_1, CAPITULO_marketplace_59:versiculo_2, CAPITULO_marketplace_60:versiculo_15, CAPITULO_marketplace_60:versiculo_12, CAPITULO_marketplace_60:versiculo_1, CAPITULO_marketplace_61:versiculo_11, CAPITULO_marketplace_61:versiculo_2, CAPITULO_marketplace_61:versiculo_7, CAPITULO_marketplace_62:versiculo_7, CAPITULO_marketplace_62:versiculo_1, CAPITULO_marketplace_62:versiculo_2`


