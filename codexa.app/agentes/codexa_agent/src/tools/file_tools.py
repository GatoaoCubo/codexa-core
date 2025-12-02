"""
File Tools
Implements file operations: Read, Write, Edit, Glob, Grep
"""

import asyncio
from pathlib import Path
from typing import Optional, List
import re
import logging

from .executor import ToolError

logger = logging.getLogger(__name__)


class FileTools:
    """File operation tools."""

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize file tools.

        Args:
            base_path: Base directory for file operations (default: cwd)
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()

    async def read(
        self,
        file_path: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None
    ) -> str:
        """
        Read file contents.

        Args:
            file_path: Path to file (absolute or relative to base_path)
            offset: Optional line offset to start reading from
            limit: Optional number of lines to read

        Returns:
            File contents

        Raises:
            ToolError: If file not found or read fails
        """
        try:
            # Resolve path
            path = self._resolve_path(file_path)

            if not path.exists():
                raise ToolError(f"File not found: {file_path}")

            if not path.is_file():
                raise ToolError(f"Not a file: {file_path}")

            # Read file
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                lines = f.readlines()

            # Apply offset and limit
            if offset is not None:
                lines = lines[offset:]

            if limit is not None:
                lines = lines[:limit]

            # Add line numbers (cat -n format)
            numbered_lines = []
            start_line = (offset or 0) + 1

            for i, line in enumerate(lines):
                line_num = start_line + i
                numbered_lines.append(f"{line_num:6d}\t{line.rstrip()}")

            content = '\n'.join(numbered_lines)

            logger.info(f"Read file: {file_path} ({len(lines)} lines)")
            return content

        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"Failed to read file: {e}")

    async def write(
        self,
        file_path: str,
        content: str
    ) -> str:
        """
        Write content to file (overwrites existing).

        Args:
            file_path: Path to file
            content: Content to write

        Returns:
            Success message

        Raises:
            ToolError: If write fails
        """
        try:
            # Resolve path
            path = self._resolve_path(file_path)

            # Create parent directories if needed
            path.parent.mkdir(parents=True, exist_ok=True)

            # Write file
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

            lines = content.count('\n') + 1
            logger.info(f"Wrote file: {file_path} ({lines} lines)")

            return f"Successfully wrote {lines} lines to {file_path}"

        except Exception as e:
            raise ToolError(f"Failed to write file: {e}")

    async def edit(
        self,
        file_path: str,
        old_string: str,
        new_string: str,
        replace_all: bool = False
    ) -> str:
        """
        Edit file by replacing text.

        Args:
            file_path: Path to file
            old_string: Text to find
            new_string: Text to replace with
            replace_all: Replace all occurrences (default: False, only first)

        Returns:
            Success message with number of replacements

        Raises:
            ToolError: If edit fails or old_string not found
        """
        try:
            # Resolve path
            path = self._resolve_path(file_path)

            if not path.exists():
                raise ToolError(f"File not found: {file_path}")

            # Read file
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if old_string exists
            if old_string not in content:
                raise ToolError(f"String not found in file: {old_string[:50]}...")

            # Count occurrences
            count = content.count(old_string)

            # Replace
            if replace_all:
                new_content = content.replace(old_string, new_string)
                replacements = count
            else:
                new_content = content.replace(old_string, new_string, 1)
                replacements = 1

            # Write back
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            logger.info(f"Edited file: {file_path} ({replacements} replacements)")

            return f"Successfully replaced {replacements} occurrence(s) in {file_path}"

        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"Failed to edit file: {e}")

    async def glob(
        self,
        pattern: str,
        path: Optional[str] = None
    ) -> List[str]:
        """
        Find files matching glob pattern.

        Args:
            pattern: Glob pattern (e.g., "**/*.py", "src/*.js")
            path: Optional directory to search in (default: base_path)

        Returns:
            List of matching file paths

        Raises:
            ToolError: If glob fails
        """
        try:
            # Resolve search path
            search_path = self._resolve_path(path) if path else self.base_path

            if not search_path.is_dir():
                raise ToolError(f"Not a directory: {path or self.base_path}")

            # Execute glob
            matches = list(search_path.glob(pattern))

            # Convert to strings, sort by modification time (newest first)
            file_paths = []
            for match in matches:
                if match.is_file():
                    file_paths.append(str(match.relative_to(self.base_path)))

            file_paths.sort(key=lambda p: Path(self.base_path / p).stat().st_mtime, reverse=True)

            logger.info(f"Glob pattern '{pattern}' matched {len(file_paths)} files")

            return file_paths

        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"Failed to glob: {e}")

    async def grep(
        self,
        pattern: str,
        path: Optional[str] = None,
        file_type: Optional[str] = None,
        glob_pattern: Optional[str] = None,
        output_mode: str = "files_with_matches",
        case_insensitive: bool = False,
        context_lines: int = 0
    ) -> str:
        """
        Search for pattern in files.

        Args:
            pattern: Regex pattern to search for
            path: Optional directory/file to search in
            file_type: Optional file type filter (e.g., "py", "js")
            glob_pattern: Optional glob pattern to filter files
            output_mode: "files_with_matches", "content", or "count"
            case_insensitive: Case insensitive search
            context_lines: Number of context lines before/after match

        Returns:
            Search results

        Raises:
            ToolError: If grep fails
        """
        try:
            # Resolve search path
            search_path = self._resolve_path(path) if path else self.base_path

            # Compile regex
            flags = re.IGNORECASE if case_insensitive else 0
            regex = re.compile(pattern, flags)

            # Find files to search
            if search_path.is_file():
                files = [search_path]
            else:
                # Get all files matching glob/type
                if glob_pattern:
                    files = list(search_path.glob(glob_pattern))
                elif file_type:
                    files = list(search_path.glob(f"**/*.{file_type}"))
                else:
                    files = list(search_path.glob("**/*"))

                files = [f for f in files if f.is_file()]

            # Search files
            results = []
            matches_by_file = {}

            for file_path in files:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        lines = f.readlines()

                    file_matches = []
                    for i, line in enumerate(lines):
                        if regex.search(line):
                            file_matches.append((i + 1, line.rstrip()))

                    if file_matches:
                        rel_path = str(file_path.relative_to(self.base_path))
                        matches_by_file[rel_path] = file_matches

                except Exception as e:
                    logger.warning(f"Failed to search {file_path}: {e}")
                    continue

            # Format output based on mode
            if output_mode == "files_with_matches":
                results = list(matches_by_file.keys())
                output = '\n'.join(results)

            elif output_mode == "count":
                for file_path, matches in matches_by_file.items():
                    results.append(f"{file_path}: {len(matches)}")
                output = '\n'.join(results)

            else:  # content
                for file_path, matches in matches_by_file.items():
                    results.append(f"{file_path}:")
                    for line_num, line in matches:
                        results.append(f"  {line_num}: {line}")
                output = '\n'.join(results)

            logger.info(f"Grep pattern '{pattern}' found matches in {len(matches_by_file)} files")

            return output

        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"Failed to grep: {e}")

    def _resolve_path(self, path: Optional[str]) -> Path:
        """Resolve path relative to base_path."""
        if not path:
            return self.base_path

        p = Path(path)

        if p.is_absolute():
            return p
        else:
            return self.base_path / p
