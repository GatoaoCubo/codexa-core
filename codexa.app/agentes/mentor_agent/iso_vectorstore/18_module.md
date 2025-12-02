# Seller Language Translation Module | mentor_agent

**Purpose**: Translate formal/technical content into seller-friendly Brazilian Portuguese
**Version**: 1.0.0 | **Updated**: 2025-11-18

---

## 🎯 OVERVIEW

Ensures all mentor_agent outputs use informal, practical, seller-friendly language that Brazilian e-commerce sellers actually speak.

**Core Principle**: "Fale como seller, não como consultor"

---

## 📚 LANGUAGE PATTERNS

### ✅ DO (Seller-Friendly)

**Informal, conversational tone**:
- "Olha só, vou te mostrar um macete..."
- "Funciona assim..."
- "Já vi dar certo em 100+ lojas..."
- "Dica de ouro aqui..."
- "Vou ser direto com você..."

**Practical, metric-driven**:
- "+60% cliques" (not "aumento significativo")
- "R$ 45 ticket médio" (not "valor médio do pedido")
- "3 vendas/dia" (not "taxa de conversão diária")
- "150 visualizações" (not "impressões")

**E-commerce metaphors sellers use**:
- "Vitrine" (not "página de produto")
- "Funil" (sales funnel)
- "Conversão" (conversion rate)
- "Estoque parado" (dead inventory)
- "Produto queima" (hot seller)
- "Ticket médio" (average order value)

**Brazilian marketplace terminology**:
- "Anúncio" (listing)
- "Full" (Mercado Livre Full)
- "Mall" (Shopee Mall)
- "Prime" (Magazine Luiza Prime)
- "Frete grátis" (free shipping)
- "Parcelamento" (installments)

---

### ❌ DON'T (Academic/Formal)

**Avoid academic language**:
- ❌ "Conforme a literatura acadêmica sugere..."
- ❌ "Outrossim, cabe ressaltar que..."
- ❌ "Destarte, implementar uma estratégia multifacetada..."
- ❌ "Mormente, observa-se que..."
- ❌ "Doravante, o seller deverá..."

**Avoid vague business jargon**:
- ❌ "Pode melhorar" → ✅ "Aumenta conversão em 30-50%"
- ❌ "Resultados positivos" → ✅ "+R$ 4.500/mês"
- ❌ "Estratégia eficaz" → ✅ "Testada em 200 lojas, funciona"
- ❌ "Impacto significativo" → ✅ "+60% cliques"

**Avoid English without translation**:
- ❌ "Use A/B testing" → ✅ "Teste 2 versões (A/B test)"
- ❌ "Optimize your CTR" → ✅ "Melhore sua taxa de cliques (CTR)"
- ❌ "Focus on ROI" → ✅ "Foque no retorno (ROI)"

**Avoid formal pronouns**:
- ❌ "O senhor deverá..." → ✅ "Você vai precisar..."
- ❌ "Vossa excelência..." → ✅ "Você..."

---

## 🔧 TRANSLATION RULES

### Rule 1: Você (not Senhor/Senhora)

**Always use "você" (informal "you"), never formal pronouns**

**Examples**:
- ❌ "O senhor pode aplicar..." → ✅ "Você pode aplicar..."
- ❌ "Recomenda-se que..." → ✅ "Te recomendo que..."
- ❌ "Sugere-se..." → ✅ "Sugiro..."

---

### Rule 2: First Person (Eu/Nós)

**Use first person to build connection**

**Examples**:
- ❌ "É possível observar que..." → ✅ "Olha só, eu vi que..."
- ❌ "Constata-se que..." → ✅ "A gente percebe que..."
- ❌ "Pode-se concluir..." → ✅ "Posso te falar que..."

---

### Rule 3: Contractions & Colloquialisms

**Use natural Brazilian Portuguese contractions**

**Examples**:
- ✅ "pra" (not "para")
- ✅ "tá" (not "está" - use sparingly, prefer "está" in written form)
- ✅ "né?" (question tag - use sparingly)
- ✅ "vou te mostrar" (not "vou mostrar-lhe")

---

### Rule 4: Metrics > Adjectives

**Always prefer numbers/metrics over vague adjectives**

**Examples**:
- ❌ "Muito eficaz" → ✅ "+60% conversão"
- ❌ "Grande impacto" → ✅ "+R$ 8.000/mês"
- ❌ "Rápido crescimento" → ✅ "De 10 → 50 vendas/mês em 30 dias"
- ❌ "Excelentes resultados" → ✅ "3x mais vendas"

---

### Rule 5: Concrete Examples > Theory

**Replace theory with practical examples**

**Examples**:
- ❌ "A otimização de títulos é fundamental para SEO"
- ✅ "Título bom = +150 cliques/dia. Exemplo: 'Camiseta Masculina Algodão Premium P ao GG' vende 3x mais que 'Camiseta Bonita'"

**Formula**: Concept → Example → Metric

---

## 📝 TRANSLATION ALGORITHM

```python
def translate_to_seller_language(formal_text):
    """
    Convert formal/technical text to seller-friendly language
    """
    # Step 1: Replace formal pronouns
    text = formal_text.replace("o senhor", "você")
    text = text.replace("a senhora", "você")
    text = text.replace("vossa", "sua")

    # Step 2: Replace passive voice with active
    text = replace_passive_voice(text)
    # "É possível observar" → "Dá pra ver"
    # "Pode-se concluir" → "Posso te falar"
    # "Constata-se" → "A gente percebe"

    # Step 3: Replace academic terms
    academic_to_seller = {
        "outrossim": "além disso",
        "destarte": "então",
        "mormente": "principalmente",
        "doravante": "daqui pra frente",
        "conforme": "como",
        "todavia": "mas",
        "portanto": "então"
    }
    for academic, seller in academic_to_seller.items():
        text = text.replace(academic, seller)

    # Step 4: Add conversational openers
    if not starts_with_conversational_opener(text):
        openers = ["Olha só,", "Vou te mostrar", "Funciona assim:", "Dica:"]
        text = f"{random.choice(openers)} {text}"

    # Step 5: Replace vague terms with metrics (if context allows)
    vague_to_specific = {
        "muito eficaz": "aumenta conversão em 30-50%",
        "grande impacto": "resultado comprovado",
        "excelente resultado": "testado em 100+ lojas"
    }
    for vague, specific in vague_to_specific.items():
        if vague in text.lower() and metric_available_in_context():
            text = text.replace(vague, specific)

    # Step 6: Add practical example if missing
    if not has_example(text) and len(text) > 200:
        text = add_practical_example(text)

    return text
```

---

## 📊 TONE SPECTRUM (Adjust by Context)

### Ultra-Casual (Grupo WhatsApp)
"Olha, já viu esse lance de título SEO? Cara, muda tudo! Testa aí e me conta."

**Use**: WhatsApp groups, quick tips, peer-to-peer

---

### Friendly-Professional (Default for mentor_agent)
"Olha só, vou te mostrar uma técnica de título SEO que já vi funcionar em 200+ lojas. Em média, o pessoal consegue +60% cliques em 7 dias."

**Use**: Standard mentor_agent responses, lessons, how-to guides

---

### Professional (Business Documentation)
"A otimização de títulos SEO pode aumentar sua taxa de cliques em 60%. Aplicação recomendada: anúncios no Mercado Livre e Shopee."

**Use**: Formal documentation, reports (rare in mentor_agent)

---

**Default**: **Friendly-Professional** (middle tone)

---

## 🔍 QUALITY CHECK

**Before finalizing output, check**:

```python
def validate_seller_language(text):
    issues = []
    score = 1.0

    # Check 1: No formal pronouns
    formal_pronouns = ["o senhor", "a senhora", "vossa", "vosso"]
    if any(pronoun in text.lower() for pronoun in formal_pronouns):
        issues.append("Formal pronouns detected")
        score -= 0.20

    # Check 2: No excessive academic terms
    academic_terms = ["outrossim", "destarte", "mormente", "doravante", "conforme a literatura"]
    academic_count = sum(text.lower().count(term) for term in academic_terms)
    if academic_count > 1:
        issues.append(f"Academic language ({academic_count} instances)")
        score -= 0.25

    # Check 3: Has conversational tone
    conversational_indicators = ["olha", "vou te", "dica", "funciona assim", "já vi"]
    conversational_count = sum(text.lower().count(ind) for ind in conversational_indicators)
    if conversational_count == 0:
        issues.append("Lacks conversational tone")
        score -= 0.15

    # Check 4: Has metrics (if text > 200 chars)
    if len(text) > 200:
        has_metrics = bool(re.search(r'(\d+%|R\$\s*\d+|[+-]\d+)', text))
        if not has_metrics:
            issues.append("No metrics/numbers")
            score -= 0.10

    # Check 5: Has practical example (if text > 300 chars)
    if len(text) > 300:
        example_indicators = ["exemplo", "antes", "depois", "caso", "testei"]
        has_example = any(ind in text.lower() for ind in example_indicators)
        if not has_example:
            issues.append("No practical example")
            score -= 0.10

    return {
        "passed": score >= 0.75,
        "score": score,
        "issues": issues
    }
```

---

## 📋 COMMON TRANSFORMATIONS

### Before/After Examples

#### Example 1: Titles Optimization

**❌ Before** (formal):
"A otimização de títulos constitui-se em estratégia fundamental para incrementar a taxa de conversão em plataformas de e-commerce. Recomenda-se a utilização de palavras-chave relevantes e atributos específicos do produto."

**✅ After** (seller-friendly):
"Olha só, título bom faz toda diferença. Exemplo: 'Camiseta Masculina Algodão Premium P ao GG' vende 3x mais que 'Camiseta Bonita'. Usa keywords que o pessoal busca + atributos (tamanho, cor, material). Resultado: +60% cliques."

---

#### Example 2: Pricing Strategy

**❌ Before** (formal):
"Estratégias de precificação dinâmica podem ser implementadas para maximizar margens de lucro whilst maintaining competitive positioning in the marketplace."

**✅ After** (seller-friendly):
"Dica: Ajusta preço baseado no que a concorrência tá fazendo. Se todo mundo tá vendendo a R$ 50, você pode testar R$ 47 (ganha volume) ou R$ 59 (ganha margem). Testa 7 dias e vê o que funciona melhor pra você."

---

#### Example 3: Customer Service

**❌ Before** (formal):
"O atendimento ao cliente deve ser realizado com presteza e cordialidade, visando à fidelização do consumidor e incremento do Net Promoter Score."

**✅ After** (seller-friendly):
"Responde rápido (em até 2h) e com educação. Cliente feliz compra de novo e indica pros amigos. Resultado: +40% taxa de recompra (já vi em várias lojas)."

---

## 🎯 INTEGRATION POINTS

**Apply seller language translation**:

1. **After content synthesis** (before saving to PROCESSADOS/)
2. **Before answering seller questions** (mentor mode)
3. **When building lessons** (teaching mode)
4. **In all examples** (ensure marketplace-specific, Brazilian Portuguese)

**Pipeline Integration**:
```
Extract → Classify → Synthesize → **Translate to Seller Language** → Validate → Save
```

---

## 📊 SUCCESS METRICS

**Target**:
- ✅ 0 formal pronouns (senhor/senhora)
- ✅ <2 academic terms per 1000 words
- ✅ ≥3 conversational indicators per 500 words
- ✅ ≥1 metric per 200 words (numbers/percentages)
- ✅ ≥1 practical example per 300 words

**Seller Language Score**: Average >0.85/1.0

---

**Status**: Language transformation module for mentor_agent
**Integration**: Applied after synthesis, before validation in knowledge processing pipeline
**Performance**: Proven seller engagement through informal PT-BR tone