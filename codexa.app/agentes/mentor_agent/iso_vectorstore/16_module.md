# Quality Validation Module (5D) | mentor_agent

**Purpose**: 5-dimension quality validation (completeness, clarity, accuracy, relevance, actionability)
**Version**: 1.0.0 | **Updated**: 2025-11-18

---

## 🎯 OVERVIEW

Fourth stage of the 4-stage knowledge processing pipeline. Validates synthesized content against 5 quality dimensions before saving to PROCESSADOS/.

**Pipeline Position**: Extract → Classify → Synthesize → **Validate**

**Proven at Scale**: 97.5% quality rate on 66,105 cards (conhecimento_agent)

---

## 📊 5 QUALITY DIMENSIONS

### 1. Completeness (Fullness)

**Definition**: All required sections present and filled

**Required Sections**:
- ✅ Title (clear, descriptive)
- ✅ Metadata (categoria, assunto, nível, tags, aplicação)
- ✅ RESUMO EXECUTIVO (1-2 paragraphs)
- ✅ CONCEITOS-CHAVE (3-5 key concepts)
- ✅ COMO APLICAR (3-5 action steps)
- ✅ EXEMPLOS PRÁTICOS (≥1 before/after example with metrics)
- ✅ QUANDO USAR (situational guidance)

**Validation Logic**:
```python
def validate_completeness(content):
    required_sections = [
        "RESUMO EXECUTIVO",
        "CONCEITOS-CHAVE",
        "COMO APLICAR",
        "EXEMPLOS PRÁTICOS",
        "QUANDO USAR"
    ]

    score = 0
    missing = []

    for section in required_sections:
        if section in content:
            # Check section has content (not just heading)
            section_text = extract_section(content, section)
            if len(section_text) > 50:  # Minimum 50 chars
                score += 1
            else:
                missing.append(f"{section} (too short)")
        else:
            missing.append(section)

    completeness_score = score / len(required_sections)

    return {
        "dimension": "completeness",
        "score": completeness_score,
        "missing": missing,
        "passed": completeness_score >= 0.75
    }
```

**Thresholds**:
- ✅ Pass: ≥75% (≥4/5 sections complete)
- ⚠️ Marginal: 60-74% (3/5 sections)
- ❌ Fail: <60% (≤2/5 sections)

---

### 2. Clarity (Readability)

**Definition**: Content is clear, seller-friendly, no jargon, easy to understand

**Validation Criteria**:
- Short sentences (avg <20 words)
- No academic language
- Brazilian Portuguese informal tone
- Clear structure (bullet points, numbered lists)
- No excessive technical terms without explanation

**Validation Logic**:
```python
def validate_clarity(content):
    issues = []
    score = 1.0

    # Check average sentence length
    sentences = content.split('.')
    avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
    if avg_sentence_length > 25:
        score -= 0.15
        issues.append(f"Long sentences (avg {avg_sentence_length:.1f} words)")

    # Check for academic jargon
    academic_terms = ["conforme", "outrossim", "destarte", "mormente", "doravante"]
    jargon_count = sum(content.lower().count(term) for term in academic_terms)
    if jargon_count > 2:
        score -= 0.20
        issues.append(f"Academic language detected ({jargon_count} instances)")

    # Check for structure (lists, bullet points)
    has_lists = bool(re.search(r'(^-|\n-|\d\.)', content, re.M))
    if not has_lists:
        score -= 0.10
        issues.append("No structured lists (bullets/numbers)")

    # Check for seller-friendly language
    friendly_indicators = ["olha só", "vou te mostrar", "funciona assim", "dica"]
    friendly_count = sum(content.lower().count(ind) for ind in friendly_indicators)
    if friendly_count == 0:
        score -= 0.10
        issues.append("Lacks seller-friendly tone")

    return {
        "dimension": "clarity",
        "score": max(0, score),
        "issues": issues,
        "passed": score >= 0.75
    }
```

**Thresholds**:
- ✅ Pass: ≥75% (clear, structured, seller-friendly)
- ⚠️ Marginal: 60-74% (some jargon or complexity)
- ❌ Fail: <60% (academic tone, hard to read)

---

### 3. Accuracy (Factual Correctness)

**Definition**: Information is factually correct, Brazil-specific, marketplace-accurate

**Validation Criteria**:
- Brazilian marketplace names correct (Mercado Livre, not MercadoLibre)
- Pricing in BRL (R$), not USD
- Regulations cited correctly (ANVISA, INMETRO, CONAR)
- No contradictory statements
- Dates/numbers/metrics are plausible

**Validation Logic**:
```python
def validate_accuracy(content):
    issues = []
    score = 1.0

    # Check for USD instead of BRL
    if re.search(r'\$\d+(?!\s*R)', content):
        score -= 0.15
        issues.append("USD detected (should use R$ for Brazil)")

    # Check marketplace names
    incorrect_names = ["MercadoLibre", "MercadoLivre", "Shoppee", "Magagine"]
    for name in incorrect_names:
        if name in content:
            score -= 0.10
            issues.append(f"Incorrect marketplace name: {name}")

    # Check for contradictions (basic heuristic)
    if "não funciona" in content and "funciona bem" in content:
        score -= 0.20
        issues.append("Potential contradiction detected")

    # Check regulation names
    if "anvisa" in content.lower():
        if "AVISA" in content:  # Common typo
            score -= 0.05
            issues.append("ANVISA misspelled")

    # Check for unrealistic metrics
    unrealistic_patterns = [
        r'(\d{3,})%',  # >100% growth
        r'R\$\s*\d{7,}',  # R$ millions (unlikely for SMB sellers)
    ]
    for pattern in unrealistic_patterns:
        if re.search(pattern, content):
            score -= 0.10
            issues.append(f"Unrealistic metric detected: {pattern}")

    return {
        "dimension": "accuracy",
        "score": max(0, score),
        "issues": issues,
        "passed": score >= 0.75
    }
```

**Thresholds**:
- ✅ Pass: ≥75% (no major errors)
- ⚠️ Marginal: 60-74% (minor errors, typos)
- ❌ Fail: <60% (factual errors, contradictions)

---

### 4. Relevance (Seller Usefulness)

**Definition**: Content is relevant to Brazilian e-commerce sellers' daily work

**Validation Criteria**:
- Marketplace-specific (ML, Shopee, Magalu, Amazon BR)
- Tactical (not just theory)
- Brazil-specific (not US/global generic advice)
- Addresses seller pain points
- Includes seller use cases

**Validation Logic**:
```python
def validate_relevance(content):
    issues = []
    score = 1.0

    # Check for Brazilian marketplaces
    br_marketplaces = ["mercado livre", "shopee", "magalu", "magazine luiza", "amazon"]
    marketplace_mentions = sum(content.lower().count(mp) for mp in br_marketplaces)
    if marketplace_mentions == 0:
        score -= 0.25
        issues.append("No Brazilian marketplace examples")

    # Check for actionable keywords
    tactical_keywords = ["como fazer", "passo a passo", "exemplo", "dica", "estratégia"]
    tactical_count = sum(content.lower().count(kw) for kw in tactical_keywords)
    if tactical_count < 2:
        score -= 0.20
        issues.append("Lacks tactical/actionable content")

    # Check for seller pain points
    pain_point_keywords = ["aumentar vendas", "conversão", "tráfego", "anuncio", "produto"]
    pain_mentions = sum(content.lower().count(kw) for kw in pain_point_keywords)
    if pain_mentions == 0:
        score -= 0.15
        issues.append("Doesn't address seller pain points")

    # Check for theoretical/academic focus (negative signal)
    theory_keywords = ["teoria", "fundamentos teóricos", "literatura acadêmica"]
    theory_count = sum(content.lower().count(kw) for kw in theory_keywords)
    if theory_count > 1:
        score -= 0.20
        issues.append("Too theoretical, not practical enough")

    return {
        "dimension": "relevance",
        "score": max(0, score),
        "issues": issues,
        "passed": score >= 0.75
    }
```

**Thresholds**:
- ✅ Pass: ≥75% (highly relevant, marketplace-specific)
- ⚠️ Marginal: 60-74% (somewhat relevant, generic)
- ❌ Fail: <60% (theoretical, not seller-focused)

---

### 5. Actionability (Executable Steps)

**Definition**: Content provides concrete, executable actions sellers can take immediately

**Validation Criteria**:
- Step-by-step instructions
- Before/after examples with metrics
- Specific actions (not vague advice)
- Tools/resources mentioned
- Timeframes indicated

**Validation Logic**:
```python
def validate_actionability(content):
    issues = []
    score = 1.0

    # Check for numbered steps
    numbered_steps = len(re.findall(r'^\d+\.', content, re.M))
    if numbered_steps < 3:
        score -= 0.20
        issues.append(f"Insufficient action steps ({numbered_steps} found, need ≥3)")

    # Check for before/after examples
    has_before_after = bool(re.search(r'(antes|before).*?(depois|after)', content, re.I))
    if not has_before_after:
        score -= 0.15
        issues.append("No before/after example")

    # Check for metrics
    has_metrics = bool(re.search(r'(\d+%|R\$\s*\d+|\d+x)', content))
    if not has_metrics:
        score -= 0.15
        issues.append("No quantitative metrics/results")

    # Check for vague language (negative signal)
    vague_terms = ["pode melhorar", "talvez", "eventualmente", "possivelmente"]
    vague_count = sum(content.lower().count(term) for term in vague_terms)
    if vague_count > 2:
        score -= 0.15
        issues.append(f"Vague language detected ({vague_count} instances)")

    # Check for specific tools/resources
    tool_keywords = ["canva", "photoshop", "excel", "planilha", "ferramenta", "app"]
    tool_mentions = sum(content.lower().count(kw) for kw in tool_keywords)
    if tool_mentions == 0:
        score -= 0.10
        issues.append("No specific tools/resources mentioned")

    return {
        "dimension": "actionability",
        "score": max(0, score),
        "issues": issues,
        "passed": score >= 0.75
    }
```

**Thresholds**:
- ✅ Pass: ≥75% (highly actionable, concrete steps)
- ⚠️ Marginal: 60-74% (some actions, but vague)
- ❌ Fail: <60% (theoretical, no executable steps)

---

## 📊 OVERALL QUALITY SCORE

**Calculation**:
```python
def calculate_overall_quality(dimensions):
    """
    dimensions = {
        "completeness": {"score": 0.85, "passed": True},
        "clarity": {"score": 0.78, "passed": True},
        "accuracy": {"score": 0.92, "passed": True},
        "relevance": {"score": 0.81, "passed": True},
        "actionability": {"score": 0.75, "passed": True}
    }
    """
    # Average of all 5 dimensions
    scores = [d["score"] for d in dimensions.values()]
    overall_score = sum(scores) / len(scores)

    # Check if all dimensions passed individual thresholds
    all_passed = all(d["passed"] for d in dimensions.values())

    # Overall pass criteria: avg ≥0.75 AND all dimensions ≥0.60
    overall_passed = overall_score >= 0.75 and all(d["score"] >= 0.60 for d in dimensions.values())

    return {
        "overall_score": overall_score,
        "overall_passed": overall_passed,
        "dimensions": dimensions,
        "quality_grade": get_quality_grade(overall_score)
    }

def get_quality_grade(score):
    if score >= 0.90: return "A - Excellent"
    elif score >= 0.80: return "B - Good"
    elif score >= 0.75: return "C - Acceptable"
    elif score >= 0.60: return "D - Needs Improvement"
    else: return "F - Fail"
```

---

## 🔄 AUTO-IMPROVEMENT LOGIC

**If quality < 0.75, attempt auto-fix**:

```python
def auto_improve_content(content, validation_report):
    """
    Automatically improve weak dimensions
    """
    dimensions_to_fix = [
        d for d, result in validation_report["dimensions"].items()
        if result["score"] < 0.75
    ]

    for dimension in dimensions_to_fix:
        if dimension == "completeness":
            content = add_missing_sections(content, validation_report["dimensions"]["completeness"]["missing"])

        elif dimension == "clarity":
            content = simplify_language(content)
            content = add_structure(content)

        elif dimension == "accuracy":
            content = fix_currency(content)
            content = fix_marketplace_names(content)

        elif dimension == "relevance":
            content = add_marketplace_examples(content)

        elif dimension == "actionability":
            content = add_action_steps(content)
            content = add_metrics(content)

    return content
```

**Max 3 improvement iterations** before manual review required.

---

## 📋 VALIDATION OUTPUT

**Expected structure**:

```json
{
  "status": "pass | needs_improvement | fail",
  "overall_score": 0.83,
  "quality_grade": "B - Good",
  "dimensions": {
    "completeness": {
      "score": 0.85,
      "passed": true,
      "missing": []
    },
    "clarity": {
      "score": 0.78,
      "passed": true,
      "issues": ["Long sentences (avg 22.3 words)"]
    },
    "accuracy": {
      "score": 0.92,
      "passed": true,
      "issues": []
    },
    "relevance": {
      "score": 0.81,
      "passed": true,
      "issues": []
    },
    "actionability": {
      "score": 0.75,
      "passed": true,
      "issues": ["No before/after example"]
    }
  },
  "recommendation": "Pass - Quality acceptable for PROCESSADOS/",
  "improvements_attempted": 0,
  "next_action": "save_to_processados"
}
```

---

## ✅ PASS/FAIL CRITERIA

**PASS** (Save to PROCESSADOS/):
- ✅ Overall score ≥0.75
- ✅ All dimensions ≥0.60
- ✅ No critical errors (factual contradictions, missing required sections)

**NEEDS IMPROVEMENT** (Auto-fix):
- ⚠️ Overall score 0.60-0.74
- OR any dimension <0.60
- ⚠️ Max 3 improvement attempts

**FAIL** (Manual review):
- ❌ Overall score <0.60 after 3 improvement attempts
- ❌ Critical errors (factual contradictions, plagiarism)
- ❌ Content extraction failed (too short, gibberish)

---

## 📊 QUALITY METRICS TRACKING

**Track over time**:
```python
quality_history = {
    "total_files_processed": 150,
    "passed_first_try": 120,  # 80% pass rate
    "passed_after_improvement": 25,  # 16.7% needed improvement
    "failed": 5,  # 3.3% manual review
    "average_overall_score": 0.82,
    "dimension_averages": {
        "completeness": 0.87,
        "clarity": 0.79,
        "accuracy": 0.91,
        "relevance": 0.83,
        "actionability": 0.72  # Weakest dimension
    }
}
```

**Target Metrics** (based on conhecimento_agent):
- First-try pass rate: >75%
- Overall pass rate (after improvement): >95%
- Average quality score: >0.80

---

## 📋 VALIDATION CHECKLIST

Before saving to PROCESSADOS/:

- [ ] All 5 dimensions validated
- [ ] Overall score ≥0.75
- [ ] Each dimension ≥0.60
- [ ] No critical errors
- [ ] Auto-improvement attempted if needed (max 3 iterations)
- [ ] Quality report generated
- [ ] Metadata logged

---

**Status**: Stage 4 (final) of knowledge processing pipeline
**Integration**: Called by knowledge_processor_HOP after synthesis, before saving
**Performance**: Proven 97.5% quality rate on 66k+ files