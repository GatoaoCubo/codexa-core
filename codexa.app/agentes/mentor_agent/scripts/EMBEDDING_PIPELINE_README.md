# CODEXA Knowledge Base Embedding Pipeline

Production-ready RAG (Retrieval-Augmented Generation) system for the CODEXA multi-agent knowledge base.

## Overview

This pipeline indexes 1741+ files across 13 agents using semantic embeddings, enabling powerful semantic search across the entire knowledge base.

### Features

- **Semantic Chunking**: Intelligent markdown section-based chunking
- **Local Embeddings**: Uses `sentence-transformers` (no API required)
- **Vector Storage**: ChromaDB for persistent vector storage
- **Incremental Updates**: Only reindex changed files
- **Token Counting**: Tracks token usage with tiktoken
- **Progress Tracking**: Real-time progress bars and logging
- **Git Hooks**: Auto-update on git pull/merge

### Architecture

```
embedding_pipeline.py
│
├─ File Discovery
│  └─ Scans 13 agents × ~130 files each
│  └─ Filters by category (fontes, hop, adw, etc.)
│
├─ Markdown Chunking
│  └─ Split by headers (##, ###)
│  └─ Max 1000 tokens/chunk, 100 token overlap
│  └─ Preserves section structure
│
├─ Embedding Generation
│  └─ Model: all-MiniLM-L6-v2 (384 dimensions)
│  └─ Batch processing (32 docs/batch)
│  └─ Local inference (no API calls)
│
└─ Vector Storage
   └─ ChromaDB persistent storage
   └─ Metadata: file, agent, category, section
   └─ Path: mentor_agent/FONTES/knowledge_vectors/
```

## Installation

### 1. Install Dependencies

```bash
cd codexa.app/agentes/mentor_agent/scripts
pip install -r requirements.txt
```

Dependencies:
- `sentence-transformers` - Local embedding model
- `chromadb` - Vector database
- `tiktoken` - Token counting
- `tqdm` - Progress bars

### 2. Setup Auto-Update Hook (Optional)

```bash
bash setup_auto_update_hook.sh
```

This installs a git post-merge hook that automatically updates embeddings after `git pull`.

## Usage

### Full Reindex

Index all knowledge files from scratch:

```bash
python embedding_pipeline.py --index
```

Output:
```
🚀 Loading embedding model: all-MiniLM-L6-v2
💾 Initializing ChromaDB at .../knowledge_vectors
🔍 Discovering files in .../agentes
📁 Found 1741 markdown files to index
📝 Processing files... 100%|██████████| 1741/1741
🧮 Embedding 8234 chunks... 100%|██████████| 258/258
✅ Indexing complete!
   📊 Files: 1741
   📦 Chunks: 8234
   💾 Stored at: .../knowledge_vectors
```

**When to use**: First time setup, or after major knowledge base restructuring.

### Search Knowledge Base

Search with semantic similarity:

```bash
# Basic search
python embedding_pipeline.py --search "how to create a subagent"

# Filter by agent
python embedding_pipeline.py --search "video prompts" --agent video_agent

# More results
python embedding_pipeline.py --search "prompt patterns" --results 20
```

Output:
```
🔍 Search results for: 'how to create a subagent'
   Found 10 results

[1] codexa.app/agentes/codexa_agent/iso_vectorstore/23_subagent_patterns.md
    Agent: codexa_agent | Category: iso_vectorstore
    Section: Subagent Construction Pattern
    Score: 0.892 | Tokens: 456
    A subagent is a specialized Claude Code agent spawned using the Task tool...

[2] codexa.app/agentes/mentor_agent/FONTES/PROMPT_ENGINEERING/playbook_prompt_engineering_20251201.md
    Agent: mentor_agent | Category: fontes
    Section: Task Management Patterns
    Score: 0.856 | Tokens: 723
    Task tools enable meta-construction: agents that build agents...
```

### Show Statistics

```bash
python embedding_pipeline.py --stats
```

Output:
```
📊 Knowledge Base Statistics

Collection: codexa_knowledge
Model: all-MiniLM-L6-v2
Path: .../knowledge_vectors

Total chunks: 8234
Total files: 1741
Last indexed: 2025-12-02T15:30:00

By agent:
  mentor_agent          1823 chunks
  codexa_agent          1456 chunks
  video_agent           1089 chunks
  curso_agent            987 chunks
  ...

By category:
  fontes                2134 chunks
  iso_vectorstore       1876 chunks
  hop                    542 chunks
  processados            789 chunks
  ...
```

### Incremental Update

Update only changed files (faster):

```bash
python embedding_pipeline.py --update
```

Output:
```
🔄 Starting incremental update...
📝 Updating 3 changed files...
Processing... 100%|██████████| 3/3
Embedding... 100%|██████████| 2/2
✅ Incremental update complete!
   📝 Updated files: 3
   📦 New chunks: 14
```

**When to use**: After editing files, before `git pull`, or automatically via git hook.

## Configuration

### File Categories

**Included categories** (will be indexed):
- `fontes` - Source knowledge
- `iso_vectorstore` - Isolated knowledge cards
- `hop` - Higher-Order Prompts
- `processados` - Processed knowledge
- `knowledge` - Agent-specific knowledge
- `patterns` - Design patterns
- `workflows` - ADWs
- `prompts` - Prompt templates
- `docs`, `architecture`, `core`, `context`, `guide`

**Excluded categories** (will be skipped):
- `outputs`, `rascunho`, `user_output` - User/temp files
- `test`, `example` - Test/example files

### Chunking Parameters

Adjust in code if needed:

```python
MAX_CHUNK_TOKENS = 1000    # Max tokens per chunk
OVERLAP_TOKENS = 100       # Overlap between chunks
BATCH_SIZE = 32            # Embedding batch size
```

### Embedding Model

Default: `all-MiniLM-L6-v2` (384 dimensions, fast, good quality)

Alternative models (edit `EMBEDDING_MODEL` in code):
- `all-mpnet-base-v2` - Better quality, slower (768 dims)
- `multi-qa-MiniLM-L6-cos-v1` - Optimized for Q&A
- `paraphrase-multilingual-MiniLM-L12-v2` - Multilingual

## Integration with Agents

### In Python Scripts

```python
from embedding_pipeline import EmbeddingPipeline

# Initialize
pipeline = EmbeddingPipeline()

# Search
results = pipeline.search(
    query="How to create a HOP",
    n_results=5,
    filter_agent="codexa_agent"
)

for result in results:
    print(f"{result['file']}: {result['section']}")
    print(f"Score: {result['score']:.3f}")
    print(f"{result['content']}\n")
```

### In Agents (via subprocess)

```python
import subprocess
import json

# Search
result = subprocess.run(
    ["python", "scripts/embedding_pipeline.py", "--search", query],
    capture_output=True,
    text=True
)

# Parse output
# (Note: output is formatted text, not JSON. Use for display.)
print(result.stdout)
```

### In HOPs

```markdown
## Knowledge Discovery

Before implementing, search the knowledge base:

```bash
python scripts/embedding_pipeline.py --search "{{task_description}}"
```

Use top results as context for implementation.
```

## File Structure

```
mentor_agent/
├── scripts/
│   ├── embedding_pipeline.py          # Main pipeline
│   ├── requirements.txt               # Dependencies
│   ├── setup_auto_update_hook.sh      # Git hook installer
│   └── EMBEDDING_PIPELINE_README.md   # This file
│
└── FONTES/
    └── knowledge_vectors/             # Vector storage (auto-created)
        ├── chroma.sqlite3             # ChromaDB database
        ├── index_stats.json           # Index statistics
        └── pipeline.log               # Operation logs
```

## Performance

### Indexing Speed

- **Full index**: ~15-20 minutes for 1741 files
- **Incremental update**: ~30 seconds for 10 changed files
- **Search**: <100ms per query

### Resource Usage

- **Disk**: ~50MB for vectors + metadata
- **RAM**: ~2GB during indexing, ~500MB during search
- **CPU**: Multi-threaded embedding generation

### Optimization Tips

1. **Use incremental updates** instead of full reindex
2. **Run full reindex overnight** or in background
3. **Filter by agent** to speed up search
4. **Adjust batch size** based on available RAM

## Troubleshooting

### Error: "Missing dependency"

```bash
pip install -r scripts/requirements.txt
```

### Error: "No such file or directory"

Make sure you're running from the correct directory:

```bash
cd codexa.app/agentes/mentor_agent/scripts
python embedding_pipeline.py --index
```

### Search returns no results

1. Check if index exists: `python embedding_pipeline.py --stats`
2. If empty, run: `python embedding_pipeline.py --index`
3. Try broader search terms

### Slow indexing

- Reduce `BATCH_SIZE` if running out of memory
- Use `--update` instead of `--index` for faster updates
- Consider using a faster embedding model (but larger size)

### Git hook not working

1. Check if hook is executable: `ls -la .git/hooks/post-merge`
2. If not: `chmod +x .git/hooks/post-merge`
3. Test manually: `.git/hooks/post-merge`

## Advanced Usage

### Custom Filters

Edit `_discover_files()` to add custom file patterns:

```python
# Include only specific agents
AGENTS_TO_INDEX = {"codexa_agent", "mentor_agent", "video_agent"}

for agent_dir in AGENTES_PATH.iterdir():
    if agent_dir.name not in AGENTS_TO_INDEX:
        continue
    # ... rest of logic
```

### Export Results to JSON

```python
results = pipeline.search(query="...", n_results=10)

import json
with open("search_results.json", "w") as f:
    json.dump(results, f, indent=2)
```

### Batch Search

```python
queries = [
    "How to create subagents",
    "Video prompt patterns",
    "Quality validation"
]

for query in queries:
    print(f"\n=== {query} ===")
    results = pipeline.search(query, n_results=3)
    for r in results:
        print(f"  {r['file']}")
```

## Future Enhancements

- [ ] Web UI for search interface
- [ ] REST API endpoint
- [ ] Multi-modal embeddings (code + docs)
- [ ] Question answering with LLM integration
- [ ] Automatic knowledge graph generation
- [ ] Cross-reference analysis
- [ ] Embedding visualization (t-SNE/UMAP)

## Related Files

- `knowledge_graph.json` - Task routing and knowledge categories
- `catalogo_fontes.json` - Source file catalog
- `fontes.py` - Knowledge processing script

## Support

For issues or questions:
1. Check this README
2. Review `pipeline.log` for errors
3. Run with verbose logging: `python -u embedding_pipeline.py --index`
4. Check ChromaDB docs: https://docs.trychroma.com/

---

**Version**: 1.0.0
**Created**: 2025-12-02
**Author**: CODEXA System
**License**: Internal Use
