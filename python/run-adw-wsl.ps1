# Script para executar ADW no Ubuntu WSL com todas as dependências
# Use: ./run-adw-wsl.ps1 <issue-number>

param(
    [string]$IssueNumber = "1"
)

Write-Host "🚀 Iniciando ADW no Ubuntu WSL..." -ForegroundColor Green
Write-Host "Issue: #$IssueNumber" -ForegroundColor Cyan

# Executar no WSL Ubuntu
wsl -d Ubuntu -e bash -c @"
# Configurar PATH
export PATH=`$HOME/.local/bin:`$PATH

# Navegar para o diretório do projeto
cd /mnt/c/Users/Dell/tac-7/adws

# Executar ADW
~/.local/bin/uv run adw_plan_build_iso.py $IssueNumber
"@

Write-Host "`n✅ ADW executado!" -ForegroundColor Green
Write-Host "Verifique os comentários em: https://github.com/GatoaoCubo/tac-teste/issues/$IssueNumber" -ForegroundColor Yellow
