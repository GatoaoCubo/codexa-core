# Validation Checklist | Hotmart Course Builder Agent

## 📋 PRE-COMMIT VALIDATION

Execute todos os itens antes de fazer commit do agente.

---

## ✅ PHASE 1: Automated Validators

### 1.1 README Validation
```bash
uv run codexa.app/agentes/codexa-agent/validators/09_readme_validator.py \
  agents/hotmart_course_builder_agent/artifacts/README.md
```

**Expected Output**:
- ✅ All required sections present (Overview, Architecture, Usage, Examples)
- ✅ No broken links
- ✅ Proper markdown formatting
- ✅ Version number present
- ✅ Quality score ≥0.85

**Status**: [ ] Pass / [ ] Fail / [ ] Not Run

---

### 1.2 Path Consistency Validation
```bash
uv run codexa.app/agentes/codexa-agent/validators/16_path_consistency_validator.py \
  agents/hotmart_course_builder_agent/
```

**Expected Output**:
- ✅ All file references are valid
- ✅ No broken relative paths
- ✅ Directory structure matches documentation

**Status**: [ ] Pass / [ ] Fail / [ ] Not Run

---

### 1.3 HOP/TAC-7 Validation (if applicable)
```bash
uv run codexa.app/agentes/codexa-agent/validators/07_hop_sync_validator.py \
  agents/hotmart_course_builder_agent/artifacts/*.md
```

**Expected Output**:
- ✅ TAC-7 structure followed (if HOPs present)
- ✅ [OPEN_VARIABLES] properly marked
- ✅ No unintentional [VARIABLES] left

**Status**: [ ] Pass / [ ] Fail / [ ] N/A (no HOPs)

---

## ✅ PHASE 2: Manual Content Review

### 2.1 MASTER_INSTRUCTIONS.md Quality

**Checklist**:
- [ ] **Purpose clearly stated** (first 3 paragraphs)
- [ ] **Input context defined** (what docs/data agent needs)
- [ ] **Output formats specified** (structure + examples)
- [ ] **Workflow steps numbered** (clear sequence)
- [ ] **[OPEN_VARIABLES] strategy explained** (when/how to use)
- [ ] **Brand voice section present** (seed words, tone, examples)
- [ ] **Quality gates defined** (validation criteria)
- [ ] **Constraints listed** (what NOT to do)
- [ ] **Examples included** (at least 1 complete example)
- [ ] **Word count reasonable** (2,000-10,000 words - not too short/long)

**Quality Score**: ___/10

---

### 2.2 AGENT_CONFIGURATION.json Completeness

**Checklist**:
- [ ] **Model specified** (gpt-4o, claude-sonnet-4, etc)
- [ ] **Temperature set** (0.7 recommended for creative content)
- [ ] **Max tokens appropriate** (16,000 for long-form content)
- [ ] **Tools enabled** (code_interpreter, file_search if needed)
- [ ] **Vector store configured** (if using context files)
- [ ] **Capabilities list accurate** (matches what agent actually does)
- [ ] **Constraints documented** (safety guardrails)
- [ ] **Input requirements clear** (what user must provide)
- [ ] **Output formats specified** (naming conventions, structure)
- [ ] **Metadata complete** (version, created date, status)

**Quality Score**: ___/10

---

### 2.3 README.md Clarity

**Checklist**:
- [ ] **Overview answers "what/why/how"** (in first 100 words)
- [ ] **Quick start is QUICK** (5 steps or less)
- [ ] **Examples are copy-paste ready** (no placeholders like "your-api-key")
- [ ] **Target audience clear** (who should use this agent)
- [ ] **Success criteria measurable** (not vague "improves quality")
- [ ] **Limitations honest** (what agent CAN'T do)
- [ ] **Support links present** (where to get help)
- [ ] **License specified** (ownership, usage rights)
- [ ] **Version number visible** (semantic versioning)
- [ ] **Screenshots/diagrams described** (if missing, note as TODO)

**Quality Score**: ___/10

---

### 2.4 DEPLOYMENT_GUIDE.md Usability

**Checklist**:
- [ ] **Time estimates realistic** (tested or well-reasoned)
- [ ] **Prerequisites complete** (nothing assumed)
- [ ] **Steps numbered and sequential** (can't skip or reorder)
- [ ] **Code blocks runnable** (syntax correct, paths valid)
- [ ] **Troubleshooting section present** (top 3-5 issues)
- [ ] **Multiple deployment paths** (at least 2 options)
- [ ] **Testing section included** (how to verify it works)
- [ ] **Configuration tuning guide** (how to adjust for use cases)
- [ ] **Cost estimates provided** (API usage, tokens)
- [ ] **Success criteria clear** ("you've deployed successfully when...")

**Quality Score**: ___/10

---

## ✅ PHASE 3: Functional Testing

### 3.1 Agent Execution Test (Basic)

**Test Prompt**:
```
"Create a 3-module course outline for CODEXA Layer 1 basics,
 target 10 hours total, video scripts priority"
```

**Expected Behavior**:
1. Agent asks clarifying questions (optional)
2. Generates outline with:
   - Module titles
   - Learning objectives
   - Duration estimates
   - Layer mapping (all Layer 1)
3. Total duration ~10 hours
4. Asks for approval before generating detailed content

**Actual Result**:
[Paste agent response here]

**Status**: [ ] Pass / [ ] Fail / [ ] Not Tested

---

### 3.2 [OPEN_VARIABLES] Preservation Test

**Test Prompt**:
```
"Generate a video script for Module 1.1 - Introduction to CODEXA Layers.
 Include sections for different tech stacks and product examples."
```

**Expected Behavior**:
Script contains [OPEN_VARIABLES] like:
- `[SEU_CRM]` or `[PLATAFORMA_ECOMMERCE]`
- `[CATEGORIA_PRODUTO]` or `[SEU_NICHO]`
- `[OPEN_VARIABLE: custom instruction]`

**Count [OPEN_VARIABLES] in output**: ___

**Status**: [ ] Pass (≥2 variables) / [ ] Fail (<2) / [ ] Not Tested

---

### 3.3 Brand Voice Compliance Test

**Test Prompt**:
```
"Generate sales copy for the course landing page"
```

**Expected Behavior**:
- Uses seed words: "Meta-Construção", "Destilação de Conhecimento", "Cérebro Plugável"
- Tone: Disruptivo-sofisticado (technical, not hype)
- Avoids: "revolucionário", "mágico", "único no mercado"
- Attacks: banalização, lock-in, commodity knowledge

**Manual Review**:
- [ ] Seed words present (≥3 mentions)
- [ ] Tone matches CODEXA brand (90% technical, 80% anti-establishment)
- [ ] No hype words detected
- [ ] Positioning clear (Layer 3 vs Layer 1)

**Status**: [ ] Pass / [ ] Fail / [ ] Not Tested

---

### 3.4 Quality Self-Validation Test

**Test Prompt**:
```
"Generate a video script, then run quality validation on it"
```

**Expected Behavior**:
Agent self-validates and reports:
- [ ] Hook timing ≤90s?
- [ ] Learning objectives measurable?
- [ ] Demonstration shows real CODEXA?
- [ ] Timing marked and feasible?
- [ ] Brand voice aligned?
- [ ] [OPEN_VARIABLES] count ≥2?

**Status**: [ ] Pass (agent self-validates) / [ ] Fail / [ ] Not Tested

---

### 3.5 Error Handling Test

**Test Prompt (Intentional Error)**:
```
"Generate a course about [INVALID_TOPIC]"
```

**Expected Behavior**:
- Agent recognizes invalid input
- Asks for clarification or refuses gracefully
- Does NOT generate generic/off-topic content

**Status**: [ ] Pass / [ ] Fail / [ ] Not Tested

---

## ✅ PHASE 4: Integration Testing

### 4.1 Registry Integration (if registering in CODEXA)

**Action**: Add agent to `51_AGENT_REGISTRY.json`

**Validation**:
```bash
uv run codexa.app/agentes/codexa-agent/validators/10_taxonomy_validator.py \
  codexa.app/agentes/51_AGENT_REGISTRY.json
```

**Expected Output**:
- ✅ JSON valid
- ✅ Agent entry complete (name, specialty, version, status)
- ✅ No duplicate names
- ✅ Dependencies listed (if any)

**Status**: [ ] Pass / [ ] Fail / [ ] N/A (not registering)

---

### 4.2 Slash Command Creation (if creating /build_course)

**Action**: Create `.claude/commands/build_course.md`

**Test**:
```bash
# In terminal with Claude Code
/build_course
```

**Expected Behavior**:
- Command loads successfully
- Prompts user for course parameters
- Executes hotmart_course_builder_agent

**Status**: [ ] Pass / [ ] Fail / [ ] N/A (no command)

---

### 4.3 Context File Loading (if using vector store)

**Action**: Upload to vector store:
- `codexa_market_research.md`
- `codexa_product_announcement.md`
- `codexa_brand_strategy_v2.md`

**Test Prompt**:
```
"What are the 6 CODEXA core agents?"
```

**Expected Answer**:
Lists correctly: anuncio_agent, pesquisa_agent, marca_agent, photo_agent, mentor_agent, codexa_agent

**Status**: [ ] Pass / [ ] Fail / [ ] N/A (no context files)

---

## ✅ PHASE 5: Documentation Sync

### 5.1 Doc Sync Validation (CODEXA system)

**Action**:
```bash
uv run codexa.app/agentes/codexa-agent/validators/12_doc_sync_validator.py \
  --agent hotmart_course_builder_agent
```

**Expected Output**:
- ✅ All required docs present (README, INSTRUCTIONS, SETUP if needed)
- ✅ Version numbers consistent across files
- ✅ No [VARIABLES] left unintentionally
- ✅ Quality score ≥0.85

**Status**: [ ] Pass / [ ] Fail / [ ] Not Run

---

## 📊 OVERALL QUALITY SCORE

### Calculation:

| Phase | Weight | Your Score | Weighted Score |
|-------|--------|------------|----------------|
| Automated Validators | 20% | ___/10 | ___ |
| Manual Content Review | 30% | ___/10 | ___ |
| Functional Testing | 30% | ___/10 | ___ |
| Integration Testing | 10% | ___/10 | ___ |
| Documentation Sync | 10% | ___/10 | ___ |
| **TOTAL** | **100%** | **___/10** | **___** |

### Pass/Fail Threshold:
- ✅ **PASS**: Overall score ≥7.0/10 (Ready for commit)
- ⚠️ **CONDITIONAL**: 5.0-6.9/10 (Fix critical issues, then commit)
- ❌ **FAIL**: <5.0/10 (Major rework needed)

---

## 🚀 READY TO COMMIT?

### Pre-Commit Checklist (Final):
- [ ] All automated validators PASS
- [ ] Manual content review ≥7.0/10
- [ ] At least 3/5 functional tests PASS
- [ ] Integration tests relevant to deployment path PASS
- [ ] Documentation sync PASS (if using CODEXA system)
- [ ] Overall quality score ≥7.0/10
- [ ] README.md has clear "What/Why/How"
- [ ] DEPLOYMENT_GUIDE.md has ≥2 deployment paths
- [ ] No sensitive data in files (API keys, credentials)
- [ ] License and ownership clear

### Git Commit Message (Suggested):
```bash
git add agents/hotmart_course_builder_agent/
git commit -m "feat(agents): Add Hotmart Course Builder Agent v1.0.0

- Hybrid intelligent agent for CODEXA course development
- Progressive pedagogy (Layer 1→2→3)
- Multi-format outputs (scripts, workbooks, exercises, sales)
- Strategic [OPEN_VARIABLES] for customization
- Brand voice compliance (disruptivo-sofisticado)
- Quality score: [YOUR_SCORE]/10

Artifacts: MASTER_INSTRUCTIONS (39KB), CONFIG (13KB), README (17KB), DEPLOYMENT_GUIDE (13KB)
Validated: All automated validators PASS"
```

---

## 📝 VALIDATION LOG

**Date**: _______________
**Validator**: _______________
**Agent Version**: 1.0.0
**Overall Score**: ___/10
**Status**: [ ] APPROVED / [ ] CONDITIONAL / [ ] REJECTED

**Notes**:
[Add any observations, edge cases found, or improvements suggested]

---

**Checklist Version**: 1.0.0
**Last Updated**: 2025-11-20
**Maintained By**: CODEXA Quality Assurance Team
