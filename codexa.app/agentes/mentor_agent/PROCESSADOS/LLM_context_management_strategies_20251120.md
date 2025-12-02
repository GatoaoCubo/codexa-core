# Context Management: Maximizando o Window Limit de LLMs

**Categoria**: llm_optimization
**Qualidade**: 0.90/1.00
**Data**: 20251120

## Conteúdo

### O Problema do Context Window (A Parede Invisível)

**Realidade dura**: Todo LLM tem limite de tokens que processa por request. Exceder esse limite = perda de informação ou erro.

- Claude Sonnet 4: ~200k tokens (~150k palavras)
- GPT-4 Turbo: ~128k tokens (~96k palavras)
- [OPEN_VARIABLE: modelo_alternativo]: ~[OPEN_VARIABLE: limite_tokens] tokens

**Analogia**: Imagine um humano que só consegue lembrar dos últimos 10 minutos de conversa. Informação antes disso simplesmente desaparece. LLMs têm problema similar, só que medido em tokens.

**Por que isso importa**: Em workflows complexos (multi-agent, sessões longas, documentação extensa), você SEMPRE bate no limite se não gerenciar contexto proativamente.

### As 4 Estratégias Fundamentais

#### **Estratégia 1: Compression (Comprimir sem Perder Essência)**

**Princípio**: Transmitir máxima informação com mínimo de tokens.

**Técnicas**:

1. **Summarization Agressiva**
```
ORIGINAL (2000 tokens):
[Documento técnico completo de 15 páginas]

COMPRESSED (300 tokens):
[Bullet points com apenas fatos essenciais + estrutura key-value]

Example:
{
  "produto": "Notebook Dell Inspiron 15",
  "specs_critical": ["i7-12700H", "16GB RAM", "512GB SSD"],
  "target_audience": "Profissionais remotos 25-45 anos",
  "price_range": "R$ 3500-4200",
  "differentiators": ["Garantia 3 anos", "Suporte 24/7 Brasil"]
}
```

**Ganho**: 85% redução de tokens mantendo 95%+ da informação acionável.

2. **Eliminate Redundancy**
```
❌ RUIM (redundante):
"O produto é uma cadeira gamer. Esta cadeira gamer possui apoio lombar.
O apoio lombar da cadeira gamer é ajustável. A cadeira gamer com apoio
lombar ajustável é ideal para gamers."

✅ BOM (conciso):
"Cadeira gamer: apoio lombar ajustável, ideal para sessões longas."
```

**Ganho**: 70% redução de tokens, zero perda de informação.

3. **Structured Data over Natural Language**
```
❌ RUIM (verbose):
"O cliente João Silva, email joao@email.com, telefone 11-99999-9999,
comprou o produto X por R$ 299 no dia 15 de novembro de 2024."

✅ BOM (estruturado):
```json
{"cliente": "João Silva", "email": "joao@email.com", "tel": "11-99999-9999",
 "produto": "X", "valor": 299, "data": "2024-11-15"}
```

**Ganho**: 40% redução de tokens + mais fácil de parsear.

#### **Estratégia 2: Chunking (Dividir e Conquistar)**

**Princípio**: Quebrar tarefas grandes em subtasks menores, cada uma com context window próprio.

**Pattern: Sequential Chunking**
```
Tarefa grande: Analisar 50 páginas de pesquisa de mercado

Chunk 1 (páginas 1-10) → LLM gera: [SUMMARY_1]
Chunk 2 (páginas 11-20) → LLM gera: [SUMMARY_2]
Chunk 3 (páginas 21-30) → LLM gera: [SUMMARY_3]
Chunk 4 (páginas 31-40) → LLM gera: [SUMMARY_4]
Chunk 5 (páginas 41-50) → LLM gera: [SUMMARY_5]

Final aggregation:
Input: [SUMMARY_1] + [SUMMARY_2] + [SUMMARY_3] + [SUMMARY_4] + [SUMMARY_5]
→ LLM gera: [CONSOLIDATED_REPORT]
```

**Vantagem**: Processa informação ilimitada, latency linear (não exponencial).

**Pattern: Hierarchical Chunking**
```
Level 1: Chunk em seções temáticas
Section A → [SUMMARY_A]
Section B → [SUMMARY_B]
Section C → [SUMMARY_C]

Level 2: Agregar summaries
[SUMMARY_A] + [SUMMARY_B] + [SUMMARY_C] → [MEGA_SUMMARY]

Level 3 (se necessário): Refinar
[MEGA_SUMMARY] + specific_question → [FINAL_ANSWER]
```

**Exemplo CODEXA (Pesquisa Agent)**:
```
User: "Pesquise mercado para notebook gaming"

Chunking strategy:
1. Chunk concorrentes Mercado Livre → [REPORT_ML]
2. Chunk concorrentes Shopee → [REPORT_SHOPEE]
3. Chunk keywords Google Trends → [REPORT_KEYWORDS]
4. Chunk pricing analysis → [REPORT_PRICING]

Aggregation:
[REPORT_ML] + [REPORT_SHOPEE] + [REPORT_KEYWORDS] + [REPORT_PRICING]
→ [CONSOLIDATED_MARKET_RESEARCH]
```

#### **Estratégia 3: Selective Loading (Carregar Apenas o Necessário)**

**Princípio**: Não carregue TUDO no contexto. Carregue apenas o que é relevante para a tarefa ATUAL.

**Anti-Pattern**:
```python
# RUIM: Carrega 20 arquivos de conhecimento sempre
context = ""
for file in iso_vectorstore:
    context += read_file(file)  # 200k tokens!

llm_call(prompt + context)  # BOOM! Context overflow
```

**Pattern Correto: Discovery-First**:
```python
# BOM: Busca semântica para carregar apenas relevante
query = extract_query_from_user_input(user_message)
relevant_files = semantic_search(query, iso_vectorstore, top_k=3)

context = ""
for file in relevant_files:  # Apenas 3 arquivos mais relevantes
    context += read_file(file)  # ~20k tokens

llm_call(prompt + context)  # ✅ Within limits
```

**Exemplo CODEXA (Mentor Agent)**:
```
User: "Como otimizar títulos no Mercado Livre?"

Semantic search em catalogo.json:
Query: "otimizar títulos mercado livre"
→ Match 1: marketplace_titulos_seo_20251113.md (score: 0.92)
→ Match 2: marketplace_keywords_strategy_20251108.md (score: 0.85)
→ Match 3: copywriting_seo_fundamentals_20251015.md (score: 0.78)

Load ONLY these 3 files (not all 100+ files in PROCESSADOS/)
→ Context: ~15k tokens
→ Room left for: prompt (5k) + conversation history (10k) + output (10k) ✅
```

**Tools for Semantic Search**:
- [OPEN_VARIABLE: embedding_model] (ex: text-embedding-ada-002, voyage-2)
- [OPEN_VARIABLE: vector_db] (ex: Chroma, Pinecone, FAISS local)

#### **Estratégia 4: Context Rotation (Girar Contexto Conforme Necessidade)**

**Princípio**: Em sessões longas, "esqueça" partes antigas do contexto para dar espaço ao novo.

**Pattern: Sliding Window**
```
Conversation com 20 mensagens:

Tokens por mensagem média: 500
Total: 20 × 500 = 10,000 tokens

Se context limit é 50k:
- Últimas 15 mensagens: KEEP (7,500 tokens)
- Mensagens 1-5: DROP (economiza 2,500 tokens)

Summary das mensagens dropadas:
"Conversa inicial sobre pesquisa de produto X, decidiu focar em nicho Y."
(50 tokens)

Total context: 7,500 + 50 + prompt + knowledge = ~20k ✅
```

**Pattern: Importance-Based Retention**
```python
def should_keep_message(msg, current_turn):
    # Sempre mantém últimas 10 mensagens
    if (current_turn - msg.turn) <= 10:
        return True

    # Mantém mensagens marcadas como "important"
    if msg.metadata.get("important"):
        return True

    # Mantém se foi mencionada recentemente
    if msg.id in recent_references:
        return True

    # Caso contrário, drop e summarize
    return False
```

**Exemplo CODEXA (Long Sessions)**:
```
User está em sessão de 2h usando Anuncio Agent, gerou 30 anúncios.

Turn 1-10: Aprendendo preferências do usuário
Turn 11-20: Iterando em anúncios específicos
Turn 21-30: Refinamento final

Na Turn 25:
- Context: Turns 15-25 (últimas 10) + SUMMARY(Turns 1-14)
- Summary: "User preferência: tom formal, foco B2B, keywords long-tail priority"
- Total tokens: 8k (messages) + 200 (summary) + 10k (knowledge) = 18k ✅
```

### Métricas para Monitorar Context Usage

**Dashboard essencial**:
```
Current context size: [X] / [LIMIT] tokens ([Y]% usage)

Breakdown:
- System prompt: 2,500 tokens (5%)
- Conversation history: 12,000 tokens (24%)
- Knowledge files: 15,000 tokens (30%)
- User input: 1,000 tokens (2%)
- Buffer for output: 19,500 tokens (39%)

Status: ✅ HEALTHY (within limits with margin)
```

**Red flags**:
- 🔴 Context usage >90% (risco de truncation)
- 🟡 Context usage 70-90% (planejar compression)
- 🟢 Context usage <70% (healthy)

### Advanced Patterns

**Pattern: Context Caching** (quando disponível)
```
Alguns LLMs (ex: Claude) permitem cachear partes do contexto:

CACHED (billed once):
- System prompt (2k tokens)
- Knowledge base files (15k tokens)

NOT CACHED (billed every call):
- Conversation history (8k tokens)
- User input (1k tokens)

Cost savings: ~40-60% em sessões longas
```

**Pattern: Dynamic Context Assembly**
```python
def assemble_context(user_query, session_history, max_tokens=50000):
    context_budget = max_tokens
    context_parts = []

    # 1. Always include: System prompt (highest priority)
    system_prompt = load_system_prompt()  # 2k tokens
    context_parts.append(system_prompt)
    context_budget -= len_tokens(system_prompt)

    # 2. Include: Relevant knowledge (semantic search)
    knowledge = semantic_search(user_query, top_k=3)  # ~15k tokens
    context_parts.append(knowledge)
    context_budget -= len_tokens(knowledge)

    # 3. Include: Recent history (sliding window)
    history_budget = context_budget * 0.4  # Reserve 40% for history
    recent_history = get_recent_messages(session_history, token_limit=history_budget)
    context_parts.append(recent_history)
    context_budget -= len_tokens(recent_history)

    # 4. Reserve: Output space (minimum 20% of total)
    output_space = max_tokens * 0.2
    if context_budget < output_space:
        # Trim history to make room for output
        recent_history = trim_to_fit(recent_history, context_budget - output_space)

    return "".join(context_parts)
```

### Troubleshooting Context Issues

**Sintoma**: "LLM parece "esquecer" informações que eu dei antes"
**Causa provável**: Context window excedido, mensagens antigas foram truncadas
**Fix**: Implement sliding window + summarization das partes antigas

**Sintoma**: "Outputs ficaram genéricos, sem personalizacão"
**Causa provável**: Knowledge base não foi carregado (selective loading falhou)
**Fix**: Debug semantic search, verificar se embeddings estão corretos

**Sintoma**: "Latência aumentou 5x após 20 mensagens"
**Causa provável**: Context crescendo linearmente sem compressão
**Fix**: Implement context rotation, limite histórico a últimas N messages

**Sintoma**: "LLM mistura informação de contextos diferentes"
**Causa provável**: Context pollution (informação não-relevante no contexto)
**Fix**: More aggressive selective loading, clear context boundaries

### Best Practices CODEXA

1. **iso_vectorstore**: 20 arquivos, cada ~5-10k tokens
   - Total: ~100-200k tokens potencial
   - Selective load: 3-5 arquivos por query (~15-50k tokens real)

2. **Conversation history**: Sliding window de 10-15 mensagens
   - Summarize mensagens antigas (1-9) em ~200 tokens
   - Keep mensagens recentes (10-15) completas

3. **System prompts**: Compactos e modulares
   - Main prompt: ~2-3k tokens
   - Task-specific additions: +1-2k tokens
   - Total system: <5k tokens

4. **Output buffer**: Reserve 20-30% do context window
   - Se limit é 200k tokens, use no máximo 140k para input
   - Reserve 60k para output (evita truncation)

---

**Tags**: context-management, context-window, optimization, llm, compression, chunking
**Palavras-chave**: Context management, window limit, compression, chunking, selective loading
**Origem**: curso_agent/PRIME.md + mentor_agent/PRIME.md (discovery-first pattern)
**Processado**: 20251120
