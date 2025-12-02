<!-- iso_vectorstore -->
<!--
  Source: templates/output_template.md
  Agent: anuncio_agent
  Version: 3.2.0
  Scope: TEXT-ONLY
  Synced: 2025-11-30
  Package: iso_vectorstore (export package)
  Structure: 3-PART OUTPUT (Visual + Copyable + Structured)
-->

# ANUNCIO | {PRODUTO_NOME}

**Schema**: 3.2 | **Agent**: anuncio_agent v3.2.0 | **Scope**: TEXT-ONLY

---

# ========================================================================
# PART 1: VISUAL REVIEW (Display Only - Audit & Review)
# ========================================================================

## IDENTIDADE

| Campo | Valor |
|-------|-------|
| Produto | {PRODUTO_NOME} |
| Categoria | {CATEGORIA} |
| Marketplace | {MARKETPLACE_TARGET} |
| Gerado | {GENERATION_TIMESTAMP} |

---

## TITULOS (3 Variacoes)

| Var | Titulo | Chars | Fonte |
|-----|--------|-------|-------|
| A | {TITULO_A} | {TITULO_A_CHARS} | {TITULO_A_SOURCE} |
| B | {TITULO_B} | {TITULO_B_CHARS} | {TITULO_B_SOURCE} |
| C | {TITULO_C} | {TITULO_C_CHARS} | {TITULO_C_SOURCE} |

---

## KEYWORDS

**Bloco 1**: {BLOCO_1_COUNT} termos | Fonte: {KEYWORDS_1_SOURCE}
**Bloco 2**: {BLOCO_2_COUNT} termos | Fonte: {KEYWORDS_2_SOURCE}

---

## BULLETS ({BULLETS_COUNT}/10)

{BULLETS_LIST_VISUAL}

---

## DESCRICAO ({DESCRICAO_CHARS} chars)

{DESCRICAO_PREVIEW}...

[Full text in PART 2]

---

## QA REPORT

**Status**: {QA_STATUS} | **Score**: {OVERALL_SCORE}/1.0

| Dim | Score | Weight | OK |
|-----|-------|--------|-----|
| Titulo | {TITULO_SCORE} | 0.30 | {TITULO_OK} |
| Keywords | {KEYWORDS_SCORE} | 0.25 | {KEYWORDS_OK} |
| Descricao | {DESCRICAO_SCORE} | 0.20 | {DESCRICAO_OK} |
| Bullets | {BULLETS_SCORE} | 0.15 | {BULLETS_OK} |
| Compliance | {COMPLIANCE_SCORE} | 0.10 | {COMPLIANCE_OK} |

**Issues**: {QA_ISSUES_SUMMARY}
**Recommendations**: {QA_RECOMMENDATIONS_SUMMARY}

---

# ========================================================================
# PART 2: COPYABLE CONTENT (1-Click Copy - Production Ready)
# ========================================================================

```txt
[INICIO_COPIAR]
================================================================================
TITULOS
================================================================================

TITULO A:
{TITULO_A}

TITULO B:
{TITULO_B}

TITULO C:
{TITULO_C}

================================================================================
DESCRICAO
================================================================================

{DESCRICAO_TEXTO}

================================================================================
BULLETS
================================================================================

1. {BULLET_1}
2. {BULLET_2}
3. {BULLET_3}
4. {BULLET_4}
5. {BULLET_5}
6. {BULLET_6}
7. {BULLET_7}
8. {BULLET_8}
9. {BULLET_9}
10. {BULLET_10}

================================================================================
KEYWORDS BLOCO 1
================================================================================

{KEYWORDS_BLOCO_1}

================================================================================
KEYWORDS BLOCO 2
================================================================================

{KEYWORDS_BLOCO_2}

[FIM_COPIAR]
```

**Instrucoes**: Selecione o bloco acima (entre [INICIO_COPIAR] e [FIM_COPIAR]) e copie. O code fence permite 1-click copy na maioria das interfaces.

---

# ========================================================================
# PART 3: STRUCTURED DATA (Optional - API/Automation)
# ========================================================================

```json
{
  "schema_version": "3.2",
  "agent": "anuncio_agent",
  "generated_at": "{GENERATION_TIMESTAMP}",
  "produto": {
    "nome": "{PRODUTO_NOME}",
    "categoria": "{CATEGORIA}",
    "marketplace": "{MARKETPLACE_TARGET}"
  },
  "titulos": [
    {"variacao": "A", "texto": "{TITULO_A}", "chars": {TITULO_A_CHARS}, "fonte": "{TITULO_A_SOURCE}"},
    {"variacao": "B", "texto": "{TITULO_B}", "chars": {TITULO_B_CHARS}, "fonte": "{TITULO_B_SOURCE}"},
    {"variacao": "C", "texto": "{TITULO_C}", "chars": {TITULO_C_CHARS}, "fonte": "{TITULO_C_SOURCE}"}
  ],
  "descricao": {
    "texto": "{DESCRICAO_TEXTO}",
    "chars": {DESCRICAO_CHARS},
    "fonte": "{DESCRICAO_SOURCE}"
  },
  "bullets": {BULLETS_JSON_ARRAY},
  "keywords": {
    "bloco_1": "{KEYWORDS_BLOCO_1}",
    "bloco_1_count": {BLOCO_1_COUNT},
    "bloco_2": "{KEYWORDS_BLOCO_2}",
    "bloco_2_count": {BLOCO_2_COUNT}
  },
  "qa": {
    "status": "{QA_STATUS}",
    "overall_score": {OVERALL_SCORE},
    "dimensions": {
      "titulo": {TITULO_SCORE},
      "keywords": {KEYWORDS_SCORE},
      "descricao": {DESCRICAO_SCORE},
      "bullets": {BULLETS_SCORE},
      "compliance": {COMPLIANCE_SCORE}
    },
    "issues": {QA_ISSUES_JSON},
    "recommendations": {QA_RECOMMENDATIONS_JSON}
  },
  "source_attribution": {SOURCE_ATTRIBUTION_JSON}
}
```

---

# ========================================================================
# NOTES
# ========================================================================

## Fallback Notes
{FALLBACK_NOTES}

## Execution Metadata
- **Duration**: {GENERATION_DURATION}min
- **Input Confidence**: {INPUT_CONFIDENCE}
- **Action Taken**: {FALLBACK_ACTION}
- **Code Interpreter Calls**: {CODE_CALLS_COUNT}

---

**Output Structure**: 3-PART (Visual + Copyable + Structured)
**Gerado por**: anuncio_agent v3.2.0
**Config Ref**: config/MANUAL_CONFIGS.md
