# HOP: Workbook Generator | TAC-7 v2.5.0

## MODULE_METADATA
```yaml
id: HOP_WORKBOOK
version: 2.5.0
purpose: Generate 8-15 page student workbooks for CODEXA courses
category: content_generation
dependencies: [curso_rules.json, pedagogy_patterns.json, 13_HOP_video_script.md]
```

## INPUT_CONTRACT
```yaml
required:
  - module_id: string (01-06 or M0-M6)
  - module_name: string
  - video_script_path: string (path to corresponding video script)
optional:
  - complexity_level: enum [basico, intermediario, avancado]
  - completion_time_hours: number (1-4)
  - exercise_count: number (3-5)
validation:
  - video_script exists
  - complexity_level in [basico, intermediario, avancado]
```

## OUTPUT_CONTRACT
```yaml
primary:
  - workbook.md: Complete workbook in PDF-ready markdown
secondary:
  - workbook.llm.json: Structured data for LLM processing
  - workbook.meta.json: Metadata and statistics
format: Trinity Output (.md + .llm.json + .meta.json)
structure:
  - COVER_PAGE (objectives, time estimate)
  - THEORY_SECTION (2-3 pages)
  - GUIDED_EXERCISES (3-4 pages)
  - HANDS_ON_PRACTICE (2-3 pages)
  - REFLECTION (1 page)
  - RESOURCES (1 page)
pages: 8-15
```

## TASK
**Role**: Educational content architect creating student workbooks
**Objective**: Create a comprehensive workbook that reinforces video content through theory, exercises, and reflection

**Standards**:
- Aligns 100% with video script content
- Progressive difficulty (easy -> medium -> hard)
- Includes checkboxes for completion tracking
- [OPEN_VARIABLES] >= 2 for personalization
- Print-friendly layout for PDF export
- Brazilian Portuguese natural tone

**Constraints**:
- Pages: 8-15
- Exercises: 3-5 per workbook
- Must reference video timestamps
- Confluence with video content (not standalone)

## STEPS

### Step 1: Video Script Analysis
1. Read corresponding video script
2. Extract learning objectives
3. Identify key concepts for reinforcement
4. Map timing to workbook sections

### Step 2: Cover Page Creation
Include:
- Module title and number
- Learning objectives (from video)
- Estimated completion time
- Prerequisites (if any)
- Checkbox progress tracker

### Step 3: Theory Section (2-3 pages)
Structure:
- **Key Concepts**: Clear definitions with examples
- **Visual Aids**: Diagrams, flowcharts where helpful
- **Important Notes**: Callout boxes for critical points
- **Video Reference**: "[Ver video 05:00-08:00]"

### Step 4: Guided Exercises (3-4 pages)
Progressive difficulty:
1. **Exercise 1 (Easy)**: Direct application of concept
2. **Exercise 2 (Medium)**: Combination of concepts
3. **Exercise 3 (Hard)**: Real-world scenario

Format per exercise:
- Objective statement
- Step-by-step instructions
- [OPEN_VARIABLE] for personalization
- Space for student response
- Solution guide (optional)

### Step 5: Hands-On Practice (2-3 pages)
Real CODEXA interaction:
- Clear task description
- Expected outcome
- Time estimate (15-45 min)
- Troubleshooting tips
- Screenshot placeholders

### Step 6: Reflection Section (1 page)
Questions:
1. "O que voce aprendeu de mais importante?"
2. "Como vai aplicar isso no seu negocio?"
3. "Quais duvidas ainda restam?"
4. "Qual seu proximo passo?"

### Step 7: Resources Section (1 page)
Include:
- Links to related content
- External resources
- Next module preview
- Support channels

## VALIDATION
```yaml
checklist:
  - pages_count: 8-15
  - exercises_count: 3-5
  - objectives_aligned_with_video: true
  - open_variables >= 2
  - difficulty_progression: [easy, medium, hard]
  - video_references_present: true
  - print_friendly_layout: true
  - reflection_questions >= 3
threshold: >= 7.0/10.0
validators:
  - 03_pedagogical_validator.py
  - 04_technical_validator.py
```

## CONTEXT
**Usage**: Execute after video script is completed for each module
**Upstream**: Video script (13_HOP_video_script.md)
**Downstream**: Sales package, Hotmart package
**$arguments chaining**: $module_id -> $script_path -> $workbook_path

**Assumptions**:
- Video script is completed and validated
- Module outline approved
- Student has access to CODEXA system

## EXAMPLE

```markdown
# Workbook: Introducao ao CODEXA
## Modulo 01 | 2 horas | Layer 1

---

## Objetivos de Aprendizagem

Ao completar este workbook, voce tera:
- [ ] IDENTIFICADO os 3 pilares do sistema CODEXA
- [ ] EXPLICADO a diferenca entre Layer 1, 2 e 3
- [ ] NAVEGADO pela interface do primeiro agente

**Tempo estimado**: 2 horas
**Pre-requisitos**: Nenhum
**Video correspondente**: Modulo 01 (25 min)

---

## Secao 1: Teoria

### Conceito Principal: Meta-Construcao

O CODEXA nao e "mais uma ferramenta de IA". E um **sistema de Meta-Construcao** - um sistema que constroi sistemas.

> **Destilacao de Conhecimento**: O processo de transformar conhecimento tacito (experiencia) em conhecimento explicito (prompts, workflows, agentes).

### Os 3 Layers do CODEXA

| Layer | Foco | Perfil |
|-------|------|--------|
| Layer 1 | Conceitos e analogias | Iniciantes |
| Layer 2 | Pratica e integracao | Intermediarios |
| Layer 3 | Meta-construcao e codigo | Avancados |

[Ver video 02:00-07:00]

---

## Secao 2: Exercicios Guiados

### Exercicio 1: Mapeando seu Contexto (Facil)
**Objetivo**: Identificar seu ponto de partida no CODEXA

**Instrucoes**:
1. Liste 3 tipos de conteudo que voce cria para seu e-commerce
2. Classifique cada um por frequencia (diario/semanal/mensal)
3. Identifique o mais trabalhoso

[OPEN_VARIABLE: SEU_ECOMMERCE]
**Meu e-commerce**: _______________________
**Produtos principais**: _______________________

**Seus 3 tipos de conteudo**:
1. _________________ | Frequencia: _______
2. _________________ | Frequencia: _______
3. _________________ | Frequencia: _______

**O mais trabalhoso**: _______________________

---

### Exercicio 2: Identificando Oportunidades (Medio)
**Objetivo**: Mapear onde o CODEXA pode ajudar

**Instrucoes**:
1. Para cada tipo de conteudo do Exercicio 1
2. Identifique: Quanto tempo gasta? Qual a qualidade?
3. Marque onde o CODEXA pode automatizar

[Ver video 14:00-18:00]

| Conteudo | Tempo Atual | Qualidade | CODEXA Pode? |
|----------|-------------|-----------|--------------|
| ________ | ___ horas | ___/10 | [ ] Sim [ ] Nao |
| ________ | ___ horas | ___/10 | [ ] Sim [ ] Nao |
| ________ | ___ horas | ___/10 | [ ] Sim [ ] Nao |

---

### Exercicio 3: Planejando sua Jornada (Dificil)
**Objetivo**: Criar seu roadmap personalizado no CODEXA

[OPEN_VARIABLE: SUA_META]
**Sua meta em 30 dias**: _______________________

**Sequencia de modulos recomendada**:
1. [ ] Modulo ___: _______________________
2. [ ] Modulo ___: _______________________
3. [ ] Modulo ___: _______________________

**Justificativa**: _______________________

---

## Secao 3: Pratica Hands-On

### Desafio: Primeiro Acesso ao CODEXA
**Tempo estimado**: 30 minutos

**Tarefa**:
1. Acesse a interface do CODEXA
2. Navegue ate o Anuncio Agent
3. Leia a descricao do agente
4. Tire uma screenshot da tela inicial

**Resultado esperado**: Screenshot salva em sua pasta de estudos

**Troubleshooting**:
- Se nao encontrar o menu: [Ver video 20:00-22:00]
- Se der erro de acesso: Verifique suas credenciais

---

## Secao 4: Reflexao

1. **O que voce aprendeu de mais importante neste modulo?**
   _________________________________________________________________

2. **Como voce vai aplicar o conceito de Meta-Construcao no seu negocio?**
   _________________________________________________________________

3. **Quais duvidas ainda restam?**
   _________________________________________________________________

4. **Qual seu proximo passo imediato?**
   _________________________________________________________________

---

## Recursos Adicionais

- **Proximo modulo**: Modulo 02 - Anuncio Agent
- **Suporte**: [Canal de suporte]
- **Comunidade**: [Link da comunidade]

---

**Parabens por completar o Modulo 01!**
Proximo passo: Assista o video do Modulo 02 antes de comecar o proximo workbook.
```

---
**Version**: 2.5.0 | **Type**: HOP (TAC-7 Enriched) | **Output**: Workbook
**Last Updated**: 2025-11-25
