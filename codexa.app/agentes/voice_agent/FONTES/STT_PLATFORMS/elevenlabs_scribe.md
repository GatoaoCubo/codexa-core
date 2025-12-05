# ElevenLabs Scribe | Knowledge Card

**Category**: STT_PLATFORMS | **Quality Score**: 0.80
**Last Updated**: 2025-12-05 | **Version**: 1.0.0

---

## Executive Summary

ElevenLabs Scribe is a speech-to-text service optimized for low-latency, real-time transcription. Part of the ElevenLabs ecosystem, it provides fast turnaround with good accuracy, making it ideal for conversational AI and live applications.

**Key Differentiator**: Ultra-low latency (~200ms) + ElevenLabs ecosystem integration

---

## Key Concepts

### Model Overview

| Aspect | Specification |
|--------|---------------|
| Model | scribe_v1 |
| Latency | ~200ms |
| Languages | 32+ |
| Max Duration | 2 hours |
| Max File Size | 1 GB |
| Accuracy | Word Error Rate ~8-12% |

### Supported Languages

**Primary (Best Quality)**: English, Spanish, Portuguese, French, German, Italian, Dutch, Polish, Russian

**Extended**: Japanese, Korean, Chinese (Mandarin), Arabic, Hindi, Turkish, Swedish, Norwegian, Danish, Finnish, Czech, Greek, Hungarian, Romanian, Bulgarian, Croatian, Slovak, Slovenian, Ukrainian, Vietnamese, Indonesian, Thai

### Supported Formats

| Format | Support |
|--------|---------|
| MP3 | Yes |
| WAV | Yes |
| M4A | Yes |
| WEBM | Yes |
| MP4 (audio) | Yes |
| OGG | Yes |
| FLAC | Yes |

### Output Features

| Feature | Description |
|---------|-------------|
| Text | Plain transcription |
| Word timestamps | Start/end per word |
| Confidence scores | Per-word confidence |
| Language detection | Auto-detect spoken language |
| Speaker labels | Basic diarization (beta) |

---

## How to Apply

### Basic Transcription (Python)

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="your_api_key")

with open("audio.mp3", "rb") as audio_file:
    result = client.speech_to_text.convert(
        file=audio_file,
        model_id="scribe_v1"
    )

print(result.text)
```

### With Language Specification

```python
result = client.speech_to_text.convert(
    file=audio_file,
    model_id="scribe_v1",
    language_code="pt"  # Portuguese
)
```

### Get Word Timestamps

```python
result = client.speech_to_text.convert(
    file=audio_file,
    model_id="scribe_v1",
    timestamps=True
)

# Access word-level data
for word in result.words:
    print(f"{word.text}: {word.start_time}s - {word.end_time}s (conf: {word.confidence})")
```

### Streaming Transcription (WebSocket)

```python
import asyncio
import websockets
import json
import base64

async def stream_transcribe(audio_chunks):
    """Real-time transcription via WebSocket."""

    uri = "wss://api.elevenlabs.io/v1/speech-to-text/stream"
    headers = {"xi-api-key": "your_api_key"}

    async with websockets.connect(uri, extra_headers=headers) as ws:
        # Send config
        await ws.send(json.dumps({
            "model_id": "scribe_v1",
            "language_code": "pt"
        }))

        # Stream audio chunks
        for chunk in audio_chunks:
            await ws.send(json.dumps({
                "audio": base64.b64encode(chunk).decode()
            }))

            # Receive partial results
            response = await ws.recv()
            result = json.loads(response)
            if result.get("text"):
                print(f"Partial: {result['text']}")

        # Signal end
        await ws.send(json.dumps({"end": True}))

        # Final result
        final = await ws.recv()
        return json.loads(final)
```

---

## Examples

### Voice Command Processing

```python
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="your_api_key")

def process_voice_command(audio_path: str) -> dict:
    """Fast transcription for voice commands."""

    with open(audio_path, "rb") as audio:
        result = client.speech_to_text.convert(
            file=audio,
            model_id="scribe_v1",
            language_code="pt"
        )

    text = result.text.lower().strip()

    # Parse common commands
    commands = {
        "proximo": "next",
        "anterior": "previous",
        "pausar": "pause",
        "continuar": "play",
        "repetir": "repeat",
        "ajuda": "help"
    }

    for keyword, action in commands.items():
        if keyword in text:
            return {"action": action, "raw_text": text}

    return {"action": "unknown", "raw_text": text}

# Usage
command = process_voice_command("user_command.wav")
print(f"Action: {command['action']}")
```

### Conversation Transcription

```python
def transcribe_conversation(audio_path: str) -> list:
    """Transcribe with word timestamps for conversation analysis."""

    with open(audio_path, "rb") as audio:
        result = client.speech_to_text.convert(
            file=audio,
            model_id="scribe_v1",
            timestamps=True
        )

    # Group into sentences by pauses
    sentences = []
    current_sentence = []
    last_end = 0

    for word in result.words:
        # New sentence if pause > 1 second
        if word.start_time - last_end > 1.0 and current_sentence:
            sentences.append({
                "text": " ".join([w.text for w in current_sentence]),
                "start": current_sentence[0].start_time,
                "end": last_end
            })
            current_sentence = []

        current_sentence.append(word)
        last_end = word.end_time

    # Add final sentence
    if current_sentence:
        sentences.append({
            "text": " ".join([w.text for w in current_sentence]),
            "start": current_sentence[0].start_time,
            "end": last_end
        })

    return sentences
```

### Real-Time Voice Assistant

```python
import asyncio
from elevenlabs import ElevenLabs

client = ElevenLabs(api_key="your_api_key")

async def voice_assistant_loop():
    """Continuous listening and response loop."""

    while True:
        # Record audio (pseudo-code)
        audio_chunk = await record_audio(duration=5)

        if audio_chunk:
            # Transcribe
            with open("temp_audio.wav", "wb") as f:
                f.write(audio_chunk)

            result = client.speech_to_text.convert(
                file=open("temp_audio.wav", "rb"),
                model_id="scribe_v1"
            )

            user_text = result.text.strip()

            if user_text:
                print(f"User: {user_text}")

                # Process and respond
                response = await process_query(user_text)

                # Speak response (using ElevenLabs TTS)
                audio = client.text_to_speech.convert(
                    voice_id="JBFqnCBsd6RMkjVDRZzb",
                    model_id="eleven_multilingual_v2",
                    text=response
                )

                await play_audio(audio)
```

---

## When to Use

### Best For
- Real-time transcription (~200ms latency)
- Voice commands and assistants
- ElevenLabs TTS + STT integration
- Conversational AI applications
- Live captioning

### Avoid When
- Need highest accuracy (use Whisper API)
- Processing long-form content (use Whisper)
- Need advanced speaker diarization
- Budget is zero (use local Whisper)
- Need 100+ language support

### Pricing (2025)

| Usage | Cost |
|-------|------|
| Transcription | ~$0.01 / minute |
| Included in plans | Varies by tier |

**Note**: Check current ElevenLabs pricing as it may change.

---

## Integration Notes

### API Endpoint

```
POST https://api.elevenlabs.io/v1/speech-to-text
xi-api-key: your_api_key
Content-Type: multipart/form-data

file: (binary audio)
model_id: scribe_v1
language_code: pt (optional)
timestamps: true (optional)
```

### WebSocket Endpoint (Streaming)

```
WSS wss://api.elevenlabs.io/v1/speech-to-text/stream
Headers: xi-api-key: your_api_key
```

### Comparison with Whisper

| Aspect | ElevenLabs Scribe | OpenAI Whisper |
|--------|-------------------|----------------|
| Latency | ~200ms | ~1-2s |
| Accuracy | Good (8-12% WER) | Excellent (5-8% WER) |
| Languages | 32+ | 99+ |
| Max file | 1 GB | 25 MB |
| Streaming | Yes | No |
| Cost | ~$0.01/min | $0.006/min |
| Best for | Real-time | Batch processing |

### Error Handling

```python
from elevenlabs import ElevenLabs
from elevenlabs.core.api_error import ApiError

client = ElevenLabs(api_key="your_api_key")

def safe_transcribe(audio_path: str) -> str:
    try:
        with open(audio_path, "rb") as audio:
            result = client.speech_to_text.convert(
                file=audio,
                model_id="scribe_v1"
            )
        return result.text

    except ApiError as e:
        if e.status_code == 429:
            print("Rate limited. Retrying...")
            time.sleep(30)
            return safe_transcribe(audio_path)
        elif e.status_code == 401:
            raise ValueError("Invalid API key")
        else:
            print(f"API error: {e}")
            return None
```

---

## Best Practices

| Practice | Implementation |
|----------|----------------|
| Specify language | Always set `language_code` for better accuracy |
| Use timestamps | Enable for any sync/UI needs |
| Handle silence | Filter out empty results |
| Chunk long audio | Process in 30-60 second chunks for streaming |
| Fallback to Whisper | For accuracy-critical tasks |

---

## Cross-References

| Related File | Context |
|--------------|---------|
| elevenlabs.md | TTS companion in same ecosystem |
| whisper_api.md | Higher-accuracy alternative |
| openai_tts.md | Alternative TTS platform |
| interaction_patterns.md | Voice UX integration |

---

**Quality Score**: 0.80 | **Confidence**: Medium-High
**Source**: ElevenLabs Documentation (2025)
