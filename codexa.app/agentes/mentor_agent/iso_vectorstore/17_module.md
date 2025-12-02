# Lesson Builder Module | mentor_agent

**Purpose**: Generate structured "aula ao vivo" (live lessons) from multiple knowledge files
**Version**: 1.0.0 | **Updated**: 2025-11-18

---

## 🎯 OVERVIEW

Teaching mode module that synthesizes multiple knowledge files into comprehensive, structured lessons for Brazilian e-commerce sellers.

**Use Case**: When seller requests "Me ensina sobre X" or "Quero aprender Y"

**Output**: 800-1200 word structured lesson with practical examples

---

## 📚 LESSON STRUCTURE (6 Sections)

### 1. 🎯 Por que importa? (Why It Matters)

**Purpose**: Business impact justification

**Content**:
- Why this topic matters for sellers
- Real impact on sales/conversions/profits
- Cost of ignoring this topic
- Who needs this most (target audience)

**Format**:
```markdown
## 🎯 Por que importa?

[Topic] pode fazer a diferença entre vender R$ 5.000/mês e R$ 20.000/mês. Sellers que dominam isso reportam:
- +45% taxa de conversão
- -30% custo de aquisição
- +60% recompra

**Quem mais precisa**: Sellers iniciantes no ML/Shopee com <50 vendas/mês
```

**Target Length**: 100-150 words

---

### 2. 📖 Pilares Essenciais (Key Pillars)

**Purpose**: Break complex topic into 3-5 core concepts

**Content**:
- 3-5 foundational pillars
- Each pilar = 1 paragraph
- Practical definition (no theory)
- Why this pilar matters

**Format**:
```markdown
## 📖 3 Pilares Essenciais

### Pilar 1: [Nome do Pilar]
**O que é**: [Definição prática em 1 frase]
**Por que importa**: [Impacto no negócio]
**Exemplo rápido**: [Caso de 1 linha]

### Pilar 2: [Nome do Pilar]
[Same structure]

### Pilar 3: [Nome do Pilar]
[Same structure]
```

**Target Length**: 200-300 words (3-5 pilars × 60-100 words each)

---

### 3. 🛠️ Como fazer (How To Execute)

**Purpose**: Step-by-step executable actions

**Content**:
- 5-8 numbered steps
- Each step = concrete action
- Tools/resources mentioned
- Timeframe indicated

**Format**:
```markdown
## 🛠️ Como fazer (Passo a Passo)

**Tempo estimado**: 30-60 minutos

### Passo 1: [Ação Concreta]
[Instrução detalhada]
🔧 **Ferramenta**: [Nome da tool]
⏱️ **Tempo**: ~10 min

### Passo 2: [Ação Concreta]
[Instrução detalhada]
🔧 **Ferramenta**: [Nome da tool]
⏱️ **Tempo**: ~15 min

[... total 5-8 passos]
```

**Target Length**: 300-400 words

---

### 4. 💡 Exemplo Real (Real Example)

**Purpose**: Before/after case study with metrics

**Content**:
- Contexto (seller profile)
- Before state (problem)
- Implementation (what was done)
- After state (results with metrics)
- Key learnings

**Format**:
```markdown
## 💡 Exemplo Real

**Contexto**: Loja de moda feminina no ML, 200 vendas/mês, CVR 1.2%

**❌ Antes**:
- Títulos genéricos ("Vestido Bonito")
- Sem keywords específicas
- 50 cliques/dia, 0.6 vendas/dia

**✅ Depois** (aplicou técnica de título SEO):
- Título otimizado: "Vestido Longo Feminino Floral Verão P ao GG Manga Curta"
- Keywords específicas + atributos
- **Resultado após 7 dias**:
  - 150 cliques/dia (+200%)
  - 2.5 vendas/dia (+317%)
  - CVR: 1.7% (+42%)

**💰 Impacto**: +R$ 4.500/mês em vendas
```

**Target Length**: 150-200 words

---

### 5. ✏️ Exercício Prático (Actionable Task)

**Purpose**: Immediate hands-on exercise for seller

**Content**:
- Specific task to complete now
- Expected output
- Success criteria
- Time limit

**Format**:
```markdown
## ✏️ Exercício Prático (Faça Agora!)

**Tarefa**: Reescreva o título do seu produto mais vendido usando a técnica [X]

**Passo a passo**:
1. Abra seu anúncio no ML/Shopee
2. Copie o título atual → [ANTES]
3. Aplique a fórmula: [Keyword] + [Atributo 1] + [Atributo 2] + [Diferencial]
4. Reescreva → [DEPOIS]

**Critério de sucesso**:
✅ Título tem 50-60 caracteres
✅ Contém ≥3 keywords relevantes
✅ Inclui ≥2 atributos específicos (cor, tamanho, material)

**Tempo**: 10 minutos

📤 **Compartilhe**: Poste seu antes/depois no grupo!
```

**Target Length**: 100-150 words

---

### 6. 🔗 Próximos Passos (Next Steps)

**Purpose**: Clear action plan + related topics

**Content**:
- Immediate next action (today)
- Short-term action (this week)
- Related topics to learn next
- Resources/links

**Format**:
```markdown
## 🔗 Próximos Passos

**Hoje** (faça agora):
- [ ] Complete o exercício prático acima
- [ ] Aplique em ≥3 produtos

**Esta semana**:
- [ ] Monitore métricas (cliques, conversão)
- [ ] Ajuste títulos baseado em performance
- [ ] Teste variações A/B

**Aprenda depois**:
1. [Topic relacionado 1] → `/prime-mentor aprenda [topic]`
2. [Topic relacionado 2] → `/prime-mentor aprenda [topic]`
3. [Topic relacionado 3] → Arquivo: `PROCESSADOS/categoria_assunto_date.md`

**Recursos**:
- 📄 Planilha de keywords: [link]
- 🎥 Vídeo tutorial: [link]
- 📊 Checklist de otimização: [link]
```

**Target Length**: 100-150 words

---

## 🔧 LESSON GENERATION ALGORITHM

### Step 1: Topic Analysis

```python
def analyze_lesson_request(request_text):
    """
    Extract topic, scope, and target nivel from request
    """
    # Detect topic
    topic = extract_topic(request_text)

    # Detect scope (broad vs specific)
    is_broad = any(word in request_text.lower() for word in ["tudo sobre", "completo", "desde o início"])

    # Detect target nivel
    if "iniciante" in request_text.lower() or "começar" in request_text.lower():
        nivel = "basico"
    elif "avançado" in request_text.lower() or "expert" in request_text.lower():
        nivel = "avancado"
    else:
        nivel = "intermediario"

    return {
        "topic": topic,
        "scope": "broad" if is_broad else "specific",
        "nivel": nivel
    }
```

---

### Step 2: Knowledge File Discovery

```python
def find_relevant_files(topic, catalogo_json):
    """
    Search catalogo.json for files matching topic
    """
    matches = []

    for file_entry in catalogo_json:
        # Match on categoria, assunto, tags, aplicacao
        relevance_score = 0

        if topic.lower() in file_entry["assunto"].lower():
            relevance_score += 3  # Exact assunto match

        if topic.lower() in file_entry["categoria"].lower():
            relevance_score += 2  # Categoria match

        if any(topic.lower() in tag.lower() for tag in file_entry["tags"]):
            relevance_score += 1  # Tag match

        if relevance_score > 0:
            matches.append({
                "file": file_entry["arquivo"],
                "score": relevance_score,
                "metadata": file_entry
            })

    # Sort by relevance, return top 5
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches[:5]
```

---

### Step 3: Content Synthesis

```python
def synthesize_lesson(topic, source_files, nivel):
    """
    Synthesize multiple files into structured lesson
    """
    # Read all source files
    all_content = []
    for file_path in source_files:
        content = read_file(f"PROCESSADOS/{file_path}")
        all_content.append(content)

    # Extract key concepts from all files
    all_concepts = []
    for content in all_content:
        concepts = extract_concepts(content)  # From CONCEITOS-CHAVE sections
        all_concepts.extend(concepts)

    # Deduplicate and prioritize concepts
    key_concepts = prioritize_concepts(all_concepts, limit=5)

    # Extract examples from all files
    all_examples = []
    for content in all_content:
        examples = extract_examples(content)  # From EXEMPLOS PRÁTICOS sections
        all_examples.extend(examples)

    # Choose best example (most specific, with metrics)
    best_example = select_best_example(all_examples)

    # Extract action steps from all files
    all_steps = []
    for content in all_content:
        steps = extract_steps(content)  # From COMO APLICAR sections
        all_steps.extend(steps)

    # Consolidate into 5-8 unique steps
    consolidated_steps = consolidate_steps(all_steps, limit=8)

    # Build lesson structure
    lesson = build_lesson_structure(
        topic=topic,
        concepts=key_concepts,
        example=best_example,
        steps=consolidated_steps,
        nivel=nivel
    )

    return lesson
```

---

### Step 4: Nivel Adaptation

```python
def adapt_to_nivel(lesson_content, target_nivel):
    """
    Adapt complexity to seller nivel
    """
    if target_nivel == "basico":
        # Simplify language
        lesson_content = simplify_vocabulary(lesson_content)

        # Add more examples
        lesson_content = add_extra_examples(lesson_content)

        # Break steps into smaller sub-steps
        lesson_content = expand_steps(lesson_content)

    elif target_nivel == "avancado":
        # Add advanced tactics
        lesson_content = add_advanced_tactics(lesson_content)

        # Include strategic context
        lesson_content = add_strategic_context(lesson_content)

        # Add optimization tips
        lesson_content = add_optimization_tips(lesson_content)

    # Intermediario = no adaptation (default structure)

    return lesson_content
```

---

## 📊 LESSON QUALITY CRITERIA

**A good lesson must have**:

- ✅ **Completeness**: All 6 sections present and filled
- ✅ **Practicality**: ≥5 executable action steps
- ✅ **Evidence**: ≥1 before/after example with metrics
- ✅ **Clarity**: Seller-friendly language (no jargon)
- ✅ **Relevance**: Brazilian marketplace examples (ML, Shopee, Magalu)
- ✅ **Actionability**: Immediate exercise seller can do now
- ✅ **Length**: 800-1200 words total

**Quality Check**:
```python
def validate_lesson(lesson_content):
    checks = {
        "all_sections": all(section in lesson_content for section in REQUIRED_SECTIONS),
        "min_steps": len(extract_steps(lesson_content)) >= 5,
        "has_example": "Exemplo Real" in lesson_content and "%" in lesson_content,
        "word_count": 800 <= len(lesson_content.split()) <= 1200,
        "has_exercise": "Exercício Prático" in lesson_content,
        "marketplace_specific": any(mp in lesson_content.lower() for mp in ["mercado livre", "shopee", "magalu"])
    }

    passed = all(checks.values())
    score = sum(checks.values()) / len(checks)

    return {
        "passed": passed,
        "score": score,
        "checks": checks
    }
```

---

## 📋 LESSON DELIVERY

**When lesson is ready**:

```markdown
# {TOPIC} | Aula ao Vivo

**Nível**: {nivel} | **Duração**: ~15 min leitura | **Tempo prática**: ~30 min

---

[6 sections content]

---

**Precisa de ajuda?** Digite:
- `/prime-mentor dúvida [sua pergunta]` - Esclarecer dúvida
- `/prime-mentor exemplo [contexto]` - Ver mais exemplos
- `/prime-anuncio` - Criar anúncio aplicando essa técnica

**Gostou?** Compartilhe com outros sellers! 🚀
```

---

## 🔄 MULTI-FILE SYNTHESIS EXAMPLE

**Request**: "Me ensina tudo sobre títulos no Mercado Livre"

**Discovery**:
```python
files_found = [
    "marketplace_titulos_otimizacao_20251110.md" (score: 3),
    "marketplace_seo_keywords_20251105.md" (score: 2),
    "copywriting_headlines_20251101.md" (score: 1),
    "marketplace_categorias_20251108.md" (score: 1)
]
# Read top 3 files
```

**Synthesis**:
- **Por que importa**: Extract from file 1 (títulos_otimizacao)
- **Pilares**: Merge concepts from files 1-3 (SEO + copywriting + categorias)
- **Como fazer**: Consolidate steps from all files into 6-step process
- **Exemplo Real**: Best example from file 1 (most specific, has metrics)
- **Exercício**: Create new exercise combining techniques from all files
- **Próximos Passos**: Link to related files (categorias, seo_keywords)

**Output**: Comprehensive 900-word lesson on ML titles (covers SEO + copy + categorization)

---

**Status**: Teaching mode module for mentor_agent
**Integration**: Called when seller requests lesson via "Me ensina..." pattern
**Performance**: Target <10s lesson generation from 3-5 source files