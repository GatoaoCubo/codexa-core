# Photo Agent Output Schemas Guide

**Version**: 1.0.0
**Date**: 2025-11-15
**Author**: CODEXA Meta-Construction System

---

## 📋 Overview

Photo agent provides **2 specialized output schemas** for different workflows:

1. **`photo_marketplace_output.json`** - Marketplace product photography (anuncio_agent integration)
2. **`photo_brand_output.json`** - Brand social media content (marca_agent integration)

Each schema is optimized for its specific use case with distinct compliance rules, validation criteria, and integration patterns.

---

## 🎯 Schema 1: Marketplace Output

### Purpose
Generate 9 product photography prompts for Brazilian marketplace listings (Mercado Livre, Shopee, Amazon BR, Magalu) with **strict compliance** for white background requirements.

### Key Features

**RIGID COMPLIANCE RULES:**
- ✅ **Scene 1 (Hero)**: MUST have #FFFFFF white background (marketplace thumbnail)
- ✅ **Scene 9 (Cover)**: MUST have #FFFFFF white background (ad cover image)
- ✅ Scenes 2-8: Flexible (lifestyle, macro, context, etc.)
- ✅ 13-point compliance validation checklist
- ✅ Reference image placeholder: `{INSERIR_IMAGEM_PRODUTO_AQUI}`

**Integration:**
- Works with `anuncio_agent` for complete marketplace ad generation
- Output images → Input for anuncio_agent ad copy (titles, descriptions, keywords)

**Validation Target:**
- ≥0.90 validation score (stricter than generic photo_agent)
- 100% compliance on white background scenes 1+9

### Schema Structure

```json
{
  "metadata": {
    "agent": "photo_agent_marketplace",
    "workflow_type": "marketplace_product",
    "target_marketplace": "mercadolivre | shopee | magalu | amazon_br | all",
    "anuncio_agent_integration": true
  },
  "prompts_grid_3x3": [
    {
      "scene_number": 1-9,
      "prompt_with_reference": "...{INSERIR_IMAGEM_PRODUTO_AQUI}...",
      "compliance_white_bg": true/false,  // MUST be true for scenes 1+9
      "marketplace_purpose": "main_thumbnail | lifestyle_context | detail_zoom | ..."
    }
  ],
  "reference_instructions": {
    "workflow_overview": "How to use {INSERIR_IMAGEM_PRODUTO_AQUI} placeholder",
    "step_by_step": ["1. Have product image ready", "2. Copy prompt", "3. Paste image in placeholder", "4. Generate"],
    "fidelity_guarantee": "Explains why reference image ensures 100% product fidelity"
  },
  "marketplace_compliance": {
    "compliant_marketplaces": ["mercadolivre", "shopee", ...],
    "rules_applied": ["ML: Scene 1 white bg", "Shopee: 9 images max", ...]
  },
  "quality_report": {
    "marketplace_compliance_status": "FULL_COMPLIANCE | PARTIAL_COMPLIANCE | NON_COMPLIANT",
    "white_bg_scenes": [1, 9],  // MUST include both
    "compliance_details": {
      "scene_1_white_bg": true,  // CRITICAL
      "scene_9_white_bg": true,  // CRITICAL
      "all_reference_placeholder": true,
      // ... 10 more checks
    }
  }
}
```

### Example Output

**Scene 1 (Hero - White Background):**
```
Professional product photography fiel ao {INSERIR_IMAGEM_PRODUTO_AQUI}, garrafa de água 750ml aço inox, pure white background #FFFFFF, centered composition rule of thirds, camera 50mm f/8 1/160s ISO 100, high-key lighting soft uniform shadows, full sharp focus texture visible, PNL: clareza imediata na escolha, no watermarks, no text, no third-party logos, 8K quality, marketplace compliant
```

**Scene 5 (Lifestyle - Flexible Background):**
```
Professional lifestyle photography fiel ao {INSERIR_IMAGEM_PRODUTO_AQUI}, garrafa sendo usada em ambiente de treino real authentic moment, background ambiente fitness natural bokeh clean, lighting natural window light warm, camera 85mm f/4 1/160s ISO 400, candid authentic composition, shallow depth of field, PNL: confiança no produto durante uso real, no watermarks, 8K quality
```

### Use Cases
- E-commerce product listings (ML, Shopee, Amazon BR, Magalu)
- Marketplace ad campaigns requiring compliance
- Integration with anuncio_agent for complete ad packages
- Products requiring strict visual fidelity (electronics, fashion, home goods)

---

## 🎨 Schema 2: Brand Social Media Output

### Purpose
Generate 9 brand-aligned photography prompts for social media campaigns (Instagram, Facebook, TikTok, Pinterest) with **deep brand integration** from marca_agent's brand_strategy.md.

### Key Features

**NO WHITE BACKGROUND COMPLIANCE:**
- ❌ No mandatory white backgrounds (creative freedom)
- ✅ Backgrounds align with brand mood and colors
- ✅ Atmospheric, contextual, branded environments encouraged

**DEEP BRAND INTEGRATION:**
- ✅ Reads `brand_strategy.md` from marca_agent
- ✅ Applies brand colors (primary, secondary, accent) to scenes
- ✅ Aligns PNL triggers with brand archetype:
  - Hero → "coragem", "transformação", "confiança"
  - Sage → "clareza", "controle", "conhecimento"
  - Creator → "liberdade", "exclusividade", "inovação"
  - Caregiver → "conforto", "segurança", "pertencimento"
- ✅ Visual mood matches brand tone (energetic vs serene vs luxurious)

**VARIABLE ASPECT RATIOS:**
- 1:1 (Instagram feed square)
- 4:5 (Instagram feed vertical)
- 9:16 (Stories, Reels, TikTok)
- 16:9 (Facebook landscape)
- 2:3 (Pinterest vertical)

**Integration:**
- Works with `marca_agent` brand_strategy.md
- Ensures visual consistency with brand identity
- Optimized for social media engagement, not marketplace conversion

**Validation Target:**
- ≥0.85 validation score (brand consistency)
- ≥0.90 visual consistency with brand identity

### Schema Structure

```json
{
  "metadata": {
    "agent": "photo_agent_brand",
    "workflow_type": "brand_social_media",
    "brand_name": "HeroWater",
    "brand_archetype": "Hero",
    "target_platforms": ["instagram_feed", "instagram_stories", "tiktok"],
    "marca_agent_integration": true
  },
  "prompts_social_grid": [
    {
      "scene_number": 1-9,
      "prompt_brand_aligned": "...brand colors...archetype mood...PNL aligned...",
      "aspect_ratio": "1:1 | 4:5 | 9:16 | 16:9 | 2:3",
      "brand_elements": {
        "brand_colors_applied": ["#FF5722", "#212121", "#FFFFFF"],
        "brand_mood": "Enérgico, determinado, inspirador",
        "brand_archetype_personality": "Hero: coragem, determinação, superação"
      },
      "pnl_trigger_archetype": "Hero: coragem que prova valor através da ação",
      "platform_optimization": {
        "primary_platform": "instagram_feed",
        "caption_suggestion": "💪 Prove seu valor...",
        "hashtag_strategy": ["#HeroWater", "#SustentabilidadeAtiva"]
      }
    }
  ],
  "brand_integration": {
    "brand_strategy_loaded": true,
    "brand_strategy_path": "USER_DOCS/Marca/hero_water_brand_strategy.md",
    "brand_identity": {
      "brand_name": "HeroWater",
      "primary_archetype": "Hero",
      "color_palette": {"primary": "#FF5722", "secondary": ["#212121"], "accent": "#4CAF50"},
      "mood_tone": "Enérgico, determinado, inspirador"
    },
    "visual_consistency_score": 0.94,
    "brand_alignment_checks": {
      "colors_from_palette": true,
      "mood_consistency": true,
      "archetype_personality": true,
      "pnl_triggers_aligned": true
    }
  },
  "social_media_specs": {
    "platform_breakdown": {
      "instagram_feed": {"scenes": [1, 2, 4, 7], "aspect_ratios": ["4:5", "1:1"]},
      "instagram_stories": {"scenes": [3, 5, 8], "aspect_ratio": "9:16"}
    },
    "recommended_posting_strategy": {
      "carousel_posts": [{"scenes": [1, 3, 5, 7, 9], "narrative": "Hero's Journey arc"}],
      "hero_singles": [1, 4, 9]
    }
  }
}
```

### Example Output

**Scene 1 (Brand Hero - Instagram Feed 4:5):**
```
Professional lifestyle photography in Hero archetype style, {INSERIR_IMAGEM_PRODUTO_AQUI} garrafa HeroWater sendo usada por atleta em ambiente urbano dinâmico ao amanhecer, background ambiente urbano com cores da marca #FF5722 laranja vibrante e #212121 cinza carvão acentos arquitetônicos, mood enérgico determinado inspirador, lighting golden hour natural warm 5500K directional com sombras longas dramáticas, camera 85mm f/4 1/160s ISO 400, composition diagonal bold asymmetric movimento implícito, shallow depth of field bokeh urbano clean, PNL Hero archetype: coragem que prova seu valor através da ação decisiva, aspect ratio 4:5 Instagram feed, no watermarks, 8K quality --ar 4:5
```

**Scene 3 (Stories/Reels - Vertical 9:16):**
```
Professional action photography in Hero style, {INSERIR_IMAGEM_PRODUTO_AQUI} garrafa em movimento durante treino intenso atleta em ação dinâmica, background ambiente de treino urbano com #FF5722 elementos vibrantes movimento blur, mood urgente energético motivacional, lighting dramatic lateral strong contrast, camera 85mm f/2.8 1/500s ISO 800, composition vertical 9:16 dynamic asymmetric, ultra shallow depth of field subject isolation, PNL Hero: transformação através da disciplina diária, aspect ratio 9:16 Instagram stories TikTok, no watermarks, 8K quality --ar 9:16
```

### Use Cases
- Instagram feed posts (carousel, single)
- Instagram/Facebook Stories
- TikTok/Reels content
- Pinterest pins
- Brand awareness campaigns
- Social proof content
- Brand narrative storytelling
- Influencer collaboration assets

---

## 🔀 Decision Matrix: Which Schema to Use?

| Criterion | Use MARKETPLACE Schema | Use BRAND Schema |
|-----------|------------------------|------------------|
| **Output Destination** | Marketplace listings (ML, Shopee, Amazon) | Social media (Instagram, TikTok, Pinterest) |
| **White BG Required?** | YES (scenes 1+9) | NO (creative backgrounds OK) |
| **Have brand_strategy.md?** | Optional | Recommended (deep integration) |
| **Aspect Ratios** | Fixed 1:1 or sequential | Variable (1:1, 4:5, 9:16, etc.) |
| **Compliance Focus** | Marketplace policies | Brand consistency |
| **Integration Agent** | anuncio_agent (ad copy) | marca_agent (brand identity) |
| **Primary Goal** | Conversion (sales) | Engagement (awareness, loyalty) |
| **Validation Score Target** | ≥0.90 (strict) | ≥0.85 (flexible) |

---

## 🛠️ Implementation Notes

### For Developers

**Schema Validation:**
- Both schemas use JSON Schema Draft-07
- Examples embedded in each schema for testing
- Required fields enforced via `"required": [...]`
- Enums restrict values to valid options

**Trinity Output Pattern:**
Both schemas output 3 files:
1. `.md` - Human-readable markdown with copy-paste prompts
2. `.llm.json` - LLM-consumable JSON for automation
3. `.meta.json` - Metadata for tracking and quality scoring

**Error Handling:**
- Marketplace schema: Fails if scenes 1 or 9 don't have white background
- Brand schema: Warns if brand_strategy.md not loaded or incomplete

### For AI Assistants

**When to use each schema:**
- User mentions "marketplace", "ML", "Shopee", "Amazon", "product listing" → Marketplace schema
- User mentions "Instagram", "TikTok", "social media", "brand campaign", "stories" → Brand schema
- User has `brand_strategy.md` file → Brand schema (reads file automatically)
- User needs white background compliance → Marketplace schema

**Prompt generation flow:**
1. Load appropriate schema
2. (Brand schema only) Read `brand_strategy.md` from marca_agent
3. Generate 9 prompts following schema rules
4. Validate against compliance checklist (13-point for marketplace, 11-point for brand)
5. Output Trinity files (.md, .llm.json, .meta.json)

---

## 📊 Validation Checklists

### Marketplace Schema (13 Checks)

1. ✅ Scene 1 has #FFFFFF white background (CRITICAL)
2. ✅ Scene 9 has #FFFFFF white background (CRITICAL)
3. ✅ All prompts 100-400 characters
4. ✅ All prompts specify camera settings
5. ✅ All prompts describe lighting
6. ✅ All prompts mention background
7. ✅ All prompts define composition
8. ✅ All prompts state "8K quality"
9. ✅ All prompts include "no watermarks"
10. ✅ All prompts include "no text"
11. ✅ All prompts include "no third-party logos"
12. ✅ All prompts include PNL trigger
13. ✅ All prompts include `{INSERIR_IMAGEM_PRODUTO_AQUI}` placeholder

**Pass Criteria:** ALL 13 checks = TRUE

### Brand Schema (11 Checks)

1. ✅ All prompts 120-500 characters
2. ✅ All prompts specify camera settings
3. ✅ All prompts describe lighting
4. ✅ All prompts mention background
5. ✅ All prompts define composition
6. ✅ All aspect ratios valid (1:1, 4:5, 9:16, etc.)
7. ✅ All brand colors applied from palette
8. ✅ All PNL triggers aligned with brand archetype
9. ✅ All prompts state "8K quality"
10. ✅ All prompts include "no watermarks"
11. ✅ Platform optimization complete (aspect ratio + platform tags)

**Pass Criteria:** ≥9/11 checks = PASS (allows 2 minor deviations)

---

## 🔗 Integration Workflows

### Marketplace → Anuncio Agent

```
1. User provides product image + subject
   ↓
2. Photo agent (MARKETPLACE schema) generates 9 prompts
   Output: 9 copy-paste prompts with {INSERIR_IMAGEM_PRODUTO_AQUI}
   Scenes 1+9: #FFFFFF white background (compliance)
   ↓
3. User generates 9 images in LLM (Gemini, DALL-E, Midjourney)
   Pastes product image in each prompt for fidelity
   ↓
4. User selects best images (recommended: scenes 1, 2, 3, 5, 9)
   ↓
5. Images fed to ANUNCIO AGENT
   Anuncio agent generates:
   - Titles (3 variations, ZERO connectors)
   - Keywords (115-120 per block)
   - Long description (≥3,300 chars)
   - SEO metadata
   ↓
6. Complete marketplace listing ready for upload
```

### Brand Strategy → Photo Agent → Social Media

```
1. User creates brand strategy with MARCA AGENT
   Output: brand_strategy.md with archetype, colors, mood, values
   ↓
2. Photo agent (BRAND schema) reads brand_strategy.md
   Extracts: brand name, archetype, color palette, mood, PNL triggers
   ↓
3. Photo agent generates 9 brand-aligned prompts
   - Colors from brand palette
   - PNL triggers aligned to archetype (Hero → courage, Caregiver → comfort)
   - Mood reflects brand tone (energetic vs serene)
   - Aspect ratios optimized for target platforms (4:5 feed, 9:16 stories)
   ↓
4. User generates images in LLM
   ↓
5. Images ready for social media posting
   - Carousel posts (scenes 1-3-5-7-9)
   - Single hero posts (scenes 1, 4, 9)
   - Stories/Reels (scenes 3, 5, 8)
```

---

## 📚 References

**Related Schemas:**
- `photo_input.json` - Input validation (applies to both workflows)
- `photo_output.json` - Generic output (deprecated in favor of specialized schemas)

**Related Agents:**
- `anuncio_agent` - Marketplace ad copy generation (integrates with marketplace schema)
- `marca_agent` - Brand strategy creation (integrates with brand schema)

**Configuration Files:**
- `config/photography_styles.json` - 5 style presets (minimalist, dramatic, lifestyle, editorial, commercial)
- `config/camera_profiles.json` - Camera technical specifications
- `config/pnl_triggers.json` - 12 emotional triggers mapped to brand archetypes

---

## ✅ Quality Targets

**Marketplace Schema:**
- Validation score: ≥0.90
- White background compliance: 100% (scenes 1+9)
- Marketplace compliance: FULL_COMPLIANCE
- Reference image fidelity: 100%

**Brand Schema:**
- Validation score: ≥0.85
- Brand consistency score: ≥0.90
- Visual alignment: ≥8/8 brand alignment checks
- Platform optimization: 100%

---

**Version History:**
- **1.0.0** (2025-11-15): Initial release with dual schema support

**Maintained by:** CODEXA Meta-Construction Framework
**License:** Internal Use
