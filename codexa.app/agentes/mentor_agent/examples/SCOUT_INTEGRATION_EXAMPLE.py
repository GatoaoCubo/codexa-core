#!/usr/bin/env python3
"""
SCOUT Integration - Live Example and Test Suite.

 PURPOSE  Demonstrate practical SCOUT integration patterns for all agent types through executable examples and validation tests  Reference SCOUT_INTEGRATION_GUIDE.md for complete integration workflows

This file serves as:
1. Live demonstration of SCOUT integration patterns
2. Test suite for SCOUT integration module
3. Template for agent developers

Run this file to see SCOUT integration in action!

Usage:
    python adws/adws/SCOUT_INTEGRATION_EXAMPLE.py
"""

import asyncio
import sys
import os
from pathlib import Path

# Add adws to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "adw_modules"))

from scout_integration import (
    prepare_scout_context,
    with_scout_context,
    query_scout,
    extract_related_files,
    get_repository_stats,
    prepare_scout_context_sync,
    is_cache_fresh,
)


# ============================================================================
# EXAMPLE 1: Automatic Context Injection (Decorator Pattern)
# ============================================================================

@with_scout_context
async def example_research_agent(research_topic: str, scout_context=None):
    """
    Example research agent with automatic SCOUT context.

    This is the RECOMMENDED pattern for most agents.
    The decorator automatically injects scout_context.
    """
    print("=" * 70)
    print("EXAMPLE 1: Automatic Context Injection (@with_scout_context)")
    print("=" * 70)

    # Check if SCOUT context loaded successfully
    if not scout_context.get('success'):
        print(f"[X] SCOUT context failed: {scout_context.get('error')}")
        return None

    # Display context information
    from_cache = scout_context.get('from_cache', False)
    cache_status = "[CACHE]" if from_cache else "[SCAN]"
    print(f"{cache_status} SCOUT context loaded (from_cache: {from_cache})")

    # Get repository statistics
    stats = scout_context.get('stats', {})
    print(f"\n[STATS] Repository Statistics:")
    print(f"   Total Files: {stats.get('total_files', 0)}")
    print(f"   Total Directories: {stats.get('total_dirs', 0)}")
    print(f"   File Types: {len(stats.get('file_types', {}))}")

    # Show top file types
    file_types = stats.get('file_types', {})
    if file_types:
        print(f"\n[FILES] Top 5 File Types:")
        sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:5]
        for ext, count in sorted_types:
            print(f"   {ext}: {count}")

    # Find files related to research topic
    print(f"\n[SEARCH] Finding files related to '{research_topic}':")
    related_files = extract_related_files(
        scout_context,
        pattern=f"*{research_topic}*.py"
    )

    if related_files:
        print(f"   Found {len(related_files)} related files:")
        for f in related_files[:5]:  # Show first 5
            print(f"    {f}")
        if len(related_files) > 5:
            print(f"   ... and {len(related_files) - 5} more")
    else:
        print(f"   No files found matching pattern '*{research_topic}*.py'")

    # Simulate research work
    print(f"\n[OK] Research agent completed for topic: {research_topic}")

    return {
        'topic': research_topic,
        'files_analyzed': len(related_files),
        'repository_size': stats.get('total_files', 0),
    }


# ============================================================================
# EXAMPLE 2: Manual Context Preparation
# ============================================================================

async def example_build_agent(build_target: str):
    """
    Example build agent with manual SCOUT context preparation.

    This pattern gives you more control over when and how SCOUT is called.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Manual Context Preparation")
    print("=" * 70)

    # Manually prepare SCOUT context
    print("[SCAN] Preparing SCOUT context...")
    scout_context = await prepare_scout_context(working_dir=".")

    # Check success
    if not scout_context.get('success'):
        print(f"[X] SCOUT preparation failed: {scout_context.get('error')}")
        print("[WARN]  Falling back to manual file discovery...")
        # Implement fallback logic here
        return None

    # Successfully loaded
    from_cache = scout_context.get('from_cache', False)
    print(f"[OK] SCOUT context ready (from_cache: {from_cache})")

    # Get all Python files
    all_files = scout_context.get('structure', {}).get('files', [])
    python_files = [f for f in all_files if f.endswith('.py')]

    print(f"\n[BUILD] Build Information:")
    print(f"   Target: {build_target}")
    print(f"   Total Python files: {len(python_files)}")

    # Find build-related files
    build_files = [f for f in python_files if 'build' in f.lower()]
    print(f"   Build scripts found: {len(build_files)}")

    if build_files:
        print(f"\n[TOOLS] Build Scripts:")
        for f in build_files:
            print(f"    {f}")

    # Simulate build
    print(f"\n[OK] Build agent completed for target: {build_target}")

    return {
        'target': build_target,
        'python_files': len(python_files),
        'build_scripts': len(build_files),
    }


# ============================================================================
# EXAMPLE 3: Query-Driven Navigation
# ============================================================================

async def example_refactor_agent(refactor_query: str):
    """
    Example refactoring agent that queries SCOUT for guidance.

    This pattern is useful for dynamic file discovery and organization decisions.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Query-Driven Navigation")
    print("=" * 70)

    print(f"[?] Querying SCOUT: '{refactor_query}'")

    # Query SCOUT (this also prepares context if needed)
    try:
        result = await query_scout(
            query_text=refactor_query,
            working_dir=".",
            model="sonnet"
        )

        if result.get('success'):
            print("[OK] SCOUT query successful!")

            query_result = result.get('result', {})

            # Display recommended path
            if 'recommended_path' in query_result:
                print(f"\n[PATH] Recommended Path:")
                print(f"   {query_result['recommended_path']}")

            # Display reasoning
            if 'reasoning' in query_result:
                print(f"\n[INFO] Reasoning:")
                print(f"   {query_result['reasoning']}")

            # Display related files
            if 'related_files' in query_result:
                related = query_result['related_files']
                print(f"\n[DIR] Related Files ({len(related)}):")
                for f in related[:5]:
                    print(f"    {f}")

            # Display consultation sequence
            if 'consultation_sequence' in query_result:
                sequence = query_result['consultation_sequence']
                print(f"\n[LINK] Consultation Sequence:")
                for i, step in enumerate(sequence, 1):
                    print(f"   {i}. {step}")

            return query_result
        else:
            print(f"[X] SCOUT query failed: {result.get('error')}")
            return None

    except Exception as e:
        print(f"[X] Query error: {str(e)}")
        return None


# ============================================================================
# EXAMPLE 4: Helper Functions
# ============================================================================

async def example_analysis_agent():
    """
    Example analysis agent using SCOUT helper functions.

    Demonstrates how to use utility functions for common operations.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Helper Functions")
    print("=" * 70)

    # Prepare context
    scout_context = await prepare_scout_context()

    if not scout_context.get('success'):
        print(f"[X] SCOUT preparation failed")
        return None

    print("[OK] SCOUT context ready")

    # Helper 1: Extract related files
    print("\n[SCAN] Helper: extract_related_files()")

    agent_files = extract_related_files(
        scout_context,
        pattern="*agent*",
        extension=".py"
    )
    print(f"   Found {len(agent_files)} agent files")

    research_files = extract_related_files(
        scout_context,
        pattern="*research*"
    )
    print(f"   Found {len(research_files)} research files")

    # Helper 2: Get repository stats
    print("\n[STATS] Helper: get_repository_stats()")

    stats = get_repository_stats(scout_context)
    print(f"   Total files: {stats.get('total_files', 0)}")
    print(f"   Total directories: {stats.get('total_dirs', 0)}")

    file_types = stats.get('file_types', {})
    print(f"   File types: {len(file_types)}")

    return {
        'agent_files': len(agent_files),
        'research_files': len(research_files),
        'stats': stats,
    }


# ============================================================================
# EXAMPLE 5: Synchronous Usage (for non-async code)
# ============================================================================

def example_sync_agent():
    """
    Example showing synchronous usage of SCOUT.

    For agents that don't use async/await.
    """
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Synchronous Usage")
    print("=" * 70)

    # Use synchronous wrapper
    print("[SCAN] Preparing SCOUT context (sync)...")

    scout_context = prepare_scout_context_sync(working_dir=".")

    if scout_context.get('success'):
        print("[OK] SCOUT context loaded (synchronous)")

        stats = get_repository_stats(scout_context)
        print(f"\n[STATS] Quick Stats:")
        print(f"   Files: {stats.get('total_files', 0)}")
        print(f"   Dirs: {stats.get('total_dirs', 0)}")

        return stats
    else:
        print(f"[X] Failed: {scout_context.get('error')}")
        return None


# ============================================================================
# TEST SUITE
# ============================================================================

async def run_test_suite():
    """Run comprehensive test suite for SCOUT integration."""

    print("\n" + "=" * 70)
    print("[TEST] SCOUT INTEGRATION TEST SUITE")
    print("=" * 70)

    tests_passed = 0
    tests_failed = 0

    # Test 1: Cache freshness check
    print("\n[TEST 1] Cache freshness check")
    try:
        cache_path = ".scout_cache.json"
        is_fresh = is_cache_fresh(cache_path, max_age_hours=24)
        print(f"   Cache exists and is fresh: {is_fresh}")
        tests_passed += 1
    except Exception as e:
        print(f"   [X] Failed: {e}")
        tests_failed += 1

    # Test 2: Context preparation
    print("\n[TEST 2] Context preparation")
    try:
        context = await prepare_scout_context()
        assert context.get('enabled') == True, "Context should be enabled"
        print(f"   [OK] Context enabled: {context.get('enabled')}")
        print(f"   [OK] Context success: {context.get('success')}")
        tests_passed += 1
    except Exception as e:
        print(f"   [X] Failed: {e}")
        tests_failed += 1

    # Test 3: File extraction
    print("\n[TEST 3] File extraction")
    try:
        context = await prepare_scout_context()
        if context.get('success'):
            py_files = extract_related_files(context, extension=".py")
            print(f"   [OK] Found {len(py_files)} Python files")
            tests_passed += 1
        else:
            print(f"   [WARN]  Skipped (context not available)")
    except Exception as e:
        print(f"   [X] Failed: {e}")
        tests_failed += 1

    # Test 4: Stats retrieval
    print("\n[TEST 4] Stats retrieval")
    try:
        context = await prepare_scout_context()
        stats = get_repository_stats(context)
        assert isinstance(stats, dict), "Stats should be a dict"
        print(f"   [OK] Stats retrieved: {len(stats)} keys")
        tests_passed += 1
    except Exception as e:
        print(f"   [X] Failed: {e}")
        tests_failed += 1

    # Summary
    print("\n" + "=" * 70)
    print(f"[TEST] TEST RESULTS: {tests_passed} passed, {tests_failed} failed")
    print("=" * 70)

    return tests_passed, tests_failed


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Main execution function - runs all examples."""

    print("\n")
    print("+" + "=" * 68 + "+")
    print("|" + " " * 15 + "SCOUT INTEGRATION EXAMPLES" + " " * 27 + "|")
    print("|" + " " * 15 + "Live Demonstration Suite" + " " * 29 + "|")
    print("+" + "=" * 68 + "+")

    # Example 1: Decorator pattern
    result1 = await example_research_agent("agent")

    # Example 2: Manual preparation
    result2 = await example_build_agent("production")

    # Example 3: Query-driven (note: requires Claude API, may fail gracefully)
    # Uncomment to test:
    # result3 = await example_refactor_agent("Where should I place authentication handlers?")

    # Example 4: Helper functions
    result4 = await example_analysis_agent()

    # Example 5: Synchronous usage (commented out due to event loop conflict)
    # result5 = example_sync_agent()
    print("\n[SKIP] Example 5 skipped (sync incompatible with async event loop)")

    # Run test suite
    await run_test_suite()

    # Final summary
    print("\n" + "=" * 70)
    print("[OK] ALL EXAMPLES COMPLETED")
    print("=" * 70)
    print("\n Next Steps:")
    print("   1. Review SCOUT_INTEGRATION_GUIDE.md for detailed patterns")
    print("   2. Choose a pattern that fits your agent")
    print("   3. Integrate SCOUT into your agent code")
    print("   4. Test with cache hit and cache miss scenarios")
    print("\n")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
