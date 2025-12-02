# Testing Commands Reference | Hotmart Course Builder Agent

Quick reference for all available testing, validation, and review commands.

---

## 🚀 QUICK START (One Command)

```powershell
# Run ALL automated validators at once
.\agents\hotmart_course_builder_agent\validate_agent.ps1
```

**Output**: Pass/Fail report + Quality score (0-10)
**Time**: ~1-2 minutes
**Recommendation**: Run this BEFORE every commit

---

## 🔍 INDIVIDUAL VALIDATORS

### 1. README Validator
```bash
uv run codexa.app/agentes/codexa-agent/validators/09_readme_validator.py \
  agents/hotmart_course_builder_agent/artifacts/README.md
```
**Checks**: Structure, links, formatting, version, quality score
**Pass Threshold**: Quality score ≥0.85

---

### 2. Path Consistency Validator
```bash
uv run codexa.app/agentes/codexa-agent/validators/16_path_consistency_validator.py \
  agents/hotmart_course_builder_agent/
```
**Checks**: File references, broken paths, directory structure
**Pass Threshold**: All paths valid

---

### 3. HOP/TAC-7 Validator (if using HOPs)
```bash
uv run codexa.app/agentes/codexa-agent/validators/07_hop_sync_validator.py \
  agents/hotmart_course_builder_agent/artifacts/*.md
```
**Checks**: TAC-7 structure, [OPEN_VARIABLES] marking
**Pass Threshold**: TAC-7 compliant

---

### 4. Taxonomy Validator (after registering agent)
```bash
uv run codexa.app/agentes/codexa-agent/validators/10_taxonomy_validator.py \
  codexa.app/agentes/51_AGENT_REGISTRY.json
```
**Checks**: JSON valid, agent entry complete, no duplicates
**Pass Threshold**: Registry valid

---

### 5. Doc Sync Validator (CODEXA system integration)
```bash
uv run codexa.app/agentes/codexa-agent/validators/12_doc_sync_validator.py \
  --agent hotmart_course_builder_agent
```
**Checks**: All docs present, version consistency, quality score
**Pass Threshold**: Score ≥0.85

---

## 🤖 AI-POWERED REVIEW COMMANDS

### General Code/Content Review
```bash
/review agents/hotmart_course_builder_agent/
```
**What it does**: AI reviews all files for quality, best practices, issues
**Use when**: Want comprehensive feedback before commit

---

### Git-Specific Review
```bash
/git-review
```
**What it does**: Reviews git diff/changes with AI
**Use when**: Already committed to branch, want review before PR

---

### In-Loop Review (Iterative)
```bash
/in_loop_review
```
**What it does**: Quick review during active development
**Use when**: Making incremental changes, want fast feedback

---

## 🧪 MANUAL TESTING PROMPTS

Copy-paste these prompts to test the agent manually:

### Test 1: Basic Outline Generation
```
"Create a 3-module course outline for CODEXA Layer 1 basics,
 target 10 hours total, video scripts priority"
```
**Expected**: Outline with modules, objectives, durations, Layer mapping

---

### Test 2: Video Script with [OPEN_VARIABLES]
```
"Generate a video script for Module 1.1 - Introduction to CODEXA Layers.
 Include sections for different tech stacks and product examples."
```
**Expected**: Script with ≥2 [OPEN_VARIABLES] like `[SEU_CRM]`, `[CATEGORIA_PRODUTO]`

---

### Test 3: Brand Voice Compliance
```
"Generate sales copy for the course landing page"
```
**Expected**:
- Seed words: "Meta-Construção", "Destilação de Conhecimento", "Cérebro Plugável"
- Tone: Disruptivo-sofisticado (technical, not hype)
- No: "revolucionário", "mágico", "único no mercado"

---

### Test 4: Self-Validation
```
"Generate a video script, then run quality validation on it"
```
**Expected**: Agent self-validates against checklist and reports results

---

### Test 5: Error Handling
```
"Generate a course about quantum computing for toddlers"
```
**Expected**: Agent recognizes invalid/mismatched input, asks for clarification

---

## 📋 QUALITY CHECKLIST (Manual)

Use this checklist alongside automated validators:

### MASTER_INSTRUCTIONS.md
- [ ] Purpose clear (first 3 paragraphs)
- [ ] Input context defined
- [ ] Output formats specified with examples
- [ ] Workflow steps numbered
- [ ] [OPEN_VARIABLES] strategy explained
- [ ] Brand voice section present (seed words, tone)
- [ ] Quality gates defined
- [ ] Constraints listed
- [ ] At least 1 complete example
- [ ] Word count: 2,000-10,000 words

### AGENT_CONFIGURATION.json
- [ ] Model specified (gpt-4o, claude-sonnet-4, etc)
- [ ] Temperature appropriate (0.7 for creative)
- [ ] Max tokens sufficient (16,000 for long content)
- [ ] Tools enabled (code_interpreter, file_search)
- [ ] Capabilities list accurate
- [ ] Constraints documented
- [ ] Metadata complete (version, date, status)

### README.md
- [ ] Overview answers "what/why/how" (first 100 words)
- [ ] Quick start ≤5 steps
- [ ] Examples copy-paste ready
- [ ] Target audience clear
- [ ] Success criteria measurable
- [ ] Limitations honest
- [ ] Support links present
- [ ] Version number visible

### DEPLOYMENT_GUIDE.md
- [ ] Time estimates realistic
- [ ] Prerequisites complete
- [ ] Steps numbered and sequential
- [ ] Code blocks runnable
- [ ] Troubleshooting section present (3-5 issues)
- [ ] Multiple deployment paths (≥2 options)
- [ ] Testing section included
- [ ] Cost estimates provided

---

## 🎯 PASS/FAIL CRITERIA

### ✅ READY TO COMMIT (Score ≥7.0/10)
- All automated validators PASS
- Manual content review ≥7.0/10
- At least 3/5 functional tests PASS
- No sensitive data in files
- README has clear "What/Why/How"
- Overall quality score ≥7.0/10

### ⚠️ CONDITIONAL PASS (Score 5.0-6.9/10)
- Fix critical issues
- Re-run validators
- Then commit

### ❌ NOT READY (Score <5.0/10)
- Major rework needed
- Review failed tests
- Address all issues before retesting

---

## 🔧 TROUBLESHOOTING VALIDATION FAILURES

### Issue: "README validator fails"
```bash
# Check what specifically failed
uv run codexa.app/agentes/codexa-agent/validators/09_readme_validator.py \
  agents/hotmart_course_builder_agent/artifacts/README.md --verbose

# Common fixes:
# - Add missing sections (Overview, Architecture, Usage)
# - Fix broken markdown syntax
# - Add version number
# - Ensure proper heading hierarchy
```

---

### Issue: "Path consistency fails"
```bash
# Find broken paths
uv run codexa.app/agentes/codexa-agent/validators/16_path_consistency_validator.py \
  agents/hotmart_course_builder_agent/ --verbose

# Common fixes:
# - Update relative paths in docs
# - Move files to expected locations
# - Fix typos in file references
```

---

### Issue: "JSON parsing fails"
```bash
# Validate JSON manually
python -m json.tool agents/hotmart_course_builder_agent/artifacts/AGENT_CONFIGURATION.json

# Common fixes:
# - Remove trailing commas
# - Fix unescaped quotes
# - Ensure proper bracket/brace matching
# - Validate with jsonlint.com
```

---

### Issue: "Sensitive data detected"
```bash
# Search for patterns
grep -r "sk-" agents/hotmart_course_builder_agent/
grep -r "api_key" agents/hotmart_course_builder_agent/

# Common fixes:
# - Replace real API keys with "your-api-key" placeholders
# - Remove credentials from examples
# - Use environment variables in code examples
```

---

## 📊 QUALITY SCORE CALCULATION

```
Overall Score = (Weighted Average of All Phases)

Phase Weights:
- Automated Validators: 20%
- Manual Content Review: 30%
- Functional Testing: 30%
- Integration Testing: 10%
- Documentation Sync: 10%

Example:
- Validators: 9/10 (20% weight) = 1.8
- Content: 8/10 (30% weight) = 2.4
- Functional: 7/10 (30% weight) = 2.1
- Integration: 8/10 (10% weight) = 0.8
- Doc Sync: 9/10 (10% weight) = 0.9
------------------------------------
TOTAL: 8.0/10 ✅ READY TO COMMIT
```

---

## 🚀 PRE-COMMIT WORKFLOW (Recommended)

```bash
# 1. Run automated validation (1-2 min)
.\agents\hotmart_course_builder_agent\validate_agent.ps1

# 2. If score ≥7.0, run AI review (2-3 min)
/review agents/hotmart_course_builder_agent/

# 3. Fix any issues AI found

# 4. Run validation again to confirm
.\agents\hotmart_course_builder_agent\validate_agent.ps1

# 5. If still ≥7.0, commit!
git add agents/hotmart_course_builder_agent/
git commit -m "feat(agents): Add Hotmart Course Builder Agent v1.0.0"
```

**Total Time**: 5-10 minutes
**Confidence Level**: High (double-validated)

---

## 📚 ADDITIONAL RESOURCES

### Documentation
- **VALIDATION_CHECKLIST.md**: Complete manual checklist (this directory)
- **CODEXA Agent SDK**: https://docs.codexa.app/agents
- **Validator Docs**: `codexa.app/agentes/codexa-agent/validators/README.md`

### Support
- **GitHub Issues**: https://github.com/codexa/agents/issues
- **Community Forum**: https://community.codexa.app
- **Discord**: https://discord.gg/codexa

---

**Commands Reference Version**: 1.0.0
**Last Updated**: 2025-11-20
**Quick Reference**: Keep this file open during validation sessions
