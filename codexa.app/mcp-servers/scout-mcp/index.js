#!/usr/bin/env node
/**
 * Scout MCP Server - Path Discovery & Navigation System
 *
 * The "Master of Paths" for CODEXA - knows where everything is.
 *
 * Tools:
 * - discover: Find files relevant to a query (with intent detection)
 * - smart_context: Get intelligent agent context for LLMs
 * - search: Search by glob pattern
 * - agent_context: Get all files for an agent
 * - create/read/update/delete/move: CRUD operations
 * - refresh/stats: Index management
 *
 * @version 1.2.0
 * @author CODEXA Meta-Constructor
 *
 * CHANGELOG v1.2.0:
 * - Added semantic_aliases.json for PT/EN query expansion
 * - Added importance scores to categories (0-100 scale)
 * - New tool: smart_context - LLM-optimized agent context
 * - Enhanced discover with intent/agent detection
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { createHash } from 'crypto';
import { glob } from 'glob';
import { minimatch } from 'minimatch';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============================================================================
// SEMANTIC ALIASES (loaded from config)
// ============================================================================

let SEMANTIC_ALIASES = null;

async function loadSemanticAliases() {
  const aliasesPath = path.join(__dirname, '../../agentes/scout_agent/config/semantic_aliases.json');
  try {
    const content = await fs.readFile(aliasesPath, 'utf-8');
    SEMANTIC_ALIASES = JSON.parse(content);
    log('info', 'Semantic aliases loaded', { agents: Object.keys(SEMANTIC_ALIASES.agent_aliases || {}).length });
  } catch (e) {
    log('warn', 'Could not load semantic_aliases.json, using defaults', { error: e.message });
    SEMANTIC_ALIASES = { agent_aliases: {}, intent_patterns: {}, category_aliases: {} };
  }
}

// ============================================================================
// CONFIGURATION
// ============================================================================

/**
 * Auto-detect project root by walking up the directory tree
 * Looks for markers: .git, codexa.gato folder, or PRIME.md at root
 */
function findProjectRoot(startDir) {
  let current = startDir;
  const markers = ['.git', 'PRIME.md', 'codexa.app'];

  // Walk up the directory tree
  while (current !== path.dirname(current)) {
    // Check if this looks like the project root
    for (const marker of markers) {
      const markerPath = path.join(current, marker);
      try {
        // Sync check for existence (only at startup)
        require('fs').accessSync(markerPath);

        // Special case: if we find codexa.app, go up one level to codexa.gato
        if (marker === 'codexa.app') {
          return current;
        }

        // For .git or PRIME.md, check if we're in codexa.gato
        if (current.includes('codexa.gato')) {
          // Find the codexa.gato level
          const codexaMatch = current.match(/(.+[\\\/]codexa\.gato)/);
          if (codexaMatch) {
            return codexaMatch[1];
          }
        }

        return current;
      } catch (e) {
        // Marker not found, continue
      }
    }
    current = path.dirname(current);
  }

  // Fallback to cwd
  return startDir;
}

const PROJECT_ROOT = process.env.SCOUT_ROOT || findProjectRoot(process.cwd());
const CACHE_MODE = process.env.SCOUT_CACHE_MODE || 'session';
const LOG_LEVEL = process.env.SCOUT_LOG_LEVEL || 'info';

// Category patterns, priorities, and importance (synced with config/categories.json v1.4.0)
// importance: 0-100 scale for LLM navigation (higher = more important to read)
const CATEGORIES = {
  prime: { patterns: ['**/PRIME.md'], priority: 1.0, importance: 100 },
  instructions: { patterns: ['**/INSTRUCTIONS.md'], priority: 0.85, importance: 95 },
  readme: { patterns: ['**/README.md'], priority: 0.9, importance: 90 },
  hop: { patterns: ['**/*_HOP.md', '**/*_hop.md'], priority: 0.8, importance: 85 },
  adw: { patterns: ['**/*_ADW*.md', '**/ADW_*.md'], priority: 0.8, importance: 85 },
  setup: { patterns: ['**/SETUP.md'], priority: 0.8, importance: 80 },
  architecture: { patterns: ['**/ARCHITECTURE*.md', '**/ARQUITETURA*.md'], priority: 0.75, importance: 80 },
  schema: { patterns: ['**/schema*.json', '**/schemas/**/*.json', '**/*_schema.json', '**/input_schema.json'], priority: 0.6, importance: 75 },
  changelog: { patterns: ['**/CHANGELOG*.md', '**/CHANGELOG.md'], priority: 0.75, importance: 70 },
  vision: { patterns: ['**/VISION.md', '**/VISAO.md'], priority: 0.7, importance: 70 },
  guide: { patterns: ['**/GUIA*.md', '**/*_GUIDE.md', '**/GUIDE*.md'], priority: 0.7, importance: 70 },
  command: { patterns: ['**/.claude/commands/**/*.md'], priority: 0.7, importance: 70 },
  config: { patterns: ['**/config/**/*.json', '**/config.json'], priority: 0.7, importance: 65 },
  prompt: { patterns: ['**/prompts/**/*.md'], priority: 0.7, importance: 65 },
  iso_vectorstore: { patterns: ['**/iso_vectorstore/**/*'], priority: 0.7, importance: 65 },
  builder: { patterns: ['**/builders/**/*.py', '**/builders/**/*.js'], priority: 0.6, importance: 60 },
  validator: { patterns: ['**/validators/**/*.py', '**/validators/**/*.js'], priority: 0.6, importance: 60 },
  workflow: { patterns: ['**/workflows/**/*.md'], priority: 0.6, importance: 60 },
  adw_code: { patterns: ['adws/**/*.py', '**/adws/**/*.py'], priority: 0.6, importance: 60 },
  core: { patterns: ['**/core/**/*.py', '**/core/**/*.js'], priority: 0.6, importance: 60 },
  api: { patterns: ['**/api/**/*.py', '**/api/**/*.js', '**/routes/**/*.py', '**/routes/**/*.js'], priority: 0.6, importance: 55 },
  knowledge: { patterns: ['**/knowledge/**/*', '**/conhecimento/**/*'], priority: 0.65, importance: 55 },
  voice: { patterns: ['**/voice/**/*.py', '**/voice/**/*.js'], priority: 0.55, importance: 55 },
  mcp: { patterns: ['**/mcp-servers/**/*.js', '**/mcp-servers/**/*.ts', '**/mcp-servers/**/*.json'], priority: 0.55, importance: 55 },
  server: { patterns: ['**/server/**/*.py', '**/server/**/*.js'], priority: 0.55, importance: 55 },
  context: { patterns: ['**/context/**/*', '**/contexto/**/*'], priority: 0.55, importance: 50 },
  planning: { patterns: ['**/planning/**/*', '**/planejamento/**/*'], priority: 0.55, importance: 50 },
  processados: { patterns: ['**/processados/**/*', '**/processed/**/*'], priority: 0.6, importance: 50 },
  source: { patterns: ['**/src/**/*.py', '**/src/**/*.js', '**/src/**/*.ts'], priority: 0.5, importance: 50 },
  docs: { patterns: ['**/docs/**/*.md'], priority: 0.5, importance: 50 },
  template: { patterns: ['**/templates/**/*'], priority: 0.5, importance: 50 },
  memory: { patterns: ['**/memory/**/*', '**/memoria/**/*'], priority: 0.5, importance: 45 },
  scripts: { patterns: ['python/**/*.py', 'scripts/**/*', '**/scripts/**/*.py', '**/scripts/**/*.sh'], priority: 0.5, importance: 45 },
  fontes: { patterns: ['**/FONTES/**/*', '**/fontes/**/*', '**/sources/**/*'], priority: 0.5, importance: 40 },
  user_output: { patterns: ['**/USER_DOCS/**/*', '**/user_docs/**/*'], priority: 0.5, importance: 40 },
  example: { patterns: ['**/examples/**/*', '**/EXAMPLE*.md', '**/EXEMPLO*.md'], priority: 0.4, importance: 40 },
  outputs: { patterns: ['**/outputs/**/*'], priority: 0.5, importance: 35 },
  test: { patterns: ['**/tests/**/*', '**/test_*.py', '**/*_test.py'], priority: 0.4, importance: 35 },
  rascunho: { patterns: ['**/RASCUNHO/**/*', '**/rascunho/**/*', '**/drafts/**/*'], priority: 0.45, importance: 30 },
  landing: { patterns: ['**/landing-pages/**/*', '**/landings/**/*'], priority: 0.4, importance: 30 },
  html: { patterns: ['**/*.html', '**/*.htm'], priority: 0.35, importance: 25 },
  asset: { patterns: ['**/assets/**/*', '**/images/**/*', '**/img/**/*'], priority: 0.4, importance: 20 },
  css: { patterns: ['**/*.css', '**/*.scss', '**/*.sass'], priority: 0.35, importance: 20 },
};

const DEFAULT_IMPORTANCE = 10;

const IGNORE_PATTERNS = [
  '**/node_modules/**',
  '**/.venv/**',
  '**/venv/**',
  '**/__pycache__/**',
  '**/*.pyc',
  '**/.git/**',
  '**/.github/**',
  '*.pyc',
  '*.pyo',
  '*.pyd',
  '*.so',
  '*.dll',
  '*.exe',
  '*.log',
  '*.tmp',
  '*.temp',
  '*.bak',
  '**/*.bak',
  '**/*.deleted.bak',
  '*.swp',
  '*.swo',
  '.DS_Store',
  'Thumbs.db',
  'desktop.ini',
  '**/*.egg-info/**',
  '**/dist/**',
  '**/build/**',
  '**/.pytest_cache/**',
  '**/.mypy_cache/**',
  '**/.ruff_cache/**',
  '**/coverage/**',
  '**/.coverage',
  '**/htmlcov/**',
  '*.min.js',
  '*.min.css',
  '*.map',
  'package-lock.json',
  'yarn.lock',
  'pnpm-lock.yaml',
  '.env',
  '.env.*',
  '*.sqlite',
  '*.db',
  '**/screenshots/**',
  '**/outputs/**/*.json',
  '**/logs/**',
  '**/nul',
  'nul',
];

const PROTECTED_PATHS = [
  '.git/**',
  'node_modules/**',
  '.venv/**',
  '*.exe',
  '*.dll',
];

// Relevance weights
const WEIGHTS = {
  text_match: 0.40,
  category_priority: 0.20,
  agent_match: 0.25,
  recency: 0.15,
};

// ============================================================================
// INDEX DATA STRUCTURE
// ============================================================================

let fileIndex = new Map();
let indexBuiltAt = null;

/**
 * File entry in the index
 */
class FileEntry {
  constructor(filePath, stats, content = null) {
    this.path = filePath;
    this.relativePath = path.relative(PROJECT_ROOT, filePath);
    this.name = path.basename(filePath);
    this.ext = path.extname(filePath);
    this.size = stats.size;
    this.modified = stats.mtime;
    this.category = detectCategory(filePath);
    this.agent = detectAgent(filePath);
    this.tags = extractTags(filePath, content);
    this.hash = content ? createHash('md5').update(content).digest('hex').slice(0, 8) : null;
  }
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

function log(level, message, data = {}) {
  const levels = { debug: 0, info: 1, warn: 2, error: 3 };
  if (levels[level] >= levels[LOG_LEVEL]) {
    console.error(`[scout:${level}] ${message}`, Object.keys(data).length ? JSON.stringify(data) : '');
  }
}

function detectCategory(filePath) {
  const relativePath = path.relative(PROJECT_ROOT, filePath).replace(/\\/g, '/');

  for (const [category, config] of Object.entries(CATEGORIES)) {
    for (const pattern of config.patterns) {
      // Use minimatch for proper glob matching
      if (minimatch(relativePath, pattern, { nocase: true, dot: true })) {
        return category;
      }
    }
  }
  return 'other';
}

function detectAgent(filePath) {
  const relativePath = path.relative(PROJECT_ROOT, filePath).replace(/\\/g, '/');

  // Pattern 1: agentes/{agent_name}/ or agents/{agent_name}/
  const agentMatch = relativePath.match(/agente?s[\\\/]([^\\\/]+)[\\\/]/i);
  if (agentMatch) {
    // Normalize: convert hyphens to underscores for consistency
    return agentMatch[1].replace(/-/g, '_');
  }

  // Pattern 2: {name}_agent/ or {name}-agent/
  const agentMatch2 = relativePath.match(/([^\\\/]+)[_-]agent[\\\/]/i);
  if (agentMatch2) {
    // Normalize: always use underscore format
    return agentMatch2[1].replace(/-/g, '_') + '_agent';
  }

  // Pattern 3: Check for agent in path component (e.g., codexa_agent/subdir/)
  const pathParts = relativePath.split('/');
  for (const part of pathParts) {
    if (part.match(/^[a-z0-9]+[_-]agent$/i)) {
      return part.replace(/-/g, '_');
    }
  }

  return null;
}

function extractTags(filePath, content = null) {
  const tags = [];
  const relativePath = path.relative(PROJECT_ROOT, filePath).replace(/\\/g, '/');

  // Extract from path
  const parts = relativePath.split(/[\\\/]/);
  for (const part of parts) {
    if (part && !part.startsWith('.') && part !== 'codexa.app') {
      tags.push(part.toLowerCase().replace(/[_-]/g, ' '));
    }
  }

  // Extract from filename
  const name = path.basename(filePath, path.extname(filePath));
  tags.push(...name.toLowerCase().split(/[_-]/).filter(t => t.length > 2));

  return [...new Set(tags)];
}

// ============================================================================
// SEMANTIC DETECTION (v1.2.0)
// ============================================================================

/**
 * Detect which agent the query is referring to using semantic aliases
 */
function detectAgentFromQuery(query) {
  if (!SEMANTIC_ALIASES?.agent_aliases) return null;

  const queryLower = query.toLowerCase();
  let bestMatch = null;
  let bestScore = 0;

  for (const [agentName, aliases] of Object.entries(SEMANTIC_ALIASES.agent_aliases)) {
    let score = 0;

    // Check PT aliases
    for (const alias of aliases.pt || []) {
      if (queryLower.includes(alias.toLowerCase())) {
        score += 1.0;
      }
    }

    // Check EN aliases
    for (const alias of aliases.en || []) {
      if (queryLower.includes(alias.toLowerCase())) {
        score += 0.9;
      }
    }

    // Check keywords
    for (const keyword of aliases.keywords || []) {
      if (queryLower.includes(keyword.toLowerCase())) {
        score += 0.5;
      }
    }

    if (score > bestScore) {
      bestScore = score;
      bestMatch = agentName;
    }
  }

  return bestScore > 0.5 ? { agent: bestMatch, confidence: Math.min(1, bestScore / 2) } : null;
}

/**
 * Detect the user's intent from the query
 */
function detectIntent(query) {
  if (!SEMANTIC_ALIASES?.intent_patterns) return null;

  const queryLower = query.toLowerCase();
  let bestIntent = null;
  let bestScore = 0;

  for (const [intent, config] of Object.entries(SEMANTIC_ALIASES.intent_patterns)) {
    let matches = 0;

    // Check PT patterns
    for (const pattern of config.pt || []) {
      if (queryLower.includes(pattern.toLowerCase())) {
        matches++;
      }
    }

    // Check EN patterns
    for (const pattern of config.en || []) {
      if (queryLower.includes(pattern.toLowerCase())) {
        matches++;
      }
    }

    const score = matches * (config.priority || 0.5);
    if (score > bestScore) {
      bestScore = score;
      bestIntent = intent;
    }
  }

  return bestScore > 0 ? { intent: bestIntent, confidence: Math.min(1, bestScore) } : null;
}

/**
 * Expand query using semantic aliases
 */
function expandQuery(query) {
  if (!SEMANTIC_ALIASES) return [query];

  const terms = [query];
  const queryLower = query.toLowerCase();

  // Add agent aliases
  for (const [agentName, aliases] of Object.entries(SEMANTIC_ALIASES.agent_aliases || {})) {
    const allAliases = [...(aliases.pt || []), ...(aliases.en || []), ...(aliases.keywords || [])];
    for (const alias of allAliases) {
      if (queryLower.includes(alias.toLowerCase())) {
        terms.push(agentName);
        break;
      }
    }
  }

  // Add category aliases
  for (const [category, aliases] of Object.entries(SEMANTIC_ALIASES.category_aliases || {})) {
    for (const alias of aliases) {
      if (queryLower.includes(alias.toLowerCase())) {
        terms.push(category);
        break;
      }
    }
  }

  return [...new Set(terms)];
}

/**
 * Get importance tier for a score
 */
function getImportanceTier(importance) {
  if (importance >= 90) return 'critical';
  if (importance >= 70) return 'high';
  if (importance >= 50) return 'medium';
  if (importance >= 30) return 'low';
  return 'skip';
}

function calculateRelevance(query, entry, targetAgent = null) {
  let score = 0;
  const queryLower = query.toLowerCase();
  const queryTerms = queryLower.split(/\s+/);

  // 1. Text match (40%)
  let textScore = 0;
  const searchText = (entry.relativePath + ' ' + entry.tags.join(' ')).toLowerCase();

  for (const term of queryTerms) {
    if (searchText.includes(term)) {
      textScore += 1 / queryTerms.length;
    }
  }
  // Boost for exact matches
  if (searchText.includes(queryLower)) {
    textScore = Math.min(1, textScore + 0.3);
  }
  score += textScore * WEIGHTS.text_match;

  // 2. Category priority (20%)
  const categoryPriority = CATEGORIES[entry.category]?.priority || 0.3;
  score += categoryPriority * WEIGHTS.category_priority;

  // 3. Agent match (25%)
  if (targetAgent && entry.agent === targetAgent) {
    score += WEIGHTS.agent_match;
  } else if (!targetAgent && entry.agent) {
    // Small boost if file belongs to any agent
    score += WEIGHTS.agent_match * 0.3;
  }

  // 4. Recency (15%)
  const daysOld = (Date.now() - entry.modified.getTime()) / (1000 * 60 * 60 * 24);
  const recencyScore = Math.max(0, 1 - (daysOld / 365));
  score += recencyScore * WEIGHTS.recency;

  return Math.min(1, score);
}

function shouldIgnore(filePath) {
  const relativePath = path.relative(PROJECT_ROOT, filePath).replace(/\\/g, '/');

  for (const pattern of IGNORE_PATTERNS) {
    if (minimatch(relativePath, pattern, { nocase: true, dot: true })) {
      return true;
    }
  }
  return false;
}

function isProtected(filePath) {
  const relativePath = path.relative(PROJECT_ROOT, filePath).replace(/\\/g, '/');

  for (const pattern of PROTECTED_PATHS) {
    if (minimatch(relativePath, pattern, { nocase: true, dot: true })) {
      return true;
    }
  }
  return false;
}

// ============================================================================
// INDEX OPERATIONS
// ============================================================================

async function buildIndex() {
  const startTime = Date.now();
  fileIndex.clear();

  log('info', 'Building index...', { root: PROJECT_ROOT });

  try {
    // Use glob to find all files
    const files = await glob('**/*', {
      cwd: PROJECT_ROOT,
      nodir: true,
      ignore: IGNORE_PATTERNS,
      absolute: true,
    });

    for (const filePath of files) {
      try {
        if (shouldIgnore(filePath)) continue;

        const stats = await fs.stat(filePath);
        if (stats.size > 1048576) continue; // Skip files > 1MB

        // Read content for text files
        let content = null;
        const ext = path.extname(filePath).toLowerCase();
        if (['.md', '.json', '.py', '.js', '.ts', '.txt'].includes(ext)) {
          try {
            content = await fs.readFile(filePath, 'utf-8');
          } catch (e) {
            // Skip unreadable files
          }
        }

        const entry = new FileEntry(filePath, stats, content);
        fileIndex.set(entry.relativePath, entry);
      } catch (e) {
        // Skip inaccessible files
      }
    }

    indexBuiltAt = new Date();
    const duration = Date.now() - startTime;

    log('info', 'Index built', {
      files: fileIndex.size,
      duration_ms: duration
    });

    return {
      files_indexed: fileIndex.size,
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

async function toolDiscover(query, agent = null, maxResults = 10, detectIntentFlag = true) {
  if (fileIndex.size === 0) {
    await buildIndex();
  }

  const startTime = Date.now();

  // Semantic detection
  const detectedAgent = detectIntentFlag ? detectAgentFromQuery(query) : null;
  const detectedIntent = detectIntentFlag ? detectIntent(query) : null;
  const expandedTerms = expandQuery(query);

  // Use detected agent if none provided
  const effectiveAgent = agent || detectedAgent?.agent;

  const results = [];

  for (const entry of fileIndex.values()) {
    // Calculate relevance with expanded terms
    let maxScore = 0;
    for (const term of expandedTerms) {
      const score = calculateRelevance(term, entry, effectiveAgent);
      maxScore = Math.max(maxScore, score);
    }

    // Boost by importance
    const importance = CATEGORIES[entry.category]?.importance || DEFAULT_IMPORTANCE;
    const importanceBoost = importance / 100 * 0.2; // Up to 0.2 boost
    maxScore = Math.min(1, maxScore + importanceBoost);

    if (maxScore > 0.15) {
      results.push({
        path: entry.relativePath,
        relevance_score: Math.round(maxScore * 100) / 100,
        importance: importance,
        importance_tier: getImportanceTier(importance),
        reason: generateReason(entry, query),
        category: entry.category,
        agent: entry.agent,
      });
    }
  }

  // Sort by relevance, then by importance
  results.sort((a, b) => {
    if (Math.abs(b.relevance_score - a.relevance_score) > 0.1) {
      return b.relevance_score - a.relevance_score;
    }
    return b.importance - a.importance;
  });

  // Build recommended reading order for top results
  const topResults = results.slice(0, maxResults);
  const readingOrder = topResults
    .filter(r => r.importance >= 70)
    .sort((a, b) => b.importance - a.importance)
    .slice(0, 5)
    .map((r, i) => `${i + 1}. ${r.path} (${r.reason})`);

  return {
    query,
    expanded_terms: expandedTerms.length > 1 ? expandedTerms : undefined,
    detected_agent: detectedAgent,
    detected_intent: detectedIntent,
    agent_filter: effectiveAgent,
    relevant_files: topResults,
    total_found: results.length,
    search_time_ms: Date.now() - startTime,
    recommended_reading_order: readingOrder.length > 0 ? readingOrder : undefined,
  };
}

/**
 * Smart Context - LLM-optimized agent context (v1.2.0)
 * Returns a condensed, prioritized view of an agent's files
 */
async function toolSmartContext(agentName, maxFiles = 20, includeHints = true) {
  if (fileIndex.size === 0) {
    await buildIndex();
  }

  const allFiles = [];
  const entryPoints = {};
  const filesByTier = {
    critical: [],
    high: [],
    medium: [],
    low: [],
    skip: [],
  };

  // Collect all agent files
  for (const entry of fileIndex.values()) {
    if (entry.agent === agentName || entry.relativePath.includes(agentName)) {
      const importance = CATEGORIES[entry.category]?.importance || DEFAULT_IMPORTANCE;
      const tier = getImportanceTier(importance);

      const fileInfo = {
        path: entry.relativePath,
        category: entry.category,
        importance,
        tier,
        hint: includeHints ? (CATEGORIES[entry.category]?.llm_hint || generateReason(entry, '')) : undefined,
      };

      allFiles.push(fileInfo);
      filesByTier[tier].push(fileInfo);

      // Detect entry points
      if (entry.category === 'prime') {
        entryPoints.prime = entry.relativePath;
      } else if (entry.category === 'readme') {
        entryPoints.readme = entry.relativePath;
      } else if (entry.category === 'instructions') {
        entryPoints.instructions = entry.relativePath;
      }
    }
  }

  // Sort each tier by importance
  for (const tier of Object.keys(filesByTier)) {
    filesByTier[tier].sort((a, b) => b.importance - a.importance);
  }

  // Build must_read list (critical + high tier, limited)
  const mustRead = [
    ...filesByTier.critical.slice(0, 5),
    ...filesByTier.high.slice(0, 5),
  ].slice(0, maxFiles);

  // Build summary
  const summary = `Agent "${agentName}" - ${allFiles.length} files total. ` +
    `Critical: ${filesByTier.critical.length}, High: ${filesByTier.high.length}, ` +
    `Medium: ${filesByTier.medium.length}, Low: ${filesByTier.low.length}`;

  // Generate reading flow
  const readingFlow = [];
  if (entryPoints.prime) {
    readingFlow.push(`1. Start with PRIME.md - ${entryPoints.prime}`);
  }
  if (entryPoints.instructions) {
    readingFlow.push(`2. Read INSTRUCTIONS.md for usage - ${entryPoints.instructions}`);
  }
  const schemaFiles = allFiles.filter(f => f.category === 'schema');
  if (schemaFiles.length > 0) {
    readingFlow.push(`3. Check input schema - ${schemaFiles[0].path}`);
  }
  const hopFiles = allFiles.filter(f => f.category === 'hop');
  if (hopFiles.length > 0) {
    readingFlow.push(`4. Execute via HOP files (${hopFiles.length} available)`);
  }

  return {
    agent: agentName,
    summary,
    entry_points: entryPoints,
    must_read: mustRead,
    reading_flow: readingFlow,
    files_by_tier: {
      critical: filesByTier.critical.length,
      high: filesByTier.high.length,
      medium: filesByTier.medium.length,
      low: filesByTier.low.length,
      skip: filesByTier.skip.length,
    },
    all_files: allFiles.length <= 50 ? allFiles : undefined, // Only include if reasonable size
    total_files: allFiles.length,
  };
}

function generateReason(entry, query) {
  const categoryNames = {
    prime: 'Agent entry point',
    readme: 'Documentation',
    instructions: 'AI instructions',
    setup: 'Setup guide',
    changelog: 'Version history',
    architecture: 'Architecture doc',
    vision: 'Project vision',
    guide: 'User/dev guide',
    hop: 'Higher-Order Prompt',
    adw: 'Agentic Workflow',
    config: 'Configuration',
    prompt: 'Prompt template',
    schema: 'JSON schema',
    builder: 'Builder script',
    validator: 'Validator script',
    command: 'Slash command',
    workflow: 'Workflow definition',
    planning: 'Planning doc',
    fontes: 'Source reference',
    user_output: 'User documentation',
    rascunho: 'Draft/WIP file',
    context: 'Context file',
    iso_vectorstore: 'Agent knowledge',
    scripts: 'Utility script',
    adw_code: 'ADW Python code',
    voice: 'Voice module',
    mcp: 'MCP server',
    core: 'Core module',
    api: 'API handler',
    server: 'Server code',
    html: 'HTML file',
    css: 'Stylesheet',
    landing: 'Landing page',
    source: 'Source code',
    docs: 'Documentation',
    template: 'Template file',
    memory: 'Memory storage',
    asset: 'Static asset',
    test: 'Test file',
    example: 'Example file',
    processados: 'Processed file',
    knowledge: 'Knowledge base',
    outputs: 'Generated output',
  };

  return categoryNames[entry.category] || `File in ${entry.category}`;
}

async function toolSearch(pattern, type = null) {
  if (fileIndex.size === 0) {
    await buildIndex();
  }

  const results = [];

  for (const entry of fileIndex.values()) {
    // Use minimatch for proper glob matching
    const normalizedPath = entry.relativePath.replace(/\\/g, '/');
    if (minimatch(normalizedPath, pattern, { nocase: true, dot: true })) {
      if (type && entry.category !== type) continue;

      results.push({
        path: entry.relativePath,
        category: entry.category,
        agent: entry.agent,
        size: entry.size,
        modified: entry.modified.toISOString(),
      });
    }
  }

  return {
    pattern,
    type_filter: type,
    files: results,
    total_found: results.length,
  };
}

async function toolAgentContext(agentName, includeDeps = true) {
  if (fileIndex.size === 0) {
    await buildIndex();
  }

  const entryPoints = {};
  const filesByCategory = {};
  const allFiles = [];

  for (const entry of fileIndex.values()) {
    if (entry.agent === agentName || entry.relativePath.includes(agentName)) {
      allFiles.push(entry);

      // Detect entry points
      if (entry.category === 'prime') {
        entryPoints.prime = entry.relativePath;
      } else if (entry.category === 'readme') {
        entryPoints.readme = entry.relativePath;
      } else if (entry.category === 'instructions') {
        entryPoints.instructions = entry.relativePath;
      } else if (entry.category === 'command') {
        entryPoints.commands = entryPoints.commands || [];
        entryPoints.commands.push(entry.relativePath);
      }

      // Group by category
      if (!filesByCategory[entry.category]) {
        filesByCategory[entry.category] = [];
      }
      filesByCategory[entry.category].push(entry.relativePath);
    }
  }

  // Detect dependencies from PRIME if exists
  let dependencies = { requires: [], optional: [] };
  if (entryPoints.prime) {
    try {
      const primeContent = await fs.readFile(
        path.join(PROJECT_ROOT, entryPoints.prime),
        'utf-8'
      );
      // Simple dependency extraction
      const depMatch = primeContent.match(/dependencies['"]*:\s*\[(.*?)\]/s);
      if (depMatch) {
        const deps = depMatch[1].match(/['"]([^'"]+)['"]/g);
        if (deps) {
          dependencies.requires = deps.map(d => d.replace(/['"]/g, ''));
        }
      }
    } catch (e) {
      // Ignore read errors
    }
  }

  return {
    agent: agentName,
    entry_points: entryPoints,
    files_by_category: Object.fromEntries(
      Object.entries(filesByCategory).map(([k, v]) => [k, v.length])
    ),
    files: allFiles.map(e => ({
      path: e.relativePath,
      category: e.category,
    })),
    dependencies: includeDeps ? dependencies : undefined,
    total_files: allFiles.length,
  };
}

async function toolCreate(filePath, content, category = null, tags = []) {
  const fullPath = path.join(PROJECT_ROOT, filePath);

  if (isProtected(fullPath)) {
    throw new Error(`Cannot create protected path: ${filePath}`);
  }

  // Ensure directory exists
  await fs.mkdir(path.dirname(fullPath), { recursive: true });

  // Write file
  await fs.writeFile(fullPath, content, 'utf-8');

  // Add to index
  const stats = await fs.stat(fullPath);
  const entry = new FileEntry(fullPath, stats, content);
  if (category) entry.category = category;
  if (tags.length) entry.tags = [...entry.tags, ...tags];
  fileIndex.set(entry.relativePath, entry);

  log('info', 'File created', { path: filePath });

  return {
    success: true,
    path: filePath,
    indexed_as: {
      category: entry.category,
      agent: entry.agent,
      tags: entry.tags,
    },
  };
}

async function toolRead(filePath) {
  const fullPath = path.join(PROJECT_ROOT, filePath);

  try {
    const content = await fs.readFile(fullPath, 'utf-8');
    const stats = await fs.stat(fullPath);
    const entry = fileIndex.get(filePath) || new FileEntry(fullPath, stats, content);

    return {
      path: filePath,
      content,
      metadata: {
        size: stats.size,
        modified: stats.mtime.toISOString(),
        category: entry.category,
        agent: entry.agent,
        tags: entry.tags,
      },
    };
  } catch (error) {
    throw new Error(`Cannot read file: ${filePath} - ${error.message}`);
  }
}

async function toolUpdate(filePath, content) {
  const fullPath = path.join(PROJECT_ROOT, filePath);

  if (isProtected(fullPath)) {
    throw new Error(`Cannot update protected path: ${filePath}`);
  }

  // Create backup
  const backupPath = fullPath + '.bak';
  try {
    await fs.copyFile(fullPath, backupPath);
  } catch (e) {
    // File might not exist yet
  }

  // Write new content
  await fs.writeFile(fullPath, content, 'utf-8');

  // Update index
  const stats = await fs.stat(fullPath);
  const entry = new FileEntry(fullPath, stats, content);
  fileIndex.set(entry.relativePath, entry);

  log('info', 'File updated', { path: filePath, backup: backupPath });

  return {
    success: true,
    path: filePath,
    backup_path: path.relative(PROJECT_ROOT, backupPath),
  };
}

async function toolDelete(filePath, confirm = false) {
  if (!confirm) {
    return {
      success: false,
      error: 'Deletion requires confirm: true',
      path: filePath,
    };
  }

  const fullPath = path.join(PROJECT_ROOT, filePath);

  if (isProtected(fullPath)) {
    throw new Error(`Cannot delete protected path: ${filePath}`);
  }

  // Create backup
  const backupPath = fullPath + '.deleted.bak';
  await fs.copyFile(fullPath, backupPath);

  // Delete file
  await fs.unlink(fullPath);

  // Remove from index
  fileIndex.delete(filePath);

  log('info', 'File deleted', { path: filePath, backup: backupPath });

  return {
    success: true,
    path: filePath,
    backup_path: path.relative(PROJECT_ROOT, backupPath),
  };
}

async function toolMove(fromPath, toPath) {
  const fullFromPath = path.join(PROJECT_ROOT, fromPath);
  const fullToPath = path.join(PROJECT_ROOT, toPath);

  if (isProtected(fullFromPath) || isProtected(fullToPath)) {
    throw new Error('Cannot move protected paths');
  }

  // Ensure destination directory exists
  await fs.mkdir(path.dirname(fullToPath), { recursive: true });

  // Move file
  await fs.rename(fullFromPath, fullToPath);

  // Update index
  const entry = fileIndex.get(fromPath);
  if (entry) {
    fileIndex.delete(fromPath);
    entry.path = fullToPath;
    entry.relativePath = toPath;
    entry.name = path.basename(toPath);
    fileIndex.set(toPath, entry);
  }

  log('info', 'File moved', { from: fromPath, to: toPath });

  return {
    success: true,
    from: fromPath,
    to: toPath,
  };
}

async function toolRefresh() {
  return await buildIndex();
}

async function toolStats() {
  if (fileIndex.size === 0) {
    await buildIndex();
  }

  const byCategory = {};
  const byAgent = {};

  for (const entry of fileIndex.values()) {
    byCategory[entry.category] = (byCategory[entry.category] || 0) + 1;
    if (entry.agent) {
      byAgent[entry.agent] = (byAgent[entry.agent] || 0) + 1;
    }
  }

  return {
    total_files: fileIndex.size,
    by_category: byCategory,
    by_agent: byAgent,
    index_built_at: indexBuiltAt?.toISOString(),
    project_root: PROJECT_ROOT,
  };
}

async function toolValidatePaths(paths) {
  const valid = [];
  const invalid = [];
  const suggestions = [];

  for (const p of paths) {
    const fullPath = path.join(PROJECT_ROOT, p);
    try {
      await fs.access(fullPath);
      valid.push(p);
    } catch {
      invalid.push(p);

      // Try to find similar paths
      const baseName = path.basename(p);
      for (const entry of fileIndex.values()) {
        if (entry.name === baseName || entry.relativePath.includes(baseName)) {
          suggestions.push({
            original: p,
            suggestion: entry.relativePath,
          });
          break;
        }
      }
    }
  }

  return { valid, invalid, suggestions };
}

async function toolMapDependencies(filePath) {
  const fullPath = path.join(PROJECT_ROOT, filePath);

  try {
    const content = await fs.readFile(fullPath, 'utf-8');
    const references = [];
    const referencedBy = [];

    // Find outgoing references (files this file links to)
    const linkMatches = content.matchAll(/\[.*?\]\(([^)]+\.(?:md|json|py|js))\)/g);
    for (const match of linkMatches) {
      references.push(match[1]);
    }

    const pathMatches = content.matchAll(/"([^"]+\.(?:md|json|py|js))"/g);
    for (const match of pathMatches) {
      if (!match[1].startsWith('http')) {
        references.push(match[1]);
      }
    }

    // Find incoming references (files that link to this file)
    const fileName = path.basename(filePath);
    for (const entry of fileIndex.values()) {
      if (entry.relativePath === filePath) continue;

      try {
        const otherContent = await fs.readFile(
          path.join(PROJECT_ROOT, entry.relativePath),
          'utf-8'
        );
        if (otherContent.includes(fileName) || otherContent.includes(filePath)) {
          referencedBy.push(entry.relativePath);
        }
      } catch {
        // Skip unreadable files
      }
    }

    return {
      file: filePath,
      references: [...new Set(references)],
      referenced_by: referencedBy,
    };
  } catch (error) {
    throw new Error(`Cannot map dependencies for: ${filePath} - ${error.message}`);
  }
}

async function toolRelated(filePath, maxResults = 10) {
  if (fileIndex.size === 0) {
    await buildIndex();
  }

  const entry = fileIndex.get(filePath);
  if (!entry) {
    throw new Error(`File not in index: ${filePath}`);
  }

  const results = [];

  for (const other of fileIndex.values()) {
    if (other.relativePath === filePath) continue;

    let score = 0;
    let relationship = [];

    // Same agent
    if (entry.agent && other.agent === entry.agent) {
      score += 0.4;
      relationship.push('same_agent');
    }

    // Same category
    if (entry.category === other.category) {
      score += 0.2;
      relationship.push('same_category');
    }

    // Same directory
    if (path.dirname(entry.relativePath) === path.dirname(other.relativePath)) {
      score += 0.3;
      relationship.push('same_directory');
    }

    // Shared tags
    const sharedTags = entry.tags.filter(t => other.tags.includes(t));
    if (sharedTags.length > 0) {
      score += 0.1 * Math.min(sharedTags.length, 3);
      relationship.push('shared_tags');
    }

    if (score > 0.2) {
      results.push({
        path: other.relativePath,
        relationship: relationship.join(', '),
        score: Math.round(score * 100) / 100,
      });
    }
  }

  results.sort((a, b) => b.score - a.score);

  return {
    file: filePath,
    related: results.slice(0, maxResults),
    total_found: results.length,
  };
}

// ============================================================================
// MCP SERVER SETUP
// ============================================================================

const server = new Server(
  {
    name: 'scout',
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
        name: 'discover',
        description: 'Find files relevant to a natural language query. Returns paths with relevance scores. v1.2.0: Now includes semantic detection of intent and agent from PT/EN queries.',
        inputSchema: {
          type: 'object',
          properties: {
            query: { type: 'string', description: 'Natural language query (e.g., "criar anúncio de produto", "create product listing")' },
            agent: { type: 'string', description: 'Optional: limit to specific agent (e.g., "anuncio_agent"). If not provided, agent is auto-detected from query.' },
            max_results: { type: 'integer', default: 10, description: 'Maximum results to return' },
          },
          required: ['query'],
        },
      },
      {
        name: 'smart_context',
        description: 'Get intelligent, LLM-optimized context for an agent. Returns prioritized file list with importance tiers (critical/high/medium/low) and recommended reading order. Use this instead of agent_context for efficient navigation.',
        inputSchema: {
          type: 'object',
          properties: {
            agent: { type: 'string', description: 'Agent name (e.g., "anuncio_agent", "pesquisa_agent")' },
            max_files: { type: 'integer', default: 20, description: 'Maximum files in must_read list' },
            include_hints: { type: 'boolean', default: true, description: 'Include LLM navigation hints' },
          },
          required: ['agent'],
        },
      },
      {
        name: 'search',
        description: 'Search files by glob pattern. Returns matching file paths.',
        inputSchema: {
          type: 'object',
          properties: {
            pattern: { type: 'string', description: 'Glob pattern (e.g., "**/*_HOP.md")' },
            type: { type: 'string', description: 'Optional: filter by category (e.g., "hop", "config")' },
          },
          required: ['pattern'],
        },
      },
      {
        name: 'agent_context',
        description: 'Get all files and context for a specific agent. Returns entry points, files by category, and dependencies.',
        inputSchema: {
          type: 'object',
          properties: {
            agent: { type: 'string', description: 'Agent name (e.g., "anuncio_agent", "codexa_agent")' },
            include_deps: { type: 'boolean', default: true, description: 'Include dependency information' },
          },
          required: ['agent'],
        },
      },
      {
        name: 'create',
        description: 'Create a new file with automatic indexing.',
        inputSchema: {
          type: 'object',
          properties: {
            path: { type: 'string', description: 'Relative path from project root' },
            content: { type: 'string', description: 'File content' },
            category: { type: 'string', description: 'Optional: override category' },
            tags: { type: 'array', items: { type: 'string' }, description: 'Optional: additional tags' },
          },
          required: ['path', 'content'],
        },
      },
      {
        name: 'read',
        description: 'Read file content with metadata.',
        inputSchema: {
          type: 'object',
          properties: {
            path: { type: 'string', description: 'Relative path from project root' },
          },
          required: ['path'],
        },
      },
      {
        name: 'update',
        description: 'Update file content. Creates backup automatically.',
        inputSchema: {
          type: 'object',
          properties: {
            path: { type: 'string', description: 'Relative path from project root' },
            content: { type: 'string', description: 'New file content' },
          },
          required: ['path', 'content'],
        },
      },
      {
        name: 'delete',
        description: 'Delete a file. Requires confirm: true for safety.',
        inputSchema: {
          type: 'object',
          properties: {
            path: { type: 'string', description: 'Relative path from project root' },
            confirm: { type: 'boolean', description: 'Must be true to confirm deletion' },
          },
          required: ['path'],
        },
      },
      {
        name: 'move',
        description: 'Move or rename a file.',
        inputSchema: {
          type: 'object',
          properties: {
            from: { type: 'string', description: 'Current path' },
            to: { type: 'string', description: 'New path' },
          },
          required: ['from', 'to'],
        },
      },
      {
        name: 'refresh',
        description: 'Rebuild the file index from scratch.',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
      {
        name: 'stats',
        description: 'Get index statistics: total files, by category, by agent.',
        inputSchema: {
          type: 'object',
          properties: {},
        },
      },
      {
        name: 'validate_paths',
        description: 'Check if paths exist. Returns valid, invalid, and suggestions.',
        inputSchema: {
          type: 'object',
          properties: {
            paths: { type: 'array', items: { type: 'string' }, description: 'Paths to validate' },
          },
          required: ['paths'],
        },
      },
      {
        name: 'map_dependencies',
        description: 'Find files that reference and are referenced by a given file.',
        inputSchema: {
          type: 'object',
          properties: {
            file: { type: 'string', description: 'File path to analyze' },
          },
          required: ['file'],
        },
      },
      {
        name: 'related',
        description: 'Find files related to a given file (same agent, category, directory).',
        inputSchema: {
          type: 'object',
          properties: {
            file: { type: 'string', description: 'File path' },
            max_results: { type: 'integer', default: 10 },
          },
          required: ['file'],
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
      case 'discover':
        result = await toolDiscover(args.query, args.agent, args.max_results || 10, true);
        break;
      case 'smart_context':
        result = await toolSmartContext(args.agent, args.max_files || 20, args.include_hints !== false);
        break;
      case 'search':
        result = await toolSearch(args.pattern, args.type);
        break;
      case 'agent_context':
        result = await toolAgentContext(args.agent, args.include_deps !== false);
        break;
      case 'create':
        result = await toolCreate(args.path, args.content, args.category, args.tags || []);
        break;
      case 'read':
        result = await toolRead(args.path);
        break;
      case 'update':
        result = await toolUpdate(args.path, args.content);
        break;
      case 'delete':
        result = await toolDelete(args.path, args.confirm);
        break;
      case 'move':
        result = await toolMove(args.from, args.to);
        break;
      case 'refresh':
        result = await toolRefresh();
        break;
      case 'stats':
        result = await toolStats();
        break;
      case 'validate_paths':
        result = await toolValidatePaths(args.paths);
        break;
      case 'map_dependencies':
        result = await toolMapDependencies(args.file);
        break;
      case 'related':
        result = await toolRelated(args.file, args.max_results || 10);
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

// Start server
async function main() {
  const cwd = process.cwd();
  const rootSource = process.env.SCOUT_ROOT ? 'env:SCOUT_ROOT' : 'auto-detected';

  log('info', 'Starting Scout MCP Server v1.2.0...', {
    root: PROJECT_ROOT,
    cwd: cwd,
    root_source: rootSource,
  });

  // Warn if cwd differs from PROJECT_ROOT
  if (cwd !== PROJECT_ROOT) {
    log('info', 'Note: Working directory differs from project root', {
      cwd: cwd,
      project_root: PROJECT_ROOT,
    });
  }

  // Load semantic aliases for intelligent query expansion
  await loadSemanticAliases();

  // Build initial index
  await buildIndex();

  const transport = new StdioServerTransport();
  await server.connect(transport);

  log('info', 'Scout MCP Server v1.2.0 running', {
    features: ['semantic_aliases', 'importance_scores', 'smart_context', 'intent_detection']
  });
}

main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
