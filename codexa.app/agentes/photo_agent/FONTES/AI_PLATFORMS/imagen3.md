# Google Imagen 3 API Guide

**Version**: 1.0.0 | **Updated**: 2025-12-05 | **Source**: Google Cloud AI Documentation

---

## OVERVIEW

Imagen 3 e o modelo mais recente de geracao de imagem do Google, disponivel via Vertex AI. Caracteristicas principais:

- Fotorrealismo superior
- Alta fidelidade a descricoes detalhadas
- Integracao com Google Cloud ecosystem
- Safety filters robustos
- Suporte a edicao de imagens (inpainting/outpainting)

---

## API SETUP

### Prerequisites

```bash
# Install Google Cloud SDK
pip install google-cloud-aiplatform

# Authenticate
gcloud auth application-default login

# Set project
gcloud config set project YOUR_PROJECT_ID
```

### Basic Usage

```python
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# Initialize Vertex AI
vertexai.init(project="your-project-id", location="us-central1")

# Load model
model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

# Generate image
response = model.generate_images(
    prompt="Professional product photo of ceramic coffee mug on white background",
    number_of_images=1,
    aspect_ratio="1:1",
    safety_filter_level="block_some",
    person_generation="allow_adult"
)

# Save image
response.images[0].save("output.png")
```

---

## API PARAMETERS

### Generation Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `prompt` | String (max 480 tokens) | Image description |
| `number_of_images` | 1-4 | Images per request |
| `aspect_ratio` | "1:1", "9:16", "16:9", "4:3", "3:4" | Output ratio |
| `safety_filter_level` | "block_few", "block_some", "block_most" | Content filtering |
| `person_generation` | "dont_allow", "allow_adult", "allow_all" | Person rendering |
| `seed` | Integer | Reproducible results |
| `negative_prompt` | String | Elements to avoid |

### Aspect Ratios

```
1:1   → Square (1024x1024) - Marketplace images
9:16  → Portrait (576x1024) - Mobile/Stories/TikTok
16:9  → Landscape (1024x576) - Banners
4:3   → Standard (1024x768) - General use
3:4   → Portrait (768x1024) - Product tall shots
```

### Safety Filter Levels

```
block_few   → Most permissive, minimal blocking
block_some  → Balanced (recommended for e-commerce)
block_most  → Most restrictive, safest
```

---

## PROMPT STRUCTURE

### Recommended Format

```
[Subject with details], [Environment/Background], [Lighting description],
[Camera/Photography style], [Quality modifiers]
```

### Best Practices

1. **Be Descriptive**: Imagen excels with detailed prompts
2. **Specify Photography Style**: "product photography", "lifestyle photo"
3. **Include Technical Details**: Lens, lighting, composition
4. **Use Quality Keywords**: "high-resolution", "professional", "sharp"

### Example Prompts

**Product Hero Shot**:
```
Professional product photograph of a matte white ceramic coffee mug with
natural wooden handle, centered on pure white seamless studio backdrop,
soft diffused lighting from multiple soft boxes creating even illumination
with no harsh shadows, shot with 50mm lens at f/8 for maximum depth of
field, commercial e-commerce quality, 8K resolution, photorealistic
```

**Lifestyle Context**:
```
Lifestyle photograph of ceramic coffee mug on rustic wooden table in
bright modern Scandinavian kitchen, warm morning sunlight streaming
through window creating soft shadows, shallow depth of field with bokeh
background, cozy inviting atmosphere, editorial magazine quality,
natural and authentic styling
```

---

## ADVANCED FEATURES

### Negative Prompts

```python
response = model.generate_images(
    prompt="Product photo of coffee mug on white background",
    negative_prompt="text, watermark, logo, shadow, blur, low quality, distorted",
    number_of_images=1
)
```

Common negative prompt elements for e-commerce:
```
text, watermark, logo, branding, shadow, reflection, blur, noise,
grain, low quality, distorted, unrealistic, illustrated, cartoon,
cropped, cut off
```

### Seed for Reproducibility

```python
# Same seed = same result (with same prompt)
response = model.generate_images(
    prompt="Coffee mug product photo",
    seed=12345,
    number_of_images=1
)
```

Use seeds for:
- Consistent product variations
- A/B testing prompt changes
- Reproducing successful results

### Image Editing (Inpainting)

```python
from vertexai.preview.vision_models import Image

# Load base image
base_image = Image.load_from_file("product.png")

# Load mask (white = edit area)
mask = Image.load_from_file("mask.png")

# Edit image
response = model.edit_image(
    base_image=base_image,
    mask=mask,
    prompt="Replace background with pure white studio backdrop",
    number_of_images=1
)
```

---

## PHOTOGRAPHY-SPECIFIC PROMPTS

### White Background Product

```
Professional commercial product photograph of {{PRODUCT}}, perfectly
centered composition, pure white seamless studio backdrop, soft diffused
multi-source lighting eliminating all shadows, shot with 50mm standard
lens at f/8 for complete sharpness throughout, product occupies 85% of
frame, high-resolution commercial quality, suitable for e-commerce
marketplace listing, clean isolated presentation
```

### Lifestyle Usage

```
Authentic lifestyle photograph of {{PRODUCT}} in use by {{PERSON}} in
{{ENVIRONMENT}}, natural {{TIME}} lighting creating warm inviting
atmosphere, shallow depth of field with 85mm lens bokeh effect, candid
moment capturing genuine product usage, editorial photography quality,
warm color grading
```

### Detail Macro

```
Extreme close-up macro photograph of {{DETAIL}}, revealing intricate
texture and material quality, 100mm macro lens at f/2.8 with smooth
bokeh background, ring light providing shadowless even illumination,
hyper-detailed surface texture visible, premium craftsmanship showcase
```

### Scale Reference

```
Product photograph of {{PRODUCT}} placed next to {{REFERENCE}} for
accurate size comparison, centered composition on neutral background,
even studio lighting, clear scale relationship visible, informative
e-commerce presentation, shot with 50mm lens at f/8
```

---

## ERROR HANDLING

### Common Errors

```python
from google.api_core import exceptions

try:
    response = model.generate_images(prompt=prompt)
except exceptions.InvalidArgument as e:
    print(f"Invalid prompt or parameters: {e}")
except exceptions.ResourceExhausted as e:
    print(f"Quota exceeded, retry later: {e}")
except exceptions.PermissionDenied as e:
    print(f"Safety filter blocked: {e}")
```

### Safety Filter Blocks

If content is blocked:
1. Check for prohibited content in prompt
2. Reduce `safety_filter_level` if appropriate
3. Modify prompt to be more neutral
4. Avoid explicit references to people in certain contexts

### Rate Limits

```
Default: 10 requests per minute
Max batch: 4 images per request
Retry with exponential backoff
```

---

## COST OPTIMIZATION

### Pricing (Vertex AI)

| Feature | Cost |
|---------|------|
| Image Generation | ~$0.020 per image |
| Image Editing | ~$0.025 per edit |
| Upscaling | ~$0.010 per image |

### Tips

1. Start with `number_of_images=1` for testing
2. Use seeds to reproduce without regenerating
3. Batch similar requests
4. Cache successful prompts
5. Use lower resolution for iterations

---

## COMPARISON WITH COMPETITORS

| Feature | Imagen 3 | DALL-E 3 | Midjourney V6 |
|---------|----------|----------|---------------|
| Photorealism | Excellent | Good | Excellent |
| Text in Image | Limited | Best | Good |
| API Access | Yes | Yes | No |
| Editing Features | Yes | No | Limited |
| Speed | Fast | Fast | Medium |
| Cost | Low | Medium | Low |
| Safety Filters | Strict | Moderate | Moderate |

### When to Choose Imagen 3

- Ultra-photorealistic products needed
- Google Cloud ecosystem
- Image editing (inpainting) required
- Strict content safety requirements
- Cost-sensitive batch generation

---

## E-COMMERCE TEMPLATES

### Template 1: Marketplace Main

```python
prompt = """
Professional e-commerce product photograph of {product_description},
perfectly centered in frame, pure white seamless studio backdrop #FFFFFF,
soft diffused lighting from multiple soft boxes creating even shadowless
illumination, shot with 50mm lens at f/8 for complete depth of field,
product occupies 85% of frame, high-resolution commercial photography,
suitable for Mercado Livre Amazon Shopee marketplace listing,
clean professional isolated product presentation
"""

negative = "text, watermark, logo, shadow, reflection, blur, grain"
```

### Template 2: Lifestyle Scene

```python
prompt = """
Authentic lifestyle photograph of {product} in natural home environment,
{person_description} using product naturally, warm morning light through
window, shallow depth of field with soft bokeh background, 85mm portrait
lens aesthetic, cozy inviting atmosphere, editorial magazine quality,
genuine candid moment
"""
```

### Template 3: Detail Close-Up

```python
prompt = """
Extreme macro photograph of {product_feature}, hyper-detailed texture
and material visible, 100mm macro lens at f/2.8, ring light illumination,
smooth bokeh background, premium quality craftsmanship showcase,
studio photography conditions
"""
```

---

## INTEGRATION WITH PHOTO_AGENT

### API Call Format

```python
def generate_scene(scene_config):
    return model.generate_images(
        prompt=scene_config["prompt"],
        negative_prompt=scene_config.get("negative", ""),
        aspect_ratio=scene_config.get("aspect", "1:1"),
        number_of_images=1,
        safety_filter_level="block_some"
    )
```

### Scene Mapping

| Scene | Aspect | Safety | Person Gen |
|-------|--------|--------|------------|
| 1 (Hero) | 1:1 | block_some | dont_allow |
| 2 (Lifestyle) | 3:4 | block_some | allow_adult |
| 3 (Detail) | 1:1 | block_few | dont_allow |
| 4 (Use Case) | 3:4 | block_some | allow_adult |
| 5 (Benefit) | 9:16 | block_some | allow_adult |
| 6 (Scale) | 1:1 | block_few | dont_allow |
| 7 (Context) | 16:9 | block_some | allow_adult |
| 8 (Material) | 1:1 | block_few | dont_allow |
| 9 (Commercial) | 1:1 | block_some | dont_allow |

---

## REFERENCES

- Vertex AI Imagen: https://cloud.google.com/vertex-ai/docs/generative-ai/image/overview
- API Reference: https://cloud.google.com/vertex-ai/docs/generative-ai/image/generate-images
- Pricing: https://cloud.google.com/vertex-ai/pricing
- Best Practices: https://cloud.google.com/vertex-ai/docs/generative-ai/image/img-gen-prompt-guide

---

**Version**: 1.0.0 | **Status**: Production Ready
