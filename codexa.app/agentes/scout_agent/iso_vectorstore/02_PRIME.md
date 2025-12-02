<!-- iso_vectorstore -->
<!--
  Source: PRIME.md
  Agent: scout_agent
  Synced: 2025-11-30
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# /prime-scout | Path Discovery & Navigation System

**Version**: 1.0.0 | **Status**: Active | **Type**: Infrastructure Agent | **Architecture**: MCP Server

> **Scout**: Este é o próprio Scout! Veja [SCOUT_INTEGRATION.md](../SCOUT_INTEGRATION.md) para instruções de uso.

---

## 1. IDENTITY

| Field | Value |
|-------|-------|
| **Agent** | `scout_agent` |
| **Domain** | Path Discovery, File Indexing, CRUD Operations |
| **Role** | "Master of Paths" - Navigation nervous system for CODEXA |
| **Architecture** | MCP Server (Model Context Protocol) |

**Transform**:
- Input: Task description / Agent name / File pattern
- Output: `relevant_files[]` with paths, scores, and reasons

**Tagline**: Every agent's companion - knows where everything is

---

## 2. MODEL RECOMMENDATIONS

| Use Case | Model | Reasoning |
|----------|-------|-----------|
| **Path Discovery** | Any | Scout handles logic, LLM just calls tools |
| **Context Assembly** | Claude Sonnet 4+ | Synthesizing multiple file contexts |
| **CRUD Operations** | Any | Direct file operations |

**Why MCP Server?** Scout runs as separate process, maintains index, provides instant responses. Any LLM can use Scout via `mcp__scout__*` tools.

---

## 3. WHEN TO USE

**USE Scout for**:
- Finding relevant files for a task
- Getting all files for an agent
- Searching by pattern (glob/regex)
- CRUD operations with tracking
- Validating path references
- Building context maps

**Scout is AUTOMATIC**: When you run any `/prime-*`, Scout provides `relevant_files` context.

**DON'T USE Scout for**:
- File content analysis (use the LLM)
- Code execution (use Bash)
- Web requests (use WebFetch)

---

## 4. MCP TOOLS

### Discovery Tools (MVP)

```
mcp__scout__discover(query, agent?, max_results?)
  → Find files relevant to a natural language query
  → Returns: [{path, relevance_score, reason}]

mcp__scout__search(pattern, type?)
  → Search by glob pattern or regex
  → Returns: [{path, type, size, modified}]

mcp__scout__agent_context(agent, include_deps?)
  → Get all files for a specific agent
  → Returns: {entry_points, files_by_category, dependencies}
```

### Context Tools

```
mcp__scout__map_dependencies(file)
  → Build dependency graph for a file
  → Returns: {references, referenced_by}

mcp__scout__related(file, max_results?)
  → Find files related to a given file
  → Returns: [{path, relationship, score}]

mcp__scout__validate_paths(paths[])
  → Check if paths exist and are valid
  → Returns: {valid[], invalid[], suggestions[]}
```

### CRUD Tools

```
mcp__scout__create(path, content, category?, tags?)
  → Create new file with automatic indexing
  → Returns: {success, indexed_as}

mcp__scout__read(path)
  → Read file with metadata
  → Returns: {content, metadata}

mcp__scout__update(path, content)
  → Update file with backup
  → Returns: {success, backup_path}

mcp__scout__delete(path, confirm?)
  → Delete with safety checks
  → Returns: {success, backup_path}

mcp__scout__move(from, to)
  → Move/rename with reference updates
  → Returns: {success, updated_references[]}
```

### Index Tools

```
mcp__scout__refresh()
  → Rebuild index from scratch
  → Returns: {files_indexed, duration_ms}

mcp__scout__stats()
  → Get index statistics
  → Returns: {total_files, by_category, by_agent}
```

---

## 5. DATA STRUCTURES

### Relevant Files Response
```json
{
  "query": "create marketplace listing",
  "relevant_files": [
    {
      "path": "codexa.app/agentes/anuncio_agent/PRIME.md",
      "relevance_score": 0.95,
      "reason": "Primary entry point for ad generation",
      "category": "prime",
      "agent": "anuncio_agent"
    }
  ],
  "total_found": 15,
  "search_time_ms": 45
}
```

### Agent Context Response
```json
{
  "agent": "anuncio_agent",
  "entry_points": {
    "prime": "codexa.app/agentes/anuncio_agent/PRIME.md",
    "readme": "codexa.app/agentes/anuncio_agent/README.md",
    "command": ".claude/commands/prime_anuncio.md"
  },
  "files_by_category": {
    "prompts": ["prompts/14_title_HOP.md", "..."],
    "config": ["config/copy_rules.json", "..."],
    "schemas": ["schemas/input.json", "..."]
  },
  "dependencies": {
    "requires": ["pesquisa_agent"],
    "optional": ["marca_agent"]
  },
  "total_files": 45
}
```

---

## 6. RELEVANCE SCORING

Scout uses multi-factor scoring (0.0 - 1.0):

| Factor | Weight | Description |
|--------|--------|-------------|
| Text Match | 40% | Fuzzy match on path + tags |
| Category Priority | 20% | PRIME > README > HOP > config |
| Agent Match | 25% | Boost if matches requested agent |
| Recency | 15% | Recently modified files rank higher |

### Category Priorities
```
prime: 1.0
readme: 0.9
instructions: 0.85
hop: 0.8
adw: 0.8
config: 0.7
prompt: 0.7
schema: 0.6
builder: 0.6
validator: 0.6
```

---

## 7. INDEXING

### What Gets Indexed
- All `.md` files (documentation)
- All `.json` files (config, schemas)
- All `.py` files (builders, validators)
- All `.js/.ts` files (MCP servers)
- Command files in `.claude/commands/`

### What Gets Ignored
```
node_modules/**
.venv/**
__pycache__/**
.git/**
*.pyc, *.pyo
*.log, *.tmp
.DS_Store, Thumbs.db
```

### Index Rebuild
- Automatic on server start
- Manual via `mcp__scout__refresh()`
- Estimated time: <5s for 5000 files

---

## 8. INTEGRATION WITH PRIMES

### How It Works
1. User runs `/prime-anuncio`
2. Prime command includes: `<scout agent="anuncio_agent" />`
3. Scout returns `agent_context` automatically
4. LLM receives full file list with relevance scores

### Example Integration
```markdown
## NAVIGATION

<!-- Scout provides this automatically -->
Entry Points:
- PRIME.md (this file) - score: 1.0
- README.md - score: 0.9
- .claude/commands/prime_anuncio.md - score: 0.85

Key Files (by category):
- prompts/ (15 HOPs)
- config/ (4 files)
- schemas/ (3 files)
```

---

## 9. SAFETY

### CRUD Safety Rules
1. **Backup Before Delete**: Creates `.bak` file
2. **Path Validation**: Rejects paths outside project
3. **Confirm Destructive**: Requires `confirm: true` for delete
4. **Audit Log**: All operations logged
5. **Protected Paths**: Cannot modify `.git/`, `node_modules/`

### Protected Patterns
```json
[
  ".git/**",
  "node_modules/**",
  ".venv/**",
  "*.exe",
  "*.dll"
]
```

---

## 10. CONFIGURATION

### Environment Variables
```bash
SCOUT_ROOT=/path/to/project     # Project root (default: cwd)
SCOUT_CACHE_MODE=session        # session | persistent
SCOUT_LOG_LEVEL=info            # debug | info | warn | error
```

### Config Files
```
scout_agent/config/
├── categories.json      # Category detection rules
├── ignore_patterns.json # Files to ignore
├── relevance_weights.json # Scoring weights
└── protected_paths.json # Cannot modify
```

---

## 11. KEY FILES

```
scout_agent/
├── PRIME.md             # This file
├── README.md            # Quick start
├── INSTRUCTIONS.md      # AI assistant guide
├── config/
│   ├── categories.json
│   ├── ignore_patterns.json
│   └── relevance_weights.json
└── iso_vectorstore/
    └── 01_QUICK_START.md

mcp-servers/scout-mcp/
├── index.js             # MCP server entry
├── package.json
└── README.md
```

---

## 12. EXAMPLES

### Example 1: Find Files for Task
```
User: "I need to create a product listing"

Scout call:
mcp__scout__discover("create product listing")

Response:
- anuncio_agent/PRIME.md (0.95) - "Entry point for ad generation"
- anuncio_agent/prompts/14_title_HOP.md (0.88) - "Title generation"
- pesquisa_agent/PRIME.md (0.72) - "Research dependency"
```

### Example 2: Get Agent Context
```
Scout call:
mcp__scout__agent_context("codexa_agent")

Response:
{
  "entry_points": {
    "prime": "codexa_agent/PRIME.md",
    "readme": "codexa_agent/README.md"
  },
  "files_by_category": {
    "builders": 13,
    "validators": 7,
    "prompts": 5,
    "workflows": 7
  },
  "total_files": 89
}
```

### Example 3: Search by Pattern
```
Scout call:
mcp__scout__search("**/*_HOP.md")

Response:
- anuncio_agent/prompts/14_title_HOP.md
- anuncio_agent/prompts/15_keywords_HOP.md
- codexa_agent/prompts/91_meta_build_agent_HOP.md
- ... (all HOP files)
```

---

## 13. PERFORMANCE

| Operation | Target | Actual |
|-----------|--------|--------|
| Index Build | <5s (5000 files) | ~2-3s |
| discover() | <100ms | ~50ms |
| search() | <50ms | ~20ms |
| agent_context() | <100ms | ~30ms |
| CRUD ops | <200ms | ~100ms |

---

## 14. CHANGELOG

### v1.0.0 (2025-11-28)
- Initial release
- MVP tools: discover, search, agent_context
- CRUD tools: create, read, update, delete, move
- Index management: refresh, stats
- Multi-factor relevance scoring
- Safety system with backups

---

## 15. SHARED PRINCIPLES

> See full details: [SHARED_PRINCIPLES.md](../SHARED_PRINCIPLES.md)

### Tasks vs Roles (Sub-agents)
- ❌ "You are a file search expert" → ✅ "Find all HOP files in codexa_agent"
- ❌ "Navigate the codebase" → ✅ "Return agent_context for anuncio_agent"

### Human Ownership (Search Results)
```markdown
- [ ] Results are relevant to query (score ≥0.7)
- [ ] File paths are valid and accessible
- [ ] Category classification makes sense
- [ ] No sensitive files exposed
```

### Value Function (Search Confidence)
| Operation | Confidence Check |
|-----------|------------------|
| discover() | ≥3 results? Top score ≥0.8? |
| search() | Pattern matches expected files? |
| agent_context() | All categories present? |
| CRUD | Backup created? Path validated? |

---

**Author**: CODEXA Meta-Constructor
**Created**: 2025-11-28
**Updated**: 2025-11-29 (Shared Principles)
**Dependencies**: None (infrastructure agent)
**Integration**: All agents via MCP tools

---

> "Scout knows where everything is, so you don't have to."
