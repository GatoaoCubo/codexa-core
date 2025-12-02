# ADW-03: Sales Package Generation
## 20-30 Minute Workflow

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "ADW-03",
  "workflow_name": "Sales Package Generation",
  "version": "2.1.0",
  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "course_creation"},
    {"phase_id": "phase_1_plan", "phase_name": "Plan", "duration": "3min"},
    {"phase_id": "phase_2_build", "phase_name": "Build", "duration": "10-15min"},
    {"phase_id": "phase_3_test", "phase_name": "Test", "duration": "5min"},
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

### Phase 1: PLAN (3 min)
**Input Required:**
- Course name (complete)
- All modules generated (01-06)
- Target price point

**Prerequisites Check:**
```bash
# Verify video scripts exist
ls outputs/video_scripts/*.md | wc -l  # Expect: 6

# Verify workbooks exist
ls outputs/workbooks/*.md | wc -l  # Expect: 6
```

**$arguments:**
```
$course_name = "[COURSE_NAME]"
$module_count = 6
$price_point = "[PRICE]"
```

### Phase 2: BUILD (10-15 min)
**Step 2.1: Generate Sales Collateral**
```bash
python builders/04_sales_collateral_builder.py \
  --course "$course_name" \
  --verbose
```

**Output:** `outputs/sales/[name]_sales.md`
- Landing page structure
- 6-email sequence
- Ad copy (Facebook, Google, LinkedIn)

**Step 2.2: Generate Hotmart Package**
```bash
python builders/05_hotmart_package_builder.py \
  --input outputs/ \
  --verbose
```

**Output:** `outputs/hotmart_package/`
- HOTMART_MANIFEST.json
- README_DEPLOY.md

**$arguments chain:**
```
$course_name → $sales_path → $manifest_path
```

### Phase 3: TEST (5 min)
**Validation Suite:**
```bash
# Brand Voice (sales)
python validators/02_brand_voice_validator.py \
  --file outputs/sales/*_sales.md

# Hotmart Compliance
python validators/05_hotmart_compliance_validator.py \
  --file outputs/hotmart_package/HOTMART_MANIFEST.json
```

**Required Scores:**
- Brand Voice: >= 7.0/10.0
- Hotmart Compliance: >= 8.0/10.0 (stricter!)

### Phase 4: REVIEW (5 min)
**Sales Collateral Checklist:**
- [ ] Landing page: Hero, Problem, Solution, Proof, FAQ, CTA?
- [ ] Email sequence: 6 emails (Awareness → Action → Engagement)?
- [ ] Ad copy: 3 platforms (Facebook, Google, LinkedIn)?
- [ ] Brand voice: Seed words presentes?
- [ ] No hype: Sem "revolucionário", "mágico", "único"?

**Hotmart Package Checklist:**
- [ ] Video specs: MP4, H.264, 1080p?
- [ ] DRM: Anti-download, watermark configurado?
- [ ] LGPD: Política de privacidade?
- [ ] Garantia: 7-30 dias explícita?
- [ ] Gotejamento: Drip schedule definido?

### Phase 5: DOCUMENT (2 min)
**Final tracking:**
```bash
# Log completion
echo "$(date): Sales package completed for $course_name" >> outputs/workflow_log.txt
echo "  - Sales: outputs/sales/*_sales.md" >> outputs/workflow_log.txt
echo "  - Manifest: outputs/hotmart_package/HOTMART_MANIFEST.json" >> outputs/workflow_log.txt
echo "  - Scores: Voice=[X], Compliance=[X]" >> outputs/workflow_log.txt
```

---
## Full $arguments Chain
```
$course_name
  → $module_count (verified)
  → $sales_path
  → $manifest_path
  → $voice_score
  → $compliance_score
```

## Brand Voice Reference
**Seed Words (USE):**
- Meta-Construção
- Destilação de Conhecimento
- Cérebro Plugável

**Tone:**
- Disruptivo-sofisticado

**Attack (Against):**
- Banalização
- Lock-in
- Commodity knowledge

**Avoid (NEVER USE):**
- Revolucionário
- Mágico
- Único no mercado

## Hotmart Technical Specs
| Spec | Requirement |
|------|-------------|
| Video | MP4, H.264 codec |
| Resolution | 1080p (720p min) |
| DRM | Hotmart Player built-in |
| LGPD | Privacy policy required |
| Garantia | 7-30 days explicit |

## Success Criteria
- Brand Voice >= 7.0/10.0
- Hotmart Compliance >= 8.0/10.0
- All deliverables generated
- Ready for Hotmart upload

## Failure Recovery
If Brand Voice fails:
1. Check hype words in copy
2. Verify seed words present
3. Adjust tone (less hype, more substance)

If Compliance fails:
1. Check video specs in manifest
2. Verify LGPD references
3. Ensure garantia is explicit

---
**Version**: 2.1.0 | **Duration**: 20-30 min | **Complexity**: Medium-High
