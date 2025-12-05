# OpenAI Whisper API | Knowledge Card

**Category**: STT_PLATFORMS | **Quality Score**: 0.85
**Last Updated**: 2025-12-05 | **Version**: 1.0.0

---

## Executive Summary

OpenAI Whisper is the industry-standard speech-to-text API offering exceptional accuracy across 99+ languages. Available as both an API service and open-source model. Handles accents, background noise, and technical vocabulary with remarkable precision.

**Key Differentiator**: Best-in-class accuracy + multilingual + timestamp support

---

## Key Concepts

### Models Available

| Model | Context | Speed | Accuracy | Use Case |
|-------|---------|-------|----------|----------|
| whisper-1 | 25MB/file | Fast | Excellent | API (recommended) |
| whisper-large-v3 | Unlimited | Slower | Best | Self-hosted |
| whisper-large-v3-turbo | Unlimited | Fast | Excellent | Self-hosted speed |

### Supported Formats

| Format | Extension | Max Size |
|--------|-----------|----------|
| MP3 | .mp3 | 25 MB |
| MP4 | .mp4 | 25 MB |
| MPEG | .mpeg | 25 MB |
| MPGA | .mpga | 25 MB |
| M4A | .m4a | 25 MB |
| WAV | .wav | 25 MB |
| WebM | .webm | 25 MB |

### Language Support (99+ Languages)

**Primary**: English, Spanish, Portuguese, French, German, Italian, Japanese, Korean, Chinese
**Full List**: Afrikaans, Arabic, Armenian, Azerbaijani, Belarusian, Bosnian, Bulgarian, Catalan, Croatian, Czech, Danish, Dutch, Estonian, Finnish, Galician, Greek, Hebrew, Hindi, Hungarian, Icelandic, Indonesian, Kannada, Kazakh, Latvian, Lithuanian, Macedonian, Malay, Marathi, Maori, Nepali, Norwegian, Persian, Polish, Romanian, Russian, Serbian, Slovak, Slovenian, Swahili, Swedish, Tagalog, Tamil, Thai, Turkish, Ukrainian, Urdu, Vietnamese, Welsh, and more.

### Response Formats

| Format | Description | Use Case |
|--------|-------------|----------|
| json | Plain JSON with text | Simple transcription |
| verbose_json | JSON with timestamps, confidence | Subtitles, analysis |
| text | Plain text only | Basic extraction |
| srt | SubRip subtitle format | Video subtitles |
| vtt | WebVTT subtitle format | Web video subtitles |

---

## How to Apply

### Basic Transcription (Python)

```python
from openai import OpenAI

client = OpenAI()

with open("audio.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

print(transcript.text)
```

### With Language Hint

```python
# Improve accuracy by specifying language
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    language="pt"  # Portuguese
)
```

### Verbose Output with Timestamps

```python
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="verbose_json",
    timestamp_granularities=["word", "segment"]
)

# Access segments
for segment in transcript.segments:
    print(f"[{segment.start:.2f}s - {segment.end:.2f}s]: {segment.text}")

# Access word-level timestamps
for word in transcript.words:
    print(f"{word.word} ({word.start:.2f}s)")
```

### Generate Subtitles (SRT)

```python
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    response_format="srt"
)

# Save as .srt file
with open("subtitles.srt", "w", encoding="utf-8") as f:
    f.write(transcript)
```

### Translation to English

```python
# Translate any language to English
translation = client.audio.translations.create(
    model="whisper-1",
    file=audio_file
)

print(translation.text)  # Always in English
```

### Custom Prompt for Context

```python
# Provide context for better accuracy
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file,
    prompt="This is a marketing course about e-commerce and digital sales strategies."
)
```

---

## Examples

### Course Audio Transcription

```python
from openai import OpenAI
from pathlib import Path

client = OpenAI()

def transcribe_course_module(audio_path: str, output_dir: str):
    """Transcribe course audio with timestamps for navigation."""

    with open(audio_path, "rb") as audio:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
            language="pt",
            prompt="Curso de marketing digital. Termos: ROI, CPA, LTV, funil de vendas."
        )

    # Save transcript
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Full text
    with open(output_path / "transcript.txt", "w", encoding="utf-8") as f:
        f.write(result.text)

    # Chapters/segments
    with open(output_path / "chapters.md", "w", encoding="utf-8") as f:
        for i, seg in enumerate(result.segments):
            minutes = int(seg.start // 60)
            seconds = int(seg.start % 60)
            f.write(f"- [{minutes:02d}:{seconds:02d}] {seg.text.strip()}\n")

    return result

# Usage
transcribe_course_module("modulo1.mp3", "./transcripts/modulo1/")
```

### Meeting Notes Extraction

```python
def transcribe_meeting(audio_path: str) -> dict:
    """Extract meeting transcript with speaker-aware segments."""

    with open(audio_path, "rb") as audio:
        result = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
            prompt="Business meeting. Participants discussing project updates and deadlines."
        )

    return {
        "full_text": result.text,
        "duration_seconds": result.duration,
        "segments": [
            {
                "start": seg.start,
                "end": seg.end,
                "text": seg.text.strip()
            }
            for seg in result.segments
        ]
    }
```

### Video Subtitle Generation

```python
def generate_subtitles(audio_path: str, format: str = "srt") -> str:
    """Generate subtitles from audio for video content."""

    with open(audio_path, "rb") as audio:
        subtitles = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio,
            response_format=format,  # "srt" or "vtt"
            language="pt"
        )

    return subtitles

# Generate SRT for YouTube
srt_content = generate_subtitles("video_audio.mp3", "srt")
with open("video_subtitles.srt", "w", encoding="utf-8") as f:
    f.write(srt_content)

# Generate VTT for web
vtt_content = generate_subtitles("video_audio.mp3", "vtt")
with open("video_subtitles.vtt", "w", encoding="utf-8") as f:
    f.write(vtt_content)
```

---

## When to Use

### Best For
- High-accuracy transcription (courses, podcasts)
- Multi-language content (99+ languages)
- Subtitle generation (SRT/VTT)
- Translation to English
- Technical vocabulary (with prompt hints)
- Word-level timestamps (karaoke, sync)

### Avoid When
- Real-time streaming (use ElevenLabs Scribe)
- Files > 25MB (split or use self-hosted)
- Need speaker diarization (use specialized tools)
- Zero budget (use local Whisper)

### Pricing (2025)

| Usage | Cost |
|-------|------|
| Transcription | $0.006 / minute |
| Translation | $0.006 / minute |

**Example Costs**:
- 1-hour podcast: $0.36
- 10-hour course: $3.60
- 100 hours/month: $36.00

---

## Integration Notes

### API Endpoint

```
POST https://api.openai.com/v1/audio/transcriptions
Authorization: Bearer $OPENAI_API_KEY
Content-Type: multipart/form-data

file: (binary)
model: whisper-1
language: pt (optional)
response_format: json (optional)
prompt: context hint (optional)
```

### File Size Handling

```python
from pydub import AudioSegment
import math

def split_audio(file_path: str, max_size_mb: int = 24) -> list:
    """Split large audio files for Whisper API."""

    audio = AudioSegment.from_file(file_path)
    file_size_mb = len(audio.raw_data) / (1024 * 1024)

    if file_size_mb <= max_size_mb:
        return [file_path]

    # Calculate chunks
    num_chunks = math.ceil(file_size_mb / max_size_mb)
    chunk_duration = len(audio) // num_chunks

    chunks = []
    for i in range(num_chunks):
        start = i * chunk_duration
        end = min((i + 1) * chunk_duration, len(audio))
        chunk = audio[start:end]

        chunk_path = f"{file_path}_chunk_{i}.mp3"
        chunk.export(chunk_path, format="mp3")
        chunks.append(chunk_path)

    return chunks
```

### Error Handling

```python
from openai import OpenAI, APIError, RateLimitError

client = OpenAI()

def safe_transcribe(audio_path: str) -> str:
    try:
        with open(audio_path, "rb") as audio:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio
            )
        return result.text

    except RateLimitError:
        print("Rate limited. Waiting 60s...")
        time.sleep(60)
        return safe_transcribe(audio_path)  # Retry

    except APIError as e:
        if "file is too large" in str(e).lower():
            print("File too large. Split required.")
            return None
        raise
```

### Quality Enhancement Tips

| Tip | Implementation |
|-----|----------------|
| Specify language | `language="pt"` |
| Add context prompt | `prompt="Technical terms: API, SDK, OAuth"` |
| Use higher quality audio | 16kHz+ sample rate |
| Reduce background noise | Pre-process with noise reduction |

---

## Cross-References

| Related File | Context |
|--------------|---------|
| openai_tts.md | TTS companion from OpenAI |
| elevenlabs_scribe.md | Real-time STT alternative |
| elevenlabs.md | TTS with same ecosystem |
| interaction_patterns.md | Voice UX integration |

---

**Quality Score**: 0.85 | **Confidence**: High
**Source**: OpenAI Official Documentation (2025)
