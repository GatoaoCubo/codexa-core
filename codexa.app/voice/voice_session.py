#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice Session Manager - Poll-Based Architecture
=======================================================

Manages async voice recording/transcription sessions.
Allows non-blocking voice capture with polling.

Architecture:
    1. listen_start  -> Creates session, starts recording in background
    2. listen_poll   -> Returns current status (recording/transcribing/done)
    3. listen_stop   -> Cancels session immediately

This solves the blocking problem where Claude Code waits 15+ seconds
for voice capture to complete.
"""

import os
import sys
import uuid
import time
import threading
import tempfile
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, Optional, Callable, List
from enum import Enum

# Fix encoding for Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Audio imports
try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False
    print("Warning: sounddevice/soundfile not installed", file=sys.stderr)

# Load environment
from dotenv import load_dotenv
VOICE_ROOT = Path(__file__).parent
PROJECT_ROOT = VOICE_ROOT.parent.parent
load_dotenv(dotenv_path=PROJECT_ROOT / '.env')

from config import (
    AUDIO_INPUT_DEVICE,
    AUDIO_OUTPUT_DEVICE,
    VAD_SILENCE_THRESHOLD,
    VAD_ENERGY_THRESHOLD,
    VOICE_SILENCE_DURATION,
    VOICE_INITIAL_TIMEOUT,
)


class SessionStatus(Enum):
    """Voice session states."""
    STARTING = "starting"
    RECORDING = "recording"
    PROCESSING = "processing"      # Saving audio
    TRANSCRIBING = "transcribing"  # Calling ElevenLabs API
    DONE = "done"
    ERROR = "error"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"            # No speech detected


@dataclass
class VoiceSession:
    """Represents an active voice recording session."""

    id: str
    status: SessionStatus = SessionStatus.STARTING

    # Config - defaults from config.py
    max_duration: float = 15.0
    language: str = "pt"
    use_vad: bool = True
    silence_threshold: float = VAD_ENERGY_THRESHOLD  # RMS threshold from config
    silence_duration: float = VOICE_SILENCE_DURATION  # 2.0s - allows natural pauses
    initial_timeout: float = VOICE_INITIAL_TIMEOUT    # 3.0s - exit if no speech

    # Runtime state
    audio_buffer: List = field(default_factory=list)
    audio_path: Optional[str] = None
    transcript: Optional[str] = None
    error: Optional[str] = None
    has_speech: bool = False

    # Timing
    started_at: float = field(default_factory=time.time)
    recording_started_at: Optional[float] = None
    ended_at: Optional[float] = None

    # Threading
    cancel_event: threading.Event = field(default_factory=threading.Event)
    thread: Optional[threading.Thread] = None

    @property
    def elapsed(self) -> float:
        """Seconds since session started."""
        return time.time() - self.started_at

    @property
    def is_active(self) -> bool:
        """Whether session is still running."""
        return self.status in (
            SessionStatus.STARTING,
            SessionStatus.RECORDING,
            SessionStatus.PROCESSING,
            SessionStatus.TRANSCRIBING
        )


class VoiceSessionManager:
    """
    Manages multiple concurrent voice sessions.

    Usage:
        manager = VoiceSessionManager()
        session_id = manager.start_session(max_duration=10)

        # Poll until done
        while True:
            status = manager.poll_session(session_id)
            if status['status'] == 'done':
                print(status['transcript'])
                break
            time.sleep(0.5)
    """

    def __init__(self):
        self.sessions: Dict[str, VoiceSession] = {}
        self.sample_rate = 44100
        self._cleanup_lock = threading.Lock()
        self._max_sessions = 5
        self._session_max_age = 300.0  # 5 minutes

    def start_session(
        self,
        max_duration: float = 10.0,
        language: str = "pt",
        use_vad: bool = True,
        silence_threshold: float = 0.015,
        silence_duration: float = 1.2,
        initial_timeout: float = 3.0,
        play_beep: bool = True
    ) -> Dict:
        """
        Create a new voice session and start recording immediately.

        Returns immediately with session_id - does NOT block.

        Args:
            max_duration: Maximum recording time (seconds)
            language: Language code for transcription
            use_vad: Use Voice Activity Detection
            silence_threshold: RMS threshold for silence
            silence_duration: Seconds of silence to stop
            initial_timeout: Exit if no speech in this time
            play_beep: Play audio feedback beeps

        Returns:
            {"session_id": str, "status": "starting"}
        """
        if not HAS_AUDIO:
            return {
                "session_id": None,
                "status": "error",
                "error": "Audio libraries not installed (sounddevice, soundfile)"
            }

        # Cleanup old sessions first
        self._cleanup_old_sessions()

        # Check session limit
        active = sum(1 for s in self.sessions.values() if s.is_active)
        if active >= self._max_sessions:
            return {
                "session_id": None,
                "status": "error",
                "error": f"Too many active sessions ({active}). Cancel some first."
            }

        # Create session
        session_id = str(uuid.uuid4())[:8]

        session = VoiceSession(
            id=session_id,
            max_duration=max_duration,
            language=language,
            use_vad=use_vad,
            silence_threshold=silence_threshold,
            silence_duration=silence_duration,
            initial_timeout=initial_timeout
        )

        self.sessions[session_id] = session

        # Start recording in background thread
        session.thread = threading.Thread(
            target=self._recording_worker,
            args=(session, play_beep),
            daemon=True,
            name=f"voice-{session_id}"
        )
        session.thread.start()

        return {
            "session_id": session_id,
            "status": "starting",
            "max_duration": max_duration
        }

    def poll_session(self, session_id: str) -> Dict:
        """
        Get current status of a session.

        Returns immediately - does NOT block.

        Returns:
            {
                "status": str,  # starting/recording/transcribing/done/error/cancelled
                "elapsed": float,
                "has_speech": bool,
                "transcript": str (if done),
                "error": str (if error)
            }
        """
        session = self.sessions.get(session_id)

        if not session:
            return {
                "status": "not_found",
                "error": f"Session '{session_id}' not found. May have expired."
            }

        result = {
            "session_id": session_id,
            "status": session.status.value,
            "elapsed": round(session.elapsed, 1),
            "max_duration": session.max_duration,
            "has_speech": session.has_speech
        }

        if session.status == SessionStatus.DONE:
            result["transcript"] = session.transcript
            if session.ended_at and session.recording_started_at:
                result["recording_duration"] = round(
                    session.ended_at - session.recording_started_at, 1
                )

        if session.status == SessionStatus.ERROR:
            result["error"] = session.error

        if session.status == SessionStatus.TIMEOUT:
            result["error"] = "No speech detected within timeout period"

        return result

    def stop_session(self, session_id: str) -> Dict:
        """
        Cancel a recording session immediately.

        Returns:
            {"status": "cancelled"} or {"status": "error", "error": str}
        """
        session = self.sessions.get(session_id)

        if not session:
            return {
                "status": "not_found",
                "error": f"Session '{session_id}' not found"
            }

        if not session.is_active:
            return {
                "status": session.status.value,
                "message": "Session already finished"
            }

        # Signal cancellation
        session.cancel_event.set()
        session.status = SessionStatus.CANCELLED

        # Wait briefly for thread to finish
        if session.thread and session.thread.is_alive():
            session.thread.join(timeout=1.0)

        # Cleanup resources
        self._cleanup_session(session)

        return {
            "status": "cancelled",
            "elapsed": round(session.elapsed, 1)
        }

    def list_sessions(self) -> Dict:
        """List all active sessions."""
        active = []
        for sid, session in self.sessions.items():
            active.append({
                "session_id": sid,
                "status": session.status.value,
                "elapsed": round(session.elapsed, 1),
                "has_speech": session.has_speech
            })
        return {"sessions": active, "count": len(active)}

    # =========================================================================
    # PRIVATE METHODS
    # =========================================================================

    def _recording_worker(self, session: VoiceSession, play_beep: bool = True):
        """Background worker for recording and transcribing audio."""

        try:
            session.recording_started_at = time.time()
            session.status = SessionStatus.RECORDING

            # Play start beep
            if play_beep:
                self._play_beep(800, 150)

            # Record audio
            if session.use_vad:
                self._record_with_vad(session)
            else:
                self._record_fixed_duration(session)

            # IMMEDIATELY update status after recording ends
            # (before beep which can have latency on Windows)
            if session.cancel_event.is_set():
                session.status = SessionStatus.CANCELLED
                return

            if not session.has_speech:
                session.status = SessionStatus.TIMEOUT
                session.ended_at = time.time()
                if play_beep:
                    self._play_beep(400, 200)  # Low beep for timeout
                return

            # Change status BEFORE beep
            print(f"[{time.time():.2f}] Setting status to PROCESSING", file=sys.stderr)
            session.status = SessionStatus.PROCESSING

            # Play end beep (non-critical, after status change)
            if play_beep:
                self._play_beep(1200, 100)

            # Save audio to file
            audio_path = self._save_audio(session)

            if not audio_path:
                session.status = SessionStatus.ERROR
                session.error = "Failed to save audio file"
                return

            session.audio_path = audio_path

            # Transcribe
            session.status = SessionStatus.TRANSCRIBING
            transcript = self._transcribe(session)

            # Check for transcription errors
            if transcript and transcript.startswith("ERROR:"):
                session.status = SessionStatus.ERROR
                session.error = transcript
                return

            session.transcript = transcript if transcript else ""
            session.status = SessionStatus.DONE
            session.ended_at = time.time()

            print(f"Session {session.id} completed: {len(session.transcript)} chars",
                  file=sys.stderr)

        except Exception as e:
            session.status = SessionStatus.ERROR
            session.error = str(e)
            print(f"Session {session.id} error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)

    def _record_with_vad(self, session: VoiceSession):
        """Record with Voice Activity Detection using InputStream.

        Uses sd.InputStream for real-time audio capture with proper
        timing control, instead of sd.rec() which has latency issues.
        """

        chunk_duration = 0.1  # 100ms target per chunk
        chunk_samples = int(self.sample_rate * chunk_duration)

        start_time = time.time()
        max_end_time = start_time + session.max_duration
        initial_timeout_time = start_time + session.initial_timeout
        silent_start = None

        print(f"[VAD v3.0 InputStream] Recording (max {session.max_duration}s, "
              f"timeout {session.initial_timeout}s)", file=sys.stderr)

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype='int16',
                device=AUDIO_INPUT_DEVICE,
                blocksize=chunk_samples
            ) as stream:

                while True:
                    current_time = time.time()

                    # Hard time limit
                    if current_time >= max_end_time:
                        print(f"Max duration reached ({session.max_duration}s)", file=sys.stderr)
                        break

                    # Cancellation check
                    if session.cancel_event.is_set():
                        print("Recording cancelled", file=sys.stderr)
                        break

                    # Read audio chunk (non-blocking with timeout)
                    try:
                        chunk, overflowed = stream.read(chunk_samples)
                        if overflowed:
                            print("Audio buffer overflow", file=sys.stderr)
                    except Exception as e:
                        print(f"Stream read error: {e}", file=sys.stderr)
                        break

                    session.audio_buffer.append(chunk.copy())

                    # VAD calculation
                    rms = np.sqrt(np.mean(chunk.astype(np.float32) ** 2)) / 32767

                    if rms > session.silence_threshold:
                        silent_start = None
                        if not session.has_speech:
                            elapsed = current_time - start_time
                            print(f"Speech detected at {elapsed:.1f}s", file=sys.stderr)
                        session.has_speech = True
                    else:
                        if silent_start is None:
                            silent_start = current_time

                    # Early exit: no speech in initial timeout
                    if current_time >= initial_timeout_time and not session.has_speech:
                        print(f"No speech in first {session.initial_timeout}s, exiting",
                              file=sys.stderr)
                        break

                    # Normal exit: silence after speech
                    if session.has_speech and silent_start is not None:
                        silence_elapsed = current_time - silent_start
                        if silence_elapsed >= session.silence_duration:
                            print(f"Silence detected ({silence_elapsed:.1f}s), stopping",
                                  file=sys.stderr)
                            break

        except Exception as e:
            print(f"InputStream error: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)

    def _record_fixed_duration(self, session: VoiceSession):
        """Record for fixed duration (no VAD).

        FIX: Uses wall clock time to respect max_duration.
        """

        chunk_samples = self.sample_rate  # 1 second chunks for cancelability
        start_time = time.time()
        max_end_time = start_time + session.max_duration

        print(f"Recording fixed duration ({session.max_duration}s)...",
              file=sys.stderr)

        while True:
            current_time = time.time()

            # Check max duration
            if current_time >= max_end_time:
                print(f"Max duration reached ({session.max_duration}s)", file=sys.stderr)
                break

            if session.cancel_event.is_set():
                break

            # Calculate remaining time
            remaining_time = max_end_time - current_time
            samples_to_record = min(chunk_samples, int(remaining_time * self.sample_rate))

            if samples_to_record <= 0:
                break

            try:
                chunk = sd.rec(
                    samples_to_record,
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype='int16',
                    device=AUDIO_INPUT_DEVICE
                )
                sd.wait()
            except Exception as e:
                print(f"Recording error: {e}", file=sys.stderr)
                break

            session.audio_buffer.append(chunk)
            session.has_speech = True  # Assume speech for fixed duration

    def _save_audio(self, session: VoiceSession) -> Optional[str]:
        """Save recorded audio to temporary WAV file."""

        if not session.audio_buffer:
            return None

        try:
            audio = np.concatenate(session.audio_buffer)

            # Create temp file
            temp_file = tempfile.NamedTemporaryFile(
                delete=False,
                suffix='.wav',
                prefix=f'voice_{session.id}_'
            )
            temp_path = temp_file.name
            temp_file.close()

            sf.write(temp_path, audio, self.sample_rate)

            file_size = os.path.getsize(temp_path)
            print(f"Saved audio: {temp_path} ({file_size} bytes)", file=sys.stderr)

            return temp_path

        except Exception as e:
            print(f"Save audio error: {e}", file=sys.stderr)
            return None

    def _transcribe(self, session: VoiceSession) -> str:
        """Transcribe audio using ElevenLabs Scribe."""

        # Import here to avoid circular dependency
        from stt import transcribe_audio

        print(f"Transcribing session {session.id}...", file=sys.stderr)
        return transcribe_audio(session.audio_path, language=session.language)

    def _play_beep(self, frequency: int, duration_ms: int):
        """Play audio feedback beep using pygame (works with Bluetooth)."""

        try:
            # Method 1: pygame (works with Bluetooth audio)
            try:
                import pygame
                import io
                import wave

                # Generate beep
                num_samples = int(self.sample_rate * duration_ms / 1000)
                t = np.linspace(0, duration_ms / 1000, num_samples, False)
                beep = 0.7 * np.sin(2 * np.pi * frequency * t)  # Volume 0.7

                fade = int(num_samples * 0.1)
                beep[:fade] *= np.linspace(0, 1, fade)
                beep[-fade:] *= np.linspace(1, 0, fade)

                # Convert to 16-bit PCM
                beep_int16 = (beep * 32767).astype(np.int16)

                # Create WAV in memory
                wav_buffer = io.BytesIO()
                with wave.open(wav_buffer, 'wb') as wav_file:
                    wav_file.setnchannels(1)
                    wav_file.setsampwidth(2)
                    wav_file.setframerate(self.sample_rate)
                    wav_file.writeframes(beep_int16.tobytes())
                wav_buffer.seek(0)

                # Play with pygame
                pygame.mixer.init()
                sound = pygame.mixer.Sound(wav_buffer)
                sound.play()
                while pygame.mixer.get_busy():
                    pygame.time.Clock().tick(100)
                pygame.mixer.quit()
                return
            except ImportError:
                pass

            # Method 2: sounddevice fallback
            num_samples = int(self.sample_rate * duration_ms / 1000)
            t = np.linspace(0, duration_ms / 1000, num_samples, False)
            beep = 0.7 * np.sin(2 * np.pi * frequency * t)

            fade = int(num_samples * 0.1)
            beep[:fade] *= np.linspace(0, 1, fade)
            beep[-fade:] *= np.linspace(1, 0, fade)

            sd.play(beep.astype(np.float32), self.sample_rate,
                    device=AUDIO_OUTPUT_DEVICE)
            sd.wait()

        except Exception as e:
            # Beep failure is not critical
            print(f"Beep error (non-critical): {e}", file=sys.stderr)

    def _cleanup_session(self, session: VoiceSession):
        """Clean up session resources."""

        with self._cleanup_lock:
            # Remove audio file
            if session.audio_path and os.path.exists(session.audio_path):
                try:
                    os.remove(session.audio_path)
                except Exception:
                    pass

            # Clear buffer
            session.audio_buffer.clear()

    def _cleanup_old_sessions(self):
        """Remove sessions older than max age."""

        now = time.time()
        to_remove = []

        for session_id, session in self.sessions.items():
            # Remove old completed/failed sessions
            if not session.is_active:
                if now - session.started_at > self._session_max_age:
                    self._cleanup_session(session)
                    to_remove.append(session_id)

        for session_id in to_remove:
            del self.sessions[session_id]

        if to_remove:
            print(f"Cleaned up {len(to_remove)} old sessions", file=sys.stderr)


# =============================================================================
# SINGLETON INSTANCE
# =============================================================================

_manager: Optional[VoiceSessionManager] = None


def get_manager() -> VoiceSessionManager:
    """Get or create the global session manager singleton."""
    global _manager
    if _manager is None:
        _manager = VoiceSessionManager()
    return _manager


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def start_session(**kwargs) -> Dict:
    """Start a new voice session. See VoiceSessionManager.start_session()."""
    return get_manager().start_session(**kwargs)


def poll_session(session_id: str) -> Dict:
    """Poll session status. See VoiceSessionManager.poll_session()."""
    return get_manager().poll_session(session_id)


def stop_session(session_id: str) -> Dict:
    """Stop/cancel session. See VoiceSessionManager.stop_session()."""
    return get_manager().stop_session(session_id)


def list_sessions() -> Dict:
    """List all sessions. See VoiceSessionManager.list_sessions()."""
    return get_manager().list_sessions()


# =============================================================================
# CLI TEST
# =============================================================================

if __name__ == "__main__":
    print("Testing VoiceSessionManager...")
    print("-" * 50)

    manager = VoiceSessionManager()

    # Start session
    result = manager.start_session(max_duration=10, initial_timeout=3.0)
    session_id = result.get("session_id")

    if not session_id:
        print(f"Failed to start: {result}")
        sys.exit(1)

    print(f"Started session: {session_id}")

    # Poll until done
    while True:
        status = manager.poll_session(session_id)
        print(f"  Status: {status['status']} ({status['elapsed']}s)")

        if status['status'] in ('done', 'error', 'cancelled', 'timeout', 'not_found'):
            break

        time.sleep(0.5)

    print("-" * 50)
    print(f"Final result: {status}")

    if status.get('transcript'):
        print(f"Transcript: {status['transcript']}")
