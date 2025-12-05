# Semantic Search Patterns

**Domain**: Search & Discovery
**Category**: SEARCH_PATTERNS
**Source**: Industry best practices + CODEXA implementation
**Quality Score**: 0.85

---

## Resumo Executivo

Semantic search vai alem da correspondencia exata de palavras-chave, utilizando embeddings vetoriais para encontrar documentos conceitualmente relacionados. Este conhecimento cobre os principais algoritmos, implementacoes e trade-offs para sistemas de busca em codebases.

## Conceitos-Chave

### **Embedding-Based Search**
Transforma texto em vetores de alta dimensao onde documentos semanticamente similares ficam proximos no espaco vetorial. Ideal para queries em linguagem natural como "como criar um agente" que deve encontrar documentos sobre agent construction mesmo sem a palavra exata.

### **Keyword + Semantic Hybrid**
Combina BM25 (keyword matching) com embeddings para capturar tanto relevancia lexica quanto semantica. O Scout usa este approach: fuzzy match (40%) + category priority (20%) + agent match (25%) + recency (15%).

### **Dense vs Sparse Retrieval**
- **Dense**: Embeddings (OpenAI, Sentence Transformers) - melhor para semantica
- **Sparse**: TF-IDF, BM25 - melhor para keywords especificas
- **Hybrid**: Combinacao de ambos - melhor resultado geral

### **Re-ranking**
Apos busca inicial, aplica modelo mais sofisticado para reordenar top-K resultados. Util quando custo computacional de embeddings e alto para todo o corpus.

## Como Aplicar

1. **Escolher estrategia baseado no caso de uso**
   - Codebase navigation: Hybrid (keyword + semantic)
   - Documentation search: Dense embeddings
   - API reference: Sparse (exact match matters)

2. **Implementar scoring multi-fator**
   ```python
   def compute_relevance(query, doc, context):
       keyword_score = fuzzy_match(query, doc.path + doc.tags)  # 40%
       category_score = CATEGORY_WEIGHTS[doc.category]          # 20%
       agent_score = 1.0 if doc.agent == context.agent else 0.5 # 25%
       recency_score = time_decay(doc.modified_date)            # 15%

       return (0.4 * keyword_score +
               0.2 * category_score +
               0.25 * agent_score +
               0.15 * recency_score)
   ```

3. **Definir thresholds de relevancia**
   - Score >= 0.8: High confidence match
   - Score 0.5-0.8: Medium confidence, include in results
   - Score < 0.5: Low confidence, exclude or warn

4. **Indexar metadata alem do conteudo**
   - File path (weighted high)
   - Tags and categories
   - Cross-references
   - Last modified date

## Exemplos Praticos

### Exemplo 1: Query de Linguagem Natural

**Query**: "como gerar titulo para produto"

**Antes** (keyword only):
- Retorna apenas arquivos com "titulo" e "produto" literais
- Perde `anuncio_agent/prompts/14_title_HOP.md`

**Depois** (semantic):
- Entende que "gerar titulo" == "title generation"
- Encontra HOPs relevantes mesmo em ingles
- Score: 0.95 para title_HOP.md

**Resultado**: 3x mais documentos relevantes encontrados

### Exemplo 2: Agent Context Discovery

**Query**: `agent_context("pesquisa_agent")`

**Processo**:
1. Load all files tagged with agent="pesquisa_agent"
2. Include dependencies (marca_agent referenced)
3. Sort by category priority (PRIME > README > HOPs)
4. Return structured response

**Resultado**: 45 arquivos em <50ms

## Quando Usar

- **USE semantic search quando**:
  - Usuario faz query em linguagem natural
  - Conceito pode ter multiplos sinonimos
  - Busca cross-lingual (PT-BR <-> EN)
  - Exploratory search ("o que existe sobre X")

- **USE keyword match quando**:
  - Busca por path exato ou glob pattern
  - Nome de funcao/variavel especifico
  - Pattern matching estrutural (`**/*_HOP.md`)

- **USE hybrid quando**:
  - Caso geral de navegacao de codebase
  - Balanco entre precisao e recall
  - Sistema de producao (Scout default)

## Relacionado

- Ver tambem: `relevance_scoring.md`
- Ver tambem: `indexing_strategies.md`
- Implementacao: `scout_agent/PRIME.md` secao 6 (Relevance Scoring)

---

**Processado**: 2025-12-05
**Tokens**: ~850
