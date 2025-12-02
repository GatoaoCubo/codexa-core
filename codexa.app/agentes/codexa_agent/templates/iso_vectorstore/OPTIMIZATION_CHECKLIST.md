# ISO_VECTORSTORE Optimization Checklist

**Agent**: {AGENT_NAME}
**Date**: {DATE}
**Executor**: {EXECUTOR}

---

## PRE-OPTIMIZATION

### Discovery
- [ ] Navigate to `agentes/{AGENT_NAME}/iso_vectorstore/`
- [ ] Count total files: ____
- [ ] Estimate total tokens: ____
- [ ] Categorize files by type

### Scope Analysis
- [ ] Read PRIME.md
- [ ] Identify scope: ____________
- [ ] List what agent GENERATES: ____________
- [ ] List what agent DELEGATES: ____________
- [ ] Identify out-of-scope files: ____________

### HOP Audit
- [ ] List all HOP_*.md files
- [ ] Count tokens per HOP
- [ ] Flag HOPs > 1500 tokens
- [ ] Identify garbage patterns

---

## OPTIMIZATION

### File Reduction
- [ ] Delete out-of-scope files
- [ ] Renumber if gaps exist
- [ ] Update references to renamed files

### HOP Optimization (per bloated HOP)

**HOP: ____________**
- [ ] Backup original (.bak)
- [ ] Extract essential sections
- [ ] Remove garbage (YAML, duplicates, injection)
- [ ] Rewrite to target tokens
- [ ] Verify < 1500 tokens
- [ ] Test essential instructions preserved

### Version Sync
- [ ] Determine canonical version: ____
- [ ] Update 00_MANIFEST.md
- [ ] Update 01_QUICK_START.md
- [ ] Update 02_PRIME.md
- [ ] Update 03_INSTRUCTIONS.md
- [ ] Update 04_README.md
- [ ] Update 05_ARCHITECTURE.md
- [ ] Update all HOPs

---

## GENERATION

### MANIFEST
- [ ] Use template: 00_MANIFEST_TEMPLATE.md
- [ ] Fill all variables
- [ ] Verify file inventory accurate
- [ ] Save to iso_vectorstore/00_MANIFEST.md

### SYSTEM_INSTRUCTIONS
- [ ] Use template: SYSTEM_INSTRUCTIONS_TEMPLATE.md
- [ ] Fill all variables
- [ ] Add {$INPUT} variable sources
- [ ] Add execution examples
- [ ] Save to agent/SYSTEM_INSTRUCTIONS_AGENT_BUILDER.md

---

## VALIDATION

### File Count
- [ ] Target: <= 21
- [ ] Actual: ____
- [ ] Status: PASS / FAIL

### Token Estimate
- [ ] Target: < 15,000
- [ ] Actual: ____
- [ ] Status: PASS / FAIL

### Version Consistency
- [ ] Target: 100%
- [ ] Actual: ____
- [ ] Status: PASS / FAIL

### MANIFEST Present
- [ ] Status: PASS / FAIL

### SYSTEM_INSTRUCTIONS Present
- [ ] Status: PASS / FAIL

### HOPs Optimized
- [ ] All HOPs < 1500 tokens
- [ ] Status: PASS / FAIL

---

## POST-OPTIMIZATION

### Report
- [ ] Generate optimization report
- [ ] Document all changes
- [ ] Calculate reduction metrics
- [ ] Save report

### Commit
- [ ] Stage changes: `git add agentes/{AGENT_NAME}/iso_vectorstore/`
- [ ] Commit: `git commit -m "feat({AGENT_NAME}): optimize iso_vectorstore v{VERSION}"`
- [ ] Push (if approved)

---

## METRICS

| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Files | ____ | ____ | ____% |
| Tokens | ____ | ____ | ____% |
| HOPs optimized | - | ____ | - |
| Version | ____ | ____ | - |

---

## NOTES

{NOTES}

---

**Completed**: [ ] YES / [ ] NO
**Overall Status**: PASS / PASS_WITH_WARNINGS / FAIL
**Signed**: ____________
**Date**: ____________
