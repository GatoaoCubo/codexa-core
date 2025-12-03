# /spawn - Parallel Agent Launcher

Lança múltiplos sub-agents em paralelo a partir de uma lista simples.

## PURPOSE

**Uso**: Humano escreve lista → LLM converte para Task tools paralelos

---

## USAGE

```
/spawn
1. [tipo]: [tarefa]
2. [tipo]: [tarefa]
3. [tipo]: [tarefa]
```

---

## TIPOS DISPONÍVEIS

| Tipo | subagent_type | Quando usar |
|------|---------------|-------------|
| `explore` | Explore | Buscar arquivos, entender codebase |
| `plan` | Plan | Planejar implementação |
| `guide` | claude-code-guide | Docs do Claude Code |
| (sem tipo) | general-purpose | Tarefas genéricas |

---

## EXAMPLES

### Exemplo 1: Busca Paralela

```
/spawn
1. explore: encontrar arquivos de video LP
2. explore: encontrar templates de roteiro
3. explore: encontrar HOPs do curso_agent
```

LLM executa 3 Task tools em paralelo, resultados voltam juntos.

### Exemplo 2: Misto

```
/spawn
1. explore: arquivos relacionados a flow
2. plan: implementar sistema de cache
3. guide: como usar hooks no Claude Code
```

### Exemplo 3: Com Flow

```
/spawn
1. flow plan: criar roteiro video LP
2. flow plan: criar visual prompts
3. explore: exemplos de roteiros existentes
```

### Exemplo 4: Tarefas Genéricas

```
/spawn
1. analisar estrutura do projeto
2. listar todos os comandos disponíveis
3. verificar dependências do package.json
```

(Sem tipo = general-purpose)

---

## SINTAXE

```
/spawn
[número]. [tipo]: [descrição da tarefa]
```

**Regras**:
- Cada linha = 1 sub-agent
- Tipo é opcional (default: general-purpose)
- Máximo recomendado: 10 paralelos
- Linhas vazias são ignoradas

---

## COMO FUNCIONA

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   HUMANO ESCREVE                        LLM CONVERTE                        │
│   ──────────────                        ────────────                        │
│                                                                             │
│   /spawn                                                                    │
│   1. explore: arquivos video      →     Task(subagent="Explore",            │
│   2. explore: arquivos curso            prompt="arquivos video")            │
│   3. plan: refatorar sistema                                                │
│                                         Task(subagent="Explore",            │
│                                         prompt="arquivos curso")            │
│                                                                             │
│                                         Task(subagent="Plan",               │
│                                         prompt="refatorar sistema")         │
│                                                                             │
│                                         // Todos em paralelo!               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## OUTPUT

Após execução, LLM retorna:

```markdown
## Resultados do /spawn (3 agents)

### 1. explore: arquivos video
- VIDEO_LP_CODEXA_10MIN.md
- TIMELINE_MASTER.md
- video_scripts/*.md

### 2. explore: arquivos curso
- curso_agent/PRIME.md
- curso_agent/outputs/*.md

### 3. plan: refatorar sistema
[Plano estruturado...]

---
Todos os 3 agents completaram em paralelo.
```

---

## INSTRUCTIONS FOR AI

Quando `/spawn` é chamado:

1. **Parse** a lista de tarefas
2. **Detecte** o tipo de cada linha:
   - `explore:` → subagent_type="Explore"
   - `plan:` → subagent_type="Plan"
   - `guide:` → subagent_type="claude-code-guide"
   - `flow plan:` → general-purpose com "/flow plan"
   - (sem prefixo) → subagent_type="general-purpose"

3. **Execute** todos os Task tools em UMA mensagem (paralelo)

4. **Colete** resultados e apresente organizados

### Código de Referência

```python
def parse_spawn(input):
    tasks = []
    for line in input.strip().split('\n'):
        if not line.strip() or line.startswith('/spawn'):
            continue

        # Remove número e ponto
        line = re.sub(r'^\d+\.\s*', '', line)

        # Detecta tipo
        if line.startswith('explore:'):
            tasks.append(('Explore', line[8:].strip()))
        elif line.startswith('plan:'):
            tasks.append(('Plan', line[5:].strip()))
        elif line.startswith('guide:'):
            tasks.append(('claude-code-guide', line[6:].strip()))
        elif line.startswith('flow'):
            tasks.append(('general-purpose', f'/flow {line[5:].strip()}'))
        else:
            tasks.append(('general-purpose', line.strip()))

    return tasks
```

---

## INTEGRAÇÃO

### Com /flow

```
/spawn
1. flow plan: criar roteiro video
2. flow plan: criar landing page
3. explore: exemplos existentes
```

### Com /handoff

```
/spawn
1. explore: contexto do trabalho anterior
2. plan: próximos passos baseado no handoff
```

---

## LIMITS

| Limite | Valor | Razão |
|--------|-------|-------|
| Max paralelo | ~10 | Performance |
| Timeout | 2 min/agent | Evitar travamento |
| Tipos | 4 | Disponíveis no Claude Code |

---

**Version**: 1.0.0
**Created**: 2025-12-03
**Type**: Parallel Agent Launcher
