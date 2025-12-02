# Documentation Index - CODEXA System

> Consolidated documentation index for the CODEXA meta-construction system.
> Last updated: 2025-11-24 (Added FONTES/ external knowledge base)

## 📚 Documentation Structure

### 📁 Claude Code Commands (NEW - 2025-11-12)

Located in: `.claude/commands/`

**Commands reorganized following HOW_TO_BUILD_COMMANDS.md standards**

| Location | Content | Count |
|----------|---------|-------|
| `.claude/commands/` | Generic commands (root) | 30 |
| `.claude/commands/docs/` | Documentation & guides | 7 |
| `.claude/commands/utils/` | Utility commands | 8 |
| `.claude/commands/_archived/` | Historical files (cleaned) | 0 |
| `agentes_codexa/*/commands/` | Agent-specific commands | 13 |
| `tests/e2e_commands/` | E2E test commands | 6 |

**Key Documentation:**
- [README.md](../.claude/commands/README.md) - Complete commands structure
- [REORGANIZATION_SUMMARY.md](../.claude/commands/REORGANIZATION_SUMMARY.md) - Reorganization details
- [COMMAND_BEST_PRACTICES.md](../.claude/commands/docs/COMMAND_BEST_PRACTICES.md) - Best practices
- [HOW_TO_BUILD_COMMANDS.md](how_to/HOW_TO_BUILD_COMMANDS.md) - Command building guide

---

### 📚 FONTES/ - External Knowledge Base (NEW - 2025-11-24)

Located in: `../FONTES/`

**Purpose**: External reference materials and documentation from third-party sources

| Source | Content | Status |
|--------|---------|--------|
| `ai_tools_prompts/` | System prompts from 30+ AI tools | ✅ Active |
| `ai_tools_prompts/cursor/` | Complete Cursor analysis | ✅ Complete |
| `[future sources]` | Frameworks, APIs, research | 📁 Planned |

**Key Documentation:**
- [FONTES/README.md](../../FONTES/README.md) - External sources overview
- [ai_tools_prompts/README.md](../../FONTES/ai_tools_prompts/README.md) - Knowledge base docs
- [ai_tools_prompts/QUICK_START.md](../../FONTES/ai_tools_prompts/QUICK_START.md) - Usage guide
- [PLATFORM_REGISTRY.json](../../FONTES/ai_tools_prompts/PLATFORM_REGISTRY.json) - Platform index

**Access Command:**
```bash
/codexa-query_platform [platform_name]  # Query AI tools knowledge
```

**Platforms Documented:**
- ✅ **Cursor**: Complete (prompt + tools + patterns + integration notes)
- 🔄 **Claude Code, Devin, v0**: Partial
- 📁 **Windsurf, Replit, Lovable, Perplexity, Cursor Composer**: Structure ready

**Use Cases:**
- Pattern reference for HOP development
- Cross-platform orchestration knowledge
- Competitive analysis and inspiration
- Foundation for platform-specific builders

**Integration:**
- Current: `/codexa-query_platform` command
- Future: `/codexa-build_for_[platform]`, `/codexa-analyze_patterns`

---

### 🔍 MENTOR Agent Documentation (Consolidated System)

✅ **Status**: Active - Consolidated from scout_agent + conhecimento_agent (2025-11-13)

**Location**: `mentor_agent/`

| Component | Purpose | Location |
|----------|---------|----------|
| PRIME | Philosophy & principles | [mentor_agent/PRIME.md](mentor_agent/PRIME.md) |
| README | Agent overview | [mentor_agent/README.md](mentor_agent/README.md) |
| Scout navigation | Discovery-driven search | [mentor_agent/prompts/](mentor_agent/prompts/) |
| Knowledge processing | RAW → Processed pipeline | [mentor_agent/PROCESSADOS/](mentor_agent/PROCESSADOS/) |

**Key Capabilities:**
- Developer onboarding & guidance
- System validation & QA workflows
- Discovery-driven codebase navigation (from scout_agent)
- Knowledge base management (from conhecimento_agent)

---

### 📝 Migration & Consolidation Documentation

**Knowledge extracted to mentor_agent** (2025-11-13)

**Key Patterns Documented:**
- Fractal Migration Patterns → [mentor_agent/PROCESSADOS/](mentor_agent/PROCESSADOS/)
- Cleanup Automation Patterns → [mentor_agent/PROCESSADOS/](mentor_agent/PROCESSADOS/)
- Consolidation Workflows → [codexa_agent/workflows/98_ADW_CONSOLIDATION_WORKFLOW.md](codexa_agent/workflows/98_ADW_CONSOLIDATION_WORKFLOW.md)

---

## 📁 Archive Structure

### Archive Status: ✅ Reset & Auto-Archive Enabled (2025-11-15)

**Location**: `_archived/`
**Status**: Complete reset, auto-archive policy in effect

**Policy Documentation**:
- 📖 [_archived/README.md](_archived/README.md) - Auto-archive policy and workflow
- 🚫 [_archived/.gitignore](_archived/.gitignore) - Git ignores all contents (local-only)

**Auto-Archive Rules**:
- ✅ Reports, logs, summaries → Automatically saved to `_archived/`
- ✅ Obsolete docs (after knowledge extraction) → Moved to `_archived/`
- ✅ Migration backups → Timestamped in `_archived/`
- ✅ Workflow outputs → Direct to `_archived/` (not root)
- ❌ Git tracking: Disabled (local-only, not versioned)

**Rationale**: Keep working tree clean, archive is developer-local for historical reference

---

## 🔄 Agent System Overview

### Active Agents (6)
1. **codexa_agent**: Meta-construction & self-improvement
2. **anuncio_agent**: E-commerce listing generation
3. **pesquisa_agent**: Market research & competitive analysis
4. **marca_agent**: Brand strategy & positioning
5. **mentor_agent**: Onboarding, QA, knowledge management
6. **photo_agent**: AI product photography

### Consolidated Agents (Historical)
- **scout_agent** → Merged into mentor_agent (2025-11-13)
- **conhecimento_agent** → Merged into mentor_agent (2025-11-13)

---

## 📈 Consolidation Metrics (Nov 2025 Cleanup)

| Metric | Before (Nov 12) | After (Nov 19) | Improvement |
|--------|-----------------|----------------|-------------|
| Active agents | 8 | 6 | -25% (2 consolidated) |
| Root files (loose) | 10+ | 3 core | -70% |
| ISO_VECTORSTORE files | 4 | 0 (deleted) | -100% |
| Obsolete docs | Multiple | 0 | -100% |
| Knowledge cards | 47 | 49+ | +2 cards |
| Documentation status | ✅ Updated | ✅ Current | Maintained |

---

## 🚀 Quick Start Paths

### For New Users
1. Read [README.md](README.md) - System overview
2. Check [51_AGENT_REGISTRY.json](51_AGENT_REGISTRY.json) - All agents catalog
3. Choose agent → Read its PRIME.md for philosophy

### For Mentor Agent Users (Onboarding/QA)
1. Start with [mentor_agent/PRIME.md](mentor_agent/PRIME.md)
2. Read [mentor_agent/README.md](mentor_agent/README.md)
3. Review capabilities (includes scout + knowledge functionality)

### For Agent Developers
1. Use `/prime-codexa` then `/codexa-build_agent` - Meta-constructor
2. Follow [PRIME.md](PRIME.md) - Core principles
3. Check [codexa_agent/workflows/](codexa_agent/workflows/) - Build patterns

---

## 🔧 Maintenance Notes

### Documentation Standards
- All active documentation in root or agent folders
- Archives in `_archived/` subdirectories
- Test files in dedicated `tests/` folder
- Analysis scripts in `analysis/` folder

### Update Protocol
1. Update this index when adding/removing documentation
2. Move deprecated docs to archive with date stamp
3. Maintain cross-references between related docs
4. Update consolidation metrics quarterly

### Version Control
- This index: v3.0 (Post-cleanup)
- Scout docs: v4.0
- CRUD docs: v3.0 (Consolidated)
- Archive: v2.0 (Cleaned)

---

*Last updated: 2025-11-19 (Agent consolidation + ISO_VECTORSTORE cleanup)*
*For agent details, see [51_AGENT_REGISTRY.json](51_AGENT_REGISTRY.json)*
*For system principles, see [PRIME.md](PRIME.md)*