# INSTRUCTIONS | [AGENT_NAME] Agent

**Version**: [VERSION]
**Purpose**: Instructions for AI assistants / Agent builders to use [AGENT_NAME]
**Type**: HOP (Higher-Order Prompt) for LLM execution
**Updated**: [LAST_UPDATED]

---

## 🎯 CORE PURPOSE

[AGENT_DESCRIPTION]

**Use this agent when**: [PRIMARY_USE_CASE]

**Output**: [OUTPUT_DESCRIPTION]

---

## 🏛️ ARCHITECTURE PILLARS

### 4 IN-AGENT Pillars (Internal Construction)

**Contexto**: [DOMAIN_CONTEXT]
- Domain knowledge, requirements, codebase understanding

**Modelo**: [RECOMMENDED_LLM]
- LLM selection (GPT-4o+, Sonnet 4.5+), reasoning mode

**Tools**: [AVAILABLE_TOOLS]
- Available functions, integrations, validators

**Prompts**: [HOP_MODULES]
- HOPs, instructions, meta-formats

### 8 OUT-AGENT Pillars (External Artifacts)

**Templates**: [TEMPLATES]
- Reusable agentic prompts with [VARIABLES]

**Standard Output**: [OUTPUT_FORMATS]
- .md (human) + .llm.json (structured) + .meta.json (metadata)

**Types**: [DATA_TYPES]
- Information flow storytelling through codebase

**Documentation**: [DOCS_FILES]
- AI_DOCS (third-party) + internal (system)

**Tests**: [TEST_CRITERIA]
- Self-validating feedback loops, quality gates

**Architecture**: [ARCHITECTURE_PATTERN]
- Easy navigation (filenames, functions, folders, README)

**Plans**: [EXECUTION_PLANS]
- Detailed prompts for MASSIVE work (ADW workflows)

**ADWs**: [ADW_WORKFLOWS]
- Agentic Developer Workflows (1-shot solutions)

---

## 🤖 AI ASSISTANT INSTRUCTIONS

**IMPORTANT**: DO NOT READ [SCRIPTS_LOCATION] directly unless discovery fails

### Discovery-First Workflow

**Pattern**: Find existing files → Understand system → Execute orchestration

```bash
# 1. SCAN: List available modules
ls -1 [AGENT_DIRECTORY]/*.py
ls -1 [AGENT_DIRECTORY]/*.md
ls -1 [AGENT_DIRECTORY]/prompts/*.md

# 2. CHECK: Review configuration
cat [AGENT_DIRECTORY]/config/*.json | head -50

# 3. EXECUTE: Run agent
[EXECUTION_COMMAND]

# 4. VERIFY: Check output
ls -1 USER_DOCS/[OUTPUT_DIRECTORY]/*.md | tail -5
```

### When to Use

**USE this agent for**:
✅ [USE_CASE_1]
✅ [USE_CASE_2]
✅ [USE_CASE_3]
✅ [USE_CASE_4]
✅ [USE_CASE_5]

**DO NOT use for**:
❌ [DONT_USE_CASE_1]
❌ [DONT_USE_CASE_2]
❌ [DONT_USE_CASE_3]

### When to Read Source Code

**ONLY** read source files when:
- Discovery workflow doesn't provide needed information
- User explicitly requests analysis of specific modules
- Debugging agent behavior or phase logic
- Extending agent capabilities or adding new features
- Modifying configuration or adding new formats/platforms

**Otherwise**: Use discovery commands above for faster, more efficient operation

---

## 🔄 WORKFLOW

[WORKFLOW_DESCRIPTION]

**Conceptual Phases**: [PHASE_COUNT] ([PHASE_NAMES])

**Technical Implementation**: [STEP_COUNT] steps

```
[WORKFLOW_DIAGRAM]
```

**Duration**: [EXECUTION_TIME]

---

## 📝 KEY FILES

**Core Modules**:
- [CORE_FILE_1] - [DESCRIPTION_1]
- [CORE_FILE_2] - [DESCRIPTION_2]
- [CORE_FILE_3] - [DESCRIPTION_3]

**HOP Modules** (prompts/):
- [HOP_MODULE_1] - [HOP_DESCRIPTION_1]
- [HOP_MODULE_2] - [HOP_DESCRIPTION_2]
- [HOP_MODULE_3] - [HOP_DESCRIPTION_3]

**Configuration** (config/):
- [CONFIG_FILE_1] - [CONFIG_DESCRIPTION_1]
- [CONFIG_FILE_2] - [CONFIG_DESCRIPTION_2]
- [CONFIG_FILE_3] - [CONFIG_DESCRIPTION_3]

**Execution Plans** (plans/):
- [PLAN_FILE_1] - [PLAN_DESCRIPTION_1]
- [PLAN_FILE_2] - [PLAN_DESCRIPTION_2]

---

## ✅ VALIDATION

### Quality Gates
[VALIDATION_CRITERIA]

### Compliance Checks
[COMPLIANCE_CHECKS]

### Quality Thresholds
- [THRESHOLD_1]: [VALUE_1]
- [THRESHOLD_2]: [VALUE_2]
- [THRESHOLD_3]: [VALUE_3]

---

## 🔗 INTEGRATION

### Upstream Dependencies
[UPSTREAM_AGENTS]
- [UPSTREAM_1]: [INTEGRATION_DESCRIPTION_1]
- [UPSTREAM_2]: [INTEGRATION_DESCRIPTION_2]

### Downstream Consumers
[DOWNSTREAM_LOCATION]
- [DOWNSTREAM_1]: [INTEGRATION_DESCRIPTION_1]

### Data Flow
```
[DATA_FLOW_DIAGRAM]
```

---

## 📊 PERFORMANCE METRICS

**Timing**: [PERFORMANCE_TIMING]
**Output Size**: [OUTPUT_SIZE]
**Token Efficiency**: [TOKEN_COUNT]
**Quality Score**: [QUALITY_SCORE]

---

## 🎯 BEST PRACTICES

1. **[BEST_PRACTICE_1_TITLE]**: [BEST_PRACTICE_1_DESCRIPTION]
2. **[BEST_PRACTICE_2_TITLE]**: [BEST_PRACTICE_2_DESCRIPTION]
3. **[BEST_PRACTICE_3_TITLE]**: [BEST_PRACTICE_3_DESCRIPTION]
4. **[BEST_PRACTICE_4_TITLE]**: [BEST_PRACTICE_4_DESCRIPTION]
5. **[BEST_PRACTICE_5_TITLE]**: [BEST_PRACTICE_5_DESCRIPTION]

---

## 🔧 AUTO-DISCOVERY CAPABILITIES

**Detection Strategy**: Agent automatically detects available capabilities on first run

**Capabilities Detected**:
- `web_search`: [WEB_SEARCH_USAGE]
- `vision`: [VISION_USAGE]
- `code_interpreter`: [CODE_INTERPRETER_USAGE]
- `file_search`: [FILE_SEARCH_USAGE]

**Adaptation Logic**:
```yaml
IF [CAPABILITY_1] available:
  - [ENHANCED_FEATURE_1]
  - [ENHANCED_FEATURE_2]
ELSE:
  - [FALLBACK_BEHAVIOR]

IF [CAPABILITY_2] available:
  - [ENHANCED_FEATURE_3]
ELSE:
  - [FALLBACK_BEHAVIOR_2]
```

**Fallback Strategy**: All critical features work without external capabilities. Auto-discovery enhances quality but never blocks execution.

---

## 📚 CHANGELOG

### [LATEST_VERSION] ([LATEST_DATE])
[CHANGELOG_LATEST]

### [PREVIOUS_VERSION] ([PREVIOUS_DATE])
[CHANGELOG_PREVIOUS]

---

**Status**: [STATUS] | **Version**: [VERSION] | **Type**: [AGENT_TYPE] | **Dependencies**: [DEPENDENCIES]
**Updated**: [LAST_UPDATED] | **ROI**: [ROI_METRICS] | **Quality Score**: [QUALITY_SCORE]/100

---

> 💡 **TIP**: [AGENT_TIP]
> 🎯 **GOAL**: [AGENT_GOAL]
> ✅ **READY**: [READINESS_STATUS]
