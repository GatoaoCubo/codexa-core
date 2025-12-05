#!/usr/bin/env python3
"""
SubagentStop Hook - Metrics collection and TTS notification for subagent completion.

This hook fires when any subagent (Task tool) completes execution.
It detects the subagent type, logs metrics, and optionally announces completion via TTS.

Version: 1.0.0
Created: 2025-12-05
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Subagent types (built-in + custom CODEXA agents)
SUBAGENT_TYPES = [
    # Built-in Claude Code types
    "general-purpose",
    "Explore",
    "Plan",
    "claude-code-guide",
    # Custom CODEXA types
    "pesquisa-agent",
    "anuncio-agent",
    "marca-agent",
    "photo-agent",
    "video-agent",
    "curso-agent",
    "mentor-agent",
    "voice-agent",
    "codexa-agent",
    "scout-agent",
    "qa-agent",
    "ronronalda-agent",
]

# TTS messages per agent type (Portuguese BR)
TTS_MESSAGES = {
    "pesquisa-agent": "Pesquisa concluída",
    "anuncio-agent": "Anúncio gerado",
    "marca-agent": "Estratégia de marca pronta",
    "photo-agent": "Prompts de foto criados",
    "video-agent": "Vídeo processado",
    "curso-agent": "Conteúdo do curso gerado",
    "mentor-agent": "Lição preparada",
    "voice-agent": "Comando de voz processado",
    "codexa-agent": "Construção concluída",
    "scout-agent": "Arquivos encontrados",
    "qa-agent": "Validação completa",
    "ronronalda-agent": "Tarefa concluída",
    "general-purpose": "Tarefa concluída",
    "Explore": "Exploração concluída",
    "Plan": "Planejamento concluído",
    "claude-code-guide": "Documentação consultada",
}

# Metrics file path
METRICS_FILE = Path(__file__).parent.parent / "subagent_metrics.json"


def detect_subagent_type(hook_data: dict) -> str:
    """
    Detect the subagent type from hook data.

    Checks:
    1. Explicit subagent_type in tool input
    2. Keywords in task description/prompt
    3. Default to general-purpose
    """
    # Check for explicit type in input
    tool_input = hook_data.get("tool_input", {})
    if isinstance(tool_input, dict):
        explicit_type = tool_input.get("subagent_type", "")
        if explicit_type in SUBAGENT_TYPES:
            return explicit_type

    # Check for custom agent keywords in description or prompt
    description = str(tool_input.get("description", "")).lower() if isinstance(tool_input, dict) else ""
    prompt = str(tool_input.get("prompt", "")).lower() if isinstance(tool_input, dict) else ""
    combined = f"{description} {prompt}"

    # Keyword mapping
    keywords = {
        "pesquisa-agent": ["pesquisa", "research", "market research", "competitor"],
        "anuncio-agent": ["anuncio", "anúncio", "listing", "copywriting", "marketplace"],
        "marca-agent": ["marca", "brand", "branding", "identity"],
        "photo-agent": ["photo", "foto", "photography", "image prompt", "midjourney"],
        "video-agent": ["video", "vídeo", "storyboard", "script", "runway"],
        "curso-agent": ["curso", "course", "hotmart", "workbook", "lesson"],
        "mentor-agent": ["mentor", "teach", "ensina", "aula"],
        "voice-agent": ["voice", "voz", "speak", "listen"],
        "codexa-agent": ["codexa", "meta-construction", "build agent", "create hop"],
        "scout-agent": ["scout", "discover", "find files", "path"],
        "qa-agent": ["qa", "validation", "quality", "check"],
    }

    for agent_type, agent_keywords in keywords.items():
        if any(kw in combined for kw in agent_keywords):
            return agent_type

    return "general-purpose"


def load_metrics() -> dict:
    """Load existing metrics or create new structure."""
    if METRICS_FILE.exists():
        try:
            with open(METRICS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    return {
        "by_type": {},
        "total_executions": 0,
        "last_updated": None,
    }


def save_metrics(metrics: dict) -> None:
    """Save metrics to file."""
    metrics["last_updated"] = datetime.now().isoformat()
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2, ensure_ascii=False)


def collect_metrics(agent_type: str, hook_data: dict) -> None:
    """Collect and save execution metrics."""
    metrics = load_metrics()

    # Initialize type if not exists
    if agent_type not in metrics["by_type"]:
        metrics["by_type"][agent_type] = {
            "count": 0,
            "last_execution": None,
            "executions": [],
        }

    # Update counters
    metrics["total_executions"] += 1
    metrics["by_type"][agent_type]["count"] += 1
    metrics["by_type"][agent_type]["last_execution"] = datetime.now().isoformat()

    # Store execution details (keep last 10)
    execution = {
        "timestamp": datetime.now().isoformat(),
        "description": hook_data.get("tool_input", {}).get("description", ""),
    }
    metrics["by_type"][agent_type]["executions"].append(execution)
    metrics["by_type"][agent_type]["executions"] = metrics["by_type"][agent_type]["executions"][-10:]

    save_metrics(metrics)


def announce_completion(agent_type: str) -> None:
    """Announce subagent completion via TTS (if voice MCP available)."""
    message = TTS_MESSAGES.get(agent_type, "Tarefa concluída")

    # Try to use voice MCP if available
    # This is a no-op if voice is not configured
    try:
        # Import dynamically to avoid hard dependency
        import subprocess

        # Check if we should announce (controlled by --notify flag)
        if "--notify" not in sys.argv:
            return

        # Use edge-tts for quick announcement
        voice_script = Path(__file__).parent.parent.parent / "codexa.app" / "voice" / "tts.py"
        if voice_script.exists():
            subprocess.run(
                [sys.executable, str(voice_script), message],
                capture_output=True,
                timeout=5,
            )
    except Exception:
        pass  # Silent fail if TTS not available


def main():
    """Main hook entry point."""
    # Read hook data from stdin
    try:
        hook_data = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, IOError):
        hook_data = {}

    # Detect agent type
    agent_type = detect_subagent_type(hook_data)

    # Collect metrics
    collect_metrics(agent_type, hook_data)

    # Announce if --notify flag is present
    announce_completion(agent_type)

    # Output for Claude Code
    print(json.dumps({
        "status": "ok",
        "agent_type": agent_type,
        "message": TTS_MESSAGES.get(agent_type, "Tarefa concluída"),
    }))


if __name__ == "__main__":
    main()
