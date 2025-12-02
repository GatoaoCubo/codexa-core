# ADW-01: Quick Course Outline
## 5-10 Minute Workflow

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "ADW-01",
  "workflow_name": "Quick Course Outline",
  "version": "2.1.0",
  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "course_creation"},
    {"phase_id": "phase_1_plan", "phase_name": "Plan", "duration": "1-2min"},
    {"phase_id": "phase_2_build", "phase_name": "Build", "duration": "2-3min"},
    {"phase_id": "phase_3_test", "phase_name": "Test", "duration": "1min"},
    {"phase_id": "phase_4_review", "phase_name": "Review", "duration": "1-2min"},
    {"phase_id": "phase_5_document", "phase_name": "Document", "duration": "1min"}
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

### Phase 1: PLAN (1-2 min)
**Input Required:**
- Course topic/theme
- Target audience (Layer 1/2/3)
- Estimated duration (hours)

**Actions:**
```bash
# Verify context files exist
ls context/00_INDICE_CURSO_CODEXA.md
```

### Phase 2: BUILD (2-3 min)
**Execute:**
```bash
python builders/01_course_outline_builder.py \
  --topic "[TOPIC]" \
  --audience "[AUDIENCE]" \
  --duration "[HOURS]" \
  --verbose
```

**Output:** `outputs/outlines/[TOPIC]_outline.md`

### Phase 3: TEST (1 min)
**Quick Validation:**
```bash
# Check structure
head -50 outputs/outlines/*_outline.md

# Verify module count (expect 4-6)
grep -c "## Módulo" outputs/outlines/*_outline.md
```

### Phase 4: REVIEW (1-2 min)
**Checklist:**
- [ ] Módulos sequenciais (Layer progression)?
- [ ] Cada módulo tem objetivo claro?
- [ ] [OPEN_VARIABLES] presentes?
- [ ] Timing realista (15-30min/módulo)?

### Phase 5: DOCUMENT (1 min)
**Log result:**
```bash
echo "$(date): Quick outline generated for [TOPIC]" >> outputs/workflow_log.txt
```

---
## $arguments Chain
```
$topic → $audience → $duration → $outline_path
```

## Success Criteria
- Outline generated in <10 min
- 4-6 modules defined
- Clear progression Layer 1 → 2 → 3

---
**Version**: 2.1.0 | **Duration**: 6-12 min | **Complexity**: Low
