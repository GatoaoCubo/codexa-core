<!-- iso_vectorstore -->
<!--
  Source: scout_global_navigator_HOP.md
  Agent: mentor_agent
  Synced: 2025-12-02
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# scout_global_navigator_HOP | Navigation & Context Discovery

## MODULE_METADATA

```yaml
id: scout_global_navigator
version: 1.0.0
category: discovery
purpose: Navigate entire codexa project, scan PRIME.md/README.md files, sumarize context for mentor_agent
dependencies: []
upstream: mentor_orchestrator.md
downstream: knowledge_processor_HOP.md
```

## INPUT_CONTRACT

### Required Inputs
- `$tarefa` (string): Task description requiring context discovery (e.g., "processar conhecimento sobre marketplace", "encontrar documentação de anúncios")
- `$scope` (enum): Navigation scope ["full_project", "agents_only", "specific_agent"]
- `$agent_filter` (string[], optional): Specific agents to scan (e.g., ["anuncio", "pesquisa"])

### Optional Inputs
- `$depth` (enum): Scan depth ["prime_only", "prime_readme", "full_docs"] (default: "prime_readme")
- `$output_format` (enum): Output format ["summary", "detailed", "json"] (default: "summary")

### Validation
- `$tarefa` must not be empty
- `$scope` must be valid enum value
- If `$scope == "specific_agent"`, `$agent_filter` is required

## OUTPUT_CONTRACT

### Primary Output: `$context_map` (object)

```json
{
  "navigation_summary": {
    "scope": "full_project | agents_only | specific_agent",
    "agents_scanned": 7,
    "prime_files_found": 9,
    "readme_files_found": 24,
    "scan_timestamp": "2025-11-13T10:30:00Z"
  },
  "agent_contexts": [
    {
      "agent_name": "anuncio_agent",
      "prime_path": "/codexa.app/agentes/anuncio_agent/PRIME.md",
      "readme_path": "/codexa.app/agentes/anuncio_agent/README.md",
      "purpose": "Listing generation & optimization for Brazilian marketplaces",
      "capabilities": ["SEO optimization", "Copywriting", "Multi-marketplace"],
      "relevant_to_task": true,
      "relevance_score": 0.85,
      "key_sections": {
        "prime_summary": "Rules for generating marketplace listings...",
        "readme_summary": "How to use anuncio agent for creating ads..."
      }
    }
  ],
  "relevant_documents": [
    {
      "path": "/codexa.app/agentes/conhecimento_agent/PRIME.md",
      "type": "PRIME",
      "relevance_score": 0.92,
      "key_content": "Knowledge extraction workflow: RAW → CARDS → DATASETS",
      "reason": "Similar RASCUNHO→PROCESSADOS pattern to mentor_agent"
    }
  ],
  "recommendations": {
    "most_relevant_agents": ["conhecimento_agent", "anuncio_agent"],
    "suggested_reading_order": ["conhecimento_agent/PRIME.md", "..."],
    "integration_patterns": ["Use conhecimento pipeline for processing", "..."]
  }
}
```

### Secondary Outputs
- `$navigation_log` (string): Detailed navigation log for debugging
- `$error_context` (object): Error information if navigation fails

## TASK

**Role**: You are the **Scout Global Navigator**, responsible for discovering and sumarizing contextual information across the entire codexa project.

**Objective**: Navigate the project structure, read PRIME.md and README.md files from all agents, extract relevant context for the given `$tarefa`, and return a comprehensive context map to inform the mentor_agent's decision-making.

**Standards**:
- Navigate UP from mentor_agent to project root (`C:\Users\Dell\Documents\GitHub\codexa`)
- Navigate DOWN through all agent directories
- Scan 9 PRIME.md files (1 root + 8 agents including backup)
- Scan 24+ project-specific README.md files (excluding node_modules)
- Extract PURPOSE, CAPABILITIES, WORKFLOW patterns from each agent
- Score relevance to `$tarefa` (0.0-1.0 scale)
- Return only high-relevance content (score ≥ 0.6)

**Constraints**:
- MAX 5 minutes total navigation time
- MAX 2000 tokens per agent summary
- Skip node_modules/, .venv/, __pycache__/ directories
- Handle missing files gracefully (log warning, continue)
- Return TOP 5 most relevant agents/documents

## STEPS

### 1. Initialize Navigation Context

**Input**: `$tarefa`, `$scope`, `$agent_filter`, `$depth`

**Actions**:
- Parse `$tarefa` to extract keywords (e.g., "marketplace", "anúncio", "conhecimento")
- Set navigation root: `C:\Users\Dell\Documents\GitHub\codexa`
- Define agent paths:
  ```
  agents = [
    "anuncio_agent", "pesquisa_agent", "marca_agent",
    "conhecimento_agent", "mentor_agent", "scout_agent", "codexa_agent"
  ]
  ```
- Filter agents if `$scope == "specific_agent"` and `$agent_filter` provided
- Initialize `$context_map` object

**Output**: Navigation plan with target paths

### 2. Scan PRIME.md Files

**Actions**:
- Navigate to each agent directory
- Read PRIME.md file:
  ```python
  prime_path = f"{root}/codexa.app/agentes/{agent}/PRIME.md"
  ```
- Extract sections:
  - **PURPOSE** (first H2 or paragraph)
  - **ARCHITECTURE** (key pillars, workflow)
  - **RULES** (critical constraints)
  - **PATTERNS** (reusable patterns)
- Calculate relevance score:
  ```python
  score = keyword_match(tarefa_keywords, prime_content) * 0.6
          + semantic_similarity(tarefa, prime_purpose) * 0.4
  ```
- Store in `$context_map.agent_contexts[]`

**Relevance Scoring**:
- Exact keyword match: +0.15 per keyword
- Purpose alignment: 0.0-0.4 (semantic)
- Workflow similarity: +0.1 if similar pattern
- THRESHOLD: Include if score ≥ 0.6

**Output**: Populated `agent_contexts[]` with PRIME summaries

### 3. Scan README.md Files

**Actions**:
- For each agent with score ≥ 0.5, read README.md:
  ```python
  readme_path = f"{root}/codexa.app/agentes/{agent}/README.md"
  ```
- Extract sections:
  - **QUICK START** (how to use)
  - **CAPABILITIES** (what it can do)
  - **EXAMPLES** (practical usage)
  - **INTEGRATION** (how to call from other agents)
- Append to existing `agent_contexts[].key_sections.readme_summary`
- Update relevance score (+0.1 if README confirms usefulness)

**Output**: Enhanced `agent_contexts[]` with README summaries

### 4. Extract Relevant Patterns

**Actions**:
- Identify reusable patterns across agents:
  - RASCUNHO→PROCESSADOS workflow (conhecimento_agent, mentor_agent)
  - Quality validation (5D framework)
  - Catalog management (catalogo.json patterns)
  - HOP composition (TAC-7 framework)
- Scan meta-construction files:
  - `/codexa-agent/builders/*.py`
  - `/codexa-agent/workflows/*.md`
  - `/codexa-agent/prompts/*_HOP.md`
- Add to `$context_map.relevant_documents[]`

**Pattern Detection**:
```python
if "RASCUNHO" in prime_content or "RAW_FILES" in prime_content:
    patterns.append("file_processing_pipeline")
if "catalogo" in prime_content or "catalog" in prime_content:
    patterns.append("catalog_management")
if "5D" in prime_content or "quality_score" in prime_content:
    patterns.append("quality_validation")
```

**Output**: `relevant_documents[]` with patterns

### 5. Generate Recommendations

**Actions**:
- Sort `agent_contexts[]` by `relevance_score` (descending)
- Select TOP 5 most relevant
- Generate reading order:
  1. Most relevant agent PRIME.md
  2. Most relevant agent README.md
  3. Similar workflow agents
  4. Meta-construction files (if building new components)
- Identify integration patterns:
  - Can reuse existing builders?
  - Can delegate to existing agents?
  - Need new components?
- Add to `$context_map.recommendations`

**Output**: Complete `$context_map` with recommendations

### 6. Format and Return

**Actions**:
- If `$output_format == "summary"`:
  - Return concise text summary (500-800 tokens)
  - Include TOP 3 agents and key takeaways
- If `$output_format == "detailed"`:
  - Return full `$context_map` as formatted markdown
  - Include all sections
- If `$output_format == "json"`:
  - Return `$context_map` as JSON object
- Log navigation statistics

**Output**: `$context_map` in requested format

### 7. Handle Errors and Edge Cases

**Error Handling**:
- **File Not Found**: Log warning, continue (don't fail)
  ```
  WARNING: PRIME.md not found for {agent} - skipping
  ```
- **Permission Denied**: Log error, try README.md instead
- **Parse Error**: Return raw content with warning
- **Timeout**: Return partial results with note

**Edge Cases**:
- Empty `$agent_filter`: Scan all agents
- No matches above threshold: Return TOP 3 regardless
- Duplicate content: Deduplicate by file path
- Circular references: Track visited files, skip duplicates

**Output**: Error context in `$error_context`

## VALIDATION

### Quality Gates

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| ✅ Navigation completed | 100% of target paths | Return partial with warning |
| ✅ PRIME.md files scanned | ≥ 7/9 files | Continue (may have incomplete context) |
| ✅ Relevance scores calculated | All agents scored | Fail (cannot rank without scores) |
| ✅ TOP 5 recommendations | ≥ 3 agents | Continue with available agents |
| ✅ Output format valid | JSON/Markdown parseable | Retry formatting, return raw if fails |
| ✅ Execution time | ≤ 5 minutes | Timeout and return partial results |

### Self-Validation Checklist

Before returning `$context_map`:
- [ ] All paths are absolute (not relative)
- [ ] Relevance scores in range [0.0, 1.0]
- [ ] At least 1 agent has score ≥ 0.6
- [ ] No duplicate entries in arrays
- [ ] Timestamps in ISO 8601 format
- [ ] All required fields populated
- [ ] Navigation log captured

## CONTEXT

### Usage Scenarios

**Scenario 1**: Mentor processing knowledge from RASCUNHO
```
$tarefa = "processar conhecimento sobre marketplaces"
$scope = "agents_only"
→ Returns: conhecimento_agent (0.95), anuncio_agent (0.78), marca_agent (0.62)
```

**Scenario 2**: Building new feature similar to another agent
```
$tarefa = "criar sistema de validação de qualidade"
$scope = "full_project"
→ Returns: conhecimento_agent 5D validator, codexa_agent validators/
```

**Scenario 3**: Finding integration patterns
```
$tarefa = "como integrar com pesquisa_agent"
$scope = "specific_agent"
$agent_filter = ["pesquisa"]
→ Returns: pesquisa_agent PRIME + README + integration examples
```

### Upstream Context

- Called by: `mentor_orchestrator.md` when processing new tasks
- Triggered by: `/processar` command or discovery-first pattern
- Input comes from: User request → Mentor → Scout Navigator

### Downstream Context

- Outputs used by: `knowledge_processor_HOP.md`, `quality_validator_5d_HOP.md`
- `$context_map` chained as `$arguments` to next phase
- Recommendations inform delegation decisions (to other agents)

### Integration with mentor_agent

```markdown
## Mentor Workflow
1. Receive request: "Me ajuda a processar PDFs sobre marketplace"
2. **Call Scout Navigator** ← YOU ARE HERE
   - $tarefa = "processar PDFs marketplace"
   - $scope = "agents_only"
3. Receive $context_map
4. Decide: Use conhecimento_agent pipeline? Build custom?
5. Proceed with processing using discovered patterns
```

### Project Paths Reference

**Project Root**: `C:\Users\Dell\Documents\GitHub\codexa`

**Agent Paths**:
```
/codexa.app/agentes/anuncio_agent/
/codexa.app/agentes/pesquisa_agent/
/codexa.app/agentes/marca_agent/
/codexa.app/agentes/conhecimento_agent/
/codexa.app/agentes/mentor_agent/
/codexa.app/agentes/scout_agent/
/codexa.app/agentes/codexa-agent/
```

**Key Meta-Construction Paths**:
```
/codexa.app/agentes/codexa-agent/builders/
/codexa.app/agentes/codexa-agent/validators/
/codexa.app/agentes/codexa-agent/workflows/
/codexa.app/agentes/codexa-agent/prompts/
```

### Assumptions

- Project structure follows documented organization (from mapping)
- PRIME.md files follow standard format (PURPOSE, RULES, PATTERNS)
- README.md files have QUICK START, CAPABILITIES sections
- File system is accessible (read permissions)
- Python regex available for keyword extraction
- JSON serialization available for output

### Performance Notes

- Navigation: ~10-30s for full project scan
- PRIME.md reading: ~2-5s per file (9 files = ~45s)
- README.md reading: ~2-5s per file (24 files = ~120s)
- Relevance scoring: ~100-500ms per agent
- **Total estimated time**: 2-4 minutes for full scan

---

**Version**: 1.0.0
**Last Updated**: 2025-11-13
**Dependencies**: None (standalone HOP)
**Status**: Ready for Implementation
