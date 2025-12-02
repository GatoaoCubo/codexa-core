# 202_ADW_BUG_FIXING | Systematic Bug Fixing Workflow

**Version**: 2.0.0 | **Created**: 2025-11-24
**Type**: 5-Phase ADW (Reproduction -> Root Cause -> Fix -> Verify -> Document)
**Duration**: 15-45 minutes (depends on bug complexity)
**Pattern**: Minimal Fix Principle - Change only what's necessary

---

## MODULE_METADATA

```yaml
id: 202_ADW_BUG_FIXING
version: 2.0.0
category: development-workflows
type: ADW (Agentic Developer Workflow)
execution_mode: sequential_with_gates
dependencies:
  - validators/13_code_quality_validator.py
  - prompts/layers/05_code_conventions.md
status: production_ready
created: 2025-11-24
platform_patterns:
  - Cursor: systematic debugging, code research
  - Claude Code: minimal changes, no over-engineering
  - Windsurf: defensive fixes, boundary validation
  - Devin: root cause analysis, comprehensive testing
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "bug_fixing",
  "workflow_name": "Systematic Bug Fixing Workflow",
  "version": "2.0.0",
  "context_strategy": "focused",
  "failure_handling": "stop_and_escalate",

  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "bug_fixing"},
    {"phase_id": "phase_1_reproduce", "phase_name": "Bug Reproduction", "duration": "3-10min"},
    {"phase_id": "phase_2_root_cause", "phase_name": "Root Cause Analysis", "duration": "5-15min"},
    {"phase_id": "phase_3_fix", "phase_name": "Fix Development", "duration": "5-15min"},
    {"phase_id": "phase_4_verify", "phase_name": "Verification", "duration": "3-5min"},
    {"phase_id": "phase_5_document", "phase_name": "Documentation", "duration": "2-5min"}
  ],

  "principles": {
    "minimal_fix": "Change only what's necessary to fix the bug",
    "no_refactoring": "Don't improve surrounding code during bug fix",
    "test_first": "Write failing test before fixing",
    "regression_prevention": "Ensure fix doesn't break existing functionality"
  }
}
```

---

## CORE PRINCIPLE: MINIMAL FIX

### What Minimal Fix Means

**DO**:
- Fix the exact issue reported
- Add test that catches the bug
- Update any directly affected documentation
- Commit with clear message referencing issue

**DON'T**:
- Refactor surrounding code "while we're here"
- Add features or improvements
- Change code style of untouched lines
- Add extra error handling beyond what's needed

### Why Minimal Fix?

1. **Reduces Risk**: Fewer changes = fewer potential regressions
2. **Easier Review**: Clear scope makes review faster
3. **Better Traceability**: git blame shows exact fix
4. **Faster Deployment**: Smaller changes deploy with confidence

---

## PHASE DETAILS

### PHASE 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `bug_fixing`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

### PHASE 1: Bug Reproduction

**Objective**: Confirm bug exists and document reproduction steps

**Task Boundary Declaration**:
```
TASK_BOUNDARY: REPRODUCTION
ACCESS: read_only + test_execution
SCOPE: Confirm and document bug behavior
```

**Actions**:
1.1. **Understand Bug Report**
   - Read issue/bug description
   - Identify expected vs actual behavior
   - Note any error messages or logs

1.2. **Reproduce Bug**
   - Set up reproduction environment
   - Follow reported steps
   - Confirm bug occurs
   - If cannot reproduce: document attempts, ask for more info

1.3. **Document Reproduction**
   ```yaml
   reproduction:
     steps:
       - "Step 1: [action]"
       - "Step 2: [action]"
     expected: "[what should happen]"
     actual: "[what actually happens]"
     error_message: "[if any]"
     environment:
       os: str
       version: str
       relevant_config: {}
   ```

1.4. **Write Failing Test** (Test-First)
   - Create test that fails due to bug
   - Test should pass after fix
   - This test becomes regression protection

**Input**: Bug report (issue description)
**Output**: `$reproduction_report`, failing test file

**Validation**:
- Bug successfully reproduced
- Failing test written
- Reproduction steps documented

**If Cannot Reproduce**:
- Document all attempts
- Request more information from reporter
- Check if already fixed in newer version
- Escalate if needed

---

### PHASE 2: Root Cause Analysis

**Objective**: Find the actual cause of the bug (not just symptoms)

**Task Boundary Declaration**:
```
TASK_BOUNDARY: ROOT_CAUSE_ANALYSIS
ACCESS: read_only
SCOPE: Identify exact cause of bug
```

**Actions**:
2.1. **Trace Execution Path**
   - Start from failure point
   - Trace backwards through call stack
   - Identify where behavior diverges from expected

2.2. **Identify Root Cause**
   - Common causes checklist:
     ```
     [ ] Off-by-one error
     [ ] Null/undefined handling
     [ ] Type coercion issue
     [ ] Race condition
     [ ] Missing validation
     [ ] Incorrect comparison
     [ ] Edge case not handled
     [ ] Wrong variable reference
     [ ] Stale cache/state
     [ ] External dependency change
     ```

2.3. **Verify Root Cause**
   - Mentally trace: if we fix X, does bug disappear?
   - Check if same pattern exists elsewhere (potential other bugs)
   - Confirm this is ROOT cause, not symptom

2.4. **Document Root Cause**
   ```yaml
   root_cause:
     file: "path/to/file.py"
     line: 42
     issue: "Null check missing before accessing property"
     category: "null_handling"
     introduced_by: "[commit/PR if known]"
     affected_scope: "[what else might be affected]"
   ```

**Input**: `$reproduction_report`
**Output**: `$root_cause_analysis`

**Validation**:
- Root cause identified (not just symptom)
- Location pinpointed (file + line)
- Category determined

---

### PHASE 3: Fix Development

**Objective**: Implement minimal fix with tests

**Task Boundary Declaration**:
```
TASK_BOUNDARY: FIX_IMPLEMENTATION
ACCESS: write
SCOPE: Minimal fix for identified root cause
CONSTRAINT: No refactoring, no improvements
```

**Actions**:
3.1. **Design Minimal Fix**
   - What's the smallest change to fix the issue?
   - Consider edge cases in same area
   - Don't add extra defensive code elsewhere

3.2. **Implement Fix**
   - Change ONLY what's necessary
   - Follow existing code style exactly
   - Don't add comments explaining obvious code
   - Don't update type annotations on unchanged lines

3.3. **Update Failing Test**
   - Verify failing test now passes
   - Add additional edge case tests if directly relevant
   - Don't add unrelated tests

3.4. **Run Affected Tests**
   - Run tests in affected module
   - Watch for regressions
   - Fix any test failures caused by fix

**Input**: `$root_cause_analysis`
**Output**: `$fix_implementation`
```yaml
$fix_implementation:
  files_modified:
    - file: "path/to/file.py"
      lines_changed: 3
      description: "Added null check before accessing property"
  tests_updated:
    - file: "tests/test_file.py"
      tests_added: 1
      tests_modified: 0
  lines_of_code_changed: 5  # Should be small
```

**Validation**:
- Fix addresses root cause
- Failing test now passes
- All existing tests still pass
- Lines changed < 50 (for most bugs)

---

### PHASE 4: Verification

**Objective**: Comprehensive verification of fix

**Task Boundary Declaration**:
```
TASK_BOUNDARY: VERIFICATION
ACCESS: read_only + test_execution
SCOPE: Verify fix is complete and safe
```

**Actions**:
4.1. **Reproduction Test**
   - Re-run original reproduction steps
   - Confirm bug no longer occurs
   - Confirm expected behavior achieved

4.2. **Regression Testing**
   - Run full test suite
   - Focus on affected module tests
   - Run integration tests if applicable

4.3. **Code Quality Check**
   ```bash
   python validators/13_code_quality_validator.py [changed_files]
   ```
   - Verify no quality degradation
   - Check naming conventions followed

4.4. **Edge Case Verification**
   - Test boundary conditions
   - Test with null/empty inputs
   - Test with extreme values

**Input**: `$fix_implementation`
**Output**: `$verification_report`
```yaml
$verification_report:
  reproduction_test: "pass|fail"
  regression_tests:
    total: int
    passed: int
    failed: int
  code_quality_score: float
  edge_cases_verified: []
  issues_found: []
  verdict: "approved|needs_work"
```

**Validation**:
- Bug no longer reproduces
- All tests pass
- Code quality >= 0.85
- No new issues introduced

---

### PHASE 5: Documentation

**Objective**: Document fix for future reference

**Task Boundary Declaration**:
```
TASK_BOUNDARY: DOCUMENTATION
ACCESS: write
SCOPE: Commit message, changelog, issue update
```

**Actions**:
5.1. **Commit Message**
   ```
   fix([scope]): [brief description]

   - Root cause: [what was wrong]
   - Fix: [what was changed]
   - Tests: [what tests added]

   Fixes #[issue_number]

   Co-Authored-By: Claude <noreply@anthropic.com>
   ```

5.2. **Changelog Entry** (if applicable)
   ```markdown
   ### Fixed
   - [Brief description of fix] (#[PR_number])
   ```

5.3. **Issue Update** (if using issue tracker)
   - Reference commit/PR
   - Describe root cause found
   - Describe fix applied
   - Note any follow-up needed

5.4. **Generate ##report**
   ```yaml
   ##report:
     workflow: bug_fixing
     issue: str
     root_cause: str
     fix_summary: str
     files_changed: []
     tests_added: []
     verification: pass|fail
   ```

**Input**: `$verification_report`, `$fix_implementation`
**Output**: Commit, changelog entry, `$final_report`

**Validation**:
- Commit message follows convention
- Issue referenced in commit
- Changelog updated (if maintaining one)

---

## EXECUTION

### Command Line
```bash
# Basic execution
uv run workflows/202_ADW_BUG_FIXING.py "Bug: Login fails with special characters"

# With issue reference
uv run workflows/202_ADW_BUG_FIXING.py --issue "#123" "Login fails with special characters"
```

### Manual Execution
```bash
# Phase 1: Reproduce
# Read bug report, reproduce issue, write failing test

# Phase 2: Root Cause
# Trace execution, identify cause

# Phase 3: Fix
# Minimal fix only

# Phase 4: Verify
# Run tests, check quality

# Phase 5: Document
# Commit with proper message
```

---

## BUG SEVERITY CLASSIFICATION

| Severity | Description | Max Duration |
|----------|-------------|--------------|
| Critical | System down, data loss | 2 hours |
| High | Major feature broken | 4 hours |
| Medium | Feature partially broken | 1 day |
| Low | Minor inconvenience | 1 week |

**Escalation**: If fix takes longer than max duration, escalate to team lead.

---

## COMMON BUG PATTERNS

### Null/Undefined Handling
```python
# Bug: AttributeError when user.profile is None
# Fix: Add null check
if user.profile is not None:
    return user.profile.name
return default_name
```

### Off-by-One
```python
# Bug: Last item never processed
# Fix: Use <= instead of <
for i in range(len(items)):  # Not range(len(items) - 1)
```

### Type Coercion
```javascript
// Bug: "10" + 5 = "105" instead of 15
// Fix: Explicit conversion
const sum = Number(a) + Number(b);
```

### Race Condition
```python
# Bug: Data inconsistency under concurrent access
# Fix: Add locking
with lock:
    value = get_value()
    set_value(value + 1)
```

### Missing Validation
```python
# Bug: Crash on empty input
# Fix: Add validation at boundary
def process(data):
    if not data:
        raise ValueError("Data cannot be empty")
```

---

## ANTI-PATTERNS TO AVOID

**Shotgun Debugging**:
- Randomly changing things hoping something works
- Fix: Use systematic root cause analysis

**Fixing Symptoms**:
- Adding try/except around error instead of fixing cause
- Fix: Find and fix actual root cause

**Over-Fixing**:
- Refactoring entire module while fixing one bug
- Fix: Minimal fix only, create separate refactoring task

**Silent Fixes**:
- Fixing bug without adding test
- Fix: Always add regression test

**Copy-Paste Fixes**:
- Copying fix to multiple places
- Fix: Extract to shared function (but as separate task)

---

## SUCCESS CRITERIA

**Workflow Succeeds When**:
- Bug confirmed and reproduced
- Root cause identified (not symptom)
- Minimal fix implemented
- Regression test added
- All tests pass
- Code quality maintained
- Proper commit message with issue reference

**Workflow Fails When**:
- Cannot reproduce bug (need more info)
- Root cause unclear (need more investigation)
- Fix causes regressions
- Fix is too invasive (>50 lines for typical bug)

---

## RELATED WORKFLOWS

- `201_ADW_FEATURE_DEVELOPMENT.md` - For new features
- `203_ADW_PARALLEL_ORCHESTRATION.md` - For multiple bugs
- `98_ADW_CONSOLIDATION_WORKFLOW.md` - For refactoring after fixes

---

**Version**: 2.0.0
**Status**: Production-Ready
**Principle**: Minimal Fix - Don't improve, just fix
**Maintainer**: CODEXA Team
