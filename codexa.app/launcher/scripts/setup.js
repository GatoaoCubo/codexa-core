#!/usr/bin/env node
/**
 * CODEXA Setup Script
 * One-click installation and configuration for all MCP servers
 *
 * Usage: node setup.js
 *
 * What it does:
 * 1. Detects project root automatically
 * 2. Installs dependencies for all MCP servers
 * 3. Updates Claude Code settings.json
 * 4. Verifies everything works
 */

import fs from 'fs/promises';
import path from 'path';
import { execSync, spawn } from 'child_process';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============================================================================
// CONFIGURATION
// ============================================================================

const CONFIG = {
  // MCP servers to install
  mcpServers: [
    {
      name: 'codexa-commands',
      path: 'codexa.app/mcp-servers/codexa-commands',
      description: 'Slash command discovery and execution',
      env: { CODEXA_ROOT: '{ROOT}' }
    },
    {
      name: 'scout',
      path: 'codexa.app/mcp-servers/scout-mcp',
      description: 'File discovery and smart context',
      env: { SCOUT_ROOT: '{ROOT}' }
    }
  ],

  // Settings files to update
  settingsFiles: [
    '.claude/settings.json',
    'codexa.app/.claude/settings.json'
  ]
};

// ============================================================================
// UTILITIES
// ============================================================================

const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
  red: '\x1b[31m',
  magenta: '\x1b[35m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

function logStep(step, message) {
  console.log(`\n${colors.cyan}[${step}]${colors.reset} ${colors.bright}${message}${colors.reset}`);
}

function logSuccess(message) {
  console.log(`  ${colors.green}✓${colors.reset} ${message}`);
}

function logWarning(message) {
  console.log(`  ${colors.yellow}⚠${colors.reset} ${message}`);
}

function logError(message) {
  console.log(`  ${colors.red}✗${colors.reset} ${message}`);
}

function logInfo(message) {
  console.log(`  ${colors.blue}ℹ${colors.reset} ${message}`);
}

// ============================================================================
// DETECTION
// ============================================================================

/**
 * Find project root by looking for codexa.app folder
 */
function findProjectRoot() {
  let current = path.resolve(__dirname, '..', '..');

  // Walk up until we find the codexa-core root
  for (let i = 0; i < 5; i++) {
    const codexaPath = path.join(current, 'codexa.app');
    const claudePath = path.join(current, '.claude');

    try {
      if (fs.statSync(codexaPath) && fs.statSync(claudePath)) {
        return current;
      }
    } catch {}

    current = path.dirname(current);
  }

  // Fallback
  return path.resolve(__dirname, '..', '..', '..');
}

// ============================================================================
// INSTALLATION
// ============================================================================

/**
 * Install npm dependencies for an MCP server
 */
async function installMcpServer(root, server) {
  const serverPath = path.join(root, server.path);
  const packageJsonPath = path.join(serverPath, 'package.json');

  try {
    await fs.access(packageJsonPath);
  } catch {
    logWarning(`${server.name}: package.json not found, skipping`);
    return false;
  }

  const nodeModulesPath = path.join(serverPath, 'node_modules');

  try {
    await fs.access(nodeModulesPath);
    logSuccess(`${server.name}: Dependencies already installed`);
    return true;
  } catch {
    // Need to install
  }

  logInfo(`${server.name}: Installing dependencies...`);

  try {
    execSync('npm install', {
      cwd: serverPath,
      stdio: 'pipe'
    });
    logSuccess(`${server.name}: Dependencies installed`);
    return true;
  } catch (error) {
    logError(`${server.name}: Failed to install - ${error.message}`);
    return false;
  }
}

/**
 * Update Claude Code settings.json
 */
async function updateSettings(root, settingsPath) {
  const fullPath = path.join(root, settingsPath);

  try {
    await fs.access(fullPath);
  } catch {
    logWarning(`Settings not found: ${settingsPath}`);
    return false;
  }

  try {
    const content = await fs.readFile(fullPath, 'utf-8');
    const settings = JSON.parse(content);

    // Ensure mcpServers exists
    if (!settings.mcpServers) {
      settings.mcpServers = {};
    }

    // Update each MCP server
    for (const server of CONFIG.mcpServers) {
      const serverPath = path.join(root, server.path, 'index.js').replace(/\\/g, '/');

      settings.mcpServers[server.name] = {
        command: 'node',
        args: [serverPath],
        env: {}
      };

      // Replace {ROOT} placeholder in env
      for (const [key, value] of Object.entries(server.env)) {
        settings.mcpServers[server.name].env[key] = value.replace('{ROOT}', root.replace(/\\/g, '/'));
      }
    }

    // Write back
    await fs.writeFile(fullPath, JSON.stringify(settings, null, 2));
    logSuccess(`Updated: ${settingsPath}`);
    return true;
  } catch (error) {
    logError(`Failed to update ${settingsPath}: ${error.message}`);
    return false;
  }
}

/**
 * Verify MCP server can start
 */
async function verifyServer(root, server) {
  const serverPath = path.join(root, server.path, 'index.js');

  try {
    await fs.access(serverPath);
  } catch {
    logWarning(`${server.name}: index.js not found`);
    return false;
  }

  return new Promise((resolve) => {
    const proc = spawn('node', ['-e', `import('${serverPath.replace(/\\/g, '/')}').then(() => process.exit(0)).catch(() => process.exit(1))`], {
      timeout: 10000,
      stdio: 'pipe'
    });

    let output = '';
    proc.stderr.on('data', (data) => {
      output += data.toString();
    });

    proc.on('close', (code) => {
      if (output.includes('Command index built')) {
        logSuccess(`${server.name}: Verified working`);
        resolve(true);
      } else if (code === 0) {
        logSuccess(`${server.name}: Import successful`);
        resolve(true);
      } else {
        logWarning(`${server.name}: May have issues`);
        resolve(false);
      }
    });

    proc.on('error', () => {
      logError(`${server.name}: Failed to verify`);
      resolve(false);
    });

    // Timeout
    setTimeout(() => {
      proc.kill();
    }, 8000);
  });
}

// ============================================================================
// MAIN
// ============================================================================

async function main() {
  console.log(`
${colors.magenta}╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ${colors.bright}${colors.cyan}CODEXA LAUNCHER${colors.reset}${colors.magenta} - One-Click Setup                        ║
║                                                                ║
║   This will install and configure all MCP servers for         ║
║   Claude Code to use CODEXA commands automatically.           ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝${colors.reset}
`);

  // Step 1: Detect root
  logStep('1/4', 'Detecting project root...');
  const root = findProjectRoot();
  logSuccess(`Found: ${root}`);

  // Step 2: Install dependencies
  logStep('2/4', 'Installing MCP server dependencies...');
  for (const server of CONFIG.mcpServers) {
    await installMcpServer(root, server);
  }

  // Also install launcher dependencies
  const launcherPath = path.join(root, 'codexa.app/launcher');
  try {
    await fs.access(path.join(launcherPath, 'node_modules'));
    logSuccess('Launcher: Dependencies already installed');
  } catch {
    logInfo('Launcher: Installing dependencies...');
    try {
      execSync('npm install', { cwd: launcherPath, stdio: 'pipe' });
      logSuccess('Launcher: Dependencies installed');
    } catch (e) {
      logWarning('Launcher: Install manually with npm install');
    }
  }

  // Step 3: Update settings
  logStep('3/4', 'Updating Claude Code settings...');
  for (const settingsPath of CONFIG.settingsFiles) {
    await updateSettings(root, settingsPath);
  }

  // Step 4: Verify
  logStep('4/4', 'Verifying MCP servers...');
  for (const server of CONFIG.mcpServers) {
    await verifyServer(root, server);
  }

  // Done!
  console.log(`
${colors.green}╔══════════════════════════════════════════════════════════════╗
║                                                                ║
║   ${colors.bright}✓ SETUP COMPLETE!${colors.reset}${colors.green}                                          ║
║                                                                ║
║   Next steps:                                                  ║
║                                                                ║
║   1. ${colors.bright}Restart Claude Code${colors.reset}${colors.green} to load MCP servers               ║
║                                                                ║
║   2. Open dashboard:                                           ║
║      ${colors.cyan}cd codexa.app/launcher && npm run dashboard${colors.reset}${colors.green}             ║
║                                                                ║
║   3. Or use CLI:                                               ║
║      ${colors.cyan}npm run start${colors.reset}${colors.green}                                            ║
║                                                                ║
║   MCP tools will be available as:                              ║
║   • mcp__codexa-commands__list_commands                        ║
║   • mcp__codexa-commands__get_command                          ║
║   • mcp__scout__discover                                       ║
║                                                                ║
╚══════════════════════════════════════════════════════════════╝${colors.reset}
`);
}

main().catch(console.error);
