#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice Client
===================

Client library for communicating with the Voice Daemon.
Used by Claude Code and other tools to interact with the voice system.

Usage:
    from voice_client import VoiceClient

    client = VoiceClient()
    if client.connect():
        client.start_recording()
        # Wait for transcription
        result = client.wait_for_transcription()
        print(result)
        client.disconnect()

    # Or use quick functions:
    from voice_client import quick_record
    text = quick_record()

Version: 8.0.0
"""

import sys
import socket
import json
import time
import threading
from pathlib import Path
from typing import Optional, Callable

# Add voice module to path
VOICE_ROOT = Path(__file__).parent
sys.path.insert(0, str(VOICE_ROOT))

from voice_state import (
    VoiceStatus, VoiceState, MessageType, SocketMessage,
    SOCKET_PATH, SOCKET_PORT, is_daemon_running
)


class VoiceClient:
    """
    Client for communicating with the Voice Daemon.

    Provides:
    - Connection management
    - Command sending (start/stop recording)
    - Status monitoring
    - Transcription callbacks
    """

    def __init__(self):
        self.socket: Optional[socket.socket] = None
        self.connected = False
        self.listener_thread: Optional[threading.Thread] = None
        self.listening = False

        # Callbacks
        self.on_status_change: Optional[Callable[[VoiceState], None]] = None
        self.on_transcription: Optional[Callable[[str], None]] = None
        self.on_error: Optional[Callable[[str], None]] = None

        # State
        self.current_status = VoiceStatus.IDLE
        self.last_transcription: Optional[str] = None
        self._transcription_event = threading.Event()

    def connect(self, timeout: float = 5.0) -> bool:
        """
        Connect to the daemon.

        Args:
            timeout: Connection timeout in seconds

        Returns:
            True if connected successfully
        """
        if self.connected:
            return True

        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(timeout)
            self.socket.connect((SOCKET_PATH, SOCKET_PORT))
            self.connected = True

            # Start listener thread
            self.listening = True
            self.listener_thread = threading.Thread(target=self._listen, daemon=True)
            self.listener_thread.start()

            return True

        except Exception as e:
            if self.on_error:
                self.on_error(f"Connection failed: {e}")
            return False

    def disconnect(self):
        """Disconnect from the daemon."""
        self.listening = False
        self.connected = False

        if self.socket:
            try:
                self.socket.close()
            except Exception:
                pass
            self.socket = None

    def _listen(self):
        """Listen for messages from the daemon."""
        while self.listening and self.socket:
            try:
                data = self.socket.recv(4096)
                if not data:
                    break

                msg = SocketMessage.from_json(data.decode('utf-8'))
                self._handle_message(msg)

            except socket.timeout:
                continue
            except Exception:
                break

        self.connected = False

    def _handle_message(self, msg: SocketMessage):
        """Handle incoming message from daemon."""
        if msg.type == MessageType.STATUS_UPDATE:
            status = VoiceStatus(msg.data.get('status', 'idle'))
            self.current_status = status

            if self.on_status_change:
                state = VoiceState.from_dict(msg.data)
                self.on_status_change(state)

        elif msg.type == MessageType.TRANSCRIPTION:
            text = msg.data.get('text', '')
            self.last_transcription = text
            self._transcription_event.set()

            if self.on_transcription:
                self.on_transcription(text)

        elif msg.type == MessageType.ERROR:
            error = msg.data.get('error', 'Unknown error')
            if self.on_error:
                self.on_error(error)

    def _send(self, msg: SocketMessage) -> Optional[SocketMessage]:
        """Send message and wait for response."""
        if not self.connected or not self.socket:
            return None

        try:
            self.socket.send(msg.to_json().encode('utf-8'))

            # Wait for response (with timeout)
            self.socket.settimeout(5.0)
            data = self.socket.recv(4096)

            if data:
                return SocketMessage.from_json(data.decode('utf-8'))

        except Exception:
            pass

        return None

    def start_recording(self) -> bool:
        """
        Start voice recording.

        Returns:
            True if command was sent successfully
        """
        msg = SocketMessage(MessageType.START_RECORDING)
        response = self._send(msg)
        return response is not None and response.type == MessageType.ACK

    def stop_recording(self) -> bool:
        """
        Stop voice recording.

        Returns:
            True if command was sent successfully
        """
        msg = SocketMessage(MessageType.STOP_RECORDING)
        response = self._send(msg)
        return response is not None and response.type == MessageType.ACK

    def cancel(self) -> bool:
        """Cancel current operation."""
        msg = SocketMessage(MessageType.CANCEL)
        response = self._send(msg)
        return response is not None

    def get_status(self) -> Optional[VoiceState]:
        """
        Get current daemon status.

        Returns:
            VoiceState object or None if failed
        """
        msg = SocketMessage(MessageType.GET_STATUS)
        response = self._send(msg)

        if response and response.type == MessageType.STATUS_UPDATE:
            return VoiceState.from_dict(response.data)

        return None

    def shutdown(self) -> bool:
        """Shutdown the daemon."""
        msg = SocketMessage(MessageType.SHUTDOWN)
        response = self._send(msg)
        return response is not None

    def wait_for_transcription(self, timeout: float = 30.0) -> Optional[str]:
        """
        Wait for a transcription result.

        Args:
            timeout: Maximum time to wait in seconds

        Returns:
            Transcription text or None if timeout
        """
        self._transcription_event.clear()
        self.last_transcription = None

        if self._transcription_event.wait(timeout=timeout):
            return self.last_transcription

        return None

    def record_and_wait(self, timeout: float = 30.0) -> Optional[str]:
        """
        Start recording and wait for transcription.

        Args:
            timeout: Maximum time to wait

        Returns:
            Transcription text or None
        """
        self._transcription_event.clear()
        self.last_transcription = None

        if self.start_recording():
            return self.wait_for_transcription(timeout)

        return None


# =============================================================================
# QUICK FUNCTIONS
# =============================================================================

def is_connected() -> bool:
    """Check if daemon is running and accessible."""
    return is_daemon_running()


def quick_status() -> Optional[dict]:
    """Get daemon status quickly."""
    client = VoiceClient()
    if client.connect(timeout=2.0):
        try:
            state = client.get_status()
            if state:
                return state.to_dict()
        finally:
            client.disconnect()
    return None


def quick_record(timeout: float = 30.0) -> Optional[str]:
    """
    Quick voice recording.

    Connects to daemon, triggers recording, waits for result.

    Args:
        timeout: Maximum time to wait

    Returns:
        Transcription text or None
    """
    client = VoiceClient()

    if not client.connect(timeout=2.0):
        print("[ERROR] Could not connect to daemon")
        print("[INFO] Start daemon with: python voice_daemon.py start")
        return None

    try:
        result = client.record_and_wait(timeout=timeout)
        return result
    finally:
        client.disconnect()


def quick_shutdown() -> bool:
    """Shutdown the daemon."""
    client = VoiceClient()
    if client.connect(timeout=2.0):
        try:
            return client.shutdown()
        finally:
            client.disconnect()
    return False


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="CODEXA Voice Client")
    parser.add_argument('command', nargs='?', default='status',
                        choices=['status', 'record', 'stop', 'shutdown'],
                        help='Command to run')
    parser.add_argument('--timeout', '-t', type=float, default=30.0,
                        help='Timeout in seconds')

    args = parser.parse_args()

    if args.command == 'status':
        status = quick_status()
        if status:
            print(f"Status: {status.get('status', 'unknown')}")
            print(f"Mode: {status.get('mode', 'unknown')}")
            print(f"Commands: {status.get('total_commands', 0)}")
            if status.get('last_transcript'):
                print(f"Last: \"{status['last_transcript']}\"")
        else:
            print("Daemon not running")

    elif args.command == 'record':
        print("Recording... (speak now)")
        result = quick_record(timeout=args.timeout)
        if result:
            print(f"Result: \"{result}\"")
        else:
            print("No result")

    elif args.command == 'shutdown':
        if quick_shutdown():
            print("Shutdown signal sent")
        else:
            print("Could not connect")
