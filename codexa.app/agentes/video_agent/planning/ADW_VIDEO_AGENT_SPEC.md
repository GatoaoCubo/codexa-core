# ADW Video Agent - Especificacao para CODEXA

**Status**: SPEC_READY
**Para**: /prime-codexa
**De**: /prime-mentor
**Data**: 2025-11-25

---

## OBJETIVO

Construir um **ADW (Agentic Development Workflow)** dedicado para o video_agent que:
1. Orquestre a execucao completa do pipeline de 5 fases
2. Sincronize com o iso_vectorstore (22 arquivos)
3. Suporte os dois video_modes: "overlay" e "clean"
4. Integre as 8 vozes pt-br (4 femininas, 4 masculinas)
5. Execute validacao dos 11 pontos de qualidade

---

## CONTEXTO ATUAL

### Arquivos Existentes
- `workflows/100_ADW_RUN_VIDEO.md` - ADW basico (v1.0.0)
- `iso_vectorstore/08_ADW_orchestrator.md` - Replica para LLM platforms
- `PROCESSADOS/` - 6 cards de conhecimento processado (NOVO)
- `iso_vectorstore/21_voice_library_ptbr.md` - Vozes pt-br (NOVO)
- `iso_vectorstore/22_video_modes.md` - Modos overlay/clean (NOVO)

### HOPs Atualizados
- `20_script_writer_HOP.md` - v2.0.0 (vozes + video_mode)
- `30_visual_prompter_HOP.md` - v2.1.0 (composicao por modo)

### Gaps no ADW Atual
1. Nao referencia video_mode (overlay/clean)
2. Nao lista vozes pt-br disponiveis
3. Nao sincroniza com PROCESSADOS/catalogo.json
4. Falta integracao com iso_vectorstore expandido (22 arquivos)
5. Falta fase de auto-selecao de voz por tom

---

## REQUISITOS DO NOVO ADW

### 1. Nome e Versao
```
ADW-100: Complete Video Generation Workflow
Version: 2.0.0
Duration: 3-7 minutes
Phases: 5 + Pre-flight + Post-validation
```

### 2. Pre-Flight Phase (NOVO)

```yaml
PRE-FLIGHT:
  objective: Validar inputs e configurar modo
  duration: ~2s
  steps:
    - Validate brief schema
    - Auto-select video_mode (overlay/clean)
    - Auto-select voice (by tom + gender)
    - Load relevant PROCESSADOS/*.md context
    - Determine target platform (auto selection)
  outputs:
    - validated_brief.json
    - config.json (video_mode, voice, platform)
  quality_gate:
    - All required fields present
    - video_mode selected
    - voice_id valid
```

### 3. Phase Updates

#### Phase 2 (Script) - ATUALIZAR
```yaml
PHASE_2_SCRIPT:
  inputs:
    - concept.json
    - config.json (video_mode, voice)
  new_logic:
    - if video_mode == "clean": text_overlays = []
    - if video_mode == "overlay": generate overlays
    - voice_id from config (not hardcoded)
  outputs:
    - script.json (with video_mode field)
```

#### Phase 3 (Visual) - ATUALIZAR
```yaml
PHASE_3_VISUAL:
  inputs:
    - concept.json
    - config.json (video_mode)
  new_logic:
    - if video_mode == "clean": full frame composition
    - if video_mode == "overlay": reserve bottom 20%
  outputs:
    - visual_prompts.json (with composition_mode)
```

### 4. Post-Validation Phase (NOVO)

```yaml
POST-VALIDATION:
  objective: Validar video final com 11 pontos
  duration: ~5s
  steps:
    - Run 11-point quality checklist
    - Validate video_mode compliance
    - Generate Trinity output (.mp4, .llm.json, .meta.json)
    - Update PROCESSADOS/catalogo.json if quality >= 0.8
  outputs:
    - validation_report.json
    - Trinity files
  quality_gate:
    - All 11 points passed
    - Quality score >= 7.0
```

### 5. ISO Vectorstore Sync

O novo ADW deve referenciar todos os 22 arquivos:
```
iso_vectorstore/
├── 01_QUICK_START.md
├── 02_PRIME.md
├── 03_INSTRUCTIONS.md
├── 04_README.md
├── 05_SETUP.md
├── 06_input_schema.json
├── 07_video_styles.json
├── 08_ADW_orchestrator.md      <- SUBSTITUIR por nova versao
├── 09_platform_veo3.md
├── 10_platform_sora2.md
├── 11_platform_kling.md
├── 12_platform_hailuo.md
├── 13_platform_runway.md
├── 14_platform_pika.md
├── 15_prompt_anatomy.md
├── 16_camera_vocabulary.md
├── 17_lighting_vocabulary.md
├── 18_magic_words.md
├── 19_brand_alignment.md
├── 20_HOP_visual_prompter.md
├── 21_voice_library_ptbr.md    <- NOVO
└── 22_video_modes.md           <- NOVO
```

### 6. Voice Integration

```yaml
VOICE_INTEGRATION:
  provider: ElevenLabs
  model: eleven_multilingual_v2
  voices:
    femininas:
      - { id: "pMsXgVXv3BLzUgSXRplE", name: "Camila", tom: "energetico" }
      - { id: "EXAVITQu4vr4xnSDxMaL", name: "Bella", tom: "sofisticado" }
      - { id: "XrExE9yKIg1WjnnlVkGX", name: "Laura", tom: "profissional" }
      - { id: "nPczCjzI2devNBz1zQrb", name: "Vitoria", tom: "acolhedor" }
    masculinas:
      - { id: "TX3LPaxmHKxFdv7VOQHJ", name: "Rafael", tom: "sofisticado" }
      - { id: "ErXwobaYiN019PkySvjV", name: "Antoni", tom: "energetico" }
      - { id: "VR6AewLTigWG4xSOukaG", name: "Eduardo", tom: "profissional" }
      - { id: "pNInz6obpgDQGcFmaJgB", name: "Lucas", tom: "acolhedor" }
  auto_selection:
    by_tom: true
    default_gender: "feminina"
```

### 7. Video Mode Logic

```yaml
VIDEO_MODE_SELECTION:
  rules:
    clean:
      - international == true
      - tom == "premium" OR "cinematografico"
      - objective == "brand_awareness"
      - repurpose == true
      - platforms includes "youtube"
    overlay:
      - objective == "conversao"
      - platforms includes "instagram" OR "tiktok"
      - preco is not null
      - cta_required == true
  default: "overlay"
```

---

## ENTREGAVEIS ESPERADOS

### 1. workflows/100_ADW_RUN_VIDEO.md (v2.0.0)
ADW completo atualizado com:
- Pre-flight phase
- Video mode logic
- Voice selection logic
- Post-validation phase
- 22-file iso_vectorstore reference

### 2. iso_vectorstore/08_ADW_orchestrator.md (v2.0.0)
Versao portavel do ADW para LLM platforms

### 3. config/voice_config.json (NOVO)
Configuracao de vozes pt-br

### 4. config/video_modes.json (NOVO)
Regras de selecao de modo

---

## VALIDACAO

O novo ADW sera considerado completo quando:

- [ ] Pre-flight phase implementada
- [ ] Voice auto-selection funcionando
- [ ] Video mode auto-selection funcionando
- [ ] Phase 2 (Script) respeita video_mode
- [ ] Phase 3 (Visual) respeita video_mode
- [ ] Post-validation com 11 pontos
- [ ] Trinity output completo
- [ ] iso_vectorstore sincronizado (22 arquivos)
- [ ] PROCESSADOS/catalogo.json atualizado

---

## PRIORIDADE

**Alta** - Este ADW e o runner principal do video_agent

---

## COMANDO PARA CODEXA

```
/prime-codexa

Contexto: Especificacao ADW video_agent v2.0.0 em:
planning/ADW_VIDEO_AGENT_SPEC.md

Task: Construir ADW completo com:
1. Pre-flight phase (voice + video_mode auto-selection)
2. Updated Phase 2 (video_mode aware)
3. Updated Phase 3 (composition by mode)
4. Post-validation phase (11-point checklist)
5. ISO vectorstore sync (22 files)
6. Config files (voice_config.json, video_modes.json)

Output:
- workflows/100_ADW_RUN_VIDEO.md v2.0.0
- iso_vectorstore/08_ADW_orchestrator.md v2.0.0
- config/voice_config.json
- config/video_modes.json
```

---

**Criado por**: /prime-mentor
**Para execucao por**: /prime-codexa
**Status**: READY_FOR_CODEXA
