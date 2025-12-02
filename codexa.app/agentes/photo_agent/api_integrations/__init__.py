"""
API Integrations for photo_agent

Handles external API calls to AI image generation services.

Available integrations:
- google_imagen: Google Imagen/Gemini image generation with reference images

Version: 1.0.0
Created: 2025-11-24
"""

from .google_imagen import (
    generate_image_with_prompt,
    generate_batch_images,
    ImageGenerationResult,
    ImageGenerationError,
)

__all__ = [
    'generate_image_with_prompt',
    'generate_batch_images',
    'ImageGenerationResult',
    'ImageGenerationError',
]
