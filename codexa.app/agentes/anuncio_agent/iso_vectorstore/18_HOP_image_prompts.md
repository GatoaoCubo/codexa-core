<!-- iso_vectorstore -->
<!--
  Source: 60_image_prompts.md
  Agent: anuncio_agent
  Synced: 2025-12-02
  Version: 2.1.0
  Package: iso_vectorstore (export package)
-->

# ═══════════════════════════════════════════════════════════════════════════
# CODEX-ANUNCIO: IMAGE PROMPTS GENERATOR MODULE (HOP v2.1)
# ═══════════════════════════════════════════════════════════════════════════

[MODULE_METADATA]
name: "image_prompts_generator_HOP"
version: "2.1.0"
framework: "HOP (Hierarchical Operational Protocol)"
specialization: "Meta-prompt generation for AI image synthesis"
output_type: "structured_markdown"
target_quantity: "9 prompts (grid 3x3)"
output_format_options: "A) Single 2000x2000 grid | B) 9 separate 2000x2000 PNGs"
compliance_level: "CRITICAL"
generation_time_target: "<15s"

[CORE_MISSION]
Generate **universal meta-prompts** for AI image generation (Midjourney, DALL-E 3, Stable Diffusion, Google Imagen) that:
→ Work for ANY product/service/brand (generic template)
→ Use `[VARIAVEL]` as dynamic placeholder for product identity
→ Are **copy-paste ready** for immediate use
→ Leave **intentional gaps** (angles, secondary lighting, props) for model creativity
→ Enforce **strict compliance** (no watermark, no third-party logos, no text)
→ Deliver professional product photography specifications
→ Provide 2 output options: Grid 3x3 OR Sequential 9 PNGs

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 1: INPUT PROTOCOL
## ═══════════════════════════════════════════════════════════════════════════

[REQUIRED_INPUTS]
1. **[VARIAVEL]**: Product/service/brand name or description
   - Example: "Cama Suspensa para Gato com Ventosas"
   - Example: "Fone Bluetooth Over-Ear ANC Preto"
   - Example: "Protetor Solar FPS 50+ Facial"

2. **[CATEGORIA]**: Product category
   - Example: "Pet Shop", "Eletrônicos", "Cosméticos", "Casa & Decoração"

3. **[DIFERENCIAIS_VISUAIS]**: Key visual differentiators (comma-separated)
   - Example: "4 ventosas transparentes, tecido Oxford cinza, estrutura aço"
   - Example: "LED azul status, almofadas memory foam, dobrável"

4. **[BENEFICIO_PRINCIPAL]**: Main benefit claim
   - Example: "alívio térmico para pets em climas quentes"
   - Example: "cancelamento de ruído ativo 30dB"

5. **[PUBLICO_ALVO]**: Target audience
   - Example: "tutores de gatos, climas quentes"
   - Example: "profissionais home office, viajantes frequentes"

[OPTIONAL_INPUTS]
6. **[REFERENCE_IMAGE_URL]**: URL to reference image (if available)
   - Used for "brand/style lock" instruction in prompts

7. **[MATERIAIS]**: Materials (if relevant)
   - Example: "Oxford 600D, ABS plástico, silicone médico"

8. **[CORES_DISPONIVEIS]**: Available colors
   - Example: "Cinza neutro, Preto fosco, Branco neve"

9. **[MARKETPLACE_TARGET]**: Target marketplace
   - Example: "Mercado Livre", "Amazon Brasil", "Shopee"
   - Affects compliance rules (white background requirement)

[CONFIGURATION_FLAGS]
- **OUTPUT_MODE**: `grid_3x3` (default) | `sequence_9png`
- **RANDOMIZE**: `on` | `off` (default: off) — enables creative variation banks
- **RANDOM_SEED**: [42, 84, 126] — rotate if RANDOMIZE=on

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 2: PROFESSIONAL PHOTOGRAPHY SPECIFICATIONS
## ═══════════════════════════════════════════════════════════════════════════

### [SPECS_COLOR]
color_space: "sRGB"
gamma: "2.2"
white_balance: "5000-5400K (daylight neutral)"
exposure: "ETTR (Expose To The Right) without clipping"
neutrals_preserve: "#F2 to #FC (highlight retention)"
saturation: "Natural — no oversaturation"

### [SPECS_LIGHTING]
key_light: "Softbox difusa 45° (main light source)"
fill_light: "-1EV to -2EV (shadow recovery)"
rim_light: "Sutil (edge separation)"
flags: "Anti-spill (prevent color contamination)"
polarizer: "ON (reduce glare on reflective surfaces)"
hotspots: "AVOID (no blown highlights)"
shadows: "Suaves sem banding (smooth gradient)"

### [SPECS_OPTICS_GEOMETRY]
lenses: "50mm (standard), 85mm (portrait), 100mm macro"
shutter_base: "1/160s (default for static product)"
apertures: "Por cena (scene-specific):
  - f/8 for full focus (scenes 1, 6, 9)
  - f/4-f/5.6 for lifestyle/context (scenes 2, 4, 5, 7)
  - f/2.8 for macro/bokeh (scene 3)
  - f/5.6 for editorial detail (scene 8)"
projection: "Rectilinear (no distortion)"
horizon: "Nivelado (level horizon)"

### [SPECS_RENDER_QUALITY]
microcontrast: "ON (local contrast enhancement)"
antialias: "Limpo sem halos (clean edges)"
sharpen: "Moderate — sem oversharpen"
noise_reduction: "Discreta (preserve texture detail)"
moire: "OFF (no interference patterns)"
jpeg_artifacts: "OFF (no compression artifacts)"
resolution: "8K (high quality output)"

### [GLOBAL_NEGATIVES]
Apply to ALL scenes (non-negotiable):
```
no text, no watermark, no third-party logos, no border, no frame, no clutter, no glitches, no artifacts, no exaggerated lighting, no unrealistic materials/skin/fur, no extra brand marks, no captions, no reflections with text, no UI elements, no timestamps
```

### [SPECIAL_POLICY_GOLD]
**Rule**: Gold/golden accents ONLY as detail — never dominant color
**Rationale**: Prevents unrealistic "luxury" look; maintains product authenticity

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 3: CREATIVE VARIATION BANKS (RANDOMIZE=on)
## ═══════════════════════════════════════════════════════════════════════════

### [BANK_PNL_EMOTIONAL_TRIGGERS]
Purpose: Inject psychological triggers into prompts (copy-NLP influence)
Selection: Pick 1 per scene when RANDOMIZE=on

```
- "clareza que valida sua escolha"
- "superfície que convida ao toque"
- "visão total — nada escondido"
- "encaixa na rotina sem atrito"
- "brilho na medida inspira confiança"
- "decisão fácil, zero ruído"
- "respira, a temperatura desce"
- "silêncio térmico, descanso profundo"
- "conforto que se percebe já"
- "toque seguro, sempre pronto"
```

### [BANK_EMOTION_CORE]
Purpose: Define emotional tone for lifestyle scenes (2-8)
```
segurança | alívio | confiança | tranquilidade | paz | controle | pertencimento | valorização | clareza | frescor | descanso
```

### [BANK_CONTEXT_AMBIENT]
Purpose: Define environment for lifestyle/context scenes (random selection)
```
- "sala minimalista luz natural"
- "quarto arejado piso claro"
- "varanda sombreada urbana"
- "estúdio high-key clean"
- "cama pet área descanso"
- "sofá claro ambiente neutro"
- "transporte com manta"
- "piso vinílico claro moderno"
- "mesa trabalho organizada"
```

### [BANK_ACTION_INTERACTIONS]
Purpose: Define user/pet interactions for lifestyle scenes
```
- "deitar e relaxar"
- "tutor posicionando produto"
- "pet explorando curioso"
- "troca rápida manutenção"
- "pausa pós-atividade"
- "cochilo calmo profundo"
- "ajuste ergonômico"
- "momento de uso cotidiano"
```

### [BANK_CAMERA_ANGLES_RANDOM]
Purpose: Intentional gaps — let model choose creative angle when not specified
```
- "ângulo levemente superior (15°)"
- "ângulo frontal direto (0°)"
- "ângulo lateral 3/4 (45°)"
- "ângulo baixo heroico (−10°)"
- "ângulo superior observacional (60°)"
```

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 4: META-PROMPT UNIVERSAL TEMPLATE
## ═══════════════════════════════════════════════════════════════════════════

### [UNIVERSAL_PREFIX]
Apply to ALL prompts as header instruction:

```
"Generate 9 professional product photography images for [VARIAVEL] with strict brand/style fidelity. Resolution: 2000x2000px each, aspect ratio 1:1. Comply with marketplace standards (scenes 1 & 9: pure white background #FFFFFF). Scenes 2-8: prioritize real-world use, lifestyle context, and user/pet interaction (product is supporting actor, not hero). No text, no watermarks, no third-party logos."
```

### [BASE_TEMPLATE_STRUCTURE]
Each scene prompt follows this structure:

```
"Professional [PHOTOGRAPHY_TYPE] photography, [SUBJECT_DESCRIPTION], [CATEGORY], lighting: [LIGHTING_SPEC], background: [BACKGROUND_SPEC], camera: [FOCAL_LENGTH] [APERTURE], composition: [COMPOSITION_SPEC], psychological trigger: [PNL_TRIGGER], no watermarks, no text overlay, brand/style lock to [VARIAVEL], 8K high quality"
```

**Intentional Gaps (to be filled by AI model based on context):**
- Secondary lighting position (intentionally not specified)
- Exact prop placement (generic "neutral props" mentioned)
- Minor angle variations within specified range
- Background texture details (when not white)

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 5: 9-SCENE GRID SPECIFICATION (3×3 LAYOUT)
## ═══════════════════════════════════════════════════════════════════════════

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ CENA 1: CAPA DUPLA BRANCA — PRODUTO HERÓI CONTROLADO                 ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[SCENE_1_SPECS]
position: "Top-left (Grid 3×3)"
hero_status: "YES (produto é protagonista)"
goal: "Apresentar produto com fidelidade total e compliance marketplace"
background: "#FFFFFF pure white (marketplace requirement)"
composition: "Dois recortes do produto: 20% (escala pequena, canto) + 80% (centro dominante)"
camera: "50mm, f/8, 1/160s, ISO 100"
lighting: "High-key limpo, sombras suaves uniformes"
pnl_trigger: "clareza imediata, decisão simples"
compliance: "CRITICAL — fundo branco obrigatório para Mercado Livre, Amazon"

[FORMULA_CENA_1]
```
Professional product photography, [VARIAVEL], pure white background #FFFFFF, two cutouts of product (20% scale in corner + 80% centered dominant), clean alignment symmetrical, camera 50mm f/8 1/160s ISO 100, high-key lighting with soft uniform shadows, full focus sharp, texture visible, PNL: "immediate clarity simple decision", no watermarks, no text, brand/style lock to [VARIAVEL], 8K
```

[EXAMPLE_CENA_1]
Product: "Cama Suspensa para Gato com Ventosas Oxford 600D Cinza"
```
Professional product photography, cama suspensa para gato Oxford 600D cinza, pure white background #FFFFFF, two cutouts of product (20% lower corner + 80% center) showing scale and transparent suction cups, clean symmetrical alignment, camera 50mm f/8 1/160s ISO 100, high-key lighting soft uniform shadows, full focus sharp oxford texture visible, PNL: "immediate clarity simple decision", no watermarks, no text, brand/style lock, 8K
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ CENA 2: USO REAL — LIFESTYLE BENEFÍCIO VISÍVEL                       ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[SCENE_2_SPECS]
position: "Top-center (Grid 3×3)"
hero_status: "NO (usuário/pet é protagonista)"
goal: "Mostrar benefício em uso real com público-alvo"
composition: "Usuário/pet em primeiro plano emocional (60-70% quadro); produto 30-40%"
camera: "85mm, f/4"
lighting: "Luz natural difusa lateral"
background: "Ambiente minimalista neutro (BANK_CONTEXT_AMBIENT)"
pnl_trigger: "corpo relaxa, benefício imediato"
intentional_gap: "Ângulo exato e iluminação secundária (deixar modelo decidir)"

[FORMULA_CENA_2]
```
Professional lifestyle photography, [PUBLICO_ALVO] in emotional foreground using [VARIAVEL] (product 30-40% frame), [BANK_CONTEXT_AMBIENT] environment, visible benefit [BENEFICIO_PRINCIPAL], soft natural diffused lighting, camera 85mm f/4, storytelling composition, PNL: "body relaxes immediate benefit", no watermarks, brand/style lock, 8K
```

[EXAMPLE_CENA_2]
```
Professional lifestyle photography, gray cat in emotional foreground comfortably resting in cama suspensa janela (product 35% frame), minimalist apartment with natural light environment, visible thermal relief benefit (pet fresh and calm), soft diffused afternoon light, camera 85mm f/4, natural storytelling composition, PNL: "body relaxes heat dissipates", no watermarks, brand/style lock, 8K
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ CENA 3: DETALHE MACRO — PONTO CRÍTICO EM USO                         ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[SCENE_3_SPECS]
position: "Top-right (Grid 3×3)"
hero_status: "NO (foco no detalhe técnico em uso)"
goal: "Evidenciar ponto crítico de qualidade/funcionalidade durante uso real"
composition: "Macro extremo no ponto de contato/apoio; contexto desfocado (bokeh limpo)"
camera: "100mm macro, f/2.8"
lighting: "Controlada lateral para revelar textura (evitar flare)"
background: "Bokeh limpo baixa saturação"
pnl_trigger: "toque seguro, conforto contínuo"

[FORMULA_CENA_3]
```
Professional macro photography in use, extreme close-up on critical contact point [DETALHE_ESPECIFICO] during real use, user/pet partially visible (context), camera 100mm macro f/2.8, clean bokeh, low saturation, controlled lateral lighting no flare, PNL: "secure touch continuous comfort", no watermarks, brand/style lock, 8K
```

[EXAMPLE_CENA_3]
```
Professional macro photography in use, extreme close-up on cat's paw resting on Oxford cushion showing soft texture and comfortable contact, cat fur partially visible (emotional context), transparent suction cup blurred background, camera 100mm macro f/2.8, clean bokeh, neutral low saturation, lateral lighting no flare, PNL: "secure touch continuous comfort", no watermarks, brand/style lock, 8K
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ CENA 4: ROTINA DO USUÁRIO — FACILIDADE DE USO                        ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[SCENE_4_SPECS]
position: "Middle-left (Grid 3×3)"
hero_status: "NO (foco na interação humana)"
goal: "Demonstrar facilidade de instalação/manutenção/ajuste"
composition: "Meio-plano (mãos do usuário + produto); horizon nivelado; respiro visual"
camera: "50mm, f/5.6"
lighting: "Natural ambiente"
background: "Contexto real neutro (BANK_CONTEXT_AMBIENT)"
pnl_trigger: "simples de usar, sempre pronto"
intentional_gap: "Gênero/etnia das mãos não especificado (modelo decide)"

[FORMULA_CENA_4]
```
Professional lifestyle mid-shot photography, user's hands positioning/adjusting [VARIAVEL], [BANK_ACTION_INTERACTIONS], level horizon, visual breathing room, [BANK_CONTEXT_AMBIENT] environment, camera 50mm f/5.6, natural composition, PNL: "easy to use always ready", no watermarks, brand/style lock, 8K
```

[EXAMPLE_CENA_4]
```
Professional lifestyle mid-shot photography, user's hands (neutral skin tone unidentifiable) fixing suction cups of cama on clean glass window, natural "quick swap" gesture, level horizon with blurred urban view background, visual breathing room clean, minimalist living room environment, camera 50mm f/5.6, natural storytelling composition, PNL: "easy to use always ready", no watermarks, brand/style lock, 8K
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ CENA 5: CENÁRIO DE BENEFÍCIO — STORY BEAT EMOCIONAL                  ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[SCENE_5_SPECS]
position: "Middle-center (Grid 3×3)"
hero_status: "NO (foco na emoção do usuário/pet)"
goal: "Sugerir transformação/alívio sem texto (visual storytelling)"
composition: "Usuário/pet em momento de benefício; produto parcial (30% quadro)"
camera: "85mm, f/4"
lighting: "Temperatura de cor fria 5000K (sugere frescor/alívio)"
background: "Neutro desfocado"
pnl_trigger: "alívio que você sente"

[FORMULA_CENA_5]
```
Professional lifestyle story beat photography, [PUBLICO_ALVO] in moment of relief/benefit, cool color temperature 5000K, calm relaxed expression, [VARIAVEL] partially visible (30% frame), suggestion of comfort/relief without text, cool controlled lighting, camera 85mm f/4, emotional intimate composition, PNL: "relief you feel", no watermarks, brand/style lock, 8K
```

[EXAMPLE_CENA_5]
```
Professional lifestyle story beat photography, gray cat with half-closed eyes in moment of thermal relief, cool color temperature 5000K transmitting freshness, calm expression stretched paw relaxed, cama suspensa partially visible (35% lower frame), suggestion of body cooling without text, cool diffused controlled lighting, camera 85mm f/4, emotional intimate composition, PNL: "relief you feel", no watermarks, brand/style lock, 8K
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ CENA 6: TOP-DOWN FUNCIONAL EM USO                                    ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[SCENE_6_SPECS]
position: "Middle-right (Grid 3×3)"
hero_status: "NO (foco na funcionalidade em uso)"
goal: "Visão superior do uso real — demonstrar ergonomia/encaixe"
composition: "Vista superior; usuário/pet ocupando produto; área de contato destacada"
camera: "50mm, f/8"
lighting: "High-key cenital; reflexos controlados"
background: "Contexto real (piso/superfície)"
pnl_trigger: "tudo no lugar, conforto pleno"

[FORMULA_CENA_6]
```
Professional top-down photography in use, aerial view of [PUBLICO_ALVO] occupying [VARIAVEL], contact area highlighted as visual focus, [BANK_ACTION_INTERACTIONS], high-key overhead lighting controlled reflections, camera 50mm f/8, centered geometric composition, PNL: "everything in place full comfort", no watermarks, brand/style lock, 8K
```

[EXAMPLE_CENA_6]
```
Professional top-down photography in use, aerial view of gray cat curled up occupying cama suspensa janela, contact area cushion highlighted (pet body guides eye), "calm nap" natural action, transparent suction cups visible corners, high-key overhead lighting controlled glass reflections, camera 50mm f/8, centered symmetrical geometric composition, PNL: "everything in place full comfort", no watermarks, brand/style lock, 8K
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ CENA 7: CONTEXTO DE VIDA — VERSATILIDADE NO COTIDIANO                ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[SCENE_7_SPECS]
position: "Bottom-left (Grid 3×3)"
hero_status: "NO (foco no contexto real de uso)"
goal: "Mostrar versatilidade e integração no cotidiano"
composition: "Produto integrado em ambiente real; usuário/pet interagindo; props neutros"
camera: "50-85mm, f/4-f/5.6"
lighting: "Natural ambiente; DOF moderada"
background: "Contexto real (BANK_CONTEXT_AMBIENT)"
pnl_trigger: "cabe na rotina sem esforço"
intentional_gap: "Props específicos não detalhados (modelo escolhe)"

[FORMULA_CENA_7]
```
Professional lifestyle real context photography, [VARIAVEL] integrated in [BANK_CONTEXT_AMBIENT], [PUBLICO_ALVO] interacting naturally, neutral props no third-party brands, visible versatility, natural ambient lighting, moderate DOF (context slightly blurred), camera 50-85mm f/4-5.6, PNL: "fits routine effortlessly", no watermarks, brand/style lock, 8K
```

[EXAMPLE_CENA_7]
```
Professional lifestyle real context photography, cama suspensa gato fixed on airy bedroom window, striped cat exploring product with natural curiosity, neutral props (beige curtain no brand, light vinyl floor), visible domestic versatility, soft lateral natural window lighting, moderate DOF (bedroom background slightly blurred), camera 85mm f/5.6, PNL: "fits routine effortlessly", no watermarks, brand/style lock, 8K
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ CENA 8: QUALIDADE PERCEBIDA EM USO — EDITORIAL MATERIAL              ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[SCENE_8_SPECS]
position: "Bottom-center (Grid 3×3)"
hero_status: "NO (foco no material durante uso)"
goal: "Transmitir valor percebido através da qualidade do material em uso real"
composition: "Close editorial no material durante contato; textura nítida; sem highlights estourados"
camera: "85mm, f/5.6"
lighting: "Spot lateral f/5.6 controlado (revelar densidade do material)"
background: "Contexto de uso desfocado"
pnl_trigger: "acabamento que inspira confiança"

[FORMULA_CENA_8]
```
Professional editorial mid-shot photography, [MATERIAIS] of [VARIAVEL] in real use, sharp texture showing quality during contact, no blown highlights, controlled lateral spot lighting f/5.6, camera 85mm f/5.6, composition transmits perceived value, PNL: "finish that inspires trust", no watermarks, brand/style lock, 8K
```

[EXAMPLE_CENA_8]
```
Professional editorial mid-shot photography, Oxford 600D gray fabric of cama in use with cat lying (partial), sharp resistant weave texture showing quality during pet contact, visible reinforced stitching edge, no blown highlights on fabric, controlled lateral spot lighting f/5.6 revealing material density, camera 85mm f/5.6, composition transmits premium durability, PNL: "finish that inspires trust", no watermarks, brand/style lock, 8K
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ CENA 9: CAPA BRANCA COMERCIAL — PRODUTO HERÓI VENDA DIRETA           ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[SCENE_9_SPECS]
position: "Bottom-right (Grid 3×3)"
hero_status: "YES (produto é protagonista)"
goal: "Venda direta com clareza total — última chance de conversão"
background: "#FFFFFF pure white (marketplace requirement)"
composition: "Frontal; produto ~85% do quadro; recorte perfeito limpo"
camera: "50mm, f/8, 1/160s, ISO 100"
lighting: "Sombras suaves uniformes; high-key"
pnl_trigger: "simples, pronto, confiável"
compliance: "CRITICAL — fundo branco obrigatório"

[FORMULA_CENA_9]
```
Professional commercial product photography, [VARIAVEL] frontal occupying ~85% frame, pure white background #FFFFFF infinite, perfect clean cutout, camera 50mm f/8 1/160s ISO 100, soft uniform shadows lighting, full sharp focus, detailed texture, PNL: "simple ready reliable", no watermarks, no text, brand/style lock to [VARIAVEL], 8K
```

[EXAMPLE_CENA_9]
```
Professional commercial product photography, cama suspensa gato Oxford 600D gray frontal occupying 85% frame, transparent suction cups steel structure visible, pure white background #FFFFFF infinite, perfect cutout no hard shadows, camera 50mm f/8 1/160s ISO 100, soft uniform shadows lighting, full sharp focus detailed oxford texture, PNL: "simple ready reliable", no watermarks, no text, brand/style lock, 8K
```

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 6: OUTPUT FORMAT OPTIONS
## ═══════════════════════════════════════════════════════════════════════════

### [OPTION_A_GRID_3X3]
**Description**: Generate 1 single PNG 2000x2000 containing 9 scenes in 3×3 grid layout
**Use case**: Quick marketplace upload (single image with full story)
**Prompt prefix to add**:
```
"Arrange all 9 scenes in a 3×3 grid layout (666×666px per scene) in a single 2000×2000px PNG. No gaps between scenes. Pure white background #FFFFFF. Final output: 1 PNG file."
```

**Example instruction block for AI generator:**
```
LAYOUT GRID 3×3:
┌─────────┬─────────┬─────────┐
│ CENA 1  │ CENA 2  │ CENA 3  │
│ Branca  │ Uso     │ Macro   │
├─────────┼─────────┼─────────┤
│ CENA 4  │ CENA 5  │ CENA 6  │
│ Rotina  │ Benefic │ Top-down│
├─────────┼─────────┼─────────┤
│ CENA 7  │ CENA 8  │ CENA 9  │
│ Contexto│ Material│ Branca  │
└─────────┴─────────┴─────────┘

Single PNG output: 2000×2000px
No gaps between scenes
```

---

### [OPTION_B_SEQUENCE_9PNG]
**Description**: Generate 9 separate PNGs (2000×2000px each) in sequential order
**Use case**: Maximum flexibility for A/B testing, carousel ads, independent optimization
**Prompt handling**: Each scene prompt generates 1 independent PNG

**File naming convention:**
```
[VARIAVEL]_scene_01_capa_branca.png          (2000×2000)
[VARIAVEL]_scene_02_uso_real.png             (2000×2000)
[VARIAVEL]_scene_03_macro_detalhe.png        (2000×2000)
[VARIAVEL]_scene_04_rotina_usuario.png       (2000×2000)
[VARIAVEL]_scene_05_beneficio_story.png      (2000×2000)
[VARIAVEL]_scene_06_topdown_funcional.png    (2000×2000)
[VARIAVEL]_scene_07_contexto_vida.png        (2000×2000)
[VARIAVEL]_scene_08_qualidade_material.png   (2000×2000)
[VARIAVEL]_scene_09_capa_branca_comercial.png(2000×2000)
```

**Advantage**: Independent optimization per scene; easier iteration; A/B testing flexibility

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 7: PROMPT VALIDATION PROTOCOL
## ═══════════════════════════════════════════════════════════════════════════

### [VALIDATION_CHECKLIST]
Each generated prompt MUST pass these checks:

**Length & Clarity:**
- [ ] ≥80 characters (sufficient detail for AI)
- [ ] ≤350 characters (avoid token overflow)
- [ ] Clear subject description (not vague)
- [ ] Objective language (no subjective terms like "beautiful", "amazing")

**Technical Specs:**
- [ ] Camera specified (focal length + aperture)
- [ ] Lighting described (type + direction)
- [ ] Background mentioned (white #FFFFFF or context)
- [ ] Composition defined (angle/perspective)
- [ ] Resolution/quality stated ("8K high quality")

**Compliance:**
- [ ] Contains "no watermarks" instruction
- [ ] Contains "no text" instruction
- [ ] Contains "no third-party logos" instruction
- [ ] Contains "brand/style lock to [VARIAVEL]" instruction
- [ ] No impossible instructions for AI (no "add text", no "show back and front simultaneously")

**Meta-Prompt Integrity:**
- [ ] Uses `[VARIAVEL]` as placeholder (not specific product name hardcoded)
- [ ] Leaves intentional gaps (angles, secondary lighting, props — not overspecified)
- [ ] Generic enough to work for ANY product in category
- [ ] Copy-paste ready (no preprocessing needed)

### [VIOLATION_EXAMPLES]
**TOO SHORT (FAIL)**:
```
"Product on white background 8K"
```
→ Lacks detail; AI cannot generate meaningful image

**TOO VAGUE (FAIL)**:
```
"Beautiful product photography with amazing lighting and stunning composition"
```
→ Subjective terms; no technical specs

**MISSING COMPLIANCE (FAIL)**:
```
"Professional photography, [VARIAVEL], white background, 50mm f/8"
```
→ Missing "no watermarks", "no text", "brand/style lock" instructions

**OVERSPECIFIED (FAIL)**:
```
"Professional photography, [VARIAVEL], white background, 50mm f/8, key light at exactly 45° from left side at 1000 lumens, fill light at 32° from right at 500 lumens, rim light at 180° at 200 lumens..."
```
→ Too specific; removes model creativity; over-tokenization

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 8: EXECUTION LOGIC & WORKFLOW
## ═══════════════════════════════════════════════════════════════════════════

### [EXECUTION_STEPS]

**STEP 1: PARSE INPUT**
- Extract `[VARIAVEL]`, `[CATEGORIA]`, `[DIFERENCIAIS_VISUAIS]`, `[BENEFICIO_PRINCIPAL]`, `[PUBLICO_ALVO]`
- Check for optional inputs: `[REFERENCE_IMAGE_URL]`, `[MATERIAIS]`, `[CORES_DISPONIVEIS]`
- Determine `OUTPUT_MODE`: `grid_3x3` or `sequence_9png`
- Check `RANDOMIZE` flag: if `on`, activate variation banks (BANK_PNL, BANK_CONTEXT, etc.)

**STEP 2: GENERATE 9 PROMPTS**
- For each scene (1-9):
  → Apply scene-specific formula (FORMULA_CENA_X)
  → Replace `[VARIAVEL]` with input value
  → Replace `[CATEGORIA]` with input value
  → Replace `[BENEFICIO_PRINCIPAL]` with input value
  → Replace `[PUBLICO_ALVO]` with input value
  → If `RANDOMIZE=on`: inject random selection from BANK_PNL, BANK_CONTEXT, BANK_ACTION
  → Append GLOBAL_NEGATIVES
  → Append "brand/style lock to [VARIAVEL]"
  → Validate against VALIDATION_CHECKLIST

**STEP 3: FORMAT OUTPUT**
- If `OUTPUT_MODE=grid_3x3`:
  → Prepend universal grid layout instruction to prompt set
  → Output 1 combined prompt block

- If `OUTPUT_MODE=sequence_9png`:
  → Output 9 independent prompts with file naming convention
  → Each prompt generates 1 separate PNG

**STEP 4: QUALITY ASSURANCE**
- Run validation checks on all 9 prompts
- Flag any violations (length, clarity, compliance)
- Provide compliance score: `PASS (9/9)` or `PARTIAL (X/9)`

**STEP 5: DELIVER STRUCTURED OUTPUT**
- Format as structured markdown with clear sections
- Include metadata: total prompts, validation status, estimated generation time
- Provide copy-paste ready prompts (no preprocessing needed)

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 9: CATEGORY-SPECIFIC ADAPTATIONS
## ═══════════════════════════════════════════════════════════════════════════

### [ADAPTATION_ELETRONICOS]
Focus: LEDs, displays, ports, buttons, connectivity
Macro scenes: Connectors, interfaces, charging ports
Lifestyle scenes: Person using headphones, typing on keyboard, etc.
Example differentials: "LED azul status", "USB-C port", "touch controls"

### [ADAPTATION_PET_SHOP]
Focus: Pet interaction, comfort, safety, materials
Macro scenes: Fabric texture, stitching, safety mechanisms
Lifestyle scenes: Pet exploring, resting, playing with product
Example differentials: "tecido Oxford resistente", "ventosas seguras", "almofada removível"

### [ADAPTATION_MODA_ACESSORIOS]
Focus: Fabric texture, stitching, closures, prints
Macro scenes: Seams, zippers, button holes, embroidery
Lifestyle scenes: Person wearing item or styled on mannequin
Example differentials: "costura reforçada", "zíper YKK", "estampa exclusiva"

### [ADAPTATION_CASA_DECORACAO]
Focus: Materials (wood, metal, glass), integration in space, style
Macro scenes: Wood grain, metal finish, glass clarity
Lifestyle scenes: Product in decorated room, showing scale and fit
Example differentials: "madeira maciça", "acabamento fosco", "design minimalista"

### [ADAPTATION_COSMETICOS]
Focus: Packaging, texture, application, results
Macro scenes: Dropper, pump, texture close-up
Lifestyle scenes: Person applying product, visible skin improvement
Example differentials: "embalagem airless", "textura gel-creme", "FPS 50+"

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 10: OUTPUT TEMPLATE (STRUCTURED MARKDOWN)
## ═══════════════════════════════════════════════════════════════════════════

### [OUTPUT_FORMAT_TEMPLATE]

```markdown
# ═══════════════════════════════════════════════════════════════════════════
# IMAGE PROMPTS: [VARIAVEL]
# ═══════════════════════════════════════════════════════════════════════════

[METADATA]
product: "[VARIAVEL]"
category: "[CATEGORIA]"
output_mode: "[grid_3x3 | sequence_9png]"
total_prompts: 9
validation_status: "PASS (9/9)" | "PARTIAL (X/9)" | "FAIL (X/9)"
randomize: "[on | off]"
estimated_generation_time: "<15s"
compliance_level: "CRITICAL"

---

## OPÇÃO A: GRID 3×3 (1 PNG 2000×2000)

### UNIVERSAL INSTRUCTION FOR GRID:
```
Generate 9 professional product photography images for [VARIAVEL] arranged in 3×3 grid layout (666×666px per scene) in single 2000×2000px PNG. No gaps between scenes. Pure white background #FFFFFF for entire grid. Scenes 1 & 9: product hero on white. Scenes 2-8: lifestyle/use context. No text, no watermarks, no third-party logos. Brand/style lock to [VARIAVEL].
```

### GRID LAYOUT:
┌─────────────┬─────────────┬─────────────┐
│ CENA 1      │ CENA 2      │ CENA 3      │
│ Branca Herói│ Uso Real    │ Macro       │
├─────────────┼─────────────┼─────────────┤
│ CENA 4      │ CENA 5      │ CENA 6      │
│ Rotina User │ Benefício   │ Top-Down    │
├─────────────┼─────────────┼─────────────┤
│ CENA 7      │ CENA 8      │ CENA 9      │
│ Contexto    │ Material    │ Branca Hero │
└─────────────┴─────────────┴─────────────┘

---

## OPÇÃO B: SEQUÊNCIA 9 PNGs (2000×2000 cada)

### CENA 1: CAPA BRANCA HERÓI
**File**: `[VARIAVEL]_scene_01_capa_branca.png`
**Type**: Product Hero — White Background
**Prompt**:
```
[GENERATED_PROMPT_CENA_1]
```
**Validation**: ✅ PASS (127 chars, specs compliant, compliance OK)

---

### CENA 2: USO REAL LIFESTYLE
**File**: `[VARIAVEL]_scene_02_uso_real.png`
**Type**: Lifestyle — Real Use with User/Pet
**Prompt**:
```
[GENERATED_PROMPT_CENA_2]
```
**Validation**: ✅ PASS (153 chars, specs compliant, compliance OK)

---

### CENA 3: MACRO DETALHE
**File**: `[VARIAVEL]_scene_03_macro_detalhe.png`
**Type**: Macro — Critical Detail in Use
**Prompt**:
```
[GENERATED_PROMPT_CENA_3]
```
**Validation**: ✅ PASS (148 chars, specs compliant, compliance OK)

---

### CENA 4: ROTINA USUÁRIO
**File**: `[VARIAVEL]_scene_04_rotina_usuario.png`
**Type**: Lifestyle — User Routine Interaction
**Prompt**:
```
[GENERATED_PROMPT_CENA_4]
```
**Validation**: ✅ PASS (161 chars, specs compliant, compliance OK)

---

### CENA 5: BENEFÍCIO STORY BEAT
**File**: `[VARIAVEL]_scene_05_beneficio_story.png`
**Type**: Lifestyle — Emotional Benefit Moment
**Prompt**:
```
[GENERATED_PROMPT_CENA_5]
```
**Validation**: ✅ PASS (159 chars, specs compliant, compliance OK)

---

### CENA 6: TOP-DOWN FUNCIONAL
**File**: `[VARIAVEL]_scene_06_topdown_funcional.png`
**Type**: Functional — Aerial View in Use
**Prompt**:
```
[GENERATED_PROMPT_CENA_6]
```
**Validation**: ✅ PASS (144 chars, specs compliant, compliance OK)

---

### CENA 7: CONTEXTO DE VIDA
**File**: `[VARIAVEL]_scene_07_contexto_vida.png`
**Type**: Lifestyle — Real Life Context
**Prompt**:
```
[GENERATED_PROMPT_CENA_7]
```
**Validation**: ✅ PASS (152 chars, specs compliant, compliance OK)

---

### CENA 8: QUALIDADE MATERIAL
**File**: `[VARIAVEL]_scene_08_qualidade_material.png`
**Type**: Editorial — Material Quality in Use
**Prompt**:
```
[GENERATED_PROMPT_CENA_8]
```
**Validation**: ✅ PASS (167 chars, specs compliant, compliance OK)

---

### CENA 9: CAPA BRANCA COMERCIAL
**File**: `[VARIAVEL]_scene_09_capa_branca_comercial.png`
**Type**: Product Hero — Commercial White Background
**Prompt**:
```
[GENERATED_PROMPT_CENA_9]
```
**Validation**: ✅ PASS (134 chars, specs compliant, compliance OK)

---

## ═══════════════════════════════════════════════════════════════════════════
## COMPLIANCE REPORT
## ═══════════════════════════════════════════════════════════════════════════

**Validation Summary:**
- Total Prompts: 9
- Passed: 9/9 (100%)
- Failed: 0/9 (0%)
- Compliance Level: ✅ CRITICAL (all checks passed)

**Compliance Checks:**
- [✅] All prompts ≥80 characters
- [✅] All prompts ≤350 characters
- [✅] All prompts contain "no watermarks"
- [✅] All prompts contain "no text"
- [✅] All prompts contain "no third-party logos"
- [✅] All prompts contain "brand/style lock to [VARIAVEL]"
- [✅] Scenes 1 & 9: white background #FFFFFF (marketplace compliance)
- [✅] Technical specs present (camera, lighting, composition)
- [✅] Generic meta-prompt structure (works for any product)

**Estimated Generation Time:** <15 seconds (all 9 scenes)

---

## ═══════════════════════════════════════════════════════════════════════════
## NOTAS DE FALLBACK & OBSERVAÇÕES
## ═══════════════════════════════════════════════════════════════════════════

**Fallback Strategy** (if input incomplete):
- Use generic category descriptions
- Focus on standard angles (frontal, 45°, top-down)
- Alert in notes that prompts are generic
- NEVER invent visual features that don't exist

**Performance Targets:**
- Generation: <15s for 9 prompts
- Validation: <3s
- Total: <20s

**Quality Gates:**
- Min compliance score: 100% (9/9 PASS)
- Min prompt length: 80 chars
- Max prompt length: 350 chars

**Revision Strategy:**
- If validation fails: auto-correct and re-validate once
- If still fails: flag for human review
- NEVER skip compliance checks

```

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 11: RELATIONSHIP TO OTHER MODULES
## ═══════════════════════════════════════════════════════════════════════════

### [UPSTREAM_INPUTS]
**From**: `input_parser_HOP.md`
- Research notes with product specs
- Visual differentiators
- Target audience
- Benefits and pain points

**From**: User Brief
- `[VARIAVEL]` (product name)
- `[CATEGORIA]` (category)
- Optional: `[REFERENCE_IMAGE_URL]`

### [DOWNSTREAM_OUTPUTS]
**To**: Final Output (`PROMPTS_IMAGENS` block)
- 9 copy-paste ready prompts
- Grid layout instruction (if OPTION A)
- File naming convention (if OPTION B)

**To**: `qa_validation_HOP.md`
- Prompts for compliance validation
- Metadata for audit trail

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 12: CRITICAL SUCCESS FACTORS
## ═══════════════════════════════════════════════════════════════════════════

### [SUCCESS_CRITERIA]
1. **Universal Applicability**: Prompts work for ANY product/service/brand (not hardcoded)
2. **Copy-Paste Ready**: No preprocessing or editing needed by user
3. **Compliance 100%**: All prompts pass validation (no watermarks, no text, no logos)
4. **Professional Specs**: Camera, lighting, composition specified in every prompt
5. **Intentional Gaps**: Secondary elements left to model creativity (angles, props)
6. **Output Flexibility**: User chooses Grid 3×3 OR Sequential 9 PNGs
7. **Speed**: <15s generation + <3s validation = <20s total
8. **Marketplace Ready**: Scenes 1 & 9 white background #FFFFFF (ML/Amazon compliance)

### [FAILURE_MODES_TO_AVOID]
- ❌ Hardcoding specific product names (breaks universality)
- ❌ Overspecifying every detail (kills model creativity)
- ❌ Vague prompts ("beautiful product photo") — not AI-generatable
- ❌ Missing compliance instructions (watermark risk)
- ❌ Impossible instructions ("show front and back simultaneously")
- ❌ Subjective language ("stunning", "amazing") — not objective
- ❌ Skipping validation checks (quality risk)

---

**END OF MODULE: image_prompts_generator_HOP.md**
**Version**: 2.1.0
**Framework**: HOP (Hierarchical Operational Protocol)
**Status**: PRODUCTION-READY
**Last Updated**: 2025-11-10
