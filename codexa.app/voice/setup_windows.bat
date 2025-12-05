@echo off
REM CODEXA Voice - Windows Setup Script
REM =====================================
REM Installs Python dependencies for the voice MCP server

echo.
echo ============================================
echo CODEXA Voice - Windows Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    exit /b 1
)

echo Found Python:
python --version
echo.

REM Get the script directory
set SCRIPT_DIR=%~dp0

echo Installing dependencies from requirements.txt...
echo.

REM Install dependencies
python -m pip install --upgrade pip
python -m pip install -r "%SCRIPT_DIR%requirements.txt"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to install dependencies!
    echo.
    echo Try running as Administrator or check your internet connection.
    exit /b 1
)

echo.
echo ============================================
echo SUCCESS! Voice server dependencies installed.
echo ============================================
echo.
echo Next steps:
echo 1. (OPTIONAL) Add ElevenLabs API key to .env file:
echo    ELEVENLABS_API_KEY=el_your_key_here
echo    Note: The voice system works WITHOUT this key!
echo    - TTS: Uses Edge TTS (free, good quality)
echo    - STT: Uses Whisper (free, offline)
echo.
echo 2. Verify setup:
echo    python codexa.app\voice\verify_setup.py
echo.
echo 3. Start Claude Code - the voice MCP server will auto-start
echo    Type /v to activate voice mode
echo.

pause
