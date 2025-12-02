# SPEC: scout_agent v1.0.0

## Executive Summary

**Problem**: CODEXA project has 5,240+ files. Navigation is manual, paths break, agents don't know each other's files, mentor_agent is overloaded with 4 responsibilities (violates OPOP).

**Solution**: Create `scout_agent` - a dedicated MCP Server for path discovery, file indexing, and CRUD operations. Scout runs as companion to ALL agents, providing `relevant_files` context automatically.

**Scope**:
- EXTRACT Scout functionality from mentor_agent
- KEEP mentor_agent focused on knowledge processing + mentoring
- CREATE scout_agent as MCP Server (scalable, portable)

---

## 1. IDENTITY

| Field | Value |
|-------|-------|
| **Agent** | `scout_agent` |
| **Version** | 1.0.0 |
| **Type** | Infrastructure / Meta-Agent |
| **Architecture** | MCP Server (Model Context Protocol) |
| **Domain** | Path Discovery, File Indexing, CRUD Operations |
| **Status** | SPEC (Not Implemented) |

**Transform**:
- Input: Task description / Agent context
- Output: `relevant_files.json` + `context_map.json` + live queries

**Tagline**: "Master of Paths" - The nervous system of CODEXA navigation

---

## 2. WHY MCP SERVER?

### Comparison of Integration Options

| Option | Scalability | Portability | Runtime | Complexity |
|--------|-------------|-------------|---------|------------|
| Python Import | Low | Low (Python only) | In-process | Simple |
| **MCP Server** | **High** | **High (any LLM)** | **Separate process** | **Medium** |
| Prompt Injection | Medium | High | Pre-process | Simple |

### MCP Advantages for Scout

1. **Universal Access**: Any agent can call `mcp__scout__*` tools
2. **Separate Process**: Scout maintains state independently
3. **Language Agnostic**: Works with any LLM (Claude, GPT, Gemini)
4. **Cacheable**: Index survives between sessions (optional persistence)
5. **Composable**: Can be used in any CODEXA project

---

## 3. CAPABILITIES (MVP → Full)

### Phase 1: MVP - Path Discovery
```
mcp__scout__discover(query: string) → relevant_files[]
mcp__scout__index(path: string) → file_metadata
mcp__scout__search(pattern: string) → matches[]
```

### Phase 2: Context Mapping
```
mcp__scout__map_dependencies(file: string) → dependency_graph
mcp__scout__related(file: string) → related_files[]
mcp__scout__agent_context(agent: string) → agent_files[]
```

### Phase 3: CRUD Operations
```
mcp__scout__create(path: string, content: string) → success
mcp__scout__read(path: string) → content
mcp__scout__update(path: string, changes: object) → success
mcp__scout__delete(path: string) → success
mcp__scout__move(from: string, to: string) → success
```

### Phase 4: Live Index
```
mcp__scout__watch(path: string) → subscription
mcp__scout__refresh() → updated_index
mcp__scout__validate_paths(paths: string[]) → validation_result
```

---

## 4. DATA STRUCTURES

### 4.1 File Index Entry
```json
{
  "path": "codexa.app/agentes/anuncio_agent/PRIME.md",
  "type": "markdown",
  "category": "prime",
  "agent": "anuncio_agent",
  "size_bytes": 12450,
  "last_modified": "2025-11-25T10:30:00Z",
  "hash": "sha256:abc123...",
  "tags": ["agent", "prime", "e-commerce", "anuncio"],
  "references": [
    "codexa.app/agentes/anuncio_agent/README.md",
    "codexa.app/agentes/pesquisa_agent/PRIME.md"
  ],
  "referenced_by": [
    ".claude/commands/prime_anuncio.md"
  ]
}
```

### 4.2 Relevant Files Response
```json
{
  "query": "create marketplace listing",
  "agent_context": "anuncio_agent",
  "relevant_files": [
    {
      "path": "codexa.app/agentes/anuncio_agent/PRIME.md",
      "relevance_score": 0.95,
      "reason": "Primary entry point for ad generation"
    },
    {
      "path": "codexa.app/agentes/anuncio_agent/prompts/14_title_generator_HOP.md",
      "relevance_score": 0.88,
      "reason": "Title generation HOP"
    }
  ],
  "total_files": 15,
  "truncated": false
}
```

### 4.3 Context Map
```json
{
  "agent": "anuncio_agent",
  "entry_points": {
    "prime": "codexa.app/agentes/anuncio_agent/PRIME.md",
    "readme": "codexa.app/agentes/anuncio_agent/README.md",
    "commands": [".claude/commands/prime_anuncio.md"]
  },
  "dependencies": {
    "requires": ["pesquisa_agent"],
    "optional": ["marca_agent", "photo_agent"]
  },
  "file_categories": {
    "prompts": 15,
    "config": 4,
    "templates": 2,
    "schemas": 3
  },
  "total_files": 45
}
```

---

## 5. MCP SERVER SPECIFICATION

### 5.1 Server Configuration
```json
{
  "name": "scout",
  "version": "1.0.0",
  "description": "Path discovery and file indexing for CODEXA",
  "transport": "stdio",
  "tools": [
    "discover",
    "index",
    "search",
    "map_dependencies",
    "related",
    "agent_context",
    "create",
    "read",
    "update",
    "delete",
    "move",
    "watch",
    "refresh",
    "validate_paths"
  ]
}
```

### 5.2 Tool Definitions

#### discover
```json
{
  "name": "discover",
  "description": "Find relevant files for a task/query",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "Natural language description of task"
      },
      "agent": {
        "type": "string",
        "description": "Optional: limit to specific agent context"
      },
      "max_results": {
        "type": "integer",
        "default": 10
      }
    },
    "required": ["query"]
  }
}
```

#### agent_context
```json
{
  "name": "agent_context",
  "description": "Get all files relevant to a specific agent",
  "inputSchema": {
    "type": "object",
    "properties": {
      "agent": {
        "type": "string",
        "description": "Agent name (e.g., anuncio_agent)"
      },
      "include_dependencies": {
        "type": "boolean",
        "default": true
      }
    },
    "required": ["agent"]
  }
}
```

#### create (CRUD)
```json
{
  "name": "create",
  "description": "Create a new file with content",
  "inputSchema": {
    "type": "object",
    "properties": {
      "path": {
        "type": "string",
        "description": "Relative path from project root"
      },
      "content": {
        "type": "string",
        "description": "File content"
      },
      "category": {
        "type": "string",
        "description": "File category for indexing"
      },
      "tags": {
        "type": "array",
        "items": {"type": "string"}
      }
    },
    "required": ["path", "content"]
  }
}
```

---

## 6. INTEGRATION WITH PRIMES

### Current State (Manual)
```markdown
## 5. NAVIGATION

### For Local Development
PRIME.md          → This file
README.md         → Full documentation
config/           → Configuration files
prompts/          → HOP modules
```

### Future State (Scout-Powered)
```markdown
## 5. NAVIGATION

<scout_context agent="anuncio_agent" />
<!-- Scout injects relevant_files automatically -->
```

### Prime Injection Pattern
When any `/prime-*` command runs:
1. Scout is called: `mcp__scout__agent_context(agent)`
2. Scout returns `relevant_files.json`
3. Files are listed in PRIME response
4. User/LLM has full context automatically

---

## 7. INDEXING STRATEGY

### 7.1 Initial Index Build
```python
def build_index(root_path: str) -> Index:
    """
    Scan project and build complete index.
    Estimated time: ~2-5 seconds for 5000 files.
    """
    index = Index()

    for path in walk_files(root_path):
        # Skip node_modules, .venv, __pycache__, etc.
        if should_ignore(path):
            continue

        entry = FileEntry(
            path=path,
            type=detect_type(path),
            category=detect_category(path),
            agent=detect_agent(path),
            size=get_size(path),
            modified=get_modified(path),
            hash=compute_hash(path),
            tags=extract_tags(path),
            references=extract_references(path)
        )
        index.add(entry)

    return index
```

### 7.2 Category Detection Rules
```python
CATEGORY_RULES = {
    "prime": lambda p: p.endswith("PRIME.md"),
    "readme": lambda p: "README" in p.upper(),
    "instructions": lambda p: "INSTRUCTIONS" in p.upper(),
    "hop": lambda p: "_HOP.md" in p,
    "adw": lambda p: "_ADW" in p or "ADW_" in p,
    "config": lambda p: p.endswith(".json") and "config" in p.lower(),
    "schema": lambda p: "schema" in p.lower() and p.endswith(".json"),
    "prompt": lambda p: "/prompts/" in p,
    "builder": lambda p: "/builders/" in p,
    "validator": lambda p: "/validators/" in p,
    "command": lambda p: "/.claude/commands/" in p,
    "workflow": lambda p: "/workflows/" in p,
}
```

### 7.3 Reference Extraction
```python
def extract_references(file_path: str) -> List[str]:
    """Extract file references from content."""
    content = read_file(file_path)
    references = []

    # Markdown links: [text](path)
    references += re.findall(r'\[.*?\]\((.*?\.(?:md|json|py))\)', content)

    # Code paths: "path/to/file.ext"
    references += re.findall(r'"([^"]+\.(?:md|json|py))"', content)

    # Relative imports: from .module import
    references += re.findall(r'from\s+\.(\w+)', content)

    return deduplicate(references)
```

---

## 8. CACHE STRATEGY

### Per-Session Cache (MVP)
```python
class SessionCache:
    """
    Rebuilds index at session start.
    Keeps in memory during session.
    No persistence between sessions.
    """
    def __init__(self, root_path: str):
        self.index = build_index(root_path)
        self.query_cache = {}  # LRU cache for queries

    def discover(self, query: str) -> List[FileEntry]:
        if query in self.query_cache:
            return self.query_cache[query]

        results = self.index.search(query)
        self.query_cache[query] = results
        return results
```

### Optimization: Incremental Updates
```python
def refresh_index(self):
    """
    Only re-index changed files.
    Uses file hashes to detect changes.
    """
    for path in walk_files(self.root_path):
        current_hash = compute_hash(path)
        cached_entry = self.index.get(path)

        if cached_entry is None:
            # New file
            self.index.add(self._index_file(path))
        elif cached_entry.hash != current_hash:
            # Modified file
            self.index.update(path, self._index_file(path))

    # Remove deleted files
    for path in self.index.all_paths():
        if not exists(path):
            self.index.remove(path)
```

---

## 9. RELEVANCE SCORING

### Multi-Factor Scoring
```python
def calculate_relevance(query: str, entry: FileEntry, agent_context: str = None) -> float:
    """
    Calculate relevance score (0.0 - 1.0) for a file entry.
    """
    score = 0.0

    # 1. Text match (40% weight)
    text_score = fuzzy_match(query, entry.path + entry.tags)
    score += text_score * 0.4

    # 2. Category priority (20% weight)
    category_priority = {
        "prime": 1.0,
        "readme": 0.9,
        "instructions": 0.85,
        "hop": 0.8,
        "adw": 0.8,
        "config": 0.7,
        "prompt": 0.7,
        "schema": 0.6,
    }
    score += category_priority.get(entry.category, 0.5) * 0.2

    # 3. Agent match (25% weight)
    if agent_context and entry.agent == agent_context:
        score += 0.25

    # 4. Recency (15% weight)
    days_old = (now() - entry.modified).days
    recency_score = max(0, 1 - (days_old / 365))
    score += recency_score * 0.15

    return min(1.0, score)
```

---

## 10. IMPLEMENTATION PLAN

### Phase 1: MVP (Path Discovery) - 2-3 days
```
[ ] Create mcp-servers/scout-mcp/ directory
[ ] Implement core MCP server (stdio transport)
[ ] Implement index building
[ ] Implement discover() tool
[ ] Implement search() tool
[ ] Implement agent_context() tool
[ ] Add to .mcp.json configuration
[ ] Test with Claude Code
```

### Phase 2: Context Mapping - 1-2 days
```
[ ] Implement map_dependencies()
[ ] Implement related()
[ ] Build reference graph
[ ] Add bidirectional links
```

### Phase 3: CRUD Operations - 2-3 days
```
[ ] Implement create()
[ ] Implement read()
[ ] Implement update()
[ ] Implement delete()
[ ] Implement move()
[ ] Add validation and safety checks
[ ] Add backup before destructive operations
```

### Phase 4: Live Index - 1-2 days
```
[ ] Implement watch() with file system events
[ ] Implement refresh()
[ ] Implement validate_paths()
[ ] Add automatic re-indexing
```

### Phase 5: Prime Integration - 1 day
```
[ ] Update all PRIMEs to use Scout
[ ] Create <scout_context> injection pattern
[ ] Update 51_AGENT_REGISTRY.json
[ ] Document integration
```

---

## 11. FILE STRUCTURE

```
codexa.app/
├── agentes/
│   └── scout_agent/           # NEW
│       ├── PRIME.md
│       ├── README.md
│       ├── INSTRUCTIONS.md
│       ├── SETUP.md
│       ├── config/
│       │   ├── categories.json
│       │   ├── ignore_patterns.json
│       │   └── relevance_weights.json
│       └── iso_vectorstore/
│           ├── 01_QUICK_START.md
│           └── ...
│
├── mcp-servers/
│   └── scout-mcp/             # NEW - MCP Server
│       ├── package.json
│       ├── tsconfig.json
│       ├── src/
│       │   ├── index.ts       # MCP entry point
│       │   ├── tools/
│       │   │   ├── discover.ts
│       │   │   ├── search.ts
│       │   │   ├── agent_context.ts
│       │   │   ├── crud.ts
│       │   │   └── watch.ts
│       │   ├── indexer/
│       │   │   ├── build.ts
│       │   │   ├── refresh.ts
│       │   │   └── categories.ts
│       │   └── utils/
│       │       ├── relevance.ts
│       │       └── cache.ts
│       └── tests/
│
└── .mcp.json                  # Add scout server config
```

---

## 12. MCP CONFIGURATION

### .mcp.json Addition
```json
{
  "mcpServers": {
    "scout": {
      "command": "node",
      "args": ["codexa.app/mcp-servers/scout-mcp/dist/index.js"],
      "env": {
        "SCOUT_ROOT": "${workspaceFolder}",
        "SCOUT_CACHE_MODE": "session"
      }
    }
  }
}
```

---

## 13. SAFETY CONSIDERATIONS

### CRUD Safety Rules
1. **Backup Before Delete**: Always create .bak before deleting
2. **Validate Paths**: Reject paths outside project root
3. **Confirm Destructive**: Require confirmation for mass operations
4. **Audit Log**: Log all CRUD operations with timestamp
5. **No System Files**: Block operations on .git, node_modules, .venv

### Ignore Patterns (Default)
```json
{
  "ignore_patterns": [
    "node_modules/**",
    ".venv/**",
    "__pycache__/**",
    ".git/**",
    "*.pyc",
    "*.pyo",
    ".DS_Store",
    "Thumbs.db",
    "*.log",
    "*.tmp"
  ]
}
```

---

## 14. SUCCESS METRICS

| Metric | Target | Measurement |
|--------|--------|-------------|
| Index Build Time | <5s for 5000 files | Timer |
| Query Response | <100ms | Timer |
| Relevance Accuracy | >80% top-3 hit rate | Manual evaluation |
| Path Validation | 100% valid paths | Automated test |
| CRUD Success Rate | >99% | Error tracking |

---

## 15. DEPENDENCIES

### Required
- Node.js 18+ (MCP Server)
- TypeScript 5+
- @modelcontextprotocol/sdk

### Optional
- chokidar (file watching)
- fast-glob (file scanning)
- fuse.js (fuzzy search)

---

## 16. MIGRATION FROM mentor_agent

### What Changes
```
mentor_agent v2.5.0 (CURRENT)
├── Discovery-First (Scout Internal) ← REMOVE (→ scout_agent)
├── Knowledge Processing ← KEEP
├── Seller Mentoring ← KEEP
└── FONTES/ External Knowledge ← KEEP

mentor_agent v3.0.0 (AFTER MIGRATION)
├── Knowledge Processing (focus)
├── Seller Mentoring (focus)
├── FONTES/ External Knowledge
└── Uses scout_agent for discovery ← NEW
```

### Migration Steps
1. Create scout_agent (this spec)
2. Update mentor_agent PRIME.md to use Scout
3. Remove Scout Internal code from mentor
4. Update 51_AGENT_REGISTRY.json
5. Test all agents work with Scout

---

## 17. OPEN QUESTIONS

1. **Persistence**: Should index persist to disk or rebuild each session?
   - Recommendation: Start with session cache, add persistence later if needed

2. **Permissions**: Should Scout have write access by default or require explicit enable?
   - Recommendation: Read-only by default, CRUD requires `--enable-crud` flag

3. **Multi-Project**: Should Scout support multiple project roots?
   - Recommendation: Single root for MVP, multi-root for v2.0

---

## APPROVAL CHECKLIST

- [ ] Architecture approved (MCP Server)
- [ ] MVP scope approved (Path Discovery)
- [ ] Data structures approved
- [ ] Integration pattern approved
- [ ] Safety rules approved
- [ ] Migration plan approved

---

**Author**: CODEXA Meta-Constructor
**Created**: 2025-11-28
**Status**: SPEC - Awaiting Approval
**Next Step**: Run in new terminal with `/codexa-build_agent scout_agent`
