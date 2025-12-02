# PATH REGISTRY SYSTEM SPECIFICATION

**Version**: 1.0.0
**Created**: 2025-12-02
**Type**: System Architecture Specification
**Status**: Design Phase

---

## EXECUTIVE SUMMARY

A centralized path management system for the CODEXA project that eliminates hardcoded paths, enables cross-platform compatibility (Windows/Unix), and provides dynamic path resolution across all agents, configurations, and documentation.

**Problem**: Hardcoded absolute paths break portability, fail across platforms, and require manual updates when project structure changes.

**Solution**: Single source of truth (path registry) + placeholder system + runtime resolution + sync mechanisms.

---

## 1. ARCHITECTURE OVERVIEW

```
┌─────────────────────────────────────────────────────────────────┐
│                    PATH REGISTRY SYSTEM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────┐     ┌──────────────────┐                │
│  │  path_registry   │────▶│  Resolution      │                │
│  │  .json           │     │  Engine          │                │
│  │                  │     │  (runtime)       │                │
│  │  Single Source   │     │                  │                │
│  │  of Truth        │     │  Python/Node/    │                │
│  └──────────────────┘     │  Claude Code     │                │
│                           └──────────────────┘                │
│                                  │                             │
│                                  ▼                             │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              CONSUMPTION LAYERS                         │  │
│  ├─────────────────────────────────────────────────────────┤  │
│  │  1. Python Modules    (curso_agent/config/paths.py)    │  │
│  │  2. MCP Configs       (.mcp.json, settings.json)       │  │
│  │  3. Documentation     (*.md with {{PLACEHOLDERS}})     │  │
│  │  4. Agent Registry    (51_AGENT_REGISTRY.json)         │  │
│  │  5. Builder Scripts   (codexa_agent/builders/*.py)     │  │
│  │  6. Git Hooks         (validate on commit)             │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Three-Layer Strategy

1. **Storage Layer**: `path_registry.json` (single source of truth)
2. **Resolution Layer**: Runtime path resolver (Python/Node/Bash)
3. **Consumption Layer**: Templates, configs, docs use placeholders

---

## 2. PATH REGISTRY SCHEMA

### 2.1 Registry File Location

```
PROJECT_ROOT/
├── path_registry.json          ← Global registry (entire project)
└── codexa.app/
    ├── agentes/
    │   ├── path_registry.json  ← Agent-level registry (optional)
    │   └── scout_agent/
    │       └── config/
    │           └── paths.json  ← Agent-specific paths
    └── ...
```

**Priority**: `agent-specific > agent-level > global`

### 2.2 JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "CODEXA Path Registry",
  "version": "1.0.0",
  "description": "Central registry for all dynamic paths in CODEXA project",

  "metadata": {
    "created": "2025-12-02T00:00:00Z",
    "last_updated": "2025-12-02T00:00:00Z",
    "schema_version": "1.0.0",
    "platform": "auto-detect",
    "git_root_strategy": "auto-detect"
  },

  "root_anchors": {
    "PROJECT_ROOT": {
      "description": "Absolute root of entire project (git root)",
      "detection_strategy": "git_root",
      "fallback": "env:PROJECT_ROOT",
      "windows_example": "C:\\Users\\Dell\\Documents\\GitHub\\connect-my-github\\codexa.gato",
      "unix_example": "/home/user/projects/codexa.gato",
      "validation": "must_contain: [.git, codexa.app]"
    },
    "CODEXA_APP": {
      "description": "Main application directory",
      "relative_to": "PROJECT_ROOT",
      "path": "codexa.app",
      "validation": "must_contain: [agentes, mcp-servers, voice]"
    },
    "AGENTES": {
      "description": "All agents directory",
      "relative_to": "CODEXA_APP",
      "path": "agentes",
      "validation": "must_contain: [51_AGENT_REGISTRY.json]"
    }
  },

  "standard_placeholders": {
    "system_level": {
      "{{PROJECT_ROOT}}": {
        "resolves_to": "root_anchors.PROJECT_ROOT",
        "usage": "Absolute root - use sparingly",
        "example": "{{PROJECT_ROOT}}/codexa.app/agentes"
      },
      "{{CODEXA_APP}}": {
        "resolves_to": "root_anchors.CODEXA_APP",
        "usage": "Main application paths",
        "example": "{{CODEXA_APP}}/agentes/scout_agent"
      },
      "{{AGENTES}}": {
        "resolves_to": "root_anchors.AGENTES",
        "usage": "Agent directories",
        "example": "{{AGENTES}}/codexa_agent"
      },
      "{{MCP_SERVERS}}": {
        "resolves_to": "{{CODEXA_APP}}/mcp-servers",
        "usage": "MCP server implementations",
        "example": "{{MCP_SERVERS}}/scout-mcp"
      },
      "{{CLAUDE_DIR}}": {
        "resolves_to": "{{PROJECT_ROOT}}/.claude",
        "usage": "Claude Code configuration",
        "example": "{{CLAUDE_DIR}}/commands/prime.md"
      }
    },
    "agent_level": {
      "{{AGENT_DIR}}": {
        "resolves_to": "context-dependent",
        "usage": "Current agent directory (dynamic)",
        "example": "{{AGENT_DIR}}/config/paths.json"
      },
      "{{AGENT_CONFIG}}": {
        "resolves_to": "{{AGENT_DIR}}/config",
        "usage": "Agent configuration files",
        "example": "{{AGENT_CONFIG}}/categories.json"
      },
      "{{AGENT_ISO}}": {
        "resolves_to": "{{AGENT_DIR}}/iso_vectorstore",
        "usage": "Agent knowledge base",
        "example": "{{AGENT_ISO}}/04_README.md"
      },
      "{{AGENT_WORKFLOWS}}": {
        "resolves_to": "{{AGENT_DIR}}/workflows",
        "usage": "Agent ADW workflows",
        "example": "{{AGENT_WORKFLOWS}}/100_ADW_DISCOVERY.md"
      },
      "{{AGENT_PROMPTS}}": {
        "resolves_to": "{{AGENT_DIR}}/prompts",
        "usage": "Agent HOP prompts",
        "example": "{{AGENT_PROMPTS}}/10_scene_planner_HOP.md"
      }
    },
    "cross_platform": {
      "path_separator": {
        "windows": "\\",
        "unix": "/",
        "resolution": "os.path.sep (Python) | path.sep (Node)"
      },
      "line_endings": {
        "windows": "CRLF",
        "unix": "LF",
        "resolution": "git config core.autocrlf"
      }
    }
  },

  "agent_paths": {
    "scout_agent": {
      "prime": "{{AGENTES}}/scout_agent/PRIME.md",
      "config": "{{AGENTES}}/scout_agent/config",
      "mcp_server": "{{MCP_SERVERS}}/scout-mcp/index.js",
      "categories": "{{AGENTES}}/scout_agent/config/categories.json",
      "relevance_weights": "{{AGENTES}}/scout_agent/config/relevance_weights.json"
    },
    "codexa_agent": {
      "prime": "{{AGENTES}}/codexa_agent/PRIME.md",
      "builders": "{{AGENTES}}/codexa_agent/builders",
      "validators": "{{AGENTES}}/codexa_agent/validators",
      "workflows": "{{AGENTES}}/codexa_agent/workflows",
      "prompts": "{{AGENTES}}/codexa_agent/prompts"
    },
    "mentor_agent": {
      "prime": "{{AGENTES}}/mentor_agent/PRIME.md",
      "fontes": "{{AGENTES}}/mentor_agent/FONTES",
      "knowledge_graph": "{{AGENTES}}/mentor_agent/FONTES/knowledge_graph.json",
      "embedding_pipeline": "{{AGENTES}}/mentor_agent/scripts/embedding_pipeline.py"
    }
  },

  "common_paths": {
    "registry": "{{AGENTES}}/51_AGENT_REGISTRY.json",
    "claude_md": "{{PROJECT_ROOT}}/CLAUDE.md",
    "scout_integration": "{{AGENTES}}/SCOUT_INTEGRATION.md",
    "supabase_config": "{{PROJECT_ROOT}}/supabase/config.toml"
  },

  "output_paths": {
    "agent_outputs": "{{AGENT_DIR}}/outputs",
    "artifacts": "{{AGENT_DIR}}/artifacts",
    "logs": "{{PROJECT_ROOT}}/logs",
    "cache": "{{PROJECT_ROOT}}/.cache"
  }
}
```

---

## 3. RESOLUTION STRATEGY

### 3.1 Python Resolution Module

**File**: `codexa.app/core/path_resolver.py`

```python
"""
CODEXA Path Resolver
Resolves {{PLACEHOLDERS}} to absolute paths at runtime
"""

import json
import os
from pathlib import Path
from typing import Dict, Optional, Any
import platform


class PathResolver:
    """
    Central path resolution engine for CODEXA project.

    Resolves placeholder syntax like {{PROJECT_ROOT}} to actual paths.
    Cross-platform compatible (Windows/Unix).
    """

    def __init__(self, registry_path: Optional[Path] = None):
        """
        Initialize resolver with path registry.

        Args:
            registry_path: Path to path_registry.json (auto-detects if None)
        """
        self.platform = platform.system()  # Windows, Linux, Darwin
        self.registry = self._load_registry(registry_path)
        self._root_cache: Dict[str, Path] = {}

    def _load_registry(self, registry_path: Optional[Path]) -> Dict[str, Any]:
        """Load path registry from JSON file."""
        if registry_path is None:
            registry_path = self._find_registry()

        if not registry_path.exists():
            raise FileNotFoundError(f"Path registry not found: {registry_path}")

        with open(registry_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _find_registry(self) -> Path:
        """Auto-detect path_registry.json location."""
        # Start from current file, walk up to git root
        current = Path(__file__).resolve()

        for parent in [current] + list(current.parents):
            registry = parent / "path_registry.json"
            if registry.exists():
                return registry

            # Check for git root
            if (parent / ".git").exists():
                return parent / "path_registry.json"

        raise FileNotFoundError("Could not locate path_registry.json")

    def _detect_project_root(self) -> Path:
        """Detect PROJECT_ROOT using git root strategy."""
        current = Path(__file__).resolve()

        for parent in [current] + list(current.parents):
            if (parent / ".git").exists():
                # Validate it's the correct root
                if (parent / "codexa.app").exists():
                    return parent

        raise RuntimeError("Could not detect PROJECT_ROOT (no .git + codexa.app)")

    def _resolve_root_anchor(self, anchor_name: str) -> Path:
        """Resolve a root anchor like PROJECT_ROOT."""
        if anchor_name in self._root_cache:
            return self._root_cache[anchor_name]

        anchor_spec = self.registry["root_anchors"].get(anchor_name)
        if not anchor_spec:
            raise KeyError(f"Unknown root anchor: {anchor_name}")

        # Handle detection strategies
        strategy = anchor_spec.get("detection_strategy")

        if strategy == "git_root":
            resolved = self._detect_project_root()
        elif strategy == "env":
            env_var = anchor_spec.get("fallback", "").split(":")[1]
            env_value = os.getenv(env_var)
            if not env_value:
                raise EnvironmentError(f"Environment variable not set: {env_var}")
            resolved = Path(env_value)
        else:
            # Relative to another anchor
            relative_to = anchor_spec.get("relative_to")
            if relative_to:
                parent = self._resolve_root_anchor(relative_to)
                resolved = parent / anchor_spec["path"]
            else:
                raise ValueError(f"Cannot resolve anchor: {anchor_name}")

        # Validate
        validation = anchor_spec.get("validation", "")
        if "must_contain:" in validation:
            required = validation.split("[")[1].split("]")[0].split(", ")
            for item in required:
                if not (resolved / item.strip()).exists():
                    raise ValueError(f"Validation failed for {anchor_name}: missing {item}")

        self._root_cache[anchor_name] = resolved
        return resolved

    def resolve(self, placeholder: str, context: Optional[Dict[str, str]] = None) -> Path:
        """
        Resolve a placeholder to an absolute path.

        Args:
            placeholder: String like "{{PROJECT_ROOT}}/codexa.app"
            context: Optional context (e.g., {"AGENT_DIR": "scout_agent"})

        Returns:
            Resolved absolute Path object

        Example:
            >>> resolver = PathResolver()
            >>> resolver.resolve("{{AGENTES}}/scout_agent/PRIME.md")
            WindowsPath('C:/Users/Dell/.../codexa.app/agentes/scout_agent/PRIME.md')
        """
        if not placeholder:
            raise ValueError("Empty placeholder")

        # Extract placeholders from string (supports multiple)
        import re
        placeholders = re.findall(r'\{\{([A-Z_]+)\}\}', placeholder)

        result = placeholder
        for ph in placeholders:
            full_placeholder = f"{{{{{ph}}}}}"

            # Check context first (for agent-level placeholders)
            if context and ph in context:
                resolved_value = context[ph]
            # Check standard placeholders
            elif ph in self.registry.get("standard_placeholders", {}).get("system_level", {}):
                spec = self.registry["standard_placeholders"]["system_level"][full_placeholder]
                anchor_name = spec["resolves_to"].split(".")[1]  # e.g., "root_anchors.PROJECT_ROOT"
                resolved_value = str(self._resolve_root_anchor(anchor_name))
            else:
                raise KeyError(f"Unknown placeholder: {full_placeholder}")

            result = result.replace(full_placeholder, resolved_value)

        # Convert to Path and resolve to absolute
        return Path(result).resolve()

    def resolve_agent_path(self, agent_name: str, path_key: str) -> Path:
        """
        Resolve an agent-specific path.

        Args:
            agent_name: Agent name (e.g., "scout_agent")
            path_key: Path key (e.g., "prime", "config")

        Returns:
            Resolved absolute Path

        Example:
            >>> resolver.resolve_agent_path("scout_agent", "prime")
            Path('.../codexa.app/agentes/scout_agent/PRIME.md')
        """
        agent_paths = self.registry.get("agent_paths", {}).get(agent_name)
        if not agent_paths:
            raise KeyError(f"Unknown agent: {agent_name}")

        path_template = agent_paths.get(path_key)
        if not path_template:
            raise KeyError(f"Unknown path key '{path_key}' for agent '{agent_name}'")

        return self.resolve(path_template)

    def get_agent_context(self, agent_name: str) -> Dict[str, Path]:
        """
        Get all resolved paths for an agent.

        Args:
            agent_name: Agent name

        Returns:
            Dictionary of path_key -> resolved Path
        """
        agent_paths = self.registry.get("agent_paths", {}).get(agent_name, {})
        return {key: self.resolve(value) for key, value in agent_paths.items()}

    def validate_all_paths(self) -> Dict[str, bool]:
        """
        Validate that all registered paths exist.

        Returns:
            Dictionary of path -> exists status
        """
        results = {}

        # Validate root anchors
        for anchor_name in self.registry.get("root_anchors", {}):
            try:
                path = self._resolve_root_anchor(anchor_name)
                results[anchor_name] = path.exists()
            except Exception as e:
                results[anchor_name] = False

        # Validate agent paths
        for agent_name in self.registry.get("agent_paths", {}):
            try:
                context = self.get_agent_context(agent_name)
                for key, path in context.items():
                    results[f"{agent_name}.{key}"] = path.exists()
            except Exception as e:
                results[agent_name] = False

        return results


# Convenience function for one-off resolutions
def resolve_path(placeholder: str, context: Optional[Dict[str, str]] = None) -> Path:
    """
    Quick path resolution without instantiating PathResolver.

    Example:
        >>> from codexa.core.path_resolver import resolve_path
        >>> resolve_path("{{AGENTES}}/scout_agent/PRIME.md")
    """
    resolver = PathResolver()
    return resolver.resolve(placeholder, context)


if __name__ == "__main__":
    # Test resolution
    resolver = PathResolver()

    print("=== CODEXA Path Resolver Test ===")
    print(f"Platform: {resolver.platform}")
    print(f"PROJECT_ROOT: {resolver._resolve_root_anchor('PROJECT_ROOT')}")
    print(f"CODEXA_APP: {resolver._resolve_root_anchor('CODEXA_APP')}")
    print(f"AGENTES: {resolver._resolve_root_anchor('AGENTES')}")
    print()

    # Test agent path resolution
    print("Scout Agent Paths:")
    for key, path in resolver.get_agent_context("scout_agent").items():
        print(f"  {key}: {path}")
    print()

    # Validate all paths
    print("Validation Results:")
    validation = resolver.validate_all_paths()
    for path_key, exists in validation.items():
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status} {path_key}")
```

### 3.2 Node.js Resolution Module

**File**: `codexa.app/core/pathResolver.js`

```javascript
/**
 * CODEXA Path Resolver (Node.js)
 * Resolves {{PLACEHOLDERS}} to absolute paths at runtime
 */

const fs = require('fs');
const path = require('path');
const os = require('os');


class PathResolver {
  /**
   * Initialize resolver with path registry
   * @param {string|null} registryPath - Path to path_registry.json
   */
  constructor(registryPath = null) {
    this.platform = os.platform(); // win32, linux, darwin
    this.registry = this._loadRegistry(registryPath);
    this._rootCache = {};
  }

  _loadRegistry(registryPath) {
    if (!registryPath) {
      registryPath = this._findRegistry();
    }

    if (!fs.existsSync(registryPath)) {
      throw new Error(`Path registry not found: ${registryPath}`);
    }

    const content = fs.readFileSync(registryPath, 'utf-8');
    return JSON.parse(content);
  }

  _findRegistry() {
    // Start from current file, walk up to git root
    let current = path.dirname(__filename);

    while (current !== path.dirname(current)) {
      const registryPath = path.join(current, 'path_registry.json');
      if (fs.existsSync(registryPath)) {
        return registryPath;
      }

      // Check for git root
      if (fs.existsSync(path.join(current, '.git'))) {
        return path.join(current, 'path_registry.json');
      }

      current = path.dirname(current);
    }

    throw new Error('Could not locate path_registry.json');
  }

  _detectProjectRoot() {
    let current = path.dirname(__filename);

    while (current !== path.dirname(current)) {
      if (fs.existsSync(path.join(current, '.git'))) {
        // Validate it's the correct root
        if (fs.existsSync(path.join(current, 'codexa.app'))) {
          return current;
        }
      }
      current = path.dirname(current);
    }

    throw new Error('Could not detect PROJECT_ROOT (no .git + codexa.app)');
  }

  _resolveRootAnchor(anchorName) {
    if (this._rootCache[anchorName]) {
      return this._rootCache[anchorName];
    }

    const anchorSpec = this.registry.root_anchors[anchorName];
    if (!anchorSpec) {
      throw new Error(`Unknown root anchor: ${anchorName}`);
    }

    let resolved;

    // Handle detection strategies
    const strategy = anchorSpec.detection_strategy;

    if (strategy === 'git_root') {
      resolved = this._detectProjectRoot();
    } else if (strategy === 'env') {
      const envVar = anchorSpec.fallback.split(':')[1];
      const envValue = process.env[envVar];
      if (!envValue) {
        throw new Error(`Environment variable not set: ${envVar}`);
      }
      resolved = envValue;
    } else {
      // Relative to another anchor
      const relativeTo = anchorSpec.relative_to;
      if (relativeTo) {
        const parent = this._resolveRootAnchor(relativeTo);
        resolved = path.join(parent, anchorSpec.path);
      } else {
        throw new Error(`Cannot resolve anchor: ${anchorName}`);
      }
    }

    // Validate
    const validation = anchorSpec.validation || '';
    if (validation.includes('must_contain:')) {
      const required = validation.match(/\[(.*?)\]/)[1].split(', ');
      for (const item of required) {
        if (!fs.existsSync(path.join(resolved, item.trim()))) {
          throw new Error(`Validation failed for ${anchorName}: missing ${item}`);
        }
      }
    }

    this._rootCache[anchorName] = resolved;
    return resolved;
  }

  /**
   * Resolve a placeholder to an absolute path
   * @param {string} placeholder - String like "{{PROJECT_ROOT}}/codexa.app"
   * @param {object|null} context - Optional context
   * @returns {string} Resolved absolute path
   */
  resolve(placeholder, context = null) {
    if (!placeholder) {
      throw new Error('Empty placeholder');
    }

    // Extract placeholders from string
    const placeholderRegex = /\{\{([A-Z_]+)\}\}/g;
    let result = placeholder;
    let match;

    while ((match = placeholderRegex.exec(placeholder)) !== null) {
      const ph = match[1];
      const fullPlaceholder = match[0];

      let resolvedValue;

      // Check context first
      if (context && context[ph]) {
        resolvedValue = context[ph];
      }
      // Check standard placeholders
      else if (
        this.registry.standard_placeholders?.system_level?.[fullPlaceholder]
      ) {
        const spec = this.registry.standard_placeholders.system_level[fullPlaceholder];
        const anchorName = spec.resolves_to.split('.')[1];
        resolvedValue = this._resolveRootAnchor(anchorName);
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
      throw new Error(`Unknown agent: ${agentName}`);
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
}


// Convenience function for one-off resolutions
function resolvePath(placeholder, context = null) {
  const resolver = new PathResolver();
  return resolver.resolve(placeholder, context);
}


// Export
module.exports = { PathResolver, resolvePath };


// Test if run directly
if (require.main === module) {
  const resolver = new PathResolver();

  console.log('=== CODEXA Path Resolver Test ===');
  console.log(`Platform: ${resolver.platform}`);
  console.log(`PROJECT_ROOT: ${resolver._resolveRootAnchor('PROJECT_ROOT')}`);
  console.log(`CODEXA_APP: ${resolver._resolveRootAnchor('CODEXA_APP')}`);
  console.log(`AGENTES: ${resolver._resolveRootAnchor('AGENTES')}`);
  console.log();

  // Test agent path resolution
  console.log('Scout Agent Paths:');
  const scoutPaths = resolver.getAgentContext('scout_agent');
  for (const [key, value] of Object.entries(scoutPaths)) {
    console.log(`  ${key}: ${value}`);
  }
  console.log();

  // Validate all paths
  console.log('Validation Results:');
  const validation = resolver.validateAllPaths();
  for (const [pathKey, exists] of Object.entries(validation)) {
    const status = exists ? '[OK]' : '[MISSING]';
    console.log(`  ${status} ${pathKey}`);
  }
}
```

### 3.3 Resolution in Documentation

**Rule**: Documentation files (*.md) MUST use placeholders, NOT resolved paths.

**Why**: Human-readable, portable across machines, self-documenting.

**Example**:
```markdown
<!-- GOOD -->
Load agent context from: {{AGENTES}}/scout_agent/PRIME.md

<!-- BAD -->
Load agent context from: C:\Users\Dell\...\scout_agent\PRIME.md
```

---

## 4. INTEGRATION WITH EXISTING SYSTEMS

### 4.1 Integration with `curso_agent/config/paths.py`

**Current State**: Hardcoded relative path detection from `__file__`.

**Migration**:

```python
# OLD (paths.py)
CURSO_AGENT_DIR = Path(__file__).parent.parent
AGENTS_ROOT = CURSO_AGENT_DIR.parent
CODEXA_APP = AGENTS_ROOT.parent
PROJECT_ROOT = CODEXA_APP.parent

# NEW (paths.py with resolver)
from codexa.core.path_resolver import PathResolver

resolver = PathResolver()
CURSO_AGENT_DIR = resolver.resolve_agent_path("curso_agent", "base")
AGENTS_ROOT = resolver.resolve("{{AGENTES}}")
CODEXA_APP = resolver.resolve("{{CODEXA_APP}}")
PROJECT_ROOT = resolver.resolve("{{PROJECT_ROOT}}")
```

**Benefit**: Single source of truth, no hardcoded traversal logic.

### 4.2 Integration with MCP Configs

**Current State**: No `.mcp.json` found (not yet created).

**Proposed `.mcp.json`**:

```json
{
  "mcpServers": {
    "scout": {
      "command": "node",
      "args": [
        "${env:PROJECT_ROOT}/codexa.app/mcp-servers/scout-mcp/index.js"
      ],
      "env": {
        "PROJECT_ROOT": "${workspaceFolder}/../..",
        "CODEXA_APP": "${workspaceFolder}",
        "AGENTES": "${workspaceFolder}/agentes"
      }
    }
  }
}
```

**Resolution Strategy**: Use environment variables for MCP configs (since they don't support custom resolution).

### 4.3 Integration with `.claude/settings.json`

**Proposed Structure**:

```json
{
  "paths": {
    "project_root": "${workspaceFolder}/../..",
    "codexa_app": "${workspaceFolder}",
    "agentes": "${workspaceFolder}/agentes",
    "mcp_servers": "${workspaceFolder}/mcp-servers"
  },
  "path_resolution": {
    "enabled": true,
    "registry_file": "${workspaceFolder}/../path_registry.json",
    "strategy": "auto-detect"
  }
}
```

### 4.4 Integration with `51_AGENT_REGISTRY.json`

**Current State**: Hardcoded paths like `"location": "codexa.app/agentes/anuncio_agent"`.

**Migration**:

```json
{
  "agents": {
    "anuncio_agent": {
      "name": "Anúncio Generation Agent",
      "location": "{{AGENTES}}/anuncio_agent",
      "components": {
        "prime": "{{AGENTES}}/anuncio_agent/PRIME.md",
        "iso_vectorstore": "{{AGENTES}}/anuncio_agent/iso_vectorstore/",
        "commands": {
          "prime": "{{CLAUDE_DIR}}/commands/prime_anuncio.md"
        }
      }
    }
  }
}
```

**Resolution**: At runtime, load registry and resolve all paths using `PathResolver`.

---

## 5. SYNC MECHANISMS

### 5.1 Validation Script

**File**: `codexa.app/agentes/codexa_agent/validators/14_path_validator.py`

```python
"""
Path Registry Validator
Validates that all paths in registry exist and are consistent
"""

from codexa.core.path_resolver import PathResolver
from typing import Dict, List, Tuple
import json


class PathValidator:
    """Validates path registry and detects hardcoded paths in codebase."""

    def __init__(self):
        self.resolver = PathResolver()
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_registry(self) -> Tuple[bool, Dict]:
        """Validate all paths in registry exist."""
        print("=== Path Registry Validation ===")

        results = self.resolver.validate_all_paths()

        passed = 0
        failed = 0

        for path_key, exists in results.items():
            if exists:
                passed += 1
                print(f"  [OK] {path_key}")
            else:
                failed += 1
                print(f"  [FAIL] {path_key}")
                self.errors.append(f"Path does not exist: {path_key}")

        print(f"\nResults: {passed} passed, {failed} failed")

        return failed == 0, {
            "passed": passed,
            "failed": failed,
            "errors": self.errors
        }

    def detect_hardcoded_paths(self, directory: str) -> List[str]:
        """
        Scan directory for hardcoded absolute paths.

        Returns list of files with hardcoded paths.
        """
        import re
        from pathlib import Path

        hardcoded_pattern = re.compile(
            r'[A-Z]:\\\\Users\\\\|/home/|/Users/'  # Windows/Linux/Mac absolute paths
        )

        violations = []

        for file_path in Path(directory).rglob('*'):
            if file_path.is_file() and file_path.suffix in ['.py', '.js', '.json', '.md']:
                try:
                    content = file_path.read_text(encoding='utf-8')
                    if hardcoded_pattern.search(content):
                        violations.append(str(file_path))
                        self.warnings.append(f"Hardcoded path in: {file_path}")
                except Exception:
                    pass

        return violations

    def generate_report(self) -> Dict:
        """Generate validation report."""
        return {
            "validator": "path_validator",
            "version": "1.0.0",
            "errors": self.errors,
            "warnings": self.warnings,
            "passed": len(self.errors) == 0
        }


if __name__ == "__main__":
    validator = PathValidator()

    # Validate registry
    success, results = validator.validate_registry()

    # Detect hardcoded paths
    print("\n=== Hardcoded Path Detection ===")
    violations = validator.detect_hardcoded_paths("./codexa.app")

    if violations:
        print(f"Found {len(violations)} files with hardcoded paths:")
        for v in violations[:10]:  # Show first 10
            print(f"  - {v}")
    else:
        print("No hardcoded paths detected")

    # Generate report
    report = validator.generate_report()
    print(f"\n=== Report ===")
    print(json.dumps(report, indent=2))
```

### 5.2 Sync Script

**File**: `codexa.app/core/path_sync.py`

```python
"""
Path Registry Sync Script
Updates all files when project root changes
"""

from codexa.core.path_resolver import PathResolver
from pathlib import Path
import json
import re


class PathSyncer:
    """Syncs all path references when registry changes."""

    def __init__(self):
        self.resolver = PathResolver()
        self.updated_files = []

    def sync_agent_configs(self):
        """Update all agent config files with resolved paths."""
        agents_dir = self.resolver.resolve("{{AGENTES}}")

        for agent_dir in agents_dir.iterdir():
            if not agent_dir.is_dir():
                continue

            config_dir = agent_dir / "config"
            if not config_dir.exists():
                continue

            paths_file = config_dir / "paths.py"
            if paths_file.exists():
                self._update_paths_py(paths_file)

    def _update_paths_py(self, file_path: Path):
        """Update a paths.py file with resolver imports."""
        content = file_path.read_text(encoding='utf-8')

        # Check if already using resolver
        if 'from codexa.core.path_resolver import' in content:
            return

        # Add resolver import at top
        new_content = (
            'from codexa.core.path_resolver import PathResolver\n\n'
            'resolver = PathResolver()\n\n'
        ) + content

        file_path.write_text(new_content, encoding='utf-8')
        self.updated_files.append(str(file_path))

    def sync_registry_paths(self):
        """Convert hardcoded paths in registry to placeholders."""
        registry_path = self.resolver.resolve("{{AGENTES}}/51_AGENT_REGISTRY.json")

        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)

        # Convert paths to placeholders
        modified = False

        for agent_name, agent_spec in registry.get("agents", {}).items():
            # Update location
            if "location" in agent_spec and not agent_spec["location"].startswith("{{"):
                agent_spec["location"] = f"{{{{AGENTES}}}}/{agent_name}"
                modified = True

            # Update components
            if "components" in agent_spec:
                for key, value in agent_spec["components"].items():
                    if isinstance(value, str) and not value.startswith("{{"):
                        # Replace with placeholder
                        agent_spec["components"][key] = value.replace(
                            "codexa.app/agentes", "{{AGENTES}}"
                        ).replace(
                            ".claude/commands", "{{CLAUDE_DIR}}/commands"
                        )
                        modified = True

        if modified:
            with open(registry_path, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2, ensure_ascii=False)

            self.updated_files.append(str(registry_path))

    def report(self):
        """Print sync report."""
        print(f"=== Path Sync Report ===")
        print(f"Updated {len(self.updated_files)} files:")
        for f in self.updated_files:
            print(f"  - {f}")


if __name__ == "__main__":
    syncer = PathSyncer()

    print("Syncing agent configs...")
    syncer.sync_agent_configs()

    print("Syncing registry paths...")
    syncer.sync_registry_paths()

    syncer.report()
```

### 5.3 Git Hook (Pre-Commit)

**File**: `.git/hooks/pre-commit`

```bash
#!/bin/bash
# Pre-commit hook to prevent hardcoded paths

echo "Running path validation..."

# Run path validator
python codexa.app/agentes/codexa_agent/validators/14_path_validator.py

if [ $? -ne 0 ]; then
  echo "[FAIL] Path validation failed. Fix errors before committing."
  exit 1
fi

echo "[OK] Path validation passed"
exit 0
```

**Installation**:
```bash
chmod +x .git/hooks/pre-commit
```

---

## 6. MIGRATION PLAN

### Phase 1: Foundation (Week 1)

**Tasks**:
1. Create `path_registry.json` at project root
2. Implement `path_resolver.py` (Python)
3. Implement `pathResolver.js` (Node.js)
4. Create `path_validator.py`
5. Run validation, document current state

**Deliverables**:
- `path_registry.json` (complete schema)
- `codexa.app/core/path_resolver.py`
- `codexa.app/core/pathResolver.js`
- `codexa_agent/validators/14_path_validator.py`
- Migration report (current hardcoded paths)

### Phase 2: Integration (Week 2)

**Tasks**:
1. Migrate `curso_agent/config/paths.py` to use resolver
2. Update `51_AGENT_REGISTRY.json` with placeholders
3. Add path resolution to Scout MCP server
4. Create `.mcp.json` with environment variables
5. Update documentation (CLAUDE.md, PRIME.md files)

**Deliverables**:
- Updated `paths.py` for all agents using resolver
- Placeholder-based `51_AGENT_REGISTRY.json`
- `.mcp.json` configuration
- Documentation updates

### Phase 3: Automation (Week 3)

**Tasks**:
1. Implement `path_sync.py` script
2. Create git pre-commit hook
3. Add CI/CD validation (GitHub Actions)
4. Create migration guide for new agents
5. Batch update all existing files

**Deliverables**:
- `codexa.app/core/path_sync.py`
- `.git/hooks/pre-commit`
- `.github/workflows/path-validation.yml`
- `docs/PATH_MIGRATION_GUIDE.md`
- All files migrated to placeholders

### Phase 4: Documentation & Testing (Week 4)

**Tasks**:
1. Complete this specification document
2. Create usage examples for each agent
3. Test on Windows, Linux, macOS
4. Document edge cases and troubleshooting
5. Update CODEXA.md with path system rules

**Deliverables**:
- `specs/PATH_REGISTRY_SYSTEM_SPEC.md` (this file)
- `examples/path_resolution_examples.py`
- Cross-platform test results
- Updated project documentation

---

## 7. USAGE EXAMPLES

### 7.1 Python Module

```python
from codexa.core.path_resolver import PathResolver, resolve_path

# Quick resolution
prime_path = resolve_path("{{AGENTES}}/scout_agent/PRIME.md")
print(prime_path)  # C:\Users\Dell\...\codexa.app\agentes\scout_agent\PRIME.md

# Advanced usage
resolver = PathResolver()

# Get all paths for an agent
scout_paths = resolver.get_agent_context("scout_agent")
for key, path in scout_paths.items():
    print(f"{key}: {path}")

# Resolve with context
context = {"AGENT_DIR": "scout_agent"}
config_path = resolver.resolve("{{AGENT_DIR}}/config/categories.json", context)
```

### 7.2 Node.js Module

```javascript
const { PathResolver, resolvePath } = require('./codexa.app/core/pathResolver');

// Quick resolution
const primePath = resolvePath('{{AGENTES}}/scout_agent/PRIME.md');
console.log(primePath);

// Advanced usage
const resolver = new PathResolver();

// Get all paths for an agent
const scoutPaths = resolver.getAgentContext('scout_agent');
Object.entries(scoutPaths).forEach(([key, path]) => {
  console.log(`${key}: ${path}`);
});
```

### 7.3 Documentation

```markdown
# Scout Agent PRIME

**Location**: {{AGENTES}}/scout_agent/PRIME.md

## Configuration Files

- Categories: {{AGENT_CONFIG}}/categories.json
- Weights: {{AGENT_CONFIG}}/relevance_weights.json
- Aliases: {{AGENT_CONFIG}}/semantic_aliases.json

## MCP Server

Server implementation: {{MCP_SERVERS}}/scout-mcp/index.js
```

### 7.4 Agent Registry

```json
{
  "agents": {
    "scout_agent": {
      "location": "{{AGENTES}}/scout_agent",
      "components": {
        "prime": "{{AGENTES}}/scout_agent/PRIME.md",
        "mcp_server": "{{MCP_SERVERS}}/scout-mcp/index.js"
      }
    }
  }
}
```

---

## 8. VALIDATION RULES

### 8.1 Registry Validation

**Rules**:
1. All `root_anchors` MUST have valid `detection_strategy`
2. All `root_anchors` MUST pass `validation` checks
3. All `agent_paths` MUST use only defined placeholders
4. No circular dependencies in placeholder resolution

### 8.2 Code Validation

**Rules**:
1. Python/JS modules MUST NOT contain hardcoded absolute paths
2. Exception: Test files MAY use hardcoded paths if marked with `# TEST ONLY`
3. Configuration files MUST use placeholders OR resolver
4. Documentation MUST use placeholders (never resolved paths)

### 8.3 Git Pre-Commit Validation

**Checks**:
1. Run `path_validator.py` - must return 0 errors
2. Scan staged files for hardcoded paths (regex)
3. Validate `path_registry.json` schema if modified
4. Check that all placeholders are defined

---

## 9. TROUBLESHOOTING

### Issue: "Could not detect PROJECT_ROOT"

**Cause**: Not running from within git repository.

**Solution**:
```bash
# Verify git root
git rev-parse --show-toplevel

# Set environment variable
export PROJECT_ROOT=/path/to/codexa.gato
```

### Issue: "Unknown placeholder: {{AGENT_DIR}}"

**Cause**: Context-dependent placeholder used without context.

**Solution**:
```python
# Provide context
context = {"AGENT_DIR": "scout_agent"}
resolver.resolve("{{AGENT_DIR}}/config", context)
```

### Issue: "Path does not exist after resolution"

**Cause**: Registry out of sync with filesystem.

**Solution**:
```bash
# Re-sync registry
python codexa.app/core/path_sync.py

# Validate
python codexa.app/agentes/codexa_agent/validators/14_path_validator.py
```

---

## 10. FUTURE ENHANCEMENTS

### v1.1.0 - Environment Variables

- Support for `.env` files alongside `path_registry.json`
- Dynamic environment variable substitution

### v1.2.0 - Remote Paths

- Support for remote paths (cloud storage, URLs)
- Caching strategy for remote resources

### v1.3.0 - Path Versioning

- Version different path configurations
- Switch between dev/staging/production paths

### v2.0.0 - Distributed Registry

- Support for multiple registries (per-agent overrides)
- Inheritance and composition of registries

---

## 11. COMPLIANCE WITH CODEXA LAWS

### LAW 1: DISTILLATION PRINCIPLE

**Compliance**: Path registry uses `{{PLACEHOLDERS}}` compatible with Mustache syntax defined in CLAUDE.md.

**Standard Placeholders Extended**:
- System-level: `{{PROJECT_ROOT}}`, `{{CODEXA_APP}}`, `{{AGENTES}}`
- Brand-level: Reuses existing `{{BRAND_NAME}}`, `{{BRAND_URL}}`, etc.

### LAW 2: FRACTAL NAVIGATION

**Compliance**: Path resolver follows same pattern at all levels:
- `path_registry.json` → Project root
- `paths.json` → Agent config directories
- Context-aware resolution at runtime

### LAW 3: META-CONSTRUCTION

**Compliance**: Path registry system is a **builder** (builds paths, not hardcoded instances).

**Meta Pattern**:
1. Registry = Template (defines structure)
2. Resolver = Builder (generates paths)
3. Validation = Quality Gate (ensures correctness)

### LAW 4: AGENTIC DESIGN

**Compliance**: Each agent can define agent-specific paths in `agent_paths` section of registry.

**Domain**: Path discovery, resolution, validation
**Workflows**: Sync, validate, migrate
**Prompts**: Integration with HOPs (path resolution in templates)
**Outputs**: Resolved paths, validation reports

---

## 12. APPENDIX

### A. Complete Path Registry Example

See Section 2.2 for full JSON schema.

### B. Migration Checklist

**Per Agent**:
- [ ] Create `config/paths.json` (agent-specific paths)
- [ ] Update `config/paths.py` to use PathResolver
- [ ] Update PRIME.md with placeholders
- [ ] Update README.md with placeholders
- [ ] Update builders to use resolver
- [ ] Update validators to use resolver
- [ ] Test all workflows with new paths

**System-wide**:
- [ ] Create `path_registry.json` at project root
- [ ] Implement `path_resolver.py` and `pathResolver.js`
- [ ] Implement `path_validator.py`
- [ ] Implement `path_sync.py`
- [ ] Create git pre-commit hook
- [ ] Update `51_AGENT_REGISTRY.json` with placeholders
- [ ] Update `.claude/settings.json` (if exists)
- [ ] Create `.mcp.json` with env variables
- [ ] Update CLAUDE.md with path system rules
- [ ] Update all documentation to use placeholders

### C. Placeholder Reference Card

| Placeholder | Resolves To | Usage |
|-------------|-------------|-------|
| `{{PROJECT_ROOT}}` | Git root (auto-detect) | Absolute root paths |
| `{{CODEXA_APP}}` | `PROJECT_ROOT/codexa.app` | Main app paths |
| `{{AGENTES}}` | `CODEXA_APP/agentes` | Agent directories |
| `{{MCP_SERVERS}}` | `CODEXA_APP/mcp-servers` | MCP servers |
| `{{CLAUDE_DIR}}` | `PROJECT_ROOT/.claude` | Claude config |
| `{{AGENT_DIR}}` | Context-dependent | Current agent (dynamic) |
| `{{AGENT_CONFIG}}` | `AGENT_DIR/config` | Agent config files |
| `{{AGENT_ISO}}` | `AGENT_DIR/iso_vectorstore` | Agent knowledge |
| `{{AGENT_WORKFLOWS}}` | `AGENT_DIR/workflows` | Agent ADWs |
| `{{AGENT_PROMPTS}}` | `AGENT_DIR/prompts` | Agent HOPs |

### D. Cross-Platform Compatibility

**Windows**:
- Paths: `C:\Users\Dell\...` → Resolved via `Path.resolve()`
- Separators: Backslash `\` → Handled by `os.path.sep`
- Line endings: CRLF → Git handles via `core.autocrlf`

**Unix/Linux/macOS**:
- Paths: `/home/user/...` → Resolved via `path.resolve()`
- Separators: Forward slash `/` → Handled by `path.sep`
- Line endings: LF → Native format

**Resolution**: Python `pathlib.Path` and Node `path.resolve()` handle cross-platform automatically.

---

## DOCUMENT METADATA

**Version**: 1.0.0
**Created**: 2025-12-02
**Author**: CODEXA Meta Agent
**Type**: System Architecture Specification
**Status**: Design Phase (Ready for Implementation)
**Related Documents**:
- `CLAUDE.md` (LAW 1: Distillation Principle)
- `51_AGENT_REGISTRY.json` (Agent registry)
- `curso_agent/config/paths.py` (Existing path system)
- `SCOUT_INTEGRATION.md` (MCP integration)

**Quality Gates**:
- [x] Comprehensive schema defined
- [x] Cross-platform compatibility addressed
- [x] Integration with existing systems documented
- [x] Migration plan provided (4 phases)
- [x] Validation strategy defined
- [x] Examples and usage documented
- [x] Compliance with CODEXA laws verified

**Next Steps**:
1. Review specification with stakeholders
2. Approve implementation phases
3. Begin Phase 1: Foundation (create registry + resolvers)
4. Test cross-platform compatibility
5. Migrate agents incrementally

---

> **Meta-Note**: This specification was generated using CODEXA meta-construction principles. It follows the **Build the builder, not the instance** philosophy by creating a system that generates paths dynamically rather than hardcoding them.

**End of Specification**
