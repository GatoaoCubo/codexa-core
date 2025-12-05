# OpenAI TTS | Knowledge Card

**Category**: TTS_PLATFORMS | **Quality Score**: 0.82
**Last Updated**: 2025-12-05 | **Version**: 1.0.0

---

## Executive Summary

OpenAI TTS provides high-quality text-to-speech through two models: `tts-1` (optimized for speed) and `tts-1-hd` (optimized for quality). Integrated natively with OpenAI ecosystem, making it ideal for GPT-powered applications. Supports 6 distinct voices and multiple output formats.

**Key Differentiator**: Native OpenAI integration + simple API + consistent quality

---

## Key Concepts

### Models Available

| Model | Latency | Quality | Cost | Use Case |
|-------|---------|---------|------|----------|
| tts-1 | ~200ms | Good | $15/1M chars | Real-time, streaming |
| tts-1-hd | ~500ms | Excellent | $30/1M chars | Production, podcasts |
| gpt-4o-audio-preview | Varies | Excellent | Token-based | Conversational AI |

### Voice Options (6 Voices)

| Voice | Character | Best For |
|-------|-----------|----------|
| alloy | Neutral, balanced | General purpose |
| echo | Warm, conversational | Podcasts, stories |
| fable | Expressive, dramatic | Narration, audiobooks |
| onyx | Deep, authoritative | Corporate, serious |
| nova | Friendly, youthful | Marketing, tutorials |
| shimmer | Soft, gentle | Meditation, ASMR |

### Supported Languages

Automatically detects and supports: English, Spanish, Portuguese, French, German, Italian, Dutch, Polish, Russian, Chinese, Japanese, Korean, Arabic, Hindi, and 40+ more languages.

**Note**: Best quality in English; other languages may have slight accent variations.

### Output Formats

| Format | Extension | Quality | Size |
|--------|-----------|---------|------|
| mp3 | .mp3 | Good | Small |
| opus | .opus | Excellent | Smallest |
| aac | .aac | Good | Medium |
| flac | .flac | Lossless | Large |
| wav | .wav | Lossless | Largest |
| pcm | raw | Lossless | Raw bytes |

---

## How to Apply

### Basic TTS Request (Python)

```python
from openai import OpenAI

client = OpenAI()

response = client.audio.speech.create(
    model="tts-1",
    voice="nova",
    input="Ola! Bem-vindo ao nosso tutorial de vendas online."
)

response.stream_to_file("output.mp3")
```

### High-Definition Audio

```python
response = client.audio.speech.create(
    model="tts-1-hd",
    voice="onyx",
    input="Apresentamos o relatorio trimestral de resultados.",
    response_format="flac"
)

with open("hd_output.flac", "wb") as f:
    f.write(response.content)
```

### Streaming for Real-Time

```python
from openai import OpenAI

client = OpenAI()

# Stream to file
with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="alloy",
    input="Texto longo que sera transmitido em chunks...",
) as response:
    response.stream_to_file("streamed_output.mp3")
```

### GPT-4o Audio (Conversational)

```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-audio-preview",
    modalities=["text", "audio"],
    audio={"voice": "alloy", "format": "wav"},
    messages=[
        {"role": "user", "content": "Explique o que e marketing digital em 30 segundos."}
    ]
)

# Audio is returned as base64 in response.choices[0].message.audio
audio_data = response.choices[0].message.audio.data
```

---

## Examples

### E-commerce Product Description

```python
product_audio = """
Descubra o Smartphone Galaxy Ultra!
Tela AMOLED de 6.8 polegadas, camera de 200 megapixels,
e bateria que dura 2 dias inteiros.
Parcele em ate 12x sem juros.
"""

response = client.audio.speech.create(
    model="tts-1-hd",
    voice="nova",  # Friendly, engaging
    input=product_audio,
    response_format="mp3"
)
response.stream_to_file("produto_galaxy.mp3")
```

### Course Module Intro

```python
lesson_intro = """
Modulo 5: Otimizacao de Conversao.
Nesta aula voce aprendera tecnicas avancadas para
transformar visitantes em clientes pagantes.
Vamos comecar!
"""

response = client.audio.speech.create(
    model="tts-1-hd",
    voice="echo",  # Warm, educational
    input=lesson_intro,
    response_format="mp3"
)
response.stream_to_file("modulo5_intro.mp3")
```

### Automated Notifications

```python
notification = "Seu pedido foi enviado! Codigo de rastreamento: BR123456789."

response = client.audio.speech.create(
    model="tts-1",  # Fast model for notifications
    voice="alloy",
    input=notification,
    response_format="opus"  # Smallest file size
)
response.stream_to_file("notificacao.opus")
```

---

## When to Use

### Best For
- OpenAI ecosystem integration (GPT apps)
- Simple, reliable TTS needs
- Multi-language content (auto-detection)
- Real-time streaming applications
- Cost-effective production audio

### Avoid When
- Need emotional/expressive voices (use elevenlabs.md)
- Require voice cloning (use elevenlabs.md)
- Budget is zero (use edge_tts.md)
- Need SSML control (limited support)

### Pricing (2025)

| Model | Cost per 1M characters |
|-------|----------------------|
| tts-1 | $15.00 |
| tts-1-hd | $30.00 |

**Example Costs**:
- 1-hour podcast (~90,000 chars): $1.35 (tts-1) / $2.70 (tts-1-hd)
- 10-module course (~300,000 chars): $4.50 (tts-1) / $9.00 (tts-1-hd)

---

## Integration Notes

### API Endpoint

```
POST https://api.openai.com/v1/audio/speech
Authorization: Bearer $OPENAI_API_KEY
Content-Type: application/json

{
  "model": "tts-1",
  "voice": "nova",
  "input": "Your text here",
  "response_format": "mp3"
}
```

### Rate Limits

| Tier | Requests/min | Tokens/min |
|------|-------------|------------|
| Free | 3 | 40,000 |
| Tier 1 | 50 | 500,000 |
| Tier 2 | 100 | 2,000,000 |
| Tier 3+ | 500+ | 10,000,000+ |

### Error Handling

```python
from openai import OpenAI, APIError, RateLimitError

client = OpenAI()

try:
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
except RateLimitError:
    # Implement exponential backoff
    time.sleep(60)
except APIError as e:
    print(f"API error: {e.message}")
```

### Character Limits

| Constraint | Limit |
|------------|-------|
| Max input length | 4,096 characters |
| Recommended chunk | 1,000-2,000 chars |

**For longer text**: Split into paragraphs and concatenate audio files.

---

## Voice Comparison Guide

| Scenario | Recommended Voice | Why |
|----------|-------------------|-----|
| Product ads | nova | Energetic, engaging |
| Course content | echo | Warm, trustworthy |
| Corporate reports | onyx | Authoritative |
| Storytelling | fable | Expressive |
| General purpose | alloy | Balanced |
| Wellness/meditation | shimmer | Calming |

---

## Cross-References

| Related File | Context |
|--------------|---------|
| whisper_api.md | STT companion from OpenAI |
| elevenlabs.md | Premium alternative with more voices |
| edge_tts.md | Free fallback option |
| interaction_patterns.md | Voice UX integration |

---

**Quality Score**: 0.82 | **Confidence**: High
**Source**: OpenAI Official Documentation (2025)
