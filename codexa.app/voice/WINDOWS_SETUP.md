# CODEXA Voice - Windows Setup Guide

## Problem Solved

The voice MCP server was configured to use `uv run` which requires the `uv` package manager to be installed. This caused issues on Windows where users typically use `python` directly.

**Solution**: Changed `.mcp.json` to use the standard `python` command, which works on all platforms.

---

## Changes Made

### 1. Updated `.mcp.json` Configuration

**File**: `C:\Users\PC\Documents\GitHub\codexa-core\.mcp.json`

**Changed from:**
```json
"voice": {
  "command": "uv",
  "args": ["run", "codexa.app/voice/server.py"],
  ...
}
```

**Changed to:**
```json
"voice": {
  "command": "python",
  "args": ["codexa.app/voice/server.py"],
  ...
}
```

### 2. Created Windows Setup Script

**File**: `codexa.app\voice\setup_windows.bat`

Automated installation script that:
- Checks if Python is installed
- Upgrades pip
- Installs all dependencies from requirements.txt
- Provides clear next steps

**Usage:**
```batch
codexa.app\voice\setup_windows.bat
```

### 3. Created Setup Verification Script

**File**: `codexa.app\voice\verify_setup.py`

Python script that verifies:
- Python version (3.10+)
- All required dependencies are installed
- .env file configuration (optional)
- Audio devices (microphone & speakers)

**Usage:**
```batch
python codexa.app\voice\verify_setup.py
```

### 4. Updated Documentation

**Files Updated:**
- `codexa.app\voice\docs\SETUP.md` - Added Windows-specific instructions
- `codexa.app\voice\README.md` - Added Windows quick start section

---

## How to Use (Windows)

### Installation

1. **Install dependencies:**
   ```batch
   codexa.app\voice\setup_windows.bat
   ```

   Or manually:
   ```batch
   python -m pip install -r codexa.app\voice\requirements.txt
   ```

2. **(Optional) Configure API key:**

   Create/edit `.env` in project root:
   ```env
   ELEVENLABS_API_KEY=el_your_key_here
   ```

   **Note**: The system works WITHOUT an API key using:
   - **TTS**: Edge TTS (free, good quality)
   - **STT**: Whisper (free, offline)

3. **Verify setup:**
   ```batch
   python codexa.app\voice\verify_setup.py
   ```

### Usage

1. Start Claude Code
2. Type `/v` to activate voice mode
3. Speak your commands
4. Say "parar", "sair", or "exit" to exit voice mode

---

## Dependencies

All dependencies are in `codexa.app\voice\requirements.txt`:

| Package | Purpose | Required |
|---------|---------|----------|
| sounddevice | Audio recording | Yes |
| soundfile | Audio file handling | Yes |
| numpy | Audio processing | Yes |
| edge-tts | Free TTS (Microsoft) | Yes |
| pyttsx3 | Offline TTS fallback | Yes |
| elevenlabs | Premium STT/TTS | Optional |
| pygame | Audio playback | Yes |
| python-dotenv | Environment variables | Yes |
| mcp | Claude Code integration | Yes |

---

## Troubleshooting

### Python not found
- Install Python 3.10+ from https://www.python.org/downloads/
- Check "Add Python to PATH" during installation
- Restart terminal after installation

### Microphone not detected
1. Check Windows sound settings
2. Grant microphone permissions to Python
3. Run: `python codexa.app\voice\verify_setup.py`

### Dependencies fail to install
1. Update pip: `python -m pip install --upgrade pip`
2. Run as Administrator (if needed)
3. Check internet connection

### Voice server doesn't start
1. Verify all dependencies: `python codexa.app\voice\verify_setup.py`
2. Check `.mcp.json` uses `"command": "python"`
3. Restart Claude Code

---

## Technical Details

### Why the change from `uv` to `python`?

**Before:**
- Required users to install `uv` (a Python package manager)
- Added extra setup complexity
- Not standard on Windows

**After:**
- Uses standard `python` command
- Works on Windows, Linux, and macOS
- No additional tools needed
- Follows Python best practices

### How does it work?

1. Claude Code reads `.mcp.json` on startup
2. Launches voice server: `python codexa.app/voice/server.py`
3. Server imports dependencies from site-packages
4. MCP protocol enables voice tools in Claude Code

### Environment Variables

Set in `.mcp.json` under `voice.env`:
- `ELEVENLABS_API_KEY` - ElevenLabs API key (optional)
- `VOICE_PORT` - Server port (default: 5000)
- `VOICE_LANGUAGE` - Language code (default: pt-BR)

---

## Version

- **Voice Server**: v3.0
- **Windows Support**: Added 2025-12-04
- **MCP Config**: Updated 2025-12-04

---

## References

- Main README: `codexa.app\voice\README.md`
- Setup Guide: `codexa.app\voice\docs\SETUP.md`
- Requirements: `codexa.app\voice\requirements.txt`
- MCP Config: `.mcp.json` (root)
