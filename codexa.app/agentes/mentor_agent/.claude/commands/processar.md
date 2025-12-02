# /processar | Transform RASCUNHO → PROCESSADOS

Execute knowledge processing pipeline to transform raw files from RASCUNHO/ into validated, structured knowledge in PROCESSADOS/.

## Arguments

- `[file]` (optional): Specific file in RASCUNHO/ to process (e.g., "guia_ml.pdf")
  - If not provided, lists all files in RASCUNHO/ and prompts for selection
- `--batch`: Process all files in RASCUNHO/ sequentially
- `--categoria [name]`: Force specific category classification
- `--mode [standard|fast|thorough]`: Processing mode (default: standard)

## Usage Examples

```bash
# Process single file
/processar guia_ml.pdf

# Process with forced category
/processar documento.pdf --categoria marketplace_optimization

# List available files (if no file specified)
/processar

# Batch process all files
/processar --batch

# Thorough processing (with context discovery)
/processar arquivo.pdf --mode thorough
```

## Execution Flow

### Phase 1: Context Discovery (Optional - only if --mode thorough)

**Follow instructions from**:
```
prompts/scout_global_navigator_HOP.md
```

**Actions**:
1. Navigate entire codexa project
2. Scan all PRIME.md and README.md files from agents
3. Identify relevant patterns for knowledge processing
4. Return `$context_map` with:
   - Relevant agents (conhecimento_agent, etc.)
   - Similar workflows (RAW→CARDS→DATASETS)
   - Reusable patterns (5D validation, catalog management)

**Input**:
```json
{
  "$tarefa": "processar conhecimento de {file}",
  "$scope": "agents_only",
  "$depth": "prime_readme",
  "$output_format": "summary"
}
```

**Output**: `$context_map` (or skip if standard mode)

---

### Phase 2: Knowledge Processing

**Follow instructions from**:
```
prompts/knowledge_processor_HOP.md
```

**Actions**:
1. **Extract**: Read file from RASCUNHO/, extract content (PDF→text, video→transcript, etc.)
2. **Classify**: Detect categoria, assunto, nível, tags, aplicacao
3. **Synthesize**: Generate structured markdown (800-1200 tokens, seller language)
4. **Validate**: Call quality_validator_5d_HOP, check 5D quality (≥0.75)
5. **Save**: Write to PROCESSADOS/ with naming convention `{categoria}_{assunto}_{date}.md`
6. **Update Catalog**: Add entry to PROCESSADOS/catalogo.json

**Input**:
```json
{
  "$rascunho_file": "RASCUNHO/{file}",
  "$context_map": $context_map,
  "$processing_mode": "{mode}",
  "$auto_validate": true
}
```

**Output**: `$processed_file` (processing report)

---

### Phase 3: Quality Validation (Embedded in Phase 2)

**Follow instructions from**:
```
prompts/quality_validator_5d_HOP.md
```

**Actions**:
1. Validate 5 dimensions:
   - **Completeness**: All required sections present?
   - **Clarity**: Seller-friendly language, no jargon?
   - **Accuracy**: Brazil-specific, factually correct?
   - **Relevance**: Useful for seller's daily work?
   - **Actionability**: Concrete executable steps?
2. Calculate overall score (weighted average)
3. Generate improvement suggestions for weak dimensions
4. Auto-improve if 0.60 ≤ score < 0.75 (max 3 retries)

**Input**:
```json
{
  "$content": "{synthesized markdown}",
  "$metadata": {categoria, assunto, nivel, tags, aplicacao},
  "$thresholds": {"overall": 0.75, "per_dimension": 0.60}
}
```

**Output**: `$validation_report`

---

## Step-by-Step Execution

### 1. Validate Environment

```bash
# Check directories exist
if not exists("RASCUNHO/"):
    create_directory("RASCUNHO/")
if not exists("PROCESSADOS/"):
    create_directory("PROCESSADOS/")
if not exists("PROCESSADOS/catalogo.json"):
    initialize_catalog()
```

### 2. Handle Arguments

```python
# Parse command arguments
if no file specified:
    list_files_in_rascunho()
    prompt_user_selection()
elif --batch:
    files = list_all_files_in_rascunho()
    process_sequentially(files)
else:
    file = parse_file_argument()
    validate_file_exists(f"RASCUNHO/{file}")
```

### 3. Execute Processing Pipeline

For each file:

```markdown
## Processing: {file}

### Phase 1: Context Discovery (if --mode thorough)
- Scanning project for relevant patterns...
- Found: conhecimento_agent (relevance: 0.95)
- Pattern identified: 5D validation framework
- Context map ready

### Phase 2: Knowledge Processing
- [1/6] Extracting content from {file}...
  ✓ Extracted 3,245 characters from PDF

- [2/6] Classifying content...
  ✓ Categoria: marketplace_optimization
  ✓ Assunto: títulos_seo
  ✓ Nível: intermediário
  ✓ Tags: mercadolivre, seo, conversão
  ✓ Aplicacao: quando_criar_anuncios

- [3/6] Synthesizing structured markdown...
  ✓ Generated 1,050 tokens
  ✓ Seller language applied
  ✓ Brazil-specific examples included

- [4/6] Validating quality (5D framework)...
  ✓ Completeness: 0.92
  ✓ Clarity: 0.85
  ✓ Accuracy: 0.88
  ✓ Relevance: 0.90
  ✓ Actionability: 0.80
  ✓ Overall: 0.87 (excellent)

- [5/6] Saving to PROCESSADOS/...
  ✓ Saved: marketplace_titulos_otimizacao_20251113.md

- [6/6] Updating catalog...
  ✓ catalogo.json updated

### Result: SUCCESS ✓
- File: PROCESSADOS/marketplace_titulos_otimizacao_20251113.md
- Quality: 0.87 (excellent)
- Tokens: 1,050
- Time: 9.4s
```

### 4. Handle Errors

```markdown
### Error Handling

If extraction fails:
- Try alternative library
- If partial (>30% recovered): Continue with warning
- If complete failure: Abort, return error

If classification confidence < 0.5:
- Prompt user for manual categoria selection
- Continue with user input

If quality < 0.60:
- Abort processing
- Return validation report with suggestions
- Suggest manual review

If quality 0.60-0.74:
- Auto-improve weak dimensions
- Revalidate (max 3 attempts)
- If still < 0.75: Save with warning

If file save fails:
- Retry once
- If still fails: Abort, return error
- Do NOT update catalog
```

### 5. Return Summary Report

```markdown
## Processing Summary

**Mode**: {mode}
**Files Processed**: {count}
**Success**: {success_count}
**Failed**: {fail_count}

### Successful Processings

| File | Output | Quality | Time |
|------|--------|---------|------|
| guia_ml.pdf | marketplace_titulos_20251113.md | 0.87 | 9.4s |
| dicas.txt | copywriting_gatilhos_20251113.md | 0.82 | 6.2s |

### Failed Processings

| File | Reason | Suggestion |
|------|--------|------------|
| corrupted.pdf | Extraction failed | Check file integrity, re-upload |

### Next Steps

Now that knowledge is processed, sellers can:
1. Ask questions: "Me ensina sobre títulos de anúncio"
2. Search catalog: "Me mostra o que sei sobre marketplace"
3. Add more files to RASCUNHO/ and run /processar again
```

---

## Relevant Files

**HOPs (Prompt Modules)**:
- `prompts/scout_global_navigator_HOP.md` - Project navigation & context discovery
- `prompts/knowledge_processor_HOP.md` - RASCUNHO→PROCESSADOS pipeline
- `prompts/quality_validator_5d_HOP.md` - 5D quality validation framework

**Configuration**:
- `config/categorias_conhecimento.json` - 10 categories, 27 tags, taxonomy
- `config/seller_language_guide.json` - Communication patterns, translation rules

**Directories**:
- `RASCUNHO/` - Input: Raw files from sellers
- `PROCESSADOS/` - Output: Validated structured knowledge (flat structure)
- `PROCESSADOS/catalogo.json` - Master index for search

**Orchestrator**:
- `prompts/mentor_orchestrator.md` - Main mentor logic (delegates to /processar)

---

## Validation Commands

After processing, validate with:

```bash
# Check file was created
ls PROCESSADOS/{categoria}_{assunto}_{date}.md

# Verify catalog updated
cat PROCESSADOS/catalogo.json | grep "{assunto}"

# Test search (scout_internal)
# Ask: "Me fala sobre {assunto}"
# Should find the processed file
```

---

## Notes

- **Processing Time**: 5-15s per file (text), 30-120s (video with transcription)
- **Quality Threshold**: Overall ≥ 0.75 (excellent/good), per-dimension ≥ 0.60
- **File Naming**: Always `{categoria}_{assunto}_{YYYYMMDD}.md` (flat structure, no subfolders)
- **Supported Formats**: PDF, MD, TXT, DOCX, HTML, JSON, CSV, XLSX, MP4, MP3, PNG, JPG
- **Inherited Pattern**: From conhecimento_agent (97.5% quality rate on 66k+ cards)

---

## Previous Output as $arguments

If running in multi-phase workflow:

```json
{
  "previous_phase": "scout_global_navigator",
  "context_map": {
    "most_relevant_agents": ["conhecimento_agent", "anuncio_agent"],
    "patterns_identified": ["5D_validation", "flat_structure", "catalog_management"],
    "recommendations": ["Use conhecimento pipeline", "Apply seller language guide"]
  },
  "current_phase": "knowledge_processor",
  "next_phase": "catalog_update"
}
```

Chain outputs using `$arguments` for seamless phase transitions.

---

**Version**: 1.0.0
**Last Updated**: 2025-11-13
**Dependencies**: scout_global_navigator_HOP, knowledge_processor_HOP, quality_validator_5d_HOP
**Status**: Ready for Use
