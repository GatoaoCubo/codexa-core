#!/usr/bin/env node
/**
 * CODEXA Commands MCP Server
 *
 * Allows agents to discover and execute slash commands dynamically.
 * Scans both agent-level and global commands.
 *
 * Tools:
 * - list_commands: List all available commands
 * - get_command: Get full content of a command
 * - agent_commands: Get commands for a specific agent
 * - execute_prompt: Expand prompt with arguments
 * - refresh: Rebuild command index
 *
 * @version 1.0.0
 * @author CODEXA Meta-Constructor
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import path from 'path';
import { fileURLToPath } from 'url';

import { scanCommands, getUniqueAgents, filterByAgent, filterGlobal } from './lib/scanner.js';
import { parseCommand, parseCommands } from './lib/parser.js';
import { expandPrompt, parseArguments, createExecutionContext } from './lib/expander.js';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============================================================================
// CONFIGURATION
// ============================================================================

/**
 * Auto-detect project root by walking up from the MCP server location
 */
function findProjectRoot() {
  // MCP server is at: codexa-core/codexa.app/mcp-servers/codexa-commands/
  // Project root is: codexa-core/
  // So we go up 3 levels from __dirname
  return path.resolve(__dirname, '..', '..', '..');
}

const PROJECT_ROOT = process.env.CODEXA_ROOT || findProjectRoot();
const LOG_LEVEL = process.env.CODEXA_LOG_LEVEL || 'info';

function log(level, message, data = {}) {
  const levels = { debug: 0, info: 1, warn: 2, error: 3 };
  if (levels[level] >= levels[LOG_LEVEL]) {
    console.error(`[codexa-commands:${level}] ${message}`, Object.keys(data).length ? JSON.stringify(data) : '');
  }
}

// ============================================================================
// COMMAND INDEX
// ============================================================================

let commandIndex = [];
let parsedCommands = new Map();
let indexBuiltAt = null;

/**
 * Build the command index
 */
async function buildIndex() {
  const startTime = Date.now();

  log('info', 'Building command index...', { root: PROJECT_ROOT });

  try {
    // Scan for command files
    commandIndex = await scanCommands(PROJECT_ROOT);

    // Parse all commands
    const parsed = await parseCommands(commandIndex);
    parsedCommands.clear();

    for (const cmd of parsed) {
      const key = cmd.agent ? `${cmd.agent}/${cmd.name}` : cmd.name;
      parsedCommands.set(key, cmd);
    }

    indexBuiltAt = new Date();
    const duration = Date.now() - startTime;

    log('info', 'Command index built', {
      total: commandIndex.length,
      agents: getUniqueAgents(commandIndex).length,
      duration_ms: duration,
    });

    return {
      total_commands: commandIndex.length,
      by_type: {
        agent: commandIndex.filter(c => c.type === 'agent').length,
        global: commandIndex.filter(c => c.type === 'global').length,
      },
      agents: getUniqueAgents(commandIndex),
      duration_ms: duration,
      built_at: indexBuiltAt.toISOString(),
    };
  } catch (error) {
    log('error', 'Index build failed', { error: error.message });
    throw error;
  }
}

// ============================================================================
// TOOL IMPLEMENTATIONS
// ============================================================================

/**
 * List all available commands
 */
async function toolListCommands(filter = null, category = null) {
  if (commandIndex.length === 0) {
    await buildIndex();
  }

  let commands = Array.from(parsedCommands.values());

  // Apply filters
  if (filter === 'global') {
    commands = commands.filter(c => !c.agent);
  } else if (filter === 'agent') {
    commands = commands.filter(c => c.agent);
  }

  if (category) {
    commands = commands.filter(c => {
      const name = c.name.toLowerCase();
      return name.includes(category.toLowerCase());
    });
  }

  return {
    commands: commands.map(c => ({
      name: c.name,
      title: c.title,
      description: c.description,
      agent: c.agent || null,
      type: c.agent ? 'agent' : 'global',
      usage: c.usage,
      version: c.version,
    })),
    total: commands.length,
    filters_applied: { filter, category },
  };
}

/**
 * Get full content of a specific command
 */
async function toolGetCommand(commandName, agent = null) {
  if (commandIndex.length === 0) {
    await buildIndex();
  }

  // Try exact match with agent prefix
  let key = agent ? `${agent}/${commandName}` : commandName;
  let cmd = parsedCommands.get(key);

  // Try without agent prefix
  if (!cmd && !agent) {
    for (const [k, v] of parsedCommands) {
      if (k.endsWith(`/${commandName}`) || k === commandName) {
        cmd = v;
        break;
      }
    }
  }

  if (!cmd) {
    return {
      error: `Command not found: ${commandName}`,
      agent,
      available_agents: getUniqueAgents(commandIndex),
    };
  }

  return {
    name: cmd.name,
    title: cmd.title,
    description: cmd.description,
    agent: cmd.agent,
    content: cmd.content,
    usage: cmd.usage,
    arguments: cmd.arguments,
    parameters: cmd.parameters,
    examples: cmd.examples,
    version: cmd.version,
    path: cmd.path,
  };
}

/**
 * Get all commands for a specific agent
 */
async function toolAgentCommands(agentName) {
  if (commandIndex.length === 0) {
    await buildIndex();
  }

  const agentCmds = filterByAgent(commandIndex, agentName);
  const parsedAgentCmds = agentCmds.map(c => {
    const key = `${c.agent}/${path.basename(c.path, '.md')}`;
    return parsedCommands.get(key);
  }).filter(Boolean);

  // Find PRIME.md path for the agent
  const primePath = `codexa.app/agentes/${agentName}/PRIME.md`;

  return {
    agent: agentName,
    commands: parsedAgentCmds.map(c => ({
      name: c.name,
      title: c.title,
      description: c.description,
      usage: c.usage,
    })),
    total: parsedAgentCmds.length,
    prime_path: primePath,
    entry_point: `agentes/${agentName}/PRIME.md`,
  };
}

/**
 * Execute/expand a prompt with arguments
 */
async function toolExecutePrompt(commandName, agent = null, userArgs = '') {
  if (commandIndex.length === 0) {
    await buildIndex();
  }

  // Find the command
  let key = agent ? `${agent}/${commandName}` : commandName;
  let cmd = parsedCommands.get(key);

  if (!cmd && !agent) {
    for (const [k, v] of parsedCommands) {
      if (k.endsWith(`/${commandName}`) || k === commandName) {
        cmd = v;
        break;
      }
    }
  }

  if (!cmd) {
    return {
      error: `Command not found: ${commandName}`,
    };
  }

  // Parse and expand arguments
  const args = parseArguments(userArgs);
  const context = await createExecutionContext(cmd, args, PROJECT_ROOT);

  return context;
}

/**
 * Refresh the command index
 */
async function toolRefresh() {
  return await buildIndex();
}

// ============================================================================
// MCP SERVER SETUP
// ============================================================================

const server = new Server(
  {
    name: 'codexa-commands',
    version: '1.0.0',
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: 'list_commands',
        description: 'List all available CODEXA slash commands. Returns command names, descriptions, and which agent they belong to.',
        inputSchema: {
          type: 'object',
          properties: {
            filter: {
              type: 'string',
              enum: ['global', 'agent', null],
              description: 'Filter by command type: "global" (no agent), "agent" (agent-specific), or null (all)',
            },
            category: {
              type: 'string',
              description: 'Filter by category in command name (e.g., "prime", "codexa", "curso")',
            },
          },
        },
      },
      {
        name: 'get_command',
        description: 'Get the full content and metadata of a specific slash command. Returns markdown content, usage, arguments, and examples.',
        inputSchema: {
          type: 'object',
          properties: {
            command: {
              type: 'string',
              description: 'Command name (e.g., "prime", "curso-outline", "anuncio")',
            },
            agent: {
              type: 'string',
              description: 'Optional: specific agent name if command exists in multiple agents',
            },
          },
          required: ['command'],
        },
      },
      {
        name: 'agent_commands',
        description: 'Get all commands available for a specific agent. Returns list of commands with their entry point and PRIME.md path.',
        inputSchema: {
          type: 'object',
          properties: {
            agent: {
              type: 'string',
              description: 'Agent name (e.g., "curso_agent", "anuncio_agent", "codexa_agent")',
            },
          },
          required: ['agent'],
        },
      },
      {
        name: 'execute_prompt',
        description: 'Expand a command prompt with user arguments. Replaces $ARGUMENTS, $1, $2, and {placeholders} with provided values. Returns expanded prompt and context files.',
        inputSchema: {
          type: 'object',
          properties: {
            command: {
              type: 'string',
              description: 'Command name to execute',
            },
            agent: {
              type: 'string',
              description: 'Optional: specific agent name',
            },
            arguments: {
              type: 'string',
              description: 'User arguments string (e.g., "scope=1-2 duration=20" or "Product name, category")',
            },
          },
          required: ['command'],
        },
      },
      {
        name: 'refresh',
        description: 'Rebuild the command index. Use after adding new commands or modifying existing ones.',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    let result;

    switch (name) {
      case 'list_commands':
        result = await toolListCommands(args.filter, args.category);
        break;
      case 'get_command':
        result = await toolGetCommand(args.command, args.agent);
        break;
      case 'agent_commands':
        result = await toolAgentCommands(args.agent);
        break;
      case 'execute_prompt':
        result = await toolExecutePrompt(args.command, args.agent, args.arguments);
        break;
      case 'refresh':
        result = await toolRefresh();
        break;
      default:
        throw new Error(`Unknown tool: ${name}`);
    }

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  } catch (error) {
    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify({ error: error.message }),
        },
      ],
      isError: true,
    };
  }
});

// ============================================================================
// MAIN
// ============================================================================

async function main() {
  log('info', 'Starting CODEXA Commands MCP Server v1.0.0...', {
    root: PROJECT_ROOT,
    cwd: process.cwd(),
  });

  // Build initial index
  await buildIndex();

  const transport = new StdioServerTransport();
  await server.connect(transport);

  log('info', 'CODEXA Commands MCP Server running', {
    commands: commandIndex.length,
    agents: getUniqueAgents(commandIndex),
  });
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
