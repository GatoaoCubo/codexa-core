# Scout Agent - Path Discovery & Navigation

> "Master of Paths" - Every agent's companion

## Quick Start

### 1. Install Dependencies
```bash
cd codexa.app/mcp-servers/scout-mcp
npm install
```

### 2. Configure MCP (already done)
The `.mcp.json` is already configured. Scout will start automatically with Claude Code.

### 3. Use Scout Tools
```
mcp__scout__discover("your query")
mcp__scout__search("**/*.md")
mcp__scout__agent_context("agent_name")
```

---

## What is Scout?

Scout is an **MCP Server** that indexes your entire project and provides:

- **Path Discovery**: Find files using natural language queries
- **Pattern Search**: Search using glob patterns
- **Agent Context**: Get all files for any agent
- **CRUD Operations**: Safe create/read/update/delete with backups
- **Dependency Mapping**: Understand file relationships

---

## Available Tools

| Tool | Description |
|------|-------------|
| `discover` | Find files relevant to a query |
| `search` | Search by glob pattern |
| `agent_context` | Get all files for an agent |
| `create` | Create new file |
| `read` | Read file with metadata |
| `update` | Update file (creates backup) |
| `delete` | Delete file (requires confirm) |
| `move` | Move/rename file |
| `refresh` | Rebuild index |
| `stats` | Get index statistics |
| `validate_paths` | Check if paths exist |
| `map_dependencies` | Find file references |
| `related` | Find related files |

---

## Examples

### Find files for a task
```javascript
mcp__scout__discover("create product listing")
// Returns: anuncio_agent/PRIME.md (0.95), prompts/14_title_HOP.md (0.88)
```

### Get agent context
```javascript
mcp__scout__agent_context("codexa_agent")
// Returns: entry_points, files_by_category, dependencies
```

### Search by pattern
```javascript
mcp__scout__search("**/*_HOP.md")
// Returns: all HOP files in project
```

### Safe file update
```javascript
mcp__scout__update("path/to/file.md", "new content")
// Creates backup at path/to/file.md.bak
```

---

## Configuration

### Environment Variables
```bash
SCOUT_ROOT=/path/to/project  # Default: cwd
SCOUT_CACHE_MODE=session     # session | persistent
SCOUT_LOG_LEVEL=info         # debug | info | warn | error
```

### Config Files
```
config/
├── categories.json      # Category detection rules
├── ignore_patterns.json # Patterns to ignore
└── relevance_weights.json # Scoring weights
```

---

## Architecture

```
scout_agent/           # Documentation
├── PRIME.md
├── README.md
└── config/

mcp-servers/scout-mcp/ # MCP Server
├── index.js
├── package.json
└── node_modules/
```

---

## Performance

| Operation | Target |
|-----------|--------|
| Index Build | <5s (5000 files) |
| discover() | <100ms |
| search() | <50ms |
| CRUD ops | <200ms |

---

## Safety

- **Backups**: Update/delete create `.bak` files
- **Protected Paths**: Cannot modify `.git/`, `node_modules/`
- **Validation**: Paths outside project root are rejected
- **Confirm Required**: Delete requires `confirm: true`

---

## Version

- **Version**: 1.0.0
- **Created**: 2025-11-28
- **Type**: Infrastructure Agent (MCP Server)

---

## Related

- `/prime-scout` - Load Scout context
- `51_AGENT_REGISTRY.json` - Agent registry
- `.mcp.json` - MCP configuration
