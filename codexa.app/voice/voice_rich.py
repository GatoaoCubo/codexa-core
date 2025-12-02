#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice Rich Terminal UI
==============================

Beautiful terminal UI for voice interactions using Rich library.
Provides visual feedback during recording, processing, and responses.

Features:
- Live waveform visualization
- Progress bar for recording duration
- Colored status indicators
- Spinner during processing
- Formatted transcription output

Usage:
    from voice_rich import VoiceRichUI

    ui = VoiceRichUI()
    result = ui.capture_voice()  # Full visual experience
    print(result)

Version: 8.0.0
"""

import sys
import os
import time
import threading
from pathlib import Path
from typing import Optional, List, Callable

# Fix encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add voice module to path
VOICE_ROOT = Path(__file__).parent
sys.path.insert(0, str(VOICE_ROOT))

# Rich imports
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from rich import box

# Audio imports
try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False
    print("[yellow]Warning: sounddevice/soundfile not installed[/]")

# Local imports
from voice_state import (
    VoiceStatus, VoiceState, VoiceConfig,
    STATUS_ICONS, STATUS_COLORS,
    audio_level_to_bars, generate_waveform, format_duration
)

# Load environment
from dotenv import load_dotenv
load_dotenv(dotenv_path=VOICE_ROOT.parent.parent / '.env')

# =============================================================================
# CONSOLE SETUP
# =============================================================================

console = Console()

# =============================================================================
# RICH UI CLASS
# =============================================================================

class VoiceRichUI:
    """
    Rich terminal UI for voice capture with visual feedback.

    Provides:
    - Live waveform during recording
    - Progress bar showing time remaining
    - Status indicators with colors
    - Spinner during processing
    - Formatted results
    """

    def __init__(self, config: Optional[VoiceConfig] = None):
        """Initialize the Rich UI."""
        self.config = config or VoiceConfig.load()
        self.console = Console()

        # State
        self.state = VoiceState()
        self.audio_levels: List[float] = []
        self.is_recording = False
        self.cancel_event = threading.Event()

        # Audio settings
        self.sample_rate = self.config.sample_rate
        self.device = self.config.input_device

    def _create_recording_panel(self, elapsed: float, level: float) -> Panel:
        """Create the recording status panel."""
        max_dur = self.config.max_duration
        remaining = max(0, max_dur - elapsed)

        # Status line
        icon = STATUS_ICONS[VoiceStatus.RECORDING]
        status_text = Text()
        status_text.append(f" {icon} ", style="bold red")
        status_text.append("GRAVANDO", style="bold red blink")
        status_text.append(f"  [{format_duration(elapsed)} / {format_duration(max_dur)}]", style="dim")

        # Progress bar
        progress_pct = elapsed / max_dur
        bar_width = 40
        filled = int(progress_pct * bar_width)
        bar = "█" * filled + "░" * (bar_width - filled)
        progress_line = Text()
        progress_line.append("  [", style="dim")
        progress_line.append(bar[:filled], style="red")
        progress_line.append(bar[filled:], style="dim")
        progress_line.append("]", style="dim")

        # Waveform
        waveform = generate_waveform(self.audio_levels[-60:], width=40)
        waveform_line = Text()
        waveform_line.append("  ", style="dim")
        waveform_line.append(waveform, style="green")

        # Level meter
        level_bar = audio_level_to_bars(level, width=40)
        level_line = Text()
        level_line.append("  ", style="dim")
        # Color based on level
        if level > 0.1:
            level_line.append(level_bar, style="bold green")
        elif level > 0.02:
            level_line.append(level_bar, style="yellow")
        else:
            level_line.append(level_bar, style="dim")

        # Instructions
        instruction = Text()
        instruction.append("\n  Fale agora... ", style="italic")
        instruction.append("(silêncio encerra)", style="dim italic")

        # Combine all
        content = Text()
        content.append_text(status_text)
        content.append("\n\n")
        content.append_text(progress_line)
        content.append("\n")
        content.append_text(waveform_line)
        content.append("\n")
        content.append_text(level_line)
        content.append_text(instruction)

        return Panel(
            Align.center(content),
            title="[bold white]🎤 CODEXA Voice[/]",
            border_style="red",
            box=box.ROUNDED,
            padding=(1, 2)
        )

    def _create_processing_panel(self, stage: str = "Processando") -> Panel:
        """Create the processing status panel."""
        icon = STATUS_ICONS[VoiceStatus.PROCESSING]

        content = Text()
        content.append(f"\n  {icon} ", style="bold yellow")
        content.append(stage.upper(), style="bold yellow")
        content.append("...\n", style="yellow")

        return Panel(
            Align.center(content),
            title="[bold white]🎤 CODEXA Voice[/]",
            border_style="yellow",
            box=box.ROUNDED,
            padding=(1, 2)
        )

    def _create_result_panel(self, transcript: str, success: bool = True) -> Panel:
        """Create the result panel."""
        if success:
            icon = "✓"
            style = "green"
            title_style = "bold green"
        else:
            icon = "✗"
            style = "red"
            title_style = "bold red"

        content = Text()
        content.append(f"\n  {icon} ", style=f"bold {style}")

        if success:
            content.append("Você disse:\n\n", style=style)
            content.append(f'  "{transcript}"', style=f"bold white")
        else:
            content.append(f"{transcript}", style=style)

        content.append("\n", style="dim")

        return Panel(
            Align.center(content),
            title="[bold white]🎤 CODEXA Voice[/]",
            border_style=style,
            box=box.ROUNDED,
            padding=(1, 2)
        )

    def _create_speaking_panel(self, text: str) -> Panel:
        """Create panel while TTS is speaking."""
        icon = STATUS_ICONS[VoiceStatus.SPEAKING]

        content = Text()
        content.append(f"\n  {icon} ", style="bold blue")
        content.append("RESPONDENDO", style="bold blue")
        content.append("\n\n", style="dim")
        content.append(f'  "{text}"', style="italic white")
        content.append("\n", style="dim")

        return Panel(
            Align.center(content),
            title="[bold white]🎤 CODEXA Voice[/]",
            border_style="blue",
            box=box.ROUNDED,
            padding=(1, 2)
        )

    def capture_voice(
        self,
        max_duration: Optional[float] = None,
        show_result: bool = True,
        play_beeps: bool = True
    ) -> Optional[str]:
        """
        Capture voice with rich visual feedback.

        Args:
            max_duration: Maximum recording duration (default: config value)
            show_result: Show result panel after transcription
            play_beeps: Play audio feedback beeps

        Returns:
            Transcribed text or None if failed/cancelled
        """
        if not HAS_AUDIO:
            self.console.print("[red]Audio libraries not available[/]")
            return None

        max_dur = max_duration or self.config.max_duration

        # Reset state
        self.audio_levels = []
        self.is_recording = True
        self.cancel_event.clear()
        audio_data = []
        speech_detected = False
        silence_frames = 0
        current_level = 0.0

        # Audio callback
        def audio_callback(indata, frames, time_info, status):
            nonlocal speech_detected, silence_frames, current_level
            if not self.is_recording:
                return

            audio_data.append(indata.copy())
            rms = float(np.sqrt(np.mean(indata**2)))
            current_level = rms
            self.audio_levels.append(rms)

            if rms > self.config.silence_threshold:
                speech_detected = True
                silence_frames = 0
            elif speech_detected:
                silence_frames += frames

        # Play start beep
        if play_beeps:
            try:
                import winsound
                winsound.Beep(800, 150)
            except Exception:
                pass

        # Start recording with live display
        start_time = time.time()

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                device=self.device,
                channels=1,
                callback=audio_callback,
                dtype='float32'
            ):
                with Live(
                    self._create_recording_panel(0, 0),
                    console=self.console,
                    refresh_per_second=10,
                    transient=True
                ) as live:
                    while self.is_recording:
                        elapsed = time.time() - start_time

                        # Update display
                        live.update(self._create_recording_panel(elapsed, current_level))

                        # Check conditions
                        if elapsed >= max_dur:
                            break

                        if speech_detected and silence_frames > self.sample_rate * self.config.silence_duration:
                            break

                        if not speech_detected and elapsed >= self.config.initial_timeout:
                            break

                        if self.cancel_event.is_set():
                            break

                        time.sleep(0.05)

        except Exception as e:
            self.console.print(f"[red]Recording error: {e}[/]")
            return None

        finally:
            self.is_recording = False

        # Play end beep
        if play_beeps:
            try:
                import winsound
                winsound.Beep(1200, 150)
            except Exception:
                pass

        # Check if we got audio
        if not audio_data or not speech_detected:
            if play_beeps:
                try:
                    import winsound
                    winsound.Beep(400, 300)
                except Exception:
                    pass
            if show_result:
                self.console.print(self._create_result_panel("Nenhuma fala detectada", success=False))
            return None

        # Processing phase
        with Live(
            self._create_processing_panel("Processando áudio"),
            console=self.console,
            refresh_per_second=4,
            transient=True
        ):
            # Combine audio
            audio = np.concatenate(audio_data)

            # Save to temp file
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                sf.write(f.name, audio, self.sample_rate)
                audio_path = f.name

        # Transcription phase
        transcript = None
        with Live(
            self._create_processing_panel("Transcrevendo"),
            console=self.console,
            refresh_per_second=4,
            transient=True
        ):
            try:
                import requests
                api_key = os.getenv('ELEVENLABS_API_KEY')

                if api_key:
                    with open(audio_path, 'rb') as f:
                        response = requests.post(
                            'https://api.elevenlabs.io/v1/speech-to-text',
                            headers={'xi-api-key': api_key},
                            files={'file': ('audio.wav', f, 'audio/wav')},
                            data={
                                'model_id': 'scribe_v1',
                                'language_code': self.config.language
                            },
                            timeout=30
                        )

                    if response.ok:
                        transcript = response.json().get('text', '').strip()
                else:
                    transcript = None

            except Exception as e:
                self.console.print(f"[red]Transcription error: {e}[/]")

            finally:
                # Cleanup temp file
                try:
                    os.unlink(audio_path)
                except Exception:
                    pass

        # Show result
        if show_result:
            if transcript and not transcript.startswith('('):
                self.console.print(self._create_result_panel(transcript, success=True))
            else:
                self.console.print(self._create_result_panel(
                    transcript or "Não foi possível transcrever",
                    success=False
                ))

        return transcript if transcript and not transcript.startswith('(') else None

    def speak_with_visual(self, text: str):
        """Speak text with visual feedback."""
        with Live(
            self._create_speaking_panel(text),
            console=self.console,
            refresh_per_second=4,
            transient=True
        ):
            try:
                from tts import speak
                speak(text)
            except Exception as e:
                self.console.print(f"[red]TTS error: {e}[/]")

    def show_status(self, state: VoiceState):
        """Show current status panel."""
        icon = STATUS_ICONS.get(state.status, "?")
        color = STATUS_COLORS.get(state.status, "white")

        table = Table(show_header=False, box=box.SIMPLE)
        table.add_column("Key", style="dim")
        table.add_column("Value")

        table.add_row("Status", f"[{color}]{icon} {state.status.value.upper()}[/]")
        table.add_row("Modo", state.mode.value)
        table.add_row("Hotkey", state.hotkey.upper())
        table.add_row("Idioma", state.language)
        table.add_row("Comandos", str(state.total_commands))

        if state.last_transcript:
            table.add_row("Último", f'"{state.last_transcript[:50]}..."' if len(state.last_transcript) > 50 else f'"{state.last_transcript}"')

        panel = Panel(
            table,
            title="[bold white]🎤 CODEXA Voice Status[/]",
            border_style=color,
            box=box.ROUNDED
        )

        self.console.print(panel)


# =============================================================================
# QUICK FUNCTIONS
# =============================================================================

def voice_capture() -> Optional[str]:
    """Quick voice capture with rich UI."""
    ui = VoiceRichUI()
    return ui.capture_voice()


def voice_speak(text: str):
    """Quick speak with visual feedback."""
    ui = VoiceRichUI()
    ui.speak_with_visual(text)


def voice_status():
    """Show voice status."""
    ui = VoiceRichUI()
    state = VoiceState.load()
    ui.show_status(state)


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CODEXA Voice Rich UI")
    parser.add_argument('--capture', '-c', action='store_true', help='Capture voice')
    parser.add_argument('--speak', '-s', type=str, help='Speak text')
    parser.add_argument('--status', action='store_true', help='Show status')
    parser.add_argument('--loop', '-l', action='store_true', help='Continuous loop')

    args = parser.parse_args()

    if args.speak:
        voice_speak(args.speak)
    elif args.status:
        voice_status()
    elif args.loop:
        console.print("[bold green]Modo contínuo iniciado. Ctrl+C para sair.[/]")
        ui = VoiceRichUI()
        try:
            while True:
                result = ui.capture_voice()
                if result:
                    # Check for exit commands
                    if any(word in result.lower() for word in ['sair', 'parar', 'exit', 'quit']):
                        ui.speak_with_visual("Até logo!")
                        break
                    ui.speak_with_visual(f"Você disse: {result}")
                time.sleep(0.5)
        except KeyboardInterrupt:
            console.print("\n[yellow]Encerrado.[/]")
    else:
        # Default: single capture
        result = voice_capture()
        if result:
            console.print(f"\n[green]Resultado:[/] {result}")
