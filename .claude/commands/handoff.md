# /handoff - Cross-Chat Transfer Protocol

## PURPOSE

Prepara saída estruturada para continuar trabalho em outro chat (sem contexto).

**Uso**: Final de sessão | Transferência para outro LLM | Documentação de progresso

---

## USAGE

```
/handoff                    → Gera handoff do trabalho atual
/handoff "contexto extra"   → Adiciona contexto específico
```

---

## OUTPUT FORMAT

Quando `/handoff` é chamado, gero este bloco:

````markdown
## HANDOFF - Transferência Cross-Chat

Cole este bloco inteiro no início do novo chat.

```handoff
contexto: [resumo do que foi feito nesta sessão]
arquivos_gerados:
  - path/arquivo1.md
  - path/arquivo2.md
arquivos_modificados:
  - path/arquivo3.md (o que mudou)
proximo: [próxima ação recomendada]
dados:
  - [info relevante 1]
  - [info relevante 2]
pendencias:
  - [o que ficou pendente]
qualidade: [score se aplicável]
```

### Contexto Expandido

[Explicação mais detalhada do que foi feito, decisões tomadas, e por quê]

### Arquivos Chave

| Arquivo | Propósito | Status |
|---------|-----------|--------|
| path/arquivo.md | O que faz | Completo/Parcial |

### Próximos Passos Sugeridos

1. [Passo 1]
2. [Passo 2]
3. [Passo 3]

---
**Gerado por**: /handoff
**Data**: [timestamp]
**Sessão**: [resumo em 1 linha]
````

---

## COMO O NOVO CHAT USA

### Opção 1: Cole Direto

```
Usuário: [cola o bloco handoff]

LLM: Entendi o contexto. Você estava trabalhando em [X].
     Próximo passo sugerido: [Y].
     Quer que eu continue?
```

### Opção 2: Com Nova Instrução

```
Usuário:
[cola handoff]

Agora quero: [nova tarefa relacionada]
```

### Opção 3: Via /flow

```
Usuário:
/flow do

```handoff
contexto: ...
proximo: criar visual prompts
```

LLM detecta handoff e continua automaticamente.
```

---

## DETECÇÃO AUTOMÁTICA

O sistema detecta `\`\`\`handoff` e entende que:

1. Há contexto prévio de outra sessão
2. Deve ler arquivos mencionados se necessário
3. A próxima ação está sugerida
4. Pode continuar sem perguntas básicas

---

## INTEGRAÇÃO COM /flow

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   CHAT 1                           CHAT 2                       │
│   ──────                           ──────                       │
│                                                                 │
│   /flow plan "tarefa"              [cola handoff]               │
│        ↓                                 ↓                      │
│   /flow do                         /flow do                     │
│        ↓                                 ↓                      │
│   [ativo gerado]                   [continua trabalho]          │
│        ↓                                 ↓                      │
│   /handoff ─────────────────────► ```handoff                    │
│                                    contexto: ...                │
│                   COPIA            ```                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## QUANDO USAR

| Situação | Use /handoff? |
|----------|---------------|
| Terminou tarefa, vai continuar depois | Sim |
| Vai passar para outro LLM (GPT→Claude) | Sim |
| Contexto ficou muito grande | Sim |
| Quer documentar progresso | Sim |
| Tarefa simples, não precisa continuar | Não |

---

## EXEMPLO REAL

```
Usuário: /handoff

LLM gera:

## HANDOFF - Transferência Cross-Chat

Cole este bloco inteiro no início do novo chat.

```handoff
contexto: Criado roteiro de vídeo LP CODEXA 10min com 5 seções
arquivos_gerados:
  - curso_agent/outputs/VIDEO_LP_CODEXA_10MIN_V2.md
  - curso_agent/outputs/TIMELINE_MASTER.md
arquivos_modificados:
  - nenhum
proximo: Gerar visual prompts para Midjourney de cada seção
dados:
  - 5 seções: hook, problema, solução, prova, cta
  - duração total: 10min
  - tom: disruptivo-sofisticado
pendencias:
  - Validar roteiro com stakeholder
qualidade: 8.5/10
```

### Contexto Expandido

Nesta sessão criamos o roteiro completo do vídeo principal
da Landing Page CODEXA. O vídeo tem 10 minutos divididos em
5 seções seguindo a estrutura clássica de VSL...

### Arquivos Chave

| Arquivo | Propósito | Status |
|---------|-----------|--------|
| VIDEO_LP_CODEXA_10MIN_V2.md | Roteiro completo | Completo |
| TIMELINE_MASTER.md | Breakdown por segundo | Completo |

### Próximos Passos Sugeridos

1. Revisar roteiro (validação humana)
2. Gerar visual prompts para cada seção
3. Criar storyboard visual

---
**Gerado por**: /handoff
**Data**: 2025-12-03
**Sessão**: Roteiro vídeo LP 10min
```

---

## SPAWN VIA TASK

```javascript
// No final de uma tarefa complexa
Task(
  subagent_type="general-purpose",
  prompt="Execute /handoff para documentar o trabalho feito"
)
```

---

**Version**: 1.0.0
**Created**: 2025-12-03
**Type**: Cross-Chat Transfer Protocol
