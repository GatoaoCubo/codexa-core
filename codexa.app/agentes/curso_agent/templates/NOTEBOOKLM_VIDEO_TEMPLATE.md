# NotebookLM: Video LP - {{PRODUCT_NAME}} Template

**Objetivo**: Material para NotebookLM gerar vídeo de {{VIDEO_DURATION}} minutos sobre {{PRODUCT_NAME}} para Landing Page.

---

## TRINITY STRUCTURE

This file is part of a 3-file production system:

```
{{SCRIPT_FILE}}.md                     → Script (what to say)
{{VISUAL_DIRECTION_FILE}}.md           → Visual Direction (how it looks)
{{NOTEBOOKLM_PROMPT_FILE}}.md          → NotebookLM Prompt (how to generate)
                                         ↑ YOU ARE HERE
```

**Separation of Concerns**:
- **Script**: Timecodes, narration, messaging, copy
- **Visual Direction**: Camera movements, lighting, mood, transitions
- **NotebookLM Prompt**: Instructions for AI to consume both files and generate production guidance

**Why separate?**
1. **Clarity**: Each file has one job
2. **Reusability**: Script can be read standalone, visuals can be referenced independently
3. **Iteration**: Update narration without touching camera specs, or vice versa

**Usage**: Upload script + visual direction + context files to NotebookLM. Use prompt below to iterate.

---

## PARTE 1: ARQUIVOS PARA UPLOAD NO NOTEBOOKLM

### Arquivos Core (Upload obrigatório)

```
1. {{SCRIPT_FILE}}.md
   → Script completo com timecodes, narração, gatilhos

2. {{VISUAL_DIRECTION_FILE}}.md
   → Direção visual: câmera, iluminação, movimento, mood

3. {{RESEARCH_FILE}}.md
   → Hooks, triggers, terminologia validada

4. {{GLOSSARY_FILE}}.md
   → Termos técnicos e definições
```

### Arquivos de Suporte (Enriquecem contexto)

```
5. {{CONTEXT_FILE_1}}.md
   → {{CONTEXT_DESCRIPTION_1}}

6. {{CONTEXT_FILE_2}}.md
   → {{CONTEXT_DESCRIPTION_2}}

7. {{CONTEXT_FILE_3}}.md
   → {{CONTEXT_DESCRIPTION_3}}
```

### Caminhos para Cópia

```
{{SCRIPT_PATH}}
{{VISUAL_DIRECTION_PATH}}
{{RESEARCH_PATH}}
{{GLOSSARY_PATH}}
{{CONTEXT_PATH_1}}
{{CONTEXT_PATH_2}}
{{CONTEXT_PATH_3}}
```

---

## PARTE 2: PROMPT PRINCIPAL NOTEBOOKLM

```
Você é um Video Production Specialist especializado em vídeos de conversão para {{BUSINESS_MODEL}}.

## TAREFA
Usando os documentos carregados (especialmente {{SCRIPT_FILE}}.md e {{VISUAL_DIRECTION_FILE}}.md), ajude-me a produzir um vídeo de {{VIDEO_DURATION}} minutos para a landing page do {{BRAND_URL}} sobre {{PRODUCT_NAME}}.

## CONTEXTO
- Duração: {{VIDEO_DURATION}} minutos
- Plataforma: {{PLATFORM_PRIMARY}} + {{PLATFORM_SECONDARY}}
- Público: {{TARGET_AUDIENCE}}
- Tom: {{TONE_DESCRIPTION}}
- Objetivo: {{CONVERSION_GOAL}}

## INPUTS PRIMÁRIOS
1. **{{SCRIPT_FILE}}.md**: Script completo com narração, timecodes, mensagens-chave
2. **{{VISUAL_DIRECTION_FILE}}.md**: Especificações de câmera, iluminação, movimento, mood

## ESTRUTURA DO VÍDEO

### Bloco 1: HOOK [{{BLOCK_1_TIME}}]
- {{BLOCK_1_STRATEGY}}
- {{BLOCK_1_EXAMPLE}}
- Contraste: {{BLOCK_1_CONTRAST}}

### Bloco 2: PROBLEMA [{{BLOCK_2_TIME}}]
- {{BLOCK_2_PAIN_POINT_1}}
- {{BLOCK_2_PAIN_POINT_2}}
- Dor: {{BLOCK_2_CORE_PAIN}}

### Bloco 3: SOLUÇÃO [{{BLOCK_3_TIME}}]
- {{SOLUTION_FEATURE_1}}
- {{SOLUTION_FEATURE_2}}
- {{SOLUTION_FEATURE_3}}
- {{SOLUTION_FEATURE_4}}

### Bloco 4: DEMO [{{BLOCK_4_TIME}}]
- {{DEMO_FLOW_DESCRIPTION}}
- Mostrar {{DEMO_PHASES}} fases executando
- {{DEMO_SUCCESS_METRIC}}

### Bloco 5: ESPECIALISTAS [{{BLOCK_5_TIME}}]
- {{EXPERTISE_SOURCE}}
- {{NUMBER_OF_COMPONENTS}} componentes
- {{INTEGRATION_DESCRIPTION}}

### Bloco 6: DIFERENCIAL [{{BLOCK_6_TIME}}]
- Dor de {{ALTERNATIVE_PAIN_CATEGORY}}: "{{ALTERNATIVE_PAIN_QUOTE}}"
- Solução: "{{UNIQUE_VALUE_PROP}}"
- Humor: {{HUMOR_ELEMENT}}
- {{POSITIONING_STATEMENT}}

### Bloco 7: CTA [{{BLOCK_7_TIME}}]
- {{CTA_RECAP_ELEMENTS}}
- {{BRAND_URL}}
- {{OFFER_STATEMENT}}
- Tagline: {{TAGLINE}}

## REGRAS

### SEMPRE
- Usar terminologia do {{GLOSSARY_FILE}}.md
- Manter timing marks
- Exemplos {{TARGET_MARKET}}
- Mencionar {{BRAND_ELEMENT_1}} + {{BRAND_ELEMENT_2}} no diferencial

### NUNCA
- Hype words: {{BANNED_WORD_1}}, {{BANNED_WORD_2}}
- Promessas garantidas
- Urgência fake

### GATILHOS PERMITIDOS
- Contraste ({{CONTRAST_EXAMPLE}})
- Prova real ({{PROOF_METRIC}})
- Humor ({{HUMOR_HOOK}})
- Escala sem risco ({{SCALE_BENEFIT}})

## OUTPUT ESPERADO
Para cada solicitação:
- Resposta prática
- Referência ao documento fonte
- Validação contra quality gates
```

---

## PARTE 3: DIREÇÃO VISUAL POR SEÇÃO

### [{{BLOCK_1_TIME}}] HOOK - {{BLOCK_1_TITLE}}

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| {{TIME_1}} | {{VISUAL_1}} | {{CAMERA_1}} | {{LIGHTING_1}} |
| {{TIME_2}} | {{VISUAL_2}} | {{CAMERA_2}} | {{LIGHTING_2}} |
| {{TIME_3}} | {{VISUAL_3}} | {{CAMERA_3}} | {{LIGHTING_3}} |
| {{TIME_4}} | {{VISUAL_4}} | {{CAMERA_4}} | {{LIGHTING_4}} |
| {{TIME_5}} | {{VISUAL_5}} | {{CAMERA_5}} | {{LIGHTING_5}} |

**Movimento Principal**: {{PRIMARY_MOVEMENT_1}}
**Mood**: {{MOOD_1}}

---

### [{{BLOCK_2_TIME}}] PROBLEMA - {{BLOCK_2_TITLE}}

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| {{TIME_6}} | {{VISUAL_6}} | {{CAMERA_6}} | {{LIGHTING_6}} |
| {{TIME_7}} | {{VISUAL_7}} | {{CAMERA_7}} | {{LIGHTING_7}} |
| {{TIME_8}} | {{VISUAL_8}} | {{CAMERA_8}} | {{LIGHTING_8}} |
| {{TIME_9}} | {{VISUAL_9}} | {{CAMERA_9}} | {{LIGHTING_9}} |
| {{TIME_10}} | {{VISUAL_10}} | {{CAMERA_10}} | {{LIGHTING_10}} |
| {{TIME_11}} | {{VISUAL_11}} | {{CAMERA_11}} | {{LIGHTING_11}} |

**Movimento Principal**: {{PRIMARY_MOVEMENT_2}}
**Mood**: {{MOOD_2}}

---

### [{{BLOCK_3_TIME}}] SOLUÇÃO - {{BLOCK_3_TITLE}}

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| {{TIME_12}} | {{VISUAL_12}} | {{CAMERA_12}} | {{LIGHTING_12}} |
| {{TIME_13}} | {{VISUAL_13}} | {{CAMERA_13}} | {{LIGHTING_13}} |
| {{TIME_14}} | {{VISUAL_14}} | {{CAMERA_14}} | {{LIGHTING_14}} |
| {{TIME_15}} | {{VISUAL_15}} | {{CAMERA_15}} | {{LIGHTING_15}} |
| {{TIME_16}} | {{VISUAL_16}} | {{CAMERA_16}} | {{LIGHTING_16}} |
| {{TIME_17}} | {{VISUAL_17}} | {{CAMERA_17}} | {{LIGHTING_17}} |
| {{TIME_18}} | {{VISUAL_18}} | {{CAMERA_18}} | {{LIGHTING_18}} |

**Movimento Principal**: {{PRIMARY_MOVEMENT_3}}
**Mood**: {{MOOD_3}}

---

### [{{BLOCK_4_TIME}}] DEMO - {{BLOCK_4_TITLE}}

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| {{TIME_19}} | {{VISUAL_19}} | {{CAMERA_19}} | {{LIGHTING_19}} |
| {{TIME_20}} | {{VISUAL_20}} | {{CAMERA_20}} | {{LIGHTING_20}} |
| {{TIME_21}} | {{VISUAL_21}} | {{CAMERA_21}} | {{LIGHTING_21}} |
| {{TIME_22}} | {{VISUAL_22}} | {{CAMERA_22}} | {{LIGHTING_22}} |
| {{TIME_23}} | {{VISUAL_23}} | {{CAMERA_23}} | {{LIGHTING_23}} |
| {{TIME_24}} | {{VISUAL_24}} | {{CAMERA_24}} | {{LIGHTING_24}} |
| {{TIME_25}} | {{VISUAL_25}} | {{CAMERA_25}} | {{LIGHTING_25}} |
| {{TIME_26}} | {{VISUAL_26}} | {{CAMERA_26}} | {{LIGHTING_26}} |

**Movimento Principal**: {{PRIMARY_MOVEMENT_4}}
**Mood**: {{MOOD_4}}

---

### [{{BLOCK_5_TIME}}] ESPECIALISTAS - {{BLOCK_5_TITLE}}

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| {{TIME_27}} | {{VISUAL_27}} | {{CAMERA_27}} | {{LIGHTING_27}} |
| {{TIME_28}} | {{VISUAL_28}} | {{CAMERA_28}} | {{LIGHTING_28}} |
| {{TIME_29}} | {{VISUAL_29}} | {{CAMERA_29}} | {{LIGHTING_29}} |
| {{TIME_30}} | {{VISUAL_30}} | {{CAMERA_30}} | {{LIGHTING_30}} |
| {{TIME_31}} | {{VISUAL_31}} | {{CAMERA_31}} | {{LIGHTING_31}} |
| {{TIME_32}} | {{VISUAL_32}} | {{CAMERA_32}} | {{LIGHTING_32}} |

**Movimento Principal**: {{PRIMARY_MOVEMENT_5}}
**Mood**: {{MOOD_5}}

---

### [{{BLOCK_6_TIME}}] DIFERENCIAL - {{BLOCK_6_TITLE}}

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| {{TIME_33}} | {{VISUAL_33}} | {{CAMERA_33}} | {{LIGHTING_33}} |
| {{TIME_34}} | {{VISUAL_34}} | {{CAMERA_34}} | {{LIGHTING_34}} |
| {{TIME_35}} | {{VISUAL_35}} | {{CAMERA_35}} | {{LIGHTING_35}} |
| {{TIME_36}} | {{VISUAL_36}} | {{CAMERA_36}} | {{LIGHTING_36}} |
| {{TIME_37}} | {{VISUAL_37}} | {{CAMERA_37}} | {{LIGHTING_37}} |
| {{TIME_38}} | {{VISUAL_38}} | {{CAMERA_38}} | {{LIGHTING_38}} |

**Momento {{BRAND_ELEMENT_1}}** ({{BRAND_MOMENT_TIME}}):
```
[VISUAL: {{BRAND_VISUAL_DESCRIPTION}}]
Câmera: {{BRAND_CAMERA}}
Iluminação: {{BRAND_LIGHTING}}
Texto overlay: {{BRAND_TEXT_OVERLAY}}
Música: {{BRAND_MUSIC_CUE}}
```

**Movimento Principal**: {{PRIMARY_MOVEMENT_6}}
**Mood**: {{MOOD_6}}

---

### [{{BLOCK_7_TIME}}] CTA - {{BLOCK_7_TITLE}}

| Tempo | Visual | Câmera | Iluminação |
|-------|--------|--------|------------|
| {{TIME_39}} | {{VISUAL_39}} | {{CAMERA_39}} | {{LIGHTING_39}} |
| {{TIME_40}} | {{VISUAL_40}} | {{CAMERA_40}} | {{LIGHTING_40}} |
| {{TIME_41}} | {{VISUAL_41}} | {{CAMERA_41}} | {{LIGHTING_41}} |
| {{TIME_42}} | {{VISUAL_42}} | {{CAMERA_42}} | {{LIGHTING_42}} |
| {{TIME_43}} | {{VISUAL_43}} | {{CAMERA_43}} | {{LIGHTING_43}} |

**Tagline Final**:
```
{{BRAND_NAME}}.
{{TAGLINE_LINE_1}}
{{TAGLINE_LINE_2}}
```

**Movimento Principal**: {{PRIMARY_MOVEMENT_7}}
**Mood**: {{MOOD_7}}

---

## PARTE 4: STYLE PRESET

| Parâmetro | Valor | Justificativa |
|-----------|-------|---------------|
| **Tone** | {{TONE_ARC}} | {{TONE_JUSTIFICATION}} |
| **Camera** | {{CAMERA_STYLE}} | {{CAMERA_JUSTIFICATION}} |
| **Lighting** | {{LIGHTING_ARC}} | {{LIGHTING_JUSTIFICATION}} |
| **Pacing** | {{PACING_STYLE}} | {{PACING_JUSTIFICATION}} |
| **Music** | {{MUSIC_ARC}} | {{MUSIC_JUSTIFICATION}} |

---

## PARTE 5: PROMPTS AUXILIARES

### Para Narração Teleprompter

```
Analise o Bloco [X] do {{SCRIPT_FILE}}.md e:

1. Reescreva para soar natural quando falado
2. Adicione pausas [PAUSA - 2s]
3. Marque ênfases [ÊNFASE: palavra]
4. Verifique timing (cabe no tempo?)

Output: Texto teleprompter-ready
```

### Para Gerar Shorts

```
Identifique {{NUMBER_OF_SHORTS}} momentos para cortes:

1. Hook ({{SHORT_1_TIME}}) - "{{SHORT_1_HOOK}}"
2. Problema ({{SHORT_2_TIME}}) - "{{SHORT_2_HOOK}}"
3. Solução ({{SHORT_3_TIME}}) - {{SHORT_3_DESCRIPTION}}
4. {{BRAND_ELEMENT_1}} ({{SHORT_4_TIME}}) - {{SHORT_4_DESCRIPTION}}
5. Tagline ({{SHORT_5_TIME}}) - "{{SHORT_5_HOOK}}"

Para cada: hook 3s + core + CTA
```

### Para Thumbnail

```
Gere {{NUMBER_OF_THUMBNAILS}} variações de thumbnail text:

1. Contraste: "{{THUMBNAIL_1}}"
2. Curiosidade: "{{THUMBNAIL_2}}"
3. Promessa: "{{THUMBNAIL_3}}"
4. Dor: "{{THUMBNAIL_4}}"
5. Resultado: "{{THUMBNAIL_5}}"
```

---

## PARTE 6: CHECKLIST PRÉ-PRODUÇÃO

- [ ] Script teleprompter-ready
- [ ] Assets visuais listados
- [ ] Música selecionada (arco narrativo)
- [ ] {{DEMO_ASSET_TYPE}} gravados
- [ ] {{BRAND_ASSET_1}} pronto
- [ ] Tagline {{TAGLINE_REFERENCE}} no final

---

**Versão**: 1.0.0
**Criado**: {{CREATION_DATE}}
**Atualizado**: {{UPDATE_DATE}}
**Integração**:
- {{SCRIPT_FILE}}.md {{SCRIPT_VERSION}}
- {{VISUAL_DIRECTION_FILE}}.md {{VISUAL_VERSION}}
**Uso**: Upload script + visual direction + context → Cole prompt → Itere

## Changelog
- **v1.0.0** ({{CREATION_DATE}}): Initial template distilled from {{SOURCE_FILE}}
