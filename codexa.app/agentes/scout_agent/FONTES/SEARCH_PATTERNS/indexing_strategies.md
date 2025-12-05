# File Indexing Strategies

**Domain**: Search & Discovery
**Category**: SEARCH_PATTERNS
**Source**: Database indexing + File system best practices
**Quality Score**: 0.82

---

## Resumo Executivo

Indexacao e o processo de catalogar arquivos para busca rapida. Um bom indice permite queries em milissegundos mesmo em codebases com milhares de arquivos. Este documento cobre estrategias de indexacao, o que indexar, e como manter o indice atualizado.

## Conceitos-Chave

### **Full Scan vs Incremental**
- **Full Scan**: Percorre todos os arquivos, reconstroi indice do zero. Usado na inicializacao ou quando indice corrompido.
- **Incremental**: Monitora mudancas (file watch), atualiza apenas o necessario. Mais eficiente para updates.

### **What to Index**
Nem todo dado precisa estar no indice. Foco em metadados que suportam queries:

```python
INDEX_FIELDS = {
    'path': str,           # Full path (searchable)
    'name': str,           # File name only
    'category': str,       # prime, hop, adw, config, etc.
    'agent': str,          # Owner agent
    'tags': List[str],     # Extracted keywords
    'modified': datetime,  # Last modification
    'size': int,           # File size in bytes
    'hash': str,           # Content hash for change detection
}
```

### **Ignore Patterns**
Evitar indexar arquivos irrelevantes melhora performance e qualidade:

```json
[
    "node_modules/**",
    ".venv/**",
    "__pycache__/**",
    ".git/**",
    "*.pyc", "*.pyo",
    "*.log", "*.tmp",
    ".DS_Store", "Thumbs.db",
    "outputs/**",
    "*.bak"
]
```

### **Category Detection**
Classificar automaticamente baseado em patterns:

```python
CATEGORY_PATTERNS = {
    'prime': ['**/PRIME.md', '**/prime*.md'],
    'readme': ['**/README.md', '**/readme*.md'],
    'hop': ['**/*_HOP.md', '**/prompts/*.md'],
    'adw': ['**/*_ADW_*.md', '**/workflows/*.md'],
    'config': ['**/config/*.json', '**/*.config.*'],
    'schema': ['**/schemas/*.json', '**/*_schema.json'],
}
```

## Como Aplicar

1. **Definir schema do indice**
   ```python
   class IndexEntry:
       path: str
       name: str
       category: str
       agent: str
       tags: List[str]
       modified: datetime
       size: int
       content_hash: str

       @classmethod
       def from_file(cls, filepath: Path):
           content = filepath.read_text()
           return cls(
               path=str(filepath),
               name=filepath.name,
               category=detect_category(filepath),
               agent=detect_agent(filepath),
               tags=extract_tags(filepath, content),
               modified=filepath.stat().st_mtime,
               size=filepath.stat().st_size,
               content_hash=hashlib.md5(content.encode()).hexdigest()
           )
   ```

2. **Implementar full scan**
   ```python
   def build_index(root: Path, ignore_patterns: List[str]) -> Index:
       index = Index()
       for filepath in root.rglob('*'):
           if filepath.is_file() and not should_ignore(filepath, ignore_patterns):
               entry = IndexEntry.from_file(filepath)
               index.add(entry)
       return index
   ```

3. **Persistir indice**
   ```python
   def save_index(index: Index, cache_path: Path):
       data = {
           'version': '1.0',
           'built_at': datetime.now().isoformat(),
           'entries': [e.to_dict() for e in index.entries]
       }
       cache_path.write_text(json.dumps(data, indent=2))

   def load_index(cache_path: Path) -> Optional[Index]:
       if not cache_path.exists():
           return None
       data = json.loads(cache_path.read_text())
       return Index.from_dict(data)
   ```

4. **Implementar incremental update**
   ```python
   def update_index(index: Index, changed_files: List[Path]):
       for filepath in changed_files:
           if filepath.exists():
               index.update(IndexEntry.from_file(filepath))
           else:
               index.remove(str(filepath))
   ```

## Exemplos Praticos

### Exemplo 1: Build Time Optimization

**Antes** (full scan every query):
- 5000 files
- ~2-3 seconds per search
- High CPU usage

**Depois** (persistent index):
- Index build: ~2-3 seconds (once)
- Search: ~20-50ms
- Index reload: ~100ms

**Resultado**: 100x faster searches after initial build

### Exemplo 2: Smart Tag Extraction

**File**: `anuncio_agent/prompts/14_title_HOP.md`

**Extracted Tags**:
```python
tags = [
    'title',           # From filename
    'HOP',             # From filename pattern
    'anuncio_agent',   # From path
    'marketplace',     # From content keywords
    'copywriting',     # From content keywords
    'product listing'  # From H1/H2 headers
]
```

**Resultado**: File encontrado por queries "title", "marketplace", "copywriting"

## Quando Usar

- **USE full scan quando**:
  - Primeira execucao (cold start)
  - Indice corrompido ou desatualizado
  - Apos grandes refactorings
  - Comando manual `mcp__scout__refresh()`

- **USE incremental quando**:
  - Updates durante sessao de trabalho
  - File watcher detecta mudancas
  - Add/remove/rename de arquivos

- **USE persistent index quando**:
  - Codebase grande (1000+ files)
  - Queries frequentes
  - Startup time importa

- **USE in-memory index quando**:
  - Codebase pequena (<500 files)
  - Desenvolvimento/debug
  - Testes

## Relacionado

- Ver tambem: `semantic_search.md`
- Ver tambem: `relevance_scoring.md`
- Config: `scout_agent/config/ignore_patterns.json`
- Config: `scout_agent/config/categories.json`

---

**Processado**: 2025-12-05
**Tokens**: ~900
