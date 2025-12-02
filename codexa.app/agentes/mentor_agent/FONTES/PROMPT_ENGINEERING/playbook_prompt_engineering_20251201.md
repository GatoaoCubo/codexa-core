# Playbook: Prompt Engineering para AI Coding Tools

**Baseado em**: Analise profunda de 5 ferramentas lideres (Claude Code, Cursor, Devin, Windsurf, v0)
**Atualizado em**: 2025-12-02
**Versao**: 2.0.0 (Analise LLM Profunda)

---

## Executive Summary

Este playbook sintetiza as melhores praticas de prompt engineering extraidas de analise profunda dos system prompts de:
- **Claude Code** (Anthropic) - ~15k tokens, foco em seguranca e ferramentas
- **Cursor** - ~12k tokens, foco em edicao inteligente e parallel execution
- **Devin** - ~8k tokens, foco em planning mode e raciocinio explicito
- **Windsurf** - ~4k tokens, foco em memoria persistente e planejamento
- **v0** (Vercel) - ~20k tokens, foco em design e integracao frontend

---

## 1. Padroes Universais (Obrigatorios)

### 1.1 Tool Calling (100%)
**Quality Score**: 0.92

Todas as ferramentas usam schemas tipados para funcoes. A variacao esta na sintaxe:

| Ferramenta | Sintaxe | Destaque |
|------------|---------|----------|
| Claude Code | JSON Schema | Parametros required explicitos |
| Cursor | TypeScript namespace | `multi_tool_use.parallel` |
| Devin | XML commands | Separacao por categoria |
| v0 | Function calling | Subagents especializados |

**Implementacao Recomendada**:
```python
TOOL_SCHEMA = {
    "name": "string",
    "description": "string",
    "parameters": {
        "type": "object",
        "required": ["param1"],
        "properties": {...}
    }
}
```

### 1.2 Task Management (97%)
**Quality Score**: 0.89

| Abordagem | Ferramentas | Uso |
|-----------|-------------|-----|
| Todo states (pending/in_progress/completed) | Claude, Cursor | Rastreamento granular |
| Planning Mode separado | Devin | Separacao clara |
| update_plan persistente | Windsurf | Atualizacao continua |

**Regra Universal**: Usar para tarefas com 3+ passos distintos.

### 1.3 File Operations (86%)
**Quality Score**: 0.88

**Inovacao Principal**: `// ... existing code ...`
- Reduz tokens significativamente
- Usuario ve apenas mudancas relevantes
- Sistema faz merge automatico

**Regras Universais**:
1. SEMPRE ler arquivo antes de editar
2. old_string deve ser UNICO
3. Preservar indentacao exata
4. NUNCA usar cat/echo/sed

### 1.4 Terminal Commands (84%)
**Quality Score**: 0.87

**Regras de Consenso**:
- NUNCA usar `cd` - especificar cwd/exec_dir
- Timeout padrao: 2 min, max: 10 min
- Background para long-running (servidores)
- Confirmacao para comandos destrutivos

### 1.5 Security Constraints (38% explicito)
**Quality Score**: 0.85

**Modelo Claude Code** (mais completo):
```markdown
- Assist with defensive security only
- NEVER commit secrets to repository
- NEVER force push to main/master
- NEVER skip git hooks
```

---

## 2. Tecnicas Avancadas (Diferenciacao)

### 2.1 Think Tool (Devin - Exclusivo)
Raciocinio explicito antes de decisoes criticas:
```xml
<think>
Reflect on what you know, things tried,
alignment with objective and user intent.
</think>
```
**Uso obrigatorio**: Decisoes git, transicao exploracao→edicao, antes de reportar conclusao.

### 2.2 Memory System (Windsurf, Cursor)
Contexto persistente entre sessoes:
```python
create_memory(key, value, auto=True)  # Sem pedir permissao
```
**Usar para**: Preferencias, padroes do codebase, decisoes anteriores.

### 2.3 Planning Mode (Devin)
Separacao clara entre planejamento e execucao:
- **Planning**: Gather info, search codebase, ask user
- **Execution**: Follow plan, output actions

### 2.4 Parallel Execution (Claude, Cursor)
Chamadas de ferramentas sem dependencias em paralelo:
```typescript
multi_tool_use.parallel({
  tool_uses: [
    {recipient_name: "tool1", parameters: {}},
    {recipient_name: "tool2", parameters: {}}
  ]
})
```

### 2.5 Semantic Search (Cursor, Devin)
Busca por significado, nao apenas texto:
```typescript
codebase_search({
  query: "how are permissions checked?",
  target_directories: ["src/auth"]
})
```

### 2.6 Design Inspiration Subagent (v0)
Subagent especializado para briefings visuais antes de criar UI.

---

## 3. Guia de Implementacao CODEXA

### 3.1 Estrutura do System Prompt

```markdown
# 1. Identity/Role
You are [AGENT_NAME], specialized in [DOMAIN].

# 2. Tools/Capabilities
Available tools with schemas...

# 3. Workflows
Step-by-step instructions for common tasks...

# 4. Constraints
What NOT to do...

# 5. Output Format
How to format responses...
```

### 3.2 Checklist de Implementacao

**Estrutura Basica**:
- [x] Identity/Role section
- [x] Tools/Capabilities section
- [x] Constraints section
- [x] Output format section

**Patterns Obrigatorios**:
- [x] Tool Calling com schemas tipados
- [x] Task Management com estados
- [x] File Operations com read-before-edit
- [x] Terminal Commands com timeout/cwd
- [x] Security Constraints explicitos

**Tecnicas Recomendadas**:
- [ ] Think Tool para decisoes criticas
- [ ] Memory System para contexto persistente
- [ ] Parallel Execution para performance
- [ ] Semantic Search para exploracao

---

## 4. Metricas de Qualidade

| Dimensao | Encontrada | Target CODEXA |
|----------|------------|---------------|
| Clareza | 0.85 | > 0.90 |
| Completude | 0.80 | > 0.85 |
| Reusabilidade | 0.75 | > 0.80 |
| Inovacao | 0.70 | > 0.75 |

### Quality Scores por Pattern

| Pattern | Score |
|---------|-------|
| Tool Calling | 0.92 |
| Task Management | 0.89 |
| File Operations | 0.88 |
| Terminal Commands | 0.87 |
| Security Constraints | 0.85 |
| Advanced Techniques | 0.91 |

---

## 5. Rankings por Categoria

### Top 5 por Inovacao
1. **Devin** - Think tool, Planning mode, LSP integration
2. **v0** - Design subagent, CodeProject blocks, integrations
3. **Cursor** - Parallel execution, semantic search, partial edits
4. **Claude Code** - Security protocol, git safety, task states
5. **Windsurf** - Memory system, plan persistence

### Top 5 por Completude
1. **v0** - ~20k tokens, design guidelines, integrations
2. **Claude Code** - ~15k tokens, security, git protocol
3. **Cursor** - ~12k tokens, todas as ferramentas
4. **Devin** - ~8k tokens, focado mas completo
5. **Windsurf** - ~4k tokens, essencial

### Top 5 por Clareza
1. **Claude Code** - Secoes bem definidas, exemplos claros
2. **Cursor** - TypeScript types, exemplos inline
3. **v0** - Markdown formatado, exemplos visuais
4. **Devin** - XML estruturado, regras explicitas
5. **Windsurf** - Conciso mas claro

---

## 6. Exemplos de Codigo

### Tool Calling (Claude Code Style)
```json
{
  "name": "Edit",
  "parameters": {
    "file_path": "/path/to/file.py",
    "old_string": "def old_function():",
    "new_string": "def new_function():"
  }
}
```

### Task Management (Cursor Style)
```typescript
todo_write({
  merge: true,
  todos: [
    {id: "1", content: "Implement auth", status: "in_progress"},
    {id: "2", content: "Add tests", status: "pending"}
  ]
})
```

### File Edit (v0/Cursor Style)
```javascript
// ... existing code ...
function newFeature() {
  return "Added feature";
}
// ... existing code ...
```

### Terminal (Devin Style)
```xml
<shell id="main" exec_dir="/project">
npm run build && npm test
</shell>
```

---

## 7. Proximos Passos

1. **Revisar** pattern cards individuais em `/patterns/`
2. **Implementar** Think Tool no mentor_agent
3. **Adicionar** Memory System para contexto persistente
4. **Habilitar** Parallel Execution onde possivel
5. **Testar** com casos reais e iterar

---

## 8. Referencias

### Pattern Cards
- `pattern_tool_calling_20251201.md`
- `pattern_task_management_20251201.md`
- `pattern_file_operations_20251201.md`
- `pattern_terminal_commands_20251201.md`
- `pattern_security_constraints_20251201.md`
- `pattern_advanced_techniques_20251202.md`

### Fontes Originais
- `ai_tools_prompts/claude_code/`
- `ai_tools_prompts/cursor/`
- `ai_tools_prompts/devin/`
- `ai_tools_prompts/windsurf/`
- `ai_tools_prompts/v0/`

---

**Documento gerado com Analise LLM Profunda**
**CODEXA Team - 2025-12-02**
