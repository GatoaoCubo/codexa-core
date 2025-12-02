#!/usr/bin/env python3
"""
KEYWORD SEARCH - Alternativa ao Embedding Pipeline
===================================================

Funciona em QUALQUER versão do Python (sem dependências ML).
Usa busca por palavras-chave no Knowledge Graph.

Quando Python 3.12/3.13 tiver suporte completo para ChromaDB,
usar embedding_pipeline.py para busca semântica.

Usage:
    python keyword_search.py "criar subagent"
    python keyword_search.py "market research" --format json
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Tuple


# Paths
SCRIPT_DIR = Path(__file__).parent
FONTES_DIR = SCRIPT_DIR.parent / "FONTES"
KNOWLEDGE_GRAPH = FONTES_DIR / "knowledge_graph.json"
PROJECT_ROOT = SCRIPT_DIR.parent.parent.parent.parent


def load_knowledge_graph() -> Dict:
    """Load the knowledge graph configuration."""
    if not KNOWLEDGE_GRAPH.exists():
        print(f"ERROR: Knowledge graph not found at {KNOWLEDGE_GRAPH}")
        sys.exit(1)

    with open(KNOWLEDGE_GRAPH, "r", encoding="utf-8") as f:
        return json.load(f)


def tokenize(text: str) -> List[str]:
    """Tokenize text into normalized words."""
    text = text.lower()
    # Remove punctuation
    text = re.sub(r'[^\w\s]', ' ', text)
    # Split and filter
    tokens = [t.strip() for t in text.split() if len(t.strip()) > 2]
    return tokens


def match_task_type(query: str, knowledge_graph: Dict) -> Tuple[str, float]:
    """Match query to best task type using keyword matching."""
    query_tokens = set(tokenize(query))

    best_match = None
    best_score = 0.0

    for task_type, config in knowledge_graph.get("task_types", {}).items():
        triggers = config.get("triggers", [])

        # Score based on trigger matches
        score = 0.0
        for trigger in triggers:
            trigger_tokens = set(tokenize(trigger))
            overlap = len(query_tokens & trigger_tokens)
            if overlap > 0:
                score += overlap / max(len(trigger_tokens), 1)

        # Bonus for task_type name match
        task_tokens = set(tokenize(task_type.replace("_", " ")))
        task_overlap = len(query_tokens & task_tokens)
        score += task_overlap * 0.5

        if score > best_score:
            best_score = score
            best_match = task_type

    return best_match, best_score


def get_knowledge_files(task_type: str, knowledge_graph: Dict) -> Dict[str, List[str]]:
    """Get required and recommended files for a task type."""
    config = knowledge_graph.get("task_types", {}).get(task_type, {})

    return {
        "required": config.get("required_knowledge", []),
        "recommended": config.get("recommended_knowledge", []),
        "cross_agent_sources": config.get("cross_agent_sources", []),
        "primary_agent": config.get("primary_agent", "unknown")
    }


def resolve_paths(files: List[str], project_root: Path) -> List[Dict]:
    """Resolve file paths and check existence."""
    resolved = []
    for f in files:
        # Try multiple path variations
        variations = [
            project_root / f,
            project_root / "agentes" / f,
            project_root / "codexa.app" / "agentes" / f,
        ]

        found = None
        for path in variations:
            if path.exists():
                found = path
                break

        resolved.append({
            "path": f,
            "exists": found is not None,
            "resolved_path": str(found) if found else None
        })

    return resolved


def search(query: str, output_format: str = "text") -> Dict:
    """
    Main search function.

    Args:
        query: Natural language query
        output_format: "text" or "json"

    Returns:
        Search results with matched files
    """
    kg = load_knowledge_graph()

    # Match task type
    task_type, confidence = match_task_type(query, kg)

    if not task_type:
        return {
            "success": False,
            "error": "No matching task type found",
            "query": query
        }

    # Get knowledge files
    knowledge = get_knowledge_files(task_type, kg)

    # Resolve paths
    required_resolved = resolve_paths(knowledge["required"], PROJECT_ROOT)
    recommended_resolved = resolve_paths(knowledge["recommended"], PROJECT_ROOT)

    result = {
        "success": True,
        "query": query,
        "matched_task_type": task_type,
        "confidence": round(confidence, 2),
        "primary_agent": knowledge["primary_agent"],
        "cross_agent_sources": knowledge["cross_agent_sources"],
        "files": {
            "required": required_resolved,
            "recommended": recommended_resolved
        },
        "total_files": len(required_resolved) + len(recommended_resolved)
    }

    return result


def format_output(result: Dict, output_format: str = "text") -> str:
    """Format search result for display."""
    if output_format == "json":
        return json.dumps(result, indent=2, ensure_ascii=False)

    # Text format
    lines = []
    lines.append("=" * 60)
    lines.append("KNOWLEDGE SEARCH RESULTS")
    lines.append("=" * 60)
    lines.append(f"Query: {result['query']}")
    lines.append(f"Matched Task: {result.get('matched_task_type', 'None')}")
    lines.append(f"Confidence: {result.get('confidence', 0):.0%}")
    lines.append(f"Primary Agent: {result.get('primary_agent', 'unknown')}")
    lines.append("")

    if result.get("cross_agent_sources"):
        lines.append(f"Cross-Agent Sources: {', '.join(result['cross_agent_sources'])}")
        lines.append("")

    lines.append("REQUIRED FILES:")
    for f in result.get("files", {}).get("required", []):
        status = "[OK]" if f.get("exists") else "[X]"
        lines.append(f"  {status} {f['path']}")

    lines.append("")
    lines.append("RECOMMENDED FILES:")
    for f in result.get("files", {}).get("recommended", []):
        status = "[OK]" if f.get("exists") else "[X]"
        lines.append(f"  {status} {f['path']}")

    lines.append("")
    lines.append(f"Total: {result.get('total_files', 0)} files")
    lines.append("=" * 60)

    return "\n".join(lines)


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python keyword_search.py <query> [--format json]")
        print("")
        print("Examples:")
        print("  python keyword_search.py 'criar subagent'")
        print("  python keyword_search.py 'market research' --format json")
        print("  python keyword_search.py 'prompt engineering patterns'")
        sys.exit(1)

    query = sys.argv[1]
    output_format = "json" if "--format" in sys.argv and "json" in sys.argv else "text"

    result = search(query, output_format)
    print(format_output(result, output_format))


if __name__ == "__main__":
    main()
