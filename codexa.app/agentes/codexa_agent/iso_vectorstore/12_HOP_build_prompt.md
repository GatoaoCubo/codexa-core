# 94_meta_build_prompt_HOP | Meta-Construction HOP Builder

**ID**: meta_build_prompt_HOP | **Version**: 1.0.0 | **Created**: 2025-11-13
**Purpose**: Guide creation of HOP modules following TAC-7 framework
**Dependencies**: 08_prompt_generator.py, 07_hop_sync_validator.py | **Category**: builder | **Framework**: TAC-7
**Usage**: Creating reusable prompt modules for workflows and agents

---

## INPUT_CONTRACT

### Required
- **$prompt_spec** (object) - HOP module specification | Format: `{module_id, purpose (1-2 sentences), category (builder|validator|analyzer|transformer), inputs: [{name: $input, type, required, validation}], outputs: [{name: $output, type, structure}], domain}` | Validation: Non-empty module_id + purpose + ≥1 input/output

### Optional
- **$template_reference** (string) - Existing HOP template path | Default: Standard TAC-7 template | Ex: "agentes/anuncio/prompts/descricao_builder_HOP.md"
- **$validation_strict** (boolean) - Strict validation after generation | Default: true

---

## OUTPUT_CONTRACT

### Primary
- **$hop_module** (object) - Complete TAC-7 compliant HOP | Format: MD file (7 sections) | Structure: `{file_path, module_id, content (full markdown), tac7_sections: {MODULE_METADATA, INPUT_CONTRACT, OUTPUT_CONTRACT, TASK, STEPS, VALIDATION, CONTEXT}, validation_passed, word_count}` | Validation: All 7 TAC sections | INPUT_CONTRACT typed + validated | OUTPUT_CONTRACT structured | STEPS numbered 3-7 actionable | VALIDATION quality gates | No orphaned $vars

### Secondary
- **$validation_report** (object) - HOP sync validator results | Structure: `{passed, errors[], warnings[]}`

---

## TASK

**Role**: HOP Module Constructor (CODEXA)

**Objective**: Create complete TAC-7 compliant HOP module (reusable prompt with clear I/O contracts)

**Quality Standards**: All 7 TAC-7 sections complete | Explicit I/O contracts with types | Clear actionable steps (3-7) | Implementable validation rules | Chainable via $arguments

**Constraints**: Follow TAC-7 exactly | No orphaned $vars | Consistent $prefix naming | Pass hop_sync_validator

**Input**: $prompt_spec
**Output**: $hop_module (complete TAC-7 structure)

---

## STEPS

### STEP 1: Parse Specification
**Extract**: Module ID + purpose | Category (builder/validator/analyzer/transformer) | All inputs (types + validation) | All outputs (structures) | Domain context | **Validate**: Specification completeness

### STEP 2: Generate MODULE_METADATA
**Create**: `ID: {module_id}_HOP | Version: 1.0.0 | Created: {DATE} | Purpose: {spec.purpose} | Dependencies: {list or None} | Category: {spec.category} | Framework: TAC-7`

### STEP 3: Write INPUT_CONTRACT
**For each input** from spec:
- Name with $prefix | Type | Description | Format | Validation rules | Default (if optional) | Example
**Sections**: Required Inputs | Optional Inputs
**Ensure**: All $variables used in STEPS are defined here

### STEP 4: Write OUTPUT_CONTRACT
**For each output** from spec:
- Name with $prefix | Type | Description | Format | Structure (detailed) | Validation rules
**Sections**: Primary Output(s) | Secondary Output(s)
**Ensure**: All $variables produced in STEPS are defined here

### STEP 5: Write TASK Section
**Components**: Role statement | Primary objective | Quality standards (3-5 bullets) | Constraints (3-5 bullets) | Clear I/O summary
**Format**: Concise information-dense using keywords

### STEP 6: Write STEPS (3-7 numbered)
**Each STEP**:
- H3 header: `### STEP N: {Clear Action Name}`
- Purpose (1 sentence if complex)
- Actions (numbered sub-list or paragraph)
- Outputs to capture (if any)
- Validation checks (if phase gate)
**Ensure**: Logical flow | All $vars defined before use | $arguments chaining clear

### STEP 6.5: Infuse Operational Intelligence (HOP Quality Enhancement)
**Pattern Application**: Embed proven patterns from operational knowledge base into HOP structure

**Entropy-Aware Design**:
- Classify HOP complexity via entropy scoring (instructions <30=clear, 30-60=moderate, >60=complex)
- Target entropy range: Keep STEPS section <40 entropy (actionable clarity)
- Validation: Measure instruction ambiguity → refactor high-entropy steps

**Argument Chaining Rigor**:
- Explicit $var lineage: Document source (INPUT_CONTRACT) → usage (STEPS) → output (OUTPUT_CONTRACT)
- Chain validation: No orphaned $vars (grep all $prefixes, cross-reference contracts)
- Context passing: Define context_strategy per workflow phase (full_history/last_step/custom)
- Dependency mapping: If HOP used in multi-phase workflow, specify depends_on + input sources

**Axiom-Based Validation Rules**:
- HOP axioms: Core quality principles as validation gates (e.g., "All $vars defined before use")
- Computational checks: Translatable to automated validation scripts (hop_sync_validator)
- Entropy gates: Quality score sections measure alignment entropy (consistency across sections)

**Knowledge Integration Patterns**:
- Versiculo structure: If HOP generates knowledge, format as semantic units (id, entropy, classification, tags)
- Vector store compatibility: Outputs compatible with embedding + retrieval (structured markdown)
- Semantic clarity: Use domain-specific keywords for retrieval optimization

**Recovery & Edge Cases**:
- Failure modes: Document expected failures per STEP (e.g., "If $input invalid → return $error_obj")
- Grace protocol: Define fallback logic (primary validation fails → secondary checks → minimal viable output)
- Validation fallback: If strict validation fails, specify acceptable degraded outputs

**Multi-Agent HOP Patterns**:
- If HOP used in agent construction: Include agent communication protocol elements
- If HOP orchestrates agents: Define AgentMessage structure, routing logic
- Agent coordination: Specify synchronization points, handoff protocols

**Quality Enhancement**:
- Actionable keyword density: Favor verbs + concrete nouns over abstract concepts
- Structural entropy reduction: Break complex steps into numbered sub-actions
- Example density: Include 1-2 concrete examples per complex concept
- Validation automation: Write checks translatable to Python/regex (hop_sync_validator compatible)

### STEP 7: Write VALIDATION Section
**Quality Gates** (5-10 checks):
- ✅ Check name | How to verify | Fix if fails
**Quality Score**:
- Scoring criteria (percentages sum to 100%)
- Minimum acceptable threshold (typically 7.0/10.0)
- Action if below threshold

### STEP 8: Write CONTEXT Section
**Components**: Usage (where HOP used) | Upstream (dependencies + inputs source) | Downstream (outputs usage) | Argument Chaining (pattern + example) | Assumptions (environment, files, platform, user input)
**Format**: Information-dense with keywords

### STEP 9: Validate & Finalize
**Actions**:
1. Run hop_sync_validator if $validation_strict=true
2. Check all TAC-7 sections present
3. Verify no orphaned $variables
4. Ensure $arguments chaining documented
5. Validate word count reasonable (<1000 lines optimal)
6. Generate $validation_report
7. Return $hop_module object

---

## VALIDATION

**Quality Gates**:
- ✅ **TAC-7 Completeness**: All 7 sections present | Verify: Check section headers | Fix: Add missing sections
- ✅ **Input Contract Complete**: All $inputs typed + validated | Verify: Each $var has type/validation | Fix: Add missing specs
- ✅ **Output Contract Complete**: All $outputs structured | Verify: Structure defined for each | Fix: Add structure definitions
- ✅ **No Orphaned Variables**: All $vars in STEPS defined in contracts | Verify: Cross-reference vars | Fix: Add to INPUT_CONTRACT or remove usage
- ✅ **Steps Actionable**: 3-7 clear numbered steps | Verify: Count steps, check clarity | Fix: Consolidate or clarify
- ✅ **Validation Rules Present**: Quality gates + score + threshold | Verify: VALIDATION section complete | Fix: Add gates/criteria
- ✅ **Context Documented**: Usage + chaining + assumptions | Verify: CONTEXT section complete | Fix: Add missing components
- ✅ **hop_sync_validator Passes**: If strict mode enabled | Verify: Run validator | Fix: Address errors/warnings

**Quality Score** (1-10): TAC-7 compliance 30% | Contract clarity 25% | Steps actionability 20% | Validation completeness 15% | Context documentation 10% | **Min acceptable: 7.0** | If <7.0: Identify weakest area, revise, re-validate

---

## CONTEXT

**Usage**: Workflow automation (creating reusable prompts) | Agent construction (defining agent behaviors) | Meta-construction pipelines | Command builders (/codexa-build_prompt)

**Upstream**: User provides $prompt_spec (module requirements) | Prerequisites: 08_prompt_generator.py, 07_hop_sync_validator.py | Optional: $template_reference for consistency

**Downstream**: $hop_module → Use in workflows/agents | $validation_report → Quality assurance | Validated HOP → Commit to prompts/ directory

**Argument Chaining**: Typically used after planning phase | Pattern: `[Planning] → meta_build_prompt_HOP → $hop_module → [Integration]`
Example: `step_1: {analyze_requirements} → step_2: {hop_module: "94_meta_build_prompt_HOP.md", inputs: {$prompt_spec: $step_1.requirements}} → step_3: {integrate_hop: $step_2.hop_module}`

**Assumptions**: Environment (Python 3.10+, uv) | Files (08_prompt_generator.py, 07_hop_sync_validator.py functional) | Framework (TAC-7 standard established) | User Input ($prompt_spec sufficient, no ambiguity) | HOPs (stored in prompts/ subdirectories, follow naming convention)

---

**Version**: 1.0.0 | **Updated**: 2025-11-13 | **Maintainer**: CODEXA Team
**Related**: 94_codexa_build_prompt.md (command) | 08_prompt_generator.py (implementation) | 07_hop_sync_validator.py (validation)
