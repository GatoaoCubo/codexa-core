# SPEC: Scout Knowledge Router v2.0.0

## Executive Summary

**Problem**: Scout MCP v1.2.0 can find files by pattern and agent, but lacks cross-agent knowledge routing. When building a subagent, codexa_agent needs prompt engineering patterns from mentor_agent. When creating an anuncio, anuncio_agent needs e-commerce knowledge from mentor_agent/FONTES. Current workaround: manual file discovery or blind guessing.

**Solution**: Enhance Scout with knowledge routing using `knowledge_graph.json` as navigation map. Scout becomes an intelligent router that:
1. Detects task types from queries ("create subagent" → needs prompt_engineering knowledge)
2. Routes queries to prerequisite knowledge across agents
3. Returns not just agent files, but required + recommended knowledge for task success

**Scope**:
- ADD 3 new MCP tools: `get_task_prerequisites`, `discover_knowledge`, `embed_and_search` (Phase 3)
- ENHANCE existing `discover()` to use knowledge graph
- ENHANCE existing `smart_context()` to include cross-agent deps
- LOAD `knowledge_graph.json` at startup, cache in memory

**Impact**:
- Before: "Find files for codexa_agent" → returns 240 files (overwhelming)
- After: "Create subagent" → returns 5 required + 3 recommended knowledge files (actionable)

---

## 1. IDENTITY

| Field | Value |
|-------|-------|
| **Spec Version** | 2.0.0 |
| **Scout Version** | 1.2.0 → 2.0.0 |
| **Type** | Enhancement - Knowledge Routing |
| **Architecture** | MCP Server (Node.js) |
| **New Dependencies** | None (uses existing index) |

**Transform**:
- Input: Task type ("create_subagent") OR natural language query ("criar um agente")
- Output: Required knowledge files + recommended knowledge files + confidence scores

---

## 2. KNOWLEDGE GRAPH STRUCTURE

### 2.1 Source File: knowledge_graph.json

Located at: `codexa.app/agentes/mentor_agent/FONTES/knowledge_graph.json`

**Structure**:
```typescript
interface KnowledgeGraph {
  version: string;
  description: string;
  created: string;
  last_updated: string;

  // Task type definitions
  task_types: Record<string, TaskType>;

  // Knowledge category definitions
  knowledge_categories: Record<string, KnowledgeCategory>;

  // Cross-agent dependencies
  cross_references: Record<string, AgentDependency>;

  // Auto-injection rules
  auto_inject_rules: AutoInjectRule[];
}

interface TaskType {
  description: string;
  primary_agent: string;
  required_knowledge: string[];  // Absolute paths
  recommended_knowledge: string[];  // Absolute paths
  triggers: string[];  // Keywords/phrases that match this task
  estimated_tokens: number;  // Token budget hint
}

interface KnowledgeCategory {
  description: string;
  source_agent: string;  // Where this knowledge lives
  base_path: string;  // Base directory
  files: string[];  // Relative paths from base_path
  consumers: string[];  // Which agents need this
  tags: string[];  // For search/discovery
}

interface AgentDependency {
  depends_on: string[];  // Other agents this agent needs
  knowledge_needed: string[];  // Categories from knowledge_categories
}

interface AutoInjectRule {
  condition: string;  // Simple expression (can be enhanced later)
  inject: string;  // Category or specific files
  priority: "required" | "recommended";
}
```

### 2.2 Example Data (from current knowledge_graph.json)

```json
{
  "task_types": {
    "create_subagent": {
      "description": "Criar subagent type para Claude Code",
      "primary_agent": "codexa_agent",
      "required_knowledge": [
        "codexa.app/agentes/codexa_agent/iso_vectorstore/23_subagent_patterns.md",
        "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/playbook_prompt_engineering_20251201.md"
      ],
      "recommended_knowledge": [
        "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_tool_calling_20251201.md"
      ],
      "triggers": ["subagent", "criar agente", "build agent", "Task tool"],
      "estimated_tokens": 15000
    }
  },

  "knowledge_categories": {
    "prompt_engineering": {
      "description": "Padroes e melhores praticas de prompt engineering",
      "source_agent": "mentor_agent",
      "base_path": "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/",
      "files": [
        "patterns/pattern_tool_calling_20251201.md",
        "playbook_prompt_engineering_20251201.md"
      ],
      "consumers": ["codexa_agent", "ALL"],
      "tags": ["prompt", "subagent", "HOP"]
    }
  }
}
```

---

## 3. NEW MCP TOOLS

### 3.1 Tool: get_task_prerequisites

**Purpose**: Given a task type, return all required and recommended knowledge files.

**Input Schema**:
```typescript
interface GetTaskPrerequisitesParams {
  task_type: string;  // e.g., "create_subagent", "create_anuncio"
  include_recommended?: boolean;  // Default: true
}
```

**Output Schema**:
```typescript
interface TaskPrerequisitesResponse {
  task_type: string;
  description: string;
  primary_agent: string;
  required_knowledge: KnowledgeFile[];
  recommended_knowledge?: KnowledgeFile[];
  estimated_tokens: number;
  status: "complete" | "partial" | "missing";
  missing_files?: string[];  // Files in graph but not in index
}

interface KnowledgeFile {
  path: string;
  exists: boolean;
  category: string;
  agent: string;
  size?: number;
  importance: number;  // From CATEGORIES importance
  reason: string;  // Why this file is needed
}
```

**Example Call**:
```javascript
mcp__scout__get_task_prerequisites({
  task_type: "create_subagent",
  include_recommended: true
})
```

**Example Response**:
```json
{
  "task_type": "create_subagent",
  "description": "Criar subagent type para Claude Code",
  "primary_agent": "codexa_agent",
  "required_knowledge": [
    {
      "path": "codexa.app/agentes/codexa_agent/iso_vectorstore/23_subagent_patterns.md",
      "exists": true,
      "category": "iso_vectorstore",
      "agent": "codexa_agent",
      "size": 15420,
      "importance": 65,
      "reason": "Core patterns for subagent construction"
    },
    {
      "path": "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/playbook_prompt_engineering_20251201.md",
      "exists": true,
      "category": "fontes",
      "agent": "mentor_agent",
      "size": 42350,
      "importance": 40,
      "reason": "Prompt engineering best practices"
    }
  ],
  "recommended_knowledge": [
    {
      "path": "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_tool_calling_20251201.md",
      "exists": true,
      "category": "fontes",
      "agent": "mentor_agent",
      "size": 18920,
      "importance": 40,
      "reason": "Tool calling patterns for subagents"
    }
  ],
  "estimated_tokens": 15000,
  "status": "complete",
  "missing_files": []
}
```

**Implementation Notes**:
1. Load knowledge_graph.json at server startup (cache in memory)
2. Validate that all files in knowledge graph exist in file index
3. For each file, lookup metadata from existing file index
4. Mark status as "partial" if some files missing, "missing" if all missing

---

### 3.2 Tool: discover_knowledge

**Purpose**: Natural language query → task type detection → knowledge routing

**Input Schema**:
```typescript
interface DiscoverKnowledgeParams {
  query: string;  // Natural language: "preciso criar um subagente"
  include_cross_agent?: boolean;  // Include knowledge from other agents (default: true)
  max_results?: number;  // Limit results (default: 15)
}
```

**Output Schema**:
```typescript
interface DiscoverKnowledgeResponse {
  query: string;
  detected_task_type: string | null;
  confidence: number;  // 0.0 - 1.0
  matched_triggers: string[];  // Which trigger words matched

  // If task type detected
  task_prerequisites?: TaskPrerequisitesResponse;

  // Always included: files from regular discover
  relevant_files: RelevantFile[];

  // Cross-agent knowledge
  cross_agent_knowledge?: CrossAgentKnowledge[];

  total_knowledge_files: number;
  total_agent_files: number;
  search_time_ms: number;
}

interface CrossAgentKnowledge {
  source_agent: string;
  category: string;
  files: KnowledgeFile[];
  reason: string;  // Why this knowledge is relevant
}
```

**Example Call**:
```javascript
mcp__scout__discover_knowledge({
  query: "preciso criar um subagente para processar imagens",
  include_cross_agent: true,
  max_results: 15
})
```

**Example Response**:
```json
{
  "query": "preciso criar um subagente para processar imagens",
  "detected_task_type": "create_subagent",
  "confidence": 0.92,
  "matched_triggers": ["subagente", "criar"],

  "task_prerequisites": {
    "task_type": "create_subagent",
    "required_knowledge": [...],
    "recommended_knowledge": [...]
  },

  "relevant_files": [
    {
      "path": "codexa.app/agentes/codexa_agent/PRIME.md",
      "relevance_score": 0.95,
      "category": "prime",
      "agent": "codexa_agent"
    }
  ],

  "cross_agent_knowledge": [
    {
      "source_agent": "mentor_agent",
      "category": "prompt_engineering",
      "files": [
        {
          "path": "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/playbook_prompt_engineering_20251201.md",
          "exists": true,
          "reason": "Required for subagent creation"
        }
      ],
      "reason": "Prompt engineering patterns needed for subagent construction"
    }
  ],

  "total_knowledge_files": 5,
  "total_agent_files": 10,
  "search_time_ms": 78
}
```

**Implementation Logic**:
```javascript
async function discoverKnowledge(query, includeCrossAgent = true, maxResults = 15) {
  // 1. Detect task type from query
  const taskMatch = detectTaskTypeFromQuery(query);

  // 2. If task type detected, get prerequisites
  let prerequisites = null;
  if (taskMatch) {
    prerequisites = await getTaskPrerequisites(taskMatch.task_type, true);
  }

  // 3. Run regular discover for agent files
  const agentFiles = await toolDiscover(query, null, maxResults);

  // 4. If cross-agent enabled, get knowledge from other agents
  let crossAgentKnowledge = [];
  if (includeCrossAgent && taskMatch) {
    crossAgentKnowledge = await getCrossAgentKnowledge(taskMatch.task_type);
  }

  // 5. Merge and return
  return {
    query,
    detected_task_type: taskMatch?.task_type || null,
    confidence: taskMatch?.confidence || 0,
    matched_triggers: taskMatch?.triggers || [],
    task_prerequisites: prerequisites,
    relevant_files: agentFiles.relevant_files,
    cross_agent_knowledge: crossAgentKnowledge,
    total_knowledge_files: crossAgentKnowledge.reduce((sum, cat) => sum + cat.files.length, 0),
    total_agent_files: agentFiles.relevant_files.length,
    search_time_ms: Date.now() - startTime
  };
}
```

---

### 3.3 Tool: embed_and_search (Phase 3 - Semantic Search)

**Purpose**: Semantic similarity search using embeddings (future enhancement)

**Input Schema**:
```typescript
interface EmbedSearchParams {
  query: string;  // Natural language query
  top_k?: number;  // Return top K results (default: 10)
  filter_agents?: string[];  // Limit to specific agents
  filter_categories?: string[];  // Limit to specific categories
  threshold?: number;  // Similarity threshold 0.0-1.0 (default: 0.7)
}
```

**Output Schema**:
```typescript
interface EmbedSearchResponse {
  query: string;
  query_embedding: number[];  // Vector (for debugging)
  results: SemanticResult[];
  total_found: number;
  search_time_ms: number;
}

interface SemanticResult {
  path: string;
  similarity_score: number;  // Cosine similarity
  category: string;
  agent: string;
  excerpt?: string;  // Relevant text snippet
}
```

**Implementation Notes (Phase 3)**:
1. **Pre-compute embeddings**: Run embedding generation for all markdown/text files at index build time
2. **Store embeddings**: Add `embedding: number[]` field to FileEntry
3. **Query embedding**: Generate embedding for query at search time
4. **Cosine similarity**: Compare query embedding with all file embeddings
5. **Return top K**: Sort by similarity, return top K results

**Recommended Embedding Model**:
- Option A: `text-embedding-3-small` (OpenAI) - 1536 dims, fast, cheap
- Option B: `all-MiniLM-L6-v2` (local) - 384 dims, free, privacy
- Option C: `voyage-code-2` (Voyage AI) - 1536 dims, optimized for code

**Why Phase 3?**
- Phase 1-2 use keyword matching + knowledge graph (fast, deterministic)
- Embeddings add latency (~50-100ms per query) and complexity
- Only add if keyword matching proves insufficient

---

## 4. ENHANCED EXISTING TOOLS

### 4.1 Enhance: discover()

**Current Behavior**: Keyword matching + semantic aliases + category scoring

**New Behavior**: ADD knowledge graph detection

```typescript
// Before (v1.2.0)
async function toolDiscover(query, agent, maxResults) {
  const detectedAgent = detectAgentFromQuery(query);
  const expandedTerms = expandQuery(query);
  // ... existing scoring logic
}

// After (v2.0.0)
async function toolDiscover(query, agent, maxResults) {
  // 1. Existing detection
  const detectedAgent = detectAgentFromQuery(query);
  const expandedTerms = expandQuery(query);

  // 2. NEW: Task type detection
  const taskMatch = detectTaskTypeFromQuery(query);

  // 3. NEW: If task detected, boost prerequisite files
  let knowledgeBoost = {};
  if (taskMatch) {
    const prereqs = await getTaskPrerequisites(taskMatch.task_type, true);
    for (const file of prereqs.required_knowledge) {
      knowledgeBoost[file.path] = 0.3;  // +0.3 relevance boost
    }
    for (const file of prereqs.recommended_knowledge || []) {
      knowledgeBoost[file.path] = 0.15;  // +0.15 relevance boost
    }
  }

  // 4. Apply boost during scoring
  for (const entry of fileIndex.values()) {
    let score = calculateRelevance(query, entry, effectiveAgent);
    if (knowledgeBoost[entry.relativePath]) {
      score = Math.min(1.0, score + knowledgeBoost[entry.relativePath]);
    }
    // ... rest of scoring
  }
}
```

**Benefits**:
- Zero API changes (backward compatible)
- Automatically surfaces knowledge files when task detected
- Users get better results without learning new tools

---

### 4.2 Enhance: smart_context()

**Current Behavior**: Returns files for a single agent

**New Behavior**: ADD cross-agent dependencies

```typescript
// Before (v1.2.0)
async function toolSmartContext(agentName, maxFiles, includeHints) {
  // Returns only files belonging to agentName
}

// After (v2.0.0)
async function toolSmartContext(agentName, maxFiles, includeHints, includeDeps = false) {
  // 1. Get agent's own files (existing logic)
  const agentFiles = [...]; // existing code

  // 2. NEW: Get cross-agent dependencies
  let dependencies = null;
  if (includeDeps && KNOWLEDGE_GRAPH.cross_references[agentName]) {
    dependencies = KNOWLEDGE_GRAPH.cross_references[agentName];

    // Load knowledge files from dependencies
    const knowledgeFiles = [];
    for (const category of dependencies.knowledge_needed) {
      const categoryDef = KNOWLEDGE_GRAPH.knowledge_categories[category];
      if (categoryDef) {
        for (const relPath of categoryDef.files) {
          const fullPath = path.join(categoryDef.base_path, relPath);
          const entry = fileIndex.get(fullPath);
          if (entry) {
            knowledgeFiles.push({
              path: entry.relativePath,
              category: entry.category,
              source_agent: categoryDef.source_agent,
              reason: `${category} knowledge`
            });
          }
        }
      }
    }
  }

  return {
    agent: agentName,
    entry_points: {...},
    must_read: [...],
    dependencies: dependencies,
    knowledge_files: knowledgeFiles || [],  // NEW
    // ... rest of response
  };
}
```

**API Change**:
```typescript
// New parameter (optional, default false for backward compat)
mcp__scout__smart_context({
  agent: "codexa_agent",
  max_files: 20,
  include_hints: true,
  include_deps: true  // NEW
})
```

**Example Enhanced Response**:
```json
{
  "agent": "codexa_agent",
  "must_read": [...],
  "knowledge_files": [
    {
      "path": "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/playbook_prompt_engineering_20251201.md",
      "category": "fontes",
      "source_agent": "mentor_agent",
      "reason": "prompt_engineering knowledge"
    }
  ],
  "dependencies": {
    "depends_on": ["mentor_agent"],
    "knowledge_needed": ["prompt_engineering", "quality_standards"]
  }
}
```

---

## 5. KNOWLEDGE GRAPH LOADING

### 5.1 Startup Sequence

```javascript
// In main() function, after buildIndex()
let KNOWLEDGE_GRAPH = null;

async function loadKnowledgeGraph() {
  const graphPath = path.join(PROJECT_ROOT, 'codexa.app/agentes/mentor_agent/FONTES/knowledge_graph.json');

  try {
    const content = await fs.readFile(graphPath, 'utf-8');
    KNOWLEDGE_GRAPH = JSON.parse(content);

    // Validate graph structure
    validateKnowledgeGraph(KNOWLEDGE_GRAPH);

    // Build lookup indices for fast access
    buildTaskTypeLookup(KNOWLEDGE_GRAPH);

    log('info', 'Knowledge graph loaded', {
      task_types: Object.keys(KNOWLEDGE_GRAPH.task_types).length,
      categories: Object.keys(KNOWLEDGE_GRAPH.knowledge_categories).length,
      agents: Object.keys(KNOWLEDGE_GRAPH.cross_references).length
    });

  } catch (error) {
    log('warn', 'Could not load knowledge graph', { error: error.message });
    // Fallback: create empty graph
    KNOWLEDGE_GRAPH = {
      task_types: {},
      knowledge_categories: {},
      cross_references: {},
      auto_inject_rules: []
    };
  }
}

function validateKnowledgeGraph(graph) {
  // Check required fields
  if (!graph.task_types || !graph.knowledge_categories) {
    throw new Error('Invalid knowledge graph: missing required fields');
  }

  // Validate file paths exist
  for (const [taskType, def] of Object.entries(graph.task_types)) {
    for (const filePath of [...def.required_knowledge, ...def.recommended_knowledge]) {
      const entry = fileIndex.get(filePath);
      if (!entry) {
        log('warn', `Knowledge graph references missing file: ${filePath} (task: ${taskType})`);
      }
    }
  }
}

// Build reverse lookup: trigger keyword → task types
let TRIGGER_LOOKUP = new Map();

function buildTaskTypeLookup(graph) {
  TRIGGER_LOOKUP.clear();

  for (const [taskType, def] of Object.entries(graph.task_types)) {
    for (const trigger of def.triggers) {
      const normalized = trigger.toLowerCase().trim();
      if (!TRIGGER_LOOKUP.has(normalized)) {
        TRIGGER_LOOKUP.set(normalized, []);
      }
      TRIGGER_LOOKUP.get(normalized).push(taskType);
    }
  }

  log('debug', 'Task type lookup built', {
    unique_triggers: TRIGGER_LOOKUP.size
  });
}
```

### 5.2 Task Type Detection Algorithm

```javascript
function detectTaskTypeFromQuery(query) {
  if (!KNOWLEDGE_GRAPH || !KNOWLEDGE_GRAPH.task_types) {
    return null;
  }

  const queryLower = query.toLowerCase();
  let bestMatch = null;
  let bestScore = 0;
  let matchedTriggers = [];

  // Check each task type
  for (const [taskType, def] of Object.entries(KNOWLEDGE_GRAPH.task_types)) {
    let score = 0;
    let localMatches = [];

    // Check if any trigger appears in query
    for (const trigger of def.triggers) {
      const triggerLower = trigger.toLowerCase();
      if (queryLower.includes(triggerLower)) {
        // Score based on trigger length (longer = more specific)
        const triggerScore = triggerLower.length / queryLower.length;
        score += triggerScore;
        localMatches.push(trigger);
      }
    }

    // Update best match if this task type scored higher
    if (score > bestScore) {
      bestScore = score;
      bestMatch = taskType;
      matchedTriggers = localMatches;
    }
  }

  // Require minimum confidence threshold
  const confidence = Math.min(1.0, bestScore * 2);  // Normalize to 0-1

  if (confidence >= 0.5) {
    return {
      task_type: bestMatch,
      confidence: confidence,
      triggers: matchedTriggers
    };
  }

  return null;
}
```

---

## 6. INTEGRATION EXAMPLES

### 6.1 Example: Building a Subagent

**User Query**: "Preciso criar um subagente para validar documentos"

**Scout Call**:
```javascript
mcp__scout__discover_knowledge({
  query: "Preciso criar um subagente para validar documentos",
  include_cross_agent: true
})
```

**Scout Response**:
```json
{
  "detected_task_type": "create_subagent",
  "confidence": 0.88,
  "matched_triggers": ["subagente", "criar"],

  "task_prerequisites": {
    "required_knowledge": [
      {
        "path": "codexa.app/agentes/codexa_agent/iso_vectorstore/23_subagent_patterns.md",
        "reason": "Core subagent construction patterns"
      },
      {
        "path": "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/playbook_prompt_engineering_20251201.md",
        "reason": "Prompt engineering fundamentals"
      }
    ],
    "recommended_knowledge": [
      {
        "path": "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_tool_calling_20251201.md",
        "reason": "Tool calling patterns for subagents"
      }
    ],
    "estimated_tokens": 15000
  },

  "relevant_files": [
    {
      "path": "codexa.app/agentes/codexa_agent/PRIME.md",
      "relevance_score": 0.93
    }
  ],

  "cross_agent_knowledge": [
    {
      "source_agent": "mentor_agent",
      "category": "prompt_engineering",
      "files": [...]
    }
  ]
}
```

**LLM Next Steps**:
1. Read required_knowledge files (2 files, ~15k tokens)
2. Read codexa_agent PRIME.md for context
3. Apply patterns from prompt engineering playbook
4. Generate subagent with tool calling patterns

---

### 6.2 Example: Creating an Anuncio

**User Query**: "criar anuncio para caixa de transporte pet"

**Scout Call**:
```javascript
mcp__scout__discover_knowledge({
  query: "criar anuncio para caixa de transporte pet",
  include_cross_agent: true
})
```

**Scout Response**:
```json
{
  "detected_task_type": "create_anuncio",
  "confidence": 0.94,

  "task_prerequisites": {
    "required_knowledge": [
      {
        "path": "codexa.app/agentes/anuncio_agent/PRIME.md",
        "reason": "Entry point for ad creation"
      }
    ],
    "recommended_knowledge": [
      {
        "path": "codexa.app/agentes/mentor_agent/FONTES/ECOMMERCE/README.md",
        "reason": "E-commerce best practices"
      }
    ]
  },

  "relevant_files": [
    {
      "path": "codexa.app/agentes/anuncio_agent/prompts/14_title_HOP.md",
      "relevance_score": 0.89
    }
  ]
}
```

---

## 7. IMPLEMENTATION PLAN

### Phase 1: Core Knowledge Routing (MVP) - 2-3 days

```
[ ] Load knowledge_graph.json at startup
[ ] Implement validateKnowledgeGraph()
[ ] Implement buildTaskTypeLookup()
[ ] Implement detectTaskTypeFromQuery()
[ ] Implement get_task_prerequisites tool
[ ] Add to ListToolsRequestSchema
[ ] Add to CallToolRequestSchema handler
[ ] Test with existing knowledge_graph.json
```

### Phase 2: Enhanced Discovery - 1-2 days

```
[ ] Implement discover_knowledge tool
[ ] Integrate task detection into existing discover()
[ ] Implement getCrossAgentKnowledge()
[ ] Add knowledge boost to relevance scoring
[ ] Enhance smart_context with include_deps parameter
[ ] Update tool descriptions in MCP server
[ ] Test cross-agent knowledge routing
```

### Phase 3: Semantic Search (Optional) - 3-5 days

```
[ ] Choose embedding model (recommend: text-embedding-3-small)
[ ] Add embedding generation to buildIndex()
[ ] Store embeddings in FileEntry
[ ] Implement embed_and_search tool
[ ] Add cosine similarity calculation
[ ] Benchmark: keyword vs semantic vs hybrid
[ ] Decide on default search strategy
```

### Phase 4: Integration & Testing - 1 day

```
[ ] Update PRIME.md with new tools
[ ] Update INSTRUCTIONS.md with examples
[ ] Add knowledge_graph.json validation to refresh()
[ ] Document knowledge graph schema
[ ] Create example queries for each task type
[ ] Update version to 2.0.0
```

---

## 8. FILE CHANGES

### 8.1 New Files

```
codexa.app/agentes/scout_agent/specs/
└── SCOUT_KNOWLEDGE_ROUTER_SPEC.md  ← THIS FILE

mcp-servers/scout-mcp/
└── src/
    ├── knowledge_graph_loader.js  ← NEW
    └── task_detection.js  ← NEW
```

### 8.2 Modified Files

```
mcp-servers/scout-mcp/index.js
  ← Add loadKnowledgeGraph() in main()
  ← Add get_task_prerequisites tool
  ← Add discover_knowledge tool
  ← Enhance toolDiscover() with knowledge boost
  ← Enhance toolSmartContext() with include_deps

codexa.app/agentes/scout_agent/PRIME.md
  ← Document new tools
  ← Add examples for knowledge routing

codexa.app/agentes/scout_agent/INSTRUCTIONS.md
  ← Add guidance for using knowledge routing
```

---

## 9. API SPECIFICATIONS

### 9.1 MCP Tool Definitions (ListToolsRequestSchema)

```javascript
{
  name: 'get_task_prerequisites',
  description: 'Get required and recommended knowledge files for a task type. Uses knowledge_graph.json to route cross-agent knowledge.',
  inputSchema: {
    type: 'object',
    properties: {
      task_type: {
        type: 'string',
        description: 'Task type identifier (e.g., "create_subagent", "create_anuncio")'
      },
      include_recommended: {
        type: 'boolean',
        default: true,
        description: 'Include recommended (optional) knowledge files'
      }
    },
    required: ['task_type']
  }
},

{
  name: 'discover_knowledge',
  description: 'Natural language query with task detection and cross-agent knowledge routing. Combines regular file discovery with prerequisite knowledge files.',
  inputSchema: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description: 'Natural language query (e.g., "preciso criar um subagente")'
      },
      include_cross_agent: {
        type: 'boolean',
        default: true,
        description: 'Include knowledge from other agents'
      },
      max_results: {
        type: 'integer',
        default: 15,
        description: 'Maximum total results to return'
      }
    },
    required: ['query']
  }
},

{
  name: 'embed_and_search',
  description: '[Phase 3] Semantic similarity search using embeddings. More accurate than keyword matching but slower.',
  inputSchema: {
    type: 'object',
    properties: {
      query: {
        type: 'string',
        description: 'Natural language query'
      },
      top_k: {
        type: 'integer',
        default: 10,
        description: 'Return top K most similar results'
      },
      filter_agents: {
        type: 'array',
        items: { type: 'string' },
        description: 'Optional: limit to specific agents'
      },
      threshold: {
        type: 'number',
        default: 0.7,
        description: 'Similarity threshold (0.0-1.0)'
      }
    },
    required: ['query']
  }
}
```

---

## 10. KNOWLEDGE GRAPH SCHEMA (TypeScript)

```typescript
// Full schema for knowledge_graph.json
export interface KnowledgeGraph {
  version: string;
  description: string;
  created: string;  // ISO date
  last_updated: string;  // ISO date

  task_types: Record<string, TaskType>;
  knowledge_categories: Record<string, KnowledgeCategory>;
  cross_references: Record<string, AgentDependency>;
  auto_inject_rules: AutoInjectRule[];
}

export interface TaskType {
  description: string;  // Human-readable description
  primary_agent: string;  // Agent that handles this task
  required_knowledge: string[];  // Absolute paths to required files
  recommended_knowledge: string[];  // Absolute paths to recommended files
  triggers: string[];  // Keywords/phrases that match this task
  estimated_tokens: number;  // Token budget for this task
}

export interface KnowledgeCategory {
  description: string;  // What this category contains
  source_agent: string;  // Agent that owns this knowledge
  base_path: string;  // Base directory (absolute or relative to PROJECT_ROOT)
  files: string[];  // File paths relative to base_path
  consumers: string[];  // Agents that need this knowledge (or ["ALL"])
  tags: string[];  // Tags for discovery
}

export interface AgentDependency {
  depends_on: string[];  // Other agents this agent depends on
  knowledge_needed: string[];  // Categories from knowledge_categories
}

export interface AutoInjectRule {
  condition: string;  // Simple expression (e.g., "task_type == 'create_subagent'")
  inject: string;  // Category name or file path to inject
  priority: "required" | "recommended";
}

// Example validation function
export function validateKnowledgeGraph(graph: any): KnowledgeGraph {
  if (!graph.version || !graph.task_types || !graph.knowledge_categories) {
    throw new Error('Invalid knowledge graph structure');
  }

  // Validate task_types
  for (const [taskType, def] of Object.entries(graph.task_types)) {
    if (!def.primary_agent || !Array.isArray(def.triggers)) {
      throw new Error(`Invalid task_type: ${taskType}`);
    }
  }

  // Validate knowledge_categories
  for (const [category, def] of Object.entries(graph.knowledge_categories)) {
    if (!def.source_agent || !def.base_path) {
      throw new Error(`Invalid knowledge_category: ${category}`);
    }
  }

  return graph as KnowledgeGraph;
}
```

---

## 11. TESTING STRATEGY

### 11.1 Unit Tests

```javascript
// Test task type detection
describe('detectTaskTypeFromQuery', () => {
  test('detects create_subagent from Portuguese query', () => {
    const result = detectTaskTypeFromQuery('preciso criar um subagente');
    expect(result.task_type).toBe('create_subagent');
    expect(result.confidence).toBeGreaterThan(0.7);
  });

  test('detects create_anuncio from keywords', () => {
    const result = detectTaskTypeFromQuery('criar anuncio produto');
    expect(result.task_type).toBe('create_anuncio');
  });

  test('returns null for non-matching query', () => {
    const result = detectTaskTypeFromQuery('hello world');
    expect(result).toBeNull();
  });
});

// Test knowledge graph loading
describe('loadKnowledgeGraph', () => {
  test('loads and validates graph successfully', async () => {
    await loadKnowledgeGraph();
    expect(KNOWLEDGE_GRAPH).toBeDefined();
    expect(KNOWLEDGE_GRAPH.task_types).toBeDefined();
  });

  test('validates all file paths exist', async () => {
    const missing = [];
    for (const [taskType, def] of Object.entries(KNOWLEDGE_GRAPH.task_types)) {
      for (const filePath of def.required_knowledge) {
        if (!fileIndex.has(filePath)) {
          missing.push({ taskType, filePath });
        }
      }
    }
    expect(missing.length).toBe(0);
  });
});
```

### 11.2 Integration Tests

```javascript
// Test get_task_prerequisites
test('get_task_prerequisites returns complete data', async () => {
  const result = await toolGetTaskPrerequisites('create_subagent', true);

  expect(result.task_type).toBe('create_subagent');
  expect(result.required_knowledge.length).toBeGreaterThan(0);
  expect(result.status).toBe('complete');
  expect(result.missing_files).toHaveLength(0);

  // All files should exist
  for (const file of result.required_knowledge) {
    expect(file.exists).toBe(true);
  }
});

// Test discover_knowledge
test('discover_knowledge detects task and returns knowledge', async () => {
  const result = await toolDiscoverKnowledge('criar subagente', true, 15);

  expect(result.detected_task_type).toBe('create_subagent');
  expect(result.confidence).toBeGreaterThan(0.5);
  expect(result.task_prerequisites).toBeDefined();
  expect(result.cross_agent_knowledge.length).toBeGreaterThan(0);
});
```

---

## 12. PERFORMANCE CONSIDERATIONS

### 12.1 Caching Strategy

```javascript
// Cache loaded knowledge graph in memory
let KNOWLEDGE_GRAPH = null;
let KNOWLEDGE_GRAPH_LOADED_AT = null;

// Cache task detection results (LRU cache)
const TASK_DETECTION_CACHE = new Map();
const MAX_CACHE_SIZE = 100;

function detectTaskTypeFromQueryCached(query) {
  const cacheKey = query.toLowerCase().trim();

  if (TASK_DETECTION_CACHE.has(cacheKey)) {
    return TASK_DETECTION_CACHE.get(cacheKey);
  }

  const result = detectTaskTypeFromQuery(query);

  // Add to cache (with LRU eviction)
  if (TASK_DETECTION_CACHE.size >= MAX_CACHE_SIZE) {
    const firstKey = TASK_DETECTION_CACHE.keys().next().value;
    TASK_DETECTION_CACHE.delete(firstKey);
  }
  TASK_DETECTION_CACHE.set(cacheKey, result);

  return result;
}
```

### 12.2 Performance Targets

| Operation | Target | Measurement |
|-----------|--------|-------------|
| Load knowledge_graph.json | <50ms | Startup time |
| detectTaskTypeFromQuery | <10ms | Query detection |
| get_task_prerequisites | <50ms | File lookup |
| discover_knowledge | <150ms | Combined operation |
| embed_and_search (Phase 3) | <200ms | Embedding + similarity |

### 12.3 Token Budget

```javascript
// Estimated token usage per operation
const TOKEN_ESTIMATES = {
  get_task_prerequisites: {
    request: 100,    // Tool call
    response: 1500,  // 5-10 files with metadata
    total: 1600
  },
  discover_knowledge: {
    request: 150,
    response: 3000,  // Task prereqs + agent files + cross-agent
    total: 3150
  },
  embed_and_search: {
    request: 100,
    response: 2000,  // Top K semantic results
    total: 2100
  }
};
```

---

## 13. MIGRATION PATH

### From v1.2.0 to v2.0.0

**Breaking Changes**: None (all new tools are additive)

**Deprecations**: None

**New Features**:
- `get_task_prerequisites` tool
- `discover_knowledge` tool
- `embed_and_search` tool (Phase 3)
- Enhanced `discover()` with knowledge boost
- Enhanced `smart_context()` with `include_deps` parameter

**Migration Steps**:
1. Update Scout MCP server to v2.0.0
2. Ensure `knowledge_graph.json` exists at expected path
3. No changes required to existing code (backward compatible)
4. Optionally update agent code to use new tools

---

## 14. SUCCESS METRICS

| Metric | Before (v1.2.0) | After (v2.0.0) | Target |
|--------|-----------------|----------------|--------|
| **Task Detection Accuracy** | N/A | TBD | >85% |
| **Cross-Agent Knowledge Discovery** | Manual | Automatic | 100% |
| **Files Returned (Precision)** | 50-200 files | 5-15 files | <20 |
| **Token Budget per Query** | ~5k | ~3k | <4k |
| **Query Response Time** | ~50ms | ~150ms | <200ms |

**Validation Method**:
1. Create test suite with 20 representative queries
2. Measure task detection accuracy
3. Measure precision (relevant files / total files)
4. Measure response time
5. User testing with 5 agents (codexa, anuncio, mentor, curso, photo)

---

## 15. OPEN QUESTIONS & DECISIONS

### Q1: Should embeddings be opt-in or default?
**Recommendation**: Opt-in (Phase 3). Start with keyword + knowledge graph (fast, deterministic), add embeddings only if precision is insufficient.

### Q2: Should knowledge_graph.json be editable via MCP?
**Recommendation**: Read-only for v2.0.0. Add editing tools in v2.1.0 if needed.

### Q3: How to handle knowledge_graph.json updates?
**Recommendation**: Auto-reload on `refresh()` call. Hot reload on file change (Phase 2).

### Q4: Should task type detection be case-sensitive?
**Recommendation**: No. Normalize to lowercase for matching.

### Q5: How to handle multiple task types detected?
**Recommendation**: Return highest confidence match. If tie (within 0.1), return both with flag `ambiguous: true`.

---

## APPROVAL CHECKLIST

- [ ] Architecture approved (knowledge graph + MCP tools)
- [ ] API schemas approved (TypeScript interfaces)
- [ ] Tool definitions approved (get_task_prerequisites, discover_knowledge)
- [ ] Integration approach approved (enhance existing tools)
- [ ] Performance targets approved (<200ms query time)
- [ ] Testing strategy approved (unit + integration tests)
- [ ] Migration path approved (backward compatible)
- [ ] Phase 3 (embeddings) approved as optional enhancement

---

**Author**: Claude (Sonnet 4.5) + Meta-Constructor Pattern
**Created**: 2025-12-02
**Status**: SPEC - Ready for Implementation
**Next Step**: Begin Phase 1 implementation
**Estimated Effort**: 4-6 days (Phase 1-2), +3-5 days (Phase 3 if approved)

---

> "Scout knows not just where files are, but what knowledge you need to succeed."
