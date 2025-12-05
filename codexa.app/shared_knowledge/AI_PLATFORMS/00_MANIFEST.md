# MANIFEST | AI_PLATFORMS v1.0.0

**Package**: AI_PLATFORMS (shared_knowledge subcategory)
**Version**: 1.0.0 | **Date**: 2025-12-05
**Scope**: AI generation platforms for image, video, and audio
**Files**: 5 | **Total Tokens**: ~12,000

---

## PURPOSE

Consolidated knowledge about AI generation platforms used across creative agents. Covers image generators (Midjourney, DALL-E, Imagen), video generators (Runway, Pika, Veo, Sora, Kling, Hailuo), and audio/voice platforms (ElevenLabs, Edge TTS).

**Philosophy**: Platform-agnostic prompting + platform-specific optimization.

---

## FILE INVENTORY (5 Files)

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 00 | MANIFEST.md | ~500 | Category index |
| 01 | platform_comparison.md | ~3,500 | Image vs Video platform matrix |
| 02 | prompt_engineering.md | ~3,000 | Universal prompting patterns |
| 03 | api_integration.md | ~2,500 | Common API patterns (auth, rate limits) |
| 04 | quality_assessment.md | ~2,500 | How to evaluate AI outputs |

---

## KNOWLEDGE CARDS

### 01_platform_comparison.md

**Content**: Comprehensive comparison of AI generation platforms
- Image: Midjourney v6, DALL-E 3, Google Imagen 3
- Video: Runway Gen-3, Pika 2.0, Google Veo 3, OpenAI Sora 2, Kling 1.6, Hailuo
- Audio: ElevenLabs, Edge TTS, OpenAI Whisper

**Primary Users**: photo_agent, video_agent, voice_agent

### 02_prompt_engineering.md

**Content**: Universal prompting patterns for AI generation
- Core anatomy: Subject + Style + Technical + Modifiers
- Platform-specific syntax adaptations
- Magic words and quality boosters
- Anti-patterns to avoid

**Primary Users**: photo_agent, video_agent

### 03_api_integration.md

**Content**: Common patterns for API integration
- Authentication methods (API keys, OAuth)
- Rate limiting and retry strategies
- Error handling patterns
- Cost optimization techniques

**Primary Users**: photo_agent, video_agent, voice_agent

### 04_quality_assessment.md

**Content**: Framework for evaluating AI-generated outputs
- Technical quality metrics
- Brand alignment scoring
- Marketplace compliance checks
- Human review criteria

**Primary Users**: photo_agent, video_agent, qa_agent

---

## CONSUMING AGENTS

| Agent | Primary Cards | Usage |
|-------|---------------|-------|
| photo_agent | 01, 02, 03, 04 | Image generation workflows |
| video_agent | 01, 02, 03, 04 | Video generation pipelines |
| voice_agent | 01, 03 | TTS and voice synthesis |
| qa_agent | 04 | Quality validation |

---

## PLATFORM QUICK REFERENCE

### Image Generation

| Platform | Best For | Cost | API |
|----------|----------|------|-----|
| Midjourney v6 | Artistic, stylized | $10-60/mo | Discord/Web |
| DALL-E 3 | Accuracy, text | $0.04-0.12/img | OpenAI API |
| Imagen 3 | Photorealism | $0.02-0.05/img | Google AI |

### Video Generation

| Platform | Max Duration | Audio | Cost |
|----------|--------------|-------|------|
| Runway Gen-3 | 10s | No | $0.05/s |
| Pika 2.0 | 8s | No | $0.03/s |
| Veo 3 | 8s | Yes | Variable |
| Sora 2 | 20s | Yes | Variable |
| Kling 1.6 | 5s | No | Low |
| Hailuo | 6s | No | Low |

### Audio/Voice

| Platform | Best For | Cost | Quality |
|----------|----------|------|---------|
| ElevenLabs | Natural TTS | $5-22/mo | Excellent |
| Edge TTS | Free option | Free | Good |
| OpenAI Whisper | STT | Free (local) | Excellent |

---

## INTEGRATION PATTERN

```markdown
## In Agent PRIME.md

### Shared Knowledge References

- [platform_comparison](../../shared_knowledge/AI_PLATFORMS/01_platform_comparison.md)
- [prompt_engineering](../../shared_knowledge/AI_PLATFORMS/02_prompt_engineering.md)
- [api_integration](../../shared_knowledge/AI_PLATFORMS/03_api_integration.md)
- [quality_assessment](../../shared_knowledge/AI_PLATFORMS/04_quality_assessment.md)
```

---

## USAGE VIA SCOUT

```python
# Discover relevant cards
mcp__scout__discover(query="AI image generation platforms")

# Get category context
mcp__scout__smart_context(agent="shared_knowledge")
```

---

## CROSS-REFERENCES

| Document | Purpose |
|----------|---------|
| [photo_agent/PRIME.md](../../agentes/photo_agent/PRIME.md) | Image agent integration |
| [video_agent/PRIME.md](../../agentes/video_agent/PRIME.md) | Video agent integration |
| [voice_agent/PRIME.md](../../agentes/voice_agent/PRIME.md) | Voice agent integration |
| [video_agent/iso_vectorstore/09_platform_specs.json](../../agentes/video_agent/iso_vectorstore/09_platform_specs.json) | Detailed video specs |

---

**Package**: AI_PLATFORMS v1.0.0
**Status**: ACTIVE
**Quality**: Target 0.85/1.00
**Date**: 2025-12-05
