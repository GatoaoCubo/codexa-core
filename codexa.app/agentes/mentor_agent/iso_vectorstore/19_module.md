# Catalog Update Module | mentor_agent

**Purpose**: Maintain catalogo.json master index with metadata for all processed knowledge files
**Version**: 1.0.0 | **Updated**: 2025-11-18

---

## 🎯 OVERVIEW

Final step of knowledge processing pipeline. Updates catalogo.json (master index) with metadata for newly processed files, enabling fast discovery and retrieval.

**Pipeline Position**: Extract → Classify → Synthesize → Validate → **Catalog Update**

---

## 📊 CATALOG STRUCTURE

### catalogo.json Format

**Location**: `PROCESSADOS/catalogo.json`

**Schema**:
```json
{
  "version": "3.0.0",
  "last_updated": "2025-11-18T14:30:00Z",
  "total_files": 150,
  "categories": {
    "marketplace_optimization": 45,
    "copywriting": 22,
    "estrategia_produto": 18,
    "analise_concorrencia": 12,
    "compliance_legal": 8,
    "branding": 15,
    "visual_design": 10,
    "customer_experience": 7,
    "operacoes_logistica": 6,
    "financeiro_precificacao": 7
  },
  "files": [
    {
      "id": "marketplace_titulos_20251110",
      "arquivo": "marketplace_titulos_otimizacao_20251110.md",
      "categoria": "marketplace_optimization",
      "assunto": "titulos_seo",
      "nivel": "intermediario",
      "tags": ["mercadolivre", "shopee", "seo", "conversao", "titulos"],
      "aplicacao": "quando_criar_anuncios",
      "criado": "2025-11-10",
      "atualizado": "2025-11-10",
      "fonte_original": "RASCUNHO/guia_ml_titulos.pdf",
      "quality_score": 0.87,
      "token_count": 1050,
      "resumo": "Otimização de títulos SEO para Mercado Livre e Shopee. Técnicas de keyword placement, character limits, e estruturação para maximizar CTR.",
      "keywords_principais": ["titulo seo", "mercado livre", "keywords", "conversão"],
      "relacionados": ["marketplace_seo_20251105", "copywriting_headlines_20251101"]
    },
    {
      "id": "...",
      "...": "..."
    }
  ]
}
```

---

## 🔧 CATALOG UPDATE ALGORITHM

### Step 1: Generate File Entry

```python
def generate_catalog_entry(processed_file_metadata):
    """
    Create catalog entry from processed file metadata
    """
    # Extract from processing pipeline
    file_id = generate_file_id(
        processed_file_metadata["categoria"],
        processed_file_metadata["assunto"],
        processed_file_metadata["criado"]
    )
    # Example: "marketplace_titulos_20251110"

    entry = {
        "id": file_id,
        "arquivo": processed_file_metadata["arquivo"],
        "categoria": processed_file_metadata["categoria"],
        "assunto": processed_file_metadata["assunto"],
        "nivel": processed_file_metadata["nivel"],
        "tags": processed_file_metadata["tags"],
        "aplicacao": processed_file_metadata["aplicacao"],
        "criado": processed_file_metadata["criado"],
        "atualizado": processed_file_metadata["criado"],  # Same on first creation
        "fonte_original": processed_file_metadata["fonte_original"],
        "quality_score": processed_file_metadata["quality_score"],
        "token_count": processed_file_metadata["token_count"],
        "resumo": extract_resumo_executivo(processed_file_metadata["content"]),
        "keywords_principais": extract_main_keywords(processed_file_metadata["content"]),
        "relacionados": []  # Will be populated after finding related files
    }

    return entry
```

---

### Step 2: Find Related Files

```python
def find_related_files(new_entry, existing_catalog):
    """
    Find files related by categoria, assunto, or tags
    """
    related = []

    for existing_file in existing_catalog["files"]:
        similarity_score = 0

        # Same categoria
        if existing_file["categoria"] == new_entry["categoria"]:
            similarity_score += 2

        # Same assunto
        if existing_file["assunto"] == new_entry["assunto"]:
            similarity_score += 3

        # Overlapping tags (≥2 common tags)
        common_tags = set(existing_file["tags"]) & set(new_entry["tags"])
        if len(common_tags) >= 2:
            similarity_score += len(common_tags)

        # Same aplicacao
        if existing_file["aplicacao"] == new_entry["aplicacao"]:
            similarity_score += 1

        # If similarity >= 3, consider related
        if similarity_score >= 3:
            related.append({
                "id": existing_file["id"],
                "score": similarity_score
            })

    # Sort by similarity score, return top 5
    related.sort(key=lambda x: x["score"], reverse=True)
    return [r["id"] for r in related[:5]]
```

---

### Step 3: Update Catalog

```python
def update_catalog(new_entry, catalog_path="PROCESSADOS/catalogo.json"):
    """
    Add new entry to catalog and update metadata
    """
    # Load existing catalog
    with open(catalog_path, 'r', encoding='utf-8') as f:
        catalog = json.load(f)

    # Check if file already exists (update vs insert)
    existing_index = next(
        (i for i, f in enumerate(catalog["files"]) if f["id"] == new_entry["id"]),
        None
    )

    if existing_index is not None:
        # Update existing entry
        catalog["files"][existing_index] = {
            **catalog["files"][existing_index],
            **new_entry,
            "atualizado": datetime.now().isoformat()
        }
        action = "updated"
    else:
        # Insert new entry
        catalog["files"].append(new_entry)
        action = "inserted"

    # Update catalog metadata
    catalog["last_updated"] = datetime.now().isoformat()
    catalog["total_files"] = len(catalog["files"])

    # Update category counts
    category_counts = {}
    for file_entry in catalog["files"]:
        cat = file_entry["categoria"]
        category_counts[cat] = category_counts.get(cat, 0) + 1
    catalog["categories"] = category_counts

    # Save updated catalog
    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    return {
        "status": "success",
        "action": action,
        "file_id": new_entry["id"],
        "total_files": catalog["total_files"]
    }
```

---

### Step 4: Bidirectional Linking (Optional)

```python
def update_bidirectional_links(new_entry_id, related_ids, catalog):
    """
    Update 'relacionados' field in both new and existing files
    """
    # Add related files to new entry
    for file_entry in catalog["files"]:
        if file_entry["id"] == new_entry_id:
            file_entry["relacionados"] = related_ids
            break

    # Add new entry to related files
    for file_entry in catalog["files"]:
        if file_entry["id"] in related_ids:
            if new_entry_id not in file_entry["relacionados"]:
                file_entry["relacionados"].append(new_entry_id)

    return catalog
```

---

## 🔍 CATALOG SEARCH (Discovery)

### Search by Categoria

```python
def search_by_categoria(categoria, catalog):
    """
    Find all files in a specific categoria
    """
    results = [
        file_entry for file_entry in catalog["files"]
        if file_entry["categoria"] == categoria
    ]

    return sorted(results, key=lambda x: x["quality_score"], reverse=True)
```

---

### Search by Assunto

```python
def search_by_assunto(assunto, catalog):
    """
    Find all files matching assunto (partial match)
    """
    results = [
        file_entry for file_entry in catalog["files"]
        if assunto.lower() in file_entry["assunto"].lower()
    ]

    return sorted(results, key=lambda x: x["quality_score"], reverse=True)
```

---

### Search by Tags

```python
def search_by_tags(tags, catalog, match_mode="any"):
    """
    Find files matching tags
    match_mode: "any" (OR) or "all" (AND)
    """
    results = []

    for file_entry in catalog["files"]:
        if match_mode == "any":
            # Match if ANY tag overlaps
            if any(tag in file_entry["tags"] for tag in tags):
                results.append(file_entry)
        else:  # "all"
            # Match if ALL tags present
            if all(tag in file_entry["tags"] for tag in tags):
                results.append(file_entry)

    return sorted(results, key=lambda x: x["quality_score"], reverse=True)
```

---

### Search by Keywords (Full-Text)

```python
def search_by_keywords(keywords, catalog):
    """
    Full-text search in resumo + keywords_principais
    """
    results = []

    for file_entry in catalog["files"]:
        score = 0

        # Search in resumo
        resumo = file_entry["resumo"].lower()
        for keyword in keywords:
            if keyword.lower() in resumo:
                score += 2

        # Search in keywords_principais
        for kw_principal in file_entry["keywords_principais"]:
            for keyword in keywords:
                if keyword.lower() in kw_principal.lower():
                    score += 3

        # Search in assunto
        if any(kw.lower() in file_entry["assunto"].lower() for kw in keywords):
            score += 1

        if score > 0:
            results.append({
                "file": file_entry,
                "score": score
            })

    # Sort by relevance score
    results.sort(key=lambda x: x["score"], reverse=True)
    return [r["file"] for r in results]
```

---

## 📊 CATALOG STATISTICS

### Generate Stats

```python
def generate_catalog_stats(catalog):
    """
    Generate analytics from catalog
    """
    stats = {
        "total_files": len(catalog["files"]),
        "by_categoria": catalog["categories"],
        "by_nivel": {},
        "avg_quality_score": 0,
        "avg_token_count": 0,
        "top_tags": {},
        "most_related": [],
        "recent_additions": []
    }

    # By nivel
    for file_entry in catalog["files"]:
        nivel = file_entry["nivel"]
        stats["by_nivel"][nivel] = stats["by_nivel"].get(nivel, 0) + 1

    # Averages
    stats["avg_quality_score"] = sum(f["quality_score"] for f in catalog["files"]) / len(catalog["files"])
    stats["avg_token_count"] = sum(f["token_count"] for f in catalog["files"]) / len(catalog["files"])

    # Top tags
    tag_counts = {}
    for file_entry in catalog["files"]:
        for tag in file_entry["tags"]:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1
    stats["top_tags"] = dict(sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10])

    # Most related (files with most connections)
    stats["most_related"] = sorted(
        catalog["files"],
        key=lambda x: len(x["relacionados"]),
        reverse=True
    )[:5]

    # Recent additions (last 10)
    stats["recent_additions"] = sorted(
        catalog["files"],
        key=lambda x: x["criado"],
        reverse=True
    )[:10]

    return stats
```

---

## ✅ CATALOG VALIDATION

### Integrity Checks

```python
def validate_catalog(catalog):
    """
    Check catalog integrity
    """
    issues = []

    # Check version
    if "version" not in catalog:
        issues.append("Missing version field")

    # Check all required fields in files
    required_fields = ["id", "arquivo", "categoria", "assunto", "nivel", "tags", "aplicacao", "criado"]
    for i, file_entry in enumerate(catalog["files"]):
        for field in required_fields:
            if field not in file_entry:
                issues.append(f"File {i} ({file_entry.get('id', 'unknown')}) missing '{field}'")

    # Check for duplicate IDs
    ids = [f["id"] for f in catalog["files"]]
    duplicates = [id for id in ids if ids.count(id) > 1]
    if duplicates:
        issues.append(f"Duplicate IDs: {duplicates}")

    # Check file existence
    for file_entry in catalog["files"]:
        file_path = f"PROCESSADOS/{file_entry['arquivo']}"
        if not os.path.exists(file_path):
            issues.append(f"File not found: {file_entry['arquivo']}")

    # Check category counts match
    actual_counts = {}
    for file_entry in catalog["files"]:
        cat = file_entry["categoria"]
        actual_counts[cat] = actual_counts.get(cat, 0) + 1

    if actual_counts != catalog["categories"]:
        issues.append(f"Category counts mismatch: {actual_counts} vs {catalog['categories']}")

    return {
        "valid": len(issues) == 0,
        "issues": issues
    }
```

---

## 📋 UPDATE CHECKLIST

Before considering catalog update complete:

- [ ] New entry generated with all required fields
- [ ] Related files identified (top 5)
- [ ] Catalog loaded and updated (insert or update)
- [ ] Bidirectional links established
- [ ] Catalog metadata updated (last_updated, total_files, categories)
- [ ] Catalog saved to disk
- [ ] Catalog validation passed (no integrity issues)

---

## 🔄 CATALOG MAINTENANCE

### Rebuild Catalog (from scratch)

```python
def rebuild_catalog_from_files(processados_dir="PROCESSADOS"):
    """
    Rebuild catalog by scanning all .md files in PROCESSADOS/
    """
    files = glob.glob(f"{processados_dir}/*.md")

    catalog = {
        "version": "3.0.0",
        "last_updated": datetime.now().isoformat(),
        "total_files": 0,
        "categories": {},
        "files": []
    }

    for file_path in files:
        # Read file content
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract metadata from frontmatter
        metadata = extract_metadata_from_md(content)

        # Generate catalog entry
        entry = generate_catalog_entry(metadata)
        catalog["files"].append(entry)

    # Update counts
    catalog["total_files"] = len(catalog["files"])
    for file_entry in catalog["files"]:
        cat = file_entry["categoria"]
        catalog["categories"][cat] = catalog["categories"].get(cat, 0) + 1

    # Find related files for each entry
    for file_entry in catalog["files"]:
        file_entry["relacionados"] = find_related_files(file_entry, catalog)

    # Save
    with open(f"{processados_dir}/catalogo.json", 'w', encoding='utf-8') as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    return catalog
```

---

### Cleanup Orphaned Entries

```python
def cleanup_orphaned_entries(catalog, processados_dir="PROCESSADOS"):
    """
    Remove catalog entries for files that no longer exist
    """
    orphaned = []

    for i, file_entry in enumerate(catalog["files"]):
        file_path = f"{processados_dir}/{file_entry['arquivo']}"
        if not os.path.exists(file_path):
            orphaned.append(i)

    # Remove orphaned entries (reverse order to maintain indices)
    for i in reversed(orphaned):
        removed = catalog["files"].pop(i)
        print(f"Removed orphaned entry: {removed['id']}")

    # Update metadata
    catalog["total_files"] = len(catalog["files"])
    catalog["last_updated"] = datetime.now().isoformat()

    return {
        "removed_count": len(orphaned),
        "remaining_files": catalog["total_files"]
    }
```

---

## 📊 PERFORMANCE METRICS

**Target Performance**:
- Catalog update: <500ms per file
- Search by categoria: <100ms (150 files)
- Full-text keyword search: <200ms (150 files)
- Rebuild entire catalog: <10s (150 files)

**Catalog Size**:
- 150 files ≈ 500KB catalogo.json
- 1000 files ≈ 3.5MB (manageable in-memory)

---

**Status**: Final module of knowledge processing pipeline
**Integration**: Called after file validation, updates master index for discovery
**Performance**: Fast search/retrieval via indexed catalog (O(n) search, <200ms for 150 files)