# Scout Agent | Quick Start

## Overview
Scout is the "Master of Paths" - the navigation nervous system for CODEXA. It provides file discovery, CRUD operations, and context building for all agents.

## Quick Commands

```javascript
// Find files related to a task
mcp__scout__discover("create product listing")

// Get all files for an agent
mcp__scout__agent_context("anuncio_agent")

// Search by pattern
mcp__scout__search("**/*_HOP.md")
```

## File Structure

```
scout_agent/
├── PRIME.md           # Agent philosophy & API
├── INSTRUCTIONS.md    # Usage guide
├── README.md          # Quick reference
├── SETUP.md           # Installation
├── config/
│   ├── categories.json      # Category detection
│   ├── ignore_patterns.json # Files to ignore
│   └── relevance_weights.json # Scoring weights
└── iso_vectorstore/
    └── (this folder)
```

## Key Features

1. **Discovery** - Natural language file finding
2. **Search** - Glob pattern matching
3. **Context** - Agent file aggregation
4. **CRUD** - Safe file operations with backups
5. **Relationships** - Dependency mapping

## Next Steps

1. Read `02_PRIME.md` for full API reference
2. Read `03_INSTRUCTIONS.md` for usage patterns
3. Check `config/` for customization options

---

**Version**: 1.0.0 | **Updated**: 2025-11-30
