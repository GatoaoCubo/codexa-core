#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice State Management
==============================

Shared state, types, and configuration for the voice system.
Used by daemon, client, GUI, and terminal UI.

Version: 8.0.0
"""

import os
import json
import time
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Callable
from pathlib import Path

# =============================================================================
# PATHS
# =============================================================================

VOICE_ROOT = Path(__file__).parent
PROJECT_ROOT = VOICE_ROOT.parent.parent
STATE_FILE = VOICE_ROOT / '.voice_state.json'
SOCKET_PATH = 'localhost'
SOCKET_PORT = 5557

# =============================================================================
# ENUMS
# =============================================================================

class VoiceStatus(str, Enum):
    """Voice system status."""
    IDLE = "idle"
    LISTENING = "listening"
    RECORDING = "recording"
    PROCESSING = "processing"
    TRANSCRIBING = "transcribing"
    SPEAKING = "speaking"
    ERROR = "error"
    STOPPED = "stopped"


class VoiceMode(str, Enum):
    """Voice interaction mode."""
    PUSH_TO_TALK = "push_to_talk"      # Hotkey held = record
    TOGGLE = "toggle"                   # Hotkey toggles recording
    CONTINUOUS = "continuous"           # Always listening with VAD
    WAKE_WORD = "wake_word"            # Wake word activates


class MessageType(str, Enum):
    """Socket message types."""
    # Commands
    START_RECORDING = "start_recording"
    STOP_RECORDING = "stop_recording"
    CANCEL = "cancel"
    GET_STATUS = "get_status"
    SHUTDOWN = "shutdown"
    SET_MODE = "set_mode"

    # Responses
    STATUS_UPDATE = "status_update"
    TRANSCRIPTION = "transcription"
    ERROR = "error"
    ACK = "ack"


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class VoiceState:
    """Current state of the voice system."""
    status: VoiceStatus = VoiceStatus.IDLE
    mode: VoiceMode = VoiceMode.PUSH_TO_TALK

    # Recording info
    is_recording: bool = False
    recording_start: Optional[float] = None
    recording_duration: float = 0.0
    audio_level: float = 0.0

    # Last result
    last_transcript: str = ""
    last_error: str = ""
    last_command_time: Optional[float] = None

    # Stats
    total_commands: int = 0
    session_start: float = field(default_factory=time.time)

    # Config
    max_duration: float = 15.0
    hotkey: str = "f12"
    language: str = "pt"

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        d = asdict(self)
        d['status'] = self.status.value
        d['mode'] = self.mode.value
        return d

    @classmethod
    def from_dict(cls, d: dict) -> 'VoiceState':
        """Create from dictionary."""
        d['status'] = VoiceStatus(d.get('status', 'idle'))
        d['mode'] = VoiceMode(d.get('mode', 'push_to_talk'))
        return cls(**d)

    def save(self):
        """Save state to file."""
        try:
            with open(STATE_FILE, 'w') as f:
                json.dump(self.to_dict(), f, indent=2)
        except Exception:
            pass

    @classmethod
    def load(cls) -> 'VoiceState':
        """Load state from file."""
        try:
            if STATE_FILE.exists():
                with open(STATE_FILE, 'r') as f:
                    return cls.from_dict(json.load(f))
        except Exception:
            pass
        return cls()


@dataclass
class SocketMessage:
    """Message for socket communication."""
    type: MessageType
    data: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def to_json(self) -> str:
        """Serialize to JSON string."""
        return json.dumps({
            'type': self.type.value,
            'data': self.data,
            'timestamp': self.timestamp
        })

    @classmethod
    def from_json(cls, s: str) -> 'SocketMessage':
        """Deserialize from JSON string."""
        d = json.loads(s)
        return cls(
            type=MessageType(d['type']),
            data=d.get('data', {}),
            timestamp=d.get('timestamp', time.time())
        )


# =============================================================================
# VISUAL CONSTANTS
# =============================================================================

# Status indicators
STATUS_ICONS = {
    VoiceStatus.IDLE: "○",
    VoiceStatus.LISTENING: "◉",
    VoiceStatus.RECORDING: "●",
    VoiceStatus.PROCESSING: "◐",
    VoiceStatus.TRANSCRIBING: "◑",
    VoiceStatus.SPEAKING: "🔊",
    VoiceStatus.ERROR: "✗",
    VoiceStatus.STOPPED: "◯",
}

STATUS_COLORS = {
    VoiceStatus.IDLE: "white",
    VoiceStatus.LISTENING: "yellow",
    VoiceStatus.RECORDING: "red",
    VoiceStatus.PROCESSING: "yellow",
    VoiceStatus.TRANSCRIBING: "cyan",
    VoiceStatus.SPEAKING: "blue",
    VoiceStatus.ERROR: "red",
    VoiceStatus.STOPPED: "dim",
}

# Waveform characters (low to high)
WAVEFORM_CHARS = " ▁▂▃▄▅▆▇█"

# Progress bar characters
PROGRESS_FULL = "█"
PROGRESS_EMPTY = "░"


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def audio_level_to_bars(level: float, width: int = 20) -> str:
    """Convert audio level (0-1) to ASCII bar."""
    filled = int(level * width * 5)  # Amplify for visibility
    filled = min(filled, width)
    return PROGRESS_FULL * filled + PROGRESS_EMPTY * (width - filled)


def audio_level_to_waveform(level: float) -> str:
    """Convert audio level to single waveform character."""
    idx = int(level * (len(WAVEFORM_CHARS) - 1) * 10)
    idx = min(idx, len(WAVEFORM_CHARS) - 1)
    return WAVEFORM_CHARS[idx]


def generate_waveform(levels: List[float], width: int = 30) -> str:
    """Generate ASCII waveform from list of audio levels."""
    if not levels:
        return WAVEFORM_CHARS[0] * width

    # Resample to fit width
    step = max(1, len(levels) // width)
    sampled = levels[::step][:width]

    # Pad if needed
    while len(sampled) < width:
        sampled.append(0)

    return ''.join(audio_level_to_waveform(l) for l in sampled)


def format_duration(seconds: float) -> str:
    """Format duration as MM:SS or SS.s"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins}:{secs:02d}"


def is_daemon_running() -> bool:
    """Check if daemon is running by trying to connect."""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        s.connect((SOCKET_PATH, SOCKET_PORT))
        s.close()
        return True
    except Exception:
        return False


# =============================================================================
# CONFIGURATION
# =============================================================================

@dataclass
class VoiceConfig:
    """Voice system configuration."""
    # Audio
    input_device: Optional[int] = 2  # Intel Smart Sound
    output_device: Optional[int] = None
    sample_rate: int = 44100

    # Recording
    max_duration: float = 15.0
    silence_threshold: float = 0.01
    silence_duration: float = 1.5
    initial_timeout: float = 5.0

    # Hotkey
    hotkey: str = "f12"
    mode: VoiceMode = VoiceMode.PUSH_TO_TALK

    # STT/TTS
    language: str = "pt"
    tts_enabled: bool = True

    # GUI
    gui_enabled: bool = True
    gui_always_on_top: bool = True
    gui_opacity: float = 0.95
    gui_position: tuple = (100, 100)

    @classmethod
    def load(cls) -> 'VoiceConfig':
        """Load from environment and defaults."""
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=PROJECT_ROOT / '.env')

        return cls(
            input_device=int(os.getenv('AUDIO_INPUT_DEVICE', '2') or '2'),
            output_device=int(os.getenv('AUDIO_OUTPUT_DEVICE', '0') or '0') if os.getenv('AUDIO_OUTPUT_DEVICE') else None,
            max_duration=float(os.getenv('STT_MAX_DURATION', '15')),
            language=os.getenv('STT_LANGUAGE', 'pt'),
            hotkey=os.getenv('VOICE_HOTKEY', 'f12'),
        )


# =============================================================================
# SINGLETON STATE
# =============================================================================

_global_state: Optional[VoiceState] = None


def get_state() -> VoiceState:
    """Get global voice state."""
    global _global_state
    if _global_state is None:
        _global_state = VoiceState.load()
    return _global_state


def set_state(state: VoiceState):
    """Set global voice state."""
    global _global_state
    _global_state = state
    state.save()
