# ElevenLabs Multilingual v2 | Knowledge Card

**Category**: TTS_PLATFORMS | **Quality Score**: 0.85
**Last Updated**: 2025-12-05 | **Version**: 1.0.0

---

## Executive Summary

ElevenLabs is the industry-leading text-to-speech platform for production-quality voice synthesis. Their Multilingual v2 model supports 29+ languages with exceptional emotional range and natural prosody. Best choice for professional content requiring human-like voice quality.

**Key Differentiator**: Emotional expressiveness + voice cloning capabilities

---

## Key Concepts

### Models Available

| Model | Latency | Quality | Use Case |
|-------|---------|---------|----------|
| Eleven Multilingual v2 | ~1s | Highest | Production, emotional content |
| Eleven Turbo v2.5 | ~300ms | High | Real-time, streaming |
| Eleven Flash v2.5 | ~75ms | Good | Ultra-low latency |
| Eleven English v1 | ~500ms | High | English-only legacy |

### Voice Library

**Pre-built Voices**: 100+ stock voices across genders, ages, accents
**Voice Lab**: Clone any voice with 1-30 minutes of audio
**Professional Clones**: High-fidelity cloning service

### Supported Languages (29+)

Primary: English, Spanish, Portuguese, French, German, Italian, Polish, Hindi
Extended: Japanese, Korean, Chinese, Arabic, Turkish, Dutch, Swedish, Norwegian, Finnish, Danish, Czech, Greek, Romanian, Hungarian, Vietnamese, Indonesian, Filipino, Malay, Tamil, Ukrainian

### Audio Output Formats

| Format | Quality | Use Case |
|--------|---------|----------|
| mp3_44100_128 | Standard | Web, general |
| mp3_44100_192 | High | Podcasts |
| pcm_16000 | Raw | Processing |
| pcm_22050 | Raw HD | Post-production |
| pcm_24000 | Raw HQ | Studio |
| pcm_44100 | Raw Max | Archival |
| ulaw_8000 | Telephony | Phone systems |

---

## How to Apply

### Basic TTS Request (Python)

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="your_api_key")

audio = client.text_to_speech.convert(
    voice_id="JBFqnCBsd6RMkjVDRZzb",  # George
    model_id="eleven_multilingual_v2",
    text="Ola! Bem-vindo ao nosso curso de marketing digital.",
    voice_settings={
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.3,
        "use_speaker_boost": True
    }
)

# Save to file
with open("output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### Voice Settings Parameters

| Parameter | Range | Effect |
|-----------|-------|--------|
| stability | 0.0-1.0 | Lower = more expressive, Higher = more consistent |
| similarity_boost | 0.0-1.0 | How closely to match original voice |
| style | 0.0-1.0 | Exaggeration of style (v2 only) |
| use_speaker_boost | bool | Enhance clarity |

### Streaming for Real-Time

```python
from elevenlabs import ElevenLabs, stream

client = ElevenLabs(api_key="your_api_key")

audio_stream = client.text_to_speech.convert_as_stream(
    voice_id="JBFqnCBsd6RMkjVDRZzb",
    model_id="eleven_turbo_v2_5",
    text="Streaming audio for real-time applications.",
    output_format="mp3_44100_128"
)

stream(audio_stream)  # Plays audio as it generates
```

### SSML Support

```xml
<speak>
  <prosody rate="slow" pitch="+2st">
    Texto mais lento e com tom mais alto.
  </prosody>
  <break time="500ms"/>
  <emphasis level="strong">Importante!</emphasis>
</speak>
```

---

## Examples

### E-commerce Product Audio

```python
product_script = """
Apresentamos o Kit Chef Profissional!
Com 12 facas de aco inox alemao e cabo ergonomico de madeira natural.
Garantia de 5 anos. Frete gratis para todo Brasil.
"""

audio = client.text_to_speech.convert(
    voice_id="pNInz6obpgDQGcFmaJgB",  # Adam (warm, professional)
    model_id="eleven_multilingual_v2",
    text=product_script,
    voice_settings={"stability": 0.6, "similarity_boost": 0.8}
)
```

### Course Narration

```python
lesson_content = """
Modulo 3: Estrategias de Precificacao.
Nesta aula, voce vai aprender as tres principais estrategias
que empresas de sucesso usam para definir precos.
"""

audio = client.text_to_speech.convert(
    voice_id="ThT5KcBeYPX3keUQqHPh",  # Dorothy (clear, educational)
    model_id="eleven_multilingual_v2",
    text=lesson_content,
    voice_settings={"stability": 0.7, "similarity_boost": 0.75, "style": 0.2}
)
```

### Emotional Advertisement

```python
emotional_ad = """
Voce ja se sentiu perdido tentando vender online?
A frustração de ver seu produto parado enquanto outros vendem aos montes?
Nós entendemos. E criamos a solução perfeita para você.
"""

audio = client.text_to_speech.convert(
    voice_id="EXAVITQu4vr4xnSDxMaL",  # Sarah (empathetic)
    model_id="eleven_multilingual_v2",
    text=emotional_ad,
    voice_settings={"stability": 0.4, "similarity_boost": 0.7, "style": 0.5}
)
```

---

## When to Use

### Best For
- Production-quality narration (courses, podcasts)
- Emotional content (ads, storytelling)
- Multi-language content (29+ languages)
- Voice cloning projects
- Real-time streaming applications

### Avoid When
- Budget is extremely limited (use edge_tts.md)
- Only need basic English TTS (use openai_tts.md)
- Prototyping/testing phase (use edge_tts.md)

### Pricing Tiers (2025)

| Plan | Characters/mo | Cost | Best For |
|------|--------------|------|----------|
| Free | 10,000 | $0 | Testing |
| Starter | 30,000 | $5 | Hobbyists |
| Creator | 100,000 | $22 | Content creators |
| Pro | 500,000 | $99 | Businesses |
| Scale | 2M+ | $330+ | Enterprise |

---

## Integration Notes

### API Endpoints

```
Base URL: https://api.elevenlabs.io/v1

POST /text-to-speech/{voice_id}           # Standard TTS
POST /text-to-speech/{voice_id}/stream    # Streaming TTS
GET  /voices                              # List voices
POST /voice-generation/generate-voice     # Create voice
GET  /models                              # List models
```

### Rate Limits

| Plan | Requests/min | Concurrent |
|------|-------------|------------|
| Free | 20 | 2 |
| Starter | 60 | 3 |
| Creator | 120 | 5 |
| Pro | 240 | 10 |
| Scale | Custom | Custom |

### Error Handling

```python
from elevenlabs.core.api_error import ApiError

try:
    audio = client.text_to_speech.convert(...)
except ApiError as e:
    if e.status_code == 429:
        # Rate limited - implement backoff
        time.sleep(60)
    elif e.status_code == 401:
        # Invalid API key
        raise ValueError("Check your ELEVENLABS_API_KEY")
```

---

## Cross-References

| Related File | Context |
|--------------|---------|
| elevenlabs_scribe.md | STT companion for same platform |
| openai_tts.md | Alternative for OpenAI ecosystem |
| edge_tts.md | Free fallback option |
| interaction_patterns.md | Voice UX integration |

---

**Quality Score**: 0.85 | **Confidence**: High
**Source**: ElevenLabs Official Documentation (2025)
