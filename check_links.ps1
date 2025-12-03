$broken = 0
$healthy = 0
$baseDir = "C:\Users\PC\Documents\GitHub\codexa-core"

# Get all MD files except node_modules
$mdFiles = Get-ChildItem -Path $baseDir -Filter "*.md" -Recurse -Exclude @("node_modules") | Select-Object -ExpandProperty FullName

foreach ($file in $mdFiles) {
    # Extract all markdown links to .md files
    $content = Get-Content $file -ErrorAction SilentlyContinue
    $links = $content | Select-String '\[.*\]\(([^)]*\.md[^)]*)\)' -AllMatches | ForEach-Object { $_.Matches.Groups[1].Value }
    
    foreach ($link in $links) {
        # Skip external links (http, https)
        if ($link -match "^https?://") { continue }
        
        # Make path absolute
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
            Write-Host "BROKEN: $file -> $link (resolved to: $fullPath)"
        }
    }
}

Write-Host "Summary: Healthy=$healthy Broken=$broken"
