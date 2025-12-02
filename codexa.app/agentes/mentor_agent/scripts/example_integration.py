#!/usr/bin/env python3
"""
Example integration of embedding pipeline with CODEXA agents

Shows how to use semantic search in agent workflows.
"""

import sys
from pathlib import Path

# Add script directory to path
sys.path.insert(0, str(Path(__file__).parent))

from search_knowledge import search_kb, search_by_agent, search_similar_to_file


def example_1_basic_search():
    """Example 1: Basic knowledge search"""
    print("=" * 60)
    print("Example 1: Basic Knowledge Search")
    print("=" * 60 + "\n")

    query = "how to create a subagent in Claude Code"
    results = search_kb(query, top_k=3)

    print(f"Query: {query}\n")
    print(f"Found {len(results)} results:\n")

    for r in results:
        print(f"[{r['rank']}] {r['section']}")
        print(f"    File: {r['file']}")
        print(f"    Score: {r['score']:.3f}")
        print()


def example_2_agent_specific():
    """Example 2: Search within specific agent"""
    print("=" * 60)
    print("Example 2: Agent-Specific Search")
    print("=" * 60 + "\n")

    query = "video prompt patterns"
    agent = "video_agent"
    results = search_by_agent(agent, query, top_k=3)

    print(f"Query: {query}")
    print(f"Agent: {agent}\n")
    print(f"Found {len(results)} results:\n")

    for r in results:
        print(f"[{r['rank']}] {r['section']}")
        print(f"    Category: {r['category']}")
        print(f"    Score: {r['score']:.3f}")
        print(f"    Preview: {r['content'][:100]}...")
        print()


def example_3_context_injection():
    """Example 3: Context injection for agent tasks"""
    print("=" * 60)
    print("Example 3: Context Injection for Agent Tasks")
    print("=" * 60 + "\n")

    # Simulate an agent receiving a task
    task_description = "Create a new HOP for quality validation"

    print(f"Task: {task_description}\n")
    print("Searching for relevant context...\n")

    # Search for relevant knowledge
    results = search_kb(task_description, top_k=5, min_score=0.6)

    print(f"Found {len(results)} relevant files:\n")

    # Build context for agent
    context_files = []
    for r in results:
        context_files.append({
            "file": r['file'],
            "section": r['section'],
            "relevance": r['score']
        })
        print(f"  • {r['file']}")
        print(f"    Section: {r['section']} (relevance: {r['score']:.2f})")

    print("\nThis context would be injected into the agent prompt.")


def example_4_similar_documents():
    """Example 4: Find similar documents"""
    print("=" * 60)
    print("Example 4: Find Similar Documents")
    print("=" * 60 + "\n")

    source_file = "codexa.app/agentes/codexa_agent/iso_vectorstore/23_subagent_patterns.md"

    print(f"Finding files similar to:\n  {source_file}\n")

    try:
        results = search_similar_to_file(source_file, top_k=5)

        print(f"Found {len(results)} similar files:\n")

        for r in results:
            print(f"[{r['rank']}] {r['file']}")
            print(f"    Similarity: {r['score']:.3f}")
            print(f"    Agent: {r['agent']} | Category: {r['category']}")
            print()

    except FileNotFoundError as e:
        print(f"Error: {e}")


def example_5_knowledge_discovery_workflow():
    """Example 5: Complete knowledge discovery workflow"""
    print("=" * 60)
    print("Example 5: Knowledge Discovery Workflow")
    print("=" * 60 + "\n")

    # Step 1: Agent receives task
    task = "Build a new video_agent workflow for product demos"
    print(f"📋 Task: {task}\n")

    # Step 2: Search for workflow patterns
    print("🔍 Step 1: Searching for workflow patterns...\n")
    workflow_results = search_kb("ADW workflow patterns", category="adw", top_k=3)

    print("Found workflow patterns:")
    for r in workflow_results:
        print(f"  • {r['file']}")

    # Step 3: Search for video agent knowledge
    print("\n🔍 Step 2: Searching for video_agent knowledge...\n")
    video_results = search_by_agent("video_agent", "workflow process", top_k=3)

    print("Found video_agent files:")
    for r in video_results:
        print(f"  • {r['file']}")

    # Step 4: Search for prompt patterns
    print("\n🔍 Step 3: Searching for prompt engineering patterns...\n")
    prompt_results = search_kb("prompt engineering best practices", top_k=3)

    print("Found prompt patterns:")
    for r in prompt_results:
        print(f"  • {r['file']}")

    # Step 5: Combine context
    print("\n📚 Step 4: Combining context for agent...\n")

    all_context = workflow_results + video_results + prompt_results

    # Remove duplicates by file path
    seen_files = set()
    unique_context = []
    for r in all_context:
        if r['file'] not in seen_files:
            seen_files.add(r['file'])
            unique_context.append(r)

    print(f"Collected {len(unique_context)} unique context files:")
    for r in sorted(unique_context, key=lambda x: x['score'], reverse=True):
        print(f"  {r['score']:.2f} | {r['file']}")

    print("\n✅ Context ready for agent execution!")


def example_6_batch_queries():
    """Example 6: Batch queries for comprehensive research"""
    print("=" * 60)
    print("Example 6: Batch Queries for Research")
    print("=" * 60 + "\n")

    research_queries = [
        "Task tool usage patterns",
        "File operation best practices",
        "Error handling in agents",
        "Quality validation standards"
    ]

    print("Running batch research queries...\n")

    all_results = {}
    for query in research_queries:
        results = search_kb(query, top_k=2, min_score=0.7)
        all_results[query] = results
        print(f"📊 {query}")
        print(f"   Found {len(results)} high-relevance results")

    print("\n📚 Consolidated Results:\n")

    # Collect all unique files
    all_files = {}
    for query, results in all_results.items():
        for r in results:
            file_path = r['file']
            if file_path not in all_files:
                all_files[file_path] = {
                    "file": file_path,
                    "queries": [],
                    "max_score": 0
                }
            all_files[file_path]["queries"].append((query, r['score']))
            all_files[file_path]["max_score"] = max(
                all_files[file_path]["max_score"],
                r['score']
            )

    # Sort by max score
    sorted_files = sorted(
        all_files.values(),
        key=lambda x: x['max_score'],
        reverse=True
    )

    for item in sorted_files:
        print(f"📄 {item['file']}")
        print(f"   Max score: {item['max_score']:.3f}")
        print(f"   Relevant to: {len(item['queries'])} queries")
        for query, score in item['queries']:
            print(f"     • {query} ({score:.2f})")
        print()


def main():
    """Run all examples"""
    examples = [
        example_1_basic_search,
        example_2_agent_specific,
        example_3_context_injection,
        example_4_similar_documents,
        example_5_knowledge_discovery_workflow,
        example_6_batch_queries
    ]

    print("\n" + "=" * 60)
    print("CODEXA Embedding Pipeline - Integration Examples")
    print("=" * 60 + "\n")

    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
            print()
        except Exception as e:
            print(f"\n❌ Example {i} failed: {e}\n")

    print("=" * 60)
    print("Examples complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("  • Review the code in example_integration.py")
    print("  • Import search_knowledge in your own scripts")
    print("  • Integrate with agent workflows and HOPs")


if __name__ == "__main__":
    main()
