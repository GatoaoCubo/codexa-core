"""
05_editing_builder.py - Stage 5: Video Editing (FFmpeg)

Assembles clips into final video with audio, text overlays, and transitions.

BLOCKERS RESOLVED:
- Narration Audio (ElevenLabs TTS integration)
- Text Overlays (FFmpeg drawtext filter)

Author: CODEXA Meta-Constructor
Version: 1.0.0
"""

import asyncio
import subprocess
import os
import sys
import json
from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass
import tempfile


@dataclass
class EditingResult:
    """Result of video editing"""
    final_path: str
    duration: float
    file_size_mb: float
    success: bool
    error: Optional[str] = None


class EditingBuilder:
    """
    Stage 5: Assemble final video with FFmpeg

    Responsibilities:
    - Concatenate video clips
    - Generate TTS narration (ElevenLabs)
    - Mix audio layers (narration + music)
    - Add text overlays
    - Export final video
    """

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.temp_dir = Path(tempfile.mkdtemp())

        # ElevenLabs configuration
        self.elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.default_voice = "Rachel"  # Default voice ID

        # FFmpeg paths
        self.ffmpeg = "ffmpeg"
        self.ffprobe = "ffprobe"

        # Font paths by platform
        self.font_paths = {
            "win32": "C:/Windows/Fonts/arial.ttf",
            "linux": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "darwin": "/System/Library/Fonts/Helvetica.ttc"
        }

    async def assemble_video(
        self,
        clips: List[Dict],
        script: Dict,
        format: str = "9:16",
        output_name: str = "final_video"
    ) -> Dict:
        """
        Assemble final video from clips and script

        Args:
            clips: List of clip paths from Stage 4
            script: Script with narration, overlays, music from Stage 2
            format: Aspect ratio ("9:16", "16:9", "1:1")
            output_name: Output filename (without extension)

        Returns:
            Result dictionary with final video path
        """

        try:
            print("   Step 1/5: Concatenating clips...")
            concatenated = await self._concatenate_clips(clips)

            print("   Step 2/5: Generating narration audio (TTS)...")
            narration_audio = await self._generate_narration_audio(script)

            print("   Step 3/5: Mixing audio layers...")
            video_with_audio = await self._mix_audio_layers(
                video=concatenated,
                narration=narration_audio,
                music_config=script.get("music", {})
            )

            print("   Step 4/5: Adding text overlays...")
            video_with_text = await self._add_text_overlays(
                video=video_with_audio,
                overlays=script.get("text_overlays", [])
            )

            print("   Step 5/5: Exporting final video...")
            final_path = await self._export_final(
                video=video_with_text,
                format=format,
                output_name=output_name
            )

            # Get file info
            duration = self._get_video_duration(final_path)
            file_size = Path(final_path).stat().st_size / (1024 * 1024)  # MB

            print(f"   Final video: {final_path}")
            print(f"   Duration: {duration:.1f}s, Size: {file_size:.1f}MB")

            return {
                "final_path": final_path,
                "duration": duration,
                "file_size_mb": file_size,
                "success": True
            }

        except Exception as e:
            print(f"   Error during editing: {e}")
            return {
                "final_path": None,
                "duration": 0,
                "file_size_mb": 0,
                "success": False,
                "error": str(e)
            }

        finally:
            # Cleanup temp files
            self._cleanup_temp()

    async def _concatenate_clips(self, clips: List[Dict]) -> str:
        """Concatenate video clips using FFmpeg concat filter"""

        # Filter successful clips only
        valid_clips = [c for c in clips if c.get("success") and c.get("clip_path")]

        if not valid_clips:
            raise ValueError("No valid clips to concatenate")

        # Sort by shot number
        valid_clips.sort(key=lambda x: x.get("shot_number", 0))

        # Create concat file
        concat_file = self.temp_dir / "concat_list.txt"
        with open(concat_file, "w") as f:
            for clip in valid_clips:
                # Escape path for FFmpeg
                path = clip["clip_path"].replace("\\", "/")
                f.write(f"file '{path}'\n")

        # Output path
        output = str(self.temp_dir / "concatenated.mp4")

        # Run FFmpeg concat
        cmd = [
            self.ffmpeg,
            "-y",  # Overwrite
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",  # No re-encoding
            output
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Concat failed: {result.stderr}")

        return output

    async def _generate_narration_audio(self, script: Dict) -> Optional[str]:
        """
        Generate TTS narration using ElevenLabs

        BLOCKER 1 RESOLVED: ElevenLabs TTS integration
        """

        narration_segments = script.get("narration", [])

        if not narration_segments:
            print("      No narration segments, skipping TTS")
            return None

        if not self.elevenlabs_api_key:
            print("      ELEVENLABS_API_KEY not set, using silent track")
            return None

        try:
            # Import ElevenLabs
            from elevenlabs import generate, set_api_key, Voice

            set_api_key(self.elevenlabs_api_key)

            # Concatenate all narration text
            full_text = " ".join([s.get("text", "") for s in narration_segments])

            if not full_text.strip():
                return None

            # Get voice setting from script or use default
            voice_id = script.get("voice", self.default_voice)

            # Generate audio
            print(f"      Generating TTS for: '{full_text[:50]}...'")

            audio = generate(
                text=full_text,
                voice=voice_id,
                model="eleven_multilingual_v2"
            )

            # Save to temp file
            audio_path = str(self.temp_dir / "narration.mp3")

            with open(audio_path, "wb") as f:
                f.write(audio)

            print(f"      TTS audio saved: {audio_path}")
            return audio_path

        except ImportError:
            print("      ElevenLabs library not installed, skipping TTS")
            return None

        except Exception as e:
            print(f"      TTS generation failed: {e}")
            return None

    async def _mix_audio_layers(
        self,
        video: str,
        narration: Optional[str],
        music_config: Dict
    ) -> str:
        """Mix narration and background music"""

        output = str(self.temp_dir / "with_audio.mp4")

        # Get music track
        music_track = music_config.get("track")
        music_volume = music_config.get("volume", 0.3)

        # Build FFmpeg command based on available audio
        if narration and music_track and Path(music_track).exists():
            # Both narration and music
            cmd = [
                self.ffmpeg,
                "-y",
                "-i", video,
                "-i", narration,
                "-i", music_track,
                "-filter_complex",
                f"[1:a]volume=1.0[narr];"
                f"[2:a]volume={music_volume}[mus];"
                f"[narr][mus]amix=inputs=2:duration=first[aout]",
                "-map", "0:v",
                "-map", "[aout]",
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                output
            ]
        elif narration:
            # Narration only
            cmd = [
                self.ffmpeg,
                "-y",
                "-i", video,
                "-i", narration,
                "-map", "0:v",
                "-map", "1:a",
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                output
            ]
        elif music_track and Path(music_track).exists():
            # Music only
            cmd = [
                self.ffmpeg,
                "-y",
                "-i", video,
                "-i", music_track,
                "-filter_complex",
                f"[1:a]volume={music_volume}[aout]",
                "-map", "0:v",
                "-map", "[aout]",
                "-c:v", "copy",
                "-c:a", "aac",
                "-b:a", "192k",
                "-shortest",
                output
            ]
        else:
            # No audio to add, just copy
            print("      No audio tracks available, keeping original")
            return video

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"      Audio mixing warning: {result.stderr[:200]}")
            # Fall back to video without audio mixing
            return video

        return output

    async def _add_text_overlays(
        self,
        video: str,
        overlays: List[Dict]
    ) -> str:
        """
        Add text overlays using FFmpeg drawtext filter

        BLOCKER 2 RESOLVED: FFmpeg drawtext integration
        """

        if not overlays:
            print("      No text overlays to add")
            return video

        output = str(self.temp_dir / "with_text.mp4")

        # Get font path for current platform
        font_path = self._get_font_path()

        # Build drawtext filters
        filters = []

        for i, overlay in enumerate(overlays):
            text = overlay.get("text", "")
            start = overlay.get("start", 0)
            end = overlay.get("end", start + 3)
            position = overlay.get("position", "center")
            style = overlay.get("style", "bold")

            # Escape special characters for FFmpeg
            text = text.replace("'", "\\'").replace(":", "\\:")

            # Calculate position
            if position == "top":
                x, y = "(w-text_w)/2", "50"
            elif position == "bottom":
                x, y = "(w-text_w)/2", "h-100"
            else:  # center
                x, y = "(w-text_w)/2", "(h-text_h)/2"

            # Font size and style
            fontsize = 48 if style == "bold" else 36

            # Build filter string
            filter_str = (
                f"drawtext="
                f"text='{text}':"
                f"fontfile='{font_path}':"
                f"fontsize={fontsize}:"
                f"fontcolor=white:"
                f"borderw=3:"
                f"bordercolor=black:"
                f"x={x}:y={y}:"
                f"enable='between(t,{start},{end})'"
            )

            filters.append(filter_str)

        # Combine filters
        filter_complex = ",".join(filters)

        # Run FFmpeg
        cmd = [
            self.ffmpeg,
            "-y",
            "-i", video,
            "-vf", filter_complex,
            "-c:a", "copy",
            output
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"      Text overlay warning: {result.stderr[:200]}")
            # Try without text overlays
            return video

        return output

    async def _export_final(
        self,
        video: str,
        format: str,
        output_name: str
    ) -> str:
        """Export final video with proper encoding"""

        output = str(self.output_dir / f"{output_name}.mp4")

        # Determine resolution based on format
        if format == "9:16":
            scale = "1080:1920"
        elif format == "1:1":
            scale = "1080:1080"
        else:  # 16:9
            scale = "1920:1080"

        cmd = [
            self.ffmpeg,
            "-y",
            "-i", video,
            "-vf", f"scale={scale}:force_original_aspect_ratio=decrease,pad={scale}:(ow-iw)/2:(oh-ih)/2",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            output
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Export failed: {result.stderr}")

        return output

    def _get_font_path(self) -> str:
        """Get font path for current platform"""

        platform = sys.platform

        # Try platform-specific path
        if platform in self.font_paths:
            path = self.font_paths[platform]
            if Path(path).exists():
                return path

        # Fallback: try to find any available font
        common_fonts = [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/TTF/DejaVuSans.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "/System/Library/Fonts/Helvetica.ttc"
        ]

        for font in common_fonts:
            if Path(font).exists():
                return font

        # Last resort: use FFmpeg's default
        return "Sans"

    def _get_video_duration(self, video_path: str) -> float:
        """Get video duration using ffprobe"""

        cmd = [
            self.ffprobe,
            "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            video_path
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        try:
            return float(result.stdout.strip())
        except ValueError:
            return 0.0

    def _cleanup_temp(self):
        """Clean up temporary files"""

        import shutil

        try:
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"      Warning: Could not clean temp dir: {e}")


# ======================
# STANDALONE USAGE
# ======================

async def main():
    """Example usage of EditingBuilder"""

    builder = EditingBuilder(output_dir="outputs")

    # Mock clips (would come from Stage 4)
    clips = [
        {"shot_number": 1, "clip_path": "outputs/clips/clip_001.mp4", "success": True},
        {"shot_number": 2, "clip_path": "outputs/clips/clip_002.mp4", "success": True},
        {"shot_number": 3, "clip_path": "outputs/clips/clip_003.mp4", "success": True}
    ]

    # Script from Stage 2
    script = {
        "narration": [
            {"start": 0, "end": 3, "text": "Conheça o futuro do conforto"},
            {"start": 5, "end": 9, "text": "Nike Air Max com tecnologia revolucionária"}
        ],
        "text_overlays": [
            {"start": 1, "end": 4, "text": "NIKE AIR MAX 2024", "position": "bottom", "style": "bold"},
            {"start": 12, "end": 15, "text": "R$ 599 | FRETE GRÁTIS", "position": "center", "style": "bold"}
        ],
        "music": {
            "track": "music/upbeat_electronic.mp3",
            "volume": 0.3
        }
    }

    print("Assembling video...")
    result = await builder.assemble_video(
        clips=clips,
        script=script,
        format="9:16",
        output_name="tenis_nike_30s"
    )

    print("\n" + "="*50)
    print("EDITING RESULT")
    print("="*50)
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    asyncio.run(main())
