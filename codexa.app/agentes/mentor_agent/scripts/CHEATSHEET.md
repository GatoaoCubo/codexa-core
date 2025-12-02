# Embedding Pipeline Cheat Sheet

Quick reference for common tasks.

## Installation

```bash
cd codexa.app/agentes/mentor_agent/scripts
pip install -r requirements.txt
```

## Commands

### Indexing

```bash
# First time: full index
python embedding_pipeline.py --index

# After changes: incremental update
python embedding_pipeline.py --update

# Check statistics
python embedding_pipeline.py --stats
```

### Searching

```bash
# Basic search
python embedding_pipeline.py --search "query"

# With filters
python embedding_pipeline.py --search "query" --agent video_agent

# More results
python embedding_pipeline.py --search "query" --results 20

# Simple wrapper
python search_knowledge.py "query"
```

### Testing

```bash
# Run test suite
python test_embedding_pipeline.py

# Run examples
python example_integration.py
```

### Git Integration

```bash
# Install auto-update hook
bash setup_auto_update_hook.sh
```

## Python API

### Basic Search

```python
from search_knowledge import search_kb

results = search_kb("how to create subagent", top_k=5)

for r in results:
    print(f"{r['file']}: {r['section']}")
    print(f"Score: {r['score']:.2f}")
```

### Filtered Search

```python
# By agent
results = search_kb(
    query="video prompts",
    agent="video_agent",
    top_k=5
)

# By category
results = search_kb(
    query="prompt patterns",
    category="hop",
    top_k=5
)

# By score threshold
results = search_kb(
    query="quality standards",
    min_score=0.7,
    top_k=5
)
```

### Similar Documents

```python
from search_knowledge import search_similar_to_file

results = search_similar_to_file(
    file_path="codexa.app/agentes/video_agent/prompts/10_concept_planner_HOP.md",
    top_k=5
)
```

### Agent-Specific Search

```python
from search_knowledge import search_by_agent

results = search_by_agent(
    agent_name="video_agent",
    query="lighting techniques",
    top_k=3
)
```

## Result Object

```python
{
    "rank": 1,
    "score": 0.856,              # 0.0 to 1.0
    "file": "path/to/file.md",
    "agent": "video_agent",
    "category": "hop",
    "section": "Section Title",
    "tokens": 456,
    "content": "Content snippet..."
}
```

## Configuration

Edit `embedding_pipeline.py`:

```python
# Chunking
MAX_CHUNK_TOKENS = 1000    # Max tokens per chunk
OVERLAP_TOKENS = 100       # Overlap between chunks

# Embedding
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Model name
BATCH_SIZE = 32            # Batch size for embedding

# Storage
COLLECTION_NAME = "codexa_knowledge"

# Categories
INCLUDE_CATEGORIES = {
    "fontes", "iso_vectorstore", "hop",
    "processados", "knowledge", "patterns"
}
EXCLUDE_CATEGORIES = {
    "outputs", "rascunho", "test"
}
```

## File Locations

```
scripts/
├── embedding_pipeline.py          # Main pipeline
├── search_knowledge.py            # Search wrapper
├── example_integration.py         # Examples
├── test_embedding_pipeline.py     # Tests
└── setup_auto_update_hook.sh      # Git hook

FONTES/
└── knowledge_vectors/             # Vector storage
    ├── chroma.sqlite3             # Database
    ├── index_stats.json           # Stats
    └── pipeline.log               # Logs
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| ImportError | `pip install -r requirements.txt` |
| No results | `python embedding_pipeline.py --index` |
| Out of memory | Reduce `BATCH_SIZE` to 16 |
| Slow search | Check if indexed with `--stats` |
| Git hook not working | `chmod +x .git/hooks/post-merge` |

## Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Full index | 15-20 min | 1741 files |
| Incremental update | 30 sec | 10 files |
| Search | <100ms | Per query |

## Integration Patterns

### In Agent Workflows

```python
# 1. Discover relevant knowledge
from search_knowledge import search_kb

task = "Create video workflow"
context = search_kb(task, top_k=5, min_score=0.6)

# 2. Build context string
context_str = "\n".join([
    f"- {r['file']}: {r['section']}"
    for r in context
])

# 3. Inject into prompt
prompt = f"""
Task: {task}

Relevant Knowledge:
{context_str}

Implement the task.
"""
```

### In HOPs

```markdown
## Knowledge Discovery Phase

```python
from search_knowledge import search_kb
context = search_kb("{{task_description}}", top_k=5)
```

Use context to inform implementation.
```

### In Scripts

```python
import subprocess
import json

# Run search
result = subprocess.run(
    ["python", "scripts/embedding_pipeline.py", "--search", query],
    capture_output=True,
    text=True
)

print(result.stdout)
```

## Useful Filters

```python
# HOPs only
search_kb("prompt patterns", category="hop")

# Specific agent
search_kb("video techniques", agent="video_agent")

# High confidence only
search_kb("quality standards", min_score=0.8)

# Combine filters
search_kb(
    "workflow patterns",
    agent="codexa_agent",
    category="adw",
    min_score=0.7
)
```

## Examples

See `example_integration.py` for:
1. Basic search
2. Agent-specific search
3. Context injection
4. Similar documents
5. Knowledge discovery workflow
6. Batch queries

## Documentation

- **Quick Start**: `QUICKSTART_EMBEDDING.md`
- **Full Guide**: `EMBEDDING_PIPELINE_README.md`
- **Architecture**: `ARCHITECTURE.md`
- **Summary**: `EMBEDDING_PIPELINE_SUMMARY.md`
- **Cheat Sheet**: This file

## Key Metrics

- **Files indexed**: 1741+
- **Chunks created**: ~8000
- **Storage size**: ~55MB
- **Search latency**: <100ms
- **Embedding dims**: 384

## Categories Indexed

**Included**:
- fontes, iso_vectorstore, hop
- processados, knowledge, patterns
- workflows, adw, prompts
- docs, architecture, core

**Excluded**:
- outputs, rascunho, user_output
- test, example

## Agents Indexed

All 13 agents:
- codexa_agent, mentor_agent
- video_agent, photo_agent
- curso_agent, marca_agent
- anuncio_agent, pesquisa_agent
- qa_gato3_agent, scout_agent
- vscode_agent, voice_agent
- ronronalda_agent

---

**Quick Tip**: Use `--stats` to check if index is up to date!

```bash
python embedding_pipeline.py --stats
```
