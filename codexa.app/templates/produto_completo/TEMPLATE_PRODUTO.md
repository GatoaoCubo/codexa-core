# {{PRODUCT_NAME}} | Pipeline Produto Completo

**Pipeline**: 200_ADW_PRODUTO_COMPLETO v2.1.0
**Gerado**: {{GENERATED_DATE}}
**Status**: {{PIPELINE_STATUS}}

---

## DADOS DO PRODUTO

| Campo | Valor |
|-------|-------|
| Nome | {{PRODUCT_NAME}} |
| SKU | {{PRODUCT_SKU}} |
| MLB ID | {{MLB_ID}} |
| Categoria | {{PRODUCT_CATEGORY}} |
| Preco | R$ {{PRODUCT_PRICE}} |
| Vendedor | {{SELLER_NAME}} |
| Rating | {{SELLER_RATING}} |

### Especificacoes Tecnicas

| Spec | Valor |
|------|-------|
| Capacidade | {{SPEC_CAPACITY}} |
| Material | {{SPEC_MATERIAL}} |
| Dimensoes | {{SPEC_DIMENSIONS}} |
| Peso | {{SPEC_WEIGHT}} |
| Cor | {{SPEC_COLOR}} |
| Garantia | {{SPEC_WARRANTY}} |

### Diferencial Principal
{{PRODUCT_DIFFERENTIATOR}}

---

## TITULOS SEO

### Mercado Livre (60 chars)
1. `{{TITLE_ML_1}}` ({{TITLE_ML_1_CHARS}} chars)
2. `{{TITLE_ML_2}}` ({{TITLE_ML_2_CHARS}} chars)
3. `{{TITLE_ML_3}}` ({{TITLE_ML_3_CHARS}} chars)

### Shopee (120 chars)
1. `{{TITLE_SHOPEE}}` ({{TITLE_SHOPEE_CHARS}} chars)

### Amazon BR (200 chars)
1. `{{TITLE_AMAZON}}` ({{TITLE_AMAZON_CHARS}} chars)

---

## KEYWORDS ({{KEYWORDS_TOTAL}} total)

### Head Terms ({{KEYWORDS_HEAD_COUNT}})
{{KEYWORDS_HEAD}}

### Longtails Atributos ({{KEYWORDS_ATTRIBUTES_COUNT}})
{{KEYWORDS_ATTRIBUTES}}

### Longtails Beneficios ({{KEYWORDS_BENEFITS_COUNT}})
{{KEYWORDS_BENEFITS}}

### Longtails Contexto ({{KEYWORDS_CONTEXT_COUNT}})
{{KEYWORDS_CONTEXT}}

---

## BULLET POINTS

### Mercado Livre (5)
{{BULLETS_ML}}

### Shopee (5)
{{BULLETS_SHOPEE}}

### Amazon BR (5)
{{BULLETS_AMAZON}}

---

## DESCRICAO COMPLETA

### Abertura (Problema → Solucao)

{{DESCRIPTION_OPENING}}

### Diferenciais

{{DESCRIPTION_DIFFERENTIALS}}

### Especificacoes Tecnicas

{{DESCRIPTION_SPECS_TABLE}}

### Comparativo

{{DESCRIPTION_COMPARISON_TABLE}}

### CTA Final

{{DESCRIPTION_CTA}}

---

## FAQ ({{FAQ_COUNT}} perguntas)

{{FAQ_ITEMS}}

---

## IMAGENS GERADAS ({{IMAGES_COUNT}}/9)

| # | Scene | Arquivo | Tamanho | Status |
|---|-------|---------|---------|--------|
{{IMAGES_TABLE}}

### Prompts Utilizados
- Arquivo: `photo_prompts.json`
- Model: {{IMAGE_MODEL}}
- Reference Image: {{REFERENCE_IMAGE_PATH}}

---

## ARQUIVOS DO PIPELINE

```
{{PRODUCT_FOLDER}}/
├── imagem_original.{{IMAGE_EXTENSION}}
├── product_data.json
├── {{PRODUCT_SLUG}}_research_notes.md
├── anuncio_completo.md
├── photo_prompts.json
├── generate_images.py
├── preview.html
└── images/
    ├── photo_01_hero.png
    ├── photo_02_detail_{{DETAIL_TYPE}}.png
    ├── photo_03_lifestyle_{{LIFESTYLE_1}}.png
    ├── photo_04_lifestyle_{{LIFESTYLE_2}}.png
    ├── photo_05_lifestyle_{{LIFESTYLE_3}}.png
    ├── photo_06_in_use_{{IN_USE_TYPE}}.png
    ├── photo_07_group_{{GROUP_TYPE}}.png
    ├── photo_08_flatlay_{{FLATLAY_TYPE}}.png
    ├── photo_09_emotional_{{EMOTIONAL_TYPE}}.png
    └── generation_log.json
```

---

## METADATA

```json
{
  "pipeline_version": "2.1.0",
  "product_name": "{{PRODUCT_NAME}}",
  "product_slug": "{{PRODUCT_SLUG}}",
  "generated_at": "{{GENERATED_DATE}}",
  "compliance_score": {{COMPLIANCE_SCORE}},
  "quality_score": {{QUALITY_SCORE}},
  "phases_completed": {{PHASES_COMPLETED}},
  "phases_total": 6,
  "marketplaces": ["Mercado Livre", "Shopee", "Amazon BR"],
  "frameworks_used": ["StoryBrand", "AIDA", "PAS"],
  "agents_used": ["pesquisa_agent", "anuncio_agent", "photo_agent"],
  "image_model": "{{IMAGE_MODEL}}",
  "titles_count": {{TITLES_COUNT}},
  "keywords_count": {{KEYWORDS_TOTAL}},
  "bullets_count": {{BULLETS_COUNT}},
  "images_count": {{IMAGES_COUNT}}
}
```

---

**Status**: {{FINAL_STATUS}}
**Proximo**: {{NEXT_ACTION}}
