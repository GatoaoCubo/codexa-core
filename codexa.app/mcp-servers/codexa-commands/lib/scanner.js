/**
 * Scanner Module - Dynamic Command Discovery
 * Scans directories for slash commands in agent and global locations.
 * @version 1.0.0
 */

import { glob } from 'glob';
import path from 'path';

/**
 * Scan for all commands in the project
 * @param {string} rootPath - Project root path
 * @returns {Promise<Array>} - List of command file paths
 */
export async function scanCommands(rootPath) {
  const commands = [];

  // Pattern 1: Agent-level commands
  const agentPattern = 'codexa.app/agentes/*/commands/*.md';

  // Pattern 2: Global commands (root .claude/commands/)
  const globalPattern = '.claude/commands/*.md';

  try {
    // Scan agent commands
    const agentFiles = await glob(agentPattern, {
      cwd: rootPath,
      absolute: true,
      ignore: ['**/README.md', '**/COMO_USAR.md'],
    });

    for (const filePath of agentFiles) {
      const relativePath = path.relative(rootPath, filePath).replace(/\\/g, '/');
      const agent = extractAgentFromPath(relativePath);

      commands.push({
        path: filePath,
        relativePath,
        agent,
        type: 'agent',
      });
    }

    // Scan global commands
    const globalFiles = await glob(globalPattern, {
      cwd: rootPath,
      absolute: true,
      ignore: ['**/README.md', '**/COMO_USAR.md'],
    });

    for (const filePath of globalFiles) {
      const relativePath = path.relative(rootPath, filePath).replace(/\\/g, '/');

      commands.push({
        path: filePath,
        relativePath,
        agent: null,
        type: 'global',
      });
    }

  } catch (error) {
    console.error('[scanner] Error scanning commands:', error.message);
  }

  return commands;
}

/**
 * Extract agent name from file path
 * @param {string} filePath - Relative file path
 * @returns {string|null} - Agent name or null
 */
export function extractAgentFromPath(filePath) {
  const match = filePath.match(/agentes\/([^\/]+)\/commands\//);
  if (match) {
    return match[1];
  }
  return null;
}

/**
 * Get all unique agents that have commands
 * @param {Array} commands - List of scanned commands
 * @returns {Array} - List of unique agent names
 */
export function getUniqueAgents(commands) {
  const agents = new Set();

  for (const cmd of commands) {
    if (cmd.agent) {
      agents.add(cmd.agent);
    }
  }

  return Array.from(agents).sort();
}

/**
 * Filter commands by agent
 * @param {Array} commands - List of scanned commands
 * @param {string} agentName - Agent name to filter
 * @returns {Array} - Filtered commands
 */
export function filterByAgent(commands, agentName) {
  return commands.filter(cmd => cmd.agent === agentName);
}

/**
 * Filter global commands only
 * @param {Array} commands - List of scanned commands
 * @returns {Array} - Global commands only
 */
export function filterGlobal(commands) {
  return commands.filter(cmd => cmd.type === 'global');
}

export default {
  scanCommands,
  extractAgentFromPath,
  getUniqueAgents,
  filterByAgent,
  filterGlobal,
};
