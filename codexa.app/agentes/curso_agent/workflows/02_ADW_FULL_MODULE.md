# ADW-02: Full Module Generation
## 30-45 Minute Workflow

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "ADW-02",
  "name": "Full Module Generation",
  "version": "2.1.0",
  "duration": "30-45min",
  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "course_creation"},
    {"phase_id": "phase_1_plan", "phase_name": "Plan", "duration": "5min"},
    {"phase_id": "phase_2_build", "phase_name": "Build", "duration": "15-20min"},
    {"phase_id": "phase_3_test", "phase_name": "Test", "duration": "5-10min"},
    {"phase_id": "phase_4_review", "phase_name": "Review", "duration": "5min"},
    {"phase_id": "phase_5_document", "phase_name": "Document", "duration": "2min"}
  ]
}
```

---

## PHASE 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `course_creation`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

### Phase 1: PLAN (5 min)
**Input Required:**
- Module ID (01-06)
- Prerequisites validated

**Actions:**
```bash
# Verify module context exists
cat context/[MODULE_ID]_*.md | head -20

# Check dependencies
python -c "from config.paths import validate_paths; validate_paths()"
```

**$arguments:**
```
$module_id = [01-06]
$context_file = context/[MODULE_ID]_*.md
```

### Phase 2: BUILD (15-20 min)
**Step 2.1: Generate Video Script**
```bash
python builders/02_video_script_builder.py --module $module_id --verbose
```
Output: `outputs/video_scripts/[ID]_[NAME].md`

**Step 2.2: Generate Workbook**
```bash
python builders/03_workbook_builder.py --module $module_id --verbose
```
Output: `outputs/workbooks/[ID]_workbook.md`

**$arguments chain:**
```
$module_id → $script_path → $workbook_path
```

### Phase 3: TEST (5-10 min)
**Validation Suite:**
```bash
# Content Quality (script)
python validators/01_content_quality_validator.py \
  --file outputs/video_scripts/[ID]_*.md --verbose

# Brand Voice (script)
python validators/02_brand_voice_validator.py \
  --file outputs/video_scripts/[ID]_*.md

# Pedagogical (workbook)
python validators/03_pedagogical_validator.py \
  --file outputs/workbooks/[ID]_workbook.md

# Technical (both)
python validators/04_technical_validator.py \
  --file outputs/video_scripts/[ID]_*.md
```

**Required Scores:**
- Content Quality: >= 7.0/10.0
- Brand Voice: >= 7.0/10.0
- Pedagogical: >= 7.0/10.0
- Technical: >= 7.0/10.0

### Phase 4: REVIEW (5 min)
**Manual Checklist:**

**Video Script:**
- [ ] Hook em <= 90 segundos?
- [ ] [OPEN_VARIABLES] >= 2?
- [ ] Timing marks presentes?
- [ ] Exemplos brasileiros?
- [ ] Demo real CODEXA?
- [ ] Sem hype words?

**Workbook:**
- [ ] 8-15 páginas?
- [ ] Exercícios práticos?
- [ ] Perguntas de reflexão?
- [ ] Recursos adicionais?

### Phase 5: DOCUMENT (2 min)
**Update tracking:**
```bash
# Log completion
echo "$(date): Module $module_id completed" >> outputs/workflow_log.txt
echo "  - Script: outputs/video_scripts/[ID]_*.md" >> outputs/workflow_log.txt
echo "  - Workbook: outputs/workbooks/[ID]_workbook.md" >> outputs/workflow_log.txt
echo "  - Scores: Content=[X], Voice=[X], Pedagogy=[X], Tech=[X]" >> outputs/workflow_log.txt
```

---
## Full $arguments Chain
```
$module_id
  → $context_file
  → $script_path
  → $workbook_path
  → $content_score
  → $voice_score
  → $pedagogy_score
  → $tech_score
```

## Success Criteria
- All 4 validators pass (>= 7.0)
- Trinity Output complete (.md + .llm.json + .meta.json)
- Script 15-30 min estimated
- Workbook 8-15 pages

## Failure Recovery
If validation fails:
1. Check specific failed criteria
2. Re-run builder with --fix flag (if available)
3. Manual edit of [OPEN_VARIABLES]
4. Re-validate

---
**Version**: 2.0.0 | **Duration**: 30-45 min | **Complexity**: Medium
