# ANUNCIO_AGENT | Manual Configurations

**Version**: 1.0.0 | **Platform**: ChatGPT Responses API | **Date**: 2025-11-30

---

## Como Usar

Estas configuracoes sao aplicadas MANUALMENTE na interface do ChatGPT Responses.
Copie os valores para os campos correspondentes antes de iniciar a execucao.

---

## CONFIG 1: EFICIENTE (Token-Optimized)

**Use Case**: Batch processing, custo reduzido, alta velocidade
**Target Tokens**: ~18,000 (-68% vs baseline)
**Quality Trade-off**: Output completo, sem feedback visual

### Valores para Aplicar

| Campo | Valor | Motivo |
|-------|-------|--------|
| **Reasoning effort** | `medium` | Tarefa deterministica, high desnecessario |
| **Response** | `text` | Sem overhead de formatacao |
| **Verbosity** | `low` | Elimina mensagens de progresso |

### Tools (desmarcar se possivel)

| Tool | Status | Motivo |
|------|--------|--------|
| Code Interpreter | ON | Necessario para validacao |
| File Search | ON | Necessario para carregar HOPs |
| Web Search | OFF | Desnecessario quando URL ja fornecida |

### System Instructions (adicionar no fim)

```
OUTPUT_MODE: efficient
- Skip progress messages (Step 1/7...)
- Skip verbose explanations
- Output ONLY: PART 2 (Copyable Block) + minimal QA summary
- Batch Code Interpreter calls (max 5 calls total)
- No Web Search unless explicitly requested
```

### Expected Behavior

```
[Executa silenciosamente]
[Output final direto, sem feedback intermediario]

================================================================================
COPYABLE CONTENT
================================================================================
[Conteudo pronto para copiar]

QA: PASS | 0.95/1.0
```

---

## CONFIG 2: PERFORMANCE (Quality-Optimized)

**Use Case**: Producao final, qualidade maxima, revisao humana
**Target Tokens**: ~35,000 (-39% vs baseline de 57k)
**Quality Trade-off**: Feedback completo, melhor output possivel

### Valores para Aplicar

| Campo | Valor | Motivo |
|-------|-------|--------|
| **Reasoning effort** | `high` | Maximiza qualidade de copywriting |
| **Response** | `text` | Compativel com todas plataformas |
| **Verbosity** | `high` | Feedback completo para auditoria |

### Tools

| Tool | Status | Motivo |
|------|--------|--------|
| Code Interpreter | ON | Validacao rigorosa |
| File Search | ON | Contexto completo dos HOPs |
| Web Search | ON | Pesquisa complementar se necessario |

### System Instructions (adicionar no fim)

```
OUTPUT_MODE: performance
- Show progress messages (Step 1/7...)
- Include reasoning for copywriting decisions
- Output ALL 3 parts:
  - PART 1: Visual Review (formatted, with scores)
  - PART 2: Copyable Block (clean, in code fence)
  - PART 3: Source Attribution (JSON)
- Validate thoroughly with 5D scoring
- Include recommendations for improvement
```

### Expected Behavior

```
[Step 1/7] Parsing input...
  Confidence: 0.75 | Action: generate_with_suggestions

[Step 2/7] Generating titles...
  Reasoning: Using head_terms for SEO, diferenciais for differentiation
  Generated: 3 titles (58-60 chars each)

[Step 3/7] Expanding keywords...
...

================================================================================
PART 1: VISUAL REVIEW
================================================================================
[Output formatado com headers, tabelas, scores]

================================================================================
PART 2: COPYABLE CONTENT
================================================================================
```txt
[Conteudo limpo para copiar]
```

================================================================================
PART 3: SOURCE ATTRIBUTION
================================================================================
```json
{"titulos": {...}, "keywords": {...}, ...}
```

QA SUMMARY:
- Overall: 0.98/1.0 | PASS
- Recommendations: [list]
```

---

## Comparativo Rapido

| Aspecto | EFICIENTE | PERFORMANCE |
|---------|-----------|-------------|
| Tokens | ~18k | ~35k |
| Custo | -68% | -39% |
| Tempo | ~1 min | ~3-5 min |
| Feedback visual | Nenhum | Completo |
| Quality score | >= 0.85 | >= 0.95 |
| Code Interpreter calls | 5 max | 10-15 |
| Web Search | OFF | ON |
| Output parts | PART 2 only | PART 1+2+3 |
| Use case | Batch, testes | Producao final |

---

## Campos de Referencia (ChatGPT Responses UI)

### Reasoning Effort
- `low`: Resposta rapida, menos reflexao
- `medium`: Balanceado (RECOMENDADO para maioria)
- `high`: Maximo esforco, melhor qualidade

### Response Format
- `text`: Texto puro (mais compativel)
- `json`: Estruturado (para integracao)

### Verbosity
- `low`: Minimo output
- `normal`: Progresso basico
- `high`: Detalhado

### Tools Toggle
- Code Interpreter: Executa Python para validacao
- File Search: Busca arquivos no vector store
- Web Search: Pesquisa web (consome tokens extras)

---

## Troubleshooting

### "Output muito grande"
Use CONFIG 1 (Eficiente) ou adicione:
```
MAX_OUTPUT_TOKENS: 4000
SKIP_PART_1: true
```

### "Download nao funciona"
O download via sandbox tem limitacoes. Use PART 2 (Copyable Block) em code fence:
```txt
[conteudo]
```
Isso permite 1-click copy em qualquer interface.

### "Muitas chamadas Code Interpreter"
Adicione ao system prompt:
```
BATCH_VALIDATION: true
MAX_CODE_CALLS: 5
```

### "Web Search desnecessario"
Desmarque Web Search na UI ou adicione:
```
WEB_SEARCH: disabled
```

---

**Author**: codexa_agent
**Related**: PERFORMANCE_OPTIMIZATION_SPEC.md, PRIME.md
