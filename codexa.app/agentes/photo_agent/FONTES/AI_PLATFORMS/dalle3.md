# DALL-E 3 Prompting Guide

**Version**: 1.0.0 | **Updated**: 2025-12-05 | **Source**: OpenAI Documentation

---

## OVERVIEW

DALL-E 3 e o modelo de geracao de imagem da OpenAI, integrado ao ChatGPT e disponivel via API. Principais caracteristicas:

- Compreensao avancada de linguagem natural
- Alta fidelidade ao prompt
- Geracao precisa de texto em imagens
- Integracao nativa com ChatGPT

---

## API PARAMETERS

### Basic Request

```python
from openai import OpenAI

client = OpenAI()

response = client.images.generate(
    model="dall-e-3",
    prompt="A white ceramic coffee mug with wooden handle on pure white background, product photography",
    size="1024x1024",
    quality="hd",
    n=1
)

image_url = response.data[0].url
```

### Available Parameters

| Parameter | Values | Default |
|-----------|--------|---------|
| `model` | "dall-e-3" | Required |
| `prompt` | String (max 4000 chars) | Required |
| `size` | "1024x1024", "1792x1024", "1024x1792" | "1024x1024" |
| `quality` | "standard", "hd" | "standard" |
| `n` | 1 (only) | 1 |
| `style` | "vivid", "natural" | "vivid" |
| `response_format` | "url", "b64_json" | "url" |

### Size Options

```
1024x1024   → Square (marketplace main images)
1792x1024   → Landscape (banners, wide shots)
1024x1792   → Portrait (mobile, TikTok, Stories)
```

### Quality Settings

```
standard    → Faster, lower cost, good for iterations
hd          → Higher detail, slower, production quality
```

### Style Settings

```
vivid       → Hyper-real, dramatic (default)
natural     → More subtle, photorealistic
```

**For E-commerce**: Use `style="natural"` for product photography

---

## PROMPT STRUCTURE

### Recommended Formula

```
[Medium] of [Subject] with [Details], [Environment], [Lighting], [Camera], [Style]
```

### Example Prompts

**Hero Product Shot**:
```
Professional product photograph of a ceramic coffee mug with natural wooden
handle and subtle gold rim accent, centered on pure white seamless backdrop,
soft diffused studio lighting with no harsh shadows, shot with 50mm lens at
f/8 for deep focus, commercial e-commerce photography style, 8K quality
```

**Lifestyle Shot**:
```
Lifestyle photograph of ceramic coffee mug on rustic wooden table in a bright
modern kitchen, morning sunlight streaming through window, shallow depth of
field with background blur, warm inviting atmosphere, editorial photography
style, natural and authentic moment
```

---

## PROMPTING BEST PRACTICES

### 1. Be Extremely Specific

DALL-E 3 follows prompts literally. Include:

```
- Exact subject description (material, color, size, details)
- Precise positioning (centered, left-aligned, top-down)
- Specific lighting (soft box, window light, backlit)
- Camera settings (lens, aperture, focus)
- Style reference (commercial, editorial, documentary)
```

### 2. Use Descriptive Language

```
Before: white mug on table
After:  Matte white ceramic coffee mug with ergonomic curved handle,
        placed on weathered oak wooden table, morning window light
        creating soft shadows, shallow depth of field
```

### 3. Specify What to Avoid

Include in prompt:
```
..., without any text, logos, or watermarks, no visible shadows on
white background, avoiding cluttered composition
```

### 4. Reference Real Photography Styles

```
- "in the style of commercial product photography"
- "editorial magazine quality"
- "professional e-commerce listing photo"
- "lifestyle Instagram aesthetic"
```

---

## PHOTOGRAPHY-SPECIFIC PROMPTS

### White Background Product (Marketplace)

```
Professional commercial product photograph of [PRODUCT DESCRIPTION],
perfectly centered in frame, pure white seamless studio backdrop with
no shadows, soft diffused lighting from multiple angles for even
illumination, shot with 50mm lens at f/8 for complete sharpness,
high-resolution 8K quality, suitable for e-commerce marketplace listing,
clean and professional presentation
```

### Lifestyle Context

```
Lifestyle photograph of [PRODUCT] being used by [PERSON DESCRIPTION]
in [ENVIRONMENT], natural [TIME OF DAY] lighting, shallow depth of
field keeping product in sharp focus, warm color palette, authentic
candid moment, 85mm portrait lens bokeh effect, editorial magazine quality
```

### Detail/Macro

```
Extreme close-up macro photograph of [SPECIFIC FEATURE/DETAIL],
revealing intricate texture and craftsmanship, 100mm macro lens with
f/2.8 aperture creating smooth bokeh, ring light for even illumination,
product material clearly visible, premium quality visualization
```

### Flat Lay Overhead

```
Overhead flat lay photograph of [PRODUCT] with [COMPLEMENTARY PROPS],
arranged on [SURFACE], shot from directly above, even diffused lighting
eliminating shadows, balanced symmetrical composition, Instagram-ready
aesthetic, clean modern styling
```

---

## TEXT IN IMAGES

DALL-E 3 handles text better than most AI models:

### Tips for Text Generation

```
1. Keep text short (1-4 words optimal)
2. Specify exact text in quotes
3. Describe text appearance (font style, size, color)
4. Place text explicitly ("text at bottom", "label reads")
```

### Example

```
Product label bottle with text reading "ORGANIC" in elegant serif font,
white text on dark green label, clearly readable typography
```

### Limitations

- Long text may have errors
- Complex fonts inconsistent
- Multiple text elements challenging
- Always verify generated text

---

## AVOIDING COMMON ISSUES

### Unwanted Elements

```
Add to prompt:
"without any text, logos, watermarks, or branding visible"
"clean background without distracting elements"
"isolated product with no additional objects"
```

### Unrealistic Proportions

```
Add to prompt:
"photorealistic proportions"
"anatomically correct" (for humans)
"accurate scale and dimensions"
```

### Over-Stylization

```
Use style="natural" in API
Add "realistic photography, not illustrated"
Add "photorealistic, not artistic interpretation"
```

### Wrong Background Color

```
Be explicit:
"pure white background #FFFFFF"
"solid [COLOR] backdrop"
"seamless studio background"
```

---

## CHATGPT INTEGRATION

### Using DALL-E 3 via ChatGPT

1. Describe what you want in natural language
2. ChatGPT refines your prompt automatically
3. Review generated image
4. Request modifications naturally

### Example Conversation

```
User: Create a product photo of a coffee mug for my e-commerce store

ChatGPT: I'll create a professional product photograph for you...
[Generates with optimized prompt]

User: Can you make the background pure white and center the mug more?

ChatGPT: [Regenerates with adjustments]
```

### Prompt Rewriting

DALL-E 3 via ChatGPT rewrites prompts for safety and quality.
To see the actual prompt used:
- Ask "What prompt did you use for that image?"
- Review in conversation history

---

## API COST OPTIMIZATION

### Pricing (as of 2025)

| Quality | Size | Cost per Image |
|---------|------|----------------|
| Standard | 1024x1024 | $0.040 |
| Standard | 1792x1024 | $0.080 |
| HD | 1024x1024 | $0.080 |
| HD | 1792x1024 | $0.120 |

### Optimization Tips

```
1. Use standard quality for iterations
2. Switch to HD for final production
3. Batch similar prompts
4. Cache successful prompts
5. Use 1024x1024 unless larger needed
```

---

## E-COMMERCE PROMPT TEMPLATES

### Template 1: Marketplace Main Image

```
Professional commercial product photograph of {{PRODUCT_DESCRIPTION}},
centered in frame on pure white seamless studio backdrop #FFFFFF,
soft diffused lighting from multiple soft boxes eliminating all shadows,
shot with 50mm lens at f/8 for complete depth of field, product occupies
85% of frame, high-resolution commercial quality suitable for Mercado Livre
or Amazon marketplace listing, clean professional presentation without
any text logos or watermarks
```

### Template 2: Lifestyle Usage

```
Lifestyle photograph of {{PRODUCT}} being used naturally by
{{MODEL_DESCRIPTION}} in {{ENVIRONMENT}}, {{TIME_OF_DAY}} natural lighting
creating warm inviting atmosphere, shallow depth of field with 85mm lens
bokeh effect keeping product sharp, authentic candid moment capturing
real usage, editorial quality suitable for social media marketing
```

### Template 3: Detail Close-Up

```
Extreme close-up photograph of {{PRODUCT_FEATURE}} showing fine detail
and craftsmanship, macro photography with 100mm lens at f/2.8, ring light
providing even illumination on surface texture, premium quality materials
clearly visible, professional studio setting, highlighting
{{SPECIFIC_QUALITY}} of the product
```

### Template 4: Brand Hero

```
Hero brand photograph of {{PRODUCT}} in aspirational setting,
dramatic lighting highlighting product form, {{BRAND_COLORS}} color palette,
premium advertising campaign quality, cinematic composition,
emotional impact emphasizing {{BRAND_VALUE}}, suitable for website
hero banner or marketing materials
```

---

## COMPARISON WITH OTHER PLATFORMS

| Aspect | DALL-E 3 | Midjourney V6 | Imagen 3 |
|--------|----------|---------------|----------|
| Text in Images | Best | Good | Limited |
| Prompt Following | Excellent | Good | Excellent |
| Artistic Style | Natural | Strong | Natural |
| API Access | Yes | No (Discord) | Yes |
| Cost | Medium | Low | Low |
| Speed | Fast | Medium | Fast |
| Customization | Limited | Parameters | Limited |

### When to Choose DALL-E 3

- Need text in images
- API integration required
- Natural language prompts preferred
- ChatGPT workflow
- Precise prompt following critical

---

## INTEGRATION WITH PHOTO_AGENT

### Output Format

photo_agent can generate DALL-E 3 optimized prompts:

```python
# API call format
{
    "model": "dall-e-3",
    "prompt": "[GENERATED_PROMPT]",
    "size": "1024x1024",
    "quality": "hd",
    "style": "natural"
}
```

### Scene to Settings Mapping

| Scene | Size | Quality | Style |
|-------|------|---------|-------|
| 1 (Hero White) | 1024x1024 | hd | natural |
| 2 (Lifestyle) | 1024x1792 | hd | natural |
| 3 (Detail) | 1024x1024 | hd | natural |
| 4 (Use Case) | 1024x1792 | standard | natural |
| 5 (Benefit) | 1024x1792 | hd | vivid |
| 6 (Scale) | 1024x1024 | standard | natural |
| 7 (Context) | 1792x1024 | standard | natural |
| 8 (Material) | 1024x1024 | hd | natural |
| 9 (Commercial) | 1024x1024 | hd | natural |

---

## REFERENCES

- OpenAI DALL-E Documentation: https://platform.openai.com/docs/guides/images
- API Reference: https://platform.openai.com/docs/api-reference/images
- Pricing: https://openai.com/pricing

---

**Version**: 1.0.0 | **Status**: Production Ready
