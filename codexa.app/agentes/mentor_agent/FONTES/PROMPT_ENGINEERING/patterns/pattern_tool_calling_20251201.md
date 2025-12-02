# Pattern: Tool Calling

**Categoria**: Universal (Obrigatorio)
**Frequencia**: 100% das ferramentas analisadas
**Ultima Atualizacao**: 2025-12-02
**Quality Score**: 0.92

## Resumo Executivo

Tool calling e o pattern mais fundamental em AI coding assistants. Todas as ferramentas analisadas implementam schemas tipados para chamadas de funcoes, com variacoes na sintaxe (JSON Schema vs XML vs TypeScript).

## Implementacoes por Ferramenta

### Claude Code (Anthropic)
**Abordagem**: JSON Schema com funcoes nomeadas
```json
{
  "name": "Edit",
  "parameters": {
    "file_path": {"type": "string", "required": true},
    "old_string": {"type": "string", "required": true},
    "new_string": {"type": "string", "required": true}
  }
}
```
**Destaque**: Parametros required explicitos, descricoes detalhadas por parametro.

### Cursor
**Abordagem**: TypeScript namespace com multi_tool_use
```typescript
namespace functions {
  type codebase_search = (_: {
    explanation: string,
    query: string,
    target_directories: string[],
  }) => any;
}

namespace multi_tool_use {
  type parallel = (_: {
    tool_uses: {recipient_name: string, parameters: object}[]
  }) => any;
}
```
**Destaque**: `multi_tool_use.parallel` para execucao simultanea.

### Devin
**Abordagem**: XML Commands com parametros inline
```xml
<shell id="shellId" exec_dir="/path/to/dir">
git status
</shell>

<str_replace path="/full/path/to/file">
<old_str>codigo antigo</old_str>
<new_str>codigo novo</new_str>
</str_replace>
```
**Destaque**: Separacao clara entre shell, editor, browser commands.

### Windsurf
**Abordagem**: Function calling padrao com explicacao obrigatoria
```
Before calling each tool, first explain why you are calling it.
```
**Destaque**: Explicacao obrigatoria antes de cada chamada.

### v0 (Vercel)
**Abordagem**: Subagents + CodeProject blocks
```markdown
*Calls SearchRepo to get an overview of the codebase*
*Calls GenerateDesignInspiration with goal: "Landing page"*
```
**Destaque**: Subagents especializados (SearchRepo, GenerateDesignInspiration).

## Melhor Pratica Identificada

**Cursor** oferece a implementacao mais completa:
1. Schema tipado com TypeScript
2. Execucao paralela via `multi_tool_use.parallel`
3. Parametros com descricoes e exemplos
4. Output modes configuraves (content, files_with_matches, count)

## Como Implementar no CODEXA

```python
# Schema de ferramenta CODEXA
TOOL_SCHEMA = {
    "name": "buscar_conhecimento",
    "description": "Busca no catalogo de conhecimento do mentor",
    "parameters": {
        "type": "object",
        "required": ["query"],
        "properties": {
            "query": {
                "type": "string",
                "description": "Pergunta em linguagem natural"
            },
            "categorias": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Filtrar por categorias especificas"
            },
            "nivel": {
                "type": "string",
                "enum": ["basico", "intermediario", "avancado"]
            }
        }
    }
}
```

## Exemplos de Codigo

### Chamada Simples (Claude Code)
```
<function_calls>
<invoke name="Read">
<parameter name="file_path">/path/to/file.py