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

**Versão**: 2.0.0
**Última Atualização**: 2025-11-29

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

### 📸 Media & Content Creation

#### **photo_agent** | AI Photography Prompts
```
Path: photo_agent/
Prime: /prime-photo
Purpose: Generate professional AI photography prompts for e-commerce

Capabilities:
✅ 9-scene photography sets (Grid 3x3 + Individual)
✅ Camera simulation (focal, aperture, lighting)
✅ PNL emotional triggers
✅ Marketplace compliance (white backgrounds)

Output: 2 copyable prompts (Grid + 9 Individual)
Version: 2.5.0
Status: ✅ Active (Production)
```

#### **video_agent** | AI Video Production
```
Path: video_agent/
Prime: /prime-video
Purpose: Transform product briefs into professional e-commerce videos

Capabilities:
✅ Storyboard generation (6-8 shots)
✅ Script writing with timing
✅ Runway/Pika prompt engineering
✅ FFmpeg editing + TTS narration

Output: final_video.mp4 + Trinity metadata
Version: 2.5.0
Status: ✅ Active (Production)
```

#### **curso_agent** | Course Builder
```
Path: curso_agent/
Prime: /prime-curso
Purpose: Educational content architecture for Hotmart courses

Capabilities:
✅ Video script generation
✅ Workbook creation
✅ Sales collateral (landing pages, emails)
✅ Hotmart platform optimization

Output: Complete course package
Version: 2.5.1
Status: ✅ Active (Production)
```

---

### 🛠️ Infrastructure & Tools

#### **scout_agent** | Path Discovery (MCP Server)
```
Path: scout_agent/
Prime: /prime-scout
Purpose: File discovery, indexing, and CRUD operations

Architecture: MCP Server (Model Context Protocol)
Tools: discover, search, agent_context, CRUD operations

Capabilities:
✅ Natural language file discovery
✅ Agent context assembly
✅ Dependency mapping
✅ Safe CRUD with backups

Version: 1.0.0
Status: ✅ Active (Production)
```

#### **voice_agent** | Voice Interface (MCP Server)
```
Path: voice_agent/
Prime: /prime-voice (/v)
Purpose: Accessibility voice interface for hands-free interaction

Architecture: Background daemon with file-based IPC
Components: STT (ElevenLabs), TTS (Edge/ElevenLabs)

Capabilities:
✅ Continuous voice loop
✅ VAD-based listening
✅ Multi-backend TTS
✅ Error recovery

Version: 3.0.0
Status: ✅ Active (Production)
```

#### **qa_gato3_agent** | QA Specialist
```
Path: qa_gato3_agent/
Prime: /prime-qa-gato3
Purpose: Automated QA validation for GATO3 e-commerce

Target: gatoaocubo.lovable.app | gato3.com.br
Stack: React + Vite + Tailwind + Supabase + Shopify

Capabilities:
✅ Page load validation
✅ SEO checks
✅ Accessibility (WCAG 2.1 AA)
✅ Checkout flow testing

Version: 1.0.0
Status: ✅ Active (Production)
```

#### **ronronalda_agent** | GATO3 Assistant
```
Path: ronronalda_agent/
Prime: /prime-ronronalda
Purpose: AI cat assistant for GATO3 e-commerce platform

Capabilities:
✅ Product recommendations based on cat issues
✅ Brazilian Portuguese natural conversation
✅ Integration with Shopify catalog

Version: 1.0.0
Status: 🔄 Beta (In Development)
```

---

### ⚠️ [ARCHIVED] Legacy Agents

#### **conhecimento_agent** | Consolidated into mentor_agent
```
Status: ⚠️ ARCHIVED (Consolidated 2025-11-13)

Legacy commands removed:
/prime-knowledge, /knowledge   - Now in /prime-mentor

All functionality now available in mentor_agent v2.5.0
See: agentes/mentor_agent/PRIME.md
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

=== MEDIA & CONTENT ===
IF (gerar prompts de foto IA)       → /prime-photo
IF (criar vídeo de produto)         → /prime-video
IF (construir curso Hotmart)        → /prime-curso

=== KNOWLEDGE & MENTORING ===
IF (extrair conhecimento)           → /prime-mentor + /processar
IF (ensinar sobre tema)             → /prime-mentor (Aula ao Vivo)
IF (processar arquivos RASCUNHO)    → /prime-mentor + /processar
IF (planejamento estratégico)       → /prime-mentor

=== INFRASTRUCTURE ===
IF (descobrir arquivos por task)    → /prime-scout
IF (interação por voz)              → /v (voice mode)
IF (validar QA GATO3)               → /prime-qa-gato3
IF (assistente gatos GATO3)         → /prime-ronronalda

=== NAVIGATION ===
IF (não sabe qual usar)             → /prime (root navigator)
IF (overview do sistema)            → README.md files
```

---

## 📊 ESTATÍSTICAS

| Agente | Versão | Type | Status |
|--------|--------|------|--------|
| **codexa_agent** | 2.5.0 | Meta-Constructor | ✅ Active |
| **anuncio_agent** | 2.5.0 | E-Commerce | ✅ Active |
| **pesquisa_agent** | 2.5.0 | E-Commerce | ✅ Active |
| **marca_agent** | 2.5.0 | E-Commerce | ✅ Active |
| **mentor_agent** | 2.5.0 | Knowledge | ✅ Active |
| **photo_agent** | 2.5.0 | Media | ✅ Active |
| **video_agent** | 2.5.0 | Media | ✅ Active |
| **curso_agent** | 2.5.1 | Media | ✅ Active |
| **scout_agent** | 1.0.0 | Infrastructure (MCP) | ✅ Active |
| **voice_agent** | 3.0.0 | Infrastructure (MCP) | ✅ Active |
| **qa_gato3_agent** | 1.0.0 | QA Specialist | ✅ Active |
| **ronronalda_agent** | 1.0.0 | GATO3 Domain | 🔄 Beta |

**Total**: 12 agentes ativos | 5 Production ADW workflows | 3 MCP Servers

---

## 🔗 PATHWAYS (Cross-References)

### Superior (Parent)
- `../PRIME.md` - Sistema de agentes (codexa.app)
- `../README.md` - Estrutura de agentes (codexa.app)

### Inferior (Children - All Agents)
- `codexa_agent/PRIME.md` - Meta-constructor context
- `anuncio_agent/PRIME.md` - Ad generation context
- `pesquisa_agent/PRIME.md` - Research context
- `marca_agent/PRIME.md` - Brand strategy context
- `mentor_agent/PRIME.md` - Strategic planning context
- `photo_agent/PRIME.md` - AI photography context
- `video_agent/PRIME.md` - Video production context
- `curso_agent/PRIME.md` - Course builder context
- `scout_agent/PRIME.md` - Path discovery context (MCP)
- `voice_agent/PRIME.md` - Voice interface context (MCP)
- `qa_gato3_agent/PRIME.md` - QA specialist context
- `ronronalda_agent/PRIME.md` - GATO3 assistant context

### Lateral (Related)
- `51_AGENT_REGISTRY.json` - Metadata registry
- `DOCUMENTATION_INDEX.md` - Documentation index
- `SCOUT_INTEGRATION.md` - **Como usar Scout em todos agentes**
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

### Workflow 3: Media Content Pipeline
```bash
1. /prime-photo                      # Load photo context
2. Generate photography prompts      # 9-scene grid
   → Output: photo_prompts.md

3. /prime-video                      # Load video context
4. Generate product video            # 15-60s
   → Output: final_video.mp4 + metadata

Time: 3-5 min (photos) + 3-5 min (video) = ~10 min total
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

**Versão**: 1.0.0
**Data**: 2025-11-14
**Status**: ✅ 7 Agentes Operacionais
**Tipo**: Agents Index (Fractal Level 3)

---

> 🤖 **AGENTES**: 7 especializados (1 meta + 3 e-commerce + 2 knowledge + 1 dev)
> 🗺️ **NAVEGAÇÃO**: Use /prime-{agent} para carregar contexto específico
> 🏗️ **META**: codexa_agent constrói e valida todos os outros agentes
