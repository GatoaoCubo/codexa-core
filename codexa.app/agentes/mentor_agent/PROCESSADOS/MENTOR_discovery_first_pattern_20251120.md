# Discovery-First Pattern: Nunca Responda Antes de Buscar

**Categoria**: mentor_patterns
**Qualidade**: 0.90/1.00
**Data**: 20251120

## Conteúdo

### O Anti-Pattern Mais Comum em Sistemas LLM

**Approach ingênuo (falha 40% das vezes)**:
```
User: "Como otimizar títulos no Mercado Livre?"

LLM (sem buscar conhecimento):
"Para otimizar títulos no ML, use keywords relevantes,
mantenha entre 50-60 caracteres, e inclua especificações do produto."
```

**Problema**: Resposta genérica, sem profundidade, poderia ser gerada por qualquer LLM sem conhecimento especializado.

**Discovery-First approach (sucesso 90% das vezes)**:
```
User: "Como otimizar títulos no Mercado Livre?"

STEP 1: Search knowledge base
Query: "otimizar títulos mercado livre"
Results:
- marketplace_titulos_seo_20251113.md (score: 0.92)
- marketplace_keywords_strategy_20251108.md (score: 0.85)
- copywriting_seo_fundamentals_20251015.md (score: 0.78)

STEP 2: Load top 3 files into context

STEP 3: Synthesize response using specific knowledge
"Para otimizar títulos no ML, siga esta estratégia testada:

1. Keywords prioritários nos primeiros 20 caracteres (algoritmo ML
   dá peso maior ao início)
2. Estrutura: [KEYWORD_PRIMARIA] [ESPECIFICACAO] [DIFERENCIAL]
3. Limite: 60 chars no desktop, 55 no mobile (corte visual)
4. Evite: artigos, preposições, caracteres especiais (conta como char
   mas não ajuda SEO)

Exemplo real:
❌ 'Linda Camiseta Masculina da Marca X'
✅ 'Camiseta Masculina Algodão Egipcio Marca X P-GG'

Resultado: +45% CTR médio após otimização"
```

**Diferença**: Resposta específica, acionável, com exemplos reais e métricas, baseada em conhecimento especializado do sistema.

### O Pillar #1 do Mentor Agent (CODEXA)

**Discovery-First**: Princípio fundacional do mentor_agent.

**Filosofia**:
> "Never answer blindly - always search catalogo.json first"

**Por que isso funciona**:

1. **Retrieval beats generation**: LLMs são bons em sintetizar informação existente, ruins em gerar conhecimento especializado do zero.

2. **Factualidade**: Baseando resposta em documentos específicos reduz alucinação de 15-20% para 2-3%.

3. **Specialization**: Sistema tem conhecimento que LLM base não tem (ex: compliance ANVISA específico, estratégias de precificação para marketplaces BR).

4. **Traceability**: Usuário pode verificar fonte ("De acordo com marketplace_titulos_seo_20251113.md...")

5. **Maintainability**: Atualizar conhecimento = adicionar novo doc, não re-treinar modelo.

### Arquitetura Discovery-First do CODEXA

**4-Stage Pipeline**:

**STAGE 1: Semantic Search**
```python
def answer_question(user_question):
    # 1. Search catalog
    results = search_catalog(
        query=user_question,
        fields=["categoria", "assunto", "tags", "aplicacao"],
        top_k=3
    )

    # Returns:
    # [
    #   {"arquivo": "marketplace_titulos_seo.md", "score": 0.92},
    #   {"arquivo": "copywriting_keywords.md", "score": 0.85},
    #   {"arquivo": "seo_fundamentals.md", "score": 0.78}
    # ]
```

**STAGE 2: Context Loading**
```python
    # 2. Read relevant files
    knowledge = []
    for result in results[:3]:  # Top 3 matches
        content = read_file(f"PROCESSADOS/{result['arquivo']}")
        knowledge.append(content)

    # Total: ~15-20k tokens (3 files @ 5-7k each)
```

**STAGE 3: Synthesis**
```python
    # 3. Synthesize + translate to seller language
    prompt = f"""
    Você é um mentor experiente para sellers brasileiros.

    Responda esta pergunta usando APENAS o conhecimento fornecido:

    Pergunta: {user_question}

    Conhecimento:
    {knowledge}

    Instruções:
    - Seja específico (números, exemplos, métricas)
    - Use linguagem prática (não acadêmica)
    - Cite de qual arquivo veio cada informação
    - Se conhecimento não cobre pergunta, diga explicitamente

    Resposta:
    """

    answer = llm_call(prompt)
```

**STAGE 4: Delivery**
```python
    # 4. Return synthesized answer
    return {
        "answer": answer,
        "sources": [r["arquivo"] for r in results[:3]],
        "confidence": results[0]["score"]
    }
```

### Multi-Dimensional Matching (Além de Semantic Search)

**Challenge**: Semantic search captura similaridade textual, mas não contexto de aplicação.

**Example**:
```
Query: "Como precificar produto?"

Semantic matches:
1. pricing_strategies_general.md (score: 0.90)
2. marketplace_pricing_ml.md (score: 0.85)
3. psychology_pricing.md (score: 0.82)

Problem: User quer especificamente para Mercado Livre.
Semantic search não capturou contexto "Mercado Livre".
```

**Solution: Multi-dimensional matching**
```python
def multi_dimensional_search(query, context_hints):
    # Dimension 1: Semantic similarity (text embedding)
    semantic_results = semantic_search(query, top_k=10)

    # Dimension 2: Category match
    if "marketplace" in context_hints:
        semantic_results = filter_by_category(
            semantic_results,
            category="marketplace_optimization"
        )

    # Dimension 3: Tags match
    if "mercadolivre" in query.lower():
        semantic_results = boost_by_tag(
            semantic_results,
            tag="mercadolivre",
            boost=1.5  # Increase score by 50%
        )

    # Dimension 4: Application context
    if detect_intent(query) == "when_pricing_products":
        semantic_results = boost_by_aplicacao(
            semantic_results,
            aplicacao="quando_precificar",
            boost=1.3
        )

    # Dimension 5: Recency (optional)
    # Newer docs get slight boost
    semantic_results = apply_recency_boost(semantic_results, decay=0.95)

    # Final ranking
    return rank_and_return_top_k(semantic_results, k=3)
```

**Result**: More contextually relevant docs, even if semantic similarity is slightly lower.

### The catalogo.json Structure (CODEXA Standard)

**Schema**:
```json
{
  "arquivos": [
    {
      "arquivo": "marketplace_titulos_otimizacao_20251113.md",
      "categoria": "marketplace_optimization",
      "assunto": "títulos_seo",
      "tags": ["mercadolivre", "seo", "conversão"],
      "nivel": "intermediário",
      "aplicacao": "quando_criar_anuncios",
      "criado": "2025-11-13",
      "fonte_original": "RASCUNHO/guia_ml.pdf",
      "quality_score": 0.87,
      "embedding": [0.023, -0.145, 0.678, ...],  // 1536-dim vector
      "token_count": 2847
    },
    // ... 100+ more files
  ],
  "categorias": [
    "marketplace_optimization",
    "copywriting",
    "estrategia_produto",
    "analise_concorrencia",
    "compliance_legal",
    "branding",
    // ... etc
  ],
  "metadata": {
    "total_arquivos": 107,
    "ultima_atualizacao": "2025-11-20",
    "embedding_model": "text-embedding-ada-002"
  }
}
```

**Fields explanation**:

- **arquivo**: Filename (structured: `{categoria}_{assunto}_{date}.md`)
- **categoria**: Primary classification (1 of 10 standard categories)
- **assunto**: Specific topic within category
- **tags**: Cross-cutting themes (array, for multi-tag search)
- **nivel**: Difficulty (básico, intermediário, avançado)
- **aplicacao**: When to use (context trigger)
- **quality_score**: 0.75-1.0 (5-dimension validation score)
- **embedding**: Vector representation for semantic search
- **token_count**: For context budgeting

### When Discovery-First vs Direct Generation

**Use Discovery-First when**:
✅ Question is about specialized domain knowledge
✅ Factual accuracy is critical
✅ You have curated knowledge base
✅ Traceability/citations matter

**Use Direct Generation when**:
✅ General knowledge questions (LLM base knowledge sufficient)
✅ Creative tasks (write poem, brainstorm ideas)
✅ No relevant docs in knowledge base
✅ Latency is critical (<2s requirement)

**Example decision tree**:
```
User: "Qual a capital do Brasil?"
→ Direct (general knowledge, LLM knows this)

User: "Como calcular ICMS para venda interestadual no ML?"
→ Discovery-First (specialized, nuanced, needs docs)

User: "Me ajude a criar um slogan criativo"
→ Direct (creative task, retrieval não ajuda)

User: "Quais são as regras de compliance ANVISA para cosméticos?"
→ Discovery-First (factual, regulatory, needs specific docs)
```

### Implementation Patterns

**Pattern 1: Hybrid (Try discovery, fallback to generation)**
```python
def answer_hybrid(question):
    # 1. Try discovery-first
    results = search_catalog(question, top_k=3)

    if results[0]["score"] > 0.75:  # High confidence match
        return answer_from_knowledge(question, results)
    else:  # Low confidence, no good match
        return direct_generation(question) + \
               " (Nota: Baseado em conhecimento geral, não em docs específicos)"
```

**Pattern 2: Multi-hop (Chain discoveries)**
```python
def answer_complex_question(question):
    # Question: "Como criar anúncio ML para suplementos?"

    # Discovery 1: What are suplementos compliance rules?
    compliance_docs = search_catalog("compliance ANVISA suplementos")

    # Discovery 2: What are ML SEO best practices?
    seo_docs = search_catalog("otimização títulos mercado livre")

    # Combine both
    combined_knowledge = load_docs(compliance_docs + seo_docs)

    # Synthesize integrated answer
    return llm_call(f"""
    Create ML ad for supplement product.

    Rules from compliance docs:
    {compliance_docs}

    SEO best practices from ML docs:
    {seo_docs}

    Combine both to create compliant + optimized ad.
    """)
```

**Pattern 3: Iterative refinement**
```python
def answer_with_refinement(question):
    # 1. Initial discovery
    initial_docs = search_catalog(question, top_k=3)
    initial_answer = synthesize(question, initial_docs)

    # 2. Evaluate quality
    quality = evaluate_answer_quality(initial_answer)

    if quality < 0.80:
        # 3. Expand search (try different query formulation)
        expanded_query = reformulate_query(question)
        additional_docs = search_catalog(expanded_query, top_k=2)

        # 4. Re-synthesize with expanded knowledge
        all_docs = initial_docs + additional_docs
        refined_answer = synthesize(question, all_docs)

        return refined_answer
    else:
        return initial_answer
```

### Metrics & Monitoring

**Track these metrics**:
```
Discovery effectiveness:
- Search hit rate: % queries with score >0.75 (target: >85%)
- Average top-1 score: Mean confidence of best match (target: >0.80)
- Coverage: % queries with ≥1 relevant doc (target: >90%)

Answer quality:
- Factual accuracy: % answers factually correct (target: >95%)
- Citation rate: % answers that cite source docs (target: 100%)
- User satisfaction: Thumbs up/down (target: >85% positive)

Performance:
- Search latency: p95 time to find docs (target: <500ms)
- Total latency: p95 end-to-end (target: <3s)
- Context overflow rate: % times docs exceed budget (target: <5%)
```

### Best Practices

**DO**:
- ✅ Always search before answering (even if you "think" you know)
- ✅ Load top 3-5 docs, not just top 1 (single doc may be incomplete)
- ✅ Cite source docs in answer ("According to marketplace_seo.md...")
- ✅ Explicitly say when knowledge base doesn't cover topic

**DON'T**:
- ❌ Mix discovered knowledge with LLM's base knowledge (confuses sources)
- ❌ Hallucinate when no good matches found (say "I don't have specific info")
- ❌ Overload context with all matches (selective loading, top-K only)
- ❌ Skip search for "obvious" questions (obvious to LLM ≠ accurate for domain)

### Evolution Path: From Discovery-First to Agentic RAG

**Current: Discovery-First (Static Retrieval)**
```
Query → Search → Load → Synthesize → Answer
```

**Next: Agentic RAG (Dynamic Tool Use)**
```
Query → Agent decides:
  - Should I search knowledge base?
  - Should I search web?
  - Should I run calculation?
  - Should I ask clarifying question?

Agent chains tools dynamically based on question complexity.
```

**Future: Self-Improving Discovery**
```
System tracks:
- Which docs were most useful for which questions
- Which queries had poor matches (knowledge gaps)
- User feedback on answer quality

System automatically:
- Re-indexes with better embeddings
- Requests new docs for gap areas
- A/B tests query reformulation strategies
```

---

**Tags**: discovery-first, rag, search, knowledge-base, mentor-pattern, retrieval
**Palavras-chave**: Discovery-first, RAG, search, catalogo.json, retrieval, knowledge base
**Origem**: mentor_agent/PRIME.md (Pillar #1) + implementation analysis
**Processado**: 20251120
