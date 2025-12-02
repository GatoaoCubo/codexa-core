/**
 * CODEXA Path Resolver (Node.js)
 * Resolves {{PLACEHOLDERS}} to absolute paths at runtime
 *
 * Usage:
 *   const { PathResolver, resolvePath } = require('./pathResolver');
 *
 *   // Quick resolution
 *   const path = resolvePath('{{AGENTES}}/scout_agent/PRIME.md');
 *
 *   // Advanced usage
 *   const resolver = new PathResolver();
 *   const scoutPaths = resolver.getAgentContext('scout_agent');
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');


class PathResolver {
  /**
   * Initialize resolver with path registry
   * @param {string|null} registryPath - Path to path_registry.json
   */
  constructor(registryPath = null) {
    this.platform = os.platform(); // win32, linux, darwin
    this._rootCache = {};
    this._projectRoot = this._detectProjectRoot();
    this.registry = this._loadRegistry(registryPath);
  }

  /**
   * Detect PROJECT_ROOT - the codexa.gato directory containing codexa.app
   * @returns {string} Absolute path to project root
   */
  _detectProjectRoot() {
    // Walk up from this file looking for codexa.gato
    let current = __dirname;
    while (current !== path.dirname(current)) {
      // The real project root has codexa.app as DIRECT child
      const hasCodexaApp = fs.existsSync(path.join(current, 'codexa.app'));
      const notCodexaAppItself = path.basename(current) !== 'codexa.app';

      if (hasCodexaApp && notCodexaAppItself) {
        // Verify this is codexa.gato by checking for path_registry.json or CLAUDE.md
        if (fs.existsSync(path.join(current, 'path_registry.json')) ||
            fs.existsSync(path.join(current, 'CLAUDE.md'))) {
          return current;
        }
        // Also check if parent name suggests it's the right one
        const name = path.basename(current).toLowerCase();
        if (name.includes('codexa') || name.includes('gato')) {
          return current;
        }
      }
      current = path.dirname(current);
    }

    // Try git root but validate it's the right level
    try {
      const gitRoot = execSync('git rev-parse --show-toplevel', {
        cwd: __dirname,
        encoding: 'utf-8',
        stdio: ['pipe', 'pipe', 'pipe']
      }).trim();

      // Check if codexa.gato is inside git_root
      const entries = fs.readdirSync(gitRoot, { withFileTypes: true });
      for (const entry of entries) {
        if (entry.isDirectory()) {
          const childPath = path.join(gitRoot, entry.name);
          if (fs.existsSync(path.join(childPath, 'codexa.app'))) {
            if (fs.existsSync(path.join(childPath, 'path_registry.json')) ||
                fs.existsSync(path.join(childPath, 'CLAUDE.md'))) {
              return childPath;
            }
          }
        }
      }

      // Or if git_root itself is the project
      if (fs.existsSync(path.join(gitRoot, 'codexa.app')) &&
          fs.existsSync(path.join(gitRoot, 'path_registry.json'))) {
        return gitRoot;
      }
    } catch (e) {
      // Git not available or not in a repo
    }

    // Last resort: environment variable
    const envRoot = process.env.PROJECT_ROOT || process.env.CODEXA_ROOT;
    if (envRoot) {
      return envRoot;
    }

    throw new Error(
      'Could not detect PROJECT_ROOT. ' +
      'Ensure you\'re in codexa.gato with codexa.app/ or set PROJECT_ROOT env var.'
    );
  }

  /**
   * Load path registry from JSON file
   * @param {string|null} registryPath
   * @returns {object}
   */
  _loadRegistry(registryPath) {
    if (!registryPath) {
      registryPath = path.join(this._projectRoot, 'path_registry.json');
    }

    if (!fs.existsSync(registryPath)) {
      return this._getDefaultRegistry();
    }

    const content = fs.readFileSync(registryPath, 'utf-8');
    return JSON.parse(content);
  }

  /**
   * Return default registry when file doesn't exist
   * @returns {object}
   */
  _getDefaultRegistry() {
    return {
      root_anchors: {
        PROJECT_ROOT: { detection_strategy: 'git_root' },
        CODEXA_APP: { relative_to: 'PROJECT_ROOT', path: 'codexa.app' },
        AGENTES: { relative_to: 'CODEXA_APP', path: 'agentes' },
        MCP_SERVERS: { relative_to: 'CODEXA_APP', path: 'mcp-servers' },
        CLAUDE_DIR: { relative_to: 'PROJECT_ROOT', path: '.claude' }
      },
      standard_placeholders: {
        system_level: {
          '{{PROJECT_ROOT}}': { resolves_to: 'root_anchors.PROJECT_ROOT' },
          '{{CODEXA_APP}}': { resolves_to: 'root_anchors.CODEXA_APP' },
          '{{AGENTES}}': { resolves_to: 'root_anchors.AGENTES' },
          '{{MCP_SERVERS}}': { resolves_to: 'root_anchors.MCP_SERVERS' },
          '{{CLAUDE_DIR}}': { resolves_to: 'root_anchors.CLAUDE_DIR' }
        }
      },
      agent_paths: {}
    };
  }

  /**
   * Resolve a root anchor like PROJECT_ROOT
   * @param {string} anchorName
   * @returns {string}
   */
  _resolveRootAnchor(anchorName) {
    if (this._rootCache[anchorName]) {
      return this._rootCache[anchorName];
    }

    if (anchorName === 'PROJECT_ROOT') {
      this._rootCache[anchorName] = this._projectRoot;
      return this._projectRoot;
    }

    const anchorSpec = this.registry.root_anchors?.[anchorName];
    if (!anchorSpec) {
      throw new Error(`Unknown root anchor: ${anchorName}`);
    }

    let resolved;

    // Handle relative anchors
    const relativeTo = anchorSpec.relative_to;
    if (relativeTo) {
      const parent = this._resolveRootAnchor(relativeTo);
      resolved = path.join(parent, anchorSpec.path || '');
    } else {
      // Handle detection strategies
      const strategy = anchorSpec.detection_strategy;
      if (strategy === 'git_root') {
        resolved = this._projectRoot;
      } else if (strategy === 'env') {
        const envVar = (anchorSpec.fallback || '').replace('env:', '');
        const envValue = process.env[envVar];
        if (!envValue) {
          throw new Error(`Environment variable not set: ${envVar}`);
        }
        resolved = envValue;
      } else {
        throw new Error(`Cannot resolve anchor: ${anchorName}`);
      }
    }

    this._rootCache[anchorName] = resolved;
    return resolved;
  }

  /**
   * Resolve a placeholder to an absolute path
   * @param {string} placeholder - String like "{{PROJECT_ROOT}}/codexa.app"
   * @param {object|null} context - Optional context for dynamic placeholders
   * @returns {string} Resolved absolute path
   */
  resolve(placeholder, context = null) {
    if (!placeholder) {
      throw new Error('Empty placeholder');
    }

    // If it's already an absolute path, return it
    if (path.isAbsolute(placeholder)) {
      return placeholder;
    }

    // Extract placeholders from string
    const placeholderRegex = /\{\{([A-Z_]+)\}\}/g;
    let result = placeholder;
    let match;

    // Reset regex state
    placeholderRegex.lastIndex = 0;

    while ((match = placeholderRegex.exec(placeholder)) !== null) {
      const ph = match[1];
      const fullPlaceholder = match[0];

      let resolvedValue;

      // Check context first
      if (context && context[ph]) {
        resolvedValue = context[ph];
      }
      // Check if it's a known root anchor
      else if (this.registry.root_anchors?.[ph]) {
        resolvedValue = this._resolveRootAnchor(ph);
      }
      // Check standard placeholders mapping
      else if (this.registry.standard_placeholders?.system_level?.[fullPlaceholder]) {
        const spec = this.registry.standard_placeholders.system_level[fullPlaceholder];
        const anchorRef = spec.resolves_to || '';
        if (anchorRef.startsWith('root_anchors.')) {
          const anchorName = anchorRef.split('.')[1];
          resolvedValue = this._resolveRootAnchor(anchorName);
        } else {
          resolvedValue = this.resolve(anchorRef, context);
        }
      } else {
        throw new Error(`Unknown placeholder: ${fullPlaceholder}`);
      }

      result = result.replace(fullPlaceholder, resolvedValue);
    }

    // Normalize to absolute path
    return path.resolve(result);
  }

  /**
   * Resolve an agent-specific path
   * @param {string} agentName - Agent name (e.g., "scout_agent")
   * @param {string} pathKey - Path key (e.g., "prime")
   * @returns {string} Resolved absolute path
   */
  resolveAgentPath(agentName, pathKey) {
    const agentPaths = this.registry.agent_paths?.[agentName];
    if (!agentPaths) {
      // Fallback to default pattern
      return this.resolve(`{{AGENTES}}/${agentName}/${pathKey}`);
    }

    const pathTemplate = agentPaths[pathKey];
    if (!pathTemplate) {
      throw new Error(`Unknown path key '${pathKey}' for agent '${agentName}'`);
    }

    return this.resolve(pathTemplate);
  }

  /**
   * Get all resolved paths for an agent
   * @param {string} agentName - Agent name
   * @returns {object} Dictionary of path_key -> resolved path
   */
  getAgentContext(agentName) {
    const agentPaths = this.registry.agent_paths?.[agentName] || {};
    const result = {};

    for (const [key, value] of Object.entries(agentPaths)) {
      result[key] = this.resolve(value);
    }

    return result;
  }

  /**
   * Validate that all registered paths exist
   * @returns {object} Dictionary of path -> exists status
   */
  validateAllPaths() {
    const results = {};

    // Validate root anchors
    for (const anchorName of Object.keys(this.registry.root_anchors || {})) {
      try {
        const resolvedPath = this._resolveRootAnchor(anchorName);
        results[anchorName] = fs.existsSync(resolvedPath);
      } catch (e) {
        results[anchorName] = false;
      }
    }

    // Validate agent paths
    for (const agentName of Object.keys(this.registry.agent_paths || {})) {
      try {
        const context = this.getAgentContext(agentName);
        for (const [key, resolvedPath] of Object.entries(context)) {
          results[`${agentName}.${key}`] = fs.existsSync(resolvedPath);
        }
      } catch (e) {
        results[agentName] = false;
      }
    }

    return results;
  }

  /**
   * Get the detected project root
   * @returns {string}
   */
  get projectRoot() {
    return this._projectRoot;
  }

  /**
   * Get the codexa.app directory
   * @returns {string}
   */
  get codexaApp() {
    return this._resolveRootAnchor('CODEXA_APP');
  }

  /**
   * Get the agentes directory
   * @returns {string}
   */
  get agentes() {
    return this._resolveRootAnchor('AGENTES');
  }
}


// Global resolver instance (lazy-loaded)
let _resolver = null;

/**
 * Get or create global PathResolver instance
 * @returns {PathResolver}
 */
function getResolver() {
  if (!_resolver) {
    _resolver = new PathResolver();
  }
  return _resolver;
}

/**
 * Quick path resolution without instantiating PathResolver
 * @param {string} placeholder
 * @param {object|null} context
 * @returns {string}
 */
function resolvePath(placeholder, context = null) {
  return getResolver().resolve(placeholder, context);
}

/**
 * Get project root path
 * @returns {string}
 */
function getProjectRoot() {
  return getResolver().projectRoot;
}

/**
 * Get directory for a specific agent
 * @param {string} agentName
 * @returns {string}
 */
function getAgentDir(agentName) {
  return getResolver().resolve(`{{AGENTES}}/${agentName}`);
}


// Export
module.exports = {
  PathResolver,
  resolvePath,
  getResolver,
  getProjectRoot,
  getAgentDir
};


// ============================================================
// CLI Interface
// ============================================================

if (require.main === module) {
  const resolver = new PathResolver();

  console.log('='.repeat(60));
  console.log('CODEXA Path Resolver (Node.js)');
  console.log('='.repeat(60));
  console.log(`Platform: ${resolver.platform}`);
  console.log(`PROJECT_ROOT: ${resolver.projectRoot}`);
  console.log(`CODEXA_APP:   ${resolver.codexaApp}`);
  console.log(`AGENTES:      ${resolver.agentes}`);
  console.log();

  // Test some resolutions
  const testPaths = [
    '{{PROJECT_ROOT}}/CLAUDE.md',
    '{{AGENTES}}/scout_agent/PRIME.md',
    '{{MCP_SERVERS}}/scout-mcp/index.js',
    '{{CLAUDE_DIR}}/commands',
  ];

  console.log('Test Resolutions:');
  console.log('-'.repeat(60));
  for (const test of testPaths) {
    try {
      const resolved = resolver.resolve(test);
      const exists = fs.existsSync(resolved) ? '[OK]' : '[MISSING]';
      console.log(`${exists} ${test}`);
      console.log(`      → ${resolved}`);
    } catch (e) {
      console.log(`[ERROR] ${test}`);
      console.log(`      → ${e.message}`);
    }
  }
  console.log();

  // Validate all paths
  console.log('Path Validation:');
  console.log('-'.repeat(60));
  const validation = resolver.validateAllPaths();
  let passed = 0;
  let failed = 0;

  for (const [pathKey, exists] of Object.entries(validation)) {
    const status = exists ? '[OK]' : '[MISSING]';
    console.log(`  ${status} ${pathKey}`);
    if (exists) passed++;
    else failed++;
  }

  console.log();
  console.log(`Results: ${passed} passed, ${failed} failed`);

  // Exit with error code if any failures
  process.exit(failed === 0 ? 0 : 1);
}
