# Scout Agent | SETUP

> Configuration and installation guide for Scout MCP Server

---

## Prerequisites

- Node.js >= 18.x
- npm or yarn
- Claude Code or compatible MCP client

---

## Installation

### 1. Install Dependencies

```bash
cd mcp-servers/scout-mcp
npm install
```

### 2. Configure Claude Settings

Add Scout to `.claude/settings.json`:

```json
{
  "mcpServers": {
    "scout": {
      "command": "node",
      "args": ["mcp-servers/scout-mcp/index.js"],
      "env": {
        "SCOUT_ROOT": ".",
        "SCOUT_LOG_LEVEL": "info"
      }
    }
  }
}
```

### 3. Verify Installation

Restart Claude Code and check for `mcp__scout__*` tools:

```javascript
// Should return index statistics
mcp__scout__stats()
```

---

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SCOUT_ROOT` | `.` (cwd) | Project root directory |
| `SCOUT_CACHE_MODE` | `session` | `session` or `persistent` |
| `SCOUT_LOG_LEVEL` | `info` | `debug`, `info`, `warn`, `error` |

### Config Files

Located in `scout_agent/config/`:

| File | Purpose |
|------|---------|
| `categories.json` | Category detection rules |
| `ignore_patterns.json` | Files to ignore |
| `relevance_weights.json` | Scoring weights |
| `protected_paths.json` | Cannot modify |

---

## File Structure

```
scout_agent/
├── PRIME.md             # Entry point
├── README.md            # Overview
├── INSTRUCTIONS.md      # This file
├── SETUP.md             # Configuration
└── config/
    ├── categories.json
    ├── ignore_patterns.json
    └── relevance_weights.json

mcp-servers/scout-mcp/
├── index.js             # MCP server entry
├── package.json
└── README.md
```

---

## Ignored Patterns

By default, Scout ignores:

```
node_modules/**
.venv/**
__pycache__/**
.git/**
*.pyc, *.pyo
*.log, *.tmp
.DS_Store, Thumbs.db
```

To customize, edit `scout_agent/config/ignore_patterns.json`.

---

## Performance Tuning

### Index Rebuild

```javascript
// Force rebuild (takes 2-5 seconds)
mcp__scout__refresh()
```

### Expected Performance

| Operation | Target | Typical |
|-----------|--------|---------|
| Index Build | <5s | 2-3s |
| discover() | <100ms | 50ms |
| search() | <50ms | 20ms |
| CRUD ops | <200ms | 100ms |

---

## Troubleshooting

### Scout tools not appearing

1. Check `.claude/settings.json` configuration
2. Restart Claude Code
3. Verify Node.js version (`node --version`)

### Slow performance

1. Run `mcp__scout__refresh()` to rebuild index
2. Check `ignore_patterns.json` for missing patterns
3. Reduce project size or add more ignore patterns

### Index errors

1. Delete cache and restart
2. Check file permissions
3. Verify SCOUT_ROOT path

---

## Updating

```bash
cd mcp-servers/scout-mcp
git pull
npm install
# Restart Claude Code
```

---

**Version**: 1.0.0
**Last Updated**: 2025-11-29
