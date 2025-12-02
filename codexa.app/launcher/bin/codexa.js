#!/usr/bin/env node
/**
 * CODEXA CLI
 *
 * Main entry point for the CODEXA launcher.
 *
 * Commands:
 *   codexa setup      - Install and configure everything
 *   codexa dashboard  - Open visual dashboard
 *   codexa status     - Check MCP server status
 *   codexa list       - List all commands
 *   codexa start      - Start all MCP servers
 *
 * Usage:
 *   npx codexa dashboard
 *   npm run dashboard (from launcher folder)
 */

import { spawn, execSync } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const LAUNCHER_ROOT = path.resolve(__dirname, '..');
const PROJECT_ROOT = path.resolve(LAUNCHER_ROOT, '..', '..');

// Colors
const c = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  red: '\x1b[31m',
  magenta: '\x1b[35m',
  white: '\x1b[37m'
};

// ============================================================================
// HELPERS
// ============================================================================

function printHeader() {
  console.log(`
${c.magenta}╔═══════════════════════════════════════════════════════════╗
║                                                             ║
║   ${c.cyan}${c.bright}CODEXA${c.reset}${c.magenta} - Meta-Construction Framework                  ║
║                                                             ║
╚═══════════════════════════════════════════════════════════╝${c.reset}
`);
}

function printUsage() {
  console.log(`${c.bright}Usage:${c.reset}

  ${c.cyan}codexa${c.reset} ${c.yellow}<command>${c.reset}

${c.bright}Commands:${c.reset}

  ${c.green}setup${c.reset}       Install and configure all MCP servers
  ${c.green}dashboard${c.reset}   Open visual dashboard (http://localhost:3333)
  ${c.green}status${c.reset}      Check MCP server status
  ${c.green}list${c.reset}        List all available commands
  ${c.green}start${c.reset}       Start dashboard server

${c.bright}Examples:${c.reset}

  ${c.dim}# First time setup${c.reset}
  ${c.cyan}codexa setup${c.reset}

  ${c.dim}# Open visual command browser${c.reset}
  ${c.cyan}codexa dashboard${c.reset}

  ${c.dim}# See what's available${c.reset}
  ${c.cyan}codexa list${c.reset}

${c.bright}Quick Start:${c.reset}

  ${c.dim}From the launcher folder:${c.reset}
  ${c.cyan}cd codexa.app/launcher${c.reset}
  ${c.cyan}npm run setup${c.reset}
  ${c.cyan}npm run dashboard${c.reset}
`);
}

// ============================================================================
// COMMANDS
// ============================================================================

async function cmdSetup() {
  const setupScript = path.join(LAUNCHER_ROOT, 'scripts', 'setup.js');

  console.log(`${c.cyan}Running setup...${c.reset}\n`);

  try {
    // Dynamic import and run
    await import(`file://${setupScript.replace(/\\/g, '/')}`);
  } catch (error) {
    console.error(`${c.red}Setup failed:${c.reset}`, error.message);
    process.exit(1);
  }
}

async function cmdDashboard() {
  printHeader();

  console.log(`${c.cyan}Starting dashboard server...${c.reset}\n`);

  const serverPath = path.join(LAUNCHER_ROOT, 'server.js');

  // Check if dependencies are installed
  const nodeModulesPath = path.join(LAUNCHER_ROOT, 'node_modules');
  if (!fs.existsSync(nodeModulesPath)) {
    console.log(`${c.yellow}Installing dependencies first...${c.reset}`);
    try {
      execSync('npm install', { cwd: LAUNCHER_ROOT, stdio: 'inherit' });
    } catch (error) {
      console.error(`${c.red}Failed to install dependencies${c.reset}`);
      process.exit(1);
    }
  }

  // Start server
  const server = spawn('node', [serverPath], {
    cwd: LAUNCHER_ROOT,
    stdio: 'inherit'
  });

  server.on('error', (error) => {
    console.error(`${c.red}Failed to start server:${c.reset}`, error.message);
    process.exit(1);
  });
}

async function cmdStatus() {
  printHeader();

  console.log(`${c.bright}MCP Server Status${c.reset}\n`);

  const servers = [
    { name: 'codexa-commands', path: 'codexa.app/mcp-servers/codexa-commands' },
    { name: 'scout', path: 'codexa.app/mcp-servers/scout-mcp' },
    { name: 'browser', path: 'codexa.app/mcp-servers/browser-mcp' },
    { name: 'voice', path: 'codexa.app/voice' }
  ];

  for (const server of servers) {
    const serverPath = path.join(PROJECT_ROOT, server.path);
    const indexPath = path.join(serverPath, 'index.js');
    const nodeModulesPath = path.join(serverPath, 'node_modules');

    let status = [];

    if (fs.existsSync(indexPath)) {
      status.push(`${c.green}✓${c.reset} index.js`);
    } else if (fs.existsSync(path.join(serverPath, 'server.py'))) {
      status.push(`${c.green}✓${c.reset} server.py`);
    } else {
      status.push(`${c.red}✗${c.reset} no entry`);
    }

    if (fs.existsSync(nodeModulesPath)) {
      status.push(`${c.green}✓${c.reset} deps`);
    } else {
      status.push(`${c.yellow}○${c.reset} no deps`);
    }

    console.log(`  ${c.cyan}${server.name.padEnd(18)}${c.reset} ${status.join('  ')}`);
  }

  console.log(`
${c.bright}Settings Files${c.reset}
`);

  const settingsFiles = [
    '.claude/settings.json',
    'codexa.app/.claude/settings.json'
  ];

  for (const file of settingsFiles) {
    const fullPath = path.join(PROJECT_ROOT, file);
    if (fs.existsSync(fullPath)) {
      console.log(`  ${c.green}✓${c.reset} ${file}`);
    } else {
      console.log(`  ${c.red}✗${c.reset} ${file}`);
    }
  }

  console.log(`
${c.dim}Run 'codexa setup' to configure everything${c.reset}
`);
}

async function cmdList() {
  printHeader();

  console.log(`${c.bright}Loading commands...${c.reset}\n`);

  try {
    const scannerPath = path.join(PROJECT_ROOT, 'codexa.app/mcp-servers/codexa-commands/lib/scanner.js');
    const parserPath = path.join(PROJECT_ROOT, 'codexa.app/mcp-servers/codexa-commands/lib/parser.js');

    const { scanCommands, getUniqueAgents } = await import(`file://${scannerPath.replace(/\\/g, '/')}`);
    const { parseCommands } = await import(`file://${parserPath.replace(/\\/g, '/')}`);

    const commands = await scanCommands(PROJECT_ROOT);
    const parsed = await parseCommands(commands);

    // Group by agent
    const global = parsed.filter(c => !c.agent);
    const byAgent = {};

    for (const cmd of parsed) {
      if (cmd.agent) {
        if (!byAgent[cmd.agent]) byAgent[cmd.agent] = [];
        byAgent[cmd.agent].push(cmd);
      }
    }

    // Print global commands
    console.log(`${c.magenta}Global Commands${c.reset} (${global.length})\n`);
    for (const cmd of global) {
      console.log(`  ${c.cyan}/${cmd.name.padEnd(25)}${c.reset} ${c.dim}${(cmd.title || '').substring(0, 40)}${c.reset}`);
    }

    // Print agent commands
    for (const [agent, cmds] of Object.entries(byAgent)) {
      console.log(`\n${c.blue}${agent}${c.reset} (${cmds.length})\n`);
      for (const cmd of cmds) {
        console.log(`  ${c.cyan}/${cmd.name.padEnd(25)}${c.reset} ${c.dim}${(cmd.title || '').substring(0, 40)}${c.reset}`);
      }
    }

    console.log(`
${c.bright}Total: ${commands.length} commands${c.reset}

${c.dim}Run 'codexa dashboard' to browse visually${c.reset}
`);
  } catch (error) {
    console.error(`${c.red}Failed to load commands:${c.reset}`, error.message);
    console.log(`\n${c.dim}Run 'codexa setup' first to install dependencies${c.reset}`);
  }
}

// ============================================================================
// MAIN
// ============================================================================

const args = process.argv.slice(2);
const command = args[0];

switch (command) {
  case 'setup':
    cmdSetup();
    break;

  case 'dashboard':
  case 'dash':
  case 'd':
    cmdDashboard();
    break;

  case 'status':
  case 's':
    cmdStatus();
    break;

  case 'list':
  case 'ls':
  case 'l':
    cmdList();
    break;

  case 'start':
    cmdDashboard();
    break;

  case 'help':
  case '-h':
  case '--help':
    printHeader();
    printUsage();
    break;

  case undefined:
    printHeader();
    printUsage();
    break;

  default:
    console.log(`${c.red}Unknown command: ${command}${c.reset}\n`);
    printUsage();
    process.exit(1);
}
