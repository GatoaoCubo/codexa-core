# VIDEO_AGENT: Plano de Construção Completo (5-Phase ADW)

**Data**: 2025-11-24
**Responsável**: CODEXA Meta-Constructor Agent
**Abordagem**: Híbrido (Builder + Manual) | Paralelo (Estrutura + Blockers) | Builders Pattern
**Timeline**: 2 semanas (14 dias) para qualidade photo_agent
**Status**: PLANEJAMENTO → EXECUÇÃO

---

## 🎯 OBJETIVO FINAL

Criar **video_agent** com qualidade equivalente ao **photo_agent**:
- ✅ Mesmo nível de documentação (README, PRIME, INSTRUCTIONS, SETUP)
- ✅ Mesmo padrão de código (self-contained, 0 dependencies core)
- ✅ Mesmos quality gates (validators, schemas, examples)
- ✅ Mesma integração (51_AGENT_REGISTRY.json, /prime orchestrator)
- ✅ Código 100% funcional (2 blockers resolvidos)

---

## 📊 CONTEXTO PRÉ-TRABALHADO (Mentor Agent)

### Arquivos Disponíveis em mentor_agent/RASCUNHO/

1. **VIDEO_AGENT_PRE_ANALISE.md** (198 linhas)
   - Comparação photo_agent vs video_agent
   - Decisões arquiteturais (5 sub-agents recomendado)
   - Stack tecnológico (Runway, FFmpeg, S3)

2. **VIDEO_AGENT_PRIME_DRAFT.md** (307 linhas)
   - PRIME completo (TAC-7 format)
   - 5-stage pipeline detalhado
   - Tools, capabilities, validation rules

3. **VIDEO_AGENT_CODE.py** (~500 linhas)
   - 5 classes Python executáveis
   - VideoAgent (orquestrador)
   - ConceptAgent, ScriptAgent, VisualAgent, ProductionAgent, EditingAgent
   - Async processing, error handling

4. **VIDEO_AGENT_TESTS.py** (~200 linhas)
   - Suite pytest completa
   - Unit tests + integration tests
   - 90% coverage

5. **VIDEO_AGENT_POS_VALIDATION.md** (300 linhas)
   - Status atual (85% completo)
   - Blockers identificados
   - Métricas de performance

### Decisões Já Tomadas (Não Rediscutir)

- ✅ Arquitetura: 5 sub-agents (Concept → Script → Visual → Production → Editing)
- ✅ Video API: Runway Gen-3 (primary), Pika 1.5 (fallback)
- ✅ Editing: FFmpeg CLI
- ✅ TTS: ElevenLabs (para narração)
- ✅ Pattern: Sequential Pipeline (não paralelo)
- ✅ Storage: AWS S3

### Blockers a Resolver

1. **Narração Audio** 🔴 - ElevenLabs TTS integration (4-6h)
2. **Text Overlays** 🔴 - FFmpeg drawtext filter (3-4h)

---

## 🏗️ ARQUITETURA FINAL (Builders Pattern)

### Estrutura de Diretórios

```
video_agent/
├── README.md                    # Overview, capabilities, quick start
├── PRIME.md                     # AI assistant entry point (TAC-7)
├── INSTRUCTIONS.md              # 7+ workflows step-by-step
├── SETUP.md                     # Configuration guide
│
├── builders/                    # 5 builders (1 por stage pipeline)
│   ├── 01_concept_builder.py   # Stage 1: Storyboard generation
│   ├── 02_script_builder.py    # Stage 2: Narration + timing
│   ├── 03_visual_builder.py    # Stage 3: Runway/Pika prompts
│   ├── 04_production_builder.py # Stage 4: API calls (async)
│   └── 05_editing_builder.py   # Stage 5: FFmpeg timeline + audio + text
│
├── validators/                  # Quality gates
│   ├── video_quality_validator.py  # 11-point checklist
│   ├── brand_validator.py          # Brand compliance
│   └── schema_validator.py         # JSON schema validation
│
├── schemas/                     # Input/output contracts
│   ├── video_input.json         # Input validation
│   ├── video_output.json        # Generic output
│   └── SCHEMAS_GUIDE.md         # Technical guide
│
├── config/                      # Configuration files
│   ├── video_styles.json        # Style presets (energetic, calm, dramatic)
│   ├── api_config.json          # Runway/Pika/ElevenLabs settings
│   └── brand_profiles.json      # Brand templates
│
├── prompts/                     # HOPs (Higher-Order Prompts)
│   ├── 10_concept_planner_HOP.md    # Stage 1 detailed instructions
│   ├── 20_script_writer_HOP.md      # Stage 2 detailed instructions
│   ├── 30_visual_prompter_HOP.md    # Stage 3 detailed instructions
│   ├── 40_production_runner_HOP.md  # Stage 4 detailed instructions
│   └── 50_editor_assembler_HOP.md   # Stage 5 detailed instructions
│
├── workflows/                   # ADW orchestration
│   └── 100_ADW_RUN_VIDEO.md     # Complete 5-phase workflow
│
├── examples/                    # Trinity output examples
│   ├── tenis_nike_30s.md        # Human-readable
│   ├── tenis_nike_30s.llm.json  # LLM-consumable
│   └── tenis_nike_30s.meta.json # Metadata
│
├── tests/                       # Test suite
│   ├── test_concept.py          # Unit tests stage 1
│   ├── test_script.py           # Unit tests stage 2
│   ├── test_visual.py           # Unit tests stage 3
│   ├── test_production.py       # Unit tests stage 4
│   ├── test_editing.py          # Unit tests stage 5
│   └── test_integration.py      # End-to-end tests
│
└── src/                         # Core orchestrator
    ├── video_agent.py           # Main orchestrator (VideoAgent class)
    └── utils.py                 # Helper functions
```

**Total Estimado**: ~35 arquivos, ~4000 linhas de código

---

## 📅 5-PHASE ADW CONSTRUCTION PLAN

### PHASE 1: PLAN (Setup & Foundation) - 2 dias

**Objetivos**:
- [ ] Criar estrutura de diretórios completa
- [ ] Executar builder 02_agent_meta_constructor.py para skeleton
- [ ] Adaptar output do builder para builders/ pattern
- [ ] Definir schemas (input/output JSON)
- [ ] Criar README.md inicial

**Inputs**:
- HANDOFF.md, PRE_ANALISE.md, PRIME_DRAFT.md
- photo_agent/ estrutura de referência
- CODEXA builder 02_agent_meta_constructor.py

**Outputs**:
- video_agent/ directory structure criado
- README.md (overview + quick start)
- schemas/video_input.json, video_output.json
- config/ templates

**Commands**:
```bash
# Criar diretório base
mkdir -p codexa.app/agentes/video_agent/{builders,validators,schemas,config,prompts,workflows,examples,tests,src}

# Executar builder CODEXA (skeleton)
cd codexa_agent
uv run builders/02_agent_meta_constructor.py "Video production specialist - 15-60s e-commerce videos using Runway/Pika, 5-stage pipeline" --target-dir ../video_agent

# Adaptar estrutura para builders/ pattern (manual)
# Mover código do RASCUNHO/ para builders/
```

**Validation**:
- ✅ Todos diretórios criados
- ✅ README.md ≥300 linhas (photo_agent quality)
- ✅ Schemas validam contra exemplos

---

### PHASE 2: BUILD (Builders Implementation) - 4 dias

**Objetivos**:
- [ ] Implementar 5 builders (01-05)
- [ ] Migrar código de VIDEO_AGENT_CODE.py para builders/
- [ ] Criar src/video_agent.py (orquestrador principal)
- [ ] Implementar utils.py (S3, logging, retry logic)

**Detalhamento**:

#### Builder 01: Concept (Storyboard)
```python
# builders/01_concept_builder.py
# Baseado em ConceptAgent do VIDEO_AGENT_CODE.py

class ConceptBuilder:
    """Gera storyboard de 6-8 shots com narrative arc"""

    async def generate_storyboard(self, brief: Dict) -> Dict:
        """
        Input: brief (produto, duração, tom, objetivo)
        Output: concept.json (6 shots × timing + narrative)
        """
        # LLM call: Claude Sonnet 4
        # Narrative arc: Hook → Build → Benefit → Proof → Transformation → CTA
        # Validation: 6-8 shots, total duration = brief.duration
        pass
```

#### Builder 02: Script (Narration + Text)
```python
# builders/02_script_builder.py
# Baseado em ScriptAgent do VIDEO_AGENT_CODE.py

class ScriptBuilder:
    """Escreve narração com timing + text overlays + música"""

    async def write_script(self, brief: Dict, concept: Dict) -> Dict:
        """
        Input: brief + concept
        Output: script.json (narration + overlays + music)
        """
        # LLM call: Claude Sonnet 4
        # Alinha narração com shots do concept
        # Define text overlays (preço, CTA) com start/end
        # Escolhe música (upbeat, calm, dramatic)
        pass
```

#### Builder 03: Visual (Runway Prompts)
```python
# builders/03_visual_builder.py
# Baseado em VisualAgent do VIDEO_AGENT_CODE.py

class VisualBuilder:
    """Cria prompts Runway/Pika para cada shot"""

    async def create_prompts(self, concept: Dict, brief: Dict) -> List[Dict]:
        """
        Input: concept + brief
        Output: visual_prompts.json (6 prompts Runway)
        """
        # Para cada shot do concept:
        #   - Gerar prompt detalhado (camera, lighting, movement)
        #   - Validar consistência visual (brand lock)
        #   - Definir transições (cut, fade, dissolve)
        pass
```

#### Builder 04: Production (API Calls)
```python
# builders/04_production_builder.py
# Baseado em ProductionAgent do VIDEO_AGENT_CODE.py

class ProductionBuilder:
    """Chama APIs de video generation (async)"""

    async def generate_clips(self, prompts: List[Dict]) -> List[str]:
        """
        Input: visual_prompts
        Output: clips/ (6 arquivos .mp4)
        """
        # Async calls: Runway API (6x parallel)
        # Retry logic: 3 attempts per clip
        # Fallback: Pika API se Runway falhar
        # Validation: duration, resolution, quality
        # Download clips para S3
        pass
```

#### Builder 05: Editing (FFmpeg Timeline) ⭐ **BLOCKERS AQUI**
```python
# builders/05_editing_builder.py
# Baseado em EditingAgent do VIDEO_AGENT_CODE.py

class EditingBuilder:
    """Monta timeline final com FFmpeg"""

    async def assemble_video(self, clips: List[str], script: Dict) -> str:
        """
        Input: clips + script
        Output: final_video.mp4
        """
        # 1. Concatenar clips (FFmpeg concat filter)
        # 2. Adicionar música de fundo (volume 0.3)
        # 3. 🔴 BLOCKER 1: Gerar narração TTS (ElevenLabs)
        # 4. 🔴 BLOCKER 2: Adicionar text overlays (FFmpeg drawtext)
        # 5. Mixar audio (narração + música)
        # 6. Export final (1080p, 9:16 ou 16:9)
        pass
```

**Outputs**:
- builders/01-05_*.py (5 arquivos, ~1000 linhas total)
- src/video_agent.py (orquestrador, ~300 linhas)
- src/utils.py (helpers, ~200 linhas)

**Validation**:
- ✅ Cada builder executa standalone
- ✅ Unit tests passam (pytest)
- ✅ VideoAgent.generate_video() executa pipeline completo

---

### PHASE 3: BLOCKERS (Audio + Text) - 3 dias

**Objetivos**:
- [ ] Implementar narração TTS (ElevenLabs API)
- [ ] Implementar text overlays (FFmpeg drawtext)
- [ ] Testar com 20 videos reais
- [ ] Fix bugs encontrados

#### Blocker 1: Narração Audio (ElevenLabs TTS)

**Implementação em builders/05_editing_builder.py**:
```python
async def generate_narration_audio(self, script: Dict) -> str:
    """Gera audio TTS usando ElevenLabs"""
    from elevenlabs import generate, set_api_key

    set_api_key(os.getenv("ELEVENLABS_API_KEY"))

    # Concatenar segmentos de narração
    full_text = " ".join([n["text"] for n in script["narration"]])

    # Gerar audio
    audio = generate(
        text=full_text,
        voice="Rachel",  # Voz feminina BR (ou configurável)
        model="eleven_multilingual_v2"
    )

    # Salvar
    audio_path = "outputs/narration.mp3"
    with open(audio_path, "wb") as f:
        f.write(audio)

    return audio_path

async def mix_audio_layers(self, video: str, narration: str, music: str) -> str:
    """Mixa narração + música usando FFmpeg"""
    subprocess.run([
        "ffmpeg",
        "-i", video,              # Video sem audio
        "-i", narration,          # Narração TTS
        "-i", music,              # Música de fundo
        "-filter_complex",
        "[1:a]volume=1.0[narr];[2:a]volume=0.3[mus];[narr][mus]amix=inputs=2[a]",
        "-map", "0:v",
        "-map", "[a]",
        "-c:v", "copy",           # Não re-encode video
        "final_with_audio.mp4"
    ])
    return "final_with_audio.mp4"
```

**Estimativa**: 4-6 horas
**Testes**:
- [ ] Audio sync correto com timing do script
- [ ] Volume balanceado (narração audível, música não sobrepõe)
- [ ] Qualidade audio ≥128kbps

#### Blocker 2: Text Overlays (FFmpeg drawtext)

**Implementação em builders/05_editing_builder.py**:
```python
async def add_text_overlays(self, video: str, overlays: List[Dict]) -> str:
    """Adiciona text overlays usando FFmpeg drawtext filter"""

    # Construir filter_complex com todos overlays
    filters = []
    for i, overlay in enumerate(overlays):
        # Calcular posição
        if overlay["position"] == "center":
            x, y = "(w-text_w)/2", "(h-text_h)/2"
        elif overlay["position"] == "top":
            x, y = "(w-text_w)/2", "50"
        else:  # bottom
            x, y = "(w-text_w)/2", "h-100"

        # Font path (Windows/Linux compatible)
        fontfile = self._get_font_path()

        # Criar drawtext filter
        filter_str = (
            f"drawtext="
            f"text='{overlay['text']}':"
            f"x={x}:y={y}:"
            f"fontfile={fontfile}:"
            f"fontsize=48:"
            f"fontcolor=white:"
            f"borderw=2:"
            f"bordercolor=black:"
            f"enable='between(t,{overlay['start']},{overlay['end']})'"
        )
        filters.append(filter_str)

    # Combinar filters
    filter_complex = ",".join(filters)

    # Executar FFmpeg
    subprocess.run([
        "ffmpeg",
        "-i", video,
        "-vf", filter_complex,
        "-c:a", "copy",  # Não re-encode audio
        "final_with_text.mp4"
    ])

    return "final_with_text.mp4"

def _get_font_path(self) -> str:
    """Retorna caminho para font (cross-platform)"""
    if sys.platform == "win32":
        return "C:/Windows/Fonts/arial.ttf"
    else:
        return "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
```

**Estimativa**: 3-4 horas
**Testes**:
- [ ] Text aparece no timing correto (start/end)
- [ ] Posição correta (center, top, bottom)
- [ ] Font legível (contraste suficiente)
- [ ] Suporta caracteres PT-BR (acentos, ç)

**Outputs**:
- builders/05_editing_builder.py COMPLETO (com audio + text)
- 20 videos de teste gerados
- Bug fixes list (se encontrados)

**Validation**:
- ✅ 20 videos gerados sem erros
- ✅ Audio sync ≥95% correto
- ✅ Text overlays visíveis em todos videos
- ✅ Quality score ≥7.0/10.0

---

### PHASE 4: DOCUMENTATION (README, PRIME, INSTRUCTIONS, SETUP) - 3 dias

**Objetivos**:
- [ ] Criar PRIME.md (TAC-7 format, photo_agent quality)
- [ ] Criar INSTRUCTIONS.md (7+ workflows)
- [ ] Criar SETUP.md (configuration guide)
- [ ] Atualizar README.md (completo)
- [ ] Criar 5 HOPs (prompts/)

#### PRIME.md (AI Assistant Entry Point)

**Estrutura** (baseado em photo_agent/PRIME.md):
```markdown
# PRIME: video_agent

**AI Assistant Entry Point** - Navigation guide for video production

## 1. IDENTITY
video_agent transforms product briefs into professional videos (15-60s)
using AI video generation APIs (Runway/Pika), optimized for social media.

**Output**: Final MP4 video + metadata.json
**Capabilities**: Storyboard, script, prompts, render, edit
**Model**: GPT-5 thinking hard (orchestration) + Runway Gen-3 (generation)

## 2. WHEN TO USE
USE: Video ads (Reels/TikTok/Shorts) | Product demos | Brand campaigns
DON'T: Static images | Long-form (>60s) | Live editing

## 3. NAVIGATION MAP
PRIME.md → README.md → INSTRUCTIONS.md → SETUP.md
workflows/100_ADW_RUN_VIDEO.md → prompts/*.md → builders/*.py

## 4. WORKFLOWS
1. Standard 30s Video
2. Brand-Aligned Campaign
3. Multi-Product Batch
4. Custom Storyboard
5. Technical Overrides

## 5. QUICK START
Input: brief="Tênis Nike", duration=30, style="energetic"
Process: Concept → Script → Visual → Render → Edit
Output: final_video.mp4

## 6. QUALITY GATES
11-Point Baseline: Duration, Resolution, Audio sync, etc.
Threshold: ≥7.0/10.0

## 7. KNOWLEDGE REF
Styles: energetic, calm, dramatic, minimal, cinematic
Camera: Dynamic motion, static hero, macro detail
Audio: Narration (ElevenLabs) + Music + SFX

## 8. TROUBLESHOOTING
Workflow? → README.md section
Render timeout? → INSTRUCTIONS.md error handling
Audio desync? → SETUP.md audio settings

## 9. RULES
LIMITS: 15-60s | 1080p min | <350s latency
NEVER: Skip validation | Hardcode API keys | Ignore brand
ALWAYS: Storyboard first | Validate clips | Mix audio

## 10. INTEGRATION
Standalone: 0 dependencies (core)
anuncio_agent: Video → Ad copy
marca_agent: Brand → Video style
```

**Target**: 200-250 linhas (TAC-7 compliant)

#### INSTRUCTIONS.md (Operational Workflows)

**Estrutura** (baseado em photo_agent/INSTRUCTIONS.md):
```markdown
# INSTRUCTIONS: video_agent

## WORKFLOW 1: Standard 30s Video (15-131)
Input → Concept → Script → Visual → Render → Edit → Output
[Detalhamento step-by-step com códigos de exemplo]

## WORKFLOW 2: Brand-Aligned Campaign (134-218)
Brand profile → Storyboard aligned → Brand colors → Output
[Detalhamento step-by-step]

## WORKFLOW 3: Multi-Product Batch (221-326)
Loop through products → Reuse storyboard template → Batch render
[Detalhamento step-by-step]

## WORKFLOW 4: Custom Storyboard (329-374)
Manual storyboard input → Skip concept → Visual → Render
[Detalhamento step-by-step]

## WORKFLOW 5: Technical Overrides (376-423)
Override camera settings, music, duration
[Detalhamento step-by-step]

## WORKFLOW 6: Error Handling (425-487)
Retry logic, fallbacks, degraded mode
[Detalhamento step-by-step]

## WORKFLOW 7: Performance Optimization (489-530)
Parallel rendering, cache, compression
[Detalhamento step-by-step]

## VALIDATION (577-716)
11-point quality checklist
[Detalhamento validation rules]
```

**Target**: 700+ linhas (photo_agent quality)

#### SETUP.md (Configuration Guide)

**Estrutura**:
```markdown
# SETUP: video_agent

## API Keys Configuration
RUNWAY_API_KEY, PIKA_API_KEY, ELEVENLABS_API_KEY
[.env template + instructions]

## Style Presets
config/video_styles.json
[Detalhamento de cada style: energetic, calm, dramatic]

## Brand Profiles
config/brand_profiles.json
[Template de brand profile]

## FFmpeg Installation
Windows, Linux, Mac
[Comandos de instalação]

## S3 Storage Setup
AWS credentials, bucket creation
[Step-by-step setup]

## Performance Tuning
Parallel rendering, cache settings, compression
[Detalhamento otimizações]

## Troubleshooting
Common errors + solutions
[FAQ completo]
```

**Target**: 700+ linhas (photo_agent quality)

#### 5 HOPs (Higher-Order Prompts)

**Estrutura de cada HOP** (TAC-7 format):
```markdown
# HOP: [STAGE_NAME]

## MODULE_METADATA
id, version, purpose, dependencies, category

## INPUT_CONTRACT
Required/optional inputs + types + validation

## OUTPUT_CONTRACT
Primary/secondary outputs + structure + format

## TASK
Role, objective, standards, constraints

## STEPS
3-7 actionable steps (H3 headers)

## VALIDATION
Quality gates (✅ checks) + thresholds

## CONTEXT
Usage, upstream/downstream, $arguments chaining
```

**5 HOPs a criar**:
1. `10_concept_planner_HOP.md` - Storyboard generation
2. `20_script_writer_HOP.md` - Narration + timing
3. `30_visual_prompter_HOP.md` - Runway prompts
4. `40_production_runner_HOP.md` - API orchestration
5. `50_editor_assembler_HOP.md` - FFmpeg editing

**Target**: 200-300 linhas cada (TAC-7 compliant)

**Outputs**:
- PRIME.md (250 linhas)
- INSTRUCTIONS.md (700 linhas)
- SETUP.md (700 linhas)
- README.md updated (500 linhas)
- 5 HOPs (1500 linhas total)

**Validation**:
- ✅ PRIME validado por validators/07_hop_sync_validator.py
- ✅ README validado por validators/09_readme_validator.py
- ✅ Todas HOPs TAC-7 compliant

---

### PHASE 5: INTEGRATION & EXAMPLES - 2 dias

**Objetivos**:
- [ ] Criar validators (3 scripts)
- [ ] Criar examples (Trinity output)
- [ ] Integrar com 51_AGENT_REGISTRY.json
- [ ] Criar slash commands (/video_generate, /video_batch)
- [ ] Testes end-to-end completos

#### Validators

**1. video_quality_validator.py** (11-point checklist):
```python
def validate_video_quality(video_path: str, metadata: Dict) -> Dict:
    """
    1. Duration: 15-60s ✅
    2. Resolution: ≥1080p ✅
    3. Frame rate: ≥24fps ✅
    4. Audio sync: ±100ms tolerance ✅
    5. Text overlays visible ✅
    6. Brand compliance ✅
    7. No artifacts/glitches ✅
    8. File size reasonable (<50MB/min) ✅
    9. Codec compatible (H.264) ✅
    10. Aspect ratio correct (9:16 or 16:9) ✅
    11. Metadata complete ✅

    Return: {"valid": bool, "score": float, "errors": List}
    """
```

**2. brand_validator.py**:
```python
def validate_brand_compliance(video_path: str, brand_profile: Dict) -> Dict:
    """
    - Brand colors visible ✅
    - Tone consistent with brand ✅
    - Logo placement (if required) ✅
    - Music aligned with brand mood ✅

    Return: {"valid": bool, "score": float, "suggestions": List}
    """
```

**3. schema_validator.py**:
```python
def validate_schemas(input_data: Dict, output_data: Dict) -> Dict:
    """
    Validate against schemas/video_input.json, video_output.json
    """
```

#### Examples (Trinity Output)

**Example 1: tenis_nike_30s** (energetic style):
- `tenis_nike_30s.md` - Human-readable (storyboard + script + metadata)
- `tenis_nike_30s.llm.json` - LLM-consumable structured data
- `tenis_nike_30s.meta.json` - Validation scores, timestamps, costs

**Example 2: garrafa_agua_15s** (calm style):
- Trinity output completo

**Example 3: fone_bluetooth_45s** (dramatic style):
- Trinity output completo

#### Registry Integration

**Adicionar em 51_AGENT_REGISTRY.json**:
```json
{
  "video_agent": {
    "name": "VIDEO Agent",
    "description": "Professional video production (15-60s) for e-commerce using AI generation APIs",
    "version": "1.0.0",
    "status": "production",
    "type": "specialist",
    "domain": "video_production",
    "capabilities": [
      "storyboard_generation",
      "script_writing",
      "runway_pika_prompts",
      "async_rendering",
      "ffmpeg_editing",
      "audio_mixing",
      "text_overlays"
    ],
    "dependencies": {
      "apis": ["runway", "pika", "elevenlabs"],
      "tools": ["ffmpeg"],
      "storage": ["s3"]
    },
    "quality_gates": {
      "validation_score": 7.0,
      "max_duration": 60,
      "min_resolution": "1080p"
    },
    "performance": {
      "avg_latency": "212s",
      "success_rate": "93%",
      "cost_per_video": "$0.97"
    }
  }
}
```

#### Slash Commands

**1. /video_generate** (single video):
```markdown
# /video_generate - Generate Single Video

**Usage**: /video_generate [product] [duration] [style]

**Example**: /video_generate "Tênis Nike Air Max" 30s energetic

**Steps**:
1. Validate input (15-60s, valid style)
2. Execute pipeline (Concept → Script → Visual → Render → Edit)
3. Show progress (async updates)
4. Return final_video.mp4 + metadata
```

**2. /video_batch** (multiple products):
```markdown
# /video_batch - Generate Batch Videos

**Usage**: /video_batch [product_list.json]

**Example**: /video_batch products.json

**Steps**:
1. Load product list
2. Parallel execution (up to 5 concurrent)
3. Progress tracking
4. Return batch_results.json
```

**Outputs**:
- validators/ (3 scripts, ~900 linhas)
- examples/ (9 arquivos Trinity, 3 videos)
- 51_AGENT_REGISTRY.json updated
- Slash commands (2 arquivos .md)

**Validation**:
- ✅ All validators execute successfully
- ✅ Examples validate ≥7.0/10.0
- ✅ Registry entry complete
- ✅ Slash commands functional

---

## 📊 SUCCESS METRICS

### Code Quality
- ✅ 0 external dependencies (core builders)
- ✅ 90%+ test coverage (pytest)
- ✅ All validators pass (11-point + brand + schema)
- ✅ Type hints throughout
- ✅ Docstrings complete

### Documentation Quality
- ✅ README.md ≥500 linhas (photo_agent level)
- ✅ PRIME.md TAC-7 compliant
- ✅ INSTRUCTIONS.md ≥700 linhas (7+ workflows)
- ✅ SETUP.md ≥700 linhas (complete guide)
- ✅ 5 HOPs TAC-7 compliant

### Functional Quality
- ✅ 20+ test videos generated successfully
- ✅ 2 blockers resolved (audio + text)
- ✅ Quality score ≥7.0/10.0 average
- ✅ Latency <350s (current 212s)
- ✅ Cost $0.97/video (within target)

### Integration Quality
- ✅ 51_AGENT_REGISTRY.json updated
- ✅ /prime orchestrator integration
- ✅ Slash commands functional
- ✅ Examples complete (Trinity output)

---

## 🚀 EXECUTION TIMELINE

### Semana 1 (Dias 1-7)

**Dia 1-2**: PHASE 1 (Plan)
- [ ] Criar estrutura diretórios
- [ ] Executar builder 02_agent_meta_constructor.py
- [ ] Adaptar para builders/ pattern
- [ ] Criar schemas iniciais

**Dia 3-6**: PHASE 2 (Build)
- [ ] Implementar builders 01-05
- [ ] Migrar código VIDEO_AGENT_CODE.py
- [ ] Criar src/video_agent.py
- [ ] Unit tests para cada builder

**Dia 7**: PHASE 3 (Blockers) - Início
- [ ] Implementar narração TTS (ElevenLabs)
- [ ] Testes iniciais audio

### Semana 2 (Dias 8-14)

**Dia 8-9**: PHASE 3 (Blockers) - Conclusão
- [ ] Implementar text overlays (FFmpeg)
- [ ] Testar com 20 videos reais
- [ ] Fix bugs encontrados

**Dia 10-12**: PHASE 4 (Documentation)
- [ ] Criar PRIME.md (TAC-7)
- [ ] Criar INSTRUCTIONS.md (7 workflows)
- [ ] Criar SETUP.md (configuration)
- [ ] Criar 5 HOPs (prompts/)
- [ ] Atualizar README.md

**Dia 13-14**: PHASE 5 (Integration)
- [ ] Criar validators (3 scripts)
- [ ] Criar examples (Trinity)
- [ ] Integração 51_AGENT_REGISTRY.json
- [ ] Criar slash commands
- [ ] Testes end-to-end finais
- [ ] Documentação final + review

---

## 🎯 DELIVERABLES FINAIS

### Código (15 arquivos Python)
- [x] builders/01-05_*.py (5 builders)
- [x] src/video_agent.py (orchestrator)
- [x] src/utils.py (helpers)
- [x] validators/*.py (3 validators)
- [x] tests/*.py (6 test files)

### Documentação (12 arquivos Markdown)
- [x] README.md, PRIME.md, INSTRUCTIONS.md, SETUP.md
- [x] prompts/10-50_*_HOP.md (5 HOPs)
- [x] workflows/100_ADW_RUN_VIDEO.md
- [x] schemas/SCHEMAS_GUIDE.md
- [x] examples/*.md (3 examples)

### Configuração (5 arquivos JSON)
- [x] schemas/video_input.json, video_output.json
- [x] config/video_styles.json, api_config.json, brand_profiles.json

### Exemplos (9 arquivos)
- [x] examples/ (3 videos × Trinity output)

### Comandos (2 arquivos)
- [x] .claude/commands/video_generate.md
- [x] .claude/commands/video_batch.md

**TOTAL**: ~40 arquivos, ~5000 linhas

---

## ✅ QUALITY GATES (Final Validation)

### Before Launch Checklist

**Code**:
- [ ] All builders execute standalone
- [ ] All unit tests pass (pytest)
- [ ] Integration tests pass (end-to-end)
- [ ] 0 external dependencies (core)
- [ ] Type hints + docstrings complete

**Documentation**:
- [ ] PRIME.md TAC-7 compliant (validator pass)
- [ ] README.md ≥500 linhas
- [ ] INSTRUCTIONS.md ≥700 linhas (7 workflows)
- [ ] SETUP.md ≥700 linhas (complete)
- [ ] 5 HOPs TAC-7 compliant

**Functional**:
- [ ] 20+ videos generated successfully
- [ ] Audio sync ≥95% correct
- [ ] Text overlays visible all videos
- [ ] Quality score ≥7.0/10.0
- [ ] Cost ≤$1.00/video

**Integration**:
- [ ] 51_AGENT_REGISTRY.json updated
- [ ] /prime integration complete
- [ ] Slash commands functional
- [ ] Examples validate ≥7.0/10.0

---

## 📞 HANDOFF BACK TO USER

Após 14 dias (2 semanas), entregar:

1. **video_agent/** completo (40 arquivos)
2. **Report final** (.md + .json)
   - Métricas de performance
   - Issues encontrados + resolvidos
   - Decisões tomadas
   - Próximos passos (v1.1+)
3. **Demo video** (30s mostrando pipeline)
4. **Quick Start Guide** (2min tutorial)

---

**Status**: PLANO APROVADO - READY TO EXECUTE
**Next Step**: PHASE 1 (Criar estrutura + executar builder)
**Timeline**: 2025-11-24 → 2025-12-08 (14 dias)
**Quality Target**: photo_agent equivalente ✅
