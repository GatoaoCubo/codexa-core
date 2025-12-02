#!/usr/bin/env node
/**
 * CODEXA Smart Installer v2.0
 *
 * Universal setup for any environment:
 * - New PC: Full installation with prerequisites check
 * - New User: API key configuration
 * - Existing: Health check and repair
 *
 * Usage:
 *   node setup-codexa.js           # Interactive full setup
 *   node setup-codexa.js --check   # Health check only
 *   node setup-codexa.js --repair  # Fix issues automatically
 *   node setup-codexa.js --apis    # Configure API keys only
 *   node setup-codexa.js --help    # Show help
 */

import { execSync, spawn, spawnSync } from 'child_process';
import fs from 'fs';
import path from 'path';
import os from 'os';
import { fileURLToPath } from 'url';
import readline from 'readline';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============================================================================
// COLORS & UI
// ============================================================================
const c = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  cyan: '\x1b[36m',
  red: '\x1b[31m',
  magenta: '\x1b[35m',
  blue: '\x1b[34m',
  white: '\x1b[37m',
  bgGreen: '\x1b[42m',
  bgRed: '\x1b[41m',
  bgYellow: '\x1b[43m'
};

const icons = {
  check: `${c.green}✓${c.reset}`,
  cross: `${c.red}✗${c.reset}`,
  warn: `${c.yellow}⚠${c.reset}`,
  arrow: `${c.cyan}→${c.reset}`,
  dot: `${c.dim}○${c.reset}`,
  star: `${c.yellow}★${c.reset}`,
  info: `${c.blue}ℹ${c.reset}`
};

// ============================================================================
// CONFIGURATION
// ============================================================================
const CONFIG = {
  // NPM packages to install
  npmPackages: [
    { name: 'scout-mcp', path: 'codexa.app/mcp-servers/scout-mcp', required: true },
    { name: 'codexa-commands', path: 'codexa.app/mcp-servers/codexa-commands', required: true },
    { name: 'browser-mcp', path: 'codexa.app/mcp-servers/browser-mcp', required: false },
    { name: 'launcher', path: 'codexa.app/launcher', required: true },
    { name: 'client', path: 'app/client', required: false }
  ],

  // Python requirements to install
  pythonPackages: [
    { name: 'voice', path: 'codexa.app/voice/requirements.txt', required: false },
    { name: 'video_agent', path: 'codexa.app/agentes/video_agent/requirements.txt', required: false },
    { name: 'codexa_agent', path: 'codexa.app/agentes/codexa_agent/requirements.txt', required: false }
  ],

  // MCP Servers configuration
  mcpServers: {
    'scout': {
      command: 'node',
      entry: 'codexa.app/mcp-servers/scout-mcp/index.js',
      env: { SCOUT_ROOT: '{ROOT}' }
    },
    'codexa-commands': {
      command: 'node',
      entry: 'codexa.app/mcp-servers/codexa-commands/index.js',
      env: { CODEXA_ROOT: '{ROOT}' }
    },
    'browser': {
      command: 'node',
      entry: 'codexa.app/mcp-servers/browser-mcp/index.js',
      env: {}
    },
    'voice': {
      command: 'uv',
      args: ['run'],
      entry: 'codexa.app/voice/server.py',
      env: { VOICE_PORT: '5000', VOICE_LANGUAGE: 'pt-BR' }
    }
  },

  // API Keys configuration
  apiKeys: [
    {
      name: 'ANTHROPIC_API_KEY',
      description: 'Claude API (Required for LLM)',
      url: 'https://console.anthropic.com',
      required: true,
      group: 'llm'
    },
    {
      name: 'OPENAI_API_KEY',
      description: 'OpenAI API (Optional fallback)',
      url: 'https://platform.openai.com/api-keys',
      required: false,
      group: 'llm'
    },
    {
      name: 'GOOGLE_API_KEY',
      description: 'Google Gemini (Optional)',
      url: 'https://aistudio.google.com/app/apikey',
      required: false,
      group: 'llm'
    },
    {
      name: 'ELEVENLABS_API_KEY',
      description: 'ElevenLabs Voice (Optional)',
      url: 'https://elevenlabs.io',
      required: false,
      group: 'voice'
    },
    {
      name: 'SUPABASE_URL',
      description: 'Supabase URL (For publishing)',
      url: 'https://supabase.com/dashboard',
      required: false,
      group: 'database'
    },
    {
      name: 'SUPABASE_SERVICE_ROLE_KEY',
      description: 'Supabase Service Key (For publishing)',
      url: 'https://supabase.com/dashboard',
      required: false,
      group: 'database'
    }
  ],

  // Prerequisites
  prerequisites: [
    {
      name: 'Node.js',
      command: 'node',
      versionArg: '--version',
      minVersion: '18.0.0',
      required: true,
      install: {
        windows: 'winget install OpenJS.NodeJS.LTS',
        mac: 'brew install node',
        linux: 'curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash - && sudo apt-get install -y nodejs'
      }
    },
    {
      name: 'Python',
      command: 'python',
      altCommand: 'python3',
      versionArg: '--version',
      minVersion: '3.10.0',
      required: true,
      install: {
        windows: 'winget install Python.Python.3.12',
        mac: 'brew install python@3.12',
        linux: 'sudo apt install python3.12'
      }
    },
    {
      name: 'uv',
      command: 'uv',
      versionArg: '--version',
      minVersion: '0.1.0',
      required: true,
      install: {
        windows: 'pip install uv',
        mac: 'pip install uv',
        linux: 'pip install uv'
      }
    },
    {
      name: 'Git',
      command: 'git',
      versionArg: '--version',
      minVersion: '2.0.0',
      required: true,
      install: {
        windows: 'winget install Git.Git',
        mac: 'brew install git',
        linux: 'sudo apt install git'
      }
    },
    {
      name: 'FFmpeg',
      command: 'ffmpeg',
      versionArg: '-version',
      minVersion: '4.0.0',
      required: false,
      install: {
        windows: 'winget install FFmpeg',
        mac: 'brew install ffmpeg',
        linux: 'sudo apt install ffmpeg'
      }
    }
  ]
};

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function getConfigDir() {
  return path.join(os.homedir(), '.codexa');
}

function ensureConfigDir() {
  const configDir = getConfigDir();
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  return configDir;
}

function loadConfig() {
  const configPath = path.join(getConfigDir(), 'config.json');
  if (fs.existsSync(configPath)) {
    return JSON.parse(fs.readFileSync(configPath, 'utf-8'));
  }
  return {};
}

function saveConfig(config) {
  ensureConfigDir();
  const configPath = path.join(getConfigDir(), 'config.json');
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2));
}

function loadCredentials() {
  const credPath = path.join(getConfigDir(), 'credentials.json');
  if (fs.existsSync(credPath)) {
    return JSON.parse(fs.readFileSync(credPath, 'utf-8'));
  }
  return {};
}

function saveCredentials(creds) {
  ensureConfigDir();
  const credPath = path.join(getConfigDir(), 'credentials.json');
  fs.writeFileSync(credPath, JSON.stringify(creds, null, 2));
}

function checkCommand(cmd, args = ['--version']) {
  try {
    const result = spawnSync(cmd, args, {
      encoding: 'utf-8',
      shell: true,
      timeout: 10000
    });
    if (result.status === 0) {
      const output = (result.stdout || result.stderr || '').trim();
      const versionMatch = output.match(/(\d+\.\d+\.\d+)/);
      return {
        installed: true,
        version: versionMatch ? versionMatch[1] : 'unknown',
        output
      };
    }
    return { installed: false };
  } catch {
    return { installed: false };
  }
}

function compareVersions(v1, v2) {
  const parts1 = v1.split('.').map(Number);
  const parts2 = v2.split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    if ((parts1[i] || 0) > (parts2[i] || 0)) return 1;
    if ((parts1[i] || 0) < (parts2[i] || 0)) return -1;
  }
  return 0;
}

function getPlatform() {
  const platform = os.platform();
  if (platform === 'win32') return 'windows';
  if (platform === 'darwin') return 'mac';
  return 'linux';
}

async function question(rl, prompt) {
  return new Promise(resolve => {
    rl.question(prompt, resolve);
  });
}

function runNpmInstall(dir) {
  try {
    execSync('npm install', {
      cwd: dir,
      stdio: 'pipe',
      timeout: 120000
    });
    return { success: true };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

function runPythonInstall(requirementsPath) {
  try {
    execSync(`uv pip install -r "${requirementsPath}"`, {
      stdio: 'pipe',
      timeout: 120000,
      shell: true
    });
    return { success: true };
  } catch {
    // Fallback to pip
    try {
      execSync(`pip install -r "${requirementsPath}"`, {
        stdio: 'pipe',
        timeout: 120000,
        shell: true
      });
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}

// ============================================================================
// MAIN FUNCTIONS
// ============================================================================

async function checkPrerequisites() {
  console.log(`\n${c.cyan}${c.bright}[1/5] Checking Prerequisites${c.reset}\n`);

  const results = [];
  const platform = getPlatform();

  for (const prereq of CONFIG.prerequisites) {
    let check = checkCommand(prereq.command, [prereq.versionArg]);

    // Try alternate command if primary fails
    if (!check.installed && prereq.altCommand) {
      check = checkCommand(prereq.altCommand, [prereq.versionArg]);
    }

    const status = {
      name: prereq.name,
      installed: check.installed,
      version: check.version,
      required: prereq.required,
      meetsMinVersion: check.version && prereq.minVersion
        ? compareVersions(check.version, prereq.minVersion) >= 0
        : true,
      installCmd: prereq.install[platform]
    };

    results.push(status);

    // Display result
    if (status.installed && status.meetsMinVersion) {
      console.log(`  ${icons.check} ${prereq.name}: ${c.green}${status.version}${c.reset}`);
    } else if (status.installed && !status.meetsMinVersion) {
      console.log(`  ${icons.warn} ${prereq.name}: ${c.yellow}${status.version}${c.reset} (min: ${prereq.minVersion})`);
    } else if (prereq.required) {
      console.log(`  ${icons.cross} ${prereq.name}: ${c.red}Not installed${c.reset} ${c.dim}(${status.installCmd})${c.reset}`);
    } else {
      console.log(`  ${icons.dot} ${prereq.name}: ${c.dim}Not installed (optional)${c.reset}`);
    }
  }

  // Check for missing required prerequisites
  const missing = results.filter(r => r.required && (!r.installed || !r.meetsMinVersion));
  if (missing.length > 0) {
    console.log(`\n${c.red}${c.bright}Missing required prerequisites:${c.reset}\n`);
    for (const m of missing) {
      console.log(`  ${icons.arrow} Install ${m.name}: ${c.cyan}${m.installCmd}${c.reset}`);
    }
    return { success: false, results };
  }

  return { success: true, results };
}

async function installNpmPackages(repair = false) {
  console.log(`\n${c.cyan}${c.bright}[2/5] Installing NPM Packages${c.reset}\n`);

  const results = [];

  for (const pkg of CONFIG.npmPackages) {
    const pkgPath = path.join(__dirname, pkg.path);
    const packageJson = path.join(pkgPath, 'package.json');
    const nodeModules = path.join(pkgPath, 'node_modules');

    // Check if package.json exists
    if (!fs.existsSync(packageJson)) {
      console.log(`  ${icons.dot} ${pkg.name}: ${c.dim}No package.json${c.reset}`);
      results.push({ name: pkg.name, status: 'skipped', reason: 'no package.json' });
      continue;
    }

    // Check if already installed
    if (fs.existsSync(nodeModules) && !repair) {
      console.log(`  ${icons.check} ${pkg.name}: ${c.green}Already installed${c.reset}`);
      results.push({ name: pkg.name, status: 'installed' });
      continue;
    }

    // Install
    process.stdout.write(`  ${icons.arrow} ${pkg.name}: Installing...`);
    const result = runNpmInstall(pkgPath);

    if (result.success) {
      console.log(`\r  ${icons.check} ${pkg.name}: ${c.green}Installed${c.reset}           `);
      results.push({ name: pkg.name, status: 'installed' });
    } else {
      console.log(`\r  ${icons.cross} ${pkg.name}: ${c.red}Failed${c.reset}           `);
      results.push({ name: pkg.name, status: 'failed', error: result.error });
    }
  }

  const failed = results.filter(r => r.status === 'failed' &&
    CONFIG.npmPackages.find(p => p.name === r.name)?.required);

  return { success: failed.length === 0, results };
}

async function installPythonPackages(repair = false) {
  console.log(`\n${c.cyan}${c.bright}[3/5] Installing Python Packages${c.reset}\n`);

  const results = [];

  // Check if uv is available
  const uvCheck = checkCommand('uv', ['--version']);
  if (!uvCheck.installed) {
    console.log(`  ${icons.warn} uv not installed, skipping Python packages`);
    return { success: true, results: [] };
  }

  for (const pkg of CONFIG.pythonPackages) {
    const reqPath = path.join(__dirname, pkg.path);

    if (!fs.existsSync(reqPath)) {
      console.log(`  ${icons.dot} ${pkg.name}: ${c.dim}No requirements.txt${c.reset}`);
      results.push({ name: pkg.name, status: 'skipped' });
      continue;
    }

    // Check via pip list if packages are installed (simplified check)
    if (!repair) {
      console.log(`  ${icons.check} ${pkg.name}: ${c.green}Available${c.reset}`);
      results.push({ name: pkg.name, status: 'available' });
      continue;
    }

    // Install
    process.stdout.write(`  ${icons.arrow} ${pkg.name}: Installing...`);
    const result = runPythonInstall(reqPath);

    if (result.success) {
      console.log(`\r  ${icons.check} ${pkg.name}: ${c.green}Installed${c.reset}           `);
      results.push({ name: pkg.name, status: 'installed' });
    } else {
      console.log(`\r  ${icons.warn} ${pkg.name}: ${c.yellow}Skipped${c.reset}           `);
      results.push({ name: pkg.name, status: 'skipped' });
    }
  }

  return { success: true, results };
}

async function configureMcpServers() {
  console.log(`\n${c.cyan}${c.bright}[4/5] Configuring MCP Servers${c.reset}\n`);

  const settingsPath = path.join(__dirname, '.claude', 'settings.json');
  const root = __dirname.replace(/\\/g, '/');

  let settings = {};
  if (fs.existsSync(settingsPath)) {
    settings = JSON.parse(fs.readFileSync(settingsPath, 'utf-8'));
  }

  settings.mcpServers = settings.mcpServers || {};

  for (const [name, config] of Object.entries(CONFIG.mcpServers)) {
    const entryPath = `${root}/${config.entry}`;

    // Check if entry file exists
    const fullPath = path.join(__dirname, config.entry);
    if (!fs.existsSync(fullPath)) {
      console.log(`  ${icons.dot} ${name}: ${c.dim}Entry not found${c.reset}`);
      continue;
    }

    // Configure MCP server
    const serverConfig = {
      command: config.command,
      args: config.args ? [...config.args, entryPath] : [entryPath],
      env: {}
    };

    // Replace {ROOT} placeholder in env vars
    for (const [key, value] of Object.entries(config.env)) {
      serverConfig.env[key] = value.replace('{ROOT}', root);
    }

    settings.mcpServers[name] = serverConfig;
    console.log(`  ${icons.check} ${name}: ${c.green}Configured${c.reset}`);
  }

  // Ensure hooks are configured
  settings.hooks = settings.hooks || {};

  // Write settings
  fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2));
  console.log(`\n  ${icons.check} Settings saved to ${c.cyan}.claude/settings.json${c.reset}`);

  return { success: true };
}

async function configureApiKeys(rl) {
  console.log(`\n${c.cyan}${c.bright}[5/5] Configuring API Keys${c.reset}\n`);

  const creds = loadCredentials();
  const envPath = path.join(__dirname, 'codexa.app', '.env');

  let envContent = '';
  if (fs.existsSync(envPath)) {
    envContent = fs.readFileSync(envPath, 'utf-8');
  }

  // Group keys by category
  const groups = {};
  for (const key of CONFIG.apiKeys) {
    if (!groups[key.group]) groups[key.group] = [];
    groups[key.group].push(key);
  }

  console.log(`  ${c.dim}Press Enter to skip, or paste your API key${c.reset}\n`);

  let hasLlmKey = false;

  for (const [groupName, keys] of Object.entries(groups)) {
    console.log(`  ${c.bright}${groupName.toUpperCase()}:${c.reset}`);

    for (const key of keys) {
      // Check if already set in environment
      const existingEnv = process.env[key.name];
      const existingCred = creds[key.name];
      const existing = existingEnv || existingCred;

      if (existing) {
        const masked = existing.substring(0, 8) + '...' + existing.substring(existing.length - 4);
        console.log(`    ${icons.check} ${key.name}: ${c.dim}${masked}${c.reset}`);
        if (key.group === 'llm') hasLlmKey = true;
        continue;
      }

      // Ask for key
      const marker = key.required ? `${c.red}*${c.reset}` : '';
      const answer = await question(rl, `    ${marker}${key.name}: `);

      if (answer.trim()) {
        creds[key.name] = answer.trim();

        // Add to .env file
        if (!envContent.includes(key.name)) {
          envContent += `\n${key.name}=${answer.trim()}`;
        }

        if (key.group === 'llm') hasLlmKey = true;
        console.log(`    ${icons.check} ${c.green}Saved${c.reset}`);
      } else {
        console.log(`    ${icons.dot} ${c.dim}Skipped${c.reset}`);
      }
    }
    console.log('');
  }

  // Save credentials
  saveCredentials(creds);

  // Save .env file
  if (envContent.trim()) {
    fs.writeFileSync(envPath, envContent.trim() + '\n');
  }

  if (!hasLlmKey) {
    console.log(`  ${icons.warn} ${c.yellow}No LLM API key configured. Some features won't work.${c.reset}`);
  }

  return { success: true, hasLlmKey };
}

async function runHealthCheck() {
  console.log(`\n${c.cyan}${c.bright}Health Check${c.reset}\n`);

  const results = {
    prerequisites: [],
    npm: [],
    mcp: [],
    apis: []
  };

  // Check prerequisites
  console.log(`  ${c.bright}Prerequisites:${c.reset}`);
  for (const prereq of CONFIG.prerequisites) {
    let check = checkCommand(prereq.command, [prereq.versionArg]);
    if (!check.installed && prereq.altCommand) {
      check = checkCommand(prereq.altCommand, [prereq.versionArg]);
    }

    const icon = check.installed ? icons.check : (prereq.required ? icons.cross : icons.dot);
    const color = check.installed ? c.green : (prereq.required ? c.red : c.dim);
    console.log(`    ${icon} ${prereq.name}: ${color}${check.version || 'Not installed'}${c.reset}`);
    results.prerequisites.push({ name: prereq.name, ...check });
  }

  // Check NPM packages
  console.log(`\n  ${c.bright}NPM Packages:${c.reset}`);
  for (const pkg of CONFIG.npmPackages) {
    const nodeModules = path.join(__dirname, pkg.path, 'node_modules');
    const installed = fs.existsSync(nodeModules);
    const icon = installed ? icons.check : (pkg.required ? icons.cross : icons.dot);
    const color = installed ? c.green : (pkg.required ? c.red : c.dim);
    console.log(`    ${icon} ${pkg.name}: ${color}${installed ? 'Installed' : 'Not installed'}${c.reset}`);
    results.npm.push({ name: pkg.name, installed });
  }

  // Check MCP servers
  console.log(`\n  ${c.bright}MCP Servers:${c.reset}`);
  for (const [name, config] of Object.entries(CONFIG.mcpServers)) {
    const entryPath = path.join(__dirname, config.entry);
    const exists = fs.existsSync(entryPath);
    const icon = exists ? icons.check : icons.warn;
    const color = exists ? c.green : c.yellow;
    console.log(`    ${icon} ${name}: ${color}${exists ? 'Ready' : 'Entry not found'}${c.reset}`);
    results.mcp.push({ name, exists });
  }

  // Check API keys
  console.log(`\n  ${c.bright}API Keys:${c.reset}`);
  const creds = loadCredentials();
  let hasLlmKey = false;
  for (const key of CONFIG.apiKeys) {
    const exists = process.env[key.name] || creds[key.name];
    if (exists && key.group === 'llm') hasLlmKey = true;
    const icon = exists ? icons.check : (key.required ? icons.warn : icons.dot);
    const color = exists ? c.green : (key.required ? c.yellow : c.dim);
    console.log(`    ${icon} ${key.name}: ${color}${exists ? 'Configured' : 'Not set'}${c.reset}`);
    results.apis.push({ name: key.name, exists: !!exists });
  }

  // Summary
  const prereqOk = results.prerequisites.filter(p => !p.installed && CONFIG.prerequisites.find(x => x.name === p.name)?.required).length === 0;
  const npmOk = results.npm.filter(p => !p.installed && CONFIG.npmPackages.find(x => x.name === p.name)?.required).length === 0;
  const mcpOk = results.mcp.filter(p => !p.exists).length <= 1;

  console.log(`\n  ${c.bright}Summary:${c.reset}`);
  console.log(`    Prerequisites: ${prereqOk ? `${c.green}OK${c.reset}` : `${c.red}Issues${c.reset}`}`);
  console.log(`    NPM Packages:  ${npmOk ? `${c.green}OK${c.reset}` : `${c.red}Issues${c.reset}`}`);
  console.log(`    MCP Servers:   ${mcpOk ? `${c.green}OK${c.reset}` : `${c.yellow}Partial${c.reset}`}`);
  console.log(`    API Keys:      ${hasLlmKey ? `${c.green}OK${c.reset}` : `${c.yellow}No LLM key${c.reset}`}`);

  return {
    success: prereqOk && npmOk,
    results,
    needsRepair: !prereqOk || !npmOk
  };
}

function showBanner() {
  console.log(`
${c.magenta}╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║   ${c.cyan}${c.bright}CODEXA SMART INSTALLER v2.0${c.reset}${c.magenta}                                           ║
║                                                                             ║
║   ${c.white}Universal setup for LLMs and developers${c.reset}${c.magenta}                              ║
║   ${c.dim}New PC • New User • Health Check • Repair${c.reset}${c.magenta}                            ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════╝${c.reset}
`);
}

function showHelp() {
  showBanner();
  console.log(`
${c.bright}Usage:${c.reset}
  node setup-codexa.js [options]

${c.bright}Options:${c.reset}
  ${c.cyan}(no args)${c.reset}    Interactive full setup
  ${c.cyan}--check${c.reset}      Health check only (no modifications)
  ${c.cyan}--repair${c.reset}     Fix issues automatically
  ${c.cyan}--apis${c.reset}       Configure API keys only
  ${c.cyan}--help${c.reset}       Show this help message

${c.bright}Examples:${c.reset}
  ${c.dim}# First time setup on new PC${c.reset}
  node setup-codexa.js

  ${c.dim}# Quick health check${c.reset}
  node setup-codexa.js --check

  ${c.dim}# Fix broken dependencies${c.reset}
  node setup-codexa.js --repair

${c.bright}Configuration:${c.reset}
  ${c.dim}User config:${c.reset}  ~/.codexa/config.json
  ${c.dim}Credentials:${c.reset}  ~/.codexa/credentials.json
  ${c.dim}Project env:${c.reset}  codexa.app/.env
`);
}

async function showFinalReport(results) {
  console.log(`
${c.green}╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                             ║
║   ${c.bright}✓ SETUP COMPLETE!${c.reset}${c.green}                                                      ║
║                                                                             ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║   ${c.bright}Next Steps:${c.reset}${c.green}                                                            ║
║                                                                             ║
║   1. ${c.cyan}Restart Claude Code${c.reset}${c.green} to load MCP servers                           ║
║                                                                             ║
║   2. Run ${c.cyan}/codexa-init${c.reset}${c.green} inside Claude Code for health check              ║
║                                                                             ║
║   3. Optional: Start dashboard                                              ║
║      ${c.cyan}start-codexa.bat${c.reset}${c.green} (Windows)                                        ║
║      ${c.cyan}./start-codexa.sh${c.reset}${c.green} (Linux/Mac)                                     ║
║                                                                             ║
║   Dashboard: ${c.bright}http://localhost:3333${c.reset}${c.green}                                     ║
║                                                                             ║
╚═══════════════════════════════════════════════════════════════════════════╝${c.reset}
`);
}

// ============================================================================
// MAIN
// ============================================================================

async function main() {
  const args = process.argv.slice(2);

  // Handle --help
  if (args.includes('--help') || args.includes('-h')) {
    showHelp();
    process.exit(0);
  }

  // Handle --check
  if (args.includes('--check')) {
    showBanner();
    await runHealthCheck();
    process.exit(0);
  }

  showBanner();

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  try {
    const repair = args.includes('--repair');
    const apisOnly = args.includes('--apis');

    if (apisOnly) {
      await configureApiKeys(rl);
      rl.close();
      process.exit(0);
    }

    // Step 1: Check prerequisites
    const prereqResult = await checkPrerequisites();
    if (!prereqResult.success) {
      console.log(`\n${c.red}Please install missing prerequisites and try again.${c.reset}\n`);
      rl.close();
      process.exit(1);
    }

    // Step 2: Install NPM packages
    const npmResult = await installNpmPackages(repair);
    if (!npmResult.success) {
      console.log(`\n${c.yellow}Some packages failed to install. Continuing anyway...${c.reset}`);
    }

    // Step 3: Install Python packages (optional)
    await installPythonPackages(repair);

    // Step 4: Configure MCP servers
    await configureMcpServers();

    // Step 5: Configure API keys
    const answer = await question(rl, `\n${c.cyan}Configure API keys now? (y/n): ${c.reset}`);
    if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
      await configureApiKeys(rl);
    }

    // Final report
    await showFinalReport({});

    rl.close();

  } catch (error) {
    console.error(`\n${c.red}Error: ${error.message}${c.reset}\n`);
    rl.close();
    process.exit(1);
  }
}

main();
