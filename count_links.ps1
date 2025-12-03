$broken = 0
$healthy = 0
$baseDir = "C:\Users\PC\Documents\GitHub\codexa-core"

$mdFiles = Get-ChildItem -Path $baseDir -Filter "*.md" -Recurse -Exclude @("node_modules") | Select-Object -ExpandProperty FullName

foreach ($file in $mdFiles) {
    $content = Get-Content $file -ErrorAction SilentlyContinue
    $links = $content | Select-String '\[.*\]\(([^)]*\.md[^)]*)\)' -AllMatches | ForEach-Object { $_.Matches.Groups[1].Value }
    
    foreach ($link in $links) {
        if ($link -match "^https?://") { continue }
        
        if ($link -match "^\.") {
            $fullPath = Join-Path (Split-Path $file) $link
        } else {
            $fullPath = Join-Path $baseDir $link
        }
        
        $fullPath = [System.IO.Path]::GetFullPath($fullPath)
        
        if (Test-Path $fullPath) {
            $healthy++
        } else {
            $broken++
        }
    }
}

Write-Host "Total Links: $($healthy + $broken)"
Write-Host "Healthy: $healthy"
Write-Host "Broken: $broken"
