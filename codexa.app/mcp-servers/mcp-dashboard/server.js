/**
 * MCP Dashboard - Web Server
 *
 * Provides REST API and WebSocket for MCP management
 * http://localhost:3456
 */

import express from 'express';
import { WebSocketServer } from 'ws';
import { createServer } from 'http';
import { fileURLToPath } from 'url';
import { dirname, join, resolve } from 'path';
import { readFileSync, existsSync, readdirSync } from 'fs';
import open from 'open';
import chokidar from 'chokidar';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const PROJECT_ROOT = resolve(__dirname, '../../..');

const app = express();
const server = createServer(app);
const wss = new WebSocketServer({ server });

const PORT = process.env.PORT || 3456;

// Serve static files
app.use(express.static(join(__dirname, 'public')));
app.use(express.json());

// Serve product images from USER_DOCS
app.use('/produtos', express.static(join(PROJECT_ROOT, 'USER_DOCS', 'produtos')));

// ============================================================================
// MCP Server Definitions
// ============================================================================

const MCP_SERVERS = {
  scout: {
    name: 'scout',
    description: 'File discovery & navigation',
    command: 'node',
    args: ['codexa.app/mcp-servers/scout-mcp/index.js'],
    tools: [
      { name: 'discover', description: 'Find files by natural language query', params: ['query', 'max_results?', 'agent?'] },
      { name: 'smart_context', description: 'Get prioritized context for an agent', params: ['agent', 'max_files?'] },
      { name: 'search', description: 'Search files by glob pattern', params: ['pattern', 'type?'] },
      { name: 'agent_context', description: 'Get all files for a specific agent', params: ['agent'] },
      { name: 'create', description: 'Create a new file with indexing', params: ['path', 'content'] },
      { name: 'read', description: 'Read file content with metadata', params: ['path'] },
      { name: 'update', description: 'Update file content', params: ['path', 'content'] },
      { name: 'delete', description: 'Delete a file', params: ['path', 'confirm'] },
      { name: 'move', description: 'Move or rename a file', params: ['from', 'to'] },
      { name: 'refresh', description: 'Rebuild the file index', params: [] },
      { name: 'stats', description: 'Get index statistics', params: [] },
      { name: 'validate_paths', description: 'Check if paths exist', params: ['paths'] },
      { name: 'map_dependencies', description: 'Find file references', params: ['file'] },
      { name: 'related', description: 'Find related files', params: ['file'] }
    ]
  },
  'codexa-commands': {
    name: 'codexa-commands',
    description: 'Slash commands management',
    command: 'node',
    args: ['codexa.app/mcp-servers/codexa-commands/index.js'],
    tools: [
      { name: 'list_commands', description: 'List all available slash commands', params: ['filter?', 'category?'] },
      { name: 'get_command', description: 'Get command content and metadata', params: ['command', 'agent?'] },
      { name: 'agent_commands', description: 'Get commands for a specific agent', params: ['agent'] },
      { name: 'execute_prompt', description: 'Expand command with arguments', params: ['command', 'arguments?'] },
      { name: 'refresh', description: 'Rebuild the command index', params: [] }
    ]
  },
  browser: {
    name: 'browser',
    description: 'Web automation & screenshots',
    command: 'npx',
    args: ['@anthropic-ai/mcp-server-puppeteer'],
    tools: [
      { name: 'screenshot', description: 'Capture webpage screenshot', params: ['url', 'fullPage?'] },
      { name: 'navigate', description: 'Navigate to URL', params: ['url'] },
      { name: 'click', description: 'Click element', params: ['selector'] },
      { name: 'type', description: 'Type text into input', params: ['selector', 'text'] },
      { name: 'evaluate', description: 'Run JavaScript on page', params: ['script'] },
      { name: 'extract', description: 'Extract data from webpage', params: ['url', 'selector'] }
    ]
  },
  voice: {
    name: 'voice',
    description: 'Speech recognition & TTS',
    command: 'python',
    args: ['codexa.app/voice/server.py'],
    tools: [
      { name: 'listen_start', description: 'Start recording (non-blocking)', params: ['max_duration?', 'language?'] },
      { name: 'listen_poll', description: 'Check recording status', params: ['session_id'] },
      { name: 'listen_stop', description: 'Cancel recording session', params: ['session_id'] },
      { name: 'listen', description: '[Legacy] Blocking voice capture', params: ['duration?'] },
      { name: 'speak', description: 'Text-to-speech output', params: ['text'] },
      { name: 'start_voice_loop', description: 'Start continuous voice mode', params: ['greeting?'] }
    ]
  }
};

// ============================================================================
// Log Storage (in-memory)
// ============================================================================

const logs = [];
const MAX_LOGS = 200;

function addLog(server, level, message) {
  const log = {
    id: Date.now(),
    timestamp: new Date().toISOString(),
    server,
    level,
    message
  };
  logs.push(log);
  if (logs.length > MAX_LOGS) logs.shift();

  // Broadcast to WebSocket clients
  broadcast({ type: 'log', data: log });

  return log;
}

function broadcast(message) {
  const data = JSON.stringify(message);
  wss.clients.forEach(client => {
    if (client.readyState === 1) {
      client.send(data);
    }
  });
}

// ============================================================================
// API Routes
// ============================================================================

// Health check for all servers
app.get('/api/health', (req, res) => {
  const results = {};

  for (const [name, server] of Object.entries(MCP_SERVERS)) {
    const serverPath = join(PROJECT_ROOT, server.args[0]);
    let status = 'offline';

    try {
      if (server.command === 'npx') {
        status = 'standby'; // NPX packages are lazy-loaded
      } else if (existsSync(serverPath)) {
        status = 'online';
      }
    } catch {
      status = 'error';
    }

    results[name] = {
      ...server,
      status,
      toolCount: server.tools.length
    };
  }

  addLog('system', 'INFO', 'Health check executed');
  res.json(results);
});

// Get server details
app.get('/api/servers/:name', (req, res) => {
  const server = MCP_SERVERS[req.params.name];
  if (!server) {
    return res.status(404).json({ error: 'Server not found' });
  }
  res.json(server);
});

// Get all tools
app.get('/api/tools', (req, res) => {
  const allTools = [];
  for (const [serverName, server] of Object.entries(MCP_SERVERS)) {
    for (const tool of server.tools) {
      allTools.push({
        ...tool,
        server: serverName,
        fullName: `mcp__${serverName.replace('-', '_')}__${tool.name}`
      });
    }
  }
  res.json(allTools);
});

// Get logs
app.get('/api/logs', (req, res) => {
  const { level, server, limit = 50 } = req.query;
  let filtered = [...logs];

  if (level && level !== 'ALL') {
    filtered = filtered.filter(l => l.level === level);
  }
  if (server && server !== 'ALL') {
    filtered = filtered.filter(l => l.server === server);
  }

  res.json(filtered.slice(-parseInt(limit)));
});

// Get commands from .claude/commands
app.get('/api/commands', (req, res) => {
  const commandsDir = join(PROJECT_ROOT, '.claude', 'commands');
  const commands = [];

  try {
    if (existsSync(commandsDir)) {
      const files = readdirSync(commandsDir, { recursive: true });

      for (const file of files) {
        if (file.endsWith('.md')) {
          const filePath = join(commandsDir, file);
          try {
            const content = readFileSync(filePath, 'utf8');
            const lines = content.split('\n');

            let title = file.replace('.md', '').replace(/-/g, ' ');
            let description = '';

            for (const line of lines.slice(0, 20)) {
              if (line.startsWith('# ')) {
                title = line.substring(2).trim();
              }
              if (line.length > 10 && !line.startsWith('#') && !line.startsWith('-') && !description) {
                description = line.substring(0, 100);
              }
            }

            commands.push({
              name: '/' + file.replace('.md', '').replace(/\\/g, '/'),
              title,
              description: description || 'No description',
              path: filePath
            });
          } catch {
            // Skip unreadable files
          }
        }
      }
    }
  } catch (err) {
    addLog('system', 'ERROR', `Failed to load commands: ${err.message}`);
  }

  res.json(commands);
});

// Get command content
app.get('/api/commands/:name', (req, res) => {
  const commandPath = join(PROJECT_ROOT, '.claude', 'commands', `${req.params.name}.md`);

  try {
    if (existsSync(commandPath)) {
      const content = readFileSync(commandPath, 'utf8');
      res.json({ name: req.params.name, content });
    } else {
      res.status(404).json({ error: 'Command not found' });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Get MCP config
app.get('/api/config', (req, res) => {
  try {
    const configPath = join(PROJECT_ROOT, '.mcp.json');
    const config = JSON.parse(readFileSync(configPath, 'utf8'));
    res.json(config);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// ============================================================================
// Pipeline API & File Watcher
// ============================================================================

const PIPELINE_STATE_PATH = join(PROJECT_ROOT, 'outputs', 'pipeline_state.json');

// Get current pipeline state
app.get('/api/pipeline', (req, res) => {
  try {
    if (existsSync(PIPELINE_STATE_PATH)) {
      const state = JSON.parse(readFileSync(PIPELINE_STATE_PATH, 'utf8'));
      res.json(state);
    } else {
      res.json({ status: 'idle', phases: [], live_thoughts: [] });
    }
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

// Watch pipeline state file for changes (usePolling for Windows compatibility)
const pipelineWatcher = chokidar.watch(PIPELINE_STATE_PATH, {
  persistent: true,
  ignoreInitial: true,
  usePolling: true,
  interval: 500,
  awaitWriteFinish: {
    stabilityThreshold: 100,
    pollInterval: 50
  }
});

pipelineWatcher.on('change', (path) => {
  try {
    const state = JSON.parse(readFileSync(path, 'utf8'));
    broadcast({ type: 'pipeline_update', data: state });

    const activePhase = state.phases?.find(p => p.status === 'running');
    const phaseName = activePhase?.name || (state.status === 'completed' ? 'completed' : 'idle');
    addLog('pipeline', 'INFO', `Pipeline updated: ${phaseName}`);
  } catch (err) {
    addLog('pipeline', 'ERROR', `Failed to parse pipeline state: ${err.message}`);
  }
});

pipelineWatcher.on('add', (path) => {
  addLog('pipeline', 'SUCCESS', 'Pipeline started - state file created');
  try {
    const state = JSON.parse(readFileSync(path, 'utf8'));
    broadcast({ type: 'pipeline_update', data: state });
  } catch (err) {
    // Ignore parse errors on initial add
  }
});

pipelineWatcher.on('unlink', () => {
  addLog('pipeline', 'INFO', 'Pipeline state file removed');
  broadcast({ type: 'pipeline_update', data: { status: 'idle', phases: [], live_thoughts: [] } });
});

// ============================================================================
// WebSocket Handling
// ============================================================================

wss.on('connection', (ws) => {
  console.log('Client connected');
  addLog('system', 'INFO', 'Dashboard client connected');

  // Send initial data
  ws.send(JSON.stringify({ type: 'connected', data: { logsCount: logs.length } }));

  ws.on('close', () => {
    console.log('Client disconnected');
  });
});

// Simulate periodic logs for demo
setInterval(() => {
  const servers = Object.keys(MCP_SERVERS);
  const levels = ['INFO', 'DEBUG', 'WARN'];
  const messages = [
    'Index refreshed',
    'Tool called successfully',
    'Processing request...',
    'Cache hit',
    'Waiting for input'
  ];

  if (Math.random() > 0.7) {
    addLog(
      servers[Math.floor(Math.random() * servers.length)],
      levels[Math.floor(Math.random() * levels.length)],
      messages[Math.floor(Math.random() * messages.length)]
    );
  }
}, 5000);

// ============================================================================
// Start Server
// ============================================================================

server.listen(PORT, async () => {
  console.log(`
╔═══════════════════════════════════════════════════════════╗
║                    MCP Dashboard v1.0                     ║
╠═══════════════════════════════════════════════════════════╣
║  URL: http://localhost:${PORT}                              ║
║  Press Ctrl+C to stop                                     ║
╚═══════════════════════════════════════════════════════════╝
  `);

  addLog('system', 'SUCCESS', `Dashboard started on port ${PORT}`);

  // Auto-open browser
  try {
    await open(`http://localhost:${PORT}`);
  } catch {
    console.log('Could not auto-open browser. Please navigate manually.');
  }
});
