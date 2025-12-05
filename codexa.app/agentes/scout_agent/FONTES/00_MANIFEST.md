# 00_MANIFEST | Scout Agent Knowledge Base

**Version**: 1.0.0 | **Created**: 2025-12-05
**Agent**: scout_agent
**Purpose**: Domain knowledge for file discovery and codebase navigation
**Status**: Active

---

## Overview

Este diretorio contem o conhecimento de dominio do scout_agent - o sistema nervoso de navegacao do CODEXA. O conhecimento aqui e focado em patterns de busca, indexacao e otimizacao de contexto para LLMs.

## Categories

| ID | Category | Files | Description |
|----|----------|-------|-------------|
| 01 | SEARCH_PATTERNS | 3 | Algoritmos e patterns de busca |
| 02 | CODEBASE_NAVIGATION | 2 | Navegacao e descoberta de arquivos |
| 03 | MCP_PATTERNS | 2 | Patterns para MCP servers |

## Total Files

- **Knowledge Cards**: 7
- **Manifest Files**: 1
- **Total**: 8 files

## Search Triggers

Keywords que ativam busca neste conhecimento:

```
# Search & Indexing
search, busca, find, encontrar, discover, descobrir
index, indexar, catalog, catalogo
relevance, relevancia, score, ranking

# File Discovery
file, arquivo, path, caminho, directory, diretorio
glob, pattern, regex, match
navigate, navegar, explore, explorar

# Context & Optimization
context, contexto, token, budget
llm, large language model, ai, artificial intelligence
mcp, model context protocol, tool, ferramenta

# Scout-Specific
scout, discovery, smart_context, agent_context
```

## Cross-Agent References

| Agent | Related Knowledge | Use Case |
|-------|-------------------|----------|
| codexa_agent | Meta-construction patterns | Building new agents |
| mentor_agent | FONTES/PROMPT_ENGINEERING | Search in knowledge bases |
| all_agents | iso_vectorstore structure | Consistent file organization |

## File Index

### SEARCH_PATTERNS/

```
SEARCH_PATTERNS/
├── semantic_search.md           # Embedding-based search patterns
├── relevance_scoring.md         # Multi-factor scoring algorithms
└── indexing_strategies.md       # File indexing best practices
```

### CODEBASE_NAVIGATION/

```
CODEBASE_NAVIGATION/
├── llm_context_optimization.md  # Token budget management
└── file_discovery_patterns.md   # Pattern matching for LLMs
```

### MCP_PATTERNS/

```
MCP_PATTERNS/
├── tool_design.md               # MCP tool best practices
└── server_architecture.md       # MCP server patterns
```

## Quality Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Card Quality Score | >= 0.75 | 0.82 |
| Coverage | 100% | 100% |
| Cross-references Valid | 100% | 100% |

## Usage

### Via Scout Tools

```
mcp__scout__discover("semantic search patterns")
mcp__scout__smart_context(agent="scout_agent")
```

### Direct Reading

```
/prime-scout  # Load scout context with FONTES
```

## Maintenance

- **Refresh Frequency**: Monthly
- **Last Updated**: 2025-12-05
- **Next Review**: 2026-01-05

---

**Author**: codexa_agent (meta-constructor)
**Reference**: ADW-300 Knowledge Hydration
