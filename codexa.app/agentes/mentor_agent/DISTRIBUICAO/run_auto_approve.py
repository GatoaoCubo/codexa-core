#!/usr/bin/env python3
"""
Wrapper para executar workflow_auto.py com aprovação automática
"""
import subprocess
import sys
from pathlib import Path

# Add config to path for centralized path management
sys.path.insert(0, str(Path(__file__).parent.parent / 'config'))
from paths import PATH_DISTRIBUICAO

def run_workflow_with_auto_approve():
    """Execute workflow and auto-approve all prompts"""

    workflow_script = PATH_DISTRIBUICAO / "workflow_auto.py"

    # Run workflow and pipe 'y' for all prompts
    process = subprocess.Popen(
        [sys.executable, str(workflow_script), "--interactive"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding='utf-8',
        errors='replace',
        cwd=str(PATH_DISTRIBUICAO)
    )

    # Auto-approve by sending 'y' responses
    # Send multiple 'y' to handle all prompts
    auto_responses = "y\n" * 200  # Enough for all possible prompts

    output, _ = process.communicate(input=auto_responses)

    print(output)
    return process.returncode

if __name__ == "__main__":
    exit_code = run_workflow_with_auto_approve()
    sys.exit(exit_code)
