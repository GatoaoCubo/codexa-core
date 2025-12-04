<!-- iso_vectorstore -->
<!--
  Source: 20_script_writer_HOP.md
  Agent: video_agent
  Synced: 2025-12-02
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# HOP: Script Writer | video_agent Stage 2

## MODULE_METADATA
```yaml
id: video_agent_script_writer
version: 1.0.0
purpose: Write narration script with timing, text overlays, and music selection
dependencies: [concept.json]
category: video_production
stage: 2
```

## INPUT_CONTRACT
```yaml
required:
  $concept:
    type: object
    source: concept.json
    description: Output from Stage 1 (storyboard)
  $produto:
    type: string
    description: Product name for text overlays
optional:
  $preco:
    type: string
    description: Price for CTA overlay (e.g., "R$ 599")
  $cta_text:
    type: string
    default: "Compre Agora"
    description: Call-to-action text
  $voice:
    type: object
    description: Voice configuration for TTS narration
    default:
      voice_id: "pMsXgVXv3BLzUgSXRplE"
      voice_name: "Camila"
      gender: "feminina"
    schema:
      voice_id: string (ElevenLabs ID)
      voice_name: string (display name)
      gender: enum ["feminina", "masculina"]
      stability: number (0.0-1.0, default 0.5)
      similarity_boost: number (0.0-1.0, default 0.75)
  $video_mode:
    type: string
    enum: ["overlay", "clean"]
    default: "overlay"
    description: |
      - "overlay": Video with text overlays (CTA, product name, benefits)
      - "clean": NO TEXT in video - pure visual with narration only (--NO TEXT mode)
  $music_mood:
    type: string
    enum: ["upbeat", "calm", "dramatic", "neutral"]
    default: "upbeat"
    description: Background music mood
```

## OUTPUT_CONTRACT
```yaml
primary:
  script.json:
    type: object
    structure:
      narration: array[NarrationSegment]
      text_overlays: array[TextOverlay]
      music: MusicConfig
      voice: string
secondary:
  script_summary.md:
    type: markdown
    description: Human-readable script timeline
```

## TASK

**Role**: Video Copywriter

**Objective**: Write concise, impactful narration copy that syncs perfectly with visual timing and maximizes engagement.

**Standards**:
- Narration: 5-10 words per segment (easy TTS)
- Text overlays: CAPS for emphasis, max 6 words (if video_mode="overlay")
- Leave 0.5s buffer between narration and shot transitions
- CTA must include price and action verb

**Constraints**:
- Narration cannot exceed shot duration
- No overlapping narration segments
- Minimum 1 text overlay (CTA) - ONLY if video_mode="overlay"
- If video_mode="clean": NO TEXT OVERLAYS (--NO TEXT mode)
- Portuguese (Brazilian) language

## VOICE LIBRARY PT-BR

### Vozes Femininas (ElevenLabs)
| Voice ID | Nome | Caracteristicas | Uso |
|----------|------|-----------------|-----|
| `pMsXgVXv3BLzUgSXRplE` | **Camila** | Jovem, energetica | Moda, cosmeticos |
| `EXAVITQu4vr4xnSDxMaL` | **Bella** | Suave, sofisticada | Luxo, wellness |
| `XrExE9yKIg1WjnnlVkGX` | **Laura** | Profissional | Tech, servicos |
| `nPczCjzI2devNBz1zQrb` | **Vitoria** | Calorosa | Casa, organicos |

### Vozes Masculinas (ElevenLabs)
| Voice ID | Nome | Caracteristicas | Uso |
|----------|------|-----------------|-----|
| `TX3LPaxmHKxFdv7VOQHJ` | **Rafael** | Grave, autoritativo | Auto, premium |
| `ErXwobaYiN019PkySvjV` | **Antoni** | Dinamico, jovem | Esportes, fitness |
| `VR6AewLTigWG4xSOukaG` | **Eduardo** | Equilibrado | Uso geral |
| `pNInz6obpgDQGcFmaJgB` | **Lucas** | Entusiasmado | Promocoes, CTA |

### Auto-Selecao de Voz
```python
def auto_select_voice(tom, gender_preference=None):
    voice_map = {
        "energetico": {"feminina": "pMsXgVXv3BLzUgSXRplE", "masculina": "ErXwobaYiN019PkySvjV"},
        "sofisticado": {"feminina": "EXAVITQu4vr4xnSDxMaL", "masculina": "TX3LPaxmHKxFdv7VOQHJ"},
        "profissional": {"feminina": "XrExE9yKIg1WjnnlVkGX", "masculina": "VR6AewLTigWG4xSOukaG"},
        "acolhedor": {"feminina": "nPczCjzI2devNBz1zQrb", "masculina": "pNInz6obpgDQGcFmaJgB"}
    }
    gender = gender_preference or "feminina"
    return voice_map.get(tom, voice_map["energetico"])[gender]
```

## VIDEO MODE

### Mode: "overlay" (Default)
- Text overlays rendered on video
- CTA with price visible
- Works in silent autoplay (social feeds)

### Mode: "clean" (--NO TEXT)
- ZERO text in video frame
- All communication via narration (audio)
- Video can be translated (swap audio track)
- Premium/cinematic appearance
- Use platform captions (Instagram, YouTube auto-subtitles)

## STEPS

### Step 1: Analyze Storyboard
```python
shots = $concept["shots"]
total_duration = $concept["total_duration"]

# Calculate cumulative timing
timeline = []
current_time = 0
for shot in shots:
    timeline.append({
        "shot": shot["number"],
        "start": current_time,
        "end": current_time + shot["duration"],
        "narrative": shot["narrative"],
        "description": shot["description"]
    })
    current_time += shot["duration"]
```

### Step 2: Write Narration Segments
```python
narration = []

for segment in timeline:
    # Skip very short shots
    if segment["end"] - segment["start"] < 2:
        continue

    # Generate narration based on narrative role
    if segment["narrative"] == "hook":
        text = generate_hook_copy($produto)
        # Example: "Descubra o que todo mundo quer"
    elif segment["narrative"] == "benefit":
        text = generate_benefit_copy($produto, $objetivo)
        # Example: "Conforto que dura o dia todo"
    elif segment["narrative"] == "cta":
        text = generate_cta_copy($preco, $cta_text)
        # Example: "Garanta o seu por apenas R$ 599"
    else:
        text = generate_build_copy($produto)
        # Example: "Design inovador para você"

    # Add 0.3s buffer at start
    narration.append({
        "start": segment["start"] + 0.3,
        "end": segment["end"] - 0.2,
        "text": text
    })
```

### Step 3: Define Text Overlays
```python
text_overlays = []

# --NO TEXT MODE: Skip all overlays if video_mode="clean"
if $video_mode == "clean":
    text_overlays = []  # ZERO text in video
    # Narration becomes REQUIRED in clean mode
    narration_required = True
else:
    # Mode: "overlay" - Add text overlays

    # Product name (early)
    text_overlays.append({
        "start": 1,
        "end": 4,
        "text": $produto.upper(),
        "position": "bottom",
        "style": "bold"
    })

    # Key benefit (middle)
    if len(shots) >= 4:
        mid_shot = timeline[len(timeline) // 2]
        text_overlays.append({
            "start": mid_shot["start"],
            "end": mid_shot["end"],
            "text": extract_benefit($objetivo).upper(),
            "position": "center",
            "style": "normal"
        })

    # CTA with price (end)
    cta_shot = timeline[-1]
    cta_text = f"{$preco or 'FRETE GRATIS'} | {$cta_text}"
    text_overlays.append({
        "start": cta_shot["start"] + 0.5,
        "end": cta_shot["end"],
        "text": cta_text.upper(),
        "position": "center",
        "style": "bold"
    })
```

### Step 4: Select Music
```python
music_library = {
    "upbeat": {
        "track": "music/upbeat_electronic.mp3",
        "bpm": 128,
        "volume": 0.3
    },
    "calm": {
        "track": "music/calm_acoustic.mp3",
        "bpm": 80,
        "volume": 0.25
    },
    "dramatic": {
        "track": "music/dramatic_cinematic.mp3",
        "bpm": 100,
        "volume": 0.35
    },
    "neutral": {
        "track": "music/neutral_ambient.mp3",
        "bpm": 90,
        "volume": 0.2
    }
}

music = music_library.get($music_mood, music_library["upbeat"])
```

### Step 5: Validate Timing
```python
# Check no overlaps
for i in range(len(narration) - 1):
    current = narration[i]
    next_seg = narration[i + 1]
    assert current["end"] <= next_seg["start"], "Overlapping narration"

# Check doesn't exceed duration
for seg in narration:
    assert seg["end"] <= total_duration, "Narration exceeds video"
```

### Step 6: Output

#### Example A: Mode "overlay" (with text)
```json
{
  "video_mode": "overlay",
  "narration": [
    {
      "start": 0.3,
      "end": 2.8,
      "text": "Conheça o futuro do conforto"
    },
    {
      "start": 5.0,
      "end": 9.0,
      "text": "Nike Air Max com tecnologia revolucionária"
    },
    {
      "start": 26.0,
      "end": 29.5,
      "text": "Garanta o seu por apenas R$ 599"
    }
  ],
  "text_overlays": [
    {
      "start": 1,
      "end": 4,
      "text": "NIKE AIR MAX 2024",
      "position": "bottom",
      "style": "bold"
    },
    {
      "start": 12,
      "end": 16,
      "text": "AMORTECIMENTO AIR",
      "position": "center",
      "style": "normal"
    },
    {
      "start": 26,
      "end": 30,
      "text": "R$ 599 | COMPRE AGORA",
      "position": "center",
      "style": "bold"
    }
  ],
  "music": {
    "track": "music/upbeat_electronic.mp3",
    "volume": 0.3
  },
  "voice": {
    "voice_id": "pMsXgVXv3BLzUgSXRplE",
    "voice_name": "Camila",
    "gender": "feminina",
    "stability": 0.5,
    "similarity_boost": 0.75
  }
}
```

#### Example B: Mode "clean" (--NO TEXT)
```json
{
  "video_mode": "clean",
  "narration": [
    {
      "start": 0.3,
      "end": 3.5,
      "text": "Conheça o futuro do conforto"
    },
    {
      "start": 5.0,
      "end": 10.0,
      "text": "Nike Air Max com tecnologia revolucionária que acompanha seus passos"
    },
    {
      "start": 15.0,
      "end": 20.0,
      "text": "Design inovador para o seu dia a dia"
    },
    {
      "start": 25.0,
      "end": 29.5,
      "text": "Nike Air Max. Just Do It."
    }
  ],
  "text_overlays": [],
  "music": {
    "track": "music/cinematic_orchestral.mp3",
    "volume": 0.25
  },
  "voice": {
    "voice_id": "TX3LPaxmHKxFdv7VOQHJ",
    "voice_name": "Rafael",
    "gender": "masculina",
    "stability": 0.6,
    "similarity_boost": 0.8
  },
  "platform_captions": true
}
```

## VALIDATION

Quality Gates:
- [ ] Narration doesn't exceed video duration
- [ ] No overlapping narration segments
- [ ] If video_mode="overlay": At least 1 text overlay (CTA)
- [ ] If video_mode="clean": text_overlays must be empty []
- [ ] If video_mode="clean": narration REQUIRED (cannot be empty)
- [ ] Each narration segment 5-15 words
- [ ] Music volume <= 0.4 (not overpowering)
- [ ] Voice ID is valid ElevenLabs ID

Thresholds:
- Narration words per segment: 5-15
- Text overlay max words: 6 (mode "overlay" only)
- Music volume: 0.2-0.4
- Voice stability: 0.3-0.7 (recommended)
- Voice similarity_boost: 0.5-0.9 (recommended)

Video Mode Rules:
- "overlay": text_overlays.length >= 1
- "clean": text_overlays.length == 0 AND narration.length >= 2

## CONTEXT

**Usage**: Called by video_agent.py as second pipeline stage

**Upstream**:
- concept.json from Stage 1

**Downstream**:
- script.json -> 05_editing_builder.py (TTS + text overlays)

**$arguments chaining**:
```
script.json.narration -> editing_builder($narration)
script.json.text_overlays -> editing_builder($overlays)
script.json.music -> editing_builder($music)
```

**Assumptions**:
- Concept already validated
- Portuguese (Brazilian) target language
- ElevenLabs voice exists

---

**Version**: 2.0.0
**Created**: 2025-11-24
**Updated**: 2025-11-25
**Builder**: builders/02_script_builder.py
**Changes in 2.0.0**:
- Added: Voice Library PT-BR (8 voices: 4 femininas, 4 masculinas)
- Added: video_mode parameter ("overlay" vs "clean")
- Added: --NO TEXT mode for clean videos
- Added: Auto voice selection by tom
- Updated: Voice object structure (voice_id, voice_name, gender, stability, similarity_boost)
- Updated: Validation rules for video_mode
