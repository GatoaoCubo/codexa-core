"""
Universal Image Generation Script
Pipeline 200_ADW_PRODUTO_COMPLETO

Generates 9 professional product images using Google Gemini API
with reference image (HARD RULE: all prompts include reference)

Usage:
    1. Copy this script to your product folder
    2. Ensure photo_prompts.json exists in same folder
    3. Ensure reference image exists (imagem_original.webp/jpg/png)
    4. Run: python generate_images.py

Output:
    images/photo_01_hero.png
    images/photo_02_detail_*.png
    ... (9 total)
    images/generation_log.json

Version: 2.0.0
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from glob import glob

# === CONFIGURATION ===

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR

# Find project root by looking for .env or codexa.app
for _ in range(5):
    if (PROJECT_ROOT / ".env").exists() or (PROJECT_ROOT / "codexa.app").exists():
        break
    PROJECT_ROOT = PROJECT_ROOT.parent

CODEXA_APP = PROJECT_ROOT / "codexa.app"

# Add to path for imports
sys.path.insert(0, str(CODEXA_APP))
sys.path.insert(0, str(CODEXA_APP / "agentes" / "photo_agent"))

# === AUTO-DETECT FILES ===

def find_prompts_file():
    """Find photo_prompts.json in current directory."""
    candidates = [
        SCRIPT_DIR / "photo_prompts.json",
        SCRIPT_DIR / "prompts.json",
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError("photo_prompts.json not found in current directory")


def find_reference_image():
    """Find reference image in current directory."""
    patterns = [
        "imagem_original.*",
        "reference.*",
        "product.*",
        "original.*",
    ]
    extensions = [".webp", ".jpg", ".jpeg", ".png"]

    for pattern in patterns:
        matches = list(SCRIPT_DIR.glob(pattern))
        for match in matches:
            if match.suffix.lower() in extensions:
                return match

    # Fallback: find any image
    for ext in extensions:
        matches = list(SCRIPT_DIR.glob(f"*{ext}"))
        if matches:
            # Exclude generated images
            for m in matches:
                if "generated" not in str(m).lower() and "images" not in str(m).lower():
                    return m

    raise FileNotFoundError("Reference image not found. Expected: imagem_original.webp/jpg/png")


# === API KEY ===

def get_api_key():
    """Get Google API key from environment or .env file."""
    api_key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

    if not api_key:
        env_paths = [
            PROJECT_ROOT / ".env",
            CODEXA_APP / ".env",
            Path.home() / ".env",
        ]
        for env_path in env_paths:
            if env_path.exists():
                with open(env_path) as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("GOOGLE_API_KEY=") or line.startswith("GEMINI_API_KEY="):
                            api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                            if api_key:
                                return api_key
    return api_key


# === IMAGE GENERATION ===

def generate_with_gemini_multimodal(prompt_data, output_path, reference_image, api_key):
    """Generate image using Gemini 2.5 Flash with reference image (multimodal)."""
    import base64
    import urllib.request
    import urllib.error

    # Load reference image
    with open(reference_image, 'rb') as f:
        ref_bytes = f.read()
    ref_base64 = base64.b64encode(ref_bytes).decode('utf-8')

    # Determine mime type
    suffix = reference_image.suffix.lower()
    mime_types = {'.webp': 'image/webp', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png'}
    mime_type = mime_types.get(suffix, 'image/jpeg')

    # Build request
    prompt_text = prompt_data["prompt_text"]

    request_body = {
        "contents": [{
            "parts": [
                {"text": f"Generate a professional product photo based on this reference. {prompt_text}"},
                {
                    "inline_data": {
                        "mime_type": mime_type,
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

                    # Ensure output directory exists
                    output_path.parent.mkdir(parents=True, exist_ok=True)

                    with open(output_path, 'wb') as f:
                        f.write(image_bytes)
                    return True, None

        return False, "No image in response"

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return False, f"HTTP {e.code}: {error_body[:200]}"
    except Exception as e:
        return False, str(e)


# === MAIN ===

def main():
    """Main execution."""
    print("=" * 60)
    print("PIPELINE 200_ADW - IMAGE GENERATION")
    print("Universal Script v2.0.0")
    print("=" * 60)
    print()

    # Auto-detect files
    try:
        prompts_file = find_prompts_file()
        print(f"[OK] Prompts: {prompts_file.name}")
    except FileNotFoundError as e:
        print(f"[ERRO] {e}")
        return 1

    try:
        reference_image = find_reference_image()
        print(f"[OK] Reference: {reference_image.name}")
    except FileNotFoundError as e:
        print(f"[ERRO] {e}")
        return 1

    # Load prompts
    with open(prompts_file, encoding="utf-8") as f:
        data = json.load(f)

    prompts = data.get("prompts", [])
    product_name = data.get("product", "Unknown Product")
    print(f"[OK] Product: {product_name}")
    print(f"[OK] Loaded {len(prompts)} prompts")

    # Get API key
    api_key = get_api_key()
    if not api_key:
        print("[ERRO] Google API key not found!")
        print("Set GOOGLE_API_KEY or GEMINI_API_KEY in environment or .env")
        return 1
    print(f"[OK] API key: {api_key[:12]}...")

    # Output directory
    output_dir = SCRIPT_DIR / "images"
    output_dir.mkdir(exist_ok=True)

    # Generation log
    generation_log = {
        "product": product_name,
        "generated_at": datetime.now().isoformat(),
        "reference_image": str(reference_image),
        "model": "gemini-2.5-flash-preview-05-20",
        "results": []
    }

    print()
    print("-" * 60)
    print(f"GENERATING {len(prompts)} IMAGES")
    print("-" * 60)
    print()

    success_count = 0
    delay = 2.0  # Rate limiting

    for i, prompt_data in enumerate(prompts, 1):
        prompt_id = prompt_data.get("prompt_id", f"scene_{i:02d}")
        scene_name = prompt_data.get("scene_name", f"Scene {i}")
        output_path = output_dir / f"{prompt_id}.png"

        print(f"[{i}/{len(prompts)}] {scene_name}")
        print(f"      Output: {output_path.name}")

        # Generate
        success, error_msg = generate_with_gemini_multimodal(
            prompt_data, output_path, reference_image, api_key
        )

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
            time.sleep(delay)

    # Save log
    log_path = output_dir / "generation_log.json"
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(generation_log, f, indent=2, ensure_ascii=False)

    # Summary
    print()
    print("=" * 60)
    print(f"RESULT: {success_count}/{len(prompts)} images generated")
    print(f"Output: {output_dir}")
    print(f"Log: {log_path}")
    print("=" * 60)

    return 0 if success_count == len(prompts) else 1


if __name__ == "__main__":
    sys.exit(main())
