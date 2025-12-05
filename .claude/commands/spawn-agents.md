# /spawn-agents - CODEXA Agent Orchestrator

**Version**: 1.0.0 | **Type**: Parallel Execution

Launch CODEXA-specific agent pipelines for common workflows.

---

## QUICK START

```
/spawn-agents product-pipeline "Garrafa Ecologica"
```

Spawns: pesquisa → (parallel: marca + anuncio + photo)

---

## PIPELINES

### 1. Product Pipeline (Full Listing)
```
/spawn-agents product-pipeline "Product Name"
```

**Spawns**:
1. `pesquisa-agent`: Market research (runs first)
2. Then in parallel:
   - `marca-agent`: Brand strategy
   - `anuncio-agent`: Marketplace copy
   - `photo-agent`: Image prompts

**Duration**: 15-25 min
**Output**: Complete product listing ready for marketplace

### 2. Research Multi (4 Marketplaces)
```
/spawn-agents research-multi "Product Name"
```

**Spawns** (parallel):
1. `pesquisa-agent`: Mercado Livre focus
2. `pesquisa-agent`: Shopee focus
3. `pesquisa-agent`: Amazon BR focus
4. `pesquisa-agent`: Magalu focus

**Duration**: 10-15 min
**Output**: 4 research_notes.md (one per marketplace)

### 3. Content Suite (Full Media)
```
/spawn-agents content-suite "Product Name"
```

**Spawns** (sequential → parallel):
1. `pesquisa-agent`: Research
2. Then parallel:
   - `photo-agent`: 9 image prompts
   - `video-agent`: Video storyboard
   - `anuncio-agent`: Marketplace copy

**Duration**: 20-30 min
**Output**: Complete content package

### 4. Quality Audit
```
/spawn-agents quality-audit
```

**Spawns** (parallel):
1. `qa-agent`: Validate anuncio outputs
2. `qa-agent`: Validate pesquisa outputs
3. `qa-agent`: Validate marca outputs
4. `qa-agent`: Check compliance rules

**Duration**: 5-10 min
**Output**: Validation reports

### 5. Course Builder
```
/spawn-agents course-builder "Module Topic"
```

**Spawns** (sequential):
1. `curso-agent`: Generate outline
2. `curso-agent`: Generate video scripts
3. `curso-agent`: Generate workbooks
4. `qa-agent`: Validate content

**Duration**: 30-45 min
**Output**: Complete course module

---

## HOW IT WORKS

When `/spawn-agents [pipeline] [args]` is called:

### 1. Parse Pipeline
```python
PIPELINES = {
    "product-pipeline": {
        "sequential": ["pesquisa-agent"],
        "parallel": ["marca-agent", "anuncio-agent", "photo-agent"],
        "input_template": "Research and create listing for: $1"
    },
    "research-multi": {
        "parallel": [
            ("pesquisa-agent", "Research $1 on Mercado Livre"),
            ("pesquisa-agent", "Research $1 on Shopee"),
            ("pesquisa-agent", "Research $1 on Amazon BR"),
            ("pesquisa-agent", "Research $1 on Magalu"),
        ]
    },
    # ... etc
}
```

### 2. Execute Phases
1. **Sequential Phase**: Run agents one by one, pass outputs as $context
2. **Parallel Phase**: Spawn all agents in ONE message with multiple Task calls
3. **Collect Results**: Aggregate outputs, generate summary

### 3. Agent Loading
Each spawned agent:
1. Loads its `.claude/agents/{name}-agent.md` definition
2. Calls `mcp__scout__smart_context` for full knowledge
3. Executes task with complete domain expertise

---

## EXAMPLES

### Full Product Launch
```
/spawn-agents product-pipeline "Tenis Running Premium"

# Result:
# - research_notes.md (22 blocks)
# - brand_strategy.md (32 blocks)
# - marketplace_listing.md (titles, keywords, bullets, description)
# - photo_prompts.md (Grid + 9 individual)
```

### Parallel Research
```
/spawn-agents research-multi "Fone Bluetooth"

# Result:
# - fone_bluetooth_ML_research.md
# - fone_bluetooth_Shopee_research.md
# - fone_bluetooth_Amazon_research.md
# - fone_bluetooth_Magalu_research.md
```

### Quality Check
```
/spawn-agents quality-audit

# Result:
# - anuncio_validation_report.md
# - pesquisa_validation_report.md
# - marca_validation_report.md
# - compliance_check.md
```

---

## LLM INSTRUCTIONS

When `/spawn-agents` is invoked:

1. **Parse pipeline name and arguments**
2. **Load pipeline definition** from this file
3. **Execute sequential phase** (if any):
   - Call Task tool with appropriate subagent_type
   - Store result as $context for next phase
4. **Execute parallel phase** (if any):
   - Send ONE message with ALL Task tool calls
   - Each Task includes agent prompt + context
5. **Aggregate results**:
   - Combine outputs
   - Generate summary
   - Report completion

### Important Notes

- Max 10 parallel agents (Claude Code limit)
- Each agent should call `mcp__scout__smart_context` first
- Pass previous phase output as context to next phase
- Use `model: haiku` for simple searches, `opus` for complex creative

---

## RELATED

- `/spawn` - Generic parallel spawner (any agent type)
- `/prime-*` - Load individual agent context
- `.claude/agents/` - Subagent definitions

---

**Version**: 1.0.0
**Created**: 2025-12-05
**Type**: CODEXA-specific parallel orchestration
