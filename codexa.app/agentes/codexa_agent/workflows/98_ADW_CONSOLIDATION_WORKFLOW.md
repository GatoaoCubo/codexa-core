# 98_ADW_CONSOLIDATION_WORKFLOW | Codebase Consolidation Workflow

**Purpose**: Consolidate, deduplicate, improve clarity across codebase
**Type**: 3-Phase ADW | **Duration**: 15-30 minutes (semi-automated)
**Output**: Cleaner, more maintainable codebase with improved documentation
**Version**: 2.0.0 | **Updated**: 2025-11-24

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "consolidation",
  "workflow_name": "Codebase Consolidation Workflow",
  "version": "2.0.0",
  "context_strategy": "full_history",
  "failure_handling": "continue",

  "v2_enhancements": {
    "parallel_execution": true,
    "batch_processing": true,
    "task_boundaries": true
  },

  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "consolidation"},
    {"phase_id": "phase_1_analysis", "phase_name": "Analyze Codebase", "duration": "5-10min", "description": "Identify duplication + improvement opportunities"},
    {"phase_id": "phase_2_consolidate", "phase_name": "Consolidate & Refactor", "duration": "8-15min", "description": "Remove duplication + improve structure"},
    {"phase_id": "phase_3_document", "phase_name": "Update Documentation", "duration": "2-5min", "description": "Sync docs with changes"}
  ]
}
```

---

## PARALLEL EXECUTION (v2.0.0 Enhancement)

### Batch Processing Strategy
```yaml
analysis_batch:
  parallel: true
  tasks:
    - scan_duplicates: "Find duplicate code patterns"
    - scan_complexity: "Identify complex functions"
    - scan_docs: "Check documentation sync"
    - scan_structure: "Analyze file structure"

consolidation_batch:
  parallel: true  # Only for independent files
  dependency_aware: true
  max_concurrent: 5
```

### Task Boundaries for Consolidation
```yaml
TASK_BOUNDARY: CONSOLIDATION_PHASE_2
ACCESS: write
SCOPE: Modify files in $consolidation_targets
CONSTRAINT: One file per task boundary
ROLLBACK: Git-based (commit per batch)
```

### Integration with 203_ADW_PARALLEL_ORCHESTRATION
For large codebases (>100 files to analyze):
```bash
uv run workflows/203_ADW_PARALLEL_ORCHESTRATION.py \
  --workflow 98_ADW_CONSOLIDATION \
  --batch-size 20
```

---

## PHASE DETAILS

### PHASE 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `consolidation`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

### PHASE 1: Analyze Codebase
**Objective**: Identify issues (duplication, complexity, outdated docs)
**Actions**: Scan codebase with Scout | Identify duplicates | Check doc sync | Analyze complexity
**Tools**: Scout agent | grep/diff | validators
**Input**: Target directory | **Output**: $analysis_report `{duplicates[], complexity_issues[], doc_issues[], recommendations[]}`
**Validation**: Report complete | Issues categorized | Priorities assigned

### PHASE 2: Consolidate & Refactor
**Objective**: Remove duplication + improve structure
**Actions**:
- Merge duplicate code into shared modules
- Simplify complex functions
- Standardize naming conventions
- Apply information-dense keywords (MAX 1000 LINES per file)
- Remove dead code
**Input**: $analysis_report | **Output**: $changes `{files_modified[], files_deleted[], new_modules[], loc_reduced}`
**Validation**: No functionality broken | Tests pass | LOC reduced | Clarity improved

### PHASE 3: Update Documentation
**Objective**: Sync docs with code changes
**Actions**: Update READMEs | Regenerate module docs | Update API references | Validate with validators
**Input**: $changes | **Output**: $updated_docs `{readmes_updated[], api_docs[], validation_results[]}`
**Validation**: All docs synced | Validators pass | No broken links

---

## EXECUTION

**Interactive Mode**:
```bash
# Step 1: Analyze
Read analysis_report

# Step 2: Review and approve consolidation plan
Approve changes

# Step 3: Execute consolidation
Make changes

# Step 4: Update docs
Regenerate documentation
```

**Automated Mode** (with approval gates):
```bash
# Execute entire workflow with human approval between phases
```

---

## SUCCESS CRITERIA

- ✅ All duplication removed or documented
- ✅ Code clarity improved (readable, maintainable)
- ✅ LOC reduced (without losing functionality)
- ✅ All files ≤1000 lines (information-dense)
- ✅ Documentation synced with code
- ✅ All validators pass
- ✅ No broken tests

---

## ANTI-PATTERNS TO FIX

**Duplication**: Multiple files with similar functions | Copy-pasted code blocks
**Verbosity**: Excessive comments | Overly descriptive variable names | Redundant documentation
**Structure**: Monolithic files >1000 lines | Poor separation of concerns | Circular dependencies
**Documentation**: Out-of-sync docs | Missing docs | Over-documentation (obvious code)

---

## LESSONS LEARNED (Nov 2025 Fractal Migration)

### Pattern: Fractal Architecture Migration
**Context**: Migrated from centralized `commands/` folder (19 files) to agent-specific `*/commands/` (fractal architecture)

**Issues Detected**:
- 9 duplicated command files between root and agent folders (100% identical)
- 2 orphaned commands without clear agent ownership
- 7 meta-commands misplaced in root instead of `codexa_agent/`
- 27+ obsolete references to consolidated agents (`scout_agent`, `conhecimento_agent`)

**Actions Taken**:
1. Verified file identity with `diff -r commands/ agentes/*/commands/`
2. Deleted root duplicates, kept agent copies as source of truth
3. Moved orphaned commands to appropriate agent folders
4. Verticalized CODEXA meta-commands into `codexa_agent/commands/`
5. Updated all references in PRIME.md, README.md, agent docs
6. Removed empty `commands/` root folder entirely

**Metrics**:
- Duplication: 9 → 0 files (-100%)
- Agent command folders: 2 → 5 (+150%)
- Root command files: 19 → 0 (-100%)
- Clear ownership: 100% of commands now have defined agent owner

**Key Takeaway**: **Fractal principle** = Each agent is self-contained. Commands, prompts, configs live WITH their agent, never duplicated in root. New agents should follow this structure from day 1.

### Pattern: Cleanup Automation with Scout Internal
**Context**: Executed comprehensive cleanup detecting 87+ issues across 6 categories in 61 files

**Categories & Metrics**:
1. **Temp files** (26 found): .backup_* files (20), .bak files (2), __pycache__ (1), old reports (2), NUL files (2)
2. **Obsolete refs** (27 found): References to `scout_agent`/`conhecimento_agent` after consolidation into `mentor_agent`
3. **Broken paths** (9 found): Links to moved files (commands/ → */commands/)
4. **Python organization** (21+ files): Flat root .py files → hierarchical builders/validators/
5. **Empty folders** (4 found): commands/git/, commands/e2e/, orphaned data folders
6. **Migration docs** (5 found): Executed reports with no future value

**Automation Strategy**:
```bash
# Dry-run for safety
./cleanup_scout_internal.sh --dry-run  # Preview changes
# Execute after review
./cleanup_scout_internal.sh --execute  # Apply fixes
```

**Safe Deletion Protocol**:
1. Backup before delete: `git commit -m "backup: pre-cleanup snapshot"`
2. Use `git rm` for traceability (not `rm -f`)
3. Move to `_archived/` instead of deleting (recoverable)
4. Verify with `git diff --stat` before final commit

**Key Takeaway**: Automate detection (find/grep), but require human approval for deletion. Categorize issues for systematic cleanup (6 phases vs. ad-hoc). Always backup first.

### Pattern: Obsolete Documentation Management
**Context**: docs_consolidados/ (14 files, 288KB) contained migration plans already executed

**Files**:
- 43_META_CONSTRUCTION_INDEX.md → Outdated structure map
- 44_MIGRATION_GUIDE.md → Migration already complete
- 45_MIGRATION_STATUS.md → Status from old migration
- 90_CONSOLIDATION_PLAN.md → Plan already executed
- 91-92_RAW_STAGING_WORKFLOW.md → Workflows already implemented
- crud/ subfolder → Architecture already in place

**Decision**:
- **Extract knowledge first**: Create mentor_agent cards (CODEXA_operacoes_48, 49) with lessons learned
- **Then archive**: Move to `_archived/docs_consolidados_2025-11/` for historical reference
- **Don't delete**: Keep in _archived/ for auditability (git doesn't track, but filesystem does)

**Key Takeaway**: Docs have lifecycle - **planning → execution → lessons learned → archive**. Don't delete executed plans; distill insights into knowledge base, then archive originals.

---

## BEST PRACTICES APPLIED

**Information-Dense**: Use keywords not sentences | Pipe notation (|) for lists | Abbreviations where clear
**MAX 1000 LINES**: Split large files | Each file single clear purpose | No "kitchen sink" modules
**DRY (Don't Repeat Yourself)**: Extract to shared modules | Use composition | Template patterns
**Clear Naming**: Function names describe action | File names indicate content | Consistent conventions

---

## TROUBLESHOOTING

**Tests fail after consolidation**: Revert specific change | Check imports | Verify function signatures unchanged
**Docs out of sync**: Re-run validators | Regenerate from code | Manual review
**Circular dependencies**: Refactor to break cycle | Extract interface/protocol | Dependency injection

---

## INTEGRATION WITH v2.0.0 ADWs

- **203_ADW_PARALLEL_ORCHESTRATION.md**: Use for parallel consolidation of large codebases
- **201_ADW_FEATURE_DEVELOPMENT.md**: After consolidation, use for new features
- **100_ADW_DOC_SYNC_WORKFLOW.md**: Run after consolidation to sync documentation

---

**Version**: 2.0.0 | **Updated**: 2025-11-24 | **Maintainer**: CODEXA Team
**Changelog v2.0.0**: Added parallel execution support, batch processing, task boundaries, integration with 203_ADW
**Related**: Scout agent | Validators | PRIME.md | 203_ADW_PARALLEL_ORCHESTRATION.md
