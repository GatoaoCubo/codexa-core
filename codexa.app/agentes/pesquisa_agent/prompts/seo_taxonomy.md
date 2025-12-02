# MÓDULO: TAXONOMIA SEO

## 📋 MODULE_METADATA (TAC-7 Header)

```yaml
id: seo_taxonomy_v1
version: 1.0.0
purpose: "Consolidate and cluster keywords semantically for SEO strategy"
category: seo_intelligence
dependencies:
  - config/accessible_urls.md (relevant sections)
  - web_search capability (required for most modules)
execution_time: 4-6 min
isolation: module
portability: llm_agnostic
```

## 📥 INPUT_CONTRACT

**Required Inputs**:
- `$marketplace_patterns` - Input parameter
- `$organic_keywords` - Input parameter

**Optional Inputs**: (see original content below)

## 📤 OUTPUT_CONTRACT

**Primary Outputs**: `[SEO INBOUND]`, `[SEO OUTBOUND]`

**Export Variables**:
```yaml
seo_clusters: "Semantic keyword clusters"
negative_keywords: "Keywords to avoid"
```

## 🎯 TASK

**Role**: SEO Strategy Specialist
**Objective**: Consolidate and cluster keywords semantically for SEO strategy
**Standards**: (see original content below)
**Constraints**: Max execution time: 4-6 min, All queries logged

## ✅ VALIDATION (Quality Gates)

(See original content for specific validation criteria)

## 🔗 CONTEXT (Usage & Integration)

**Upstream Dependencies**: Previous steps in execution plan
**Downstream Consumers**: Subsequent steps + output blocks
**Data Flow**: (see original content)

---



## Objetivo
Consolidar taxonomia completa de palavras-chave, clusters semânticos, morfologias e termos de conversão para SEO inbound (marketplaces) e outbound (SERP, conteúdo).

## Entradas
- Head terms identificados no brief e validação
- Longtails gerados no banco de consultas
- Termos coletados em web search inbound (marketplaces)
- Termos coletados em web search outbound (SERP, social)
- Sinônimos e variações morfológicas
- Regras de compliance (termos bloqueados)

## Estrutura de Taxonomia

### 1. Head Terms (Núcleo)

Termos principais de 1-3 palavras com maior volume e intenção clara.

```
[HEAD TERMS PRIORITÁRIOS]
termo_1
termo_2
termo_3
...
```

Critérios de priorização:
- Presente no brief ou derivado direto
- Intenção de compra clara
- Aderência a políticas (sem bloqueios)
- Potencial de variação longtail
- Observado em múltiplas fontes (inbound + outbound)

### 2. Longtails (Expansão)

Termos de 3+ palavras combinando head + modificadores.

```
[LONGTAILS]
head_term + material
head_term + cor
head_term + tamanho
head_term + compatibilidade
head_term + benefício
head_term + ocasião
head_term + público
...
```

Estruturas eficazes:
- **Atributo físico**: [head] + [material/cor/tamanho]
  - Ex: fone bluetooth preto grande
- **Especificação técnica**: [head] + [medida/capacidade]
  - Ex: fone bluetooth 50h bateria
- **Benefício**: [head] + [para/com] + [uso/resultado]
  - Ex: fone bluetooth para treino
- **Comparação**: [head] + [vs/ou/melhor que]
  - Ex: fone bluetooth vs com fio
- **Segmento**: [head] + [preço/tipo]
  - Ex: fone bluetooth barato original

### 3. Sinônimos e Variações Morfológicas

```
[SINÔNIMOS E VARIAÇÕES MORFOLÓGICAS]
head_term: sinônimo_1 sinônimo_2
variação_singular: variação_plural
variação_regional: variação_formal
termo_técnico: termo_coloquial
...
```

Fontes:
- Termos alternativos observados em SERP
- Gírias e coloquialismos em UGC (TikTok, YouTube)
- Diferenças regionais Brasil
- Nomenclaturas técnicas vs comerciais

Exemplo:
```
fone bluetooth: fone sem fio headphone bluetooth fone wireless
fone: fones headphone headfone
original: legítimo autêntico verdadeiro
barato: econômico acessível bom preço custo-benefício
```

### 4. Clusters Semânticos

Agrupamento por intenção e contexto.

#### Intenção Informacional
Busca por conhecimento antes da compra.
```
como funciona [head]
o que é [head]
[head] vale a pena
diferença entre [head] e [alternativa]
vantagens de [head]
```

#### Intenção Comparativa
Avaliação de opções.
```
melhor [head]
top [N] [head]
[head] vs [alternativa]
[head] mais barato
[head] custo-benefício
```

#### Intenção Transacional
Pronto para comprar.
```
comprar [head]
[head] preço
[head] promoção
[head] frete grátis
[head] entrega rápida
onde comprar [head]
```

#### Intenção Navegacional
Busca marca/modelo específico.
```
[marca] [head]
[modelo] [head]
[head] [marca] oficial
```

### 5. Bigramas e Trigramas Úteis

Combinações de 2-3 palavras recorrentes em títulos eficazes.

```
Bigramas eficazes:
- original lacrado
- frete grátis
- melhor preço
- garantia estendida
- entrega rápida

Trigramas eficazes:
- original com garantia
- melhor preço Brasil
- frete grátis Brasil
- lacrado nota fiscal
```

### 6. Verbos de Compra e Ação

Verbos que indicam intenção transacional.

```
Verbos de compra:
- comprar
- adquirir
- encomendar
- pedir
- solicitar

Verbos de avaliação:
- comparar
- avaliar
- testar
- verificar
- conferir

Verbos de benefício:
- economizar
- ganhar
- melhorar
- resolver
- facilitar
```

### 7. Modificadores de Qualificação

Adjetivos e advérbios que refinam busca.

```
Preço/Valor:
- barato
- econômico
- premium
- custo-benefício
- promoção

Qualidade:
- melhor
- top
- bom
- excelente
- confiável

Originalidade:
- original
- legítimo
- oficial
- autorizado

Novidade:
- novo
- lançamento
- última geração
- 2025 (ano atual)
```

### 8. Contexto e Ocasião

```
[TERMO CONTEXTUAL E OCASIÃO]
ocasião: trabalho estudo treino viagem casa
público: profissional estudante atleta viajante família
ambiente: escritório academia transporte público home office
frequência: uso diário ocasional intensivo
estilo: casual formal esportivo minimalista
```

Longtails contextuais:
- [head] para [ocasião]
- [head] de [estilo]
- [head] [público-alvo]

### 9. Negativos e Bloqueios

Termos a evitar por compliance ou irrelevância.

```
Termos bloqueados (compliance):
- [termos médicos não autorizados]
- [claims absolutos sem prova]
- [comparações denigratórias]
- [termos de urgência falsa]

Termos negativos (SEO):
- [termos de baixa intenção]
- [spam keywords]
- [termos de categoria errada]
```

## Output: Blocos no research_notes

### [HEAD TERMS PRIORITÁRIOS]
```
fone bluetooth
fone sem fio
headphone bluetooth
```

### [LONGTAILS]
```
fone bluetooth com cancelamento de ruído
fone bluetooth para treino
fone bluetooth barato original
fone bluetooth 50h bateria
fone bluetooth dobrável
fone bluetooth com fio auxiliar
fone bluetooth para trabalho
fone bluetooth confortável
```

### [SINÔNIMOS E VARIAÇÕES MORFOLÓGICAS]
```
fone bluetooth: fone sem fio headphone bluetooth fone wireless
original: legítimo autêntico certificado
barato: econômico acessível bom preço
bateria: autonomia duração carga
```

### [TERMO CONTEXTUAL E OCASIÃO]
```
ocasião: trabalho remoto treino viagem estudo
público: profissionais estudantes atletas viajantes
ambiente: home office academia transporte
frequência: uso diário prolongado intensivo
estilo: minimalista esportivo corporativo
```

### [SEO INBOUND]
Foco em marketplaces.

```
padrão de título eficaz: [Marca] [Produto] [Especificação Chave] [Benefício] [Prova]
exemplo: Fone JBL Tune 510BT Bluetooth 40h Bateria Original Anatel

atributo que melhora ranqueamento: duração de bateria em horas (observado em 80% dos top 10)

combinação longtail com benefício: fone bluetooth para home office com cancelamento de ruído

sinal de prova que diferencia: certificação Anatel visível + rating >4.5 + volume >500 avaliações
```

### [SEO OUTBOUND]
Foco em SERP e conteúdo.

```
head ou padrão de título eficaz: "Melhores Fones Bluetooth 2025: Top 10 com Review Completo"

pergunta frequente do público: "Qual o melhor fone bluetooth custo-benefício 2025?"

termo semântico útil: headphone sem fio para trabalho remoto qualidade de áudio

pauta sugerida: "Guia completo: como escolher fone bluetooth para home office (duração bateria, conforto, cancelamento ruído)"
```

## Processo de Consolidação

### 1. Coleta de Termos Brutos
Reunir de todas as fontes:
- Brief e validação
- Web search inbound (títulos de marketplace)
- Web search outbound (SERP titles, social)
- Reviews e comentários

### 2. Deduplilcação
- Remover termos idênticos
- Agrupar variações mínimas (plural/singular)
- Manter variações regionais ou de intenção diferentes

### 3. Classificação
Categorizar por:
- Tipo (head, longtail, sinônimo)
- Intenção (informacional, transacional)
- Fonte (inbound, outbound)
- Compliance (permitido, bloqueado, revisar)

### 4. Priorização
Ordenar por:
- Frequência observada (múltiplas fontes)
- Intenção de compra (transacional > informacional)
- Aderência a políticas
- Potencial de diferenciação

### 5. Validação de Compliance
Cruzar com regras internas:
- Verificar termos bloqueados
- Validar claims são verificáveis
- Checar exigências por categoria
- Confirmar limites de caracteres para inbound

## Heurísticas de Qualidade

### Para Head Terms
- Mínimo 2, ideal 5-8
- 1-3 palavras cada
- Intenção clara e mensurável
- Diferenciáveis entre si (não redundantes)

### Para Longtails
- Mínimo 10, ideal 30-50
- Cobrir múltiplos modificadores (atributo, benefício, contexto)
- Derivadas de head terms prioritários
- Validadas contra dados reais (se termo foi observado)

### Para Sinônimos
- Incluir variações coloquiais (UGC)
- Incluir termos técnicos (SERP, reviews especializados)
- Não forçar sinônimos artificiais

## Integração com Decisões de Copy

Taxonomia alimenta:
- **Título de anúncio**: usar head + longtail prioritária + prova
- **Descrição**: incorporar longtails secundárias e semânticas
- **Palavras-chave de busca**: head + longtails + sinônimos
- **Conteúdo orgânico**: pautas baseadas em clusters informacionais

## Exemplo Completo: Fone Bluetooth

### Head Terms
```
fone bluetooth
fone sem fio
headphone bluetooth
```

### Longtails (top 20)
```
fone bluetooth com cancelamento de ruído
fone bluetooth para treino
fone bluetooth barato original
fone bluetooth 50h bateria
fone bluetooth dobrável
fone bluetooth confortável para uso prolongado
fone bluetooth com fio auxiliar
fone bluetooth para trabalho remoto
fone bluetooth à prova d'água
fone bluetooth com microfone
fone bluetooth dobrável leve
fone bluetooth custo-benefício
fone bluetooth original lacrado
fone bluetooth entrega rápida
fone bluetooth garantia estendida
fone bluetooth marca JBL
fone bluetooth melhor avaliado
fone bluetooth para estudar
fone bluetooth graves potentes
fone bluetooth multipoint (conecta 2 dispositivos)
```

### Sinônimos
```
fone bluetooth: fone sem fio, headphone bluetooth, fone wireless, headset bluetooth
original: legítimo, autêntico, certificado, oficial
barato: econômico, acessível, bom preço, custo-benefício, em conta
confortável: ergonômico, macio, leve, ajustável
```

### Clusters Semânticos

**Informacional**:
- como escolher fone bluetooth
- fone bluetooth vs fone com fio
- o que é cancelamento de ruído
- vale a pena fone bluetooth barato

**Comparativo**:
- melhor fone bluetooth 2025
- top 10 fone bluetooth
- fone bluetooth JBL vs Sony
- fone bluetooth custo-benefício

**Transacional**:
- comprar fone bluetooth
- fone bluetooth preço
- fone bluetooth promoção
- fone bluetooth frete grátis
- onde comprar fone bluetooth original

### Contexto
```
ocasião: trabalho remoto, treino, viagem, estudo, lazer
público: profissionais, estudantes, atletas, viajantes frequentes
ambiente: home office, academia, transporte público, escritório
frequência: uso diário, uso prolongado >4h, uso ocasional
```

### SEO Inbound
```
padrão título: [Marca] Fone [Modelo] Bluetooth [Bateria] [Diferencial] [Prova]
exemplo: JBL Fone Tune 510BT Bluetooth 40h Original Anatel Garantia 12m

atributos ranqueiam: bateria (horas), certificação Anatel, original, marca
```

### SEO Outbound
```
títulos eficazes:
- "Melhores Fones Bluetooth 2025: Guia Completo com Reviews"
- "Fone Bluetooth Bom e Barato: Top 10 Custo-Benefício"
- "Como Escolher Fone Bluetooth para Home Office"

perguntas frequentes:
- Qual o melhor fone bluetooth custo-benefício?
- Fone bluetooth estraga o ouvido?
- Como saber se fone bluetooth é original?

pautas sugeridas:
- "Duração real de bateria: testamos 10 fones bluetooth"
- "Fone bluetooth para treino: o que considerar (água, conforto, segurança)"
- "Original vs réplica: como identificar fone bluetooth falso"
```

---

**Execução**: Após web searches e antes de decisões de copy
**Inputs**: Dados de inbound + outbound + brief validado
**Output**: Blocos [HEAD TERMS], [LONGTAILS], [SINÔNIMOS], [SEO INBOUND], [SEO OUTBOUND]



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
*Enriquecido em: 2025-11-03T16:21:53.255671*
*Fonte: PaddleOCR Organized Knowledge Base*

## Conteúdo

Each component uses **dense keywords** for inter-file communication:

```
market_research → market|size|trends|growth|customer|pain-points
competitors → competitor|analysis|positioning|messaging|gap
keywords → keyword|seo|hierarchy|search-volume|buyer-intent
faq → faq|objection|question|answer|counter
validation → validation|quality|scoring|completeness|error
prompts → prompt|composition|ai-input|instruction|chunk
meta → meta|improvement|methodology|optimization
```

Files embed these keywords in comments and docstrings for easy searching.

---

**Tags**: ecommerce, general, implementation

**Palavras-chave**: Dense, Keywords, System

**Origem**: desconhecida


---

### Keywords
*Relevância: 0.31 | Tags: ecommerce, implementation*

# Keywords

**Categoria**: analise_concorrencia
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

market_research → market|size|trends|growth|customer|pain-points
competitors → competitor|analysis|positioning|messaging|gap
keywords → keyword|seo|hierarchy|search-volume|buyer-intent
faq → faq|objection|question|answer|counter
validation → validation|quality|scoring|completeness|error
prompts → prompt|composition|ai-input|instruction|chunk
meta → meta|improvement|methodology|optimization
, dense keywords, dense-keywords-system

each, files

**Tags**: ecommerce, implementation

**Palavras-chave**: Keywords

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---

### Research Workflow: 5 Types
*Relevância: 0.32 | Tags: architectural, ecommerce, general*

# Research Workflow: 5 Types

**Categoria**: analise_concorrencia
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

### 1. Quick Research (45-60 minutes)
- Market research
- Keyword extraction
- Prompt composition
- **Best for**: Fast turnaround needed

### 2. Deep Research (3-4 hours)
- All phases
- Comprehensive analysis
- Full AI prompt composition
- **Best for**: Strategic decisions

### 3. Keywords Only (20-30 minutes)
- Keyword extraction only
- 4-level hierarchy
- Long-tail generation
- **Best for**: SEO optimization

### 4. Competitors (90 minutes)
- Competitive analysis
- Market positioning
- Differentiation strategy
- **Best for**: Competitive moves

### 5. AI-Assisted (15-30 minutes)
- AI-optimized workflow
- Claude-powered analysis
- Fast turnaround
- **Best for**: Quick decisions with AI help

---

**Tags**: architectural, ecommerce, general

**Palavras-chave**: Types, Workflow, Research

**Origem**: desconhecida


---

### 🚀 Quick Start Workflows
*Relevância: 0.32 | Tags: ecommerce, general, intermediate*

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

### Regras de Otimização
*Relevância: 0.31 | Tags: ecommerce, general, intermediate*

# Regras de Otimização

**Categoria**: copywriting
**Qualidade**: 0.71/1.00
**Data**: 20251113

## Conteúdo

- Marca entre 115 e 120 caracteres (densidade máxima de keywords)
- Modelo entre 115 e 120 caracteres (foco absoluto em conversão)
- Títulos ≤ 60 caracteres cada (3 versões A/B)
- ZERO stop words em títulos - apenas keywords que convertem
- Mínimo 8 keywords relevantes por campo
- Keywords são enriquecidas automaticamente com a pesquisa SEO
- Estrutura StoryBrand obrigatória na descrição

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Otimização, Regras

**Origem**: desconhecida


---

### Regras de Otimização
*Relevância: 0.31 | Tags: ecommerce, intermediate*

# Regras de Otimização

**Categoria**: copywriting
**Qualidade**: 0.71/1.00
**Data**: 20251113

## Conteúdo

- Marca entre 115 e 120 caracteres (densidade máxima de keywords)
- Modelo entre 115 e 120 caracteres (foco absoluto em conversão)
- Títulos ≤ 60 caracteres cada (3 versões A/B)
- ZERO stop words em títulos - apenas keywords que convertem
- Mínimo 8 keywords relevantes por campo
- Keywords são enriquecidas automaticamente com a pesquisa SEO
- Estrutura StoryBrand obrigatória na descrição

**Tags**: ecommerce, intermediate

**Palavras-chave**: Regras, Otimização

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---

### Response Format
*Relevância: 0.31 | Tags: ecommerce, concrete*

# Response Format

**Categoria**: copywriting
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

Tipo: JSON Schema

```json
{
  "name": "produto_otimizado_seo",
  "strict": true,
  "schema": {
    "type": "object",
    "properties": {
      "marca_modelo": {
        "type": "object",
        "properties": {
          "marca": {
            "type": "string",
            "minLength": 115,
            "maxLength": 120,
            "description": "Nome da marca otimizado para SEO"
          },
          "modelo": {
            "type": "string",
            "minLength": 115,
            "maxLength": 120,
            "description": "Nome do modelo otimizado para conversão"
          },
          "keywords_utilizadas": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Keywords principais utilizadas na otimização"
          }
        },
        "required": ["marca", "modelo", "keywords_utilizadas"],
        "additionalProperties": false
      },
      "titulos_otimizados": {
        "type": "array",
        "items": {"type": "string", "max

**Tags**: ecommerce, concrete

**Palavras-chave**: Response, Format

**Origem**: _CONSOLIDATED_ecommerce_other.md


---

*... (conteúdo truncado por limite de 1500 tokens)*
---

**Metadados da Injeção:**
- **Versículos injetados**: 199
- **Fonte**: mentor_agent/PROCESSADOS/
- **Última atualização**: 2025-11-14 07:44:47
- **Versão do schema**: 1.0.0

**Referências**: `CAPITULO_analise_03:versiculo_16, CAPITULO_analise_03:versiculo_38, CAPITULO_analise_05:versiculo_22, CAPITULO_analise_05:versiculo_18, CAPITULO_copywriting_04:versiculo_1, CAPITULO_copywriting_04:versiculo_2, CAPITULO_copywriting_04:versiculo_4, CAPITULO_estrategia_01:versiculo_1, CAPITULO_estrategia_01:versiculo_9, CAPITULO_estrategia_01:versiculo_10, CAPITULO_estrategia_02:versiculo_20, CAPITULO_marketplace_03:versiculo_1, CAPITULO_marketplace_03:versiculo_10, CAPITULO_marketplace_03:versiculo_12, CAPITULO_marketplace_04:versiculo_17, CAPITULO_marketplace_04:versiculo_1, CAPITULO_marketplace_04:versiculo_8, CAPITULO_marketplace_05:versiculo_7, CAPITULO_marketplace_05:versiculo_10, CAPITULO_marketplace_05:versiculo_13, CAPITULO_marketplace_06:versiculo_8, CAPITULO_marketplace_06:versiculo_14, CAPITULO_marketplace_06:versiculo_22, CAPITULO_marketplace_07:versiculo_8, CAPITULO_marketplace_07:versiculo_12, CAPITULO_marketplace_07:versiculo_15, CAPITULO_marketplace_08:versiculo_17, CAPITULO_marketplace_08:versiculo_20, CAPITULO_marketplace_08:versiculo_6, CAPITULO_marketplace_09:versiculo_12, CAPITULO_marketplace_09:versiculo_1, CAPITULO_marketplace_09:versiculo_3, CAPITULO_marketplace_10:versiculo_21, CAPITULO_marketplace_10:versiculo_13, CAPITULO_marketplace_10:versiculo_11, CAPITULO_marketplace_11:versiculo_6, CAPITULO_marketplace_11:versiculo_18, CAPITULO_marketplace_11:versiculo_14, CAPITULO_marketplace_12:versiculo_7, CAPITULO_marketplace_12:versiculo_1, CAPITULO_marketplace_12:versiculo_3, CAPITULO_marketplace_13:versiculo_8, CAPITULO_marketplace_13:versiculo_3, CAPITULO_marketplace_13:versiculo_17, CAPITULO_marketplace_14:versiculo_16, CAPITULO_marketplace_14:versiculo_8, CAPITULO_marketplace_14:versiculo_11, CAPITULO_marketplace_15:versiculo_1, CAPITULO_marketplace_15:versiculo_2, CAPITULO_marketplace_15:versiculo_5, CAPITULO_marketplace_16:versiculo_2, CAPITULO_marketplace_16:versiculo_1, CAPITULO_marketplace_16:versiculo_11, CAPITULO_marketplace_17:versiculo_2, CAPITULO_marketplace_17:versiculo_3, CAPITULO_marketplace_17:versiculo_14, CAPITULO_marketplace_18:versiculo_4, CAPITULO_marketplace_18:versiculo_25, CAPITULO_marketplace_18:versiculo_10, CAPITULO_marketplace_19:versiculo_16, CAPITULO_marketplace_19:versiculo_10, CAPITULO_marketplace_19:versiculo_26, CAPITULO_marketplace_20:versiculo_1, CAPITULO_marketplace_20:versiculo_2, CAPITULO_marketplace_20:versiculo_5, CAPITULO_marketplace_21:versiculo_14, CAPITULO_marketplace_21:versiculo_18, CAPITULO_marketplace_21:versiculo_20, CAPITULO_marketplace_22:versiculo_1, CAPITULO_marketplace_22:versiculo_13, CAPITULO_marketplace_22:versiculo_16, CAPITULO_marketplace_23:versiculo_15, CAPITULO_marketplace_23:versiculo_19, CAPITULO_marketplace_23:versiculo_3, CAPITULO_marketplace_24:versiculo_5, CAPITULO_marketplace_24:versiculo_13, CAPITULO_marketplace_24:versiculo_8, CAPITULO_marketplace_25:versiculo_1, CAPITULO_marketplace_25:versiculo_2, CAPITULO_marketplace_25:versiculo_3, CAPITULO_marketplace_26:versiculo_7, CAPITULO_marketplace_26:versiculo_6, CAPITULO_marketplace_26:versiculo_8, CAPITULO_marketplace_27:versiculo_4, CAPITULO_marketplace_27:versiculo_8, CAPITULO_marketplace_27:versiculo_14, CAPITULO_marketplace_28:versiculo_1, CAPITULO_marketplace_28:versiculo_4, CAPITULO_marketplace_28:versiculo_5, CAPITULO_marketplace_29:versiculo_13, CAPITULO_marketplace_29:versiculo_4, CAPITULO_marketplace_29:versiculo_6, CAPITULO_marketplace_30:versiculo_17, CAPITULO_marketplace_30:versiculo_30, CAPITULO_marketplace_30:versiculo_22, CAPITULO_marketplace_31:versiculo_21, CAPITULO_marketplace_31:versiculo_23, CAPITULO_marketplace_31:versiculo_4, CAPITULO_marketplace_32:versiculo_13, CAPITULO_marketplace_32:versiculo_6, CAPITULO_marketplace_32:versiculo_10, CAPITULO_marketplace_33:versiculo_8, CAPITULO_marketplace_33:versiculo_12, CAPITULO_marketplace_33:versiculo_1, CAPITULO_marketplace_34:versiculo_1, CAPITULO_marketplace_34:versiculo_4, CAPITULO_marketplace_34:versiculo_2, CAPITULO_marketplace_35:versiculo_3, CAPITULO_marketplace_35:versiculo_4, CAPITULO_marketplace_35:versiculo_10, CAPITULO_marketplace_36:versiculo_19, CAPITULO_marketplace_36:versiculo_11, CAPITULO_marketplace_36:versiculo_8, CAPITULO_marketplace_37:versiculo_11, CAPITULO_marketplace_37:versiculo_14, CAPITULO_marketplace_37:versiculo_9, CAPITULO_marketplace_38:versiculo_2, CAPITULO_marketplace_38:versiculo_6, CAPITULO_marketplace_38:versiculo_4, CAPITULO_marketplace_39:versiculo_6, CAPITULO_marketplace_39:versiculo_13, CAPITULO_marketplace_39:versiculo_14, CAPITULO_marketplace_40:versiculo_17, CAPITULO_marketplace_40:versiculo_1, CAPITULO_marketplace_40:versiculo_3, CAPITULO_marketplace_41:versiculo_7, CAPITULO_marketplace_41:versiculo_4, CAPITULO_marketplace_41:versiculo_5, CAPITULO_marketplace_42:versiculo_14, CAPITULO_marketplace_42:versiculo_16, CAPITULO_marketplace_42:versiculo_17, CAPITULO_marketplace_43:versiculo_23, CAPITULO_marketplace_43:versiculo_18, CAPITULO_marketplace_43:versiculo_19, CAPITULO_marketplace_44:versiculo_15, CAPITULO_marketplace_44:versiculo_8, CAPITULO_marketplace_44:versiculo_9, CAPITULO_marketplace_45:versiculo_5, CAPITULO_marketplace_45:versiculo_3, CAPITULO_marketplace_45:versiculo_15, CAPITULO_marketplace_46:versiculo_17, CAPITULO_marketplace_46:versiculo_2, CAPITULO_marketplace_46:versiculo_11, CAPITULO_marketplace_47:versiculo_1, CAPITULO_marketplace_47:versiculo_10, CAPITULO_marketplace_47:versiculo_13, CAPITULO_marketplace_48:versiculo_10, CAPITULO_marketplace_48:versiculo_5, CAPITULO_marketplace_48:versiculo_12, CAPITULO_marketplace_49:versiculo_5, CAPITULO_marketplace_49:versiculo_6, CAPITULO_marketplace_49:versiculo_10, CAPITULO_marketplace_50:versiculo_2, CAPITULO_marketplace_50:versiculo_6, CAPITULO_marketplace_50:versiculo_13, CAPITULO_marketplace_51:versiculo_13, CAPITULO_marketplace_51:versiculo_16, CAPITULO_marketplace_51:versiculo_8, CAPITULO_marketplace_52:versiculo_2, CAPITULO_marketplace_52:versiculo_10, CAPITULO_marketplace_52:versiculo_9, CAPITULO_marketplace_53:versiculo_13, CAPITULO_marketplace_53:versiculo_8, CAPITULO_marketplace_53:versiculo_1, CAPITULO_marketplace_54:versiculo_16, CAPITULO_marketplace_54:versiculo_13, CAPITULO_marketplace_54:versiculo_4, CAPITULO_marketplace_55:versiculo_3, CAPITULO_marketplace_55:versiculo_13, CAPITULO_marketplace_55:versiculo_8, CAPITULO_marketplace_56:versiculo_16, CAPITULO_marketplace_56:versiculo_2, CAPITULO_marketplace_56:versiculo_5, CAPITULO_marketplace_57:versiculo_20, CAPITULO_marketplace_57:versiculo_11, CAPITULO_marketplace_57:versiculo_15, CAPITULO_marketplace_58:versiculo_7, CAPITULO_marketplace_58:versiculo_2, CAPITULO_marketplace_58:versiculo_1, CAPITULO_marketplace_59:versiculo_9, CAPITULO_marketplace_59:versiculo_1, CAPITULO_marketplace_59:versiculo_2, CAPITULO_marketplace_60:versiculo_15, CAPITULO_marketplace_60:versiculo_4, CAPITULO_marketplace_60:versiculo_6, CAPITULO_marketplace_61:versiculo_11, CAPITULO_marketplace_61:versiculo_2, CAPITULO_marketplace_61:versiculo_7, CAPITULO_marketplace_62:versiculo_6, CAPITULO_marketplace_62:versiculo_7, CAPITULO_marketplace_62:versiculo_1, CAPITULO_operacoes_23:versiculo_28, CAPITULO_operacoes_39:versiculo_22, CAPITULO_operacoes_40:versiculo_3, CAPITULO_visual_01:versiculo_7, CAPITULO_visual_03:versiculo_29, CAPITULO_visual_04:versiculo_23, CAPITULO_visual_10:versiculo_7, CAPITULO_visual_10:versiculo_8`

## Conteúdo

Each component uses **dense keywords** for inter-file communication:

```
market_research → market|size|trends|growth|customer|pain-points
competitors → competitor|analysis|positioning|messaging|gap
keywords → keyword|seo|hierarchy|search-volume|buyer-intent
faq → faq|objection|question|answer|counter
validation → validation|quality|scoring|completeness|error
prompts → prompt|composition|ai-input|instruction|chunk
meta → meta|improvement|methodology|optimization
```

Files embed these keywords in comments and docstrings for easy searching.

---

**Tags**: ecommerce, general, implementation

**Palavras-chave**: Dense, Keywords, System

**Origem**: desconhecida


---

### Keywords
*Relevância: 0.31 | Tags: ecommerce, implementation*

# Keywords

**Categoria**: analise_concorrencia
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

market_research → market|size|trends|growth|customer|pain-points
competitors → competitor|analysis|positioning|messaging|gap
keywords → keyword|seo|hierarchy|search-volume|buyer-intent
faq → faq|objection|question|answer|counter
validation → validation|quality|scoring|completeness|error
prompts → prompt|composition|ai-input|instruction|chunk
meta → meta|improvement|methodology|optimization
, dense keywords, dense-keywords-system

each, files

**Tags**: ecommerce, implementation

**Palavras-chave**: Keywords

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---

### Research Workflow: 5 Types
*Relevância: 0.32 | Tags: architectural, ecommerce, general*

# Research Workflow: 5 Types

**Categoria**: analise_concorrencia
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

### 1. Quick Research (45-60 minutes)
- Market research
- Keyword extraction
- Prompt composition
- **Best for**: Fast turnaround needed

### 2. Deep Research (3-4 hours)
- All phases
- Comprehensive analysis
- Full AI prompt composition
- **Best for**: Strategic decisions

### 3. Keywords Only (20-30 minutes)
- Keyword extraction only
- 4-level hierarchy
- Long-tail generation
- **Best for**: SEO optimization

### 4. Competitors (90 minutes)
- Competitive analysis
- Market positioning
- Differentiation strategy
- **Best for**: Competitive moves

### 5. AI-Assisted (15-30 minutes)
- AI-optimized workflow
- Claude-powered analysis
- Fast turnaround
- **Best for**: Quick decisions with AI help

---

**Tags**: architectural, ecommerce, general

**Palavras-chave**: Types, Workflow, Research

**Origem**: desconhecida


---

### 🚀 Quick Start Workflows
*Relevância: 0.32 | Tags: ecommerce, general, intermediate*

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

### Regras de Otimização
*Relevância: 0.31 | Tags: ecommerce, general, intermediate*

# Regras de Otimização

**Categoria**: copywriting
**Qualidade**: 0.71/1.00
**Data**: 20251113

## Conteúdo

- Marca entre 115 e 120 caracteres (densidade máxima de keywords)
- Modelo entre 115 e 120 caracteres (foco absoluto em conversão)
- Títulos ≤ 60 caracteres cada (3 versões A/B)
- ZERO stop words em títulos - apenas keywords que convertem
- Mínimo 8 keywords relevantes por campo
- Keywords são enriquecidas automaticamente com a pesquisa SEO
- Estrutura StoryBrand obrigatória na descrição

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Otimização, Regras

**Origem**: desconhecida


---

### Regras de Otimização
*Relevância: 0.31 | Tags: ecommerce, intermediate*

# Regras de Otimização

**Categoria**: copywriting
**Qualidade**: 0.71/1.00
**Data**: 20251113

## Conteúdo

- Marca entre 115 e 120 caracteres (densidade máxima de keywords)
- Modelo entre 115 e 120 caracteres (foco absoluto em conversão)
- Títulos ≤ 60 caracteres cada (3 versões A/B)
- ZERO stop words em títulos - apenas keywords que convertem
- Mínimo 8 keywords relevantes por campo
- Keywords são enriquecidas automaticamente com a pesquisa SEO
- Estrutura StoryBrand obrigatória na descrição

**Tags**: ecommerce, intermediate

**Palavras-chave**: Regras, Otimização

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---

### Response Format
*Relevância: 0.31 | Tags: ecommerce, concrete*

# Response Format

**Categoria**: copywriting
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

Tipo: JSON Schema

```json
{
  "name": "produto_otimizado_seo",
  "strict": true,
  "schema": {
    "type": "object",
    "properties": {
      "marca_modelo": {
        "type": "object",
        "properties": {
          "marca": {
            "type": "string",
            "minLength": 115,
            "maxLength": 120,
            "description": "Nome da marca otimizado para SEO"
          },
          "modelo": {
            "type": "string",
            "minLength": 115,
            "maxLength": 120,
            "description": "Nome do modelo otimizado para conversão"
          },
          "keywords_utilizadas": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Keywords principais utilizadas na otimização"
          }
        },
        "required": ["marca", "modelo", "keywords_utilizadas"],
        "additionalProperties": false
      },
      "titulos_otimizados": {
        "type": "array",
        "items": {"type": "string", "max

**Tags**: ecommerce, concrete

**Palavras-chave**: Response, Format

**Origem**: _CONSOLIDATED_ecommerce_other.md


---

*... (conteúdo truncado por limite de 1500 tokens)*
---

**Metadados da Injeção:**
- **Versículos injetados**: 199
- **Fonte**: mentor_agent/PROCESSADOS/
- **Última atualização**: 2025-11-14 08:11:53
- **Versão do schema**: 1.0.0

**Referências**: `CAPITULO_analise_03:versiculo_16, CAPITULO_analise_03:versiculo_38, CAPITULO_analise_05:versiculo_22, CAPITULO_analise_05:versiculo_18, CAPITULO_copywriting_04:versiculo_1, CAPITULO_copywriting_04:versiculo_2, CAPITULO_copywriting_04:versiculo_4, CAPITULO_estrategia_01:versiculo_1, CAPITULO_estrategia_01:versiculo_9, CAPITULO_estrategia_01:versiculo_10, CAPITULO_estrategia_02:versiculo_20, CAPITULO_marketplace_03:versiculo_1, CAPITULO_marketplace_03:versiculo_10, CAPITULO_marketplace_03:versiculo_12, CAPITULO_marketplace_04:versiculo_17, CAPITULO_marketplace_04:versiculo_1, CAPITULO_marketplace_04:versiculo_8, CAPITULO_marketplace_05:versiculo_7, CAPITULO_marketplace_05:versiculo_10, CAPITULO_marketplace_05:versiculo_13, CAPITULO_marketplace_06:versiculo_8, CAPITULO_marketplace_06:versiculo_14, CAPITULO_marketplace_06:versiculo_22, CAPITULO_marketplace_07:versiculo_8, CAPITULO_marketplace_07:versiculo_12, CAPITULO_marketplace_07:versiculo_15, CAPITULO_marketplace_08:versiculo_17, CAPITULO_marketplace_08:versiculo_20, CAPITULO_marketplace_08:versiculo_6, CAPITULO_marketplace_09:versiculo_12, CAPITULO_marketplace_09:versiculo_1, CAPITULO_marketplace_09:versiculo_3, CAPITULO_marketplace_10:versiculo_21, CAPITULO_marketplace_10:versiculo_13, CAPITULO_marketplace_10:versiculo_11, CAPITULO_marketplace_11:versiculo_6, CAPITULO_marketplace_11:versiculo_18, CAPITULO_marketplace_11:versiculo_14, CAPITULO_marketplace_12:versiculo_7, CAPITULO_marketplace_12:versiculo_1, CAPITULO_marketplace_12:versiculo_3, CAPITULO_marketplace_13:versiculo_8, CAPITULO_marketplace_13:versiculo_3, CAPITULO_marketplace_13:versiculo_17, CAPITULO_marketplace_14:versiculo_16, CAPITULO_marketplace_14:versiculo_8, CAPITULO_marketplace_14:versiculo_11, CAPITULO_marketplace_15:versiculo_1, CAPITULO_marketplace_15:versiculo_2, CAPITULO_marketplace_15:versiculo_5, CAPITULO_marketplace_16:versiculo_2, CAPITULO_marketplace_16:versiculo_1, CAPITULO_marketplace_16:versiculo_11, CAPITULO_marketplace_17:versiculo_2, CAPITULO_marketplace_17:versiculo_3, CAPITULO_marketplace_17:versiculo_14, CAPITULO_marketplace_18:versiculo_4, CAPITULO_marketplace_18:versiculo_25, CAPITULO_marketplace_18:versiculo_10, CAPITULO_marketplace_19:versiculo_16, CAPITULO_marketplace_19:versiculo_10, CAPITULO_marketplace_19:versiculo_26, CAPITULO_marketplace_20:versiculo_1, CAPITULO_marketplace_20:versiculo_2, CAPITULO_marketplace_20:versiculo_5, CAPITULO_marketplace_21:versiculo_14, CAPITULO_marketplace_21:versiculo_18, CAPITULO_marketplace_21:versiculo_20, CAPITULO_marketplace_22:versiculo_1, CAPITULO_marketplace_22:versiculo_13, CAPITULO_marketplace_22:versiculo_16, CAPITULO_marketplace_23:versiculo_15, CAPITULO_marketplace_23:versiculo_19, CAPITULO_marketplace_23:versiculo_3, CAPITULO_marketplace_24:versiculo_5, CAPITULO_marketplace_24:versiculo_13, CAPITULO_marketplace_24:versiculo_8, CAPITULO_marketplace_25:versiculo_1, CAPITULO_marketplace_25:versiculo_2, CAPITULO_marketplace_25:versiculo_3, CAPITULO_marketplace_26:versiculo_7, CAPITULO_marketplace_26:versiculo_6, CAPITULO_marketplace_26:versiculo_8, CAPITULO_marketplace_27:versiculo_4, CAPITULO_marketplace_27:versiculo_8, CAPITULO_marketplace_27:versiculo_14, CAPITULO_marketplace_28:versiculo_1, CAPITULO_marketplace_28:versiculo_4, CAPITULO_marketplace_28:versiculo_5, CAPITULO_marketplace_29:versiculo_13, CAPITULO_marketplace_29:versiculo_4, CAPITULO_marketplace_29:versiculo_6, CAPITULO_marketplace_30:versiculo_17, CAPITULO_marketplace_30:versiculo_30, CAPITULO_marketplace_30:versiculo_22, CAPITULO_marketplace_31:versiculo_21, CAPITULO_marketplace_31:versiculo_23, CAPITULO_marketplace_31:versiculo_4, CAPITULO_marketplace_32:versiculo_13, CAPITULO_marketplace_32:versiculo_6, CAPITULO_marketplace_32:versiculo_10, CAPITULO_marketplace_33:versiculo_8, CAPITULO_marketplace_33:versiculo_12, CAPITULO_marketplace_33:versiculo_1, CAPITULO_marketplace_34:versiculo_1, CAPITULO_marketplace_34:versiculo_4, CAPITULO_marketplace_34:versiculo_2, CAPITULO_marketplace_35:versiculo_3, CAPITULO_marketplace_35:versiculo_4, CAPITULO_marketplace_35:versiculo_10, CAPITULO_marketplace_36:versiculo_19, CAPITULO_marketplace_36:versiculo_11, CAPITULO_marketplace_36:versiculo_8, CAPITULO_marketplace_37:versiculo_11, CAPITULO_marketplace_37:versiculo_14, CAPITULO_marketplace_37:versiculo_9, CAPITULO_marketplace_38:versiculo_2, CAPITULO_marketplace_38:versiculo_6, CAPITULO_marketplace_38:versiculo_4, CAPITULO_marketplace_39:versiculo_6, CAPITULO_marketplace_39:versiculo_13, CAPITULO_marketplace_39:versiculo_14, CAPITULO_marketplace_40:versiculo_17, CAPITULO_marketplace_40:versiculo_1, CAPITULO_marketplace_40:versiculo_3, CAPITULO_marketplace_41:versiculo_7, CAPITULO_marketplace_41:versiculo_4, CAPITULO_marketplace_41:versiculo_5, CAPITULO_marketplace_42:versiculo_14, CAPITULO_marketplace_42:versiculo_16, CAPITULO_marketplace_42:versiculo_17, CAPITULO_marketplace_43:versiculo_23, CAPITULO_marketplace_43:versiculo_18, CAPITULO_marketplace_43:versiculo_19, CAPITULO_marketplace_44:versiculo_15, CAPITULO_marketplace_44:versiculo_8, CAPITULO_marketplace_44:versiculo_9, CAPITULO_marketplace_45:versiculo_5, CAPITULO_marketplace_45:versiculo_3, CAPITULO_marketplace_45:versiculo_15, CAPITULO_marketplace_46:versiculo_17, CAPITULO_marketplace_46:versiculo_2, CAPITULO_marketplace_46:versiculo_11, CAPITULO_marketplace_47:versiculo_1, CAPITULO_marketplace_47:versiculo_10, CAPITULO_marketplace_47:versiculo_13, CAPITULO_marketplace_48:versiculo_10, CAPITULO_marketplace_48:versiculo_5, CAPITULO_marketplace_48:versiculo_12, CAPITULO_marketplace_49:versiculo_5, CAPITULO_marketplace_49:versiculo_6, CAPITULO_marketplace_49:versiculo_10, CAPITULO_marketplace_50:versiculo_2, CAPITULO_marketplace_50:versiculo_6, CAPITULO_marketplace_50:versiculo_13, CAPITULO_marketplace_51:versiculo_13, CAPITULO_marketplace_51:versiculo_16, CAPITULO_marketplace_51:versiculo_8, CAPITULO_marketplace_52:versiculo_2, CAPITULO_marketplace_52:versiculo_10, CAPITULO_marketplace_52:versiculo_9, CAPITULO_marketplace_53:versiculo_13, CAPITULO_marketplace_53:versiculo_8, CAPITULO_marketplace_53:versiculo_1, CAPITULO_marketplace_54:versiculo_16, CAPITULO_marketplace_54:versiculo_13, CAPITULO_marketplace_54:versiculo_4, CAPITULO_marketplace_55:versiculo_3, CAPITULO_marketplace_55:versiculo_13, CAPITULO_marketplace_55:versiculo_8, CAPITULO_marketplace_56:versiculo_16, CAPITULO_marketplace_56:versiculo_2, CAPITULO_marketplace_56:versiculo_5, CAPITULO_marketplace_57:versiculo_20, CAPITULO_marketplace_57:versiculo_11, CAPITULO_marketplace_57:versiculo_15, CAPITULO_marketplace_58:versiculo_7, CAPITULO_marketplace_58:versiculo_2, CAPITULO_marketplace_58:versiculo_1, CAPITULO_marketplace_59:versiculo_9, CAPITULO_marketplace_59:versiculo_1, CAPITULO_marketplace_59:versiculo_2, CAPITULO_marketplace_60:versiculo_15, CAPITULO_marketplace_60:versiculo_4, CAPITULO_marketplace_60:versiculo_6, CAPITULO_marketplace_61:versiculo_11, CAPITULO_marketplace_61:versiculo_2, CAPITULO_marketplace_61:versiculo_7, CAPITULO_marketplace_62:versiculo_6, CAPITULO_marketplace_62:versiculo_7, CAPITULO_marketplace_62:versiculo_1, CAPITULO_operacoes_23:versiculo_28, CAPITULO_operacoes_39:versiculo_22, CAPITULO_operacoes_40:versiculo_3, CAPITULO_visual_01:versiculo_7, CAPITULO_visual_03:versiculo_29, CAPITULO_visual_04:versiculo_23, CAPITULO_visual_10:versiculo_7, CAPITULO_visual_10:versiculo_8`




## 📚 CONHECIMENTO TÉCNICO

*Este conhecimento foi injetado automaticamente do mentor_agent para enriquecer este prompt com expertise técnica validada.*

### 🎯 Dense Keywords System
*Relevância: 0.31 | Tags: ecommerce, general, implementation*

# 🎯 Dense Keywords System

**Categoria**: analise_concorrencia
**Qualidade**: 0.73/1.00
**Data**: 20251113

## Conteúdo

Each component uses **dense keywords** for inter-file communication:

```
market_research → market|size|trends|growth|customer|pain-points
competitors → competitor|analysis|positioning|messaging|gap
keywords → keyword|seo|hierarchy|search-volume|buyer-intent
faq → faq|objection|question|answer|counter
validation → validation|quality|scoring|completeness|error
prompts → prompt|composition|ai-input|instruction|chunk
meta → meta|improvement|methodology|optimization
```

Files embed these keywords in comments and docstrings for easy searching.

---

**Tags**: ecommerce, general, implementation

**Palavras-chave**: Dense, Keywords, System

**Origem**: desconhecida


---

### Keywords
*Relevância: 0.31 | Tags: ecommerce, implementation*

# Keywords

**Categoria**: analise_concorrencia
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

market_research → market|size|trends|growth|customer|pain-points
competitors → competitor|analysis|positioning|messaging|gap
keywords → keyword|seo|hierarchy|search-volume|buyer-intent
faq → faq|objection|question|answer|counter
validation → validation|quality|scoring|completeness|error
prompts → prompt|composition|ai-input|instruction|chunk
meta → meta|improvement|methodology|optimization
, dense keywords, dense-keywords-system

each, files

**Tags**: ecommerce, implementation

**Palavras-chave**: Keywords

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---

### Research Workflow: 5 Types
*Relevância: 0.32 | Tags: architectural, ecommerce, general*

# Research Workflow: 5 Types

**Categoria**: analise_concorrencia
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

### 1. Quick Research (45-60 minutes)
- Market research
- Keyword extraction
- Prompt composition
- **Best for**: Fast turnaround needed

### 2. Deep Research (3-4 hours)
- All phases
- Comprehensive analysis
- Full AI prompt composition
- **Best for**: Strategic decisions

### 3. Keywords Only (20-30 minutes)
- Keyword extraction only
- 4-level hierarchy
- Long-tail generation
- **Best for**: SEO optimization

### 4. Competitors (90 minutes)
- Competitive analysis
- Market positioning
- Differentiation strategy
- **Best for**: Competitive moves

### 5. AI-Assisted (15-30 minutes)
- AI-optimized workflow
- Claude-powered analysis
- Fast turnaround
- **Best for**: Quick decisions with AI help

---

**Tags**: architectural, ecommerce, general

**Palavras-chave**: Types, Workflow, Research

**Origem**: desconhecida


---

### 🚀 Quick Start Workflows
*Relevância: 0.32 | Tags: ecommerce, general, intermediate*

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

### Regras de Otimização
*Relevância: 0.31 | Tags: ecommerce, general, intermediate*

# Regras de Otimização

**Categoria**: copywriting
**Qualidade**: 0.71/1.00
**Data**: 20251113

## Conteúdo

- Marca entre 115 e 120 caracteres (densidade máxima de keywords)
- Modelo entre 115 e 120 caracteres (foco absoluto em conversão)
- Títulos ≤ 60 caracteres cada (3 versões A/B)
- ZERO stop words em títulos - apenas keywords que convertem
- Mínimo 8 keywords relevantes por campo
- Keywords são enriquecidas automaticamente com a pesquisa SEO
- Estrutura StoryBrand obrigatória na descrição

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Otimização, Regras

**Origem**: desconhecida


---

### Regras de Otimização
*Relevância: 0.31 | Tags: ecommerce, intermediate*

# Regras de Otimização

**Categoria**: copywriting
**Qualidade**: 0.71/1.00
**Data**: 20251113

## Conteúdo

- Marca entre 115 e 120 caracteres (densidade máxima de keywords)
- Modelo entre 115 e 120 caracteres (foco absoluto em conversão)
- Títulos ≤ 60 caracteres cada (3 versões A/B)
- ZERO stop words em títulos - apenas keywords que convertem
- Mínimo 8 keywords relevantes por campo
- Keywords são enriquecidas automaticamente com a pesquisa SEO
- Estrutura StoryBrand obrigatória na descrição

**Tags**: ecommerce, intermediate

**Palavras-chave**: Regras, Otimização

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---

### Response Format
*Relevância: 0.31 | Tags: ecommerce, concrete*

# Response Format

**Categoria**: copywriting
**Qualidade**: 0.67/1.00
**Data**: 20251113

## Conteúdo

Tipo: JSON Schema

```json
{
  "name": "produto_otimizado_seo",
  "strict": true,
  "schema": {
    "type": "object",
    "properties": {
      "marca_modelo": {
        "type": "object",
        "properties": {
          "marca": {
            "type": "string",
            "minLength": 115,
            "maxLength": 120,
            "description": "Nome da marca otimizado para SEO"
          },
          "modelo": {
            "type": "string",
            "minLength": 115,
            "maxLength": 120,
            "description": "Nome do modelo otimizado para conversão"
          },
          "keywords_utilizadas": {
            "type": "array",
            "items": {"type": "string"},
            "description": "Keywords principais utilizadas na otimização"
          }
        },
        "required": ["marca", "modelo", "keywords_utilizadas"],
        "additionalProperties": false
      },
      "titulos_otimizados": {
        "type": "array",
        "items": {"type": "string", "max

**Tags**: ecommerce, concrete

**Palavras-chave**: Response, Format

**Origem**: _CONSOLIDATED_ecommerce_other.md


---

*... (conteúdo truncado por limite de 1500 tokens)*
---

**Metadados da Injeção:**
- **Versículos injetados**: 199
- **Fonte**: mentor_agent/PROCESSADOS/
- **Última atualização**: 2025-11-14 08:19:53
- **Versão do schema**: 1.0.0

**Referências**: `CAPITULO_analise_03:versiculo_16, CAPITULO_analise_03:versiculo_38, CAPITULO_analise_05:versiculo_22, CAPITULO_analise_05:versiculo_18, CAPITULO_copywriting_04:versiculo_1, CAPITULO_copywriting_04:versiculo_2, CAPITULO_copywriting_04:versiculo_4, CAPITULO_estrategia_01:versiculo_1, CAPITULO_estrategia_01:versiculo_9, CAPITULO_estrategia_01:versiculo_10, CAPITULO_estrategia_02:versiculo_20, CAPITULO_marketplace_03:versiculo_1, CAPITULO_marketplace_03:versiculo_10, CAPITULO_marketplace_03:versiculo_12, CAPITULO_marketplace_04:versiculo_17, CAPITULO_marketplace_04:versiculo_1, CAPITULO_marketplace_04:versiculo_8, CAPITULO_marketplace_05:versiculo_7, CAPITULO_marketplace_05:versiculo_10, CAPITULO_marketplace_05:versiculo_13, CAPITULO_marketplace_06:versiculo_8, CAPITULO_marketplace_06:versiculo_14, CAPITULO_marketplace_06:versiculo_22, CAPITULO_marketplace_07:versiculo_8, CAPITULO_marketplace_07:versiculo_12, CAPITULO_marketplace_07:versiculo_15, CAPITULO_marketplace_08:versiculo_17, CAPITULO_marketplace_08:versiculo_20, CAPITULO_marketplace_08:versiculo_6, CAPITULO_marketplace_09:versiculo_12, CAPITULO_marketplace_09:versiculo_1, CAPITULO_marketplace_09:versiculo_3, CAPITULO_marketplace_10:versiculo_21, CAPITULO_marketplace_10:versiculo_13, CAPITULO_marketplace_10:versiculo_11, CAPITULO_marketplace_11:versiculo_6, CAPITULO_marketplace_11:versiculo_18, CAPITULO_marketplace_11:versiculo_14, CAPITULO_marketplace_12:versiculo_7, CAPITULO_marketplace_12:versiculo_1, CAPITULO_marketplace_12:versiculo_3, CAPITULO_marketplace_13:versiculo_8, CAPITULO_marketplace_13:versiculo_3, CAPITULO_marketplace_13:versiculo_17, CAPITULO_marketplace_14:versiculo_16, CAPITULO_marketplace_14:versiculo_8, CAPITULO_marketplace_14:versiculo_11, CAPITULO_marketplace_15:versiculo_1, CAPITULO_marketplace_15:versiculo_2, CAPITULO_marketplace_15:versiculo_5, CAPITULO_marketplace_16:versiculo_2, CAPITULO_marketplace_16:versiculo_1, CAPITULO_marketplace_16:versiculo_11, CAPITULO_marketplace_17:versiculo_2, CAPITULO_marketplace_17:versiculo_3, CAPITULO_marketplace_17:versiculo_14, CAPITULO_marketplace_18:versiculo_4, CAPITULO_marketplace_18:versiculo_25, CAPITULO_marketplace_18:versiculo_10, CAPITULO_marketplace_19:versiculo_16, CAPITULO_marketplace_19:versiculo_10, CAPITULO_marketplace_19:versiculo_26, CAPITULO_marketplace_20:versiculo_1, CAPITULO_marketplace_20:versiculo_2, CAPITULO_marketplace_20:versiculo_5, CAPITULO_marketplace_21:versiculo_14, CAPITULO_marketplace_21:versiculo_18, CAPITULO_marketplace_21:versiculo_20, CAPITULO_marketplace_22:versiculo_1, CAPITULO_marketplace_22:versiculo_13, CAPITULO_marketplace_22:versiculo_16, CAPITULO_marketplace_23:versiculo_15, CAPITULO_marketplace_23:versiculo_19, CAPITULO_marketplace_23:versiculo_3, CAPITULO_marketplace_24:versiculo_5, CAPITULO_marketplace_24:versiculo_13, CAPITULO_marketplace_24:versiculo_8, CAPITULO_marketplace_25:versiculo_1, CAPITULO_marketplace_25:versiculo_2, CAPITULO_marketplace_25:versiculo_3, CAPITULO_marketplace_26:versiculo_7, CAPITULO_marketplace_26:versiculo_6, CAPITULO_marketplace_26:versiculo_8, CAPITULO_marketplace_27:versiculo_4, CAPITULO_marketplace_27:versiculo_8, CAPITULO_marketplace_27:versiculo_14, CAPITULO_marketplace_28:versiculo_1, CAPITULO_marketplace_28:versiculo_4, CAPITULO_marketplace_28:versiculo_5, CAPITULO_marketplace_29:versiculo_13, CAPITULO_marketplace_29:versiculo_4, CAPITULO_marketplace_29:versiculo_6, CAPITULO_marketplace_30:versiculo_17, CAPITULO_marketplace_30:versiculo_30, CAPITULO_marketplace_30:versiculo_22, CAPITULO_marketplace_31:versiculo_21, CAPITULO_marketplace_31:versiculo_23, CAPITULO_marketplace_31:versiculo_4, CAPITULO_marketplace_32:versiculo_13, CAPITULO_marketplace_32:versiculo_6, CAPITULO_marketplace_32:versiculo_10, CAPITULO_marketplace_33:versiculo_8, CAPITULO_marketplace_33:versiculo_12, CAPITULO_marketplace_33:versiculo_1, CAPITULO_marketplace_34:versiculo_1, CAPITULO_marketplace_34:versiculo_4, CAPITULO_marketplace_34:versiculo_2, CAPITULO_marketplace_35:versiculo_3, CAPITULO_marketplace_35:versiculo_4, CAPITULO_marketplace_35:versiculo_10, CAPITULO_marketplace_36:versiculo_19, CAPITULO_marketplace_36:versiculo_11, CAPITULO_marketplace_36:versiculo_8, CAPITULO_marketplace_37:versiculo_11, CAPITULO_marketplace_37:versiculo_14, CAPITULO_marketplace_37:versiculo_9, CAPITULO_marketplace_38:versiculo_2, CAPITULO_marketplace_38:versiculo_6, CAPITULO_marketplace_38:versiculo_4, CAPITULO_marketplace_39:versiculo_6, CAPITULO_marketplace_39:versiculo_13, CAPITULO_marketplace_39:versiculo_14, CAPITULO_marketplace_40:versiculo_17, CAPITULO_marketplace_40:versiculo_1, CAPITULO_marketplace_40:versiculo_3, CAPITULO_marketplace_41:versiculo_7, CAPITULO_marketplace_41:versiculo_4, CAPITULO_marketplace_41:versiculo_5, CAPITULO_marketplace_42:versiculo_14, CAPITULO_marketplace_42:versiculo_16, CAPITULO_marketplace_42:versiculo_17, CAPITULO_marketplace_43:versiculo_23, CAPITULO_marketplace_43:versiculo_18, CAPITULO_marketplace_43:versiculo_19, CAPITULO_marketplace_44:versiculo_15, CAPITULO_marketplace_44:versiculo_8, CAPITULO_marketplace_44:versiculo_9, CAPITULO_marketplace_45:versiculo_5, CAPITULO_marketplace_45:versiculo_3, CAPITULO_marketplace_45:versiculo_15, CAPITULO_marketplace_46:versiculo_17, CAPITULO_marketplace_46:versiculo_2, CAPITULO_marketplace_46:versiculo_11, CAPITULO_marketplace_47:versiculo_1, CAPITULO_marketplace_47:versiculo_10, CAPITULO_marketplace_47:versiculo_13, CAPITULO_marketplace_48:versiculo_10, CAPITULO_marketplace_48:versiculo_5, CAPITULO_marketplace_48:versiculo_12, CAPITULO_marketplace_49:versiculo_5, CAPITULO_marketplace_49:versiculo_6, CAPITULO_marketplace_49:versiculo_10, CAPITULO_marketplace_50:versiculo_2, CAPITULO_marketplace_50:versiculo_6, CAPITULO_marketplace_50:versiculo_13, CAPITULO_marketplace_51:versiculo_13, CAPITULO_marketplace_51:versiculo_16, CAPITULO_marketplace_51:versiculo_8, CAPITULO_marketplace_52:versiculo_2, CAPITULO_marketplace_52:versiculo_10, CAPITULO_marketplace_52:versiculo_9, CAPITULO_marketplace_53:versiculo_13, CAPITULO_marketplace_53:versiculo_8, CAPITULO_marketplace_53:versiculo_1, CAPITULO_marketplace_54:versiculo_16, CAPITULO_marketplace_54:versiculo_13, CAPITULO_marketplace_54:versiculo_4, CAPITULO_marketplace_55:versiculo_3, CAPITULO_marketplace_55:versiculo_13, CAPITULO_marketplace_55:versiculo_8, CAPITULO_marketplace_56:versiculo_16, CAPITULO_marketplace_56:versiculo_2, CAPITULO_marketplace_56:versiculo_5, CAPITULO_marketplace_57:versiculo_20, CAPITULO_marketplace_57:versiculo_11, CAPITULO_marketplace_57:versiculo_15, CAPITULO_marketplace_58:versiculo_7, CAPITULO_marketplace_58:versiculo_2, CAPITULO_marketplace_58:versiculo_1, CAPITULO_marketplace_59:versiculo_9, CAPITULO_marketplace_59:versiculo_1, CAPITULO_marketplace_59:versiculo_2, CAPITULO_marketplace_60:versiculo_15, CAPITULO_marketplace_60:versiculo_4, CAPITULO_marketplace_60:versiculo_6, CAPITULO_marketplace_61:versiculo_11, CAPITULO_marketplace_61:versiculo_2, CAPITULO_marketplace_61:versiculo_7, CAPITULO_marketplace_62:versiculo_6, CAPITULO_marketplace_62:versiculo_7, CAPITULO_marketplace_62:versiculo_1, CAPITULO_operacoes_23:versiculo_28, CAPITULO_operacoes_39:versiculo_22, CAPITULO_operacoes_40:versiculo_3, CAPITULO_visual_01:versiculo_7, CAPITULO_visual_03:versiculo_29, CAPITULO_visual_04:versiculo_23, CAPITULO_visual_10:versiculo_7, CAPITULO_visual_10:versiculo_8`


