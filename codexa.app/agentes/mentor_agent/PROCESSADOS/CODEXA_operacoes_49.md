# LIVRO: Operacoes
## CAPÍTULO 49

**Versículos consolidados**: 1
**Linhas totais**: 198
**Gerado em**: 2025-11-15 08:42:00

---

<!-- VERSÍCULO 1/1 - cleanup_automation_patterns.md (198 linhas) -->

# Padrões de Limpeza Automatizada | Scout Internal Mode

## CONCEITOS-CHAVE

• **Scout Internal**: Modo de varredura completa do projeto para detectar issues
• **Categorização de Issues**: 6 tipos detectáveis - backups, refs obsoletas, paths quebrados, Python desorganizado, pastas vazias, docs migração
• **Limpeza Progressiva**: Executar por fases - temp files → refs → structure → docs
• **Safe Deletion**: Sempre backup antes de deletar, usar `git rm` para rastreabilidade

## POR QUE IMPORTA

Cleanup Report 2025-11-14 demonstrou impacto de limpeza sistemática:
- **87+ issues** detectados e corrigidos em 61 arquivos
- **26 arquivos temporários** removidos (backups, __pycache__, NUL files)
- **27 referências obsoletas** corrigidas (scout_agent, conhecimento_agent)
- **21+ Python files** reorganizados (flat root → builders/validators hierarchy)

Sem automação:
- Issues se acumulam silenciosamente (backups de Nov ainda em Dec)
- Referências quebradas propagam (11 arquivos referenciando agent morto)
- Estrutura degrada (10 .py no root, zero hierarquia)

Com Scout Internal:
- Detecção em minutos vs. dias manual
- Categorização automática (87 issues → 6 categorias)
- Métricas objetivas (100% coverage em cada categoria)

## FASES DE LIMPEZA

### FASE 1: Arquivos Temporários (26 files)

**Categoria 1A: Backups de Prompts** (20 files)
```bash
# Padrão de detecção
find agentes/*/prompts -name "*.backup_*"

# Encontrados
anuncio_agent/prompts/20_titulo_generator.backup_* (5 versões)
anuncio_agent/prompts/40_bullet_points.backup_* (4 versões)
anuncio_agent/prompts/50_descricao_builder.backup_* (4 versões)
pesquisa_agent/prompts/seo_taxonomy.backup_* (3 versões)
pesquisa_agent/prompts/competitor_analysis.backup_* (3 versões)
mentor_agent/DISTRIBUICAO/knowledge_map.backup_* (1 versão)
```

**Ação**:
```bash
# Deletar todos os backups
find . -name "*.backup_*" -type f -delete

# Adicionar ao .gitignore
echo "*.backup_*" >> .gitignore
```

**Categoria 1B: Arquivos .bak** (2 files)
```bash
# Detectar
find . -name "*.bak"

# Deletar
git rm agentes/anuncio_agent/SETUP.md.bak
git rm agentes/mentor_agent/SETUP.md.bak
```

**Categoria 1C: Python Cache** (1 directory)
```bash
# Detectar
find . -type d -name "__pycache__"

# Deletar
rm -rf agentes/mentor_agent/DISTRIBUICAO/__pycache__/

# .gitignore (should exist)
__pycache__/
*.pyc
*.pyo
```

**Categoria 1D: Workflow Reports Antigos** (2 files)
```bash
# Estratégia: Manter apenas o mais recente
ls -lt workflows/reports/workflow_report_*.txt | tail -n +2

# Deletar old
git rm workflow_report_20251114_074447.txt
git rm workflow_report_20251114_081153.txt
# KEEP workflow_report_20251114_081953.txt (latest)
```

**Categoria 1E: NUL Files (Windows)** (2 files)
```bash
# Detectar
find . -name "nul" -o -name "NUL"

# Deletar
git rm agentes/NUL
git rm agentes/codexa_agent/nul
```

### FASE 2: Referências Obsoletas (11 files)

**Contexto**: `scout_agent` + `conhecimento_agent` consolidados em `mentor_agent` v2.0.0 (Nov 2025)

**Detecção Automática**:
```bash
# Encontrar todas as referências
grep -r "scout_agent\|conhecimento_agent" \
  --exclude-dir=_archived \
  --exclude-dir=.git \
  --include="*.md" \
  -l

# Output: 11 files encontrados
```

**Arquivos a Corrigir**:
1. **PRIME.md** (ROOT)
   ```diff
   - /prime-scout → Code discovery specialist
   - /prime-knowledge → ML training datasets
   + /prime-mentor → Onboarding (guides, tutorials, code discovery)
   ```

2. **README.md** (ROOT)
   ```diff
   - scout_agent: Code exploration, grep, find
   - conhecimento_agent: Knowledge base, ML datasets
   + mentor_agent: Comprehensive onboarding, knowledge base, code discovery
   ```

3. **Agent READMEs** (anuncio, pesquisa, marca)
   - Atualizar links de integração
   - Mudar dependency de `scout_agent` → `mentor_agent`

4. **Integration Guides**
   - Update import paths: `from scout_agent import X` → `from mentor_agent.src.scout_ops import X`

**Script de Automação**:
```bash
# Find and replace em massa (safe)
find . -name "*.md" -not -path "./_archived/*" -exec sed -i \
  's/scout_agent/mentor_agent/g; s/conhecimento_agent/mentor_agent/g' {} +

# Validar manualmente depois
git diff --stat
```

### FASE 3: Paths Quebrados (9 fixes)

**Detecção**:
```bash
# Encontrar links markdown quebrados
grep -r "\[.*\](\.\./\|\./" --include="*.md" | \
  while read line; do
    file=$(echo "$line" | cut -d: -f1)
    link=$(echo "$line" | grep -o "(.*)" | tr -d "()")
    if [[ ! -e "$link" ]]; then
      echo "BROKEN: $file → $link"
    fi
  done
```

**Padrões Comuns**:
```diff
# Padrão 1: Agente path references
- [Setup](../agentes_old/anuncio_agent/SETUP.md)
+ [Setup](../agentes/anuncio_agent/SETUP.md)

# Padrão 2: Command movido para fractal
- [Command](../../commands/anuncio.md)
+ [Command](./commands/anuncio.md)

# Padrão 3: Doc consolidado movido
- [Guide](../how_to/BUILD_AGENTS.md)
+ [Guide](../docs_consolidados/44_MIGRATION_GUIDE.md)
```

### FASE 4: Python Desorganizado (21+ files)

**Antes** (Flat Root):
```
codexa.app/
├── 01_agent_builder.py
├── 02_agent_meta_constructor.py
├── ... (10 files sem hierarquia)
```

**Depois** (Hierárquico):
```
agentes/codexa_agent/
├── builders/
│   ├── 01_agent_builder.py
│   ├── 02_agent_meta_constructor.py
│   ├── 03_build_task.py
│   ├── ... (7 builders)
└── validators/
    ├── 07_hop_sync_validator.py
    ├── 09_readme_validator.py
    └── ... (4 validators)
```

**Script de Migração**:
```bash
# Criar estrutura
mkdir -p agentes/codexa_agent/{builders,validators}

# Mover builders (01-06, 08)
for i in 01 02 03 04 05 06 08; do
  git mv ${i}_*.py agentes/codexa_agent/builders/
done

# Mover validators (07, 09, 10)
for i in 07 09 10; do
  git mv ${i}_*.py agentes/codexa_agent/validators/
done
```

### FASE 5: Pastas Vazias (4 folders)

**Detecção**:
```bash
# Encontrar pastas vazias (sem .gitkeep)
find . -type d -empty

# Encontrar pastas só com .gitkeep
find . -type d -exec sh -c 'ls -A "$1" | grep -qv "^\.gitkeep$"' _ {} \; -print
```

**Ação**:
```bash
# Opção 1: Adicionar .gitkeep se deve existir
touch agentes/anuncio_agent/user_anuncios/.gitkeep
git add agentes/anuncio_agent/user_anuncios/.gitkeep

# Opção 2: Remover se não é necessária
rm -rf commands/git/  # Empty after fractal migration
rm -rf commands/e2e/  # Empty after fractal migration
```

### FASE 6: Docs de Migração Obsoletos (5 files)

**Categoria**: Reports já executados, sem valor futuro

**Detecção**:
```bash
# Encontrar reports com datas passadas
find . -name "*REPORT*.md" -o -name "*CLEANUP*.md" | \
  xargs grep -l "Date.*2025-11-14"
```

**Arquivos**:
```
CLEANUP_REPORT_2025-11-14.md          → Executado, pode arquivar
CLEANUP_ADDENDUM_COMMANDS.md          → Executado, pode arquivar
FRACTAL_ARCHITECTURE_ANALYSIS.md      → Implementado, pode arquivar
FRACTAL_CLEANUP_FINAL_REPORT.md       → Executado, pode arquivar
```

**Ação**:
```bash
# Mover para arquivo histórico
mkdir -p _archived/cleanup_reports_2025-11
mv *CLEANUP*.md *FRACTAL*.md _archived/cleanup_reports_2025-11/
git add _archived/cleanup_reports_2025-11/
git rm CLEANUP_*.md FRACTAL_*.md
```

## AUTOMAÇÃO - SCRIPT COMPLETO

```bash
#!/bin/bash
# cleanup_scout_internal.sh
# Run: ./cleanup_scout_internal.sh --dry-run  (preview)
#      ./cleanup_scout_internal.sh --execute  (run)

DRY_RUN=false
[[ "$1" == "--dry-run" ]] && DRY_RUN=true

echo "=== SCOUT INTERNAL CLEANUP ==="
echo "Mode: $([ "$DRY_RUN" = true ] && echo "DRY RUN" || echo "EXECUTE")"
echo ""

# FASE 1: Temp files
echo "FASE 1: Detecting temporary files..."
BACKUPS=$(find . -name "*.backup_*" -type f)
BAKS=$(find . -name "*.bak" -type f)
PYCACHE=$(find . -type d -name "__pycache__")
NULS=$(find . -name "nul" -o -name "NUL")

echo "  Backups: $(echo "$BACKUPS" | wc -l)"
echo "  .bak files: $(echo "$BAKS" | wc -l)"
echo "  __pycache__: $(echo "$PYCACHE" | wc -l)"
echo "  NUL files: $(echo "$NULS" | wc -l)"

if [ "$DRY_RUN" = false ]; then
  echo "$BACKUPS" | xargs -r rm -f
  echo "$BAKS" | xargs -r git rm -f
  echo "$PYCACHE" | xargs -r rm -rf
  echo "$NULS" | xargs -r git rm -f
  echo "  ✅ Cleaned"
fi

# FASE 2: Obsolete refs
echo ""
echo "FASE 2: Detecting obsolete references..."
REFS=$(grep -r "scout_agent\|conhecimento_agent" \
  --exclude-dir=_archived --exclude-dir=.git \
  --include="*.md" -l | wc -l)
echo "  Files with obsolete refs: $REFS"

if [ "$DRY_RUN" = false ]; then
  find . -name "*.md" -not -path "./_archived/*" -exec sed -i \
    's/scout_agent/mentor_agent/g; s/conhecimento_agent/mentor_agent/g' {} +
  echo "  ✅ Updated"
fi

# FASE 3: Broken paths
echo ""
echo "FASE 3: Detecting broken paths..."
echo "  (Manual review required - run path checker separately)"

# FASE 4: Python organization
echo ""
echo "FASE 4: Checking Python organization..."
ROOT_PY=$(find . -maxdepth 1 -name "*.py" | wc -l)
echo "  Python files in root: $ROOT_PY"

# FASE 5: Empty folders
echo ""
echo "FASE 5: Detecting empty folders..."
EMPTY=$(find . -type d -empty | wc -l)
echo "  Empty folders: $EMPTY"

# FASE 6: Migration docs
echo ""
echo "FASE 6: Detecting obsolete migration docs..."
OLD_DOCS=$(find . -maxdepth 1 -name "*CLEANUP*.md" -o -name "*FRACTAL*.md" | wc -l)
echo "  Obsolete docs: $OLD_DOCS"

echo ""
echo "=== SUMMARY ==="
echo "Total issues detected across 6 categories"
echo "Run with --execute to apply fixes"
```

## MÉTRICAS E REPORTING

**Formato de Report**:
```markdown
# CLEANUP REPORT - Scout Internal
Date: YYYY-MM-DD
Executor: [Agent Name]
Scope: [Project Path]

## SUMMARY
| Category | Found | Fixed | Status |
|----------|-------|-------|--------|
| Temp files | 26 | 26 | ✅ 100% |
| Obsolete refs | 27 | 11 files updated | ✅ 100% |
| Broken paths | 9 | 9 | ✅ 100% |
| Python organization | 21+ | 21+ | ✅ 100% |
| Empty folders | 4 | 4 | ✅ 100% |
| Migration docs | 5 | 5 | ✅ 100% |

## DETAILED EXECUTION
[Phase-by-phase breakdown]

## GIT METRICS
git status output:
- Deleted: 22
- Moved: 28
- Modified: 7
- Added: 4
```

## APLICAÇÃO PRÁTICA

**Quando executar Scout Internal**:
- Após major refactor (fractal migration, agent consolidation)
- Mensalmente (routine cleanup)
- Antes de releases
- Quando `git status` mostra >30 modified files

**Workflow**:
1. Backup: `git commit -m "backup: pre-cleanup snapshot"`
2. Dry-run: `./cleanup_scout_internal.sh --dry-run`
3. Review output
4. Execute: `./cleanup_scout_internal.sh --execute`
5. Manual review: `git diff --stat`
6. Commit: `git commit -m "chore: scout internal cleanup - 87 issues fixed"`
