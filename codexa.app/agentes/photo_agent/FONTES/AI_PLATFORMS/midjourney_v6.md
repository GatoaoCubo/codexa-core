# Midjourney V6 Prompting Guide

**Version**: 1.0.0 | **Updated**: 2025-12-05 | **Source**: Midjourney Documentation

---

## OVERVIEW

Midjourney V6 e a versao mais recente do modelo, com melhorias significativas em:
- Compreensao de prompts naturais
- Renderizacao de texto em imagens
- Fidelidade fotografica
- Consistencia de personagens

---

## PROMPT STRUCTURE

### Basic Formula

```
[Subject] + [Environment] + [Lighting] + [Camera] + [Style] + [Parameters]
```

### Example

```
Professional product photograph of a ceramic coffee mug with wooden handle,
on white seamless backdrop, soft box lighting from front, 50mm lens f/8,
commercial e-commerce style --ar 1:1 --v 6 --style raw
```

---

## PARAMETERS

### Essential Parameters

| Parameter | Values | Purpose |
|-----------|--------|---------|
| `--v 6` | 6 | Model version (latest) |
| `--ar` | 1:1, 16:9, 9:16, 4:3 | Aspect ratio |
| `--style raw` | raw | Less opinionated, more literal |
| `--stylize` | 0-1000 | Artistic interpretation (default 100) |
| `--chaos` | 0-100 | Variation level |
| `--quality` | .25, .5, 1, 2 | Render quality |

### Aspect Ratios for E-commerce

```
--ar 1:1    → Marketplace main (ML, Shopee, Amazon)
--ar 4:5    → Instagram feed, portrait products
--ar 16:9   → Website banners, hero images
--ar 9:16   → TikTok, Stories, vertical video stills
--ar 3:4    → Pinterest optimal
```

### Style Parameter Guide

```
--stylize 0-50    → Literal interpretation, product-focused
--stylize 50-100  → Balanced (default)
--stylize 100-200 → Slightly artistic
--stylize 200+    → Highly stylized, artistic interpretation
```

**For E-commerce**: Use `--stylize 0-50` or `--style raw`

---

## PROMPTING TECHNIQUES

### 1. Multi-Prompt Weighting

Use `::` to separate concepts with weights:

```
product photography::2 coffee mug::1.5 white background::1 --ar 1:1 --v 6
```

- Higher weight = more emphasis
- Default weight is 1
- Negative weights remove concepts: `text::-0.5`

### 2. Negative Prompting

Use `--no` parameter:

```
ceramic mug on white background --no text, watermark, logo, shadow --ar 1:1 --v 6
```

Common negatives for e-commerce:
```
--no text, watermark, logo, shadow, reflection, blur, noise, grain
```

### 3. Image Reference

Use uploaded image + prompt:

```
[uploaded product image] same product, white seamless background,
studio lighting, professional product photography --ar 1:1 --v 6 --iw 2
```

- `--iw 0.5-2` controls image weight
- Higher = closer to reference image

### 4. Style Reference

```
--sref [URL]     → Apply style from reference image
--sw 0-1000      → Style reference weight (default 100)
```

---

## PHOTOGRAPHY-SPECIFIC PROMPTS

### Hero Shot (White Background)

```
Professional product photograph of [PRODUCT], centered composition,
pure white seamless backdrop #FFFFFF, soft diffused front lighting,
sharp focus throughout, 50mm lens f/8 equivalent, commercial e-commerce
style, no shadows, isolated product, high-resolution --ar 1:1 --v 6 --style raw
```

### Lifestyle Shot

```
[PRODUCT] in natural home setting, morning light through window,
shallow depth of field, warm color palette, lifestyle photography,
authentic moment, 85mm lens f/2.8 bokeh, editorial quality --ar 4:5 --v 6
```

### Detail/Macro Shot

```
Extreme close-up of [PRODUCT DETAIL], macro photography,
100mm lens f/2.8, shallow depth of field highlighting texture,
ring light illumination, studio quality, hyper-detailed,
material texture visible --ar 1:1 --v 6 --style raw
```

### 45-Degree Angle

```
[PRODUCT] photographed at 45-degree angle showing depth and dimension,
soft gradient white background, three-point lighting setup,
professional product photography, sharp details, commercial quality
--ar 1:1 --v 6
```

### Flat Lay (Top-Down)

```
Flat lay overhead view of [PRODUCT] with complementary props,
clean white background, even diffused lighting, symmetrical arrangement,
Instagram aesthetic, curated composition, 35mm lens --ar 1:1 --v 6
```

---

## LIGHTING KEYWORDS

### Studio Lighting

```
soft box lighting       → Even, diffused, no harsh shadows
three-point lighting    → Professional, dimensional
ring light              → Even face/front, macro
backlit / rim light     → Dramatic edge definition
low key lighting        → Dark, moody, dramatic
high key lighting       → Bright, minimal shadows
```

### Natural Lighting

```
golden hour             → Warm, orange tones
blue hour               → Cool, cinematic
window light            → Soft, directional natural
overcast natural        → Even, soft, no harsh shadows
dappled light           → Through leaves, patterns
```

### Color Temperature

```
warm lighting (3000K)   → Cozy, inviting, golden
neutral lighting (5500K)→ Natural, balanced
cool lighting (6500K)   → Clean, professional, blue tint
```

---

## CAMERA & LENS KEYWORDS

### Lens Simulation

```
50mm lens               → Standard, natural perspective
35mm lens               → Slight wide, environmental
85mm lens               → Portrait, compression, bokeh
100mm macro             → Detail, extreme close-up
24mm wide               → Environmental, architecture
```

### Aperture Effects

```
f/1.4 - f/2.8          → Shallow DOF, strong bokeh
f/4 - f/5.6            → Moderate DOF, lifestyle
f/8 - f/11             → Deep DOF, full focus (products)
```

### Quality Keywords

```
8K resolution           → Ultra-high detail
photorealistic          → Natural, believable
hyperrealistic          → Extreme realism
sharp focus             → Crisp details
tack sharp              → Maximum sharpness
```

---

## V6-SPECIFIC IMPROVEMENTS

### Text in Images

V6 can render text more accurately:

```
product with label showing "BRAND NAME" text, clearly readable,
professional product photography --ar 1:1 --v 6
```

**Tips**:
- Keep text short (1-3 words)
- Use quotes around text
- Specify "clearly readable" or "legible text"
- May need regeneration for accuracy

### Coherent Hands/Bodies

V6 improved but still verify:
- Use reference images when possible
- Specify natural pose
- Add `--style raw` for less stylization

### Prompt Following

V6 follows prompts more literally:
- Be specific about what you want
- Order matters: put important elements first
- Use fewer words for key concepts
- More words = more interpretation room

---

## COMMON ISSUES & FIXES

### Issue: Product Not Centered

```
Before: product on white background
After:  product CENTERED in frame, white background, isolated subject
```

### Issue: Unwanted Text/Logos

```
Add: --no text, watermark, logo, branding, words, letters
```

### Issue: Shadows on White Background

```
Add: pure white background #FFFFFF, no shadows, isolated product,
     seamless white backdrop, even lighting
```

### Issue: Too Artistic/Stylized

```
Add: --style raw --stylize 0
     photorealistic, commercial photography, literal interpretation
```

### Issue: Wrong Aspect Ratio

```
Specify exactly: --ar 1:1 for square, --ar 4:5 for portrait
```

---

## E-COMMERCE PROMPT TEMPLATES

### Template 1: Marketplace Main Image

```
Professional product photograph of {{PRODUCT}}, centered composition,
pure white seamless backdrop #FFFFFF, soft diffused studio lighting,
sharp focus throughout entire product, 50mm lens f/8, commercial
e-commerce photography, no shadows, isolated product, Mercado Livre
marketplace style --ar 1:1 --v 6 --style raw --stylize 0
--no text, watermark, logo, shadow
```

### Template 2: Lifestyle Context

```
{{PRODUCT}} in natural {{ENVIRONMENT}} setting, {{TIME_OF_DAY}} light,
shallow depth of field with product in focus, warm inviting atmosphere,
85mm lens f/4 bokeh background, lifestyle photography, authentic moment,
editorial quality --ar 4:5 --v 6
```

### Template 3: Detail Macro

```
Extreme macro close-up of {{PRODUCT_FEATURE}}, revealing texture and
craftsmanship, 100mm macro lens f/2.8, shallow DOF focusing on detail,
ring light illumination, premium quality visualization, material texture
clearly visible --ar 1:1 --v 6 --style raw
```

### Template 4: Scale Reference

```
{{PRODUCT}} next to {{REFERENCE_OBJECT}} for scale, centered composition,
clean white background, even lighting, showing actual size comparison,
50mm lens f/8, informative product photography --ar 1:1 --v 6 --style raw
```

---

## BATCH GENERATION

### Using Permutations

```
{ceramic, stainless steel, glass} mug on white background, product photography
--ar 1:1 --v 6
```

Generates 3 variations automatically.

### Using Seeds

```
coffee mug on white background --seed 12345 --ar 1:1 --v 6
```

- Same seed = reproducible results
- Change seed for controlled variations
- Useful for product color variants

---

## INTEGRATION WITH PHOTO_AGENT

### Output Format

photo_agent generates prompts with:

```
{user_image} {seed:[RANDOM]} [PROMPT_CONTENT] --ar 1:1 --v 6 --style raw
```

- `{user_image}` → Placeholder for uploaded product image
- `{seed:[RANDOM]}` → Ensures variation while maintaining style
- `[OPEN_VARIABLES]` → Options like [warm | cool | neutral] lighting

### Scene Mapping

| Scene | MJ Parameters |
|-------|---------------|
| 1 (Hero White) | `--ar 1:1 --style raw --stylize 0` |
| 2 (Lifestyle) | `--ar 4:5 --stylize 50` |
| 3 (Detail) | `--ar 1:1 --style raw` |
| 4 (Use Case) | `--ar 4:5` |
| 5 (Benefit) | `--ar 4:5 --stylize 100` |
| 6 (Scale) | `--ar 1:1 --style raw` |
| 7 (Context) | `--ar 16:9` |
| 8 (Material) | `--ar 1:1 --style raw` |
| 9 (Commercial) | `--ar 1:1 --style raw --stylize 0` |

---

## REFERENCES

- Midjourney Documentation: https://docs.midjourney.com
- Midjourney Discord: https://discord.gg/midjourney
- Parameter Reference: https://docs.midjourney.com/docs/parameter-list

---

**Version**: 1.0.0 | **Status**: Production Ready
