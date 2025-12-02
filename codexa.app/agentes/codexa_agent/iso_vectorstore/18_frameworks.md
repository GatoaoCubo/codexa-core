# CODEXA Frameworks Reference

Quick reference for TAC-7 and PITER frameworks used in meta-construction.

---

## TAC-7 Framework (Higher-Order Prompts)

**7 Required Sections** for all HOP modules:

### 1. MODULE_METADATA
- `id`: Unique identifier (snake_case_HOP)
- `version`: Semantic versioning (X.Y.Z)
- `purpose`: One-sentence description
- `dependencies`: Required files/modules
- `category`: builder | validator | orchestrator | template

### 2. INPUT_CONTRACT
- **Required inputs**: $variable_name (type) + validation + example
- **Optional inputs**: $variable_name (type) + default + example
- **Format**: NL (natural language) | JSON | MD | Python
- **Validation rules**: Non-empty, type checks, ranges

### 3. OUTPUT_CONTRACT
- **Primary output**: $output_name (type) + structure + format
- **Secondary outputs**: Additional artifacts
- **Validation**: Quality thresholds, completeness checks
- **Format**: MD | JSON | Python | Trinity (.md + .llm.json + .meta.json)

### 4. TASK
- **Role**: Agent/module identity
- **Objective**: What to accomplish
- **Quality standards**: Score thresholds, requirements
- **Constraints**: Limitations, restrictions, boundaries

### 5. STEPS
- **3-7 actionable steps** (H3 headers: `### Step 1: ...`)
- Each step: What to do, how to do it, what output
- Use code blocks for examples
- Reference files explicitly

### 6. VALIDATION
- **Quality gates**: ✅ Checks (minimum 3-5)
- **Thresholds**: Score ≥7.0/10.0 (general) | ≥0.85 (doc sync)
- **Self-validation**: Agent checks own output
- **Error handling**: What to do if validation fails

### 7. CONTEXT
- **Usage**: When to use this HOP
- **Upstream**: What comes before (dependencies)
- **Downstream**: What comes after (consumers)
- **$arguments chaining**: How data flows between phases
- **Assumptions**: What agent can assume

---

## PITER Framework (Execution Pattern)

**5-Phase Autonomous Execution**:

### P - Prompt
- Entry instructions and context
- User request parsing
- Goal identification

### I - Identify
- Find relevant files (discovery-first)
- Locate dependencies
- Identify patterns in codebase

### T - Trigger
- Execute builders/validators/commands
- Run workflows (ADW)
- Chain $arguments between phases

### E - Environment
- Check context (files, permissions)
- Verify tools available
- Validate prerequisites met

### R - Review
- Validate outputs against quality gates
- Self-improvement loop
- Iterate if needed

---

## Meta-Construction Principles

1. **Meta > Instance** - Build builders, not artifacts
2. **OPOP** - One-Prompt-One-Purpose (modularity)
3. **[VARIABLES]** - Intentional blanks for entropy
4. **$arguments** - Explicit data flow chaining
5. **Isolation** - Self-contained, no hidden deps
6. **Trinity** - .md + .llm.json + .meta.json
7. **Information-Dense** - Keywords, MAX 1000 LINES
8. **ADW Pattern** - Plan→Code→Test→Review→Document

---

## ADW Pattern (Agentic Developer Workflow)

**5-Phase Pattern** for complex construction:

1. **Plan** - Define [VARIABLES], design structure
2. **Code** - Execute builders, generate artifacts
3. **Test** - Run validators, quality gates
4. **Review** - Analyze results, identify improvements
5. **Document** - README, CHANGELOG, migration guides

**$arguments Chaining**:
```
Phase 1 → $plan
Phase 2 → $artifacts (uses $plan)
Phase 3 → $test_results (uses $artifacts)
Phase 4 → $review_notes (uses $test_results)
Phase 5 → $final_docs (uses $all_context)
```

---

## Quality Thresholds

- **General HOPs**: Score ≥7.0/10.0
- **Documentation Sync**: Score ≥0.85
- **File Size**: MAX 1000 LINES
- **OPOP Compliance**: 10/10
- **[VARIABLES] Limit**: ≤15 in docs (examples allowed)
- **Trinity Output**: 3 files (.md + .llm.json + .meta.json)

---

**Version**: 1.0.0 | **Updated**: 2025-11-18
