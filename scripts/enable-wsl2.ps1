# ============================================
# CODEXA - Habilitar WSL2 Completo
# REQUER ADMIN: Execute como Administrador!
# ============================================

#Requires -RunAsAdministrator

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " CODEXA - Habilitando WSL2" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se eh admin
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "[ERRO] Este script precisa ser executado como Administrador!" -ForegroundColor Red
    Write-Host "Clique direito no PowerShell > 'Executar como administrador'" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/4] Habilitando Windows Subsystem for Linux..." -ForegroundColor Yellow
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

Write-Host ""
Write-Host "[2/4] Habilitando Virtual Machine Platform..." -ForegroundColor Yellow
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

Write-Host ""
Write-Host "[3/4] Definindo WSL2 como padrao..." -ForegroundColor Yellow
wsl --set-default-version 2

Write-Host ""
Write-Host "[4/4] Baixando kernel do WSL2..." -ForegroundColor Yellow
wsl --update

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " WSL2 HABILITADO!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANTE: Reinicie o computador para aplicar as mudancas!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Apos reiniciar, execute:" -ForegroundColor White
Write-Host "  wsl --install -d Ubuntu" -ForegroundColor Cyan
Write-Host ""

$restart = Read-Host "Deseja reiniciar agora? (S/N)"
if ($restart -eq "S" -or $restart -eq "s") {
    Write-Host "Reiniciando em 5 segundos..." -ForegroundColor Yellow
    Start-Sleep -Seconds 5
    Restart-Computer -Force
}
