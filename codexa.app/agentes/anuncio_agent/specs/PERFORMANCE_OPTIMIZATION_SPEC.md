# ANUNCIO_AGENT Performance Optimization Spec

**Version**: 1.0.0 | **Date**: 2025-11-30 | **Type**: Performance Analysis + Configuration Guide

---

## 1. DIAGNOSTIC: Log Analysis (57k tokens)

### Token Breakdown

| Component | Tokens | % Total | Assessment |
|-----------|--------|---------|------------|
| **Input (System + User)** | 34,915 | 61.2% | HIGH - System prompt muito verbose |
| **Output (Response)** | 22,090 | 38.8% | OK - Conteudo util |
| **TOTAL** | 57,005 | 100% | Target: <25k |

### Inefficiencies Identified

#### A. Code Interpreter Overuse (~30+ calls)
```
Problem: Multiplas chamadas para tarefas simples
- Linhas 221-280: 10+ calls so para ajustar tamanho de titulos (58-60 chars)
- Linhas 304-402: 6+ calls para ajustar contagem de keywords
- Linhas 669-876: 3+ rewrites do mesmo arquivo .txt

Impact: ~5,000 tokens desperdicados
Fix: Batch operations, pre-compute constraints in memory
```

#### B. Empty Reasoning Items (15+ occurrences)
```
Problem: "Empty reasoning item" aparece repetidamente
- Cada occurrence = tokens de overhead sem valor

Impact: ~500-1,000 tokens desperdicados
Fix: reasoning_effort=medium para tarefas deterministicas
```

#### C. Unnecessary Web Search (2 calls)
```
Problem: Web Search acionado quando input ja tinha URL do produto
- Linha 166: "Searched the web"
- Linha 169: "Searched the web"

Impact: ~2,000 tokens (results + processing)
Fix: Disable web_search quando URL ja fornecida
```

#### D. System Prompt Verbosity
```
Problem: System instructions = ~4,000 chars (muito denso)
- Tabelas markdown nao sao token-efficient
- Exemplos completos de codigo no system prompt
- Duplicacao de regras em multiplas secoes

Impact: ~8,000 tokens fixos por request
Fix: Modularizar instructions, carregar sob demanda via File Search
```

#### E. Duplicate Content Generation
```
Problem: Mesmo conteudo escrito 3x no log
- Descricao completa no Code Interpreter
- Descricao no arquivo .txt (reescrito 2x)
- Descricao no output final

Impact: ~4,000 tokens duplicados
Fix: Generate once, reference thereafter
```

### Performance Score

| Metric | Current | Target | Gap |
|--------|---------|--------|-----|
| Total Tokens | 57,005 | <25,000 | -56% needed |
| Code Interpreter Calls | ~30 | <10 | -67% needed |
| Execution Time | ~3-5min | <1min | -80% needed |
| Output Reusability | 60% | 95% | +35% needed |

---

## 2. CONFIGURATION VARIABLES

### Variable Matrix (Token-Efficiency vs UX)

```json
{
  "AGENT_CONFIG_TEMPLATE": {
    "version": "1.0.0",
    "variables": {
      "reasoning_effort": {
        "type": "enum",
        "options": ["low", "medium", "high"],
        "default": "[TASK_COMPLEXITY]",
        "token_impact": {
          "low": "-40%",
          "medium": "baseline",
          "high": "+60%"
        },
        "ux_impact": {
          "low": "Fast, may miss edge cases",
          "medium": "Balanced, good for most tasks",
          "high": "Thorough, slower, more expensive"
        },
        "recommendation": "medium for anuncio_agent (deterministic task)"
      },

      "output_format": {
        "type": "enum",
        "options": ["text", "json", "markdown", "hybrid"],
        "default": "[USER_PREFERENCE]",
        "token_impact": {
          "text": "baseline",
          "json": "+10% (structure overhead)",
          "markdown": "+5% (formatting)",
          "hybrid": "+15% (both formats)"
        },
        "ux_impact": {
          "text": "Human-readable, copy/paste friendly",
          "json": "Machine-parseable, API-ready",
          "markdown": "Formatted, visual hierarchy",
          "hybrid": "Best of both, highest tokens"
        },
        "recommendation": "text for copy/paste, json for automation"
      },

      "verbosity": {
        "type": "enum",
        "options": ["minimal", "normal", "high"],
        "default": "[FEEDBACK_PREFERENCE]",
        "token_impact": {
          "minimal": "-30%",
          "normal": "baseline",
          "high": "+40%"
        },
        "ux_impact": {
          "minimal": "Only final output, no progress",
          "normal": "Key milestones (Step 1/7...)",
          "high": "Every operation detailed"
        },
        "recommendation": "normal (Step 1/7 progress)"
      },

      "summary_mode": {
        "type": "enum",
        "options": ["none", "brief", "detailed"],
        "default": "[TASK_TYPE]",
        "token_impact": {
          "none": "-5%",
          "brief": "baseline",
          "detailed": "+15%"
        },
        "ux_impact": {
          "none": "No summary, direct output",
          "brief": "2-3 line summary at start",
          "detailed": "Full context + rationale"
        },
        "recommendation": "brief for production, detailed for debug"
      },

      "display_response_on_chat": {
        "type": "boolean",
        "default": true,
        "token_impact": {
          "true": "baseline",
          "false": "-0% (still generated)"
        },
        "ux_impact": {
          "true": "User sees response immediately",
          "false": "Silent mode (API/automation only)"
        },
        "recommendation": "true for interactive, false for batch"
      },

      "show_in_progress_messages": {
        "type": "boolean",
        "default": "[VERBOSITY_DERIVED]",
        "token_impact": {
          "true": "+5% (status messages)",
          "false": "baseline"
        },
        "ux_impact": {
          "true": "User sees Step 1... Step 2...",
          "false": "Waits until complete"
        },
        "recommendation": "true for UX, false for token savings"
      },

      "show_search_source": {
        "type": "boolean",
        "default": false,
        "token_impact": {
          "true": "+10% (citations)",
          "false": "baseline"
        },
        "ux_impact": {
          "true": "Shows [Fonte: X] per section",
          "false": "Clean output without attribution"
        },
        "recommendation": "false for copy/paste, true for audit"
      },

      "write_to_conversation_history": {
        "type": "boolean",
        "default": true,
        "token_impact": {
          "true": "+cumulative (grows per turn)",
          "false": "constant (no history)"
        },
        "ux_impact": {
          "true": "Context preserved across turns",
          "false": "Each turn is independent"
        },
        "recommendation": "true for iterative, false for 1-shot"
      },

      "continue_on_error": {
        "type": "boolean",
        "default": true,
        "token_impact": {
          "true": "variable (may add recovery tokens)",
          "false": "may save tokens (early exit)"
        },
        "ux_impact": {
          "true": "Best effort output even with issues",
          "false": "Fails fast, clearer error handling"
        },
        "recommendation": "true for production, false for debug"
      }
    }
  }
}
```

### Preset Configurations

#### PRESET: Token-Optimized (Production Batch)
```json
{
  "reasoning_effort": "medium",
  "output_format": "text",
  "verbosity": "minimal",
  "summary_mode": "none",
  "display_response_on_chat": false,
  "show_in_progress_messages": false,
  "show_search_source": false,
  "write_to_conversation_history": false,
  "continue_on_error": true,
  "_expected_tokens": "~18,000 (-68%)",
  "_use_case": "Batch processing, API automation"
}
```

#### PRESET: UX-Optimized (Interactive)
```json
{
  "reasoning_effort": "medium",
  "output_format": "markdown",
  "verbosity": "normal",
  "summary_mode": "brief",
  "display_response_on_chat": true,
  "show_in_progress_messages": true,
  "show_search_source": true,
  "write_to_conversation_history": true,
  "continue_on_error": true,
  "_expected_tokens": "~35,000 (-39%)",
  "_use_case": "Interactive chat, user iteration"
}
```

#### PRESET: Balanced (Recommended Default)
```json
{
  "reasoning_effort": "medium",
  "output_format": "text",
  "verbosity": "normal",
  "summary_mode": "brief",
  "display_response_on_chat": true,
  "show_in_progress_messages": true,
  "show_search_source": false,
  "write_to_conversation_history": true,
  "continue_on_error": true,
  "_expected_tokens": "~25,000 (-56%)",
  "_use_case": "Default for most users"
}
```

---

## 3. OUTPUT STRUCTURE (Copyable Block Proposal)

### Current Problem
```
- Download link aparece mas nao funciona (sandbox limitation)
- User precisa scroll/select para copiar
- Conteudo misturado com formatting/metadata
```

### Proposed Solution: 3-Part Output

```markdown
## OUTPUT STRUCTURE v2.0

### PART 1: VISUAL (Display Only)
- Formatted with headers, separators
- Quality report, source attribution
- For: Reading, reviewing, auditing
- Tokens: ~3,000

### PART 2: COPYABLE BLOCK (Reusable)
- Plain text, no markdown
- ONLY the content user needs to paste
- Wrapped in code fence for easy copy
- For: Copy/paste to marketplace
- Tokens: ~2,500

### PART 3: STRUCTURED DATA (Optional)
- JSON format if requested
- Machine-readable
- For: API integration, automation
- Tokens: ~1,500 (only if enabled)
```

### Implementation Template

```markdown
===============================================================
PART 1: VISUAL REVIEW
===============================================================
[Full formatted output with headers, scores, attribution]

===============================================================
PART 2: COPYABLE CONTENT
===============================================================
```txt
[START_COPY]
TITULO: Caixa Retratil Dobravel para Transporte de Gato Cachorro Pet

DESCRICAO:
Se levar seu pet com voce e parte da sua rotina...
[full text without markdown]

BULLETS:
1. Conforto imediato para seu pet...
2. Seguranca que da tranquilidade...
[etc]

KEYWORDS BLOCO 1:
caixa transportadora, transportadora pet, caixa para pet...

KEYWORDS BLOCO 2:
transportadora compacta, caixa pet para viagem...
[END_COPY]
```

===============================================================
PART 3: JSON (if show_structured=true)
===============================================================
```json
{"titulos": [...], "descricao": "...", "bullets": [...], "keywords": {...}}
```
```

### Benefits
1. **Copy button works**: Code fence = one-click copy
2. **No scroll hunting**: Clearly marked sections
3. **Platform agnostic**: Works in ChatGPT, Claude, any interface
4. **Token efficient**: User enables only parts needed

---

## 4. IMPLEMENTATION CHECKLIST

### Phase 1: System Prompt Optimization
- [ ] Modularize instructions (move examples to File Search)
- [ ] Remove markdown tables from system prompt
- [ ] Reduce duplicated rules
- [ ] Target: -8,000 tokens from input

### Phase 2: Code Interpreter Consolidation
- [ ] Batch character counting operations
- [ ] Pre-compute constraints before generation
- [ ] Single file write instead of multiple rewrites
- [ ] Target: -5,000 tokens from Code Interpreter

### Phase 3: Output Structure Update
- [ ] Implement 3-part output template
- [ ] Add code fence for copyable block
- [ ] Make PART 3 (JSON) optional via config
- [ ] Target: Better UX without token increase

### Phase 4: Configuration System
- [ ] Add config variables to anuncio_agent
- [ ] Create preset selector in instructions
- [ ] Document trade-offs per variable
- [ ] Target: User control over token/UX balance

---

## 5. METRICS & VALIDATION

### Success Criteria
| Metric | Before | After | Target |
|--------|--------|-------|--------|
| Total Tokens | 57,005 | TBD | <25,000 |
| Code Interpreter Calls | ~30 | TBD | <10 |
| Output Copyability | 60% | TBD | 95% |
| User Effort (copy) | 3+ actions | TBD | 1 click |

### Validation Commands
```bash
# After implementation, validate with:
python validators/07_hop_sync_validator.py anuncio_agent/prompts/13_HOP_main_agent.md
python validators/12_doc_sync_validator.py --agent anuncio_agent
```

---

**Author**: codexa_agent (meta-constructor)
**Related**: PRIME.md (anuncio_agent), INSTRUCTIONS.md
**Next**: Implement changes, measure delta, iterate
