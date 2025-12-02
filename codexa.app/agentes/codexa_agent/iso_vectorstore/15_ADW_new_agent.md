# 97_ADW_NEW_AGENT_WORKFLOW | Complete Agent Creation Workflow

**Purpose**: End-to-end workflow (description → deployment)
**Type**: 5-Phase ADW (Autonomous Document Workflow) | **Duration**: 20-40 minutes (automated)
**Output**: Production-ready agent with full documentation

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "new_agent_creation",
  "workflow_name": "Complete Agent Creation Workflow",
  "version": "1.0.0",
  "context_strategy": "full_history",
  "failure_handling": "stop",

  "phases": [
    {"phase_id": "phase_1_requirements", "phase_name": "Requirements Gathering", "duration": "2-5min", "command": "/codexa-when_to_use", "description": "Clarify agent requirements + choose approach"},
    {"phase_id": "phase_2_planning", "phase_name": "Agent Planning", "duration": "3-6min", "hop_module": "91_meta_build_agent_HOP.md", "sub_phase": "Phase 1 - Strategic Planning", "description": "Create strategic plan with [OPEN_VARIABLES]"},
    {"phase_id": "phase_3_construction", "phase_name": "Agent Construction", "duration": "8-15min", "hop_module": "91_meta_build_agent_HOP.md", "sub_phases": "Phases 2-4", "description": "Build artifacts + test + review"},
    {"phase_id": "phase_4_documentation", "phase_name": "Documentation Generation", "duration": "3-6min", "hop_module": "91_meta_build_agent_HOP.md", "sub_phase": "Phase 5 - Documentation", "description": "Generate complete docs suite"},
    {"phase_id": "phase_5_registration", "phase_name": "System Registration", "duration": "2-4min", "description": "Register agent in CODEXA system"}
  ]
}
```

---

## PHASE DETAILS

### PHASE 1: Requirements Gathering
**Objective**: Clarify agent requirements
**Actions**: Execute /codexa-when_to_use decision tree | User confirms agent build
**Input**: User's initial idea | **Output**: $agent_description (clear 1-3 sentences)
**Validation**: Description has purpose + domain | ≥20 chars

### PHASE 2: Agent Planning
**Objective**: Create strategic plan with [OPEN_VARIABLES]
**Actions**: Invoke 91_meta_build_agent_HOP Phase 1 | Pass $agent_description | Generate plan with creative blanks
**Input**: $agent_description | **Output**: $plan, $agent_name, $specifications
**Validation**: Plan non-empty | Agent name extracted | Specs include purpose/model/capabilities
**Dependencies**: Phase 1

### PHASE 3: Agent Construction
**Objective**: Build all artifacts + test + review
**Actions**:
- Phase 2: Build artifacts (MASTER_INSTRUCTIONS, AGENT_CONFIGURATION, VECTOR_STORE_MANIFEST, OUTPUT_SCHEMA) using $plan
- Phase 3: Test artifacts + create scenarios
- Phase 4: Critical review + quality score
**Input**: $plan (from Phase 2) | **Output**: $artifacts, $test_results, $review_notes, $quality_score
**Validation**: All 4 artifacts created | MASTER_INSTRUCTIONS 2000-5000 words | Valid JSON config | Quality ≥7.0
**Dependencies**: Phase 2

### PHASE 4: Documentation Generation
**Objective**: Generate complete docs
**Actions**: Invoke 91_meta_build_agent_HOP Phase 5 | Pass $all_context | Generate README, DEPLOYMENT_GUIDE, EXAMPLES, META_CONSTRUCTION_LOG
**Input**: $artifacts, $test_results, $review_notes | **Output**: $documentation (4 files)
**Validation**: All docs present | README complete | DEPLOYMENT_GUIDE has steps | EXAMPLES ≥3 | LOG has all phases
**Dependencies**: Phase 3

### PHASE 5: System Registration
**Objective**: Register in CODEXA
**Actions**: Extract agent metadata | Update AGENT_REGISTRY.json | Verify registration
**Input**: $agent_artifacts, $agent_name, $specifications | **Output**: $registration_confirmation
**Validation**: Registry updated | Agent ID unique | Entry complete
**Dependencies**: Phase 4

---

## EXECUTION

**Command**: `uv run builders/02_agent_meta_constructor.py "Your agent description here"`

**Or via orchestrator**:
```bash
# Using 96_meta_orchestrate_HOP with workflow_spec from above
```

---

## SUCCESS CRITERIA

- ✅ All 5 phases completed
- ✅ 8 artifacts created (MASTER_INSTRUCTIONS, AGENT_CONFIGURATION, VECTOR_STORE_MANIFEST, OUTPUT_SCHEMA, README, DEPLOYMENT_GUIDE, EXAMPLES, META_CONSTRUCTION_LOG)
- ✅ Quality score ≥7.0/10.0
- ✅ Agent registered in system
- ✅ No [PLACEHOLDER] text remains
- ✅ Full traceability in META_CONSTRUCTION_LOG

---

## TROUBLESHOOTING

**Phase 2 fails**: Check $agent_description clarity | Ensure 20-500 chars | Verify prerequisites (Python, uv, API key)
**Phase 3 artifacts incomplete**: Re-run Phase 2 with verbose | Check $plan completeness
**Quality <7.0**: Review weakest area from $review_notes | Re-run relevant phase
**Registration fails**: Check AGENT_REGISTRY.json exists | Verify write permissions | Check ID uniqueness

---

**Version**: 1.0.0 | **Updated**: 2025-11-13 | **Maintainer**: CODEXA Team
**Related**: 91_meta_build_agent_HOP.md (execution) | 96_meta_orchestrate_HOP.md (orchestration) | 02_agent_meta_constructor.py (implementation)
