# Pattern: Task Management

**Categoria**: Universal (Obrigatorio)
**Frequencia**: 97% das ferramentas analisadas
**Ultima Atualizacao**: 2025-12-02
**Quality Score**: 0.89

## Resumo Executivo

Task management permite que AI assistants planejem, rastreiem e executem tarefas complexas de forma sistematica. As implementacoes variam de todo lists simples a sistemas de planning com modos separados.

## Implementacoes por Ferramenta

### Claude Code (Anthropic)
**Abordagem**: TodoWrite tool com estados
```markdown
Task States:
- pending: Task not yet started
- in_progress: Currently working on (limit to ONE at a time)
- completed: Task finished successfully

Task fields:
- content: "Fix authentication bug"
- activeForm: "Fixing authentication bug"
- status: "in_progress"
```
**Regras**:
- Marcar tasks como completed IMEDIATAMENTE apos terminar
- Apenas UMA task in_progress por vez
- Usar para tarefas com 3+ passos

### Cursor
**Abordagem**: todo_write com merge flag
```typescript
type todo_write = (_: {
  merge: boolean,  // true = merge with existing, false = replace
  todos: Array<{
    content: string,
    status: "pending" | "in_progress" | "completed" | "cancelled",
    id: string
  }>
}) => any;
```
**Regras**:
- NUNCA incluir: linting, testing, searching (acoes operacionais)
- Criar todo como in_progress ao iniciar trabalho
- Batch tool calls com todo updates para latencia

### Devin
**Abordagem**: Planning Mode vs Standard Mode
```markdown
Planning Mode:
- Gather all information needed
- Search and understand codebase
- Use browser for missing info
- Call <suggest_plan /> when confident

Standard Mode:
- Execute plan steps
- Output actions for current/next steps
- Follow plan requirements
```
**Comandos**:
- `<suggest_plan/>` - Indica plano pronto
- `<think>` - Raciocinio antes de decisoes criticas

### Windsurf
**Abordagem**: update_plan tool persistente
```markdown
You will maintain a plan of action for the user's project.
This plan will be updated by the plan mastermind through
calling the update_plan tool.

Update when:
- New instructions from user
- Complete items from plan
- Learn info that changes scope/direction
```

### v0 (Vercel)
**Abordagem**: Todo Manager para refactoring
```markdown
*Calls Todo Manager to create a systematic refactoring plan:
"Update Core Auth Hook, Refactor Login Components,
Update Dashboard Components, Update API Integration,
Test Auth Flow"*
```

## Melhor Pratica Identificada

**Devin** oferece a abordagem mais sofisticada:
1. Separacao clara entre Planning e Execution
2. `<think>` tool para raciocinio explicito
3. Validacao obrigatoria antes de commit
4. Iteracao controlada (max 3 tentativas em CI)

## Como Implementar no CODEXA

```python
# Sistema de tarefas CODEXA
class TaskManager:
    STATES = ["pending", "in_progress", "completed", "blocked"]

    def create_task(self, content: str, priority: int = 1):
        return {
            "id": str(uuid4()),
            "content": content,
            "active_form": self._to_active_form(content),
            "status": "pending",
            "priority": priority,
            "created_at": datetime.now().isoformat()
        }

    def _to_active_form(self, content: str) -> str:
        # "Fix bug" -> "Fixing bug"
        # "Add feature" -> "Adding feature"
        verbs = {"Fix": "Fixing", "Add": "Adding", "Update": "Updating"}
        for v, gerund in verbs.items():
            if content.startswith(v):
                return content.replace(v, gerund, 1)
        return content + "..."

    def validate_single_in_progress(self, tasks: list) -> bool:
        in_progress = [t for t in tasks if t["status"] == "in_progress"]
        return len(in_progress) <= 1
```

## Quando Usar (Consenso das Ferramentas)

**USAR**:
- Tarefas com 3+ passos distintos
- Refactoring em multiplos arquivos
- Usuario fornece lista de tarefas
- Implementacao de features complexas

**NAO USAR**:
- Tarefas triviais (adicionar comentario, renomear variavel)
- Perguntas informacionais
- Comandos simples (npm install)
- Menos de 3 passos

## Variacoes Encontradas

| Ferramenta | Estados | Merge | Planning Mode |
|------------|---------|-------|---------------|
| Claude Code | 3 | N/A | Nao |
| Cursor | 4 | Sim | Nao |
| Devin | N/A | N/A | Sim (separado) |
| Windsurf | N/A | N/A | update_plan |
| v0 | N/A | N/A | Todo Manager |

---
**Fonte**: Analise profunda de 5 ferramentas AI (Claude Code, Cursor, Devin, Windsurf, v0)
**Quality Score**: 0.89/1.0
