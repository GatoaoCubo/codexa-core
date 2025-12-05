# Scout Agent | INSTRUCTIONS

> Operational guide for using the Scout MCP Server

**Version**: 1.1.0 | **Last Updated**: 2025-11-29

---

## Quick Start

### 1. Ensure Scout MCP is Running

Scout runs as an MCP server. Verify it's configured in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "scout": {
      "command": "node",
      "args": ["mcp-servers/scout-mcp/index.js"]
    }
  }
}
```

### 2. Basic Discovery

```javascript
// Find files related to a task
mcp__scout__discover("create product listing")

// Get all files for an agent
mcp__scout__agent_context("anuncio_agent")

// Search by pattern
mcp__scout__search("**/*_HOP.md")
```

---

## Tool Reference

### Discovery Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `discover(query)` | Find files by natural language | `discover("market research")` |
| `search(pattern)` | Find files by glob pattern | `search("**/*.json")` |
| `agent_context(agent)` | Get all files for agent | `agent_context("codexa_agent")` |
| `smart_context(agent)` | Get LLM-optimized context | `smart_context("anuncio_agent")` |

### CRUD Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `create(path, content)` | Create new file | `create("test.md", "# Test")` |
| `read(path)` | Read file with metadata | `read("PRIME.md")` |
| `update(path, content)` | Update file (auto-backup) | `update("test.md", "# Updated")` |
| `delete(path, confirm)` | Delete file | `delete("test.md", true)` |
| `move(from, to)` | Move/rename file | `move("old.md", "new.md")` |

### Index Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `refresh()` | Rebuild index | `refresh()` |
| `stats()` | Get statistics | `stats()` |
| `validate_paths(paths)` | Check if paths exist | `validate_paths(["a.md", "b.md"])` |

### Relationship Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `map_dependencies(file)` | Find file dependencies | `map_dependencies("PRIME.md")` |
| `related(file)` | Find related files | `related("anuncio_agent/PRIME.md")` |

---

## Common Workflows

### Workflow 1: Find Files for Task

```javascript
// User asks: "Help me create a product listing"
const result = await mcp__scout__discover("create product listing");

// Returns:
// - anuncio_agent/PRIME.md (0.95)
// - anuncio_agent/prompts/14_title_HOP.md (0.88)
// - pesquisa_agent/PRIME.md (0.72)
```

### Workflow 2: Load Agent Context

```javascript
// User asks: "Show me all codexa_agent files"
const context = await mcp__scout__agent_context("codexa_agent");

// Returns:
// - entry_points: {prime, readme, ...}
// - files_by_category: {builders: 13, validators: 7, ...}
// - total_files: 89
```

### Workflow 3: Safe File Operations

```javascript
// Create new file
await mcp__scout__create("docs/new_doc.md", "# New Document");

// Update with automatic backup
await mcp__scout__update("docs/new_doc.md", "# Updated Content");

// Delete (requires confirmation)
await mcp__scout__delete("docs/new_doc.md", true);
```

---

## Relevance Scoring

Scout uses multi-factor scoring (0.0 - 1.0):

| Factor | Weight | Description |
|--------|--------|-------------|
| Text Match | 40% | Fuzzy match on path + tags |
| Category Priority | 20% | PRIME > README > HOP > config |
| Agent Match | 25% | Boost if matches requested agent |
| Recency | 15% | Recently modified files rank higher |

### Category Priorities
```
prime: 1.0
readme: 0.9
instructions: 0.85
hop: 0.8
adw: 0.8
config: 0.7
```

---

## Safety Rules

1. **Backup Before Delete**: Creates `.bak` file automatically
2. **Path Validation**: Rejects paths outside project
3. **Confirm Destructive**: Requires `confirm: true` for delete
4. **Protected Paths**: Cannot modify `.git/`, `node_modules/`

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Tools not available | Check MCP server is running |
| Slow responses | Run `refresh()` to rebuild index |
| Wrong results | Check query specificity |
| File not found | Use `validate_paths()` to check |

---

## Path Registry System

Scout manages the **PATH_REGISTRY_SYSTEM** for centralized path management.

### Using Path Placeholders

Instead of hardcoding paths, use placeholders:

```python
# Python
from codexa.app.core.path_resolver import resolve_path
path = resolve_path("{{AGENTES}}/scout_agent/PRIME.md")
```

```javascript
// Node.js
const { resolvePath } = require('./codexa.app/core/pathResolver.cjs');
const path = resolvePath('{{AGENTES}}/scout_agent/PRIME.md');
```

### Standard Placeholders

- `{{PROJECT_ROOT}}` - Git root (auto-detect)
- `{{CODEXA_APP}}` - codexa.app directory
- `{{AGENTES}}` - agentes directory
- `{{MCP_SERVERS}}` - mcp-servers directory
- `{{CLAUDE_DIR}}` - .claude directory

### Regenerating Paths

When setting up on a new machine:

```bash
python codexa.app/core/setup_paths.py
```

This regenerates all MCP configurations with correct absolute paths.

See: `specs/PATH_REGISTRY_SYSTEM_SPEC.md` for full documentation.

---

## Best Practices

1. **Use natural language** for `discover()` - it understands context
2. **Use `smart_context()`** for LLM-optimized file navigation
3. **Be specific** with agent names in `agent_context()`
4. **Always confirm deletes** - pass `confirm: true`
5. **Check results** before acting on discovered files
6. **Use `related()`** to find connected files
7. **Use path placeholders** instead of hardcoded paths

---

## Changelog

### v1.1.0 (2025-11-29)
- Added PATH REGISTRY SYSTEM documentation
- Added `smart_context` tool for LLM-optimized agent context
- Enhanced path management with placeholder system
- Added path resolver integration (Python & Node.js)

### v1.0.0 (2025-11-28)
- Initial release
- MVP tools: discover, search, agent_context
- CRUD operations with safety features
- Multi-factor relevance scoring

---

**Version**: 1.1.0
**Last Updated**: 2025-11-29
