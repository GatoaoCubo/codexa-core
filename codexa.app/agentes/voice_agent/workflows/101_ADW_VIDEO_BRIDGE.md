# 101_ADW_VIDEO_BRIDGE

**ID**: 101_ADW_VIDEO_BRIDGE
**Version**: 1.0.0
**Type**: ADW (Bridge Workflow)
**Chain**: video_agent → voice_agent

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "adw_video_bridge",
  "workflow_name": "Video to Voice Bridge",
  "agent": "voice_agent",
  "version": "1.0.0",
  "type": "bridge",
  "chain": "video_agent → voice_agent",
  "context_strategy": "isolated",
  "failure_handling": "stop_and_report",
  "min_llm_model": "claude-sonnet-4-20250514",
  "required_capabilities": {
    "scout_mcp": true,
    "file_parsing": true,
    "json_extraction": true,
    "tts_production": true
  },
  "quality_threshold": 7.0,
  "estimated_duration": "2-3 minutes",
  "phases": ["LOCATE", "EXTRACT", "VALIDATE", "HANDOFF"]
}
```

---

## PURPOSE

Bridges video script output from `video_agent` to `voice_agent` input, transforming video narration into voice-over production specs with timing marks, intonation hints, pronunciation guides, and TTS configuration.

---

## INPUT_CONTRACT

From `video_agent`:
- `$video_script`: Path to video script output (outputs/*.llm.json or script.json)

Expected video script data:
```json
{
  "script": {
    "video_mode": "overlay|clean",
    "narration": [
      {
        "start": 0.3,
        "end": 2.8,
        "text": "Conheça o futuro do conforto"
      }
    ],
    "voice": {
      "voice_id": "pMsXgVXv3BLzUgSXRplE",
      "voice_name": "Camila",
      "gender": "feminina",
      "stability": 0.5,
      "similarity_boost": 0.75
    },
    "text_overlays": [],
    "music": {
      "track": "music/upbeat.mp3",
      "volume": 0.3
    }
  },
  "storyboard": {
    "shots": [
      {
        "number": 1,
        "duration": 4,
        "description": "Close-up do tênis",
        "narrative": "hook"
      }
    ],
    "total_duration": 30
  },
  "metadata": {
    "produto": "Nike Air Max",
    "duration": 30,
    "shots": 6,
    "quality_score": 8.5
  }
}
```

---

## PHASES

### Phase 1: LOCATE (30s)

Discover video script for target video.

```bash
# Using Scout
mcp__scout__discover("video script for [video_name]")

# OR direct glob
Glob: codexa.app/agentes/video_agent/outputs/*[video_name]*.llm.json
```

**Output**: `$script_paths` (list of matching files)

**Validation**:
- [ ] At least 1 script file found
- [ ] File is readable JSON
- [ ] Contains required fields: script.narration, script.voice

---

### Phase 2: EXTRACT (1min)

Parse video script and map to voice production context.

#### 2.1: Extract Narration Segments

```python
# Map video narration to voice segments
VIDEO_TO_VOICE = {
    "narration[].text": "voice_segments[].text",
    "narration[].start": "voice_segments[].timing.start",
    "narration[].end": "voice_segments[].timing.end",
    "storyboard.shots[].narrative": "voice_segments[].emotion_tag"
}

voice_segments = []
for i, narration in enumerate($script["narration"]):
    # Find corresponding shot
    shot = find_shot_by_time($storyboard, narration["start"])

    # Determine intonation from narrative role
    intonation = map_narrative_to_intonation(shot["narrative"])

    segment = {
        "segment_id": i + 1,
        "text": narration["text"],
        "timing": {
            "start": narration["start"],
            "end": narration["end"],
            "duration": narration["end"] - narration["start"]
        },
        "intonation": intonation,
        "emotion_tag": shot["narrative"],
        "scene_context": shot["description"]
    }
    voice_segments.append(segment)
```

#### 2.2: Map Scene Timing to Audio Timing

```python
# Convert video timeline to audio production timeline
audio_timeline = []
for shot in $storyboard["shots"]:
    audio_timeline.append({
        "shot_number": shot["number"],
        "start_time": shot["start"],
        "end_time": shot["end"],
        "visual_context": shot["description"],
        "narrative_role": shot["narrative"],
        "required_pauses": calculate_breath_marks(shot)
    })
```

#### 2.3: Extract Intonation Hints

```python
# Map narrative roles to TTS intonation patterns
NARRATIVE_TO_INTONATION = {
    "hook": {
        "tone": "excited",
        "emphasis": "high",
        "speed": 1.1,
        "pitch_shift": "+5%",
        "description": "Energetic, attention-grabbing"
    },
    "build": {
        "tone": "engaging",
        "emphasis": "medium",
        "speed": 1.0,
        "pitch_shift": "0%",
        "description": "Conversational, building interest"
    },
    "benefit": {
        "tone": "confident",
        "emphasis": "medium-high",
        "speed": 0.95,
        "pitch_shift": "+2%",
        "description": "Assured, highlighting value"
    },
    "proof": {
        "tone": "credible",
        "emphasis": "medium",
        "speed": 0.9,
        "pitch_shift": "0%",
        "description": "Authoritative, trustworthy"
    },
    "transformation": {
        "tone": "inspirational",
        "emphasis": "high",
        "speed": 0.95,
        "pitch_shift": "+3%",
        "description": "Uplifting, aspirational"
    },
    "cta": {
        "tone": "urgent",
        "emphasis": "high",
        "speed": 1.05,
        "pitch_shift": "+8%",
        "description": "Direct, action-oriented"
    }
}

for segment in voice_segments:
    segment["intonation_hints"] = NARRATIVE_TO_INTONATION[segment["emotion_tag"]]
```

#### 2.4: Add Pronunciation Guides

```python
# Detect technical terms and add pronunciation
PRONUNCIATION_DICT = {
    "Nike": "NAI-kee (emphasis on first syllable)",
    "Air Max": "AIR MAX (distinct separation, emphasis on MAX)",
    "LED": "L-E-D (spell out letters)",
    "USB-C": "U-S-B C (spell out, pause before C)",
    "5G": "CINCO-GÊ (Brazilian pronunciation)",
    "Bluetooth": "BLU-tuth (avoid 'blue-tooth')",
    "Wi-Fi": "UAI-FAI (English pronunciation common in BR)"
}

for segment in voice_segments:
    segment["pronunciation_notes"] = []
    for term, guide in PRONUNCIATION_DICT.items():
        if term.lower() in segment["text"].lower():
            segment["pronunciation_notes"].append({
                "term": term,
                "guide": guide
            })
```

#### 2.5: Calculate Breath Marks

```python
# Add natural pause markers for TTS breathing
def calculate_breath_marks(voice_segments):
    breath_marks = []
    for i, segment in enumerate(voice_segments):
        # Add pause after segment if gap exists
        if i < len(voice_segments) - 1:
            next_segment = voice_segments[i + 1]
            gap = next_segment["timing"]["start"] - segment["timing"]["end"]

            if gap >= 1.0:
                breath_marks.append({
                    "position": segment["timing"]["end"],
                    "type": "breath",
                    "duration": min(gap, 1.5),
                    "note": "Natural pause between scenes"
                })
            elif gap >= 0.5:
                breath_marks.append({
                    "position": segment["timing"]["end"],
                    "type": "micro_pause",
                    "duration": gap,
                    "note": "Quick breath"
                })
    return breath_marks
```

#### 2.6: Extract Voice Configuration

```python
# Map video voice config to TTS production config
voice_config = {
    "provider": "elevenlabs",
    "voice_id": $script["voice"]["voice_id"],
    "voice_name": $script["voice"]["voice_name"],
    "gender": $script["voice"]["gender"],
    "model_id": "eleven_multilingual_v2",
    "settings": {
        "stability": $script["voice"].get("stability", 0.5),
        "similarity_boost": $script["voice"].get("similarity_boost", 0.75),
        "style": 0.0,
        "use_speaker_boost": True
    },
    "output_format": "mp3_44100_128",
    "optimize_streaming_latency": 0
}
```

**Output**: `$voice_context` (structured JSON with segments, timing, intonation, pronunciation)

---

### Phase 3: VALIDATE (30s)

Check data completeness and quality before handoff.

```markdown
## Validation Checklist
- [ ] voice_segments has ≥1 item
- [ ] All segments have timing.start and timing.end
- [ ] No overlapping segments (segment[i].end <= segment[i+1].start)
- [ ] Total duration matches video duration ±0.5s
- [ ] voice_id is valid ElevenLabs ID
- [ ] All intonation hints defined
- [ ] Pronunciation guides added for technical terms
- [ ] Breath marks calculated
- [ ] Quality score ≥7.0/10
```

**Validation Rules**:

```python
def validate_voice_context(voice_context):
    errors = []
    warnings = []

    # Check segments exist
    if len(voice_context["segments"]) == 0:
        errors.append("No voice segments found")

    # Check timing
    for i, segment in enumerate(voice_context["segments"]):
        if segment["timing"]["start"] >= segment["timing"]["end"]:
            errors.append(f"Segment {i+1}: Invalid timing")

        # Check overlap
        if i < len(voice_context["segments"]) - 1:
            next_seg = voice_context["segments"][i + 1]
            if segment["timing"]["end"] > next_seg["timing"]["start"]:
                errors.append(f"Segments {i+1} and {i+2} overlap")

    # Check voice config
    valid_voices = [
        "pMsXgVXv3BLzUgSXRplE", "EXAVITQu4vr4xnSDxMaL",
        "XrExE9yKIg1WjnnlVkGX", "nPczCjzI2devNBz1zQrb",
        "TX3LPaxmHKxFdv7VOQHJ", "ErXwobaYiN019PkySvjV",
        "VR6AewLTigWG4xSOukaG", "pNInz6obpgDQGcFmaJgB"
    ]
    if voice_context["voice_config"]["voice_id"] not in valid_voices:
        warnings.append("Voice ID not in standard library")

    # Check intonation hints
    for segment in voice_context["segments"]:
        if not segment.get("intonation_hints"):
            warnings.append(f"Segment {segment['segment_id']}: Missing intonation hints")

    # Calculate quality score
    score = 10.0
    score -= len(errors) * 2.0
    score -= len(warnings) * 0.5

    return {
        "passed": len(errors) == 0,
        "score": max(0, score),
        "errors": errors,
        "warnings": warnings
    }
```

**Output**: `$validation_result` (pass/fail + score)

---

### Phase 4: HANDOFF (30s)

Prepare context for voice_agent TTS production.

```handoff
contexto: Video script processed for [video_name]
arquivos_gerados:
  - voice_production_context.json
proximo: Run voice_agent TTS production with timing specs
dados:
  segments: $voice_context.segments (count: [X])
  total_duration: [X]s
  voice: {voice_name} ({gender})
  intonation_hints: complete
  pronunciation_guides: [X] terms
  breath_marks: [X] pauses
  music_background: {track} (vol: {volume})
qualidade: $validation_result.score/10
```

**Handoff Block Structure**:

```json
{
  "handoff": {
    "from_agent": "video_agent",
    "to_agent": "voice_agent",
    "timestamp": "2025-12-03T10:30:00Z",
    "video_source": "outputs/nike_air_max_30s.mp4",
    "script_source": "outputs/nike_air_max_30s.llm.json"
  },
  "voice_production": {
    "segments": [...],
    "voice_config": {...},
    "timing_specs": {...},
    "intonation_map": {...},
    "pronunciation_guides": [...],
    "breath_marks": [...],
    "background_music": {...}
  },
  "metadata": {
    "total_segments": 5,
    "total_duration": 30.0,
    "language": "pt-BR",
    "quality_score": 8.5
  }
}
```

---

## OUTPUT_CONTRACT

- `$handoff_block`: Formatted handoff for voice_agent
- `$voice_context`: Complete voice production context JSON
- `voice_production_context.json`: Saved context file

**Output Structure**:

```json
{
  "voice_production_context": {
    "version": "1.0.0",
    "created_at": "2025-12-03T10:30:00Z",
    "source_video": "outputs/nike_air_max_30s.mp4",
    "source_script": "outputs/nike_air_max_30s.llm.json",
    "segments": [
      {
        "segment_id": 1,
        "text": "Conheça o futuro do conforto",
        "timing": {
          "start": 0.3,
          "end": 2.8,
          "duration": 2.5
        },
        "intonation_hints": {
          "tone": "excited",
          "emphasis": "high",
          "speed": 1.1,
          "pitch_shift": "+5%",
          "description": "Energetic, attention-grabbing"
        },
        "emotion_tag": "hook",
        "scene_context": "Close-up do tênis girando 360°",
        "pronunciation_notes": []
      },
      {
        "segment_id": 2,
        "text": "Nike Air Max com tecnologia revolucionária",
        "timing": {
          "start": 5.0,
          "end": 9.0,
          "duration": 4.0
        },
        "intonation_hints": {
          "tone": "confident",
          "emphasis": "medium-high",
          "speed": 0.95,
          "pitch_shift": "+2%",
          "description": "Assured, highlighting value"
        },
        "emotion_tag": "benefit",
        "scene_context": "Zoom in no logo Nike",
        "pronunciation_notes": [
          {
            "term": "Nike",
            "guide": "NAI-kee (emphasis on first syllable)"
          },
          {
            "term": "Air Max",
            "guide": "AIR MAX (distinct separation, emphasis on MAX)"
          }
        ]
      },
      {
        "segment_id": 3,
        "text": "Garanta o seu por apenas R$ 599",
        "timing": {
          "start": 26.0,
          "end": 29.5,
          "duration": 3.5
        },
        "intonation_hints": {
          "tone": "urgent",
          "emphasis": "high",
          "speed": 1.05,
          "pitch_shift": "+8%",
          "description": "Direct, action-oriented"
        },
        "emotion_tag": "cta",
        "scene_context": "Product + price overlay",
        "pronunciation_notes": []
      }
    ],
    "breath_marks": [
      {
        "position": 2.8,
        "type": "breath",
        "duration": 1.2,
        "note": "Natural pause between scenes"
      },
      {
        "position": 9.0,
        "type": "breath",
        "duration": 1.0,
        "note": "Natural pause between scenes"
      }
    ],
    "voice_config": {
      "provider": "elevenlabs",
      "voice_id": "pMsXgVXv3BLzUgSXRplE",
      "voice_name": "Camila",
      "gender": "feminina",
      "model_id": "eleven_multilingual_v2",
      "settings": {
        "stability": 0.5,
        "similarity_boost": 0.75,
        "style": 0.0,
        "use_speaker_boost": true
      },
      "output_format": "mp3_44100_128",
      "optimize_streaming_latency": 0
    },
    "background_music": {
      "track": "music/upbeat_electronic.mp3",
      "volume": 0.3,
      "fade_in": 1.0,
      "fade_out": 2.0,
      "mix_with_voice": true
    },
    "metadata": {
      "total_segments": 3,
      "total_duration": 30.0,
      "language": "pt-BR",
      "video_mode": "overlay",
      "quality_score": 8.5
    }
  }
}
```

---

## TRIGGERS

### Manual
```bash
/flow do "bridge video to voice for [video_name]"
```

### Automatic (after video script generated)
```bash
# In video_agent workflow completion:
NEXT_WORKFLOW: 101_ADW_VIDEO_BRIDGE
```

### Via Spawn
```bash
/spawn
1. explore: find video script for [video_name]
2. review: validate script completeness
3. build: execute 101_ADW_VIDEO_BRIDGE
```

---

## EXAMPLE

### Input (video script excerpt)

```json
{
  "script": {
    "video_mode": "overlay",
    "narration": [
      {"start": 0.3, "end": 2.8, "text": "Descubra o poder da tecnologia"},
      {"start": 5.0, "end": 9.0, "text": "Samsung Galaxy S24 com IA integrada"},
      {"start": 26.0, "end": 29.5, "text": "Por apenas R$ 3.499"}
    ],
    "voice": {
      "voice_id": "XrExE9yKIg1WjnnlVkGX",
      "voice_name": "Laura",
      "gender": "feminina",
      "stability": 0.5,
      "similarity_boost": 0.75
    }
  },
  "storyboard": {
    "shots": [
      {"number": 1, "duration": 4, "description": "Phone emerging from darkness", "narrative": "hook"},
      {"number": 2, "duration": 5, "description": "AI features demonstration", "narrative": "benefit"},
      {"number": 3, "duration": 4, "description": "Price reveal with CTA", "narrative": "cta"}
    ]
  }
}
```

### Output (voice production context)

```json
{
  "segments": [
    {
      "segment_id": 1,
      "text": "Descubra o poder da tecnologia",
      "timing": {"start": 0.3, "end": 2.8, "duration": 2.5},
      "intonation_hints": {
        "tone": "excited",
        "emphasis": "high",
        "speed": 1.1,
        "pitch_shift": "+5%"
      },
      "emotion_tag": "hook",
      "pronunciation_notes": []
    },
    {
      "segment_id": 2,
      "text": "Samsung Galaxy S24 com IA integrada",
      "timing": {"start": 5.0, "end": 9.0, "duration": 4.0},
      "intonation_hints": {
        "tone": "confident",
        "emphasis": "medium-high",
        "speed": 0.95,
        "pitch_shift": "+2%"
      },
      "emotion_tag": "benefit",
      "pronunciation_notes": [
        {"term": "Samsung", "guide": "SÃM-sãng (Korean pronunciation)"},
        {"term": "Galaxy", "guide": "GÁ-la-xi (emphasis on first syllable)"},
        {"term": "IA", "guide": "I-Á (spell out, emphasis on A)"}
      ]
    },
    {
      "segment_id": 3,
      "text": "Por apenas R$ 3.499",
      "timing": {"start": 26.0, "end": 29.5, "duration": 3.5},
      "intonation_hints": {
        "tone": "urgent",
        "emphasis": "high",
        "speed": 1.05,
        "pitch_shift": "+8%"
      },
      "emotion_tag": "cta",
      "pronunciation_notes": []
    }
  ],
  "breath_marks": [
    {"position": 2.8, "type": "breath", "duration": 1.2},
    {"position": 9.0, "type": "breath", "duration": 1.0}
  ],
  "voice_config": {
    "voice_id": "XrExE9yKIg1WjnnlVkGX",
    "voice_name": "Laura",
    "gender": "feminina",
    "settings": {"stability": 0.5, "similarity_boost": 0.75}
  }
}
```

### Generated Handoff

```handoff
contexto: Video script processed for samsung_galaxy_s24_30s
arquivos_gerados:
  - voice_production_context.json
proximo: Run voice_agent TTS production with timing specs
dados:
  segments: 3 segments
  total_duration: 30.0s
  voice: Laura (feminina)
  intonation_hints: complete (3/3 segments)
  pronunciation_guides: 3 terms (Samsung, Galaxy, IA)
  breath_marks: 2 pauses
  music_background: music/upbeat_electronic.mp3 (vol: 0.3)
qualidade: 9.0/10
```

---

## INTEGRATION

### With /flow
```bash
/flow plan "create voice-over from video [video_name]"
# Automatically includes bridge phase
```

### With /spawn
```bash
/spawn
1. build: video for [product]
2. build: bridge video→voice
3. build: produce TTS with context
```

### With voice_agent Production
```python
# In voice_agent TTS workflow:
context = load_voice_context("voice_production_context.json")

for segment in context["segments"]:
    audio = generate_tts(
        text=segment["text"],
        voice_id=context["voice_config"]["voice_id"],
        speed=segment["intonation_hints"]["speed"],
        emphasis=segment["intonation_hints"]["emphasis"]
    )
    audio_clips.append(audio)
```

---

## VALIDATION

Quality gate (≥7.0/10):
- [ ] Segments extracted (≥1 item)
- [ ] Timing validated (no overlaps)
- [ ] Intonation hints defined (all segments)
- [ ] Pronunciation guides added (technical terms)
- [ ] Breath marks calculated (natural pauses)
- [ ] Voice config validated (valid ElevenLabs ID)
- [ ] Total duration matches video ±0.5s
- [ ] Handoff format correct

---

## TTS PRODUCTION HINTS

### Speed Modulation by Narrative
- **hook**: 1.1x speed (energetic)
- **build**: 1.0x speed (conversational)
- **benefit**: 0.95x speed (emphasized)
- **proof**: 0.9x speed (authoritative)
- **transformation**: 0.95x speed (inspirational)
- **cta**: 1.05x speed (urgent)

### Pitch Adjustment by Emotion
- **excited/urgent**: +5% to +8%
- **confident/inspirational**: +2% to +3%
- **credible/professional**: 0% (neutral)
- **calm/soothing**: -2%

### Emphasis Mapping
- **high**: Bold intonation, clear enunciation
- **medium-high**: Moderate stress on key words
- **medium**: Conversational emphasis
- **low**: Subtle, natural delivery

---

## ERROR HANDLING

### Phase 1 Failure
- **Cause**: Video script not found
- **Action**: Prompt user for correct path, offer to list available videos

### Phase 2 Failure
- **Cause**: Invalid script format or missing fields
- **Action**: Attempt to extract partial data, flag missing fields, create fallback context

### Phase 3 Failure
- **Cause**: Validation score < 7.0
- **Action**: Report specific validation errors, offer to continue with warnings

### Phase 4 Failure
- **Cause**: Cannot write output file
- **Action**: Return handoff block as text, offer alternative save location

---

**Version**: 1.0.0
**Created**: 2025-12-03
**Type**: Bridge Workflow (video_agent → voice_agent)
