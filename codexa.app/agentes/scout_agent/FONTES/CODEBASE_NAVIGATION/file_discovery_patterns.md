# File Discovery Patterns for LLMs

**Domain**: Codebase Navigation
**Category**: CODEBASE_NAVIGATION
**Source**: Claude Code patterns + IDE implementations
**Quality Score**: 0.84

---

## Resumo Executivo

File discovery e o processo de encontrar arquivos relevantes para uma tarefa. LLMs precisam de patterns especificos para navegar codebases eficientemente. Este documento cobre patterns de glob, regex, busca por contexto e heuristicas para descoberta automatica.

## Conceitos-Chave

### **Glob Patterns**
Padrao mais comum para matching de arquivos:

```bash
# Basic patterns
*.md              # All markdown files in current dir
**/*.md           # All markdown files recursively
src/**/*.py       # All Python files under src/

# Advanced patterns
**/[A-Z]*.md      # Files starting with uppercase
**/*_HOP.md       # All HOP files
**/{config,schemas}/*.json  # JSON in specific folders
```

### **Context-Aware Discovery**
Usar contexto do task para filtrar resultados:

```python
def discover_for_task(task_description, agent=None):
    # Extract intent from task
    intent = classify_intent(task_description)

    # Map intent to file patterns
    patterns = INTENT_PATTERNS.get(intent, ['**/*.md'])

    # Filter by agent if specified
    if agent:
        patterns = [f"**/agentes/{agent}/**" + p for p in patterns]

    return search_patterns(patterns)
```

### **Entry Point Strategy**
Comecar por entry points conhecidos, expandir conforme necessario:

```
Step 1: Load PRIME.md (identity, capabilities)
Step 2: Check INSTRUCTIONS.md (how to operate)
Step 3: Explore referenced files (from PRIME/INSTRUCTIONS)
Step 4: Search for task-specific files (HOPs, ADWs)
Step 5: Load configs as needed
```

### **Heuristic Filtering**
Regras para excluir arquivos irrelevantes rapidamente:

```python
EXCLUDE_HEURISTICS = [
    lambda f: f.name.startswith('.'),           # Hidden files
    lambda f: 'node_modules' in f.parts,        # Dependencies
    lambda f: '__pycache__' in f.parts,         # Cache
    lambda f: f.suffix in ['.pyc', '.log'],     # Generated
    lambda f: f.stat().st_size > 1_000_000,     # Large files
    lambda f: 'output' in f.parts,              # Generated outputs
]
```

## Como Aplicar

1. **Definir intent patterns**
   ```python
   INTENT_PATTERNS = {
       'create_content': ['**/prompts/*_HOP.md', '**/workflows/*_ADW_*.md'],
       'configure': ['**/config/*.json', '**/schemas/*.json'],
       'understand': ['**/PRIME.md', '**/README.md'],
       'debug': ['**/*.py', '**/*.ts', '**/logs/*.log'],
       'build_agent': ['**/codexa_agent/**/*.md', '**/templates/**/*.md'],
   }
   ```

2. **Implementar discovery pipeline**
   ```python
   class FileDiscovery:
       def discover(self, query: str, context: dict) -> List[File]:
           # Step 1: Parse query for patterns
           explicit_patterns = self.extract_patterns(query)

           # Step 2: Infer patterns from intent
           inferred_patterns = self.infer_patterns(query, context)

           # Step 3: Combine and dedupe
           all_patterns = set(explicit_patterns + inferred_patterns)

           # Step 4: Execute search
           results = []
           for pattern in all_patterns:
               matches = self.glob_search(pattern)
               results.extend(matches)

           # Step 5: Rank and filter
           ranked = self.rank_results(results, query, context)
           return self.filter_irrelevant(ranked)
   ```

3. **Usar Scout MCP tools**
   ```python
   # Natural language discovery
   results = mcp__scout__discover("create product listing")

   # Pattern-based search
   results = mcp__scout__search("**/*_HOP.md")

   # Agent-specific context
   results = mcp__scout__agent_context("anuncio_agent")
   ```

4. **Implementar fallback chain**
   ```python
   def find_with_fallback(query, agent):
       # Try specific first
       results = search(f"**/agentes/{agent}/**/*{query}*")
       if results:
           return results

       # Fallback to broader search
       results = search(f"**/*{query}*")
       if results:
           return results

       # Final fallback: semantic search
       return semantic_search(query)
   ```

## Exemplos Praticos

### Exemplo 1: Task-Based Discovery

**Query**: "generate keywords for product"
**Agent**: anuncio_agent

**Discovery Process**:
```
1. Extract keywords: [generate, keywords, product]
2. Match intent: create_content
3. Apply agent filter: anuncio_agent/**
4. Search patterns:
   - anuncio_agent/prompts/*keyword*
   - anuncio_agent/prompts/*_HOP.md
   - anuncio_agent/config/*.json

Results:
- 15_keywords_HOP.md (score: 0.95)
- PRIME.md (score: 0.75)
- config/copy_rules.json (score: 0.60)
```

**Resultado**: Arquivo correto encontrado em primeiro lugar

### Exemplo 2: Cross-Agent Discovery

**Query**: "how agents communicate"

**Discovery Process**:
```
1. No specific agent mentioned
2. Intent: understand (system architecture)
3. Search patterns:
   - **/PRIME.md
   - docs/*.md
   - **/AGENT_CHAINS.md

Results:
- docs/AGENT_CHAINS.md (score: 0.90)
- codexa_agent/PRIME.md (score: 0.82)
- CLAUDE.md (score: 0.75)
```

**Resultado**: Documentacao de arquitetura descoberta automaticamente

## Quando Usar

- **USE glob patterns quando**:
  - Estrutura de arquivos conhecida
  - Busca por extensao/nome
  - Performance critica

- **USE semantic discovery quando**:
  - Query em linguagem natural
  - Estrutura desconhecida
  - Exploratory search

- **USE agent_context quando**:
  - Tarefa especifica de um agente
  - Precisa de todos os arquivos relacionados
  - Context building para LLM

- **USE entry point strategy quando**:
  - Nova codebase
  - Onboarding de usuario
  - Debugging broad issues

## Relacionado

- Ver tambem: `llm_context_optimization.md`
- Ver tambem: `../SEARCH_PATTERNS/semantic_search.md`
- Tool: `mcp__scout__discover()`
- Tool: `mcp__scout__search()`

---

**Processado**: 2025-12-05
**Tokens**: ~1050
