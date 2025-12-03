# CLAUDE.md - Project Laws & AI Instructions

**Auto-loaded by Claude Code** - These are fundamental laws that apply to ALL operations in this project.

---

## LAW 1: DISTILLATION PRINCIPLE

> **"Todo documento criado deve ser um template universal."**

### The Law

Documents created by domain agents (anuncio, pesquisa, marca, photo, video, curso) MUST be **distilled** to remove brand-specific content and create reusable templates for ANY business/brand/user/LLM.

### Why This Matters

```
SPECIFIC (Locked)              TEMPLATE (Universal)
┌────────────────────┐         ┌────────────────────┐
│ "codexa.app"       │   →     │ {{BRAND_URL}}      │
│ #0D9488 (teal)     │   →     │ {{PRIMARY_COLOR}}  │
│ "6 agentes CODEXA" │   →     │ {{AGENT_COUNT}}    │
└────────────────────┘         └────────────────────┘

Specific = Works for 1 brand
Template = Works for ANY brand
```

### Process

```
1. CREATE    → Domain agent creates document for specific brand
2. DISTILL   → Replace specifics with {{PLACEHOLDERS}}
3. HYDRATE   → New brand fills placeholders
4. DEPLOY    → Document works for new brand
```

### Standard Placeholders (Mustache Format)

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{BRAND_NAME}}` | Company/product name | CODEXA, Nike, etc. |
| `{{BRAND_URL}}` | Main website URL | codexa.app |
| `{{PRIMARY_COLOR}}` | Brand primary color (hex) | #0D9488 |
| `{{SECONDARY_COLOR}}` | Brand secondary color | #14B8A6 |
| `{{ACCENT_COLOR}}` | Accent/CTA color | #F59E0B |
| `{{LOGO_PATH}}` | Path to logo asset | /assets/logo.svg |
| `{{TAGLINE}}` | Brand tagline/slogan | "Build the builder" |
| `{{TARGET_AUDIENCE}}` | Primary audience | "e-commerce sellers" |
| `{{PRODUCT_CATEGORY}}` | Main product category | "AI tools" |
| `{{AGENT_COUNT}}` | Number of agents/features | 6, 12, etc. |
| `{{CTA_TEXT}}` | Call-to-action text | "Start now" |
| `{{CONTACT_EMAIL}}` | Contact email | hello@brand.com |

### Trigger

Use `/codexa-distill <path>` to process documents:

```bash
# Single file
/codexa-distill curso_agent/context/VISUAL_STYLE_CODEXA.md

# Entire folder
/codexa-distill curso_agent/context/video_tutorials/

# All context files
/codexa-distill curso_agent/context/
```

### Output

Documents are **replaced in-place** as templates. The original specific content is converted to placeholders.

### Validation

A distilled document MUST:
- [ ] Have NO hardcoded brand names (except in examples marked `<!-- EXAMPLE -->`)
- [ ] Have NO hardcoded URLs
- [ ] Have NO hardcoded colors
- [ ] Use ONLY standard placeholders from the table above
- [ ] Be usable by ANY brand after hydration

---

## LAW 2: FRACTAL NAVIGATION

> **"Each level reflects the structure below."**

Every directory follows the same pattern:
```
PRIME.md        → Entry point (what is this?)
INSTRUCTIONS.md → How to use (operations)
README.md       → Documentation (details)
```

Navigate with `/prime-*` commands.

---

## LAW 3: META-CONSTRUCTION

> **"Build the thing that builds the thing."**

1. **Meta > Instance** - Build builders, not artifacts
2. **Templates > One-offs** - Reusable patterns
3. **Discovery-First** - Find before building
4. **Quality Gates** - Validate every phase (≥7.0/10.0)

---

## LAW 4: AGENTIC DESIGN

> **"Agents are autonomous specialists."**

Each agent has:
- **Domain** - What it knows
- **Workflows (ADWs)** - What it does
- **Prompts (HOPs)** - How it thinks
- **Outputs** - What it produces

---

## TOOLS

### Navigation
- `/prime` - System navigator
- `/prime-*` - Domain specialists

### Meta-Construction
- `/codexa-distill` - Distill docs to templates
- `/codexa-build-agent` - Create new agent
- `/codexa-build-prompt` - Create HOP
- `/codexa-orchestrate` - Multi-phase workflows

### Scout (MCP)
- `mcp__scout__discover` - Find relevant files
- `mcp__scout__smart_context` - Get agent context
- `mcp__scout__search` - Pattern search

---

## LAW 5: AUTO-PUBLISH WORKFLOW

> **"Anuncios gerados DEVEM ser publicados no Supabase + Shopify."**

### Fluxo Completo

```
┌─────────────────────────────────────────────────────────────┐
│ 1. GERAR ANUNCIOS (anuncio_agent)                           │
│    └─ Salva: user_anuncios/*.md (22 produtos reformados)    │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. AUTO-PUBLISH (scripts/auto_publish_anuncios.py)          │
│    └─ Parseia .md → Extrai titulo, descricao, bullets       │
│    └─ Match com produto via preco/nome                      │
│    └─ PATCH no Supabase (REST API)                          │
│    └─ Sync com Shopify (Edge Function)                      │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. LIVE (gatoaocubo.lovable.app + Shopify)                  │
│    └─ Produtos atualizados com copy otimizada               │
│    └─ Checkout Shopify funcional                            │
└─────────────────────────────────────────────────────────────┘
```

### Comandos

```bash
# Simular (dry-run) - ver o que seria atualizado
python codexa.app/agentes/anuncio_agent/scripts/auto_publish_anuncios.py --dry-run

# Publicar TODOS os anuncios pendentes
export SUPABASE_SERVICE_ROLE_KEY="sua-chave"
python codexa.app/agentes/anuncio_agent/scripts/auto_publish_anuncios.py

# Publicar apenas um produto
python auto_publish_anuncios.py --file arranhador

# Listar produtos e anuncios
python auto_publish_anuncios.py --list
```

### Arquivos Criticos

| Arquivo | Funcao |
|---------|--------|
| `scripts/auto_publish_anuncios.py` | Workflow autonomo de publicacao |
| `scripts/products_cache.json` | Cache local de produtos Supabase |
| `scripts/publish_log.json` | Log de publicacoes (evita duplicatas) |
| `src/supabase_publisher.py` | Wrapper para Edge Functions |
| `user_anuncios/*.md` | Anuncios gerados pelo agent |

### Dependencias

- `SUPABASE_SERVICE_ROLE_KEY` (env var) - Obrigatoria para escrita
- `products_cache.json` atualizado - Rodar `list_products.py` antes
- Edge Function `sync-shopify-product` deployada

### Quando Usar

1. Apos gerar anuncios com anuncio_agent
2. Apos reformar catalogo de produtos
3. Para sincronizar copy otimizada com LP e Shopify

---

## LAW 6: EXECUTION INTELLIGENCE

> **"A LLM decide o melhor ambiente de execução."**

### Filosofia

A LLM tem **autonomia** para escolher entre Windows e WSL/Ubuntu baseado em heurísticas, não regras rígidas. O objetivo é **menor fricção, maior compatibilidade**.

### Ambientes Disponíveis

```
┌─────────────────────────────────────────────────────────────┐
│  WINDOWS (default)          │  WSL/UBUNTU (via wsl cmd)    │
│  ├── Node.js / npm          │  ├── Python com deps Linux   │
│  ├── PowerShell scripts     │  ├── Docker containers       │
│  ├── Git operations         │  ├── Shell scripts (.sh)     │
│  └── MCP servers            │  └── Ferramentas GNU         │
└─────────────────────────────────────────────────────────────┘
```

### Heurísticas para Decisão (LLM usa como guia)

| Sinal | Ambiente | Razão |
|-------|----------|-------|
| Arquivo `.py` com deps complexas | WSL | numpy, torch, etc. funcionam melhor |
| Arquivo `.sh` | WSL | Bash nativo |
| Comando `docker` | WSL | Docker Desktop WSL backend |
| Arquivo `.ps1` | Windows | PowerShell nativo |
| Node.js / npm | Windows | Mais rápido, menos overhead |
| Git operations | Windows | Funciona bem, evita overhead |
| `curl`, `jq`, `grep` pesado | WSL | Ferramentas GNU mais robustas |
| Qualquer MCP server | Windows | Configurado para Windows |

### Como Executar

```bash
# Windows (default)
node script.js
python script.py

# WSL/Ubuntu (quando decidir que é melhor)
wsl python script.py
wsl bash deploy.sh
wsl docker compose up
```

### Decisão Autônoma

A LLM deve considerar:
1. **Dependências** - O script precisa de libs que só funcionam bem no Linux?
2. **Performance** - WSL adiciona overhead, vale a pena?
3. **Contexto** - O usuário está trabalhando em qual ambiente?
4. **Erro anterior** - Se falhou no Windows, tentar WSL

### Exemplo de Raciocínio

```
Tarefa: rodar auto_publish_anuncios.py

Análise:
- É Python ✓
- Usa requests, json (funcionam em ambos) ✓
- Não precisa de deps Linux-only ✓
- Usuário está no Windows ✓

Decisão: Windows (menor overhead)
Comando: python codexa.app/agentes/anuncio_agent/scripts/auto_publish_anuncios.py
```

---

## NEVER

- Create documents with hardcoded brand content (distill first)
- Skip validation
- Modify core files without understanding
- Run .py files directly

## ALWAYS

- Distill documents to templates
- Use standard placeholders
- Validate outputs
- Follow fractal patterns

---

**Version**: 1.1.0
**Created**: 2025-12-01
**Updated**: 2025-12-03
**Type**: Project Laws (Auto-loaded)
