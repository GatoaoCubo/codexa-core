# Flux Model Prompting Guide

**Version**: 1.0.0 | **Updated**: 2025-12-05 | **Source**: Black Forest Labs / Community Documentation

---

## OVERVIEW

Flux e uma familia de modelos de geracao de imagem open-source da Black Forest Labs (criadores do Stable Diffusion). Caracteristicas:

- Alta velocidade de geracao
- Suporte a LoRA e fine-tuning
- Arquitetura transformer moderna
- Versoes open-source e comerciais
- Excelente para customizacao

---

## MODEL VARIANTS

### Flux.1 Family

| Model | Description | Use Case |
|-------|-------------|----------|
| Flux.1 [pro] | Commercial, highest quality | Production |
| Flux.1 [dev] | Open, high quality | Development/testing |
| Flux.1 [schnell] | Fast, lower quality | Rapid prototyping |

### Comparison

```
[pro]     → Best quality, API only, commercial use
[dev]     → Open weights, research/dev, high quality
[schnell] → 4 steps, fastest, acceptable quality
```

---

## API ACCESS

### Replicate (Hosted)

```python
import replicate

output = replicate.run(
    "black-forest-labs/flux-1.1-pro",
    input={
        "prompt": "Professional product photo of coffee mug on white background",
        "aspect_ratio": "1:1",
        "output_format": "png",
        "output_quality": 100,
        "safety_tolerance": 2,
        "prompt_upsampling": True
    }
)
```

### ComfyUI (Local)

```yaml
# Workflow nodes
KSampler:
  steps: 20-28
  cfg: 3.5-4.5
  sampler: euler
  scheduler: normal
  denoise: 1.0

FluxCLIPTextEncode:
  t5xxl: [prompt text]
  clip_l: [prompt text]
```

### fal.ai (Hosted)

```python
import fal_client

result = fal_client.subscribe(
    "fal-ai/flux/dev",
    arguments={
        "prompt": "Product photography of ceramic mug",
        "image_size": "square_hd",
        "num_images": 1,
        "enable_safety_checker": True
    }
)
```

---

## PROMPT STRUCTURE

### Basic Format

```
[Subject description], [Environment], [Lighting], [Style keywords], [Quality modifiers]
```

### Flux-Specific Tips

1. **Front-load important concepts**: Put main subject first
2. **Use natural language**: Flux understands context well
3. **Quality keywords matter**: Add resolution/quality terms
4. **Weighted tokens**: Use (concept:weight) syntax
5. **Keep moderate length**: 75-150 words optimal

---

## TOKEN WEIGHTING

### Syntax

```
(important concept:1.3)     → Increase emphasis
(concept:0.7)               → Decrease emphasis
((double brackets)):1.4     → Equivalent to :1.21
(((triple))):1.6           → Stronger emphasis
```

### Examples

```
(ceramic coffee mug:1.3), (pure white background:1.2), professional
product photography, (sharp focus:1.1), commercial quality
```

### Common Weights

```
Main subject:     1.2-1.4
Background:       1.0-1.2
Lighting:         0.9-1.1
Style:            0.8-1.0
Quality:          1.0-1.2
```

---

## PHOTOGRAPHY PROMPTS

### Product Hero (White Background)

```
(Professional product photograph:1.2) of (ceramic coffee mug:1.3) with
wooden handle, (centered composition:1.1), (pure white seamless backdrop:1.2),
soft diffused studio lighting, no shadows, 50mm lens f/8, commercial
e-commerce photography, (sharp focus throughout:1.1), high resolution,
(isolated product:1.2)
```

### Lifestyle Shot

```
(Lifestyle photography:1.2) of coffee mug on rustic wooden table,
(cozy kitchen environment:1.1), natural window light, morning atmosphere,
shallow depth of field, (85mm lens bokeh:1.1), warm color palette,
authentic moment, editorial quality
```

### Detail Macro

```
(Extreme macro close-up:1.3) of ceramic texture surface,
(100mm macro lens:1.1), f/2.8 shallow DOF, ring light illumination,
(hyper-detailed texture:1.2), material quality visible, premium
craftsmanship, studio photography
```

---

## ASPECT RATIOS

### API Options

```python
aspect_ratio = "1:1"    # Square (1024x1024)
aspect_ratio = "16:9"   # Landscape (1024x576)
aspect_ratio = "9:16"   # Portrait (576x1024)
aspect_ratio = "4:3"    # Standard
aspect_ratio = "3:4"    # Portrait standard
aspect_ratio = "21:9"   # Ultra-wide
```

### Resolution Variants

```
square         → 1024x1024
square_hd      → 1440x1440
portrait_4_3   → 768x1024
portrait_16_9  → 576x1024
landscape_4_3  → 1024x768
landscape_16_9 → 1024x576
```

---

## NEGATIVE PROMPTS

### Basic Structure

```python
negative_prompt = """
blurry, low quality, distorted, deformed, ugly, bad anatomy,
watermark, text, logo, signature, oversaturated, underexposed,
overexposed, noise, grain, pixelated, cropped, out of frame
"""
```

### E-commerce Specific

```
text, watermark, logo, brand name, shadow on white background,
reflection, blur, noise, grain, low quality, distorted proportions,
cropped product, cluttered background, multiple products,
illustration style, cartoon, artistic interpretation
```

---

## LORA INTEGRATION

### What are LoRAs?

LoRA (Low-Rank Adaptation) allows fine-tuning for specific styles or subjects without full model retraining.

### Popular E-commerce LoRAs

```
Product Photography LoRA    → Commercial quality enhancement
Studio Lighting LoRA        → Professional lighting simulation
White Background LoRA       → Clean cutout style
Lifestyle LoRA              → Natural lifestyle aesthetics
```

### Usage (ComfyUI)

```yaml
LoraLoader:
  model: flux.1-dev
  lora_name: "product_photography.safetensors"
  strength_model: 0.8
  strength_clip: 0.8
```

### Combining LoRAs

```python
# Multiple LoRAs with weights
loras = [
    ("product_photo.safetensors", 0.7),
    ("studio_lighting.safetensors", 0.5),
]
```

---

## GENERATION SETTINGS

### Recommended for Product Photography

```yaml
# Flux.1 [dev] settings
steps: 25-30
cfg_scale: 3.5-4.0
sampler: euler
scheduler: normal

# Flux.1 [schnell] settings (fast)
steps: 4
cfg_scale: 1.0
sampler: euler
scheduler: simple
```

### Quality vs Speed

```
High Quality:
  - steps: 28-30
  - cfg: 4.0
  - time: ~15-20s

Balanced:
  - steps: 20
  - cfg: 3.5
  - time: ~10s

Fast Draft:
  - steps: 8-12
  - cfg: 3.0
  - time: ~5s

Schnell (Ultra Fast):
  - steps: 4
  - cfg: 1.0
  - time: ~2s
```

---

## CONTROLNET INTEGRATION

### Available Controls

```
Canny Edge       → Edge-guided generation
Depth Map        → 3D structure control
Pose             → Human pose control
Inpainting       → Region-based editing
Outpainting      → Extend image borders
```

### Product Photography Use Cases

```
Canny Control:
  - Maintain product shape from reference
  - Consistent product across variations

Depth Control:
  - Control foreground/background separation
  - Consistent perspective

Inpainting:
  - Replace backgrounds
  - Fix specific product areas
```

---

## BATCH GENERATION

### Variations Strategy

```python
# Same prompt, different seeds
for i in range(9):
    result = generate(
        prompt=base_prompt,
        seed=base_seed + i,
        # ... other params
    )
```

### Scene Variations

```python
scenes = [
    {"bg": "white studio", "lighting": "soft box"},
    {"bg": "rustic table", "lighting": "window light"},
    {"bg": "modern desk", "lighting": "ambient"},
    # ...
]

for scene in scenes:
    prompt = template.format(**scene)
    generate(prompt=prompt)
```

---

## E-COMMERCE TEMPLATES

### Template 1: Marketplace White

```
(Professional commercial product photograph:1.3) of {{PRODUCT}},
(perfectly centered in frame:1.2), (pure white seamless studio
backdrop:1.3), soft diffused multi-source lighting creating
(no shadows:1.2), 50mm lens at f/8 for complete depth of field,
(product occupies 85% of frame:1.1), high-resolution commercial
photography, e-commerce marketplace ready, (clean isolated
product presentation:1.2), 8K quality
```

Negative:
```
shadow, reflection, gradient background, multiple products,
text, watermark, logo, blur, noise, cropped
```

### Template 2: Lifestyle Natural

```
(Authentic lifestyle photograph:1.2) of {{PRODUCT}} in
{{ENVIRONMENT}}, {{PERSON}} interacting naturally,
(warm {{TIME_OF_DAY}} lighting:1.1) creating inviting atmosphere,
(shallow depth of field:1.1) with 85mm lens bokeh, candid moment,
editorial magazine quality, (natural color grading:1.0)
```

### Template 3: Detail Macro

```
(Extreme macro close-up:1.3) of {{FEATURE}}, revealing
(intricate texture and craftsmanship:1.2), 100mm macro lens
at f/2.8, ring light providing (even shadowless illumination:1.1),
(hyper-detailed surface texture:1.3) visible, premium quality
materials showcase
```

---

## COMPARISON TABLE

| Feature | Flux.1 Pro | Flux.1 Dev | Flux.1 Schnell |
|---------|------------|------------|----------------|
| Quality | Excellent | Very Good | Good |
| Speed | Medium | Medium | Very Fast |
| Steps | 20-28 | 20-28 | 4 |
| Commercial Use | Yes | No | No |
| Open Weights | No | Yes | Yes |
| LoRA Support | Limited | Yes | Yes |
| Best For | Production | Development | Prototyping |

---

## COMMON ISSUES & FIXES

### Issue: Inconsistent Product Shape

```
Solution:
- Use ControlNet Canny with reference
- Increase (product description:1.4) weight
- Add "accurate proportions, correct scale"
```

### Issue: Background Not Pure White

```
Solution:
- Add (pure white background #FFFFFF:1.3)
- Negative: "gradient, off-white, cream, gray"
- Use white background LoRA if available
```

### Issue: Over-Stylized Output

```
Solution:
- Lower cfg_scale to 3.0-3.5
- Add "photorealistic, not illustrated"
- Remove artistic keywords
```

### Issue: Blurry Details

```
Solution:
- Increase steps to 28-30
- Add (sharp focus:1.2) (tack sharp:1.1)
- Use higher resolution output
```

---

## INTEGRATION WITH PHOTO_AGENT

### API Call Template

```python
def flux_generate(scene_config):
    return {
        "prompt": build_weighted_prompt(scene_config),
        "negative_prompt": ECOMMERCE_NEGATIVES,
        "aspect_ratio": scene_config["aspect"],
        "steps": 25,
        "cfg_scale": 3.5,
        "seed": scene_config.get("seed", random.randint(0, 999999))
    }
```

### Scene Settings

| Scene | Steps | CFG | Aspect |
|-------|-------|-----|--------|
| 1 (Hero) | 28 | 4.0 | 1:1 |
| 2 (Lifestyle) | 25 | 3.5 | 4:3 |
| 3 (Detail) | 28 | 4.0 | 1:1 |
| 4 (Use Case) | 25 | 3.5 | 4:3 |
| 5 (Benefit) | 25 | 3.5 | 9:16 |
| 6 (Scale) | 25 | 4.0 | 1:1 |
| 7 (Context) | 20 | 3.5 | 16:9 |
| 8 (Material) | 28 | 4.0 | 1:1 |
| 9 (Commercial) | 28 | 4.0 | 1:1 |

---

## RESOURCES

- Black Forest Labs: https://blackforestlabs.ai
- Replicate Flux: https://replicate.com/black-forest-labs
- ComfyUI Flux: https://github.com/comfyanonymous/ComfyUI
- fal.ai Flux: https://fal.ai/models/flux
- Community LoRAs: https://civitai.com (search "flux")

---

**Version**: 1.0.0 | **Status**: Production Ready
