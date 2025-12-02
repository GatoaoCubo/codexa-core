# /prime-agentes | Agents Registry & Navigator

> **AGENTES_CODEXA**: Specialized AI agents for e-commerce automation and meta-construction

---

## 📍 LOCALIZAÇÃO NA HIERARQUIA

**Nível**: 3 (Agentes Container)
**Path**: `codexa.app/agentes/`

### Navegação Hierárquica
```
codexa/              (Nível 1 - ROOT)
└── codexa.app/             (Nível 2 - Sistema)
    └── agentes/     (Nível 3 - Você está aqui ⭐)
        └── {agent}/        (Nível 4 - Agente individual)
```

**Versão**: {VERSION}
**Última Atualização**: {LAST_UPDATED}

---

## 🤖 AGENTES DISPONÍVEIS

### 🏗️ Meta-Construction (Build the Builders)

#### **codexa_agent** | Meta-Constructor
```
Path: codexa_agent/
Prime: /prime-codexa
Purpose: Self-building agent that constructs and validates other agents

Components:
├── builders/     (8 scripts) - Create agents/HOPs/commands
├── validators/   (4 scripts) - Quality gates
├── prompts/      (3 HOPs)    - Meta-construction patterns
├── workflows/    (3 ADWs)    - Orchestrated workflows
└── templates/    (docs/fractal) - Navigation templates

Capabilities:
✅ Build complete agents (5-phase ADW workflow)
✅ Create HOP modules (TAC-7 framework)
✅ Generate slash commands
✅ Orchestrate multi-phase workflows
✅ Validate documentation and schemas
✅ Self-improvement and system consolidation

Commands:
/prime-codexa         - Load full meta-construction context
/codexa-build_agent   - Create new agent (5 phases)
/codexa-build_prompt  - Create HOP module (TAC-7)
/codexa-build_command - Create slash command
/codexa-build_schema  - Create JSON schema
/codexa-build_mcp     - Create MCP server
/codexa-orchestrate   - Multi-phase workflow orchestration

Version: 1.2.0
Status: ✅ Active (Production)
```

---

### 🛍️ E-Commerce Domain (Brazilian Marketplaces)

#### **anuncio_agent** | Product Listing Generation
```
Path: anuncio_agent/
Prime: /prime-anuncio
Purpose: Generate optimized product listings for 9+ marketplaces

Components:
├── prompts/          (15 HOPs) - Ad generation pipeline
├── config/           Marketplace specs + quality thresholds
├── templates/        Ad templates per marketplace
└── user_anuncios/    User-generated listings

Capabilities:
✅ Generate listings for 9 Brazilian marketplaces
✅ SEO optimization (keyword density 9-10 terms)
✅ Compliance validation (100% compliance rate)
✅ Conversion optimization (+25% avg CTR)

Output: anuncio.json (structured) + marketplace_listings/

Commands:
/prime-anuncio        - Load ad generation context
/anuncio [research]   - Generate listing from research

Version: 1.2.1
Status: ✅ Active (Production)
Dependencies: pesquisa_agent
```

#### **pesquisa_agent** | Market Research & Analysis
```
Path: pesquisa_agent/
Prime: /prime-pesquisa
Purpose: Conduct market research and competitive analysis

Components:
├── prompts/      (22 HOPs) - Research workflow (22 blocks)
├── config/       Research parameters + sources
└── cache/        Cached research results

Capabilities:
✅ Research across 9+ Brazilian marketplaces
✅ Competitor analysis (pricing, features, positioning)
✅ Keyword extraction and SEO analysis
✅ Market trend identification
✅ 22-block structured output (research_notes.md)

Output: research_notes.md (22 structured blocks)

Commands:
/prime-pesquisa       - Load research context
/pesquisa "produto"   - Run market research

Version: 2.1.0
Status: ✅ Active (Production)
Dependencies: None
```

#### **marca_agent** | Brand Strategy & Positioning
```
Path: marca_agent/
Prime: /prime-marca
Purpose: Develop brand strategy and identity

Components:
├── prompts/      (1 HOP) - Brand strategy workflow
├── config/       Brand guidelines
└── templates/    Brand identity templates

Capabilities:
✅ Brand strategy development
✅ Brand positioning and messaging
✅ Brand guidelines creation
✅ Consistency scoring

Output: brand_strategy.md + brand_guidelines.json

Commands:
/prime-marca          - Load brand context
/marca                - Develop brand strategy

Version: 1.0.0
Status: 🔄 Beta (In Development)
Dependencies: None
```

---

### 🧠 Knowledge & Planning

#### **conhecimento_agent** | Knowledge & ML Training Data
```
Path: conhecimento_agent/
Prime: /prime-knowledge
Purpose: Extract knowledge and generate ML training datasets

Components:
├── scripts/      Knowledge extraction scripts
├── shared/       Shared utilities
└── config/       Knowledge base configuration

Capabilities:
✅ Knowledge card generation
✅ ML training data extraction
✅ Knowledge base management
✅ Dataset versioning

Commands:
/prime-knowledge      - Load knowledge context
/knowledge            - Extract knowledge

Version: 1.1.0
Status: ✅ Active (Production)
Dependencies: None
```

#### **mentor_agent** | Strategic Planning & KPIs
```
Path: mentor_agent/
Prime: /prime-mentor
Purpose: Provide strategic guidance and planning

Components:
├── prompts/          (16 HOPs) - Strategic workflows
├── DISTRIBUICAO/     Distribution patterns
└── config/           Planning templates

Capabilities:
✅ Strategic planning and roadmapping
✅ KPI definition and tracking
✅ Process optimization
✅ Mentoring and guidance

Commands:
/prime-mentor         - Load mentor context
/mentor               - Strategic planning

Version: 2.0.0
Status: ✅ Active (Production)
Dependencies: None
```

---

### 🔭 Development Tools

#### **scout_agent** | Code Navigation & Discovery
```
Path: scout_agent/
Prime: /prime-scout
Purpose: Navigate and discover codebase patterns

Components:
├── prompts/      (1 HOP) - Code exploration
└── config/       Search patterns

Capabilities:
✅ Repository navigation
✅ Code pattern discovery
✅ File and function search
✅ Dependency analysis

Commands:
/prime-scout          - Load scout context
/scout [query]        - Navigate codebase

Version: 1.0.0
Status: ✅ Active (Production)
Dependencies: None
```

---

## 🗺️ QUANDO USAR QUAL AGENTE?

### Decision Tree (IF/THEN)

```
=== META-CONSTRUCTION (Building System) ===
IF (criar novo agente)              → /prime-codexa + /codexa-build_agent
IF (criar HOP reutilizável)         → /prime-codexa + /codexa-build_prompt
IF (criar comando slash)            → /prime-codexa + /codexa-build_command
IF (orquestrar workflow complexo)   → /prime-codexa + /codexa-orchestrate
IF (melhorar o sistema)             → /prime-codexa (self-improvement)

=== E-COMMERCE WORKFLOW (Brazilian Marketplaces) ===
IF (pesquisar mercado/nicho)        → /prime-pesquisa + /pesquisa
IF (gerar anúncio de produto)       → /prime-anuncio + /anuncio
IF (definir estratégia de marca)    → /prime-marca + /marca
IF (consistência de marca)          → /prime-marca

=== KNOWLEDGE & PLANNING ===
IF (extrair conhecimento)           → /prime-knowledge + /knowledge
IF (gerar training data ML)         → /prime-knowledge
IF (planejamento estratégico)       → /prime-mentor + /mentor
IF (definir KPIs)                   → /prime-mentor

=== DEVELOPMENT ===
IF (navegar código)                 → /prime-scout + /scout
IF (encontrar arquivo/função)       → /prime-scout
IF (analisar dependências)          → /prime-scout

=== NAVIGATION ===
IF (não sabe qual usar)             → /prime (root navigator)
IF (overview do sistema)            → README.md files
```

---

## 📊 ESTATÍSTICAS

| Agente | Versão | HOPs | Commands | Status |
|--------|--------|------|----------|--------|
| **codexa_agent** | 1.2.0 | 3 | 7 | ✅ Active |
| **anuncio_agent** | 1.2.1 | 15 | 1 | ✅ Active |
| **pesquisa_agent** | 2.1.0 | 22 | 1 | ✅ Active |
| **marca_agent** | 1.0.0 | 1 | 1 | 🔄 Beta |
| **mentor_agent** | 2.0.0 | 16 | 1 | ✅ Active |
| **scout_agent** | 1.0.0 | 1 | 1 | ✅ Active |
| **conhecimento_agent** | 1.1.0 | 0 | 1 | ✅ Active |

**Total**: 7 agentes | 58 HOPs | 13 commands primários

---

## 🔗 PATHWAYS (Cross-References)

### Superior (Parent)
- `../PRIME.md` - Sistema de agentes (codexa.app)
- `../README.md` - Estrutura de agentes (codexa.app)
- `../../PRIME.md` - Master navigator (ROOT)

### Inferior (Children)
- `codexa_agent/PRIME.md` - Meta-constructor context
- `anuncio_agent/PRIME.md` - Ad generation context
- `pesquisa_agent/PRIME.md` - Research context
- `marca_agent/PRIME.md` - Brand strategy context
- `mentor_agent/PRIME.md` - Strategic planning context
- `scout_agent/PRIME.md` - Code navigation context
- `conhecimento_agent/` - Knowledge extraction (no PRIME yet)

### Lateral (Related)
- `../51_AGENT_REGISTRY.json` - Metadata registry
- `codexa_agent/builders/` - Meta-construction builders
- `codexa_agent/validators/` - Quality gates

---

## 🚀 WORKFLOWS TÍPICOS

### Workflow 1: E-commerce Listing (Complete Pipeline)
```bash
1. /prime-pesquisa                   # Load research context
2. /pesquisa "fone bluetooth"        # Market research
   → Output: research_notes.md

3. /prime-marca                      # Load brand context (optional)
4. /marca                            # Define brand strategy
   → Output: brand_strategy.md

5. /prime-anuncio                    # Load ad context
6. /anuncio research_notes.md        # Generate listing
   → Output: anuncio.json + marketplace_listings/

Time: 15-30 min (research) + 2-3 min (generation) = ~20-35 min total
Traditional: 2-4 hours
Reduction: -95%
```

### Workflow 2: Create New Agent (Meta-Construction)
```bash
1. /prime-codexa                     # Load full meta context
2. /codexa-when_to_use               # Decision tree (optional)
3. /codexa-build_agent               # 5-phase construction
   → Output: agents/{name}/ (complete agent)

Time: 30-45 min (automated 5 phases)
Traditional: Days of manual work
```

### Workflow 3: Knowledge Extraction → Training Data
```bash
1. /prime-knowledge                  # Load knowledge context
2. /knowledge                        # Extract knowledge
   → Output: knowledge_cards/ + training_data/
```

---

## ⚙️ CONFIGURAÇÃO E SETUP

### Cada Agente Possui
- ✅ `PRIME.md` - Domain-specific context (load via /prime-{agent})
- ✅ `README.md` - Documentation and structure
- ✅ `SETUP.md` - Setup instructions (alguns agentes)
- ✅ `INSTRUCTIONS.md` - Operational instructions (alguns agentes)
- ✅ `prompts/` - HOP modules (TAC-7 format)
- ✅ `config/` - Configuration files

### Para Usar um Agente
1. Execute `/prime-{agent}` para carregar contexto completo
2. Leia `README.md` do agente para entender estrutura
3. Execute comando específico do agente
4. Valide outputs com validators (se aplicável)

---

## 📚 DOCUMENTAÇÃO ADICIONAL

| Documento | Localização | Propósito |
|-----------|-------------|-----------|
| **Agent Registry** | `../51_AGENT_REGISTRY.json` | Metadata de todos agentes |
| **HOP Framework** | `../42_HOP_FRAMEWORK.md` | TAC-7 documentation |
| **Documentation Index** | `../41_DOCUMENTATION_INDEX.md` | Índice geral |
| **Individual READMEs** | `{agent}/README.md` | Docs de cada agente |
| **Individual PRIMEs** | `{agent}/PRIME.md` | Context de cada agente |

---

## 🧠 FILOSOFIA DOS AGENTES

### Princípios
1. **One Agent, One Domain** - Especialização clara
2. **HOP-Driven** - Prompts reutilizáveis (TAC-7)
3. **Self-Contained** - Sem dependências ocultas
4. **Quality Gates** - Validation em cada fase
5. **Meta-Buildable** - codexa_agent pode criar novos agentes

### Meta-Construction (CODEXA Agent)
O `codexa_agent` é especial porque:
- ✅ Constrói outros agentes (5-phase ADW)
- ✅ Valida componentes do sistema
- ✅ **Pode melhorar a si próprio** (bootstrapping)
- ✅ Templates e padrões reutilizáveis

---

**Versão**: {VERSION}
**Data**: {LAST_UPDATED}
**Status**: ✅ 7 Agentes Operacionais
**Tipo**: Agents Index (Fractal Level 3)

---

> 🤖 **AGENTES**: 7 especializados (1 meta + 3 e-commerce + 2 knowledge + 1 dev)
> 🗺️ **NAVEGAÇÃO**: Use /prime-{agent} para carregar contexto específico
> 🏗️ **META**: codexa_agent constrói e valida todos os outros agentes
