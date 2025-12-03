$baseDir = "C:\Users\PC\Documents\GitHub\codexa-core"

# Get all MD files excluding node_modules
$mdFiles = Get-ChildItem -Path $baseDir -Filter "*.md" -Recurse -Exclude @("node_modules") | Select-Object -ExpandProperty FullName

Write-Host "=== PROJECT PATH HEALTH ANALYSIS ==="
Write-Host ""
Write-Host "Total Markdown Files (excluding node_modules): $($mdFiles.Count)"

# Count files with broken links
$filesWithBrokenLinks = @()
$filesWithHealthyLinks = @()
$totalBrokenLinks = 0
$totalHealthyLinks = 0

foreach ($file in $mdFiles) {
    $content = Get-Content $file -ErrorAction SilentlyContinue
    $links = $content | Select-String '\[.*\]\(([^)]*\.md[^)]*)\)' -AllMatches | ForEach-Object { $_.Matches.Groups[1].Value }
    
    $fileBroken = 0
    $fileHealthy = 0
    
    foreach ($link in $links) {
        if ($link -match "^https?://") { continue }
        
        if ($link -match "^\.") {
            $fullPath = Join-Path (Split-Path $file) $link
        } else {
            $fullPath = Join-Path $baseDir $link
        }
        
        $fullPath = [System.IO.Path]::GetFullPath($fullPath)
        
        if (Test-Path $fullPath) {
            $fileHealthy++
            $totalHealthyLinks++
        } else {
            $fileBroken++
            $totalBrokenLinks++
        }
    }
    
    if ($fileBroken -gt 0) {
        $filesWithBrokenLinks += $file
    } elseif ($fileHealthy -gt 0) {
        $filesWithHealthyLinks += $file
    }
}

Write-Host ""
Write-Host "Link Analysis:"
Write-Host "  - Total Internal Links: $($totalHealthyLinks + $totalBrokenLinks)"
Write-Host "  - Healthy Links: $totalHealthyLinks"
Write-Host "  - Broken Links: $totalBrokenLinks"
Write-Host ""

# Calculate file health percentage
$filesWithLinks = $filesWithBrokenLinks.Count + $filesWithHealthyLinks.Count
$healthyFileCount = $filesWithHealthyLinks.Count

if ($filesWithLinks -eq 0) {
    $healthyPercentage = 100
} else {
    $healthyPercentage = [Math]::Round(($healthyFileCount / $filesWithLinks) * 100, 2)
}

Write-Host "File Health:"
Write-Host "  - Files with Links: $filesWithLinks"
Write-Host "  - Healthy Files (all links valid): $healthyFileCount"
Write-Host "  - Files with Broken Links: $($filesWithBrokenLinks.Count)"
Write-Host "  - Healthy Files Percentage: $healthyPercentage%"
Write-Host ""

# Calculate overall score out of 10
# Factor 1: Link health (60% weight) 
# Factor 2: File coverage (40% weight)
if ($totalHealthyLinks + $totalBrokenLinks -eq 0) {
    $linkScore = 10
} else {
    $linkHealthPercentage = ($totalHealthyLinks / ($totalHealthyLinks + $totalBrokenLinks)) * 100
    $linkScore = ($linkHealthPercentage / 100) * 10
}

$fileCoveragePercentage = if ($filesWithLinks -eq 0) { 100 } else { ($healthyFileCount / $filesWithLinks) * 100 }
$fileScore = ($fileCoveragePercentage / 100) * 10

$overallScore = ($linkScore * 0.6) + ($fileScore * 0.4)
$overallScore = [Math]::Round($overallScore, 2)

Write-Host "=== OVERALL PROJECT HEALTH SCORE ==="
Write-Host "Score: $overallScore / 10.0"
Write-Host ""

if ($overallScore -ge 8.5) {
    Write-Host "Status: EXCELLENT"
} elseif ($overallScore -ge 7.0) {
    Write-Host "Status: GOOD"
} elseif ($overallScore -ge 5.0) {
    Write-Host "Status: ACCEPTABLE"
} else {
    Write-Host "Status: NEEDS IMPROVEMENT"
}

Write-Host ""
Write-Host "Scoring Breakdown:"
Write-Host "  - Link Health Score: $([Math]::Round($linkScore, 2))/10"
Write-Host "  - File Coverage Score: $([Math]::Round($fileScore, 2))/10"
