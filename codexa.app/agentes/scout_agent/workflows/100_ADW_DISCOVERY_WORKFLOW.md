# ADW-100: Discovery Workflow | Scout Agent

> **Version**: 1.0.0 | **Agent**: scout_agent | **Type**: Agentic Developer Workflow

---

## IDENTITY

**Purpose**: Intelligent codebase discovery and file categorization
**Domain**: File indexing, categorization, and navigation
**Output**: Structured file index, category mappings, relevance scores

---

## TRIGGER

```yaml
triggers:
  - command: /scout-discover
  - command: /scout-index
  - command: /scout-stats
  - event: on_startup (MCP server init)
  - event: file_change (watch mode)
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "ADW-100",
  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "discovery"},
    {"phase_id": "phase_1_scan", "phase_name": "Scan", "duration": "10sec"},
    {"phase_id": "phase_2_categorize", "phase_name": "Categorize", "duration": "5sec"},
    {"phase_id": "phase_3_score", "phase_name": "Score", "duration": "2sec"},
    {"phase_id": "phase_4_index", "phase_name": "Index", "duration": "3sec"},
    {"phase_id": "phase_5_serve", "phase_name": "Serve", "duration": "ongoing"}
  ]
}
```

---

## WORKFLOW PHASES

### Phase 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `discovery`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

### Phase 1: SCAN (10 sec)

```yaml
phase: scan
objective: Recursively scan codebase
actions:
  - Read ignore_patterns.json
  - Walk directory tree
  - Filter out ignored paths
  - Collect file metadata (size, mtime)

outputs:
  - file_list: Array of discovered files
  - total_files: Count
  - scan_time: Duration
```

### Phase 2: CATEGORIZE (5 sec)

```yaml
phase: categorize
objective: Assign categories to each file
actions:
  - Load categories.json (33 categories)
  - For each file:
    - Match by extension
    - Match by path pattern
    - Match by filename pattern
    - Assign primary category

outputs:
  - categorized_files: Files with categories
  - category_counts: Stats per category
```

**Categories**: prompt, config, prime, output, code, test, docs, template, workflow, etc.

### Phase 3: SCORE (2 sec)

```yaml
phase: score
objective: Calculate relevance scores
actions:
  - Load relevance_weights.json
  - Apply boost rules:
    - is_command: +0.3
    - is_prompt: +0.3
    - is_config: +0.2
    - is_output: -0.2
    - parent_is_agent: +0.5
    - contains_todo: +0.1

outputs:
  - scored_files: Files with relevance scores
  - high_priority: Files with score > 0.7
```

### Phase 4: INDEX (3 sec)

```yaml
phase: index
objective: Build searchable index
actions:
  - Create in-memory index
  - Map: path -> metadata
  - Map: category -> paths
  - Map: agent -> files

outputs:
  - index: Searchable data structure
  - stats: Summary statistics
```

### Phase 5: SERVE

```yaml
phase: serve
objective: Expose MCP tools
tools:
  - discover: Fuzzy file search
  - search: Glob pattern search
  - get_file_summary: File metadata
  - agent_context: Agent file collection
  - stats: Index statistics
```

---

## EXECUTION MODES

### Full Index

```javascript
mcp__scout__discover("rebuild index")
```

Rebuilds entire index from scratch.

### Quick Stats

```javascript
mcp__scout__stats()
```

Returns current index statistics.

### Agent Context

```javascript
mcp__scout__agent_context("anuncio_agent")
```

Returns all files for specific agent.

### Pattern Search

```javascript
mcp__scout__search("**/iso_vectorstore/*.md")
```

Returns files matching glob pattern.

---

## QUALITY GATES

```yaml
quality_gates:
  index_health:
    - total_files > 0
    - other_category < 30% (ideally)
    - all agents indexed

  performance:
    - scan_time < 10s
    - query_time < 100ms
```

---

## CONFIGURATION FILES

| File | Purpose |
|------|---------|
| config/categories.json | 33 category definitions |
| config/ignore_patterns.json | Paths to skip |
| config/relevance_weights.json | Scoring boost rules |

---

## OUTPUT FORMAT

### Stats Response

```json
{
  "total_files": 11849,
  "categories": {
    "code": 3245,
    "prompt": 156,
    "config": 423,
    "output": 1892,
    "other": 4133
  },
  "agents": {
    "anuncio_agent": 89,
    "codexa_agent": 127,
    ...
  },
  "last_indexed": "2025-11-30T10:00:00Z"
}
```

### Discover Response

```json
{
  "matches": [
    {
      "path": "agentes/anuncio_agent/PRIME.md",
      "category": "prime",
      "relevance": 0.95,
      "agent": "anuncio_agent"
    }
  ],
  "query": "anuncio prime",
  "count": 1
}
```

---

## INTEGRATION

**Upstream**: File system changes
**Downstream**: All agents (use scout for discovery)

---

**Created by**: scout_agent v1.0.0
**Last Updated**: 2025-11-30
