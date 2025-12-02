# HOP: Video Script Generator | TAC-7 v2.5.0

## MODULE_METADATA
```yaml
id: HOP_VIDEO_SCRIPT
version: 2.5.0
purpose: Generate 15-30 minute video scripts for CODEXA courses
category: content_generation
dependencies: [curso_rules.json, hotmart_specs.json, pedagogy_patterns.json]
```

## INPUT_CONTRACT
```yaml
required:
  - module_id: string (01-06 or M0-M6)
  - module_name: string
  - layer_level: enum [layer_1, layer_2, layer_3]
  - duration_minutes: number (15-30)
optional:
  - prerequisites: string[]
  - learning_objectives: string[]
  - open_variables: object
validation:
  - duration_minutes >= 15 AND <= 30
  - layer_level in [layer_1, layer_2, layer_3]
```

## OUTPUT_CONTRACT
```yaml
primary:
  - video_script.md: Complete script with timing marks
secondary:
  - video_script.llm.json: Structured data for LLM processing
  - video_script.meta.json: Metadata and statistics
format: Trinity Output (.md + .llm.json + .meta.json)
structure:
  - HOOK (0:00-1:30)
  - OBJECTIVES (1:30-2:00)
  - CORE_CONTENT (2:00-25:00)
  - DEMO (varies)
  - RECAP (25:00-28:00)
  - CTA (28:00-30:00)
```

## TASK
**Role**: Educational content architect for CODEXA courses
**Objective**: Create a production-ready video script that teaches CODEXA concepts with clear timing, engaging hooks, and actionable demonstrations

**Standards**:
- Hook captures attention in <=90 seconds
- Learning objectives are measurable (Bloom's Taxonomy verbs)
- Demonstrations show REAL CODEXA system (not generic AI)
- [OPEN_VARIABLES] >= 2 per module for customization
- Brazilian e-commerce examples only
- Brand voice: disruptivo-sofisticado

**Constraints**:
- Duration: 15-30 minutes total
- Timing marks every 2-3 minutes
- No hype words: "revolucionario", "magico", "unico no mercado"
- Must include seed words: Meta-Construcao, Destilacao de Conhecimento

## STEPS

### Step 1: Context Loading
Load and analyze:
1. Module context from `context/0X_MODULO_*.md`
2. Brand voice rules from `08_curso_rules.json`
3. Hotmart video specs from `09_hotmart_specs.json`
4. Pedagogy patterns from `10_pedagogy_patterns.json`

### Step 2: Hook Construction (0:00-1:30)
Structure:
- **0:00-0:15**: Problem statement or provocative question
- **0:15-0:45**: Transformation promise (what they'll learn)
- **0:45-1:30**: Quick demo teaser or case study snapshot

Validation: Must retain 80%+ viewers (engaging, not promotional)

### Step 3: Objectives Definition (1:30-2:00)
Write 2-3 measurable objectives using Bloom's Taxonomy:
- Layer 1: listar, definir, identificar
- Layer 2: aplicar, demonstrar, executar
- Layer 3: criar, projetar, avaliar

Format: "Ao final deste modulo, voce sera capaz de [VERBO] [OBJETO]"

### Step 4: Core Content Creation (2:00-25:00)
Structure in 3-5 minute chunks:
1. **Concept introduction** (explain the what)
2. **Example demonstration** (show the how)
3. **Application exercise** (let them try)
4. **Recap checkpoint** (reinforce the why)

Include [OPEN_VARIABLES] for customization:
- `[SEU_PRODUTO]` - Student's product category
- `[PLATAFORMA_ECOMMERCE]` - Student's e-commerce platform
- `[SEU_NICHO]` - Student's market niche

### Step 5: Demonstration Sequence
Real CODEXA demonstrations:
- Show actual agent interface
- Use Brazilian e-commerce examples
- Include before/after results
- Timing: 4-6 minutes total

### Step 6: Recap and CTA (25:00-30:00)
- **Recap (25:00-28:00)**: Summarize 3 key points
- **CTA (28:00-30:00)**: Clear next action

CTA options:
- Complete workbook exercise
- Try hands-on practice
- Watch next module

## VALIDATION
```yaml
checklist:
  - hook_timing <= 90 seconds
  - objectives_measurable: true (Bloom's verbs)
  - open_variables >= 2
  - timing_marks_present: every 2-3 minutes
  - demo_shows_real_codexa: true
  - examples_brazilian_market: true
  - seed_words_present: [Meta-Construcao, Destilacao]
  - no_hype_words: true
  - total_duration: 15-30 minutes
threshold: >= 7.0/10.0
validators:
  - 01_content_quality_validator.py
  - 02_brand_voice_validator.py
```

## CONTEXT
**Usage**: Execute after course outline is approved, for each module
**Upstream**: Course outline (01_course_outline_builder.py)
**Downstream**: Workbook generation (03_workbook_builder.py)
**$arguments chaining**: $module_id -> $script_path -> $workbook_path

**Assumptions**:
- User has approved module outline
- Context files are loaded
- Brand voice guidelines understood

## EXAMPLE

```markdown
# Modulo 01: Introducao ao CODEXA
## Duracao: 25 minutos | Layer 1

---

### HOOK [00:00 - 01:30]

[00:00 - 00:15]
"Voce ja gastou horas escrevendo anuncios que ninguem clicou?"

[00:15 - 00:45]
Neste modulo, voce vai entender como o CODEXA transforma sua forma de criar conteudo para e-commerce. Nao e sobre IA generica - e sobre um sistema que aprende SEU negocio.

[00:45 - 01:30]
Veja rapidamente o que vamos construir juntos: [DEMO TEASER - mostra resultado final do modulo]

---

### OBJETIVOS [01:30 - 02:00]

Ao final deste modulo, voce sera capaz de:
1. IDENTIFICAR os 3 pilares do sistema CODEXA
2. EXPLICAR a diferenca entre Layer 1, 2 e 3
3. NAVEGAR pela interface do primeiro agente

---

### CONTEUDO PRINCIPAL [02:00 - 22:00]

#### Secao 1: O que e CODEXA [02:00 - 07:00]

[02:00 - 03:00]
CODEXA nao e "mais uma ferramenta de IA". E um sistema de Meta-Construcao...

[OPEN_VARIABLE: SEU_CONTEXTO]
> Pense no seu [SEU_PRODUTO]. Como voce cria conteudo para ele hoje?

[05:00 - 07:00]
[CHECKPOINT] Vamos pausar aqui. Voce ja entendeu a diferenca entre usar IA e construir com IA?

#### Secao 2: Os 3 Layers [07:00 - 14:00]
...

#### Secao 3: Primeiro Contato [14:00 - 22:00]
...

---

### DEMONSTRACAO [22:00 - 25:00]

[Mostrar tela do CODEXA]
Vou criar um anuncio para [CATEGORIA_EXEMPLO: moda feminina] usando o Anuncio Agent...

---

### RECAP [25:00 - 27:00]

Resumo dos 3 pontos principais:
1. CODEXA = Sistema de Meta-Construcao (nao ferramenta)
2. 3 Layers = Jornada de aprendizado progressiva
3. Comece pelo Layer 1, avance conforme domina

---

### CTA [27:00 - 28:00]

Proximo passo: Abra a apostila do Modulo 01 e complete o exercicio "Mapeando seu contexto".

No proximo modulo, vamos mergulhar no Anuncio Agent.
```

---
**Version**: 2.5.0 | **Type**: HOP (TAC-7 Enriched) | **Output**: Video Script
**Last Updated**: 2025-11-25
