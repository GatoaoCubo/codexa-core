# Platform Comparison | shared_knowledge

**Purpose**: Comprehensive comparison matrix of AI generation platforms
**Version**: 1.0.0 | **Updated**: 2025-12-05
**Quality Score**: 0.85/1.00

---

## OVERVIEW

This knowledge card provides a detailed comparison of AI generation platforms across three categories: image, video, and audio. Use this to select the right platform for specific creative tasks.

**Decision Framework**: Match task requirements to platform strengths.

---

## IMAGE GENERATION PLATFORMS

### Midjourney v6

| Attribute | Value |
|-----------|-------|
| **Provider** | Midjourney Inc. |
| **Access** | Discord bot / Web interface |
| **Pricing** | $10/mo (Basic) - $60/mo (Pro) |
| **Best For** | Artistic, stylized, editorial imagery |

**Strengths**:
- Superior aesthetic quality
- Consistent stylization
- Strong composition understanding
- Excellent lighting simulation
- Active community with style references

**Weaknesses**:
- Limited API access (third-party only)
- Text rendering is unreliable
- Less control over exact details
- Requires Discord interaction

**Prompt Style**:
```
[Subject], [style descriptors], [lighting], [composition] --ar 16:9 --v 6 --style raw
```

**Key Parameters**:
- `--ar`: Aspect ratio (1:1, 16:9, 9:16, etc.)
- `--v 6`: Version (current: v6.1)
- `--style raw`: Less stylized, more photographic
- `--chaos 0-100`: Variation amount
- `--stylize 0-1000`: Artistic interpretation level

---

### DALL-E 3

| Attribute | Value |
|-----------|-------|
| **Provider** | OpenAI |
| **Access** | API / ChatGPT Plus |
| **Pricing** | $0.04 (Standard) - $0.12 (HD) per image |
| **Best For** | Accuracy, text rendering, specific details |

**Strengths**:
- Excellent text rendering
- Strong instruction following
- Good at specific details
- Reliable API access
- Safety filters for brand-safe content

**Weaknesses**:
- Less artistic flexibility
- Can be overly literal
- Limited style transfer
- Fewer aspect ratio options

**Prompt Style**:
```
A detailed description in natural language. Include specific details about composition, lighting, and style.
```

**API Parameters**:
- `model`: "dall-e-3"
- `size`: "1024x1024", "1792x1024", "1024x1792"
- `quality`: "standard", "hd"
- `style`: "vivid", "natural"

---

### Google Imagen 3

| Attribute | Value |
|-----------|-------|
| **Provider** | Google |
| **Access** | AI Studio API / Vertex AI |
| **Pricing** | ~$0.02-0.05 per image |
| **Best For** | Photorealism, product photography, image-to-image |

**Strengths**:
- Superior photorealism
- Excellent image-to-image editing
- Reference image support (up to 14 images)
- Subject preservation (products stay recognizable)
- Good text rendering

**Weaknesses**:
- Stricter content policies
- Slower generation
- Less artistic flexibility
- API complexity

**Prompt Style**:
```
Professional product photography, [subject description], [background], [lighting setup], [style qualifiers], 8K quality
```

**API Models**:
- `gemini-2.5-flash-image`: Fast, cost-effective
- `gemini-3-pro-image-preview`: High quality

---

### Image Platform Selection Matrix

| Requirement | Recommended | Alternative |
|-------------|-------------|-------------|
| Product photos (marketplace) | Imagen 3 | DALL-E 3 |
| Editorial/lifestyle | Midjourney v6 | Imagen 3 |
| Text on images | DALL-E 3 | Imagen 3 |
| Artistic/stylized | Midjourney v6 | - |
| Budget-conscious | Imagen 3 | DALL-E 3 |
| API automation | DALL-E 3 | Imagen 3 |
| Image editing | Imagen 3 | - |

---

## VIDEO GENERATION PLATFORMS

### Google Veo 3

| Attribute | Value |
|-----------|-------|
| **Provider** | Google |
| **Max Duration** | 8 seconds |
| **Resolution** | 1080p |
| **Native Audio** | Yes (dialogue + SFX) |
| **Best For** | Dialogue scenes, realistic content |

**Strengths**:
- Native audio generation
- Excellent photorealism
- Dialogue support (character speech)
- JSON prompting capability

**Prompt Structure**:
```
[Camera movement]: [Scene]. [Subject]. [Action]. [Lighting]. [Style]. [Audio].
```

**Dialogue Syntax**:
```
Character says: "Your text here" (no subtitles)
```

---

### OpenAI Sora 2

| Attribute | Value |
|-----------|-------|
| **Provider** | OpenAI |
| **Max Duration** | 20 seconds |
| **Resolution** | 1080p |
| **Native Audio** | Yes |
| **Best For** | Cinematic content, complex motion |

**Strengths**:
- Longest duration (20s)
- Superior cinematography
- Physics-accurate motion
- Storyboard mode

**Prompt Structure**:
```
LOOK: [visual style, color grade]
CAMERA: [lens, movement, angle]
LIGHTING: [key, fill, mood]
SOUNDSCAPE: [ambient, sfx, music]
ACTION: [subject movement, timing]
```

---

### Runway Gen-3 Alpha Turbo

| Attribute | Value |
|-----------|-------|
| **Provider** | Runway |
| **Max Duration** | 10 seconds |
| **Resolution** | 1080p |
| **Native Audio** | No |
| **Cost** | $0.05/second |
| **Best For** | Fast iteration, camera control |

**Strengths**:
- Reliable output quality
- Good camera control
- Fast turbo mode
- Simple prompt structure
- Established API

**Prompt Structure**:
```
[camera movement]: [establishing scene]. [additional details].
```

---

### Pika 2.0

| Attribute | Value |
|-----------|-------|
| **Provider** | Pika Labs |
| **Max Duration** | 8 seconds |
| **Resolution** | 1080p |
| **Native Audio** | No |
| **Cost** | $0.03/second |
| **Best For** | Effects, transformations, budget |

**Strengths**:
- Cost-effective
- Good for effects
- Pikadditions (add elements)
- Pikaswaps (replace elements)

**Prompt Structure**:
```
[Style] + [Subject] + [Action] + [Environment] + [Lighting] + [Camera]
```

**Camera Flag**: `--camera [movement]`

---

### Kling 1.6

| Attribute | Value |
|-----------|-------|
| **Provider** | Kuaishou |
| **Max Duration** | 5 seconds |
| **Resolution** | 1080p |
| **Native Audio** | No |
| **Cost** | Low (variable) |
| **Best For** | Human animation, budget-conscious |

**Strengths**:
- Cost-effective
- Good human animation
- Fast generation
- 60fps support

**Prompt Structure**:
```
[Subject], [description], [movement], [scene]. [Camera, lighting, atmosphere].
```

---

### Hailuo (MiniMax-01)

| Attribute | Value |
|-----------|-------|
| **Provider** | MiniMax |
| **Max Duration** | 6 seconds |
| **Resolution** | 768p |
| **Native Audio** | No |
| **Cost** | Low |
| **Best For** | VFX-heavy, dynamic movement |

**Strengths**:
- Fast generation
- VFX support
- Dynamic movement
- Emphasis markers

**Prompt Structure**:
```
[Camera Shot + Motion] + [Subject] + [Action] + [Scene] + [Lighting] + [Style/Mood]
```

**Emphasis Syntax**: `((element))` for priority

---

### Video Platform Selection Matrix

| Requirement | Primary | Fallback |
|-------------|---------|----------|
| Dialogue scenes | Veo 3 | Sora 2 |
| Cinematic/narrative | Sora 2 | Runway |
| Fast iteration | Runway | Pika |
| Budget-conscious | Kling | Pika |
| VFX/effects | Hailuo | Pika |
| Transformations | Pika | Runway |
| Human animation | Kling | Sora 2 |
| Long clips (>10s) | Sora 2 | - |

**Fallback Chain**: Runway -> Pika -> Templates

---

## AUDIO/VOICE PLATFORMS

### ElevenLabs

| Attribute | Value |
|-----------|-------|
| **Provider** | ElevenLabs Inc. |
| **Service** | Text-to-Speech (TTS), Voice Cloning |
| **Pricing** | Free tier / $5-22/month |
| **Best For** | Natural-sounding narration |

**Strengths**:
- Most natural TTS available
- Voice cloning (with consent)
- Emotion control
- Multiple languages (PT-BR excellent)
- Streaming support

**Weaknesses**:
- Monthly character limits
- Voice cloning requires samples
- Higher cost than alternatives

**Voice Models**:
- `eleven_multilingual_v2`: Best for PT-BR
- `eleven_turbo_v2`: Faster, lower latency

---

### Microsoft Edge TTS

| Attribute | Value |
|-----------|-------|
| **Provider** | Microsoft |
| **Service** | Text-to-Speech |
| **Pricing** | Free |
| **Best For** | Free option, basic narration |

**Strengths**:
- Completely free
- Good quality for free tier
- Many voice options
- PT-BR support (FranciscaNeural)

**Weaknesses**:
- Less natural than ElevenLabs
- Limited emotion control
- No voice cloning

**Recommended Voice (PT-BR)**:
```
pt-BR-FranciscaNeural
```

---

### OpenAI Whisper

| Attribute | Value |
|-----------|-------|
| **Provider** | OpenAI |
| **Service** | Speech-to-Text (STT) |
| **Pricing** | Free (local), $0.006/minute (API) |
| **Best For** | Accurate transcription |

**Strengths**:
- Excellent accuracy
- Multi-language support
- Can run locally (free)
- Handles accents well

**Weaknesses**:
- STT only (no TTS)
- Local requires GPU for speed
- API has rate limits

**Models**:
- `whisper-large-v3`: Best accuracy
- `whisper-medium`: Good balance
- `whisper-small`: Faster, less accurate

---

### Audio Platform Selection Matrix

| Requirement | Recommended | Alternative |
|-------------|-------------|-------------|
| Natural narration | ElevenLabs | Edge TTS |
| Free TTS | Edge TTS | - |
| Voice cloning | ElevenLabs | - |
| Transcription (STT) | Whisper | - |
| Low latency | ElevenLabs Turbo | Edge TTS |
| PT-BR content | ElevenLabs | Edge TTS |

---

## CROSS-PLATFORM DECISION TREE

```
START: What are you generating?
       |
       +-- IMAGE --> Need text on image?
       |              |
       |              +-- Yes --> DALL-E 3
       |              +-- No --> Photorealistic?
       |                          |
       |                          +-- Yes --> Imagen 3
       |                          +-- No --> Midjourney
       |
       +-- VIDEO --> Need dialogue/audio?
       |              |
       |              +-- Yes --> Veo 3 or Sora 2
       |              +-- No --> Budget-conscious?
       |                          |
       |                          +-- Yes --> Kling or Pika
       |                          +-- No --> Runway
       |
       +-- AUDIO --> Need TTS?
                      |
                      +-- Yes --> Budget?
                      |            |
                      |            +-- Free --> Edge TTS
                      |            +-- Paid --> ElevenLabs
                      +-- No (STT) --> Whisper
```

---

## BRAZILIAN E-COMMERCE RECOMMENDATIONS

For marketplace product content (ML, Shopee, Amazon BR):

| Content Type | Platform | Notes |
|--------------|----------|-------|
| Main product photo | Imagen 3 | White background, photorealistic |
| Lifestyle images | Midjourney | Editorial feel |
| Product videos | Runway | Fast iteration |
| Narrated videos | Runway + ElevenLabs | Combine for best results |
| Short-form (Reels) | Kling | Cost-effective |

---

## INTEGRATION NOTES

**photo_agent**: Uses Imagen 3 as primary, DALL-E 3 as fallback
**video_agent**: Uses Runway as default, platform selection per task
**voice_agent**: Uses Edge TTS (free), ElevenLabs for premium

---

**Package**: AI_PLATFORMS v1.0.0
**Card**: 01_platform_comparison
**Quality**: 0.85/1.00
**Date**: 2025-12-05
