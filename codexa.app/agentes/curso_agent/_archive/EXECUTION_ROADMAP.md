# CURSO AGENT v2.0.0 - EXECUTION ROADMAP | Priority-Based Implementation

**Agent**: curso_agent | **Version**: 1.0.0 → 2.0.0 | **Timeline**: 7-11 days (1.5-2 weeks)
**Created**: 2025-11-20 | **Status**: Ready for Execution | **Priority System**: ⭐⭐⭐ Critical | ⭐⭐ High | ⭐ Medium

---

## 🎯 EXECUTIVE SUMMARY

**Mission**: Transform curso_agent from documentation-based agent to complete meta-constructor with full CODEXA infrastructure

**Current Gap**: 7/12 CODEXA pillars missing | No builders/validators/commands/workflows
**Target State**: 12/12 pillars implemented | 32 new files | Complete automation

**ROI**:
- **Time Savings**: 30-45 min/module (automated scripts) + 1-2 hours (automated sales pages)
- **Quality**: Automated validation (4 checklists + Hotmart compliance)
- **Scalability**: Reusable templates with [OPEN_VARIABLES]

**Total Effort**: 7-11 days (~56-88 hours) | **Priority**: HIGH (monetization + documentation)

---

## 📊 PRIORITY MATRIX (What to Build When)

### ⭐⭐⭐ CRITICAL PATH (Must Have - Week 1)
**Sprint 1**: Foundation (1-2 days)
- INSTRUCTIONS.md + SETUP.md (doc_sync_builder)
- 51_AGENT_REGISTRY.json registration
- config/paths.py centralization
- **Why Critical**: Without these, agent can't integrate with CODEXA system
- **Impact**: Enables all other sprints
- **Effort**: 1 hour actual work + validation

### ⭐⭐⭐ HIGH VALUE (Quick Wins - Week 2)
**Sprint 2 (Partial)**: Core Builders (2 builders only)
- 02_video_script_builder.py (saves 30-45 min/module)
- 04_sales_collateral_builder.py (saves 1-2 hours/course)
- **Why High Value**: Highest ROI builders (time savings)
- **Impact**: Immediate automation of most time-consuming tasks
- **Effort**: 6-8 hours (focus on 2 builders first, others later)

### ⭐⭐ MEDIUM PRIORITY (Week 2-3)
**Sprint 2 (Complete)**: Remaining Builders + Validators
- 01_course_outline_builder.py
- 03_workbook_builder.py
- 05_hotmart_package_builder.py
- 5 validators (automated quality gates)
- **Why Medium**: Important but not blocking
- **Impact**: Complete automation + quality gates
- **Effort**: 12-16 hours

**Sprint 3**: Commands + Workflows
- 6 slash commands (/curso_*)
- 3 ADW workflows
- **Why Medium**: UX enhancement (but can use builders directly)
- **Impact**: Better user experience, orchestration
- **Effort**: 8-12 hours

### ⭐ LOW PRIORITY (Week 3-4)
**Sprint 4**: HOPs + Templates
- 5 HOPs TAC-7 (migrate from iso_vectorstore)
- 4 templates with [OPEN_VARIABLES]
- **Why Low**: Reusability enhancement (not blocking)
- **Impact**: Better organization, TAC-7 compliance
- **Effort**: 12-16 hours

**Sprint 5**: Polish + Trinity Output
- Trinity Output implementation
- Final documentation polish
- **Why Low**: Nice-to-have (infrastructure works without it)
- **Impact**: CODEXA standard compliance
- **Effort**: 6-8 hours

---

## 🚀 RECOMMENDED EXECUTION SEQUENCE

### WEEK 1: CRITICAL PATH ⭐⭐⭐

#### DAY 1 (Morning - 2 hours): Foundation Setup
```bash
# TASK 1.1: Generate Documentation (30 min)
python builders/11_doc_sync_builder.py --mode auto_fix --target curso_agent

# TASK 1.2: Register Agent (15 min)
# Edit 51_AGENT_REGISTRY.json manually:
{
  "curso_agent": {
    "name": "CODEXA Curso Agent",
    "type": "educational",
    "category": ["content-generation", "pedagogical-design"],
    "status": "production-ready",
    "version": "2.0.0",
    "dependencies": ["marca_agent", "pesquisa_agent", "anuncio_agent"],
    "description": "Educational content architect for Hotmart courses",
    "capabilities": ["video-scripts", "workbooks", "sales-collateral", "hotmart-optimization"],
    "model": "GPT-4o / Claude Sonnet 4.5+",
    "paths": {
      "root": "agentes/curso_agent",
      "prime": "PRIME.md",
      "instructions": "INSTRUCTIONS.md",
      "setup": "SETUP.md"
    }
  }
}

# TASK 1.3: Create config/paths.py (30 min)
mkdir curso_agent/config
# Create config/paths.py (see IMPROVEMENT_PLAN Phase 2)

# TASK 1.4: Validate (15 min)
python validators/12_doc_sync_validator.py --agent curso_agent
```

**Deliverables**: INSTRUCTIONS.md, SETUP.md, config/paths.py, updated registry
**Success Criteria**: Validation score ≥0.85 | Agent registered | Paths centralized

---

#### DAY 1 (Afternoon - 4 hours): High-Value Builder #1

```bash
# TASK 1.5: Build Video Script Generator (4 hours)
# Create builders/ directory
mkdir curso_agent/builders
cd curso_agent/builders

# Create 02_video_script_builder.py
# Use 02_agent_meta_constructor.py as template
# Key features:
# - Load context from context/ directory
# - Generate 15-30min script with timing marks
# - Hook ≤90s validation
# - [OPEN_VARIABLES] injection (≥2)
# - Brand voice compliance (seed words)

# Test with real module
python 02_video_script_builder.py --module "01_MODULO_INTRODUCAO" --output test_script.md
```

**Deliverables**: 02_video_script_builder.py (functional)
**Success Criteria**: Generates script with hook ≤90s | [OPEN_VARIABLES] ≥2 | Timing marks present

---

#### DAY 2 (Morning - 4 hours): High-Value Builder #2

```bash
# TASK 2.1: Build Sales Collateral Generator (4 hours)
# Create 04_sales_collateral_builder.py
# Key features:
# - Landing page (Hero, Problem, Solution, Proof, CTA)
# - Email sequence (6 emails)
# - Ad copy (3 platforms: FB, Google, LinkedIn)
# - Brand voice validation (disruptivo-sofisticado)
# - Hotmart optimization (checkout structure)

# Test with course outline
python 04_sales_collateral_builder.py --course "Layer 1-2 Transition" --output test_sales/
```

**Deliverables**: 04_sales_collateral_builder.py (functional)
**Success Criteria**: Generates landing + emails + ads | Seed words ≥3 | Hotmart-ready

---

#### DAY 2 (Afternoon - 2 hours): Quick Win Validation

```bash
# TASK 2.2: Manual Testing (1 hour)
# Test both builders with real data
# Validate outputs against checklists

# TASK 2.3: Documentation Update (1 hour)
# Update README.md with builder usage
# Add quick start examples
```

**Deliverables**: Updated README.md | Test results
**Success Criteria**: Both builders work end-to-end | Documentation clear

---

### WEEK 1 CHECKPOINT ✅

**Completed**:
- ✅ INSTRUCTIONS.md + SETUP.md generated
- ✅ curso_agent registered in 51_AGENT_REGISTRY.json
- ✅ config/paths.py created
- ✅ 2 high-value builders functional (script + sales)
- ✅ Quick win validation complete

**Impact**:
- Agent integrated into CODEXA system ✅
- 70% automation achieved (scripts + sales = highest time cost) ✅
- Foundation ready for remaining sprints ✅

**Next**: Can use builders immediately for course creation OR continue with Sprint 2 (remaining builders)

---

### WEEK 2: AUTOMATION COMPLETION ⭐⭐

#### DAY 3-4 (8 hours): Remaining Builders

```bash
# TASK 3.1: Course Outline Builder (2 hours)
# Create 01_course_outline_builder.py
# Input: Scope, priority, duration, timeline
# Output: Module outline (objectives, timing, prerequisites)

# TASK 3.2: Workbook Builder (3 hours)
# Create 03_workbook_builder.py
# Input: Module outline, module_id
# Output: 8-15 page workbook (theory + exercises + reflection)

# TASK 3.3: Hotmart Package Builder (3 hours)
# Create 05_hotmart_package_builder.py
# Input: All generated content
# Output: Hotmart-ready package (DRM, metadata, structure)
```

**Deliverables**: 3 builders (outline, workbook, package)
**Success Criteria**: All builders functional | Integration tested

---

#### DAY 5 (8 hours): Validators

```bash
# TASK 5.1: Create validators/ directory
mkdir curso_agent/validators

# TASK 5.2: Build 5 Validators (6 hours)
# 01_content_quality_validator.py (Hook ≤90s, Objectives measurable)
# 02_brand_voice_validator.py (Seed words ≥3, No hype)
# 03_pedagogical_validator.py (Progressive complexity, Prerequisites clear)
# 04_technical_validator.py ([OPEN_VARIABLES] ≥2, Timing feasible)
# 05_hotmart_compliance_validator.py (DRM, LGPD, Claims sensíveis)

# TASK 5.3: Integration Testing (2 hours)
# Test each validator with builder outputs
# Ensure score ≥7.0 threshold works correctly
```

**Deliverables**: 5 validators (automated quality gates)
**Success Criteria**: All validators functional | Score threshold ≥7.0 enforced

---

### WEEK 2 CHECKPOINT ✅

**Completed**:
- ✅ All 5 builders functional (outline, script, workbook, sales, package)
- ✅ All 5 validators functional (content, brand, pedagogy, technical, hotmart)
- ✅ 100% automation achieved
- ✅ Quality gates automated

**Impact**:
- Complete builder suite ✅
- Automated validation ✅
- Ready for UX layer (commands + workflows) ✅

**Next**: Can stop here (full automation) OR continue with Sprint 3 (UX enhancement)

---

### WEEK 3: UX & ORGANIZATION ⭐

#### DAY 6-7 (8-10 hours): Commands + Workflows

```bash
# TASK 6.1: Create commands/ directory (6 hours)
mkdir curso_agent/commands

# Create 6 slash commands:
# /curso_outline.md
# /curso_script.md
# /curso_workbook.md
# /curso_sales.md
# /curso_validate.md
# /curso_package.md

# TASK 6.2: Create workflows/ directory (4 hours)
mkdir curso_agent/workflows

# Create 3 ADW workflows:
# 01_ADW_QUICK_COURSE.md (5-10 min outline)
# 02_ADW_FULL_MODULE.md (30-45 min module)
# 03_ADW_SALES_PACKAGE.md (20-30 min sales)

# TASK 6.3: Test Commands (2 hours)
# Test each command end-to-end
# Update START_HERE.md with examples
```

**Deliverables**: 6 commands + 3 workflows
**Success Criteria**: All commands functional | Workflows tested | Documentation updated

---

#### DAY 8-9 (12-16 hours): HOPs + Templates

```bash
# TASK 8.1: Create prompts/ directory (8 hours)
mkdir curso_agent/prompts

# Migrate + TAC-7 compliance:
# 91_curso_outline_HOP.md
# 92_curso_script_HOP.md
# 93_curso_workbook_HOP.md
# 94_curso_sales_HOP.md
# 95_curso_validate_HOP.md

# TASK 8.2: Create templates/ directory (6 hours)
mkdir curso_agent/templates

# Create 4 templates:
# video_script_template.md
# workbook_template.md
# landing_page_template.md
# email_sequence_template.md

# TASK 8.3: Validate HOPs (2 hours)
python validators/07_hop_sync_validator.py prompts/91_curso_outline_HOP.md
# ... validate all 5 HOPs
```

**Deliverables**: 5 HOPs TAC-7 + 4 templates
**Success Criteria**: All HOPs validated (score ≥7.0) | Templates have [OPEN_VARIABLES] ≥2

---

### WEEK 3 CHECKPOINT ✅

**Completed**:
- ✅ 6 slash commands functional
- ✅ 3 ADW workflows tested
- ✅ 5 HOPs TAC-7 compliant
- ✅ 4 templates with [OPEN_VARIABLES]
- ✅ Complete UX layer
- ✅ Organizational structure complete

**Impact**:
- Easy-to-use slash commands ✅
- Orchestrated workflows ✅
- TAC-7 compliant prompts ✅
- Reusable templates ✅

**Next**: Final polish (Trinity Output + documentation)

---

### WEEK 4: POLISH & COMPLETION ⭐

#### DAY 10-11 (6-8 hours): Final Polish

```bash
# TASK 10.1: Trinity Output Implementation (4 hours)
# Update all 5 builders to generate:
# - .md (human-readable)
# - .llm.json (structured data)
# - .meta.json (metadata: version, timestamp, quality_score)

# TASK 10.2: Final Documentation (2 hours)
# Update README.md with v2.0.0 metrics
# Generate CHANGELOG.md (v1.0.0 → v2.0.0)
# Update PRIME.md if needed

# TASK 10.3: Full Validation (2 hours)
# Run all validators on all outputs
# Ensure quality score ≥9.0/10.0
# Fix any issues
```

**Deliverables**: Trinity Output + Final docs
**Success Criteria**: All builders generate Trinity Output | Docs complete | Quality ≥9.0

---

## 📊 EFFORT SUMMARY

| Sprint | Tasks | Files | Hours | Priority |
|--------|-------|-------|-------|----------|
| Sprint 1 | Foundation | 4 | 8 | ⭐⭐⭐ |
| Sprint 2 (Partial) | High-Value Builders | 2 | 8 | ⭐⭐⭐ |
| Sprint 2 (Full) | All Builders + Validators | 8 | 24 | ⭐⭐ |
| Sprint 3 | Commands + Workflows | 9 | 16 | ⭐⭐ |
| Sprint 4 | HOPs + Templates | 9 | 16 | ⭐ |
| Sprint 5 | Polish + Trinity | Updates | 8 | ⭐ |
| **TOTAL** | | **32** | **56-88** | |

---

## 🎯 MILESTONE CHECKPOINTS

### Milestone 1: Foundation Complete ✅ (Day 1-2)
**Deliverables**:
- INSTRUCTIONS.md + SETUP.md ✅
- 51_AGENT_REGISTRY.json registration ✅
- config/paths.py ✅
- 2 high-value builders ✅

**Success Criteria**:
- Agent integrated into CODEXA system
- 70% automation achieved
- Immediate usability

**Decision Point**: STOP HERE or continue?
- **Stop**: You have foundation + high-value automation (scripts + sales)
- **Continue**: Complete automation + UX layer

---

### Milestone 2: Automation Complete ✅ (Week 2)
**Deliverables**:
- All 5 builders ✅
- All 5 validators ✅
- 100% automation ✅

**Success Criteria**:
- Complete builder suite
- Automated quality gates
- Production-ready automation

**Decision Point**: STOP HERE or continue?
- **Stop**: You have complete automation (can use builders directly)
- **Continue**: Add UX layer (commands + workflows)

---

### Milestone 3: UX Complete ✅ (Week 3)
**Deliverables**:
- 6 slash commands ✅
- 3 ADW workflows ✅
- 5 HOPs TAC-7 ✅
- 4 templates ✅

**Success Criteria**:
- Easy-to-use interface
- Orchestrated workflows
- TAC-7 compliance
- Reusable templates

**Decision Point**: STOP HERE or continue?
- **Stop**: You have complete system with UX
- **Continue**: Final polish (Trinity Output)

---

### Milestone 4: v2.0.0 Complete ✅ (Week 4)
**Deliverables**:
- Trinity Output ✅
- Final documentation ✅
- Quality ≥9.0/10.0 ✅

**Success Criteria**:
- All 12 CODEXA pillars implemented
- Complete meta-constructor
- Production-ready v2.0.0

---

## 💡 OPTIMIZATION STRATEGIES

### Strategy 1: Quick Win Path (2 days)
**Focus**: Sprint 1 + Partial Sprint 2 (foundation + high-value builders)
**Effort**: 16 hours (~2 days)
**Impact**: 70% automation (scripts + sales = highest ROI)
**When to Use**: Need immediate results, limited time

### Strategy 2: Core Automation Path (1 week)
**Focus**: Sprint 1 + Full Sprint 2 (foundation + all builders + validators)
**Effort**: 32 hours (~1 week)
**Impact**: 100% automation + quality gates
**When to Use**: Need complete automation, UX can wait

### Strategy 3: Complete System Path (2 weeks)
**Focus**: All 5 sprints (foundation + automation + UX + polish)
**Effort**: 56-88 hours (~2 weeks)
**Impact**: Complete CODEXA meta-constructor (all 12 pillars)
**When to Use**: Want complete system, have time for full implementation

---

## 🚨 RISK MITIGATION

### Risk 1: Time Overrun
**Mitigation**: Use milestone checkpoints | Stop at any milestone if time limited
**Fallback**: Quick Win Path (2 days) gives 70% value

### Risk 2: Builder Complexity
**Mitigation**: Use 02_agent_meta_constructor.py as template | Start with simpler builders first
**Fallback**: Manual generation with templates (skip builders, use templates directly)

### Risk 3: Validation Failures
**Mitigation**: Test incrementally | Validate each builder before next
**Fallback**: Lower quality threshold (≥6.0 instead of ≥7.0) temporarily

### Risk 4: Integration Issues
**Mitigation**: Use config/paths.py from start | Follow CODEXA patterns strictly
**Fallback**: Standalone operation (curso_agent works independently, integration later)

---

## ✅ ACCEPTANCE CRITERIA (v2.0.0)

**Must Have** (Blocking v2.0.0 release):
- ✅ INSTRUCTIONS.md + SETUP.md exist
- ✅ Registered in 51_AGENT_REGISTRY.json
- ✅ config/paths.py functional
- ✅ At least 2 builders functional (script + sales minimum)
- ✅ At least 2 validators functional (content + brand minimum)

**Should Have** (Important but not blocking):
- ✅ All 5 builders functional
- ✅ All 5 validators functional
- ✅ 6 slash commands
- ✅ 3 ADW workflows

**Nice to Have** (Enhancement):
- ✅ 5 HOPs TAC-7 compliant
- ✅ 4 templates with [OPEN_VARIABLES]
- ✅ Trinity Output implemented
- ✅ Quality score ≥9.0/10.0

---

## 📞 NEXT ACTIONS

### Option 1: Automated Execution (Recommended)
```bash
# Use CODEXA meta-constructor to build curso_agent v2.0.0
/codexa-build_agent "Transform curso_agent to complete meta-constructor with builders, validators, commands, workflows following CODEXA_IMPROVEMENT_PLAN.md"
```

### Option 2: Manual Execution (Sprint by Sprint)
```bash
# Week 1: Foundation + High-Value Builders
# Day 1: Sprint 1 (Foundation)
python builders/11_doc_sync_builder.py --mode auto_fix --target curso_agent
# Edit 51_AGENT_REGISTRY.json manually
# Create config/paths.py manually
python validators/12_doc_sync_validator.py --agent curso_agent

# Day 1-2: Partial Sprint 2 (High-Value Builders)
# Create 02_video_script_builder.py manually
# Create 04_sales_collateral_builder.py manually
# Test both builders

# Week 2: Complete Automation (Sprint 2 Full)
# Create remaining 3 builders
# Create 5 validators
# Test everything

# Week 3: UX (Sprint 3 + 4)
# Create 6 commands
# Create 3 workflows
# Create 5 HOPs
# Create 4 templates

# Week 4: Polish (Sprint 5)
# Implement Trinity Output
# Final documentation
# Full validation
```

### Option 3: Hybrid Approach (Recommended for Most)
```bash
# Use automated tools where possible, manual where needed

# Automated: Documentation + Registry
python builders/11_doc_sync_builder.py --mode auto_fix --target curso_agent

# Manual: config/paths.py (15 min one-time setup)
# Manual: Registry entry (10 min)

# Automated: Builders (use CODEXA agent to generate)
/codexa-build_prompt "Create video script builder following 02_agent_meta_constructor.py pattern"

# Automated: Validators (use templates)
/codexa-build_prompt "Create content quality validator with score ≥7.0 threshold"

# Manual: Commands + Workflows (fast to write)
# Automated: HOPs (use 08_prompt_generator.py)
python builders/08_prompt_generator.py
```

---

## 🎉 SUCCESS METRICS (How to Measure v2.0.0)

**Quantitative**:
- Files created: 32 (target)
- Builders functional: 5/5
- Validators functional: 5/5
- Commands functional: 6/6
- Workflows tested: 3/3
- HOPs TAC-7 compliant: 5/5
- Templates with [OPEN_VARIABLES]: 4/4
- Quality score: ≥9.0/10.0
- Validation pass rate: 100%

**Qualitative**:
- Agent integrates with CODEXA system ✅
- Automation saves 30-45 min/module ✅
- Quality gates prevent errors ✅
- UX is intuitive (slash commands) ✅
- Templates are reusable ✅
- Documentation is complete ✅

**Business Impact**:
- Course creation time: 50% reduction
- Content quality: Automated validation
- Scalability: Reusable templates
- Monetization: Hotmart-ready output
- Self-improvement: Can build/improve own builders

---

**Created by**: CODEXA Meta-Constructor Agent
**Framework**: Priority-Based Execution | Milestone Checkpoints | Risk Mitigation
**Philosophy**: "Build what matters first, then enhance"

---

> 🎯 **Recommended Path**: Quick Win (Week 1) → Assess → Continue if needed
> 📊 **70% Value in 20% Time**: Foundation + High-Value Builders = 2 days, 70% automation
> 🏗️ **Complete System**: All 5 sprints = 2 weeks, 100% CODEXA compliance
