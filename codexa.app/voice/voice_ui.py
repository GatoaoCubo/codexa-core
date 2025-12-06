#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CODEXA Voice UI v1.0 - Flask Edition
====================================

Interface web local para sistema de voz com feedback visual.

Uso:
    python voice_ui.py
    # Abre em http://localhost:7860

Requer:
    pip install flask sounddevice numpy
"""

from flask import Flask, render_template_string, jsonify, request
import numpy as np
import sounddevice as sd
import threading
import time
import asyncio
import tempfile
import wave
from pathlib import Path

# Import local modules
try:
    from config import (
        TTS_TO_RECORD_DELAY,
        VAD_SILENCE_DURATION,
        VAD_MAX_DURATION,
        VOICE_INITIAL_TIMEOUT,
    )
    from tts import speak
    from stt import transcribe_audio
    CONFIG_LOADED = True
except ImportError:
    # Fallback defaults if running standalone
    TTS_TO_RECORD_DELAY = 1.5
    VAD_SILENCE_DURATION = 2.0
    VAD_MAX_DURATION = 15.0
    VOICE_INITIAL_TIMEOUT = 5.0
    CONFIG_LOADED = False

app = Flask(__name__)

# =============================================================================
# GLOBAL STATE
# =============================================================================

class VoiceState:
    """Manage voice recording state."""

    def __init__(self):
        self.is_recording = False
        self.audio_data = []
        self.sample_rate = 16000
        self.has_speech = False
        self.start_time = None
        self.level = 0.0
        self.status = "idle"
        self.transcript = ""
        self.error = ""
        self.elapsed = 0.0
        self.max_duration = 15.0

    def reset(self):
        self.is_recording = False
        self.audio_data = []
        self.has_speech = False
        self.start_time = None
        self.level = 0.0
        self.status = "idle"
        self.transcript = ""
        self.error = ""
        self.elapsed = 0.0

    def to_dict(self):
        return {
            "status": self.status,
            "level": self.level,
            "elapsed": self.elapsed,
            "max_duration": self.max_duration,
            "has_speech": self.has_speech,
            "transcript": self.transcript,
            "error": self.error
        }


state = VoiceState()


# =============================================================================
# AUDIO FUNCTIONS
# =============================================================================

def get_audio_level(audio_chunk: np.ndarray) -> float:
    """Calculate RMS level of audio chunk (0-1)."""
    if len(audio_chunk) == 0:
        return 0.0
    rms = np.sqrt(np.mean(audio_chunk.astype(np.float32) ** 2))
    return min(1.0, rms / 3000)


def record_thread(use_tts: bool, duration: float):
    """Background thread for recording."""
    global state

    state.reset()
    state.max_duration = duration
    state.status = "preparing"

    # Step 1: TTS
    if use_tts and CONFIG_LOADED:
        state.status = "tts"
        try:
            asyncio.run(speak("Pode falar"))
        except Exception as e:
            print(f"TTS error: {e}")
        time.sleep(TTS_TO_RECORD_DELAY)

    # Step 2: Record
    state.status = "recording"
    state.is_recording = True
    state.start_time = time.time()
    audio_chunks = []

    try:
        with sd.InputStream(
            samplerate=state.sample_rate,
            channels=1,
            dtype='int16',
            blocksize=1024
        ) as stream:
            while state.is_recording:
                state.elapsed = time.time() - state.start_time

                if state.elapsed >= duration:
                    break

                data, _ = stream.read(1024)
                audio_chunks.append(data.copy())

                state.level = get_audio_level(data)
                if state.level > 0.02:
                    state.has_speech = True

                time.sleep(0.05)

    except Exception as e:
        state.status = "error"
        state.error = str(e)
        return

    state.is_recording = False

    # Step 3: Transcribe
    if not audio_chunks:
        state.status = "error"
        state.error = "Nenhum audio capturado"
        return

    state.status = "transcribing"
    audio_data = np.concatenate(audio_chunks, axis=0)

    try:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            temp_path = f.name
            with wave.open(f.name, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(state.sample_rate)
                wf.writeframes(audio_data.tobytes())

        if CONFIG_LOADED:
            transcript = asyncio.run(transcribe_audio(temp_path))
        else:
            transcript = "[Transcricao simulada - config nao carregado]"

        Path(temp_path).unlink(missing_ok=True)

        if transcript:
            state.transcript = transcript
            state.status = "done"
        else:
            state.status = "error"
            state.error = "Transcricao vazia"

    except Exception as e:
        state.status = "error"
        state.error = str(e)


# =============================================================================
# HTML TEMPLATE
# =============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CODEXA Voice UI</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #fff;
        }
        .container {
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            width: 100%;
            max-width: 500px;
            text-align: center;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 10px;
            color: #0ea5e9;
        }
        .subtitle {
            color: #94a3b8;
            margin-bottom: 30px;
        }
        .status-icon {
            font-size: 80px;
            margin: 20px 0;
            transition: all 0.3s;
        }
        .status-text {
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 10px;
        }
        .status-detail {
            color: #94a3b8;
            font-size: 14px;
            margin-bottom: 20px;
        }
        .level-bar {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            height: 20px;
            margin: 15px 0;
            overflow: hidden;
        }
        .level-fill {
            height: 100%;
            background: linear-gradient(90deg, #22c55e, #10b981);
            transition: width 0.1s;
            border-radius: 10px;
        }
        .time-bar {
            background: rgba(255,255,255,0.1);
            border-radius: 5px;
            height: 8px;
            margin: 10px 0;
            overflow: hidden;
        }
        .time-fill {
            height: 100%;
            background: #3b82f6;
            transition: width 0.5s;
        }
        .transcript-box {
            background: rgba(0,0,0,0.3);
            border-radius: 10px;
            padding: 15px;
            margin: 20px 0;
            min-height: 60px;
            text-align: left;
            font-size: 16px;
        }
        .controls {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
        }
        button {
            padding: 15px 30px;
            font-size: 16px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s;
            font-weight: 600;
        }
        .btn-record {
            background: linear-gradient(135deg, #ef4444, #dc2626);
            color: white;
        }
        .btn-record:hover { transform: scale(1.05); }
        .btn-record:disabled {
            background: #6b7280;
            cursor: not-allowed;
            transform: none;
        }
        .btn-stop {
            background: rgba(255,255,255,0.2);
            color: white;
        }
        .btn-stop:hover { background: rgba(255,255,255,0.3); }
        .options {
            display: flex;
            gap: 20px;
            justify-content: center;
            margin: 20px 0;
            flex-wrap: wrap;
        }
        .option {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #94a3b8;
        }
        input[type="checkbox"] {
            width: 18px;
            height: 18px;
            accent-color: #0ea5e9;
        }
        input[type="range"] {
            width: 100px;
            accent-color: #0ea5e9;
        }
        .config-info {
            margin-top: 30px;
            padding-top: 20px;
            border-top: 1px solid rgba(255,255,255,0.1);
            font-size: 12px;
            color: #64748b;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.7; transform: scale(1.1); }
        }
        .recording .status-icon { animation: pulse 1s infinite; }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        .transcribing .status-icon { animation: spin 2s linear infinite; }
    </style>
</head>
<body>
    <div class="container">
        <h1>CODEXA Voice UI v1.0</h1>
        <p class="subtitle">Interface visual para sistema de voz</p>

        <div id="statusArea">
            <div class="status-icon" id="statusIcon">&#127908;</div>
            <div class="status-text" id="statusText">Pronto para gravar</div>
            <div class="status-detail" id="statusDetail">Clique em Gravar para iniciar</div>
        </div>

        <div id="levelArea" style="display:none;">
            <div style="font-size: 12px; color: #94a3b8;">Nivel de audio</div>
            <div class="level-bar">
                <div class="level-fill" id="levelFill" style="width: 0%"></div>
            </div>
            <div style="font-size: 12px; color: #94a3b8;">
                Tempo: <span id="elapsed">0.0</span>s / <span id="maxDur">15</span>s
            </div>
            <div class="time-bar">
                <div class="time-fill" id="timeFill" style="width: 0%"></div>
            </div>
        </div>

        <div class="transcript-box" id="transcriptBox">
            <span style="color: #64748b;">Transcricao aparecera aqui...</span>
        </div>

        <div class="options">
            <label class="option">
                <input type="checkbox" id="useTts" checked>
                TTS "Pode falar"
            </label>
            <label class="option">
                Duracao:
                <input type="range" id="duration" min="5" max="30" value="15">
                <span id="durationVal">15</span>s
            </label>
        </div>

        <div class="controls">
            <button class="btn-record" id="btnRecord" onclick="startRecording()">
                &#127908; Gravar
            </button>
            <button class="btn-stop" id="btnStop" onclick="stopRecording()">
                &#9209; Parar
            </button>
        </div>

        <div class="config-info">
            <strong>Config v10.1:</strong>
            TTS->Record delay: {{ tts_delay }}s |
            VAD silence: {{ vad_silence }}s |
            Max duration: {{ max_dur }}s
        </div>
    </div>

    <script>
        let pollInterval = null;

        document.getElementById('duration').addEventListener('input', (e) => {
            document.getElementById('durationVal').textContent = e.target.value;
            document.getElementById('maxDur').textContent = e.target.value;
        });

        function startRecording() {
            const useTts = document.getElementById('useTts').checked;
            const duration = document.getElementById('duration').value;

            fetch('/start', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({use_tts: useTts, duration: parseInt(duration)})
            });

            document.getElementById('btnRecord').disabled = true;
            pollInterval = setInterval(pollStatus, 100);
        }

        function stopRecording() {
            fetch('/stop', {method: 'POST'});
        }

        function pollStatus() {
            fetch('/status')
                .then(r => r.json())
                .then(data => updateUI(data));
        }

        function updateUI(data) {
            const statusArea = document.getElementById('statusArea');
            const icon = document.getElementById('statusIcon');
            const text = document.getElementById('statusText');
            const detail = document.getElementById('statusDetail');
            const levelArea = document.getElementById('levelArea');
            const levelFill = document.getElementById('levelFill');
            const elapsed = document.getElementById('elapsed');
            const timeFill = document.getElementById('timeFill');
            const transcript = document.getElementById('transcriptBox');
            const btn = document.getElementById('btnRecord');

            statusArea.className = data.status;

            switch(data.status) {
                case 'idle':
                    icon.innerHTML = '&#127908;';
                    text.textContent = 'Pronto para gravar';
                    detail.textContent = 'Clique em Gravar para iniciar';
                    levelArea.style.display = 'none';
                    btn.disabled = false;
                    clearInterval(pollInterval);
                    break;
                case 'tts':
                    icon.innerHTML = '&#128266;';
                    text.textContent = 'Aguardando TTS...';
                    detail.textContent = 'Preparando para gravar';
                    levelArea.style.display = 'none';
                    break;
                case 'recording':
                    icon.innerHTML = '&#128308;';
                    text.textContent = 'GRAVANDO';
                    detail.textContent = data.has_speech ? '&#127908; Fala detectada!' : 'Aguardando fala...';
                    levelArea.style.display = 'block';
                    levelFill.style.width = (data.level * 100) + '%';
                    levelFill.style.background = data.level > 0.02 ? 'linear-gradient(90deg, #22c55e, #10b981)' : '#64748b';
                    elapsed.textContent = data.elapsed.toFixed(1);
                    timeFill.style.width = ((data.elapsed / data.max_duration) * 100) + '%';
                    break;
                case 'transcribing':
                    icon.innerHTML = '&#9203;';
                    text.textContent = 'Transcrevendo...';
                    detail.textContent = 'Processando audio';
                    levelArea.style.display = 'none';
                    break;
                case 'done':
                    icon.innerHTML = '&#9989;';
                    text.textContent = 'Concluido!';
                    detail.textContent = '';
                    levelArea.style.display = 'none';
                    transcript.innerHTML = data.transcript || '<span style="color:#64748b">Vazio</span>';
                    btn.disabled = false;
                    clearInterval(pollInterval);
                    break;
                case 'error':
                    icon.innerHTML = '&#10060;';
                    text.textContent = 'Erro';
                    detail.textContent = data.error;
                    levelArea.style.display = 'none';
                    btn.disabled = false;
                    clearInterval(pollInterval);
                    break;
            }
        }
    </script>
</body>
</html>
"""


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def index():
    return render_template_string(
        HTML_TEMPLATE,
        tts_delay=TTS_TO_RECORD_DELAY,
        vad_silence=VAD_SILENCE_DURATION,
        max_dur=VAD_MAX_DURATION
    )


@app.route('/status')
def get_status():
    return jsonify(state.to_dict())


@app.route('/start', methods=['POST'])
def start_recording():
    data = request.get_json() or {}
    use_tts = data.get('use_tts', True)
    duration = data.get('duration', 15)

    thread = threading.Thread(target=record_thread, args=(use_tts, duration))
    thread.daemon = True
    thread.start()

    return jsonify({"status": "started"})


@app.route('/stop', methods=['POST'])
def stop_recording():
    global state
    state.is_recording = False
    return jsonify({"status": "stopping"})


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("=" * 50)
    print("CODEXA Voice UI v1.0 (Flask)")
    print("=" * 50)
    print(f"TTS->Record delay: {TTS_TO_RECORD_DELAY}s")
    print(f"VAD silence: {VAD_SILENCE_DURATION}s")
    print(f"Config loaded: {CONFIG_LOADED}")
    print("=" * 50)
    print("\nAcesse: http://localhost:7860\n")

    app.run(host='127.0.0.1', port=7860, debug=False)
