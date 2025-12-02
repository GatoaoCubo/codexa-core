# Agent Builder Patterns | OpenAI Platform Optimization

**Version**: 1.0.0 | **Created**: 2025-11-30
**Purpose**: Engineering patterns for OpenAI Agent Builder with File Search optimization
**Type**: Technical Reference | **Applies To**: All iso_vectorstore files

---

## OVERVIEW

This document captures best practices for structuring files used in OpenAI Agent Builder's File Search (vector store) feature. Based on empirical testing and platform analysis.

**Key Insight**: File Search chunks documents into ~800 token segments with 400 token overlap. Structure files to optimize for this chunking behavior.

---

## FILE SEARCH CONFIGURATION

### Default Settings (OpenAI)

| Parameter | Default | Range | Recommendation |
|-----------|---------|-------|----------------|
| Chunk Size | 800 tokens | 100-4096 | 800 (default works well) |
| Chunk Overlap | 400 tokens | 0 to chunk_size/2 | 400 (50% overlap optimal) |

### Token Estimation

```
1 token ~= 4 characters (English)
1 token ~= 3 characters (Portuguese)

800 tokens ~= 2400-3200 chars
400 tokens ~= 1200-1600 chars
```

---

## STRUCTURAL PATTERNS

### Pattern 1: Self-Contained Sections

**Problem**: Long sections get split across chunks, losing context.

**Solution**: Keep each section under 600 tokens (~2000 chars) so it fits in one chunk with room for header/footer context.

**BAD** (section too long):
```markdown
## Configuration

This is a very long section that spans 2000+ tokens
explaining configuration in great detail...
[continues for 3000 more characters]
...and finally ends here.
```

**GOOD** (section split logically):
```markdown
## Configuration Overview

Brief explanation of configuration system. Max 500 tokens.
Key points: X, Y, Z.

---

## Configuration: Required Fields

Detailed required fields. Max 500 tokens each section.
Fields: A, B, C with descriptions.

---

## Configuration: Optional Fields

Optional fields explanation. Separate chunk-friendly section.
```

---

### Pattern 2: Header-Content Proximity

**Problem**: With 400 token overlap, headers may appear without their content (or vice versa).

**Solution**: Repeat key terms in both header AND first line of content.

**BAD**:
```markdown
## Validation

The system checks all inputs against defined schemas...
```

**GOOD**:
```markdown
## Validation Rules for Input Schema

Validation rules check all inputs against the input_schema.json...
```

---

### Pattern 3: Keyword Density in Headers

**Problem**: File Search uses semantic similarity. Generic headers reduce findability.

**Solution**: Include specific keywords in H2/H3 headers.

**BAD**:
```markdown
## Overview
## Details
## Usage
```

**GOOD**:
```markdown
## anuncio_agent Overview and Purpose
## Title Generation Details (58-60 chars)
## Keywords Expansion Usage (115-120 terms)
```

---

### Pattern 4: Reference Anchors

**Problem**: Cross-file references get lost in chunking.

**Solution**: Use explicit file references with numbers.

**BAD**:
```markdown
See the output template for formatting.
```

**GOOD**:
```markdown
See 07_output_template.md for single-block formatting rules.
```

---

### Pattern 5: Inline Context

**Problem**: Chunks lack context about which agent/file they belong to.

**Solution**: Include agent name in section headers.

**BAD**:
```markdown
## Workflow Phases
```

**GOOD**:
```markdown
## anuncio_agent Workflow Phases (6 Core)
```

---

## FILE STRUCTURE TEMPLATE

Optimal structure for iso_vectorstore files:

```markdown
# {FILE_NUMBER}_{FILE_NAME} | {AGENT_NAME}

**Version**: X.Y.Z | **Purpose**: One-line description
**Type**: Config/Template/HOP/ADW | **Updated**: YYYY-MM-DD

---

## {AGENT_NAME} {SECTION_1_TITLE}

{Content under 600 tokens. Self-contained. Keywords in first sentence.}

---

## {AGENT_NAME} {SECTION_2_TITLE}

{Content under 600 tokens. Repeat key terms from header.}

---

## {AGENT_NAME} Quick Reference

| Term | Definition |
|------|------------|
| ... | ... |

---

**File**: {NUMBER}_{NAME} | **Agent**: {AGENT_NAME} | **Version**: X.Y.Z
```

---

## CHUNKING OPTIMIZATION CHECKLIST

Before uploading to File Search:

- [ ] Each section < 600 tokens (~2000 chars)
- [ ] Headers include agent name and keywords
- [ ] First sentence repeats header keywords
- [ ] Cross-references use file numbers (e.g., "07_output_template.md")
- [ ] No orphan headers (content immediately follows)
- [ ] Footer includes file identifier for chunk attribution
- [ ] Tables have descriptive headers (not just "Item | Value")
- [ ] Code blocks have language tags and comments

---

## TOOLS INTEGRATION

### Code Interpreter

When available, use Code Interpreter for:

1. **Metric Calculation**: Character counts, keyword density
2. **Slug Generation**: Product names to file-safe slugs
3. **JSON Validation**: Schema compliance checking
4. **Timestamp Generation**: ISO format dates

**Example prompt addition**:
```markdown
## Code Interpreter Usage (anuncio_agent)

When Code Interpreter is available:
- Calculate exact character counts for titles (target: 58-60)
- Validate JSON structure of output
- Generate file slug: `anuncio_{slugify(product_name)}_{date}.md`
- Count keywords in each block (target: 115-120)
```

### File Search

Optimize queries by:
- Using exact file names in questions
- Including section headers in queries
- Referencing file numbers (01, 07, 13-18)

---

## KNOWN PLATFORM ISSUES

### Issue 1: Code Interpreter File Downloads (Nov 2025)

**Problem**: Files generated by Code Interpreter show non-clickable "Download Link" text.

**Status**: Unresolved (community.openai.com/t/1364793)

**Workaround**: Use "Method A" - present file content in code blocks with save instructions.

```markdown
## Download Section

\`\`\`txt
[File content here]
\`\`\`

### Save Instructions
1. Copy content from code block
2. Paste in text editor
3. Save as filename.ext
```

### Issue 2: Chunk Boundary Loss

**Problem**: Important context split across chunk boundaries.

**Workaround**:
- Use 50% overlap (400/800)
- Repeat key terms in adjacent sections
- Keep critical info in section first 200 tokens

---

## METRICS

### Optimal File Sizes

| File Type | Tokens | Chars | Chunks |
|-----------|--------|-------|--------|
| QUICK_START | 1500-2000 | 5000-7000 | 3-4 |
| INSTRUCTIONS | 2500-3500 | 8000-12000 | 5-7 |
| HOP modules | 3000-5000 | 10000-17000 | 6-10 |
| Config JSON | 1000-3000 | 4000-12000 | 2-5 |
| Templates | 1500-2500 | 5000-9000 | 3-5 |

### Chunk Coverage

With 800/400 config:
- 2000 char section = 1 chunk (good)
- 4000 char section = 2 chunks with overlap (acceptable)
- 8000 char section = 4+ chunks (consider splitting)

---

## IMPLEMENTATION EXAMPLES

### Example: Dual Output Section

Optimized for chunking - each part is self-contained:

```markdown
## anuncio_agent Output Format PART 1 (Visual Block)

Visual block output for copy-paste. Uses decorative separators.
Contains: Titles, Description, Bullets, Keywords, Metadata.
User copies individual sections as needed.

See 07_output_template.md for complete template structure.

---

## anuncio_agent Output Format PART 2 (Download Block)

Download block for file saving. Clean text without emojis.
Wrapped in \`\`\`txt code fence for easy copying.
Includes save instructions and filename convention.

File naming: anuncio_{product_slug}_{YYYYMMDD}.md
```

---

## RELATED DOCUMENTATION

- `PRIME.md` - Meta-construction principles
- `templates/REPORT_STANDARD.md` - Output formatting
- `workflows/` - ADW patterns

---

**Version**: 1.0.0 | **Created**: 2025-11-30 | **Author**: CODEXA Meta-System
**Status**: Production Reference | **Applies To**: All Agent Builder deployments
