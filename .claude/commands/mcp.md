# /mcp - MCP Dashboard

Launch the MCP Dashboard web interface for managing and monitoring MCP servers.

## Usage

```
/mcp
```

## Features

The dashboard provides 4 panels:

1. **Health** - Real-time status of all MCP servers (online/standby/offline)
2. **Tools** - Browse all 31 tools across 4 servers, with copy-to-clipboard
3. **Logs** - Live log viewer with filtering by level and server
4. **Commands** - Search and view all 46 slash commands

## Instructions for Claude

When user runs `/mcp`, start the dashboard server:

```bash
cd C:/Users/PC/Documents/GitHub/codexa-core/codexa.app/mcp-servers/mcp-dashboard && npm start
```

If dependencies not installed:
```bash
cd C:/Users/PC/Documents/GitHub/codexa-core/codexa.app/mcp-servers/mcp-dashboard && npm install && npm start
```

The dashboard will:
1. Start Express server on port 3456
2. Auto-open browser to http://localhost:3456
3. Connect WebSocket for live log updates

## Quick Health Check (no dashboard)

If user just wants a quick status without the dashboard, call:
- `mcp__scout__stats` - Check scout
- `mcp__codexa_commands__list_commands` - Check commands

Report as table:

| Server | Status | Tools |
|--------|--------|-------|
| scout | ONLINE | 14 |
| codexa-commands | ONLINE | 5 |
| browser | STANDBY | 6 |
| voice | STANDBY | 6 |

## Keyboard Shortcuts (in dashboard)

- Click tabs to switch panels
- Type in search box to filter commands
- Click tool usage to copy to clipboard
