# PATH REGISTRY SYSTEM - EXECUTIVE SUMMARY

**Version**: 1.0.0 | **Status**: Design Complete, Ready for Implementation | **Created**: 2025-12-02

---

## THE PROBLEM

```
CURRENT STATE (Broken):
┌─────────────────────────────────────────────────────────────┐
│  Agent 1: C:\Users\Dell\...\scout_agent\config\paths.py    │
│  Agent 2: /home/user/.../mentor_agent/scripts/search.py    │
│  Agent 3: ../../../codexa.app/agentes/codexa_agent/...     │
└─────────────────────────────────────────────────────────────┘
                           ❌ PROBLEMS:
    • Breaks when project moves to different machine
    • Fails on Windows ↔ Linux
    • Requires manual updates across 100+ files
    • No single source of truth
```

## THE SOLUTION

```
NEW STATE (Scalable):
┌─────────────────────────────────────────────────────────────┐
│               path_registry.json                            │
│         (Single Source of Truth)                            │
│                                                             │
│  {{PROJECT_ROOT}}  → auto-detect git root                  │
│  {{CODEXA_APP}}    → PROJECT_ROOT/codexa.app               │
│  {{AGENTES}}       → CODEXA_APP/agentes                    │
│  {{AGENT_DIR}}     → context-dependent (dynamic)           │
│                                                             │
│         PathResolver (Python/Node)                          │
│         resolves at runtime                                 │
└─────────────────────────────────────────────────────────────┘
                           ✅ BENEFITS:
    • Works on ANY machine (auto-detects root)
    • Cross-platform (Windows/Linux/macOS)
    • Update once, applies everywhere
    • Human-readable documentation
```

---

## QUICK START

### For AI Agents (Read This First)

```bash
# 1. Load specification
Read: codexa.app/agentes/scout_agent/specs/PATH_REGISTRY_SYSTEM_SPEC.md

# 2. Use in code (Python)
from codexa.core.path_resolver import resolve_path
path = resolve_path("{{AGENTES}}/scout_agent/PRIME.md")

# 3. Use in documentation (Markdown)
Location: {{AGENTES}}/scout_agent/PRIME.md
Config: {{AGENTES}}/scout_agent/config/categories.json
```

### For Human Developers

```bash
# Install (Phase 1 - not yet implemented)
git pull origin main
python codexa.app/core/path_resolver.py  # Test

# Migrate an agent (Phase 2+)
python codexa.app/core/path_sync.py --agent scout_agent

# Validate
python codexa.app/agentes/codexa_agent/validators/14_path_validator.py
```

---

## ARCHITECTURE (3 LAYERS)

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: STORAGE (path_registry.json)                     │
│  ├─ root_anchors: PROJECT_ROOT, CODEXA_APP, AGENTES        │
│  ├─ agent_paths: scout_agent, codexa_agent, etc.           │
│  └─ common_paths: registry, claude_md, etc.                │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: RESOLUTION (PathResolver)                         │
│  ├─ Python: codexa.app/core/path_resolver.py               │
│  ├─ Node.js: codexa.app/core/pathResolver.js               │
│  └─ Auto-detects git root, resolves placeholders           │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: CONSUMPTION                                       │
│  ├─ Python modules: import path_resolver                   │
│  ├─ Node modules: require('./pathResolver')                │
│  ├─ Documentation: {{PLACEHOLDERS}} (human-readable)       │
│  ├─ MCP configs: ${env:VARIABLE} (environment vars)        │
│  └─ Agent registry: {{AGENTES}}/agent_name                 │
└─────────────────────────────────────────────────────────────┘
```

---

## STANDARD PLACEHOLDERS

| Placeholder | Resolves To | Example Usage |
|-------------|-------------|---------------|
| `{{PROJECT_ROOT}}` | Git root (auto-detect) | `{{PROJECT_ROOT}}/path_registry.json` |
| `{{CODEXA_APP}}` | `PROJECT_ROOT/codexa.app` | `{{CODEXA_APP}}/agentes` |
| `{{AGENTES}}` | `CODEXA_APP/agentes` | `{{AGENTES}}/scout_agent` |
| `{{MCP_SERVERS}}` | `CODEXA_APP/mcp-servers` | `{{MCP_SERVERS}}/scout-mcp` |
| `{{CLAUDE_DIR}}` | `PROJECT_ROOT/.claude` | `{{CLAUDE_DIR}}/commands` |
| `{{AGENT_DIR}}` | Context-dependent | `{{AGENT_DIR}}/config` |
| `{{AGENT_CONFIG}}` | `AGENT_DIR/config` | `{{AGENT_CONFIG}}/paths.py` |
| `{{AGENT_ISO}}` | `AGENT_DIR/iso_vectorstore` | `{{AGENT_ISO}}/04_README.md` |

---

## CODE EXAMPLES

### Python (Before vs After)

```python
# ❌ BEFORE (Hardcoded, breaks on other machines)
from pathlib import Path
SCOUT_AGENT_DIR = Path(__file__).parent.parent
AGENTS_ROOT = SCOUT_AGENT_DIR.parent
CODEXA_APP = AGENTS_ROOT.parent
PROJECT_ROOT = CODEXA_APP.parent

# ✅ AFTER (Dynamic, works everywhere)
from codexa.core.path_resolver import PathResolver
resolver = PathResolver()
SCOUT_AGENT_DIR = resolver.resolve("{{AGENTES}}/scout_agent")
AGENTS_ROOT = resolver.resolve("{{AGENTES}}")
CODEXA_APP = resolver.resolve("{{CODEXA_APP}}")
PROJECT_ROOT = resolver.resolve("{{PROJECT_ROOT}}")
```

### Documentation (Before vs After)

```markdown
<!-- ❌ BEFORE (Machine-specific, breaks on Windows/Linux) -->
Location: codexa.app/agentes/scout_agent/PRIME.md
Config: C:\Users\Dell\...\scout_agent\config\categories.json

<!-- ✅ AFTER (Universal, human-readable) -->
Location: {{AGENTES}}/scout_agent/PRIME.md
Config: {{AGENTES}}/scout_agent/config/categories.json
```

### Agent Registry (Before vs After)

```json
// ❌ BEFORE
{
  "scout_agent": {
    "location": "codexa.app/agentes/scout_agent",
    "prime": "codexa.app/agentes/scout_agent/PRIME.md"
  }
}

// ✅ AFTER
{
  "scout_agent": {
    "location": "{{AGENTES}}/scout_agent",
    "prime": "{{AGENTES}}/scout_agent/PRIME.md"
  }
}
```

---

## MIGRATION PHASES (4 Weeks)

```
PHASE 1: FOUNDATION (Week 1)
├─ Create path_registry.json
├─ Implement path_resolver.py (Python)
├─ Implement pathResolver.js (Node.js)
├─ Implement path_validator.py
└─ Test cross-platform

PHASE 2: PILOT (Week 2)
├─ Migrate scout_agent (proof of concept)
├─ Update 51_AGENT_REGISTRY.json
├─ Create .mcp.json
└─ Document lessons learned

PHASE 3: BULK (Week 3)
├─ Migrate codexa_agent (critical - builds others)
├─ Migrate mentor_agent
├─ Migrate remaining 6 agents
└─ Run validation on all agents

PHASE 4: CLEANUP (Week 4)
├─ Remove legacy path code
├─ Enable git pre-commit hook
├─ Update CLAUDE.md
└─ Training & documentation
```

---

## KEY FILES CREATED

| File | Location | Purpose |
|------|----------|---------|
| **Specification** | `specs/PATH_REGISTRY_SYSTEM_SPEC.md` | Complete system design (12,000+ words) |
| **Registry** | `path_registry.json` | Single source of truth (project root) |
| **Migration Guide** | `specs/PATH_MIGRATION_GUIDE.md` | Step-by-step migration instructions |
| **Summary** | `specs/PATH_REGISTRY_SUMMARY.md` | This file (quick reference) |

**To Implement** (Phase 1):
- `codexa.app/core/path_resolver.py` (Python resolver)
- `codexa.app/core/pathResolver.js` (Node.js resolver)
- `codexa_agent/validators/14_path_validator.py` (Validator)
- `codexa.app/core/path_sync.py` (Sync script)

---

## VALIDATION RULES

### Code Validation

```bash
# ✅ GOOD
from codexa.core.path_resolver import resolve_path
path = resolve_path("{{AGENTES}}/scout_agent")

# ❌ BAD
path = "C:\\Users\\Dell\\...\\scout_agent"  # Hardcoded Windows path
path = "/home/user/.../scout_agent"        # Hardcoded Linux path
path = Path(__file__).parent.parent.parent  # Relative traversal
```

### Documentation Validation

```markdown
<!-- ✅ GOOD -->
Location: {{AGENTES}}/scout_agent/PRIME.md

<!-- ❌ BAD -->
Location: codexa.app/agentes/scout_agent/PRIME.md  (not a placeholder)
Location: C:\Users\Dell\...\PRIME.md              (hardcoded absolute)
```

### Pre-Commit Hook

```bash
# Automatically runs on git commit
python validators/14_path_validator.py

# Blocks commit if:
# - Hardcoded paths detected
# - Placeholders undefined
# - Resolved paths don't exist
```

---

## BENEFITS

### For Developers

✅ **Portability**: Project works on ANY machine (Windows/Linux/macOS)
✅ **Maintainability**: Update paths in ONE place (path_registry.json)
✅ **Clarity**: `{{AGENTES}}` is clearer than `../../agentes`
✅ **Safety**: Validation prevents hardcoded paths

### For AI Agents

✅ **Consistency**: Always use same placeholder syntax
✅ **Discovery**: Query registry for all agent paths
✅ **Validation**: Auto-check paths exist before using
✅ **Documentation**: Human-readable placeholders in docs

### For System

✅ **Scalability**: Add new agents without breaking existing paths
✅ **Testability**: Test on CI/CD across multiple platforms
✅ **Automation**: Sync script updates all files automatically
✅ **Quality**: Git hook enforces path standards

---

## COMPATIBILITY

| Feature | Windows | Linux | macOS | Status |
|---------|---------|-------|-------|--------|
| Path resolution | ✅ | ✅ | ✅ | Designed |
| Auto-detect root | ✅ | ✅ | ✅ | Designed |
| Python resolver | ✅ | ✅ | ✅ | To implement |
| Node resolver | ✅ | ✅ | ✅ | To implement |
| MCP integration | ✅ | ✅ | ✅ | To implement |
| Git hook | ✅ | ✅ | ✅ | To implement |

**Requirements**:
- Python 3.10+
- Node.js 18+ (for MCP servers)
- Git (for root detection)

---

## INTEGRATION WITH CODEXA LAWS

### LAW 1: DISTILLATION PRINCIPLE

✅ **Aligned**: Path registry extends Mustache `{{PLACEHOLDERS}}` from CLAUDE.md

**Standard Placeholders Extended**:
- Brand-level: `{{BRAND_NAME}}`, `{{BRAND_URL}}` (from CLAUDE.md)
- System-level: `{{PROJECT_ROOT}}`, `{{AGENTES}}` (new)
- Agent-level: `{{AGENT_DIR}}`, `{{AGENT_CONFIG}}` (new)

### LAW 2: FRACTAL NAVIGATION

✅ **Aligned**: Path registry follows fractal pattern at all levels

```
PROJECT_ROOT/path_registry.json
  → CODEXA_APP/path_registry.json (optional)
    → AGENT_DIR/config/paths.json (optional)
```

### LAW 3: META-CONSTRUCTION

✅ **Aligned**: Path registry IS a builder (generates paths, not instances)

**Meta Pattern**:
- Registry = Template (structure)
- Resolver = Builder (generates)
- Validator = Quality Gate (validates)

### LAW 4: AGENTIC DESIGN

✅ **Aligned**: Each agent can define agent-specific paths

**Domain**: Path discovery, resolution, validation
**Workflows**: Sync, validate, migrate (ADWs)
**Prompts**: Path resolution in HOPs
**Outputs**: Resolved paths, validation reports

---

## NEXT ACTIONS

### For CODEXA Meta Agent (You)

1. **Review** this summary + full specification
2. **Approve** design or request changes
3. **Implement** Phase 1 (foundation files)
4. **Test** cross-platform compatibility
5. **Migrate** scout_agent (pilot)

### For Human Developer

1. **Read** full specification: `PATH_REGISTRY_SYSTEM_SPEC.md`
2. **Review** migration guide: `PATH_MIGRATION_GUIDE.md`
3. **Approve** implementation phases
4. **Test** on Windows + Linux
5. **Deploy** incrementally (agent by agent)

---

## QUESTIONS & ANSWERS

**Q: Why not just use relative paths?**
A: Relative paths break when script is called from different directories. Placeholders + resolver works from ANY location.

**Q: Why both Python and Node.js resolvers?**
A: Python for agents/builders, Node.js for MCP servers. Both platforms need resolution.

**Q: Can I still use environment variables?**
A: Yes! Registry supports `env:VARIABLE` fallback strategy.

**Q: What if I need a custom path?**
A: Add to `agent_paths` section in registry, then resolve with `PathResolver`.

**Q: Do all files need to be migrated at once?**
A: No. Phase 2 migrates 1 agent (pilot), Phase 3 does the rest. Incremental is safe.

**Q: What happens to old paths.py files?**
A: They're updated to USE the resolver (not deleted). Backwards compatible.

---

## RESOURCES

📄 **Full Specification**: `specs/PATH_REGISTRY_SYSTEM_SPEC.md` (12,000+ words)
📄 **Migration Guide**: `specs/PATH_MIGRATION_GUIDE.md` (detailed instructions)
📄 **Registry Template**: `path_registry.json` (project root)
📄 **This Summary**: `specs/PATH_REGISTRY_SUMMARY.md`

🔗 **Related**:
- CLAUDE.md (LAW 1: Distillation Principle)
- 51_AGENT_REGISTRY.json (Agent registry)
- curso_agent/config/paths.py (Existing path system)

---

## STATUS

- [x] Design complete
- [x] Specification written (12,000+ words)
- [x] Migration guide created
- [x] Registry template created
- [ ] Phase 1: Foundation (path_resolver.py, pathResolver.js, validator)
- [ ] Phase 2: Pilot (scout_agent migration)
- [ ] Phase 3: Bulk (8 remaining agents)
- [ ] Phase 4: Cleanup (remove legacy, enable hooks)

**Current Phase**: Design Complete → Ready for Phase 1 Implementation

---

**Version**: 1.0.0
**Created**: 2025-12-02
**Type**: Executive Summary
**Status**: Ready for Review & Implementation

**End of Summary**
