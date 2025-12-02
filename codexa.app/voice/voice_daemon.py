#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice Daemon v8.0
========================

Background daemon for continuous voice interaction.
Runs as a separate process with socket server + hotkey listener.

Features:
- Socket server for IPC (port 5557)
- Global hotkey listener (F12)
- Push-to-talk and toggle modes
- Continuous state broadcasting
- TTS responses

Usage:
    python voice_daemon_v8.py start    # Start daemon
    python voice_daemon_v8.py stop     # Stop daemon
    python voice_daemon_v8.py status   # Check status

Version: 8.0.0
"""

import sys
import os
import json
import time
import socket
import threading
import tempfile
import signal
import atexit
from pathlib import Path
from typing import Optional, List

# Fix encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Add voice module to path
VOICE_ROOT = Path(__file__).parent
sys.path.insert(0, str(VOICE_ROOT))

# Load environment
from dotenv import load_dotenv
load_dotenv(dotenv_path=VOICE_ROOT.parent.parent / '.env')

# Audio imports
try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    HAS_AUDIO = True
except ImportError:
    HAS_AUDIO = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# Local imports
from voice_state import (
    VoiceStatus, VoiceMode, VoiceState, VoiceConfig,
    MessageType, SocketMessage,
    SOCKET_PATH, SOCKET_PORT
)

# =============================================================================
# PID FILE
# =============================================================================

PID_FILE = VOICE_ROOT / '.voice_daemon.pid'


def write_pid():
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))


def read_pid() -> Optional[int]:
    try:
        if PID_FILE.exists():
            with open(PID_FILE, 'r') as f:
                return int(f.read().strip())
    except Exception:
        pass
    return None


def remove_pid():
    try:
        if PID_FILE.exists():
            PID_FILE.unlink()
    except Exception:
        pass


def is_process_running(pid: int) -> bool:
    try:
        if sys.platform == 'win32':
            import subprocess
            result = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'], capture_output=True, text=True)
            return str(pid) in result.stdout
        else:
            os.kill(pid, 0)
            return True
    except Exception:
        return False


# =============================================================================
# VOICE DAEMON CLASS
# =============================================================================

class VoiceDaemon:
    """Background daemon for voice capture with hotkey support."""

    def __init__(self, config: Optional[VoiceConfig] = None):
        self.config = config or VoiceConfig.load()
        self.state = VoiceState()
        self.running = False

        self.server_socket: Optional[socket.socket] = None
        self.clients: List[socket.socket] = []
        self.client_lock = threading.Lock()

        self.sample_rate = self.config.sample_rate
        self.device = self.config.input_device
        self.audio_data: List = []
        self.audio_levels: List[float] = []
        self.current_level = 0.0

        self.is_recording = False
        self.speech_detected = False
        self.silence_frames = 0
        self.recording_thread: Optional[threading.Thread] = None

    def start(self):
        if self.running:
            return

        self.running = True
        write_pid()

        self._start_socket_server()
        self._start_hotkey_listener()

        self.state.status = VoiceStatus.IDLE
        self.state.save()
        self._broadcast_status()

        print("=" * 50)
        print("  CODEXA Voice Daemon v8.0")
        print("=" * 50)
        print(f"  Socket: {SOCKET_PATH}:{SOCKET_PORT}")
        print(f"  Hotkey: {self.config.hotkey.upper()}")
        print(f"  Mode:   {self.config.mode.value}")
        print(f"  Device: {self.device}")
        print("=" * 50)
        print(f"  Press {self.config.hotkey.upper()} to talk")
        print("  Ctrl+C to stop")
        print("=" * 50)

        try:
            while self.running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def stop(self):
        print("\n[DAEMON] Stopping...")
        self.running = False
        self.is_recording = False

        if self.server_socket:
            try:
                self.server_socket.close()
            except Exception:
                pass

        with self.client_lock:
            for client in self.clients:
                try:
                    client.close()
                except Exception:
                    pass
            self.clients.clear()

        self.state.status = VoiceStatus.STOPPED
        self.state.save()
        remove_pid()
        print("[DAEMON] Stopped")

    def _start_socket_server(self):
        def server_thread():
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.settimeout(1.0)

            try:
                self.server_socket.bind((SOCKET_PATH, SOCKET_PORT))
                self.server_socket.listen(5)

                while self.running:
                    try:
                        client, addr = self.server_socket.accept()
                        client.settimeout(1.0)
                        with self.client_lock:
                            self.clients.append(client)
                        threading.Thread(target=self._handle_client, args=(client,), daemon=True).start()
                    except socket.timeout:
                        continue
                    except Exception as e:
                        if self.running:
                            print(f"[DAEMON] Socket error: {e}")
                        break
            except Exception as e:
                print(f"[DAEMON] Server error: {e}")

        threading.Thread(target=server_thread, daemon=True).start()

    def _handle_client(self, client: socket.socket):
        try:
            while self.running:
                try:
                    data = client.recv(4096)
                    if not data:
                        break
                    msg = SocketMessage.from_json(data.decode('utf-8'))
                    response = self._handle_message(msg)
                    if response:
                        client.send(response.to_json().encode('utf-8'))
                except socket.timeout:
                    continue
                except Exception:
                    break
        finally:
            with self.client_lock:
                if client in self.clients:
                    self.clients.remove(client)
            try:
                client.close()
            except Exception:
                pass

    def _handle_message(self, msg: SocketMessage) -> Optional[SocketMessage]:
        if msg.type == MessageType.START_RECORDING:
            self._start_recording()
            return SocketMessage(MessageType.ACK, {'status': 'recording_started'})
        elif msg.type == MessageType.STOP_RECORDING:
            self._stop_recording()
            return SocketMessage(MessageType.ACK, {'status': 'recording_stopped'})
        elif msg.type == MessageType.CANCEL:
            self.is_recording = False
            self.state.status = VoiceStatus.IDLE
            return SocketMessage(MessageType.ACK, {'status': 'cancelled'})
        elif msg.type == MessageType.GET_STATUS:
            return SocketMessage(MessageType.STATUS_UPDATE, self.state.to_dict())
        elif msg.type == MessageType.SET_MODE:
            mode = VoiceMode(msg.data.get('mode', 'push_to_talk'))
            self.config.mode = mode
            self.state.mode = mode
            return SocketMessage(MessageType.ACK, {'mode': mode.value})
        elif msg.type == MessageType.SHUTDOWN:
            self.running = False
            return SocketMessage(MessageType.ACK, {'status': 'shutting_down'})
        return None

    def _broadcast_status(self):
        msg = SocketMessage(MessageType.STATUS_UPDATE, self.state.to_dict())
        data = msg.to_json().encode('utf-8')
        with self.client_lock:
            for client in self.clients[:]:
                try:
                    client.send(data)
                except Exception:
                    self.clients.remove(client)

    def _broadcast_transcription(self, text: str):
        msg = SocketMessage(MessageType.TRANSCRIPTION, {'text': text})
        data = msg.to_json().encode('utf-8')
        with self.client_lock:
            for client in self.clients[:]:
                try:
                    client.send(data)
                except Exception:
                    self.clients.remove(client)

    def _start_hotkey_listener(self):
        try:
            from pynput import keyboard
            hotkey = self.config.hotkey.lower()
            key_map = {
                'f12': keyboard.Key.f12, 'f11': keyboard.Key.f11,
                'f10': keyboard.Key.f10, 'f9': keyboard.Key.f9,
                'f8': keyboard.Key.f8, 'f7': keyboard.Key.f7,
            }
            target_key = key_map.get(hotkey, keyboard.Key.f12)

            def on_press(key):
                if key == target_key:
                    if self.config.mode == VoiceMode.PUSH_TO_TALK:
                        if not self.is_recording:
                            self._start_recording()
                    elif self.config.mode == VoiceMode.TOGGLE:
                        if self.is_recording:
                            self._stop_recording()
                        else:
                            self._start_recording()

            def on_release(key):
                if key == target_key:
                    if self.config.mode == VoiceMode.PUSH_TO_TALK:
                        if self.is_recording:
                            self._stop_recording()

            listener = keyboard.Listener(on_press=on_press, on_release=on_release)
            listener.daemon = True
            listener.start()
            print(f"[DAEMON] Hotkey: {hotkey.upper()}")
        except ImportError:
            print("[DAEMON] pynput not installed - pip install pynput")
        except Exception as e:
            print(f"[DAEMON] Hotkey error: {e}")

    def _start_recording(self):
        if self.is_recording:
            return
        self.is_recording = True
        self.speech_detected = False
        self.silence_frames = 0
        self.audio_data = []
        self.audio_levels = []

        self._play_beep(800, 150)
        self.state.status = VoiceStatus.RECORDING
        self.state.is_recording = True
        self.state.recording_start = time.time()
        self._broadcast_status()
        print("[DAEMON] Recording...")

        self.recording_thread = threading.Thread(target=self._record_audio, daemon=True)
        self.recording_thread.start()

    def _stop_recording(self):
        if not self.is_recording:
            return
        self.is_recording = False
        if self.recording_thread:
            self.recording_thread.join(timeout=2.0)
        self._play_beep(1200, 150)
        print("[DAEMON] Processing...")
        self._process_audio()

    def _record_audio(self):
        if not HAS_AUDIO:
            return

        def callback(indata, frames, time_info, status):
            if not self.is_recording:
                raise sd.CallbackAbort()
            self.audio_data.append(indata.copy())
            rms = float(np.sqrt(np.mean(indata**2)))
            self.current_level = rms
            self.audio_levels.append(rms)
            self.state.audio_level = rms
            if rms > self.config.silence_threshold:
                self.speech_detected = True
                self.silence_frames = 0
            elif self.speech_detected:
                self.silence_frames += frames

        try:
            start_time = time.time()
            with sd.InputStream(samplerate=self.sample_rate, device=self.device,
                              channels=1, callback=callback, dtype='float32'):
                while self.is_recording:
                    elapsed = time.time() - start_time
                    self.state.recording_duration = elapsed
                    if elapsed >= self.config.max_duration:
                        break
                    if self.speech_detected and self.silence_frames > self.sample_rate * self.config.silence_duration:
                        break
                    if not self.speech_detected and elapsed >= self.config.initial_timeout:
                        break
                    time.sleep(0.05)
        except sd.CallbackAbort:
            pass
        except Exception as e:
            print(f"[DAEMON] Recording error: {e}")
        finally:
            self.is_recording = False

    def _process_audio(self):
        if not self.audio_data:
            self.state.status = VoiceStatus.IDLE
            self._broadcast_status()
            return

        self.state.status = VoiceStatus.PROCESSING
        self.state.is_recording = False
        self._broadcast_status()

        if not self.speech_detected:
            self._play_beep(400, 300)
            self.state.status = VoiceStatus.IDLE
            self.state.last_error = "No speech"
            self._broadcast_status()
            print("[DAEMON] No speech")
            return

        audio = np.concatenate(self.audio_data)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            sf.write(f.name, audio, self.sample_rate)
            audio_path = f.name

        self.state.status = VoiceStatus.TRANSCRIBING
        self._broadcast_status()

        transcript = self._transcribe_audio(audio_path)
        try:
            os.unlink(audio_path)
        except Exception:
            pass

        if transcript:
            print(f"[DAEMON] \"{transcript}\"")
            self.state.last_transcript = transcript
            self.state.total_commands += 1
            self.state.last_command_time = time.time()
            self._broadcast_transcription(transcript)
            if self.config.tts_enabled:
                self.state.status = VoiceStatus.SPEAKING
                self._broadcast_status()
                self._speak(f"Entendi: {transcript}")
        else:
            print("[DAEMON] Transcription failed")
            self.state.last_error = "Transcription failed"

        self.state.status = VoiceStatus.IDLE
        self._broadcast_status()

    def _transcribe_audio(self, audio_path: str) -> Optional[str]:
        if not HAS_REQUESTS:
            return None
        api_key = os.getenv('ELEVENLABS_API_KEY')
        if not api_key:
            return None
        try:
            with open(audio_path, 'rb') as f:
                response = requests.post(
                    'https://api.elevenlabs.io/v1/speech-to-text',
                    headers={'xi-api-key': api_key},
                    files={'file': ('audio.wav', f, 'audio/wav')},
                    data={'model_id': 'scribe_v1', 'language_code': self.config.language},
                    timeout=30
                )
            if response.ok:
                text = response.json().get('text', '').strip()
                if text and not text.startswith('('):
                    return text
        except Exception as e:
            print(f"[DAEMON] STT error: {e}")
        return None

    def _speak(self, text: str):
        try:
            from tts import speak
            speak(text)
        except Exception as e:
            print(f"[DAEMON] TTS error: {e}")

    def _play_beep(self, freq: int, dur: int):
        try:
            if sys.platform == 'win32':
                import winsound
                winsound.Beep(freq, dur)
        except Exception:
            pass


# =============================================================================
# CLI
# =============================================================================

def cmd_start():
    pid = read_pid()
    if pid and is_process_running(pid):
        print(f"[ERROR] Already running (PID: {pid})")
        return False
    daemon = VoiceDaemon()
    atexit.register(daemon.stop)
    signal.signal(signal.SIGTERM, lambda s, f: daemon.stop())
    signal.signal(signal.SIGINT, lambda s, f: daemon.stop())
    daemon.start()
    return True


def cmd_stop():
    pid = read_pid()
    if not pid or not is_process_running(pid):
        print("[INFO] Not running")
        remove_pid()
        return True
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((SOCKET_PATH, SOCKET_PORT))
        msg = SocketMessage(MessageType.SHUTDOWN)
        s.send(msg.to_json().encode('utf-8'))
        s.close()
        print("[INFO] Shutdown sent")
        time.sleep(1)
    except Exception:
        pass
    if is_process_running(pid):
        try:
            if sys.platform == 'win32':
                os.system(f'taskkill /F /PID {pid}')
            else:
                os.kill(pid, signal.SIGTERM)
        except Exception:
            pass
    remove_pid()
    return True


def cmd_status():
    pid = read_pid()
    if not pid or not is_process_running(pid):
        print("[STATUS] NOT RUNNING")
        return
    print(f"[STATUS] RUNNING (PID: {pid})")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((SOCKET_PATH, SOCKET_PORT))
        msg = SocketMessage(MessageType.GET_STATUS)
        s.send(msg.to_json().encode('utf-8'))
        response = s.recv(4096)
        s.close()
        if response:
            resp_msg = SocketMessage.from_json(response.decode('utf-8'))
            state = resp_msg.data
            print(f"[STATUS] Voice: {state.get('status', '?')}")
            print(f"[STATUS] Mode: {state.get('mode', '?')}")
            print(f"[STATUS] Commands: {state.get('total_commands', 0)}")
            if state.get('last_transcript'):
                t = state['last_transcript']
                print(f"[STATUS] Last: \"{t[:40]}\"")
    except Exception as e:
        print(f"[STATUS] Error: {e}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="CODEXA Voice Daemon v8.0")
    parser.add_argument('command', nargs='?', default='start', choices=['start', 'stop', 'status', 'restart'])
    args = parser.parse_args()

    if args.command == 'start':
        cmd_start()
    elif args.command == 'stop':
        cmd_stop()
    elif args.command == 'status':
        cmd_status()
    elif args.command == 'restart':
        cmd_stop()
        time.sleep(1)
        cmd_start()
