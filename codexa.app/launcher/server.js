#!/usr/bin/env node
/**
 * CODEXA Dashboard Server
 * Visual interface for browsing and using CODEXA commands
 *
 * Usage: node server.js
 * Opens: http://localhost:3333
 */

import express from 'express';
import path from 'path';
import { fileURLToPath } from 'url';
import open from 'open';
import fs from 'fs/promises';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Find project root
function findRoot() {
  return path.resolve(__dirname, '..', '..');
}

const ROOT = findRoot();
const PORT = process.env.PORT || 3333;

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// ============================================================================
// API ROUTES
// ============================================================================

/**
 * Get all commands
 */
app.get('/api/commands', async (req, res) => {
  try {
    // Import scanner dynamically
    const scannerPath = path.join(ROOT, 'codexa.app/mcp-servers/codexa-commands/lib/scanner.js');
    const parserPath = path.join(ROOT, 'codexa.app/mcp-servers/codexa-commands/lib/parser.js');

    const { scanCommands, getUniqueAgents } = await import(`file://${scannerPath.replace(/\\/g, '/')}`);
    const { parseCommands } = await import(`file://${parserPath.replace(/\\/g, '/')}`);

    const commands = await scanCommands(ROOT);
    const parsed = await parseCommands(commands);

    const result = {
      commands: parsed.map(c => ({
        name: c.name,
        title: c.title || c.name,
        description: c.description || '',
        agent: c.agent || null,
        type: c.agent ? 'agent' : 'global',
        usage: c.usage || `/${c.name}`,
        path: c.path
      })),
      stats: {
        total: commands.length,
        global: commands.filter(c => c.type === 'global').length,
        agent: commands.filter(c => c.type === 'agent').length,
        agents: getUniqueAgents(commands)
      }
    };

    res.json(result);
  } catch (error) {
    console.error('Error loading commands:', error);
    res.status(500).json({ error: error.message });
  }
});

/**
 * Get single command content
 */
app.get('/api/commands/:name', async (req, res) => {
  try {
    const { name } = req.params;
    const { agent } = req.query;

    const scannerPath = path.join(ROOT, 'codexa.app/mcp-servers/codexa-commands/lib/scanner.js');
    const parserPath = path.join(ROOT, 'codexa.app/mcp-servers/codexa-commands/lib/parser.js');

    const { scanCommands } = await import(`file://${scannerPath.replace(/\\/g, '/')}`);
    const { parseCommand } = await import(`file://${parserPath.replace(/\\/g, '/')}`);

    const commands = await scanCommands(ROOT);
    let cmd = commands.find(c => {
      const cmdName = path.basename(c.path, '.md');
      if (agent) {
        return cmdName === name && c.agent === agent;
      }
      return cmdName === name;
    });

    if (!cmd) {
      return res.status(404).json({ error: 'Command not found' });
    }

    const parsed = await parseCommand(cmd);
    res.json(parsed);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

/**
 * Get MCP server status
 */
app.get('/api/status', async (req, res) => {
  const servers = [
    { name: 'codexa-commands', path: 'codexa.app/mcp-servers/codexa-commands' },
    { name: 'scout', path: 'codexa.app/mcp-servers/scout-mcp' }
  ];

  const status = [];

  for (const server of servers) {
    const serverPath = path.join(ROOT, server.path);
    const indexPath = path.join(serverPath, 'index.js');
    const nodeModulesPath = path.join(serverPath, 'node_modules');

    let installed = false;
    let hasIndex = false;

    try {
      await fs.access(nodeModulesPath);
      installed = true;
    } catch {}

    try {
      await fs.access(indexPath);
      hasIndex = true;
    } catch {}

    status.push({
      name: server.name,
      installed,
      hasIndex,
      ready: installed && hasIndex,
      path: server.path
    });
  }

  res.json({ servers: status, root: ROOT });
});

// ============================================================================
// START SERVER
// ============================================================================

app.listen(PORT, async () => {
  console.log(`
\x1b[35m╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   \x1b[1m\x1b[36mCODEXA DASHBOARD\x1b[0m\x1b[35m                                          ║
║                                                                ║
║   Server running at: \x1b[1m\x1b[32mhttp://localhost:${PORT}\x1b[0m\x1b[35m                    ║
║                                                                ║
║   Press Ctrl+C to stop                                         ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝\x1b[0m
`);

  // Auto-open browser
  if (process.argv.includes('--open') || !process.argv.includes('--no-open')) {
    try {
      await open(`http://localhost:${PORT}`);
    } catch {}
  }
});
