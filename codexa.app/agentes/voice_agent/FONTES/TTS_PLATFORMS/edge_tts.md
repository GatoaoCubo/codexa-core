# Microsoft Edge TTS | Knowledge Card

**Category**: TTS_PLATFORMS | **Quality Score**: 0.78
**Last Updated**: 2025-12-05 | **Version**: 1.0.0

---

## Executive Summary

Edge TTS is Microsoft's free text-to-speech service accessed through the Edge browser's speech synthesis API. Provides high-quality neural voices in 100+ languages with zero cost. Ideal for prototyping, testing, and budget-conscious production use.

**Key Differentiator**: Completely free + excellent quality + massive language support

---

## Key Concepts

### Access Methods

| Method | Pros | Cons |
|--------|------|------|
| edge-tts (Python) | Easy, CLI support | Unofficial wrapper |
| Azure Cognitive | Official API | Paid service |
| Browser API | Native JS | Browser-only |

### Voice Categories

**Neural Voices**: High-quality, natural-sounding (recommended)
**Standard Voices**: Legacy, robotic (avoid)

### Portuguese (Brazil) Voices

| Voice ID | Name | Gender | Style |
|----------|------|--------|-------|
| pt-BR-FranciscaNeural | Francisca | Female | Warm, clear |
| pt-BR-AntonioNeural | Antonio | Male | Professional |
| pt-BR-BrendaNeural | Brenda | Female | Youthful |
| pt-BR-DonatoNeural | Donato | Male | Mature |
| pt-BR-ElzaNeural | Elza | Female | Friendly |
| pt-BR-FabioNeural | Fabio | Male | Casual |
| pt-BR-GiovannaNeural | Giovanna | Female | Professional |
| pt-BR-HumbertoNeural | Humberto | Male | Authoritative |
| pt-BR-LeilaNeural | Leila | Female | Soft |
| pt-BR-LeticiaNeural | Leticia | Female | Energetic |
| pt-BR-ManuelaNeural | Manuela | Female | Warm |
| pt-BR-NicolauNeural | Nicolau | Male | Friendly |
| pt-BR-ThalitaNeural | Thalita | Female | Young |
| pt-BR-ValerioNeural | Valerio | Male | Deep |
| pt-BR-YaraNeural | Yara | Female | Clear |

### English Voices (Selection)

| Voice ID | Name | Accent | Style |
|----------|------|--------|-------|
| en-US-JennyNeural | Jenny | US | Conversational |
| en-US-GuyNeural | Guy | US | News anchor |
| en-US-AriaNeural | Aria | US | Professional |
| en-GB-SoniaNeural | Sonia | UK | Formal |
| en-AU-NatashaNeural | Natasha | AU | Friendly |

---

## How to Apply

### Installation

```bash
pip install edge-tts
```

### Basic Usage (Python)

```python
import edge_tts
import asyncio

async def generate_audio(text: str, voice: str, output: str):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output)

# Generate Brazilian Portuguese audio
asyncio.run(generate_audio(
    text="Ola! Seja bem-vindo ao nosso canal.",
    voice="pt-BR-FranciscaNeural",
    output="bem_vindo.mp3"
))
```

### Command Line Interface

```bash
# List all available voices
edge-tts --list-voices

# Filter Brazilian Portuguese voices
edge-tts --list-voices | grep pt-BR

# Generate audio file
edge-tts --voice "pt-BR-AntonioNeural" \
         --text "Seu pedido foi confirmado!" \
         --write-media pedido.mp3

# Generate with subtitles
edge-tts --voice "pt-BR-FranciscaNeural" \
         --text "Texto com legendas sincronizadas." \
         --write-media output.mp3 \
         --write-subtitles output.vtt
```

### Streaming Audio

```python
import edge_tts
import asyncio

async def stream_audio(text: str, voice: str):
    communicate = edge_tts.Communicate(text, voice)

    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            # Process audio chunk
            audio_data = chunk["data"]
            yield audio_data
        elif chunk["type"] == "WordBoundary":
            # Word timing for sync
            print(f"Word: {chunk['text']} at {chunk['offset']}ms")

# Use in async context
async def main():
    async for audio in stream_audio("Texto para streaming.", "pt-BR-FranciscaNeural"):
        # Send to audio player or save
        pass

asyncio.run(main())
```

### SSML Support

```python
import edge_tts
import asyncio

ssml_text = """
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="pt-BR">
    <voice name="pt-BR-FranciscaNeural">
        <prosody rate="-10%" pitch="+5%">
            Texto mais lento e com tom mais alto.
        </prosody>
        <break time="500ms"/>
        <emphasis level="strong">Destaque importante!</emphasis>
    </voice>
</speak>
"""

async def generate_ssml():
    communicate = edge_tts.Communicate(ssml_text, voice="pt-BR-FranciscaNeural")
    await communicate.save("ssml_output.mp3")

asyncio.run(generate_ssml())
```

---

## Examples

### E-commerce Notification

```python
import edge_tts
import asyncio

async def product_notification():
    text = """
    Parabens! Sua compra foi aprovada.
    Produto: Kit Gourmet Premium.
    Valor: 299 reais e 90 centavos.
    Previsao de entrega: 5 dias uteis.
    """

    communicate = edge_tts.Communicate(
        text,
        "pt-BR-AntonioNeural"
    )
    await communicate.save("compra_aprovada.mp3")

asyncio.run(product_notification())
```

### Course Module Audio

```python
import edge_tts
import asyncio

async def course_module():
    text = """
    Modulo 2: Fundamentos de Marketing Digital.

    Nesta aula, voce vai aprender os conceitos essenciais
    para criar campanhas de sucesso na internet.

    Vamos abordar tres topicos principais:
    Primeiro, definicao de publico-alvo.
    Segundo, canais de aquisicao.
    Terceiro, metricas de conversao.

    Vamos comecar!
    """

    communicate = edge_tts.Communicate(
        text,
        "pt-BR-FranciscaNeural"  # Clear, educational voice
    )
    await communicate.save("modulo2_intro.mp3")

asyncio.run(course_module())
```

### Batch Processing

```python
import edge_tts
import asyncio
from pathlib import Path

async def batch_generate(texts: list, voice: str, output_dir: str):
    Path(output_dir).mkdir(exist_ok=True)

    for i, text in enumerate(texts):
        communicate = edge_tts.Communicate(text, voice)
        output_path = f"{output_dir}/audio_{i:03d}.mp3"
        await communicate.save(output_path)
        print(f"Generated: {output_path}")

# Generate multiple audios
texts = [
    "Introducao ao curso.",
    "Topico 1: Conceitos basicos.",
    "Topico 2: Aplicacoes praticas.",
    "Conclusao e proximos passos."
]

asyncio.run(batch_generate(texts, "pt-BR-FranciscaNeural", "./audios"))
```

---

## When to Use

### Best For
- Prototyping and testing (zero cost)
- Budget-limited projects
- High-volume content (no API limits)
- Multi-language projects (100+ languages)
- Subtitle generation (VTT sync)
- Offline processing (no API calls in production)

### Avoid When
- Need commercial license clarity (check Microsoft ToS)
- Require voice cloning (use elevenlabs.md)
- Need premium emotional range (use elevenlabs.md)
- Building production SaaS (consider paid APIs)

### Pricing

| Aspect | Cost |
|--------|------|
| API Usage | FREE |
| Character Limits | Unlimited* |
| Commercial Use | Check Microsoft ToS |

*No hard limits, but respect fair use.

---

## Integration Notes

### Voice Selection by Use Case

| Use Case | Recommended Voice | Reason |
|----------|-------------------|--------|
| E-commerce | pt-BR-AntonioNeural | Professional, trustworthy |
| Courses | pt-BR-FranciscaNeural | Clear, warm |
| Notifications | pt-BR-FabioNeural | Casual, quick |
| Corporate | pt-BR-HumbertoNeural | Authoritative |
| Youth content | pt-BR-ThalitaNeural | Young, energetic |

### Output Specifications

| Property | Value |
|----------|-------|
| Format | MP3 (default) |
| Sample Rate | 24kHz |
| Bitrate | 48kbps |
| Channels | Mono |

### Subtitle Generation

```bash
# Generate audio + VTT subtitles
edge-tts --voice "pt-BR-FranciscaNeural" \
         --file input.txt \
         --write-media output.mp3 \
         --write-subtitles output.vtt
```

### Error Handling

```python
import edge_tts
import asyncio

async def safe_generate(text: str, voice: str, output: str):
    try:
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output)
        return True
    except edge_tts.exceptions.NoAudioReceived:
        print("Error: No audio generated. Check text/voice.")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

asyncio.run(safe_generate("Test text", "pt-BR-FranciscaNeural", "test.mp3"))
```

---

## Limitations

| Limitation | Workaround |
|------------|------------|
| No voice cloning | Use ElevenLabs |
| Limited emotional control | Use SSML prosody tags |
| Unofficial Python wrapper | Monitor for updates |
| No real-time WebSocket | Use streaming chunks |
| Microsoft ToS for commercial | Check Azure TTS for clarity |

---

## Cross-References

| Related File | Context |
|--------------|---------|
| elevenlabs.md | Premium alternative |
| openai_tts.md | Official API alternative |
| whisper_api.md | STT companion |
| interaction_patterns.md | Voice UX integration |

---

**Quality Score**: 0.78 | **Confidence**: High
**Source**: edge-tts Python package documentation + Microsoft Azure Cognitive Services
