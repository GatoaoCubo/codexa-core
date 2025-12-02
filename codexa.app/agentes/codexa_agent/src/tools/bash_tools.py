"""
Bash Tools
Implements command execution with safety and timeout controls.
"""

import asyncio
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
import logging
import shlex

from .executor import ToolError

logger = logging.getLogger(__name__)


class BashTools:
    """Bash command execution tools."""

    def __init__(
        self,
        base_path: Optional[Path] = None,
        max_timeout: int = 300,
        allowed_commands: Optional[list] = None
    ):
        """
        Initialize bash tools.

        Args:
            base_path: Base directory for command execution (default: cwd)
            max_timeout: Maximum timeout in seconds (default: 300s/5min)
            allowed_commands: Optional whitelist of allowed commands
        """
        self.base_path = Path(base_path) if base_path else Path.cwd()
        self.max_timeout = max_timeout
        self.allowed_commands = allowed_commands

    async def execute(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: int = 30,
        capture_output: bool = True,
        env: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Execute bash command.

        Args:
            command: Command to execute
            cwd: Optional working directory (default: base_path)
            timeout: Timeout in seconds (default: 30s, max: max_timeout)
            capture_output: Capture stdout/stderr (default: True)
            env: Optional environment variables

        Returns:
            Command output (stdout + stderr)

        Raises:
            ToolError: If command fails or times out
        """
        try:
            # Validate timeout
            if timeout > self.max_timeout:
                raise ToolError(
                    f"Timeout {timeout}s exceeds maximum {self.max_timeout}s"
                )

            # Check command whitelist if configured
            if self.allowed_commands:
                command_name = shlex.split(command)[0]
                if command_name not in self.allowed_commands:
                    raise ToolError(
                        f"Command '{command_name}' not in allowed list"
                    )

            # Resolve working directory
            work_dir = self._resolve_path(cwd) if cwd else self.base_path

            if not work_dir.exists():
                raise ToolError(f"Working directory does not exist: {work_dir}")

            if not work_dir.is_dir():
                raise ToolError(f"Not a directory: {work_dir}")

            logger.info(f"Executing command: {command} (cwd: {work_dir})")

            # Execute command
            process = await asyncio.create_subprocess_shell(
                command,
                cwd=str(work_dir),
                stdout=subprocess.PIPE if capture_output else None,
                stderr=subprocess.PIPE if capture_output else None,
                env=env
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                raise ToolError(
                    f"Command timed out after {timeout}s: {command[:50]}..."
                )

            # Format output
            output_lines = []

            if capture_output:
                if stdout:
                    stdout_text = stdout.decode('utf-8', errors='replace')
                    if stdout_text.strip():
                        output_lines.append("=== STDOUT ===")
                        output_lines.append(stdout_text.rstrip())

                if stderr:
                    stderr_text = stderr.decode('utf-8', errors='replace')
                    if stderr_text.strip():
                        output_lines.append("=== STDERR ===")
                        output_lines.append(stderr_text.rstrip())

            # Check return code
            if process.returncode != 0:
                error_msg = f"Command failed with exit code {process.returncode}"
                if output_lines:
                    error_msg += "\n" + "\n".join(output_lines)
                raise ToolError(error_msg)

            result = "\n".join(output_lines) if output_lines else "[No output]"

            logger.info(
                f"Command succeeded: exit_code=0, "
                f"output_length={len(result)}"
            )

            return result

        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"Failed to execute command: {e}")

    async def execute_script(
        self,
        script_content: str,
        cwd: Optional[str] = None,
        timeout: int = 60,
        shell: str = "/bin/bash"
    ) -> str:
        """
        Execute a bash script from content.

        Args:
            script_content: Script content to execute
            cwd: Optional working directory
            timeout: Timeout in seconds
            shell: Shell to use (default: /bin/bash)

        Returns:
            Script output

        Raises:
            ToolError: If script fails
        """
        try:
            # Resolve working directory
            work_dir = self._resolve_path(cwd) if cwd else self.base_path

            logger.info(f"Executing script ({len(script_content)} bytes)")

            # Execute script via stdin
            process = await asyncio.create_subprocess_exec(
                shell,
                cwd=str(work_dir),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            try:
                stdout, stderr = await asyncio.wait_for(
                    process.communicate(input=script_content.encode('utf-8')),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                raise ToolError(f"Script timed out after {timeout}s")

            # Format output
            output_lines = []

            if stdout:
                stdout_text = stdout.decode('utf-8', errors='replace')
                if stdout_text.strip():
                    output_lines.append("=== STDOUT ===")
                    output_lines.append(stdout_text.rstrip())

            if stderr:
                stderr_text = stderr.decode('utf-8', errors='replace')
                if stderr_text.strip():
                    output_lines.append("=== STDERR ===")
                    output_lines.append(stderr_text.rstrip())

            # Check return code
            if process.returncode != 0:
                error_msg = f"Script failed with exit code {process.returncode}"
                if output_lines:
                    error_msg += "\n" + "\n".join(output_lines)
                raise ToolError(error_msg)

            result = "\n".join(output_lines) if output_lines else "[No output]"

            logger.info(f"Script succeeded: exit_code=0")

            return result

        except ToolError:
            raise
        except Exception as e:
            raise ToolError(f"Failed to execute script: {e}")

    async def check_command_exists(self, command: str) -> bool:
        """
        Check if a command exists in PATH.

        Args:
            command: Command name to check

        Returns:
            True if command exists, False otherwise
        """
        try:
            result = await self.execute(
                f"command -v {shlex.quote(command)}",
                capture_output=True,
                timeout=5
            )
            return bool(result.strip())
        except ToolError:
            return False

    def _resolve_path(self, path: Optional[str]) -> Path:
        """Resolve path relative to base_path."""
        if not path:
            return self.base_path

        p = Path(path)

        if p.is_absolute():
            return p
        else:
            return self.base_path / p
