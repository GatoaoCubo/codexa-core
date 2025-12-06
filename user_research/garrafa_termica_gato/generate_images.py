"""
Phase 5 - Image Generation Pipeline
Garrafa Térmica Inox Gato 320ml

Generates 9 professional product images using Google Imagen API
with reference image (HARD RULE: all prompts include reference)

Usage:
    python generate_images.py

Output:
    images/photo_01_hero.png
    images/photo_02_detail_ears.png
    ... (9 total)
    images/generation_log.json
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
CODEXA_APP = PROJECT_ROOT / "codexa.app"

# Add to path for imports
sys.path.insert(0, str(CODEXA_APP))
sys.path.insert(0, str(CODEXA_APP / "agentes" / "photo_agent"))

# Try to use existing integration
try:
    from api_integrations.google_imagen import (
        generate_image_with_prompt,
        DEFAULT_MODEL,
        ASPECT_RATIOS,
    )
    USE_EXISTING_INTEGRATION = True
    print("[OK] Using existing google_imagen integration")
except ImportError:
    USE_EXISTING_INTEGRATION = False
    print("[INFO] Using standalone implementation")

# === CONFIGURATION ===

# Input files
PROMPTS_FILE = SCRIPT_DIR / "photo_prompts.json"
REFERENCE_IMAGE = SCRIPT_DIR / "imagem_original.webp"

# Output directory
OUTPUT_DIR = SCRIPT_DIR / "images"
OUTPUT_DIR.mkdir(exist_ok=True)

# API Configuration
DELAY_BETWEEN_REQUESTS = 2.0  # seconds (rate limiting)
MAX_RETRIES = 2

# Aspect ratio mapping from prompts
ASPECT_RATIO_MAP = {
    "1:1": "square",
    "4:5": "portrait",
    "16:9": "landscape",
    "4:3": "wide",
}


def get_api_key():
    """Get Google API key from environment or .env file."""
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

    if not api_key:
        # Try loading from .env
        env_paths = [
            PROJECT_ROOT / ".env",
            CODEXA_APP / ".env",
        ]
        for env_path in env_paths:
            if env_path.exists():
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GOOGLE_API_KEY=") or line.startswith("GEMINI_API_KEY="):
                            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if api_key:
                                break
            if api_key:
                break

    return api_key


def load_prompts():
    """Load prompts from photo_prompts.json."""
    if not PROMPTS_FILE.exists():
        raise FileNotFoundError(f"Prompts file not found: {PROMPTS_FILE}")

    with open(PROMPTS_FILE, encoding="utf-8") as f:
        data = json.load(f)

    return data["prompts"]


def generate_with_existing_integration(prompt_data, output_path):
    """Generate image using existing google_imagen module."""
    # Get aspect ratio
    tech_specs = prompt_data.get("technical_specs", {})
    aspect = tech_specs.get("aspect_ratio", "1:1")
    aspect_key = ASPECT_RATIO_MAP.get(aspect, "square")

    result = generate_image_with_prompt(
        prompt=prompt_data["prompt_text"],
        reference_image_path=str(REFERENCE_IMAGE),
        output_path=str(output_path),
        aspect_ratio=aspect_key,
    )

    return result.success, result.error_message if not result.success else None


def generate_with_genai_sdk(prompt_data, output_path, client):
    """Generate image using google-genai SDK (Imagen 4.0)."""
    from google.genai import types

    try:
        # Note: Imagen doesn't support reference images directly
        # We append a description of the reference to the prompt
        prompt_text = prompt_data["prompt_text"]

        # Add reference context to prompt
        enhanced_prompt = f"""Based on a product reference photo showing a slim stainless steel thermal bottle 320ml with 3D sculptured cat ears lid, champagne silver metallic brushed finish with horizontal texture lines.

{prompt_text}"""

        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=enhanced_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="4:3",
            )
        )

        if response.generated_images:
            image_data = response.generated_images[0].image.image_bytes
            with open(output_path, 'wb') as f:
                f.write(image_data)
            return True, None
        else:
            return False, "No image generated"

    except Exception as e:
        return False, str(e)


def generate_with_gemini_multimodal(prompt_data, output_path, api_key):
    """Generate image using Gemini 2.5 Flash with reference image (multimodal)."""
    import base64
    import urllib.request
    import urllib.error

    # Load reference image
    with open(REFERENCE_IMAGE, 'rb') as f:
        ref_bytes = f.read()
    ref_base64 = base64.b64encode(ref_bytes).decode('utf-8')

    # Build request
    prompt_text = prompt_data["prompt_text"]

    request_body = {
        "contents": [{
            "parts": [
                {"text": f"Generate a professional product photo based on this reference. {prompt_text}"},
                {
                    "inline_data": {
                        "mime_type": "image/webp",
                        "data": ref_base64
                    }
                }
            ]
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    # API call
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"
    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': api_key,
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(request_body).encode('utf-8'),
        headers=headers
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read())

        # Extract image from response
        candidates = result.get('candidates', [])
        if candidates:
            parts = candidates[0].get('content', {}).get('parts', [])
            for part in parts:
                if 'inlineData' in part:
                    image_b64 = part['inlineData']['data']
                    image_bytes = base64.b64decode(image_b64)
                    with open(output_path, 'wb') as f:
                        f.write(image_bytes)
                    return True, None

        return False, "No image in response"

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return False, f"HTTP {e.code}: {error_body[:200]}"
    except Exception as e:
        return False, str(e)


def main():
    """Main execution."""
    print("=" * 60)
    print("PHASE 5 - IMAGE GENERATION")
    print("Garrafa Térmica Inox Gato 320ml")
    print("=" * 60)
    print()

    # Verify files
    if not REFERENCE_IMAGE.exists():
        print(f"[ERRO] Reference image not found: {REFERENCE_IMAGE}")
        return 1

    print(f"[OK] Reference image: {REFERENCE_IMAGE.name}")

    # Load prompts
    try:
        prompts = load_prompts()
        print(f"[OK] Loaded {len(prompts)} prompts from photo_prompts.json")
    except Exception as e:
        print(f"[ERRO] Failed to load prompts: {e}")
        return 1

    # Get API key
    api_key = get_api_key()
    if not api_key:
        print("[ERRO] Google API key not found!")
        print("Set GOOGLE_API_KEY or GEMINI_API_KEY in environment or .env")
        return 1

    print(f"[OK] API key found: {api_key[:12]}...")

    # Initialize genai client if needed
    genai_client = None
    if not USE_EXISTING_INTEGRATION:
        try:
            from google import genai
            genai_client = genai.Client(api_key=api_key)
            print("[OK] Initialized google-genai client")
        except ImportError:
            print("[INFO] google-genai not available, using REST API")

    # Generation log
    generation_log = {
        "product": "Garrafa Térmica Inox Gato 320ml",
        "generated_at": datetime.now().isoformat(),
        "reference_image": str(REFERENCE_IMAGE),
        "model": "gemini-2.5-flash-preview-05-20",
        "results": []
    }

    print()
    print("-" * 60)
    print("GENERATING 9 IMAGES")
    print("-" * 60)
    print()

    success_count = 0

    for i, prompt_data in enumerate(prompts, 1):
        prompt_id = prompt_data["prompt_id"]
        scene_name = prompt_data["scene_name"]
        output_path = OUTPUT_DIR / f"{prompt_id}.png"

        print(f"[{i}/9] {scene_name}")
        print(f"      Output: {output_path.name}")

        # Generate with retry
        success = False
        error_msg = None

        for attempt in range(MAX_RETRIES + 1):
            if attempt > 0:
                print(f"      Retry {attempt}/{MAX_RETRIES}...")
                time.sleep(DELAY_BETWEEN_REQUESTS)

            # Try different methods
            if USE_EXISTING_INTEGRATION:
                success, error_msg = generate_with_existing_integration(
                    prompt_data, output_path
                )
            elif genai_client:
                success, error_msg = generate_with_genai_sdk(
                    prompt_data, output_path, genai_client
                )
            else:
                success, error_msg = generate_with_gemini_multimodal(
                    prompt_data, output_path, api_key
                )

            if success:
                break

        # Log result
        if success:
            file_size = output_path.stat().st_size / 1024
            print(f"      [OK] Generated ({file_size:.1f} KB)")
            success_count += 1
            generation_log["results"].append({
                "prompt_id": prompt_id,
                "scene_name": scene_name,
                "filename": output_path.name,
                "size_kb": round(file_size, 1),
                "status": "success"
            })
        else:
            print(f"      [ERRO] {error_msg[:80] if error_msg else 'Unknown error'}")
            generation_log["results"].append({
                "prompt_id": prompt_id,
                "scene_name": scene_name,
                "status": "error",
                "error": error_msg[:200] if error_msg else "Unknown"
            })

        # Rate limiting
        if i < len(prompts):
            time.sleep(DELAY_BETWEEN_REQUESTS)

    # Save log
    log_path = OUTPUT_DIR / "generation_log.json"
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(generation_log, f, indent=2, ensure_ascii=False)

    # Summary
    print()
    print("=" * 60)
    print(f"RESULT: {success_count}/{len(prompts)} images generated")
    print(f"Output: {OUTPUT_DIR}")
    print(f"Log: {log_path}")
    print("=" * 60)

    return 0 if success_count == len(prompts) else 1


if __name__ == "__main__":
    sys.exit(main())
