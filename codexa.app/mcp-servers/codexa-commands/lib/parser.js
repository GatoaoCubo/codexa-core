/**
 * Parser Module - Markdown Metadata Extraction
 *
 * Extracts structured metadata from command markdown files:
 * - Title (# heading)
 * - Description (first paragraph)
 * - Arguments ($ARGUMENTS, $1, $2)
 * - Usage examples
 * - Version info
 *
 * @version 1.0.0
 */

import fs from 'fs/promises';
import path from 'path';

/**
 * Parse a command markdown file and extract metadata
 * @param {string} filePath - Full path to the markdown file
 * @returns {Promise<Object>} - Parsed command metadata
 */
export async function parseCommand(filePath) {
  try {
    const content = await fs.readFile(filePath, 'utf-8');
    const fileName = path.basename(filePath, '.md');

    return {
      name: fileName,
      title: extractTitle(content),
      description: extractDescription(content),
      usage: extractUsage(content),
      arguments: extractArguments(content),
      parameters: extractParameters(content),
      examples: extractExamples(content),
      version: extractVersion(content),
      path: filePath,
      content,
    };
  } catch (error) {
    return {
      name: path.basename(filePath, '.md'),
      title: null,
      description: null,
      error: error.message,
      path: filePath,
    };
  }
}

/**
 * Extract title from markdown (first # heading)
 * @param {string} content - Markdown content
 * @returns {string|null} - Title or null
 */
export function extractTitle(content) {
  // Match first # heading (not ##)
  const match = content.match(/^#\s+(.+?)(?:\s*\|.*)?$/m);
  if (match) {
    // Clean up the title (remove | separators if present)
    return match[1].trim().replace(/\s*\|.*$/, '').trim();
  }
  return null;
}

/**
 * Extract description (first paragraph after title or ## Purpose section)
 * @param {string} content - Markdown content
 * @returns {string|null} - Description or null
 */
export function extractDescription(content) {
  // Try to find ## Purpose section first
  const purposeMatch = content.match(/##\s*Purpose\s*\n+([^\n#]+)/i);
  if (purposeMatch) {
    return purposeMatch[1].trim();
  }

  // Fallback: first paragraph after title
  const lines = content.split('\n');
  let foundTitle = false;
  let description = [];

  for (const line of lines) {
    if (line.startsWith('# ')) {
      foundTitle = true;
      continue;
    }
    if (foundTitle && line.trim() && !line.startsWith('#') && !line.startsWith('```')) {
      description.push(line.trim());
      if (description.length >= 2 || line.endsWith('.')) {
        break;
      }
    }
    if (foundTitle && line.startsWith('#')) {
      break;
    }
  }

  return description.length > 0 ? description.join(' ').slice(0, 200) : null;
}

/**
 * Extract usage pattern
 * @param {string} content - Markdown content
 * @returns {string|null} - Usage pattern or null
 */
export function extractUsage(content) {
  // Look for ## Usage section
  const usageMatch = content.match(/##\s*Usage\s*\n+```[^\n]*\n([^`]+)```/i);
  if (usageMatch) {
    return usageMatch[1].trim();
  }

  // Look for inline usage patterns
  const inlineMatch = content.match(/\/([a-z0-9_-]+)(?:\s+\{[^}]+\}|\s+\[.*?\])?/i);
  if (inlineMatch) {
    return inlineMatch[0];
  }

  return null;
}

/**
 * Extract argument placeholders from content
 * @param {string} content - Markdown content
 * @returns {Array} - List of arguments
 */
export function extractArguments(content) {
  const args = [];

  // Pattern 1: $ARGUMENTS (generic)
  if (content.includes('$ARGUMENTS')) {
    args.push({
      name: 'ARGUMENTS',
      type: 'string',
      required: false,
      description: 'Command arguments',
    });
  }

  // Pattern 2: $1, $2, $3 etc. (positional)
  const positionalMatches = content.match(/\$(\d+)/g);
  if (positionalMatches) {
    const unique = [...new Set(positionalMatches)];
    for (const match of unique.sort()) {
      const num = match.replace('$', '');
      args.push({
        name: `arg${num}`,
        type: 'string',
        required: false,
        position: parseInt(num),
        description: `Positional argument ${num}`,
      });
    }
  }

  // Pattern 3: {placeholder} in usage
  const placeholderMatches = content.match(/\{([a-z_]+)\}/gi);
  if (placeholderMatches) {
    const unique = [...new Set(placeholderMatches)];
    for (const match of unique) {
      const name = match.replace(/[{}]/g, '');
      // Skip if already captured
      if (!args.find(a => a.name === name)) {
        args.push({
          name,
          type: 'string',
          required: false,
          description: `Parameter: ${name}`,
        });
      }
    }
  }

  return args;
}

/**
 * Extract parameters from ## Parameters section
 * @param {string} content - Markdown content
 * @returns {Array} - List of parameters
 */
export function extractParameters(content) {
  const params = [];

  // Look for ## Parameters section
  const paramsSection = content.match(/##\s*Parameters[^\n]*\n([\s\S]*?)(?=\n##|\n---|\Z)/i);
  if (paramsSection) {
    // Parse bullet points: - **Name**: Description
    const bulletMatches = paramsSection[1].matchAll(/[-*]\s+\*\*([^*]+)\*\*:\s*(.+)/g);
    for (const match of bulletMatches) {
      params.push({
        name: match[1].trim(),
        description: match[2].trim(),
      });
    }
  }

  return params;
}

/**
 * Extract examples from ## Example or ## Examples section
 * @param {string} content - Markdown content
 * @returns {Array} - List of examples
 */
export function extractExamples(content) {
  const examples = [];

  // Look for ## Example(s) section
  const exampleSection = content.match(/##\s*Examples?\s*\n([\s\S]*?)(?=\n##|\n---|\Z)/i);
  if (exampleSection) {
    // Extract code blocks
    const codeBlocks = exampleSection[1].matchAll(/```[^\n]*\n([^`]+)```/g);
    for (const match of codeBlocks) {
      const code = match[1].trim();
      if (code.startsWith('/') || code.includes('User:') || code.includes('/prime')) {
        examples.push(code);
      }
    }
  }

  return examples.slice(0, 5); // Limit to 5 examples
}

/**
 * Extract version from content
 * @param {string} content - Markdown content
 * @returns {string|null} - Version or null
 */
export function extractVersion(content) {
  const match = content.match(/\*\*Version\*\*:\s*([0-9.]+)/i);
  if (match) {
    return match[1];
  }

  const altMatch = content.match(/Version:\s*([0-9.]+)/i);
  if (altMatch) {
    return altMatch[1];
  }

  return null;
}

/**
 * Parse multiple commands in batch
 * @param {Array} commandPaths - List of command file paths
 * @returns {Promise<Array>} - List of parsed commands
 */
export async function parseCommands(commandPaths) {
  const results = [];

  for (const cmdPath of commandPaths) {
    const parsed = await parseCommand(cmdPath.path || cmdPath);
    if (cmdPath.agent) {
      parsed.agent = cmdPath.agent;
    }
    if (cmdPath.type) {
      parsed.type = cmdPath.type;
    }
    results.push(parsed);
  }

  return results;
}

export default {
  parseCommand,
  parseCommands,
  extractTitle,
  extractDescription,
  extractUsage,
  extractArguments,
  extractParameters,
  extractExamples,
  extractVersion,
};
