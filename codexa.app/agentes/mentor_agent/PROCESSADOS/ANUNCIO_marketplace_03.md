# LIVRO: Marketplace
## CAPÍTULO 3

**Versículos consolidados**: 17
**Linhas totais**: 1182
**Gerado em**: 2025-11-13 18:45:49

---


<!-- VERSÍCULO 1/17 - marketplace_optimization_4_agente_1_research_notes_20251113.md (202 linhas) -->

# 4. AGENTE 1: RESEARCH NOTES

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### 4.1 Objetivos e Responsabilidades

**Objetivo Principal:**
Coletar, analisar e sintetizar informações de mercado para informar as próximas etapas de criação do anúncio.

**Responsabilidades:**
1. ✅ Validar completude do brief
2. ✅ Gerar keywords estratégicas (head terms + longtails)
3. ✅ Pesquisar concorrentes em marketplaces
4. ✅ Analisar conteúdo social e UGC
5. ✅ Identificar padrões de sucesso
6. ✅ Mapear risks e compliance
7. ✅ Documentar gaps e oportunidades
8. ✅ Fornecer recomendações iniciais

**NÃO é responsabilidade:**
- ❌ Escrever copy final
- ❌ Criar CTAs
- ❌ Gerar imagens
- ❌ Tomar decisões de tom/voz (apenas recomenda)

### 4.2 Metodologia de Pesquisa Detalhada

#### Fase 1: Intake e Validação

**Input Mínimo Requerido:**
```yaml
produto:
  nome: string [obrigatório]
  categoria: string [obrigatório]
  descricao_breve: string [obrigatório]

marca:
  nome: string [obrigatório]
  valores: array<string> [opcional]
  tom_voz: string [opcional]

publico:
  demografico: object [opcional]
  psicografico: object [opcional]
  dores: array<string> [recomendado]

marketplace:
  plataformas: array<string> [obrigatório]
  
referencias:
  imagens: array<url> [opcional]
  anuncios_inspiracao: array<url> [opcional]
```

**Checklist de Validação:**
```python
def validate_brief(brief):
    errors = []
    warnings = []
    
    # Obrigatórios
    required = ['produto.nome', 'produto.categoria', 'marca.nome', 'marketplace.plataformas']
    for field in required:
        if not get_nested(brief, field):
            errors.append(f"Campo obrigatório ausente: {field}")
    
    # Recomendados
    recommended = ['produto.descricao_breve', 'publico.dores']
    for field in recommended:
        if not get_nested(brief, field):
            warnings.append(f"Campo recomendado ausente: {field}")
    
    # Qualidade
    if brief.get('produto', {}).get('descricao_breve', ''):
        desc = brief['produto']['descricao_breve']
        if len(desc.split()) < 10:
            warnings.append("Descrição breve muito curta (< 10 palavras)")
    
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings
    }
```

#### Fase 2: Geração de Head Terms

**Metodologia:**

1. **Extração de Termos Base**
```python
def extract_base_terms(product_name, description):
    """
    Extrai termos candidatos do nome e descrição
    """
    # Tokenização
    tokens = tokenize(product_name + " " + description)
    
    # Remove stopwords
    tokens = [t for t in tokens if t not in STOPWORDS_PT]
    
    # POS tagging - mantém apenas substantivos, adjetivos
    tokens = [t for t, pos in pos_tag(tokens) if pos in ['NOUN', 'ADJ']]
    
    # Normalização
    tokens = [lemmatize(t) for t in tokens]
    
    return tokens

# Exemplo
product = "Mochila Executiva Couro Genuíno com Compartimento Notebook"
description = "Mochila de couro para profissionais, com espaço para laptop 15 polegadas"

base_terms = extract_base_terms(product, description)
# ['mochila', 'executivo', 'couro', 'genuíno', 'compartimento', 'notebook', 'laptop', 'profissional']
```

2. **Expansão Semântica**
```python
def expand_semantic(terms):
    """
    Expande termos com sinônimos e variações
    """
    expanded = set(terms)
    
    for term in terms:
        # Sinônimos
        syns = get_synonyms(term)  # via WordNet ou API
        expanded.update(syns)
        
        # Hipônimos (mais específicos)
        hypos = get_hyponyms(term)
        expanded.update(hypos)
        
        # Hiperônimos (mais gerais)
        hypers = get_hypernyms(term)
        expanded.update(hypers)
    
    return list(expanded)

# Exemplo
expand_semantic(['mochila'])
# ['mochila', 'bolsa', 'bag', 'backpack', 'mochila_escolar', 'mochila_viagem']
```

3. **Ranking por Potencial**
```python
def rank_head_terms(terms, category, marketplace_data):
    """
    Rankeia termos por potencial de busca e conversão
    """
    scored = []
    
    for term in terms:
        score = 0
        
        # Volume de busca (estimado)
        search_volume = estimate_search_volume(term, marketplace_data)
        score += log(search_volume + 1) * 10
        
        # Competição (menor é melhor)
        competition = count_competing_listings(term, marketplace_data)
        score -= log(competition + 1) * 5
        
        # Relevância à categoria
        category_relevance = calculate_relevance(term, category)
        score += category_relevance * 15
        
        # Especificidade (médio é melhor)
        specificity = calculate_specificity(term)
        score += (1 - abs(specificity - 0.5)) * 10
        
        scored.append((term, score))
    
    # Ordena por score
    scored.sort(key=lambda x: x[1], reverse=True)
    
    return scored

# Exemplo output
# [
#   ('mochila executiva', 85.3),
#   ('mochila couro', 78.1),
#   ('mochila notebook', 75.8),
#   ('mochila profissional', 71.2),
#   ...
# ]
```

**Output Esperado:**
```markdown

**Tags**: concrete, general

**Palavras-chave**: RESEARCH, NOTES, AGENTE

**Origem**: unknown


---


<!-- VERSÍCULO 2/17 - marketplace_optimization_4_conceitos_chave_20251113.md (34 linhas) -->

# 4️⃣ Conceitos-Chave

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

### Entropia (0-100)

Mede **densidade de informação nova**:
- **80-100**: Muito específico, denso, inovador
- **50-79**: Bom para contexto, prático, balanceado
- **0-49**: Óbvio, genérico, repetitivo

### Deus-vs-Todo (Abstração)

**DEUS (Absoluto):**
- "ACID properties are fundamental..."
- Válido universalmente, atemporalmente

**TODO (Contextual):**
- "Our PostgreSQL 14.2 in us-east-1..."
- Específico de contexto, temporal

**MIXED:**
- Combina conceitos universais com aplicações práticas

**Tags**: ecommerce, intermediate

**Palavras-chave**: Conceitos, Chave

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 3/17 - marketplace_optimization_4_destilação_de_conhecimento_20251113.md (59 linhas) -->

# 4. DESTILAÇÃO DE CONHECIMENTO

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### 4.1 O que é Knowledge Distillation

**Definição:**
Processo de transferir conhecimento de um modelo "professor" (grande, complexo) para um modelo "aluno" (pequeno, eficiente).

**Aplicado a Documentação:**
Transformar conhecimento complexo em formato digestível sem perder essência.

**Paralelo: LLM Grande → LLM Pequeno = Doc Complexa → Doc Acessível**

```python
class KnowledgeDistillation:
    """
    Framework conceitual para destilar conhecimento em docs
    """
    
    def distill(self, complex_knowledge):
        """
        Processo de destilação em 4 etapas
        """
        # 1. EXTRACT: Identificar conceitos-chave
        key_concepts = self.extract_core_concepts(complex_knowledge)
        
        # 2. SIMPLIFY: Reduzir complexidade sem perder precisão
        simplified = self.simplify_concepts(key_concepts)
        
        # 3. EXEMPLIFY: Adicionar exemplos concretos
        with_examples = self.add_examples(simplified)
        
        # 4. VALIDATE: Testar compreensão
        validated = self.validate_understanding(with_examples)
        
        return validated
```

### 4.2 Técnicas de Destilação para Documentação

#### Técnica 1: Abstraction Ladder (Escada de Abstração)

**Princípio:** Apresentar mesmo conceito em múltiplos níveis de abstração

**Exemplo: Explicando "Attention Mechanism"**

```markdown

**Tags**: abstract, general

**Palavras-chave**: CONHECIMENTO, DESTILAÇÃO

**Origem**: unknown


---


<!-- VERSÍCULO 4/17 - marketplace_optimization_4_notas_de_citação_e_boas_práticas_20251113.md (19 linhas) -->

# 4) Notas de Citação e Boas Práticas

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

- Cite números com parcimônia (ex.: “+63% preferem concluir no marketplace”), sempre mantendo **contexto**.  
- Evite afirmar **causalidade** onde a fonte apenas indica **correlação**.  
- Atualize dados anualmente para manter credibilidade (versões 2025 → revisar em 2026).  
- Para Mercado Livre, priorize **prova social própria** (avaliações reais) + **garantias claras**; use as fontes acima como **apoio** à lógica da copy, não como protagonista da mensage

**Tags**: ecommerce, intermediate

**Palavras-chave**: Notas, Citação, Boas, Práticas

**Origem**: _CONSOLIDATED_ecommerce_livro.md


---


<!-- VERSÍCULO 5/17 - marketplace_optimization_4_seção_faq_5_8_perguntas_20251113.md (72 linhas) -->

# 4️⃣ Seção FAQ (5-8 Perguntas)

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### Estrutura

```
P: [OBJEÇÃO/DÚVIDA COMUM]
R: [RESPOSTA CURTA + BENEFÍCIO + PROVA]
```

### Coleta de Perguntas

Use dados de pesquisa:
- Comentários em anúncios de concorrentes
- Reviews negativos (o que reclamam?)
- Comunidades online (fóruns, Discord)
- Seu próprio suporte (se tiver experiência)

### Exemplo de FAQ Completa:

```
P: "Roda bem para programação Python/Django/React?"
R: "Sim! Processador i7 + 16GB roda até 5 abas VSCode +
    Docker + npm dev server sem travamentos. Testado com
    projetos de 50k+ linhas de código."

P: "Aquece muito? Vou trabalhar 8h direto."
R: "Não! Ventilação otimizada mantém ~45°C em trabalho continuo.
    Mesmo em compilation pesada (Webpack bundling), não passa de 60°C.
    Clientes que trabalham 10h+ confirmam: nenhum problema de calor."

P: "Bateria dura quanto tempo? Preciso de dia inteiro."
R: "11 horas em uso normal (IDE + documentação + Slack).
    Em modo econômico, chega a 13h. Testado e comprovado."

P: "Devolve em 30 dias se não gostar?"
R: "Sim! Temos política de 30 dias sem risco. Se não atender
    suas expectativas, devolvemos 100% + frete de volta grátis."

P: "Qual a diferença entre este e o Modelo Y que é R$ 300 mais caro?"
R: "Ambos têm i7 + 16GB. A diferença: tela de 14' (vs nossa 15.6').
    Para programação, a tela maior é melhor. Para portabilidade,
    a mais fina vence. Depende de seu uso."

P: "É novo ou recondicionado?"
R: "100% NOVO lacrado na caixa. Vem com nota fiscal,
    garantia de 2 anos e Windows 11 ativado."

P: "Posso fazer upgrade? Trocar RAM, HD depois?"
R: "Sim! RAM e SSD são acessíveis (debaixo do teclado).
    Processador é solda (não muda). Vem 16GB, mas pode
    expandir para 32GB se precisar em 2-3 anos."

P: "Por que vocês são R$ 200 mais baratos que a loja oficial?"
R: "Somos distribuidor autorizado, não fabricante.
    Sem margem de loja física, repassamos economia ao cliente.
    Mesma garantia, mesma qualidade."
```

---

**Tags**: concrete, general

**Palavras-chave**: Perguntas, Seção

**Origem**: unknown


---


<!-- VERSÍCULO 6/17 - marketplace_optimization_4_string_de_lógica_resumo_para_montagem_de_prompt_20251113.md (21 linhas) -->

# 4) String de Lógica (resumo para montagem de prompt)

**Categoria**: marketplace_optimization
**Qualidade**: 0.87/1.00
**Data**: 20251113

## Conteúdo

```text
Você é um orquestrador CODEXA. Siga o padrão Raiz/Galhos; respeite brand_guidelines; 
quando image_mode='fidelidade', use briefing_imagens (10 cenas) como padrão; 
não invente certificações e marque suposições em notes. 
Se criativo/branding, você *pode* evocar tokens herméticos (metáforas), sem tratá-los como ciência.
```

**Tags**: ecommerce, concrete

**Palavras-chave**: String, Lógica, resumo, montagem, prompt

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 7/17 - marketplace_optimization_4_tools_the_capabilities_20251113.md (51 linhas) -->

# 4. TOOLS (The Capabilities)

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```yaml
tool_categories:
  SLASH_COMMANDS:
    - /plan: create_specification
    - /code: implement_solution
    - /test: validate_functionality
    - /review: check_quality
    - /doc: generate_documentation
    
  SKILLS:
    location: /mnt/skills/
    purpose: specialized_capabilities
    examples: [docx, xlsx, pdf, web_scraping]
    
  MCP_SERVERS:
    purpose: external_integrations
    examples: [github, slack, databases, apis]
    
  SUB_AGENTS:
    purpose: specialized_intelligence
    pattern: agent_calling_agent
    composition: unlimited_nesting
    
  BASH_COMMANDS:
    purpose: system_operations
    use_case: file_ops_git_env_management

tool_orchestration:
  principle: "Call any tool from agentic layer"
  chaining: "Tools compose into workflows"
  validation: "Every tool output validated"
```

---

# PART II: THE LCM FRAMEWORK (Large Commerce Model)

**Tags**: abstract, general

**Palavras-chave**: TOOLS, Capabilities

**Origem**: unknown


---


<!-- VERSÍCULO 8/17 - marketplace_optimization_51_lcm_ai_processing_20251113.md (58 linhas) -->

# 5.1 LCM-AI PROCESSING

**Categoria**: marketplace_optimization
**Qualidade**: 0.79/1.00
**Data**: 20251113

## Conteúdo

```yaml
trinity_output:
  human_readable:
    format: .md
    purpose: documentation
    audience: developers
    
  llm_optimized:
    format: .llm.json
    purpose: context_window_consumption
    structure: [embeddings, keywords, qa_pairs]
    
  metadata:
    format: .meta.json
    purpose: system_intelligence
    content: [relations, versions, metrics]

skill_transformations:
  synthesizer:
    input: raw_document
    output: structured_summary
    technique: abstractive_summarization
    
  tokenizer:
    input: large_text
    output: semantic_chunks
    technique: sliding_window_with_overlap
    
  purpose_extractor:
    input: any_content
    output: taxonomy_tags
    technique: zero_shot_classification
    
  qa_generator:
    input: knowledge_unit
    output: question_answer_pairs
    technique: t5_question_generation
    
  evaluator:
    input: generated_content
    output: quality_score
    technique: reward_model_scoring
```

**Tags**: general, intermediate

**Palavras-chave**: PROCESSING

**Origem**: unknown


---


<!-- VERSÍCULO 9/17 - marketplace_optimization_52_distillation_patterns_20251113.md (52 linhas) -->

# 5.2 DISTILLATION PATTERNS

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

```yaml
knowledge_distillation:
  teacher_to_student:
    method: behavior_cloning
    data: teacher_outputs_as_training
    
  large_to_small:
    method: logit_matching
    benefit: compression_without_loss
    
  ensemble_to_single:
    method: knowledge_aggregation
    benefit: best_of_all_experts

document_optimization:
  for_context_window:
    - maximize_information_density
    - hierarchical_structure
    - redundancy_at_key_concepts
    - clear_navigation_markers
    
  for_fine_tuning:
    - instruction_response_pairs
    - diverse_examples
    - edge_case_coverage
    - quality_over_quantity
    
  for_retrieval:
    - semantic_chunking
    - keyword_optimization
    - vector_embedding_friendly
    - metadata_rich
```

---

# 🎮 CARD 6: OPERATIONAL MODES

**Tags**: abstract, general

**Palavras-chave**: PATTERNS, DISTILLATION

**Origem**: unknown


---


<!-- VERSÍCULO 10/17 - marketplace_optimization_5_agente_2_copy_generator_20251113.md (207 linhas) -->

# 5. AGENTE 2: COPY GENERATOR

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### 5.1 Objetivos e Responsabilidades

**Objetivo Principal:**
Transformar insights de pesquisa em copy persuasivo otimizado para conversão em marketplaces.

**Responsabilidades:**
1. ✅ Criar título SEO-otimizado
2. ✅ Escrever descrição curta (hook)
3. ✅ Desenvolver descrição principal (4 parágrafos)
4. ✅ Listar características com benefícios
5. ✅ Formular CTAs eficazes
6. ✅ Validar compliance
7. ✅ Otimizar densidade de keywords
8. ✅ Incorporar gatilhos psicológicos

**NÃO é responsabilidade:**
- ❌ Fazer pesquisa de mercado
- ❌ Gerar imagens
- ❌ Definir preço
- ❌ Gerenciar inventory

### 5.2 Fundamentos de Copywriting para E-commerce

#### Framework AIDA

```
A - Attention (Atenção)
  ├─> Título impactante
  └─> Primeira imagem chamativa

I - Interest (Interesse)
  ├─> Descrição curta provocativa
  └─> Demonstração de entendimento da dor

D - Desire (Desejo)
  ├─> Benefícios emocionais
  ├─> Prova social
  └─> Visualização de ganhos

A - Action (Ação)
  ├─> CTA claro
  ├─> Remoção de fricção
  └─> Urgência/escassez
```

#### Framework PAS

```
P - Problem (Problema)
  "Cansado de mochilas que machucam as costas?"

A - Agitate (Agitar)
  "Dor nas costas no fim do dia, alças que cortam ombros,
   zíperes que travam... tudo isso compromete sua produtividade."

S - Solution (Solução)
  "Nossa mochila ergonômica distribui peso uniformemente,
   com alças acolchoadas de espuma memory foam e zíperes YKK..."
```

#### Framework BAB

```
B - Before (Antes)
  Situação atual do cliente (com o problema)

A - After (Depois)
  Situação desejada (problema resolvido)

B - Bridge (Ponte)
  Como seu produto leva de Before para After
```

### 5.3 Anatomia de Um Título Vencedor

**Estrutura Recomendada:**

```
[MARCA] [PRODUTO-CORE] [MATERIAL/QUALIDADE] [TAMANHO/ESPECIFICAÇÃO] - [BENEFÍCIO-CHAVE]

Exemplo:
"ACME Mochila Executiva Couro Genuíno Notebook 15.6 - Ergonômica Impermeável"

Breakdown:
├─ ACME: Marca (reconhecimento)
├─ Mochila Executiva: Produto + Contexto (keyword primária)
├─ Couro Genuíno: Material (diferencial, keyword secundária)
├─ Notebook 15.6: Especificação técnica (long-tail)
└─ Ergonômica Impermeável: Benefícios (converte dor em ganho)
```

**Fórmulas Testadas:**

```python
FORMULAS = {
    'especificacao_completa': '{MARCA} {PRODUTO} {MATERIAL} {TAMANHO} - {BENEFICIO}',
    'problema_solucao': '{PRODUTO} {ATRIBUTO} Que {RESOLVE_PROBLEMA}',
    'premium_positioning': '{PRODUTO} Premium {MATERIAL} - {GARANTIA} {BENEFICIO}',
    'value_proposition': '{PRODUTO} {ATRIBUTO}: {BENEFICIO_1} + {BENEFICIO_2}',
    'target_specific': '{PRODUTO} Para {PUBLICO} {OCASIAO} - {DIFERENCIAL}'
}

# Exemplos práticos
exemplos = [
    # Especificação Completa
    "Mochila Executiva Couro Legítimo 17 Polegadas - Ergonômica Resistente",
    
    # Problema-Solução
    "Mochila Ergonômica Que Elimina Dor nas Costas - Couro Premium",
    
    # Premium Positioning
    "Mochila Premium Couro Italiano - Garantia Vitalícia Alta Durabilidade",
    
    # Value Proposition
    "Mochila Executiva Couro: Organização Perfeita + Proteção Notebook",
    
    # Target Specific
    "Mochila Para Executivos Moderno Trabalho - Design Minimalista Funcional"
]
```

**Otimização de Palavras:**

```python
def optimize_title(title, char_limit=60):
    """
    Otimiza título para máximo impacto dentro do limite
    """
    words = title.split()
    
    # Priorização de palavras por valor
    word_values = {}
    for word in words:
        value = 0
        
        # Keyword primária/secundária
        if word in primary_keywords:
            value += 10
        elif word in secondary_keywords:
            value += 5
        
        # Especificidade técnica
        if word.replace('"', '').replace('.', '').isdigit():
            value += 3
        
        # Diferenciador
        if word in differentiators:
            value += 7
        
        # Benefício emocional
        if word in emotional_triggers:
            value += 6
        
        word_values[word] = value
    
    # Ordena por valor
    sorted_words = sorted(words, key=lambda w: word_values[w], reverse=True)
    
    # Reconstrói título
    optimized = []
    current_length = 0
    
    for word in sorted_words:
        if current_length + len(word) + 1 <= char_limit:
            optimized.append(word)
            current_length += len(word) + 1
    
    # Reordena para naturalidade
    optimized = reorder_naturally(optimized)
    
    return ' '.join(optimized)
```

**A/B Testing de Títulos:**

| Variação | CTR | Conversão | Nota |
|----------|-----|-----------|------|
| Título A: "Mochila Couro Notebook" | 2.3% | 3.1% | Genérico |
| Título B: "Mochila Executiva Couro Notebook 15.6 Impermeável" | 4.7% | 5.8% | Completo ✅ |
| Título C: "Mochila Premium Couro Italiano Garantia Vitalícia" | 3.9% | 4.2% | Preço-sensível |

### 5.4 Descrição Curta (Hook)

**Objetivo:** Capturar atenção em 1-2 linhas

**Estrutura:**
```
[GANHO_EMOCIONAL] + [PROBLEMA_RESOLVIDO] + [DIFERENCIAL_ÚNICO]
```


[... content truncated ...]

**Tags**: abstract, general

**Palavras-chave**: GENERATOR, COPY, AGENTE

**Origem**: unknown


---


<!-- VERSÍCULO 11/17 - marketplace_optimization_5_chunk_prompt_composition_library_20251113.md (48 linhas) -->

# 5-Chunk Prompt Composition Library

**Categoria**: marketplace_optimization
**Qualidade**: 0.85/1.00
**Data**: 20251113

## Conteúdo

The system uses 5 reusable prompt chunks that agents compose:

### Chunk 1: Research Consolidation
**Purpose**: Consolidate market and competitive research into insights

**Input**: Market research + competitive analysis
**Output**: Key opportunities, positioning, strategic recommendations

### Chunk 2: Keyword Analysis
**Purpose**: Organize and prioritize keywords

**Input**: Extracted keywords
**Output**: Ranked keywords by potential, strategy

### Chunk 3: Competitor Insights
**Purpose**: Extract competitive intelligence

**Input**: Competitor data
**Output**: Advantages, positioning, messaging angles

### Chunk 4: Ad Brief Generation
**Purpose**: Create advertising briefs

**Input**: Research consolidated data
**Output**: Ad copy variations, CTAs, value props

### Chunk 5: Copy Optimization
**Purpose**: Optimize ad copy for conversion

**Input**: Ad copy + research context
**Output**: Optimized variations by element

---

**Tags**: architectural, ecommerce, general

**Palavras-chave**: Chunk, Prompt, Composition, Library

**Origem**: unknown


---


<!-- VERSÍCULO 12/17 - marketplace_optimization_5_chunk_prompts_20251113.md (94 linhas) -->

# 5-Chunk Prompts

**Categoria**: marketplace_optimization
**Qualidade**: 0.95/1.00
**Data**: 20251113

## Conteúdo

### Chunk 1: Research Consolidation
[Full prompt ready to use]

### Chunk 2: Keyword Analysis
[Full prompt ready to use]

[... continues for Chunks 3, 4, 5 ...]
```

### Output 2: JSON Structured Data

```json
{
  "pesquisa": {
    "produto": "Notebook Gamer",
    "data": "2024-11-02",
    "status": "complete"
  },
  "pilar_1_mercado": {
    "volume_mensal": 50000,
    "crescimento_yoy": 15,
    "sazonalidade": ["janeiro", "julho"],
    "preco_medio": 5000,
    "principais_canais": ["amazon", "mercado_livre"]
  },
  "pilar_2_competicao": {
    "competidores_principais": ["Samsung", "Asus", "Dell"],
    "gaps_identificados": ["suporte brasileiro", "custo-beneficio"]
  },
  "pilar_4_keywords": {
    "nivel_1_head": ["notebook gamer"],
    "nivel_2_midtail": ["notebook gamer barato"],
    "nivel_3_longtail": ["melhor notebook gamer custo-beneficio 2024"],
    "nivel_4_faq": ["qual notebook é melhor para programação?"]
  },
  "chunks": {
    "chunk_1": "{ full prompt JSON }",
    "chunk_2": "{ full prompt JSON }",
    "chunk_3": "{ full prompt JSON }",
    "chunk_4": "{ full prompt JSON }",
    "chunk_5": "{ full prompt JSON }"
  }
}
```

### Output 3: 5 AI-Ready Prompts

Cada chunk é um prompt completo com:
- **System Prompt**: Define o papel do AI
- **User Prompt**: Define a tarefa específica
- **Context Data**: Dados contextuais da pesquisa
- **Expected Output**: Estrutura esperada do resultado

```
CHUNK 1: Research Consolidation
=================================

SYSTEM PROMPT:
"You are a strategic research analyst. Your role is to consolidate
market research and competitive intelligence into actionable insights..."

USER PROMPT:
"Consolidate the following research data:
MARKET DATA: [market insights]
COMPETITIVE DATA: [competitor analysis]
KEYWORDS: [keyword hierarchy]

Task: Generate strategic positioning recommendations..."

EXPECTED OUTPUT:
{
  "strategic_insights": [],
  "market_opportunities": [],
  "competitive_advantages": [],
  "positioning_recommendations": ""
}
```

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Chunk, Prompts

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 13/17 - marketplace_optimization_5_mapas_r_pidos_o_que_consultar_para_1_20251113.md (21 linhas) -->

# 5) Mapas Rápidos (o que consultar para…)

**Categoria**: marketplace_optimization
**Qualidade**: 0.72/1.00
**Data**: 20251113

## Conteúdo

- **Definir o problema em 3 níveis:** Creativeo (estrutura) + notas internas do produto.  
- **Escolher CTA forte:** Creativeo (exemplos) + prática de “dissonância cognitiva” (Verywell Mind).  
- **Validar gatilhos emocionais:** Forbes (4 razões) + Psychology Today (emoções).  
- **Justificar políticas de devolução/UX:** ChannelEngine (preferência por marketplaces e confiança).

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Mapas, Rápidos, consultar

**Origem**: _CONSOLIDATED_ECOMMERCE_VERSICULOS_FROM_GIT.md


---


<!-- VERSÍCULO 14/17 - marketplace_optimization_5_mapas_r_pidos_o_que_consultar_para_20251113.md (21 linhas) -->

# 5) Mapas Rápidos (o que consultar para…)

**Categoria**: marketplace_optimization
**Qualidade**: 0.72/1.00
**Data**: 20251113

## Conteúdo

- **Definir o problema em 3 níveis:** Creativeo (estrutura) + notas internas do produto.  
- **Escolher CTA forte:** Creativeo (exemplos) + prática de “dissonância cognitiva” (Verywell Mind).  
- **Validar gatilhos emocionais:** Forbes (4 razões) + Psychology Today (emoções).  
- **Justificar políticas de devolução/UX:** ChannelEngine (preferência por marketplaces e confiança).

---

**Tags**: ecommerce, intermediate

**Palavras-chave**: Mapas, Rápidos, consultar

**Origem**: _CONSOLIDATED_ecommerce_other.md


---


<!-- VERSÍCULO 15/17 - marketplace_optimization_5_mapas_rápidos_o_que_consultar_para_20251113.md (21 linhas) -->

# 5) Mapas Rápidos (o que consultar para…)

**Categoria**: marketplace_optimization
**Qualidade**: 0.81/1.00
**Data**: 20251113

## Conteúdo

- **Definir o problema em 3 níveis:** Creativeo (estrutura) + notas internas do produto.  
- **Escolher CTA forte:** Creativeo (exemplos) + prática de “dissonância cognitiva” (Verywell Mind).  
- **Validar gatilhos emocionais:** Forbes (4 razões) + Psychology Today (emoções).  
- **Justificar políticas de devolução/UX:** ChannelEngine (preferência por marketplaces e confiança).

---

**Tags**: ecommerce, general, intermediate

**Palavras-chave**: Rápidos, Mapas, consultar

**Origem**: unknown


---


<!-- VERSÍCULO 16/17 - marketplace_optimization_5_metodologias_de_treinamento_smollm_approach_20251113.md (175 linhas) -->

# 5. METODOLOGIAS DE TREINAMENTO (SMOLLM APPROACH)

**Categoria**: marketplace_optimization
**Qualidade**: 0.89/1.00
**Data**: 20251113

## Conteúdo

### 5.1 Visão Geral: Multi-Stage Training

**Insight do SmolLM2:**
Modelos pequenos precisam de **curadoria de dados agressiva** e **treinamento multi-estágio**.

```
STAGE 1: BASE PRETRAINING (0-6T tokens)
├── FineWeb-Edu (60%): Conteúdo educacional de alta qualidade
├── DCLM (40%): Q&A diversificado e real-world
└── StarCoderData (10%): Código multi-linguagem

STAGE 2: MATH & CODE UPSAMPLING (6-9T tokens)
├── FineMath (novo dataset): Problemas matemáticos graduais
├── Stack-Edu (filtrado): Código educacional do StackExchange
└── Rebalance ratios baseado em eval

STAGE 3: FINAL REBALANCING (9-11T tokens)
├── Ajuste fino de proporções
└── Foco em áreas de fraqueza identificadas

POST-TRAINING:
├── Supervised Fine-Tuning (SFT)
│   └── SmolTalk (dataset de instruções)
└── Direct Preference Optimization (DPO)
    └── UltraFeedback (feedback sintético)
```

**Lições-Chave:**

1. **Não há "one-size-fits-all"**: Proporções ideais dependem do tamanho do modelo
2. **Avaliação contínua**: Avaliar a cada 1-2T tokens e ajustar
3. **Dados > Arquitectura**: SmolLM2 vence outros modelos 1.7B via dados melhores
4. **Qualidade > Quantidade**: Filtrar agressivamente vale a pena

### 5.2 Data-Centric Training

**Princípio:** Modelo é função dos dados mais que hyperparameters

#### Dataset Quality Hierarchy (SmolLM2)

```
TIER 1: GOLD (usar muito)
├── FineWeb-Edu: Score 3-5 no classifier educacional
├── FineMath: Problemas com explicações step-by-step
└── SmolTalk: Instruções curadas manualmente

TIER 2: SILVER (usar moderadamente)
├── DCLM filtered: Score 1-2 no classifier
├── Stack-Edu: Código com >5 upvotes
└── Cosmopedia: Textos sintéticos de alta qualidade

TIER 3: BRONZE (usar sparingly ou descartar)
├── Web data raw (muito ruído)
├── Código sem contexto
└── Instruções genéricas
```

#### Filtering Pipeline

```python
class DataQualityFilter:
    """
    Pipeline de filtragem baseado em SmolLM approach
    """
    
    def __init__(self, quality_threshold=0.7):
        self.threshold = quality_threshold
        self.classifier = self.load_quality_classifier()
    
    def filter_web_data(self, documents):
        """
        Filtra documentos web por qualidade educacional
        """
        filtered = []
        
        for doc in documents:
            # 1. Score educacional (FineWeb-Edu approach)
            edu_score = self.classifier.score_educational_value(doc)
            
            # 2. Filtros heurísticos
            passes_heuristics = (
                self.check_length(doc) and
                self.check_language_quality(doc) and
                self.check_no_spam(doc) and
                self.check_no_toxic(doc)
            )
            
            # 3. Deduplicação
            is_unique = self.check_not_duplicate(doc, filtered)
            
            if edu_score >= self.threshold and passes_heuristics and is_unique:
                filtered.append({
                    'text': doc,
                    'score': edu_score,
                    'tier': self.assign_tier(edu_score)
                })
        
        return filtered
    
    def check_length(self, doc):
        """Nem muito curto (spam) nem muito longo (livros)"""
        word_count = len(doc.split())
        return 100 < word_count < 10000
    
    def check_language_quality(self, doc):
        """Gramática razoável, pontuação adequada"""
        # Implementação: use language tool ou modelo
        return True  # Simplified
    
    def check_no_spam(self, doc):
        """Detecta padrões de spam (URLs excessivos, caps lock)"""
        url_count = doc.count('http')
        caps_ratio = sum(c.isupper() for c in doc) / len(doc)
        return url_count < 10 and caps_ratio < 0.3
    
    def check_no_toxic(self, doc):
        """Remove conteúdo tóxico/ofensivo"""
        # Implementação: use Perspective API ou modelo
        return True  # Simplified
    
    def assign_tier(self, score):
        """Atribui tier baseado em score"""
        if score >= 4.0:
            return "GOLD"
        elif score >= 2.0:
            return "SILVER"
        else:
            return "BRONZE"
```

#### Dataset Mixing Strategy

```python
class DatasetMixer:
    """
    Mix datasets com proporções dinâmicas (SmolLM2 style)
    """
    
    def __init__(self, stage="early", model_size="1.7B"):
        self.stage = stage
        self.model_size = model_size
        self.proportions = self.get_proportions()
    
    def get_proportions(self):
        """
        Proporções variam por estágio e tamanho de modelo
        """
        if self.model_size == "1.7B":
            if self.stage == "early":  # 0-6T tokens
                return {
                    'web_edu': 0.60,    # FineWeb-Edu
                    'web_general': 0.30, # DCLM filtered
                    'code': 0.10        # StarCoder
                }
            elif self.stage == "mid":  # 6-9T tokens
                return {
                    'web_edu': 0.45,
                    'web_general'

[... content truncated ...]

**Tags**: concrete, general

**Palavras-chave**: METODOLOGIAS, SMOLLM, TREINAMENTO, APPROACH

**Origem**: unknown


---


<!-- VERSÍCULO 17/17 - marketplace_optimization_5_princ_pios_orientadores_para_treinar_20251113.md (27 linhas) -->

# 5. Princípios Orientadores para Treinar LLMs

**Categoria**: marketplace_optimization
**Qualidade**: 0.79/1.00
**Data**: 20251113

## Conteúdo

1. **Formato Primeiro**: os modelos devem ser instruídos a respeitar JSON STRICT; qualquer saída inválida precisa acionar reparo ou retry.
2. **Fluxo Multi-etapas**: reforçar a sequência benchmark → síntese → geração → validação → empacotamento para maximizar consistência.
3. **Resiliência de Fornecedor**: manter fallback cross-vendor e monitorar métricas de sucesso para calibrar preferências dinâmicas.
4. **Enriquecimento Determinístico**: SEO e normalização pós-LLM são cruciais para compatibilidade com marketplaces e precisam de regras estáveis.
5. **Feedback Contínuo**: telemetria e erros diagnósticos alimentam ajustes do prompt, heurísticas de reparo e UX do formulário.


---

### RAW_009_SCALED_DISTILL.md

# 🚀 Estratégia Escalada: 36k → Versionable Knowledge Base

**Tags**: ecommerce, intermediate

**Palavras-chave**: Princípios, Orientadores, Treinar, LLMs

**Origem**: _CONSOLIDATED_ECOMMERCE_RAW_FROM_GIT.md


---


<!-- FIM DO CAPÍTULO 3 -->
<!-- Total: 17 versículos, 1182 linhas -->
