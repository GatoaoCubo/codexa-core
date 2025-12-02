@echo off
REM Script para executar ADW no Ubuntu WSL
REM Use: run-adw-wsl.bat <issue-number>

setlocal enabledelayedexpansion

if "%1"=="" (
    set ISSUE=1
) else (
    set ISSUE=%1
)

echo 🚀 Iniciando ADW no Ubuntu WSL...
echo Issue: #!ISSUE!

REM Executar no WSL Ubuntu
wsl -d Ubuntu -e bash -c "export PATH=$HOME/.local/bin:$PATH && cd /mnt/c/Users/Dell/tac-7/adws && ~/.local/bin/uv run adw_plan_build_iso.py !ISSUE!"

echo.
echo ✅ ADW executado!
echo Verifique os comentarios em: https://github.com/GatoaoCubo/tac-teste/issues/!ISSUE!

pause
