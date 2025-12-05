# API Integration | shared_knowledge

**Purpose**: Common patterns for AI platform API integration
**Version**: 1.0.0 | **Updated**: 2025-12-05
**Quality Score**: 0.85/1.00

---

## OVERVIEW

This knowledge card documents common patterns for integrating with AI generation platform APIs. Covers authentication, rate limiting, error handling, and cost optimization across major providers.

**Philosophy**: Robust integration = reliable creative workflows.

---

## AUTHENTICATION PATTERNS

### API Key Authentication

Most AI platforms use API key authentication in headers.

**Standard Pattern**:
```python
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
```

### Platform-Specific Auth

#### OpenAI (DALL-E 3)

```python
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.images.generate(
    model="dall-e-3",
    prompt="Your prompt here",
    size="1024x1024",
    quality="hd"
)
```

**Env Variable**: `OPENAI_API_KEY`

#### Google AI (Imagen 3)

```python
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-image")
response = model.generate_content([prompt, image])
```

**Env Variable**: `GOOGLE_API_KEY`

**Alternative (Vertex AI)**:
```python
from google.cloud import aiplatform

aiplatform.init(
    project=os.getenv("GCP_PROJECT_ID"),
    location="us-central1"
)
```

**Env Variables**: `GCP_PROJECT_ID`, `GOOGLE_APPLICATION_CREDENTIALS`

#### Runway

```python
import requests

headers = {
    "Authorization": f"Bearer {os.getenv('RUNWAY_API_KEY')}",
    "Content-Type": "application/json"
}

response = requests.post(
    "https://api.runwayml.com/v1/generate",
    headers=headers,
    json=payload
)
```

**Env Variable**: `RUNWAY_API_KEY`

#### ElevenLabs

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

audio = client.generate(
    text="Your text here",
    voice="FranciscaNeural",
    model="eleven_multilingual_v2"
)
```

**Env Variable**: `ELEVENLABS_API_KEY`

---

## SECURE KEY MANAGEMENT

### Environment Variables (.env)

```bash
# codexa.app/.env
OPENAI_API_KEY=sk-...
GOOGLE_API_KEY=AIzaSy...
RUNWAY_API_KEY=rw_...
ELEVENLABS_API_KEY=...
```

### Key Manager Pattern

```python
# config/secrets.py
import os
from pathlib import Path
from dotenv import load_dotenv

class SecretManager:
    def __init__(self):
        env_path = Path(__file__).parent.parent / ".env"
        load_dotenv(env_path)

    def get(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Missing required key: {key}")
        return value

    def validate(self) -> dict:
        """Check all required keys exist."""
        required = [
            "OPENAI_API_KEY",
            "GOOGLE_API_KEY",
            "RUNWAY_API_KEY"
        ]
        results = {}
        for key in required:
            try:
                value = self.get(key)
                results[key] = f"{value[:10]}...{value[-4:]}"
            except ValueError:
                results[key] = "MISSING"
        return results

secrets = SecretManager()
```

### Security Rules

1. **NEVER** commit `.env` to git
2. **NEVER** log full API keys
3. **ALWAYS** use `.gitignore` for secrets
4. **VALIDATE** keys before API calls
5. **MASK** keys in error messages

```gitignore
# .gitignore
.env
.env.local
*.key
credentials.json
```

---

## RATE LIMITING

### Understanding Limits

| Platform | Rate Limit | Retry After |
|----------|------------|-------------|
| OpenAI | 50 images/min | Exponential |
| Google AI | Variable | Headers |
| Runway | 10 req/min | 60s |
| ElevenLabs | 100 chars/s | Monthly reset |

### Retry Strategy Pattern

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, base_delay=1, max_delay=60):
    """Decorator for exponential backoff retry."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except RateLimitError as e:
                    retries += 1
                    if retries >= max_retries:
                        raise
                    delay = min(base_delay * (2 ** retries), max_delay)
                    print(f"Rate limited. Retry {retries}/{max_retries} in {delay}s")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@retry_with_backoff(max_retries=3)
def generate_image(prompt):
    return client.images.generate(prompt=prompt)
```

### Rate Limit Response Handling

```python
def handle_rate_limit(response):
    """Extract retry information from response."""
    if response.status_code == 429:
        retry_after = response.headers.get("Retry-After", 60)
        return int(retry_after)
    return None
```

### Batch Processing with Delays

```python
import asyncio

async def batch_generate(prompts, delay_between=1.0):
    """Generate multiple images with delay to avoid rate limits."""
    results = []
    for i, prompt in enumerate(prompts):
        print(f"Generating {i+1}/{len(prompts)}")
        result = await generate_image(prompt)
        results.append(result)
        if i < len(prompts) - 1:
            await asyncio.sleep(delay_between)
    return results
```

---

## ERROR HANDLING

### Error Categories

| Category | HTTP Code | Action |
|----------|-----------|--------|
| Rate Limit | 429 | Retry with backoff |
| Auth Error | 401, 403 | Check API key |
| Bad Request | 400 | Validate input |
| Server Error | 500-503 | Retry once |
| Timeout | - | Increase timeout |
| Content Filter | 400 | Modify prompt |

### Comprehensive Error Handler

```python
class APIError(Exception):
    """Base API error."""
    pass

class RateLimitError(APIError):
    """Rate limit exceeded."""
    pass

class AuthenticationError(APIError):
    """Invalid or missing API key."""
    pass

class ContentFilterError(APIError):
    """Content blocked by safety filter."""
    pass

def handle_api_response(response):
    """Handle API response with appropriate errors."""
    if response.status_code == 200:
        return response.json()

    error_body = response.json() if response.text else {}
    error_msg = error_body.get("error", {}).get("message", "Unknown error")

    if response.status_code == 429:
        raise RateLimitError(f"Rate limit: {error_msg}")

    if response.status_code in (401, 403):
        raise AuthenticationError(f"Auth error: {error_msg}")

    if response.status_code == 400:
        if "content_policy" in error_msg.lower():
            raise ContentFilterError(f"Content blocked: {error_msg}")
        raise APIError(f"Bad request: {error_msg}")

    if response.status_code >= 500:
        raise APIError(f"Server error ({response.status_code}): {error_msg}")

    raise APIError(f"Unknown error ({response.status_code}): {error_msg}")
```

### Graceful Degradation

```python
def generate_with_fallback(prompt, platforms=["imagen", "dalle", "midjourney"]):
    """Try multiple platforms in order."""
    errors = []

    for platform in platforms:
        try:
            return generate_on_platform(platform, prompt)
        except (RateLimitError, APIError) as e:
            errors.append(f"{platform}: {str(e)}")
            continue

    # All platforms failed
    raise APIError(f"All platforms failed: {'; '.join(errors)}")
```

---

## REQUEST/RESPONSE PATTERNS

### Standard Request Structure

```python
def make_api_request(
    endpoint: str,
    payload: dict,
    api_key: str,
    timeout: int = 120
) -> dict:
    """Standard API request pattern."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=timeout
        )
        return handle_api_response(response)
    except requests.Timeout:
        raise APIError(f"Request timed out after {timeout}s")
    except requests.ConnectionError:
        raise APIError("Connection failed. Check network.")
```

### Image Upload Pattern

```python
import base64

def encode_image(image_path: str) -> str:
    """Encode image to base64 for API upload."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def prepare_image_payload(prompt: str, image_path: str) -> dict:
    """Prepare payload with image and prompt."""
    image_data = encode_image(image_path)
    mime_type = "image/png" if image_path.endswith(".png") else "image/jpeg"

    return {
        "prompt": prompt,
        "image": {
            "data": image_data,
            "mime_type": mime_type
        }
    }
```

### Async Polling Pattern

```python
async def poll_for_result(job_id: str, max_wait: int = 300):
    """Poll for async job completion."""
    start_time = time.time()
    poll_interval = 2

    while time.time() - start_time < max_wait:
        status = await check_job_status(job_id)

        if status["state"] == "completed":
            return status["result"]
        elif status["state"] == "failed":
            raise APIError(f"Job failed: {status.get('error')}")

        await asyncio.sleep(poll_interval)
        poll_interval = min(poll_interval * 1.5, 10)  # Increase interval

    raise APIError(f"Job timed out after {max_wait}s")
```

---

## COST OPTIMIZATION

### Cost Tracking

```python
class CostTracker:
    """Track API usage costs."""

    COSTS = {
        "dalle3_standard": 0.04,
        "dalle3_hd": 0.08,
        "imagen_flash": 0.02,
        "imagen_pro": 0.05,
        "runway_per_second": 0.05,
        "pika_per_second": 0.03
    }

    def __init__(self):
        self.usage = []

    def log(self, platform: str, count: int = 1, duration: int = None):
        """Log API usage."""
        if duration:
            cost = self.COSTS.get(f"{platform}_per_second", 0) * duration
        else:
            cost = self.COSTS.get(platform, 0) * count

        self.usage.append({
            "platform": platform,
            "count": count,
            "duration": duration,
            "cost": cost,
            "timestamp": time.time()
        })
        return cost

    def total(self) -> float:
        return sum(u["cost"] for u in self.usage)

    def report(self) -> str:
        total = self.total()
        return f"Total cost: ${total:.2f} ({len(self.usage)} operations)"

tracker = CostTracker()
```

### Budget Guards

```python
MAX_DAILY_BUDGET = 10.00  # USD

def check_budget(tracker: CostTracker, estimated_cost: float) -> bool:
    """Check if operation is within budget."""
    current_total = tracker.total()
    if current_total + estimated_cost > MAX_DAILY_BUDGET:
        raise BudgetExceededError(
            f"Budget exceeded. Current: ${current_total:.2f}, "
            f"Estimated: ${estimated_cost:.2f}, "
            f"Limit: ${MAX_DAILY_BUDGET:.2f}"
        )
    return True
```

### Cost-Effective Platform Selection

```python
def select_cheapest_platform(task_type: str) -> str:
    """Select most cost-effective platform for task."""
    platform_costs = {
        "image_basic": [("imagen_flash", 0.02), ("dalle3_standard", 0.04)],
        "image_quality": [("imagen_pro", 0.05), ("dalle3_hd", 0.08)],
        "video_short": [("pika", 0.03), ("runway", 0.05), ("kling", 0.02)],
        "video_quality": [("runway", 0.05), ("veo3", 0.10)]
    }

    options = platform_costs.get(task_type, [])
    if options:
        return min(options, key=lambda x: x[1])[0]
    return "runway"  # Default fallback
```

---

## INTEGRATION EXAMPLES

### Photo Agent Integration

```python
# agentes/photo_agent/api_integrations/google_imagen.py

from config.secrets import secrets
import google.generativeai as genai

def generate_product_image(prompt: str, reference_image: str = None) -> str:
    """Generate product image using Imagen 3."""
    genai.configure(api_key=secrets.get("GOOGLE_API_KEY"))

    model = genai.GenerativeModel("gemini-2.5-flash-image")

    contents = [prompt]
    if reference_image:
        contents.append(load_image(reference_image))

    response = model.generate_content(contents)
    return save_image(response.image)
```

### Video Agent Integration

```python
# agentes/video_agent/api_integrations/runway.py

import requests
from config.secrets import secrets

def generate_video(prompt: str, duration: int = 5) -> str:
    """Generate video using Runway Gen-3."""
    api_key = secrets.get("RUNWAY_API_KEY")

    response = requests.post(
        "https://api.runwayml.com/v1/generate",
        headers={"Authorization": f"Bearer {api_key}"},
        json={
            "prompt": prompt,
            "duration": duration,
            "model": "gen-3-alpha-turbo"
        }
    )

    result = handle_api_response(response)
    return poll_for_result(result["job_id"])
```

### Voice Agent Integration

```python
# agentes/voice_agent/api_integrations/elevenlabs.py

from elevenlabs import ElevenLabs
from config.secrets import secrets

def generate_speech(text: str, voice: str = "FranciscaNeural") -> bytes:
    """Generate speech using ElevenLabs."""
    client = ElevenLabs(api_key=secrets.get("ELEVENLABS_API_KEY"))

    audio = client.generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v2"
    )

    return audio
```

---

## ENVIRONMENT SETUP CHECKLIST

```bash
# Required .env variables
OPENAI_API_KEY=sk-...          # DALL-E 3
GOOGLE_API_KEY=AIzaSy...       # Imagen 3
RUNWAY_API_KEY=rw_...          # Runway Gen-3
ELEVENLABS_API_KEY=...         # ElevenLabs TTS

# Optional
GCP_PROJECT_ID=...             # For Vertex AI
PIKA_API_KEY=...               # Pika Labs
```

---

## CROSS-REFERENCES

| Document | Purpose |
|----------|---------|
| [01_platform_comparison.md](01_platform_comparison.md) | Platform selection |
| [photo_agent/api_integrations/](../../agentes/photo_agent/api_integrations/) | Image API implementation |
| [video_agent/config/](../../agentes/video_agent/config/) | Video API config |
| [docs/API_KEYS_REFERENCE.md](../../docs/API_KEYS_REFERENCE.md) | Key management guide |

---

**Package**: AI_PLATFORMS v1.0.0
**Card**: 03_api_integration
**Quality**: 0.85/1.00
**Date**: 2025-12-05
