# 101_ADW_ANUNCIO_BRIDGE

**ID**: 101_ADW_ANUNCIO_BRIDGE
**Version**: 1.0.0
**Type**: ADW (Bridge Workflow)
**Chain**: anuncio_agent → photo_agent

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_anuncio_bridge",
  "workflow_name": "Anuncio to Photo Bridge",
  "agent": "photo_agent",
  "version": "1.0.0",
  "type": "bridge",
  "chain": "anuncio_agent → photo_agent",
  "context_strategy": "isolated",
  "failure_handling": "stop_and_report",
  "min_llm_model": "claude-sonnet-4-20250514",
  "required_capabilities": {
    "scout_mcp": true,
    "file_parsing": true,
    "markdown_extraction": true,
    "pnl_mapping": true
  },
  "quality_threshold": 7.0,
  "estimated_duration": "2-3 minutes",
  "phases": ["LOCATE", "EXTRACT", "VALIDATE", "HANDOFF"]
}
```

---

## PURPOSE

Bridges product copy output from `anuncio_agent` to `photo_agent` input, transforming marketplace copy (benefits, features, emotional triggers) into visual scene descriptions, mood, and style directives for AI image generation.

**Transform**: Persuasive text → Visual concepts
**Goal**: Ensure product photos align with ad copy emotional positioning and key selling points

---

## INPUT_CONTRACT

From `anuncio_agent`:
- `$anuncio_file`: Path to anuncio output (user_anuncios/*.md)

Expected anuncio data:
```markdown
## TITULO
[Product name + keywords]

## BULLETS
1. [Feature/benefit with mental trigger] (250-299 chars)
2. [Feature/benefit with mental trigger] (250-299 chars)
...

## DESCRICAO
[StoryBrand long copy with emotional positioning, dores, ganhos, transformacao]

## KEYWORDS
Bloco 1: [keyword list]
Bloco 2: [keyword list]

## METADATA (optional)
emocao_alvo: [primary emotion]
categoria: [product category]
marketplace_target: [ML/Shopee/Magalu/Amazon]
```

---

## PHASES

### Phase 1: LOCATE (30s)
Discover anuncio outputs for target product.

```bash
# Using Scout
mcp__scout__discover("anuncio output for [product_name]")

# OR direct glob
Glob: user_anuncios/*[product_name]*.md
```

**Output**: `$anuncio_paths` (list of matching files)

**Error Handling**:
- If no files found → HALT: "No anuncio found for [product]. Run anuncio_agent first or specify file path."
- If multiple files → SELECT: Most recent (by timestamp) or prompt user

---

### Phase 2: EXTRACT (1min)
Parse anuncio and transform copy elements into visual concepts.

**Extraction Mapping**:
```python
ANUNCIO_TO_PHOTO = {
    "TITULO": {
        "keywords": "subject_description",
        "product_name": "primary_subject"
    },
    "BULLETS": {
        "features": "hero_shot_elements",
        "benefits": "lifestyle_context",
        "mental_triggers": "pnl_triggers"
    },
    "DESCRICAO": {
        "emocao_alvo": "mood_primary",
        "dores": "scene_problems_solved",
        "ganhos": "scene_transformations",
        "transformacao": "emotional_arc"
    },
    "KEYWORDS": {
        "head_terms": "visual_elements",
        "long_tail": "scene_details"
    },
    "METADATA": {
        "categoria": "style_selection",
        "marketplace_target": "compliance_mode"
    }
}
```

**Copy → Visual Translation**:

| Anuncio Element | Photo Context | Example |
|-----------------|---------------|---------|
| "Design modular" | Scene description: modular assembly | "Product shown with detachable components, exploded view" |
| "Material premium" | Texture focus shot | "Macro detail showing material texture, high-end finish" |
| "Fácil de usar" | Lifestyle shot with user | "Person effortlessly using product, natural motion" |
| Emocao: "orgulho" | PNL trigger: "confiança" | High-key lighting, centered composition, eye-level |
| Emocao: "praticidade" | PNL trigger: "clareza" | Clean background, sharp focus, organized layout |
| Emocao: "exclusividade" | PNL trigger: "desejo" | Dramatic lighting, low-key, luxury mood |

**Mental Trigger Translation**:
```json
{
  "escassez": "urgência",
  "prova_social": "pertencimento",
  "autoridade": "confiança",
  "reciprocidade": "conforto",
  "compromisso": "controle",
  "afinidade": "pertencimento",
  "novidade": "transformação"
}
```

**Marketplace-Specific Visual Requirements**:
```json
{
  "Mercado Livre": {
    "compliance_mode": "marketplace",
    "scene_1": "white background #FFFFFF (mandatory)",
    "scene_9": "white background #FFFFFF (mandatory)",
    "style": "commercial"
  },
  "Shopee": {
    "compliance_mode": "marketplace",
    "lifestyle_required": true,
    "style": "lifestyle"
  },
  "Amazon BR": {
    "compliance_mode": "marketplace",
    "infographic_allowed": true,
    "style": "editorial"
  }
}
```

**Output**: `$photo_context` (structured JSON)

**Error Handling**:
- If TITULO missing → HALT: "No product title found in anuncio. Cannot determine subject."
- If BULLETS missing → WARN: "No bullets found. Photo context will lack feature-specific scenes."
- If DESCRICAO too short (<1000 chars) → WARN: "Description brief. Emotional context may be limited."

---

### Phase 3: VALIDATE (30s)
Check data completeness and visual concept quality.

**Validation Checklist**:
```markdown
- [ ] Subject description extracted (from TITULO)
- [ ] At least 3 visual scenes defined (from BULLETS)
- [ ] PNL triggers mapped (at least 1)
- [ ] Mood/emotional tone defined (from DESCRICAO)
- [ ] Style appropriate for category
- [ ] Marketplace compliance requirements included (if applicable)
- [ ] Quality score ≥7.0/10
```

**Quality Scoring Rubric**:
```json
{
  "subject_clarity": 2.0,  // Clear product description
  "scene_diversity": 2.0,  // 3+ distinct scene types (hero, lifestyle, detail)
  "emotional_alignment": 2.0,  // PNL triggers match anuncio emotion
  "visual_completeness": 2.0,  // All required elements present
  "compliance_ready": 2.0   // Marketplace requirements met
}
```

**Output**: `$validation_result` (pass/fail + score)

**Error Handling**:
- If quality_score <7.0 → RETRY: "Quality too low ([X]/10). Missing: [list deficiencies]"
- If subject_unclear → HALT: "Cannot define photography subject. Anuncio title unclear or product ambiguous."
- If pnl_unmapped → WARN: "No PNL triggers extracted. Photos may lack emotional resonance."

---

### Phase 4: HANDOFF (30s)
Prepare structured context for photo_agent input.

**Handoff Format**:
```handoff
contexto: Anuncio complete for [product_name]
arquivos_gerados:
  - user_anuncios/[product]_anuncio.md
proximo: Run photo_agent with visual context
dados:
  subject: $photo_context.subject
  style: $photo_context.style
  scenes: 9
  pnl_triggers: $photo_context.pnl_triggers
  brand_profile:
    mood: $photo_context.mood
    target_audience: $photo_context.target_audience
  compliance_mode: $photo_context.compliance_mode
scene_concepts:
  - hero_pack_shot: $photo_context.scenes.hero
  - lifestyle_use_case: $photo_context.scenes.lifestyle
  - detail_feature: $photo_context.scenes.detail
  - [additional scenes...]
qualidade: $validation_result.score
midjourney_hints:
  - Focus on [key feature from bullets]
  - Emphasize [material/texture from description]
  - Mood: [emotional tone from anuncio]
```

**Example Output Contract**:
```json
{
  "subject": "Arranhador Gato Modular Torre Vertical Carpete Sustentável",
  "style": "lifestyle",
  "scenes": 9,
  "pnl_triggers": ["confiança", "prazer", "transformação"],
  "brand_profile": {
    "mood": "natural conforto pet-friendly",
    "target_audience": "donos de gatos preocupados com bem-estar"
  },
  "compliance_mode": "marketplace",
  "scene_concepts": [
    {
      "scene_1": "Pack shot white background #FFFFFF, product centered, full view",
      "keywords": ["arranhador", "modular", "completo"]
    },
    {
      "scene_2": "Cat using scratcher actively, natural behavior, happiness",
      "keywords": ["gato arranhando", "satisfação", "bem-estar"]
    },
    {
      "scene_3": "Close-up carpete texture, sustainable material detail",
      "keywords": ["material", "qualidade", "sustentável"]
    },
    {
      "scene_4": "Modular assembly process, ease of setup",
      "keywords": ["montagem", "praticidade", "fácil"]
    },
    {
      "scene_5": "Multiple cats using tower simultaneously, social play",
      "keywords": ["múltiplos gatos", "interação", "diversão"]
    },
    {
      "scene_6": "Home environment integration, modern interior",
      "keywords": ["decoração", "ambiente", "integração"]
    },
    {
      "scene_7": "Before/after cat behavior transformation",
      "keywords": ["transformação", "comportamento", "antes-depois"]
    },
    {
      "scene_8": "Product durability detail, reinforced structure",
      "keywords": ["durabilidade", "resistência", "qualidade"]
    },
    {
      "scene_9": "Pack shot white background #FFFFFF, product with cat for scale",
      "keywords": ["produto completo", "dimensões", "escala"]
    }
  ],
  "midjourney_hints": [
    "Focus on modular assembly visualization (bullet #1 highlight)",
    "Emphasize natural sustainable carpete material (bullet #2)",
    "Show cats actively engaged and happy (emotional transformation)",
    "Use warm natural lighting for comfort/trust PNL triggers",
    "Include human hand for scale and ease-of-use demonstration"
  ]
}
```

---

## OUTPUT_CONTRACT

- `$handoff_block`: Formatted handoff for photo_agent
- `$photo_context`: Extracted visual context JSON (photo_agent input schema)
- `$scene_concepts`: Array of 9 scene descriptions mapped from copy

---

## TRIGGERS

### Manual
```bash
/flow do "bridge anuncio to photo for [product]"
```

### Automatic (after anuncio)
```bash
# In anuncio workflow completion:
NEXT_WORKFLOW: 101_ADW_ANUNCIO_BRIDGE
```

### Via Spawn
```bash
/spawn
1. explore: find anuncio output for [product]
2. review: validate anuncio quality
3. build: execute 101_ADW_ANUNCIO_BRIDGE
4. build: execute photo_agent with context
```

---

## EXAMPLE

### Input (anuncio output)
```markdown
# Anuncio: Arranhador Gato Modular Torre Vertical

## TITULO
Arranhador Gato Modular Torre Vertical Carpete Premium Sustentável Resistente

## BULLETS
1. Design modular único permite configuração personalizada conforme espaço disponível, torre ajustável vertical horizontal, máxima versatilidade instalação ambientes pequenos grandes, sem ferramentas montagem, praticidade total donos gatos (285 chars)

2. Material carpete sustentável alta resistência suporta arranhões intensos múltiplos gatos, durabilidade comprovada anos uso, textura perfeita satisfação felina, sem desgaste fibras, qualidade premium investimento longo prazo (279 chars)

3. Promove comportamento natural saudável gatos, reduz estresse ansiedade, estimula exercício físico escalada, arranhadura direcionada protege móveis sofás cortinas, bem-estar felino garantido ambiente harmonioso (260 chars)

## DESCRICAO
[3500+ chars with StoryBrand framework describing cat behavior problems, product as solution, transformation to happy well-adjusted cats]

Emocao_alvo: Orgulho (dono responsável), Praticidade (fácil setup), Bem-estar (gato feliz)

## KEYWORDS
Bloco 1: arranhador gato, torre gato, arranhador modular, brinquedo gato, arranhador vertical...
Bloco 2: arranhador resistente, torre carpete, arranhador grande, arranhador premium...

## METADATA
categoria: Pet > Gatos > Brinquedos e Acessórios
marketplace_target: Mercado Livre
preco_sugerido: R$ 189
emocao_alvo: orgulho, praticidade, bem-estar
```

### Output (photo context JSON)
```json
{
  "subject": "Arranhador Gato Modular Torre Vertical Carpete Sustentável Premium",
  "style": "lifestyle",
  "scenes": 9,
  "pnl_triggers": ["confiança", "prazer", "transformação"],
  "brand_profile": {
    "mood": "natural conforto pet-friendly warm",
    "target_audience": "donos de gatos preocupados com bem-estar"
  },
  "compliance_mode": "marketplace",
  "ai_model": "midjourney",
  "output_format": "grid_3x3",
  "scene_concepts": [
    "Scene 1 (Hero Pack Shot): Cat scratcher tower on pure white background #FFFFFF, centered composition, front view showing full modular structure, all carpeted surfaces visible, product only no props",
    "Scene 2 (Active Use): Orange tabby cat actively scratching vertical post, extended claws engaged with carpete texture, natural satisfied expression, mid-action motion, lifestyle home setting",
    "Scene 3 (Material Detail): Extreme close-up of sustainable carpete fiber texture, macro photography showing weave pattern, durability indicators, warm natural lighting highlighting material quality",
    "Scene 4 (Assembly/Modularity): Hands assembling modular components, no tools visible, intuitive connection system shown, step-by-step simplicity, clean modern background",
    "Scene 5 (Multiple Cats): Two cats using tower simultaneously, one scratching lower post, one perched on upper platform, social play interaction, spacious modern apartment interior",
    "Scene 6 (Home Integration): Cat tower in contemporary living room setting, blends with modern decor, neutral color palette, shows scale against furniture, non-intrusive design",
    "Scene 7 (Before/After Transformation): Split scene or diptych showing stressed cat vs happy relaxed cat using scratcher, emotional transformation visual storytelling",
    "Scene 8 (Durability/Quality): Close-up of reinforced base structure, showing stability, weight capacity indicators, quality construction details, professional commercial lighting",
    "Scene 9 (Pack Shot with Scale): Cat scratcher tower on pure white background #FFFFFF, cat sitting beside for scale reference, full product view, all angles visible"
  ],
  "midjourney_hints": [
    "Emphasize modular assembly visualization (bullet #1: 'design modular único')",
    "Focus on sustainable carpete material texture (bullet #2: 'material carpete sustentável')",
    "Show cats actively engaged, scratching, climbing (bullet #3: 'comportamento natural saudável')",
    "Use warm natural lighting for comfort/trust (emocao_alvo: bem-estar)",
    "Include lifestyle shots with modern home interior (target: responsible cat owners)",
    "Demonstrate size/scale with cat or human hand",
    "Show durability through close-ups of construction quality",
    "Final shot must be white background for Mercado Livre compliance"
  ]
}
```

### Generated Handoff
```handoff
contexto: Anuncio complete for Arranhador Gato Modular Torre Vertical
arquivos_gerados:
  - user_anuncios/arranhador_gato_modular_anuncio.md
proximo: Run /photo with visual context
dados:
  subject: "Arranhador Gato Modular Torre Vertical Carpete Sustentável Premium"
  style: "lifestyle"
  scenes: 9
  pnl_triggers: ["confiança", "prazer", "transformação"]
  mood: "natural conforto pet-friendly warm"
  compliance: "marketplace" (Mercado Livre - white bg scenes 1+9 required)
scene_concepts:
  - hero_pack_shot: White bg #FFFFFF, centered, full view
  - active_use: Cat scratching, satisfied, natural behavior
  - material_detail: Macro carpete texture, sustainability
  - assembly: Modular setup demonstration, tool-free
  - multiple_cats: Social play, tower capacity
  - home_integration: Modern interior, decor blend
  - transformation: Before/after cat behavior
  - durability: Reinforced structure, quality construction
  - scale_reference: White bg #FFFFFF, cat for scale
qualidade: 8.7/10
visual_alignment:
  - Copy emphasizes "modular" → Photo shows assembly/configuration
  - Copy emphasizes "sustentável" → Photo macro of carpete eco-texture
  - Copy emphasizes "comportamento natural" → Photo cats actively using
  - Emotion "orgulho" → Photo high-quality aesthetic
  - Emotion "praticidade" → Photo easy assembly demonstration
  - Emotion "bem-estar" → Photo happy cats in action
```

---

## INTEGRATION

### With /flow
```bash
/flow plan "criar fotos produto com copy para [product]"
# Automatically includes anuncio → photo bridge
```

### With /spawn
```bash
/spawn
1. build: anuncio for [product]
2. build: bridge anuncio→photo (this workflow)
3. build: photo with visual context
```

### With /codexa-orchestrate
```bash
/codexa-orchestrate "anuncio to photo pipeline for [product]"
# Multi-phase workflow: anuncio → bridge → photo → validation
```

---

## VALIDATION

Quality gate (≥7.0/10):
```markdown
- [ ] Subject description extracted and clear (2.0 pts)
- [ ] 9 scene concepts defined (2.0 pts)
- [ ] PNL triggers mapped from copy (2.0 pts)
- [ ] Mood/style appropriate for category (2.0 pts)
- [ ] Marketplace compliance requirements included (2.0 pts)
- [ ] Handoff format correct and complete
- [ ] Visual concepts align with copy key points
- [ ] Midjourney hints actionable and specific
```

**Score Calculation**:
```python
score = (
    subject_clarity * 2.0 +     # Clear product identification
    scene_diversity * 2.0 +     # Distinct scene types defined
    emotional_alignment * 2.0 + # PNL triggers match anuncio
    visual_completeness * 2.0 + # All required elements present
    compliance_ready * 2.0      # Marketplace requirements met
) / 10.0
```

---

## NOTES

**Why This Bridge Matters**:
- **Consistency**: Product photos visually reinforce ad copy messaging
- **Emotional Alignment**: Visual PNL triggers match written persuasion triggers
- **Compliance**: Marketplace requirements flow from anuncio metadata
- **Efficiency**: Copy insights directly inform photo direction, no redundant research

**Common Pitfalls**:
- Ignoring marketplace-specific visual requirements (white bg for ML)
- Missing emotional tone from description (results in misaligned photos)
- Over-literal translation (copy says "durable" → photo must show WHY durable, not just product)
- Forgetting scale reference (especially for pet products)

**Best Practices**:
- Always map at least 3 distinct scene types: hero, lifestyle, detail
- Translate abstract benefits to concrete visual demonstrations
- Use bullets as direct scene descriptions (1 bullet ≈ 1 scene)
- Preserve marketplace target from anuncio metadata
- Include Midjourney hints for specific visual elements from copy

---

**Version**: 1.0.0
**Created**: 2025-12-03
**Type**: Bridge Workflow (anuncio → photo)
**Maintainer**: CODEXA Meta-Constructor
**Related Workflows**:
- anuncio_agent: 100_ADW_RUN_ANUNCIO.md
- photo_agent: 100_ADW_RUN_PHOTO.md
- pesquisa_agent: 101_ADW_PESQUISA_BRIDGE.md (pattern reference)
