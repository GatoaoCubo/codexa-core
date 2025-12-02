# Quick Start: AI Image Generation with Google Imagen

**NEW**: photo_agent now supports automatic image generation via Google Imagen API!

Instead of just getting text prompts, you can now get actual product images generated automatically.

---

## 🚀 Setup (5 minutes)

### Step 1: Get Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your key (starts with `AIzaSy...`)

### Step 2: Configure API Key

```bash
# Navigate to codexa.app/
cd codexa.app

# Copy example file
cp .env.example .env

# Edit .env file and add your key
# Replace 'your_google_api_key_here' with your actual key
```

**Contents of .env**:
```bash
GOOGLE_API_KEY=AIzaSyC_your_actual_key_here
```

### Step 3: Verify Setup

```bash
# Test API key configuration
python config/secrets.py

# Should show:
# ✓ Google API Key: AIzaSyC...abc
```

✅ **Setup complete!** You're ready to generate images.

---

## 📸 Usage

### Option A: Single Image Generation

**Test the API with a simple prompt**:

```bash
cd agentes/photo_agent

python api_integrations/google_imagen.py \
  "Professional product photography, minimalist studio, white background, soft lighting, 8K" \
  --reference "path/to/your/product.jpg" \
  --output "test_output.png"
```

**Result**: `test_output.png` with your product in professional lighting

---

### Option B: Full 9-Scene Workflow

**Generate complete product photography set** (recommended):

This is the complete photo_agent workflow that:
1. Generates 9 professional prompts
2. Calls Google Imagen API for each
3. Returns 9 marketplace-ready images

**Workflow**: `110_ADW_IMAGE_TO_IMAGE.md`

**Usage through Claude Code or other AI assistant**:

```markdown
User: Generate professional product photos for my thermal water bottle

AI reads: agentes/photo_agent/workflows/110_ADW_IMAGE_TO_IMAGE.md

AI asks for:
- Product description: "Garrafa térmica 500ml aço inox"
- Product image: /path/to/product.jpg
- Style: minimalist (or dramatic/lifestyle/editorial/commercial)
- Marketplace: mercado_livre (optional)

AI executes workflow → generates 9 images in outputs/ folder
```

**Output**:
```
outputs/20251124_120000/
├── images/
│   ├── scene_01.png  ← Main photo (white background)
│   ├── scene_02.png  ← Lifestyle scene
│   ├── scene_03.png  ← Detail shot
│   └── ... (9 total)
├── prompts.json      ← All prompts used
├── metadata.json     ← Complete data
└── REPORT.md         ← Summary
```

---

## 🎯 When to Use Each Option

### Use Workflow 100 (TEXT PROMPTS ONLY):
- You want to use Midjourney or DALL-E manually
- You need maximum control over each generation
- You want to review prompts before generating
- **Output**: 9 text prompts to copy-paste

### Use Workflow 110 (AUTO IMAGE GENERATION):
- You want automated end-to-end generation
- You have Google API key configured
- You need 9 images quickly
- **Output**: 9 actual PNG images

**Both workflows** use the same professional prompt generation engine!

---

## 💡 Examples

### Example 1: Marketplace Product Photo

```bash
python api_integrations/google_imagen.py \
  "Professional product photography, white background (#FFFFFF), centered composition, soft even lighting, high detail, 8K, no text, no watermarks" \
  --reference "products/thermal_bottle.jpg" \
  --output "marketplace/main_photo.png" \
  --aspect square
```

### Example 2: Lifestyle Scene

```bash
python api_integrations/google_imagen.py \
  "Lifestyle product photography, thermal bottle on wooden picnic table, outdoor natural lighting, golden hour, shallow depth of field (f/2.8), warm tones, bokeh background, 8K" \
  --reference "products/thermal_bottle.jpg" \
  --output "lifestyle/scene_outdoor.png" \
  --aspect landscape
```

### Example 3: Batch Generation (9 scenes)

**See workflow**: `workflows/110_ADW_IMAGE_TO_IMAGE.md`

This automatically generates all 9 scenes using the photo_agent prompt engine.

---

## 🔧 Troubleshooting

### Error: "Google API key not configured"

**Solution**:
```bash
# 1. Create .env file
cp .env.example .env

# 2. Edit .env and add key
# GOOGLE_API_KEY=AIzaSyC_your_key_here

# 3. Verify
python config/secrets.py
```

### Error: "Image too large: 15.2MB (max: 10MB)"

**Solution** - Resize image:
```bash
# Using ImageMagick
convert product.jpg -resize 2048x2048> product_resized.jpg

# Using Python PIL
from PIL import Image
img = Image.open("product.jpg")
img.thumbnail((2048, 2048))
img.save("product_resized.jpg")
```

### Error: "API request failed (HTTP 429): Rate limit exceeded"

**Solution** - Add delay between requests:
```python
# In generate_batch_images(), increase delay:
results = generate_batch_images(
    prompts=prompts,
    reference_image_path="product.jpg",
    delay_between_requests=3.0  # Changed from 1.0 to 3.0
)
```

### Error: "No image data in API response"

**Possible causes**:
1. Prompt contains forbidden content (check prompt wording)
2. Reference image is invalid/corrupted
3. API model is unavailable (try different model)

**Solution**:
```python
# Try different model
generate_image_with_prompt(
    prompt=your_prompt,
    reference_image_path="product.jpg",
    model='gemini-3-pro-image-preview'  # Instead of flash
)
```

---

## 📊 Cost Estimates

**Google Imagen API Pricing** (as of Nov 2024):
- **Flash model** (`gemini-2.5-flash-image`): ~$0.02 per image
- **Pro model** (`gemini-3-pro-image-preview`): ~$0.05 per image

**9-scene workflow cost**:
- Flash: 9 × $0.02 = **~$0.18**
- Pro: 9 × $0.05 = **~$0.45**

**Recommendation**: Use Flash for testing, Pro for final production images.

---

## 🎨 Supported Features

### Aspect Ratios
- `square` → 1:1 (Instagram, marketplace thumbnails)
- `landscape` → 16:9 (website banners, YouTube)
- `portrait` → 9:16 (Instagram Stories, Pinterest)
- `wide` → 4:3 (product catalogs)

### Image Formats
- **Input**: PNG, JPG, JPEG, WEBP, GIF
- **Output**: PNG (high quality, no compression artifacts)

### Reference Images
- **Max size**: 10MB
- **Recommended**: 2048×2048px or smaller
- **Purpose**: Your actual product photo (not a placeholder)

---

## 🚀 Advanced Usage

### Custom Brand Colors

```python
# Generate with brand colors
prompt = f"""
Professional product photography, minimalist studio,
background gradient from #2C5F2D to #FFFFFF,
brand colors: forest green (#2C5F2D), off-white (#F8F8F8),
soft lighting, centered composition, 8K
"""

result = generate_image_with_prompt(
    prompt=prompt,
    reference_image_path="product.jpg"
)
```

### Marketplace-Specific Requirements

```python
# Mercado Livre (scene 1 - main photo)
prompt_scene1 = """
Professional product photography, pure white background (#FFFFFF),
product centered and fills 85% of frame, even soft lighting,
front-facing view, high fidelity, 8K, no text, no watermarks
"""

# Shopee (colorful, lifestyle)
prompt_shopee = """
Lifestyle product photography, vibrant colorful background,
natural lifestyle context, warm inviting lighting, 8K
"""
```

### Retry Failed Generations

```python
from api_integrations import generate_image_with_prompt

# Load failed prompts
import json
with open("outputs/batch_001/failed_prompts.json") as f:
    failed = json.load(f)

# Retry with different model
for i, prompt in enumerate(failed, 1):
    result = generate_image_with_prompt(
        prompt=prompt,
        reference_image_path="product.jpg",
        output_path=f"outputs/retry/scene_{i:02d}.png",
        model='gemini-3-pro-image-preview'  # Try Pro model
    )

    if result.success:
        print(f"✓ Retry {i} successful")
    else:
        print(f"✗ Retry {i} failed: {result.error_message}")
```

---

## 📚 Related Documentation

- **Workflow 110**: `workflows/110_ADW_IMAGE_TO_IMAGE.md` (full pipeline)
- **API Module**: `api_integrations/google_imagen.py` (implementation)
- **Config**: `config/secrets.py` (API key management)
- **Original Workflow**: `workflows/100_ADW_RUN_PHOTO.md` (text prompts only)

---

## ✅ Next Steps

1. **Test single image**: Try Option A above
2. **Review output**: Check quality and adjust prompt
3. **Run full workflow**: Use Workflow 110 for 9 scenes
4. **Upload to marketplace**: Use generated images

---

**Questions?**
- Check `workflows/110_ADW_IMAGE_TO_IMAGE.md` for detailed workflow
- Test API with `python api_integrations/google_imagen.py --help`
- Validate setup with `python config/secrets.py`

**Ready to generate professional product photos!** 📸

---

**Version**: 1.0.0
**Created**: 2025-11-24
**API**: Google Imagen 3 via Gemini
**Models**: gemini-2.5-flash-image, gemini-3-pro-image-preview
