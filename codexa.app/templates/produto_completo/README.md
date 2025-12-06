# Pipeline Produto Completo - Templates Reusaveis

**Version**: 2.1.0 | **Updated**: 2025-12-05
**Purpose**: Templates consolidados para criar produtos em escala
**Workflow**: 200_ADW_PRODUTO_COMPLETO

---

## QUICK START

```bash
# 1. Criar pasta do produto
mkdir user_research/meu_produto

# 2. Copiar templates
cp codexa.app/templates/produto_completo/generate_images_universal.py user_research/meu_produto/generate_images.py

# 3. Adicionar imagem original
# → Salvar como: user_research/meu_produto/imagem_original.webp

# 4. Gerar photo_prompts.json
# → Usar /prime-photo ou adaptar TEMPLATE_PHOTO_PROMPTS.json

# 5. Executar geracao de imagens
cd user_research/meu_produto && python generate_images.py

# 6. Servir preview
python -m http.server 3456
# → Abrir http://localhost:3456/preview.html
```

---

## ARQUIVOS DO TEMPLATE

| Arquivo | Proposito | Placeholders |
|---------|-----------|--------------|
| `TEMPLATE_PRODUTO.md` | Documentacao completa do produto | 80+ placeholders |
| `TEMPLATE_PHOTO_PROMPTS.json` | 9 prompts de foto com variaveis | 50+ placeholders |
| `generate_images_universal.py` | Script Python auto-detecta arquivos | Zero config |
| `preview_template.html` | Preview HTML com todas secoes | 30+ placeholders |

---

## PLACEHOLDERS PRINCIPAIS

### Produto
```
{{PRODUCT_NAME}}           → Nome completo do produto
{{PRODUCT_SLUG}}           → Slug URL-friendly (ex: garrafa-termica-gato)
{{PRODUCT_SKU}}            → Codigo SKU/MLB
{{PRODUCT_CATEGORY}}       → Categoria (ex: Casa, Cozinha, Fitness)
{{PRODUCT_PRICE}}          → Preco em reais (ex: 65.89)
{{PRODUCT_DIFFERENTIATOR}} → Diferencial unico (ex: "Tampa com orelhas 3D")
```

### Especificacoes
```
{{SPEC_CAPACITY}}    → Capacidade (ex: 320ml)
{{SPEC_MATERIAL}}    → Material (ex: Aco Inoxidavel + PP + Silicone)
{{SPEC_DIMENSIONS}}  → Dimensoes (ex: 18cm x 7cm)
{{SPEC_WEIGHT}}      → Peso (ex: 200g)
{{SPEC_COLOR}}       → Cor (ex: Azul metalizado)
{{SPEC_WARRANTY}}    → Garantia (ex: 3 meses)
```

### Vendedor
```
{{SELLER_NAME}}   → Nome do vendedor (ex: GATO AO CUBO)
{{SELLER_RATING}} → Rating (ex: 4.8/5.0)
{{MLB_ID}}        → ID Mercado Livre (ex: MLB34173780)
```

### Imagens
```
{{REFERENCE_IMAGE_PATH}}   → Caminho da imagem original
{{IMAGE_EXTENSION}}        → Extensao (webp, jpg, png)
{{IMAGE_MODEL}}            → Modelo usado (ex: gemini-2.5-flash)
{{IMAGES_COUNT}}           → Quantidade gerada (ex: 9)
```

### Photo Prompts (variaveis de cena)
```
{{PRODUCT_MAIN_OBJECT}}        → Objeto principal (ex: thermal bottle)
{{PRODUCT_DISTINCTIVE_FEATURE}} → Caracteristica unica (ex: 3D cat ears lid)
{{PRODUCT_FINISH}}             → Acabamento (ex: brushed metallic)
{{MATERIAL_TYPE}}              → Tipo de material (ex: metallic, matte, glossy)

{{LIFESTYLE_1_NAME}}   → Nome do lifestyle 1 (ex: Gym)
{{LIFESTYLE_1_SLUG}}   → Slug (ex: gym)
{{LIFESTYLE_1_PROPS}}  → Props da cena (ex: towel, earbuds)

{{DETAIL_FEATURE_NAME}} → Feature em destaque (ex: Cat Ears)
{{DETAIL_FEATURE_SLUG}} → Slug (ex: ears)

{{EMOTIONAL_THEME}}     → Tema emocional (ex: cat)
{{EMOTIONAL_COMMUNITY}} → Comunidade alvo (ex: cat lovers)
```

---

## WORKFLOW DE PRODUCAO

### Fase 1: Pesquisa
```
/prime-pesquisa "URL do produto"
```
**Output**: `product_data.json`, `research_notes.md`

### Fase 2: Anuncio
```
/prime-anuncio
```
**Output**: `anuncio_completo.md` com:
- 6 titulos SEO (ML 60, Shopee 120, Amazon 200)
- 60 keywords
- 15 bullets (5 por marketplace)
- Descricao StoryBrand

### Fase 3: Photo Prompts
```
/prime-photo
```
**Output**: `photo_prompts.json` com 9 cenas:
1. Hero (fundo branco)
2. Detail (close-up feature)
3. Lifestyle 1 (contexto 1)
4. Lifestyle 2 (contexto 2)
5. Lifestyle 3 (contexto 3)
6. In-Use (mao segurando)
7. Group (variantes de cor)
8. Flatlay (essenciais)
9. Emotional (conexao marca)

### Fase 4: Geracao de Imagens
```bash
python generate_images.py
```
**Output**: `images/photo_*.png` (9 arquivos)

### Fase 5: Preview
```bash
python -m http.server 3456
```
**Acesso**: http://localhost:3456/preview.html

### Fase 6: Publicacao
- Shopify Sync (opcional)
- Mercado Livre (manual ou API)
- Shopee (manual ou API)

---

## EXEMPLO: GARRAFA TERMICA GATO

### Inputs Usados
```json
{
  "PRODUCT_NAME": "Garrafa Termica Inox Gato Parede Dupla 320ml",
  "PRODUCT_SLUG": "garrafa_termica_gato",
  "PRODUCT_MAIN_OBJECT": "slim stainless steel thermal bottle",
  "PRODUCT_DISTINCTIVE_FEATURE": "3D sculptured cat ears lid",
  "PRODUCT_COLOR": "champagne silver",
  "PRODUCT_FINISH": "metallic brushed",
  "PRODUCT_SIZE": "320ml",
  "MATERIAL_TYPE": "metallic",

  "LIFESTYLE_1_NAME": "Gym",
  "LIFESTYLE_1_SLUG": "gym",
  "LIFESTYLE_2_NAME": "Office",
  "LIFESTYLE_2_SLUG": "office",
  "LIFESTYLE_3_NAME": "Study",
  "LIFESTYLE_3_SLUG": "study",

  "DETAIL_FEATURE_NAME": "3D Cat Ears",
  "DETAIL_FEATURE_SLUG": "ears",

  "EMOTIONAL_THEME": "cat",
  "EMOTIONAL_COMMUNITY": "cat lovers"
}
```

### Outputs Gerados
```
user_research/garrafa_termica_gato/
├── imagem_original.webp          ← Input
├── product_data.json             ← Fase 1
├── garrafa_termica_gato_research_notes.md
├── anuncio_completo.md           ← Fase 2
├── photo_prompts.json            ← Fase 3
├── generate_images.py            ← Script
├── preview.html                  ← Preview
└── images/                       ← Fase 4
    ├── photo_01_hero.png
    ├── photo_02_detail_ears.png
    ├── photo_03_lifestyle_gym.png
    ├── photo_04_lifestyle_office.png
    ├── photo_05_lifestyle_study.png
    ├── photo_06_in_use_drinking.png
    ├── photo_07_group_colors.png
    ├── photo_08_flatlay_essentials.png
    ├── photo_09_emotional_cat.png
    └── generation_log.json
```

---

## HARD RULES

1. **REFERENCE IMAGE**: Toda geracao de imagem DEVE incluir imagem original
2. **FUNDO BRANCO**: Cenas 1, 7 e 9 SEMPRE com #FFFFFF (marketplace compliant)
3. **ENGLISH PROMPTS**: Todos os prompts de foto em ingles (melhor para Imagen)
4. **9 CENAS**: Pipeline sempre gera exatamente 9 imagens
5. **PLACEHOLDERS**: Nunca hardcodar valores - sempre usar {{PLACEHOLDER}}

---

## ESCALA: NOVO PRODUTO EM 15 MIN

```bash
# 1. Setup (30s)
mkdir user_research/novo_produto
cp codexa.app/templates/produto_completo/generate_images_universal.py user_research/novo_produto/

# 2. Pesquisa (5min)
# → /prime-pesquisa com URL/imagem do produto
# → Salvar imagem original

# 3. Anuncio (3min)
# → /prime-anuncio
# → Revisar titulos e bullets

# 4. Photos (2min)
# → /prime-photo
# → Adaptar cenas se necessario

# 5. Geracao (5min)
cd user_research/novo_produto && python generate_images.py

# 6. Preview (30s)
python -m http.server 3456
# → Validar em http://localhost:3456/preview.html

# DONE! Produto pronto para publicacao
```

---

## REFERENCIAS

- **ADW**: `codexa.app/agentes/codexa_agent/workflows/200_ADW_PRODUTO_COMPLETO.md`
- **Photo Agent**: `codexa.app/agentes/photo_agent/PRIME.md`
- **Anuncio Agent**: `codexa.app/agentes/anuncio_agent/PRIME.md`
- **Placeholders**: `docs/PLACEHOLDERS.md`
- **Exemplo**: `user_research/garrafa_termica_gato/`

---

**Status**: Production-Ready
**Maintainer**: CODEXA Pipeline
**Last Validated**: 2025-12-05 (Garrafa Termica Gato - 9/9 images, 100% compliance)
