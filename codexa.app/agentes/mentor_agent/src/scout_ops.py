"""
CODEXA Scout Operations

Repository Librarian Agent - Organize, Annotate, Navigate

SCOUT PHILOSOPHY:
- Know where everything is and where it should be
- Annotate files with PURPOSE bullets that compress maximum semantic density
- Create entropic guidance systems for knowledge navigation
- Enable verticalized consultation patterns through axioms

CORE CAPABILITIES:
1. Repository Scanning: Deep structural analysis of codebase
2. Intelligent Organization: Context-aware file placement
3. Entropic Annotation: PURPOSE bullets at file headers
4. Vertical Navigation: Axiom-driven consultation chains

ANNOTATION FORMAT:
Every file that SCOUT processes receives a header bullet:
```
• PURPOSE ▸ [ENTROPIC_AXIOM] → [VERTICAL_SEQUENCE_TRIGGER]
```

ENTROPIC AXIOM RULES:
- Non-truncated: Complete thought, no abbreviated meaning
- Axiomatically Dense: Maximum information per word
- Consultation Trigger: Seeds next-step vertical queries
- Context Invariant: Meaningful without surrounding context
"""

from typing import Optional, Dict, List, Any, Set, Tuple
from pathlib import Path
from datetime import datetime
import json
import re

from .utils.logger import get_logger
from .utils.file_ops import get_file_ops, FileOperations
from .utils.git_helper import get_git_helper, GitHelper

logger = get_logger()

# Constants
ANNOTATION_MARKER = "• PURPOSE ▸"
SCAN_CACHE = ".scout_cache.json"
ORGANIZATION_LOG = ".scout_organization.jsonl"


class ScoutAnnotation:
    """Represents a SCOUT PURPOSE annotation."""

    def __init__(self, axiom: str, trigger: str, timestamp: Optional[str] = None):
        self.axiom = axiom
        self.trigger = trigger
        self.timestamp = timestamp or datetime.now().isoformat()

    def format(self) -> str:
        """Format annotation for file header."""
        return f"{ANNOTATION_MARKER} {self.axiom} → {self.trigger}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert annotation to dictionary."""
        return {
            "axiom": self.axiom,
            "trigger": self.trigger,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScoutAnnotation":
        """Create annotation from dictionary."""
        return cls(
            axiom=data["axiom"],
            trigger=data["trigger"],
            timestamp=data.get("timestamp"),
        )


class ScoutRepository:
    """Repository structure and metadata management."""

    def __init__(self, root_path: str):
        """
        Initialize Scout repository.

        Args:
            root_path: Root directory of the repository
        """
        self.root_path = Path(root_path)
        self.structure: Dict[str, Any] = {}
        self.file_index: Dict[str, str] = {}
        self.annotations: Dict[str, ScoutAnnotation] = {}

    def scan(
        self, ignore_patterns: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Scan repository and build structure map.

        Args:
            ignore_patterns: List of glob patterns to ignore

        Returns:
            Dictionary containing repository structure
        """
        if ignore_patterns is None:
            ignore_patterns = [
                ".git",
                "__pycache__",
                "node_modules",
                ".venv",
                "venv",
                "*.pyc",
                ".DS_Store",
                "*.egg-info",
                "dist",
                "build",
            ]

        logger.operation_start("scout_scan", root=str(self.root_path))

        structure = {
            "root": str(self.root_path),
            "directories": [],
            "files": [],
            "stats": {
                "total_files": 0,
                "total_dirs": 0,
                "file_types": {},
            },
        }

        for item in self.root_path.rglob("*"):
            # Skip ignored patterns
            if any(item.match(pattern) for pattern in ignore_patterns):
                continue

            rel_path = item.relative_to(self.root_path)

            if item.is_file():
                ext = item.suffix or "no_extension"
                structure["stats"]["file_types"][ext] = (
                    structure["stats"]["file_types"].get(ext, 0) + 1
                )
                structure["stats"]["total_files"] += 1
                structure["files"].append(str(rel_path))
                self.file_index[str(rel_path)] = str(item)
            elif item.is_dir():
                structure["stats"]["total_dirs"] += 1
                structure["directories"].append(str(rel_path))

        self.structure = structure
        logger.operation_success(
            "scout_scan",
            files=structure["stats"]["total_files"],
            dirs=structure["stats"]["total_dirs"],
        )
        return structure

    def save_cache(self, cache_path: Optional[Path] = None) -> Tuple[bool, str]:
        """
        Save scan results to cache.

        Args:
            cache_path: Path to cache file (defaults to .scout_cache.json in root)

        Returns:
            Tuple of (success, message)
        """
        if cache_path is None:
            cache_path = self.root_path / SCAN_CACHE

        try:
            cache_data = {
                "structure": self.structure,
                "annotations": {k: v.to_dict() for k, v in self.annotations.items()},
                "timestamp": datetime.now().isoformat(),
            }

            with open(cache_path, "w") as f:
                json.dump(cache_data, f, indent=2)

            logger.info(f"Saved Scout cache to: {cache_path}")
            return True, str(cache_path)

        except Exception as e:
            logger.error(f"Failed to save Scout cache: {e}")
            return False, str(e)

    def load_cache(self, cache_path: Optional[Path] = None) -> bool:
        """
        Load scan results from cache.

        Args:
            cache_path: Path to cache file

        Returns:
            True if cache was loaded successfully
        """
        if cache_path is None:
            cache_path = self.root_path / SCAN_CACHE

        if not Path(cache_path).exists():
            logger.info(f"No Scout cache found at: {cache_path}")
            return False

        try:
            with open(cache_path, "r") as f:
                cache_data = json.load(f)

            self.structure = cache_data.get("structure", {})

            # Reconstruct annotations
            for path, ann_data in cache_data.get("annotations", {}).items():
                self.annotations[path] = ScoutAnnotation.from_dict(ann_data)

            logger.info(
                f"Loaded Scout cache: {len(self.annotations)} annotations, "
                f"{self.structure.get('stats', {}).get('total_files', 0)} files"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to load Scout cache: {e}")
            return False


class ScoutOperations:
    """
    Core Scout operations for repository organization and annotation.

    Capabilities:
    - scan: Scan repository structure
    - annotate: Add PURPOSE bullets to files
    - query: Ask about file organization
    - organize: Suggest file reorganization
    """

    def __init__(
        self,
        auto_backup: bool = True,
        auto_git: bool = True,
        dry_run: bool = False,
        agent_executor: Optional[Any] = None,
    ):
        """
        Initialize Scout operations.

        Args:
            auto_backup: Automatically backup files before modification
            auto_git: Automatically commit changes to git
            dry_run: Preview operations without executing them
            agent_executor: Optional agent executor for AI-powered operations
        """
        self.auto_backup = auto_backup
        self.auto_git = auto_git
        self.dry_run = dry_run
        self.agent_executor = agent_executor

        self.file_ops = get_file_ops(auto_backup=auto_backup, auto_git=False)
        self.git_helper = get_git_helper() if auto_git else None

        logger.module_loaded(
            "ScoutOperations",
            capabilities=["scan", "annotate", "query", "organize"],
        )

    # ==================== SCANNING OPERATIONS ====================

    def scan_repository(
        self,
        root_path: str,
        ignore_patterns: Optional[List[str]] = None,
        use_cache: bool = True,
    ) -> Tuple[bool, Union[ScoutRepository, str]]:
        """
        Scan repository and build structure map.

        Args:
            root_path: Root directory to scan
            ignore_patterns: Patterns to ignore during scan
            use_cache: Whether to use/create cache

        Returns:
            Tuple of (success, repository_or_error)
        """
        logger.operation_start("scan_repository", path=root_path)

        try:
            repo = ScoutRepository(root_path)

            # Try to load from cache
            if use_cache and repo.load_cache():
                logger.info("Using cached repository structure")
                return True, repo

            # Perform scan
            repo.scan(ignore_patterns=ignore_patterns)

            # Save cache if enabled
            if use_cache:
                success, cache_path = repo.save_cache()
                if success:
                    logger.info(f"Cached repository structure to: {cache_path}")

            logger.operation_success("scan_repository", path=root_path)
            return True, repo

        except Exception as e:
            logger.operation_failure("scan_repository", str(e), path=root_path)
            return False, str(e)

    # ==================== ANNOTATION OPERATIONS ====================

    def create_annotation(
        self,
        file_path: str,
        file_content: str,
        context: Dict[str, Any],
        use_ai: bool = True,
    ) -> Tuple[bool, Union[ScoutAnnotation, str]]:
        """
        Create a PURPOSE annotation for a file.

        Args:
            file_path: Path to the file
            file_content: Content of the file
            context: Repository context
            use_ai: Whether to use AI to generate annotation

        Returns:
            Tuple of (success, annotation_or_error)
        """
        if not use_ai:
            # Create simple annotation without AI
            annotation = ScoutAnnotation(
                axiom=f"File at {file_path}",
                trigger=f"Review {Path(file_path).name} for implementation details",
            )
            return True, annotation

        if not self.agent_executor:
            msg = "AI annotation requires agent_executor to be configured"
            logger.warning(msg)
            return False, msg

        logger.operation_start("create_annotation", file=file_path)

        try:
            # Prepare prompt for AI
            prompt = self._build_annotation_prompt(file_path, file_content, context)

            # Execute AI request (placeholder - will be implemented with agent integration)
            # For now, create a basic annotation
            # TODO: Integrate with agent executor
            logger.warning("AI annotation not yet implemented, using fallback")

            annotation = ScoutAnnotation(
                axiom=f"Implements core functionality for {Path(file_path).stem}",
                trigger=f"Consult related files for integration patterns",
            )

            logger.operation_success("create_annotation", file=file_path)
            return True, annotation

        except Exception as e:
            logger.operation_failure("create_annotation", str(e), file=file_path)
            return False, str(e)

    def annotate_file(
        self,
        file_path: Union[str, Path],
        annotation: ScoutAnnotation,
    ) -> Tuple[bool, str]:
        """
        Add PURPOSE annotation to file header.

        Args:
            file_path: Path to the file
            annotation: Annotation to add

        Returns:
            Tuple of (success, message)
        """
        if self.dry_run:
            logger.info(f"[DRY RUN] Would annotate file: {file_path}")
            return True, f"[DRY RUN] Would annotate: {file_path}"

        logger.operation_start("annotate_file", path=str(file_path))

        try:
            path = Path(file_path)

            if not path.exists():
                msg = f"File does not exist: {file_path}"
                logger.warning(msg)
                return False, msg

            # Read current content
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            # Determine comment style
            comment_char = self._get_comment_char(path.suffix)

            # Format annotation
            if comment_char == "<!--":
                annotation_line = f"<!-- {annotation.format()} -->\n\n"
            else:
                annotation_line = f"{comment_char} {annotation.format()}\n\n"

            # Check if annotation already exists
            if ANNOTATION_MARKER in content:
                # Replace existing annotation
                pattern = r"(#|//|<!--|--)\s*" + re.escape(ANNOTATION_MARKER) + r".+?(\n|-->)"
                new_content = re.sub(
                    pattern, annotation_line.strip() + "\n", content, count=1
                )
            else:
                # Add annotation at the beginning
                lines = content.split("\n")
                insert_pos = self._find_insertion_point(lines)
                lines.insert(insert_pos, annotation_line.rstrip())
                new_content = "\n".join(lines)

            # Write updated content
            success, message = self.file_ops.update_file(path, new_content)

            if success and self.auto_git:
                self._git_commit(
                    "annotate", [path], f"Add Scout annotation: {path.name}"
                )

            if success:
                logger.operation_success("annotate_file", path=str(file_path))
            else:
                logger.operation_failure("annotate_file", message, path=str(file_path))

            return success, message

        except Exception as e:
            logger.operation_failure("annotate_file", str(e), path=str(file_path))
            return False, str(e)

    def annotate_directory(
        self,
        directory: Union[str, Path],
        pattern: str = "*",
        recursive: bool = True,
        use_ai: bool = True,
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        Annotate multiple files in a directory.

        Args:
            directory: Directory to annotate
            pattern: File pattern to match
            recursive: Whether to search recursively
            use_ai: Whether to use AI for annotations

        Returns:
            Tuple of (success, results_dict)
        """
        logger.operation_start("annotate_directory", path=str(directory))

        try:
            dir_path = Path(directory)
            if not dir_path.exists():
                return False, {"error": f"Directory not found: {directory}"}

            # Find files
            if recursive:
                files = list(dir_path.rglob(pattern))
            else:
                files = list(dir_path.glob(pattern))

            files = [f for f in files if f.is_file()]

            results = {
                "total": len(files),
                "success": 0,
                "failed": 0,
                "skipped": 0,
                "files": {},
            }

            # Scan repository for context
            scan_success, repo = self.scan_repository(str(dir_path), use_cache=True)
            context = {"repository_structure": repo.structure} if scan_success else {}

            # Process each file
            for file_path in files:
                try:
                    # Read file content
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()

                    # Create annotation
                    ann_success, annotation = self.create_annotation(
                        str(file_path), content, context, use_ai=use_ai
                    )

                    if not ann_success:
                        results["failed"] += 1
                        results["files"][str(file_path)] = {"status": "failed", "error": annotation}
                        continue

                    # Apply annotation
                    apply_success, message = self.annotate_file(file_path, annotation)

                    if apply_success:
                        results["success"] += 1
                        results["files"][str(file_path)] = {"status": "success"}
                    else:
                        results["failed"] += 1
                        results["files"][str(file_path)] = {"status": "failed", "error": message}

                except Exception as e:
                    results["failed"] += 1
                    results["files"][str(file_path)] = {"status": "error", "error": str(e)}

            logger.operation_success(
                "annotate_directory",
                path=str(directory),
                success=results["success"],
                failed=results["failed"],
            )
            return True, results

        except Exception as e:
            logger.operation_failure("annotate_directory", str(e), path=str(directory))
            return False, {"error": str(e)}

    # ==================== QUERY OPERATIONS ====================

    def query_organization(
        self,
        query: str,
        repository: ScoutRepository,
    ) -> Tuple[bool, Union[Dict[str, Any], str]]:
        """
        Query SCOUT about file organization.

        Args:
            query: Organization query
            repository: Repository to query against

        Returns:
            Tuple of (success, result_or_error)
        """
        if not self.agent_executor:
            msg = "Query requires agent_executor to be configured"
            logger.warning(msg)
            return False, msg

        logger.operation_start("query_organization", query=query)

        try:
            # Build query prompt
            prompt = self._build_query_prompt(query, repository)

            # Execute AI query (placeholder)
            # TODO: Integrate with agent executor
            logger.warning("AI query not yet implemented, using fallback")

            result = {
                "recommended_path": "suggested/path/location",
                "reasoning": "Based on repository patterns and file organization",
                "related_files": [],
                "consultation_sequence": [],
            }

            logger.operation_success("query_organization", query=query)
            return True, result

        except Exception as e:
            logger.operation_failure("query_organization", str(e), query=query)
            return False, str(e)

    # ==================== HELPER METHODS ====================

    def _get_comment_char(self, ext: str) -> str:
        """Get comment character for file extension."""
        comment_styles = {
            ".py": "#",
            ".js": "//",
            ".ts": "//",
            ".tsx": "//",
            ".jsx": "//",
            ".java": "//",
            ".c": "//",
            ".cpp": "//",
            ".go": "//",
            ".rs": "//",
            ".md": "<!--",
            ".html": "<!--",
            ".xml": "<!--",
            ".sh": "#",
            ".bash": "#",
            ".yaml": "#",
            ".yml": "#",
            ".toml": "#",
            ".sql": "--",
        }
        return comment_styles.get(ext, "#")

    def _find_insertion_point(self, lines: List[str]) -> int:
        """Find the best insertion point for annotation."""
        insert_pos = 0

        # Skip shebang
        if lines and lines[0].startswith("#!"):
            insert_pos = 1

        # Skip encoding declarations (Python)
        if insert_pos < len(lines) and "coding:" in lines[insert_pos]:
            insert_pos += 1

        return insert_pos

    def _build_annotation_prompt(
        self, file_path: str, file_content: str, context: Dict[str, Any]
    ) -> str:
        """Build prompt for AI annotation generation."""
        return f"""You are SCOUT, a meta-librarian creating entropic PURPOSE annotations.

FILE TO ANNOTATE:
Path: {file_path}
Content Preview (first 1000 chars):
{file_content[:1000]}

Repository Context:
{json.dumps(context, indent=2)}

YOUR TASK:
Create a PURPOSE annotation following this format:
• PURPOSE ▸ [ENTROPIC_AXIOM] → [VERTICAL_SEQUENCE_TRIGGER]

ENTROPIC AXIOM RULES:
1. **Non-truncated**: Complete thought, no abbreviated meaning
2. **Axiomatically Dense**: Maximum information per word
3. **Consultation Trigger**: Seeds next-step vertical queries
4. **Context Invariant**: Meaningful without surrounding context

EXAMPLES:
✓ GOOD: "• PURPOSE ▸ Transform raw OCR output into structured knowledge cards through semantic enrichment and validation → Query card_validator.py for quality assurance patterns"

✓ GOOD: "• PURPOSE ▸ Orchestrate 7-phase ML knowledge processing pipeline from raw documents to production-ready embeddings → Consult pipeline_orchestrator.py for phase dependencies and quality gates"

✗ BAD: "• PURPOSE ▸ Utilities → See other files" (truncated, not axiomatically dense)

OUTPUT FORMAT:
Return ONLY the annotation line, nothing else. Format:
• PURPOSE ▸ [your axiom] → [your vertical trigger]
"""

    def _build_query_prompt(self, query: str, repository: ScoutRepository) -> str:
        """Build prompt for organization query."""
        return f"""You are SCOUT, a repository librarian. Answer organization queries.

REPOSITORY STRUCTURE:
{json.dumps(repository.structure, indent=2)}

EXISTING ANNOTATIONS:
{json.dumps({k: v.to_dict() for k, v in repository.annotations.items()}, indent=2)}

USER QUERY:
{query}

YOUR TASK:
Analyze the query and provide:
1. Recommended location(s) for the file/directory
2. Reasoning based on repository patterns
3. Related files that should be consulted
4. Suggested directory structure if needed

OUTPUT FORMAT:
```json
{{
  "recommended_path": "path/to/location",
  "reasoning": "explanation of why this location makes sense",
  "related_files": ["file1.py", "file2.py"],
  "directory_structure": {{
    "create_dirs": ["dir1", "dir2"],
    "move_files": {{"old_path": "new_path"}}
  }},
  "consultation_sequence": [
    "First consult file1.py for pattern X",
    "Then reference file2.py for integration Y"
  ]
}}
```
"""

    def _git_commit(
        self, operation: str, files: List[Path], message: Optional[str] = None
    ):
        """Commit changes to git if enabled."""
        if self.git_helper and self.git_helper.is_git_repo:
            self.git_helper.commit_with_codexa_attribution(
                operation=operation, files=files, details=message
            )

    def get_capabilities(self) -> List[str]:
        """Get list of available capabilities."""
        return [
            "scan_repository",
            "create_annotation",
            "annotate_file",
            "annotate_directory",
            "query_organization",
        ]


# Global Scout operations instance
_global_scout_ops: Optional[ScoutOperations] = None


def get_scout_ops(
    auto_backup: bool = True,
    auto_git: bool = True,
    dry_run: bool = False,
    agent_executor: Optional[Any] = None,
) -> ScoutOperations:
    """
    Get or create the global Scout operations instance.

    Args:
        auto_backup: Automatically backup files before modification
        auto_git: Automatically commit changes to git
        dry_run: Preview operations without executing
        agent_executor: Optional agent executor for AI operations

    Returns:
        ScoutOperations instance
    """
    global _global_scout_ops

    if _global_scout_ops is None:
        _global_scout_ops = ScoutOperations(
            auto_backup=auto_backup,
            auto_git=auto_git,
            dry_run=dry_run,
            agent_executor=agent_executor,
        )

    return _global_scout_ops
