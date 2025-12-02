# 22_agent_builder_patterns | codexa_agent Platform Optimization

**Version**: 1.0.0 | **Purpose**: Engineering patterns for OpenAI Agent Builder
**Type**: Technical Reference | **Updated**: 2025-11-30
**Applies To**: All iso_vectorstore files across agents

---

## codexa_agent Agent Builder Overview

This document captures best practices for structuring files used in OpenAI Agent Builder's File Search (vector store) feature.

**Key Insight**: File Search chunks documents into ~800 token segments with 400 token overlap. Structure files to optimize for this chunking behavior.

---

## codexa_agent File Search Configuration

### Default Settings (OpenAI Platform)

| Parameter | Default | Range | Recommendation |
|-----------|---------|-------|----------------|
| Chunk Size | 800 tokens | 100-4096 | 800 (default optimal) |
| Chunk Overlap | 400 tokens | 0 to chunk_size/2 | 400 (50% overlap) |

### Token Estimation Rules

```
1 token ~= 4 characters (English)
1 token ~= 3 characters (Portuguese)

800 tokens ~= 2400-3200 chars
400 tokens ~= 1200-1600 chars
```

---

## codexa_agent Structural Pattern 1: Self-Contained Sections

**Problem**: Long sections get split across chunks, losing context.

**Solution**: Keep each section under 600 tokens (~2000 chars).

**BAD** (section too long):
```markdown
## Configuration
[2000+ tokens of content without breaks]
```

**GOOD** (section split logically):
```markdown
## Configuration Overview
[Brief intro, max 500 tokens]

---

## Configuration: Required Fields
[Details, max 500 tokens]

---

## Configuration: Optional Fields
[Details, max 500 tokens]
```

---

## codexa_agent Structural Pattern 2: Header-Content Proximity

**Problem**: With 400 token overlap, headers may appear without content.

**Solution**: Repeat key terms in header AND first line.

**BAD**:
```markdown
## Validation
The system checks all inputs...
```

**GOOD**:
```markdown
## Validation Rules for Input Schema
Validation rules check all inputs against input_schema.json...
```

---

## codexa_agent Structural Pattern 3: Keyword-Rich Headers

**Problem**: Generic headers reduce findability in File Search.

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

## codexa_agent Structural Pattern 4: Agent Name Anchoring

**Problem**: Chunks lack context about which agent/file they belong to.

**Solution**: Include agent name in section headers.

**Template**:
```markdown
## {agent_name} {Section Title}
```

**Examples**:
- `## anuncio_agent Workflow Phases`
- `## pesquisa_agent Data Sources`
- `## codexa_agent Meta-Construction`

---

## codexa_agent Structural Pattern 5: File Number References

**Problem**: Cross-file references get lost in chunking.

**Solution**: Use explicit file numbers.

**BAD**:
```markdown
See the output template for formatting.
```

**GOOD**:
```markdown
See 07_output_template.md for single-block formatting rules.
```

---

## codexa_agent File Template for iso_vectorstore

```markdown
# {NUMBER}_{FILE_NAME} | {AGENT_NAME}

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

## codexa_agent Optimal File Sizes

| File Type | Tokens | Chars | Chunks |
|-----------|--------|-------|--------|
| QUICK_START | 1500-2000 | 5000-7000 | 3-4 |
| INSTRUCTIONS | 2500-3500 | 8000-12000 | 5-7 |
| HOP modules | 3000-5000 | 10000-17000 | 6-10 |
| Config JSON | 1000-3000 | 4000-12000 | 2-5 |
| Templates | 1500-2500 | 5000-9000 | 3-5 |

---

## codexa_agent Tools Integration

### Code Interpreter Usage

When available, use for:

| Task | Example |
|------|---------|
| Metric calculation | Character counts, keyword density |
| Slug generation | Product names to file-safe slugs |
| JSON validation | Schema compliance checking |
| Timestamp generation | ISO format dates |

### File Search Optimization

Query optimization:
- Use exact file names in questions
- Include section headers in queries
- Reference file numbers (01, 07, 13-18)

---

## codexa_agent Known Platform Issues

### Issue 1: Code Interpreter Downloads (Nov 2025)

**Problem**: Files generated show non-clickable "Download Link" text.

**Status**: Unresolved

**Workaround**: Method A - content in code blocks with save instructions.

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

### Issue 2: Chunk Boundary Context Loss

**Problem**: Important context split across boundaries.

**Workaround**:
- Use 50% overlap (400/800)
- Repeat key terms in adjacent sections
- Keep critical info in first 200 tokens of section

---

## codexa_agent Chunking Checklist

Before uploading to File Search:

- [ ] Each section < 600 tokens (~2000 chars)
- [ ] Headers include agent name and keywords
- [ ] First sentence repeats header keywords
- [ ] Cross-references use file numbers
- [ ] No orphan headers (content immediately follows)
- [ ] Footer includes file identifier
- [ ] Tables have descriptive headers
- [ ] Code blocks have language tags

---

## codexa_agent Application to Other Agents

This pattern applies to all agent iso_vectorstore directories:

| Agent | iso_vectorstore Files |
|-------|----------------------|
| anuncio_agent | 20 files (01-20) |
| pesquisa_agent | Similar structure |
| marca_agent | Similar structure |
| codexa_agent | 22 files (01-22) |

**Consistency rule**: All agents should follow same structural patterns for File Search optimization.

---

**File**: 22_agent_builder_patterns.md | **Agent**: codexa_agent | **Version**: 1.0.0
