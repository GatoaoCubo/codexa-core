# quality_validator_5d_HOP | 5-Dimensional Quality Validation

## MODULE_METADATA

```yaml
id: quality_validator_5d
version: 1.0.0
category: validation
purpose: Validate knowledge content quality across 5 dimensions (Completeness, Clarity, Accuracy, Relevance, Actionability)
dependencies: []
upstream: knowledge_processor_HOP
downstream: knowledge_processor_HOP (feedback loop)
```

## INPUT_CONTRACT

### Required Inputs
- `$content` (string): Markdown content to validate (synthesized knowledge file)
- `$metadata` (object): Content metadata (categoria, assunto, nivel, tags, aplicacao)

### Optional Inputs
- `$thresholds` (object): Custom quality thresholds (default: overall ≥ 0.75, per_dimension ≥ 0.60)
  ```json
  {
    "overall": 0.75,
    "per_dimension": 0.60,
    "strict_mode": false
  }
  ```
- `$validation_mode` (enum): ["standard", "strict", "lenient"] (default: "standard")
- `$improvement_suggestions` (bool): Return improvement suggestions (default: true)

### Validation
- `$content` must not be empty (min 200 characters)
- `$metadata.categoria` must be valid category
- `$thresholds.overall` must be in range [0.0, 1.0]

## OUTPUT_CONTRACT

### Primary Output: `$validation_report` (object)

```json
{
  "status": "passed | failed | warning",
  "overall_score": 0.87,
  "dimension_scores": {
    "completeness": 0.92,
    "clarity": 0.85,
    "accuracy": 0.88,
    "relevance": 0.90,
    "actionability": 0.80
  },
  "quality_level": "excellent | good | acceptable | poor",
  "passed_threshold": true,
  "weak_dimensions": ["actionability"],
  "improvement_suggestions": [
    {
      "dimension": "actionability",
      "issue": "Step 3 lacks concrete example",
      "suggestion": "Add specific example with marketplace and metrics"
    }
  ],
  "validation_details": {
    "sections_found": ["CONCEITOS-CHAVE", "POR QUE IMPORTA", "COMO FAZER", "EXEMPLO REAL"],
    "sections_missing": [],
    "token_count": 1050,
    "reading_level": "intermediário",
    "brazil_specific": true,
    "marketplace_examples": ["Mercado Livre", "Shopee"],
    "concrete_metrics": 3,
    "jargon_words": 0
  }
}
```

### Secondary Outputs
- `$auto_improvement_plan` (object): Specific actions to improve weak dimensions
- `$revalidation_needed` (bool): Whether content should be revalidated after improvements

## TASK

**Role**: You are the **Quality Validator**, responsible for ensuring all processed knowledge meets high quality standards across 5 critical dimensions.

**Objective**: Analyze content using the 5D framework (inherited from conhecimento_agent's 97.5% quality rate), score each dimension (0.0-1.0), calculate overall score, and provide actionable improvement suggestions for weak areas.

**Standards**:
- **5 Dimensions**: Completeness, Clarity, Accuracy, Relevance, Actionability
- **Threshold**: Overall score ≥ 0.75 (excellent), ≥ 0.60 (acceptable), < 0.60 (poor)
- **Per-dimension minimum**: Each dimension ≥ 0.60
- **Quality Levels**: excellent (≥0.85), good (0.75-0.84), acceptable (0.60-0.74), poor (<0.60)
- **Brazil-specific validation**: Must include Brazilian marketplace examples, avoid US/Europe contexts

**Constraints**:
- Validation must complete in < 5 seconds
- No external API calls (local validation only)
- Must be deterministic (same input → same score)
- Improvement suggestions must be specific and actionable

## STEPS

### 1. Parse Content Structure

**Input**: `$content`

**Actions**:
- Parse markdown structure:
  ```python
  sections = extract_sections(content)
  # Returns: {"CONCEITOS-CHAVE": "...", "POR QUE IMPORTA": "...", ...}
  ```
- Count tokens:
  ```python
  token_count = len(content.split())  # Approximate
  ```
- Extract metadata from content:
  - Marketplace mentions (ML, Shopee, Magalu, Amazon BR, Americanas)
  - Numeric metrics (%, R$, numbers with context)
  - Concrete examples
  - Jargon words (academic terms, English without translation)

**Output**: `$parsed_structure` (object with sections, counts, features)

### 2. Evaluate Dimension 1: COMPLETENESS (0.0-1.0)

**Definition**: Are all required sections present and sufficiently detailed?

**Required Sections**:
```python
required_sections = [
    "CONCEITOS-CHAVE",      # 3-5 bullet points
    "POR QUE IMPORTA",      # 1-2 paragraphs
    "COMO FAZER",           # 3-7 steps
    "EXEMPLO REAL",         # Concrete case
    "BOAS PRÁTICAS",        # 3-5 tips (optional but recommended)
    "PRÓXIMOS PASSOS"       # Learning path
]
```

**Scoring Logic**:
```python
score = 0.0
for section in required_sections:
    if section in parsed_structure:
        if len(parsed_structure[section]) >= min_length[section]:
            score += section_weight[section]

# Weights
weights = {
    "CONCEITOS-CHAVE": 0.20,
    "POR QUE IMPORTA": 0.15,
    "COMO FAZER": 0.30,
    "EXEMPLO REAL": 0.20,
    "BOAS PRÁTICAS": 0.10,
    "PRÓXIMOS PASSOS": 0.05
}

completeness_score = min(score, 1.0)
```

**Quality Checks**:
- CONCEITOS-CHAVE: ≥ 3 bullet points
- COMO FAZER: ≥ 3 numbered steps
- EXEMPLO REAL: Contains marketplace name + result metrics
- Token count 800-1200 (within target range)

**Output**: `completeness_score` (0.0-1.0)

### 3. Evaluate Dimension 2: CLARITY (0.0-1.0)

**Definition**: Is the language clear, simple, and accessible for sellers (no jargon)?

**Scoring Criteria**:

**A) Language Simplicity**:
```python
# Check for jargon/academic terms
jargon_words = [
    "implementar", "estratégia multifacetada", "otimizar",
    "conforme literatura", "paradigma", "holístico",
    # ... (list of 50+ jargon terms)
]

jargon_count = sum([content.lower().count(word) for word in jargon_words])
jargon_penalty = min(jargon_count * 0.05, 0.30)  # Max -0.30
```

**B) Sentence Complexity**:
```python
avg_sentence_length = calculate_avg_sentence_length(content)
if avg_sentence_length > 25:  # Too complex
    complexity_penalty = (avg_sentence_length - 25) * 0.01
else:
    complexity_penalty = 0
```

**C) Informal Brazilian Portuguese**:
```python
# Check for seller-friendly patterns
friendly_patterns = ["olha só", "funciona assim", "você", "vou te mostrar"]
friendly_count = sum([pattern in content.lower() for pattern in friendly_patterns])
friendly_bonus = min(friendly_count * 0.05, 0.15)
```

**D) Translation of Technical Terms**:
```python
# English terms should have Portuguese translation
english_terms = ["conversion", "SEO", "engagement", "churn"]
translated = check_translations(content, english_terms)
translation_score = translated / len(english_terms) * 0.10
```

**Final Clarity Score**:
```python
clarity_score = 1.0 - jargon_penalty - complexity_penalty + friendly_bonus + translation_score
clarity_score = max(0.0, min(clarity_score, 1.0))
```

**Output**: `clarity_score` (0.0-1.0)

### 4. Evaluate Dimension 3: ACCURACY (0.0-1.0)

**Definition**: Is the content factually correct and Brazil-specific?

**Scoring Criteria**:

**A) Brazil-Specific Context**:
```python
# Must mention Brazilian marketplaces or context
brazil_indicators = [
    "brasil", "mercado livre", "mercadolivre", "shopee",
    "magalu", "magazine luiza", "amazon br", "americanas",
    "r$", "reais", "cpf", "cnpj"
]

brazil_score = any([ind in content.lower() for ind in brazil_indicators])
if not brazil_score:
    accuracy_score -= 0.30  # Major penalty for non-Brazil content
```

**B) Marketplace-Specific Rules**:
```python
# Check if marketplace rules/examples are current (not outdated)
# Example: ML character limits, Shopee fees
if metadata.categoria in ["marketplace_optimization", "compliance_legal"]:
    # Verify facts against known rules
    facts_correct = verify_marketplace_facts(content, metadata)
    if not facts_correct:
        accuracy_score -= 0.20
```

**C) Concrete vs Vague Metrics**:
```python
# Prefer "+45% conversão" over "melhora conversão"
vague_phrases = ["pode melhorar", "tende a aumentar", "geralmente ajuda"]
vague_count = sum([phrase in content.lower() for phrase in vague_phrases])

concrete_metrics = re.findall(r'\+?\d+%|\d+ unidades|r\$\d+', content.lower())
metrics_count = len(concrete_metrics)

if metrics_count >= 3:
    metrics_bonus = 0.10
elif vague_count > metrics_count:
    metrics_penalty = 0.15
else:
    metrics_bonus = 0
```

**D) Source Credibility** (if fonte_original present):
```python
# Known credible sources get bonus
credible_sources = ["mercado livre", "shopee seller center", "magalu parceiros"]
if any([source in metadata.fonte_original.lower() for source in credible_sources]):
    source_bonus = 0.05
```

**Final Accuracy Score**:
```python
accuracy_score = 1.0
accuracy_score += brazil_score_adjustment
accuracy_score += facts_adjustment
accuracy_score += metrics_adjustment
accuracy_score += source_bonus
accuracy_score = max(0.0, min(accuracy_score, 1.0))
```

**Output**: `accuracy_score` (0.0-1.0)

### 5. Evaluate Dimension 4: RELEVANCE (0.0-1.0)

**Definition**: Is the content useful for seller's daily work in their context?

**Scoring Criteria**:

**A) Practical Applicability**:
```python
# Check for "quando usar" context in content
aplicacao_patterns = [
    "quando criar", "ao fazer", "use isso para",
    "aplique quando", "funciona melhor para"
]
aplicacao_mentions = sum([pattern in content.lower() for pattern in aplicacao_patterns])
aplicacao_score = min(aplicacao_mentions * 0.1, 0.2)
```

**B) Seller Level Alignment**:
```python
# Content should match seller nivel
if metadata.nivel == "básico":
    # Should explain fundamentals, avoid advanced concepts
    advanced_terms = ["cross-sell avançado", "análise preditiva", "machine learning"]
    if any([term in content.lower() for term in advanced_terms]):
        level_penalty = 0.15
elif metadata.nivel == "avançado":
    # Should include sophisticated strategies
    if not contains_advanced_concepts(content):
        level_penalty = 0.10
```

**C) Category Fit**:
```python
# Content should clearly relate to assigned categoria
categoria_keywords = get_categoria_keywords(metadata.categoria)
keyword_density = count_keyword_matches(content, categoria_keywords) / len(content.split())

if keyword_density >= 0.05:  # 5% of content
    category_fit = 0.20
elif keyword_density >= 0.02:
    category_fit = 0.10
else:
    category_fit = 0
```

**D) Actionable for Seller's Current Stage**:
```python
# Can seller execute this TODAY?
immediate_actionability = [
    "primeiro passo", "comece por", "agora você",
    "teste hoje", "implemente já"
]
immediate_count = sum([phrase in content.lower() for phrase in immediate_actionability])
immediate_bonus = min(immediate_count * 0.08, 0.15)
```

**Final Relevance Score**:
```python
relevance_score = 0.5  # Base
relevance_score += aplicacao_score
relevance_score -= level_penalty
relevance_score += category_fit
relevance_score += immediate_bonus
relevance_score = max(0.0, min(relevance_score, 1.0))
```

**Output**: `relevance_score` (0.0-1.0)

### 6. Evaluate Dimension 5: ACTIONABILITY (0.0-1.0)

**Definition**: Does the content include concrete, executable steps?

**Scoring Criteria**:

**A) Step-by-Step Instructions**:
```python
# Check COMO FAZER section
steps = extract_numbered_steps(content)
step_count = len(steps)

if step_count >= 5:
    step_score = 0.30
elif step_count >= 3:
    step_score = 0.20
elif step_count >= 1:
    step_score = 0.10
else:
    step_score = 0
```

**B) Concrete Examples in Steps**:
```python
# Each step should have example or sub-steps
steps_with_examples = 0
for step in steps:
    if has_example(step) or has_substeps(step):
        steps_with_examples += 1

example_ratio = steps_with_examples / max(len(steps), 1)
example_score = example_ratio * 0.25
```

**C) Real-World Case Study**:
```python
# EXEMPLO REAL section should include:
# - Context (seller type, marketplace)
# - Action taken
# - Result (with metrics)

exemplo_section = parsed_structure.get("EXEMPLO REAL", "")
has_context = any([word in exemplo_section.lower() for word in ["contexto", "vendedor", "seller"]])
has_action = any([word in exemplo_section.lower() for word in ["ação", "fez", "aplicou"]])
has_result = any([word in exemplo_section.lower() for word in ["resultado", "conversão", "%", "r$"]])

if has_context and has_action and has_result:
    case_study_score = 0.20
elif (has_context and has_action) or (has_action and has_result):
    case_study_score = 0.10
else:
    case_study_score = 0
```

**D) Tools/Templates Provided**:
```python
# Bonus if provides tools, checklists, templates
tools = ["template", "checklist", "planilha", "script", "modelo"]
tool_count = sum([tool in content.lower() for tool in tools])
tool_bonus = min(tool_count * 0.05, 0.10)
```

**E) Next Steps Clarity**:
```python
# PRÓXIMOS PASSOS should suggest concrete next actions
proximos_section = parsed_structure.get("PRÓXIMOS PASSOS", "")
if len(proximos_section.split()) >= 30:  # Substantial next steps
    next_steps_score = 0.15
elif len(proximos_section.split()) >= 15:
    next_steps_score = 0.08
else:
    next_steps_score = 0
```

**Final Actionability Score**:
```python
actionability_score = step_score + example_score + case_study_score + tool_bonus + next_steps_score
actionability_score = max(0.0, min(actionability_score, 1.0))
```

**Output**: `actionability_score` (0.0-1.0)

### 7. Calculate Overall Score and Quality Level

**Input**: 5 dimension scores

**Actions**:

**A) Calculate Weighted Average**:
```python
weights = {
    "completeness": 0.20,
    "clarity": 0.20,
    "accuracy": 0.25,      # Most important (factual correctness)
    "relevance": 0.20,
    "actionability": 0.15
}

overall_score = sum([dimension_scores[dim] * weights[dim] for dim in weights])
```

**B) Determine Quality Level**:
```python
if overall_score >= 0.85:
    quality_level = "excellent"
elif overall_score >= 0.75:
    quality_level = "good"
elif overall_score >= 0.60:
    quality_level = "acceptable"
else:
    quality_level = "poor"
```

**C) Check Threshold**:
```python
passed_threshold = (overall_score >= thresholds.overall) and \
                   all([score >= thresholds.per_dimension for score in dimension_scores.values()])
```

**D) Identify Weak Dimensions**:
```python
weak_dimensions = [dim for dim, score in dimension_scores.items() if score < 0.70]
```

**Output**: `overall_score`, `quality_level`, `passed_threshold`, `weak_dimensions`

### 8. Generate Improvement Suggestions

**Input**: `dimension_scores`, `weak_dimensions`, `parsed_structure`

**Actions**:

For each weak dimension, generate specific suggestions:

```python
suggestions = []

if "completeness" in weak_dimensions:
    missing_sections = identify_missing_sections(parsed_structure)
    for section in missing_sections:
        suggestions.append({
            "dimension": "completeness",
            "issue": f"Missing section: {section}",
            "suggestion": f"Add {section} with {section_requirements[section]}"
        })

if "clarity" in weak_dimensions:
    jargon_found = identify_jargon_words(content)
    for jargon in jargon_found[:3]:  # Top 3
        suggestions.append({
            "dimension": "clarity",
            "issue": f"Jargon detected: '{jargon}'",
            "suggestion": f"Replace with simpler term: {jargon_replacements.get(jargon, 'use plain language')}"
        })

if "accuracy" in weak_dimensions:
    if not has_brazil_context(content):
        suggestions.append({
            "dimension": "accuracy",
            "issue": "Missing Brazil-specific context",
            "suggestion": "Add Brazilian marketplace examples (ML, Shopee, Magalu) and use R$ for prices"
        })

if "relevance" in weak_dimensions:
    suggestions.append({
        "dimension": "relevance",
        "issue": "Content may not align with seller's daily work",
        "suggestion": "Add 'quando usar' context and practical application scenarios"
    })

if "actionability" in weak_dimensions:
    if step_count < 3:
        suggestions.append({
            "dimension": "actionability",
            "issue": "Too few steps in COMO FAZER",
            "suggestion": "Expand to 3-7 numbered steps with sub-steps and examples"
        })
    if not case_study_score:
        suggestions.append({
            "dimension": "actionability",
            "issue": "EXEMPLO REAL lacks structure",
            "suggestion": "Include: Context (seller type), Action (what they did), Result (metrics achieved)"
        })
```

**Output**: `improvement_suggestions[]` (list of actionable suggestions)

### 9. Create Auto-Improvement Plan (if needed)

**Input**: `improvement_suggestions`, `weak_dimensions`

**Actions**:

If `overall_score < 0.75` but `≥ 0.60`, create auto-improvement plan:

```python
auto_improvement_plan = {
    "target_score": 0.75,
    "current_score": overall_score,
    "actions": []
}

for suggestion in improvement_suggestions:
    auto_improvement_plan["actions"].append({
        "dimension": suggestion["dimension"],
        "action": suggestion["suggestion"],
        "priority": "high" if dimension_scores[suggestion["dimension"]] < 0.60 else "medium",
        "estimated_impact": calculate_impact(suggestion)
    })

# Sort by priority and impact
auto_improvement_plan["actions"].sort(key=lambda x: (x["priority"], x["estimated_impact"]), reverse=True)
```

**Output**: `auto_improvement_plan` (object with prioritized actions)

### 10. Return Validation Report

**Actions**:
- Compile complete `$validation_report` (see OUTPUT_CONTRACT)
- Include all scores, quality level, suggestions
- Set `revalidation_needed = True` if improvements planned
- Return to caller (knowledge_processor_HOP)

**Output**: `$validation_report` (complete validation report)

## VALIDATION

### Quality Gates

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| ✅ Content parsed | Structure valid | Return error, cannot validate |
| ✅ All dimensions scored | 5 scores [0.0-1.0] | Fail validation |
| ✅ Overall score calculated | Weighted average | Fail validation |
| ✅ Suggestions generated | ≥ 1 per weak dimension | Continue (suggestions helpful but optional) |
| ✅ Execution time | ≤ 5 seconds | Timeout warning, return partial results |

### Self-Validation Checklist

Before returning `$validation_report`:
- [ ] All 5 dimension scores in range [0.0, 1.0]
- [ ] Overall score is weighted average (verified)
- [ ] Quality level matches overall score range
- [ ] `passed_threshold` correctly calculated
- [ ] `weak_dimensions` includes all dimensions < 0.70
- [ ] Improvement suggestions specific and actionable
- [ ] No generic suggestions ("improve quality")

## CONTEXT

### Usage Scenarios

**Scenario 1**: High-quality content
```
Scores: completeness=0.92, clarity=0.88, accuracy=0.90, relevance=0.85, actionability=0.82
Overall: 0.87 → "excellent"
→ Pass, no improvements needed
```

**Scenario 2**: Needs improvement
```
Scores: completeness=0.70, clarity=0.65, accuracy=0.75, relevance=0.68, actionability=0.60
Overall: 0.68 → "acceptable"
→ Pass threshold (0.60) but suggest improvements for clarity, actionability
```

**Scenario 3**: Failed validation
```
Scores: completeness=0.55, clarity=0.50, accuracy=0.60, relevance=0.58, actionability=0.52
Overall: 0.55 → "poor"
→ Fail, return auto-improvement plan with prioritized actions
```

### Upstream Context

- Called by: `knowledge_processor_HOP.md` (step 4: Validate Quality)
- Input from: Synthesized content after classification and structuring
- Context from: Metadata provides categoria, nivel for context-aware validation

### Downstream Context

- Returns to: `knowledge_processor_HOP.md`
- If passed (≥0.75): Processor saves file to PROCESSADOS/
- If acceptable (0.60-0.74): Processor auto-improves and revalidates
- If failed (<0.60): Processor aborts or requests manual review

### Reusable Pattern from conhecimento_agent

This 5D validation framework is inherited from `conhecimento_agent`:
- **97.5% quality rate** on 66,105+ processed cards
- **Proven at scale** across diverse e-commerce content
- **Balanced scoring** across dimensions (no single dimension dominates)
- **Actionable feedback** (not just scores, but specific improvements)

### Assumptions

- Content is markdown format
- Seller language guide loaded (`config/seller_language_guide.json`)
- Category taxonomy loaded (`config/categorias_conhecimento.json`)
- Validation is deterministic (same input → same score)
- No external API calls (local validation only)
- Brazilian Portuguese language (pt-BR)

### Performance Notes

- Structure parsing: ~0.5s
- Dimension scoring: ~0.5-1s per dimension (2.5-5s total)
- Suggestion generation: ~0.5s
- **Total execution**: 3-6 seconds per validation

---

**Version**: 1.0.0
**Last Updated**: 2025-11-13
**Dependencies**: None (standalone validator)
**Status**: Ready for Implementation
