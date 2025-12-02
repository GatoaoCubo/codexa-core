# HOP 18: QA Validation | anuncio_agent v3.2.0

**Purpose**: Execute 5-dimension quality validation on all generated content
**Scope**: TEXT-ONLY | **Output**: Validation report with scores

---

## 5-DIMENSION SCORING

| Dimension | Weight | Threshold | Criteria |
|-----------|--------|-----------|----------|
| Titulo | 30% | >= 0.75 | 3 x 58-60 chars, ZERO conectores |
| Keywords | 25% | >= 0.75 | 2 x 115-120 termos, deduplicados |
| Descricao | 20% | >= 0.75 | >= 3,300 chars, StoryBrand |
| Bullets | 15% | >= 0.75 | 10 x 250-299 chars |
| Compliance | 10% | >= 0.75 | Zero violations |

**PASS**: overall >= 0.85
**PASS_WITH_WARNINGS**: 0.75 <= overall < 0.85
**FAIL**: overall < 0.75

---

## VALIDACOES POR DIMENSAO

### V1: TITULOS
```
Check titulo_chars >= 58 AND <= 60 (each)
Check titulo_count == 3
Check conectores_count == 0
Check head_term_position <= 15
Check keywords_count >= 8 (each)
```

### V2: KEYWORDS
```
Check bloco_1_count >= 115 AND <= 120
Check bloco_2_count >= 115 AND <= 120
Check duplicatas_entre_blocos == 0
Check duplicatas_com_titulos == 0
```

### V3: DESCRICAO
```
Check total_chars >= 3300
Check blocos_presentes == 12
Check storybrand_elements >= 3/4
  - problem: regex(problema|dor|dificuldade)
  - solution: regex(solucao|resolve)
  - success: regex(resultado|sucesso|conquist)
  - cta: regex(compre|adquira|garanta)
```

### V4: BULLETS
```
Check bullet_count == 10
Check each bullet_chars >= 250 AND <= 299
Check categorias_cobertas == 5
```

### V5: COMPLIANCE
```
Check html_tags == 0: regex(<[^>]+>)
Check emojis == 0: regex([\U0001F300-\U0001F9FF])
Check prohibited_claims == 0: regex(#1|melhor do brasil|numero 1)
Check therapeutic_claims == 0: regex(cura|trata doenca)
Check external_links == 0: regex(https?://|www\.)
```

---

## OUTPUT FORMAT

```json
{
  "qa_report": {
    "timestamp": "ISO8601",
    "version": "3.2.0",
    "overall_score": 0.92,
    "status": "PASS",
    "dimensions": {
      "titulo": {"score": 0.95, "weight": 0.30, "contrib": 0.285},
      "keywords": {"score": 0.90, "weight": 0.25, "contrib": 0.225},
      "descricao": {"score": 0.88, "weight": 0.20, "contrib": 0.176},
      "bullets": {"score": 0.92, "weight": 0.15, "contrib": 0.138},
      "compliance": {"score": 1.00, "weight": 0.10, "contrib": 0.100}
    },
    "issues": [],
    "auto_fixes": [],
    "recommendations": []
  }
}
```

---

## COMPLIANCE RULES (Marketplace-Specific)

### Global (All)
- Zero HTML/CSS/JS
- Zero emojis
- Zero links externos
- Zero claims absolutos sem prova

### Mercado Livre
- Titulo <= 60 chars
- "frete gratis" only if true

### Shopee
- Titulo <= 120 chars
- Precos no titulo prohibited

### Amazon BR
- Titulo <= 200 chars
- Palavras repetidas <= 2x

---

## INTELLIGENT FALLBACK

| Input Confidence | Action |
|------------------|--------|
| >= 0.8 | generate_full |
| 0.6-0.79 | generate_with_suggestions [VERIFICAR] |
| 0.4-0.59 | generate_partial [COMPLETAR] |
| < 0.4 | request_enrichment |

---

## EXECUTION

### Step 1: Collect All Content
- Titulos (3)
- Keywords (2 blocos)
- Descricao
- Bullets (10)

### Step 2: Run 5D Validation
- Execute checks per dimension
- Calculate scores

### Step 3: Calculate Overall
```
overall = sum(dimension.score * dimension.weight)
```

### Step 4: Generate Report
- Status (PASS/FAIL)
- Issues list
- Recommendations

---

## INTEGRATION

**Upstream**: Receives output from HOPs 14-17
**Downstream**: Final validation before output assembly

**Tool**: Use `validator.py` in Code Interpreter for automated validation

---

**HOP**: 18 | **Agent**: anuncio_agent | **Version**: 3.2.0
**Tokens**: ~800 (otimizado)
