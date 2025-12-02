# CODEXA.APP | Sistema de Meta-Construção de Agentes

> **IMPORTANTE**: Esta pasta contém **APENAS DOCUMENTAÇÃO E COMANDOS**.
> Todos os scripts Python (.py) devem ser **LIDOS mas NUNCA EXECUTADOS diretamente desta pasta**.
> Use os comandos (`/codexa-*`) para interagir com o sistema de forma segura.

---

## 📁 ESTRUTURA GERAL

```
codexa.app/                           # Este diretório (UX - Interface)
├── 📄 README.md, PRIME.md            # Entry points
├── 📄 41_*, 42_*, 51_*               # Documentação UX
├── 📂 agentes/                       # EXECUÇÃO - Lógica dos agentes
│   ├── codexa_agent/commands/        # Meta-construction commands
│   ├── anuncio_agent/commands/       # Anuncio command
│   ├── marca_agent/commands/         # Brand command
│   ├── pesquisa_agent/commands/      # Pesquisa command
│   └── mentor_agent/commands/        # Mentor command
└── 📂 docs_consolidados/             # Docs técnicos/histórico

../.claude/commands/                  # Comandos ativos (Claude Code)
├── prime.md, prime_*.md              # Comandos de inicialização
└── [slash commands symlinked from agents]

../FONTES/                            # 📚 External knowledge & references
└── ai_tools_prompts/                 # System prompts from AI tools
    ├── PLATFORM_REGISTRY.json        # Platform index
    └── [platform_name]/              # Per-platform documentation
```

**Fractal Architecture**: Commands live WITH their agents, not in root.

---

## 📚 DOCUMENTAÇÃO UX (Raiz - 5 arquivos)

| Arquivo | Propósito | Como Usar |
|---------|-----------|-----------|
| `README.md` | Entry point e guia principal | Começar aqui |
| `PRIME.md` | Regras primárias do sistema | Ler antes de usar |
| `41_DOCUMENTATION_INDEX.md` | Índice de toda documentação | Encontrar docs específicos |
| `42_HOP_FRAMEWORK.md` | Framework TAC-7 para HOPs | Criar prompts reutilizáveis |
| `51_AGENT_REGISTRY.json` | Registro de todos agentes | Ver agentes e capabilities |

**⚠️ FOCO**: Estes são documentos de **interface/UX** - o que o usuário precisa ver.

---

## 📂 DIRETÓRIOS PRINCIPAIS

### 1. `agentes/` - Agentes Organizados

Contém todos os agentes do sistema, cada um em sua pasta:

```
agentes/
├── codexa_agent/          ⭐ Meta-constructor (auto-construção)
├── anuncio_agent/         Geração de anúncios de produtos
├── pesquisa_agent/        Pesquisa de mercado
├── conhecimento_agent/    Gestão de conhecimento
├── marca_agent/           Estratégia de marca
├── mentor_agent/          Orientação estratégica
└── scout_agent/           Exploração de código
```

#### `agentes/codexa-agent/` ⭐ (Principal)

**Propósito**: Agente que constrói outros agentes e componentes do sistema.

**Estrutura**:
```
codexa_agent/
├── builders/              Scripts de construção (7 arquivos .py)
├── validators/            Scripts de validação (3 arquivos .py)
├── prompts/               HOPs TAC-7 (3 arquivos .md)
├── workflows/             Workflows ADW (3 arquivos .md)
└── README.md              Documentação do agente
```

**⚠️ IMPORTANTE - Scripts Python (.py)**:
- **NÃO executar diretamente** os arquivos .py
- **Apenas LER** para entender como funcionam
- **Usar os comandos** `/codexa-*` que chamam estes scripts de forma segura

**Scripts de Construção** (builders/):
- `01_agent_builder.py` - Construtor básico de agentes
- `02_agent_meta_constructor.py` - Meta-construtor (5 fases)
- `03_build_task.py` - Construtor de tarefas
- `04_chore_task.py` - Construtor de tarefas de manutenção
- `05_command_generator.py` - Gerador de comandos
- `06_cron_orchestrator.py` - Orquestrador de cron jobs
- `08_prompt_generator.py` - Gerador de HOPs

**Scripts de Validação** (validators/):
- `07_hop_sync_validator.py` - Valida HOPs contra TAC-7
- `09_readme_validator.py` - Valida READMEs
- `10_taxonomy_validator.py` - Valida taxonomia

**HOPs (prompts/)** - Prompt Modules TAC-7:
- `agentes/codexa-agent/prompts/91_meta_build_agent_HOP.md` - HOP para construir agentes
- `agentes/codexa-agent/prompts/94_meta_build_prompt_HOP.md` - HOP para construir HOPs
- `agentes/codexa-agent/prompts/96_meta_orchestrate_HOP.md` - HOP para orquestrar workflows

**Workflows ADW** (workflows/):
- `agentes/codexa-agent/workflows/97_ADW_NEW_AGENT_WORKFLOW.md` - Criar agente completo (5 fases)
- `agentes/codexa-agent/workflows/98_ADW_CONSOLIDATION_WORKFLOW.md` - Consolidar sistema (5 fases)
- `agentes/codexa-agent/workflows/99_ADW_SYSTEM_UPGRADE_WORKFLOW.md` - Upgrade seguro (5 fases)

---

### 2. Agent Commands (Fractal Structure)

**Propósito**: Commands live WITH their agents (fractal architecture).

**Locations**:

**CODEXA Meta-Commands** (`agentes/codexa-agent/commands/`):
| Comando | Descrição | Quando Usar |
|---------|-----------|-------------|
| `/codexa-when_to_use` | Decision tree - escolhe ferramenta certa | Não sabe qual tool usar |
| `/codexa-build_agent` | Cria agente completo (5 fases) | Quer criar novo agente |
| `/codexa-build_command` | Cria novo comando slash | Quer criar `/novo_comando` |
| `/codexa-build_mcp` | Cria servidor MCP | Integração com API externa |
| `/codexa-build_prompt` | Cria HOP module (TAC-7) | Quer prompt reutilizável |
| `/codexa-build_schema` | Cria schema ou execution plan | Validação de outputs |
| `/codexa-orchestrate` | Orquestra workflow multi-fase | Workflow complexo ≥3 fases |

**Agent-Specific Commands**:
- `/anuncio` → `agentes/anuncio_agent/commands/anuncio.md`
- `/brand` → `agentes/marca_agent/commands/brand.md`
- `/pesquisa` → `agentes/pesquisa_agent/commands/pesquisa.md`
- `/mentor` → `agentes/mentor_agent/commands/mentor.md`

**How It Works**:
1. Each agent contains its own `commands/` folder
2. Commands are self-contained with the agent
3. No duplication in root directory
4. Fractal: Same structure at every level

**Quick Start**:
```
/codexa-when_to_use    # Decision tree
/codexa-build_agent    # Create new agent
/anuncio               # Run anuncio agent
/brand                 # Run brand agent
```

---

### 3. `docs_consolidados/` - Documentação Técnica/Histórico

**Propósito**: Documentação técnica, histórico, migrações.

```
docs_consolidados/
├── 43_META_CONSTRUCTION_INDEX.md      # Meta-construction
├── 44_MIGRATION_GUIDE.md              # Guias de migração (movido)
├── 45_MIGRATION_STATUS.md             # Status migrações (movido)
├── 46_ORGANIZATION_MAP.md             # Mapa organização (movido)
├── 90_CONSOLIDATION_PLAN.md           # Plano consolidação (movido)
├── 91_RAW_STAGING_WORKFLOW.md         # Workflow staging (movido)
├── 92_CODEXA_SELF_BUILD_DELEGATION.md # Self-build (movido)
└── crud/                              # Documentação CRUD
    ├── 21_CRUD_ARCHITECTURE_PLAN.md
    ├── 22_CRUD_CONSOLIDATION_HISTORY.md
    └── [mais 5 arquivos CRUD]
```

**Como Usar**:
- **Docs técnicos** para devs (43, 92)
- **Histórico** para entender mudanças (44, 45, 46, 90, 91)
- **CRUD** para arquitetura de repositório

---

## 🚀 COMO USAR O SISTEMA

### Fluxo Básico

1. **Descoberta**: `/codexa-when_to_use`
   - Usa decision tree para escolher ferramenta certa

2. **Execução**: `/codexa-[ação]`
   - Executa comando recomendado

3. **Validação**: Automática
   - Sistema valida outputs automaticamente

### Casos de Uso Comuns

#### Caso 1: Criar Novo Agente
```bash
/codexa-build_agent
# ou diretamente (se souber o que quer):
# Sistema executa 02_agent_meta_constructor.py de forma segura
# 5 fases: Plan → Build → Test → Review → Document
# Resultado: Agente completo em agents/{nome}/
```

#### Caso 2: Criar Comando Novo
```bash
/codexa-build_command
# Sistema guia criação de novo /comando
# Resultado: commands/{XX}_{nome}.md
```

#### Caso 3: Criar HOP (Prompt Module)
```bash
/codexa-build_prompt
# Sistema guia criação de HOP TAC-7
# Resultado: agentes/{agent}/prompts/{nome}_HOP.md
```

#### Caso 4: Orquestrar Workflow Complexo
```bash
/codexa-orchestrate
# Define workflow multi-fase
# Sistema executa com $arguments chaining
```

---

## ⚠️ REGRAS IMPORTANTES

### ❌ O QUE NÃO FAZER

1. **NÃO executar arquivos .py diretamente**
   ```bash
   # ❌ ERRADO:
   python agentes/codexa-agent/builders/02_agent_meta_constructor.py

   # ✅ CORRETO:
   /codexa-build_agent
   ```

2. **NÃO modificar arquivos core (41-47, 51, 90-92)**
   - São documentação de referência do sistema

3. **NÃO criar arquivos soltos na raiz**
   - Use estrutura organizada (agentes/, commands/, docs_consolidados/)

### ✅ O QUE FAZER

1. **Ler documentação antes de usar**
   - Comece com `README.md` e `41_DOCUMENTATION_INDEX.md`

2. **Usar comandos slash**
   - Sempre prefira `/codexa-*` em vez de executar scripts

3. **Validar com sistema**
   - Deixe validadores checarem seus HOPs, READMEs, etc.

4. **Organizar novos arquivos**
   - Agentes → `agentes/{nome}/`
   - Commands → `agentes/{agent}/commands/` (fractal)
   - Docs → `docs_consolidados/{categoria}/`

---

## 🎯 FILOSOFIA DO SISTEMA

**"Build the thing that builds the thing"**

O CODEXA é um sistema **auto-construtor**:
- Pode criar novos agentes
- Pode criar novos comandos
- Pode criar novos HOPs
- **Pode melhorar a si próprio**

### Meta-Construção

O agente `codexa_agent` é especial:
- Constrói outros agentes
- Valida componentes do sistema
- Orquestra workflows complexos
- É o "cérebro" do sistema de construção

### Princípios

1. **Executable Documentation**: Documentos viram comandos executáveis
2. **Self-Building**: Sistema pode se auto-melhorar
3. **Clear Contracts**: INPUT/OUTPUT definidos (TAC-7)
4. **Full Traceability**: Logs completos de todas operações
5. **Safe Execution**: Comandos são wrappers seguros para scripts

---

## 📊 MÉTRICAS DO SISTEMA

| Métrica | Valor |
|---------|-------|
| Agentes | 7 (anuncio, pesquisa, marca, scout, mentor, conhecimento, codexa) |
| Commands CODEXA | 7 (/codexa-*) |
| Commands Prime | 8 (/prime, /prime-*) |
| HOPs TAC-7 | 81 prompts em agentes |
| Workflows ADW | 3 orquestrados |
| Builders | 7 scripts (codexa_agent) |
| Validators | 3 scripts (codexa_agent) |
| Arquivos Raiz | 5 (antes: 13) ✅ |
| Organização | -62% files na raiz ✅ |

---

## 🔗 PRÓXIMOS PASSOS

1. **Leia a documentação**:
   - `README.md` - Visão geral
   - `docs_consolidados/43_META_CONSTRUCTION_INDEX.md` - Como funciona
   - `42_HOP_FRAMEWORK.md` - Entender HOPs

2. **Experimente comandos**:
   - `/codexa-when_to_use` - Para descobrir features
   - `/codexa-build_agent` - Para criar seu primeiro agente

3. **Explore agentes**:
   - Veja `agentes/codexa-agent/README.md`
   - Leia (não execute!) os scripts em `builders/`

4. **Consulte registry**:
   - `51_AGENT_REGISTRY.json` tem todos agentes e capabilities

---

## ❓ FAQ

**P: Posso executar os scripts .py?**
R: ❌ Não diretamente. Use os comandos `/codexa-*` que executam de forma segura.

**P: Como criar um novo agente?**
R: ✅ Use `/codexa-build_agent` - sistema guia você por 5 fases.

**P: O que é TAC-7?**
R: Framework de 7 componentes para HOPs. Veja `42_HOP_FRAMEWORK.md`.

**P: Como saber qual comando usar?**
R: ✅ Use `/codexa-when_to_use` - decision tree interativo.

**P: Posso modificar o sistema?**
R: ✅ Sim! Sistema é auto-construtor. Use `/codexa-orchestrate` para upgrades seguros.

**P: Onde adiciono novos arquivos?**
R: Estrutura organizada (fractal):
- Agentes → `agentes/{nome}/`
- Commands → `agentes/{agent}/commands/{nome}.md`
- Docs → `docs_consolidados/{categoria}/`

---

## 📝 NOTAS DA CONSOLIDAÇÃO

Este sistema foi consolidado em 2025-11-13:
- **Antes**: 37 arquivos soltos na raiz
- **Depois**: 9 arquivos core + estrutura organizada
- **Redução**: -78% de clutter
- **Features Novas**: 7 commands, 3 HOPs, 3 workflows

Ver `docs_consolidados/90_CONSOLIDATION_PLAN.md` para detalhes completos.

---

**Versão**: 1.1.0
**Data**: 2025-11-13
**Status**: ✅ Sistema Consolidado e Operacional
**Próximo**: Renomear pasta `codexa/` → `codexa.app/`
