# Embedding Pipeline - Quick Start

Get started with the CODEXA knowledge base embedding pipeline in 5 minutes.

## 1. Install Dependencies

```bash
cd codexa.app/agentes/mentor_agent/scripts
pip install -r requirements.txt
```

This installs:
- `sentence-transformers` - Local embedding model
- `chromadb` - Vector database
- `tiktoken` - Token counting
- `tqdm` - Progress bars

## 2. Run Tests (Optional)

Verify everything is working:

```bash
python test_embedding_pipeline.py
```

Expected output:
```
✓ PASS   Imports
✓ PASS   Markdown Chunker
✓ PASS   File Discovery
✓ PASS   Embedding Generation
✓ PASS   Metadata Extraction

Results: 5/5 tests passed
✅ All tests passed! Pipeline is ready to use.
```

## 3. Index Knowledge Base

First-time indexing (takes ~15-20 minutes):

```bash
python embedding_pipeline.py --index
```

This will:
- Discover 1741+ markdown files across 13 agents
- Chunk documents by markdown sections
- Generate embeddings using all-MiniLM-L6-v2
- Store in ChromaDB at `FONTES/knowledge_vectors/`

## 4. Search

Now you can search the entire knowledge base:

```bash
# Basic search
python embedding_pipeline.py --search "how to create a subagent"

# Filter by agent
python embedding_pipeline.py --search "video prompts" --agent video_agent

# More results
python embedding_pipeline.py --search "prompt patterns" --results 20
```

## 5. View Statistics

```bash
python embedding_pipeline.py --stats
```

Shows:
- Total files and chunks indexed
- Breakdown by agent and category
- Last indexed timestamp
- Storage path

## Daily Usage

### After Editing Files

After making changes to knowledge files:

```bash
python embedding_pipeline.py --update
```

This is much faster than full reindex (only updates changed files).

### Setup Auto-Update (Optional)

Install git hook to auto-update after `git pull`:

```bash
bash setup_auto_update_hook.sh
```

## Common Commands

```bash
# Full reindex
python embedding_pipeline.py --index

# Incremental update
python embedding_pipeline.py --update

# Search with filters
python embedding_pipeline.py --search "query" --agent video_agent --results 10

# Show statistics
python embedding_pipeline.py --stats

# Help
python embedding_pipeline.py --help
```

## What Gets Indexed?

**Included:**
- `fontes/` - Source knowledge
- `iso_vectorstore/` - Knowledge cards
- `prompts/` - HOP prompts
- `workflows/` - ADWs
- `knowledge/`, `patterns/`, `docs/`, etc.

**Excluded:**
- `outputs/`, `user_output/` - User files
- `rascunho/` - Drafts
- `test/`, `example/` - Test files

## Troubleshooting

### Installation fails

```bash
# On Windows, you might need:
pip install --upgrade pip setuptools wheel

# Then retry:
pip install -r requirements.txt
```

### Search returns no results

```bash
# Check if indexed:
python embedding_pipeline.py --stats

# If empty, run:
python embedding_pipeline.py --index
```

### Out of memory

Edit `embedding_pipeline.py` and reduce batch size:

```python
BATCH_SIZE = 16  # Default: 32
```

## Next Steps

1. Read full documentation: `EMBEDDING_PIPELINE_README.md`
2. Integrate with your agents/scripts
3. Setup git hook for auto-updates
4. Explore advanced features (filters, custom queries, etc.)

---

**Need help?** Check `EMBEDDING_PIPELINE_README.md` for detailed documentation.
