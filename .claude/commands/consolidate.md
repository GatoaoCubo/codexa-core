# /consolidate | Scout-First Consolidation Scanner

**Purpose**: Scan for consolidatable files and auto-merge duplicates following LAW 9
**Time**: 2-5 min per scope | **Output**: Consolidation report + auto-fixes (if not --dry-run)

---

## QUICK START

```bash
# Full scan + auto-consolidate (default)
/consolidate

# Report only - no changes
/consolidate --dry-run

# Scope to specific directories
/consolidate --scope agents     # Only agent directories
/consolidate --scope commands   # Only command files
/consolidate --scope iso        # Only iso_vectorstore dirs
```

---

## WORKFLOW

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: SCOUT                                                 │
│  ├── Spawn 3-5 parallel scouts (haiku model)                   │
│  ├── Scout 1: Find duplicate content across locations          │
│  ├── Scout 2: Find iso_vectorstore ↔ parent mismatches         │
│  ├── Scout 3: Find orphaned/stale files                        │
│  └── Scout 4: Find HOPs with *_HOP.md suffix duplicates        │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 2: ANALYZE                                               │
│  ├── Group findings by consolidation type                      │
│  ├── Calculate similarity scores (>80% = consolidate)          │
│  ├── Identify source of truth for each group                   │
│  └── Generate action plan per finding                          │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 3: CRUD ACTION (if not --dry-run)                        │
│  ├── DELETE: Remove duplicates, orphans, stale files           │
│  ├── UPDATE: Sync content to source of truth                   │
│  ├── MERGE: Consolidate similar files into one                 │
│  └── Backup all affected files (.bak) before changes           │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 4: REPORT                                                │
│  ├── Generate consolidation_report.md                          │
│  ├── List all changes made (or would be made if --dry-run)     │
│  ├── Show before/after file counts                             │
│  └── Flag any items needing manual review                      │
└─────────────────────────────────────────────────────────────────┘
```

---

## CRUD PRIORITY (LAW 9)

| Priority | Action | When to Apply |
|----------|--------|---------------|
| 1 | **DELETE** | Orphaned files, exact duplicates, stale content |
| 2 | **UPDATE** | Sync iso_vectorstore from parent (parent = source) |
| 3 | **MERGE** | Similar files (>80% overlap) into single canonical |
| 4 | **CREATE** | Only if scouts confirm nothing exists (rare in consolidation) |

---

## CONSOLIDATION PATTERNS

### Pattern 1: iso_vectorstore Duplicates
```
FOUND:
  anuncio_agent/PRIME.md (v2.6.0) ← SOURCE OF TRUTH
  anuncio_agent/iso_vectorstore/02_PRIME.md (v2.5.0) ← STALE

ACTION: UPDATE iso_vectorstore/02_PRIME.md from PRIME.md
```

### Pattern 2: HOP Suffix Duplicates
```
FOUND:
  prompts/13_HOP_scene_planner.md (canonical)
  prompts/13_HOP_scene_planner_HOP.md (export marker)

ACTION: DELETE *_HOP.md suffix file (redundant)
```

### Pattern 3: Ordinal Number Conflicts
```
FOUND:
  iso_vectorstore/13_HOP_competitor_analysis.md
  iso_vectorstore/15_HOP_competitor_analysis.md (same content)

ACTION: DELETE higher ordinal, keep canonical
```

### Pattern 4: Command Overlaps
```
FOUND:
  .claude/commands/prime-anuncio.md (full context)
  .claude/commands/anuncio.md (minimal shortcut)

ACTION: MERGE into prime-anuncio.md, DELETE anuncio.md
       OR FLAG for manual decision
```

---

## INPUT

**Automatic Detection**:
- Scans all `codexa.app/agentes/*/` directories
- Scans `.claude/commands/` directory
- Scans `docs/` directory
- Detects file types: .md, .json, .py

**Optional Arguments**:
```
/consolidate [options]

Options:
  --dry-run          Report only, no changes
  --scope SCOPE      Limit scan (agents|commands|iso|docs|all)
  --threshold N      Similarity threshold % (default: 80)
  --verbose          Show detailed scout findings
  --backup-dir PATH  Custom backup location (default: .consolidate-backup/)
```

---

## OUTPUT

### Console Output
```
[CONSOLIDATE] Starting LAW 9 scan...
[SCOUT] Spawning 4 parallel scouts (haiku)...
[SCOUT 1] Found 12 iso_vectorstore duplicates
[SCOUT 2] Found 8 HOP suffix duplicates
[SCOUT 3] Found 3 orphaned files
[SCOUT 4] Found 2 command overlaps

[ANALYZE] Grouping findings...
  - TIER 1 (auto-fix): 20 items
  - TIER 2 (manual review): 5 items

[ACTION] Applying CRUD priority...
  - DELETE: 8 files (exact duplicates)
  - UPDATE: 12 files (sync from parent)
  - MERGE: 0 files (none qualified)
  - SKIP: 5 files (needs manual review)

[BACKUP] Created .consolidate-backup/2025-12-05_1530/
[REPORT] Saved consolidation_report.md

[DONE] Consolidation complete.
  Before: 213 files | After: 193 files | Reduced: 20 files (9.4%)
```

### Consolidation Report (`outputs/consolidation/YYYY-MM-DD_HHmm.md`)
```markdown
# Consolidation Report | 2025-12-05 15:30

## Summary
- **Scope**: all
- **Duration**: 3m 12s
- **Files Scanned**: 213
- **Files Affected**: 20
- **Reduction**: 9.4%

## Actions Taken

### DELETED (8 files)
| File | Reason |
|------|--------|
| iso_vectorstore/13_HOP_scene_planner_HOP.md | HOP suffix duplicate |
| iso_vectorstore/15_HOP_competitor_analysis.md | Ordinal conflict |
| ... | ... |

### UPDATED (12 files)
| File | Source | Changes |
|------|--------|---------|
| anuncio_agent/iso_vectorstore/02_PRIME.md | anuncio_agent/PRIME.md | Version sync |
| ... | ... | ... |

### NEEDS MANUAL REVIEW (5 items)
| Item | Reason |
|------|--------|
| .claude/commands/anuncio.md vs prime-anuncio.md | Functional overlap |
| ... | ... |

## Backups
Location: `.consolidate-backup/2025-12-05_1530/`
```

---

## SCOUT SPAWN PATTERN

When `/consolidate` runs, it executes:

```
/spawn model:haiku
1. explore: find duplicate content in codexa.app/agentes/*/
2. explore: find iso_vectorstore files mismatched with parent dirs
3. explore: find orphaned *_HOP.md suffix files
4. explore: find stale files (not modified in 30+ days, no references)
5. explore: find command file overlaps in .claude/commands/
```

---

## SAFETY MECHANISMS

**Backup Before Change**:
- All affected files backed up to `.consolidate-backup/YYYY-MM-DD_HHmm/`
- Backup includes full directory structure

**Rollback Capability**:
```bash
# Restore from backup if needed
cp -r .consolidate-backup/2025-12-05_1530/* .
```

**Never Auto-Delete**:
- Files with active git changes (uncommitted)
- Files referenced in config.json or imports
- Files modified in last 24 hours
- Files flagged as "source of truth"

**Manual Review Triggers**:
- Similarity between 60-80% (ambiguous)
- Both files have different valuable content
- File is entry point (PRIME.md, README.md)
- File has external dependencies

---

## INTEGRATION

### Pre-commit Hook
```bash
# .husky/pre-commit
claude "/consolidate --dry-run" || echo "Warning: consolidatables found"
```

### Weekly Maintenance
```bash
# Run weekly consolidation scan
claude "/consolidate --scope all"
```

### CI/CD Pipeline
```yaml
# .github/workflows/consolidate.yml
on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  consolidate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run consolidation scan
        run: claude "/consolidate --dry-run"
```

---

## TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Too many false positives | Increase `--threshold 90` |
| Missing expected duplicates | Lower `--threshold 70` |
| Scouts timeout | Reduce scope with `--scope agents` |
| Important file deleted | Restore from `.consolidate-backup/` |
| iso_vectorstore keeps regenerating | Check sync scripts, may need update |

---

## RELATED

- **LAW 9**: SCOUT-FIRST CONSOLIDATION (CLAUDE.md)
- **LAW 3**: META-CONSTRUCTION (Discovery-First)
- **Command**: `/spawn preset:consolidate` (parallel scouts)
- **ADW**: [100_ADW_DOC_SYNC_WORKFLOW.md](codexa.app/agentes/codexa_agent/workflows/100_ADW_DOC_SYNC_WORKFLOW.md)
- **Validator**: [12_doc_sync_validator.py](codexa.app/agentes/codexa_agent/validators/12_doc_sync_validator.py)

---

**Version**: 1.0.0
**Created**: 2025-12-05
**Type**: Consolidation Workflow Command
**Implements**: LAW 9 (Scout-First Consolidation)
