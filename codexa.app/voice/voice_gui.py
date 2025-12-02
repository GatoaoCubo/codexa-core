#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice GUI Overlay
========================

Minimal floating GUI for voice interaction feedback.
Shows recording status, waveform, and transcriptions.

Features:
- Transparent, always-on-top window
- Pulsing indicator during recording
- Waveform visualization
- Live transcription display
- Draggable position

Usage:
    python voice_gui.py                  # Standalone mode
    python voice_gui.py --daemon         # Connect to daemon

Version: 8.0.0
"""

import sys
import os
import time
import threading
import math
from pathlib import Path
from typing import Optional, List

# Add voice module to path
VOICE_ROOT = Path(__file__).parent
sys.path.insert(0, str(VOICE_ROOT))

# GUI imports
try:
    import tkinter as tk
    from tkinter import ttk
    HAS_TK = True
except ImportError:
    HAS_TK = False
    print("Tkinter not available")

# Local imports
from voice_state import (
    VoiceStatus, VoiceState, VoiceConfig,
    STATUS_ICONS, STATUS_COLORS,
    audio_level_to_bars, generate_waveform
)


# =============================================================================
# COLOR SCHEME
# =============================================================================

COLORS = {
    'bg': '#1a1a2e',
    'bg_light': '#16213e',
    'text': '#eaeaea',
    'text_dim': '#888888',
    'red': '#e94560',
    'yellow': '#f0a500',
    'green': '#4ecca3',
    'blue': '#00adb5',
    'purple': '#7b2cbf',
}


# =============================================================================
# VOICE GUI CLASS
# =============================================================================

class VoiceGUI:
    """
    Floating voice status overlay.

    Shows:
    - Recording status indicator (pulsing circle)
    - Audio level meter
    - Waveform visualization
    - Last transcription
    """

    def __init__(self, config: Optional[VoiceConfig] = None):
        if not HAS_TK:
            raise RuntimeError("Tkinter not available")

        self.config = config or VoiceConfig.load()
        self.state = VoiceState()

        # Window
        self.root: Optional[tk.Tk] = None
        self.running = False

        # Animation
        self.pulse_phase = 0
        self.waveform_data: List[float] = [0] * 30

        # Dragging
        self._drag_x = 0
        self._drag_y = 0

        # Canvas items
        self.status_circle = None
        self.level_bar = None
        self.waveform_line = None
        self.status_text = None
        self.transcript_text = None

    def create_window(self):
        """Create the overlay window."""
        self.root = tk.Tk()
        self.root.title("CODEXA Voice")

        # Window settings
        self.root.overrideredirect(True)  # No window decorations
        self.root.attributes('-topmost', True)  # Always on top
        self.root.attributes('-alpha', self.config.gui_opacity)

        # Set size and position
        width, height = 280, 140
        x, y = self.config.gui_position
        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Background color
        self.root.configure(bg=COLORS['bg'])

        # Main frame
        self.frame = tk.Frame(self.root, bg=COLORS['bg'])
        self.frame.pack(fill='both', expand=True, padx=5, pady=5)

        # Title bar (for dragging)
        self.title_bar = tk.Frame(self.frame, bg=COLORS['bg_light'], height=25)
        self.title_bar.pack(fill='x')
        self.title_bar.pack_propagate(False)

        title_label = tk.Label(
            self.title_bar,
            text="🎤 CODEXA Voice",
            bg=COLORS['bg_light'],
            fg=COLORS['text'],
            font=('Segoe UI', 9, 'bold')
        )
        title_label.pack(side='left', padx=5)

        # Close button
        close_btn = tk.Label(
            self.title_bar,
            text="✕",
            bg=COLORS['bg_light'],
            fg=COLORS['text_dim'],
            font=('Segoe UI', 10),
            cursor='hand2'
        )
        close_btn.pack(side='right', padx=5)
        close_btn.bind('<Button-1>', lambda e: self.close())

        # Bind dragging
        self.title_bar.bind('<Button-1>', self._start_drag)
        self.title_bar.bind('<B1-Motion>', self._do_drag)
        title_label.bind('<Button-1>', self._start_drag)
        title_label.bind('<B1-Motion>', self._do_drag)

        # Canvas for visualizations
        self.canvas = tk.Canvas(
            self.frame,
            width=270,
            height=80,
            bg=COLORS['bg'],
            highlightthickness=0
        )
        self.canvas.pack(pady=5)

        # Status indicator (circle)
        self.status_circle = self.canvas.create_oval(
            10, 10, 40, 40,
            fill=COLORS['text_dim'],
            outline=''
        )

        # Status text
        self.status_text = self.canvas.create_text(
            50, 25,
            text="IDLE",
            anchor='w',
            fill=COLORS['text'],
            font=('Segoe UI', 10, 'bold')
        )

        # Hotkey hint
        self.canvas.create_text(
            260, 25,
            text=f"[{self.config.hotkey.upper()}]",
            anchor='e',
            fill=COLORS['text_dim'],
            font=('Segoe UI', 8)
        )

        # Level meter background
        self.canvas.create_rectangle(
            10, 50, 260, 60,
            fill=COLORS['bg_light'],
            outline=''
        )

        # Level meter foreground
        self.level_bar = self.canvas.create_rectangle(
            10, 50, 10, 60,
            fill=COLORS['green'],
            outline=''
        )

        # Waveform
        self.waveform_points = [(10 + i * 8, 75) for i in range(32)]
        self.waveform_line = self.canvas.create_line(
            *[coord for point in self.waveform_points for coord in point],
            fill=COLORS['blue'],
            width=2,
            smooth=True
        )

        # Transcript label
        self.transcript_label = tk.Label(
            self.frame,
            text="",
            bg=COLORS['bg'],
            fg=COLORS['text_dim'],
            font=('Segoe UI', 8),
            wraplength=260,
            anchor='w',
            justify='left'
        )
        self.transcript_label.pack(fill='x', padx=5)

    def _start_drag(self, event):
        """Start window drag."""
        self._drag_x = event.x
        self._drag_y = event.y

    def _do_drag(self, event):
        """Handle window drag."""
        x = self.root.winfo_x() + (event.x - self._drag_x)
        y = self.root.winfo_y() + (event.y - self._drag_y)
        self.root.geometry(f"+{x}+{y}")

    def update_state(self, state: VoiceState):
        """Update UI from state."""
        self.state = state

        # Update status indicator color
        status = state.status
        if status == VoiceStatus.RECORDING:
            color = COLORS['red']
        elif status == VoiceStatus.PROCESSING or status == VoiceStatus.TRANSCRIBING:
            color = COLORS['yellow']
        elif status == VoiceStatus.SPEAKING:
            color = COLORS['blue']
        elif status == VoiceStatus.IDLE:
            color = COLORS['green']
        else:
            color = COLORS['text_dim']

        # Apply pulse effect for recording
        if status == VoiceStatus.RECORDING:
            self.pulse_phase += 0.2
            alpha = 0.5 + 0.5 * math.sin(self.pulse_phase)
            # Tkinter doesn't support alpha on items, so we'll blink instead
            if int(self.pulse_phase * 2) % 2 == 0:
                self.canvas.itemconfig(self.status_circle, fill=color)
            else:
                self.canvas.itemconfig(self.status_circle, fill=COLORS['bg'])
        else:
            self.canvas.itemconfig(self.status_circle, fill=color)

        # Update status text
        status_names = {
            VoiceStatus.IDLE: "PRONTO",
            VoiceStatus.RECORDING: "GRAVANDO",
            VoiceStatus.PROCESSING: "PROCESSANDO",
            VoiceStatus.TRANSCRIBING: "TRANSCREVENDO",
            VoiceStatus.SPEAKING: "FALANDO",
            VoiceStatus.ERROR: "ERRO",
            VoiceStatus.STOPPED: "PARADO",
        }
        self.canvas.itemconfig(
            self.status_text,
            text=status_names.get(status, "?"),
            fill=color
        )

        # Update level meter
        level = state.audio_level
        bar_width = int(level * 250 * 5)  # Amplify
        bar_width = min(bar_width, 250)
        self.canvas.coords(self.level_bar, 10, 50, 10 + bar_width, 60)

        # Color level bar based on level
        if level > 0.05:
            self.canvas.itemconfig(self.level_bar, fill=COLORS['green'])
        elif level > 0.02:
            self.canvas.itemconfig(self.level_bar, fill=COLORS['yellow'])
        else:
            self.canvas.itemconfig(self.level_bar, fill=COLORS['text_dim'])

        # Update waveform
        self.waveform_data.append(level)
        self.waveform_data = self.waveform_data[-30:]

        points = []
        for i, lvl in enumerate(self.waveform_data):
            x = 10 + i * 8
            y = 75 - int(lvl * 200)  # Scale
            y = max(55, min(75, y))  # Clamp
            points.extend([x, y])

        if len(points) >= 4:
            self.canvas.coords(self.waveform_line, *points)

        # Update transcript
        if state.last_transcript:
            text = state.last_transcript
            if len(text) > 60:
                text = text[:57] + "..."
            self.transcript_label.config(text=f'"{text}"')

    def animate(self):
        """Animation loop."""
        if not self.running:
            return

        # Update pulse for recording
        if self.state.status == VoiceStatus.RECORDING:
            self.pulse_phase += 0.15
            alpha = 0.5 + 0.5 * math.sin(self.pulse_phase)
            if alpha > 0.7:
                self.canvas.itemconfig(self.status_circle, fill=COLORS['red'])
            else:
                self.canvas.itemconfig(self.status_circle, fill='#8b0000')

        # Schedule next frame
        self.root.after(50, self.animate)

    def run(self):
        """Run the GUI main loop."""
        self.create_window()
        self.running = True
        self.animate()
        self.root.mainloop()

    def close(self):
        """Close the GUI."""
        self.running = False
        if self.root:
            self.root.quit()
            self.root.destroy()


# =============================================================================
# DAEMON-CONNECTED GUI
# =============================================================================

class VoiceGUIWithDaemon(VoiceGUI):
    """GUI that connects to the voice daemon for status updates."""

    def __init__(self):
        super().__init__()
        self.client = None

    def connect_to_daemon(self):
        """Connect to the daemon and start receiving updates."""
        from voice_client import VoiceClient

        self.client = VoiceClient()
        self.client.on_status_change = self._on_status_change
        self.client.on_transcription = self._on_transcription

        if self.client.connect():
            print("[GUI] Connected to daemon")
            return True
        else:
            print("[GUI] Could not connect to daemon")
            return False

    def _on_status_change(self, state: VoiceState):
        """Handle status update from daemon."""
        if self.root:
            self.root.after(0, lambda: self.update_state(state))

    def _on_transcription(self, text: str):
        """Handle transcription from daemon."""
        self.state.last_transcript = text
        if self.root:
            self.root.after(0, lambda: self.update_state(self.state))

    def run(self):
        """Run with daemon connection."""
        self.create_window()
        self.running = True

        # Connect to daemon in background
        def connect():
            if self.connect_to_daemon():
                # Get initial status
                state = self.client.get_status()
                if state:
                    self.root.after(0, lambda: self.update_state(state))

        threading.Thread(target=connect, daemon=True).start()

        self.animate()
        self.root.mainloop()

    def close(self):
        """Close GUI and disconnect."""
        if self.client:
            self.client.disconnect()
        super().close()


# =============================================================================
# STANDALONE GUI (with built-in recording)
# =============================================================================

class VoiceGUIStandalone(VoiceGUI):
    """GUI with built-in voice recording (no daemon needed)."""

    def __init__(self):
        super().__init__()
        self.recording = False
        self.audio_data = []

    def create_window(self):
        """Create window with record button."""
        super().create_window()

        # Add record button
        self.record_btn = tk.Button(
            self.frame,
            text="🎤 GRAVAR",
            bg=COLORS['red'],
            fg='white',
            font=('Segoe UI', 9, 'bold'),
            relief='flat',
            cursor='hand2',
            command=self.toggle_recording
        )
        self.record_btn.pack(fill='x', padx=5, pady=5)

    def toggle_recording(self):
        """Toggle recording state."""
        if self.recording:
            self.stop_recording()
        else:
            self.start_recording()

    def start_recording(self):
        """Start voice recording."""
        self.recording = True
        self.record_btn.config(text="⏹ PARAR", bg=COLORS['yellow'])
        self.state.status = VoiceStatus.RECORDING
        self.update_state(self.state)

        # Start recording thread
        threading.Thread(target=self._record, daemon=True).start()

    def stop_recording(self):
        """Stop recording and process."""
        self.recording = False
        self.record_btn.config(text="🎤 GRAVAR", bg=COLORS['red'])

    def _record(self):
        """Recording thread."""
        try:
            import sounddevice as sd
            import numpy as np

            self.audio_data = []

            def callback(indata, frames, time_info, status):
                if not self.recording:
                    raise sd.CallbackAbort()

                self.audio_data.append(indata.copy())
                rms = float(np.sqrt(np.mean(indata**2)))
                self.state.audio_level = rms

                # Update UI
                self.root.after(0, lambda: self.update_state(self.state))

            with sd.InputStream(
                samplerate=44100,
                device=self.config.input_device,
                channels=1,
                callback=callback,
                dtype='float32'
            ):
                start = time.time()
                while self.recording and time.time() - start < 15:
                    time.sleep(0.05)

        except Exception as e:
            print(f"Recording error: {e}")

        finally:
            self.recording = False
            self.state.status = VoiceStatus.PROCESSING
            self.root.after(0, lambda: self.update_state(self.state))
            self.root.after(0, lambda: self.record_btn.config(text="🎤 GRAVAR", bg=COLORS['red']))

            # Process audio
            if self.audio_data:
                self._process_audio()

    def _process_audio(self):
        """Process recorded audio."""
        try:
            import numpy as np
            import soundfile as sf
            import tempfile
            import requests

            audio = np.concatenate(self.audio_data)

            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                sf.write(f.name, audio, 44100)
                audio_path = f.name

            self.state.status = VoiceStatus.TRANSCRIBING
            self.root.after(0, lambda: self.update_state(self.state))

            # Transcribe
            api_key = os.getenv('ELEVENLABS_API_KEY')
            if api_key:
                with open(audio_path, 'rb') as f:
                    response = requests.post(
                        'https://api.elevenlabs.io/v1/speech-to-text',
                        headers={'xi-api-key': api_key},
                        files={'file': ('audio.wav', f, 'audio/wav')},
                        data={'model_id': 'scribe_v1', 'language_code': 'pt'},
                        timeout=30
                    )

                if response.ok:
                    text = response.json().get('text', '').strip()
                    if text:
                        self.state.last_transcript = text

            os.unlink(audio_path)

        except Exception as e:
            print(f"Processing error: {e}")

        finally:
            self.state.status = VoiceStatus.IDLE
            self.root.after(0, lambda: self.update_state(self.state))


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CODEXA Voice GUI")
    parser.add_argument('--daemon', '-d', action='store_true',
                        help='Connect to daemon for status')
    parser.add_argument('--standalone', '-s', action='store_true',
                        help='Standalone mode with built-in recording')

    args = parser.parse_args()

    # Load environment
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=VOICE_ROOT.parent.parent / '.env')

    if args.daemon:
        gui = VoiceGUIWithDaemon()
    elif args.standalone:
        gui = VoiceGUIStandalone()
    else:
        # Default: try daemon, fallback to standalone
        from voice_state import is_daemon_running
        if is_daemon_running():
            gui = VoiceGUIWithDaemon()
        else:
            gui = VoiceGUIStandalone()

    try:
        gui.run()
    except KeyboardInterrupt:
        gui.close()
