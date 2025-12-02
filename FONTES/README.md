# FONTES/ - External Knowledge & Reference Materials

## Purpose

This directory contains **external reference materials, documentation, and knowledge bases** that support CODEXA development and operations. Unlike `codexa.app/` which contains CODEXA's own logic, FONTES/ stores curated external knowledge.

## Directory Structure

```
FONTES/
├── README.md                    # This file
├── ai_tools_prompts/            # System prompts from AI coding tools
│   ├── README.md                # Knowledge base documentation
│   ├── QUICK_START.md           # Usage guide
│   ├── PLATFORM_REGISTRY.json   # Index of all platforms
│   └── [platform_name]/         # Per-platform documentation
│       ├── system_prompt.txt
│       ├── tools.json
│       ├── metadata.json
│       └── NOTES.md
└── [future external sources]/   # Additional external knowledge bases
```

## Contents

### 1. ai_tools_prompts/ - AI Tools Knowledge Base

**Purpose**: Reference library of system prompts and patterns from 30+ AI coding platforms

**What's Inside**:
- System prompts from tools like Cursor, Devin, v0, Claude Code
- Tool definitions and capabilities
- Unique patterns and architectural insights
- Integration suggestions for CODEXA

**How to Use**:
```bash
# Query platform information
/codexa-query_platform cursor

# Compare platforms
/codexa-query_platform cursor,devin,v0

# Get integration ideas
/codexa-query_platform cursor --integration
```

**Documentation**:
- [ai_tools_prompts/README.md](ai_tools_prompts/README.md) - Full documentation
- [ai_tools_prompts/QUICK_START.md](ai_tools_prompts/QUICK_START.md) - Quick usage guide
- [ai_tools_prompts/PLATFORM_REGISTRY.json](ai_tools_prompts/PLATFORM_REGISTRY.json) - Platform index

**Source**: https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools

---

### Future External Sources (Planned)

**Potential Additions**:
- `/frameworks/` - External framework documentation (Next.js, React, etc.)
- `/apis/` - Third-party API references (Stripe, Supabase, etc.)
- `/research/` - AI/ML research papers and insights
- `/patterns/` - Software engineering patterns and best practices
- `/competitors/` - Competitive analysis and market research

---

## Integration with CODEXA

### Commands that Use FONTES/

**Existing**:
- `/codexa-query_platform` - Query AI tools knowledge base

**Future**:
- `/codexa-build_for_[platform]` - Build platform-specific code
- `/codexa-analyze_patterns` - Extract patterns from external sources
- `/codexa-import_external` - Import new external documentation

### How Agents Use This

**Current**:
- `codexa_agent`: Reference for building better prompts/HOPs
- Pattern inspiration for agent architecture
- Cross-platform orchestration knowledge

**Future**:
- Platform-specific code generation
- Automated pattern extraction
- Competitive feature analysis

---

## Guidelines

### What Goes in FONTES/

**DO Add**:
- ✅ External documentation (not created by CODEXA)
- ✅ Reference materials for development
- ✅ Curated knowledge from external sources
- ✅ Competitor analysis and market research
- ✅ Third-party tool documentation

**DON'T Add**:
- ❌ CODEXA's own code/logic (use `codexa.app/`)
- ❌ Generated outputs (use `_archived/` or working directories)
- ❌ User data or secrets
- ❌ Temporary files or cache

### Maintenance

**Update Frequency**:
- **ai_tools_prompts**: Weekly check for new platforms/updates
- **Other sources**: As needed when new knowledge is required

**Curation**:
- Focus on actionable, high-value information
- Document insights, not just raw data
- Maintain index files for discoverability
- Version external knowledge when appropriate

### Licensing

All external materials in FONTES/ are:
- For **reference and learning only**
- **Not for direct copying** (respect source licenses)
- **Must cite sources** in documentation
- Used for **inspiration and pattern analysis**

Current licenses:
- `ai_tools_prompts/`: GPL-3.0 (reference only from x1xhlol repo)

---

## Adding New External Sources

### Process

1. **Create Directory**:
   ```bash
   mkdir FONTES/[source_name]/
   ```

2. **Add Documentation**:
   - `README.md` - Purpose and contents
   - `[content files]` - Actual reference materials
   - `metadata.json` - Source info, license, dates

3. **Update This File**:
   - Add to "Contents" section
   - Document how to use
   - Note integration points

4. **Create Access Command** (if needed):
   ```bash
   # Example: /codexa-query_[source_name]
   ```

5. **Update DOCUMENTATION_INDEX**:
   - Add entry in `codexa.app/agentes/DOCUMENTATION_INDEX.md`

---

## Relationship to Other Directories

```
Project Root
├── FONTES/                      ← External knowledge (YOU ARE HERE)
│   └── ai_tools_prompts/        ← Reference: How other tools work
│
├── codexa.app/                  ← CODEXA's own logic
│   ├── agentes/                 ← Agent implementations
│   └── docs_consolidados/       ← Internal CODEXA documentation
│
├── .claude/commands/            ← Active slash commands
│   └── codexa_query_platform.md ← Uses FONTES/ai_tools_prompts/
│
└── _archived/                   ← Historical outputs (local only)
```

**Key Distinction**:
- **FONTES/**: External, for reference → "What others do"
- **codexa.app/**: Internal, for execution → "What CODEXA does"

---

## Quick Reference

**Browse AI Tools**:
```bash
/codexa-query_platform
```

**Get Specific Platform**:
```bash
/codexa-query_platform cursor
```

**Compare Approaches**:
```bash
/codexa-query_platform cursor,devin
```

**View Registry**:
```bash
cat FONTES/ai_tools_prompts/PLATFORM_REGISTRY.json
```

---

## Status

**Last Updated**: 2025-11-24
**Total Sources**: 1 (ai_tools_prompts)
**Total Platforms Documented**: 9 (1 complete, 8 partial/planned)
**Integration Commands**: 1 (/codexa-query_platform)

---

**Next Steps**:
1. Expand ai_tools_prompts with more platforms
2. Add framework documentation (Next.js, React)
3. Create API reference library
4. Build automated sync mechanisms
