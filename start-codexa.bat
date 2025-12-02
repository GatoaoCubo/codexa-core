@echo off
REM CODEXA.app Startup Script for Windows
REM
REM Usage:
REM   start-codexa.bat          - Start dashboard
REM   start-codexa.bat voice    - Start with voice
REM   start-codexa.bat stop     - Stop all services
REM

setlocal enabledelayedexpansion

set CODEXA_ROOT=%~dp0
set LAUNCHER_DIR=%CODEXA_ROOT%codexa.app\launcher
set VOICE_DIR=%CODEXA_ROOT%codexa.app\voice
set DASHBOARD_PORT=3333
set VOICE_PORT=5000

if "%1"=="stop" goto :stop
if "%1"=="status" goto :status
if "%1"=="voice" goto :start_with_voice

:start
echo [CODEXA] Starting Dashboard...
cd /d "%LAUNCHER_DIR%"

REM Install deps if needed
if not exist "node_modules" (
    echo [CODEXA] Installing dependencies...
    call npm install
)

REM Start dashboard
start "CODEXA Dashboard" /B node server.js

timeout /t 3 /nobreak >nul
echo [CODEXA] Dashboard running at http://localhost:%DASHBOARD_PORT%

goto :status

:start_with_voice
call :start
echo [CODEXA] Starting Voice daemon...
cd /d "%VOICE_DIR%"
start "CODEXA Voice" /B uv run server.py
timeout /t 3 /nobreak >nul
echo [CODEXA] Voice daemon running at http://localhost:%VOICE_PORT%
goto :status

:stop
echo [CODEXA] Stopping services...
taskkill /F /FI "WINDOWTITLE eq CODEXA Dashboard" 2>nul
taskkill /F /FI "WINDOWTITLE eq CODEXA Voice" 2>nul
echo [CODEXA] Services stopped.
goto :eof

:status
echo.
echo ===============================================
echo              CODEXA.app Status
echo ===============================================
echo.
echo   Dashboard: http://localhost:%DASHBOARD_PORT%
echo   Voice:     http://localhost:%VOICE_PORT%
echo.
echo   MCP Servers: Configured in .mcp.json
echo   - scout, codexa-commands, browser, voice
echo.
echo   Commands:
echo   - /codexa "task" - Primary orchestrator
echo   - /prime - System status
echo   - /v - Voice mode
echo.
echo   To start Claude Code:
echo   claude
echo.
echo ===============================================
goto :eof
