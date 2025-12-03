# Scout Integration Guide

> Como todos os agentes CODEXA podem usar o Scout MCP Server para descoberta de arquivos

---

## O Que é Scout?

**Scout** é um MCP Server que roda em background e fornece ferramentas de descoberta de arquivos para TODOS os agentes.

```
┌─────────────────────────────────────────────────────────┐
│                    CLAUDE CODE                           │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐               │
│  │ anuncio  │  │ pesquisa │  │  marca   │  ...          │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘               │
│       │             │             │                      │
│       └─────────────┼─────────────┘                      │
│                     ▼                                    │
│         ┌─────────────────────┐                          │
│         │  mcp__scout__*      │  ◄── Ferramentas         │
│         │  (13 tools)         │      disponíveis         │
│         └─────────────────────┘      para todos          │
└─────────────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              SCOUT MCP SERVER (Background)               │
│                                                          │
│  - Indexa 11.000+ arquivos automaticamente              │
│  - Responde queries em <100ms                           │
│  - CRUD com backups automáticos                         │
└─────────────────────────────────────────────────────────┘
```

---

## Quando Scout Está Ativo?

| Condição | Scout Ativo? |
|----------|--------------|
| Claude Code aberto em `codexa.app/` | ✅ Sim |
| Claude Code aberto em outro projeto | ❌ Não |
| Configuração em `.claude/settings.json` existe | ✅ Sim |
| Node.js não instalado | ❌ Não |
| Primeiro uso (índice não construído) | ✅ Sim (constrói em ~3s) |

### Como Verificar se Scout Está Ativo

```javascript
// Se retornar estatísticas, está ativo
mcp__scout__stats()

// Esperado:
// { total_files: 11741, by_category: {...}, by_agent: {...} }
```

---

## Ferramentas Disponíveis

### Discovery (Mais Usadas)

| Ferramenta | Uso | Exemplo |
|------------|-----|---------|
| `mcp__scout__discover(query)` | Busca por linguagem natural | `discover("criar anuncio")` |
| `mcp__scout__smart_context(agent)` | Contexto inteligente LLM-otimizado | `smart_context("anuncio_agent")` |
| `mcp__scout__agent_context(agent)` | Todos arquivos de um agente | `agent_context("anuncio_agent")` |
| `mcp__scout__search(pattern)` | Busca por glob pattern | `search("**/*_HOP.md")` |

### CRUD (Operações de Arquivo)

| Ferramenta | Uso | Nota |
|------------|-----|------|
| `mcp__scout__create(path, content)` | Criar arquivo | Auto-indexa |
| `mcp__scout__read(path)` | Ler com metadata | Inclui categoria |
| `mcp__scout__update(path, content)` | Atualizar | Cria backup .bak |
| `mcp__scout__delete(path, confirm)` | Deletar | Requer confirm=true |
| `mcp__scout__move(from, to)` | Mover/renomear | Atualiza índice |

### Index & Validation

| Ferramenta | Uso |
|------------|-----|
| `mcp__scout__refresh()` | Reconstruir índice |
| `mcp__scout__stats()` | Estatísticas do índice |
| `mcp__scout__validate_paths(paths[])` | Verificar se paths existem |
| `mcp__scout__map_dependencies(file)` | Encontrar dependências |
| `mcp__scout__related(file)` | Encontrar arquivos relacionados |

---

## Instruções para Agentes

### QUANDO Usar Scout

```
✅ USE Scout quando:
- Precisar encontrar arquivos relevantes para uma tarefa
- Não souber onde um arquivo está
- Precisar listar todos arquivos de um agente
- Quiser verificar se um path existe
- Precisar criar/atualizar arquivos com tracking

❌ NÃO USE Scout quando:
- Já souber o path exato (use Read/Write direto)
- For operação simples de leitura
- Scout não estiver ativo (verifique com stats())
```

### COMO Usar Scout (Padrão Recomendado)

```javascript
// 1. ANTES de iniciar uma tarefa, descubra arquivos relevantes
const files = await mcp__scout__discover("sua tarefa aqui");

// 2. Para contexto INTELIGENTE (LLM-otimizado, priorizado)
const smart = await mcp__scout__smart_context("nome_agent");
// Retorna: { must_read: [...], should_read: [...], optional: [...], hints: "..." }

// 3. Para contexto completo de um agente (todos os arquivos)
const context = await mcp__scout__agent_context("nome_agent");

// 4. Para buscar padrões específicos
const hops = await mcp__scout__search("**/*_HOP.md");

// 5. Para operações de arquivo com tracking
await mcp__scout__create("path/file.md", "conteudo");
await mcp__scout__update("path/file.md", "novo conteudo"); // cria backup
```

---

## Best Practices

### Use smart_context para Navegação Eficiente

`mcp__scout__smart_context(agent)` retorna arquivos **priorizados** e **otimizados para LLMs**:

```javascript
{
  "must_read": [
    "agentes/anuncio_agent/PRIME.md",           // Critical: Start here
    "agentes/anuncio_agent/INSTRUCTIONS.md"      // Critical: How to operate
  ],
  "should_read": [
    "agentes/anuncio_agent/workflows/100_ADW_RUN_ANUNCIO.md",  // High priority
    "agentes/anuncio_agent/prompts/10_HOP_*.md"                 // Domain prompts
  ],
  "optional": [
    "agentes/anuncio_agent/iso_vectorstore/*.md"  // Reference material
  ],
  "hints": "Start with PRIME.md for identity, then INSTRUCTIONS.md for operations..."
}
```

**Quando usar smart_context:**
- Primeira vez explorando um agente
- Precisa entender rapidamente o que um agente faz
- Quer contexto mínimo mas suficiente (não todos os arquivos)

**Quando usar agent_context:**
- Precisa de TODOS os arquivos do agente
- Fazendo análise profunda ou refatoração
- Precisa de arquivos de configuração e dependências

---

## Integração por Agente

### Para anuncio_agent
```javascript
// PREFERIDO: Contexto inteligente e priorizado
mcp__scout__smart_context("anuncio_agent")

// Descobrir arquivos de pesquisa para gerar anúncio
mcp__scout__discover("research notes produto")
mcp__scout__agent_context("pesquisa_agent") // dependência
```

### Para pesquisa_agent
```javascript
// PREFERIDO: Contexto inteligente e priorizado
mcp__scout__smart_context("pesquisa_agent")

// Descobrir configurações de marketplace
mcp__scout__search("**/marketplace*.json")
mcp__scout__discover("competitor analysis")
```

### Para marca_agent
```javascript
// PREFERIDO: Contexto inteligente e priorizado
mcp__scout__smart_context("marca_agent")

// Descobrir arquivos de identidade
mcp__scout__discover("brand identity archetype")
mcp__scout__search("**/brand*.json")
```

### Para codexa_agent
```javascript
// PREFERIDO: Contexto inteligente e priorizado
mcp__scout__smart_context("codexa_agent")

// Meta-construção: descobrir builders e validators
mcp__scout__search("**/builders/*.py")
mcp__scout__search("**/validators/*.py")
```

---

## Fallback (Se Scout Não Estiver Ativo)

Se `mcp__scout__stats()` falhar, use ferramentas nativas:

```javascript
// Alternativa para discover
Glob({ pattern: "**/*.md" })
Grep({ pattern: "keyword" })

// Alternativa para agent_context
Glob({ pattern: "agentes/nome_agent/**/*" })

// Alternativa para search
Glob({ pattern: "**/*_HOP.md" })
```

---

## Configuração

Scout está configurado em `.claude/settings.json`:

```json
{
  "mcpServers": {
    "scout": {
      "command": "node",
      "args": ["mcp-servers/scout-mcp/index.js"],
      "env": {
        "SCOUT_ROOT": "."
      }
    }
  }
}
```

### Requisitos
- Node.js >= 18.x
- Diretório `mcp-servers/scout-mcp/` com `index.js`
- Claude Code iniciado no diretório do projeto

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| `mcp__scout__*` não disponível | Verificar `.claude/settings.json` e reiniciar Claude Code |
| Resultados desatualizados | Executar `mcp__scout__refresh()` |
| Arquivos não encontrados | Verificar `SCOUT_ROOT` no settings.json |
| Performance lenta | Normal no primeiro uso (~3s para indexar) |

---

## Referências

- **Scout PRIME**: `agentes/scout_agent/PRIME.md`
- **Scout INSTRUCTIONS**: `agentes/scout_agent/INSTRUCTIONS.md`
- **Scout SETUP**: `agentes/scout_agent/SETUP.md`
- **MCP Server**: `mcp-servers/scout-mcp/`

---

**Versão**: 1.1.0
**Última Atualização**: 2025-12-03
**Aplicável a**: Todos os agentes CODEXA

## Changelog

- **v1.1.0** (2025-12-03): Added `smart_context` function documentation with LLM-optimized context
- **v1.0.0** (2025-11-29): Initial version
