# 200_ADW_PRODUTO_COMPLETO | Quick Reference

## PIPELINE VISUAL

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PRODUCT CREATION PIPELINE                            │
│                                                                             │
│  INPUT                  PARALLEL AGENTS              SEQUENTIAL EXEC        │
│  ─────                  ───────────────              ───────────────        │
│                                                                             │
│  ┌─────────┐           ┌─────────────────┐                                 │
│  │ URL     │           │ pesquisa_agent  │──┐                              │
│  │ Image   │──────────►│ (identification)│  │                              │
│  │ Text    │           └─────────────────┘  │                              │
│  └─────────┘                                │     ┌──────────────────────┐ │
│                        ┌─────────────────┐  ├────►│ MERGE & GENERATE     │ │
│       $input           │ anuncio_agent   │──┤     │                      │ │
│                        │ (content)       │  │     │ 5. Imagen 4.0        │ │
│                        └─────────────────┘  │     │ 6. Upload Storage    │ │
│                                             │     │ 7. Insert Supabase   │ │
│                        ┌─────────────────┐  │     │ 8. Sync Shopify      │ │
│                        │ photo_agent     │──┘     │ 9. Validate          │ │
│                        │ (prompts)       │        │ 10. Git Push         │ │
│                        └─────────────────┘        └──────────────────────┘ │
│                                                              │              │
│                                                              ▼              │
│                                                   ┌──────────────────────┐ │
│                                                   │  PRODUTO LIVE        │ │
│                                                   │  - 9 images          │ │
│                                                   │  - Supabase DB       │ │
│                                                   │  - Shopify Store     │ │
│                                                   │  - Git Repo          │ │
│                                                   └──────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## STEP-BY-STEP EXECUTION

### FASE A: PARALLEL AGENTS (spawn)

```bash
/spawn
1. pesquisa_agent: Identify product, extract features, materials, dimensions
2. anuncio_agent: Generate titles, keywords, description, FAQ, video script
3. photo_agent: Create 9 image prompts (HERO_WHITE, HERO_GRADIENT, etc.)
```

**Output**: `produto.json`, `anuncio.json`, `photo_prompts.json`

---

### FASE B: IMAGE GENERATION

```python
# generate_images.py
from google import genai
from google.genai import types

client = genai.Client(api_key=GOOGLE_API_KEY)

for prompt in prompts:
    response = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=prompt["prompt_dalle"],
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio=prompt["aspect_ratio"],
        )
    )
    save_image(response.generated_images[0].image.image_bytes)
```

**Output**: 9 PNG files (~1MB each)

---

### FASE C: UPLOAD TO STORAGE

```python
# upload_to_supabase.py
api_url = f"{SUPABASE_URL}/storage/v1/object/{bucket}/{path}"
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "image/png",
    "x-upsert": "true",
}
# POST image bytes
# Get public URL (URL-encoded!)
```

**Output**: 9 public URLs

---

### FASE D: CREATE IN DATABASE

```python
# create_product.py
api_url = f"{SUPABASE_URL}/rest/v1/products"
headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}
body = {
    "name": "...",
    "slug": "...",
    "price": 33.00,
    "quantity": 23,
    "status": "published",
    "images": [url1, url2, ...],  # From Phase C
    # ... all other fields
}
# POST creates product, returns ID
```

**Output**: `product_id` (UUID)

---

### FASE E: SYNC TO SHOPIFY

```python
# Call Edge Function
api_url = f"{SUPABASE_URL}/functions/v1/sync-shopify-product"
headers = {
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}
body = {"productId": product_id}
# Returns Shopify IDs
```

**Output**: `shopify_product_id`, `shopify_variant_id`

---

### FASE F: COMMIT & PUSH

```bash
git add USER_DOCS/produtos/{slug}/
git commit -m "feat(produto): add {product_name}"
git push
```

---

## ARQUIVOS GERADOS

```
USER_DOCS/produtos/{slug}/
├── README.md              # Product overview
├── produto.json           # Full product data
├── anuncio.json           # Marketing content
├── photo_prompts.json     # 9 image prompts
├── video_script.md        # 30s video script
├── imagem_original.webp   # Reference image
├── supabase_result.json   # DB insert result
├── generate_images.py     # Image gen script
├── upload_to_supabase.py  # Upload script
├── create_product.py      # DB + Shopify script
└── imagens_geradas/
    ├── HERO_WHITE_*.png
    ├── HERO_GRADIENT_*.png
    ├── SCALE_HAND_*.png
    ├── LIFESTYLE_VANITY_*.png
    ├── LIFESTYLE_BEDROOM_*.png
    ├── DETAIL_MIRROR_*.png
    ├── DETAIL_JEWELRY_*.png
    ├── SOCIAL_FLATLAY_*.png
    ├── SOCIAL_AESTHETIC_*.png
    └── generation_log.json
```

---

## CHECKLIST DE EXECUCAO

```
[ ] 1. INPUT: URL/imagem do produto
[ ] 2. SPAWN: 3 agents em paralelo
    [ ] pesquisa_agent → produto.json
    [ ] anuncio_agent → anuncio.json
    [ ] photo_agent → photo_prompts.json
[ ] 3. IMAGES: python generate_images.py
    [ ] 9/9 imagens geradas
[ ] 4. UPLOAD: python upload_to_supabase.py
    [ ] 9 URLs publicas
[ ] 5. DATABASE: python create_product.py
    [ ] Produto no Supabase
    [ ] Sincronizado com Shopify
[ ] 6. VALIDATE:
    [ ] Produto no site
    [ ] Imagens visíveis
    [ ] Preco correto
[ ] 7. COMMIT: git add + commit + push
```

---

## APIS E KEYS

| API | Env Var | Uso |
|-----|---------|-----|
| Google Imagen | `GOOGLE_API_KEY` | Gerar imagens |
| Supabase DB | `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` | Database + Storage |
| Shopify | (no Edge Function) | Sync produto |

---

## DURACAO ESTIMADA

| Fase | Duracao | Modo |
|------|---------|------|
| Spawn (A) | 5-8 min | Parallel |
| Images (B) | 3-5 min | Sequential |
| Upload (C) | 1-2 min | Sequential |
| Database (D) | < 1 min | Sequential |
| Shopify (E) | < 1 min | Sequential |
| Commit (F) | < 1 min | Sequential |
| **TOTAL** | **10-18 min** | |

---

## TRIGGER

```
/flow do "criar produto completo para [URL ou descricao]"
```

Ou step-by-step:
```
1. /spawn (3 agents)
2. python generate_images.py
3. python upload_to_supabase.py
4. python create_product.py
5. git add && git commit && git push
```
