# Lessons Learned | anuncio_agent Optimization v3.2→v3.5

**Date**: 2025-11-30
**Source**: Production deployment and log analysis
**Purpose**: Enrich ADW-104 with real-world patterns

---

## PATTERN 1: File Name Verification

**Problem**: SYSTEM_INSTRUCTIONS referenced files that didn't exist
- `13_HOP_main.md` → actual file: `13_HOP_main_agent.md`
- `16_HOP_bullets_creator.md` → actual file: `16_HOP_bullet_points.md`

**Solution**: Add STEP 8.5 - Cross-reference all file names in SYSTEM_INSTRUCTIONS with actual iso_vectorstore files

**Checklist**:
```yaml
- [ ] Every doc reference in SYSTEM_INSTRUCTIONS exists in iso_vectorstore
- [ ] Use hybrid format: {number}_{name}.md (e.g., 13_HOP_main_agent.md)
- [ ] DOCUMENT REFERENCE table lists ALL 21 files
```

---

## PATTERN 2: Output Format - Single Code Block

**Problem**: GPT duplicated content (PART 1 + PART 2) and didn't use code fences

**Before (v3.4)**:
```
PART 1: Visual Block (for review)
PART 2: Copyable Block (for download)
PART 3: JSON (optional)
```

**After (v3.5)**:
```
ONE code block with triple backticks containing ALL content
```

**Solution**: Add STEP 8.6 - OUTPUT FORMAT section with:
- REGRA ABSOLUTA: UM ÚNICO CODE BLOCK
- Template explícito do formato
- PROIBIDO: duplicação, texto fora do code block

**Template**:
~~~markdown
# OUTPUT FORMAT - CRITICAL

## REGRA ABSOLUTA: UM ÚNICO CODE BLOCK

**TODA a resposta final DEVE estar dentro de UM ÚNICO bloco de código** usando triple backticks.

**FORMATO OBRIGATÓRIO:**
~~~
```
[todo o conteúdo aqui dentro]
```
~~~

**PROIBIDO:**
- NÃO duplique conteúdo (nada de PART 1 + PART 2 separados)
- NÃO coloque texto fora do code block
~~~

---

## PATTERN 3: Constraints Update

**Problem**: Constraints didn't explicitly forbid duplication

**Solution**: Add to CONSTRAINTS section:
```markdown
- ALWAYS output inside ONE code block (triple backticks)
- NEVER duplicate content (no PART 1 + PART 2)
- NEVER output text outside the code block
```

---

## PATTERN 4: Self-Validation Checklist

**Problem**: Self-validation didn't check for code block format

**Solution**: Add CRITICAL checks:
```markdown
- [ ] **Output is ONE code block with triple backticks?** (CRITICAL)
- [ ] **No text outside the code block?** (CRITICAL)
- [ ] **No duplicated content?** (CRITICAL)
```

---

## PATTERN 5: Token Optimization Rules

**Problem**: 47k tokens consumed (target 35k)
- 11 empty reasoning items
- 20+ code interpreter calls (target 5)
- Unnecessary web searches

**Solution**: Add TOKEN OPTIMIZATION section:
```markdown
**Rules**:
1. **Batch Code Interpreter Calls**: Target <= 5 calls total
2. **Web Search Policy**: DISABLE when URL/research provided
3. **Reasoning Efficiency**: NEVER emit empty blocks
4. **File Search Optimization**: All 21 docs loaded at once
5. **Output Efficiency**: ONE code block only
```

---

## PATTERN 6: Document Reference Table

**Problem**: Original table only listed 15 of 21 files

**Solution**: Complete DOCUMENT REFERENCE with ALL files:
```markdown
| # | Document | Purpose | Used in Step |
|---|----------|---------|--------------|
| 00 | MANIFEST.md | Package inventory | - |
| 01 | QUICK_START.md | LLM entry point | - |
| ... | ... | ... | ... |
| 20 | quality_dimensions.json | 5D scoring schema | 6 |
```

---

## PATTERN 7: Meta-HOP Orchestrator Architecture

**Problem**: SYSTEM_INSTRUCTIONS was just a list of instructions

**Solution**: Structure as META-HOP ORCHESTRATOR:
```markdown
# WORKFLOW ORCHESTRATION (7 Steps)

Este é um **meta-HOP orquestrador**. Cada step referencia documentos do iso_vectorstore.
O output de cada step é **input do próximo** (chaining).

## STEP 1: PARSE INPUT
**Doc**: `13_HOP_main_agent.md`
**Input**: `{$INPUT}` (any source)
**Output**: `{parsed_input, confidence, fallback_action}`

## STEP 2: GENERATE {CONTENT}
**Doc**: `14_HOP_{content}_generator.md`
**Input**: `{parsed_input}` ← from STEP 1
**Output**: `{content}`
...
```

---

## PATTERN 8: Production Testing Feedback Loop

**Process**:
1. Deploy SYSTEM_INSTRUCTIONS v1
2. Run test with real input
3. Analyze log for issues
4. Fix issues in v2
5. Redeploy and verify

**Issues found in production**:
- Empty reasoning blocks → Add "NEVER emit empty blocks"
- Excessive code interpreter → Add batching rule
- Unnecessary web search → Add policy
- Duplicated output → Rewrite OUTPUT FORMAT
- No code fence → Explicit instruction

---

## UPDATED ADW-104 STEPS

### NEW STEP 8.5: VERIFY FILE REFERENCES
After generating SYSTEM_INSTRUCTIONS, verify:
- [ ] All doc references match actual filenames
- [ ] No typos in file names
- [ ] Hybrid format used (number + name)

### NEW STEP 8.6: OUTPUT FORMAT
Add single code block section:
- [ ] REGRA ABSOLUTA defined
- [ ] Template with triple backticks
- [ ] PROIBIDO list

### NEW STEP 8.7: UPDATE CONSTRAINTS
Add code block rules:
- [ ] ALWAYS output inside ONE code block
- [ ] NEVER duplicate content
- [ ] NEVER output text outside

### NEW STEP 8.8: UPDATE SELF-VALIDATION
Add CRITICAL checks:
- [ ] Code block check
- [ ] No duplication check
- [ ] No text outside check

### NEW STEP 11: PRODUCTION TEST (Optional)
If possible:
- [ ] Deploy to ChatGPT Responses
- [ ] Run test with sample input
- [ ] Analyze log for issues
- [ ] Fix and redeploy if needed

---

## METRICS

| Version | Tokens | Duplication | Code Block | Score |
|---------|--------|-------------|------------|-------|
| v3.2.0 | 47,472 | PART 1+2 | No | 1.0 |
| v3.4.0 | 50,269 | PART 1+2 | No | 1.0 |
| v3.5.0 | 45,077 | None | Yes | 0.98 |

**Improvement**: -11% tokens, no duplication, proper format

---

**Document**: LESSONS_LEARNED_ANUNCIO_AGENT.md
**Version**: 1.0.0
**Author**: codexa_agent
**Date**: 2025-11-30
