<!-- iso_vectorstore -->
<!--
  Source: 50_editor_assembler_HOP.md
  Agent: video_agent
  Synced: 2025-11-30
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# HOP: Editor Assembler | video_agent Stage 5

## MODULE_METADATA
```yaml
id: video_agent_editor_assembler
version: 1.0.0
purpose: Assemble final video with audio mixing, text overlays, and export
dependencies: [clips/*.mp4, script.json, ffmpeg]
category: video_production
stage: 5
```

## INPUT_CONTRACT
```yaml
required:
  $clips:
    type: array
    source: Stage 4 output
    description: Generated video clips
  $script:
    type: object
    source: script.json
    description: Script with narration, overlays, music
  $formato:
    type: string
    enum: ["9:16", "16:9", "1:1"]
    description: Output aspect ratio
optional:
  $output_name:
    type: string
    default: "final_video"
    description: Output filename (without extension)
  $tts_enabled:
    type: boolean
    default: true
    description: Generate TTS narration
  $quality:
    type: string
    enum: ["draft", "standard", "high"]
    default: "standard"
    description: Export quality preset
```

## OUTPUT_CONTRACT
```yaml
primary:
  final_video.mp4:
    type: file
    format: MP4 (H.264)
    resolution: 1080p+
    audio: AAC 192kbps
secondary:
  metadata.llm.json:
    type: object
    description: Structured metadata for LLM consumption
  metadata.meta.json:
    type: object
    description: Technical metadata (duration, size, codec)
```

## TASK

**Role**: Video Editor

**Objective**: Assemble all components into a polished, platform-ready video with professional audio mixing and text overlays.

**Standards**:
- Clip concatenation without re-encoding (if possible)
- Audio levels: narration 1.0, music 0.3
- Text overlays: white with black border (visibility)
- Export: H.264, AAC, faststart flag
- Platform-specific resolution

**Constraints**:
- FFmpeg must be installed
- Font file must exist for text overlays
- Output file < 50MB/minute
- Duration must match source clips

## STEPS

### Step 1: Filter Valid Clips
```python
from pathlib import Path

# Filter successful clips
valid_clips = [
    c for c in $clips
    if c.get("success") and c.get("clip_path") and Path(c["clip_path"]).exists()
]

if not valid_clips:
    raise ValueError("No valid clips to assemble")

# Sort by shot number
valid_clips.sort(key=lambda x: x.get("shot_number", 0))

print(f"Assembling {len(valid_clips)} clips")
```

### Step 2: Concatenate Clips
```python
import subprocess
import tempfile

temp_dir = Path(tempfile.mkdtemp())

# Create concat file
concat_file = temp_dir / "concat_list.txt"
with open(concat_file, "w") as f:
    for clip in valid_clips:
        # Escape path for FFmpeg
        path = clip["clip_path"].replace("\\", "/")
        f.write(f"file '{path}'\n")

# Concatenate without re-encoding
concatenated = temp_dir / "concatenated.mp4"
cmd = [
    "ffmpeg", "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", str(concat_file),
    "-c", "copy",
    str(concatenated)
]
subprocess.run(cmd, check=True, capture_output=True)
```

### Step 3: Generate TTS Narration
```python
from elevenlabs import generate, set_api_key

if $tts_enabled and os.getenv("ELEVENLABS_API_KEY"):
    set_api_key(os.getenv("ELEVENLABS_API_KEY"))

    # Concatenate narration text
    narration_text = " ".join([
        seg["text"] for seg in $script.get("narration", [])
    ])

    if narration_text.strip():
        # Generate audio
        audio = generate(
            text=narration_text,
            voice=$script.get("voice", "Rachel"),
            model="eleven_multilingual_v2"
        )

        # Save to temp file
        narration_audio = temp_dir / "narration.mp3"
        with open(narration_audio, "wb") as f:
            f.write(audio)
    else:
        narration_audio = None
else:
    narration_audio = None
```

### Step 4: Mix Audio Layers
```python
music_config = $script.get("music", {})
music_track = music_config.get("track")
music_volume = music_config.get("volume", 0.3)

video_with_audio = temp_dir / "with_audio.mp4"

if narration_audio and music_track and Path(music_track).exists():
    # Both narration and music
    cmd = [
        "ffmpeg", "-y",
        "-i", str(concatenated),
        "-i", str(narration_audio),
        "-i", music_track,
        "-filter_complex",
        f"[1:a]volume=1.0[narr];"
        f"[2:a]volume={music_volume}[mus];"
        f"[narr][mus]amix=inputs=2:duration=first[aout]",
        "-map", "0:v",
        "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        str(video_with_audio)
    ]
elif narration_audio:
    # Narration only
    cmd = [
        "ffmpeg", "-y",
        "-i", str(concatenated),
        "-i", str(narration_audio),
        "-map", "0:v", "-map", "1:a",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        str(video_with_audio)
    ]
elif music_track and Path(music_track).exists():
    # Music only
    cmd = [
        "ffmpeg", "-y",
        "-i", str(concatenated),
        "-i", music_track,
        "-filter_complex", f"[1:a]volume={music_volume}[aout]",
        "-map", "0:v", "-map", "[aout]",
        "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        str(video_with_audio)
    ]
else:
    # No audio
    video_with_audio = concatenated

subprocess.run(cmd, check=True, capture_output=True)
```

### Step 5: Add Text Overlays
```python
overlays = $script.get("text_overlays", [])

if overlays:
    video_with_text = temp_dir / "with_text.mp4"

    # Get font path
    font_path = get_system_font()

    # Build drawtext filters
    filters = []
    for overlay in overlays:
        text = overlay["text"].replace("'", "\\'").replace(":", "\\:")
        start = overlay.get("start", 0)
        end = overlay.get("end", start + 3)
        position = overlay.get("position", "center")
        style = overlay.get("style", "normal")

        # Position mapping
        pos_map = {
            "top": ("(w-text_w)/2", "50"),
            "center": ("(w-text_w)/2", "(h-text_h)/2"),
            "bottom": ("(w-text_w)/2", "h-100")
        }
        x, y = pos_map.get(position, pos_map["center"])

        fontsize = 48 if style == "bold" else 36

        filter_str = (
            f"drawtext=text='{text}':"
            f"fontfile='{font_path}':"
            f"fontsize={fontsize}:"
            f"fontcolor=white:"
            f"borderw=3:bordercolor=black:"
            f"x={x}:y={y}:"
            f"enable='between(t,{start},{end})'"
        )
        filters.append(filter_str)

    filter_complex = ",".join(filters)

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_with_audio),
        "-vf", filter_complex,
        "-c:a", "copy",
        str(video_with_text)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
else:
    video_with_text = video_with_audio
```

### Step 6: Export Final
```python
# Resolution by format
resolution_map = {
    "9:16": "1080:1920",
    "16:9": "1920:1080",
    "1:1": "1080:1080"
}
scale = resolution_map.get($formato, "1080:1920")

# Quality presets
quality_map = {
    "draft": {"crf": 28, "preset": "ultrafast"},
    "standard": {"crf": 23, "preset": "medium"},
    "high": {"crf": 18, "preset": "slow"}
}
quality = quality_map.get($quality, quality_map["standard"])

# Output path
output_dir = Path("outputs")
output_dir.mkdir(parents=True, exist_ok=True)
final_path = output_dir / f"{$output_name}.mp4"

cmd = [
    "ffmpeg", "-y",
    "-i", str(video_with_text),
    "-vf", f"scale={scale}:force_original_aspect_ratio=decrease,"
           f"pad={scale}:(ow-iw)/2:(oh-ih)/2",
    "-c:v", "libx264",
    "-preset", quality["preset"],
    "-crf", str(quality["crf"]),
    "-c:a", "aac", "-b:a", "192k",
    "-movflags", "+faststart",
    str(final_path)
]
subprocess.run(cmd, check=True, capture_output=True)

# Get metadata
duration = get_video_duration(final_path)
file_size = final_path.stat().st_size / (1024 * 1024)

print(f"Final video: {final_path}")
print(f"Duration: {duration:.1f}s, Size: {file_size:.1f}MB")
```

### Step 7: Generate Trinity Output
```python
import json

# LLM-readable metadata
llm_metadata = {
    "video_path": str(final_path),
    "duration_seconds": duration,
    "format": $formato,
    "resolution": scale,
    "clips_used": len(valid_clips),
    "has_narration": narration_audio is not None,
    "has_music": music_track is not None,
    "text_overlays_count": len(overlays),
    "quality_preset": $quality
}

with open(output_dir / f"{$output_name}.llm.json", "w") as f:
    json.dump(llm_metadata, f, indent=2)

# Technical metadata
tech_metadata = {
    "codec_video": "H.264",
    "codec_audio": "AAC",
    "audio_bitrate": "192kbps",
    "file_size_mb": file_size,
    "created_at": datetime.now().isoformat(),
    "ffmpeg_version": get_ffmpeg_version()
}

with open(output_dir / f"{$output_name}.meta.json", "w") as f:
    json.dump(tech_metadata, f, indent=2)
```

## OUTPUT EXAMPLE
```
outputs/
├── tenis_nike_30s.mp4          # Final video
├── tenis_nike_30s.llm.json     # LLM metadata
└── tenis_nike_30s.meta.json    # Technical metadata
```

**final_video.mp4**: 1080x1920, 30s, H.264, AAC

**metadata.llm.json**:
```json
{
  "video_path": "outputs/tenis_nike_30s.mp4",
  "duration_seconds": 30.2,
  "format": "9:16",
  "resolution": "1080:1920",
  "clips_used": 6,
  "has_narration": true,
  "has_music": true,
  "text_overlays_count": 3,
  "quality_preset": "standard"
}
```

## VALIDATION

Quality Gates:
- [ ] Final file exists and is playable
- [ ] Duration matches source clips +/-10%
- [ ] Audio present (if TTS/music available)
- [ ] Text overlays visible (manual check)
- [ ] File size < 50MB/minute
- [ ] Trinity output complete (3 files)

Thresholds:
- Duration tolerance: +/-10%
- File size: < 50MB/minute
- Resolution: >= 1080p

## CONTEXT

**Usage**: Called by video_agent.py as final pipeline stage

**Upstream**:
- clips/*.mp4 from Stage 4
- script.json from Stage 2

**Downstream**:
- Final deliverable to user
- Ready for social media upload

**$arguments chaining**:
```
This is the final stage.
Output: Trinity (video + 2 JSON files)
```

**Assumptions**:
- FFmpeg installed and in PATH
- System fonts available
- Sufficient disk space for temp files
- Clips are compatible format (MP4, H.264)

---

**Version**: 1.0.0
**Created**: 2025-11-24
**Builder**: builders/05_editing_builder.py
