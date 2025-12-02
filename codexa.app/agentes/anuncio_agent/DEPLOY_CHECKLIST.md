# DEPLOY CHECKLIST | anuncio_agent iso_vectorstore v3.2.0

**Data**: 2025-11-30 | **Status**: PRECISA ACAO MANUAL

---

## PROBLEMAS ENCONTRADOS

### 1. CRITICO: Arquivos Fora do Scope (TEXT-ONLY)

```
REMOVER (nao pertencem ao scope TEXT-ONLY):
- 18_HOP_image_prompts.md  ← Delegado para photo_agent
- 19_HOP_video_script.md   ← Delegado para video_agent
```

**Acao**: Deletar esses 2 arquivos do iso_vectorstore

---

### 2. CRITICO: Numeracao Inconsistente

**Estado Atual** (24 arquivos - ACIMA DO LIMITE DE 20):
```
00_MANIFEST.md           ✓ (recém criado)
01_QUICK_START.md        ✓
02_PRIME.md              ✓
03_INSTRUCTIONS.md       ✓
04_README.md             ✓
05_ARCHITECTURE.md       ✓
06_input_schema.json     ✓
07_output_template.md    ✓
08_copy_rules.json       ✓
09_marketplace_specs.json ✓
10_persuasion_patterns.json ✓
11_ADW_orchestrator.md   ✓
12_execution_plans.json  ✓
13_HOP_main_agent.md     ✓
14_HOP_titulo_generator.md ✓
15_HOP_keywords_expander.md ✓
16_HOP_bullet_points.md  ✓
17_HOP_descricao_builder.md ✓
18_HOP_image_prompts.md  ✗ REMOVER (fora do scope)
19_HOP_video_script.md   ✗ REMOVER (fora do scope)
20_CHANGELOG.md          ✓
21_HOP_qa_validation.md  ✗ RENUMERAR para 18
22_frameworks.md         ✗ RENUMERAR para 19
23_quality_dimensions.json ✗ RENUMERAR para 20
```

**Acao**: Renumerar apos remocao

---

### 3. IMPORTANTE: validator.py Fora do Pacote

```
Localizacao atual: code_interpreter/validator.py
Problema: Nao esta no iso_vectorstore para upload
```

**Opcoes**:
A. Copiar para iso_vectorstore (inclui no upload)
B. Manter separado (upload manual ao Code Interpreter)

**Recomendacao**: Opcao B - mais limpo, validator.py e para Code Interpreter

---

### 4. MEDIO: HOPs Muito Grandes

```
14_HOP_titulo_generator.md    ~26,000 tokens
17_HOP_descricao_builder.md   ~34,000 tokens
```

**Risco**: Alguns LLMs podem ter limite de arquivo
**Mitigacao**: Testar upload, compactar se necessario

---

## ACOES MANUAIS NECESSARIAS

### Fase 1: Limpeza (5 min)

```bash
# Remover arquivos fora do scope
rm iso_vectorstore/18_HOP_image_prompts.md
rm iso_vectorstore/19_HOP_video_script.md
```

### Fase 2: Renumeracao (10 min)

```bash
# Renumerar arquivos
mv iso_vectorstore/21_HOP_qa_validation.md iso_vectorstore/18_HOP_qa_validation.md
mv iso_vectorstore/22_frameworks.md iso_vectorstore/19_frameworks.md
mv iso_vectorstore/23_quality_dimensions.json iso_vectorstore/20_quality_dimensions.json

# Resultado: 21 arquivos (00-20)
```

### Fase 3: Atualizar Referencias (5 min)

Arquivos que referenciam numeracao errada:
- 00_MANIFEST.md (atualizar lista)
- 01_QUICK_START.md (verificar referencias)
- 12_execution_plans.json (verificar prompt_module paths)

### Fase 4: Upload Code Interpreter (2 min)

```bash
# Upload separado do validator.py
# Destino: Code Interpreter no Agent Builder
code_interpreter/validator.py
```

---

## ESTRUTURA FINAL ESPERADA (21 arquivos)

```
iso_vectorstore/
├── 00_MANIFEST.md              Entry/inventory
├── 01_QUICK_START.md           LLM entry point
├── 02_PRIME.md                 Agent identity
├── 03_INSTRUCTIONS.md          Workflow rules
├── 04_README.md                Documentation
├── 05_ARCHITECTURE.md          Tech architecture
├── 06_input_schema.json        Input validation
├── 07_output_template.md       3-PART output format
├── 08_copy_rules.json          ANVISA/INMETRO compliance
├── 09_marketplace_specs.json   Platform limits
├── 10_persuasion_patterns.json PNL triggers
├── 11_ADW_orchestrator.md      Workflow manager
├── 12_execution_plans.json     Full/Quick plans
├── 13_HOP_main_agent.md        Parse + confidence
├── 14_HOP_titulo_generator.md  Title generation
├── 15_HOP_keywords_expander.md Keyword expansion
├── 16_HOP_bullet_points.md     Bullet generation
├── 17_HOP_descricao_builder.md Description building
├── 18_HOP_qa_validation.md     5D validation [RENUMERADO]
├── 19_frameworks.md            CODEXA/HOP reference [RENUMERADO]
└── 20_quality_dimensions.json  5D scoring schema [RENUMERADO]

SEPARADO (Code Interpreter):
└── validator.py                Python validation
```

---

## OPORTUNIDADES CODE INTERPRETER

### Atual: validator.py (EXCELENTE)
- 5D scoring completo
- Intelligent fallback
- Source attribution
- Legacy compatibility
- ~742 linhas, bem estruturado

### Melhorias Sugeridas (Opcional)

| Funcao | Beneficio | Esforco |
|--------|-----------|---------|
| `batch_validate()` | Validar multiplos outputs | Baixo |
| `auto_fix_titulo()` | Ajustar chars automaticamente | Medio |
| `generate_copyable_block()` | Formatar PART 2 automaticamente | Medio |
| `count_tokens()` | Estimar custo antes de gerar | Baixo |
| `compress_hop()` | Compactar HOP para limites | Alto |

### Recomendacao

**NAO adicionar agora** - o validator.py atual e suficiente para deploy.
Melhorias podem vir em v3.3.0 apos testes em producao.

---

## CHECKLIST FINAL DE DEPLOY

### Pre-Deploy
- [ ] Remover 18_HOP_image_prompts.md
- [ ] Remover 19_HOP_video_script.md
- [ ] Renumerar 21 → 18, 22 → 19, 23 → 20
- [ ] Atualizar 00_MANIFEST.md com lista correta
- [ ] Verificar referencias em 01_QUICK_START.md
- [ ] Verificar prompt_module paths em 12_execution_plans.json

### Deploy
- [ ] Upload 21 arquivos do iso_vectorstore ao vector store
- [ ] Upload validator.py ao Code Interpreter separadamente
- [ ] Aplicar config preset (EFICIENTE ou PERFORMANCE)

### Pos-Deploy
- [ ] Testar com URL de produto real
- [ ] Verificar 3-PART output renderiza corretamente
- [ ] Verificar PART 2 e copiavel (code fence funciona)
- [ ] Medir tokens consumidos vs target

---

## CONFIGS PARA DEPLOY

### ChatGPT Responses API

```yaml
# EFICIENTE (batch, custo baixo)
reasoning_effort: medium
response: text
tools:
  - code_interpreter: ON (upload validator.py)
  - file_search: ON (upload iso_vectorstore)
  - web_search: OFF

# PERFORMANCE (producao final)
reasoning_effort: high
response: text
tools:
  - code_interpreter: ON
  - file_search: ON
  - web_search: ON
```

### System Instructions (adicionar)

```
OUTPUT_MODE: [efficient|performance]
SCOPE: TEXT-ONLY
VERSION: 3.2.0
```

---

## METRICAS DE SUCESSO

| Metrica | Target | Como Medir |
|---------|--------|------------|
| Tokens por run | <25,000 | Usage stats no dashboard |
| Code Interpreter calls | <10 | Contar no log |
| Output copyability | 95% | PART 2 funciona? |
| 5D Score | >= 0.85 | QA report |
| Tempo de execucao | <10 min | Timestamp |

---

**Proxima Acao**: Executar Fase 1-4 acima, depois deploy

**Autor**: codexa_agent | **Data**: 2025-11-30
