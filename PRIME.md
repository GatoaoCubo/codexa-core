# PRIME: ECOMLM.CODEXA System Navigator

**Master entry point** - Navigation for e-commerce AI multi-agent system

---

## 1. SYSTEM IDENTITY

**ECOMLM.CODEXA**: E-commerce AI multi-agent orchestration for Brazilian marketplaces
**Purpose**: End-to-end automation (research → ads) - 95% time reduction, 100% compliance
**Version**: 1.0.0

---

## 2. FRACTAL NAVIGATION

### Level 1: ROOT (here)
```
/
├── PRIME.md          → Master navigator
├── README.md         → Project overview
├── codexa.app/       → Agent system (L2)
├── app/              → FastAPI + Vite
└── .claude/          → Claude integration
```
**Command**: `/prime`

### Level 2: CODEXA.APP
```
codexa.app/
├── PRIME.md      → Agent instructions
├── agentes/      → Implementations (L3)
├── commands/     → Slash commands
└── 41-51_*.md    → Core docs
```
**Command**: `/prime-codexa`

### Level 3: AGENTS
```
agentes/
├── codexa_agent/   → Meta-constructor
├── anuncio_agent/  → Ad generation
├── pesquisa_agent/ → Market research
├── marca_agent/    → Brand strategy
├── mentor_agent/   → Strategic planning
├── photo_agent/    → Photo prompts
└── scout_agent/    → Code navigation
```
**Commands**: `/prime-{agent}`

### Level 4: AGENT
```
{agent}/
├── PRIME.md        → Domain context
├── INSTRUCTIONS.md → Operations
├── prompts/        → HOPs (TAC-7)
└── config/         → Settings
```

---

## 3. COMMANDS

### Navigation
`/prime` - System status + routing

### Meta-Construction
```
/prime-codexa       → Load context
/codexa-build_agent → Create agent (5-phase)
/codexa-build_prompt → Create HOP (TAC-7)
/codexa-build_command → Create command
/codexa-orchestrate → Workflow orchestration
/codexa-when_to_use → Decision tree
```

### Domain Specialists
```
/prime-anuncio  → Ad generation
/prime-pesquisa → Market research
/prime-marca    → Brand strategy
/prime-mentor   → Strategic planning
/prime-photo    → Photo prompts
```

---

## 4. TOOLS

### Builders
```
codexa_agent/builders/ (8 total)
├── 02_agent_meta_constructor.py → 5-phase builder
├── 08_prompt_generator.py       → HOP generator
├── 05_command_generator.py      → Command creator
└── 11_doc_sync_builder.py       → Doc sync
```

### Validators
```
codexa_agent/validators/ (4 total)
├── 07_hop_sync_validator.py    → TAC-7 compliance
├── 09_readme_validator.py      → README standards
├── 10_taxonomy_validator.py    → Registry consistency
└── 12_doc_sync_validator.py    → Doc sync validation
```

### HOPs
```
81+ HOPs: codexa(3) anuncio(15) pesquisa(22) marca(1) mentor(16) scout(1)
```

### Commands
```
52+ commands: prime(8) codexa(7) domain(37+)
```

---

## 5. QUICK START

**New Users**: README.md → codexa.app/PRIME.md → /prime → /prime-pesquisa

**Build Agents**: /prime-codexa → /codexa-when_to_use → /codexa-build_agent

**Generate Ads**: /prime-pesquisa → /pesquisa "product" → /prime-anuncio → /anuncio

---

## 6. PRINCIPLES

**"Build the thing that builds the thing"**

1. Meta > Instance - Build builders, not artifacts
2. Templates > One-offs - Reusable patterns
3. Discovery-First - Find before building
4. Quality Gates - Validate every phase (≥7.0/10.0)
5. Fractal Navigation - Each level reflects below
6. Self-Improvement - System builds itself

**codexa_agent**: Builds agents | Validates components | Orchestrates workflows | Self-improves (bootstrapping)

---

## 7. METRICS

```
Agents: 7 (anuncio, pesquisa, marca, scout, mentor, photo, codexa)
Commands: 52+ (/prime 8, /codexa 7, domain 37+)
HOPs: 81+
Builders: 8
Validators: 4
```
**Registry**: `codexa.app/51_AGENT_REGISTRY.json`

---

## 8. DECISION TREE

```
Build agent?       → /prime-codexa + /codexa-build_agent
Create command?    → /prime-codexa + /codexa-build_command
Create HOP?        → /prime-codexa + /codexa-build_prompt
Orchestrate?       → /prime-codexa + /codexa-orchestrate

Ad generation?     → /prime-anuncio + /anuncio
Market research?   → /prime-pesquisa + /pesquisa
Brand strategy?    → /prime-marca + /marca
Strategic plan?    → /prime-mentor + /mentor
Photo prompts?     → /prime-photo + /photo

Not sure?          → /prime (here!)
```

---

## 9. RULES

**NEVER**: Run .py directly | Modify core files | Create loose files | Skip validation

**ALWAYS**: Read docs first | Use slash commands | Validate output | Organize correctly | Follow patterns (TAC-7, ADW)

---

## 10. PATHWAYS

**Parent**: N/A (ROOT)

**Children**: codexa.app/PRIME.md | codexa.app/agentes/PRIME.md

**Related**: README.md | .claude/commands/prime.md | codexa.app/51_AGENT_REGISTRY.json | codexa.app/41_DOCUMENTATION_INDEX.md | codexa.app/42_HOP_FRAMEWORK.md

---

## 11. KEY DOCS

```
README.md (root)                     → Project overview
codexa.app/PRIME.md                  → Agent system
codexa.app/41_DOCUMENTATION_INDEX.md → Doc index
codexa.app/42_HOP_FRAMEWORK.md       → TAC-7 framework
codexa.app/51_AGENT_REGISTRY.json    → Agent registry
codexa.app/agentes/{agent}/PRIME.md  → Agent context
```

---

## 12. EXECUTION

```
NAVIGATION:
1. PRIME.md → 2. Identify (§8) → 3. /prime-{specialist} → 4. Execute

META-CONSTRUCTION:
/prime-codexa → /codexa-when_to_use → /codexa-build_* → Validate

DOMAIN:
/prime-{agent} → Run commands → Validate
```

---

**Version**: 2.0.0 | **Updated**: 2025-11-15 | **Target**: ≤8000 chars
**Status**: Production | **Type**: Master navigator (Fractal root)

> TIP: /prime (navigate) | /prime-codexa (build) | /prime-{agent} (specialize)
