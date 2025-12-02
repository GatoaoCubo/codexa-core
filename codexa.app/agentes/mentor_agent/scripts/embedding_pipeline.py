#!/usr/bin/env python3
"""
CODEXA Knowledge Base Embedding Pipeline

Production-ready RAG system for CODEXA multi-agent knowledge base.
Indexes 1741 files across 13 agents using semantic embeddings.

Features:
- Semantic chunking by markdown sections
- Local embeddings (sentence-transformers, no API)
- ChromaDB vector storage
- Incremental updates
- Token counting and metadata
- Progress tracking and logging

Usage:
    python embedding_pipeline.py --index              # Full reindex
    python embedding_pipeline.py --search "query"    # Search
    python embedding_pipeline.py --stats             # Show stats
    python embedding_pipeline.py --update            # Incremental update
"""

import argparse
import glob
import hashlib
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from collections import defaultdict

# Check dependencies
try:
    from sentence_transformers import SentenceTransformer
    import chromadb
    from chromadb.config import Settings
    import tiktoken
    from tqdm import tqdm
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    print("\n📦 Install required packages:")
    print("pip install sentence-transformers chromadb tiktoken tqdm")
    sys.exit(1)

# Constants
PROJECT_ROOT = Path(__file__).resolve().parents[4]  # codexa.gato root
AGENTES_PATH = PROJECT_ROOT / "codexa.app" / "agentes"
VECTOR_STORE_PATH = AGENTES_PATH / "mentor_agent" / "FONTES" / "knowledge_vectors"
KNOWLEDGE_GRAPH_PATH = AGENTES_PATH / "mentor_agent" / "FONTES" / "knowledge_graph.json"

# Embedding configuration
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # 384 dimensions, fast, good quality
COLLECTION_NAME = "codexa_knowledge"
MAX_CHUNK_TOKENS = 1000
OVERLAP_TOKENS = 100
BATCH_SIZE = 32

# File categories to include/exclude
INCLUDE_CATEGORIES = {
    "fontes", "iso_vectorstore", "hop", "processados",
    "knowledge", "patterns", "workflows", "adw", "prompts",
    "docs", "architecture", "core", "context", "guide"
}
EXCLUDE_CATEGORIES = {
    "outputs", "rascunho", "user_output", "test", "example"
}
EXCLUDE_DIRS = {
    ".git", "node_modules", "__pycache__", ".cache",
    "outputs", "user_output", ".vscode"
}

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(VECTOR_STORE_PATH / "pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ChunkMetadata:
    """Metadata for document chunks"""
    def __init__(self, file_path: str, agent: str, category: str,
                 section_title: str, chunk_index: int, total_chunks: int,
                 token_count: int, file_hash: str):
        self.file_path = file_path
        self.agent = agent
        self.category = category
        self.section_title = section_title
        self.chunk_index = chunk_index
        self.total_chunks = total_chunks
        self.token_count = token_count
        self.file_hash = file_hash
        self.indexed_at = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "file_path": self.file_path,
            "agent": self.agent,
            "category": self.category,
            "section_title": self.section_title,
            "chunk_index": self.chunk_index,
            "total_chunks": self.total_chunks,
            "token_count": self.token_count,
            "file_hash": self.file_hash,
            "indexed_at": self.indexed_at
        }


class MarkdownChunker:
    """Smart markdown chunking by sections with token limits"""

    def __init__(self, max_tokens: int = MAX_CHUNK_TOKENS, overlap: int = OVERLAP_TOKENS):
        self.max_tokens = max_tokens
        self.overlap = overlap
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.tokenizer.encode(text))

    def split_by_headers(self, content: str) -> List[Tuple[str, str]]:
        """Split markdown by headers, return [(title, content)]"""
        sections = []
        current_title = "Introduction"
        current_content = []

        lines = content.split('\n')
        for line in lines:
            # Match markdown headers ## or ###
            header_match = re.match(r'^(#{2,3})\s+(.+)$', line)
            if header_match:
                # Save previous section
                if current_content:
                    sections.append((current_title, '\n'.join(current_content)))
                # Start new section
                current_title = header_match.group(2).strip()
                current_content = [line]
            else:
                current_content.append(line)

        # Save last section
        if current_content:
            sections.append((current_title, '\n'.join(current_content)))

        return sections

    def chunk_section(self, title: str, content: str) -> List[Tuple[str, str]]:
        """Chunk a section if it exceeds max tokens"""
        tokens = self.count_tokens(content)

        if tokens <= self.max_tokens:
            return [(title, content)]

        # Split long section into chunks with overlap
        chunks = []
        lines = content.split('\n')
        current_chunk = []
        current_tokens = 0

        for line in lines:
            line_tokens = self.count_tokens(line)

            if current_tokens + line_tokens > self.max_tokens and current_chunk:
                # Save current chunk
                chunk_content = '\n'.join(current_chunk)
                chunks.append((f"{title} (part {len(chunks) + 1})", chunk_content))

                # Start new chunk with overlap
                overlap_lines = []
                overlap_tokens = 0
                for prev_line in reversed(current_chunk):
                    prev_tokens = self.count_tokens(prev_line)
                    if overlap_tokens + prev_tokens <= self.overlap:
                        overlap_lines.insert(0, prev_line)
                        overlap_tokens += prev_tokens
                    else:
                        break

                current_chunk = overlap_lines + [line]
                current_tokens = overlap_tokens + line_tokens
            else:
                current_chunk.append(line)
                current_tokens += line_tokens

        # Save last chunk
        if current_chunk:
            chunk_content = '\n'.join(current_chunk)
            chunks.append((f"{title} (part {len(chunks) + 1})", chunk_content))

        return chunks

    def chunk_document(self, content: str) -> List[Tuple[str, str, int]]:
        """
        Chunk entire document, return [(title, content, tokens)]
        """
        sections = self.split_by_headers(content)
        all_chunks = []

        for title, section_content in sections:
            section_chunks = self.chunk_section(title, section_content)
            for chunk_title, chunk_content in section_chunks:
                tokens = self.count_tokens(chunk_content)
                all_chunks.append((chunk_title, chunk_content, tokens))

        return all_chunks


class EmbeddingPipeline:
    """Main embedding pipeline orchestrator"""

    def __init__(self):
        # Initialize paths
        self.vector_store_path = VECTOR_STORE_PATH
        self.vector_store_path.mkdir(parents=True, exist_ok=True)

        # Initialize components
        logger.info(f"🚀 Loading embedding model: {EMBEDDING_MODEL}")
        self.model = SentenceTransformer(EMBEDDING_MODEL)

        logger.info(f"💾 Initializing ChromaDB at {self.vector_store_path}")
        self.client = chromadb.PersistentClient(
            path=str(self.vector_store_path),
            settings=Settings(anonymized_telemetry=False)
        )

        self.chunker = MarkdownChunker()
        self.collection = None

        # Load knowledge graph
        self.knowledge_graph = self._load_knowledge_graph()

    def _load_knowledge_graph(self) -> Dict:
        """Load knowledge graph for metadata"""
        if KNOWLEDGE_GRAPH_PATH.exists():
            with open(KNOWLEDGE_GRAPH_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _get_or_create_collection(self):
        """Get or create ChromaDB collection"""
        try:
            self.collection = self.client.get_collection(
                name=COLLECTION_NAME,
                embedding_function=None  # We'll provide embeddings manually
            )
            logger.info(f"📚 Loaded existing collection: {COLLECTION_NAME}")
        except:
            self.collection = self.client.create_collection(
                name=COLLECTION_NAME,
                embedding_function=None,
                metadata={"description": "CODEXA multi-agent knowledge base"}
            )
            logger.info(f"✨ Created new collection: {COLLECTION_NAME}")

    def _discover_files(self) -> List[Path]:
        """Discover all markdown files to index"""
        logger.info(f"🔍 Discovering files in {AGENTES_PATH}")

        all_files = []
        for agent_dir in AGENTES_PATH.iterdir():
            if not agent_dir.is_dir() or agent_dir.name.startswith('.'):
                continue

            # Find all .md files
            for md_file in agent_dir.rglob("*.md"):
                # Check if in excluded directory
                if any(exc in md_file.parts for exc in EXCLUDE_DIRS):
                    continue

                # Categorize file
                category = self._categorize_file(md_file)
                if category in EXCLUDE_CATEGORIES:
                    continue

                all_files.append(md_file)

        logger.info(f"📁 Found {len(all_files)} markdown files to index")
        return sorted(all_files)

    def _categorize_file(self, file_path: Path) -> str:
        """Determine file category from path"""
        parts = file_path.parts

        # Check for known category directories
        for category in INCLUDE_CATEGORIES | EXCLUDE_CATEGORIES:
            if category.upper() in parts or category.lower() in parts:
                return category.lower()

        # Check filename patterns
        name_lower = file_path.name.lower()
        if '_HOP.md' in file_path.name:
            return "hop"
        elif 'ADW_' in file_path.name:
            return "adw"
        elif name_lower in ['readme.md', 'instructions.md', 'prime.md']:
            return file_path.stem.lower()

        return "other"

    def _get_agent_name(self, file_path: Path) -> str:
        """Extract agent name from file path"""
        parts = file_path.parts
        agentes_idx = parts.index("agentes") if "agentes" in parts else -1

        if agentes_idx >= 0 and agentes_idx + 1 < len(parts):
            return parts[agentes_idx + 1]

        return "unknown"

    def _compute_file_hash(self, file_path: Path) -> str:
        """Compute MD5 hash of file for change detection"""
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()

    def _process_file(self, file_path: Path) -> List[Tuple[str, str, ChunkMetadata]]:
        """Process a single file into chunks with metadata"""
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if not content.strip():
                return []

            # Extract metadata
            agent = self._get_agent_name(file_path)
            category = self._categorize_file(file_path)
            file_hash = self._compute_file_hash(file_path)
            relative_path = str(file_path.relative_to(PROJECT_ROOT))

            # Chunk document
            chunks = self.chunker.chunk_document(content)
            total_chunks = len(chunks)

            # Create chunks with metadata
            processed_chunks = []
            for idx, (title, chunk_content, tokens) in enumerate(chunks):
                chunk_id = f"{file_hash}_{idx}"
                metadata = ChunkMetadata(
                    file_path=relative_path,
                    agent=agent,
                    category=category,
                    section_title=title,
                    chunk_index=idx,
                    total_chunks=total_chunks,
                    token_count=tokens,
                    file_hash=file_hash
                )
                processed_chunks.append((chunk_id, chunk_content, metadata))

            return processed_chunks

        except Exception as e:
            logger.error(f"❌ Error processing {file_path}: {e}")
            return []

    def _embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for batch of texts"""
        embeddings = self.model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()

    def index_full(self):
        """Full reindex of all files"""
        logger.info("🔄 Starting full reindex...")

        # Get or create collection
        self._get_or_create_collection()

        # Clear existing data
        try:
            self.client.delete_collection(COLLECTION_NAME)
            logger.info("🗑️  Cleared existing collection")
        except:
            pass

        self._get_or_create_collection()

        # Discover files
        files = self._discover_files()

        # Process files
        all_chunks = []
        stats = defaultdict(int)

        logger.info("📝 Processing files...")
        for file_path in tqdm(files, desc="Processing"):
            chunks = self._process_file(file_path)
            all_chunks.extend(chunks)

            # Update stats
            agent = self._get_agent_name(file_path)
            category = self._categorize_file(file_path)
            stats[f"agent:{agent}"] += len(chunks)
            stats[f"category:{category}"] += len(chunks)

        stats["total_files"] = len(files)
        stats["total_chunks"] = len(all_chunks)

        # Batch embed and store
        logger.info(f"🧮 Embedding {len(all_chunks)} chunks...")

        for i in tqdm(range(0, len(all_chunks), BATCH_SIZE), desc="Embedding"):
            batch = all_chunks[i:i + BATCH_SIZE]

            # Extract data
            chunk_ids = [c[0] for c in batch]
            texts = [c[1] for c in batch]
            metadatas = [c[2].to_dict() for c in batch]

            # Generate embeddings
            embeddings = self._embed_batch(texts)

            # Store in ChromaDB
            self.collection.add(
                ids=chunk_ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )

        # Save stats
        stats["indexed_at"] = datetime.now().isoformat()
        stats_path = self.vector_store_path / "index_stats.json"
        with open(stats_path, 'w') as f:
            json.dump(dict(stats), f, indent=2)

        logger.info(f"✅ Indexing complete!")
        logger.info(f"   📊 Files: {stats['total_files']}")
        logger.info(f"   📦 Chunks: {stats['total_chunks']}")
        logger.info(f"   💾 Stored at: {self.vector_store_path}")

        return stats

    def search(self, query: str, n_results: int = 10, filter_agent: Optional[str] = None) -> List[Dict]:
        """Search knowledge base"""
        self._get_or_create_collection()

        # Generate query embedding
        query_embedding = self.model.encode([query])[0].tolist()

        # Build filter
        where_filter = None
        if filter_agent:
            where_filter = {"agent": filter_agent}

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter
        )

        # Format results
        formatted_results = []
        for idx, (doc_id, document, metadata, distance) in enumerate(zip(
            results['ids'][0],
            results['documents'][0],
            results['metadatas'][0],
            results['distances'][0]
        )):
            formatted_results.append({
                "rank": idx + 1,
                "score": 1 / (1 + distance),  # Convert distance to similarity
                "file": metadata['file_path'],
                "agent": metadata['agent'],
                "category": metadata['category'],
                "section": metadata['section_title'],
                "tokens": metadata['token_count'],
                "content": document[:200] + "..." if len(document) > 200 else document
            })

        return formatted_results

    def get_stats(self) -> Dict:
        """Get index statistics"""
        self._get_or_create_collection()

        count = self.collection.count()

        # Load saved stats
        stats_path = self.vector_store_path / "index_stats.json"
        if stats_path.exists():
            with open(stats_path, 'r') as f:
                saved_stats = json.load(f)
        else:
            saved_stats = {}

        return {
            "total_chunks": count,
            "collection_name": COLLECTION_NAME,
            "embedding_model": EMBEDDING_MODEL,
            "vector_store_path": str(self.vector_store_path),
            **saved_stats
        }

    def update_incremental(self):
        """Incremental update: only reindex changed files"""
        logger.info("🔄 Starting incremental update...")

        self._get_or_create_collection()

        # Get all indexed file hashes
        all_metadata = self.collection.get()
        indexed_hashes = {}
        for metadata in all_metadata['metadatas']:
            file_path = metadata['file_path']
            file_hash = metadata['file_hash']
            if file_path not in indexed_hashes:
                indexed_hashes[file_path] = file_hash

        # Discover current files
        files = self._discover_files()

        # Check for changes
        files_to_update = []
        for file_path in files:
            relative_path = str(file_path.relative_to(PROJECT_ROOT))
            current_hash = self._compute_file_hash(file_path)

            if relative_path not in indexed_hashes or indexed_hashes[relative_path] != current_hash:
                files_to_update.append(file_path)

        if not files_to_update:
            logger.info("✅ No changes detected. Index is up to date.")
            return {"updated_files": 0}

        logger.info(f"📝 Updating {len(files_to_update)} changed files...")

        # Remove old chunks for changed files
        for file_path in files_to_update:
            relative_path = str(file_path.relative_to(PROJECT_ROOT))
            # Delete old chunks
            try:
                results = self.collection.get(where={"file_path": relative_path})
                if results['ids']:
                    self.collection.delete(ids=results['ids'])
            except:
                pass

        # Process and add new chunks
        all_chunks = []
        for file_path in tqdm(files_to_update, desc="Processing"):
            chunks = self._process_file(file_path)
            all_chunks.extend(chunks)

        # Batch embed and store
        for i in tqdm(range(0, len(all_chunks), BATCH_SIZE), desc="Embedding"):
            batch = all_chunks[i:i + BATCH_SIZE]

            chunk_ids = [c[0] for c in batch]
            texts = [c[1] for c in batch]
            metadatas = [c[2].to_dict() for c in batch]

            embeddings = self._embed_batch(texts)

            self.collection.add(
                ids=chunk_ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )

        logger.info(f"✅ Incremental update complete!")
        logger.info(f"   📝 Updated files: {len(files_to_update)}")
        logger.info(f"   📦 New chunks: {len(all_chunks)}")

        return {
            "updated_files": len(files_to_update),
            "new_chunks": len(all_chunks)
        }


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(
        description="CODEXA Knowledge Base Embedding Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full reindex
  python embedding_pipeline.py --index

  # Search knowledge base
  python embedding_pipeline.py --search "how to create a subagent"

  # Filter search by agent
  python embedding_pipeline.py --search "video prompts" --agent video_agent

  # Show statistics
  python embedding_pipeline.py --stats

  # Incremental update
  python embedding_pipeline.py --update
        """
    )

    parser.add_argument('--index', action='store_true',
                       help='Full reindex of knowledge base')
    parser.add_argument('--search', type=str, metavar='QUERY',
                       help='Search knowledge base')
    parser.add_argument('--agent', type=str, metavar='AGENT',
                       help='Filter search by agent')
    parser.add_argument('--stats', action='store_true',
                       help='Show index statistics')
    parser.add_argument('--update', action='store_true',
                       help='Incremental update (only changed files)')
    parser.add_argument('--results', type=int, default=10, metavar='N',
                       help='Number of search results (default: 10)')

    args = parser.parse_args()

    # Initialize pipeline
    pipeline = EmbeddingPipeline()

    # Execute command
    if args.index:
        stats = pipeline.index_full()

    elif args.search:
        results = pipeline.search(
            query=args.search,
            n_results=args.results,
            filter_agent=args.agent
        )

        print(f"\n🔍 Search results for: '{args.search}'")
        if args.agent:
            print(f"   Filtered by agent: {args.agent}")
        print(f"   Found {len(results)} results\n")

        for result in results:
            print(f"[{result['rank']}] {result['file']}")
            print(f"    Agent: {result['agent']} | Category: {result['category']}")
            print(f"    Section: {result['section']}")
            print(f"    Score: {result['score']:.3f} | Tokens: {result['tokens']}")
            print(f"    {result['content']}")
            print()

    elif args.stats:
        stats = pipeline.get_stats()

        print("\n📊 Knowledge Base Statistics\n")
        print(f"Collection: {stats['collection_name']}")
        print(f"Model: {stats['embedding_model']}")
        print(f"Path: {stats['vector_store_path']}")
        print(f"\nTotal chunks: {stats['total_chunks']}")

        if 'total_files' in stats:
            print(f"Total files: {stats['total_files']}")

        if 'indexed_at' in stats:
            print(f"Last indexed: {stats['indexed_at']}")

        # Show breakdown by agent
        agent_stats = {k: v for k, v in stats.items() if k.startswith('agent:')}
        if agent_stats:
            print("\nBy agent:")
            for agent, count in sorted(agent_stats.items(), key=lambda x: x[1], reverse=True):
                agent_name = agent.replace('agent:', '')
                print(f"  {agent_name:20} {count:6} chunks")

        # Show breakdown by category
        category_stats = {k: v for k, v in stats.items() if k.startswith('category:')}
        if category_stats:
            print("\nBy category:")
            for category, count in sorted(category_stats.items(), key=lambda x: x[1], reverse=True):
                category_name = category.replace('category:', '')
                print(f"  {category_name:20} {count:6} chunks")

    elif args.update:
        result = pipeline.update_incremental()

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
