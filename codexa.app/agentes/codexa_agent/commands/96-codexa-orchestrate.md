# /codexa-orchestrate | Orchestrate Multi-Phase Workflow

**Purpose**: Execute multi-phase ADW workflows with $arguments chaining
**Time**: Variable (depends on workflow) | **Output**: Complete workflow result with traceability

---

## QUICK START

```bash
# Interactive mode - provide workflow spec
/codexa-orchestrate

# With workflow file
/codexa-orchestrate --workflow="workflow_spec.json"
```

---

## INPUT

**Required**: `workflow_spec` object containing:
- workflow_id + workflow_name
- phases array (≥3 phases):
  - phase_id, phase_name
  - command_or_hop (what to execute)
  - inputs ($variables with sources)
  - outputs ($variables produced)
  - depends_on (phase dependencies)
  - validation rules
- context_strategy (full_history|last_step|custom)
- failure_handling (stop|continue|retry)

**Optional**:
- context_config (custom context management)
- validation_strict (enforce validation)
- verbose (detailed logging)

---

## WORKFLOW PATTERN

```json
{
  "workflow_id": "example_workflow",
  "phases": [
    {"phase_id": "plan", "command": "/plan", "outputs": ["$plan"]},
    {"phase_id": "build", "depends_on": ["plan"], "inputs": {"$plan": "phase.plan"}, "outputs": ["$artifacts"]},
    {"phase_id": "test", "depends_on": ["build"], "inputs": {"$artifacts": "phase.build"}, "outputs": ["$results"]}
  ],
  "context_strategy": "full_history",
  "failure_handling": "stop"
}
```

---

## STEPS

1. **Parse Workflow Spec**: Extract phases + dependencies + strategies
2. **Build Dependency Graph**: Topological sort | Detect cycles
3. **Initialize Context**: Set up context manager per strategy
4. **Execute Phases Sequentially**:
   - Prepare inputs from context
   - Execute command/HOP
   - Capture outputs
   - Validate if strict mode
   - Update context
   - Handle failures per strategy
5. **Aggregate Results**: Compile $workflow_result with all phase outputs
6. **Generate Report**: Execution log + context chain + final status

---

## VALIDATION

✅ All phases executed in dependency order
✅ No circular dependencies
✅ $arguments properly chained
✅ All outputs captured
✅ Validation rules passed (if strict)
✅ Context managed per strategy
✅ Full traceability

---

## TROUBLESHOOTING

**Circular dependency**: Reorder phases | Remove cycle
**Phase fails**: Check inputs available | Verify command/HOP exists | Review logs
**Arguments not passed**: Check $variable sources | Verify phase outputs
**Context issues**: Adjust context_strategy | Check context_config

---

**Related**: 96_meta_orchestrate_HOP.md (execution logic) | workflows/*.md (examples) | ADW workflows
