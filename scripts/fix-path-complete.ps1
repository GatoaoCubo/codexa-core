# ============================================
# CODEXA - Script de Correcao Completa do PATH
# Executa como ADMIN: powershell -ExecutionPolicy Bypass -File fix-path-complete.ps1
# ============================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " CODEXA PATH FIX - Correcao Completa" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se eh admin
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
Write-Host "Executando como Admin: $isAdmin" -ForegroundColor $(if ($isAdmin) { "Green" } else { "Yellow" })
Write-Host ""

# ============================================
# PASSO 1: Remover Python Aliases do WindowsApps
# ============================================
Write-Host "[1/5] Removendo Python aliases do WindowsApps..." -ForegroundColor Yellow

$pythonAliases = @(
    "$env:LOCALAPPDATA\Microsoft\WindowsApps\python.exe",
    "$env:LOCALAPPDATA\Microsoft\WindowsApps\python3.exe"
)

foreach ($alias in $pythonAliases) {
    if (Test-Path $alias) {
        try {
            Remove-Item $alias -Force -ErrorAction Stop
            Write-Host "  [OK] Removido: $alias" -ForegroundColor Green
        } catch {
            Write-Host "  [!] Nao foi possivel remover: $alias" -ForegroundColor Red
            Write-Host "      Execute manualmente:" -ForegroundColor Gray
            Write-Host "      Settings > Apps > Advanced app settings > App execution aliases" -ForegroundColor Gray
            Write-Host "      Desabilite 'python.exe' e 'python3.exe'" -ForegroundColor Gray
        }
    } else {
        Write-Host "  [OK] Alias ja removido: $alias" -ForegroundColor Green
    }
}
Write-Host ""

# ============================================
# PASSO 2: Definir caminhos necessarios
# ============================================
Write-Host "[2/5] Verificando caminhos necessarios..." -ForegroundColor Yellow

$requiredPaths = @{
    "Python 3.12"    = "$env:LOCALAPPDATA\Programs\Python\Python312"
    "Python Scripts" = "$env:LOCALAPPDATA\Programs\Python\Python312\Scripts"
    "UV"             = "$env:USERPROFILE\.local\bin"
    "Bun"            = "$env:USERPROFILE\.bun\bin"
    "GitHub CLI"     = "C:\Program Files\GitHub CLI"
    "FFmpeg"         = "$env:LOCALAPPDATA\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
    "npm global"     = "$env:APPDATA\npm"
}

foreach ($name in $requiredPaths.Keys) {
    $path = $requiredPaths[$name]
    if (Test-Path $path) {
        Write-Host "  [OK] $name : $path" -ForegroundColor Green
    } else {
        Write-Host "  [!] $name NAO ENCONTRADO: $path" -ForegroundColor Red
    }
}
Write-Host ""

# ============================================
# PASSO 3: Atualizar PATH do Usuario
# ============================================
Write-Host "[3/5] Atualizando PATH do usuario..." -ForegroundColor Yellow

$currentUserPath = [Environment]::GetEnvironmentVariable("PATH", "User")
$pathsToAdd = @()

foreach ($name in $requiredPaths.Keys) {
    $path = $requiredPaths[$name]
    if ((Test-Path $path) -and ($currentUserPath -notlike "*$path*")) {
        $pathsToAdd += $path
        Write-Host "  [+] Adicionando: $path" -ForegroundColor Cyan
    }
}

if ($pathsToAdd.Count -gt 0) {
    $newPath = ($pathsToAdd -join ";") + ";" + $currentUserPath
    [Environment]::SetEnvironmentVariable("PATH", $newPath, "User")
    Write-Host "  [OK] PATH atualizado com $($pathsToAdd.Count) novos caminhos" -ForegroundColor Green
} else {
    Write-Host "  [OK] Todos os caminhos ja estao no PATH" -ForegroundColor Green
}
Write-Host ""

# ============================================
# PASSO 4: Atualizar PowerShell Profile
# ============================================
Write-Host "[4/5] Atualizando PowerShell Profile..." -ForegroundColor Yellow

$profilePath = $PROFILE
$profileDir = Split-Path $profilePath -Parent

# Criar diretorio se nao existir
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
}

# Verificar se ja tem o bloco de PATH
$profileContent = ""
if (Test-Path $profilePath) {
    $profileContent = Get-Content $profilePath -Raw
}

$pathBlock = @"

# ============================================
# CODEXA PATH Refresh (Auto-generated)
# ============================================
function Refresh-Path {
    `$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
}

# Auto-refresh PATH ao iniciar
Refresh-Path

# Aliases para ferramentas
Set-Alias python312 "C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe"
Set-Alias py312 "C:\Users\PC\AppData\Local\Programs\Python\Python312\python.exe"
# ============================================
"@

if ($profileContent -notlike "*CODEXA PATH Refresh*") {
    Add-Content -Path $profilePath -Value $pathBlock
    Write-Host "  [OK] Profile atualizado com refresh automatico" -ForegroundColor Green
} else {
    Write-Host "  [OK] Profile ja configurado" -ForegroundColor Green
}
Write-Host ""

# ============================================
# PASSO 5: Verificacao Final
# ============================================
Write-Host "[5/5] Verificacao Final..." -ForegroundColor Yellow
Write-Host ""

# Refresh PATH na sessao atual
$env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")

$tools = @{
    "git"      = "git --version"
    "node"     = "node --version"
    "npm"      = "npm --version"
    "python"   = "python --version"
    "py"       = "py --version"
    "uv"       = "uv --version"
    "bun"      = "bun --version"
    "gh"       = "gh --version"
    "pytest"   = "python -m pytest --version"
    "ffmpeg"   = "ffmpeg -version"
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " STATUS FINAL DAS FERRAMENTAS" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

foreach ($tool in $tools.Keys) {
    try {
        $output = Invoke-Expression $tools[$tool] 2>&1 | Select-Object -First 1
        if ($output -match "version|Python") {
            Write-Host "  [OK] $tool : $output" -ForegroundColor Green
        } else {
            Write-Host "  [!] $tool : resposta inesperada" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  [X] $tool : NAO ENCONTRADO" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host " CONCLUIDO!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANTE: Feche e reabra o terminal para aplicar todas as mudancas." -ForegroundColor Yellow
Write-Host ""

# Se nao eh admin, mostrar instrucoes
if (-not $isAdmin) {
    Write-Host "NOTA: Para remover os aliases do Python, execute como Admin ou:" -ForegroundColor Yellow
    Write-Host "  Settings > Apps > Advanced app settings > App execution aliases" -ForegroundColor Gray
    Write-Host "  Desabilite 'python.exe' e 'python3.exe'" -ForegroundColor Gray
}
