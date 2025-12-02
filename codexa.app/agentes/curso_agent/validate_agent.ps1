# ============================================================================
# HOTMART COURSE BUILDER AGENT - QUICK VALIDATION SCRIPT
# ============================================================================
# Purpose: Run all automated validators before commit
# Usage: .\validate_agent.ps1
# Requirements: Python 3.10+, uv package manager
# ============================================================================

Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  CODEXA Agent Validation Suite - Hotmart Course Builder Agent   ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$AGENT_PATH = "agents/hotmart_course_builder_agent"
$ARTIFACTS_PATH = "$AGENT_PATH/artifacts"
$VALIDATORS_PATH = "codexa.app/agentes/codexa_agent/validators"

$total_tests = 0
$passed_tests = 0
$failed_tests = 0

# ============================================================================
# FUNCTION: Run Validator
# ============================================================================
function Run-Validator {
    param(
        [string]$Name,
        [string]$Command,
        [string]$ExpectedPattern
    )

    $global:total_tests++

    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
    Write-Host "▶ Running: $Name" -ForegroundColor Yellow
    Write-Host "  Command: $Command" -ForegroundColor DarkGray
    Write-Host ""

    try {
        $output = Invoke-Expression $Command 2>&1 | Out-String

        if ($LASTEXITCODE -eq 0 -or $output -match $ExpectedPattern) {
            Write-Host "✅ PASS: $Name" -ForegroundColor Green
            $global:passed_tests++
            return $true
        } else {
            Write-Host "❌ FAIL: $Name" -ForegroundColor Red
            Write-Host "  Output: $output" -ForegroundColor DarkGray
            $global:failed_tests++
            return $false
        }
    }
    catch {
        Write-Host "❌ ERROR: $Name" -ForegroundColor Red
        Write-Host "  Exception: $_" -ForegroundColor DarkGray
        $global:failed_tests++
        return $false
    }
}

# ============================================================================
# PHASE 1: File Existence Check
# ============================================================================
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PHASE 1: File Existence Validation" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$required_files = @(
    "$ARTIFACTS_PATH/MASTER_INSTRUCTIONS.md",
    "$ARTIFACTS_PATH/AGENT_CONFIGURATION.json",
    "$ARTIFACTS_PATH/README.md",
    "$ARTIFACTS_PATH/DEPLOYMENT_GUIDE.md"
)

foreach ($file in $required_files) {
    $total_tests++
    if (Test-Path $file) {
        $size = (Get-Item $file).Length
        $size_kb = [math]::Round($size / 1KB, 2)
        Write-Host "✅ Found: $file ($size_kb KB)" -ForegroundColor Green
        $passed_tests++
    } else {
        Write-Host "❌ Missing: $file" -ForegroundColor Red
        $failed_tests++
    }
}

# ============================================================================
# PHASE 2: README Validation
# ============================================================================
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PHASE 2: README Validation" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Run-Validator `
    -Name "README Structure & Quality" `
    -Command "uv run $VALIDATORS_PATH/09_readme_validator.py $ARTIFACTS_PATH/README.md" `
    -ExpectedPattern "(PASS|Quality score)"

# ============================================================================
# PHASE 3: Path Consistency Validation
# ============================================================================
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PHASE 3: Path Consistency Validation" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Run-Validator `
    -Name "Path Consistency Check" `
    -Command "uv run $VALIDATORS_PATH/16_path_consistency_validator.py $AGENT_PATH/" `
    -ExpectedPattern "(PASS|consistent|valid)"

# ============================================================================
# PHASE 4: HOP/TAC-7 Validation (if applicable)
# ============================================================================
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PHASE 4: HOP/TAC-7 Validation" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$hop_files = Get-ChildItem -Path $ARTIFACTS_PATH -Filter "*HOP*.md" -ErrorAction SilentlyContinue

if ($hop_files.Count -gt 0) {
    foreach ($hop in $hop_files) {
        Run-Validator `
            -Name "HOP Structure: $($hop.Name)" `
            -Command "uv run $VALIDATORS_PATH/07_hop_sync_validator.py $($hop.FullName)" `
            -ExpectedPattern "(PASS|TAC-7|compliant)"
    }
} else {
    Write-Host "⚠️  No HOP files found (N/A for this agent)" -ForegroundColor DarkYellow
}

# ============================================================================
# PHASE 5: JSON Configuration Validation
# ============================================================================
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PHASE 5: JSON Configuration Validation" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$total_tests++
try {
    $json_content = Get-Content "$ARTIFACTS_PATH/AGENT_CONFIGURATION.json" -Raw | ConvertFrom-Json

    $required_keys = @("name", "description", "version", "model", "tools", "capabilities")
    $missing_keys = @()

    foreach ($key in $required_keys) {
        if (-not $json_content.PSObject.Properties.Name.Contains($key)) {
            $missing_keys += $key
        }
    }

    if ($missing_keys.Count -eq 0) {
        Write-Host "✅ JSON valid with all required keys" -ForegroundColor Green
        Write-Host "  Name: $($json_content.name)" -ForegroundColor DarkGray
        Write-Host "  Version: $($json_content.version)" -ForegroundColor DarkGray
        Write-Host "  Model: $($json_content.model)" -ForegroundColor DarkGray
        $passed_tests++
    } else {
        Write-Host "❌ JSON missing keys: $($missing_keys -join ', ')" -ForegroundColor Red
        $failed_tests++
    }
}
catch {
    Write-Host "❌ JSON parsing failed: $_" -ForegroundColor Red
    $failed_tests++
}

# ============================================================================
# PHASE 6: Content Quality Checks
# ============================================================================
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PHASE 6: Content Quality Checks" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Check MASTER_INSTRUCTIONS word count
$total_tests++
$master_instructions = Get-Content "$ARTIFACTS_PATH/MASTER_INSTRUCTIONS.md" -Raw
$word_count = ($master_instructions -split '\s+').Count

if ($word_count -ge 2000 -and $word_count -le 15000) {
    Write-Host "✅ MASTER_INSTRUCTIONS word count: $word_count (optimal range: 2,000-15,000)" -ForegroundColor Green
    $passed_tests++
} else {
    Write-Host "⚠️  MASTER_INSTRUCTIONS word count: $word_count (outside optimal range)" -ForegroundColor Yellow
}

# Check for [OPEN_VARIABLES] presence
$total_tests++
$open_vars_count = ([regex]::Matches($master_instructions, '\[OPEN_VARIABLE')).Count

if ($open_vars_count -ge 5) {
    Write-Host "✅ [OPEN_VARIABLES] found: $open_vars_count instances (good flexibility)" -ForegroundColor Green
    $passed_tests++
} else {
    Write-Host "⚠️  [OPEN_VARIABLES] found: $open_vars_count instances (consider adding more)" -ForegroundColor Yellow
}

# Check for CODEXA seed words
$total_tests++
$seed_words = @("Meta-Construção", "Destilação de Conhecimento", "Cérebro Plugável")
$seed_words_found = 0

foreach ($word in $seed_words) {
    if ($master_instructions -match $word) {
        $seed_words_found++
    }
}

if ($seed_words_found -eq $seed_words.Count) {
    Write-Host "✅ All CODEXA seed words present ($seed_words_found/$($seed_words.Count))" -ForegroundColor Green
    $passed_tests++
} else {
    Write-Host "⚠️  Missing some seed words ($seed_words_found/$($seed_words.Count))" -ForegroundColor Yellow
    $failed_tests++
}

# ============================================================================
# PHASE 7: Security Check (No Sensitive Data)
# ============================================================================
Write-Host ""
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PHASE 7: Security & Sensitive Data Check" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$total_tests++
$sensitive_patterns = @(
    "sk-[a-zA-Z0-9]{20,}",  # OpenAI API keys
    "sk-ant-[a-zA-Z0-9]{20,}",  # Anthropic API keys
    "[a-zA-Z0-9]{32,}",  # Generic long tokens
    "password\s*=",  # Password assignments
    "api_key\s*="  # API key assignments
)

$all_content = Get-ChildItem -Path $ARTIFACTS_PATH -Filter "*.md" |
    ForEach-Object { Get-Content $_.FullName -Raw }

$sensitive_found = $false
foreach ($pattern in $sensitive_patterns) {
    if ($all_content -match $pattern) {
        $sensitive_found = $true
        Write-Host "⚠️  Potential sensitive data pattern found: $pattern" -ForegroundColor Red
        break
    }
}

if (-not $sensitive_found) {
    Write-Host "✅ No sensitive data patterns detected" -ForegroundColor Green
    $passed_tests++
} else {
    Write-Host "❌ SECURITY ALERT: Review files for sensitive data before commit!" -ForegroundColor Red
    $failed_tests++
}

# ============================================================================
# FINAL REPORT
# ============================================================================
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                      VALIDATION SUMMARY                          ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

$pass_rate = [math]::Round(($passed_tests / $total_tests) * 100, 1)

Write-Host "Total Tests: $total_tests" -ForegroundColor White
Write-Host "Passed: $passed_tests" -ForegroundColor Green
Write-Host "Failed: $failed_tests" -ForegroundColor Red
Write-Host "Pass Rate: $pass_rate%" -ForegroundColor $(if ($pass_rate -ge 70) { "Green" } else { "Red" })
Write-Host ""

# Quality Score
$quality_score = [math]::Round(($pass_rate / 10), 1)
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  OVERALL QUALITY SCORE: $quality_score / 10" -ForegroundColor $(
    if ($quality_score -ge 7.0) { "Green" }
    elseif ($quality_score -ge 5.0) { "Yellow" }
    else { "Red" }
)
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Recommendation
if ($quality_score -ge 7.0) {
    Write-Host "✅ RECOMMENDATION: Agent is READY TO COMMIT" -ForegroundColor Green
    Write-Host "   All critical validations passed. Proceed with git commit." -ForegroundColor DarkGray
    exit 0
}
elseif ($quality_score -ge 5.0) {
    Write-Host "⚠️  RECOMMENDATION: CONDITIONAL PASS" -ForegroundColor Yellow
    Write-Host "   Fix critical issues above, then commit." -ForegroundColor DarkGray
    exit 1
}
else {
    Write-Host "❌ RECOMMENDATION: NOT READY TO COMMIT" -ForegroundColor Red
    Write-Host "   Major rework needed. Review failed tests above." -ForegroundColor DarkGray
    exit 2
}
