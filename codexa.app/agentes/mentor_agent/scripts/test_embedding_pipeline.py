#!/usr/bin/env python3
"""
Quick test script for embedding pipeline

Tests basic functionality without full indexing.
"""

import sys
from pathlib import Path

# Add script directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all dependencies are installed"""
    print("🧪 Testing imports...")
    try:
        from sentence_transformers import SentenceTransformer
        print("  ✓ sentence-transformers")
    except ImportError:
        print("  ✗ sentence-transformers - run: pip install sentence-transformers")
        return False

    try:
        import chromadb
        print("  ✓ chromadb")
    except ImportError:
        print("  ✗ chromadb - run: pip install chromadb")
        return False

    try:
        import tiktoken
        print("  ✓ tiktoken")
    except ImportError:
        print("  ✗ tiktoken - run: pip install tiktoken")
        return False

    try:
        from tqdm import tqdm
        print("  ✓ tqdm")
    except ImportError:
        print("  ✗ tqdm - run: pip install tqdm")
        return False

    return True


def test_chunker():
    """Test markdown chunking"""
    print("\n🧪 Testing markdown chunker...")

    from embedding_pipeline import MarkdownChunker

    chunker = MarkdownChunker(max_tokens=100, overlap=20)

    sample_doc = """# Test Document

## Introduction

This is a test document to verify chunking works correctly.

## Section One

This is the first section with some content.
It has multiple lines.

## Section Two

This is the second section.
It also has content.

### Subsection

Even subsections work.
"""

    chunks = chunker.chunk_document(sample_doc)

    print(f"  ✓ Created {len(chunks)} chunks")

    for idx, (title, content, tokens) in enumerate(chunks):
        print(f"    Chunk {idx + 1}: '{title}' ({tokens} tokens)")

    return len(chunks) > 0


def test_file_discovery():
    """Test file discovery"""
    print("\n🧪 Testing file discovery...")

    from embedding_pipeline import EmbeddingPipeline

    pipeline = EmbeddingPipeline()
    files = pipeline._discover_files()

    print(f"  ✓ Found {len(files)} markdown files")

    # Show sample files
    sample_size = min(5, len(files))
    print(f"\n  Sample files:")
    for file_path in files[:sample_size]:
        agent = pipeline._get_agent_name(file_path)
        category = pipeline._categorize_file(file_path)
        print(f"    {file_path.name:40} | {agent:15} | {category}")

    return len(files) > 0


def test_embedding():
    """Test embedding generation"""
    print("\n🧪 Testing embedding generation...")

    from embedding_pipeline import EmbeddingPipeline

    pipeline = EmbeddingPipeline()

    test_texts = [
        "This is a test document about subagents.",
        "How to create a video prompt.",
        "Quality validation patterns."
    ]

    embeddings = pipeline._embed_batch(test_texts)

    print(f"  ✓ Generated embeddings for {len(test_texts)} texts")
    print(f"  ✓ Embedding dimensions: {len(embeddings[0])}")

    return len(embeddings) == len(test_texts)


def test_metadata():
    """Test metadata extraction"""
    print("\n🧪 Testing metadata extraction...")

    from embedding_pipeline import EmbeddingPipeline
    import tempfile
    from pathlib import Path

    pipeline = EmbeddingPipeline()

    # Create a temporary test file
    test_content = """# Test File

## Section 1

Content here.
"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False, encoding='utf-8') as f:
        f.write(test_content)
        test_file = Path(f.name)

    try:
        # Mock file path to look like it's in the project
        chunks = pipeline._process_file(test_file)

        if chunks:
            print(f"  ✓ Processed file into {len(chunks)} chunks")

            chunk_id, content, metadata = chunks[0]
            print(f"  ✓ Metadata fields:")
            metadata_dict = metadata.to_dict()
            for key, value in metadata_dict.items():
                print(f"    {key:20} : {value}")

            return True
        else:
            print(f"  ✗ No chunks generated")
            return False

    finally:
        # Cleanup
        test_file.unlink()


def main():
    """Run all tests"""
    print("=" * 60)
    print("CODEXA Embedding Pipeline Test Suite")
    print("=" * 60)

    tests = [
        ("Imports", test_imports),
        ("Markdown Chunker", test_chunker),
        ("File Discovery", test_file_discovery),
        ("Embedding Generation", test_embedding),
        ("Metadata Extraction", test_metadata),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n  ✗ Error: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status:8} {name}")

    print(f"\nResults: {passed}/{total} tests passed")

    if passed == total:
        print("\n✅ All tests passed! Pipeline is ready to use.")
        print("\nNext steps:")
        print("  1. Run full index: python embedding_pipeline.py --index")
        print("  2. Search: python embedding_pipeline.py --search 'your query'")
        print("  3. View stats: python embedding_pipeline.py --stats")
        return 0
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
