# /flow - Task Execution Pipeline

Unified command for planning, executing, and templatizing tasks.

## PURPOSE

**Modes**: `plan` | `do` | `distill`

---

## USAGE

```
/flow plan "descrição da tarefa"    → Cria plano estruturado
/flow do                            → Executa plano aprovado
/flow do "tarefa direta"            → Executa sem plano prévio
/flow distill arquivo.md            → Transforma em template {{VARS}}
/flow auto "tarefa"                 → Loop completo (plan→do→distill)
```

---

## MODES

### MODE 1: PLAN

Cria plano estruturado antes de executar.

**Input**: Descrição da tarefa
**Output**: Plano com escopo, etapas, riscos, critérios

```markdown
## PLANO DE EXECUÇÃO

### ESCOPO
- O que SERÁ feito: [items]
- O que NÃO será feito: [limites]
- Premissas: [assumindo que...]

### ETAPAS
| # | Etapa | Ação | Entrega |
|---|-------|------|---------|
| 1 | Nome  | O que fazer | Output |

### RISCOS
| Risco | Impacto | Mitigação |
|-------|---------|-----------|

### CRITÉRIOS DE SUCESSO
- [ ] Critério 1
- [ ] Critério 2

---
AGUARDO: "ok" para executar | "ajusta X" para modificar
```

---

### MODE 2: DO

Executa tarefa e gera ativo.

**Input**: Plano aprovado OU tarefa direta
**Output**: Ativo específico (documento com dados reais)

```markdown
# [TÍTULO DO ATIVO]

**Criado**: [DATA]
**Versão**: 1.0
**Propósito**: [para que serve]

---

## CONTEÚDO

[resultado da execução]

---

## METADADOS
- Tipo: [Contexto | Template | Guia | Output]
- Domínio: [área]
- Reutilizável: Sim/Não

---
PRÓXIMO: "distill" para template | "handoff" para outro chat
```

---

### MODE 3: DISTILL

Transforma ativo específico em template universal.

**Input**: Arquivo com dados específicos
**Output**: Template com `{{PLACEHOLDERS}}`

**Substituições automáticas**:
| Específico | Placeholder |
|------------|-------------|
| Nome da marca | `{{BRAND_NAME}}` |
| URL do site | `{{BRAND_URL}}` |
| Cor primária (#hex) | `{{PRIMARY_COLOR}}` |
| Número de agents/features | `{{AGENT_COUNT}}` |
| Tagline/slogan | `{{TAGLINE}}` |
| Público-alvo | `{{TARGET_AUDIENCE}}` |
| Email de contato | `{{CONTACT_EMAIL}}` |

**Output format**:
```markdown
# [TÍTULO] - TEMPLATE

**Tipo**: Template Universal
**Versão**: 1.0
**Placeholders**: X variáveis

---

## CONTEÚDO

[conteúdo com {{VARS}} no lugar de dados específicos]

---

## VARIÁVEIS PARA PREENCHER

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| {{VAR_1}} | O que colocar | Exemplo |

---

## COMO USAR

1. Copie este template
2. Substitua {{VARIÁVEIS}} pelos seus dados
3. Use em qualquer LLM
```

---

## AUTO MODE

Loop completo com aprovações:

```
/flow auto "criar roteiro video LP"

┌─────────┐     ┌─────────┐     ┌─────────┐
│  PLAN   │ ──► │   DO    │ ──► │ DISTILL │
└─────────┘     └─────────┘     └─────────┘
     │               │               │
     ▼               ▼               ▼
  "ok?"           "ok?"          "ok?"
```

---

## INTEGRAÇÃO COM TASK TOOL

Para spawn via Task tool:

```javascript
Task(
  subagent_type="general-purpose",
  prompt="Execute /flow plan para: [descrição da tarefa]"
)
```

Paralelo (múltiplos flows):
```javascript
Task(subagent_type="general-purpose", prompt="/flow plan: tarefa 1")
Task(subagent_type="general-purpose", prompt="/flow plan: tarefa 2")
Task(subagent_type="general-purpose", prompt="/flow plan: tarefa 3")
// Todos executam em paralelo
```

---

## DETECÇÃO AUTOMÁTICA

O comando detecta o input e escolhe o modo:

| Input | Modo Detectado |
|-------|----------------|
| `"criar X"`, `"fazer Y"` | PLAN |
| `"ok"`, `"aprovado"`, plano colado | DO |
| `arquivo.md`, `"distill"` | DISTILL |
| ````handoff` block | Continua do handoff |

---

## EXAMPLES

```bash
# Planejar nova tarefa
/flow plan "criar roteiro video LP 10 minutos"

# Executar após aprovação
/flow do

# Executar tarefa direta (sem plano)
/flow do "listar arquivos do curso_agent"

# Transformar em template
/flow distill curso_agent/outputs/VIDEO_LP_CODEXA.md

# Loop completo automático
/flow auto "criar landing page para produto X"
```

---

**Version**: 1.0.0
**Created**: 2025-12-03
**Type**: Task Pipeline Command
