# Phase 4: Enrichment Implementation Plan

**ID**: PHASE-4-ENRICHMENT
**Version**: 1.0.0
**Created**: 2025-11-24
**Status**: READY FOR EXECUTION
**Estimated Effort**: 3-4 hours focused work

---

## Current State Analysis

### Completed Phases

| Phase | Status | Key Deliverables |
|-------|--------|------------------|
| 1. Prompt Layers | COMPLETE | 8 layers in `prompts/layers/` |
| 2. Agents | COMPLETE | 5 agent definitions + TaskBoundary + MultiAgentOrchestrator |
| 3. Real Integration | COMPLETE | src/llm, src/tools, src/runtime, src/auth, codexa.py |

### Phase 4 Gap Analysis

#### HOPs (5 files) - Need Enrichment

| File | Current | Target |
|------|---------|--------|
| 91_meta_build_agent_HOP.md | v1.0.0, standalone | v2.0.0, prompt layer references, TaskBoundary |
| 92_meta_chore_plan_HOP.md | v1.0.0 | v2.0.0, two-phase planning patterns |
| 93_meta_review_HOP.md | v1.0.0 | v2.0.0, walkthrough generation |
| 94_meta_build_prompt_HOP.md | v1.0.0 | v2.0.0, prompt layer composition |
| 96_meta_orchestrate_HOP.md | v1.0.0 | v2.0.0, multi-agent patterns from agents/ |

**Enrichment Pattern**:
```markdown
## PROMPT LAYER COMPOSITION

This HOP composes the following layers:
- 01_identity_layer.md (core identity)
- 02_operating_modes.md (PLANNING mode)
- 03_tool_usage_layer.md (Read, Glob, Grep)
- 08_workflows.md (ADW patterns)

## TASK BOUNDARY

**Mode**: PLANNING | READ_ONLY
**Transitions**:
- From: IDLE → PLANNING (on task start)
- To: EXECUTION (after plan approval)

## ARTIFACT GENERATION

Generates:
- implementation_plan.md (Antigravity pattern)
- task_checklist.md (living document)
```

#### Validators (5 files) - Need ##report

| Validator | Current Output | Target Output |
|-----------|----------------|---------------|
| 07_hop_sync_validator.py | Console only | JSON + MD report |
| 09_readme_validator.py | Console only | JSON + MD report |
| 10_taxonomy_validator.py | Console only | JSON + MD report |
| 12_doc_sync_validator.py | Console only | JSON + MD report |
| 16_path_consistency_validator.py | Console only | JSON + MD report |

**Report Structure**:
```json
{
  "validator": "hop_sync_validator",
  "version": "2.0.0",
  "timestamp": "2025-11-24T...",
  "target": "prompts/91_*.md",
  "results": {
    "total_files": 5,
    "passed": 4,
    "failed": 1,
    "warnings": 2
  },
  "issues": [
    {"file": "...", "line": 42, "severity": "error", "message": "..."}
  ],
  "summary": "4/5 HOPs passed validation"
}
```

#### Builders (14 files) - Need src/ Integration

**Current Pattern** (02_agent_meta_constructor.py):
```python
from agent import prompt_claude_code_with_retry  # Old pattern
```

**Target Pattern**:
```python
from src import ProviderFactory, ModelType, ToolExecutor
from builders import TaskBoundary, AgentMode

# Use new providers
provider = ProviderFactory.create_provider(model=ModelType.CLAUDE_OPUS)
result = await provider.complete(messages=[...])

# Track task boundaries
boundary = TaskBoundary(task_id="...", mode=AgentMode.PLANNING)
```

---

## Implementation Roadmap

### Step 1: Create Report Generator Module (30 min)

Create `validators/report_generator.py`:

```python
"""
Report Generator for Validators
Generates JSON and Markdown reports for all validators.
"""
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json

@dataclass
class ValidationResult:
    file: str
    line: int | None
    severity: str  # error, warning, info
    message: str
    rule: str

@dataclass
class ValidationReport:
    validator: str
    version: str
    timestamp: str
    target: str
    results: dict
    issues: list[ValidationResult]
    summary: str

class ReportGenerator:
    def __init__(self, validator_name: str, version: str = "2.0.0"):
        self.validator = validator_name
        self.version = version
        self.issues = []

    def add_issue(self, file: str, severity: str, message: str,
                  line: int = None, rule: str = ""):
        self.issues.append(ValidationResult(
            file=file, line=line, severity=severity,
            message=message, rule=rule
        ))

    def generate_report(self, target: str, passed: int, failed: int,
                       warnings: int) -> ValidationReport:
        return ValidationReport(
            validator=self.validator,
            version=self.version,
            timestamp=datetime.now().isoformat(),
            target=target,
            results={
                "total_files": passed + failed,
                "passed": passed,
                "failed": failed,
                "warnings": warnings
            },
            issues=[asdict(i) for i in self.issues],
            summary=f"{passed}/{passed+failed} files passed validation"
        )

    def save_report(self, report: ValidationReport, output_dir: Path):
        output_dir.mkdir(parents=True, exist_ok=True)

        # JSON report
        json_path = output_dir / f"{self.validator}_report.json"
        with open(json_path, 'w') as f:
            json.dump(asdict(report), f, indent=2)

        # Markdown report
        md_path = output_dir / f"{self.validator}_report.md"
        with open(md_path, 'w') as f:
            f.write(self._to_markdown(report))

        return json_path, md_path

    def _to_markdown(self, report: ValidationReport) -> str:
        md = f"# {report.validator} Report\n\n"
        md += f"**Generated**: {report.timestamp}\n"
        md += f"**Target**: {report.target}\n\n"
        md += f"## Results\n\n"
        md += f"- Passed: {report.results['passed']}\n"
        md += f"- Failed: {report.results['failed']}\n"
        md += f"- Warnings: {report.results['warnings']}\n\n"

        if report.issues:
            md += "## Issues\n\n"
            for issue in report.issues:
                md += f"- **{issue['severity'].upper()}** [{issue['file']}:{issue['line'] or '-'}]: {issue['message']}\n"

        md += f"\n## Summary\n\n{report.summary}\n"
        return md
```

### Step 2: Enrich HOPs (45 min)

**For each HOP, add these sections**:

1. **PROMPT_LAYER_COMPOSITION** - Which layers compose this HOP
2. **TASK_BOUNDARY** - Mode, transitions, constraints
3. **ARTIFACT_OUTPUTS** - What documents are generated
4. **SRC_INTEGRATION** - Reference to src/ modules used

**Priority Order**:
1. 91_meta_build_agent_HOP.md (most used)
2. 94_meta_build_prompt_HOP.md (prompt layer reference)
3. 96_meta_orchestrate_HOP.md (multi-agent patterns)
4. 92_meta_chore_plan_HOP.md
5. 93_meta_review_HOP.md

### Step 3: Update Validators with ##report (45 min)

**For each validator**:

1. Import ReportGenerator
2. Add `--output-dir` CLI option
3. Collect issues during validation
4. Generate JSON + MD report at end
5. Print summary to console

**Priority**:
1. 07_hop_sync_validator.py (core)
2. 12_doc_sync_validator.py
3. Others follow same pattern

### Step 4: Update Builders with src/ Integration (60 min)

**High-priority builders**:
1. 02_agent_meta_constructor.py - Use src.llm.ProviderFactory
2. 08_prompt_generator.py - Use prompt layer composition
3. 11_doc_sync_builder.py - Use TaskBoundary for parallel execution

**Pattern**:
```python
# Before
from agent import prompt_claude_code_with_retry

# After
from src import ProviderFactory, ModelType, ToolExecutor
from src.auth import check_rate_limit
from builders import TaskBoundary, AgentMode

async def execute_with_provider(prompt: str, model: str = "claude"):
    provider = ProviderFactory.create_provider(
        model=ModelType.CLAUDE_SONNET if model == "sonnet" else ModelType.CLAUDE_OPUS
    )
    await check_rate_limit("claude")
    return await provider.complete(messages=[{"role": "user", "content": prompt}])
```

### Step 5: Update PRIME.md to v2.0.0 (30 min)

Add sections:
- Phase 3 Integration (src/, codexa.py)
- Prompt Layer Composition
- Multi-Agent Orchestration
- Task Boundary System
- ##report Standard

---

## Validation Checklist

After Phase 4 completion:

```bash
# Test HOPs have new sections
grep -l "PROMPT_LAYER_COMPOSITION" prompts/9*_HOP.md | wc -l  # Should be 5

# Test validators generate reports
python validators/07_hop_sync_validator.py --output-dir reports/
ls reports/*.json | wc -l  # Should exist

# Test src/ imports work
python -c "from src import ProviderFactory, ToolExecutor; print('OK')"

# Test codexa.py integration
python codexa.py status
```

---

## Success Criteria

| Metric | Target |
|--------|--------|
| HOPs enriched | 5/5 with v2.0.0 patterns |
| Validators with ##report | 5/5 generating JSON+MD |
| Builders with src/ integration | 3/14 priority builders |
| PRIME.md version | 2.0.0 |

---

## Next Steps After Phase 4

1. **Phase 5**: Standards - CODE_STYLE_GUIDE.md, DESIGN_SYSTEM.md
2. **Phase 6**: Workflows - New ADWs for feature development
3. **Phase 7**: Documentation - Platform analysis, migration guide

---

**Plan Status**: READY FOR EXECUTION
**Estimated Duration**: 3-4 hours
**Complexity**: MEDIUM
**Impact**: HIGH (enables autonomous operation)
