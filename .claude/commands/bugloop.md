# /bugloop | Autonomous Bug-Fix Feedback Loop

**Purpose**: Execute autonomous test→review→fix→verify→commit→push cycle
**Time**: 2-10 min per cycle | **Output**: Fixed code + commit + bugfix log

---

## QUICK START

```bash
# Full autonomous cycle (LEVEL 4)
/bugloop

# Observe only - report what would be fixed
/bugloop --dry-run

# Single iteration (no loop)
/bugloop --once

# With explicit confirmation before push
/bugloop --confirm-push
```

---

## WORKFLOW

```
┌─────────────────────────────────────────────────────────────────┐
│  PHASE 1: TEST                                                  │
│  ├── Run test suite (pytest / npm test / uv run tests)         │
│  ├── Collect failures with stack traces                        │
│  └── IF all pass → Skip to PHASE 5 (commit if changes exist)   │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 2: REVIEW                                                │
│  ├── Analyze each failure (root cause identification)          │
│  ├── Categorize: syntax | logic | type | integration           │
│  └── Estimate fix complexity (trivial | moderate | complex)    │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 3: FIX                                                   │
│  ├── Apply minimal fix (Minimal Fix Principle from LAW 7)      │
│  ├── One fix per failure (atomic commits)                      │
│  └── Skip complex fixes → log for manual review                │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 4: VERIFY                                                │
│  ├── Re-run affected tests                                     │
│  ├── Run full suite if integration test failed                 │
│  ├── IF still failing → LOOP (max 3 attempts)                  │
│  └── IF pass → Continue to PHASE 5                             │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 5: UPDATE                                                │
│  ├── Log fix details to outputs/bugfixes/YYYY-MM-DD_HHmm.md   │
│  ├── Update CHANGELOG only if user requests                    │
│  └── No pollution to main docs (gitignored logs)               │
├─────────────────────────────────────────────────────────────────┤
│  PHASE 6: COMMIT + PUSH                                         │
│  ├── Stage fixed files only                                    │
│  ├── Commit: fix(scope): brief description                     │
│  ├── Push to current branch (with --confirm-push: ask first)   │
│  └── IF push fails → Rollback commit, log error                │
└─────────────────────────────────────────────────────────────────┘
```

---

## AUTONOMY LEVELS

| Level | Flag | Behavior |
|-------|------|----------|
| 1 | `--dry-run` | Observe only, report what would be fixed |
| 2 | `--suggest` | Propose fixes, wait for approval |
| 3 | `--confirm-push` | Fix + commit, ask before push |
| 4 | (default) | Full auto: fix, commit, push |

---

## INPUT

**Automatic Detection**:
- Detects test framework from `package.json`, `pyproject.toml`, `pytest.ini`
- Detects current branch and remote
- Reads recent git diff for context

**Optional Arguments**:
```
/bugloop [options]

Options:
  --dry-run         Level 1: Report only, no changes
  --suggest         Level 2: Propose fixes, wait approval
  --confirm-push    Level 3: Ask before push
  --once            Single iteration (no retry loop)
  --max-retries N   Override max retries (default: 3)
  --timeout M       Override timeout in minutes (default: 10)
  --scope PATH      Limit to specific directory/file
```

---

## OUTPUT

### Console Output
```
[BUGLOOP] Starting feedback loop...
[TEST] Running pytest...
[TEST] 3 failures detected
[REVIEW] Analyzing failures...
  - test_auth.py::test_login: TypeError (trivial)
  - test_api.py::test_endpoint: AssertionError (moderate)
  - test_db.py::test_query: ConnectionError (complex → skip)
[FIX] Applying 2 fixes...
[VERIFY] Re-running tests...
[VERIFY] 2/3 now passing
[LOOP] Iteration 2/3...
[VERIFY] All tests passing!
[COMMIT] fix(auth,api): resolve login type error and endpoint assertion
[PUSH] Pushed to origin/feature-branch
[LOG] Details saved to outputs/bugfixes/2025-12-04_1423.md
[DONE] Feedback loop complete. 2 fixes applied, 1 skipped (complex).
```

### Bugfix Log (`outputs/bugfixes/YYYY-MM-DD_HHmm.md`)
```markdown
# Bugfix Log | 2025-12-04 14:23

## Summary
- **Branch**: feature-branch
- **Commit**: abc1234
- **Duration**: 3m 42s
- **Iterations**: 2

## Fixes Applied
### 1. test_auth.py::test_login
- **Root Cause**: Missing null check on user.profile
- **Fix**: Added `if user.profile:` guard
- **File**: src/auth/login.py:42
- **Lines Changed**: 2

### 2. test_api.py::test_endpoint
- **Root Cause**: Expected 200, got 201 (creation endpoint)
- **Fix**: Updated assertion to accept 201
- **File**: tests/test_api.py:78
- **Lines Changed**: 1

## Skipped (Manual Review Required)
### test_db.py::test_query
- **Reason**: ConnectionError - requires infrastructure fix
- **Suggestion**: Check database connection string in .env

## Commit Message
```
fix(auth,api): resolve login type error and endpoint assertion

- Added null check for user.profile in login flow
- Fixed assertion for creation endpoint (201 vs 200)

Fixes detected by /bugloop autonomous cycle

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## QUALITY GATES

| Gate | Threshold | Action if Fail |
|------|-----------|----------------|
| Test pass rate | 100% | Loop continues |
| Max iterations | 3 | Escalate to user |
| Max duration | 10 min | Abort + report |
| Complex fix detected | Any | Skip + log |
| Security-related | Any | Never auto-fix |
| Breaking change | Any | Escalate immediately |

---

## ESCALATION TRIGGERS

The loop **stops and asks for help** when:
1. Max retries (3) exhausted for same test
2. Fix requires semantic code change (not just syntax)
3. Multiple files need coordinated changes
4. Test involves external services (DB, API, auth)
5. Any security-sensitive code detected
6. Breaking change would be introduced

---

## SAFETY MECHANISMS

**Rollback Capability**:
```bash
# If push causes issues, rollback is automatic:
git revert HEAD --no-edit
git push
```

**Backup Before Fix**:
- Creates `.bak` files before modifying (cleaned after success)

**Atomic Commits**:
- One commit per logical fix
- Easy to cherry-pick or revert individual fixes

**Branch Protection**:
- Never force-pushes
- Respects branch protection rules
- Creates PR if direct push blocked

---

## INTEGRATION

### CI/CD Pipeline
```yaml
# .github/workflows/bugloop.yml
on:
  push:
    branches: [main, develop]

jobs:
  bugloop:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run bugloop
        run: claude "/bugloop --once --confirm-push"
```

### Pre-commit Hook
```bash
# .husky/pre-push
claude "/bugloop --dry-run" || exit 1
```

### Git Alias
```bash
git config --global alias.fix '!claude "/bugloop"'
# Usage: git fix
```

---

## TROUBLESHOOTING

| Issue | Solution |
|-------|----------|
| Loop never exits | Check for flaky tests (non-deterministic) |
| Push rejected | Ensure branch permissions, try `--confirm-push` |
| Wrong tests running | Use `--scope PATH` to limit scope |
| Too many skips | Lower complexity threshold or fix infra first |
| Timeout reached | Increase with `--timeout 15` or fix slow tests |

---

## RELATED

- **LAW 8**: FEEDBACK LOOPS (CLAUDE.md)
- **LAW 7**: ERROR RECOVERY (retry strategies)
- **ADW**: [202_ADW_BUG_FIXING.md](codexa.app/agentes/codexa_agent/workflows/202_ADW_BUG_FIXING.md)
- **Validator**: [13_code_quality_validator.py](codexa.app/agentes/codexa_agent/validators/13_code_quality_validator.py)

---

**Version**: 1.0.0
**Created**: 2025-12-04
**Type**: Autonomous Workflow Command
**Implements**: LAW 8 (Feedback Loops)
