# knowledge_processor_HOP | RASCUNHO→PROCESSADOS Pipeline

## MODULE_METADATA

```yaml
id: knowledge_processor
version: 1.0.0
category: processing
purpose: Extract, classify, synthesize, and validate knowledge files from RASCUNHO/ to PROCESSADOS/
dependencies: [quality_validator_5d_HOP]
upstream: scout_global_navigator_HOP, mentor_orchestrator
downstream: quality_validator_5d_HOP, catalog_updater
```

## INPUT_CONTRACT

### Required Inputs
- `$rascunho_file` (string): Path to file in RASCUNHO/ to process (e.g., "RASCUNHO/guia_ml.pdf")
- `$context_map` (object, optional): Context from scout_global_navigator_HOP for pattern guidance

### Optional Inputs
- `$target_categoria` (string, optional): Force specific category if known (e.g., "marketplace_optimization")
- `$seller_context` (object, optional): Seller-specific info (nível, marketplace preference)
- `$processing_mode` (enum): ["standard", "fast", "thorough"] (default: "standard")
- `$auto_validate` (bool): Auto-validate quality (default: true)

### Validation
- `$rascunho_file` must exist in RASCUNHO/ directory
- File extension must be supported: [.pdf, .md, .txt, .docx, .html, .json, .csv, .xlsx, .mp4, .mp3, .png, .jpg]
- `$target_categoria` must be one of 10 valid categories (if provided)

## OUTPUT_CONTRACT

### Primary Output: `$processed_file` (object)

```json
{
  "status": "success | failed | partial",
  "processed_path": "PROCESSADOS/marketplace_titulos_otimizacao_20251113.md",
  "metadata": {
    "arquivo": "marketplace_titulos_otimizacao_20251113.md",
    "categoria": "marketplace_optimization",
    "assunto": "títulos_seo",
    "nivel": "intermediário",
    "tags": ["mercadolivre", "seo", "conversão"],
    "aplicacao": "quando_criar_anuncios",
    "criado": "2025-11-13",
    "fonte_original": "RASCUNHO/guia_ml.pdf",
    "quality_score": 0.87,
    "token_count": 1050
  },
  "content_preview": "# Otimização de Títulos para SEO no Mercado Livre\n\n## CONCEITOS-CHAVE...",
  "processing_log": {
    "extraction_time": "2.3s",
    "classification_time": "0.8s",
    "synthesis_time": "5.2s",
    "validation_time": "1.1s",
    "total_time": "9.4s"
  }
}
```

### Secondary Outputs
- `$catalog_entry` (object): Metadata for catalogo.json update
- `$validation_report` (object): Quality validation details from quality_validator_5d_HOP
- `$error_context` (object): Error details if processing failed

## TASK

**Role**: You are the **Knowledge Processor**, responsible for transforming raw files from RASCUNHO/ into structured, validated knowledge files in PROCESSADOS/.

**Objective**: Execute the 4-stage pipeline (Extract → Classify → Synthesize → Validate) to produce high-quality, seller-friendly knowledge files that meet 5D quality standards (>0.75 overall score).

**Standards**:
- Follow conhecimento_agent proven pipeline (97.5% quality rate on 66k+ cards)
- Target output: 800-1200 tokens per processed file
- Seller language: Informal Brazilian Portuguese, no jargon
- Brazil-specific: Marketplace examples (ML, Shopee, Magalu, Amazon BR)
- Actionable: Always include concrete executable steps
- Flat structure: Save directly to PROCESSADOS/ root (NO subfolders)

**Constraints**:
- MAX 10 minutes per file processing
- MAX 3 retry attempts if quality < 0.75
- MUST update catalogo.json after successful processing
- NEVER leave temp files or generic names (file1.md, test.md)
- Handle extraction failures gracefully (partial content acceptable if quality ≥ 0.60)

## STEPS

### 1. Extract Content from Raw File

**Input**: `$rascunho_file`

**Actions**:
- Detect file type from extension
- Apply appropriate extraction method:

  **PDF** (.pdf):
  ```python
  import PyPDF2
  text = extract_text_from_pdf(file_path)
  # Handle OCR if needed for scanned PDFs
  ```

  **Markdown/Text** (.md, .txt):
  ```python
  text = read_file(file_path, encoding='utf-8')
  ```

  **DOCX** (.docx):
  ```python
  import docx
  doc = docx.Document(file_path)
  text = '\n'.join([p.text for p in doc.paragraphs])
  ```

  **HTML** (.html):
  ```python
  from bs4 import BeautifulSoup
  html = read_file(file_path)
  text = BeautifulSoup(html, 'html.parser').get_text()
  ```

  **JSON/CSV/XLSX** (.json, .csv, .xlsx):
  ```python
  # Parse structured data, extract relevant fields
  data = parse_structured_file(file_path)
  text = format_as_markdown(data)
  ```

  **Video** (.mp4):
  ```python
  # Extract audio → Speech-to-text transcription
  transcript = transcribe_video(file_path)
  text = transcript
  ```

  **Audio** (.mp3):
  ```python
  transcript = transcribe_audio(file_path)
  text = transcript
  ```

  **Image** (.png, .jpg):
  ```python
  # OCR text extraction
  text = extract_text_ocr(file_path)
  ```

- Clean extracted text:
  - Remove excessive whitespace
  - Fix encoding issues
  - Normalize line breaks
  - Remove irrelevant headers/footers

**Error Handling**:
- If extraction fails: Try alternative libraries
- If partial extraction: Continue if > 30% content recovered
- If complete failure: Return error, log to `$error_context`

**Output**: `$raw_content` (string, cleaned text)

### 2. Classify Content (Detect Categoria, Assunto, Nível, Tags)

**Input**: `$raw_content`, `$target_categoria` (optional)

**Actions**:

**A) Detect Primary Categoria** (if not forced):
```python
# Keyword matching against 10 categories
categoria_keywords = {
    "marketplace_optimization": ["seo", "título", "descrição", "foto", "posicionamento"],
    "copywriting": ["gatilho", "persuasão", "storytelling", "conversão"],
    "estrategia_produto": ["mix", "bundling", "upsell", "ciclo de vida"],
    "analise_concorrencia": ["concorrente", "benchmarking", "diferenciação"],
    "compliance_legal": ["regras", "legislação", "bloqueio", "compliance"],
    "branding": ["marca", "logo", "identidade", "reputação"],
    "visual_design": ["foto", "infográfico", "vídeo", "estética"],
    "customer_experience": ["atendimento", "avaliação", "SAC", "pós-venda"],
    "operacoes_logistica": ["estoque", "entrega", "frete", "fulfillment"],
    "financeiro_precificacao": ["preço", "margem", "custo", "promoção"]
}

# Score each category by keyword frequency
scores = {}
for cat, keywords in categoria_keywords.items():
    scores[cat] = sum([raw_content.lower().count(kw) for kw in keywords])

categoria = max(scores, key=scores.get)
```

**B) Extract Assunto** (specific topic):
```python
# Use noun phrase extraction + most frequent terms
assunto = extract_main_topic(raw_content, categoria)
# Examples: "títulos_seo", "gatilhos_mentais", "análise_preços"
```

**C) Detect Nível** (básico, intermediário, avançado):
```python
# Indicators
if any(word in raw_content for word in ["começando", "iniciante", "primeiro passo"]):
    nivel = "básico"
elif any(word in raw_content for word in ["avançado", "expert", "profissional"]):
    nivel = "avançado"
else:
    nivel = "intermediário"
```

**D) Extract Tags** (cross-cutting themes):
```python
# Detect marketplaces
tags = []
if "mercadolivre" in raw_content or "mercado livre" in raw_content:
    tags.append("mercadolivre")
if "shopee" in raw_content:
    tags.append("shopee")
# ... (27 predefined tags from categorias_conhecimento.json)
```

**E) Detect Aplicacao** (when to use):
```python
# Context patterns
aplicacao_patterns = {
    "quando_criar_anuncios": ["criar anúncio", "novo produto"],
    "quando_otimizar_existentes": ["otimizar", "melhorar anúncio existente"],
    "quando_analisar_competicao": ["concorrente", "benchmark"],
    # ...
}
aplicacao = detect_context(raw_content, aplicacao_patterns)
```

**Output**: `$metadata` (object with categoria, assunto, nivel, tags, aplicacao)

### 3. Synthesize Structured Markdown

**Input**: `$raw_content`, `$metadata`

**Actions**:

**A) Generate Structured Content**:

Template:
```markdown
# {assunto} para E-commerce | {categoria}

## CONCEITOS-CHAVE

[3-5 bullet points with essential concepts]
- Conceito 1: Explicação clara em 1-2 linhas
- Conceito 2: ...
- Conceito 3: ...

## POR QUE IMPORTA

[1-2 paragraphs explaining relevance to seller's daily work]
[Include specific metrics or examples when possible]

## COMO FAZER

[3-7 numbered steps, actionable and concrete]
1. **Passo 1**: Descrição detalhada com exemplo
   - Sub-passo A
   - Sub-passo B

2. **Passo 2**: ...

## EXEMPLO REAL

[Concrete example from Brazilian marketplace]
**Contexto**: Seller vendendo {produto} no {marketplace}
**Ação**: {o que fez}
**Resultado**: {métricas concretas, ex: +45% conversão}

## BOAS PRÁTICAS

[3-5 tips/recommendations]
- ✅ Faça: ...
- ❌ Evite: ...

## ERROS COMUNS

[2-4 common mistakes]
1. **Erro**: Descrição
   **Solução**: Como evitar

## PRÓXIMOS PASSOS

[Learning path or related topics]
- Depois de dominar isso, veja: {assunto relacionado}
- Combine com: {técnica complementar}

---

**Categoria**: {categoria}
**Nível**: {nivel}
**Tags**: {tags}
**Aplicação**: {aplicacao}
**Fonte**: {fonte_original}
```

**B) Apply Seller Language Translation**:
- Replace jargon with simple terms
- Use informal Brazilian Portuguese
- Add e-commerce metaphors (funil, vitrine, estoque)
- Include marketplace-specific examples (ML, Shopee)
- Convert vague claims to concrete metrics

Examples:
```
❌ "Implementar estratégia multifacetada de otimização"
✅ "Melhorar seu anúncio em 3 frentes: título, foto e preço"

❌ "Pode melhorar conversão"
✅ "+30-50% conversão (testado em 100+ anúncios no ML)"

❌ "Utilize técnicas de copywriting persuasivo"
✅ "Use gatilhos mentais como escassez ('últimas unidades') e urgência ('promoção acaba hoje')"
```

**C) Ensure Token Target**:
- Target: 800-1200 tokens
- If < 800: Expand examples, add more details to steps
- If > 1200: Condense, remove redundancy, focus on essentials

**Output**: `$synthesized_content` (markdown string, 800-1200 tokens)

### 4. Validate Quality (5D Framework)

**Input**: `$synthesized_content`, `$metadata`

**Actions**:
- Call `quality_validator_5d_HOP.md` with:
  ```json
  {
    "content": $synthesized_content,
    "metadata": $metadata,
    "thresholds": {
      "overall": 0.75,
      "per_dimension": 0.60
    }
  }
  ```
- Receive `$validation_report` with 5D scores:
  1. **Completeness** (all required sections present?)
  2. **Clarity** (readable for sellers, no jargon?)
  3. **Accuracy** (factually correct, Brazil-specific?)
  4. **Relevance** (useful for seller's work?)
  5. **Actionability** (concrete executable steps?)

**Quality Gates**:
```python
if validation_report.overall_score >= 0.75:
    proceed_to_save()
elif validation_report.overall_score >= 0.60:
    auto_improve_weak_dimensions()
    revalidate()
else:
    return_error("Quality too low to save")
```

**Auto-Improvement** (if 0.60 ≤ score < 0.75):
```python
for dimension, score in validation_report.dimension_scores.items():
    if score < 0.60:
        if dimension == "completeness":
            add_missing_sections()
        elif dimension == "clarity":
            simplify_language()
        elif dimension == "accuracy":
            verify_facts_add_sources()
        elif dimension == "relevance":
            add_seller_context()
        elif dimension == "actionability":
            make_steps_more_concrete()
```

**MAX 3 retry attempts**. If still < 0.75 after 3 tries, abort or request manual review.

**Output**: `$validation_report`, `$final_content` (improved if needed)

### 5. Save to PROCESSADOS/ with Naming Convention

**Input**: `$final_content`, `$metadata`

**Actions**:

**A) Generate Filename**:
```python
filename = f"{metadata.categoria}_{metadata.assunto}_{date.today().strftime('%Y%m%d')}.md"
# Example: "marketplace_titulos_otimizacao_20251113.md"

# Normalize assunto (remove special chars, spaces → underscores)
assunto_normalized = re.sub(r'[^a-z0-9_]', '', metadata.assunto.lower().replace(' ', '_'))
```

**B) Ensure Flat Structure**:
```python
output_path = f"PROCESSADOS/{filename}"
# NEVER: "PROCESSADOS/marketplace/titulos.md" (NO SUBFOLDERS!)
# ALWAYS: "PROCESSADOS/marketplace_titulos_20251113.md" (FLAT)
```

**C) Write File**:
```python
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(final_content)
```

**D) Verify File Saved**:
```python
if not os.path.exists(output_path):
    raise Exception(f"Failed to save file: {output_path}")
```

**Output**: `$processed_path` (absolute path to saved file)

### 6. Update catalogo.json

**Input**: `$metadata`, `$processed_path`, `$validation_report`

**Actions**:

**A) Load Existing Catalog**:
```python
catalog_path = "PROCESSADOS/catalogo.json"
catalog = json.load(open(catalog_path))
```

**B) Create Catalog Entry**:
```json
{
  "arquivo": "marketplace_titulos_otimizacao_20251113.md",
  "categoria": "marketplace_optimization",
  "assunto": "títulos_seo",
  "tags": ["mercadolivre", "seo", "conversão"],
  "nivel": "intermediário",
  "aplicacao": "quando_criar_anuncios",
  "criado": "2025-11-13",
  "fonte_original": "RASCUNHO/guia_ml.pdf",
  "quality_score": 0.87,
  "token_count": 1050
}
```

**C) Append to Catalog**:
```python
catalog["arquivos"].append(catalog_entry)
catalog["metadata"]["total_arquivos"] += 1
catalog["metadata"]["ultima_atualizacao"] = datetime.now().isoformat()
```

**D) Save Catalog**:
```python
with open(catalog_path, 'w', encoding='utf-8') as f:
    json.dump(catalog, f, indent=2, ensure_ascii=False)
```

**Output**: Updated catalogo.json

### 7. Return Processing Report

**Actions**:
- Compile `$processed_file` object (see OUTPUT_CONTRACT)
- Include all metadata, paths, timing, quality scores
- Log success/failure
- Return to caller (mentor_orchestrator or /processar command)

**Output**: `$processed_file` (complete processing report)

## VALIDATION

### Quality Gates

| Check | Threshold | Action if Failed |
|-------|-----------|------------------|
| ✅ File extracted | Content length > 100 chars | Abort, return error |
| ✅ Categoria detected | Confidence > 0.5 | Request manual classification |
| ✅ Content synthesized | 800-1200 tokens | Auto-adjust (expand/condense) |
| ✅ Quality score | Overall ≥ 0.75 | Auto-improve weak dimensions (max 3 retries) |
| ✅ File saved | File exists at path | Retry save, abort if fails |
| ✅ Catalog updated | Entry added | Rollback file save, return error |
| ✅ Execution time | ≤ 10 minutes | Timeout, return partial results |

### Self-Validation Checklist

Before returning `$processed_file`:
- [ ] File saved in PROCESSADOS/ root (flat structure, no subfolders)
- [ ] Filename follows convention: `{categoria}_{assunto}_{date}.md`
- [ ] Quality score ≥ 0.75 (or ≥ 0.60 with auto-improvement)
- [ ] Token count 800-1200 (±10% acceptable)
- [ ] catalogo.json updated successfully
- [ ] All metadata fields populated
- [ ] Seller language validated (informal, no jargon)
- [ ] Brazil-specific examples included
- [ ] Actionable steps present

## CONTEXT

### Usage Scenarios

**Scenario 1**: Processing PDF guide from RASCUNHO
```bash
$rascunho_file = "RASCUNHO/guia_ml_titulos.pdf"
→ Extract text → Classify as marketplace_optimization → Synthesize → Validate (0.87) → Save to PROCESSADOS/
```

**Scenario 2**: Batch processing multiple files
```bash
/processar --batch RASCUNHO/*.pdf
→ Process each file sequentially → Return summary report
```

**Scenario 3**: Failed quality validation
```bash
Initial quality: 0.68 (clarity: 0.55, actionability: 0.62)
→ Auto-improve: Simplify language, make steps concrete
→ Revalidate: 0.76 (clarity: 0.72, actionability: 0.78)
→ Save
```

### Upstream Context

- Called by: `/processar` command, `mentor_orchestrator.md`
- Input from: User drops file in RASCUNHO/, or explicit command
- Context from: `scout_global_navigator_HOP` provides pattern guidance

### Downstream Context

- Calls: `quality_validator_5d_HOP.md` for validation
- Updates: `catalogo.json` for search indexing
- Outputs: Processed file in PROCESSADOS/ (used by mentor for answering questions)

### Integration with mentor_agent Workflow

```markdown
## Full Mentor Workflow
1. Seller adds file to RASCUNHO/ (e.g., guia_ml.pdf)
2. Seller runs: /processar guia_ml.pdf
3. Mentor orchestrator calls scout_global_navigator (optional, for context)
4. **Mentor calls knowledge_processor** ← YOU ARE HERE
   - Extract content from PDF
   - Classify as marketplace_optimization
   - Synthesize structured markdown
   - Validate quality (5D framework)
   - Save to PROCESSADOS/
5. Mentor returns success message to seller
6. Seller can now ask: "Me ensina sobre títulos de anúncio"
7. Mentor uses scout_internal → finds processed file → teaches
```

### Reusable Patterns from conhecimento_agent

This pipeline inherits proven patterns from `conhecimento_agent`:
- **RAW_FILES → CARDS → DATASETS** (equivalent to RASCUNHO → PROCESSADOS)
- **5D Quality Validation** (97.5% success rate on 66k+ cards)
- **Seller Language Translation** (informal Brazilian Portuguese)
- **Token Optimization** (800-1200 tokens sweet spot)
- **Flat Structure** (no subfolders for easy iteration)

### Assumptions

- RASCUNHO/ and PROCESSADOS/ directories exist
- File extraction libraries available (PyPDF2, python-docx, BeautifulSoup, etc.)
- quality_validator_5d_HOP.md is implemented and functional
- catalogo.json has correct schema
- File system has write permissions
- Seller language guide loaded from `config/seller_language_guide.json`
- Category taxonomy loaded from `config/categorias_conhecimento.json`

### Performance Notes

- **PDF extraction**: 2-5s per file
- **DOCX extraction**: 1-3s per file
- **Video transcription**: 10-60s (depends on length)
- **Classification**: 0.5-1s (keyword matching)
- **Synthesis**: 3-10s (LLM generation)
- **Validation**: 1-3s (5D scoring)
- **File save + catalog update**: 0.5-1s
- **Total estimate**: 10-90s per file (text), 30-120s (media)

---

**Version**: 1.0.0
**Last Updated**: 2025-11-13
**Dependencies**: quality_validator_5d_HOP
**Status**: Ready for Implementation
