# AGENTES_CODEXA | Specialized AI Agents Directory

> **Directory Purpose**: Container for all specialized AI agents in the ECOMLM.CODEXA system

---

## 📍 LOCATION IN HIERARCHY

**Level**: 3 (Agents Container)
**Path**: `codexa.app/agentes/`

```
codexa/              (Level 1 - ROOT)
└── codexa.app/             (Level 2 - System)
    └── agentes/     (Level 3 - You are here ⭐)
        └── {agent}/        (Level 4 - Individual agent)
```

**Version**: {VERSION}
**Last Updated**: {LAST_UPDATED}

---

## 🎯 OVERVIEW

This directory contains **7 specialized AI agents** that together form the ECOMLM.CODEXA multi-agent orchestration system:

1. **Meta-Construction** (1 agent): Builds and validates other agents
2. **E-Commerce Domain** (3 agents): Brazilian marketplace automation
3. **Knowledge & Planning** (2 agents): Knowledge extraction and strategic planning
4. **Development Tools** (1 agent): Code navigation and discovery

**Total**: 7 agents | 58+ HOPs | 13 primary commands | 8 builders | 4 validators

---

## 📂 DIRECTORY STRUCTURE

```
agentes/
├── PRIME.md                    ⭐ Agents index & navigator
├── README.md                   📖 This file - Overview
│
├── codexa_agent/               🏗️ Meta-Constructor (v1.2.0)
│   ├── PRIME.md               Context: /prime-codexa
│   ├── README.md              Documentation
│   ├── builders/              8 Python scripts (meta-construction)
│   ├── validators/            4 Python scripts (quality gates)
│   ├── prompts/               3 HOPs (TAC-7 format)
│   ├── workflows/             3 ADW workflows
│   └── templates/             Doc templates (including fractal nav)
│
├── anuncio_agent/              🛍️ Product Listing Generation (v1.2.1)
│   ├── PRIME.md               Context: /prime-anuncio
│   ├── README.md              Documentation
│   ├── SETUP.md               Setup instructions
│   ├── INSTRUCTIONS.md        Operational instructions
│   ├── prompts/               15 HOPs (ad generation pipeline)
│   ├── config/                Marketplace specs + quality thresholds
│   ├── templates/             Ad templates per marketplace
│   └── user_anuncios/         User-generated listings
│
├── pesquisa_agent/             🔍 Market Research (v2.1.0)
│   ├── PRIME.md               Context: /prime-pesquisa
│   ├── README.md              Documentation
│   ├── SETUP.md               Setup instructions
│   ├── prompts/               22 HOPs (research workflow)
│   └── config/                Research parameters + sources
│
├── marca_agent/                🎨 Brand Strategy (v1.0.0)
│   ├── PRIME.md               Context: /prime-marca
│   ├── README.md              Documentation
│   ├── SETUP.md               Setup instructions
│   ├── prompts/               1 HOP (brand strategy workflow)
│   ├── config/                Brand guidelines
│   └── templates/             Brand identity templates
│
├── mentor_agent/               👨‍🏫 Strategic Planning (v2.0.0)
│   ├── PRIME.md               Context: /prime-mentor
│   ├── README.md              Documentation
│   ├── SETUP.md               Setup instructions
│   ├── prompts/               16 HOPs (strategic workflows)
│   ├── DISTRIBUICAO/          Distribution patterns
│   └── config/                Planning templates
│
├── scout_agent/                🔭 Code Navigation (v1.0.0)
│   ├── PRIME.md               Context: /prime-scout
│   ├── README.md              Documentation
│   ├── prompts/               1 HOP (code exploration)
│   └── config/                Search patterns
│
└── conhecimento_agent/         🧠 Knowledge & ML (v1.1.0)
    ├── README.md              Documentation
    ├── scripts/               Knowledge extraction scripts
    ├── shared/                Shared utilities
    └── config/                Knowledge base configuration
```

---

## 🤖 AGENTS QUICK REFERENCE

### 🏗️ codexa_agent (Meta-Constructor)
**Purpose**: Self-building agent that constructs and validates other agents

**Key Features**:
- 5-phase agent construction (Plan → Build → Test → Review → Document)
- HOP generation (TAC-7 framework)
- Slash command creation
- Multi-phase workflow orchestration
- Documentation synchronization
- Self-improvement capabilities

**Commands**: `/prime-codexa`, `/codexa-build_agent`, `/codexa-build_prompt`, `/codexa-build_command`, `/codexa-orchestrate`

**Location**: `codexa_agent/`

---

### 🛍️ anuncio_agent (Product Listings)
**Purpose**: Generate optimized product listings for Brazilian marketplaces

**Key Features**:
- 9+ marketplace support (Mercado Livre, Shopee, Amazon BR, etc.)
- SEO optimization (9-10 keyword density)
- 100% compliance validation
- +25% avg conversion rate improvement

**Commands**: `/prime-anuncio`, `/anuncio`

**Location**: `anuncio_agent/`

**Dependencies**: `pesquisa_agent` (for market research input)

---

### 🔍 pesquisa_agent (Market Research)
**Purpose**: Conduct market research and competitive analysis

**Key Features**:
- 22-block structured research output
- 9+ marketplace coverage
- Competitor analysis (pricing, features, positioning)
- Keyword extraction and SEO analysis

**Commands**: `/prime-pesquisa`, `/pesquisa`

**Location**: `pesquisa_agent/`

**Dependencies**: None

---

### 🎨 marca_agent (Brand Strategy)
**Purpose**: Develop brand strategy and identity

**Key Features**:
- Brand strategy development
- Brand positioning and messaging
- Brand guidelines creation
- Consistency scoring

**Commands**: `/prime-marca`, `/marca`

**Location**: `marca_agent/`

**Dependencies**: None

**Status**: 🔄 Beta (In Development)

---

### 👨‍🏫 mentor_agent (Strategic Planning)
**Purpose**: Provide strategic guidance and planning

**Key Features**:
- Strategic planning and roadmapping
- KPI definition and tracking
- Process optimization
- Mentoring and guidance

**Commands**: `/prime-mentor`, `/mentor`

**Location**: `mentor_agent/`

**Dependencies**: None

---

### 🔭 scout_agent (Code Navigation)
**Purpose**: Navigate and discover codebase patterns

**Key Features**:
- Repository navigation
- Code pattern discovery
- File and function search
- Dependency analysis

**Commands**: `/prime-scout`, `/scout`

**Location**: `scout_agent/`

**Dependencies**: None

---

### 🧠 conhecimento_agent (Knowledge & ML)
**Purpose**: Extract knowledge and generate ML training datasets

**Key Features**:
- Knowledge card generation
- ML training data extraction
- Knowledge base management
- Dataset versioning

**Commands**: `/prime-knowledge`, `/knowledge`

**Location**: `conhecimento_agent/`

**Dependencies**: None

---

## 🗺️ NAVIGATION PATTERNS

### Loading Agent Context
Each agent has a `/prime-{agent}` command that loads its full context:

```bash
/prime-codexa       # Meta-construction specialist (deep context)
/prime-anuncio      # E-commerce ads specialist
/prime-pesquisa     # Market research specialist
/prime-marca        # Brand strategy specialist
/prime-mentor       # Strategic planning specialist
/prime-scout        # Code navigation specialist
/prime-knowledge    # Knowledge extraction specialist
```

### Accessing Agent Documentation
Each agent directory contains:
- `PRIME.md` - Domain-specific context (loaded by `/prime-{agent}`)
- `README.md` - Technical documentation
- `SETUP.md` - Setup instructions (if applicable)
- `INSTRUCTIONS.md` - Operational instructions (if applicable)

### Cross-Agent Dependencies
```
pesquisa_agent → anuncio_agent
(research)       (listing generation)

All agents ← codexa_agent
             (meta-construction & validation)
```

---

## 📊 STATISTICS & METRICS

### Agent Distribution
- **Meta-Construction**: 1 agent (codexa_agent)
- **E-Commerce**: 3 agents (anuncio, pesquisa, marca)
- **Knowledge & Planning**: 2 agents (mentor, conhecimento)
- **Development**: 1 agent (scout)

### Components Count
| Component | Count | Location |
|-----------|-------|----------|
| **Total Agents** | 7 | This directory |
| **HOPs (TAC-7)** | 58+ | `{agent}/prompts/` |
| **Builders** | 8 | `codexa_agent/builders/` |
| **Validators** | 4 | `codexa_agent/validators/` |
| **ADW Workflows** | 3+ | `codexa_agent/workflows/` |
| **Commands** | 13 primary | Via `/prime-{agent}` |

### Status Overview
- ✅ **Active (Production)**: 6 agents
- 🔄 **Beta (In Development)**: 1 agent (marca_agent)

---

## 🚀 TYPICAL WORKFLOWS

### Workflow 1: E-commerce Listing Creation
```bash
1. /prime-pesquisa                   # Load research context
2. /pesquisa "fone bluetooth"        # Conduct market research
   → Output: research_notes.md (22 blocks)

3. /prime-anuncio                    # Load ad generation context
4. /anuncio research_notes.md        # Generate optimized listing
   → Output: anuncio.json + marketplace_listings/

Total Time: ~20-35 minutes (vs. 2-4 hours traditional)
Time Reduction: -95%
```

### Workflow 2: Create New Agent
```bash
1. /prime-codexa                     # Load meta-construction context
2. /codexa-build_agent               # Execute 5-phase construction
   → Output: Complete agent with documentation

Total Time: ~30-45 minutes (automated)
```

### Workflow 3: Brand Strategy → Listing
```bash
1. /prime-marca                      # Load brand context
2. /marca                            # Define brand strategy
   → Output: brand_strategy.md

3. /prime-pesquisa                   # Load research context
4. /pesquisa "produto"               # Market research
   → Output: research_notes.md

5. /prime-anuncio                    # Load ad context
6. /anuncio research_notes.md        # Generate listing (brand-aligned)
   → Output: anuncio.json (with brand consistency)
```

---

## 🔧 DEVELOPMENT & MAINTENANCE

### Adding New Agents
Use the `codexa_agent` meta-constructor:
```bash
/prime-codexa                        # Load context
/codexa-build_agent                  # Follow 5-phase workflow
```

The system will create:
- ✅ Agent directory structure
- ✅ PRIME.md (domain context)
- ✅ README.md (documentation)
- ✅ Prompts (HOPs in TAC-7 format)
- ✅ Configuration files
- ✅ Validation schemas

### Updating Existing Agents
1. Use `/prime-codexa` to load meta-construction context
2. Use builders/validators in `codexa_agent/`
3. Follow ADW workflows for systematic updates
4. Validate with quality gates

### Documentation Sync
Use the doc sync builder:
```bash
# From codexa_agent directory
uv run builders/11_doc_sync_builder.py --mode auto_fix
```

This validates and synchronizes:
- ✅ PRIME.md files (all agents)
- ✅ README.md files (all agents)
- ✅ SETUP.md files (where applicable)
- ✅ Cross-references (pathways)
- ✅ Version metadata

---

## 🔗 PATHWAYS (Cross-References)

### Parent (Superior)
- `../PRIME.md` - System instructions (codexa.app)
- `../README.md` - System structure (codexa.app)
- `../../PRIME.md` - Master navigator (ROOT)

### Children (Inferior)
- `codexa_agent/PRIME.md` - Meta-constructor context
- `anuncio_agent/PRIME.md` - Ad generation context
- `pesquisa_agent/PRIME.md` - Research context
- `marca_agent/PRIME.md` - Brand strategy context
- `mentor_agent/PRIME.md` - Strategic planning context
- `scout_agent/PRIME.md` - Code navigation context
- `conhecimento_agent/README.md` - Knowledge extraction docs

### Lateral (Related)
- `../51_AGENT_REGISTRY.json` - Agent metadata registry
- `../42_HOP_FRAMEWORK.md` - TAC-7 framework documentation
- `../41_DOCUMENTATION_INDEX.md` - Complete documentation index
- `codexa_agent/builders/` - Meta-construction tools
- `codexa_agent/validators/` - Quality gate tools

---

## 📚 ADDITIONAL DOCUMENTATION

| Document | Location | Purpose |
|----------|----------|---------|
| **PRIME.md** | This directory | Agents index & navigator |
| **Agent Registry** | `../51_AGENT_REGISTRY.json` | Metadata for all agents |
| **HOP Framework** | `../42_HOP_FRAMEWORK.md` | TAC-7 documentation |
| **Documentation Index** | `../41_DOCUMENTATION_INDEX.md` | Complete docs index |
| **Individual Docs** | `{agent}/README.md` | Per-agent documentation |

---

## ⚙️ CONFIGURATION

### Registry Configuration
All agents are registered in `../51_AGENT_REGISTRY.json` with:
- Agent name and description
- Version and status
- Entry commands
- Component locations
- Dependencies
- Capabilities

### Quality Standards
All agents follow:
- ✅ TAC-7 framework for HOPs
- ✅ MAX 1000 lines per file
- ✅ Quality score ≥ 7.0/10.0
- ✅ 100% validation coverage
- ✅ Fractal navigation patterns

---

**Version**: {VERSION}
**Last Updated**: {LAST_UPDATED}
**Total Agents**: 7 (6 Active, 1 Beta)
**Type**: Agents Container (Fractal Level 3)

---

> 🤖 **SPECIALIZATION**: Each agent focuses on one domain with clear boundaries
> 🗺️ **NAVIGATION**: Use PRIME.md for context, README.md for structure
> 🏗️ **META**: codexa_agent builds, validates, and improves all agents
