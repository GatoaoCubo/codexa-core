# /prime | ECOMLM.CODEXA System Navigator

> **PRIME** = **P**rimary **R**ules for **I**nteraction and **M**eta-construction **E**xecution

---

## 🎯 SISTEMA

**ECOMLM.CODEXA**: E-Commerce AI Multi-Agent Orchestration System for Brazilian marketplaces.

**Propósito**: Automação end-to-end de workflows de e-commerce - pesquisa de mercado até geração de anúncios com 95% de redução de tempo e 100% de compliance.

**Versão**: {VERSION}
**Última Atualização**: {LAST_UPDATED}

---

## 🗺️ NAVEGAÇÃO HIERÁRQUICA (Fractal)

### 📍 Nível 1: ROOT (você está aqui)
```
codexa/
├── PRIME.md          ⭐ Master Navigator (você está aqui)
├── README.md         📖 Documentação do projeto
├── codexa.app/       📂 Sistema de agentes (Nível 2)
├── app/              📂 FastAPI + Vite application
├── .claude/          ⚙️ Claude Code integration
└── ai_docs/          📚 AI Documentation
```

**Commands disponíveis neste nível**:
- `/prime` → Status geral + routing (carrega este arquivo)

### 📍 Nível 2: CODEXA.APP (Sistema de Agentes)
```
codexa.app/
├── PRIME.md              🔧 Instruções do sistema de agentes
├── README.md             📖 Estrutura e organização
├── agentes/       📂 Agentes implementados (Nível 3)
├── commands/             📂 Slash commands (referência)
└── 41-51_*.md           📄 Documentação core
```

**Commands disponíveis neste nível**:
- `/prime-codexa` → Meta-construction specialist (deep context)

### 📍 Nível 3: AGENTES (Implementações)
```
agentes/
├── PRIME.md              📋 Index de todos agentes
├── README.md             📖 Overview de agentes
├── codexa_agent/         🏗️ Meta-constructor (builds other agents)
├── anuncio_agent/        🛍️ Product listing generation
├── pesquisa_agent/       🔍 Market research
├── marca_agent/          🎨 Brand strategy
├── mentor_agent/         👨‍🏫 Strategic planning
└── scout_agent/          🔭 Code navigation
```

**Commands disponíveis neste nível**:
- `/prime-anuncio` → E-commerce ads specialist
- `/prime-pesquisa` → Market research specialist
- `/prime-marca` → Brand strategy specialist
- `/prime-mentor` → Strategic planning specialist
- `/prime-scout` → Code navigation specialist

### 📍 Nível 4: AGENTE INDIVIDUAL
```
{agent}/
├── PRIME.md              🎯 Domain-specific context
├── README.md             📖 Agent documentation
├── SETUP.md              ⚙️ Setup instructions
├── INSTRUCTIONS.md       📝 Operational instructions
├── prompts/              📂 HOP modules (TAC-7)
├── config/               📂 Configuration files
└── [agent-specific]      📂 Outros diretórios
```

---

## 📋 COMANDOS RÁPIDOS

### Navigation & Status
```bash
/prime              # Status geral + navegação (este arquivo)
```

### Meta-Construction (Building Agents/HOPs/Commands)
```bash
/prime-codexa       # Load full meta-construction context
/codexa-build_agent # Create new agent (5-phase ADW)
/codexa-build_prompt # Create HOP module (TAC-7)
/codexa-build_command # Create slash command
/codexa-orchestrate # Multi-phase workflow orchestration
```

### Domain Specialists (E-commerce Workflow)
```bash
/prime-anuncio      # E-commerce ads generation
/prime-pesquisa     # Market research & analysis
/prime-marca        # Brand strategy development
/prime-mentor       # Strategic planning & KPIs
/prime-scout        # Code navigation & discovery
```

---

## 🔧 FERRAMENTAS DISPONÍVEIS

### Builders (Meta-Construction)
```
codexa_agent/builders/
├── 01_agent_builder.py              # Legacy agent builder
├── 02_agent_meta_constructor.py ⭐  # 5-phase meta-constructor
├── 03_build_task.py                 # Build task workflows
├── 04_chore_task.py                 # Maintenance tasks
├── 05_command_generator.py          # Slash command creation
├── 06_cron_orchestrator.py          # Scheduled orchestration
├── 08_prompt_generator.py           # HOP module generation
└── 11_doc_sync_builder.py           # Documentation sync
```

### Validators (Quality Gates)
```
codexa_agent/validators/
├── 07_hop_sync_validator.py         # HOP TAC-7 compliance
├── 09_readme_validator.py           # README standards
├── 10_taxonomy_validator.py         # Registry consistency
└── 12_doc_sync_validator.py         # Documentation sync validation
```

### HOPs (Higher-Order Prompts - Reusable)
```
Total: 81+ HOPs across all agents
├── codexa_agent/prompts/     (3 HOPs)  - Meta-construction
├── anuncio_agent/prompts/    (15 HOPs) - Ad generation
├── pesquisa_agent/prompts/   (22 HOPs) - Market research
├── marca_agent/prompts/      (1 HOP)   - Brand strategy
├── mentor_agent/prompts/     (16 HOPs) - Strategic planning
└── scout_agent/prompts/      (1 HOP)   - Code navigation
```

### Commands (Slash Commands - Executable)
```
.claude/commands/
├── prime*.md                 (8 commands)  - Navigation & priming
├── codexa_*.md              (7 commands)  - Meta-construction
└── [domain commands]        (37+ commands) - Domain-specific
```

---

## 🚀 INÍCIO RÁPIDO

### Para Novatos (First Time)
```bash
1. Leia README.md (raiz)              # Visão geral do projeto
2. Leia codexa.app/PRIME.md          # Sistema de agentes
3. Execute /prime                     # Status + navegação
4. Experimente /prime-pesquisa       # Specialist simples
```

### Para Construir Agentes (Meta-Construction)
```bash
1. Execute /prime-codexa             # Load full context
2. Execute /codexa-when_to_use       # Decision tree
3. Execute /codexa-build_agent       # Create agent (5 phases)
```

### Para Gerar Anúncios (E-commerce Workflow)
```bash
1. Execute /prime-pesquisa           # Market research
2. Execute /pesquisa "produto"       # Run research
3. Execute /prime-anuncio            # Load ad context
4. Execute /anuncio research_notes.md # Generate listing
```

### Para Navegar Código (Development)
```bash
1. Execute /prime-scout              # Code navigation specialist
2. Execute /scout [query]            # Find files/functions
```

---

## 🧠 FILOSOFIA DO SISTEMA

**"Build the thing that builds the thing"**

### Princípios Core
1. **Meta > Instance** - Build builders, not artifacts
2. **Templates > One-offs** - Reusable patterns over single solutions
3. **Discovery-First** - Find existing before building new
4. **Quality Gates** - Validation at every phase (≥7.0/10.0)
5. **Fractal Navigation** - Each level reflects structure below
6. **Self-Improvement** - System can build/improve itself

### Meta-Construction (CODEXA Agent)
O agente `codexa_agent` é especial:
- ✅ Constrói outros agentes (5-phase ADW)
- ✅ Valida componentes do sistema
- ✅ Orquestra workflows complexos
- ✅ **Pode melhorar a si próprio** (bootstrapping completo)

---

## 📊 MÉTRICAS DO SISTEMA

| Métrica | Valor |
|---------|-------|
| **Agentes** | 7 (anuncio, pesquisa, marca, scout, mentor, conhecimento, codexa) |
| **Commands CODEXA** | 7 (/codexa-*) |
| **Commands Prime** | 8 (/prime, /prime-*) |
| **Total Commands** | 52+ slash commands |
| **HOPs TAC-7** | 81+ prompts reusáveis |
| **Workflows ADW** | 3+ orquestrados |
| **Builders** | 8 scripts (meta-construction) |
| **Validators** | 4 scripts (quality gates) |

---

## 🎯 QUANDO USAR O QUÊ?

### Decision Tree (IF/THEN)

```
IF (construir novo agente)          → /prime-codexa + /codexa-build_agent
IF (criar comando slash)             → /prime-codexa + /codexa-build_command
IF (criar HOP reutilizável)          → /prime-codexa + /codexa-build_prompt
IF (orquestrar workflow complexo)    → /prime-codexa + /codexa-orchestrate

IF (gerar anúncio de produto)        → /prime-anuncio + /anuncio
IF (pesquisar mercado)               → /prime-pesquisa + /pesquisa
IF (definir estratégia de marca)     → /prime-marca + /marca
IF (orientação estratégica)          → /prime-mentor + /mentor
IF (navegar código)                  → /prime-scout + /scout

IF (não sabe qual usar)              → /prime (você está aqui!)
```

---

## ⚠️ REGRAS IMPORTANTES

### ❌ NÃO FAZER
1. Executar scripts .py diretamente (use /codexa-* commands)
2. Modificar arquivos core (41-51_*.md, PRIME.md, README.md)
3. Criar arquivos soltos na raiz
4. Pular validação de quality gates

### ✅ FAZER
1. Ler documentação antes de usar
2. Usar comandos slash (/prime*, /codexa-*)
3. Validar com sistema (validators)
4. Organizar novos arquivos corretamente
5. Seguir padrões existentes (TAC-7, ADW)

---

## 🔗 PATHWAYS (Cross-References)

### Superior (Parent)
- N/A (este é o ROOT)

### Inferior (Children)
- `codexa.app/PRIME.md` - Sistema de agentes
- `codexa.app/README.md` - Estrutura de agentes
- `codexa.app/agentes/PRIME.md` - Index de agentes

### Lateral (Related)
- `README.md` - Documentação do projeto
- `.claude/commands/prime.md` - Este comando
- `codexa.app/51_AGENT_REGISTRY.json` - Registry de agentes

---

## 📚 DOCUMENTAÇÃO ADICIONAL

| Arquivo | Propósito | Localização |
|---------|-----------|-------------|
| `README.md` | Documentação principal do projeto | `/` |
| `codexa.app/PRIME.md` | Instruções do sistema de agentes | `/codexa.app/` |
| `codexa.app/README.md` | Estrutura e organização | `/codexa.app/` |
| `codexa.app/41_DOCUMENTATION_INDEX.md` | Índice de toda documentação | `/codexa.app/` |
| `codexa.app/42_HOP_FRAMEWORK.md` | Framework TAC-7 para HOPs | `/codexa.app/` |
| `codexa.app/51_AGENT_REGISTRY.json` | Registry de todos agentes | `/codexa.app/` |

---

**Versão**: {VERSION}
**Data**: {LAST_UPDATED}
**Status**: ✅ Sistema Consolidado e Operacional
**Tipo**: Master Navigator (Fractal Root)

---

> 💡 **TIP**: Use `/prime` para navegar, `/prime-codexa` para construir, `/prime-{agent}` para especializar
> 🗺️ **NAVEGAÇÃO**: Este arquivo é o topo da hierarquia - todos os caminhos começam aqui
> 🏗️ **META**: Sistema auto-construtor - pode melhorar a si próprio usando codexa_agent
