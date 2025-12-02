# ADW: Image-to-Image Product Photography Pipeline
**Workflow ID**: 110_ADW_IMAGE_TO_IMAGE
**Version**: 1.0.0
**Duration**: 5-15 minutes (9 API calls)
**Type**: Full Pipeline (Prompt Generation + Image Generation)

---

## WHAT THIS WORKFLOW DOES

**Complete end-to-end product photography generation**:
1. User provides: Product description + original product image
2. photo_agent generates: 9 professional photography prompts
3. Google Imagen API: Generates 9 professional photos using original image + prompts
4. Output: 9 marketplace-ready product images + metadata

**Key difference from 100_ADW_RUN_PHOTO**:
- Workflow 100: Generates TEXT PROMPTS only (for manual use in Midjourney/DALL-E)
- Workflow 110: Generates ACTUAL IMAGES via Google Imagen API (automated)

---

## PREREQUISITES

### 1. API Key Configuration
```bash
# Copy .env.example to .env
cp codexa.app/.env.example codexa.app/.env

# Edit .env and add your Google API key
# Get key at: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your_actual_api_key_here
```

### 2. Verify API Key
```bash
cd codexa.app
python config/secrets.py
# Should show: ✓ Google API Key: AIzaSyC...abc
```

### 3. Required Files
- ✅ Original product image (PNG/JPG/WEBP, max 10MB)
- ✅ Product description (text)
- ✅ Style preference (minimalist/dramatic/lifestyle/editorial/commercial)

---

## INPUT SCHEMA

```json
{
  "product_description": "Garrafa térmica 500ml aço inox",
  "product_image_path": "/path/to/product_photo.jpg",
  "style": "minimalist",
  "brand_profile": {
    "colors": ["#2C5F2D", "#FFFFFF"],
    "mood": "clean, eco-friendly, modern"
  },
  "marketplace": "mercado_livre",
  "aspect_ratio": "square",
  "output_dir": "outputs/batch_001"
}
```

**Required**:
- `product_description` (string)
- `product_image_path` (valid file path)

**Optional**:
- `style` (default: "minimalist")
- `brand_profile` (default: none)
- `marketplace` (default: "mercado_livre")
- `aspect_ratio` (default: "square")
- `output_dir` (default: "outputs/YYYYMMDD_HHMMSS")

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "110_ADW_IMAGE_TO_IMAGE",
  "version": "1.1.0",
  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "photo_prompt"},
    {"phase_id": "phase_1_setup", "phase_name": "Setup & Validation", "duration": "2min", "module": "PHASE_1_SETUP"},
    {"phase_id": "phase_2_prompts", "phase_name": "Prompt Generation", "duration": "2-5min", "module": "PHASE_2_PROMPTS"},
    {"phase_id": "phase_3_generation", "phase_name": "Image Generation", "duration": "5-10min", "module": "PHASE_3_GENERATION"},
    {"phase_id": "phase_4_validation", "phase_name": "Post-Processing & Validation", "duration": "1-2min", "module": "PHASE_4_VALIDATION"},
    {"phase_id": "phase_5_delivery", "phase_name": "Delivery", "duration": "30sec", "module": "PHASE_5_DELIVERY"}
  ]
}
```

---

## PHASE 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `photo_prompt`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

## PHASE 1: SETUP & VALIDATION (2 min)

### Objective
Validate all inputs and API configuration before starting generation.

### Steps

#### 1.1 Validate API Key
```python
from config.secrets import get_google_api_key, validate_api_keys

status = validate_api_keys()
if not status['google_api_key']:
    raise Exception(
        "Google API key not configured!\n"
        "1. Copy .env.example to .env\n"
        "2. Add your API key from https://aistudio.google.com/app/apikey\n"
        "3. Set GOOGLE_API_KEY=your_key_here"
    )

print("✓ API key validated")
```

#### 1.2 Validate Product Image
```python
from pathlib import Path

product_image = Path(input_data['product_image_path'])

# Check exists
if not product_image.exists():
    raise FileNotFoundError(f"Product image not found: {product_image}")

# Check format
valid_formats = ['.png', '.jpg', '.jpeg', '.webp']
if product_image.suffix.lower() not in valid_formats:
    raise ValueError(f"Invalid format. Supported: {valid_formats}")

# Check size
size_mb = product_image.stat().st_size / (1024 * 1024)
if size_mb > 10:
    raise ValueError(f"Image too large: {size_mb:.2f}MB (max: 10MB)")

print(f"✓ Product image validated: {product_image.name} ({size_mb:.2f}MB)")
```

#### 1.3 Create Output Directory
```python
from datetime import datetime

output_dir = input_data.get('output_dir')
if not output_dir:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"outputs/{timestamp}"

output_dir = Path(output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

print(f"✓ Output directory: {output_dir}")
```

### Success Criteria
- ✅ API key configured and valid
- ✅ Product image exists and meets requirements
- ✅ Output directory created

### Outputs
- `validated_image_path` (Path)
- `output_dir` (Path)
- `api_key_status` (bool)

---

## PHASE 2: PROMPT GENERATION (2-5 min)

### Objective
Generate 9 professional photography prompts using photo_agent workflow.

### Steps

#### 2.1 Load Prompt Generator HOP
```markdown
Read: agentes/photo_agent/prompts/30_prompt_generator_HOP.md

This contains the complete instructions for generating professional
photography prompts with camera specs, lighting, composition, and PNL.
```

#### 2.2 Execute Prompt Generation
Follow the 30_prompt_generator_HOP.md workflow to generate 9 prompts based on:
- Product description
- Style preference
- Brand profile (if provided)
- Marketplace requirements (if specified)

**Output**: 9 prompts saved to `{output_dir}/prompts.json`

```json
{
  "prompts": [
    "Professional product photography of thermal water bottle, minimalist studio...",
    "Lifestyle shot of thermal bottle on wooden hiking table...",
    // ... 9 total prompts
  ],
  "metadata": {
    "product": "Garrafa térmica 500ml aço inox",
    "style": "minimalist",
    "generated_at": "2025-11-24T12:00:00"
  }
}
```

#### 2.3 Validate Prompts
```python
# Check all 9 prompts exist
if len(prompts) != 9:
    raise ValueError(f"Expected 9 prompts, got {len(prompts)}")

# Check prompt length (80-350 chars per photo_agent specs)
for i, prompt in enumerate(prompts, 1):
    if len(prompt) < 80 or len(prompt) > 350:
        print(f"⚠️  Warning: Prompt {i} length {len(prompt)} (expected 80-350)")

print(f"✓ Generated {len(prompts)} prompts")
```

### Success Criteria
- ✅ 9 prompts generated
- ✅ All prompts meet length requirements (80-350 chars)
- ✅ Prompts saved to {output_dir}/prompts.json

### Outputs
- `prompts` (List[str]) - 9 professional photography prompts
- `prompts.json` - Saved file with all prompts + metadata

---

## PHASE 3: IMAGE GENERATION (5-10 min)

### Objective
Generate 9 professional product images using Google Imagen API.

### Steps

#### 3.1 Import API Integration
```python
from api_integrations import generate_batch_images
```

#### 3.2 Execute Batch Generation
```python
results = generate_batch_images(
    prompts=prompts,
    reference_image_path=str(validated_image_path),
    output_dir=str(output_dir / "images"),
    aspect_ratio=input_data.get('aspect_ratio', 'square'),
    model='gemini-2.5-flash-image',  # or 'gemini-3-pro-image-preview'
    delay_between_requests=1.0,  # Rate limiting
)

print(f"Starting batch generation ({len(prompts)} images)...")
print(f"Reference image: {validated_image_path.name}")
print(f"Output directory: {output_dir / 'images'}")
print(f"Estimated time: {len(prompts) * 2} seconds")
print()

# Results are returned as list of ImageGenerationResult
```

#### 3.3 Monitor Progress
```python
successful = []
failed = []

for i, result in enumerate(results, 1):
    if result.success:
        successful.append(result)
        print(f"✓ Scene {i:02d}: {Path(result.output_path).name}")
    else:
        failed.append(result)
        print(f"✗ Scene {i:02d}: {result.error_message}")

print()
print(f"Results: {len(successful)}/{len(prompts)} successful")
```

#### 3.4 Handle Errors
```python
if failed:
    print(f"⚠️  {len(failed)} images failed to generate:")
    for i, result in enumerate(failed, 1):
        print(f"  {i}. {result.error_message}")
        if result.prompt_used:
            print(f"     Prompt: {result.prompt_used[:60]}...")
    print()

    # Save failed prompts for retry
    failed_prompts = [r.prompt_used for r in failed if r.prompt_used]
    with open(output_dir / "failed_prompts.json", 'w') as f:
        json.dump(failed_prompts, f, indent=2)
    print(f"Failed prompts saved to: {output_dir}/failed_prompts.json")
```

### Success Criteria
- ✅ At least 7/9 images generated successfully (≥77%)
- ✅ All successful images saved to output directory
- ✅ Failed prompts logged for retry

### Outputs
- 9 PNG images (e.g., `scene_01.png` through `scene_09.png`)
- `generation_results.json` - Full results metadata
- `failed_prompts.json` - Failed prompts for retry (if any)

---

## PHASE 4: POST-PROCESSING & VALIDATION (1-2 min)

### Objective
Validate generated images and create final delivery package.

### Steps

#### 4.1 Validate Image Quality
```python
from PIL import Image

for result in successful:
    img_path = Path(result.output_path)

    # Check file exists
    if not img_path.exists():
        print(f"⚠️  Warning: {img_path.name} not found")
        continue

    # Check image can be opened
    try:
        with Image.open(img_path) as img:
            width, height = img.size
            print(f"✓ {img_path.name}: {width}x{height}px, {img.mode}")
    except Exception as e:
        print(f"✗ {img_path.name}: Invalid image - {e}")
```

#### 4.2 Generate Metadata File
```python
import json
from datetime import datetime

metadata = {
    "workflow": "110_ADW_IMAGE_TO_IMAGE",
    "version": "1.0.0",
    "generated_at": datetime.now().isoformat(),
    "input": {
        "product_description": input_data['product_description'],
        "product_image": str(validated_image_path),
        "style": input_data.get('style', 'minimalist'),
        "marketplace": input_data.get('marketplace'),
    },
    "output": {
        "total_images": len(prompts),
        "successful": len(successful),
        "failed": len(failed),
        "output_directory": str(output_dir),
    },
    "images": [
        {
            "scene_number": i,
            "filename": Path(r.output_path).name,
            "prompt": r.prompt_used,
            "reference_image": r.reference_image_path,
        }
        for i, r in enumerate(successful, 1)
    ],
}

# Save metadata
with open(output_dir / "metadata.json", 'w', encoding='utf-8') as f:
    json.dump(metadata, f, indent=2, ensure_ascii=False)

print(f"✓ Metadata saved: {output_dir}/metadata.json")
```

#### 4.3 Create Summary Report
```markdown
# Product Photography Generation Report

**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Product**: {product_description}
**Style**: {style}
**Marketplace**: {marketplace}

## Results

- **Total Scenes**: {len(prompts)}
- **Successful**: {len(successful)}
- **Failed**: {len(failed)}
- **Success Rate**: {len(successful)/len(prompts)*100:.1f}%

## Generated Images

{list of images with filenames}

## Failed Images

{list of failed images with error messages, if any}

## Next Steps

1. Review generated images in: `{output_dir}/images/`
2. Upload to marketplace: {marketplace}
3. If images failed, retry with: `{output_dir}/failed_prompts.json`

---
Generated by photo_agent workflow 110_ADW_IMAGE_TO_IMAGE v1.0.0
```

Save report to `{output_dir}/REPORT.md`

### Success Criteria
- ✅ All successful images validated (can be opened, correct format)
- ✅ Metadata file created with complete information
- ✅ Summary report generated

### Outputs
- `metadata.json` - Complete workflow metadata
- `REPORT.md` - Human-readable summary
- Validated image files

---

## PHASE 5: DELIVERY (30 sec)

### Objective
Package final deliverables and provide user instructions.

### Final Output Structure
```
outputs/batch_001/
├── images/
│   ├── scene_01.png  # Generated images
│   ├── scene_02.png
│   └── ... (9 total)
├── prompts.json      # All prompts used
├── metadata.json     # Complete workflow data
├── REPORT.md         # Human-readable summary
└── failed_prompts.json  # (only if failures)
```

### User Instructions
```markdown
## ✅ Generation Complete!

Your product photography has been generated:

**Location**: `{output_dir}`
**Images**: {len(successful)}/{len(prompts)} successful
**Total Size**: {total_size_mb:.2f}MB

### Next Steps:

1. **Review Images**: Open `{output_dir}/images/` folder
2. **Read Report**: Check `{output_dir}/REPORT.md` for details
3. **Upload to Marketplace**: Use scene_01.png and scene_09.png for main photos (white background)
4. **Use Lifestyle Scenes**: Scenes 02-08 for product gallery

### If Any Failed:

Retry failed images:
```bash
cd agentes/photo_agent
python api_integrations/google_imagen.py "your prompt" --reference "product.jpg" --output "scene_XX.png"
```

Or check `{output_dir}/failed_prompts.json` for prompts to retry.
```

### Success Criteria
- ✅ All files organized in output directory
- ✅ User instructions printed to console
- ✅ Return paths to user/calling system

### Outputs
- Organized output directory
- Console output with next steps
- Return value: `{"success": True, "output_dir": str(output_dir), "images": len(successful)}`

---

## ERROR HANDLING

### Common Errors

#### 1. API Key Not Configured
```
Error: Google API key not configured

Solution:
1. Copy .env.example to .env
2. Get API key: https://aistudio.google.com/app/apikey
3. Set GOOGLE_API_KEY=your_key in .env
```

#### 2. Image Too Large
```
Error: Image too large: 15.2MB (max: 10MB)

Solution:
Resize image before uploading:
```bash
convert product.jpg -resize 2048x2048> product_resized.jpg
```
```

#### 3. API Rate Limit
```
Error: API request failed (HTTP 429): Rate limit exceeded

Solution:
- Increase delay_between_requests to 2.0 or 3.0
- Wait 1 minute and retry
- Use batch processing with smaller batches
```

#### 4. Invalid Reference Image
```
Error: Unsupported image format: .bmp

Solution:
Convert image to supported format (PNG/JPG/WEBP):
```bash
convert product.bmp product.png
```
```

---

## PERFORMANCE NOTES

### Expected Timings
- Phase 1 (Setup): 1-2 minutes
- Phase 2 (Prompts): 2-5 minutes
- Phase 3 (Generation): 5-10 minutes (9 images @ 1s delay)
- Phase 4 (Validation): 1-2 minutes
- Phase 5 (Delivery): 30 seconds

**Total**: 10-20 minutes for 9 professional product images

### Optimization Tips
1. **Use Flash Model**: `gemini-2.5-flash-image` is faster and cheaper
2. **Parallel Generation**: For advanced users, remove delay and use async
3. **Batch Size**: Generate 3-4 images first, validate, then continue
4. **Caching**: Reuse prompts.json for different reference images

---

## VERSION HISTORY

**v1.0.0** (2025-11-24)
- Initial release
- Google Imagen API integration
- Batch generation support
- Complete error handling
- Metadata and reporting

---

## RELATED WORKFLOWS

- **100_ADW_RUN_PHOTO**: Generate TEXT PROMPTS only (no API calls)
- **120_ADW_RETRY_FAILED**: Retry failed image generations
- **130_ADW_UPSCALE**: Upscale generated images to 4K

---

**Workflow Complete** ✓
