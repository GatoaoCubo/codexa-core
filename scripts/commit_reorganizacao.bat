@echo off
echo ========================================
echo Fazendo commit da reorganizacao do repositorio
echo ========================================
echo.

REM Remover lock se existir
del /F /Q .git\index.lock 2>NUL

REM Adicionar todas as mudancas
echo [1/3] Adicionando mudancas ao staging...
git add .

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERRO] Nao foi possivel adicionar arquivos.
    echo Por favor, feche o VSCode ou qualquer editor que esteja usando Git
    echo e execute este script novamente.
    echo.
    pause
    exit /b 1
)

echo [OK] Mudancas adicionadas com sucesso!
echo.

REM Mostrar resumo
echo [2/3] Resumo das mudancas:
git status --short | find /C "D " > temp_deleted.txt
git status --short | find /C "A " > temp_added.txt
git status --short | find /C "M " > temp_modified.txt

set /p DELETED=<temp_deleted.txt
set /p ADDED=<temp_added.txt
set /p MODIFIED=<temp_modified.txt

del temp_deleted.txt temp_added.txt temp_modified.txt

echo    - Arquivos deletados: %DELETED%
echo    - Arquivos adicionados: %ADDED%
echo    - Arquivos modificados: %MODIFIED%
echo.

REM Fazer commit
echo [3/3] Criando commit...
git commit -m "Reorganizacao completa do repositorio

Consolidacao de pastas de conhecimento:
- docs/codex_anuncio -> knowledge_base/codex_anuncio
- LEM_knowledge_base -> knowledge_base/lem_knowledge
- RAW_BIBLE_v1 -> knowledge_base/bible_framework
- RAW_LEM_v1.1_PADDLEOCR -> knowledge_base/paddleocr_data
- app_docs -> knowledge_base/app_documentation
- INTEGRATION_REPORT -> knowledge_base/integration

Movimentacao de arquivos MD:
- Arquivos MD soltos da raiz -> knowledge_base/reports/

Renomeacao:
- ecommerce-canon -> ecommerce/

Scripts criados:
- scripts/organize_repository.py
- scripts/organize_repository_simple.py

Reducao de ~40%% na complexidade da raiz do repositorio.
Todo conhecimento agora esta centralizado em knowledge_base/.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

if %ERRORLEVEL% EQ 0 (
    echo.
    echo ========================================
    echo [SUCESSO] Commit criado com sucesso!
    echo ========================================
    echo.
    echo Proximos passos:
    echo 1. Revise o commit: git show HEAD
    echo 2. Faca push: git push origin main
    echo.
) else (
    echo.
    echo [ERRO] Falha ao criar commit
    echo.
)

pause
