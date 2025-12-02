# PATH REGISTRY MIGRATION GUIDE

**Version**: 1.0.0
**Created**: 2025-12-02
**For**: CODEXA Developers & AI Agents
**Related**: `PATH_REGISTRY_SYSTEM_SPEC.md`

---

## QUICK START

### For AI Agents (You)

When instructed to migrate an agent to the path registry system:

```bash
# 1. Read the specification
Read: codexa.app/agentes/scout_agent/specs/PATH_REGISTRY_SYSTEM_SPEC.md

# 2. Check current state
python -c "from codexa.core.path_resolver import PathResolver; PathResolver().validate_all_paths()"

# 3. Run migration for specific agent
python codexa.app/core/path_sync.py --agent scout_agent

# 4. Validate results
python codexa.app/agentes/codexa_agent/validators/14_path_validator.py
```

### For Human Developers

```bash
# Install dependencies
pip install pathlib

# Test path resolution
python codexa.app/core/path_resolver.py

# Run full migration
python codexa.app/core/path_sync.py --all

# Commit changes
git add path_registry.json
git commit -m "feat: Implement path registry system"
```

---

## MIGRATION CHECKLIST

### Per-Agent Migration

For each agent (e.g., `scout_agent`):

#### Step 1: Read Existing Paths

```bash
# Find existing path definitions
grep -r "Path(__file__)" codexa.app/agentes/scout_agent/
grep -r "\\\\Users\\\\" codexa.app/agentes/scout_agent/
grep -r "/home/" codexa.app/agentes/scout_agent/
```

#### Step 2: Update Python Modules

**Before** (`config/paths.py`):
```python
from pathlib import Path

SCOUT_AGENT_DIR = Path(__file__).parent.parent
AGENTS_ROOT = SCOUT_AGENT_DIR.parent
CODEXA_APP = AGENTS_ROOT.parent
PROJECT_ROOT = CODEXA_APP.parent
```

**After** (`config/paths.py`):
```python
from codexa.core.path_resolver import PathResolver

resolver = PathResolver()

# Resolve agent paths
SCOUT_AGENT_DIR = resolver.resolve_agent_path("scout_agent", "base")
AGENTS_ROOT = resolver.resolve("{{AGENTES}}")
CODEXA_APP = resolver.resolve("{{CODEXA_APP}}")
PROJECT_ROOT = resolver.resolve("{{PROJECT_ROOT}}")

# Agent-specific paths
PATH_CONFIG = resolver.resolve("{{AGENTES}}/scout_agent/config")
PATH_ISO = resolver.resolve("{{AGENTES}}/scout_agent/iso_vectorstore")
PATH_WORKFLOWS = resolver.resolve("{{AGENTES}}/scout_agent/workflows")
```

#### Step 3: Update Documentation

**Before** (`PRIME.md`):
```markdown
Location: codexa.app/agentes/scout_agent/PRIME.md
Config: codexa.app/agentes/scout_agent/config/categories.json
```

**After** (`PRIME.md`):
```markdown
Location: {{AGENTES}}/scout_agent/PRIME.md
Config: {{AGENTES}}/scout_agent/config/categories.json
```

#### Step 4: Update Registry Entry

**Before** (`51_AGENT_REGISTRY.json`):
```json
{
  "scout_agent": {
    "location": "codexa.app/agentes/scout_agent",
    "components": {
      "prime": "codexa.app/agentes/scout_agent/PRIME.md"
    }
  }
}
```

**After** (`51_AGENT_REGISTRY.json`):
```json
{
  "scout_agent": {
    "location": "{{AGENTES}}/scout_agent",
    "components": {
      "prime": "{{AGENTES}}/scout_agent/PRIME.md"
    }
  }
}
```

#### Step 5: Test Agent Workflows

```bash
# Test all agent workflows still work
python codexa.app/agentes/scout_agent/workflows/100_ADW_DISCOVERY_WORKFLOW.py

# Validate paths resolve correctly
python -c "
from codexa.core.path_resolver import PathResolver
resolver = PathResolver()
print(resolver.get_agent_context('scout_agent'))
"
```

#### Step 6: Update Builder Scripts

If agent has builders (like `codexa_agent`):

**Before**:
```python
output_dir = Path("codexa.app/agentes/codexa_agent/outputs")
```

**After**:
```python
from codexa.core.path_resolver import resolve_path
output_dir = resolve_path("{{AGENTES}}/codexa_agent/outputs")
```

---

## COMMON MIGRATION PATTERNS

### Pattern 1: Relative Path Traversal

**Before**:
```python
# Traverse up to find root
current = Path(__file__).parent
project_root = current.parent.parent.parent
```

**After**:
```python
from codexa.core.path_resolver import resolve_path
project_root = resolve_path("{{PROJECT_ROOT}}")
```

### Pattern 2: Hardcoded Config Paths

**Before**:
```python
config_path = "C:\\Users\\Dell\\...\\codexa.app\\agentes\\scout_agent\\config"
```

**After**:
```python
config_path = resolve_path("{{AGENTES}}/scout_agent/config")
```

### Pattern 3: Cross-Agent References

**Before**:
```python
mentor_fontes = Path("../mentor_agent/FONTES")
```

**After**:
```python
mentor_fontes = resolve_path("{{AGENTES}}/mentor_agent/FONTES")
```

### Pattern 4: MCP Server Paths

**Before** (`.mcp.json`):
```json
{
  "command": "node",
  "args": ["C:\\Users\\Dell\\...\\scout-mcp\\index.js"]
}
```

**After** (`.mcp.json`):
```json
{
  "command": "node",
  "args": ["${env:CODEXA_APP}/mcp-servers/scout-mcp/index.js"],
  "env": {
    "CODEXA_APP": "${workspaceFolder}"
  }
}
```

---

## AUTOMATED MIGRATION

### Using `path_sync.py`

```bash
# Migrate single agent
python codexa.app/core/path_sync.py --agent scout_agent

# Migrate all agents
python codexa.app/core/path_sync.py --all

# Dry run (preview changes)
python codexa.app/core/path_sync.py --all --dry-run

# Verbose output
python codexa.app/core/path_sync.py --all --verbose
```

### Migration Script Output

```
=== Path Registry Sync ===
Scanning agents directory...
Found 9 agents to process

[1/9] scout_agent
  - Updated config/paths.py (added resolver import)
  - Updated PRIME.md (3 paths converted to placeholders)
  - Updated README.md (5 paths converted to placeholders)
  [OK] scout_agent migrated

[2/9] codexa_agent
  - Updated builders/02_agent_meta_constructor.py
  - Updated validators/07_hop_sync_validator.py
  [OK] codexa_agent migrated

...

[9/9] curso_agent
  [OK] curso_agent migrated

=== Summary ===
Agents migrated: 9/9
Files updated: 47
Validation: PASSED
```

---

## VALIDATION

### Pre-Migration Validation

```bash
# Check current hardcoded paths
python codexa.app/agentes/codexa_agent/validators/14_path_validator.py --scan

# Expected output:
# Found 23 files with hardcoded paths
#   - codexa.app/agentes/scout_agent/config/paths.py
#   - codexa.app/agentes/curso_agent/config/paths.py
#   ...
```

### Post-Migration Validation

```bash
# Validate all paths resolve correctly
python codexa.app/agentes/codexa_agent/validators/14_path_validator.py --validate

# Expected output:
# [OK] PROJECT_ROOT resolved and exists
# [OK] CODEXA_APP resolved and exists
# [OK] AGENTES resolved and exists
# [OK] All agent paths validated
#
# Result: 0 errors, 0 warnings
```

### Continuous Validation (Git Hook)

```bash
# Install pre-commit hook
cp .git/hooks/pre-commit.sample .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Add validation to hook
cat >> .git/hooks/pre-commit << 'EOF'
# Path validation
python codexa.app/agentes/codexa_agent/validators/14_path_validator.py
if [ $? -ne 0 ]; then
  echo "[FAIL] Path validation failed"
  exit 1
fi
EOF
```

---

## TROUBLESHOOTING

### Issue: "Module not found: codexa.core.path_resolver"

**Cause**: Path resolver not yet implemented.

**Solution**:
```bash
# Create core directory if not exists
mkdir -p codexa.app/core

# Copy path_resolver.py from spec (Section 3.1)
# Or wait for Phase 1 implementation
```

### Issue: "Could not detect PROJECT_ROOT"

**Cause**: Running from outside git repository.

**Solution**:
```bash
# Option 1: Run from within repository
cd /path/to/codexa.gato

# Option 2: Set environment variable
export PROJECT_ROOT=/path/to/codexa.gato
```

### Issue: "Path does not exist: {{AGENTES}}/new_agent"

**Cause**: Agent not yet created, but referenced in registry.

**Solution**:
```bash
# Remove from registry or create the agent
python codexa.app/agentes/codexa_agent/builders/02_agent_meta_constructor.py "new_agent"
```

### Issue: "Validation failed: missing .git"

**Cause**: Not in correct directory.

**Solution**:
```bash
# Verify you're in project root
git rev-parse --show-toplevel

# Should show: /path/to/codexa.gato
```

---

## ROLLBACK PROCEDURE

If migration causes issues:

### Step 1: Restore from Git

```bash
# Discard changes
git checkout -- path_registry.json
git checkout -- codexa.app/agentes/*/config/paths.py
git checkout -- codexa.app/agentes/51_AGENT_REGISTRY.json

# Or restore specific agent
git checkout -- codexa.app/agentes/scout_agent/
```

### Step 2: Verify Rollback

```bash
# Test agent still works
python codexa.app/agentes/scout_agent/test_agent.py

# Should pass with old paths
```

### Step 3: Report Issue

Create GitHub issue with:
- Agent name
- Error message
- Steps to reproduce
- Environment (Windows/Linux/macOS)

---

## PHASE-BY-PHASE MIGRATION

### Phase 1: Foundation (Week 1)

**Goal**: Create infrastructure, no agent changes yet.

**Tasks**:
- [x] Create `path_registry.json`
- [ ] Implement `codexa.app/core/path_resolver.py`
- [ ] Implement `codexa.app/core/pathResolver.js`
- [ ] Implement `validators/14_path_validator.py`
- [ ] Test cross-platform (Windows/Linux/macOS)

**Validation**: All validators pass, no production impact.

### Phase 2: Pilot Migration (Week 2)

**Goal**: Migrate 1 agent (scout_agent) as proof of concept.

**Tasks**:
- [ ] Migrate `scout_agent/config/paths.py`
- [ ] Update `scout_agent/PRIME.md`
- [ ] Update `scout_agent/README.md`
- [ ] Test all scout workflows
- [ ] Document lessons learned

**Validation**: Scout agent fully functional with new paths.

### Phase 3: Bulk Migration (Week 3)

**Goal**: Migrate remaining 8 agents.

**Tasks**:
- [ ] Migrate `codexa_agent` (critical)
- [ ] Migrate `mentor_agent`
- [ ] Migrate `anuncio_agent`
- [ ] Migrate `pesquisa_agent`
- [ ] Migrate `marca_agent`
- [ ] Migrate `photo_agent`
- [ ] Migrate `video_agent`
- [ ] Migrate `curso_agent`

**Validation**: All agents pass validation, all workflows work.

### Phase 4: Cleanup (Week 4)

**Goal**: Remove old path code, enforce new system.

**Tasks**:
- [ ] Remove legacy path traversal code
- [ ] Enable git pre-commit hook
- [ ] Update documentation (CLAUDE.md, PRIME.md)
- [ ] Create training materials
- [ ] Announce completion

**Validation**: No hardcoded paths remain, validation enforced.

---

## COMPATIBILITY MATRIX

| Platform | Python 3.10+ | Node.js 18+ | Git | Status |
|----------|--------------|-------------|-----|--------|
| Windows 11 | ✅ Required | ✅ Required | ✅ Required | Tested |
| Windows 10 | ✅ Required | ✅ Required | ✅ Required | Not tested |
| Linux (Ubuntu 22.04) | ✅ Required | ✅ Required | ✅ Required | Not tested |
| macOS 13+ | ✅ Required | ✅ Required | ✅ Required | Not tested |

**Note**: Cross-platform testing required before Phase 3.

---

## BEST PRACTICES

### DO

- ✅ Use `{{PLACEHOLDERS}}` in all documentation
- ✅ Use `PathResolver` in all Python scripts
- ✅ Test on Windows AND Linux before committing
- ✅ Run validation before pushing
- ✅ Keep `path_registry.json` in sync with filesystem

### DON'T

- ❌ Hardcode absolute paths (`C:\Users\...`, `/home/...`)
- ❌ Use relative path traversal (`../../..`)
- ❌ Bypass validation checks
- ❌ Modify `path_registry.json` manually (use sync script)
- ❌ Commit without running validators

---

## AGENT-SPECIFIC NOTES

### scout_agent

- MCP server path must be updated in `.mcp.json`
- Config files already well-structured (easy migration)
- No builders/validators to update

### codexa_agent

- CRITICAL: Update all builders first (they create other agents)
- Validators must use resolver before validating others
- Workflows reference many other agents (update carefully)

### mentor_agent

- Large `FONTES` directory with many references
- Embedding pipeline hardcodes paths (update carefully)
- Knowledge graph paths must be resolved at runtime

### curso_agent

- Already has `config/paths.py` (good starting point)
- Many context files with cross-references
- Hotmart integration paths must work

### Other Agents

- Follow standard pattern: config/paths.py → resolver
- Update PRIME.md and README.md
- Test workflows after migration

---

## COMPLETION CRITERIA

Migration is complete when:

- [ ] All 9 agents migrated
- [ ] `path_validator.py` reports 0 errors, 0 warnings
- [ ] All ADW workflows pass
- [ ] All builders/validators work
- [ ] Cross-platform tested (Windows + Linux)
- [ ] Documentation updated
- [ ] Git hook enabled
- [ ] CLAUDE.md updated with path system rules

---

## RESOURCES

- **Specification**: `specs/PATH_REGISTRY_SYSTEM_SPEC.md`
- **Registry**: `path_registry.json` (project root)
- **Resolver (Python)**: `codexa.app/core/path_resolver.py`
- **Resolver (Node)**: `codexa.app/core/pathResolver.js`
- **Validator**: `codexa_agent/validators/14_path_validator.py`
- **Sync Script**: `codexa.app/core/path_sync.py`

---

## QUESTIONS?

For migration issues or questions:

1. Check troubleshooting section above
2. Read full specification: `PATH_REGISTRY_SYSTEM_SPEC.md`
3. Run validator for detailed errors: `14_path_validator.py --verbose`
4. Create GitHub issue if unresolved

---

**Version**: 1.0.0
**Status**: Ready for Implementation
**Next Step**: Begin Phase 1 (Foundation)

**End of Migration Guide**
