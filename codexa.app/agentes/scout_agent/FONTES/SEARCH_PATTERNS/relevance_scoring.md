# Relevance Scoring Algorithms

**Domain**: Search & Discovery
**Category**: SEARCH_PATTERNS
**Source**: Information Retrieval Theory + CODEXA Implementation
**Quality Score**: 0.88

---

## Resumo Executivo

Relevance scoring determina a qualidade do match entre uma query e um documento. O Scout implementa um sistema multi-fator que combina text matching, category priorities, agent context e recency para produzir scores de 0.0 a 1.0. Este documento detalha os algoritmos e como ajusta-los.

## Conceitos-Chave

### **Multi-Factor Scoring**
Em vez de um unico criterio, combina multiplos sinais com pesos configuraves. Permite ajustar o comportamento para diferentes use cases sem reescrever a logica.

### **Category Priority System**
Nem todos os arquivos tem igual importancia. PRIMEs sao mais importantes que configs. O sistema de prioridade reflete isso:

```
prime:        1.0   # Entry points - always relevant
readme:       0.9   # Documentation
instructions: 0.85  # Operational guides
hop:          0.8   # Prompts (task-specific)
adw:          0.8   # Workflows
config:       0.7   # Configuration files
prompt:       0.7   # Generic prompts
schema:       0.6   # Data schemas
builder:      0.6   # Builder scripts
validator:    0.6   # Validation scripts
```

### **Time Decay Function**
Arquivos recentemente modificados podem ser mais relevantes. Aplica decaimento temporal:

```python
def time_decay(modified_date, half_life_days=30):
    age = (now - modified_date).days
    return 0.5 ** (age / half_life_days)  # Exponential decay
```

### **Fuzzy Matching**
Tolera erros de digitacao e variacoes. Usa algoritmos como Levenshtein distance ou ratio-based matching para score parcial.

## Como Aplicar

1. **Configurar pesos base**
   ```json
   {
     "text_match": 0.40,
     "category_priority": 0.20,
     "agent_match": 0.25,
     "recency": 0.15
   }
   ```

2. **Implementar cada componente**
   ```python
   class RelevanceScorer:
       def __init__(self, weights):
           self.weights = weights

       def score(self, query, doc, context):
           scores = {
               'text_match': self.fuzzy_match(query, doc),
               'category_priority': self.category_weight(doc),
               'agent_match': self.agent_relevance(doc, context),
               'recency': self.time_score(doc)
           }
           return sum(self.weights[k] * scores[k] for k in scores)

       def fuzzy_match(self, query, doc):
           # Combine path + tags matching
           path_score = fuzz.partial_ratio(query, doc.path) / 100
           tag_score = max(fuzz.ratio(query, t) for t in doc.tags) / 100
           return max(path_score, tag_score)

       def category_weight(self, doc):
           return CATEGORY_PRIORITIES.get(doc.category, 0.5)

       def agent_relevance(self, doc, context):
           if not context.agent:
               return 0.5  # Neutral
           return 1.0 if doc.agent == context.agent else 0.3

       def time_score(self, doc):
           age_days = (datetime.now() - doc.modified).days
           return max(0.1, 1.0 - (age_days / 365))  # Linear decay over year
   ```

3. **Definir thresholds de acao**
   ```python
   THRESHOLDS = {
       'include': 0.3,    # Minimum to include in results
       'confident': 0.7,  # High confidence match
       'exact': 0.95      # Near-exact match
   }
   ```

4. **Ordenar e limitar resultados**
   ```python
   results = sorted(matches, key=lambda x: x.score, reverse=True)
   return results[:max_results]
   ```

## Exemplos Praticos

### Exemplo 1: Query Especifica de Agente

**Query**: "title generation"
**Context**: agent="anuncio_agent"

**Scoring**:
| File | Text | Category | Agent | Recency | Total |
|------|------|----------|-------|---------|-------|
| 14_title_HOP.md | 0.90 | 0.80 | 1.00 | 0.95 | 0.91 |
| PRIME.md | 0.30 | 1.00 | 1.00 | 0.90 | 0.62 |
| config/rules.json | 0.20 | 0.70 | 1.00 | 0.80 | 0.52 |

**Resultado**: title_HOP.md retornado primeiro (0.91)

### Exemplo 2: Query Generica

**Query**: "how to create agent"
**Context**: (sem agente especifico)

**Scoring**:
| File | Text | Category | Agent | Recency | Total |
|------|------|----------|-------|---------|-------|
| codexa_agent/PRIME.md | 0.85 | 1.00 | 0.50 | 0.90 | 0.77 |
| 91_meta_build_agent_HOP.md | 0.95 | 0.80 | 0.50 | 0.95 | 0.79 |
| iso_vectorstore/23_subagent_patterns.md | 0.80 | 0.60 | 0.50 | 0.85 | 0.67 |

**Resultado**: HOP de construcao rankeado mais alto por text match

## Quando Usar

- **USE multi-factor scoring quando**:
  - Multiplos sinais de relevancia disponiveis
  - Contexto do usuario e conhecido (agente atual)
  - Balanco entre precisao e recall necessario

- **USE single-factor quando**:
  - Busca simples por glob pattern
  - Exact match necessario (API lookup)
  - Performance e critica (skip computation)

- **AJUSTE pesos quando**:
  - Resultados nao refletem expectativas do usuario
  - Novo tipo de arquivo adicionado
  - Novo agente com patterns diferentes

## Relacionado

- Ver tambem: `semantic_search.md`
- Ver tambem: `indexing_strategies.md`
- Config: `scout_agent/config/relevance_weights.json`

---

**Processado**: 2025-12-05
**Tokens**: ~950
