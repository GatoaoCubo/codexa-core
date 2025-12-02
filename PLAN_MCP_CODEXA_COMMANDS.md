# PLANO: MCP codexa-commands

**Objetivo**: Criar MCP Server que permite agentes descobrirem e executarem seus próprios commands de forma fractal e autônoma.

**Problema**: Claude Code só detecta `.claude/commands/` na raiz. Commands distribuídos em `agentes/*/commands/` não são detectados.

**Solução**: MCP Server que escaneia dinamicamente e expõe commands como tools.

---

## ARQUITETURA

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        MCP codexa-commands v1.0.0                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DESCOBERTA DINÂMICA                                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Scan: codexa.app/agentes/*/commands/*.md                            │   │
│  │       codexa.app/.claude/commands/*.md                              │   │
│  │                                                                     │   │
│  │ Parse: Extrai metadata do markdown                                  │   │
│  │   - Título (# heading)                                              │   │
│  │   - Descrição (primeiro parágrafo)                                  │   │
│  │   - Argumentos ($ARGUMENTS, $1, $2)                                 │   │
│  │   - Agente (detectado do path)                                      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  TOOLS EXPOSTAS                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                                                                     │   │
│  │  mcp__codexa__list_commands                                         │   │
│  │  ├─ Retorna: todos commands disponíveis                             │   │
│  │  ├─ Filtro: por agente, categoria                                   │   │
│  │  └─ Output: { agent, command, description, path }[]                 │   │
│  │                                                                     │   │
│  │  mcp__codexa__get_command                                           │   │
│  │  ├─ Input: agent, command_name                                      │   │
│  │  ├─ Retorna: conteúdo completo do .md                               │   │
│  │  └─ Output: { content, metadata, arguments }                        │   │
│  │                                                                     │   │
│  │  mcp__codexa__agent_commands                                        │   │
│  │  ├─ Input: agent_name                                               │   │
│  │  ├─ Retorna: todos commands do agente específico                    │   │
│  │  └─ Output: { commands[], entry_point, prime_path }                 │   │
│  │                                                                     │   │
│  │  mcp__codexa__execute_prompt                                        │   │
│  │  ├─ Input: agent, command, arguments                                │   │
│  │  ├─ Retorna: prompt expandido com argumentos                        │   │
│  │  └─ Output: { expanded_prompt, context_files[] }                    │   │
│  │                                                                     │   │
│  │  mcp__codexa__refresh                                               │   │
│  │  ├─ Rebuild index de commands                                       │   │
│  │  └─ Output: { total_commands, by_agent }                            │   │
│  │                                                                     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  INTEGRAÇÃO COM SCOUT                                                       │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ Usa scout para descobrir arquivos de contexto                       │   │
│  │ Complementa smart_context com commands disponíveis                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ESTRUTURA DE ARQUIVOS

```
codexa.app/mcp-servers/codexa-commands/
├── index.js              # MCP Server principal
├── package.json          # Dependências
├── lib/
│   ├── scanner.js        # Escaneia diretórios por commands
│   ├── parser.js         # Parse markdown → metadata
│   └── expander.js       # Expande prompts com argumentos
└── test/
    └── test_commands.js  # Testes básicos
```

---

## FLUXO DE USO

```
┌─────────────────────────────────────────────────────────────────┐
│ AGENTE QUER SABER SEUS COMMANDS                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. Claude chama: mcp__codexa__agent_commands("anuncio_agent")   │
│                                                                 │
│ 2. MCP retorna:                                                 │
│    {                                                            │
│      "agent": "anuncio_agent",                                  │
│      "commands": [                                              │
│        { "name": "anuncio", "description": "Gera anúncio..." }, │
│      ],                                                         │
│      "prime_path": "agentes/anuncio_agent/PRIME.md"             │
│    }                                                            │
│                                                                 │
│ 3. Claude sabe exatamente o que o agente pode fazer             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ AGENTE QUER EXECUTAR COMMAND                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ 1. Claude chama: mcp__codexa__get_command("curso_agent",        │
│                                            "curso-outline")     │
│                                                                 │
│ 2. MCP retorna conteúdo completo do markdown                    │
│                                                                 │
│ 3. Claude executa as instruções do prompt                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## IMPLEMENTAÇÃO

### Fase 1: Setup (10 min)

```bash
# Criar estrutura
mkdir -p codexa.app/mcp-servers/codexa-commands/lib
mkdir -p codexa.app/mcp-servers/codexa-commands/test

# Inicializar package.json
cd codexa.app/mcp-servers/codexa-commands
npm init -y
npm install @modelcontextprotocol/sdk glob
```

### Fase 2: Scanner (scanner.js)

```javascript
// Escaneia diretórios por commands
// Paths:
//   - codexa.app/agentes/*/commands/*.md
//   - codexa.app/.claude/commands/*.md

export async function scanCommands(rootPath) {
  const commands = [];

  // 1. Agent-level commands
  const agentPattern = 'agentes/*/commands/*.md';
  // glob and parse

  // 2. Global commands
  const globalPattern = '.claude/commands/*.md';
  // glob and parse

  return commands;
}
```

### Fase 3: Parser (parser.js)

```javascript
// Extrai metadata do markdown
export function parseCommand(content, filePath) {
  return {
    name: extractName(filePath),      // nome do arquivo sem .md
    title: extractTitle(content),      // # heading
    description: extractDesc(content), // primeiro parágrafo
    arguments: extractArgs(content),   // $ARGUMENTS, $1, $2
    agent: detectAgent(filePath),      // do path
    path: filePath,
  };
}
```

### Fase 4: MCP Server (index.js)

```javascript
// Baseado no scout-mcp
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';

// Tools:
// - list_commands
// - get_command
// - agent_commands
// - execute_prompt
// - refresh
```

### Fase 5: Integração (settings.json)

```json
{
  "mcpServers": {
    "codexa-commands": {
      "command": "node",
      "args": ["codexa.app/mcp-servers/codexa-commands/index.js"],
      "env": {
        "CODEXA_ROOT": "."
      }
    }
  }
}
```

---

## COMMANDS DISPONÍVEIS (Atual)

### Global (codexa.app/.claude/commands/) - 26 arquivos

| Categoria | Commands |
|-----------|----------|
| **Navigation** | prime, adw-list |
| **Domain Specialists** | prime-anuncio, prime-codexa, prime-marca, prime-mentor, prime-pesquisa, prime-photo, prime-scout, prime-video |
| **Meta-Construction** | codexa-build-agent, codexa-build-command, codexa-build-mcp, codexa-build-prompt, codexa-build-schema, codexa-cleanup, codexa-orchestrate, codexa-when-to-use |
| **Voice** | v, vstart, vstop, vstatus, vgui, video |

### Agent-Level (agentes/*/commands/) - 23 arquivos

| Agent | Commands |
|-------|----------|
| **codexa_agent** (12) | codexa, codexa-quick, codexa-run, orchestrator, 90-codexa-when-to-use, 91-codexa-build-agent, 92-codexa-build-command, 93-codexa-build-mcp, 94-codexa-build-prompt, 95-codexa-build-schema, 96-codexa-orchestrate, 98-codexa-cleanup |
| **anuncio_agent** (1) | anuncio |
| **mentor_agent** (1) | mentor |
| **pesquisa_agent** (2) | pesquisa, update-competitor-docs |
| **curso_agent** (7) | curso-outline, curso-package, curso-sales, curso-script, curso-validate, curso-workbook |

---

## PROMPT PARA NOVO CHAT

```markdown
# MISSÃO: Implementar MCP codexa-commands

## CONTEXTO
Leia estes arquivos na ordem:
1. PLAN_MCP_CODEXA_COMMANDS.md (este plano)
2. codexa.app/mcp-servers/scout-mcp/index.js (padrão a seguir)
3. codexa.app/.claude/settings.json (configuração MCP)

## TAREFA
Implementar o MCP Server seguindo a arquitetura definida no plano.

## ENTREGÁVEIS
1. codexa.app/mcp-servers/codexa-commands/package.json
2. codexa.app/mcp-servers/codexa-commands/index.js
3. Atualizar .claude/settings.json (raiz) com novo MCP
4. Corrigir paths antigos (codexa.gato → codexa-core)

## RESTRIÇÕES
- Seguir padrão do scout-mcp (ES modules, SDK oficial)
- Não modificar arquivos existentes além do settings.json
- Testar conexão antes de declarar sucesso

## VALIDAÇÃO
Após implementar, executar:
- node codexa.app/mcp-servers/codexa-commands/index.js (deve iniciar sem erros)
- Verificar que tools aparecem no Claude Code
```

---

## PROBLEMAS A CORRIGIR (BONUS)

### settings.json com paths errados

**Atual** (ERRADO):
```json
"SCOUT_ROOT": "C:/Users/Dell/Documents/GitHub/connect-my-github/codexa.gato"
```

**Correto**:
```json
"SCOUT_ROOT": "C:/Users/Dell/Documents/GitHub/codexa-core"
```

Todos os paths precisam ser atualizados de `codexa.gato` para `codexa-core`.

---

## SPAWN AGENTS

Para executar em paralelo:

```
AGENT 1 (Explore): Validar estrutura atual de commands
AGENT 2 (Plan): Revisar arquitetura MCP proposta
AGENT 3 (General): Implementar scanner.js + parser.js
AGENT 4 (General): Implementar index.js principal
AGENT 5 (General): Integrar settings.json e testar
```

---

**Versão**: 1.0.0
**Data**: 2025-12-02
**Status**: Pronto para execução
