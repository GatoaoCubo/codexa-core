#Requires -Version 5.1
<#
.SYNOPSIS
    CODEXA Bootstrap - Zero to Hero installer for fresh Windows PCs

.DESCRIPTION
    This script installs EVERYTHING needed to run CODEXA from a completely fresh Windows PC:
    1. Enables script execution (if needed)
    2. Installs winget (if not present)
    3. Installs Node.js LTS
    4. Installs Python 3.12
    5. Installs Git
    6. Installs uv (fast Python runner)
    7. Installs Claude Code CLI
    8. Clones codexa-core repository
    9. Runs setup-codexa.js for final configuration

.NOTES
    Run this in PowerShell as Administrator:

    Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/GatoaoCubo/codexa-core/main/bootstrap-codexa.ps1'))

    Or if you have the file locally:

    powershell -ExecutionPolicy Bypass -File bootstrap-codexa.ps1

.EXAMPLE
    .\bootstrap-codexa.ps1

.EXAMPLE
    .\bootstrap-codexa.ps1 -SkipClone
    # Skip cloning if you already have the repo
#>

param(
    [switch]$SkipClone,
    [switch]$SkipClaude,
    [string]$InstallPath = "$env:USERPROFILE\Documents\GitHub"
)

# ============================================================================
# CONFIGURATION
# ============================================================================
$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"  # Faster downloads

$CONFIG = @{
    RepoUrl = "https://github.com/GatoaoCubo/codexa-core.git"
    RepoName = "codexa-core"
    NodeVersion = "22"  # LTS
    PythonVersion = "3.12"
}

# ============================================================================
# COLORS & UI
# ============================================================================
function Write-Step { param($msg) Write-Host "`n[$([char]0x2192)] $msg" -ForegroundColor Cyan }
function Write-Ok { param($msg) Write-Host "  [OK] $msg" -ForegroundColor Green }
function Write-Warn { param($msg) Write-Host "  [!] $msg" -ForegroundColor Yellow }
function Write-Err { param($msg) Write-Host "  [X] $msg" -ForegroundColor Red }
function Write-Info { param($msg) Write-Host "  [i] $msg" -ForegroundColor Gray }

function Show-Banner {
    Write-Host ""
    Write-Host "  ========================================" -ForegroundColor Magenta
    Write-Host "       CODEXA BOOTSTRAP INSTALLER" -ForegroundColor White
    Write-Host "       Fresh PC -> Ready to Code" -ForegroundColor Gray
    Write-Host "  ========================================" -ForegroundColor Magenta
    Write-Host ""
}

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================
function Test-Admin {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

function Test-Command {
    param($cmd)
    try {
        $null = Get-Command $cmd -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Get-CommandVersion {
    param($cmd, $versionArg = "--version")
    try {
        $output = & $cmd $versionArg 2>&1 | Select-Object -First 1
        return $output -replace '[^\d\.]', '' -replace '^\.+|\.+$', ''
    } catch {
        return $null
    }
}

function Refresh-Path {
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")
}

function Install-WithWinget {
    param($packageId, $name)

    Write-Info "Installing $name via winget..."
    try {
        $result = winget install -e --id $packageId --accept-source-agreements --accept-package-agreements 2>&1
        if ($LASTEXITCODE -eq 0 -or $result -match "already installed") {
            Write-Ok "$name installed"
            return $true
        } else {
            Write-Warn "winget install returned: $result"
            return $false
        }
    } catch {
        Write-Err "Failed to install $name : $_"
        return $false
    }
}

# ============================================================================
# INSTALLATION FUNCTIONS
# ============================================================================
function Install-NodeJS {
    Write-Step "Checking Node.js..."

    if (Test-Command "node") {
        $version = Get-CommandVersion "node"
        Write-Ok "Node.js $version already installed"
        return $true
    }

    if (Install-WithWinget "OpenJS.NodeJS.LTS" "Node.js LTS") {
        Refresh-Path
        return $true
    }

    # Fallback: direct download
    Write-Warn "Trying direct download..."
    $nodeUrl = "https://nodejs.org/dist/v22.11.0/node-v22.11.0-x64.msi"
    $msiPath = "$env:TEMP\nodejs.msi"

    try {
        Invoke-WebRequest -Uri $nodeUrl -OutFile $msiPath -UseBasicParsing
        Start-Process msiexec.exe -ArgumentList "/i `"$msiPath`" /qn" -Wait
        Remove-Item $msiPath -Force -ErrorAction SilentlyContinue
        Refresh-Path
        Write-Ok "Node.js installed via direct download"
        return $true
    } catch {
        Write-Err "Failed to install Node.js: $_"
        return $false
    }
}

function Install-Python {
    Write-Step "Checking Python..."

    if (Test-Command "python") {
        $version = Get-CommandVersion "python"
        if ($version -match "^3\.1[0-4]") {
            Write-Ok "Python $version already installed"
            return $true
        }
    }

    if (Install-WithWinget "Python.Python.3.12" "Python 3.12") {
        Refresh-Path
        return $true
    }

    Write-Err "Failed to install Python"
    return $false
}

function Install-Git {
    Write-Step "Checking Git..."

    if (Test-Command "git") {
        $version = Get-CommandVersion "git"
        Write-Ok "Git $version already installed"
        return $true
    }

    if (Install-WithWinget "Git.Git" "Git") {
        Refresh-Path
        return $true
    }

    Write-Err "Failed to install Git"
    return $false
}

function Install-UV {
    Write-Step "Checking uv (Python runner)..."

    if (Test-Command "uv") {
        $version = Get-CommandVersion "uv"
        Write-Ok "uv $version already installed"
        return $true
    }

    Write-Info "Installing uv via pip..."
    try {
        & pip install uv 2>&1 | Out-Null
        Refresh-Path

        if (Test-Command "uv") {
            Write-Ok "uv installed"
            return $true
        }
    } catch {}

    # Fallback: standalone installer
    Write-Info "Trying standalone installer..."
    try {
        irm https://astral.sh/uv/install.ps1 | iex
        Refresh-Path
        Write-Ok "uv installed via standalone"
        return $true
    } catch {
        Write-Warn "uv installation failed (optional)"
        return $false
    }
}

function Install-ClaudeCode {
    Write-Step "Checking Claude Code CLI..."

    if (Test-Command "claude") {
        $version = Get-CommandVersion "claude"
        Write-Ok "Claude Code $version already installed"
        return $true
    }

    Write-Info "Installing Claude Code via npm..."
    try {
        & npm install -g @anthropic-ai/claude-code 2>&1 | Out-Null
        Refresh-Path

        if (Test-Command "claude") {
            Write-Ok "Claude Code installed"
            return $true
        } else {
            # npm global might not be in PATH
            $npmGlobal = & npm config get prefix 2>&1
            $env:Path += ";$npmGlobal"

            if (Test-Command "claude") {
                Write-Ok "Claude Code installed (added to PATH)"
                # Make it permanent
                $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
                if ($userPath -notlike "*$npmGlobal*") {
                    [Environment]::SetEnvironmentVariable("Path", "$userPath;$npmGlobal", "User")
                }
                return $true
            }
        }
    } catch {
        Write-Err "Failed to install Claude Code: $_"
    }

    return $false
}

function Clone-Repository {
    Write-Step "Setting up CODEXA repository..."

    $repoPath = Join-Path $InstallPath $CONFIG.RepoName

    # Create directory if needed
    if (-not (Test-Path $InstallPath)) {
        New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
        Write-Info "Created: $InstallPath"
    }

    if (Test-Path $repoPath) {
        Write-Ok "Repository already exists at: $repoPath"
        Set-Location $repoPath

        # Pull latest
        Write-Info "Pulling latest changes..."
        & git pull 2>&1 | Out-Null
        return $repoPath
    }

    Write-Info "Cloning repository..."
    Set-Location $InstallPath
    & git clone $CONFIG.RepoUrl 2>&1

    if (Test-Path $repoPath) {
        Write-Ok "Cloned to: $repoPath"
        Set-Location $repoPath
        return $repoPath
    } else {
        Write-Err "Failed to clone repository"
        return $null
    }
}

function Run-SetupScript {
    param($repoPath)

    Write-Step "Running CODEXA setup..."

    $setupScript = Join-Path $repoPath "setup-codexa.js"

    if (-not (Test-Path $setupScript)) {
        Write-Err "setup-codexa.js not found at: $setupScript"
        return $false
    }

    Set-Location $repoPath
    Write-Info "Executing: node setup-codexa.js"

    try {
        & node $setupScript
        return $true
    } catch {
        Write-Err "Setup script failed: $_"
        return $false
    }
}

function Setup-PowerShellProfile {
    Write-Step "Setting up PowerShell shortcuts..."

    $profileDir = Split-Path $PROFILE -Parent
    if (-not (Test-Path $profileDir)) {
        New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    }

    $shortcuts = @'

# ============================================================================
# CODEXA Shortcuts (added by bootstrap-codexa.ps1)
# ============================================================================

# Start Claude Code in autonomous mode
function cc { claude --dangerously-skip-permissions @args }

# Start Claude Code in standard mode
function ccs { claude @args }

# Health check
function codexa-check {
    $root = "$env:USERPROFILE\Documents\GitHub\codexa-core"
    if (Test-Path $root) {
        Push-Location $root
        node setup-codexa.js --check
        Pop-Location
    } else {
        Write-Host "CODEXA not found at: $root" -ForegroundColor Red
    }
}

# Auto-repair
function codexa-repair {
    $root = "$env:USERPROFILE\Documents\GitHub\codexa-core"
    if (Test-Path $root) {
        Push-Location $root
        node setup-codexa.js --repair
        Pop-Location
    } else {
        Write-Host "CODEXA not found at: $root" -ForegroundColor Red
    }
}

# Navigate to CODEXA
function goto-codexa { Set-Location "$env:USERPROFILE\Documents\GitHub\codexa-core" }

Write-Host ""
Write-Host "CODEXA Shortcuts:" -ForegroundColor Cyan
Write-Host "  cc           - Claude (autonomous)" -ForegroundColor Green
Write-Host "  ccs          - Claude (standard)" -ForegroundColor Yellow
Write-Host "  codexa-check - Health check" -ForegroundColor Gray
Write-Host "  goto-codexa  - Go to project" -ForegroundColor Gray
Write-Host ""
'@

    # Check if already added
    if (Test-Path $PROFILE) {
        $content = Get-Content $PROFILE -Raw
        if ($content -match "CODEXA Shortcuts") {
            Write-Ok "Shortcuts already in profile"
            return
        }
    }

    # Append to profile
    Add-Content -Path $PROFILE -Value $shortcuts
    Write-Ok "Shortcuts added to PowerShell profile"
}

# ============================================================================
# MAIN EXECUTION
# ============================================================================
function Main {
    Show-Banner

    # Check admin (recommended but not required)
    if (-not (Test-Admin)) {
        Write-Warn "Running without admin rights. Some installs may fail."
        Write-Warn "Recommended: Right-click PowerShell -> Run as Administrator"
        Write-Host ""
        $continue = Read-Host "Continue anyway? (y/n)"
        if ($continue -ne "y") {
            exit 1
        }
    }

    # Set execution policy for this process
    Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

    $results = @{
        NodeJS = $false
        Python = $false
        Git = $false
        UV = $false
        ClaudeCode = $false
        Repository = $false
        Setup = $false
    }

    # Install prerequisites
    $results.NodeJS = Install-NodeJS
    $results.Python = Install-Python
    $results.Git = Install-Git
    $results.UV = Install-UV

    # Refresh PATH after installations
    Refresh-Path

    # Install Claude Code
    if ($results.NodeJS -and -not $SkipClaude) {
        $results.ClaudeCode = Install-ClaudeCode
    }

    # Clone repository
    $repoPath = $null
    if ($results.Git -and -not $SkipClone) {
        $repoPath = Clone-Repository
        $results.Repository = ($null -ne $repoPath)
    }

    # Run setup script
    if ($results.Repository -and $results.NodeJS) {
        $results.Setup = Run-SetupScript $repoPath
    }

    # Setup PowerShell profile
    Setup-PowerShellProfile

    # Summary
    Write-Host ""
    Write-Host "  ========================================" -ForegroundColor Magenta
    Write-Host "              INSTALLATION SUMMARY" -ForegroundColor White
    Write-Host "  ========================================" -ForegroundColor Magenta
    Write-Host ""

    $statusIcon = { param($ok) if ($ok) { "[OK]" } else { "[--]" } }
    $statusColor = { param($ok) if ($ok) { "Green" } else { "Red" } }

    Write-Host "  $(&$statusIcon $results.NodeJS) Node.js" -ForegroundColor (&$statusColor $results.NodeJS)
    Write-Host "  $(&$statusIcon $results.Python) Python" -ForegroundColor (&$statusColor $results.Python)
    Write-Host "  $(&$statusIcon $results.Git) Git" -ForegroundColor (&$statusColor $results.Git)
    Write-Host "  $(&$statusIcon $results.UV) uv (optional)" -ForegroundColor (&$statusColor $results.UV)
    Write-Host "  $(&$statusIcon $results.ClaudeCode) Claude Code" -ForegroundColor (&$statusColor $results.ClaudeCode)
    Write-Host "  $(&$statusIcon $results.Repository) Repository" -ForegroundColor (&$statusColor $results.Repository)
    Write-Host "  $(&$statusIcon $results.Setup) Setup" -ForegroundColor (&$statusColor $results.Setup)

    Write-Host ""

    # Next steps
    if ($results.ClaudeCode) {
        Write-Host "  NEXT STEPS:" -ForegroundColor Yellow
        Write-Host "  1. Close and reopen PowerShell" -ForegroundColor White
        Write-Host "  2. Run: claude" -ForegroundColor White
        Write-Host "     (Login via browser on first run)" -ForegroundColor Gray
        Write-Host "  3. After login, use: cc" -ForegroundColor White
        Write-Host "     (Shortcut for autonomous mode)" -ForegroundColor Gray
        Write-Host ""

        if ($repoPath) {
            Write-Host "  PROJECT LOCATION:" -ForegroundColor Yellow
            Write-Host "  $repoPath" -ForegroundColor Cyan
            Write-Host ""
        }
    } else {
        Write-Host "  [!] Claude Code installation failed." -ForegroundColor Red
        Write-Host "  Please restart PowerShell and try:" -ForegroundColor Yellow
        Write-Host "  npm install -g @anthropic-ai/claude-code" -ForegroundColor White
        Write-Host ""
    }

    Write-Host "  ========================================" -ForegroundColor Magenta
    Write-Host ""
}

# Run main
Main
