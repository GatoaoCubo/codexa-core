# ADW_ISO_VECTORSTORE_OPTIMIZATION | Scalable Agent Package Optimization

**ID**: 104_ADW_ISO_VECTORSTORE
**Version**: 1.0.0
**Created**: 2025-11-30
**Type**: Agentic Developer Workflow
**Purpose**: Optimize any agent's iso_vectorstore for LLM deployment (file count, tokens, consistency)

---

## MODULE_METADATA

```yaml
id: 104_ADW_ISO_VECTORSTORE
version: 1.0.0
category: meta-construction
type: ADW (Agentic Developer Workflow)
execution_mode: single_agent_sequential
baseline: anuncio_agent v3.2.0 (-90% token reduction)
status: production_ready
created: 2025-11-30
```

---

## INPUT_CONTRACT

### Required Inputs
```yaml
$agent_name:
  type: string
  description: Name of agent to optimize (e.g., "pesquisa_agent")
  validation: must_exist_in_agentes_directory

$agents_directory:
  type: string
  default: "agentes/"
  description: Base directory containing all agents
```

### Optional Inputs
```yaml
$target_file_count:
  type: integer
  default: 21
  description: Maximum files in iso_vectorstore

$target_tokens:
  type: integer
  default: 15000
  description: Maximum total tokens estimate

$hop_token_limit:
  type: integer
  default: 1500
  description: Maximum tokens per HOP file

$dry_run:
  type: boolean
  default: false
  description: Simulate without writing files
```

---

## OUTPUT_CONTRACT

### Primary Outputs
```yaml
$optimized_iso_vectorstore:
  type: directory
  description: Optimized iso_vectorstore folder
  validation:
    - file_count <= $target_file_count
    - estimated_tokens <= $target_tokens
    - version_consistency == 100%

$optimization_report:
  type: object
  format: MD + JSON
  structure:
    - files_before: integer
    - files_after: integer
    - tokens_before: integer
    - tokens_after: integer
    - reduction_percent: float
    - changes_made: array
    - validation_status: PASS/FAIL
```

### Secondary Outputs
```yaml
$manifest_file: 00_MANIFEST.md
$system_instructions_file: SYSTEM_INSTRUCTIONS_AGENT_BUILDER.md
$backup_files: array of .bak files
```

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "104_ADW_ISO_VECTORSTORE",
  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "iso_optimization"},
    {"phase_id": "step_1", "phase_name": "Discovery", "duration": "2-5min"},
    {"phase_id": "step_2", "phase_name": "Scope Analysis", "duration": "2-3min"},
    {"phase_id": "step_3", "phase_name": "HOP Token Audit", "duration": "5-10min"},
    {"phase_id": "step_4", "phase_name": "Generate Manifest", "duration": "2-3min"},
    {"phase_id": "step_5", "phase_name": "Optimize HOPs", "duration": "15-30min"},
    {"phase_id": "step_6", "phase_name": "Remove Out-of-Scope", "duration": "5-10min"},
    {"phase_id": "step_7", "phase_name": "Version Sync", "duration": "5-10min"},
    {"phase_id": "step_8", "phase_name": "Generate System Instructions", "duration": "5-10min"},
    {"phase_id": "step_9", "phase_name": "Validate", "duration": "2-3min"},
    {"phase_id": "step_10", "phase_name": "Report", "duration": "2-3min"},
    {"phase_id": "step_11", "phase_name": "Production Test", "duration": "10-20min"}
  ]
}
```

---

## STEPS

## PHASE 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `iso_optimization`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

### STEP 1: DISCOVERY (Scan Current State)

**Duration**: 2-5 min

**Actions**:
1.1. Navigate to `$agents_directory/$agent_name/iso_vectorstore/`
1.2. List all files with sizes
1.3. Estimate tokens per file (chars / 4)
1.4. Categorize files:
    - Core (00-05): MANIFEST, QUICK_START, PRIME, INSTRUCTIONS, README, ARCHITECTURE
    - Config (06-10): schemas, rules, patterns
    - Execution (11-12): ADW, plans
    - HOPs (13-XX): HOP_*.md files
    - Reference (XX-XX): frameworks, quality_dimensions
1.5. Calculate totals

**Output**:
```json
{
  "agent": "$agent_name",
  "path": "agentes/$agent_name/iso_vectorstore/",
  "file_count": 30,
  "estimated_tokens": 45000,
  "files_by_category": {
    "core": ["00_MANIFEST.md", ...],
    "config": ["06_input_schema.json", ...],
    "execution": ["11_ADW_orchestrator.md", ...],
    "hops": ["13_HOP_main.md", ...],
    "reference": ["19_frameworks.md", ...]
  },
  "hop_token_audit": [
    {"file": "14_HOP_titulo.md", "tokens": 26000, "status": "BLOATED"},
    {"file": "15_HOP_keywords.md", "tokens": 800, "status": "OK"}
  ]
}
```

**Validation**:
- [ ] Directory exists
- [ ] Files readable
- [ ] Token estimates calculated

---

### STEP 2: SCOPE ANALYSIS (Identify Agent Purpose)

**Duration**: 2-3 min

**Actions**:
2.1. Read `$agent_name/PRIME.md`
2.2. Extract:
    - Agent scope (TEXT-ONLY, VISUAL, AUDIO, etc.)
    - What agent GENERATES
    - What agent DELEGATES to other agents
2.3. Identify out-of-scope files in iso_vectorstore

**Scope Patterns**:
```yaml
TEXT-ONLY:
  generates: [titulos, descricao, bullets, keywords]
  delegates: [image_prompts → photo_agent, video_scripts → video_agent]
  out_of_scope: [HOP_image_*, HOP_video_*, visual_*, audio_*]

VISUAL:
  generates: [image_prompts, photo_specs, visual_guidelines]
  delegates: [text_copy → anuncio_agent]
  out_of_scope: [HOP_text_*, copy_rules]

RESEARCH:
  generates: [research_notes, competitor_analysis, market_data]
  delegates: [ad_copy → anuncio_agent, visuals → photo_agent]
  out_of_scope: [HOP_titulo_*, HOP_descricao_*]
```

**Output**:
```json
{
  "scope": "TEXT-ONLY",
  "generates": ["titulos", "descricao", "bullets", "keywords"],
  "delegates": ["image_prompts → photo_agent", "video_scripts → video_agent"],
  "out_of_scope_files": ["18_HOP_image_prompts.md", "19_HOP_video_script.md"]
}
```

**Validation**:
- [ ] PRIME.md exists and readable
- [ ] Scope clearly identified
- [ ] Out-of-scope files listed

---

### STEP 3: HOP TOKEN AUDIT (Identify Bloat)

**Duration**: 5-10 min

**Actions**:
3.1. For each HOP_*.md file:
    - Count characters
    - Estimate tokens (chars / 4)
    - Scan for garbage patterns:
      ```regex
      # YAML blocks that don't belong
      /^---\n[\s\S]*?^---/m

      # Duplicate metadata
      /Version:.*\nVersion:/

      # Injection from other agents
      /mentor_agent|pesquisa_agent|photo_agent/

      # Empty reasoning blocks
      /<reasoning>\s*<\/reasoning>/

      # Massive example blocks
      /```[\s\S]{5000,}```/
      ```
3.2. Flag HOPs > $hop_token_limit
3.3. Identify essential vs removable content

**Output**:
```json
{
  "hops_audited": 6,
  "hops_bloated": 2,
  "bloated_details": [
    {
      "file": "14_HOP_titulo_generator.md",
      "tokens": 26000,
      "target": 800,
      "garbage_detected": ["yaml_injection", "duplicate_metadata", "massive_examples"],
      "essential_sections": ["FORMULAS", "REGRAS", "OUTPUT_FORMAT"]
    }
  ]
}
```

**Validation**:
- [ ] All HOPs audited
- [ ] Bloated HOPs identified
- [ ] Garbage patterns detected

---

### STEP 4: GENERATE MANIFEST (Create Inventory)

**Duration**: 2-3 min

**Actions**:
4.1. Use template: `codexa_agent/templates/iso_vectorstore/00_MANIFEST_TEMPLATE.md`
4.2. Fill variables:
    - AGENT_NAME, VERSION, DATE
    - SCOPE, OUTPUT_FORMAT
    - FILE_COUNT, TOKEN_ESTIMATE
    - File tables by category
4.3. Write to `iso_vectorstore/00_MANIFEST.md`

**Template Variables**:
```yaml
{AGENT_NAME}: pesquisa_agent
{VERSION}: 3.2.0
{DATE}: 2025-11-30
{SCOPE}: RESEARCH
{OUTPUT_FORMAT}: research_notes.md + competitive_analysis.json
{FILE_COUNT}: 21
{TOKEN_ESTIMATE}: ~12,000
```

**Validation**:
- [ ] All variables filled
- [ ] No [PLACEHOLDERS] remaining
- [ ] File inventory accurate

---

### STEP 5: OPTIMIZE HOPS (Remove Bloat)

**Duration**: 15-30 min (per bloated HOP)

**Actions**:
5.1. For each bloated HOP:
    - Backup original (.bak)
    - Extract essential sections:
      - PURPOSE/OBJETIVO
      - INPUT/OUTPUT contracts
      - STEPS/PASSOS (numbered)
      - RULES/REGRAS (bullet list)
      - OUTPUT FORMAT (code block)
      - VALIDATION criteria
    - Remove:
      - Duplicate content
      - YAML metadata blocks
      - Massive examples (keep 1 concise example)
      - Cross-agent injection
      - Empty sections
    - Rewrite to target token count

**HOP Structure (optimized)**:
```markdown
# HOP {NUMBER}: {NAME} | {agent_name} v{VERSION}

**Purpose**: {one-line description}
**Scope**: {scope} | **Output**: {output description}

---

## INPUT
{bullet list of inputs}

---

## RULES
{numbered or bullet list of critical rules}

---

## STEPS
1. {step 1}
2. {step 2}
...

---

## OUTPUT FORMAT
```
{example output structure}
```

---

## VALIDATION
{checklist of validation criteria}

---

**HOP**: {number} | **Agent**: {agent_name} | **Version**: {VERSION}
**Tokens**: ~{count} (optimized)
```

**Validation**:
- [ ] Token count < $hop_token_limit
- [ ] Essential instructions preserved
- [ ] No garbage remaining

---

### STEP 6: REMOVE OUT-OF-SCOPE (Clean Up)

**Duration**: 5-10 min

**Actions**:
6.1. Delete files identified as out-of-scope in STEP 2
6.2. Renumber remaining files if gaps exist:
    - 18_HOP_image_prompts.md (deleted)
    - 19_HOP_video_script.md (deleted)
    - 21_HOP_qa_validation.md → 18_HOP_qa_validation.md
6.3. Update all internal references to renamed files
6.4. Update MANIFEST with new file list

**Validation**:
- [ ] Out-of-scope files removed
- [ ] No numbering gaps
- [ ] References updated

---

### STEP 7: VERSION SYNC (Consistency)

**Duration**: 5-10 min

**Actions**:
7.1. Determine canonical version (latest or specified)
7.2. Update version in ALL files:
    - 00_MANIFEST.md
    - 01_QUICK_START.md
    - 02_PRIME.md
    - 03_INSTRUCTIONS.md
    - 04_README.md
    - 05_ARCHITECTURE.md
    - All HOPs
7.3. Update "Updated" date to current date
7.4. Update footer signatures

**Validation**:
- [ ] 100% version consistency
- [ ] All dates current
- [ ] No version mismatches

---

### STEP 8: GENERATE SYSTEM_INSTRUCTIONS (Deploy Ready)

**Duration**: 5-10 min

**Actions**:
8.1. Use template: `codexa_agent/templates/iso_vectorstore/SYSTEM_INSTRUCTIONS_TEMPLATE.md`
8.2. Fill variables from PRIME.md and MANIFEST:
    - AGENT_NAME, VERSION, SCOPE
    - GENERATES list, DELEGATES list
    - WORKFLOW steps
    - INPUT sources ({$variables})
    - QA criteria
8.3. Add execution examples
8.4. Write to `$agent_name/SYSTEM_INSTRUCTIONS_AGENT_BUILDER.md`

**8.5. VERIFY FILE REFERENCES** (Pattern 1 - Lesson Learned):
- Cross-reference ALL file names in SYSTEM_INSTRUCTIONS with actual iso_vectorstore files
- Use hybrid format: `{number}_{name}.md` (e.g., 13_HOP_main_agent.md)
- Verify DOCUMENT REFERENCE table lists ALL files (not partial)

**8.6. ADD OUTPUT FORMAT SECTION** (Pattern 2 - Lesson Learned):
- Add "REGRA ABSOLUTA: UM ÚNICO CODE BLOCK"
- Include template with triple backticks
- Add PROIBIDO list (no duplication, no text outside)

**8.7. UPDATE CONSTRAINTS** (Pattern 3 - Lesson Learned):
- ALWAYS output inside ONE code block (triple backticks)
- NEVER duplicate content (no PART 1 + PART 2)
- NEVER output text outside the code block

**8.8. UPDATE SELF-VALIDATION** (Pattern 4 - Lesson Learned):
- Add CRITICAL checks:
  - [ ] Output is ONE code block with triple backticks?
  - [ ] No text outside the code block?
  - [ ] No duplicated content?

**Validation**:
- [ ] All variables filled
- [ ] {$INPUT} variables defined
- [ ] Examples included
- [ ] File references verified
- [ ] Output format section present
- [ ] Constraints include code block rules
- [ ] Self-validation has CRITICAL checks
- [ ] Ready for copy/paste to Agent Builder

---

### STEP 9: VALIDATE (Quality Gate)

**Duration**: 2-3 min

**Actions**:
9.1. Count final files in iso_vectorstore
9.2. Estimate total tokens
9.3. Check version consistency
9.4. Verify no unfilled [VARIABLES]
9.5. Calculate optimization metrics

**Validation Checklist**:
```yaml
file_count:
  target: <= 21
  actual: {count}
  status: PASS/FAIL

token_estimate:
  target: < 15000
  actual: {estimate}
  status: PASS/FAIL

version_consistency:
  target: 100%
  actual: {percent}
  status: PASS/FAIL

manifest_present: PASS/FAIL
system_instructions_present: PASS/FAIL

hop_optimization:
  hops_audited: {count}
  hops_under_limit: {count}
  status: PASS/FAIL
```

**Overall Status**:
- PASS: All criteria met
- PASS_WITH_WARNINGS: Minor issues
- FAIL: Critical issues

---

### STEP 10: REPORT (Document Changes)

**Duration**: 2-3 min

**Actions**:
10.1. Generate optimization report (MD + JSON)
10.2. List all changes made
10.3. Calculate reduction metrics
10.4. Recommendations for future
10.5. Save to `$agent_name/specs/ISO_VECTORSTORE_OPTIMIZATION_REPORT.md`

**Report Structure**:
```markdown
# ISO_VECTORSTORE Optimization Report | {agent_name}

**Date**: {date}
**Version**: {before} → {after}
**Status**: {PASS/FAIL}

## Summary
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| Files | {n} | {n} | {-n%} |
| Tokens | {n} | {n} | {-n%} |
| HOPs optimized | - | {n} | - |

## Changes Made
{bulleted list of changes}

## Validation Results
{checklist with status}

## Recommendations
{future improvements}
```

**Validation**:
- [ ] Report generated
- [ ] All changes documented
- [ ] Metrics calculated

---

### STEP 11: PRODUCTION TEST (Optional - Pattern 8)

**Duration**: 10-20 min

**Actions**:
11.1. Deploy to ChatGPT Responses (or target LLM):
    - Create vector store with chunk 800 / overlap 200
    - Upload all iso_vectorstore files
    - Copy SYSTEM_INSTRUCTIONS to Agent Builder
11.2. Run test with sample input
11.3. Analyze log for issues:
    - Token consumption (target < 35k)
    - Code interpreter calls (target <= 5)
    - Empty reasoning blocks (target 0)
    - Output format (single code block)
    - Duplication (should be none)
11.4. Fix issues and redeploy if needed
11.5. Document production issues in LESSONS_LEARNED

**Feedback Loop**:
```
Deploy v1 → Test → Analyze Log → Fix → Deploy v2 → Verify
```

**Common Production Issues**:
- Empty reasoning items → Add "NEVER emit empty blocks"
- Excessive code interpreter → Add batching rule (<=5 calls)
- Unnecessary web search → Add "DISABLE when URL/research provided"
- Duplicated output → Enforce single code block
- Missing code fence → Add explicit template

**Validation**:
- [ ] Production test completed
- [ ] Issues documented
- [ ] Fixes applied
- [ ] Final verification passed

---

## EXECUTION

### In Claude Code Terminal

```bash
# Load context
/prime-codexa

# Execute for single agent
Execute ADW-104 (ISO_VECTORSTORE_OPTIMIZATION) for pesquisa_agent

# Reference files
- Workflow: codexa_agent/workflows/104_ADW_ISO_VECTORSTORE_OPTIMIZATION.md
- Templates: codexa_agent/templates/iso_vectorstore/
- Spec: codexa_agent/specs/ISO_VECTORSTORE_STANDARD.md
```

### Batch Execution (All Agents)

```bash
# Priority order
for agent in pesquisa_agent photo_agent mentor_agent video_agent marca_agent codexa_agent curso_agent; do
  Execute ADW-104 for $agent
  git add agentes/$agent/iso_vectorstore/
  git commit -m "feat($agent): optimize iso_vectorstore v3.2.0"
done
```

---

## CONTEXT

### Baseline Reference
- **anuncio_agent v3.2.0**: 80k → 8k tokens (-90%)
- **HOP optimization**: 26k → 800 tokens (-97%)
- **File structure**: 21 files, clean numbering

### Templates Location
```
codexa_agent/templates/iso_vectorstore/
├── 00_MANIFEST_TEMPLATE.md
├── SYSTEM_INSTRUCTIONS_TEMPLATE.md
└── OPTIMIZATION_CHECKLIST.md
```

### Related Workflows
- ADW-100: Documentation Sync
- ADW-97: New Agent Creation
- ADW-98: Consolidation

---

## SUCCESS CRITERIA

**Workflow succeeds when**:
- [ ] File count <= 21
- [ ] Token estimate < 15,000
- [ ] Version consistency 100%
- [ ] MANIFEST present and accurate
- [ ] SYSTEM_INSTRUCTIONS present and complete
- [ ] All HOPs < 1500 tokens
- [ ] No out-of-scope files
- [ ] Report generated
- [ ] File references verified (8.5)
- [ ] Output format section present (8.6)
- [ ] Constraints include code block rules (8.7)
- [ ] Self-validation has CRITICAL checks (8.8)

**Workflow fails when**:
- [ ] Cannot reduce to target file count
- [ ] Essential content lost in optimization
- [ ] Version conflicts unresolved
- [ ] SYSTEM_INSTRUCTIONS references non-existent files
- [ ] Output format allows duplication

---

## PERFORMANCE METRICS

| Agent | Files | Tokens | Est. Time |
|-------|-------|--------|-----------|
| pesquisa_agent | 30 | ~40k | 2-3h |
| photo_agent | 27 | ~35k | 2h |
| mentor_agent | 31 | ~45k | 3h |
| video_agent | 25 | ~30k | 1.5h |
| marca_agent | 32 | ~50k | 3h |
| codexa_agent | 29 | ~40k | 2.5h |
| curso_agent | 27 | ~35k | 2h |

**Total estimated**: 15-20h for all 7 agents

---

**Version**: 2.1.0 | **Status**: Production Ready
**Baseline**: anuncio_agent v3.5.0 (single code block, no duplication)
**Lessons Learned**: codexa_agent/specs/LESSONS_LEARNED_ANUNCIO_AGENT.md
**New Steps**: 8.5 (File References), 8.6 (Output Format), 8.7 (Constraints), 8.8 (Self-Validation), 11 (Production Test)
**Author**: codexa_agent + human collaboration
