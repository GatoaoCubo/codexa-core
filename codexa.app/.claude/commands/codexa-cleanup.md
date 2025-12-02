# /codexa-cleanup | Clean Temporary Files

**Role**: Cleanup Manager | **Philosophy**: Keep only code + reusable artifacts
**Output**: Clean workspace (minimal temp files)

---

## WHAT TO CLEAN

### ALWAYS REMOVE
- **Temp Agent Outputs**: `agents/[8-char-hex]/` (ADW test artifacts)
- **Loose Summaries**: `*.summary.json`, `*_summary.json` (test outputs)
- **Raw Outputs**: `cc_raw_output.*` (Claude Code logs)
- **Temp Logs**: `*.log` (execution logs)
- **Cache Files**: `__pycache__/`, `*.pyc`, `.pytest_cache/`

### ALWAYS KEEP
- **Source Code**: `builders/`, `validators/`, `agents/*/src/`
- **Core Docs**: README, PRIME, INSTRUCTIONS, workflows, commands
- **Examples**: `_examples/`, documented reference implementations
- **Tests**: `tests/`, validation suites

---

## QUICK CLEANUP

```bash
# Remove temp agent outputs
rm -rf agents/[a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9]/

# Remove summaries
find . -name "*.summary.json" -delete
find . -name "*_summary.json" -delete

# Remove logs
find . -name "*.log" -delete
find . -name "cc_raw_output.*" -delete

# Remove Python cache
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -name "*.pyc" -delete
```

---

## VALIDATION

- No source code deleted
- Core docs intact
- Examples preserved
- Tests functional
- Temp files removed

**Check**: Run tests after cleanup | Verify all builders/validators work

---

**Related**: File management | Workspace hygiene
