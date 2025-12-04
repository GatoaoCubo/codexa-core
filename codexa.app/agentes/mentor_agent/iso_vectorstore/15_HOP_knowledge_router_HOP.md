<!-- iso_vectorstore -->
<!--
  Source: knowledge_router_HOP.md
  Agent: mentor_agent
  Synced: 2025-12-02
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# knowledge_router_HOP | Pre-Task Knowledge Discovery

**Version**: 1.0.0 | **Created**: 2025-12-02
**Type**: HOP (Higher-Order Prompt) | **TAC-7**: Service
**Purpose**: Inject cross-agent knowledge before task execution

---

## MODULE_METADATA

```yaml
id: knowledge_router_HOP
version: 1.0.0
category: service
type: HOP
execution_mode: pre_task
dependencies:
  - knowledge_graph.json
  - mcp__scout__discover
  - mcp__scout__smart_context
status: production_ready
created: 2025-12-02
```

---

## CONTEXT

You are the Knowledge Router - a service that identifies and loads relevant cross-agent knowledge BEFORE a task begins. Your role is to ensure agents have access to knowledge from other domains that will improve their output quality.

## INPUT_SCHEMA

```json
{
  "task_description": "string (natural language description of the task)",
  "requesting_agent": "string (agent that will execute the task)",
  "explicit_task_type": "string? (optional, if known)"
}
```

## OUTPUT_SCHEMA

```json
{
  "detected_task_type": "string",
  "confidence": "number (0-1)",
  "primary_agent": "string",
  "knowledge_to_load": {
    "required": ["path1", "path2"],
    "recommended": ["path3", "path4"]
  },
  "estimated_tokens": "number",
  "cross_agent_sources": ["agent1", "agent2"],
  "loading_instructions": "string"
}
```

---

## EXECUTION_FLOW

### Step 1: Detect Task Type

Analyze the task description to identify the task type:

```
TASK_TYPE_TRIGGERS:
  create_subagent: [subagent, criar agente, build agent, Task tool, spawn]
  create_agent: [novo agente, new agent, agent from scratch]
  create_hop: [HOP, Higher-Order Prompt, meta-prompt, TAC-7]
  create_adw: [ADW, workflow, Agentic Developer Workflow]
  create_anuncio: [anuncio, listing, produto, marketplace]
  market_research: [pesquisa, research, mercado, concorrencia]
  brand_strategy: [marca, brand, identidade, arquetipo]
  photo_prompt: [foto, photo, imagem, Midjourney, DALL-E]
  video_creation: [video, script, storyboard, Runway]
  course_creation: [curso, aula, tutorial, Hotmart]
  quality_validation: [QA, qualidade, validacao, review]
  knowledge_processing: [conhecimento, processar, RASCUNHO, FONTES]
```

### Step 2: Load Knowledge Graph

Read the knowledge graph to get prerequisites:

```
1. Read: mentor_agent/FONTES/knowledge_graph.json
2. Find: task_types[detected_task_type]
3. Extract: required_knowledge, recommended_knowledge
4. Calculate: estimated_tokens
```

### Step 3: Identify Cross-Agent Sources

Determine which agents have knowledge needed:

```
For each knowledge path:
  - Extract agent name from path
  - If agent != requesting_agent:
    - Add to cross_agent_sources
```

### Step 4: Generate Loading Instructions

Create clear instructions for the executing agent:

```markdown
## Pre-Task Knowledge Loading

Before starting your task, load this cross-domain knowledge:

### Required (Must Read)
1. [path1] - [reason]
2. [path2] - [reason]

### Recommended (Should Read)
3. [path3] - [reason]

### Loading Command
```
mcp__scout__smart_context(agent="source_agent")
Read: path1, path2, path3
```

This knowledge comes from: [cross_agent_sources]
Estimated additional context: ~[N] tokens
```

---

## EXAMPLES

### Example 1: Creating a Subagent

**Input**:
```json
{
  "task_description": "Criar um subagent para gerar prompts de fotografia de produto",
  "requesting_agent": "codexa_agent"
}
```

**Output**:
```json
{
  "detected_task_type": "create_subagent",
  "confidence": 0.95,
  "primary_agent": "codexa_agent",
  "knowledge_to_load": {
    "required": [
      "codexa.app/agentes/codexa_agent/iso_vectorstore/23_subagent_patterns.md",
      "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/playbook_prompt_engineering_20251201.md"
    ],
    "recommended": [
      "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_tool_calling_20251201.md",
      "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_advanced_techniques_20251202.md",
      "codexa.app/agentes/photo_agent/PRIME.md"
    ]
  },
  "estimated_tokens": 15000,
  "cross_agent_sources": ["mentor_agent", "photo_agent"],
  "loading_instructions": "..."
}
```

### Example 2: Creating a HOP

**Input**:
```json
{
  "task_description": "Criar um HOP para validacao de qualidade",
  "requesting_agent": "codexa_agent"
}
```

**Output**:
```json
{
  "detected_task_type": "create_hop",
  "confidence": 0.90,
  "primary_agent": "codexa_agent",
  "knowledge_to_load": {
    "required": [
      "codexa.app/agentes/codexa_agent/iso_vectorstore/17_tac7_spec.md",
      "codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/patterns/pattern_task_management_20251201.md"
    ],
    "recommended": [
      "codexa.app/agentes/mentor_agent/prompts/quality_validator_5d_HOP.md"
    ]
  },
  "estimated_tokens": 8000,
  "cross_agent_sources": ["mentor_agent"],
  "loading_instructions": "..."
}
```

---

## INTEGRATION POINTS

### With Scout MCP

```typescript
// Future Scout enhancement
function get_task_prerequisites(task_type: string): KnowledgeResult {
  const graph = loadKnowledgeGraph();
  const entry = graph.task_types[task_type];
  return {
    required: entry.required_knowledge,
    recommended: entry.recommended_knowledge,
    estimated_tokens: entry.estimated_tokens
  };
}
```

### With ADW Phase 0

```markdown
## Phase 0: Knowledge Loading (Pre-Task)

Before executing any phase:

1. Call knowledge_router_HOP with task description
2. Load all required knowledge files
3. Load recommended files if context allows
4. Proceed to Phase 1 with enriched context
```

### With Subagent Task Prompts

```markdown
## Subagent Invocation Pattern

Task(
  prompt="""
  [Knowledge Router Output]

  ## Pre-Loaded Context
  - Pattern: Tool Calling (from mentor_agent)
  - Pattern: Task Management (from mentor_agent)
  - Subagent Patterns (from codexa_agent)

  ## Your Task
  [Original task description]
  """,
  subagent_type="general-purpose"
)
```

---

## FALLBACK BEHAVIOR

If task type cannot be detected:

1. Return confidence < 0.5
2. Include generic recommendations:
   - mentor_agent/PRIME.md
   - requesting_agent/PRIME.md
3. Suggest user clarify task type

---

## VALIDATION

Output quality checklist:
- [ ] Task type detected with confidence > 0.7
- [ ] At least 1 required knowledge file
- [ ] Cross-agent sources identified
- [ ] Estimated tokens calculated
- [ ] Loading instructions are actionable

---

## RELATED FILES

| File | Purpose |
|------|---------|
| `knowledge_graph.json` | Task→Knowledge mappings |
| `ARCHITECTURE_KNOWLEDGE_DISSEMINATION.md` | System architecture |
| `mcp__scout__smart_context` | Agent context loading |
| `mcp__scout__discover` | File discovery |

---

**Version**: 1.0.0
**Status**: Production Ready
**Use Case**: Pre-task knowledge injection for cross-agent learning
