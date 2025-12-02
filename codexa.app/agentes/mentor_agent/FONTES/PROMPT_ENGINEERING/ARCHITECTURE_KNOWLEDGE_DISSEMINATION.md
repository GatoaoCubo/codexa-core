# Knowledge Dissemination Architecture

**Version**: 1.0.0 | **Created**: 2025-12-02
**Type**: Architecture Proposal | **Status**: Draft
**Problem**: Knowledge silos between agents prevent cross-domain learning

---

## EXECUTIVE SUMMARY

### The Problem

```
┌─────────────────────────────────────────────────────────────────┐
│                    CURRENT STATE (Siloed)                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐     │
│  │   codexa    │      │   mentor    │      │   anuncio   │     │
│  │   _agent    │      │   _agent    │      │   _agent    │     │
│  ├─────────────┤      ├─────────────┤      ├─────────────┤     │
│  │ subagent    │      │ PROMPT_ENG  │      │ copywriting │     │
│  │ patterns    │      │ patterns    │      │ knowledge   │     │
│  │             │      │ playbook    │      │             │     │
│  └──────┬──────┘      └──────┬──────┘      └──────┬──────┘     │
│         │                    │                    │             │
│         │   NO CONNECTION    │   NO CONNECTION    │             │
│         ▼                    ▼                    ▼             │
│  ┌──────────────────────────────────────────────────────┐      │
│  │                    Scout MCP                          │      │
│  │  discover() = keyword-based, agent-filtered           │      │
│  │  search()   = glob patterns only                      │      │
│  │  smart_context() = per-agent, no cross-reference      │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
│  RESULT: codexa_agent creating subagent does NOT               │
│          automatically get prompt engineering patterns          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### The Solution

```
┌─────────────────────────────────────────────────────────────────┐
│                    TARGET STATE (Connected)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 KNOWLEDGE GRAPH                          │   │
│  │                                                          │   │
│  │   "criar subagent"                                       │   │
│  │         │                                                │   │
│  │         ├──► codexa_agent/23_subagent_patterns.md       │   │
│  │         ├──► mentor_agent/pattern_tool_calling.md       │   │
│  │         ├──► mentor_agent/pattern_task_management.md    │   │
│  │         └──► mentor_agent/playbook_prompt_engineering   │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                          │                                      │
│                          ▼                                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │              Scout MCP + Knowledge Router                │   │
│  │                                                          │   │
│  │  1. discover_knowledge(intent, task_type)               │   │
│  │     → Returns cross-agent relevant files                 │   │
│  │                                                          │   │
│  │  2. get_task_prerequisites(task_type)                   │   │
│  │     → Returns mandatory knowledge before task            │   │
│  │                                                          │   │
│  │  3. embed_and_search(query, top_k=10)                   │   │
│  │     → Semantic search across ALL knowledge               │   │
│  │                                                          │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## PROPOSED ARCHITECTURE

### Layer 1: Knowledge Graph (Declarative Rules)

Low-cost, immediate implementation. No embeddings needed.

```json
{
  "knowledge_graph": {
    "task_types": {
      "create_subagent": {
        "primary_agent": "codexa_agent",
        "required_knowledge": [
          "codexa_agent/iso_vectorstore/23_subagent_patterns.md",
          "mentor_agent/FONTES/PROMPT_ENGINEERING/playbook_prompt_engineering_20251201.md"
        ],
        "recommended_knowledge": [
          "mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_tool_calling_20251201.md",
          "mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_task_management_20251201.md",
          "mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_advanced_techniques_20251202.md"
        ],
        "triggers": ["subagent", "criar agente", "build agent", "Task tool"]
      },
      "create_hop": {
        "primary_agent": "codexa_agent",
        "required_knowledge": [
          "codexa_agent/iso_vectorstore/17_tac7_spec.md",
          "mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_task_management_20251201.md"
        ],
        "triggers": ["HOP", "prompt", "Higher-Order Prompt"]
      },
      "create_anuncio": {
        "primary_agent": "anuncio_agent",
        "required_knowledge": [
          "anuncio_agent/PRIME.md",
          "mentor_agent/FONTES/ECOMMERCE/seo_optimization.md"
        ],
        "triggers": ["anuncio", "listing", "produto"]
      }
    }
  }
}
```

### Layer 2: Scout Enhancement (discover_knowledge)

New Scout MCP function that uses the knowledge graph:

```typescript
// New Scout function
function discover_knowledge(params: {
  query: string,           // Natural language query
  task_type?: string,      // Optional explicit task type
  include_cross_agent: boolean  // Default: true
}): KnowledgeResult {

  // 1. Detect task type from query
  const taskType = params.task_type || detectTaskType(params.query);

  // 2. Get knowledge graph entry
  const graphEntry = knowledgeGraph.task_types[taskType];

  // 3. Combine with standard discover results
  const standardResults = discover({ query: params.query });

  // 4. Add cross-agent knowledge
  if (params.include_cross_agent && graphEntry) {
    return {
      ...standardResults,
      required_knowledge: graphEntry.required_knowledge,
      recommended_knowledge: graphEntry.recommended_knowledge,
      cross_agent_context: true
    };
  }

  return standardResults;
}
```

### Layer 3: Embeddings (Semantic Search)

For complex queries where declarative rules fail:

```python
# Vector store for all knowledge files
class KnowledgeVectorStore:
    def __init__(self):
        self.index = None
        self.documents = []

    def index_knowledge(self, paths: list[str]):
        """Index all knowledge files from all agents"""
        for path in paths:
            content = read_file(path)
            chunks = chunk_document(content, chunk_size=1000)
            embeddings = embed_chunks(chunks)  # OpenAI/Voyage/local
            self.add_to_index(embeddings, path, chunks)

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        """Semantic search across all knowledge"""
        query_embedding = embed_query(query)
        results = self.index.search(query_embedding, top_k)
        return [
            {
                "path": r.path,
                "chunk": r.chunk,
                "score": r.score,
                "agent": extract_agent(r.path)
            }
            for r in results
        ]
```

---

## IMPLEMENTATION PHASES

### Phase 1: Knowledge Graph (Week 1)

**Effort**: Low | **Impact**: High | **Dependencies**: None

1. Create `knowledge_graph.json` with task→knowledge mappings
2. Add `get_task_prerequisites()` to Scout MCP
3. Update ADW workflows to call prerequisites before execution

```
Files to create:
- codexa.app/agentes/mentor_agent/FONTES/knowledge_graph.json
- Scout MCP: add get_task_prerequisites() function
```

### Phase 2: Scout Enhancement (Week 2)

**Effort**: Medium | **Impact**: High | **Dependencies**: Phase 1

1. Add `discover_knowledge()` function to Scout
2. Integrate with existing `discover()` and `smart_context()`
3. Add CLI flag: `--cross-agent` for explicit cross-agent search

```
Files to modify:
- Scout MCP source (index.ts or equivalent)
- Add knowledge_graph.json loading
```

### Phase 3: Embeddings (Week 3-4)

**Effort**: High | **Impact**: Very High | **Dependencies**: Phase 2

1. Create embedding pipeline for knowledge files
2. Store vectors in local SQLite/ChromaDB
3. Add `embed_and_search()` to Scout
4. Auto-reindex on file changes

```
Files to create:
- codexa.app/agentes/mentor_agent/scripts/embed_knowledge.py
- codexa.app/agentes/mentor_agent/FONTES/knowledge_vectors.db
- Scout MCP: add embed_and_search() function
```

---

## KNOWLEDGE CATEGORIES

### What Should Be Cross-Referenced

| Category | Source Agent | Consumers | Priority |
|----------|--------------|-----------|----------|
| Prompt Engineering Patterns | mentor_agent | codexa_agent, ALL | HIGH |
| SEO/E-commerce Best Practices | mentor_agent | anuncio_agent, pesquisa_agent | HIGH |
| Quality Standards | qa_agent | ALL | MEDIUM |
| Brand Guidelines | marca_agent | anuncio_agent, photo_agent, video_agent | MEDIUM |
| Market Research Insights | pesquisa_agent | anuncio_agent, marca_agent | MEDIUM |

### Knowledge File Index

```yaml
prompt_engineering:
  base_path: mentor_agent/FONTES/PROMPT_ENGINEERING/
  files:
    - patterns/pattern_tool_calling_20251201.md
    - patterns/pattern_task_management_20251201.md
    - patterns/pattern_file_operations_20251201.md
    - patterns/pattern_terminal_commands_20251201.md
    - patterns/pattern_security_constraints_20251201.md
    - patterns/pattern_advanced_techniques_20251202.md
    - playbook_prompt_engineering_20251201.md
    - catalogo_prompts.json
  tags: [prompt, subagent, HOP, tool, task, security]

subagent_construction:
  base_path: codexa_agent/iso_vectorstore/
  files:
    - 23_subagent_patterns.md
    - 22_agent_builder_patterns.md
  tags: [subagent, construction, meta, builder]

ecommerce:
  base_path: mentor_agent/FONTES/ECOMMERCE/
  files:
    - seo_optimization.md
    - copywriting_principles.md
    - conversion_tactics.md
  tags: [seo, copy, ecommerce, anuncio, listing]
```

---

## USAGE PATTERNS

### Pattern 1: Pre-Task Knowledge Injection

```markdown
## ADW Phase 0: Knowledge Loading (NEW)

Before Phase 1, automatically load prerequisite knowledge:

```
0.1. Detect task type from user request
0.2. Call mcp__scout__get_task_prerequisites(task_type)
0.3. Read all required_knowledge files
0.4. Store in context for subsequent phases
```

This ensures agents always have cross-domain knowledge.
```

### Pattern 2: Subagent Construction with Knowledge

```markdown
## Creating a Subagent (Enhanced Flow)

1. User: "Create a subagent for product photography prompts"

2. Scout detects: task_type = "create_subagent"

3. Scout returns:
   - codexa_agent/23_subagent_patterns.md (primary)
   - mentor_agent/pattern_tool_calling.md (cross-agent)
   - mentor_agent/pattern_advanced_techniques.md (cross-agent)
   - photo_agent/PRIME.md (domain context)

4. codexa_agent reads ALL files before constructing

5. Result: Better subagent with proper prompt engineering patterns
```

### Pattern 3: Semantic Query

```markdown
## Using Embeddings for Complex Queries

User: "How do I make my prompts more effective for tool calling?"

1. Query doesn't match any explicit task_type

2. Scout falls back to embed_and_search()

3. Returns semantic matches:
   - mentor_agent/pattern_tool_calling.md (score: 0.92)
   - mentor_agent/pattern_advanced_techniques.md (score: 0.87)
   - codexa_agent/23_subagent_patterns.md (score: 0.76)

4. User gets comprehensive cross-agent results
```

---

## SCOUT MCP ENHANCEMENT SPEC

### New Functions

```typescript
// 1. Get prerequisites for a task type
interface GetTaskPrerequisitesParams {
  task_type: string;  // e.g., "create_subagent", "create_hop"
}

interface GetTaskPrerequisitesResult {
  task_type: string;
  primary_agent: string;
  required_knowledge: string[];
  recommended_knowledge: string[];
  estimated_tokens: number;
}

// 2. Discover with cross-agent knowledge
interface DiscoverKnowledgeParams {
  query: string;
  task_type?: string;
  include_cross_agent?: boolean;  // default: true
  max_results?: number;
}

interface DiscoverKnowledgeResult {
  query: string;
  detected_task_type: string | null;
  primary_results: FileResult[];
  cross_agent_results: FileResult[];
  required_knowledge: string[];
  total_estimated_tokens: number;
}

// 3. Semantic search (Phase 3)
interface EmbedSearchParams {
  query: string;
  top_k?: number;  // default: 10
  filter_agents?: string[];
  filter_categories?: string[];
}

interface EmbedSearchResult {
  query: string;
  results: {
    path: string;
    chunk: string;
    score: number;
    agent: string;
    category: string;
  }[];
  search_time_ms: number;
}
```

---

## SUCCESS METRICS

### Phase 1 (Knowledge Graph)

- [ ] 100% of meta-construction tasks have defined prerequisites
- [ ] Scout can return cross-agent knowledge for 5+ task types
- [ ] ADW workflows include Phase 0 knowledge loading

### Phase 2 (Scout Enhancement)

- [ ] `discover_knowledge()` function operational
- [ ] Cross-agent results appear in standard discover calls
- [ ] 80%+ of test queries return relevant cross-agent files

### Phase 3 (Embeddings)

- [ ] All knowledge files indexed (~500 files)
- [ ] Semantic search latency < 500ms
- [ ] Recall@10 > 0.8 for test queries
- [ ] Auto-reindex on file changes

---

## RISKS & MITIGATIONS

| Risk | Impact | Mitigation |
|------|--------|------------|
| Knowledge graph maintenance | Medium | Auto-detect task types from ADW files |
| Embedding costs | Low | Use local models (sentence-transformers) |
| Index staleness | Medium | Git hooks to trigger reindex |
| Context overflow | High | Prioritize by importance tier |

---

## NEXT STEPS

1. **Immediate**: Create `knowledge_graph.json` with initial mappings
2. **This week**: Add `get_task_prerequisites()` to Scout
3. **Next week**: Integrate into ADW Phase 0
4. **Future**: Implement embeddings for semantic search

---

**Version**: 1.0.0
**Status**: Architecture Proposal
**Author**: Mentor Agent + Claude Analysis
**Review Required**: Yes
