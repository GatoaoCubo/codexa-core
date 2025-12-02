@echo off
REM Brand Agent Standalone - Export Script for OpenAI Agent Builder (Windows)
REM Version: 1.0
REM Date: 2025-11-09

setlocal enabledelayedexpansion

echo ================================================
echo   Brand Agent Standalone - Export Package
echo ================================================
echo.

REM Configuration
set EXPORT_DIR=export_package
set TIMESTAMP=%date:~-4%%date:~3,2%%date:~0,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set TIMESTAMP=%TIMESTAMP: =0%
set EXPORT_ZIP=brand-agent-export_%TIMESTAMP%.zip

REM Clean previous exports
echo 🧹 Cleaning previous exports...
if exist "%EXPORT_DIR%" rmdir /s /q "%EXPORT_DIR%"
del /q brand-agent-export_*.zip 2>nul

REM Create export directory
echo 📁 Creating export directory...
mkdir "%EXPORT_DIR%"

REM Copy core files
echo 📋 Copying core files...
if exist README.md (copy /y README.md "%EXPORT_DIR%\" >nul) else (echo ⚠️  README.md not found)
if exist QUICK_START.md (copy /y QUICK_START.md "%EXPORT_DIR%\" >nul) else (echo ⚠️  QUICK_START.md not found)
if exist IMPROVEMENT_ANALYSIS.md (copy /y IMPROVEMENT_ANALYSIS.md "%EXPORT_DIR%\" >nul) else (echo ⚠️  IMPROVEMENT_ANALYSIS.md not found)
if exist IMPROVEMENTS_SUMMARY.md (copy /y IMPROVEMENTS_SUMMARY.md "%EXPORT_DIR%\" >nul) else (echo ⚠️  IMPROVEMENTS_SUMMARY.md not found)
if exist ROADMAP_MELHORIAS.md (copy /y ROADMAP_MELHORIAS.md "%EXPORT_DIR%\" >nul) else (echo ⚠️  ROADMAP_MELHORIAS.md not found)

REM Copy vector store files (PRIORITY)
echo 📦 Copying OpenAI Vector Store files...
if exist openai_vector_store (
    xcopy /e /i /y /q openai_vector_store "%EXPORT_DIR%\openai_vector_store\" >nul

    REM Count files
    set FILE_COUNT=0
    for /r "%EXPORT_DIR%\openai_vector_store" %%f in (*) do set /a FILE_COUNT+=1
    echo    ✅ Copied !FILE_COUNT! files from openai_vector_store/
) else (
    echo    ❌ ERROR: openai_vector_store/ directory not found!
    exit /b 1
)

REM Copy config files
echo ⚙️  Copying config files...
if exist config (
    xcopy /e /i /y /q config "%EXPORT_DIR%\config\" >nul
    echo    ✅ Config files copied
) else (
    echo    ⚠️  config/ directory not found (optional)
)

REM Copy validation scripts (optional)
if exist scripts (
    echo 🧪 Copying validation scripts...
    xcopy /e /i /y /q scripts "%EXPORT_DIR%\scripts\" >nul
    echo    ✅ Scripts copied
)

REM Create manifest file
echo 📝 Creating EXPORT_MANIFEST.txt...
(
    echo ========================================
    echo BRAND AGENT STANDALONE - Export Package
    echo ========================================
    echo.
    echo Export Date: %date% %time%
    echo Export Version: 1.0
    echo.
    echo CONTENTS:
    echo ---------
    echo 📁 openai_vector_store/       - Upload ALL these files to OpenAI Vector Store
    echo 📁 config/                    - Configuration files (brand_archetypes.json^)
    echo 📁 scripts/                   - Validation scripts (brand_validator.py^)
    echo 📄 README.md                  - Main documentation
    echo 📄 QUICK_START.md             - Quick start guide
    echo 📄 IMPROVEMENT_ANALYSIS.md    - Gap analysis and roadmap
    echo 📄 IMPROVEMENTS_SUMMARY.md    - What was implemented
    echo 📄 ROADMAP_MELHORIAS.md       - Original improvement roadmap
    echo.
    echo INSTRUCTIONS:
    echo -------------
    echo 1. Go to: https://platform.openai.com/agents
    echo 2. Create New Agent or open existing Brand Strategy Agent
    echo 3. Upload ALL files from openai_vector_store/ to Vector Store
    echo 4. Paste MASTER_INSTRUCTIONS.md content into Instructions field
    echo 5. Enable tools: file_search + code_interpreter
    echo 6. Set model: gpt-4-turbo or gpt-4o
    echo 7. Save and test with sample brief
    echo.
    echo PRIORITY FILES (Must upload^):
    echo ------------------------------
) > "%EXPORT_DIR%\EXPORT_MANIFEST.txt"

REM List priority files
if exist "%EXPORT_DIR%\openai_vector_store\MASTER_INSTRUCTIONS.md" (
    echo ✅ MASTER_INSTRUCTIONS.md >> "%EXPORT_DIR%\EXPORT_MANIFEST.txt"
)
if exist "%EXPORT_DIR%\openai_vector_store\OUTPUT_SCHEMA.md" (
    echo ✅ OUTPUT_SCHEMA.md >> "%EXPORT_DIR%\EXPORT_MANIFEST.txt"
)
if exist "%EXPORT_DIR%\openai_vector_store\brand_archetypes.json" (
    echo ✅ brand_archetypes.json >> "%EXPORT_DIR%\EXPORT_MANIFEST.txt"
)
if exist "%EXPORT_DIR%\openai_vector_store\positioning_frameworks.json" (
    echo ✅ positioning_frameworks.json >> "%EXPORT_DIR%\EXPORT_MANIFEST.txt"
)
if exist "%EXPORT_DIR%\openai_vector_store\tone_taxonomies.json" (
    echo ✅ tone_taxonomies.json >> "%EXPORT_DIR%\EXPORT_MANIFEST.txt"
)

echo. >> "%EXPORT_DIR%\EXPORT_MANIFEST.txt"

REM Count total files
set TOTAL_FILES=0
for /r "%EXPORT_DIR%" %%f in (*) do set /a TOTAL_FILES+=1
echo Total files in package: !TOTAL_FILES! >> "%EXPORT_DIR%\EXPORT_MANIFEST.txt"

REM Create ZIP archive (requires PowerShell or 7-Zip)
echo.
echo 📦 Creating ZIP archive...

REM Try PowerShell compression
powershell -command "Compress-Archive -Path '%EXPORT_DIR%' -DestinationPath '%EXPORT_ZIP%' -Force" 2>nul
if %errorlevel% equ 0 (
    for %%A in ("%EXPORT_ZIP%") do set ZIP_SIZE=%%~zA
    set /a ZIP_SIZE_KB=!ZIP_SIZE! / 1024
    echo    ✅ Archive created: %EXPORT_ZIP% (!ZIP_SIZE_KB! KB^)
) else (
    echo    ⚠️  PowerShell compression failed. Package available uncompressed.
)

REM Summary
echo.
echo ================================================
echo ✅ EXPORT COMPLETE!
echo ================================================
echo.
echo 📦 Package location:
if exist "%EXPORT_ZIP%" (
    echo    %CD%\%EXPORT_ZIP%
) else (
    echo    %CD%\%EXPORT_DIR%\ (uncompressed^)
)
echo.
echo 📁 Uncompressed package:
echo    %CD%\%EXPORT_DIR%\
echo.
echo 📋 Next steps:
echo    1. Extract the archive or use %EXPORT_DIR%\ directly
echo    2. Read EXPORT_MANIFEST.txt for upload instructions
echo    3. Upload files to OpenAI Agent Builder
echo.
echo ================================================

pause
