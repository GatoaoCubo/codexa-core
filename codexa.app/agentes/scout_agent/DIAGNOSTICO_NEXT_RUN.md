# Diagnóstico Scout MCP - Próxima Run

## Mudanças Aplicadas (v1.1.0)

### 1. Auto-detecção do PROJECT_ROOT
- Agora detecta `codexa.gato/` automaticamente mesmo iniciando em subpastas
- Sobe na árvore procurando: `.git`, `PRIME.md`, `codexa.app`

### 2. Detecção de Agentes Flexível
- Aceita `_` e `-`: `scout_agent` = `scout-agent`
- Normaliza para underscore

### 3. Novas Categorias (11 adicionadas)
- `scripts`, `adw_code`, `voice`, `mcp`, `core`
- `api`, `server`, `html`, `css`, `landing`

### 4. Ignore Patterns Corrigidos
- Todos com `**/` prefix para capturar nested dirs

---

## Comandos de Diagnóstico

### Após reiniciar o Claude Code, execute:

```
# 1. Verificar stats do Scout
mcp__scout__stats()

# 2. Verificar se PROJECT_ROOT foi detectado corretamente
# (olhar logs do servidor no stderr)

# 3. Verificar distribuição de categorias
# Esperado: "other" deve ter diminuído significativamente de 9451

# 4. Testar detecção de agentes
mcp__scout__discover("scout agent files")
mcp__scout__agent_context("scout_agent")

# 5. Verificar novas categorias funcionando
mcp__scout__search("**/*.html")  # deve retornar como "html"
mcp__scout__search("**/mcp-servers/**/*.js")  # deve retornar como "mcp"
mcp__scout__search("**/voice/**/*.py")  # deve retornar como "voice"
```

---

## Métricas de Sucesso

| Métrica | Antes | Esperado Após |
|---------|-------|---------------|
| Arquivos "other" | 9451 | < 5000 |
| Categorias ativas | 32 | 43 |
| PROJECT_ROOT | cwd() | codexa.gato |
| Agentes detectados | 14 | 14+ |

---

## Se algo der errado

1. **PROJECT_ROOT errado**: Verificar logs de startup
2. **Categorias não aplicadas**: Reiniciar Claude Code completamente
3. **node_modules ainda indexado**: Verificar IGNORE_PATTERNS no index.js

---

## Arquivos Modificados

- `codexa.app/mcp-servers/scout-mcp/index.js` (v1.1.0)
- `codexa.app/agentes/scout_agent/config/categories.json` (v1.3.0)
- `codexa.app/agentes/scout_agent/config/ignore_patterns.json` (v1.1.0)
