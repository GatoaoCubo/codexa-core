# MCP Tool Design Best Practices

**Domain**: MCP (Model Context Protocol)
**Category**: MCP_PATTERNS
**Source**: MCP Specification + Claude Code implementation
**Quality Score**: 0.86

---

## Resumo Executivo

MCP tools sao a interface entre LLMs e sistemas externos. Um bom design de tool maximiza usabilidade pelo LLM, minimiza erros, e fornece feedback claro. Este documento cobre patterns para design de tools efetivas baseado nas melhores implementacoes do mercado.

## Conceitos-Chave

### **Tool Schema Design**
Cada tool precisa de schema bem definido:

```json
{
  "name": "tool_name",
  "description": "Clear description of what the tool does and when to use it",
  "parameters": {
    "type": "object",
    "required": ["param1"],
    "properties": {
      "param1": {
        "type": "string",
        "description": "What this parameter controls"
      },
      "param2": {
        "type": "integer",
        "default": 10,
        "description": "Optional parameter with default"
      }
    }
  }
}
```

### **Naming Conventions**
Nomes claros e previssiveis:

```
DO:
- mcp__scout__discover     # Namespace + action verb
- mcp__scout__search       # Clear purpose
- mcp__scout__create       # CRUD verbs

DON'T:
- scout_find_files_v2      # Version in name
- doSearch                 # Camel case
- process                  # Too generic
```

### **Parameter Design**
Parametros que LLMs entendem facilmente:

```python
# GOOD: Clear types and descriptions
{
    "query": {
        "type": "string",
        "description": "Natural language query (e.g., 'find HOP files for anuncio')"
    },
    "max_results": {
        "type": "integer",
        "default": 10,
        "minimum": 1,
        "maximum": 100,
        "description": "Maximum number of results to return"
    }
}

# BAD: Ambiguous or complex
{
    "options": {
        "type": "object",
        "description": "Various options"  # Too vague
    }
}
```

### **Error Handling**
Erros informativos que guiam correcao:

```python
class ToolError:
    def __init__(self, code: str, message: str, suggestion: str = None):
        self.code = code
        self.message = message
        self.suggestion = suggestion

    def to_response(self):
        response = {
            "error": True,
            "code": self.code,
            "message": self.message
        }
        if self.suggestion:
            response["suggestion"] = self.suggestion
        return response

# Example usage
raise ToolError(
    code="FILE_NOT_FOUND",
    message="File 'config.json' not found at specified path",
    suggestion="Did you mean 'config/settings.json'? Use mcp__scout__search to find files."
)
```

## Como Aplicar

1. **Definir schema completo**
   ```python
   TOOL_SCHEMA = {
       "name": "mcp__scout__discover",
       "description": """
       Find files relevant to a natural language query.
       Returns paths with relevance scores.

       Use when:
       - You need to find files related to a task
       - You're exploring the codebase
       - You need context for an agent

       Examples:
       - discover("create product listing") -> finds anuncio_agent files
       - discover("how to build agent") -> finds codexa_agent docs
       """,
       "parameters": {
           "type": "object",
           "required": ["query"],
           "properties": {
               "query": {
                   "type": "string",
                   "description": "Natural language query describing what you're looking for"
               },
               "agent": {
                   "type": "string",
                   "description": "Optional: limit search to specific agent"
               },
               "max_results": {
                   "type": "integer",
                   "default": 10,
                   "description": "Maximum results to return"
               }
           }
       }
   }
   ```

2. **Implementar handler robusto**
   ```python
   async def handle_discover(params: dict) -> dict:
       # Validate required params
       query = params.get("query")
       if not query:
           return error_response("MISSING_PARAM", "query is required")

       # Apply defaults
       agent = params.get("agent")
       max_results = params.get("max_results", 10)

       # Execute with error handling
       try:
           results = await search_engine.discover(query, agent, max_results)
       except SearchError as e:
           return error_response("SEARCH_FAILED", str(e))

       # Return structured response
       return {
           "success": True,
           "query": query,
           "results": [r.to_dict() for r in results],
           "total_found": len(results),
           "search_time_ms": results.duration_ms
       }
   ```

3. **Fornecer exemplos no description**
   ```python
   DESCRIPTION = """
   Search for files using glob patterns.

   Examples:
   - search("**/*.md") - all markdown files
   - search("**/prompts/*.md", type="hop") - HOP files only
   - search("config/*.json") - JSON configs

   Returns list of matching file paths with metadata.
   """
   ```

4. **Documentar retornos esperados**
   ```python
   RESPONSE_SCHEMA = {
       "type": "object",
       "properties": {
           "success": {"type": "boolean"},
           "results": {
               "type": "array",
               "items": {
                   "type": "object",
                   "properties": {
                       "path": {"type": "string"},
                       "relevance_score": {"type": "number"},
                       "category": {"type": "string"}
                   }
               }
           }
       }
   }
   ```

## Exemplos Praticos

### Exemplo 1: Tool com Defaults Inteligentes

**Tool**: `mcp__scout__smart_context`

**Schema**:
```json
{
  "name": "mcp__scout__smart_context",
  "parameters": {
    "required": ["agent"],
    "properties": {
      "agent": {
        "type": "string",
        "description": "Agent name (e.g., 'anuncio_agent')"
      },
      "max_files": {
        "type": "integer",
        "default": 20,
        "description": "Max files in must_read list"
      },
      "include_hints": {
        "type": "boolean",
        "default": true,
        "description": "Include LLM navigation hints"
      }
    }
  }
}
```

**Resultado**: LLM precisa especificar apenas o agent, defaults fazem o resto

### Exemplo 2: Error Response Actionable

**Cenario**: Usuario busca arquivo que nao existe

**Response**:
```json
{
  "error": true,
  "code": "NO_RESULTS",
  "message": "No files found matching query 'xyz_agent'",
  "suggestion": "Available agents: anuncio_agent, codexa_agent, photo_agent. Use mcp__scout__discover('list agents') for full list.",
  "searched_patterns": ["**/xyz_agent/**"],
  "search_time_ms": 45
}
```

**Resultado**: LLM sabe exatamente o que corrigir

## Quando Usar

- **USE descriptions detalhadas quando**:
  - Tool e complexa ou tem muitos parametros
  - Casos de uso nao sao obvios
  - Erros comuns precisam ser prevenidos

- **USE defaults quando**:
  - Valor comum cobre 80%+ dos casos
  - Parametro e otimizacao, nao semantica
  - Reduz fricao para LLM

- **USE enums quando**:
  - Valores possiveis sao finitos e conhecidos
  - Previne erros de typo
  - Guia LLM para escolhas validas

- **AVOID over-parameterization quando**:
  - Muitos parametros confundem LLM
  - Defaults podem cobrir casos raros
  - Simplicidade > flexibilidade

## Relacionado

- Ver tambem: `server_architecture.md`
- Spec: MCP Protocol Specification
- Implementacao: `mcp-servers/scout-mcp/index.js`

---

**Processado**: 2025-12-05
**Tokens**: ~1200
