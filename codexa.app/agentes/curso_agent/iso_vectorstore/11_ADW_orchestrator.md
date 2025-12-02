<!-- iso_vectorstore -->
<!--
  Source: 01_ADW_QUICK_COURSE.md
  Agent: curso_agent
  Synced: 2025-11-30
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# ADW-01: Quick Course Outline
## 5-10 Minute Workflow

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
**Version**: 2.0.0 | **Duration**: 5-10 min | **Complexity**: Low
