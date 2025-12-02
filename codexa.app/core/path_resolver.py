"""
CODEXA Path Resolver
Resolves {{PLACEHOLDERS}} to absolute paths at runtime

Usage:
    from codexa.app.core.path_resolver import PathResolver, resolve_path

    # Quick resolution
    path = resolve_path("{{AGENTES}}/scout_agent/PRIME.md")

    # Advanced usage
    resolver = PathResolver()
    scout_paths = resolver.get_agent_context("scout_agent")
"""

import json
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, Optional, Any, List


class PathResolver:
    """
    Central path resolution engine for CODEXA project.

    Resolves placeholder syntax like {{PROJECT_ROOT}} to actual paths.
    Cross-platform compatible (Windows/Unix).
    Auto-detects project root via git.
    """

    def __init__(self, registry_path: Optional[Path] = None):
        """
        Initialize resolver with path registry.

        Args:
            registry_path: Path to path_registry.json (auto-detects if None)
        """
        import platform
        self.platform = platform.system()  # Windows, Linux, Darwin
        self._root_cache: Dict[str, Path] = {}
        self._project_root = self._detect_project_root()
        self.registry = self._load_registry(registry_path)

    def _detect_project_root(self) -> Path:
        """Detect PROJECT_ROOT - the codexa.gato directory containing codexa.app."""
        # Walk up from this file looking for codexa.gato
        current = Path(__file__).resolve()
        for parent in current.parents:
            # The real project root has codexa.app as DIRECT child
            if (parent / "codexa.app").exists() and parent.name != "codexa.app":
                # Verify this is codexa.gato by checking for path_registry.json or CLAUDE.md
                if (parent / "path_registry.json").exists() or (parent / "CLAUDE.md").exists():
                    return parent
                # Also check if parent name suggests it's the right one
                if "codexa" in parent.name.lower() or "gato" in parent.name.lower():
                    return parent

        # Try git root but validate it's the right level
        try:
            result = subprocess.run(
                ['git', 'rev-parse', '--show-toplevel'],
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            if result.returncode == 0:
                git_root = Path(result.stdout.strip())
                # Check if codexa.gato is inside git_root
                for child in git_root.iterdir():
                    if child.is_dir() and (child / "codexa.app").exists():
                        if (child / "path_registry.json").exists() or (child / "CLAUDE.md").exists():
                            return child
                # Or if git_root itself is the project
                if (git_root / "codexa.app").exists() and (git_root / "path_registry.json").exists():
                    return git_root
        except Exception:
            pass

        # Last resort: check environment variable
        env_root = os.getenv("PROJECT_ROOT") or os.getenv("CODEXA_ROOT")
        if env_root:
            return Path(env_root)

        raise RuntimeError(
            "Could not detect PROJECT_ROOT. "
            "Ensure you're in codexa.gato with codexa.app/ or set PROJECT_ROOT env var."
        )

    def _load_registry(self, registry_path: Optional[Path]) -> Dict[str, Any]:
        """Load path registry from JSON file."""
        if registry_path is None:
            registry_path = self._project_root / "path_registry.json"

        if not registry_path.exists():
            # Return minimal registry if file doesn't exist
            return self._get_default_registry()

        with open(registry_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _get_default_registry(self) -> Dict[str, Any]:
        """Return default registry when file doesn't exist."""
        return {
            "root_anchors": {
                "PROJECT_ROOT": {
                    "detection_strategy": "git_root"
                },
                "CODEXA_APP": {
                    "relative_to": "PROJECT_ROOT",
                    "path": "codexa.app"
                },
                "AGENTES": {
                    "relative_to": "CODEXA_APP",
                    "path": "agentes"
                },
                "MCP_SERVERS": {
                    "relative_to": "CODEXA_APP",
                    "path": "mcp-servers"
                },
                "CLAUDE_DIR": {
                    "relative_to": "PROJECT_ROOT",
                    "path": ".claude"
                }
            },
            "standard_placeholders": {
                "system_level": {
                    "{{PROJECT_ROOT}}": {"resolves_to": "root_anchors.PROJECT_ROOT"},
                    "{{CODEXA_APP}}": {"resolves_to": "root_anchors.CODEXA_APP"},
                    "{{AGENTES}}": {"resolves_to": "root_anchors.AGENTES"},
                    "{{MCP_SERVERS}}": {"resolves_to": "root_anchors.MCP_SERVERS"},
                    "{{CLAUDE_DIR}}": {"resolves_to": "root_anchors.CLAUDE_DIR"}
                }
            },
            "agent_paths": {}
        }

    def _resolve_root_anchor(self, anchor_name: str) -> Path:
        """Resolve a root anchor like PROJECT_ROOT."""
        if anchor_name in self._root_cache:
            return self._root_cache[anchor_name]

        if anchor_name == "PROJECT_ROOT":
            self._root_cache[anchor_name] = self._project_root
            return self._project_root

        anchor_spec = self.registry.get("root_anchors", {}).get(anchor_name)
        if not anchor_spec:
            raise KeyError(f"Unknown root anchor: {anchor_name}")

        # Handle relative anchors
        relative_to = anchor_spec.get("relative_to")
        if relative_to:
            parent = self._resolve_root_anchor(relative_to)
            resolved = parent / anchor_spec.get("path", "")
        else:
            # Handle detection strategies
            strategy = anchor_spec.get("detection_strategy")
            if strategy == "git_root":
                resolved = self._project_root
            elif strategy == "env":
                env_var = anchor_spec.get("fallback", "").replace("env:", "")
                env_value = os.getenv(env_var)
                if not env_value:
                    raise EnvironmentError(f"Environment variable not set: {env_var}")
                resolved = Path(env_value)
            else:
                raise ValueError(f"Cannot resolve anchor: {anchor_name}")

        self._root_cache[anchor_name] = resolved
        return resolved

    def resolve(self, placeholder: str, context: Optional[Dict[str, str]] = None) -> Path:
        """
        Resolve a placeholder to an absolute path.

        Args:
            placeholder: String like "{{PROJECT_ROOT}}/codexa.app" or "{{AGENTES}}/scout_agent"
            context: Optional context for dynamic placeholders (e.g., {"AGENT_DIR": "scout_agent"})

        Returns:
            Resolved absolute Path object

        Example:
            >>> resolver = PathResolver()
            >>> resolver.resolve("{{AGENTES}}/scout_agent/PRIME.md")
            Path('C:/Users/.../codexa.app/agentes/scout_agent/PRIME.md')
        """
        if not placeholder:
            raise ValueError("Empty placeholder")

        # If it's already an absolute path, return it
        if Path(placeholder).is_absolute():
            return Path(placeholder)

        # Extract placeholders from string (supports multiple)
        placeholders_found = re.findall(r'\{\{([A-Z_]+)\}\}', placeholder)

        result = placeholder
        for ph in placeholders_found:
            full_placeholder = f"{{{{{ph}}}}}"

            # Check context first (for agent-level placeholders)
            if context and ph in context:
                resolved_value = str(context[ph])
            # Check if it's a known root anchor
            elif ph in self.registry.get("root_anchors", {}):
                resolved_value = str(self._resolve_root_anchor(ph))
            # Check standard placeholders mapping
            elif full_placeholder in self.registry.get("standard_placeholders", {}).get("system_level", {}):
                spec = self.registry["standard_placeholders"]["system_level"][full_placeholder]
                anchor_ref = spec.get("resolves_to", "")
                if anchor_ref.startswith("root_anchors."):
                    anchor_name = anchor_ref.split(".")[1]
                    resolved_value = str(self._resolve_root_anchor(anchor_name))
                else:
                    resolved_value = str(self.resolve(anchor_ref, context))
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
        """
        agent_paths = self.registry.get("agent_paths", {}).get(agent_name)
        if not agent_paths:
            # Fallback to default pattern
            return self.resolve(f"{{{{AGENTES}}}}/{agent_name}/{path_key}")

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
            except Exception:
                results[anchor_name] = False

        # Validate agent paths
        for agent_name in self.registry.get("agent_paths", {}):
            try:
                context = self.get_agent_context(agent_name)
                for key, path in context.items():
                    results[f"{agent_name}.{key}"] = path.exists()
            except Exception:
                results[agent_name] = False

        return results

    @property
    def project_root(self) -> Path:
        """Get the detected project root."""
        return self._project_root

    @property
    def codexa_app(self) -> Path:
        """Get the codexa.app directory."""
        return self._resolve_root_anchor("CODEXA_APP")

    @property
    def agentes(self) -> Path:
        """Get the agentes directory."""
        return self._resolve_root_anchor("AGENTES")


# Global resolver instance (lazy-loaded)
_resolver: Optional[PathResolver] = None


def get_resolver() -> PathResolver:
    """Get or create global PathResolver instance."""
    global _resolver
    if _resolver is None:
        _resolver = PathResolver()
    return _resolver


def resolve_path(placeholder: str, context: Optional[Dict[str, str]] = None) -> Path:
    """
    Quick path resolution without instantiating PathResolver.

    Example:
        >>> from codexa.app.core.path_resolver import resolve_path
        >>> resolve_path("{{AGENTES}}/scout_agent/PRIME.md")
        Path('C:/.../codexa.app/agentes/scout_agent/PRIME.md')
    """
    return get_resolver().resolve(placeholder, context)


def get_project_root() -> Path:
    """Get project root path."""
    return get_resolver().project_root


def get_agent_dir(agent_name: str) -> Path:
    """Get directory for a specific agent."""
    return get_resolver().resolve(f"{{{{AGENTES}}}}/{agent_name}")


# ============================================================
# CLI Interface
# ============================================================

if __name__ == "__main__":
    import sys

    resolver = PathResolver()

    print("=" * 60)
    print("CODEXA Path Resolver")
    print("=" * 60)
    print(f"Platform: {resolver.platform}")
    print(f"PROJECT_ROOT: {resolver.project_root}")
    print(f"CODEXA_APP:   {resolver.codexa_app}")
    print(f"AGENTES:      {resolver.agentes}")
    print()

    # Test some resolutions
    test_paths = [
        "{{PROJECT_ROOT}}/CLAUDE.md",
        "{{AGENTES}}/scout_agent/PRIME.md",
        "{{MCP_SERVERS}}/scout-mcp/index.js",
        "{{CLAUDE_DIR}}/commands",
    ]

    print("Test Resolutions:")
    print("-" * 60)
    for test in test_paths:
        try:
            resolved = resolver.resolve(test)
            exists = "[OK]" if resolved.exists() else "[MISSING]"
            print(f"{exists} {test}")
            print(f"      -> {resolved}")
        except Exception as e:
            print(f"[ERROR] {test}")
            print(f"      -> {e}")
    print()

    # Validate all paths if registry exists
    print("Path Validation:")
    print("-" * 60)
    validation = resolver.validate_all_paths()
    passed = sum(1 for v in validation.values() if v)
    failed = sum(1 for v in validation.values() if not v)

    for path_key, exists in validation.items():
        status = "[OK]" if exists else "[MISSING]"
        print(f"  {status} {path_key}")

    print()
    print(f"Results: {passed} passed, {failed} failed")

    # Exit with error code if any failures
    sys.exit(0 if failed == 0 else 1)
