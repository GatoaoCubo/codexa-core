# /prime-codexa | CODEXA Meta-Construction System

> **Scout**: Para descoberta de arquivos, use `mcp__scout__*` | [SCOUT_INTEGRATION.md](../SCOUT_INTEGRATION.md)

## 🎯 PURPOSE

**CODEXA**: Self-building meta-construction system for LLMs. Bootstrapping architecture using its own construction files to self-build and self-improve.

**Provides**: Builders (prompts, agents, commands, schemas) | Specialized e-commerce agents (Brazilian market) | HOP Framework (Higher-Order Prompts) | Validation system (quality gates) | Multi-phase ADW workflows

**Philosophy**: Build the builder, not the instance. Meta > Instance. Templates > One-offs.

## 🏛️ ARCHITECTURE PILLARS

### 12 LEVERAGE POINTS OF AGENTIC CODING

**Context** (Foundation) - Information & Perspective | What does the agent know?
**Model** (Intelligence) - Intelligence & Potential | How smart is the reasoning?
**Prompt** (Communication) - Communication Method | How do you instruct it?
**Tools** (Capabilities) - Agent Capabilities | What can it do?
**Standard Out** (Visibility) - Command Visibility | Can you see what happens?
**Types** (Flow) - Information Flow | How does data move through system?
**Documentation** (Knowledge) - Knowledge Base | Where is tribal knowledge stored?
**Tests** (Validation) - Self-Validation | Does it verify its own work?
**Architecture** (Patterns) - Consistent Patterns | Is codebase navigable?
**Plans** (Massive Work) - Massive Agentic Prompts | Can you orchestrate complex tasks?
**Templates** (Reuse) - Reusable Prompts | Do you build once, use many times?
**ADWs** (Workflows) - AI Developer Workflows | Can agent work autonomously while you're AFK?

**Priority Ladder**: Start bottom (Context) → Work up → Top 3 (Templates, Plans, ADWs) = highest leverage

### 4 IN-AGENT Pillars (Internal Construction)
1. **Contexto** - Domain knowledge, codebase context, requirements
2. **Modelo** - Claude Opus 4.5 / Sonnet 4.5+ (meta-construction = most complex task, requires extended reasoning mode)
3. **Tools** - Available functions, integrations, validators
4. **Prompts** - HOPs, instructions, meta-formats

**Why Claude Opus 4.5?** Meta-construction is the MOST complex cognitive task: building systems that build systems. Requires multi-phase planning (5 phases: Plan→Build→Test→Review→Document), architectural reasoning (choosing best patterns), quality validation (multiple gates), and self-improvement loops. Claude Opus 4.5 excels at deep reasoning; Claude Sonnet 4.5 excels at long context (analyzing entire codebases). Both are essential for meta-level work.

### 8 OUT-AGENT Pillars (External Artifacts)
1. **Templates** - Reusable agentic prompts with [VARIABLES]
2. **Standard Output** - .md (human) + .llm.json (structured) + .meta.json (metadata)
3. **Types** - Information flow storytelling through codebase
4. **Documentation** - AI_DOCS (third-party) + internal (system)
5. **Tests** - Self-validating feedback loops, quality gates
6. **Architecture** - Easy navigation (filenames, functions, folders, README)
7. **Plans** - Detailed prompts for MASSIVE work (ADW workflows)
8. **ADWs** - Agentic Developer Workflows (1-shot solutions)

## 🤖 INSTRUCTIONS FOR AI ASSISTANTS

**IMPORTANT:** META-LEVEL. Read strategically. Find and use existing files to orchestrate [any task].

### Scout-First Workflow (LAW 9)

**Pattern**: Scout → Analyze Consolidatables → CRUD Priority → Execute

```bash
# 0. SCOUT FIRST (MANDATORY - LAW 9)
# Before ANY task, spawn scouts to find relevant files and duplicates
/spawn model:haiku
1. explore: find files relevant to "{task description}"
2. explore: find consolidatable duplicates in affected directories

# 1. ANALYZE: Review scout findings
# - Existing files to UPDATE (not duplicate)
# - Similar files to CONSOLIDATE
# - Orphaned files to DELETE

# 2. BUILD: Execute construction (5-phase agent / 3-phase workflow)
uv run builders/02_agent_meta_constructor.py "Agent description"

# 3. VALIDATE: Quality gates
uv run validators/07_hop_sync_validator.py [file.md]
```

**CRUD Priority** (highest to lowest):
1. **DELETE** - Remove stale, orphaned, duplicate files first
2. **UPDATE** - Modify existing files to match new requirements
3. **READ** - Use existing content as foundation
4. **CREATE** - Only when scouts confirm nothing exists

### PITER Framework (AFK Coding Agents)

**P**rompt entry - Initial instructions and context
**I**dentify - Find relevant files, dependencies, patterns
**T**rigger - Execute builders, commands, workflows
**E**nvironment - Check context, tools, permissions
**R**eview - Validate outputs, quality gates, self-improvement

### Meta-Formato Básico (Template Pattern)

```markdown
{name} | {category}
{follow instructions from: [file]}
{description: detailed purpose}
{relevant files: find and list}
{step-by-step: H3 headers + bullet points}
{validation commands: list}
{notes: edge cases, warnings}
{previous output as $arguments}
```

### When to Use

**USE** `/prime-codexa` for: Building agents | Creating builders (meta-meta) | Orchestrating workflows (ADW) | Generating prompts/HOPs | Creating commands | System self-improvement | Meta-construction | Architecture decisions

**DON'T USE** for: Domain tasks (use specialized agents) | One-offs (direct code) | Simple file ops (basic tools)

### Key Files for Context

**Core Structure**: `builders/` (8 scripts) | `validators/` (4 scripts) | `prompts/` (HOPs) | `workflows/` (ADWs)

**Primary Builders**:
- `02_agent_meta_constructor.py` ⭐ - 5 phases: Plan→Build→Test→Review→Document
- `11_doc_sync_builder.py` ⭐ - ADW-100: Auto-sync documentation across all agents
- `08_prompt_generator.py` - HOPs (TAC-7 framework)
- `05_command_generator.py` - Slash commands

**Primary Validators**:
- `12_doc_sync_validator.py` ⭐ - Full documentation synchronization validation
- `13_code_quality_validator.py` ⭐ - Code style guide compliance (naming, types, docs)
- `07_hop_sync_validator.py` - HOP TAC-7 compliance
- `09_readme_validator.py` - Documentation standards
- `10_taxonomy_validator.py` - Registry consistency

**Primary ADWs** (v2.0.0):
- `201_ADW_FEATURE_DEVELOPMENT.md` ⭐ NEW - Two-phase planning (Planning Agent → Execution Agent)
- `202_ADW_BUG_FIXING.md` ⭐ NEW - Systematic bug fixing (Reproduce → Root Cause → Fix → Verify)
- `203_ADW_PARALLEL_ORCHESTRATION.md` ⭐ NEW - Multi-agent parallel execution
- `97_ADW_NEW_AGENT_WORKFLOW.md` - Complete agent creation (5 phases)
- `100_ADW_DOC_SYNC_WORKFLOW.md` - Auto-sync documentation

**Primary Documentation** (v2.3.0):
- `docs/PLATFORM_ANALYSIS.md` ⭐ NEW - 32 platforms analyzed, patterns extracted
- `docs/INTEGRATION_GUIDE.md` ⭐ NEW - Complete v2.0 feature usage guide
- `docs/MIGRATION_GUIDE.md` ⭐ NEW - v1.3 → v2.x migration steps
- `docs/BEST_PRACTICES.md` ⭐ NEW - Compiled from 30+ platforms

**Entry Points**: `PRIME.md` (this file) | `README.md` (structure) | `INSTRUCTIONS.md` (operations)

### Meta-Construction Principles

**1. Scout-First (LAW 9)** - Every task starts with scouts | Find before build | Consolidate before create | CRUD: Delete > Update > Read > Create
**2. Meta > Instance** - Build builders not artifacts | Templates not instances | Patterns not solutions
**3. One-Prompt-One-Purpose (OPOP)** - 1 module = 1 responsibility | Compose don't duplicate | Single agent, single prompt, single purpose
**4. [OPEN_VARIABLES]** - Intentional blanks | Creative entropy | LLM fills appropriately
**5. $arguments-chaining** - Phase N output → Phase N+1 input | Explicit data flow | Traceable
**6. Isolation Principle** - Self-contained agents | No hidden dependencies | Portable/composable
**7. Trinity Output** - .md (human) + .llm.json (structured) + .meta.json (metadata)
**8. Information-Dense** - Keywords not sentences | Token-efficient | MAX 1000 LINES/FILE
**9. Plan>Code>Test>Review>Document** - ADW workflow pattern | Quality gates at each step
**10. Always Add Feedback Loops** - Test → Validate → Fix → Repeat | Closing the Loop | Self-correcting systems
**11. Template Your Engineering** - Transform workflows into reusable units | 1 template → many plans → many results
**12. Prioritize Agentics** - 50%+ time in agentic layer (building builders) vs application layer (building features)
**13. ##report Standard** - Every builder/validator/workflow must output structured report (MD + JSON) with metrics/results

### Keywords Reference (Information-Dense Communication)

**Core**: Purpose, Workflow, Step-by-step, Output format, Commands, Hooks, Styles, Skills
**Prompts**: HOPs (Higher-Order Prompts) | Execute long tool chains | Compose other files
**Agent**: Programmable, Scalable, Performance-focused | Think hard → Plan → Execute
**Meta**: $arguments (chaining) | [VARIABLES] (open) | Report (structured output)

### Builder Workflows

**WORKFLOW 1: Build Agent (5-phase)**
```bash
uv run builders/02_agent_meta_constructor.py "Agent description"
# Phases: Plan→Build→Test→Review→Document
# Output: Complete agent with 8 artifacts (README, config, schemas, etc.)
```

**WORKFLOW 2: Build HOP (TAC-7)**
```bash
uv run builders/08_prompt_generator.py
# Structure: Metadata→Input→Output→Task→Steps→Validation→Context
# Validate: uv run validators/07_hop_sync_validator.py [file.md]
```

**WORKFLOW 3: Sync Documentation (ADW-100)** ⭐ NEW
```bash
# Automatic documentation synchronization across ALL agents
python builders/11_doc_sync_builder.py --mode auto_fix

# Audit only (no changes)
python builders/11_doc_sync_builder.py --mode audit_only

# Dry run (simulate changes)
python builders/11_doc_sync_builder.py --mode auto_fix --dry-run

# Validate results
python validators/12_doc_sync_validator.py --all

# Output:
# - Creates missing INSTRUCTIONS.md and SETUP.md files
# - Synchronizes versions across all documentation
# - Updates 51_AGENT_REGISTRY.json
# - Generates comprehensive reports (MD + JSON)
# - Quality score improvement: avg +69% (0.55 → 0.93)
```

**ADW-100 Features**:
- 10-step workflow (Discovery → Template → Variable Extract → Generate → Validate × 5 → Report)
- ~200 template variables automatically filled
- Windows-compatible (ASCII-only output)
- Automatic backups (.bak before overwrites)
- Version synchronization across README/PRIME/INSTRUCTIONS/SETUP
- Quality gates: ALL agents must reach ≥0.85 score
- CI/CD ready (GitHub Actions + pre-commit hooks)

**Key Learnings**:
1. **Template completeness critical** - Missing even 1 variable breaks generation
2. **Registry naming consistency** - Use `{name}_agent` suffix everywhere
3. **STRUCTURE sections essential** - Validators need filesystem ↔ docs sync
4. **Windows Unicode handling** - Replace emojis with [OK]/[WARN]/[FAIL]
5. **Threshold-based validation** - Allow ≤15 [VARIABLES] for documentation examples
6. **Regex backreference pitfalls** - Use lambda functions for replacements with dots

### HOP Framework v2.0.0 (TAC-7 + Enrichments)

**Core TAC-7 Sections** (Original):
```markdown
# MODULE_METADATA: id, version, purpose, dependencies, category
# INPUT_CONTRACT: Required/optional inputs ($variables) + types + validation
# OUTPUT_CONTRACT: Primary/secondary outputs + structure + format
# TASK: Role, objective, standards, constraints
# STEPS: 3-7 actionable steps (numbered H3 headers)
# VALIDATION: Quality gates (✅ checks) + thresholds (score ≥ 7.0/10.0)
# CONTEXT: Usage, upstream/downstream, $arguments chaining, assumptions
```

**v2.0.0 Enrichments** (NEW):
```markdown
# PROMPT_LAYER_COMPOSITION: Which prompt layers compose this HOP
# TASK_BOUNDARY: Operating mode, transitions, constraints
# SRC_INTEGRATION: References to src/ modules (llm/, tools/, runtime/, auth/)
# ARTIFACT_OUTPUTS: What files/reports this HOP generates
# FEEDBACK_LOOP: Closing the Loop pattern for this workflow
```

**Prompt Layer Compositions**:
- `PLANNING_AGENT`: Identity + Modes + Tools + Communication
- `EXECUTION_AGENT`: Identity + Modes + Tools + Code + Workflows
- `VERIFICATION_AGENT`: Identity + Modes + Tools + Steering
- `ORCHESTRATION_AGENT`: Identity + Modes + Tools + Workflows

**Runtime Example**:
```python
from src.runtime import PromptLoader, CompositionType

loader = PromptLoader()
base = loader.load_composition(CompositionType.EXECUTION_AGENT)
hop = loader.load_hop("91_meta_build_agent_HOP")
full_prompt = base + "\n\n" + hop
```

### Self-Improvement Loop

**Pattern**: Analyze (Scout) → Identify (Mentor) → Plan (CODEXA) → Build (Builders) → Validate (Validators) → Integrate → Document (Knowledge) → Repeat

CODEXA builds itself using its own builders. Bootstrapping complete.

### Template Metaprompt Framework

**Concept**: Reusable prompts that generate other prompts by filling templates with domain-specific patterns

**Structure**:
- **Template** = Static instructions + [VARIABLES] + generation zones
- **Metaprompt** = Template + Fill logic + Validation rules
- **Generated Prompt** = Filled template ready for execution

**Pattern**: 1 Template → N Plans → M Results (exponential leverage)

**Example Flow**:
```
Template: "Create plan for {TASK_TYPE} following {STANDARDS}"
Metaprompt: Apply to "bug fix" + "CODEXA standards"
Generated: "Bug Fix Plan | Read file → Identify issue → Apply fix → Test → Commit"
```

**Benefits**: Reusable | Scalable | Consistent | Self-documenting | Versioned in codebase

### SDLC as Questions (5 Quality Gates)

**Phase 1: Plan** - What are we building? | Output: Spec with clear scope
**Phase 2: Build** - Did we make it real? | Output: Working artifacts
**Phase 3: Test** - Does it work? | Output: Test results + validation
**Phase 4: Review** - Is what we built what we asked for? (Prove it) | Output: Comparison + refinements
**Phase 5: Document** - How does it work? | Output: Complete documentation

**Usage**: Every ADW workflow MUST answer all 5 questions | Skip = incomplete work

### Composable Agentic Primitives

**Primitives** (12 Leverage Points):
- Context, Model, Prompt, Tools, Standard Out, Types, Documentation, Tests, Architecture, Plans, Templates, ADWs

**Composition Pattern**:
```
Plan + Build + Test = Mini Workflow
Build + Review + Deploy = Release Workflow
Test + Document = Documentation Workflow
ANY COMBINATION = Valid Composed Workflow
```

**Rules**:
- Primitives are independent (no hidden deps)
- Primitives are chainable ($arguments flow)
- Primitives are reusable (compose don't duplicate)
- Primitives are validatable (quality gates)

### Feedback Loops (Closing the Loop)

**Pattern**: Request → Execute → Validate → Fix → Repeat until success

**Implementation**:
```python
def closing_loop(task, validator, max_attempts=3):
    for attempt in range(max_attempts):
        result = execute(task)
        validation = validator(result)
        if validation.success:
            return result
        task = refine(task, validation.feedback)
    raise Exception("Failed after max attempts")
```

**Types of Loops**:
- **Linter Loop**: Code → Lint → Fix syntax → Re-lint → Pass
- **Test Loop**: Feature → Test → Fix failing tests → Re-test → Pass
- **Quality Loop**: Output → Score → Improve low-scoring parts → Re-score → Pass (≥threshold)
- **User Loop**: Draft → Show user → Apply feedback → Show again → Approve

### Value Function (Intermediate Feedback)

**Problem**: Binary pass/fail feedback comes too late (after full execution)
**Solution**: Intermediate signals during execution — like emotions in human learning

**Concept from RL**: Value function = expected future reward from current state
**Application**: Add checkpoint assessments during task execution

**Implementation**:
```python
def value_aware_loop(task, validator, confidence_threshold=0.7):
    for step in task.steps:
        result = execute_step(step)
        confidence = assess_confidence(result)  # 0.0-1.0

        if confidence < confidence_threshold:
            # Early course correction - don't wait until end
            result = retry_with_feedback(step, f"Low confidence: {confidence}")

        if confidence < 0.3:
            # Abort early - fundamental problem detected
            return escalate_to_human(task, step, result)

    return validator(task.aggregate_results())
```

**Key insight**: Emotions in humans act as immediate feedback ("this feels wrong")
**Application**: Add "confidence signals" at each step, not just final validation

**Gradient feedback** (better than binary):
- 0.0-0.3: Stop, escalate, fundamental issue
- 0.3-0.7: Retry current step with refinement
- 0.7-0.9: Continue but flag for review
- 0.9-1.0: Proceed with high confidence

**Rule**: Never return work without validation | Always add validation commands | Agents test and fix autonomously

### Context Management Patterns

**Context Pollution** - Too much irrelevant info | Solution: OPOP (focused agents)
**Context Overload** - Exceeding window limits | Solution: Chain shorter prompts
**Toxic Context** - Wrong/outdated information | Solution: Validate sources, timestamp data
**Context Rot** - Degraded information over conversation | Solution: Reset agent, fresh context
**Context Confusion** - Mixed purposes in one agent | Solution: Dedicated agents per purpose

**Best Practice**: 50% context for problem → 50% context for solution | No more than 3 responsibilities per agent

### Performance Metrics (v1.2.0)

**Timing**:
- Agent (5-phase): ~30-45min
- HOP (single-phase): ~5-10min
- Doc Sync (ADW-100): ~6min/agent (~30min for 5 agents)
- Orchestration (3-phase): variable

**Scanning**: 1000 files ~1-2s (cached) | Code analysis: regex, ~10-50ms/file
**Quality**: Templates 100% reusable | Retry backoff: 1s→2s→4s exponential
**Limits**: MAX 1000 LINES/FILE | Quality score ≥ 0.85 (doc sync) / ≥ 7.0/10.0 (general)

### Integration & Status (v1.2.0)

**META Layer**: CODEXA creates all agents | Generates prompts (HOP) | Builds commands | Designs schemas | Validates quality | Auto-documents | **Syncs documentation**

**Implementation**:
- ✅ 8 builders (NEW: 11_doc_sync_builder.py)
- ✅ 4 validators (NEW: 12_doc_sync_validator.py)
- ✅ HOPs (TAC-7)
- ✅ ADW workflows (NEW: ADW-100 doc sync)
- ✅ CI/CD integration (GitHub Actions + pre-commit hooks)
- ✅ Production modules (agent.py, scout_integration.py)

### Best Practices (Rules)

**DO**: Scout first (LAW 9) | Read philosophy first | Use templates | Validate incrementally | Document everything | Embrace [VARIABLES] | Chain $arguments | Build for reuse | Information-dense keywords | MAX 1000 LINES | Consolidate before create

**DON'T**: Skip scouting | Create without checking existing | Skip validation | Create orphaned dependencies | Ignore quality thresholds | Build instances (build builders instead) | Duplicate content across locations

---

**Version**: 2.6.0
**Last Updated**: 2025-12-05
**Agent Type**: Meta-Construction & Self-Improvement
**Dependencies**: All other agents (CODEXA builds them all)
**Status**: Production-Ready Multi-Agent Orchestration System

**Changelog v2.6.0** (LAW 9 INTEGRATION):
- ✅ Added Scout-First Workflow (LAW 9) as principle #1
- ✅ Added CRUD Priority discipline (Delete > Update > Read > Create)
- ✅ Updated Best Practices with consolidation rules
- ✅ Integrated with CLAUDE.md v2.6.0

**Changelog v2.5.0** (PHASE 9 DEPLOYMENT):
- ✅ Created CHANGELOG.md (complete version history, metrics, migration path)
- ✅ Created DEPLOYMENT.md (deployment steps, rollback plan, verification)
- ✅ Final version consolidation: v2.5.0 Production Release
- ✅ 9-phase self-improvement process complete (Foundation → Deployment)

**Changelog v2.4.0** (PHASE 8 VALIDATION):
- ✅ Created tests/test_task_boundary.py (TaskBoundary + TaskBoundaryManager tests)
- ✅ Created tests/test_prompt_layers.py (PromptLayerValidator + PromptComposer tests)
- ✅ Created tests/test_validators.py (ValidationReport + CodeQualityChecker tests)
- ✅ Created tests/test_adw_workflows.py (ADWWorkflow + ADWParser + ADWValidator tests)
- ✅ Complete test coverage for v2.0 features: task boundaries, prompt layers, validators, ADWs

**Changelog v2.3.0** (PHASE 7 DOCUMENTATION):
- ✅ Created docs/PLATFORM_ANALYSIS.md (32 platforms documented, patterns extracted)
- ✅ Created docs/INTEGRATION_GUIDE.md (complete v2.0 feature usage guide)
- ✅ Created docs/MIGRATION_GUIDE.md (v1.3 → v2.x migration steps)
- ✅ Created docs/BEST_PRACTICES.md (compiled from 30+ platforms)

**Changelog v2.2.0** (PHASE 6 WORKFLOWS):
- ✅ Created workflows/201_ADW_FEATURE_DEVELOPMENT.md (Two-phase planning: Planning Agent → Execution Agent)
- ✅ Created workflows/202_ADW_BUG_FIXING.md (Systematic: Reproduce → Root Cause → Fix → Verify)
- ✅ Created workflows/203_ADW_PARALLEL_ORCHESTRATION.md (Multi-agent parallel execution)
- ✅ Enriched 97_ADW_NEW_AGENT_WORKFLOW.md → v2.0.0 (two-phase planning, artifact generation)
- ✅ Enriched 98_ADW_CONSOLIDATION_WORKFLOW.md → v2.0.0 (parallel execution, batch processing)
- ✅ Enriched 99_ADW_SYSTEM_UPGRADE_WORKFLOW.md → v2.0.0 (task boundaries, rollback points)
- ✅ Enriched 100_ADW_DOC_SYNC_WORKFLOW.md → v2.0.0 (multi-agent coordination)

**Changelog v2.1.0** (PHASE 5 STANDARDS):
- ✅ Created templates/CODE_STYLE_GUIDE.md (reference to prompts/layers/05_code_conventions.md)
- ✅ Created templates/DESIGN_SYSTEM.md (reference to prompts/layers/06_design_system.md)
- ✅ Created validators/13_code_quality_validator.py (550+ lines, multi-language support)
- ✅ Code quality scoring: type coverage, docstrings, structure limits, naming conventions

**Changelog v2.0.0** (PHASE 4 ENRICHMENT):
- ✅ HOP Framework v2.0.0: Added 5 new sections (PROMPT_LAYER_COMPOSITION, TASK_BOUNDARY, SRC_INTEGRATION, ARTIFACT_OUTPUTS, FEEDBACK_LOOP)
- ✅ All 5 HOPs enriched: 91 (build_agent), 92 (chore_plan), 93 (review), 94 (build_prompt), 96 (orchestrate)
- ✅ Validators v2.0.0: Added ##report foundation to all 5 validators (07, 09, 10, 12, 16)
- ✅ Created validators/report_generator.py: Simple report generator for validators
- ✅ src/ infrastructure: Full integration (llm/, tools/, runtime/, auth/)
- ✅ Prompt Layers: 8 composable layers in prompts/layers/
- ✅ TaskBoundary: builders/task_boundary.py for progress communication

**Changelog v1.3.0**:
- ✅ Added 12 Leverage Points of Agentic Coding
- ✅ Added Template Metaprompt Framework
- ✅ Added SDLC as Questions (5 quality gates)
- ✅ Added Composable Agentic Primitives
- ✅ Added Feedback Loops (Closing the Loop)
- ✅ Added Context Management Patterns
- ✅ Expanded Meta-Construction Principles (12 principles)
- ✅ Added ##report Standard for all builders/validators/workflows

---

> [TIP]: CODEXA is the system that builds the system - use it to build, not to execute
> [META]: This prime was built using CODEXA's own builders (bootstrapping complete)
> [v2.5.0]: Multi-Agent Orchestration System - 9 phases complete (Foundation → Deployment)
