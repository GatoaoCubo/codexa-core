# LLM Context Optimization

**Domain**: Codebase Navigation
**Category**: CODEBASE_NAVIGATION
**Source**: Claude Code patterns + Token optimization research
**Quality Score**: 0.87

---

## Resumo Executivo

LLMs tem janelas de contexto limitadas (100K-200K tokens). Otimizar o que entra no contexto e crucial para performance e qualidade das respostas. Este documento cobre estrategias para maximizar valor por token em contextos de navegacao de codebase.

## Conceitos-Chave

### **Token Budget Management**
Alocar tokens por categoria de informacao:

```
Total Budget: 100K tokens (example)
├── System Prompt: 5K (5%)        # Fixed overhead
├── Task Context: 15K (15%)       # User query + history
├── File Contents: 60K (60%)      # Actual code/docs
├── Tool Outputs: 15K (15%)       # Search results, etc.
└── Response Buffer: 5K (5%)      # Space for output
```

### **Information Density**
Nem todo conteudo tem igual densidade de informacao:

| Content Type | Info Density | Token Cost | Priority |
|--------------|--------------|------------|----------|
| PRIME.md | Very High | ~500-1000 | 1st |
| README.md | High | ~800-1500 | 2nd |
| Code files | Medium | ~200-5000 | 3rd |
| Configs | Low-Medium | ~100-500 | 4th |
| Logs/outputs | Very Low | ~1000+ | Skip |

### **Tiered Loading**
Carregar informacao em camadas, aumentando detalhe conforme necessario:

```
Tier 1: Entry Points (always load)
  - PRIME.md for relevant agents
  - Key configs referenced in task

Tier 2: Supporting Docs (load on demand)
  - README.md for deep context
  - Related HOPs for task execution

Tier 3: Implementation (load when needed)
  - Source code for specific files
  - Full configs when editing
```

### **Smart Truncation**
Quando conteudo excede budget, truncar inteligentemente:

```python
def smart_truncate(content, max_tokens, preserve=['headers', 'first_section']):
    if estimate_tokens(content) <= max_tokens:
        return content

    sections = parse_sections(content)
    result = []
    remaining = max_tokens

    # Always include preserved sections
    for preserve_type in preserve:
        if preserve_type in sections:
            section = sections[preserve_type]
            result.append(section)
            remaining -= estimate_tokens(section)

    # Add remaining sections by priority until budget exhausted
    for section in prioritize_sections(sections):
        tokens = estimate_tokens(section)
        if tokens <= remaining:
            result.append(section)
            remaining -= tokens

    result.append(f"\n[Truncated: {estimate_tokens(content) - max_tokens} tokens omitted]")
    return '\n'.join(result)
```

## Como Aplicar

1. **Definir budget por contexto**
   ```python
   CONTEXT_BUDGETS = {
       'simple_query': 30_000,      # Single file operations
       'agent_task': 60_000,        # Multi-file with agent context
       'complex_workflow': 100_000, # Full ADW execution
   }
   ```

2. **Implementar priority queue para arquivos**
   ```python
   class ContextBuilder:
       def __init__(self, budget: int):
           self.budget = budget
           self.used = 0
           self.files = []

       def add_file(self, path: str, priority: int, content: str):
           tokens = estimate_tokens(content)
           if self.used + tokens <= self.budget:
               self.files.append({
                   'path': path,
                   'priority': priority,
                   'content': content,
                   'tokens': tokens
               })
               self.used += tokens
               return True
           return False

       def build(self):
           # Sort by priority, return formatted context
           sorted_files = sorted(self.files, key=lambda x: x['priority'])
           return '\n\n'.join(
               f"### {f['path']}\n{f['content']}"
               for f in sorted_files
           )
   ```

3. **Usar smart_context do Scout**
   ```python
   # Scout already implements tiered loading
   context = mcp__scout__smart_context(
       agent="anuncio_agent",
       max_files=20,
       include_hints=True
   )

   # Returns prioritized list:
   # - critical: PRIME.md, key HOPs
   # - high: README, related configs
   # - medium: Supporting docs
   # - low: Reference files
   ```

4. **Monitorar usage em runtime**
   ```python
   def check_context_health(used_tokens, budget):
       usage = used_tokens / budget
       if usage > 0.9:
           logger.warning(f"Context 90% full ({used_tokens}/{budget})")
       elif usage > 0.75:
           logger.info(f"Context 75% used ({used_tokens}/{budget})")
   ```

## Exemplos Praticos

### Exemplo 1: Agent Context Loading

**Task**: "Create title for wireless headphone"
**Agent**: anuncio_agent

**Optimal Context** (50K budget):
```
Tier 1 (15K):
  - anuncio_agent/PRIME.md (1K)
  - 14_title_HOP.md (2K)
  - config/copy_rules.json (500)
  - marca_agent context hint (500)

Tier 2 (20K, on demand):
  - README.md (1.5K)
  - schemas/input.json (300)
  - Related HOPs if needed

Tier 3 (15K, reserve):
  - Buffer for tool outputs
  - User clarifications
```

**Resultado**: Task completed with 35K tokens used (70% of budget)

### Exemplo 2: Cross-Agent Workflow

**Task**: "Full product listing (research -> copy -> photo)"
**Budget**: 100K tokens

**Distribution**:
```
Phase 1 - Research (30K):
  - pesquisa_agent context: 15K
  - Search results: 10K
  - Synthesis: 5K

Phase 2 - Copy (35K):
  - anuncio_agent context: 15K
  - Research output: 10K (compressed)
  - Generation: 10K

Phase 3 - Photo (25K):
  - photo_agent context: 10K
  - Copy for reference: 5K
  - Image generation: 10K

Buffer (10K):
  - Inter-phase coordination
  - Error handling
```

**Resultado**: 3-phase workflow in single context window

## Quando Usar

- **USE tiered loading quando**:
  - Budget limitado (<50K)
  - Task bem definida
  - Agente especifico conhecido

- **USE full context quando**:
  - Budget amplo (>100K)
  - Exploratory task
  - Multiple agents may be needed

- **USE aggressive truncation quando**:
  - Mobile/embedded contexts
  - High-frequency operations
  - Cost optimization priority

- **AVOID overloading quando**:
  - Response quality degrades
  - LLM starts hallucinating
  - Token costs spike

## Relacionado

- Ver tambem: `file_discovery_patterns.md`
- Tool: `mcp__scout__smart_context()`
- Reference: Claude context window documentation

---

**Processado**: 2025-12-05
**Tokens**: ~1100
