# MANIFEST | {AGENT_NAME} iso_vectorstore v{VERSION}

**Package**: iso_vectorstore (drag-and-drop for any LLM)
**Agent**: {AGENT_NAME} | **Version**: {VERSION} | **Date**: {DATE}
**Scope**: {SCOPE}
**Output**: {OUTPUT_FORMAT}
**Files**: {FILE_COUNT} | **Total Tokens**: ~{TOKEN_ESTIMATE}

---

## DEPLOY CHECKLIST

```
[ ] Upload {FILE_COUNT} arquivos ao vector store / file search
[ ] Upload validator.py ao Code Interpreter (se aplicavel)
[ ] Aplicar config preset (EFICIENTE ou PERFORMANCE)
[ ] Testar com input de exemplo
[ ] Verificar output format
```

---

## FILE INVENTORY ({FILE_COUNT} Files)

### Core (00-05) ~{CORE_TOKENS} tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 00 | MANIFEST.md | ~400 | Package inventory |
| 01 | QUICK_START.md | ~600 | LLM entry point |
| 02 | PRIME.md | ~500 | Agent identity |
| 03 | INSTRUCTIONS.md | ~400 | Workflow rules |
| 04 | README.md | ~300 | Documentation |
| 05 | ARCHITECTURE.md | ~500 | Tech architecture |

### Config (06-10) ~{CONFIG_TOKENS} tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
{CONFIG_FILES_TABLE}

### Execution (11-12) ~{EXEC_TOKENS} tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 11 | ADW_orchestrator.md | ~400 | Workflow manager |
| 12 | execution_plans.json | ~400 | Full/Quick plans |

### HOPs (13-{LAST_HOP}) ~{HOP_TOKENS} tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
{HOP_FILES_TABLE}

### Reference ({REF_START}-{REF_END}) ~{REF_TOKENS} tokens

| # | File | Tokens | Purpose |
|---|------|--------|---------|
{REF_FILES_TABLE}

---

## TOKEN OPTIMIZATION

| Componente | Antes | Depois | Reducao |
|------------|-------|--------|---------|
{OPTIMIZATION_TABLE}

---

## CONFIG PRESETS

### EFICIENTE
```yaml
tokens_target: ~{EFFICIENT_TOKENS}
reasoning_effort: medium
verbosity: low
web_search: OFF
output: {EFFICIENT_OUTPUT}
```

### PERFORMANCE
```yaml
tokens_target: ~{PERFORMANCE_TOKENS}
reasoning_effort: high
verbosity: high
web_search: ON
output: {PERFORMANCE_OUTPUT}
```

---

## OUTPUT STRUCTURE

```
{OUTPUT_STRUCTURE}
```

---

## COMPATIBILITY

| Platform | Status |
|----------|--------|
| ChatGPT Responses API | OK |
| Claude Projects | OK |
| OpenAI Assistants | OK |
| Gemini | OK |

---

**Package**: {AGENT_NAME} iso_vectorstore v{VERSION}
**Status**: DEPLOY READY
**Tokens**: ~{TOKEN_ESTIMATE} (otimizado {REDUCTION_PERCENT})
**Date**: {DATE}
