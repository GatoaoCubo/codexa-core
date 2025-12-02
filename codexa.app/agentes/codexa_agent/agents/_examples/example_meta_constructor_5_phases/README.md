# Example: Meta-Constructor 5-Phase Workflow

> **Example ID**: `dd2b5962`
> **Workflow**: Complete Meta-Constructor (Plan → Build → Test → Review → Document)
> **Model**: Claude Sonnet
> **Execution Date**: 2025-11-13
> **Status**: ✅ All 5 phases completed successfully

## 📋 Overview

This example demonstrates a **complete end-to-end execution** of the CODEXA Meta-Constructor workflow, which creates an AI agent through 5 autonomous phases.

### Input

```
Agent Description: "Create a simple test agent for validating workflow"
Model: sonnet
Target Directory: agents/dd2b5962/agent-artifacts
```

### Output

5 phases executed with full $argument chaining:

```
Phase 1 (Planning)
    ↓ $plan
Phase 2 (Construction)
    ↓ $artifacts
Phase 3 (Testing)
    ↓ $test_results
Phase 4 (Review)
    ↓ $review
Phase 5 (Documentation)
    ↓ $documentation
```

## 🗂️ Directory Structure

```
example_meta_constructor_5_phases/
├── README.md                           # This file
├── meta_construction_summary.json      # Overall workflow metadata (22KB)
│
├── meta-planner-dd2b59/               # PHASE 1: Strategic Planning
│   ├── cc_raw_output.jsonl            # Claude Code streaming output
│   ├── cc_raw_output.json             # Parsed message array
│   ├── cc_final_object.json           # Final response object
│   └── custom_summary_output.json     # Phase 1 execution summary
│
├── meta-builder-dd2b59/               # PHASE 2: Artifact Construction
│   └── [same structure]
│
├── meta-tester-dd2b59/                # PHASE 3: Testing & Validation
│   └── [same structure]
│
├── meta-reviewer-dd2b59/              # PHASE 4: Critical Review
│   └── [same structure]
│
└── meta-documenter-dd2b59/           # PHASE 5: Documentation
    └── [same structure]
```

## 🎯 What This Example Demonstrates

### 1. Multi-Phase Workflow Orchestration

Shows how the meta-constructor chains 5 distinct phases:

- **Phase 1**: Strategic planning with [OPEN_VARIABLES]
- **Phase 2**: Construction based on $plan
- **Phase 3**: Testing based on $artifacts
- **Phase 4**: Review based on $test_results
- **Phase 5**: Documentation based on $all_context

### 2. $argument Chaining

Each phase passes outputs to the next via $arguments:

```bash
# Phase 1 Output → Phase 2 Input
workflow_context["$plan"] = plan_response.output

# Phase 2 Output → Phase 3 Input
workflow_context["$artifacts"] = build_response.output

# And so on...
```

### 3. Structured Outputs

All phases generate consistent metadata:

```json
{
  "agent_name": "meta-planner-dd2b59",
  "adw_id": "dd2b5962",
  "model": "sonnet",
  "status": "completed",
  "timestamp": "2025-11-13T09:08:20.243758",
  "prompt_length": 1677,
  "context_files": []
}
```

### 4. SCOUT Integration

Shows repository context loading:

```
[SCOUT] Loading repository context...
[SCOUT] Indexed 37 files
[SCOUT] Found 3 existing agent files for pattern analysis
```

## 📊 Execution Timeline

| Phase | Name | Duration | Status |
|-------|------|----------|--------|
| 1 | Strategic Planning | ~3s | ✅ Success |
| 2 | Artifact Construction | ~3s | ✅ Success |
| 3 | Testing & Validation | ~3s | ✅ Success |
| 4 | Critical Review | ~3s | ✅ Success |
| 5 | Documentation | ~3s | ✅ Success |
| **Total** | | **~15s** | ✅ All phases completed |

## 🔍 Key Files to Examine

### Overall Summary

```bash
cat meta_construction_summary.json
```

Contains:
- ADW ID and agent description
- All 5 phase results
- Workflow-level metadata
- SCOUT context summary

### Phase-Specific Summaries

```bash
# See what each phase generated
cat meta-planner-dd2b59/custom_summary_output.json
cat meta-builder-dd2b59/custom_summary_output.json
cat meta-tester-dd2b59/custom_summary_output.json
cat meta-reviewer-dd2b59/custom_summary_output.json
cat meta-documenter-dd2b59/custom_summary_output.json
```

### Final Agent Output

```bash
# See the final Claude Code response from Phase 5
cat meta-documenter-dd2b59/cc_final_object.json
```

## 🧪 How to Reproduce

Run the same workflow:

```bash
python builders/02_agent_meta_constructor.py \
  "Create a simple test agent for validating workflow" \
  --model sonnet \
  --verbose
```

This will:
1. Generate a new ADW ID (e.g., `a1b2c3d4`)
2. Execute all 5 phases
3. Create output in `agents/a1b2c3d4/`
4. Generate similar structure to this example

## 📝 Lessons from This Example

### What Worked Well

✅ **$argument chaining**: Each phase correctly received context from previous phases
✅ **SCOUT integration**: Repository context loaded successfully
✅ **Structured outputs**: All phases generated consistent JSON metadata
✅ **Error handling**: No failures, graceful execution
✅ **Metadata tracking**: Complete execution trace preserved

### Key Patterns

1. **Agent Naming Convention**: `meta-{role}-{adw_id_prefix}`
   - Example: `meta-planner-dd2b59`

2. **Output Files**: Always 4 files per phase
   - `cc_raw_output.jsonl` - Streaming output
   - `cc_raw_output.json` - Message array
   - `cc_final_object.json` - Final result
   - `custom_summary_output.json` - Metadata

3. **Summary Structure**: Consistent across phases
   ```json
   {
     "agent_name": "...",
     "adw_id": "...",
     "model": "...",
     "status": "completed",
     "timestamp": "...",
     "prompt_length": 1677
   }
   ```

## 🚀 Using This Example

### As a Template

```bash
# Copy structure for new workflow
cp -r example_meta_constructor_5_phases my_new_workflow
```

### For Testing

```bash
# Validate output structure
python validators/09_readme_validator.py --file example_meta_constructor_5_phases/
```

### For Documentation

Reference this example when explaining:
- How meta-constructor works
- $argument chaining patterns
- Output structure conventions
- SCOUT integration

## 🔗 Related

- **Builder**: `builders/02_agent_meta_constructor.py`
- **Workflow**: `workflows/97_ADW_NEW_AGENT_WORKFLOW.md`
- **Command**: `commands/91_codexa_build_agent.md`
- **Documentation**: `agents/README.md`

---

**Status**: ✅ Complete and validated
**Purpose**: Reference example for meta-constructor workflow
**Maintained**: Yes (tracked in git)
