# CONSOLIDATION_PATTERNS.md | LAW 9 Reference

**Version**: 1.0.0 | **Status**: Active | **Implements**: LAW 9 (Scout-First Consolidation)

---

## OVERVIEW

This document defines consolidation patterns for the CODEXA project, ensuring consistent application of LAW 9: Scout-First Consolidation.

**Philosophy**: Every task begins with discovery. Update before create. Delete before duplicate.

---

## CRUD PRIORITY

| Priority | Action | When | Example |
|----------|--------|------|---------|
| **1** | DELETE | Exact duplicates, orphans, stale | `*_HOP.md` suffix files |
| **2** | UPDATE | Sync from source of truth | iso_vectorstore ← parent |
| **3** | READ | Use existing as foundation | Extend existing HOP |
| **4** | CREATE | Only after scout confirms none exists | New agent type |

---

## CONSOLIDATION PATTERNS

### PATTERN 1: iso_vectorstore Sync

**Rule**: Parent directory is ALWAYS source of truth. iso_vectorstore is export target only.

```
SOURCE OF TRUTH:
  codexa.app/agentes/{agent}/PRIME.md
  codexa.app/agentes/{agent}/INSTRUCTIONS.md
  codexa.app/agentes/{agent}/README.md

EXPORT TARGET (auto-generated):
  codexa.app/agentes/{agent}/iso_vectorstore/02_PRIME.md
  codexa.app/agentes/{agent}/iso_vectorstore/03_INSTRUCTIONS.md
  codexa.app/agentes/{agent}/iso_vectorstore/04_README.md
```

**Action**: If mismatch detected, UPDATE iso_vectorstore from parent.

**Sync Script**: `python builders/11_doc_sync_builder.py --mode auto_fix`

---

### PATTERN 2: HOP Suffix Duplicates

**Rule**: One canonical HOP per function. `*_HOP.md` suffix files are export markers.

```
CANONICAL:
  prompts/13_HOP_scene_planner.md

DUPLICATE (delete):
  prompts/13_HOP_scene_planner_HOP.md
  iso_vectorstore/13_HOP_scene_planner_HOP.md
```

**Action**: DELETE files with `_HOP.md` suffix (they duplicate the base file).

**Detection**: `Glob("**/*_HOP_HOP.md")` or `Glob("**/*_HOP.md")` with matching base.

---

### PATTERN 3: Ordinal Number Conflicts

**Rule**: One ordinal number per file function. Lower ordinal is canonical.

```
FOUND:
  iso_vectorstore/13_HOP_competitor_analysis.md (canonical)
  iso_vectorstore/15_HOP_competitor_analysis.md (duplicate)

FOUND:
  iso_vectorstore/14_HOP_gap_identification.md (canonical)
  iso_vectorstore/16_HOP_gap_identification.md (duplicate)
```

**Action**: DELETE higher ordinal file. Keep lower ordinal as canonical.

**Exception**: If content differs significantly (>20%), flag for manual review.

---

### PATTERN 4: Command File Overlaps

**Rule**: One command per workflow. Consolidate overlapping functionality.

```
OVERLAP DETECTED:
  .claude/commands/prime-anuncio.md (150 lines - full context loader)
  .claude/commands/anuncio.md (46 lines - minimal shortcut)

DECISION MATRIX:
  - If prime-* has full context → DELETE minimal version
  - If both have unique value → MERGE into prime-*
  - If unclear → FLAG for manual review
```

**Action**: Prefer `prime-{agent}` commands. Delete or merge direct shortcuts.

---

### PATTERN 5: Documentation Overlap

**Rule**: Avoid duplicating content between docs/ and agent PRIMEs.

```
OVERLAP DETECTED:
  docs/ANUNCIO_PIPELINE.md (1695 lines - comprehensive)
  anuncio_agent/PRIME.md (265 lines - identity focused)

RESOLUTION:
  - PRIME.md = Agent identity, quick reference
  - docs/*.md = Deep dive, comprehensive guide
  - Cross-reference, don't duplicate
```

**Action**: Remove duplicated overview sections from docs/. Link to PRIME instead.

---

### PATTERN 6: Template Consolidation

**Rule**: Shared templates in `codexa_agent/templates/`. Agent-specific only when necessary.

```
CURRENT (fragmented):
  anuncio_agent/templates/
  curso_agent/templates/
  marca_agent/templates/
  ...

CONSOLIDATED:
  codexa_agent/templates/
  ├── shared/           # Used by multiple agents
  ├── anuncio/          # Agent-specific overrides only
  ├── curso/
  └── ...
```

**Action**: Move shared templates to codexa_agent. Keep only agent-specific overrides.

---

### PATTERN 7: Config File Duplicates

**Rule**: One config per concern. No duplicate rules across agents.

```
OVERLAP DETECTED:
  anuncio_agent/config/marketplace_specs.json
  pesquisa_agent/config/marketplace_specs.json (same content)

RESOLUTION:
  codexa.app/shared/config/marketplace_specs.json (single source)
  Agents reference: "../shared/config/marketplace_specs.json"
```

**Action**: Extract shared configs to central location.

---

## SCOUT-FIRST WORKFLOW

Before ANY task, spawn scouts:

```bash
/spawn model:haiku
1. explore: find files relevant to "{task description}"
2. explore: find consolidatable duplicates in affected directories
3. explore: check if similar content already exists
```

**Decision After Scout**:
| Scout Finds | Action |
|-------------|--------|
| Exact match exists | UPDATE existing file |
| Similar file exists (>80%) | MERGE into existing |
| Multiple duplicates | CONSOLIDATE first, then proceed |
| Orphaned/stale files | DELETE before creating new |
| Nothing exists | CREATE new file (only option) |

---

## ANTI-PATTERNS (NEVER DO)

| Anti-Pattern | Why Bad | Correct Approach |
|--------------|---------|------------------|
| Create before scout | May duplicate existing | Scout first, always |
| iso_vectorstore as source | Export target only | Parent is source |
| Multiple HOPs same function | Maintenance nightmare | One canonical HOP |
| Copy-paste between agents | Sync drift | Shared templates |
| Direct commands + prime commands | User confusion | Consolidate to prime-* |

---

## AUTOMATION

### Weekly Consolidation Scan
```bash
claude "/consolidate --scope all"
```

### Pre-commit Check
```bash
claude "/consolidate --dry-run" || echo "Consolidatables found"
```

### Doc Sync Validation
```bash
python validators/12_doc_sync_validator.py --all
```

---

## METRICS

Track consolidation health:

| Metric | Target | Current |
|--------|--------|---------|
| Duplicate files | 0 | - |
| iso_vectorstore sync rate | 100% | - |
| HOP suffix files | 0 | - |
| Ordinal conflicts | 0 | - |
| Command overlaps | 0 | - |

---

## RELATED

- **LAW 9**: SCOUT-FIRST CONSOLIDATION (CLAUDE.md)
- **Command**: `/consolidate` (scanner)
- **Command**: `/spawn preset:consolidate` (parallel scouts)
- **ADW**: 100_ADW_DOC_SYNC_WORKFLOW.md
- **Validator**: 12_doc_sync_validator.py

---

**Version**: 1.0.0
**Created**: 2025-12-05
**Type**: Reference Documentation
**Implements**: LAW 9 (Scout-First Consolidation)
