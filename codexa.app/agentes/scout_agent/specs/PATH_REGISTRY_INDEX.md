# PATH REGISTRY SYSTEM - DOCUMENTATION INDEX

**Version**: 1.0.0 | **Created**: 2025-12-02 | **Status**: Complete Design Package

---

## OVERVIEW

Complete documentation package for the CODEXA Path Registry System - a centralized, cross-platform path management solution that eliminates hardcoded paths and enables true portability.

**Problem Solved**: Project breaks when moved between machines or platforms (Windows ↔ Linux).
**Solution**: Single source of truth (`path_registry.json`) + dynamic runtime resolution + placeholder syntax.

---

## DOCUMENTATION STRUCTURE

```
PATH REGISTRY SYSTEM DOCUMENTATION
├─ 📄 PATH_REGISTRY_SUMMARY.md        ← START HERE (Quick reference)
├─ 📘 PATH_REGISTRY_SYSTEM_SPEC.md   ← Complete specification (12,000+ words)
├─ 📗 PATH_MIGRATION_GUIDE.md         ← Step-by-step migration instructions
└─ 📋 PATH_REGISTRY_INDEX.md          ← This file (navigation)

IMPLEMENTATION FILES (To be created in Phase 1)
├─ 📄 path_registry.json              ← Registry template (project root)
├─ 🐍 codexa.app/core/path_resolver.py
├─ 🟨 codexa.app/core/pathResolver.js
├─ ✅ codexa_agent/validators/14_path_validator.py
└─ 🔄 codexa.app/core/path_sync.py
```

---

## READING ORDER

### For AI Agents (First Session)

1. **PATH_REGISTRY_SUMMARY.md** (5 min read)
   - Executive summary
   - Quick start examples
   - Key concepts

2. **PATH_REGISTRY_SYSTEM_SPEC.md** (20 min read)
   - Section 1: Architecture Overview
   - Section 2: Path Registry Schema
   - Section 3: Resolution Strategy
   - Section 7: Usage Examples

3. **PATH_MIGRATION_GUIDE.md** (10 min read)
   - Migration checklist
   - Common patterns
   - Troubleshooting

### For Human Developers

1. **PATH_REGISTRY_SUMMARY.md**
   - Understand the problem and solution
   - Review benefits and compatibility

2. **PATH_REGISTRY_SYSTEM_SPEC.md**
   - Full technical specification
   - Integration with existing systems
   - Validation rules

3. **PATH_MIGRATION_GUIDE.md**
   - Phase-by-phase migration plan
   - Agent-specific notes
   - Rollback procedures

4. **path_registry.json**
   - Review registry structure
   - Understand placeholder definitions

---

## QUICK NAVIGATION

### By Use Case

**"I need to understand the system"**
→ Start with `PATH_REGISTRY_SUMMARY.md`

**"I need to implement Phase 1"**
→ Read `PATH_REGISTRY_SYSTEM_SPEC.md` Section 3 (Resolution Strategy)
→ Implement `path_resolver.py` and `pathResolver.js`

**"I need to migrate an agent"**
→ Follow `PATH_MIGRATION_GUIDE.md` Section "Per-Agent Migration"

**"I need to troubleshoot an issue"**
→ Check `PATH_MIGRATION_GUIDE.md` Section "Troubleshooting"

**"I need to validate paths"**
→ Run `validators/14_path_validator.py` (to be implemented)

### By Section

**Architecture & Design**
- Summary: Section "Architecture (3 Layers)"
- Spec: Section 1 "Architecture Overview"
- Spec: Section 2 "Path Registry Schema"

**Implementation**
- Spec: Section 3 "Resolution Strategy"
- Spec: Section 3.1 "Python Resolution Module" (complete code)
- Spec: Section 3.2 "Node.js Resolution Module" (complete code)

**Integration**
- Spec: Section 4 "Integration with Existing Systems"
- Spec: Section 4.1 "Integration with curso_agent/config/paths.py"
- Spec: Section 4.4 "Integration with 51_AGENT_REGISTRY.json"

**Migration**
- Migration Guide: Section "Migration Checklist"
- Migration Guide: Section "Phase-by-Phase Migration"
- Migration Guide: Section "Agent-Specific Notes"

**Validation**
- Spec: Section 5 "Sync Mechanisms"
- Spec: Section 5.1 "Validation Script" (complete code)
- Spec: Section 8 "Validation Rules"

**Examples**
- Summary: Section "Code Examples"
- Spec: Section 7 "Usage Examples"
- Migration Guide: Section "Common Migration Patterns"

---

## FILE DESCRIPTIONS

### 📄 PATH_REGISTRY_SUMMARY.md

**Purpose**: Executive summary and quick reference
**Length**: ~3,000 words
**Read Time**: 5-10 minutes

**Contents**:
- Problem statement (current vs new state)
- Quick start guide
- Architecture diagram (3 layers)
- Standard placeholders table
- Code examples (before/after)
- Migration phases overview
- Key benefits
- Q&A section

**When to Read**: First introduction to the system, quick reference during implementation

### 📘 PATH_REGISTRY_SYSTEM_SPEC.md

**Purpose**: Complete technical specification
**Length**: ~12,000 words
**Read Time**: 30-45 minutes

**Contents**:
1. Architecture Overview (diagrams, three-layer strategy)
2. Path Registry Schema (complete JSON schema with examples)
3. Resolution Strategy (Python + Node.js complete implementations)
4. Integration with Existing Systems (curso_agent, MCP, registry)
5. Sync Mechanisms (validator, sync script, git hook)
6. Migration Plan (4 phases, 4 weeks)
7. Usage Examples (Python, Node, documentation, registry)
8. Validation Rules (registry, code, git pre-commit)
9. Troubleshooting (common issues and solutions)
10. Future Enhancements (v1.1-v2.0 roadmap)
11. Compliance with CODEXA Laws (LAW 1-4 alignment)
12. Appendix (complete registry example, checklists, reference card)

**When to Read**: Before implementation, during development, for troubleshooting

### 📗 PATH_MIGRATION_GUIDE.md

**Purpose**: Step-by-step migration instructions
**Length**: ~5,000 words
**Read Time**: 15-20 minutes

**Contents**:
- Quick start (AI agents vs human developers)
- Migration checklist (per-agent steps)
- Common migration patterns (6 patterns with before/after)
- Automated migration (using path_sync.py)
- Validation (pre-migration, post-migration, continuous)
- Troubleshooting (5 common issues)
- Rollback procedure (3-step recovery)
- Phase-by-phase migration (detailed tasks)
- Compatibility matrix (platforms tested)
- Best practices (DO/DON'T lists)
- Agent-specific notes (9 agents)
- Completion criteria (checklist)

**When to Read**: During migration, for troubleshooting, before committing changes

### 📋 PATH_REGISTRY_INDEX.md

**Purpose**: Navigation and documentation overview
**Length**: ~2,000 words (this file)
**Read Time**: 5 minutes

**Contents**:
- Documentation structure
- Reading order (by role)
- Quick navigation (by use case, by section)
- File descriptions (all 4 docs)
- Implementation roadmap
- Resources and references

**When to Read**: First contact with documentation, when lost, for finding specific sections

---

## IMPLEMENTATION ROADMAP

### Phase 1: Foundation (Week 1)

**Goal**: Create infrastructure without breaking existing code

**Files to Create**:
1. `codexa.app/core/path_resolver.py`
   - 400+ lines of Python code
   - Complete implementation in Spec Section 3.1
   - Includes: PathResolver class, resolve_path function, validation

2. `codexa.app/core/pathResolver.js`
   - 300+ lines of Node.js code
   - Complete implementation in Spec Section 3.2
   - Includes: PathResolver class, resolvePath function, validation

3. `codexa_agent/validators/14_path_validator.py`
   - 150+ lines of Python code
   - Complete implementation in Spec Section 5.1
   - Includes: PathValidator class, registry validation, hardcoded path detection

4. `codexa.app/core/path_sync.py`
   - 200+ lines of Python code
   - Complete implementation in Spec Section 5.2
   - Includes: PathSyncer class, config sync, registry sync

5. `.git/hooks/pre-commit`
   - 20 lines of Bash
   - Complete implementation in Spec Section 5.3
   - Validates paths before commit

**Deliverables**:
- All 5 files implemented
- Cross-platform testing (Windows + Linux)
- Validation passing
- Documentation complete

### Phase 2: Pilot Migration (Week 2)

**Goal**: Migrate scout_agent as proof of concept

**Files to Update**:
1. `scout_agent/config/paths.py` → use PathResolver
2. `scout_agent/PRIME.md` → use placeholders
3. `scout_agent/README.md` → use placeholders
4. `51_AGENT_REGISTRY.json` → add scout_agent with placeholders
5. `.mcp.json` → create with scout-mcp paths

**Deliverables**:
- Scout agent fully migrated
- All workflows passing
- Lessons learned document
- Validated on Windows + Linux

### Phase 3: Bulk Migration (Week 3)

**Goal**: Migrate remaining 8 agents

**Priority Order**:
1. `codexa_agent` (CRITICAL - builds other agents)
2. `mentor_agent` (knowledge processing)
3. `anuncio_agent` (e-commerce)
4. `pesquisa_agent` (research)
5. `marca_agent` (branding)
6. `photo_agent` (photography)
7. `video_agent` (video)
8. `curso_agent` (courses)

**Deliverables**:
- All 8 agents migrated
- All builders/validators updated
- All workflows passing
- Full system validation

### Phase 4: Cleanup (Week 4)

**Goal**: Remove legacy code, enforce new system

**Tasks**:
1. Remove legacy path traversal code
2. Enable git pre-commit hook (enforce)
3. Update CLAUDE.md (add LAW 5: Path Management)
4. Create training materials
5. Announce completion

**Deliverables**:
- Zero hardcoded paths
- Validation enforced
- Documentation complete
- System production-ready

---

## KEY CONCEPTS

### Placeholder Syntax

```
{{UPPER_CASE_PLACEHOLDER}}

Examples:
{{PROJECT_ROOT}}  - Git root (auto-detected)
{{AGENTES}}       - All agents directory
{{AGENT_DIR}}     - Current agent (context-dependent)
```

### Resolution Strategy

```
Placeholder → Registry Lookup → Root Anchor → Auto-Detect → Absolute Path

Example:
"{{AGENTES}}/scout_agent"
→ Lookup "AGENTES" in registry
→ Resolves to "{{CODEXA_APP}}/agentes"
→ Resolves CODEXA_APP to "{{PROJECT_ROOT}}/codexa.app"
→ Resolves PROJECT_ROOT to git root (auto-detect)
→ Final: "C:\Users\Dell\...\codexa.gato\codexa.app\agentes\scout_agent"
```

### Three Consumption Modes

1. **Python Code**: `resolve_path("{{AGENTES}}/scout_agent")`
2. **Node.js Code**: `resolvePath('{{AGENTES}}/scout_agent')`
3. **Documentation**: Keep placeholders (human-readable)

---

## VALIDATION CHECKLIST

Before committing changes:

- [ ] Run `path_validator.py` → 0 errors, 0 warnings
- [ ] No hardcoded paths (`C:\`, `/home/`, relative traversal)
- [ ] All placeholders defined in registry
- [ ] All resolved paths exist
- [ ] Cross-platform tested (Windows + Linux)
- [ ] Documentation uses placeholders
- [ ] Agent workflows still pass
- [ ] MCP servers still work

---

## INTEGRATION POINTS

### With Existing Systems

| System | Integration Type | Status |
|--------|------------------|--------|
| `curso_agent/config/paths.py` | Update to use PathResolver | Designed |
| `51_AGENT_REGISTRY.json` | Convert paths to placeholders | Designed |
| `.mcp.json` | Use environment variables | Designed |
| `.claude/settings.json` | Add path_resolution config | Designed |
| Git hooks | Pre-commit validation | Designed |
| CI/CD | GitHub Actions validation | Designed |

### With CODEXA Laws

| Law | Alignment | Details |
|-----|-----------|---------|
| **LAW 1**: Distillation Principle | ✅ Aligned | Extends Mustache `{{PLACEHOLDERS}}` |
| **LAW 2**: Fractal Navigation | ✅ Aligned | Same pattern at all levels |
| **LAW 3**: Meta-Construction | ✅ Aligned | Registry = Builder (generates paths) |
| **LAW 4**: Agentic Design | ✅ Aligned | Each agent defines own paths |

---

## RESOURCES

### Documentation Files

- **This Index**: `specs/PATH_REGISTRY_INDEX.md`
- **Summary**: `specs/PATH_REGISTRY_SUMMARY.md`
- **Specification**: `specs/PATH_REGISTRY_SYSTEM_SPEC.md`
- **Migration Guide**: `specs/PATH_MIGRATION_GUIDE.md`

### Implementation Files (To Create)

- **Registry**: `path_registry.json` (project root)
- **Python Resolver**: `codexa.app/core/path_resolver.py`
- **Node Resolver**: `codexa.app/core/pathResolver.js`
- **Validator**: `codexa_agent/validators/14_path_validator.py`
- **Sync Script**: `codexa.app/core/path_sync.py`
- **Git Hook**: `.git/hooks/pre-commit`

### Related CODEXA Files

- **CLAUDE.md**: Project laws (LAW 1: Distillation Principle)
- **51_AGENT_REGISTRY.json**: Agent registry (to be updated)
- **ORCHESTRATION.md**: System orchestration
- **SCOUT_INTEGRATION.md**: MCP integration

---

## SUPPORT

### Getting Help

**Issue**: "I don't understand the architecture"
→ Read `PATH_REGISTRY_SUMMARY.md` Section "Architecture (3 Layers)"

**Issue**: "I need to implement the resolver"
→ Read `PATH_REGISTRY_SYSTEM_SPEC.md` Section 3.1 (complete Python code)

**Issue**: "I need to migrate an agent"
→ Follow `PATH_MIGRATION_GUIDE.md` per-agent checklist

**Issue**: "Path resolution is failing"
→ Check `PATH_MIGRATION_GUIDE.md` Section "Troubleshooting"

**Issue**: "I want to add a new placeholder"
→ Update `path_registry.json` Section "standard_placeholders"

### Creating Issues

For unresolved problems, create GitHub issue with:
1. Which document you read
2. Which step failed
3. Error message (full traceback)
4. Platform (Windows/Linux/macOS)
5. Python/Node.js version

---

## STATUS TRACKING

### Documentation

- [x] Summary created (PATH_REGISTRY_SUMMARY.md)
- [x] Specification created (PATH_REGISTRY_SYSTEM_SPEC.md)
- [x] Migration guide created (PATH_MIGRATION_GUIDE.md)
- [x] Index created (PATH_REGISTRY_INDEX.md)
- [x] Registry template created (path_registry.json)

### Implementation (Phase 1)

- [ ] Python resolver (path_resolver.py)
- [ ] Node.js resolver (pathResolver.js)
- [ ] Path validator (14_path_validator.py)
- [ ] Sync script (path_sync.py)
- [ ] Git hook (pre-commit)

### Migration (Phases 2-4)

- [ ] Phase 2: Pilot (scout_agent)
- [ ] Phase 3: Bulk (8 agents)
- [ ] Phase 4: Cleanup (remove legacy)

**Current Status**: Design Complete → Ready for Phase 1 Implementation

---

## VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-02 | Initial design package complete |

---

## CONTRIBUTORS

- **CODEXA Meta Agent**: System design, specification, documentation
- **Scout Agent**: Path discovery patterns, MCP integration
- **Mentor Agent**: Prompt engineering patterns, knowledge management

---

**End of Index**

> **Next Step**: Read `PATH_REGISTRY_SUMMARY.md` to understand the system, then proceed to `PATH_REGISTRY_SYSTEM_SPEC.md` for implementation details.
