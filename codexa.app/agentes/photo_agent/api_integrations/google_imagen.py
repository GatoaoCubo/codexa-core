"""
Google Imagen/Gemini API Integration

Handles image generation using Google's Imagen 3 via Gemini API.
Supports reference image + text prompt workflow for product photography.

Key Features:
- Reference image support (send product image + professional prompt)
- Batch processing (9 scenes in one call)
- Error handling and retry logic
- Image download and storage
- API key management from config/secrets.py

Usage:
    from api_integrations import generate_image_with_prompt

    result = generate_image_with_prompt(
        prompt="Professional product photo, minimalist studio...",
        reference_image_path="product.jpg",
        output_path="generated/scene1.png"
    )

    if result.success:
        print(f"Image saved to: {result.output_path}")
    else:
        print(f"Error: {result.error_message}")

Version: 1.0.0
Created: 2025-11-24
API Docs: https://ai.google.dev/gemini-api/docs/image-generation
"""

import base64
import json
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List, Dict, Any
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


# Import config (with fallback for standalone use)
try:
    import sys
    # Add codexa.app to path
    AGENT_DIR = Path(__file__).parent.parent
    CODEXA_APP = AGENT_DIR.parent
    sys.path.insert(0, str(CODEXA_APP))
    from config.secrets import (
        get_google_api_key,
        get_api_timeout,
        get_max_image_size_mb,
    )
except ImportError:
    # Fallback to environment variables
    def get_google_api_key():
        return os.environ.get('GOOGLE_API_KEY')

    def get_api_timeout():
        return int(os.environ.get('GOOGLE_API_TIMEOUT', '30'))

    def get_max_image_size_mb():
        return int(os.environ.get('MAX_IMAGE_SIZE_MB', '10'))


# === CONSTANTS ===

# Gemini API endpoint
API_BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

# Models
MODEL_FLASH = "gemini-2.5-flash-image"  # Faster, cheaper (supports imageConfig but unstable)
MODEL_PRO = "gemini-3-pro-image-preview"  # Higher quality, supports 14 images
MODEL_GEMINI_2_0 = "gemini-2.0-flash-exp-image-generation"  # Experimental, no imageConfig
MODEL_NANO_BANANA = "gemini-2.5-flash-image-preview"  # Nano Banana (no imageConfig, stable)

# Default model (use Nano Banana as it's stable and high quality)
DEFAULT_MODEL = MODEL_NANO_BANANA

# Models that don't support imageConfig
MODELS_WITHOUT_IMAGE_CONFIG = [MODEL_GEMINI_2_0, MODEL_NANO_BANANA, MODEL_FLASH]

# Aspect ratios (for generation config)
# Gemini 2.5 Flash Image supports: 1:1, 3:2, 2:3, 3:4, 4:3, 4:5, 5:4, 9:16, 16:9, 21:9
ASPECT_RATIOS = {
    'square': '1:1',
    'landscape': '16:9',
    'portrait': '9:16',
    'wide': '4:3',
    'ultrawide': '21:9',
    '3:2': '3:2',
    '2:3': '2:3',
    '3:4': '3:4',
    '4:5': '4:5',
    '5:4': '5:4',
}


# === DATA CLASSES ===

@dataclass
class ImageGenerationResult:
    """Result from image generation API call."""
    success: bool
    output_path: Optional[str] = None
    image_data: Optional[bytes] = None
    error_message: Optional[str] = None
    api_response: Optional[Dict[str, Any]] = None
    prompt_used: Optional[str] = None
    reference_image_path: Optional[str] = None


class ImageGenerationError(Exception):
    """Custom exception for image generation errors."""
    pass


# === HELPER FUNCTIONS ===

def _load_image_as_base64(image_path: str) -> tuple[str, str]:
    """
    Load image file and convert to base64.

    Args:
        image_path: Path to image file

    Returns:
        Tuple of (mime_type, base64_data)

    Raises:
        FileNotFoundError: If image doesn't exist
        ImageGenerationError: If image is too large or invalid format
    """
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Check file size
    file_size_mb = image_path.stat().st_size / (1024 * 1024)
    max_size = get_max_image_size_mb()

    if file_size_mb > max_size:
        raise ImageGenerationError(
            f"Image too large: {file_size_mb:.2f}MB (max: {max_size}MB)"
        )

    # Determine MIME type
    suffix = image_path.suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.webp': 'image/webp',
        '.gif': 'image/gif',
    }

    mime_type = mime_types.get(suffix)
    if not mime_type:
        raise ImageGenerationError(
            f"Unsupported image format: {suffix}. "
            f"Supported: {', '.join(mime_types.keys())}"
        )

    # Read and encode
    with open(image_path, 'rb') as f:
        image_bytes = f.read()

    base64_data = base64.b64encode(image_bytes).decode('utf-8')

    return mime_type, base64_data


def _build_request_body(
    prompt: str,
    reference_image_base64: Optional[str] = None,
    reference_mime_type: Optional[str] = None,
    aspect_ratio: str = 'square',
    model: str = DEFAULT_MODEL,
) -> Dict[str, Any]:
    """
    Build API request body.

    Args:
        prompt: Text prompt for image generation
        reference_image_base64: Base64-encoded reference image
        reference_mime_type: MIME type of reference image
        aspect_ratio: Aspect ratio (square/landscape/portrait/wide)
        model: Model name (to determine if imageConfig is supported)

    Returns:
        Request body dictionary
    """
    parts = []

    # Add text prompt
    parts.append({"text": prompt})

    # Add reference image if provided
    if reference_image_base64 and reference_mime_type:
        parts.append({
            "inline_data": {
                "mime_type": reference_mime_type,
                "data": reference_image_base64
            }
        })

    # Build generation config
    generation_config = {
        "responseModalities": ["TEXT", "IMAGE"]
    }

    # Add imageConfig only if model supports it
    if model not in MODELS_WITHOUT_IMAGE_CONFIG:
        generation_config["imageConfig"] = {
            "aspectRatio": ASPECT_RATIOS.get(aspect_ratio, '1:1'),
            "imageSize": "2K"
        }

    # Build request
    request_body = {
        "contents": [{
            "parts": parts
        }],
        "generationConfig": generation_config
    }

    return request_body


def _make_api_request(
    request_body: Dict[str, Any],
    model: str = DEFAULT_MODEL,
    timeout: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Make HTTP request to Gemini API.

    Args:
        request_body: Request body dictionary
        model: Model name
        timeout: Request timeout in seconds

    Returns:
        API response dictionary

    Raises:
        ImageGenerationError: If API request fails
    """
    api_key = get_google_api_key()
    if not api_key:
        raise ImageGenerationError(
            "Google API key not configured. "
            "Set GOOGLE_API_KEY in .env file. "
            "Get key at: https://aistudio.google.com/app/apikey"
        )

    # Build URL
    url = f"{API_BASE_URL}/models/{model}:generateContent"

    # Build request
    headers = {
        'Content-Type': 'application/json',
        'x-goog-api-key': api_key,
    }

    request_data = json.dumps(request_body).encode('utf-8')
    request = Request(url, data=request_data, headers=headers)

    # Set timeout
    if timeout is None:
        timeout = get_api_timeout()

    # Make request
    try:
        with urlopen(request, timeout=timeout) as response:
            response_data = response.read()
            return json.loads(response_data)

    except HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get('error', {}).get('message', error_body)
        except json.JSONDecodeError:
            error_msg = error_body

        raise ImageGenerationError(
            f"API request failed (HTTP {e.code}): {error_msg}"
        )

    except URLError as e:
        raise ImageGenerationError(f"Network error: {e.reason}")

    except Exception as e:
        raise ImageGenerationError(f"Unexpected error: {str(e)}")


def _extract_image_from_response(
    response: Dict[str, Any]
) -> Optional[bytes]:
    """
    Extract image data from API response.

    Args:
        response: API response dictionary

    Returns:
        Image bytes or None if not found
    """
    try:
        candidates = response.get('candidates', [])
        if not candidates:
            return None

        content = candidates[0].get('content', {})
        parts = content.get('parts', [])

        for part in parts:
            inline_data = part.get('inlineData')
            if inline_data:
                base64_data = inline_data.get('data')
                if base64_data:
                    return base64.b64decode(base64_data)

        return None

    except (KeyError, IndexError, AttributeError):
        return None


def _save_image(
    image_data: bytes,
    output_path: str
) -> str:
    """
    Save image data to file.

    Args:
        image_data: Image bytes
        output_path: Output file path

    Returns:
        Absolute path to saved file
    """
    output_path = Path(output_path)

    # Create parent directories
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write image
    with open(output_path, 'wb') as f:
        f.write(image_data)

    return str(output_path.absolute())


# === PUBLIC API ===

def generate_image_with_prompt(
    prompt: str,
    reference_image_path: Optional[str] = None,
    output_path: str = "generated_image.png",
    aspect_ratio: str = 'square',
    model: str = DEFAULT_MODEL,
) -> ImageGenerationResult:
    """
    Generate image using text prompt and optional reference image.

    This is the main function for photo_agent workflow:
    1. User provides product image (reference_image_path)
    2. photo_agent generates professional prompt
    3. This function sends both to Google Imagen
    4. Returns generated professional product photo

    Args:
        prompt: Professional photography prompt (from photo_agent)
        reference_image_path: Path to product image (optional but recommended)
        output_path: Where to save generated image
        aspect_ratio: Image aspect ratio (square/landscape/portrait/wide)
        model: Gemini model to use (flash or pro)

    Returns:
        ImageGenerationResult with success status and output path

    Example:
        >>> result = generate_image_with_prompt(
        ...     prompt="Professional product photography, minimalist studio...",
        ...     reference_image_path="product.jpg",
        ...     output_path="outputs/scene1.png"
        ... )
        >>> if result.success:
        ...     print(f"Saved to: {result.output_path}")
    """
    try:
        # Load reference image if provided
        reference_base64 = None
        reference_mime = None

        if reference_image_path:
            reference_mime, reference_base64 = _load_image_as_base64(
                reference_image_path
            )

        # Build request
        request_body = _build_request_body(
            prompt=prompt,
            reference_image_base64=reference_base64,
            reference_mime_type=reference_mime,
            aspect_ratio=aspect_ratio,
            model=model,
        )

        # Make API request
        response = _make_api_request(request_body, model=model)

        # Extract image
        image_data = _extract_image_from_response(response)

        if not image_data:
            return ImageGenerationResult(
                success=False,
                error_message="No image data in API response",
                api_response=response,
                prompt_used=prompt,
                reference_image_path=reference_image_path,
            )

        # Save image
        saved_path = _save_image(image_data, output_path)

        return ImageGenerationResult(
            success=True,
            output_path=saved_path,
            image_data=image_data,
            api_response=response,
            prompt_used=prompt,
            reference_image_path=reference_image_path,
        )

    except ImageGenerationError as e:
        return ImageGenerationResult(
            success=False,
            error_message=str(e),
            prompt_used=prompt,
            reference_image_path=reference_image_path,
        )

    except Exception as e:
        return ImageGenerationResult(
            success=False,
            error_message=f"Unexpected error: {str(e)}",
            prompt_used=prompt,
            reference_image_path=reference_image_path,
        )


def generate_batch_images(
    prompts: List[str],
    reference_image_path: Optional[str] = None,
    output_dir: str = "outputs",
    aspect_ratio: str = 'square',
    model: str = DEFAULT_MODEL,
    delay_between_requests: float = 1.0,
) -> List[ImageGenerationResult]:
    """
    Generate multiple images in batch (e.g., 9 scenes from photo_agent).

    Args:
        prompts: List of prompts (typically 9 from photo_agent)
        reference_image_path: Single product image used for all scenes
        output_dir: Directory to save generated images
        aspect_ratio: Image aspect ratio
        model: Gemini model to use
        delay_between_requests: Delay between API calls (rate limiting)

    Returns:
        List of ImageGenerationResult (one per prompt)

    Example:
        >>> prompts = [
        ...     "Scene 1 prompt...",
        ...     "Scene 2 prompt...",
        ...     # ... 9 total prompts
        ... ]
        >>> results = generate_batch_images(
        ...     prompts=prompts,
        ...     reference_image_path="product.jpg",
        ...     output_dir="outputs/batch_001"
        ... )
        >>> successful = [r for r in results if r.success]
        >>> print(f"Generated {len(successful)}/{len(prompts)} images")
    """
    results = []

    for i, prompt in enumerate(prompts, start=1):
        output_path = Path(output_dir) / f"scene_{i:02d}.png"

        print(f"Generating image {i}/{len(prompts)}...")

        result = generate_image_with_prompt(
            prompt=prompt,
            reference_image_path=reference_image_path,
            output_path=str(output_path),
            aspect_ratio=aspect_ratio,
            model=model,
        )

        results.append(result)

        # Delay between requests (except for last one)
        if i < len(prompts) and delay_between_requests > 0:
            time.sleep(delay_between_requests)

    return results


# === CLI FOR TESTING ===

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Test Google Imagen API integration"
    )
    parser.add_argument(
        "prompt",
        help="Text prompt for image generation"
    )
    parser.add_argument(
        "--reference",
        help="Path to reference image (product photo)"
    )
    parser.add_argument(
        "--output",
        default="test_output.png",
        help="Output file path"
    )
    parser.add_argument(
        "--aspect",
        default="square",
        choices=['square', 'landscape', 'portrait', 'wide'],
        help="Aspect ratio"
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        choices=[MODEL_FLASH, MODEL_PRO],
        help="Model to use"
    )

    args = parser.parse_args()

    print("=" * 70)
    print("Google Imagen API Test")
    print("=" * 70)
    print(f"Prompt: {args.prompt}")
    print(f"Reference: {args.reference or 'None'}")
    print(f"Output: {args.output}")
    print(f"Aspect: {args.aspect}")
    print(f"Model: {args.model}")
    print("=" * 70)
    print()

    result = generate_image_with_prompt(
        prompt=args.prompt,
        reference_image_path=args.reference,
        output_path=args.output,
        aspect_ratio=args.aspect,
        model=args.model,
    )

    if result.success:
        print("✓ SUCCESS")
        print(f"  Image saved to: {result.output_path}")
        print(f"  Size: {len(result.image_data)} bytes")
    else:
        print("✗ FAILED")
        print(f"  Error: {result.error_message}")

    print()
    print("=" * 70)
