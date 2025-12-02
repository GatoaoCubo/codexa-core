# Classification Module | mentor_agent

**Purpose**: Auto-detect categoria, assunto, nível, tags from extracted content
**Version**: 1.0.0 | **Updated**: 2025-11-18

---

## 🎯 OVERVIEW

Second stage of the 4-stage knowledge processing pipeline. Analyzes extracted text to classify content into mentor_agent's 10-category taxonomy with metadata enrichment.

**Pipeline Position**: Extract → **Classify** → Synthesize → Validate

---

## 📊 10 KNOWLEDGE CATEGORIES

### 1. marketplace_optimization
**Focus**: Marketplace-specific tactics (titles, SEO, conversion, platform rules)
**Assuntos**: titulos_seo, fotos_produto, descricoes, categorias, badges, anuncios_premium
**Keywords**: mercadolivre, shopee, magalu, amazon, seo, titulo, conversão, anuncio

### 2. copywriting
**Focus**: Persuasive writing, mental triggers, ad copy
**Assuntos**: gatilhos_mentais, headlines, cta, storytelling, prova_social, objecoes
**Keywords**: copywriting, persuasão, gatilho, headline, cta, conversão

### 3. estrategia_produto
**Focus**: Product selection, pricing, positioning, validation
**Assuntos**: selecao_produto, precificacao, posicionamento, validacao_mercado, nicho
**Keywords**: produto, nicho, preço, margem, validação, dropshipping, arbitragem

### 4. analise_concorrencia
**Focus**: Competitive intelligence, benchmarking, differentiation
**Assuntos**: pesquisa_concorrentes, benchmarking, diferenciais, gaps_mercado
**Keywords**: concorrente, benchmark, diferenciação, gap, análise competitiva

### 5. compliance_legal
**Focus**: Brazilian regulations (ANVISA, INMETRO, CONAR, consumer law)
**Assuntos**: anvisa, inmetro, conar, defesa_consumidor, notas_fiscais, impostos
**Keywords**: anvisa, inmetro, regulamentação, compliance, legal, fiscal

### 6. branding
**Focus**: Brand identity, archetypes, storytelling, visual identity
**Assuntos**: identidade_visual, arquetipos, naming, storytelling, posicionamento_marca
**Keywords**: marca, branding, identidade, arquétipo, storytelling, logo

### 7. visual_design
**Focus**: Product photography, mockups, layouts, Canva/Photoshop
**Assuntos**: fotografia_produto, mockups, layouts, design_grafico, cores_tipografia
**Keywords**: design, foto, mockup, layout, canva, photoshop, visual

### 8. customer_experience
**Focus**: Customer service, post-sales, retention, reviews
**Assuntos**: atendimento, pos_venda, fidelizacao, reviews, sac, nps
**Keywords**: atendimento, cliente, pós-venda, fidelização, experiência, sac

### 9. operacoes_logistica
**Focus**: Inventory, shipping, fulfillment, suppliers
**Assuntos**: estoque, envio, fornecedores, fulfillment, logistica_reversa
**Keywords**: estoque, logística, envio, fornecedor, fulfillment, armazenagem

### 10. financeiro_precificacao
**Focus**: Pricing models, margins, costs, financial planning
**Assuntos**: margem, custos, precificacao_dinamica, fluxo_caixa, roi
**Keywords**: preço, margem, custo, roi, lucro, financeiro

---

## 🔍 CLASSIFICATION ALGORITHM

### Step 1: Categoria Detection (Primary Classification)

**Method**: Keyword frequency + semantic analysis

```python
def detect_categoria(text):
    categoria_scores = {}

    # Count keyword matches per category
    for categoria, keywords in CATEGORIA_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            # Case-insensitive, whole word match
            matches = len(re.findall(rf'\b{keyword}\b', text, re.I))
            score += matches

        # Normalize by text length
        categoria_scores[categoria] = score / (len(text) / 1000)

    # Get top category
    top_categoria = max(categoria_scores, key=categoria_scores.get)
    confidence = categoria_scores[top_categoria] / sum(categoria_scores.values())

    return {
        "categoria": top_categoria,
        "confidence": confidence,
        "scores": categoria_scores
    }
```

**Confidence Thresholds**:
- **High** (>0.60): Clear category match
- **Medium** (0.40-0.60): Mixed signals, likely multi-category
- **Low** (<0.40): Ambiguous, may need manual review

---

### Step 2: Assunto Detection (Secondary Classification)

**Method**: Extract specific topic within categoria

```python
def detect_assunto(text, categoria):
    # Get assunto keywords for detected categoria
    assunto_keywords = ASSUNTO_MAP[categoria]

    assunto_scores = {}
    for assunto, keywords in assunto_keywords.items():
        score = sum(text.lower().count(kw) for kw in keywords)
        assunto_scores[assunto] = score

    # Get top assunto
    if max(assunto_scores.values()) > 0:
        top_assunto = max(assunto_scores, key=assunto_scores.get)
        return top_assunto
    else:
        # Default assunto if none detected
        return f"{categoria}_geral"
```

**Examples**:
- **Categoria**: marketplace_optimization → **Assunto**: titulos_seo
- **Categoria**: copywriting → **Assunto**: gatilhos_mentais
- **Categoria**: branding → **Assunto**: arquetipos

---

### Step 3: Nível Detection (Complexity Level)

**Method**: Analyze vocabulary complexity + instructional depth

```python
def detect_nivel(text):
    nivel_indicators = {
        "basico": ["iniciante", "começar", "básico", "introdução", "primeiro passo", "o que é"],
        "intermediario": ["estratégia", "otimizar", "melhorar", "avançar", "técnica", "implementar"],
        "avancado": ["avançado", "expert", "complexo", "análise profunda", "framework", "sistema"]
    }

    scores = {}
    for nivel, indicators in nivel_indicators.items():
        score = sum(text.lower().count(ind) for ind in indicators)
        scores[nivel] = score

    # Check complexity metrics
    avg_sentence_length = len(text.split()) / len(text.split('.'))
    if avg_sentence_length > 25:
        scores["avancado"] += 2
    elif avg_sentence_length < 15:
        scores["basico"] += 2

    # Determine level
    if max(scores.values()) == 0:
        return "intermediario"  # Default
    else:
        return max(scores, key=scores.get)
```

**Level Definitions**:
- **Básico**: Foundational concepts, step-by-step, beginner-friendly (80% of sellers)
- **Intermediário**: Tactical execution, optimization, some experience needed (15% of sellers)
- **Avançado**: Strategic frameworks, advanced tactics, expert-level (5% of sellers)

---

### Step 4: Tags Extraction

**Method**: Extract contextual keywords for search/filtering

```python
def extract_tags(text, categoria, assunto):
    # Start with categoria/assunto as base tags
    tags = [categoria.split('_')[0], assunto.split('_')[0]]

    # Add marketplace tags if mentioned
    marketplaces = ["mercadolivre", "shopee", "magalu", "amazon", "americanas", "casasbahia"]
    for marketplace in marketplaces:
        if marketplace in text.lower():
            tags.append(marketplace)

    # Add common tactical tags
    tactical_keywords = {
        "seo": ["seo", "palavra-chave", "keyword", "busca organica"],
        "conversao": ["conversão", "taxa de conversão", "cvr", "converter"],
        "trafego": ["tráfego", "visitantes", "cliques", "impressões"],
        "preco": ["preço", "precificação", "margem", "desconto"],
        "foto": ["foto", "imagem", "fotografia", "visual"]
    }

    for tag_name, keywords in tactical_keywords.items():
        if any(kw in text.lower() for kw in keywords):
            tags.append(tag_name)

    # Remove duplicates, limit to 8 tags
    tags = list(set(tags))[:8]

    return tags
```

**Tag Examples**:
- marketplace_optimization + titulos_seo → ["marketplace", "titulos", "mercadolivre", "seo", "conversao"]
- copywriting + gatilhos_mentais → ["copywriting", "gatilhos", "persuasao", "conversao"]

---

### Step 5: Aplicação Detection (Use Case)

**Method**: Identify when/where seller would apply this knowledge

```python
def detect_aplicacao(text, categoria):
    aplicacao_patterns = {
        "quando_criar_anuncios": ["criar anuncio", "novo produto", "cadastrar produto", "listar produto"],
        "quando_otimizar_conversao": ["aumentar conversão", "melhorar vendas", "otimizar", "cvr baixo"],
        "quando_precificar": ["definir preço", "precificar", "calcular margem", "preço competitivo"],
        "quando_responder_cliente": ["atendimento", "responder cliente", "dúvida", "reclamação"],
        "quando_analisar_concorrencia": ["analisar concorrente", "benchmark", "pesquisa de mercado"],
        "quando_escolher_produto": ["selecionar produto", "validar nicho", "produto vencedor"],
        "quando_criar_marca": ["criar marca", "identidade visual", "naming", "logo"],
        "quando_fotografar": ["tirar foto", "fotografia", "imagem produto", "mockup"],
        "quando_cumprir_regulamentos": ["anvisa", "inmetro", "regulamentação", "compliance"],
        "quando_gerenciar_estoque": ["estoque", "reposição", "fornecedor", "logística"]
    }

    for aplicacao, patterns in aplicacao_patterns.items():
        if any(pattern in text.lower() for pattern in patterns):
            return aplicacao

    # Default based on categoria
    categoria_defaults = {
        "marketplace_optimization": "quando_criar_anuncios",
        "copywriting": "quando_criar_anuncios",
        "estrategia_produto": "quando_escolher_produto",
        "analise_concorrencia": "quando_analisar_concorrencia",
        "compliance_legal": "quando_cumprir_regulamentos",
        "branding": "quando_criar_marca",
        "visual_design": "quando_fotografar",
        "customer_experience": "quando_responder_cliente",
        "operacoes_logistica": "quando_gerenciar_estoque",
        "financeiro_precificacao": "quando_precificar"
    }

    return categoria_defaults.get(categoria, "geral")
```

---

## 🎯 CLASSIFICATION OUTPUT

**Expected structure**:

```json
{
  "categoria": "marketplace_optimization",
  "assunto": "titulos_seo",
  "nivel": "intermediario",
  "tags": ["marketplace", "titulos", "mercadolivre", "seo", "conversao"],
  "aplicacao": "quando_criar_anuncios",
  "confidence": {
    "categoria": 0.78,
    "overall": 0.85
  },
  "metadata": {
    "text_length": 15420,
    "detected_marketplaces": ["mercadolivre", "shopee"],
    "complexity_score": "medium"
  }
}
```

---

## 📋 CLASSIFICATION VALIDATION

**Quality checks before proceeding**:

```python
def validate_classification(classification):
    issues = []

    # Check categoria is valid
    if classification["categoria"] not in VALID_CATEGORIAS:
        issues.append(f"Invalid categoria: {classification['categoria']}")

    # Check confidence threshold
    if classification["confidence"]["categoria"] < 0.30:
        issues.append("Low categoria confidence (< 30%)")

    # Check tags not empty
    if len(classification["tags"]) < 2:
        issues.append("Insufficient tags (< 2)")

    # Check nivel is valid
    if classification["nivel"] not in ["basico", "intermediario", "avancado"]:
        issues.append(f"Invalid nivel: {classification['nivel']}")

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "confidence": classification["confidence"]["overall"]
    }
```

---

## 🔄 MULTI-CATEGORY HANDLING

**If content spans multiple categories** (confidence <0.60):

**Option 1**: Choose primary + add secondary tag
```python
if categoria_confidence < 0.60:
    # Get top 2 categories
    top_2 = sorted(categoria_scores.items(), key=lambda x: x[1], reverse=True)[:2]
    primary = top_2[0][0]
    secondary = top_2[1][0]

    classification["categoria"] = primary
    classification["tags"].append(f"tb_{secondary}")  # "tb" = também
```

**Option 2**: Create as multi-category
```python
classification["categoria"] = f"{primary}_{secondary}"
# Example: "marketplace_copywriting" (titles + persuasion)
```

---

## 📊 CLASSIFICATION ACCURACY

**Expected Performance**:
- Categoria accuracy: >85% (tested on conhecimento_agent 66k+ cards)
- Assunto accuracy: >75%
- Tags relevance: >80%
- Overall confidence: >0.75 average

**Common Misclassifications**:
- marketplace_optimization ↔ copywriting (overlapping SEO/copy tactics)
- estrategia_produto ↔ analise_concorrencia (product research overlap)
- branding ↔ visual_design (brand identity + design overlap)

**Resolution**: Use multi-category tagging or manual review for confidence <0.50

---

## 📋 CLASSIFICATION CHECKLIST

Before moving to Synthesis stage:

- [ ] Categoria detected with confidence >0.40
- [ ] Assunto extracted (specific topic within categoria)
- [ ] Nível determined (básico/intermediário/avançado)
- [ ] Tags generated (≥2 relevant tags)
- [ ] Aplicação identified (when to use this knowledge)
- [ ] Validation passed (no critical issues)
- [ ] Metadata logged (confidence scores, detected entities)

---

**Status**: Stage 2 of knowledge processing pipeline
**Integration**: Called by knowledge_processor_HOP after extraction, before synthesis
**Performance**: Target <2s per classification (NLP + pattern matching)