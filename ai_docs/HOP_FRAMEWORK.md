# HOP Framework Guide | ECOMLM.CODEXA

> **Status**: Production Documentation
> **Last Updated**: 2025-11-14
> **Version**: 1.0.0
> **Framework**: TAC-7

---

## 🎯 Overview

The **HOP (Higher-Order Prompt) Framework** is a revolutionary approach to prompt engineering that treats prompts as composable, versionable, and validated data structures rather than static text strings.

**Key Innovation**: HOPs transform prompts from unstructured text into modular components with explicit input/output contracts, validation rules, and chainable $arguments.

---

## 🧠 Core Concepts

### What is a HOP?

```
Traditional Prompt: Static instruction text
↓
HOP: Structured prompt module with:
  - Metadata (ID, version, purpose, dependencies)
  - Input Contract (typed inputs with validation)
  - Output Contract (structured outputs with schemas)
  - Task Definition (role, objective, constraints)
  - Actionable Steps (3-7 numbered procedures)
  - Validation Gates (quality thresholds, checks)
  - Context Documentation (usage, chaining, assumptions)
```

### The Paradigm Shift

**Before HOPs**:
```
"You are a market research agent. Analyze this product and return insights."
```

**With HOPs**:
```markdown
## INPUT_CONTRACT
- $product_description (string, required, 20-500 chars)
- $market (string, required, enum: ["BR", "US", "EU"])
- $depth (string, optional, default: "standard")

## OUTPUT_CONTRACT
- $market_insights (object) - Structure: {size, growth, competitors[], pricing{}}
- $quality_score (number) - Range: 0-10, threshold ≥ 7.0

## STEPS
### STEP 1: Validate Inputs
### STEP 2: Execute Market Analysis
### STEP 3: Generate Insights
### STEP 4: Validate Quality

## VALIDATION
- ✅ All required fields present in $market_insights
- ✅ Quality score ≥ 7.0
```

---

## 📐 TAC-7 Framework Structure

HOPs follow the **TAC-7 standard**, consisting of **7 mandatory sections**:

### 1. MODULE_METADATA

**Purpose**: Identify and version the HOP module

**Required Fields**:
```markdown
**ID**: {module_id}_HOP
**Version**: {semver}
**Created**: {YYYY-MM-DD}
**Purpose**: {1-2 sentence description}
**Dependencies**: {list or None}
**Category**: {builder|validator|analyzer|transformer}
**Framework**: TAC-7
```

**Example**:
```markdown
**ID**: market_analysis_HOP
**Version**: 2.1.0
**Created**: 2025-11-14
**Purpose**: Conduct comprehensive market research for e-commerce products in Brazilian marketplaces
**Dependencies**: None
**Category**: analyzer
**Framework**: TAC-7
```

---

### 2. INPUT_CONTRACT

**Purpose**: Define all inputs with types, validation rules, and examples

**Structure**:
```markdown
## INPUT_CONTRACT

### Required
- **$variable_name** (type) - Description | Format: spec | Validation: rules | Ex: example

### Optional
- **$variable_name** (type) - Description | Default: value | Validation: rules | Ex: example
```

**Example**:
```markdown
## INPUT_CONTRACT

### Required
- **$agent_description** (string) - Clear 1-3 sentence agent purpose | Format: Natural language | Validation: Non-empty, 20-500 chars, mentions domain | Ex: "Sentiment analysis agent for product reviews, generates positive/neutral/negative scores with justifications"

### Optional
- **$model** (string) - AI model for construction | Default: "opus" | Validation: ["opus", "sonnet"] | Ex: "sonnet"
- **$verbose** (boolean) - Enable verbose logging | Default: false | Validation: Boolean | Ex: true
```

**Key Principles**:
- **$prefix notation**: All variables start with `$` for clear identification
- **Typed inputs**: Specify string, number, boolean, array, object
- **Explicit validation**: Define constraints (length, range, enum, regex)
- **Examples included**: Concrete examples for each input
- **Required vs Optional**: Clear separation with defaults for optional

---

### 3. OUTPUT_CONTRACT

**Purpose**: Define all outputs with structure, format, and validation

**Structure**:
```markdown
## OUTPUT_CONTRACT

### Primary
- **$output_name** (type) - Description | Format: spec | Structure: {detailed} | Validation: rules

### Secondary
- **$output_name** (type) - Description | Structure: {detailed}
```

**Example**:
```markdown
## OUTPUT_CONTRACT

### Primary
- **$agent_artifacts** (object) - Complete deployment-ready agent artifacts
  - Format: Directory structure (MD + JSON files)
  - Structure: `{adw_id, agent_name, target_directory, artifacts: {MASTER_INSTRUCTIONS.md, AGENT_CONFIGURATION.json, README.md, DEPLOYMENT_GUIDE.md, EXAMPLES.md, META_CONSTRUCTION_LOG.md}, workflow_summary}`
  - Validation: All 8 artifacts present | MASTER_INSTRUCTIONS 2000-5000 words | Valid JSON config | No [VARIABLE] placeholders

### Secondary
- **$workflow_log** (array) - Execution log for all phases | Structure: `[{phase, duration_seconds, inputs, outputs, status}]`
- **$extracted_variables** (object) - Key construction variables | Structure: `{$agent_name, $agent_purpose, $model_choice, $tools_enabled[], $reasoning_mode}`
```

**Key Principles**:
- **Structured outputs**: Detailed schema definitions
- **Primary vs Secondary**: Distinguish main output from metadata
- **Validation rules**: Define acceptable output criteria
- **Chaining ready**: Outputs become inputs for downstream HOPs

---

### 4. TASK

**Purpose**: Define the HOP's role, objective, standards, and constraints

**Structure**:
```markdown
## TASK

**Role**: {What this HOP acts as}

**Objective**: {What this HOP accomplishes}

**Quality Standards**: {3-5 bullet points of quality expectations}

**Constraints**: {3-5 bullet points of limitations/requirements}

**Input**: {Summary of inputs}
**Output**: {Summary of outputs}
```

**Example**:
```markdown
## TASK

**Role**: Agent Meta-Constructor Module (CODEXA system)

**Objective**: Orchestrate construction of complete, production-ready AI agent via 5-phase meta-construction workflow

**Quality Standards**:
- All artifacts complete and validated
- MASTER_INSTRUCTIONS 2000-5000 words comprehensive
- Valid configuration for target platform
- Clear actionable documentation
- Full traceability via META_CONSTRUCTION_LOG

**Constraints**:
- Use only $agent_description (no additional user input)
- Strict 5-phase workflow (no skipping phases)
- Pass context via $arguments between phases
- Isolation principle (self-contained agent)
- Automatic generation (no manual intervention)

**Input**: $agent_description + optional ($model, $target_dir, $verbose)
**Output**: $agent_artifacts (complete directory structure + all files)
```

**Key Principles**:
- **Information-dense**: Use keywords, not verbose sentences
- **Clear scope**: Explicit about what HOP does/doesn't do
- **Quality focus**: Set expectations for output quality
- **Constraint awareness**: Document limitations upfront

---

### 5. STEPS

**Purpose**: Provide 3-7 numbered, actionable steps to execute the HOP

**Structure**:
```markdown
## STEPS

### STEP 1: {Action Name}
**Purpose**: {Why this step exists}
**Actions**: {What to do - numbered list or paragraph}
**Outputs**: {Variables captured}
**Validation**: {Checks before proceeding}

### STEP 2: {Action Name}
...

### STEP N: {Action Name}
```

**Example**:
```markdown
## STEPS

### STEP 1: Validate Inputs
**Verify**: $agent_description (non-empty, sufficient detail, clear purpose, domain mentioned) | Prerequisites (Python ≥3.10, uv, ANTHROPIC_API_KEY)
**Prepare**: Generate ADW ID | Create target_dir | Init logging

### STEP 2: Phase 1 - Strategic Planning
**Purpose**: Create strategic plan with [OPEN_VARIABLES] for creative freedom
**Actions**: Invoke `/agent_plan` → Pass $agent_description → Create spec (Agent name, Purpose, Model, Reasoning, Capabilities 3-5)
**Outputs**: $plan, $agent_name, $specifications
**Validation**: Non-empty plan | Name extracted | Spec has purpose/model/capabilities

### STEP 3: Phase 2 - Artifact Construction
**Purpose**: Build artifacts using $plan
**Actions**: Invoke `/agent_build` → Pass $plan → Generate MASTER_INSTRUCTIONS.md (2000-5000 words), AGENT_CONFIGURATION.json, schemas
**Outputs**: $artifacts, $agent_configuration
**Validation**: 4 core artifacts | MASTER_INSTRUCTIONS 2000-5000 words | Valid JSON | No [PLACEHOLDER]
```

**Key Principles**:
- **3-7 steps optimal**: Too few lacks clarity, too many overwhelming
- **Actionable**: Each step is executable, not theoretical
- **Logical flow**: Steps build on each other sequentially
- **Variable tracking**: Document when $vars are created/used
- **Phase gates**: Validation at critical checkpoints

---

### 6. VALIDATION

**Purpose**: Define quality gates, scoring criteria, and failure handling

**Structure**:
```markdown
## VALIDATION

**Quality Gates** (before completion):
- ✅ **Check Name**: Description | Verify: How to check | Fix: What to do if fails

**Quality Score** (1-10):
- Criterion 1: X%
- Criterion 2: Y%
- Criterion N: Z%
- **Min acceptable: 7.0**
- If <7.0: {Action}
```

**Example**:
```markdown
## VALIDATION

**Quality Gates** (before returning $agent_artifacts):
- ✅ **Phase Completion**: All 5 phases executed | Verify: Workflow log has all phases | Fix: Re-run failed phase with verbose mode
- ✅ **Artifact Completeness**: All 8 files present | Verify: List $target_dir, count=8 | Fix: Re-run relevant phase
- ✅ **MASTER_INSTRUCTIONS Quality**: 2000-5000 words comprehensive | Verify: Word count + sections | Fix: Re-run Phase 2 with expansion
- ✅ **Configuration Validity**: Valid JSON + required fields | Verify: Parse AGENT_CONFIGURATION.json | Fix: Re-run Phase 2 with schema validation
- ✅ **Documentation Complete**: README, DEPLOYMENT_GUIDE, EXAMPLES present + non-empty | Verify: Check files exist | Fix: Re-run Phase 5
- ✅ **No Placeholders**: No [VARIABLE] or [PLACEHOLDER] remains | Verify: Grep `\[.*\]` | Fix: Re-run phase and fill all variables
- ✅ **Traceability**: META_CONSTRUCTION_LOG documents all phases | Verify: Log has 5 sections | Fix: Regenerate from summary

**Quality Score** (1-10):
- Completeness: 30%
- Quality: 30%
- Documentation: 20%
- Traceability: 20%
- **Min acceptable: 7.0**
- If <7.0: Re-run weakest area with focused improvements
```

**Key Principles**:
- **Automated checks**: Write verifiable, not subjective rules
- **Clear thresholds**: Explicit numeric or boolean criteria
- **Fix strategies**: Tell how to remediate failures
- **Quality scoring**: Weighted criteria sum to 100%
- **Minimum bars**: Set acceptable quality floor (typically 7.0/10.0)

---

### 7. CONTEXT

**Purpose**: Document usage patterns, dependencies, and argument chaining

**Structure**:
```markdown
## CONTEXT

**Usage**: {Where/when this HOP is used}

**Upstream**: {What feeds into this HOP}

**Downstream**: {What consumes this HOP's outputs}

**Argument Chaining**: {How $vars flow between HOPs}

**Assumptions**: {Environment, files, platform, user input assumptions}
```

**Example**:
```markdown
## CONTEXT

**Usage**: Execution plans (automated agent creation) | Workflow orchestration scripts | CLI agent builders (/codexa-build_agent) | Meta-construction pipelines

**Upstream**: User provides $agent_description | Prerequisites: Python 3.10+, uv, ANTHROPIC_API_KEY, meta-constructor script | Optional: $model, $target_dir

**Downstream**: $agent_artifacts → Deploy to OpenAI Agent Builder | $workflow_log → Analysis/improvement of process | $extracted_variables → AGENT_REGISTRY.json

**Argument Chaining**: Typically **first module** in agent creation workflow
- Pattern: `[User Input] → meta_build_agent_HOP → $agent_artifacts → [Deploy/Register]`
- Example execution plan:
  ```json
  {
    "step_1": {
      "hop_module": "91_meta_build_agent_HOP.md",
      "inputs": {"$agent_description": "...", "$model": "opus"},
      "outputs": ["$agent_artifacts"]
    },
    "step_2": {
      "depends_on": ["step_1"],
      "inputs": {"$artifacts": "$step_1.agent_artifacts"}
    }
  }
  ```

**Assumptions**:
- Environment: Python 3.10+, uv, ANTHROPIC_API_KEY set
- Files: 02_agent_meta_constructor.py exists in builders/ directory
- Agent Isolation: Self-contained, no external dependencies beyond OpenAI
- Platform: OpenAI Agent Builder (gpt-4o/gpt-5, Vector Store, Code Interpreter)
- User Input: $agent_description is sufficient, no follow-up questions
```

**Key Principles**:
- **Full lifecycle**: Document from input sources to output consumers
- **Chaining explicit**: Show exact $variable flow patterns
- **Assumptions clear**: Don't hide prerequisites or expectations
- **Examples included**: Concrete execution plan snippets

---

## 🔗 Argument Chaining

### The $arguments Pattern

**Core Idea**: HOPs communicate via typed $variables that flow through workflow phases

**Example Workflow**:
```
Phase 1: Research HOP
  Input: $product_description
  Output: $market_insights

Phase 2: Brand HOP
  Input: $market_insights (from Phase 1)
  Output: $brand_strategy

Phase 3: Listing HOP
  Input: $market_insights + $brand_strategy (from Phases 1&2)
  Output: $product_listing
```

### Context Strategies

**1. Minimal Context**
```json
{
  "context_strategy": "minimal",
  "description": "Each step gets only its required inputs"
}
```
- Use when: Steps are independent
- Pros: Lower token usage, faster execution
- Cons: No cross-step awareness

**2. Step-by-Step Context**
```json
{
  "context_strategy": "step_by_step",
  "description": "Each step gets previous step's output"
}
```
- Use when: Linear dependency chain
- Pros: Efficient sequential flow
- Cons: Can't reference earlier steps

**3. Accumulative Context**
```json
{
  "context_strategy": "accumulative",
  "description": "Each step gets all previous outputs"
}
```
- Use when: Complex interdependencies
- Pros: Full awareness, rich context
- Cons: Higher token usage

### Variable Naming Conventions

**Best Practices**:
- **$prefix**: All variables start with `$`
- **snake_case**: Use underscores for multi-word names
- **Descriptive**: `$market_insights` not `$data`
- **Typed**: Document types in contracts
- **No orphans**: Every $var defined in INPUT_CONTRACT before use

**Examples**:
- ✅ `$agent_description`, `$market_insights`, `$quality_score`
- ❌ `description`, `insights`, `score` (missing $)
- ❌ `$d`, `$mi`, `$qs` (too abbreviated)

---

## ✅ Validation System

### Schema Validation

**Purpose**: Ensure outputs conform to expected structure

**Example** (JSON Schema for product listing):
```json
{
  "type": "object",
  "required": ["title", "description", "keywords"],
  "properties": {
    "title": {
      "type": "string",
      "minLength": 58,
      "maxLength": 60
    },
    "description": {
      "type": "string",
      "minLength": 3000
    },
    "keywords": {
      "type": "array",
      "minItems": 10,
      "items": {"type": "string"}
    }
  }
}
```

### Quality Gates

**Automated Checks**:
```python
# Example quality gate implementation
def validate_hop_output(output, hop_spec):
    checks = []

    # Check 1: Required fields present
    checks.append(all(k in output for k in hop_spec['required_fields']))

    # Check 2: Quality score above threshold
    checks.append(output.get('quality_score', 0) >= 7.0)

    # Check 3: No placeholder variables
    checks.append('[VARIABLE]' not in str(output))

    # Check 4: Word count in range
    word_count = len(str(output).split())
    checks.append(2000 <= word_count <= 5000)

    return all(checks), checks
```

### Validation Tools

**hop_sync_validator.py**: Built-in validator for TAC-7 compliance
```bash
# Validate a HOP module
uv run validators/07_hop_sync_validator.py path/to/module_HOP.md

# Output example:
# [OK] MODULE_METADATA complete
# [OK] INPUT_CONTRACT has 3 inputs (all typed)
# [OK] OUTPUT_CONTRACT has 2 outputs (all structured)
# [OK] TASK section complete
# [OK] STEPS section has 5 steps
# [OK] VALIDATION section has 7 quality gates
# [OK] CONTEXT section complete
# [OK] No orphaned $variables
# [OK] Quality score: 9.2/10.0
```

---

## 🏗️ Complete HOP Examples

### Example 1: Agent Construction HOP (Simplified)

```markdown
# meta_build_agent_HOP | Agent Meta-Constructor

**ID**: meta_build_agent_HOP | **Version**: 1.0.0 | **Created**: 2025-11-13
**Purpose**: Guide autonomous agent construction (5-phase workflow)
**Dependencies**: 02_agent_meta_constructor.py | **Category**: builder | **Framework**: TAC-7

---

## INPUT_CONTRACT

### Required
- **$agent_description** (string) - Clear 1-3 sentence purpose | Validation: 20-500 chars, mentions domain | Ex: "Sentiment analysis agent for product reviews"

### Optional
- **$model** (string) - AI model | Default: "opus" | Validation: ["opus", "sonnet"]

---

## OUTPUT_CONTRACT

### Primary
- **$agent_artifacts** (object) - Complete agent files
  - Structure: `{adw_id, agent_name, artifacts: {MASTER_INSTRUCTIONS.md, AGENT_CONFIGURATION.json, README.md, ...}}`
  - Validation: All 8 files present | No placeholders

---

## TASK

**Role**: Agent Meta-Constructor Module

**Objective**: Construct production-ready AI agent via 5-phase workflow

**Quality Standards**: All artifacts validated | Documentation complete | Deployment-ready

**Constraints**: Use only $agent_description | Strict 5-phase flow | Automatic generation

**Input**: $agent_description
**Output**: $agent_artifacts

---

## STEPS

### STEP 1: Validate Inputs
Verify $agent_description is non-empty and clear | Check prerequisites

### STEP 2: Phase 1 - Plan
Create strategic plan with agent name, purpose, model, capabilities

### STEP 3: Phase 2 - Build
Generate MASTER_INSTRUCTIONS.md and AGENT_CONFIGURATION.json

### STEP 4: Phase 3 - Test
Validate artifacts and create test scenarios

### STEP 5: Phase 4 - Review
Critical review and quality scoring

### STEP 6: Phase 5 - Document
Generate README, DEPLOYMENT_GUIDE, EXAMPLES, META_LOG

### STEP 7: Compile Output
Organize all 8 files and return $agent_artifacts

---

## VALIDATION

**Quality Gates**:
- ✅ All 5 phases executed | Verify: Check workflow log
- ✅ All 8 files present | Verify: Count files in target_dir
- ✅ No [PLACEHOLDER] variables | Verify: Grep for placeholders
- ✅ Quality score ≥ 7.0 | Verify: Calculate from criteria

**Quality Score** (1-10):
- Completeness: 30%
- Quality: 30%
- Documentation: 20%
- Traceability: 20%
- **Min acceptable: 7.0**

---

## CONTEXT

**Usage**: Automated agent creation | CLI builders | Meta-construction pipelines

**Upstream**: User provides $agent_description | Prerequisites: Python 3.10+, uv

**Downstream**: $agent_artifacts → Deploy to OpenAI Agent Builder

**Argument Chaining**: First module in creation workflow
- Pattern: `[User Input] → meta_build_agent_HOP → $agent_artifacts → [Deploy]`

**Assumptions**: Environment setup | Agent isolation | OpenAI platform
```

---

### Example 2: Prompt Builder HOP (Simplified)

```markdown
# meta_build_prompt_HOP | HOP Module Constructor

**ID**: meta_build_prompt_HOP | **Version**: 1.0.0 | **Created**: 2025-11-13
**Purpose**: Create TAC-7 compliant HOP modules
**Dependencies**: 08_prompt_generator.py, 07_hop_sync_validator.py | **Category**: builder

---

## INPUT_CONTRACT

### Required
- **$prompt_spec** (object) - HOP specification
  - Structure: `{module_id, purpose, category, inputs[], outputs[], domain}`
  - Validation: Non-empty module_id + purpose + ≥1 input/output

---

## OUTPUT_CONTRACT

### Primary
- **$hop_module** (object) - Complete TAC-7 HOP
  - Format: Markdown file with 7 sections
  - Validation: All TAC-7 sections | No orphaned $vars | Passes hop_sync_validator

---

## TASK

**Role**: HOP Module Constructor

**Objective**: Create complete TAC-7 compliant HOP module

**Quality Standards**: All 7 sections complete | Typed I/O contracts | 3-7 actionable steps

**Constraints**: Follow TAC-7 exactly | No orphaned $vars | Consistent $naming

**Input**: $prompt_spec
**Output**: $hop_module

---

## STEPS

### STEP 1: Parse Specification
Extract module ID, purpose, category, inputs, outputs, domain

### STEP 2: Generate MODULE_METADATA
Create ID, version, purpose, dependencies, category

### STEP 3: Write INPUT_CONTRACT
For each input: name ($prefix), type, description, validation, example

### STEP 4: Write OUTPUT_CONTRACT
For each output: name ($prefix), structure, format, validation

### STEP 5: Write TASK Section
Role, objective, quality standards, constraints

### STEP 6: Write STEPS (3-7)
Numbered actionable steps with clear flow

### STEP 7: Write VALIDATION Section
Quality gates (5-10 checks) + scoring criteria

### STEP 8: Write CONTEXT Section
Usage, upstream, downstream, chaining, assumptions

### STEP 9: Validate & Finalize
Run hop_sync_validator | Check completeness | Return $hop_module

---

## VALIDATION

**Quality Gates**:
- ✅ TAC-7 Completeness: All 7 sections | Verify: Check headers
- ✅ No Orphaned Variables: All $vars defined | Verify: Cross-reference
- ✅ Steps Actionable: 3-7 clear steps | Verify: Count + clarity
- ✅ hop_sync_validator Passes | Verify: Run validator

**Quality Score** (1-10):
- TAC-7 compliance: 30%
- Contract clarity: 25%
- Steps actionability: 20%
- Validation completeness: 15%
- Context documentation: 10%
- **Min acceptable: 7.0**

---

## CONTEXT

**Usage**: Workflow automation | Agent construction | Meta-construction pipelines

**Upstream**: User provides $prompt_spec | Prerequisites: Python tools

**Downstream**: $hop_module → Use in workflows/agents

**Argument Chaining**: After planning phase
- Pattern: `[Planning] → meta_build_prompt_HOP → $hop_module → [Integration]`

**Assumptions**: Python 3.10+ | TAC-7 standard established | HOPs stored in prompts/
```

---

## 🛠️ How to Create a HOP (Step-by-Step)

### Phase 1: Planning (5 minutes)

**1. Define Purpose**
- What does this HOP do? (1 sentence)
- What problem does it solve?
- What domain/category? (builder/validator/analyzer/transformer)

**2. Identify Inputs**
- What data does it need?
- Which inputs are required vs optional?
- What are the types and validation rules?

**3. Identify Outputs**
- What does it produce?
- What is the structure?
- Primary vs secondary outputs?

**4. List Steps**
- What are the 3-7 major actions?
- What is the logical flow?
- Where are the validation checkpoints?

---

### Phase 2: Writing (20 minutes)

**1. MODULE_METADATA (2 min)**
```markdown
**ID**: {your_module}_HOP
**Version**: 1.0.0
**Created**: 2025-11-14
**Purpose**: {One clear sentence}
**Dependencies**: {List or None}
**Category**: {builder|validator|analyzer|transformer}
**Framework**: TAC-7
```

**2. INPUT_CONTRACT (5 min)**
- List all inputs under Required/Optional
- Use $prefix for all variables
- Specify types, validation, examples

**3. OUTPUT_CONTRACT (3 min)**
- List all outputs under Primary/Secondary
- Define detailed structures
- Specify validation rules

**4. TASK (3 min)**
- Role: What this HOP acts as
- Objective: What it accomplishes
- Quality Standards: 3-5 bullets
- Constraints: 3-5 bullets
- I/O summary

**5. STEPS (5 min)**
- Write 3-7 numbered H3 headers
- Each step: purpose, actions, outputs, validation
- Ensure logical flow

**6. VALIDATION (3 min)**
- Quality Gates: 5-10 ✅ checks
- Quality Score: Weighted criteria (sum=100%)
- Min acceptable threshold

**7. CONTEXT (2 min)**
- Usage, upstream, downstream
- Argument chaining pattern
- Assumptions

---

### Phase 3: Validation (5 minutes)

**1. Self-Check**
- [ ] All 7 TAC-7 sections present?
- [ ] All $vars defined in INPUT_CONTRACT?
- [ ] All outputs in OUTPUT_CONTRACT?
- [ ] 3-7 actionable steps?
- [ ] Quality gates with verify/fix?
- [ ] Chaining pattern documented?

**2. Run Validator**
```bash
uv run validators/07_hop_sync_validator.py your_module_HOP.md
```

**3. Fix Issues**
- Address errors (missing sections, orphaned $vars)
- Address warnings (weak validation, unclear steps)
- Iterate until validator passes

---

### Phase 4: Testing (10 minutes)

**1. Manual Test**
- Try executing the HOP with real inputs
- Verify outputs match OUTPUT_CONTRACT
- Check quality gates work

**2. Integration Test**
- Test argument chaining with upstream/downstream HOPs
- Verify $variables flow correctly
- Check context assumptions hold

**3. Documentation Check**
- Can someone else understand this HOP?
- Are examples clear?
- Is chaining pattern obvious?

---

## 📊 HOP Quality Checklist

Use this checklist before committing a HOP:

### Structure (TAC-7 Compliance)
- [ ] MODULE_METADATA complete (ID, version, purpose, dependencies, category)
- [ ] INPUT_CONTRACT has all inputs (required/optional separated)
- [ ] OUTPUT_CONTRACT has all outputs (primary/secondary separated)
- [ ] TASK section defines role, objective, standards, constraints
- [ ] STEPS section has 3-7 numbered actionable steps
- [ ] VALIDATION section has quality gates + scoring
- [ ] CONTEXT section documents usage, chaining, assumptions

### Inputs & Outputs
- [ ] All $variables use $prefix notation
- [ ] All inputs have types and validation rules
- [ ] All inputs have examples
- [ ] All outputs have structure definitions
- [ ] No orphaned $variables (all defined before use)

### Steps & Flow
- [ ] Steps are numbered with H3 headers (### STEP N)
- [ ] Each step is actionable (not theoretical)
- [ ] Logical flow from step to step
- [ ] Variables captured at appropriate steps
- [ ] Validation checkpoints at critical phases

### Validation
- [ ] Quality gates are automated (verifiable, not subjective)
- [ ] Each gate has: check name, verify method, fix action
- [ ] Quality scoring criteria sum to 100%
- [ ] Minimum acceptable threshold defined (typically 7.0/10.0)

### Context & Chaining
- [ ] Usage scenarios documented
- [ ] Upstream dependencies clear
- [ ] Downstream consumers identified
- [ ] Argument chaining pattern shown
- [ ] Assumptions explicitly stated

### Quality
- [ ] hop_sync_validator passes with no errors
- [ ] File length under 1000 lines (optimal)
- [ ] Information-dense (keywords not verbose prose)
- [ ] Examples included for complex concepts
- [ ] Cross-references to related HOPs

---

## 🔮 Advanced Patterns

### Pattern 1: Multi-Phase Workflows

**Problem**: Complex tasks requiring multiple steps with accumulating context

**Solution**: Chain multiple HOPs with accumulative context strategy

```json
{
  "workflow": "e-commerce_complete_listing",
  "context_strategy": "accumulative",
  "steps": [
    {
      "id": "research",
      "hop": "pesquisa_HOP",
      "inputs": {"$product_description": "..."},
      "outputs": ["$research_notes"]
    },
    {
      "id": "brand",
      "hop": "marca_HOP",
      "inputs": {"$research_notes": "$research.research_notes"},
      "outputs": ["$brand_strategy"]
    },
    {
      "id": "listing",
      "hop": "anuncio_HOP",
      "inputs": {
        "$research_notes": "$research.research_notes",
        "$brand_strategy": "$brand.brand_strategy"
      },
      "outputs": ["$product_listing"]
    }
  ]
}
```

---

### Pattern 2: Validation-Retry Loops

**Problem**: Outputs may not meet quality threshold on first attempt

**Solution**: Implement retry logic with quality feedback

```markdown
### STEP 5: Generate with Retry
**Actions**:
1. Generate initial output using $inputs
2. Validate against quality gates
3. If quality_score >= threshold: Return output
4. If quality_score < threshold AND retries < max_retries:
   - Add $quality_feedback to context
   - Retry generation with improvements
5. If max_retries exceeded: Return best attempt with warning

**Outputs**: $final_output, $quality_score, $retry_count
```

---

### Pattern 3: Dynamic Module Selection

**Problem**: Different inputs require different processing paths

**Solution**: Use conditional module loading

```markdown
### STEP 2: Select Processing Module
**Actions**:
1. Analyze $input_type
2. If $input_type == "csv": Load csv_processor_HOP
3. If $input_type == "json": Load json_processor_HOP
4. If $input_type == "jsonl": Load jsonl_processor_HOP
5. Execute selected module with $input_data

**Outputs**: $selected_module, $processed_data
```

---

## 📚 Related Documentation

**Internal**:
- [API Reference](./API_REFERENCE.md) - FastAPI endpoints and client examples
- [WORKFLOWS](./WORKFLOWS.md) - Complete workflow examples
- [Meta-Construction Guide](../codexa.app/docs_consolidados/43_META_CONSTRUCTION_INDEX.md)
- [Agent Registry](../codexa.app/51_AGENT_REGISTRY.json)

**CODEXA Framework**:
- [42_HOP_FRAMEWORK.md](../codexa.app/42_HOP_FRAMEWORK.md) - Original HOP framework specification
- [PRIME.md](../codexa.app/agentes_codexa/codexa-agent/PRIME.md) - CODEXA meta-construction system

**External Resources**:
- [Prompt Engineering Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [LangChain LCEL](https://python.langchain.com/docs/expression_language/)
- [Semantic Kernel](https://learn.microsoft.com/semantic-kernel/)

---

**Last Updated**: 2025-11-14
**Maintained By**: CODEXA Team
**Status**: Production Documentation
**Version**: 1.0.0
