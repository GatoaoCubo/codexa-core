# ADW-100: Documentation Synchronization System

**Version**: 1.0.0
**Status**: ✅ Specification Complete | ⏳ Implementation Pending
**Created**: 2025-11-14
**Type**: Fully Automatic CI/CD-Style Workflow

---

## 🎯 Purpose

**ADW-100** is a complete **documentation synchronization and standardization system** for all CODEXA agents. It automatically:

1. **Validates** all documentation (README, PRIME, INSTRUCTIONS, SETUP)
2. **Detects inconsistencies** (versions, structure, registry sync)
3. **Generates missing files** using standardized templates
4. **Synchronizes** all documentation across agents
5. **Reports** quality scores and recommendations

---

## 📦 Components

### 1. Workflow Specification
**File**: `100_ADW_DOC_SYNC_WORKFLOW.md`
**Purpose**: Complete 10-step workflow for automatic documentation sync
**Status**: ✅ Complete

**Workflow Steps**:
1. DISCOVERY & AUDIT - Scan all agents (2-5min)
2. TEMPLATE GENERATION - Create standardized templates (1-2min)
3. VARIABLE EXTRACTION - Agent-specific data (2-5min/agent)
4. DOCUMENTATION GENERATION - Apply templates (1-2min/agent)
5. STRUCTURE VALIDATION - README ↔ filesystem sync (1-2min/agent)
6. HOP SYNC VALIDATION - INSTRUCTIONS ↔ prompts/ (1-2min/agent)
7. VERSION SYNCHRONIZATION - Sync all versions (30s/agent)
8. TAXONOMY VALIDATION - Registry ↔ docs (1min)
9. QUALITY GATE VALIDATION - Run all validators (2-3min)
10. REPORT GENERATION & COMMIT - Final report + git commit (1min)

**Total Time**: ~30min for 5 agents (~6min per agent)

---

### 2. Documentation Templates
**Location**: `templates/docs/`
**Status**: ✅ Complete

**Templates**:
- `INSTRUCTIONS_TEMPLATE.md` - HOP format for agent builders (AI assistants)
- `SETUP_TEMPLATE.md` - Universal installation guide (all platforms)
- `README_TEMPLATE.md` - Agent overview (TODO)
- `PRIME_TEMPLATE.md` - TAC-7 format agent context (TODO)

**Features**:
- [VARIABLE] placeholders for agent-specific content
- Consistent structure across all agents
- Platform-agnostic (Claude, OpenAI, Gemini, etc.)
- Discovery-first workflow patterns

---

### 3. Validator
**File**: `validators/12_doc_sync_validator.py`
**Purpose**: Validate documentation synchronization
**Status**: ✅ Complete & Tested

**Validations** (6 checks):
1. **files_present** (25% weight) - All 4 files exist?
2. **version_consistency** (20% weight) - Same version across all docs?
3. **structure_sync** (15% weight) - README structure ↔ filesystem match?
4. **line_limits** (10% weight) - All files ≤1000 lines?
5. **no_template_variables** (15% weight) - No [VARIABLES] left?
6. **registry_sync** (15% weight) - Agent in AGENT_REGISTRY.json?

**Quality Thresholds**:
- **EXCELLENT** (≥0.90): Production-ready, zero issues
- **GOOD** (0.85-0.89): Minor improvements needed
- **FAIR** (0.75-0.84): Some fixes required
- **POOR** (<0.75): Major work needed

**Usage**:
```bash
# Validate single agent
python validators/12_doc_sync_validator.py anuncio_agent

# Validate all agents
python validators/12_doc_sync_validator.py --all

# Generate report
python validators/12_doc_sync_validator.py --all --output report.md
```

---

### 4. Builder (TODO)
**File**: `builders/11_doc_sync_builder.py`
**Purpose**: Automatic documentation generation and fixing
**Status**: ⏳ Pending Implementation

**Key Functions** (planned):
```python
def scan_agents(directory: str) -> dict
def extract_variables(agent_path: str) -> dict
def apply_template(template: str, variables: dict) -> str
def validate_structure_sync(readme: str, filesystem: list) -> float
def validate_hop_sync(instructions: str, prompts_dir: str) -> float
def sync_versions(agent_files: list) -> str
def calculate_quality_score(agent_results: dict) -> float
def generate_report(results: dict) -> tuple[str, str]  # (md, json)
```

**Execution Modes**:
- `audit_only` - Generate report, no changes
- `auto_fix` - Auto-apply fixes (default)
- `interactive` - Ask before each fix

---

## 📊 Current Status (2025-11-14)

### Validation Results

**5 agents validated**:
- **Average Score**: 0.55 / 1.00 (POOR)
- **Agents ≥0.85**: 0 / 5 (0%)

**Quality Distribution**:
- EXCELLENT (≥0.90): 0 agents
- GOOD (0.85-0.89): 0 agents
- FAIR (0.75-0.84): 0 agents
- POOR (<0.75): **5 agents** ❌

### Key Issues Detected

**Missing Files** (7 total):
- INSTRUCTIONS.md: 2 agents (anuncio, marca)
- SETUP.md: 4 agents (codexa, marca, mentor, pesquisa)

**Version Inconsistencies**:
- anuncio_agent: SETUP.md v1.0.0 vs README/PRIME v1.2.1
- marca_agent: No versions found in any file

**Structure Issues**:
- codexa_agent: Missing `workflows/` in README structure
- marca_agent, mentor_agent, pesquisa_agent: No STRUCTURE section

**Registry Issues**:
- anuncio_agent, codexa_agent: NOT in AGENT_REGISTRY.json

**Full Report**: See `workflows/reports/DOC_SYNC_AUDIT_20251114.md`

---

## 🚀 How to Use

### Step 1: Validate Current State
```bash
cd codexa_agent
python validators/12_doc_sync_validator.py --all --output validation_report.md
```

Review the report to understand current issues.

### Step 2: Manual Fixes (Until Builder Implemented)

**Option A: Fix individually** (4-6 hours)
1. Create missing INSTRUCTIONS files (use templates)
2. Create missing SETUP files (use templates)
3. Synchronize versions
4. Update AGENT_REGISTRY.json
5. Add STRUCTURE sections to READMEs

**Option B: Wait for auto-fix** (8-12 hours to implement builder)
1. Implement `builders/11_doc_sync_builder.py`
2. Run `python builders/11_doc_sync_builder.py --mode auto_fix`
3. Review and commit changes

### Step 3: Re-validate
```bash
python validators/12_doc_sync_validator.py --all
```

Target: ALL agents ≥0.85 quality score

---

## 📈 Roadmap

### Phase 1: Foundation ✅ COMPLETE
- [x] ADW-100 workflow specification
- [x] INSTRUCTIONS template
- [x] SETUP template
- [x] Documentation validator (12_doc_sync_validator.py)
- [x] Test on all agents
- [x] Generate initial audit report

### Phase 2: Manual Fixes ⏳ CURRENT
- [ ] Create missing INSTRUCTIONS files (2 agents)
- [ ] Create missing SETUP files (4 agents)
- [ ] Synchronize versions (1 agent)
- [ ] Update AGENT_REGISTRY.json (2 agents)
- [ ] Add STRUCTURE sections (3 agents)

**Target**: Average score ≥0.80 (FAIR)
**Estimated Effort**: 4-6 hours
**Timeline**: 2025-11-15

### Phase 3: Automation 📋 PLANNED
- [ ] Implement builders/11_doc_sync_builder.py
- [ ] Test auto-fix mode on one agent
- [ ] Roll out to all agents
- [ ] Integrate with git workflows

**Target**: Average score ≥0.90 (EXCELLENT)
**Estimated Effort**: 8-12 hours development
**Timeline**: 2025-11-16 to 2025-11-18

### Phase 4: CI/CD Integration 🔮 FUTURE
- [ ] Pre-commit hook (validate before commit)
- [ ] GitHub Actions workflow (auto-validate on PR)
- [ ] Automatic monthly audits
- [ ] Dashboard for quality metrics

---

## 🎓 Design Principles

**Meta-Construction**:
- Build the builder, not the instance
- Templates > one-offs
- Reusable patterns across all agents

**Automation**:
- Zero manual intervention for repetitive tasks
- Human review for critical decisions
- Git-safe: all changes reviewable and revertible

**Quality Gates**:
- Threshold: ≥0.85 for production
- Blocking validation: prevent bad commits
- Continuous improvement: monthly re-audits

**Self-Improvement**:
- CODEXA uses ADW-100 to sync its own documentation
- Validator can validate itself
- Bootstrapping complete

---

## 📚 Related Files

**Workflows**:
- `100_ADW_DOC_SYNC_WORKFLOW.md` - Complete workflow specification
- `97_ADW_NEW_AGENT_WORKFLOW.md` - Uses doc templates
- `98_ADW_CONSOLIDATION_WORKFLOW.md` - Runs doc sync as final step

**Templates**:
- `templates/docs/INSTRUCTIONS_TEMPLATE.md` - Agent instructions
- `templates/docs/SETUP_TEMPLATE.md` - Installation guide

**Validators**:
- `validators/12_doc_sync_validator.py` - Main validator
- `validators/09_readme_validator.py` - README standards
- `validators/07_hop_sync_validator.py` - HOP TAC-7 compliance
- `validators/10_taxonomy_validator.py` - Registry consistency

**Reports**:
- `workflows/reports/DOC_SYNC_AUDIT_20251114.md` - Current audit

---

## 💡 Pro Tips

1. **Run validator frequently**: After every doc change
2. **Use templates**: Don't write from scratch
3. **Sync versions**: Update all files together
4. **Review diffs**: Before committing auto-fixes
5. **Target 0.85+**: Don't settle for FAIR (0.75-0.84)

---

## ✅ Success Criteria

**ADW-100 succeeds when**:
- ✅ ALL agents ≥0.85 quality score
- ✅ 100% documentation files present (4 per agent)
- ✅ 100% version synchronization
- ✅ ≥95% structure accuracy (README ↔ filesystem)
- ✅ 100% HOP sync (INSTRUCTIONS ↔ prompts/)
- ✅ 100% registry accuracy
- ✅ Zero critical validation errors

**Current Progress**:
- Average Score: 0.55 → **Target: 0.90** (gap: +0.35)
- Files Present: 65% → **Target: 100%** (gap: +35%)
- Version Sync: 60% → **Target: 100%** (gap: +40%)
- Registry Sync: 20% → **Target: 100%** (gap: +80%)

---

## 📞 Support

**Questions or Issues?**
- Read: `100_ADW_DOC_SYNC_WORKFLOW.md` (full specification)
- Check: `workflows/reports/DOC_SYNC_AUDIT_20251114.md` (current state)
- Run: `python validators/12_doc_sync_validator.py --help`

---

**Version**: 1.0.0
**Status**: ✅ Specification Complete | ⏳ Implementation Pending
**Next Milestone**: Manual fixes → Target avg score 0.80+ by 2025-11-15

---

> 🏗️ **Meta-Construction**: ADW-100 builds the documentation that describes the agents
> 🔄 **Self-Improving**: CODEXA uses ADW-100 to sync its own documentation
> ✅ **CI/CD Ready**: Fully automatic, zero manual intervention (when builder implemented)
