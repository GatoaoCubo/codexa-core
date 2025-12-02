#!/usr/bin/env python3
"""
Simple knowledge base search wrapper

Easy-to-use interface for searching CODEXA knowledge base.
Can be imported or used as CLI.

Usage:
    # As CLI
    python search_knowledge.py "how to create subagent"

    # In Python
    from search_knowledge import search_kb
    results = search_kb("prompt patterns", agent="video_agent", top_k=5)
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional

# Add script directory to path
sys.path.insert(0, str(Path(__file__).parent))


def search_kb(
    query: str,
    top_k: int = 5,
    agent: Optional[str] = None,
    category: Optional[str] = None,
    min_score: float = 0.0,
    return_content: bool = False
) -> List[Dict]:
    """
    Search CODEXA knowledge base

    Args:
        query: Search query string
        top_k: Number of results to return
        agent: Filter by agent name (e.g., "video_agent")
        category: Filter by category (e.g., "hop", "fontes")
        min_score: Minimum similarity score (0.0 to 1.0)
        return_content: If True, include full content in results

    Returns:
        List of result dictionaries with:
        - file: File path
        - agent: Agent name
        - category: Category
        - section: Section title
        - score: Similarity score
        - tokens: Token count
        - content: Content snippet or full content

    Example:
        >>> results = search_kb("how to create HOP", top_k=3)
        >>> for r in results:
        ...     print(f"{r['file']}: {r['section']} (score: {r['score']:.2f})")
    """
    try:
        from embedding_pipeline import EmbeddingPipeline
    except ImportError:
        raise ImportError(
            "embedding_pipeline not found. Make sure you're in the scripts directory."
        )

    # Initialize pipeline
    pipeline = EmbeddingPipeline()

    # Search
    results = pipeline.search(
        query=query,
        n_results=top_k,
        filter_agent=agent
    )

    # Post-process results
    filtered_results = []
    for result in results:
        # Apply score filter
        if result['score'] < min_score:
            continue

        # Apply category filter
        if category and result['category'] != category:
            continue

        # Optionally include full content
        if not return_content:
            # Truncate content to snippet
            content = result['content']
            if len(content) > 200:
                content = content[:200] + "..."
            result['content'] = content

        filtered_results.append(result)

    return filtered_results


def search_similar_to_file(
    file_path: str,
    top_k: int = 5,
    exclude_same_file: bool = True
) -> List[Dict]:
    """
    Find files similar to a given file

    Args:
        file_path: Path to file (relative to project root)
        top_k: Number of results to return
        exclude_same_file: If True, exclude the source file from results

    Returns:
        List of similar files with scores
    """
    from embedding_pipeline import EmbeddingPipeline

    # Read file content
    full_path = Path(__file__).parents[4] / file_path
    if not full_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Use first 500 chars as query
    query = content[:500]

    # Search
    pipeline = EmbeddingPipeline()
    results = pipeline.search(query=query, n_results=top_k + 5)

    # Filter out same file if requested
    if exclude_same_file:
        results = [r for r in results if r['file'] != file_path]

    return results[:top_k]


def search_by_agent(agent_name: str, query: str, top_k: int = 5) -> List[Dict]:
    """
    Search within a specific agent's knowledge

    Args:
        agent_name: Agent name (e.g., "video_agent")
        query: Search query
        top_k: Number of results

    Returns:
        List of results from the specified agent
    """
    return search_kb(query=query, top_k=top_k, agent=agent_name)


def search_by_category(category: str, query: str, top_k: int = 5) -> List[Dict]:
    """
    Search within a specific category

    Args:
        category: Category name (e.g., "hop", "fontes", "iso_vectorstore")
        query: Search query
        top_k: Number of results

    Returns:
        List of results from the specified category
    """
    return search_kb(query=query, top_k=top_k, category=category)


def format_results(results: List[Dict], show_content: bool = True) -> str:
    """
    Format search results as readable text

    Args:
        results: List of result dictionaries
        show_content: If True, include content snippets

    Returns:
        Formatted string
    """
    if not results:
        return "No results found."

    output = []
    for r in results:
        output.append(f"[{r['rank']}] {r['file']}")
        output.append(f"    Agent: {r['agent']:15} | Category: {r['category']:15}")
        output.append(f"    Section: {r['section']}")
        output.append(f"    Score: {r['score']:.3f} | Tokens: {r['tokens']}")

        if show_content:
            output.append(f"    {r['content']}")

        output.append("")  # Blank line

    return "\n".join(output)


def main():
    """CLI interface"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Search CODEXA knowledge base",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic search
  python search_knowledge.py "how to create subagent"

  # Filter by agent
  python search_knowledge.py "video prompts" --agent video_agent

  # More results
  python search_knowledge.py "prompt patterns" --top-k 20

  # Find similar files
  python search_knowledge.py --similar-to "codexa.app/agentes/video_agent/prompts/10_concept_planner_HOP.md"
        """
    )

    parser.add_argument('query', nargs='?', help='Search query')
    parser.add_argument('--top-k', type=int, default=10,
                       help='Number of results (default: 10)')
    parser.add_argument('--agent', type=str,
                       help='Filter by agent')
    parser.add_argument('--category', type=str,
                       help='Filter by category')
    parser.add_argument('--min-score', type=float, default=0.0,
                       help='Minimum similarity score (0.0-1.0)')
    parser.add_argument('--no-content', action='store_true',
                       help='Hide content snippets')
    parser.add_argument('--similar-to', type=str,
                       help='Find files similar to given file path')

    args = parser.parse_args()

    # Mode: similar files
    if args.similar_to:
        try:
            results = search_similar_to_file(
                file_path=args.similar_to,
                top_k=args.top_k
            )
            print(f"\n🔍 Files similar to: {args.similar_to}\n")
            print(format_results(results, show_content=not args.no_content))
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1

    # Mode: search
    elif args.query:
        try:
            results = search_kb(
                query=args.query,
                top_k=args.top_k,
                agent=args.agent,
                category=args.category,
                min_score=args.min_score
            )

            print(f"\n🔍 Search results for: '{args.query}'")
            if args.agent:
                print(f"   Filtered by agent: {args.agent}")
            if args.category:
                print(f"   Filtered by category: {args.category}")
            print(f"   Found {len(results)} results\n")

            print(format_results(results, show_content=not args.no_content))
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1

    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
