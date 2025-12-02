# PATH REGISTRY SYSTEM - VISUAL GUIDE

**Version**: 1.0.0 | **Created**: 2025-12-02 | **Type**: Visual Documentation

---

## SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CODEXA PATH REGISTRY SYSTEM                      │
│                    (Cross-Platform Path Management)                     │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
┌───────────────────────┐ ┌──────────────────┐ ┌───────────────────────┐
│   STORAGE LAYER       │ │ RESOLUTION LAYER │ │  CONSUMPTION LAYER    │
│                       │ │                  │ │                       │
│  path_registry.json   │ │  PathResolver    │ │  Python Modules       │
│                       │ │                  │ │  Node.js Modules      │
│  • root_anchors       │ │  • Python        │ │  Documentation        │
│  • agent_paths        │ │  • Node.js       │ │  MCP Configs          │
│  • common_paths       │ │  • Auto-detect   │ │  Agent Registry       │
│  • placeholders       │ │  • Validation    │ │  Builder Scripts      │
│                       │ │                  │ │  Git Hooks            │
└───────────────────────┘ └──────────────────┘ └───────────────────────┘
```

---

## PATH RESOLUTION FLOW

```
USER CODE
   │
   │  resolve_path("{{AGENTES}}/scout_agent/PRIME.md")
   │
   ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: Parse Placeholder                                  │
│  Extract: "AGENTES"                                         │
└─────────────────────────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: Lookup in Registry                                 │
│  "{{AGENTES}}" → "{{CODEXA_APP}}/agentes"                  │
└─────────────────────────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: Resolve Parent Placeholder                         │
│  "{{CODEXA_APP}}" → "{{PROJECT_ROOT}}/codexa.app"          │
└─────────────────────────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: Auto-Detect Root                                   │
│  Walk up from __file__ to find .git directory               │
│  Found: "C:\Users\Dell\...\codexa.gato"                     │
└─────────────────────────────────────────────────────────────┘
   │
   ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: Substitute & Resolve                               │
│  "C:\...\codexa.gato\codexa.app\agentes\scout_agent\..."   │
└─────────────────────────────────────────────────────────────┘
   │
   ▼
RESOLVED ABSOLUTE PATH
```

---

## PLACEHOLDER HIERARCHY

```
{{PROJECT_ROOT}}
    │
    ├─ .git/
    ├─ path_registry.json
    ├─ CLAUDE.md
    │
    ├─ {{CODEXA_APP}}
    │   │
    │   ├─ {{AGENTES}}
    │   │   │
    │   │   ├─ 51_AGENT_REGISTRY.json
    │   │   │
    │   │   ├─ {{AGENT_DIR}} (scout_agent)
    │   │   │   ├─ PRIME.md
    │   │   │   ├─ README.md
    │   │   │   │
    │   │   │   ├─ {{AGENT_CONFIG}}
    │   │   │   │   ├─ categories.json
    │   │   │   │   ├─ relevance_weights.json
    │   │   │   │   └─ paths.py
    │   │   │   │
    │   │   │   ├─ {{AGENT_ISO}}
    │   │   │   │   └─ 04_README.md
    │   │   │   │
    │   │   │   └─ {{AGENT_WORKFLOWS}}
    │   │   │       └─ 100_ADW_DISCOVERY.md
    │   │   │
    │   │   ├─ {{AGENT_DIR}} (codexa_agent)
    │   │   │   ├─ {{AGENT_BUILDERS}}
    │   │   │   ├─ {{AGENT_VALIDATORS}}
    │   │   │   └─ {{AGENT_PROMPTS}}
    │   │   │
    │   │   └─ ... (7 more agents)
    │   │
    │   ├─ {{MCP_SERVERS}}
    │   │   └─ scout-mcp/
    │   │       └─ index.js
    │   │
    │   └─ voice/
    │
    └─ {{CLAUDE_DIR}}
        ├─ commands/
        └─ hooks/
```

---

## CROSS-PLATFORM COMPATIBILITY

```
┌─────────────────────────────────────────────────────────────────────┐
│                         SAME CODE                                   │
│  resolve_path("{{AGENTES}}/scout_agent/PRIME.md")                  │
└─────────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│   WINDOWS         │ │     LINUX        │ │     macOS        │
│                   │ │                  │ │                  │
│  C:\Users\Dell\   │ │  /home/user/     │ │  /Users/dev/     │
│  ...\codexa.gato\ │ │  .../codexa.gato/│ │  .../codexa.gato/│
│  codexa.app\      │ │  codexa.app/     │ │  codexa.app/     │
│  agentes\         │ │  agentes/        │ │  agentes/        │
│  scout_agent\     │ │  scout_agent/    │ │  scout_agent/    │
│  PRIME.md         │ │  PRIME.md        │ │  PRIME.md        │
│                   │ │                  │ │                  │
│  ✅ WORKS         │ │  ✅ WORKS        │ │  ✅ WORKS        │
└───────────────────┘ └──────────────────┘ └──────────────────┘
```

---

## BEFORE VS AFTER

### Before (Hardcoded Paths)

```
┌────────────────────────────────────────────────────────────────┐
│  FILE: scout_agent/config/paths.py                            │
├────────────────────────────────────────────────────────────────┤
│  from pathlib import Path                                      │
│                                                                │
│  # Hardcoded relative traversal ❌                            │
│  SCOUT_AGENT_DIR = Path(__file__).parent.parent               │
│  AGENTS_ROOT = SCOUT_AGENT_DIR.parent                         │
│  CODEXA_APP = AGENTS_ROOT.parent                              │
│  PROJECT_ROOT = CODEXA_APP.parent                             │
│                                                                │
│  # Breaks when:                                                │
│  # - Called from different directory                           │
│  # - Project moves to different machine                        │
│  # - Symlinks involved                                         │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  FILE: PRIME.md                                                │
├────────────────────────────────────────────────────────────────┤
│  # Scout Agent                                                 │
│                                                                │
│  Location: codexa.app/agentes/scout_agent/PRIME.md ❌         │
│  Config: codexa.app/agentes/scout_agent/config/categories.json│
│                                                                │
│  # Not portable - assumes specific structure                   │
└────────────────────────────────────────────────────────────────┘
```

### After (Path Registry)

```
┌────────────────────────────────────────────────────────────────┐
│  FILE: scout_agent/config/paths.py                            │
├────────────────────────────────────────────────────────────────┤
│  from codexa.core.path_resolver import PathResolver           │
│                                                                │
│  resolver = PathResolver()                                     │
│                                                                │
│  # Dynamic resolution ✅                                       │
│  SCOUT_AGENT_DIR = resolver.resolve("{{AGENTES}}/scout_agent")│
│  AGENTS_ROOT = resolver.resolve("{{AGENTES}}")                │
│  CODEXA_APP = resolver.resolve("{{CODEXA_APP}}")              │
│  PROJECT_ROOT = resolver.resolve("{{PROJECT_ROOT}}")          │
│                                                                │
│  # Works everywhere:                                           │
│  # - Auto-detects git root                                     │
│  # - Cross-platform (Windows/Linux/macOS)                      │
│  # - Single source of truth                                    │
└────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────┐
│  FILE: PRIME.md                                                │
├────────────────────────────────────────────────────────────────┤
│  # Scout Agent                                                 │
│                                                                │
│  Location: {{AGENTES}}/scout_agent/PRIME.md ✅                │
│  Config: {{AGENTES}}/scout_agent/config/categories.json       │
│                                                                │
│  # Portable - works on any machine                             │
│  # Human-readable - clear intent                               │
└────────────────────────────────────────────────────────────────┘
```

---

## DATA FLOW DIAGRAM

```
┌──────────────────────────────────────────────────────────────────────┐
│                     APPLICATION STARTUP                              │
└──────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  1. Load path_registry.json                 │
        │     (Single source of truth)                │
        └─────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  2. Auto-detect PROJECT_ROOT                │
        │     Walk up to find .git directory          │
        │     Validate: must contain codexa.app       │
        └─────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  3. Resolve root anchors                    │
        │     CODEXA_APP = PROJECT_ROOT/codexa.app    │
        │     AGENTES = CODEXA_APP/agentes            │
        └─────────────────────────────────────────────┘
                              │
                              ▼
        ┌─────────────────────────────────────────────┐
        │  4. Cache resolved paths                    │
        │     Store in _root_cache for performance    │
        └─────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────┐
│                     RUNTIME PATH RESOLUTION                          │
└──────────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┴─────────────────┐
            │                                   │
            ▼                                   ▼
  ┌─────────────────────┐           ┌─────────────────────┐
  │  Python Code        │           │  Documentation      │
  │                     │           │                     │
  │  resolve_path()     │           │  {{PLACEHOLDERS}}   │
  │  → absolute path    │           │  → keep as-is       │
  └─────────────────────┘           │  (human-readable)   │
                                    └─────────────────────┘
```

---

## MIGRATION TIMELINE

```
WEEK 1: FOUNDATION
┌────────────────────────────────────────────────────────────┐
│  Monday    │ Create path_registry.json                     │
│  Tuesday   │ Implement path_resolver.py (Python)           │
│  Wednesday │ Implement pathResolver.js (Node.js)           │
│  Thursday  │ Implement path_validator.py                   │
│  Friday    │ Test cross-platform (Windows + Linux)         │
└────────────────────────────────────────────────────────────┘
           Status: Infrastructure ready, no production impact

WEEK 2: PILOT
┌────────────────────────────────────────────────────────────┐
│  Monday    │ Migrate scout_agent/config/paths.py           │
│  Tuesday   │ Update scout_agent documentation              │
│  Wednesday │ Test all scout workflows                      │
│  Thursday  │ Create .mcp.json for scout-mcp                │
│  Friday    │ Document lessons learned                      │
└────────────────────────────────────────────────────────────┘
           Status: 1/9 agents migrated (proof of concept)

WEEK 3: BULK MIGRATION
┌────────────────────────────────────────────────────────────┐
│  Monday    │ Migrate codexa_agent (critical)               │
│  Tuesday   │ Migrate mentor_agent + anuncio_agent          │
│  Wednesday │ Migrate pesquisa_agent + marca_agent          │
│  Thursday  │ Migrate photo_agent + video_agent             │
│  Friday    │ Migrate curso_agent + validation              │
└────────────────────────────────────────────────────────────┘
           Status: 9/9 agents migrated, all workflows passing

WEEK 4: CLEANUP
┌────────────────────────────────────────────────────────────┐
│  Monday    │ Remove legacy path code                       │
│  Tuesday   │ Enable git pre-commit hook                    │
│  Wednesday │ Update CLAUDE.md (LAW 5: Paths)               │
│  Thursday  │ Create training materials                     │
│  Friday    │ Announce completion + retrospective           │
└────────────────────────────────────────────────────────────┘
           Status: Production-ready, validation enforced
```

---

## VALIDATION WORKFLOW

```
┌──────────────────────────────────────────────────────────────┐
│                    DEVELOPER WORKFLOW                        │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │  1. Write code with placeholders  │
        │     resolve_path("{{AGENTES}}/")  │
        └───────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │  2. Test locally                  │
        │     python script.py              │
        └───────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │  3. Run validator                 │
        │     path_validator.py             │
        └───────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
        ┌──────────────┐        ┌──────────────┐
        │   PASS ✅    │        │   FAIL ❌    │
        └──────────────┘        └──────────────┘
                │                       │
                │                       ▼
                │               ┌──────────────┐
                │               │  Fix errors  │
                │               └──────────────┘
                │                       │
                └───────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────┐
        │  4. Git commit                    │
        │     Pre-commit hook runs          │
        └───────────────────────────────────┘
                            │
                ┌───────────┴───────────┐
                │                       │
                ▼                       ▼
        ┌──────────────┐        ┌──────────────┐
        │  COMMIT ✅   │        │  BLOCKED ❌  │
        └──────────────┘        └──────────────┘
```

---

## AGENT DEPENDENCY MAP

```
┌──────────────────────────────────────────────────────────────┐
│                   PATH REGISTRY SYSTEM                       │
│                  (Central Infrastructure)                    │
└──────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ scout_agent  │    │ codexa_agent │    │ mentor_agent │
│              │    │              │    │              │
│ • No deps    │    │ • No deps    │    │ • scout dep  │
│ • MCP server │    │ • Builders   │    │ • FONTES     │
│ • Phase 2    │    │ • Validators │    │ • Phase 3    │
└──────────────┘    │ • CRITICAL   │    └──────────────┘
                    │ • Phase 3.1  │
                    └──────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│anuncio_agent │    │pesquisa_agent│    │ marca_agent  │
│              │    │              │    │              │
│ • pesquisa   │    │ • No deps    │    │ • No deps    │
│   dep        │    │ • Phase 3.2  │    │ • Phase 3.3  │
│ • Phase 3.2  │    └──────────────┘    └──────────────┘
└──────────────┘
        │
        ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│ photo_agent  │    │ video_agent  │    │ curso_agent  │
│              │    │              │    │              │
│ • No deps    │    │ • No deps    │    │ • 3 agent    │
│ • Phase 3.4  │    │ • Phase 3.5  │    │   deps       │
└──────────────┘    └──────────────┘    │ • Phase 3.6  │
                                        └──────────────┘
```

---

## ERROR HANDLING FLOW

```
resolve_path("{{INVALID}}/path")
        │
        ▼
┌────────────────────────────────────┐
│  Check placeholder in registry?    │
└────────────────────────────────────┘
        │
        ├─ NO → KeyError: "Unknown placeholder: {{INVALID}}"
        │       ↓
        │       Log error + suggest valid placeholders
        │
        └─ YES → Continue resolution
                    │
                    ▼
        ┌────────────────────────────────────┐
        │  Can auto-detect root?             │
        └────────────────────────────────────┘
                    │
                    ├─ NO → RuntimeError: "Could not detect PROJECT_ROOT"
                    │       ↓
                    │       Suggest: Set env var or check .git exists
                    │
                    └─ YES → Continue resolution
                                │
                                ▼
                    ┌────────────────────────────────────┐
                    │  Does resolved path exist?         │
                    └────────────────────────────────────┘
                                │
                                ├─ NO → Warning: "Path does not exist: ..."
                                │       ↓
                                │       Return path anyway (may be created later)
                                │
                                └─ YES → Return absolute path ✅
```

---

## REGISTRY STRUCTURE VISUAL

```
path_registry.json
├─ metadata
│  ├─ version: "1.0.0"
│  ├─ created: "2025-12-02"
│  └─ schema_version: "1.0.0"
│
├─ root_anchors (Auto-detected)
│  ├─ PROJECT_ROOT
│  │  ├─ detection_strategy: "git_root"
│  │  ├─ fallback: "env:PROJECT_ROOT"
│  │  └─ validation: "must_contain: [.git, codexa.app]"
│  │
│  ├─ CODEXA_APP
│  │  ├─ relative_to: "PROJECT_ROOT"
│  │  └─ path: "codexa.app"
│  │
│  └─ AGENTES
│     ├─ relative_to: "CODEXA_APP"
│     └─ path: "agentes"
│
├─ standard_placeholders (Reusable)
│  ├─ system_level
│  │  ├─ {{PROJECT_ROOT}}
│  │  ├─ {{CODEXA_APP}}
│  │  ├─ {{AGENTES}}
│  │  ├─ {{MCP_SERVERS}}
│  │  └─ {{CLAUDE_DIR}}
│  │
│  └─ agent_level
│     ├─ {{AGENT_DIR}}
│     ├─ {{AGENT_CONFIG}}
│     ├─ {{AGENT_ISO}}
│     └─ {{AGENT_WORKFLOWS}}
│
├─ agent_paths (Per-agent)
│  ├─ scout_agent
│  │  ├─ prime: "{{AGENTES}}/scout_agent/PRIME.md"
│  │  ├─ config: "{{AGENTES}}/scout_agent/config"
│  │  └─ mcp_server: "{{MCP_SERVERS}}/scout-mcp/index.js"
│  │
│  ├─ codexa_agent
│  │  ├─ prime: "{{AGENTES}}/codexa_agent/PRIME.md"
│  │  ├─ builders: "{{AGENTES}}/codexa_agent/builders"
│  │  └─ validators: "{{AGENTES}}/codexa_agent/validators"
│  │
│  └─ ... (7 more agents)
│
├─ common_paths (Shared)
│  ├─ registry: "{{AGENTES}}/51_AGENT_REGISTRY.json"
│  ├─ claude_md: "{{PROJECT_ROOT}}/CLAUDE.md"
│  └─ scout_integration: "{{AGENTES}}/SCOUT_INTEGRATION.md"
│
└─ output_paths (Generated)
   ├─ agent_outputs: "{{AGENT_DIR}}/outputs"
   ├─ artifacts: "{{AGENT_DIR}}/artifacts"
   └─ logs: "{{PROJECT_ROOT}}/logs"
```

---

## COMPLETION CHECKLIST

```
PHASE 1: FOUNDATION
[ ] path_registry.json created (project root)
[ ] path_resolver.py implemented (Python)
[ ] pathResolver.js implemented (Node.js)
[ ] path_validator.py implemented
[ ] path_sync.py implemented
[ ] Git pre-commit hook created
[ ] Cross-platform testing (Windows + Linux)
[ ] Documentation complete

PHASE 2: PILOT
[ ] scout_agent/config/paths.py migrated
[ ] scout_agent/PRIME.md updated
[ ] scout_agent/README.md updated
[ ] All scout workflows passing
[ ] .mcp.json created for scout-mcp
[ ] Lessons learned documented

PHASE 3: BULK
[ ] codexa_agent migrated (CRITICAL)
[ ] mentor_agent migrated
[ ] anuncio_agent migrated
[ ] pesquisa_agent migrated
[ ] marca_agent migrated
[ ] photo_agent migrated
[ ] video_agent migrated
[ ] curso_agent migrated
[ ] All workflows passing
[ ] Full system validation

PHASE 4: CLEANUP
[ ] Legacy path code removed
[ ] Git pre-commit hook enabled (enforced)
[ ] CLAUDE.md updated (LAW 5: Paths)
[ ] Training materials created
[ ] Announcement sent
[ ] Retrospective completed

SYSTEM STATUS
[ ] 0 hardcoded paths remain
[ ] 0 validation errors
[ ] 0 validation warnings
[ ] 100% agent coverage
[ ] Cross-platform verified
[ ] Production-ready
```

---

**Version**: 1.0.0
**Type**: Visual Guide
**Purpose**: Quick understanding through diagrams
**Status**: Complete

**End of Visual Guide**
