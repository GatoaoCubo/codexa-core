# 99_ADW_SYSTEM_UPGRADE_WORKFLOW | System-Wide Upgrade Workflow

**Purpose**: Upgrade CODEXA system components (builders, validators, HOPs, agents)
**Type**: 4-Phase ADW | **Duration**: 30-60 minutes (automated with gates)
**Output**: Upgraded system with backwards compatibility + migration guides
**Version**: 2.0.0 | **Updated**: 2025-11-24

---

## WORKFLOW SPECIFICATION

```json
{
  "workflow_id": "system_upgrade",
  "workflow_name": "System-Wide Upgrade Workflow",
  "version": "2.0.0",
  "context_strategy": "full_history",
  "failure_handling": "stop",

  "v2_enhancements": {
    "task_boundaries": true,
    "rollback_points": true,
    "verification_agents": true
  },

  "phases": [
    {"phase_id": "phase_0_knowledge", "phase_name": "Knowledge Loading", "duration": "1-2min", "module": "PHASE_0_KNOWLEDGE_LOADING", "task_hint": "system_upgrade"},
    {"phase_id": "phase_1_plan", "phase_name": "Upgrade Planning", "duration": "5-10min", "description": "Analyze current system + plan upgrade path"},
    {"phase_id": "phase_2_backup", "phase_name": "Backup & Preparation", "duration": "3-5min", "description": "Backup current state + prepare environment"},
    {"phase_id": "phase_3_upgrade", "phase_name": "Execute Upgrade", "duration": "15-30min", "description": "Upgrade components sequentially"},
    {"phase_id": "phase_4_validate", "phase_name": "Validation & Rollback", "duration": "7-15min", "description": "Validate upgrades + rollback if needed"}
  ]
}
```

---

## TASK BOUNDARIES (v2.0.0 Enhancement)

### Per-Component Boundaries
Each upgrade operation declares its scope:
```yaml
TASK_BOUNDARY: UPGRADE_BUILDERS
COMPONENT: builders/
OPERATION: version_upgrade
ROLLBACK_POINT: git_tag_pre_upgrade
VERIFICATION: run_all_builders_help
```

### Rollback Points Strategy
```yaml
rollback_points:
  - id: "pre_upgrade"
    type: git_tag
    created_at: "before Phase 3"

  - id: "post_core"
    type: git_commit
    created_at: "after core modules upgraded"

  - id: "post_builders"
    type: git_commit
    created_at: "after builders upgraded"

  - id: "post_validators"
    type: git_commit
    created_at: "after validators upgraded"
```

### Verification Agent Integration
```yaml
verification_agent:
  access: read_only + test_execution
  triggers:
    - after_each_component_upgrade
    - before_final_commit
  validators:
    - validators/13_code_quality_validator.py
    - validators/07_hop_sync_validator.py
  rollback_on_failure: true
```

---

## PHASE DETAILS

## PHASE 0: Knowledge Loading (Cross-Agent)
**Objective**: Load cross-agent knowledge before execution
**Module**: `builders/adw_modules/PHASE_0_KNOWLEDGE_LOADING.md`
**Task Type**: `system_upgrade`

**Actions**:
1. Detect task type from user request
2. Load knowledge_graph.json from mentor_agent/FONTES/
3. Read required files for task type
4. Read recommended files (if context allows)
5. Store in $knowledge_context

**Output**: $knowledge_context available for all subsequent phases

---

### PHASE 1: Upgrade Planning
**Objective**: Analyze system + plan safe upgrade path
**Actions**: Scan current versions | Check compatibility | Identify breaking changes | Generate upgrade plan
**Tools**: Scout (version detection) | Dependency analyzer
**Input**: Target version / upgrade scope | **Output**: $upgrade_plan `{current_versions{}, target_versions{}, breaking_changes[], migration_steps[], risk_assessment}`
**Validation**: Plan complete | Dependencies resolved | Breaking changes documented

### PHASE 2: Backup & Preparation
**Objective**: Create safe rollback point
**Actions**: Git commit current state | Tag version | Backup configs | Export data | Verify backups
**Input**: $upgrade_plan | **Output**: $backup_info `{commit_sha, tag, backup_paths[], verification_passed}`
**Validation**: Backup complete | Rollback possible | No uncommitted changes

### PHASE 3: Execute Upgrade
**Objective**: Upgrade components in dependency order
**Actions** (sequential):
1. Upgrade core modules (adw_modules/, utils)
2. Upgrade builders (02, 08, 05, etc.)
3. Upgrade validators (07, 09, 10)
4. Upgrade HOPs (91, 94, 96)
5. Upgrade workflows (97, 98, 99)
6. Upgrade agents (all agent directories)
7. Update dependencies (requirements.txt, pyproject.toml)
**Input**: $upgrade_plan, $backup_info | **Output**: $upgrade_results `{components_upgraded[], failures[], warnings[]}`
**Validation**: Each component passes tests after upgrade | No breaking changes introduced | Backwards compatibility maintained

### PHASE 4: Validation & Rollback
**Objective**: Verify system health post-upgrade
**Actions**: Run all validators | Execute test suite | Check integration | Validate docs | If failures: rollback to backup
**Input**: $upgrade_results | **Output**: $validation_report `{all_tests_passed, validators_passed, rollback_performed, final_status}`
**Validation**: All tests pass | All validators green | System functional | Docs updated

---

## UPGRADE TYPES

**MAJOR** (x.0.0): Breaking changes | Requires migration | Full testing
**MINOR** (0.x.0): New features | Backwards compatible | Standard testing
**PATCH** (0.0.x): Bug fixes | No breaking changes | Quick validation

---

## BACKWARDS COMPATIBILITY

**Maintain**: Old HOPs still work | Old commands functional | Existing agents unaffected (unless explicitly upgraded)
**Deprecation Path**: Warn → Deprecate → Remove (across 3 versions minimum)
**Migration Guides**: For all breaking changes | Step-by-step instructions | Example conversions

---

## ROLLBACK PROCEDURE

1. Stop all services
2. Git reset to $backup_info.commit_sha
3. Restore configs from backup
4. Verify system functional
5. Document rollback reason
6. Plan safer upgrade path

---

## SUCCESS CRITERIA

- ✅ All components upgraded successfully
- ✅ All tests pass
- ✅ All validators green
- ✅ Backwards compatibility maintained (or migration guides provided)
- ✅ Documentation updated (version numbers, changelogs)
- ✅ No regressions detected
- ✅ System performance maintained or improved

---

## TROUBLESHOOTING

**Upgrade fails**: Check $upgrade_results.failures | Review logs | Rollback if critical | Fix issue | Retry
**Tests fail**: Identify broken tests | Check if test needs update | Fix code or test | Re-validate
**Validators fail**: Check breaking changes | Update validator if needed | Fix issues | Re-run
**Performance regression**: Profile before/after | Identify bottleneck | Optimize or rollback

---

## INTEGRATION WITH v2.0.0 ADWs

- **203_ADW_PARALLEL_ORCHESTRATION.md**: Use for parallel component upgrades
- **202_ADW_BUG_FIXING.md**: Use for fixing issues discovered during upgrade
- **100_ADW_DOC_SYNC_WORKFLOW.md**: Run after upgrade to sync all documentation

---

**Version**: 2.0.0 | **Updated**: 2025-11-24 | **Maintainer**: CODEXA Team
**Changelog v2.0.0**: Added task boundaries per component, rollback points strategy, verification agent integration
**Related**: All builders/validators/HOPs | PRIME.md | Git | 203_ADW_PARALLEL_ORCHESTRATION.md
