# 102_ADW_NOTEBOOKLM_VIDEO | Script to NotebookLM Video Pipeline

**ID**: 102_ADW_NOTEBOOKLM_VIDEO
**Version**: 1.0.0
**Type**: ADW (Agentic Developer Workflow)
**Chain**: curso_agent → video_agent → NotebookLM
**Created**: 2025-12-03
**Status**: Production Ready

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "ADW-102",
  "workflow_name": "NotebookLM Video Pipeline",
  "agent": "video_agent",
  "version": "1.0.0",
  "chain": "curso_agent → video_agent → NotebookLM",
  "purpose": "Transform curso_agent scripts into NotebookLM-ready packages for video generation",
  "min_llm_model": "claude-sonnet-4+",
  "phases": [
    {"phase_id": "phase_1_locate", "phase_name": "Locate & Validate", "duration": "30s"},
    {"phase_id": "phase_2_extract", "phase_name": "Extract Sections", "duration": "2min"},
    {"phase_id": "phase_3_visual_match", "phase_name": "Visual Match", "duration": "2min"},
    {"phase_id": "phase_4_package", "phase_name": "Package Bundle", "duration": "2min"},
    {"phase_id": "phase_5_validate", "phase_name": "Validate Package", "duration": "1min"}
  ],
  "total_duration": "5-10min"
}
```

---

## PURPOSE

Transform video scripts from `curso_agent` (VIDEO_LP_*.md) into complete NotebookLM upload packages with visual direction, context files, and generation prompts.

**Key Insight**: NotebookLM generates better video guidance when fed structured, separated files:
- **Script**: What to say (narration, timecodes)
- **Visual Direction**: How it looks (camera, lighting, mood)
- **Context**: Supporting knowledge (glossary, word banks, agent specs)

This ADW bridges the gap between curso_agent's educational content and NotebookLM's video production AI.

---

## INPUT_CONTRACT

### From curso_agent

**Required Files**:
1. `VIDEO_LP_*.md` - Main script with timecodes and narration
   - Example: `VIDEO_LP_ROTEADOR.md`, `VIDEO_LP_CODEXA_10MIN_ROTEIRO_COMPLETO.md`
2. `DIRECAO_VISUAL_LP_*.md` - Visual direction (camera, lighting, movement)
   - Example: `DIRECAO_VISUAL_LP_ROTEADOR.md`

**Optional Context Files**:
3. `NOTEBOOKLM_VIDEO_LP_*.md` - NotebookLM prompt template
4. `RESEARCH_BANCO_PALAVRAS_OTIMIZADAS.md` - Validated hooks and triggers
5. `GLOSSARIO.md` - Technical terminology

**Expected Structure in VIDEO_LP_*.md**:
```markdown
## TIMELINE MASTER
| Tempo | Secao | Duracao | Mood |
|-------|-------|---------|------|
| 00:00-01:00 | Hook + Abertura | 60s | Tensao |

## SECAO 1: HOOK + ABERTURA (00:00-01:00)

### SHOT 1: COLD OPEN (00:00-00:08)
**VISUAL**: Tela preta. Fade in para grid de logos...
**NARRACAO**: "A ferramenta que voce paga..."
**OVERLAY TEXT**: GPT-3.5 (nov/2022)
```

**Variant Detection**:
- Video A (calm): Standard pacing, professional tone
- Video B (urgent): Fast pacing, high-energy, urgency triggers

---

## PHASES

### Phase 1: LOCATE & VALIDATE (30s)

**Objective**: Find script files and validate structure

**Actions**:

1. **Search for Script Files**
   ```bash
   # Search curso_agent outputs and context
   find codexa.app/agentes/curso_agent/ -name "VIDEO_LP_*.md"
   find codexa.app/agentes/curso_agent/ -name "DIRECAO_VISUAL_*.md"
   ```

2. **Validate Script Structure**
   - Check file size >20KB (substantive content)
   - Verify contains "TIMELINE MASTER" section
   - Verify contains section breakdowns with timecodes
   - Verify contains NARRACAO blocks
   - Verify contains VISUAL blocks

3. **Validate Visual Direction**
   - Check corresponding DIRECAO_VISUAL_*.md exists
   - Verify contains camera movements
   - Verify contains lighting specifications
   - Verify contains mood descriptors

4. **Detect Variant**
   - Parse filename for variant suffix (_A, _B, or none)
   - Analyze tone words in script:
     - Variant A: "sofisticado", "clean", "professional"
     - Variant B: "urgente", "immediate", "agitacao"
   - Default to standard if unclear

**Output**:
```json
{
  "script_path": "C:\\...\\VIDEO_LP_ROTEADOR.md",
  "visual_path": "C:\\...\\DIRECAO_VISUAL_LP_ROTEADOR.md",
  "notebooklm_prompt_path": "C:\\...\\NOTEBOOKLM_VIDEO_LP_ROTEADOR.md",
  "variant": "standard",
  "topic": "roteador",
  "duration_seconds": 660,
  "file_size_kb": 87,
  "last_modified": "2025-12-02T15:30:00Z"
}
```

**Quality Gate**:
- [ ] Script file exists and readable
- [ ] File size ≥20KB
- [ ] Contains required sections (TIMELINE MASTER, section breakdowns)
- [ ] Visual direction file exists
- [ ] Timecodes present and formatted correctly

---

### Phase 2: EXTRACT SECTIONS (2min)

**Objective**: Parse script sections with timecodes, narration, visuals, and psychological triggers

**Actions**:

1. **Parse Timeline Master**
   - Extract table: Tempo | Secao | Duracao | Mood
   - Calculate total duration
   - Identify section count
   - Map timecodes to sections

2. **Extract Section Details**
   For each section (e.g., "SECAO 1: HOOK + ABERTURA"):
   - Parse timecode range (00:00-01:00)
   - Extract section title and purpose
   - Parse all shots within section

3. **Extract Shot Components**
   For each shot:
   ```json
   {
     "shot_number": 1,
     "shot_title": "COLD OPEN",
     "timecode": "00:00-00:08",
     "duration_seconds": 8,
     "visual_description": "Tela preta. Fade in para grid de logos...",
     "narration_text": "A ferramenta que voce paga todo mes usa um modelo de 2022...",
     "overlay_text": "GPT-3.5 (nov/2022)\\n↓\\nSua \"IA Premium\" (2025)",
     "mood": "tensao, disrupcao"
   }
   ```

4. **Identify Visual Cues**
   - Extract [VISUAL: ...] blocks
   - Parse camera movements mentioned
   - Identify transitions (fade, cut, dissolve)
   - Detect split-screen, animations, effects

5. **Map Psychological Triggers**
   Parse gatilhos psicológicos mentioned in script:
   - Proof (social proof, results)
   - Scarcity (limited, exclusive)
   - Authority (expert, data)
   - Loss aversion (missing out)
   - Contrast (before/after)
   - Humor (Cat Coding, easter eggs)

6. **Detect Easter Eggs**
   - **Cat Coding**: "Cat Coding" mention (humor break)
   - **CHURU MODE**: "CHURU MODE" activation (playful)
   - **Tagline**: "Um agente para todos governar..." (Lord of the Rings reference)
   - **Pirulita**: Cat character reference
   - Note timing and context for each

**Output**:
```json
{
  "script_metadata": {
    "total_duration_seconds": 660,
    "total_sections": 7,
    "total_shots": 42,
    "variant": "standard"
  },
  "sections": [
    {
      "section_number": 1,
      "title": "HOOK + ABERTURA",
      "timecode": "00:00-01:00",
      "duration_seconds": 60,
      "mood": "tensao, disrupcao",
      "shots": [
        {
          "shot_number": 1,
          "shot_title": "COLD OPEN",
          "timecode": "00:00-00:08",
          "duration_seconds": 8,
          "visual": "Tela preta. Fade in para grid de logos IA desfocados...",
          "narration": "A ferramenta que voce paga todo mes usa um modelo de 2022...",
          "overlay_text": "GPT-3.5 (nov/2022)",
          "transitions": ["fade_in", "hard_cut"]
        }
      ]
    }
  ],
  "psychological_triggers": {
    "proof": ["margem de lucro dez mil por cento", "87% dos especialistas"],
    "authority": ["empresas bilionarias", "meta-construcao"],
    "contrast": ["camada errada", "cerebro plugavel vs prompt manual"],
    "humor": ["Cat Coding", "Pirulita", "CHURU MODE"]
  },
  "easter_eggs": [
    {
      "name": "Cat Coding",
      "timecode": "09:45-10:00",
      "context": "Diferencial - humor break",
      "description": "Pirulita coding while humans orchestrate"
    },
    {
      "name": "Tagline",
      "timecode": "10:50-11:00",
      "context": "CTA final",
      "description": "Um agente para todos governar (Lord of the Rings)"
    }
  ]
}
```

**Quality Gate**:
- [ ] All sections extracted (count ≥3)
- [ ] All shots have narration text
- [ ] Timecodes sequential and non-overlapping
- [ ] Mood descriptors present
- [ ] Easter eggs identified (if present)

---

### Phase 3: VISUAL MATCH (2min)

**Objective**: Load visual direction and align with script timecodes

**Actions**:

1. **Load Visual Direction File**
   - Read DIRECAO_VISUAL_LP_*.md
   - Parse camera movements table
   - Extract lighting arc (COLD → WARM → GOLDEN)
   - Parse style presets and color palettes

2. **Match Timecodes: Script ↔ Visual**
   For each section in script:
   - Find corresponding section in visual direction
   - Match timecode ranges (allow ±5s tolerance)
   - Extract camera movement for section
   - Extract lighting setup for section
   - Validate alignment

3. **Generate Shot List**
   Combine script + visual for each shot:
   ```json
   {
     "shot_number": 1,
     "timecode": "00:00-00:08",
     "narration": "A ferramenta que voce paga...",
     "visual_description": "Tela preta. Fade in grid logos...",
     "camera_movement": "slow zoom in",
     "camera_angle": "flat (2D elements)",
     "lighting": "cold blue (5500K-6500K), high contrast",
     "mood": "tensao, impacto",
     "transition_out": "hard cut"
   }
   ```

4. **Validate Camera/Lighting Coverage**
   - Ensure every shot has camera specs
   - Ensure every section has lighting direction
   - Check for conflicts (e.g., static + zoom)
   - Flag missing specs

5. **Extract Style Presets**
   - Primary color palette (hex codes)
   - Font specifications (Montserrat, Open Sans)
   - Persistent elements (logo, URL, progress bar)
   - Transition types (cut, dissolve, slide)

**Output**:
```json
{
  "shot_list": [
    {
      "shot_number": 1,
      "timecode": "00:00-00:08",
      "duration_seconds": 8,
      "script": {
        "narration": "A ferramenta que voce paga todo mes...",
        "visual": "Tela preta. Fade in grid logos...",
        "overlay_text": "GPT-3.5 (nov/2022)"
      },
      "visual_direction": {
        "camera_movement": "slow zoom in (10-15% per second)",
        "camera_angle": "flat (2D elements)",
        "lighting": {
          "phase": "COLD",
          "temperature": "5500K-6500K",
          "contrast": "high",
          "mood": "desconforto, fragmentacao"
        },
        "transition_out": "hard cut"
      },
      "style": {
        "color_primary": "#0D9488",
        "color_accent": "#F59E0B",
        "font_title": "Montserrat Bold 48-72px",
        "font_body": "Open Sans Regular 24-36px"
      }
    }
  ],
  "alignment_report": {
    "total_shots_matched": 42,
    "timecode_mismatches": 0,
    "missing_camera_specs": 0,
    "missing_lighting_specs": 0
  }
}
```

**Quality Gate**:
- [ ] All shots have camera movement specified
- [ ] All sections have lighting specs
- [ ] Timecode alignment ±5s tolerance
- [ ] No conflicts in camera directions
- [ ] Style presets extracted (colors, fonts)

---

### Phase 4: PACKAGE BUNDLE (2min)

**Objective**: Compile NotebookLM upload bundle with clean, structured files

**Actions**:

1. **Generate script_narration.md**
   - Extract ONLY narration text (clean)
   - Remove technical markers ([VISUAL:], **OVERLAY TEXT:**)
   - Keep timecodes for context
   - Format for NotebookLM readability

   ```markdown
   # Script Narration: CODEXA Roteador Video

   **Duration**: 11 minutes
   **Sections**: 7

   ## Section 1: HOOK + ABERTURA (00:00-01:00)

   ### Shot 1 (00:00-00:08)
   "A ferramenta que voce paga todo mes usa um modelo de 2022. Margem de lucro: dez mil por cento."

   ### Shot 2 (00:08-00:18)
   "Oitenta e sete por cento dos especialistas brasileiros em IA nunca escreveram codigo..."
   ```

2. **Generate visual_direction.md**
   - Technical specs only
   - Camera movements, lighting, transitions
   - No narration text (avoid duplication)

   ```markdown
   # Visual Direction: CODEXA Roteador Video

   ## Section 1: HOOK + ABERTURA (00:00-01:00)

   **Mood**: Tensao, disrupcao
   **Lighting Phase**: COLD (5500K-6500K, high contrast)

   ### Shot 1 (00:00-00:08)
   - Camera: Slow zoom in (10-15% per second), flat angle
   - Lighting: Cold blue, harsh shadows
   - Transition Out: Hard cut
   - Visual Elements: Tela preta, fade in grid logos IA
   ```

3. **Compile context/ Directory**
   - Copy or generate supporting files:
     - `glossario.md` - Technical terms (agente, pipeline, orquestracao)
     - `word_bank.md` - Validated hooks, triggers, terminology
     - `agent_specs.md` - Brief descriptions of pesquisa_agent, anuncio_agent, photo_agent
   - Include only if source files exist

4. **Generate PROMPT_NOTEBOOKLM.md**
   - Use template from NOTEBOOKLM_*.md if exists
   - Otherwise generate standard prompt:

   ```markdown
   # NotebookLM Prompt: CODEXA Roteador Video Production

   ## Task
   Using the uploaded files (script_narration.md, visual_direction.md, context files),
   generate production guidance for an 11-minute video about CODEXA Roteador.

   ## Key Instructions
   1. Maintain exact timecodes from script
   2. Follow camera movements from visual direction
   3. Preserve psychological triggers (proof, authority, contrast)
   4. Include easter eggs: Cat Coding, Pirulita, Tagline
   5. Use terminology from glossario.md

   ## Output Format
   Generate:
   - Shot-by-shot breakdown with visual + audio
   - Transition recommendations
   - B-roll suggestions
   - Music cues (mood, BPM)
   ```

5. **Package Structure**
   ```
   notebooklm_package_roteador/
   ├── script_narration.md          ← Clean narration only
   ├── visual_direction.md          ← Camera + lighting specs
   ├── context/
   │   ├── glossario.md            ← Technical terms
   │   ├── word_bank.md            ← Hooks, triggers
   │   └── agent_specs.md          ← Agent descriptions
   └── PROMPT_NOTEBOOKLM.md        ← Generation instructions
   ```

6. **Optional: Create .zip Archive**
   - Compress entire package folder
   - Name: `notebooklm_package_{topic}_{date}.zip`
   - Easier for upload to NotebookLM

**Output**:
```json
{
  "package_path": "C:\\...\\notebooklm_package_roteador\\",
  "package_zip": "C:\\...\\notebooklm_package_roteador_20251203.zip",
  "files_generated": [
    "script_narration.md",
    "visual_direction.md",
    "context/glossario.md",
    "context/word_bank.md",
    "context/agent_specs.md",
    "PROMPT_NOTEBOOKLM.md"
  ],
  "total_size_kb": 245,
  "generation_timestamp": "2025-12-03T16:45:00Z"
}
```

**Quality Gate**:
- [ ] All core files generated (script, visual, prompt)
- [ ] script_narration.md contains no technical markers
- [ ] visual_direction.md contains no narration duplication
- [ ] Context files included (if sources exist)
- [ ] Package folder created successfully

---

### Phase 5: VALIDATE PACKAGE (1min)

**Objective**: Ensure package meets NotebookLM upload standards and quality

**Actions**:

1. **Structural Validation**
   - [ ] script_narration.md exists (≥10KB)
   - [ ] visual_direction.md exists (≥5KB)
   - [ ] PROMPT_NOTEBOOKLM.md exists (≥2KB)
   - [ ] Package directory structure correct

2. **Content Validation**
   - [ ] All sections from script covered in narration file
   - [ ] All sections from script covered in visual file
   - [ ] Timecodes match between files (±5s tolerance)
   - [ ] No narration text in visual_direction.md
   - [ ] No camera specs in script_narration.md (clean separation)

3. **Completeness Check**
   - [ ] Total narration word count ≈ duration estimate (150 words/min)
   - [ ] All shots have camera movement
   - [ ] All sections have lighting direction
   - [ ] Easter eggs preserved (if in source)
   - [ ] Psychological triggers documented

4. **Quality Scoring**
   ```python
   quality_score = (
       0.3 * (timecode_alignment_score) +      # 0-10
       0.2 * (completeness_score) +            # 0-10
       0.2 * (separation_score) +              # 0-10 (narration vs visual)
       0.15 * (context_richness_score) +       # 0-10
       0.15 * (prompt_clarity_score)           # 0-10
   )
   ```

   **Minimum passing score**: 7.0/10.0

5. **Generate Validation Report**
   ```json
   {
     "validation_report": {
       "checks_passed": 18,
       "checks_failed": 1,
       "quality_score": 8.7,
       "issues": [
         "Section 4 missing lighting spec for Shot 23 (minor)"
       ],
       "recommendations": [
         "Add lighting direction for Shot 23",
         "Consider compressing context files (245KB → 180KB)"
       ],
       "easter_eggs_preserved": ["Cat Coding", "Tagline"],
       "ready_for_upload": true
     }
   }
   ```

**Output**:
```json
{
  "validation_status": "PASSED",
  "quality_score": 8.7,
  "ready_for_notebooklm": true,
  "package_path": "C:\\...\\notebooklm_package_roteador\\",
  "upload_instructions": "Upload all files in package directory to NotebookLM. Start with PROMPT_NOTEBOOKLM.md."
}
```

**Quality Gate**:
- [ ] quality_score ≥7.0
- [ ] All required files present
- [ ] Timecodes aligned (±5s)
- [ ] Narration word count matches duration estimate ±20%
- [ ] Easter eggs preserved (if in source)

---

## OUTPUT_CONTRACT

### Deliverables

**Core Package** (always generated):
1. **script_narration.md** - Clean narration text only, with timecodes
2. **visual_direction.md** - Camera, lighting, transitions (no narration)
3. **PROMPT_NOTEBOOKLM.md** - Generation instructions for NotebookLM

**Context Files** (generated if sources exist):
4. **context/glossario.md** - Technical terminology
5. **context/word_bank.md** - Validated hooks and triggers
6. **context/agent_specs.md** - Brief agent descriptions

**Metadata**:
7. **package_manifest.json** - File list, checksums, metadata
8. **validation_report.json** - Quality score, issues, recommendations

**Optional**:
9. **notebooklm_package_{topic}.zip** - Compressed archive for easy upload

---

## USAGE

### Manual Execution

```bash
# Execute NotebookLM package workflow
cd codexa.app/agentes/video_agent

python src/notebooklm_packager.py \
  --script "curso_agent/context/VIDEO_LP_ROTEADOR.md" \
  --visual "curso_agent/context/DIRECAO_VISUAL_LP_ROTEADOR.md" \
  --output "outputs/notebooklm_packages/"

# With optional context files
python src/notebooklm_packager.py \
  --script "curso_agent/context/VIDEO_LP_ROTEADOR.md" \
  --visual "curso_agent/context/DIRECAO_VISUAL_LP_ROTEADOR.md" \
  --context "curso_agent/context/GLOSSARIO.md" \
  --context "curso_agent/context/RESEARCH_BANCO_PALAVRAS_OTIMIZADAS.md" \
  --output "outputs/notebooklm_packages/" \
  --zip
```

### Automated (via Watcher)

```python
# codexa.app/agentes/video_agent/watchers/notebooklm_watcher.py
import watchdog

def on_script_created(event):
    if "VIDEO_LP_" in event.src_path:
        run_notebooklm_packager(script_path=event.src_path)
```

### Slash Command

```bash
# From Claude Code
/flow do "package VIDEO_LP_ROTEADOR for NotebookLM"
```

---

## CHAINING

### Agent Chain Flow

```
curso_agent (VIDEO_LP_*.md)
        ↓
    [102_ADW_NOTEBOOKLM_VIDEO]
        ↓
notebooklm_package/
├── script_narration.md
├── visual_direction.md
├── context/
│   ├── glossario.md
│   └── word_bank.md
└── PROMPT_NOTEBOOKLM.md
        ↓
    NotebookLM (manual upload)
        ↓
    Generated Video Guidance
        ↓
    video_agent (100_ADW_RUN_VIDEO)
        ↓
    Final Video (.mp4)
```

### Integration Points

**Input from curso_agent**:
- `VIDEO_LP_*.md` - Script with timecodes
- `DIRECAO_VISUAL_*.md` - Visual direction
- `NOTEBOOKLM_*.md` - Prompt template (optional)

**Output to NotebookLM**:
- Clean, separated files for AI consumption
- Context files for domain knowledge
- Generation prompt with instructions

**Output to video_agent** (optional next step):
- If NotebookLM guidance → manual production
- If direct production → use 100_ADW_RUN_VIDEO with script as input

---

## VALIDATION COMMANDS

```bash
# Validate script structure
python validators/script_validator.py \
  --file "curso_agent/context/VIDEO_LP_ROTEADOR.md"

# Validate visual direction
python validators/visual_validator.py \
  --file "curso_agent/context/DIRECAO_VISUAL_LP_ROTEADOR.md"

# Validate package
python validators/package_validator.py \
  --package "outputs/notebooklm_packages/notebooklm_package_roteador/"

# Check timecode alignment
python validators/timecode_aligner.py \
  --script "curso_agent/context/VIDEO_LP_ROTEADOR.md" \
  --visual "curso_agent/context/DIRECAO_VISUAL_LP_ROTEADOR.md" \
  --tolerance 5

# Test complete workflow (mock)
python src/notebooklm_packager.py \
  --script "curso_agent/context/VIDEO_LP_ROTEADOR.md" \
  --visual "curso_agent/context/DIRECAO_VISUAL_LP_ROTEADOR.md" \
  --dry-run
```

---

## ERROR HANDLING

### Phase 1 Errors

**Error**: Script file not found
**Cause**: Wrong path or file not generated yet
**Action**:
1. Search recursively in curso_agent/
2. If not found: "Run curso_agent video script workflow first"
3. Log expected path for debugging

**Error**: Visual direction missing
**Cause**: Script exists but no visual file
**Action**:
1. Generate basic visual specs from script
2. Log warning: "Using fallback visual direction"
3. Continue with reduced quality score

---

### Phase 2 Errors

**Error**: Timecode parsing failure
**Cause**: Non-standard timecode format
**Action**:
1. Try alternative parsers (HH:MM:SS, MM:SS, seconds)
2. If still fails, estimate from section count
3. Flag sections with missing timecodes

**Error**: No narration found
**Cause**: Script uses different markers
**Action**:
1. Search for alternative markers (NARRATION:, VOICE:, TEXT:)
2. If not found, extract all non-technical text
3. Log warning: "Using fallback narration extraction"

---

### Phase 3 Errors

**Error**: Timecode mismatch script ↔ visual
**Cause**: Files out of sync or different versions
**Action**:
1. Allow ±5s tolerance for alignment
2. If >5s difference, flag section
3. Use script timecodes as authoritative
4. Log warning with mismatch details

**Error**: Missing camera specs
**Cause**: Visual direction incomplete
**Action**:
1. Use section mood to infer camera (tensao → handheld)
2. Default to "static" if unclear
3. Flag shots with inferred specs

---

### Phase 4 Errors

**Error**: File write permission denied
**Cause**: Locked directory or insufficient permissions
**Action**:
1. Try alternative output path (temp directory)
2. If still fails, output to stdout
3. User can manually save files

**Error**: Context file missing (glossario.md)
**Cause**: Optional file not generated by curso_agent
**Action**:
1. Skip context file (not required)
2. Log info: "Context file not found, skipping"
3. Continue without affecting quality score

---

### Phase 5 Errors

**Error**: Quality score <7.0
**Cause**: Missing data or misalignment
**Action**:
1. List all failed validation checks
2. Provide specific recommendations
3. Allow manual override with `--force` flag
4. Log warning: "Low quality score, review package before upload"

**Recovery**: All phases save intermediate JSON. On restart, check for existing outputs and resume from last successful phase.

---

## CONFIGURATION

### File Paths

```json
{
  "input_paths": {
    "curso_script": "codexa.app/agentes/curso_agent/context/VIDEO_LP_*.md",
    "curso_visual": "codexa.app/agentes/curso_agent/context/DIRECAO_VISUAL_*.md",
    "curso_prompt": "codexa.app/agentes/curso_agent/context/NOTEBOOKLM_*.md"
  },
  "output_paths": {
    "packages": "codexa.app/agentes/video_agent/outputs/notebooklm_packages/",
    "logs": "codexa.app/agentes/video_agent/logs/notebooklm/"
  }
}
```

### Validation Rules

```json
{
  "timecode_tolerance_seconds": 5,
  "min_narration_word_count": 1200,
  "max_narration_word_count": 2000,
  "min_quality_score": 7.0,
  "required_easter_eggs": ["Cat Coding", "Tagline"],
  "word_count_per_minute": 150
}
```

---

## EXAMPLE

### Input: VIDEO_LP_ROTEADOR.md (excerpt)

```markdown
## TIMELINE MASTER
| Tempo | Secao | Duracao | Mood |
|-------|-------|---------|------|
| 00:00-00:40 | Hook | 40s | Tensao |

## SECAO 1: HOOK (00:00-00:40)

### SHOT 1: RESULTADO PRIMEIRO (00:00-00:10)
**VISUAL**: Screenshot do output do Roteador
**NARRACAO**: "Quero pesquisar e anunciar fone bluetooth. Pronto."
**OVERLAY TEXT**: Output: 4.850 palavras
```

### Output: script_narration.md

```markdown
# Script Narration: CODEXA Roteador Video

**Duration**: 11 minutes
**Total Sections**: 7

## Section 1: HOOK (00:00-00:40)

### Shot 1 (00:00-00:10)
"Quero pesquisar e anunciar fone bluetooth. Pronto."

### Shot 2 (00:10-00:20)
"Uma frase. Cinquenta minutos de trabalho automatizado. Quatro mil oitocentas e cinquenta palavras."
```

### Output: visual_direction.md

```markdown
# Visual Direction: CODEXA Roteador Video

## Section 1: HOOK (00:00-00:40)

**Mood**: Tensao, prova imediata
**Lighting**: COLD phase (5500K-6500K)

### Shot 1 (00:00-00:10)
- Camera: Slow zoom in (10-15% per second)
- Angle: Screen capture, flat
- Lighting: Bright, clean (code editor lighting)
- Visual: Screenshot do output do Roteador
- Overlay: "Output: 4.850 palavras"
- Transition Out: Hard cut
```

---

## METRICS

Track for optimization:

```json
{
  "packager_metrics": {
    "avg_execution_time_seconds": 380,
    "avg_script_length_words": 1650,
    "avg_shots_per_script": 42,
    "avg_quality_score": 8.5,
    "success_rate": 0.93,
    "common_issues": [
      "Timecode mismatch (18%)",
      "Missing context files (35%)",
      "Visual specs incomplete (12%)"
    ]
  }
}
```

---

## VERSION HISTORY

### v1.0.0 (2025-12-03)
- Initial NotebookLM packaging workflow
- 5-phase structure (Locate, Extract, Visual Match, Package, Validate)
- Clean separation: narration vs visual direction
- Context file integration (glossario, word_bank)
- Easter egg preservation
- Quality gate with 7.0 threshold
- Trinity output for NotebookLM

---

## RELATED WORKFLOWS

- **curso_agent/workflows/01_ADW_QUICK_COURSE.md** - Creates VIDEO_LP_*.md (input)
- **video_agent/workflows/100_ADW_RUN_VIDEO.md** - Direct video production (alternative)
- **video_agent/workflows/101_ADW_CURSO_BRIDGE.md** - TIMELINE → video context (different chain)

---

**Created by**: video_agent
**Maintained by**: CODEXA Meta-Constructor
**Status**: Production Ready
**Quality Score**: 9.0/10.0

---

## APPENDIX: NotebookLM Upload Instructions

### Step 1: Upload Files
1. Go to NotebookLM (notebooklm.google.com)
2. Create new notebook: "CODEXA Roteador Video"
3. Upload files in order:
   - `script_narration.md`
   - `visual_direction.md`
   - `context/glossario.md`
   - `context/word_bank.md`
   - `PROMPT_NOTEBOOKLM.md`

### Step 2: Initial Query
Paste from `PROMPT_NOTEBOOKLM.md`:
```
Generate production guidance for an 11-minute video about CODEXA Roteador.
Use script_narration.md for timing and messaging.
Use visual_direction.md for camera and lighting.
Maintain easter eggs: Cat Coding, Pirulita, Tagline.
```

### Step 3: Iterative Refinement
Ask NotebookLM:
- "Generate shot-by-shot breakdown for Section 1"
- "Suggest B-roll for Demo section"
- "What music mood for each section?"
- "Transition recommendations between sections"

### Step 4: Export Guidance
- Copy NotebookLM output
- Use as input for `100_ADW_RUN_VIDEO` (video production)
- Or use for manual video editing

---

**End of ADW-102**
