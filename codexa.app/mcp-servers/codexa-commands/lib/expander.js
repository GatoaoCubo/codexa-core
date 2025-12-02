/**
 * Expander Module - Prompt Expansion with Arguments
 *
 * Expands command prompts with user-provided arguments:
 * - Replaces $ARGUMENTS with full argument string
 * - Replaces $1, $2, $3 with positional arguments
 * - Replaces {placeholder} with named arguments
 * - Resolves context file references
 *
 * @version 1.0.0
 */

import fs from 'fs/promises';
import path from 'path';
import { glob } from 'glob';

/**
 * Expand a command prompt with arguments
 * @param {string} content - Command markdown content
 * @param {Object} args - Arguments object { positional: [], named: {}, raw: '' }
 * @returns {string} - Expanded prompt content
 */
export function expandPrompt(content, args = {}) {
  let expanded = content;

  // Replace $ARGUMENTS with raw arguments string
  if (args.raw) {
    expanded = expanded.replace(/\$ARGUMENTS/g, args.raw);
  }

  // Replace positional arguments ($1, $2, etc.)
  if (args.positional && Array.isArray(args.positional)) {
    for (let i = 0; i < args.positional.length; i++) {
      const placeholder = `$${i + 1}`;
      expanded = expanded.replace(new RegExp(`\\$${i + 1}`, 'g'), args.positional[i]);
    }
  }

  // Replace named arguments ({placeholder})
  if (args.named && typeof args.named === 'object') {
    for (const [key, value] of Object.entries(args.named)) {
      const pattern = new RegExp(`\\{${key}\\}`, 'gi');
      expanded = expanded.replace(pattern, value);
    }
  }

  return expanded;
}

/**
 * Parse user input into arguments structure
 * @param {string} input - Raw user input
 * @returns {Object} - Parsed arguments { positional: [], named: {}, raw: '' }
 */
export function parseArguments(input) {
  const result = {
    positional: [],
    named: {},
    raw: input || '',
  };

  if (!input) return result;

  // Parse named arguments (key=value or key:value)
  const namedPattern = /(\w+)\s*[=:]\s*(?:"([^"]+)"|'([^']+)'|([^\s,]+))/g;
  let match;
  const processedParts = [];

  while ((match = namedPattern.exec(input)) !== null) {
    const key = match[1];
    const value = match[2] || match[3] || match[4];
    result.named[key] = value;
    processedParts.push(match[0]);
  }

  // Remaining parts are positional arguments
  let remaining = input;
  for (const part of processedParts) {
    remaining = remaining.replace(part, '');
  }

  // Split remaining by common delimiters
  const positional = remaining
    .split(/[,;]+/)
    .map(s => s.trim())
    .filter(s => s.length > 0);

  result.positional = positional;

  return result;
}

/**
 * Find context files referenced in the command
 * @param {string} content - Command markdown content
 * @param {string} rootPath - Project root path
 * @param {string} agentName - Agent name for context resolution
 * @returns {Promise<Array>} - List of context file paths
 */
export async function findContextFiles(content, rootPath, agentName = null) {
  const contextFiles = [];

  // Pattern 1: Explicit file references (e.g., agentes/xxx/config/xxx.json)
  const fileRefs = content.match(/agentes\/[^\s)]+\.(md|json|py)/g) || [];
  for (const ref of fileRefs) {
    const fullPath = path.join(rootPath, 'codexa.app', ref);
    try {
      await fs.access(fullPath);
      contextFiles.push({
        path: ref,
        fullPath,
        type: 'explicit',
      });
    } catch {
      // File doesn't exist
    }
  }

  // Pattern 2: HOP references (e.g., prompts/xxx_HOP.md)
  const hopRefs = content.match(/prompts\/[^\s)]+_HOP\.md/g) || [];
  for (const ref of hopRefs) {
    if (agentName) {
      const fullPath = path.join(rootPath, 'codexa.app', 'agentes', agentName, ref);
      try {
        await fs.access(fullPath);
        contextFiles.push({
          path: `agentes/${agentName}/${ref}`,
          fullPath,
          type: 'hop',
        });
      } catch {
        // File doesn't exist
      }
    }
  }

  // Pattern 3: PRIME.md references
  if (content.includes('PRIME.md') && agentName) {
    const primePath = path.join(rootPath, 'codexa.app', 'agentes', agentName, 'PRIME.md');
    try {
      await fs.access(primePath);
      contextFiles.push({
        path: `agentes/${agentName}/PRIME.md`,
        fullPath: primePath,
        type: 'prime',
      });
    } catch {
      // File doesn't exist
    }
  }

  // Pattern 4: Config files referenced
  if (content.includes('config/') && agentName) {
    try {
      const configFiles = await glob(`codexa.app/agentes/${agentName}/config/*.json`, {
        cwd: rootPath,
        absolute: true,
      });
      for (const configPath of configFiles) {
        const relativePath = path.relative(path.join(rootPath, 'codexa.app'), configPath);
        contextFiles.push({
          path: relativePath.replace(/\\/g, '/'),
          fullPath: configPath,
          type: 'config',
        });
      }
    } catch {
      // Glob failed
    }
  }

  return contextFiles;
}

/**
 * Create an execution context for a command
 * @param {Object} parsedCommand - Parsed command metadata
 * @param {Object} args - User arguments
 * @param {string} rootPath - Project root path
 * @returns {Promise<Object>} - Execution context
 */
export async function createExecutionContext(parsedCommand, args, rootPath) {
  const expandedPrompt = expandPrompt(parsedCommand.content, args);
  const contextFiles = await findContextFiles(
    parsedCommand.content,
    rootPath,
    parsedCommand.agent
  );

  return {
    command: parsedCommand.name,
    agent: parsedCommand.agent,
    expanded_prompt: expandedPrompt,
    arguments: args,
    context_files: contextFiles,
    metadata: {
      title: parsedCommand.title,
      description: parsedCommand.description,
      version: parsedCommand.version,
    },
  };
}

export default {
  expandPrompt,
  parseArguments,
  findContextFiles,
  createExecutionContext,
};
