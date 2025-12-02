# AULA BUILDER - Live Lesson Generator

**Version**: 2.0.0
**Purpose**: Build structured lessons when seller requests "me ensina sobre X"
**Output**: Comprehensive, practical lesson in seller language

---

## WHEN TO USE

Trigger aula_builder when seller says:
- "Me ensina sobre [topic]"
- "Quero aprender [topic]"
- "Explica pra mim [topic]"
- "Como funciona [topic]?"

**NOT for simple questions** - use those for quick answers

---

## LESSON STRUCTURE

### Standard Template

```markdown
📚 AULA AO VIVO: [Título Atraente]

🎯 POR QUE ISSO IMPORTA?
[1-2 parágrafos sobre impacto no negócio do seller]

📖 OS [3-5] PILARES ESSENCIAIS
[Conceitos-chave explicados de forma prática]

🛠️ COMO FAZER (PASSO-A-PASSO)
[Instruções executáveis, não teoria]

💡 EXEMPLO REAL
[Caso prático de seller brasileiro]

✏️ EXERCÍCIO PRA VOCÊ
[Tarefa prática para aplicar no próprio negócio]

🔗 PRÓXIMOS PASSOS
[O que estudar depois]
```

---

## BUILDING PROCESS

### Step 1: Gather Knowledge

```python
def gather_knowledge_for_lesson(topic):
    # 1. Scout searches ALL related files (not just top 3)
    scout_results = scout_search_comprehensive(topic)

    # 2. Read up to 5 most relevant files
    knowledge_base = []
    for match in scout_results["matches"][:5]:
        content = read_file(f"PROCESSADOS/{match['arquivo']}")
        knowledge_base.append({
            "content": content,
            "metadata": match["arquivo_metadata"]
        })

    return knowledge_base
```

### Step 2: Extract Key Concepts

```python
def extract_concepts(knowledge_base):
    # Identify 3-5 most important concepts across all files

    concepts = []

    for knowledge in knowledge_base:
        # Parse markdown
        sections = parse_markdown_sections(knowledge["content"])

        # Extract from "CONCEITOS-CHAVE" section
        if "CONCEITOS-CHAVE" in sections:
            concepts.extend(sections["CONCEITOS-CHAVE"])

    # Deduplicate and prioritize
    unique_concepts = deduplicate_concepts(concepts)
    ranked_concepts = rank_by_importance(unique_concepts)

    return ranked_concepts[:5]  # Top 5
```

### Step 3: Build Step-by-Step Guide

```python
def build_steps(knowledge_base):
    # Synthesize actionable steps from multiple sources

    all_steps = []

    for knowledge in knowledge_base:
        sections = parse_markdown_sections(knowledge["content"])

        if "COMO APLICAR" in sections:
            all_steps.extend(sections["COMO APLICAR"])

    # Merge overlapping steps
    merged_steps = merge_similar_steps(all_steps)

    # Sequence logically
    sequenced = sequence_steps_logically(merged_steps)

    return sequenced
```

### Step 4: Select Best Example

```python
def select_best_example(knowledge_base):
    # Find most compelling example

    all_examples = []

    for knowledge in knowledge_base:
        sections = parse_markdown_sections(knowledge["content"])

        if "EXEMPLOS PRÁTICOS" in sections:
            all_examples.extend(sections["EXEMPLOS PRÁTICOS"])

    # Rank by:
    # - Has before/after
    # - Has concrete metrics
    # - Is Brazil-specific
    # - Is relatable to seller

    best_example = rank_examples(all_examples)[0]

    return best_example
```

### Step 5: Generate Exercise

```python
def generate_exercise(topic, concepts, steps):
    # Create practical exercise seller can do immediately

    exercise = {
        "intro": "Pega um produto seu agora e:",
        "tasks": []
    }

    # Transform key concepts into actionable tasks
    for i, concept in enumerate(concepts[:3]):
        task = convert_concept_to_task(concept, steps)
        exercise["tasks"].append(f"{i+1}. {task}")

    # Add measurement step
    exercise["tasks"].append("4. Testa por 7 dias")
    exercise["tasks"].append("5. Compara os resultados (antes vs depois)")

    return exercise
```

---

## SECTION TEMPLATES

### Por Que Isso Importa?

**Purpose**: Motivate seller to pay attention

**Template**:
```
[Hook: Impacto direto no negócio]

[Estatística concreta ou exemplo]

[Consequência de NÃO saber isso]
```

**Example**:
```
Seu texto é o vendedor que trabalha 24/7 pra você. Um copywriting bom pode aumentar sua conversão em 30-50%, sem gastar mais nada.

Sellers que dominam copy vendem 2-3x mais com o mesmo produto e preço.

Sem copy, você fica invisível no meio de milhares de anúncios iguais ao seu.
```

### Os 3-5 Pilares Essenciais

**Purpose**: Teach core concepts clearly

**Template per Pilar**:
```
**[Nome do Pilar]**: [Definição prática em 1 frase]

- [Sub-conceito 1]: [Explicação prática]
- [Sub-conceito 2]: [Explicação prática]
- [Exemplo curto inline]
```

**Example**:
```
**Pilar 1: Título SEO-Friendly**

Título é o primeiro filtro. Se não aparece na busca, não vende.

- Keywords: Palavras que o cliente digita ("masculina", "algodão")
- Atributos: Tamanho, cor, material (P-GG, azul, 100% algodão)
- Diferencial: O que te destaca ("entrega rápida", "premium")

Ex: "Camiseta Masculina Algodão Premium P-GG Azul Entrega Rápida"
```

### Como Fazer (Passo-a-Passo)

**Purpose**: Give executable instructions

**Template per Step**:
```
[Passo X] [Ação específica em linguagem imperativa]

- [Detalhe prático 1]
- [Detalhe prático 2]
- [Mini-exemplo inline]
```

**Example**:
```
[Passo 1] Pesquise keywords no buscador do marketplace

- Abra o ML/Shopee
- Digite a palavra-chave do seu produto
- Veja as sugestões que aparecem automaticamente
- Anote as 5 mais populares

Mini-exemplo: Se vende camiseta, digite "camiseta masculina" e veja o que completa

[Passo 2] Monte seu título usando o template

- Template: [PRODUTO] [MATERIAL] [DIFERENCIAL] [ATRIBUTOS]
- Preencha cada parte com suas keywords
- Confira se ficou dentro do limite (70 chars ML, 80 Shopee)

Mini-exemplo: "Camiseta Masculina Algodão Premium Malha Fria P-GG"
```

### Exemplo Real

**Purpose**: Show concrete before/after

**Template**:
```
**Contexto**: [Tipo de produto + marketplace + situação]

**Antes**:
[Situação problemática com detalhes]
- [Métrica ruim 1]
- [Métrica ruim 2]

**Depois**:
[Situação melhorada com detalhes]
- [O que mudou especificamente]

**Resultado**:
- [Métrica 1]: [Antes] → [Depois] (+X%)
- [Métrica 2]: [Antes] → [Depois] (+Y%)
- [Insight]: [Por que funcionou]
```

**Example**:
```
**Contexto**: Vendedor de camisetas masculinas no Mercado Livre, estava com 20 vendas/mês

**Antes**:
Título: "Camiseta Bonita"
Descrição: "Camiseta de algodão. Várias cores disponíveis."
- Cliques: 150/mês
- Conversão: 2.5%

**Depois**:
Título: "Camiseta Masculina Algodão Premium Malha Fria P-GG"
Descrição: "Mantenha-se fresco o dia todo com nossa camiseta de malha fria premium. Perfeita para o calor brasileiro! Algodão 100%, respirável. Tamanhos P ao GG. +500 vendidas!"
- Mudou: Keywords no título, benefícios na descrição, prova social

**Resultado**:
- Cliques: 150 → 240 (+60%)
- Conversão: 2.5% → 3.4% (+36%)
- Vendas: 20 → 34/mês (+70%)
- Insight: Título trouxe mais tráfego, descrição converteu melhor
```

### Exercício Pra Você

**Purpose**: Make seller apply immediately

**Template**:
```
[Intro: Ação inicial]

1. [Tarefa específica 1]
2. [Tarefa específica 2]
3. [Tarefa específica 3]
4. Testa por [X dias]
5. Mede resultado: [métricas específicas]

[Pergunta engajadora: "E aí, vai testar?"]
```

**Example**:
```
Pega um produto seu que tá vendendo pouco e:

1. Reescreve o título usando keywords que descobriu
2. Adiciona 3 gatilhos mentais na descrição (urgência, prova social, autoridade)
3. Melhora a primeira frase pra falar de BENEFÍCIO, não característica
4. Testa por 7 dias
5. Compara: cliques antes vs depois, conversão antes vs depois

Qual produto você vai melhorar primeiro?
```

### Próximos Passos

**Purpose**: Continue learning journey

**Template**:
```
Depois de dominar [topic atual], estude:

- [Tópico relacionado 1]: [Por que é relevante]
- [Tópico relacionado 2]: [Por que é relevante]
- [Tópico relacionado 3]: [Por que é relevante]

[Pergunta engajadora sobre qual caminho seguir]
```

**Example**:
```
Depois de dominar copywriting básico, estude:

- **Gatilhos Mentais Avançados**: Aprenda 10+ gatilhos além dos 3 básicos
- **A/B Testing**: Como testar variações e descobrir o que funciona
- **SEO Específico por Marketplace**: Cada um tem suas regras (ML ≠ Shopee)

Quer se aprofundar em qual desses primeiro?
```

---

## ADAPTIVE DIFFICULTY

### Detect Seller Level

Based on questions asked:

**Basic**:
- Asks "o que é X?"
- Never used technical terms
- Questions are broad

**Intermediate**:
- Asks "como fazer X?"
- Uses some terms correctly
- Questions are specific

**Advanced**:
- Asks "como otimizar X?"
- Uses technical terms
- Questions about edge cases

### Adapt Lesson Depth

**For Basic**:
- More explanation of concepts
- Simpler vocabulary
- More hand-holding in steps
- Very concrete examples

**For Intermediate**:
- Balance explanation and action
- Normal vocabulary
- Clear steps without over-explaining
- Practical examples

**For Advanced**:
- Less explanation, more techniques
- Technical terms OK
- Assume knowledge of basics
- Edge cases and optimizations

---

## QUALITY CHECKS

Before delivering lesson, validate:

- [ ] All sections present?
- [ ] Concepts are clear and practical?
- [ ] Steps are executable?
- [ ] Example has before/after/metrics?
- [ ] Exercise is doable immediately?
- [ ] Language is seller-friendly?
- [ ] No academic jargon?
- [ ] Brazil-specific examples?

---

## EXAMPLE OUTPUT

```markdown
📚 AULA AO VIVO: Copywriting para Marketplaces

🎯 POR QUE ISSO IMPORTA?

Seu texto é o vendedor que trabalha 24/7 pra você. Um copywriting bom pode aumentar sua conversão em 30-50%, sem gastar mais nada.

Sellers que dominam copy vendem 2-3x mais com o mesmo produto e preço. Sem copy, você fica invisível no meio de milhares de anúncios iguais.

📖 OS 3 PILARES ESSENCIAIS

1. **Título SEO-Friendly**: [detalhes...]
2. **Descrição Orientada a Benefícios**: [detalhes...]
3. **Gatilhos Mentais**: [detalhes...]

🛠️ COMO FAZER (PASSO-A-PASSO)

[Passo 1] Pesquise keywords: [detalhes...]
[Passo 2] Monte título: [detalhes...]
[Passo 3] Escreva descrição: [detalhes...]

💡 EXEMPLO REAL

Contexto: [detalhes...]
Antes: [detalhes...]
Depois: [detalhes...]
Resultado: [métricas...]

✏️ EXERCÍCIO PRA VOCÊ

Pega um produto seu e:
1. [tarefa...]
2. [tarefa...]
3. [tarefa...]

🔗 PRÓXIMOS PASSOS

- Gatilhos Mentais Avançados
- A/B Testing
- SEO Específico

Quer se aprofundar em qual?
```

---

**END OF AULA BUILDER**

**Remember**: Lessons should empower sellers to act immediately. Theory without practice is useless. Always end with actionable exercise.

**Version**: 2.0.0
**Last Updated**: 2025-11-13
