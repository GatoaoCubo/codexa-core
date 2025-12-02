# MIGRATION_GUIDE | CODEXA v1.3 → v2.x Migration

**Version**: 1.0.0 | **Created**: 2025-11-24
**Purpose**: Step-by-step guide for migrating from CODEXA v1.3 to v2.x
**Audience**: Developers using existing CODEXA installations

---

## MIGRATION OVERVIEW

### Version History

| Version | Codename | Key Features |
|---------|----------|--------------|
| v1.3.0 | Foundation | 12 Leverage Points, Template Metaprompt, TAC-7 |
| v2.0.0 | Enrichment | HOP v2.0, ##report standard, src/ integration |
| v2.1.0 | Standards | Code quality validator, design system |
| v2.2.0 | Workflows | ADW Suite v2.0, parallel orchestration |

### Breaking Changes Summary

| Area | v1.3 | v2.x | Migration Action |
|------|------|------|------------------|
| HOPs | TAC-7 only | TAC-7 + 5 new sections | Add new sections |
| Validators | Basic | ##report required | Update validator calls |
| ADWs | v1.0 structure | v2.0 with task boundaries | Update workflow files |
| Builders | Basic | src/ integration | Update imports |

---

## PRE-MIGRATION CHECKLIST

### 1. Backup Current State

```bash
# Create backup tag
cd codexa_agent
git tag -a v1.3-backup -m "Pre-migration backup"
git push origin v1.3-backup

# Verify backup
git log -1 --oneline v1.3-backup
```

### 2. Check Current Version

```bash
# Check PRIME.md version
grep "Version:" PRIME.md

# Expected: **Version**: 1.3.x
```

### 3. Run Current Validators

```bash
# Ensure clean state before migration
python validators/07_hop_sync_validator.py prompts/*.md
python validators/09_readme_validator.py README.md
python validators/10_taxonomy_validator.py
```

### 4. Document Customizations

List any custom modifications:
- [ ] Custom HOPs
- [ ] Modified validators
- [ ] Custom builders
- [ ] Local configurations

---

## PHASE 1: HOP MIGRATION (v1.3 → v2.0)

### What Changed

HOPs now have 5 additional sections after the standard TAC-7:

```markdown
## TAC-7 Sections (unchanged)
1. MODULE_METADATA
2. INPUT_CONTRACT
3. OUTPUT_CONTRACT
4. TASK
5. STEPS
6. VALIDATION
7. CONTEXT

## New v2.0 Sections (add these)
8. PROMPT_LAYER_COMPOSITION
9. TASK_BOUNDARY
10. SRC_INTEGRATION
11. ARTIFACT_OUTPUTS
12. FEEDBACK_LOOP
```

### Migration Steps

**For each HOP file** (`prompts/9*_HOP.md`):

1. **Add PROMPT_LAYER_COMPOSITION**:
```markdown
## PROMPT_LAYER_COMPOSITION

### Recommended Layers
```yaml
base_layers:
  - 01_identity_layer.md
  - 03_tool_usage_layer.md

task_specific:
  - 05_code_conventions.md  # For code tasks
```

### Composition Strategy
[Describe which layers to combine for this HOP's tasks]
```

2. **Add TASK_BOUNDARY**:
```markdown
## TASK_BOUNDARY

### Boundary Declaration
```yaml
TASK_BOUNDARY: [HOP_NAME]_EXECUTION
AGENT: execution_agent
ACCESS: write
SCOPE: [What this HOP modifies]
ROLLBACK: git revert
```

### Phase Boundaries
- Phase 1: [PLANNING] - Read-only exploration
- Phase 2: [BUILDING] - Write with boundaries
```

3. **Add SRC_INTEGRATION**:
```markdown
## SRC_INTEGRATION

### Available Modules
- `src/llm/` - LLM provider abstraction
- `src/tools/` - Tool implementations
- `src/runtime/` - Execution runtime
- `src/auth/` - Authentication

### Usage
```python
from src.llm import get_provider
from src.tools import ToolRegistry
```
```

4. **Add ARTIFACT_OUTPUTS**:
```markdown
## ARTIFACT_OUTPUTS

### Generated Artifacts
| Artifact | Format | Purpose |
|----------|--------|---------|
| [name].md | Markdown | Human readable |
| [name].json | JSON | Structured data |

### Output Directory
`outputs/[task_name]/`
```

5. **Add FEEDBACK_LOOP**:
```markdown
## FEEDBACK_LOOP

### Validation Points
1. After Phase X: [What to validate]
2. After Phase Y: [What to validate]

### Retry Logic
- Max retries: 2
- On failure: [Action]

### Quality Gates
- Minimum score: 0.85
- Required validations: [List]
```

### Automated Migration Script

```python
# Run HOP migration
python scripts/migrate_hops_v2.py --all

# Or individual HOP
python scripts/migrate_hops_v2.py prompts/91_meta_build_agent_HOP.md
```

---

## PHASE 2: VALIDATOR MIGRATION (v1.3 → v2.0)

### What Changed

All validators now must generate ##report output:

```python
# Old (v1.3)
def validate(file):
    issues = check_file(file)
    if issues:
        print(f"Found {len(issues)} issues")
    return len(issues) == 0

# New (v2.0)
from validators.report_generator import ValidatorReportGenerator

def validate(file):
    report = ValidatorReportGenerator("validator_name", "2.0.0")
    issues = check_file(file)
    for issue in issues:
        report.add_issue(issue['severity'], issue['category'], issue['message'])
    return report.generate()  # Returns (success, json_report, md_report)
```

### Migration Steps

**For each validator** (`validators/*.py`):

1. **Add report generator import**:
```python
from validators.report_generator import ValidatorReportGenerator
```

2. **Initialize report at start**:
```python
def validate(target):
    report = ValidatorReportGenerator(
        module_name="your_validator",
        version="2.0.0"
    )
```

3. **Replace print statements with report.add_issue()**:
```python
# Old
print(f"ERROR: {message}")

# New
report.add_issue("error", "category", message, file=filepath, line=line_num)
```

4. **Return report at end**:
```python
# Old
return success

# New
success, json_report, md_report = report.generate()
report.print_summary()
return success
```

### Example Migration

```python
# Before (v1.3)
def validate_readme(path):
    errors = []
    with open(path) as f:
        content = f.read()
    if "## Purpose" not in content:
        errors.append("Missing Purpose section")
        print("ERROR: Missing Purpose section")
    return len(errors) == 0

# After (v2.0)
from validators.report_generator import ValidatorReportGenerator

def validate_readme(path):
    report = ValidatorReportGenerator("readme_validator", "2.0.0")

    with open(path) as f:
        content = f.read()

    if "## Purpose" not in content:
        report.add_issue(
            severity="error",
            category="structure",
            message="Missing Purpose section",
            file=path
        )

    success, json_out, md_out = report.generate()
    report.print_summary()
    return success
```

---

## PHASE 3: ADW MIGRATION (v1.0 → v2.0)

### What Changed

ADWs now include:
- Version specification in JSON
- v2_enhancements block
- Task boundary sections
- Integration with new ADWs

### Migration Steps

**For each ADW** (`workflows/*_ADW_*.md`):

1. **Update version header**:
```markdown
# Before
**Type**: 5-Phase ADW | **Duration**: 20-40 minutes

# After
**Type**: 5-Phase ADW | **Duration**: 20-40 minutes
**Version**: 2.0.0 | **Updated**: 2025-11-24
```

2. **Add v2_enhancements to JSON spec**:
```json
{
  "workflow_id": "your_workflow",
  "version": "2.0.0",

  "v2_enhancements": {
    "two_phase_planning": true,
    "task_boundaries": true,
    "artifact_generation": true
  },

  "phases": [...]
}
```

3. **Add enhancement section** (after WORKFLOW SPECIFICATION):
```markdown
## [ENHANCEMENT_NAME] (v2.0.0 Enhancement)

### Pattern Description
[What this enhancement adds]

### Usage
[How to use it]

### Integration
[How it connects to 201/202/203 ADWs]
```

4. **Update footer**:
```markdown
## INTEGRATION WITH v2.0.0 ADWs

- **201_ADW_FEATURE_DEVELOPMENT.md**: [When to use]
- **202_ADW_BUG_FIXING.md**: [When to use]
- **203_ADW_PARALLEL_ORCHESTRATION.md**: [When to use]

---

**Version**: 2.0.0 | **Updated**: 2025-11-24 | **Maintainer**: CODEXA Team
**Changelog v2.0.0**: [List changes]
```

---

## PHASE 4: BUILDER MIGRATION (v1.3 → v2.0)

### What Changed

Builders now integrate with `src/` modules:

```python
# Old (v1.3) - Direct implementation
import openai
client = openai.Client()

# New (v2.0) - src/ abstraction
from src.llm import get_provider
provider = get_provider("openai")
```

### Migration Steps

1. **Update imports**:
```python
# Add src imports
from src.llm import get_provider, LLMConfig
from src.tools import ToolRegistry
from src.runtime import PromptLoader
```

2. **Use provider abstraction**:
```python
# Old
response = openai.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

# New
provider = get_provider("openai")
response = provider.complete(prompt, model="gpt-4")
```

3. **Add ##report generation**:
```python
from validators.report_generator import ValidatorReportGenerator

def build(args):
    report = ValidatorReportGenerator("builder_name", "2.0.0")
    # ... build logic ...
    report.add_artifact("output.md")
    return report.generate()
```

---

## PHASE 5: NEW FILES TO CREATE

### Required New Files

If not present, create these files:

1. **validators/report_generator.py** (if missing)
2. **validators/13_code_quality_validator.py**
3. **templates/CODE_STYLE_GUIDE.md**
4. **templates/DESIGN_SYSTEM.md**
5. **workflows/201_ADW_FEATURE_DEVELOPMENT.md**
6. **workflows/202_ADW_BUG_FIXING.md**
7. **workflows/203_ADW_PARALLEL_ORCHESTRATION.md**

### Copy from Reference

```bash
# If migrating existing installation, copy new files
cp reference/validators/13_code_quality_validator.py validators/
cp reference/workflows/20*.md workflows/
cp reference/templates/*.md templates/
```

---

## PHASE 6: PRIME.MD UPDATE

### Update Version

```markdown
# Change
**Version**: 1.3.x

# To
**Version**: 2.2.0
```

### Add New Sections

1. **Add Primary ADWs section** (after Primary Validators):
```markdown
**Primary ADWs** (v2.0.0):
- `201_ADW_FEATURE_DEVELOPMENT.md` - Two-phase planning
- `202_ADW_BUG_FIXING.md` - Systematic bug fixing
- `203_ADW_PARALLEL_ORCHESTRATION.md` - Multi-agent parallel
- `97_ADW_NEW_AGENT_WORKFLOW.md` - Agent creation
- `100_ADW_DOC_SYNC_WORKFLOW.md` - Documentation sync
```

2. **Add Changelog**:
```markdown
**Changelog v2.2.0** (PHASE 6 WORKFLOWS):
- Created 201/202/203 ADWs
- Enriched all existing ADWs to v2.0.0

**Changelog v2.1.0** (PHASE 5 STANDARDS):
- Created code quality validator
- Created design system reference

**Changelog v2.0.0** (PHASE 4 ENRICHMENT):
- HOP Framework v2.0.0 with 5 new sections
- ##report standard for all validators
```

---

## POST-MIGRATION VALIDATION

### Run All Validators

```bash
# Validate HOPs
python validators/07_hop_sync_validator.py prompts/*.md

# Validate documentation
python validators/09_readme_validator.py README.md
python validators/12_doc_sync_validator.py --all

# Validate code quality
python validators/13_code_quality_validator.py builders/
python validators/13_code_quality_validator.py validators/

# Validate taxonomy
python validators/10_taxonomy_validator.py
```

### Test ADWs

```bash
# Test feature development (dry run)
uv run workflows/201_ADW_FEATURE_DEVELOPMENT.py --dry-run "Test feature"

# Test bug fixing (dry run)
uv run workflows/202_ADW_BUG_FIXING.py --dry-run "Test bug"
```

### Verify Versions

```bash
# All files should show v2.x
grep -r "Version.*2\." *.md prompts/*.md workflows/*.md
```

---

## ROLLBACK PROCEDURE

If migration fails:

```bash
# 1. Reset to backup
git reset --hard v1.3-backup

# 2. Verify rollback
grep "Version:" PRIME.md  # Should show 1.3.x

# 3. Run validators to confirm
python validators/07_hop_sync_validator.py prompts/*.md
```

---

## MIGRATION TIMELINE

| Step | Duration | Dependencies |
|------|----------|--------------|
| Pre-migration checks | 15 min | None |
| HOP migration | 30 min | Pre-checks |
| Validator migration | 30 min | Pre-checks |
| ADW migration | 20 min | Pre-checks |
| Builder migration | 20 min | Pre-checks |
| New files creation | 10 min | Previous steps |
| PRIME.md update | 10 min | Previous steps |
| Post-migration validation | 20 min | All steps |

**Total estimated time**: 2-3 hours

---

## COMMON MIGRATION ISSUES

### Issue: Missing report_generator.py

```
ImportError: No module named 'validators.report_generator'
```

**Solution**: Create or copy report_generator.py to validators/

### Issue: HOP validation fails after migration

```
ERROR: Missing PROMPT_LAYER_COMPOSITION section
```

**Solution**: Add all 5 new sections to HOP

### Issue: ADW version mismatch

```
WARNING: ADW version 1.0.0 detected, expected 2.0.0
```

**Solution**: Update ADW JSON spec version and add v2_enhancements

### Issue: src/ imports fail

```
ImportError: No module named 'src'
```

**Solution**: Ensure src/ directory exists with __init__.py files

---

## SUPPORT

If you encounter issues during migration:

1. Check this guide's troubleshooting section
2. Review INTEGRATION_GUIDE.md for feature usage
3. Check BEST_PRACTICES.md for patterns
4. Rollback if needed, then retry

---

**Version**: 1.0.0
**Status**: Complete Migration Guide
**Covers**: v1.3.0 → v2.2.0
**Maintainer**: CODEXA Team
