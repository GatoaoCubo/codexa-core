# ARCHITECTURE - CodeXAnuncio

Documentação técnica da arquitetura do sistema de geração de anúncios.

## Visão Geral

```
┌─────────────────────────────────────────────────────────────┐
│                SELLER / RESEARCH_NOTES INPUT                 │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│           MAIN AGENT (10_main_agent_hop.md)                  │
│  Orquestra execução de 11 steps (7 fases conceituais)       │
└─────┬───────────────────────────────────────────────────────┘
      │
      ├──► [STEP 1] PARSE INPUT RESEARCH
      │        ├─ Parse research_notes.md (22 blocos)
      │        ├─ Valida contra schema JSON
      │        ├─ Verifica confidence score ≥0.75
      │        └─ Extrai Strategic Brief
      │
      ├──► [STEP 2] TITULO GENERATION (20_titulo_generator.md)
      │        ├─ Input: [HEAD TERMS], [DIFERENCIAIS]
      │        ├─ Gera 3 títulos (58-60 chars, ZERO conectores)
      │        ├─ Densidade: 8-10 keywords por título
      │        └─ Output: [BLOCOS_DE_TITULOS]
      │
      ├──► [STEP 3] KEYWORDS EXPANSION (30_keywords_expander.md)
      │        ├─ Input: [HEAD TERMS], [TITULOS]
      │        ├─ Gera BLOCO_PALAVRAS_1 (115-120 termos)
      │        ├─ Gera BLOCO_PALAVRAS_2 (115-120 termos, deduplica)
      │        └─ Output: [BLOCO_PALAVRAS_1], [BLOCO_PALAVRAS_2]
      │
      ├──► [STEP 4] BULLET POINTS (40_bullet_points.md)
      │        ├─ Input: [DIFERENCIAIS], [DORES], [GANHOS]
      │        ├─ Gera 10 bullet points (250-299 chars cada)
      │        ├─ Aplica gatilhos mentais
      │        └─ Output: [BULLET_POINTS_ESTRATEGICOS]
      │
      ├──► [STEP 5] DESCRIPTION BUILDER (50_descricao_builder.md)
      │        ├─ Input: [BULLETS], [KEYWORDS], [DORES], [GANHOS]
      │        ├─ Framework StoryBrand (7 elementos)
      │        ├─ Mínimo 3,300 caracteres
      │        └─ Output: [DESCRICAO_LONGA]
      │
      ├──► [STEP 6] IMAGE PROMPTS (60_image_prompts.md) [PARALLEL]
      │        ├─ Grid 3x3: 9 prompts de imagem
      │        └─ Output: [PROMPTS_IMAGENS]
      │
      ├──► [STEP 7] VIDEO SCRIPT (70_video_script.md) [PARALLEL]
      │        ├─ Roteiro VEO3 (6-9 cenas, 30-60s, 9:16)
      │        └─ Output: [PROMPT_VEO3]
      │
      ├──► [STEP 8] SEO METADATA (80_seo_metadata.md) [PARALLEL]
      │        ├─ Keywords primary/secondary/tertiary
      │        └─ Output: [METADADOS_SEO]
      │
      ├──► [STEP 9] VARIATIONS S5 (85_variacoes_s5.md)
      │        ├─ Variação A: Equilibrada
      │        ├─ Variação B: Emocional
      │        └─ Variação C: Técnica
      │
      ├──► [STEP 10] QA VALIDATION (90_qa_validation.md)
      │        ├─ Executa AUDITORIA_QA (11 critérios)
      │        ├─ Valida compliance (zero proibições)
      │        ├─ Calcula persuasion_score
      │        └─ Output: [AUDITORIA_QA]
      │
      └──► [STEP 11] OUTPUT ASSEMBLY
               ├─ Consolida todos os outputs
               ├─ Renderiza usando templates/output_template.md
               ├─ Gera Trinity (.md + .llm.json + .meta.json)
               └─ Salva em user_anuncios/
```

## Componentes

### 1. Prompts (Módulos Especializados)

| Arquivo | Função | Input | Output | Duração |
|---------|--------|-------|--------|---------|
| **10_main_agent_hop.md** | Orquestração HOP | research_notes | anuncio_output | 10-15min |
| 20_titulo_generator.md | Gera títulos SEO | HEAD TERMS, DIFERENCIAIS | 3 títulos 58-60 chars | 10-15s |
| 30_keywords_expander.md | Expande keywords | HEAD TERMS, TITULOS | 2 blocos 115-120 termos | 15-20s |
| 40_bullet_points.md | Bullet points estratégicos | DIFERENCIAIS, DORES, GANHOS | 10 bullets 250-299 chars | 10-15s |
| 50_descricao_builder.md | Constrói descrição | BULLETS, KEYWORDS, DORES | Descrição ≥3.300 chars | 30-40s |
| 60_image_prompts.md | Gera prompts imagem | DIFERENCIAIS | 9 prompts (grid 3x3) | 20-30s |
| 70_video_script.md | Roteiro de vídeo | BULLETS | Roteiro 6-9 cenas | 20-30s |
| 80_seo_metadata.md | Metadados SEO | KEYWORDS, TITULOS | JSON metadata | 10-15s |
| 85_variacoes_s5.md | 3 variações | TITULOS, BULLETS, DESCRICAO | 3 abordagens StoryBrand | 15-20s |
| 90_qa_validation.md | Validação QA | Output completo | Checklist + score | 10-15s |

### 2. Templates

| Arquivo | Propósito | Formato |
|---------|-----------|---------|
| **templates/output_template.md** | Template do anúncio final | Markdown estruturado, 15 blocos |
| **research_notes_schema.json** | Validação de input | JSON Schema draft-07, 22 blocos (implementado em models.py) |

### 3. Configurações

| Arquivo | Conteúdo | Uso |
|---------|----------|-----|
| **copy_rules.json** | Regras de compliance por marketplace | Proibições, thresholds, validação |
| **persuasion_patterns.json** | Gatilhos mentais e frameworks | StoryBrand, PNL, AIDA, gatilhos |
| **marketplace_specs.json** | Specs técnicas dos marketplaces | Limites de chars, políticas, features |

## Fluxo de Dados

```
research_notes.md (22 blocos)
    │
    ├─► Parsing & Validation ──► Lacunas identificadas
    │
    ├─► Context Loading ──► Compliance rules + Persuasion patterns
    │
    ├─► Titulo Generation ──┐
    │                        │
    ├─► Keywords Expansion ──┤
    │                        ├──► Output consolidado
    ├─► Content Building ────┤
    │                        │
    ├─► Variations S5 ───────┘
    │
    ├─► QA Validation ──► Compliance check + Persuasion score
    │
    └─► Template Rendering ──► anuncio_output.md
```

## Estrutura de Dados

### Research Notes Schema (Input)

```json
{
  "required_blocks": [
    "LACUNAS_DO_BRIEF",
    "HEAD_TERMS",
    "LONGTAILS",
    "DORES_DO_PUBLICO",
    "GANHOS_DESEJADOS",
    "OBJECOES_E_RESPOSTAS",
    "PROVAS_E_EVIDENCIAS",
    "DIFERENCIAIS_COMPETITIVOS",
    "RISCOS_OU_ALERTAS",
    "REGRAS_CRITICAS_MARKETPLACE",
    "ANALISE_DE_CONCORRENTES",
    "BENCHMARK_DE_CONCORRENTES",
    "ESTRATEGIAS_E_GAPS"
  ],
  "recommended_blocks": [
    "SINONIMOS_E_VARIACOES",
    "TERMO_CONTEXTUAL_E_OCASIAO",
    "PADROES_DE_LINGUAGEM_EFICAZ",
    "SEO_OUTBOUND",
    "SEO_INBOUND"
  ],
  "confidence_threshold": 0.75
}
```

### Anuncio Output (Output)

```markdown
15 blocos estruturados:
├─ Metadata
│  ├─ NOME_DO_ARQUIVO_SUGERIDO
│  ├─ VERSAO_SCHEMA
│  └─ PROIBICOES
├─ Identidade
│  ├─ IDENTIDADE_DO_PRODUTO
│  └─ PROPOSTA_DE_VALOR
├─ Copy Principal
│  ├─ BLOCOS_DE_TITULOS (3 × 58-60 chars)
│  ├─ BLOCO_PALAVRAS_1 (115-120 termos)
│  ├─ BLOCO_PALAVRAS_2 (115-120 termos)
│  └─ DESCRICAO_LONGA (≥3.300 chars)
├─ Mídia
│  ├─ PROMPTS_IMAGENS (9 prompts)
│  └─ PROMPT_VEO3 (roteiro vídeo)
├─ SEO & QA
│  ├─ METADADOS_SEO (JSON)
│  └─ AUDITORIA_QA (checklist + score)
├─ Variações
│  └─ VARIACOES_S5 (3 abordagens)
└─ Notas
   └─ NOTAS_DE_FALLBACK
```

## Políticas e Validações

### Compliance Validation

```python
def validate_compliance(output, marketplace):
    violations = []

    # Proibições gerais
    if "<" in output or ">" in output:
        violations.append("HTML tags detectados")
    if contains_emojis(output):
        violations.append("Emojis detectados")
    if "#1" in output or "melhor do mundo" in output:
        violations.append("Superlativos absolutos")
    if re.search(r"cur(a|ar)|terap[êe]utic", output, re.I):
        violations.append("Claims terapêuticas (ANVISA)")

    # Proibições por marketplace
    if marketplace == "mercadolivre":
        if "http://" in output or "www." in output:
            violations.append("Links externos (ML policy)")

    return len(violations) == 0, violations
```

### Quality Gates

```python
def validate_quality(output):
    checks = {
        "titulos_validos": len(titulos) == 3 and all(58 <= len(t) <= 60 for t in titulos),
        "keywords_validos": 115 <= len(bloco_palavras_1) <= 120 and 115 <= len(bloco_palavras_2) <= 120,
        "descricao_valida": len(descricao_longa) >= 3300,
        "prompts_imagens_completos": len(prompts_imagens) == 9,
        "prompt_video_completo": video_scenes >= 6 and video_duration >= 30,
        "compliance_pass": validate_compliance(output)
    }

    score = sum(checks.values()) / len(checks)
    return "PASS" if score == 1.0 else "PARTIAL" if score >= 0.9 else "FAIL"
```

## Extensibilidade

### Adicionar Novo Módulo

1. Criar `prompts/novo_modulo.md`:
```markdown
# MÓDULO: Nome do Módulo
## Objetivo
## Entradas
## Processo
## Output
```

2. Registrar em `main_agent.md`:
```markdown
**PHASE N: NOVO_MODULO (novo_modulo.md)**
- Input: [DADOS_NECESSARIOS]
- Output: [NOVO_BLOCO]
```

3. Adicionar bloco em `templates/output_template.md`:
```markdown
## [NOVO_BLOCO]
[Estrutura do output]
```

### Adicionar Novo Marketplace

Editar `config/marketplace_specs.json`:
```json
{
  "id": "novo_marketplace",
  "name": "Nome Oficial",
  "limits": {
    "titulo_max_chars": 120,
    "descricao_max_chars": 5000,
    "keywords_max": 200
  },
  "policies": {
    "allow_html": false,
    "allow_external_links": false,
    "allow_emojis": false
  }
}
```

## Dependências

### Ferramentas Necessárias

| Ferramenta | Obrigatório | Uso |
|------------|-------------|-----|
| **LLM (Claude/GPT-4)** | ✅ Sim | Geração de copy criativa |
| **JSON Parser** | ✅ Sim | Parsing de research_notes |
| **Regex Engine** | ✅ Sim | Detecção de proibições |

### Plataformas Suportadas

- ✅ **Claude Code** (comando nativo `/codex_anuncio`)
- ✅ **OpenAI Assistants** (via instructions + code_interpreter)
- ⚠️ **Standalone LLM** (com parsing manual)

## Performance

### Benchmarks Típicos

| Fase | Duração | % do Total |
|------|---------|------------|
| Input Validation | 10s | 6% |
| Context Loading | 5s | 3% |
| Titulo Generation | 20s | 11% |
| Keywords Expansion | 30s | 17% |
| Content Building | 60s | 33% |
| Variations | 30s | 17% |
| Validation & Output | 20s | 11% |
| **Total** | **180s (3min)** | **100%** |

### Otimizações

1. **Paralelize onde possível:** Títulos + Keywords + Imagens (não dependem um do outro)
2. **Cache compliance rules:** Carrega 1x por sessão, não por anúncio
3. **Deduplicate early:** Remove redundâncias em keywords logo após expansão

## Segurança e Compliance

### Dados Sensíveis
- ❌ **NÃO armazena:** Dados de clientes, estratégias confidenciais
- ✅ **OK armazenar:** Research públicos, benchmarks agregados

### Compliance
- ✅ Validação automática contra 4 marketplaces BR
- ✅ Zero ações (só leitura de research)
- ✅ Respeita políticas de ANVISA, INMETRO, CONAR

## Versioning

**Esquema:** MAJOR.MINOR.PATCH

- **MAJOR:** Mudanças incompatíveis no output schema
- **MINOR:** Novos módulos ou features compatíveis
- **PATCH:** Correções de bugs ou refinamentos

**Atual:** v1.0.0

---

**Documentação técnica completa**
**Última atualização:** 2025-11-03
**Mantenedor:** [nome]
