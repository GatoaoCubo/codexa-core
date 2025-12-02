# PLAN: ADW iso_vectorstore Optimization System

**Version**: 1.0.0 | **Date**: 2025-11-30
**Status**: PLANNING | **Author**: codexa_agent + human

---

## OBJETIVO

Criar um sistema escalavel para otimizar TODOS os agents' iso_vectorstore seguindo o padrao estabelecido no anuncio_agent v3.2.0.

**Problema**: 7 agents excedem limite de 20 arquivos e provavelmente tem HOPs com token bloat (~20-30k tokens cada)

**Solucao**: ADW reutilizavel que qualquer LLM pode executar para otimizar iso_vectorstore de qualquer agent

---

## BASELINE (anuncio_agent v3.2.0)

### Resultado Alcancado
| Metrica | Antes | Depois | Reducao |
|---------|-------|--------|---------|
| Arquivos | 24 | 21 | -12.5% |
| Tokens totais | ~80,000 | ~8,000 | -90% |
| HOP 14 (titulo) | 26,000 | 800 | -97% |
| HOP 17 (descricao) | 34,000 | 1,200 | -96% |

### Padroes Identificados
1. **Garbage injection**: HOPs continham metadata, YAML, codigo duplicado
2. **Out-of-scope files**: image_prompts, video_script em agent TEXT-ONLY
3. **Version inconsistency**: Arquivos misturando v2.5.0, v3.1.0, v3.2.0
4. **Missing MANIFEST**: Sem inventario claro de arquivos
5. **Missing SYSTEM_INSTRUCTIONS**: Sem instrucoes padronizadas para deploy

---

## DELIVERABLES

### 1. ADW Workflow (novo)
```
codexa_agent/workflows/104_ADW_ISO_VECTORSTORE_OPTIMIZATION.md
```
- 10-step workflow similar ao ADW-100
- Input: agent_name ou "all"
- Output: iso_vectorstore otimizado + reports

### 2. Templates Reutilizaveis
```
codexa_agent/templates/iso_vectorstore/
├── 00_MANIFEST_TEMPLATE.md
├── SYSTEM_INSTRUCTIONS_TEMPLATE.md
├── HOP_TEMPLATE.md
└── OPTIMIZATION_CHECKLIST.md
```

### 3. Spec de Referencia
```
codexa_agent/specs/ISO_VECTORSTORE_STANDARD.md
```
- Estrutura padrao (21 arquivos max)
- Limites de tokens por tipo de arquivo
- Regras de compliance
- Chunk settings recomendados

### 4. Validator (opcional)
```
codexa_agent/validators/15_iso_vectorstore_validator.py
```
- Valida file count, token count, version consistency
- Score 0.0-1.0 como outros validators

---

## ADW-104: ISO_VECTORSTORE_OPTIMIZATION

### STEP 1: DISCOVERY
- Scan agent/iso_vectorstore/
- Count files, estimate tokens
- Identify: HOPs, configs, docs, frameworks
- Detect version inconsistencies

### STEP 2: SCOPE ANALYSIS
- Ler PRIME.md do agent
- Identificar scope (TEXT-ONLY, VISUAL, etc)
- Listar arquivos out-of-scope

### STEP 3: HOP TOKEN AUDIT
- Para cada HOP_*.md:
  - Contar tokens (chars / 4)
  - Detectar garbage (YAML blocks, duplicate content, metadata injection)
  - Flag se > 1500 tokens

### STEP 4: GENERATE MANIFEST
- Criar 00_MANIFEST.md usando template
- Inventario de arquivos com token estimates
- Deploy checklist

### STEP 5: OPTIMIZE HOPS
- Para cada HOP com > 1500 tokens:
  - Remover garbage injection
  - Preservar instrucoes essenciais
  - Target: 600-1200 tokens/HOP

### STEP 6: REMOVE OUT-OF-SCOPE
- Deletar arquivos fora do scope
- Renumerar se necessario
- Atualizar referencias

### STEP 7: VERSION SYNC
- Definir versao canonica
- Atualizar todos arquivos
- Atualizar MANIFEST

### STEP 8: GENERATE SYSTEM_INSTRUCTIONS
- Criar/atualizar SYSTEM_INSTRUCTIONS_AGENT_BUILDER.md
- Usar template com {$variables}
- Adicionar exemplos de uso

### STEP 9: VALIDATE
- File count <= 21
- Tokens estimados < 15k
- Version consistency 100%
- No [VARIABLES] unfilled

### STEP 10: REPORT
- Gerar report (MD + JSON)
- Listar changes
- Recommendations

---

## TEMPLATES

### 00_MANIFEST_TEMPLATE.md
```markdown
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
[ ] Aplicar config preset ({PRESET_NAME})
[ ] Testar com input de exemplo
[ ] Verificar output format
```

---

## FILE INVENTORY

### Core (00-05) ~{CORE_TOKENS} tokens
{CORE_FILES_TABLE}

### Config (06-10) ~{CONFIG_TOKENS} tokens
{CONFIG_FILES_TABLE}

### Execution (11-12) ~{EXEC_TOKENS} tokens
{EXEC_FILES_TABLE}

### HOPs (13-{LAST_HOP}) ~{HOP_TOKENS} tokens
{HOP_FILES_TABLE}

### Reference ({REF_START}-{REF_END}) ~{REF_TOKENS} tokens
{REF_FILES_TABLE}

---

## TOKEN OPTIMIZATION

| Componente | Antes | Depois | Reducao |
|------------|-------|--------|---------|
{OPTIMIZATION_TABLE}

---

**Package**: {AGENT_NAME} iso_vectorstore v{VERSION}
**Status**: DEPLOY READY
**Tokens**: ~{TOKEN_ESTIMATE} (otimizado {REDUCTION_PERCENT})
**Date**: {DATE}
```

### SYSTEM_INSTRUCTIONS_TEMPLATE.md
```markdown
# {AGENT_NAME} | System Instructions v{VERSION}

**Purpose**: Cole nas System Instructions do Agent Builder
**Scope**: {SCOPE}
**Mode**: {MODE}
**Output**: {OUTPUT_FORMAT}
**Updated**: {DATE}

---

## COPIE DAQUI PARA BAIXO

---

# IDENTITY

You are **{AGENT_NAME}** v{VERSION}, {AGENT_DESCRIPTION}.

**Function**: {FUNCTION}
**Markets**: {MARKETS}
**Compliance**: {COMPLIANCE}
**Mode**: {MODE}

## AUTONOMY

You operate AUTONOMOUSLY from input to final output:
- **Input Source**: `{$INPUT}` - accepts any of:
  {INPUT_SOURCES}
- **Decision Authority**: You decide fallback strategies and fixes
- **No Human Intervention**: Complete workflow without stopping

### Variable Resolution
1. Explicit `{$variable}` in prompt
2. Previous assistant output
3. Attached files/URLs
4. Direct user text

---

# SCOPE - CRITICAL

**YOU GENERATE:**
{GENERATES_LIST}

**YOU DO NOT GENERATE (delegated):**
{DELEGATES_LIST}

---

# WORKFLOW ({STEP_COUNT} Steps)

```
{WORKFLOW_DIAGRAM}
```

{WORKFLOW_STEPS}

---

# FILE SEARCH

Load from vector store:
{FILE_SEARCH_LIST}

---

# OUTPUT FORMAT

{OUTPUT_FORMAT_SPEC}

---

# QA CRITERIA

{QA_CRITERIA_LIST}

---

# CONSTRAINTS

{CONSTRAINTS_LIST}

---

**Agent**: {AGENT_NAME} | **Version**: {VERSION} | **Scope**: {SCOPE}
**Mode**: {MODE} | **Output**: {OUTPUT_FORMAT}
**Input**: {INPUT_SPEC}
```

---

## EXECUTION

### Para Executar em Outro Terminal

1. **Abrir novo terminal Claude Code**
2. **Carregar contexto**:
   ```
   /prime-codexa
   ```
3. **Executar ADW**:
   ```
   Execute ADW-104 (ISO_VECTORSTORE_OPTIMIZATION) para {agent_name}

   Reference: specs/ADW_ISO_VECTORSTORE_OPTIMIZATION_PLAN.md
   Templates: codexa_agent/templates/iso_vectorstore/
   ```

### Ordem de Prioridade
1. pesquisa_agent (30 files) - upstream do anuncio
2. photo_agent (27 files) - visual generation
3. mentor_agent (31 files) - pre-enrichment
4. video_agent (25 files) - video scripts
5. marca_agent (32 files) - brand strategy
6. codexa_agent (29 files) - meta-agent
7. curso_agent (27 files) - course creation

---

## METRICAS DE SUCESSO

| Metrica | Target |
|---------|--------|
| File count | <= 21 |
| Token estimate | < 15,000 |
| Version consistency | 100% |
| MANIFEST presente | Yes |
| SYSTEM_INSTRUCTIONS presente | Yes |
| HOPs otimizados | < 1500 tokens cada |

---

## RISCOS E MITIGACAO

| Risco | Mitigacao |
|-------|-----------|
| Perda de instrucoes essenciais | Review manual antes de commit |
| Garbage injection nao detectada | Regex patterns para YAML, metadata |
| Scope ambiguo | Ler PRIME.md para clarificar |
| Dependencias quebradas | Verificar referencias entre arquivos |

---

**Status**: READY FOR APPROVAL
**Estimated Effort**: 2-3h por agent (primeira vez), 30min (subsequentes com templates)
**Total para 7 agents**: ~15-20h (com templates reusaveis)

---

## APROVACAO

- [ ] User aprova plano
- [ ] Criar ADW-104 workflow
- [ ] Criar templates
- [ ] Criar spec de referencia
- [ ] Testar em 1 agent (pesquisa_agent)
- [ ] Aplicar aos demais
