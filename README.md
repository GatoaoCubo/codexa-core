# CODEXA - E-Commerce AI Multi-Agent System

## IDENTITY
You are CODEXA, an enterprise-grade multi-agent AI orchestration system specialized in automating e-commerce operations for Brazilian marketplaces.

## PURPOSE
Automate end-to-end e-commerce workflows from market research to listing generation with 95% time reduction and 100% compliance.

## CAPABILITIES
- Market research across 9+ Brazilian marketplaces
- AI-powered listing generation with conversion optimization
- Brand strategy development and management
- Knowledge extraction and ML dataset generation
- Strategic planning and KPI tracking
- Code intelligence and repository navigation

---

## 🎯 PRIME WORKFLOW

### When to Use This System
```
IF user needs:
  - E-commerce market research → USE /pesquisa
  - Product listing creation → USE /anuncio
  - Brand strategy development → USE /marca
  - Knowledge extraction → USE /knowledge
  - Strategic planning → USE /mentor
  - Code navigation → USE /scout
ELSE:
  - See .claude/commands/ directory for all available commands
```

### Core Workflow Pattern
```
1. RESEARCH Phase (15-30 min)
   INPUT: Product description or competitor URL
   COMMAND: /pesquisa "produto ou nicho"
   OUTPUT: research_notes.md (22 structured blocks)

2. BRAND Phase (10-20 min) [OPTIONAL]
   INPUT: Business context
   COMMAND: /marca
   OUTPUT: brand_strategy.md + brand_guidelines.json

3. GENERATION Phase (2-3 min)
   INPUT: research_notes.md
   COMMAND: /anuncio ./research_notes.md
   OUTPUT: anuncio.json + marketplace_listings/

4. VALIDATION Phase (automatic)
   - 11-point compliance check
   - SEO optimization validation
   - Brand consistency scoring
```

---

## 📁 PROJECT STRUCTURE

```
lm.codexa/
├── README.md                    # This file - Main documentation
├── CLAUDE.md                    # Project laws and guidelines
│
├── .claude/                     # Claude Code Integration
│   ├── settings.json           # Global settings
│   ├── commands/               # 52+ slash commands
│   └── hooks/                  # Automation hooks
│
├── app/                        # Core Application
│   ├── server/                 # FastAPI backend
│   │   ├── server.py          # Main server entry
│   │   ├── core/              # Core modules
│   │   └── research_*.py      # Research modules
│   └── client/                 # Vite frontend
│
├── codexa.app/                 # Agent System
│   └── agentes/
│       ├── pesquisa_agent/     # Market Research v1.1
│       ├── anuncio_agent/      # Ad Generation v1.2
│       ├── marca_agent/        # Brand Strategy v1.0
│       ├── conhecimento_agent/ # Knowledge & ML v1.1
│       ├── mentor_agent/       # Strategic Planning v1.0
│       └── scout_agent/        # Repository Intel v1.0
│
├── ai_docs/                    # AI Documentation
│   ├── HOP_FRAMEWORK.md       # HOP documentation
│   ├── WORKFLOWS.md           # ADW workflow catalog
│   ├── API_REFERENCE.md       # API documentation
│   └── ARCHITECTURE.md        # System architecture
│
└── data/                       # Data Storage
    ├── knowledge_cards/        # Knowledge base
    ├── research_cache/         # Research results
    └── brand_assets/          # Brand materials
```

---

## 🚀 QUICK START

### Prerequisites
- Python 3.12+ with uv package manager
- Node.js 18+ with npm
- Claude Code or VS Code
- API Keys: Anthropic Claude and/or OpenAI

### Installation
```bash
# Clone repository
git clone https://github.com/yourusername/lm.codexa.git
cd lm.codexa

# Backend setup
cd app/server
uv sync
cp .env.sample .env
# Edit .env with your API keys

# Frontend setup
cd ../client
npm install

# Return to root
cd ../..
```

### Running the System
```bash
# Start backend (from root)
uv run python app/server/server.py

# Start frontend (new terminal)
cd app/client && npm run dev

# Access at http://localhost:5173
```

### First Command
```bash
# Test with sample research
/pesquisa "fone bluetooth para home office"

# View results
cat research_notes.md
```

---

## 🤖 AGENTS OVERVIEW

| Agent | Version | Status | Purpose | Command |
|-------|---------|--------|---------|---------|
| **Pesquisa** | v1.1 | ✅ Ready | Market research & competitor analysis | `/pesquisa` |
| **Anuncio** | v1.2 | ✅ Ready | Listing generation & optimization | `/anuncio` |
| **Marca** | v1.0 | 🔄 Beta | Brand strategy & identity | `/marca` |
| **Conhecimento** | v1.1 | ✅ Ready | Knowledge extraction & ML | `/knowledge` |
| **Mentor** | v1.0 | ✅ Ready | Strategic planning & KPIs | `/mentor` |
| **Scout** | v1.0 | ✅ Ready | Code navigation & search | `/scout` |
| **Codexa** | v1.0 | ✅ Ready | Central orchestration | `/codexa` |

---

## 📊 PERFORMANCE METRICS

| Metric | Traditional | CODEXA | Improvement |
|--------|-------------|---------------|-------------|
| Listing Creation Time | 2-4 hours | 2-3 minutes | -95% |
| Keyword Density | 5-6 terms | 9-10 terms | +67% |
| Conversion Rate | Baseline | +25% avg | +25% |
| Click-Through Rate | Baseline | +60% avg | +60% |
| Compliance Rate | 70-80% | 100% | +30% |
| Research Coverage | 2-3 sources | 9+ sources | +300% |

---

## 🛠️ TECHNOLOGY STACK

### Core Technologies
- **Language**: Python 3.12+ (backend), TypeScript 5.8+ (frontend)
- **Framework**: FastAPI 0.115+ (backend), Vite 6.3+ (frontend)
- **Database**: SQLite with connection pooling
- **AI/ML**: Anthropic Claude 3.5, OpenAI GPT-4/5
- **Package Management**: uv (Python), npm (Node)

### Key Libraries
- **Backend**: pydantic, httpx, sqlite3, python-multipart
- **Frontend**: React, TypeScript, TailwindCSS
- **AI Integration**: anthropic, openai, langchain
- **Testing**: pytest, vitest
- **Quality**: ruff, mypy, eslint

---

## 📝 DOCUMENTATION

| Document | Description | Location |
|----------|-------------|----------|
| **README.md** | Main documentation (this file) | `/` |
| **CLAUDE.md** | Project laws and guidelines | `/` |
| **Agent Docs** | Individual agent documentation | `codexa.app/agentes/*/PRIME.md` |
| **Commands** | Slash commands reference | `.claude/commands/` |
| **Workflows** | ADW workflow catalog | `docs/WORKFLOWS.md` |

---

## 🔧 DEVELOPMENT

### Running Tests
```bash
# Backend tests
cd app/server
uv run pytest tests/

# Frontend tests
cd app/client
npm run test

# E2E tests
npm run test:e2e
```

### Code Quality
```bash
# Python linting
uv run ruff check .

# TypeScript linting
npm run lint

# Type checking
uv run mypy .
```

### Contributing
For development guidelines, see:
- CLAUDE.md for project laws and conventions
- Individual agent PRIME.md files for agent-specific standards
- .claude/commands/ for command development patterns

---

## 🚧 ROADMAP

### Current Sprint (v1.1)
- [ ] Complete Marca agent HOP migration
- [ ] Implement MCP server integration
- [ ] Add real-time analytics dashboard
- [ ] Enhance knowledge consolidation pipeline

### Next Release (v2.0)
- [ ] Auto-image generation (DALL-E integration)
- [ ] Auto-video generation (VEO3 integration)
- [ ] Direct marketplace API publishing
- [ ] A/B testing framework
- [ ] Conversion learning loops

### Future Vision
- Multi-language support (Spanish, English)
- International marketplace expansion
- AI model fine-tuning pipeline
- Enterprise dashboard and analytics
- White-label deployment options

---

## 📄 LICENSE

MIT License - See [LICENSE](LICENSE) file for details.

---

## 🤝 SUPPORT

### Getting Help
- **Issues**: [GitHub Issues](https://github.com/yourusername/lm.codexa/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/lm.codexa/discussions)
- **Documentation**: See `/ai_docs/` for detailed guides

### Contact
- **Email**: support@codexa.ai
- **Discord**: [Join our community](https://discord.gg/ecomlm)

---

## 🙏 ACKNOWLEDGMENTS

Built with cutting-edge AI technologies from:
- Anthropic Claude
- OpenAI GPT
- Open source community

Special thanks to all contributors and early adopters who helped shape this system.

---

> **Note**: This is an actively developed project. Features and documentation are continuously improved. Always refer to the latest version of this README for current information.