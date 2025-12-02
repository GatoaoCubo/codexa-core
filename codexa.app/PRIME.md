# PRIME | Instruções Primárias para CODEXA.APP

> **PRIME** = **P**rimary **R**ules for **I**nteraction and **M**eta-construction **E**xecution

---

## 🧭 VERTICALIZAÇÃO DE COMANDOS (v3.0)

### `/prime` vs `/prime-codexa` - Separação Clara

**`/prime`** - **System Navigator** (Pure Status & Routing)
```
🎯 Purpose: Show where you are and where you can go
📊 Output: ~30-40 lines, pure navigation
✅ Shows: Status, agent list, command list, docs links
❌ Does NOT: Load context, explain philosophy, teach frameworks
🔧 Use when: Starting session, checking health, routing to specialists
```

**`/prime-codexa`** - **Meta-Construction Specialist** (Deep Context)
```
🎯 Purpose: Load full meta-construction knowledge for building
📊 Output: Heavy context load (PRIME.md + builders + validators)
✅ Shows: 5-phase ADW, TAC-7 HOPs, builder workflows, principles
❌ Does NOT: Show system-wide status, list all agents, general nav
🔧 Use when: Building agents, creating HOPs, meta-construction tasks
```

**Other `/prime-*`** - **Domain Specialists**
```
/prime-anuncio    → E-commerce ads specialist
/prime-pesquisa   → Market research specialist
/prime-marca      → Brand strategy specialist
/prime-mentor     → Knowledge & mentoring specialist (consolidated scout + knowledge)
```

### Princípios de Verticalização

1. **One Purpose Per Command** - Cada comando = UM domínio claro
2. **No Overlap** - Contexto não se repete entre comandos
3. **Deep Not Wide** - Profundidade no domínio, não amplitude
4. **Load Only What Needed** - Carrega apenas arquivos do seu domínio
5. **Clear Entry Points** - Humano/LLM sabe exatamente quando usar

---

## 🚨 REGRA #1: NÃO EXECUTAR SCRIPTS PYTHON

### ❌ NUNCA FAZER

```bash
# ❌ PROIBIDO - NÃO EXECUTAR DIRETAMENTE:
python agentes/codexa_agent/builders/02_agent_meta_constructor.py
python agentes/codexa_agent/validators/07_hop_sync_validator.py
uv run agentes/codexa_agent/builders/01_agent_builder.py
./agentes/codexa_agent/builders/03_build_task.py

# ❌ PROIBIDO - NÃO IMPORTAR EM SCRIPTS EXTERNOS:
from agentes.codexa_agent.builders import agent_builder
import agentes.codexa_agent.validators.hop_sync_validator

# ❌ PROIBIDO - NÃO MODIFICAR SCRIPTS:
# Não edite os arquivos .py diretamente
```

### ✅ PERMITIDO

```bash
# ✅ LER para entender como funcionam:
cat agentes/codexa_agent/builders/02_agent_meta_constructor.py
less agentes/codexa_agent/validators/07_hop_sync_validator.py

# ✅ USAR comandos slash que executam de forma segura:
/codexa-build_agent
/codexa-build_command
/codexa-build_prompt

# ✅ VER documentação:
cat agentes/codexa_agent/README.md
cat 42_HOP_FRAMEWORK.md
```

---

## 📖 COMO USAR SCRIPTS PYTHON (Modo Leitura)

### Propósito da Leitura

Os scripts Python são **código de referência**. Leia-os para:

1. **Entender a lógica** de construção de agentes
2. **Ver padrões** de meta-construção
3. **Aprender** como o sistema funciona
4. **Inspirar-se** para criar seus próprios sistemas

### O Que Procurar ao Ler

#### `builders/` - Scripts de Construção

**`02_agent_meta_constructor.py`** (Principal):
```python
# O que observar:
# 1. 5-PHASE WORKFLOW
#    - Phase 1: Planning com [OPEN_VARIABLES]
#    - Phase 2: Construction
#    - Phase 3: Testing
#    - Phase 4: Review
#    - Phase 5: Documentation
#
# 2. $ARGUMENTS CHAINING
#    - Como output de fase N vira input de fase N+1
#    - workflow_context = {"$plan": ..., "$artifacts": ...}
#
# 3. VALIDATION GATES
#    - Como valida cada fase antes de continuar
#    - Quality gates e retry logic
```

**`08_prompt_generator.py`**:
```python
# O que observar:
# - Como gera HOPs seguindo TAC-7
# - Estrutura de 7 componentes
# - INPUT_CONTRACT e OUTPUT_CONTRACT
# - Validation rules
```

**`05_command_generator.py`**:
```python
# O que observar:
# - Template de commands
# - Identity → Task → Steps → Output
# - Como adiciona exemplos
```

#### `validators/` - Scripts de Validação

**`07_hop_sync_validator.py`**:
```python
# O que observar:
# - Como valida TAC-7 framework
# - Checks de completeness
# - Variable consistency (sem orphaned $vars)
# - Type specifications
```

**`09_readme_validator.py`**:
```python
# O que observar:
# - Estrutura esperada de READMEs
# - Required sections
# - Format validation
```

### Exemplo de Leitura Produtiva

```bash
# 1. Leia o header do script
head -50 agentes/codexa_agent/builders/02_agent_meta_constructor.py

# Você verá:
# - Docstring explicando o propósito
# - Dependencies necessárias
# - Usage examples
# - Meta-construction philosophy

# 2. Leia as funções principais
grep -A 20 "def execute_phase" agentes/codexa_agent/builders/02_agent_meta_constructor.py

# Você verá:
# - Como cada fase é executada
# - Inputs e outputs
# - Validation logic

# 3. Leia os comentários
grep "^#" agentes/codexa_agent/builders/02_agent_meta_constructor.py

# Você verá:
# - Explicações da lógica
# - TODOs e FIXMEs
# - Design decisions
```

---

## ✅ MODO DE USO CORRETO

### Uso via Comandos Slash

Os comandos `/codexa-*` são wrappers seguros que:

1. **Validam inputs** antes de executar
2. **Gerenciam contexto** corretamente
3. **Tratam erros** gracefully
4. **Logam operações** para rastreabilidade
5. **Aplicam quality gates**

### Fluxo Recomendado

```
┌─────────────────────────────────────────────────┐
│ 1. DESCOBERTA                                   │
│    /codexa-when_to_use                          │
│    ↓                                            │
│    Sistema mostra decision tree                 │
│    ↓                                            │
│    Recomenda comando apropriado                 │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 2. EXECUÇÃO                                     │
│    /codexa-[comando_recomendado]                │
│    ↓                                            │
│    Sistema executa builders/validators          │
│    de forma segura e controlada                 │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 3. VALIDAÇÃO                                    │
│    Sistema valida automaticamente               │
│    ↓                                            │
│    - Checks de completeness                     │
│    - Validation rules                           │
│    - Quality gates                              │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ 4. RESULTADO                                    │
│    Output organizado e validado                 │
│    ↓                                            │
│    - Arquivos criados em local correto          │
│    - Logs disponíveis                           │
│    - Próximos passos sugeridos                  │
└─────────────────────────────────────────────────┘
```

---

## 🎯 COMANDOS DISPONÍVEIS

### Decision Tree (Começe Aqui)

```bash
/codexa-when_to_use
```

**O que faz**:
- Pergunta o que você quer construir
- Mostra opções disponíveis
- Recomenda comando certo
- Explica quando usar cada um

**Quando usar**: Sempre que não souber qual comando usar.

---

### Construção de Agentes

```bash
/codexa-build_agent
```

**O que faz**:
- Executa 5-phase meta-constructor
- Cria agente completo e isolado
- Gera MASTER_INSTRUCTIONS, config, docs
- Ready para OpenAI Agent Builder

**Quando usar**: Quer criar agente novo do zero.

**Exemplo**:
```
Você: /codexa-build_agent
Sistema: Descreva o agente (1-3 frases)
Você: Agente de análise de sentimentos para reviews
Sistema: [Executa 5 fases - 20-40 min]
Resultado: agents/sentiment-v1/ com tudo pronto
```

---

### Construção de Commands

```bash
/codexa-build_command
```

**O que faz**:
- Cria novo comando slash
- Segue template padrão
- Adiciona exemplos e validação
- Salva em commands/

**Quando usar**: Quer criar `/novo_comando`.

**Exemplo**:
```
Você: /codexa-build_command
Sistema: Nome do comando?
Você: analyze_logs
Sistema: O que faz?
Você: Analisa logs e encontra erros
Sistema: [Cria commands/XX_analyze_logs.md]
```

---

### Construção de HOPs

```bash
/codexa-build_prompt
```

**O que faz**:
- Cria HOP module TAC-7
- Define INPUT/OUTPUT contracts
- Adiciona validation rules
- Valida com hop_sync_validator

**Quando usar**: Quer prompt reutilizável.

**Exemplo**:
```
Você: /codexa-build_prompt
Sistema: ID do módulo?
Você: sentiment_analyzer
Sistema: [Guia por 7 componentes TAC-7]
Resultado: prompts/sentiment_analyzer_HOP.md
```

---

### Construção de Schemas

```bash
/codexa-build_schema
```

**O que faz**:
- Cria JSON Schema v7 ou Execution Plan
- Define validation rules
- Estrutura para workflows

**Quando usar**: Precisa validar outputs estruturados.

---

### Construção de MCP

```bash
/codexa-build_mcp
```

**O que faz**:
- Cria MCP server
- Define tools customizadas
- Integra com Claude Desktop

**Quando usar**: Quer integrar API externa.

---

### Orquestração de Workflows

```bash
/codexa-orchestrate
```

**O que faz**:
- Define workflow multi-fase
- Configura $arguments chaining
- Adiciona validation gates
- Executa com rastreabilidade

**Quando usar**: Workflow complexo ≥3 fases.

---

## 📁 ESTRUTURA DE ARQUIVOS

### O Que Está Onde

```
codexa.app/
│
├── 📚 DOCS CORE
│   ├── PRIME.md                        # Este arquivo (entry point)
│   ├── README.md                       # Visão geral do sistema
│   ├── 42_HOP_FRAMEWORK.md             # TAC-7 framework
│   ├── QUICK_START_ADW.md              # Guia rápido ADW
│   └── ORCHESTRATION.md                # Orquestração multi-agente
│
├── 📂 agentes/                         # ⭐ FRACTAL ARCHITECTURE
│   ├── PRIME.md                        # Registry de todos agentes
│   ├── DOCUMENTATION_INDEX.md          # Índice de documentação
│   ├── 51_AGENT_REGISTRY.json          # Registry JSON
│   │
│   ├── 🤖 codexa_agent/                # Meta-constructor
│   │   ├── builders/                   # Scripts .py (LER, não executar)
│   │   ├── validators/                 # Scripts .py (LER, não executar)
│   │   ├── prompts/                    # HOPs .md
│   │   ├── workflows/                  # ADW workflows .md
│   │   └── README.md                   # Docs do agente
│   │
│   ├── 🛍️ anuncio_agent/               # Anúncios de produtos
│   ├── 🎨 marca_agent/                 # Estratégia marca
│   ├── 🔍 pesquisa_agent/              # Pesquisa mercado
│   ├── 👨‍🏫 mentor_agent/                # Orientação e-commerce
│   ├── 📸 photo_agent/                 # Fotografia IA
│   ├── 🎬 video_agent/                 # Produção de vídeo
│   ├── 📚 curso_agent/                 # Construtor de cursos
│   ├── 🔭 scout_agent/                 # Descoberta de paths (MCP)
│   ├── 🎤 voice_agent/                 # Interface de voz (MCP)
│   ├── 🐱 ronronalda_agent/            # Assistente GATO3
│   └── 🧪 qa_gato3_agent/              # QA para GATO3
│
├── 📂 mcp-servers/                     # MCP Servers
│   ├── browser-mcp/                    # Browser automation
│   ├── voice-mcp/                      # Voice interface
│   └── scout-mcp/                      # Path discovery
│
└── 📂 USER_DOCS/                       # Outputs do usuário
    ├── anuncios/                       # Anúncios gerados
    ├── produtos/                       # Research notes
    └── Marca/                          # Brand strategies
```

**Fractal Principle**: Commands live WITH their agents, not in root.

### Como Navegar

1. **Começar**: Leia `README.md` (este diretório)
2. **Referência**: Use `agentes/DOCUMENTATION_INDEX.md`
3. **Aprender**: Leia scripts em `agentes/codexa_agent/builders/`
4. **Usar**: Execute comandos via `/prime-*` e `/codexa-*`

---

## 🛡️ REGRAS DE SEGURANÇA

### Não Fazer

1. ❌ Executar scripts .py diretamente
2. ❌ Modificar arquivos core (41-47, 51, 90)
3. ❌ Criar arquivos na raiz
4. ❌ Importar módulos Python deste diretório
5. ❌ Executar comandos sem entender o que fazem

### Fazer

1. ✅ Ler scripts para aprender
2. ✅ Usar comandos `/codexa-*`
3. ✅ Consultar documentação
4. ✅ Validar com sistema
5. ✅ Organizar novos arquivos corretamente

---

## 🎓 APRENDIZADO

### Para Iniciantes

1. Leia `README.md` (este diretório)
2. Execute `/codexa-when_to_use`
3. Experimente `/codexa-build_command` (mais simples)
4. Leia `42_HOP_FRAMEWORK.md` para entender HOPs
5. Tente `/codexa-build_prompt`

### Para Avançados

1. Leia `agentes/codexa_agent/PRIME.md` para meta-construção
2. Estude `agentes/codexa_agent/builders/02_agent_meta_constructor.py`
3. Entenda workflows em `agentes/codexa_agent/workflows/`
4. Use `/codexa-orchestrate` para workflows complexos
5. Leia `agentes/codexa_agent/docs/` para documentação técnica

---

## ❓ FAQ

**P: Por que não posso executar os .py?**
R: Scripts são código de **referência e aprendizado**. Comandos `/codexa-*` executam de forma controlada e segura.

**P: Como sei se posso modificar um arquivo?**
R:
- ❌ Não modificar: Core docs (41-47, 51, 90), scripts .py
- ✅ Pode adicionar: Novos commands, HOPs, workflows (em locais corretos)

**P: E se eu quiser melhorar um script?**
R: Use `/codexa-build_agent` ou `/codexa-build_prompt` para criar **nova versão**. Não modifique originais.

**P: Posso criar meu próprio agente?**
R: ✅ Sim! Use `/codexa-build_agent` - sistema cria tudo para você.

**P: Como valido meus HOPs?**
R: Sistema valida automaticamente com `07_hop_sync_validator.py` quando usa `/codexa-build_prompt`.

---

## 🚀 QUICK START

```bash
# 1. Descubra features
/codexa-when_to_use

# 2. Crie seu primeiro comando
/codexa-build_command

# 3. Teste o comando
/[seu_comando]

# 4. Leia código para entender como funciona
cat agentes/codexa_agent/builders/05_command_generator.py

# 5. Crie seu primeiro agente
/codexa-build_agent
```

---

**LEMBRE-SE**:
- 📖 **LER** scripts .py para aprender
- ⚙️ **EXECUTAR** via comandos `/codexa-*`
- 🎯 **COMEÇAR** com `/codexa-when_to_use`

---

**Versão**: 1.0.0
**Data**: 2025-11-13
**Status**: ✅ Sistema Pronto para Uso Seguro
