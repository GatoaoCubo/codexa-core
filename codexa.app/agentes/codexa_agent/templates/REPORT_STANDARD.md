# ##report STANDARD | Structured Reporting for All Builders/Validators/Workflows

**Version**: 1.0.0 | **Created**: 2025-11-24
**Purpose**: Define mandatory reporting format for all CODEXA meta-construction components
**Type**: Standard Specification
**Applies To**: All builders/* | All validators/* | All workflows/*

---

## 🎯 PURPOSE

Every builder, validator, and workflow in CODEXA MUST output a structured report following this standard. This ensures:
- **Transparency**: Clear visibility into what happened
- **Traceability**: Full audit trail of operations
- **Composability**: Outputs can be chained to next phase
- **Debugging**: Easy identification of failures
- **Monitoring**: Metrics for performance tracking

**Rule**: If it executes, it reports. No exceptions.

---

## 📋 REPORT STRUCTURE

Every ##report MUST include BOTH formats:
1. **Markdown Report** (.md) - Human-readable, formatted
2. **JSON Report** (.json) - Machine-parsable, structured

### Report Naming Convention
```
{component_name}_report_{timestamp}.md
{component_name}_report_{timestamp}.json
```

Examples:
- `agent_meta_constructor_report_20251124_143052.md`
- `hop_sync_validator_report_20251124_143052.json`
- `doc_sync_workflow_report_20251124_143052.md`

---

## 📦 MANDATORY SECTIONS (Markdown)

### 1. HEADER (Metadata)
```markdown
# ##report | {Component Name} Execution Report

**Component**: {builder|validator|workflow} | {component_id}
**Version**: {component_version}
**Execution ID**: {unique_execution_id}
**Timestamp Start**: {ISO-8601}
**Timestamp End**: {ISO-8601}
**Duration**: {seconds}s
**Status**: {SUCCESS|PARTIAL|FAILURE}
```

### 2. SUMMARY (Executive Overview)
```markdown
## 📊 SUMMARY

**Status**: {✅ SUCCESS | ⚠️ PARTIAL | ❌ FAILURE}
**Score**: {metric_score}/100 (if applicable)
**Items Processed**: {count}
**Items Passed**: {count}
**Items Failed**: {count}
**Warnings**: {count}
**Errors**: {count}

**Key Metrics**:
- Metric 1: {value} {unit}
- Metric 2: {value} {unit}
- Metric N: {value} {unit}
```

### 3. INPUTS (What Was Provided)
```markdown
## 📥 INPUTS

**Arguments Received**:
- `$arg1`: {value}
- `$arg2`: {value}
- `$argN`: {value}

**Files Read**: {count}
**Configuration**: {config_summary}
**Environment**: {env_details}
```

### 4. EXECUTION (What Happened)
```markdown
## ⚙️ EXECUTION

### Phase 1: {Phase Name}
**Duration**: {seconds}s
**Status**: {✅|⚠️|❌}
**Actions**: {count}
**Output**: {summary}

### Phase 2: {Phase Name}
...

### Phase N: {Phase Name}
...
```

### 5. OUTPUTS (What Was Generated)
```markdown
## 📤 OUTPUTS

**Primary Outputs**:
- `$output1`: {value} ({type})
- `$output2`: {value} ({type})

**Files Created**: {count}
- {file_path_1} ({size})
- {file_path_2} ({size})

**Files Modified**: {count}
- {file_path_1}
- {file_path_2}

**Files Deleted**: {count} (if applicable)
```

### 6. VALIDATION (Quality Gates)
```markdown
## ✅ VALIDATION

**Quality Gates**:
- ✅ Gate 1: {description} - PASSED
- ⚠️ Gate 2: {description} - WARNING ({reason})
- ❌ Gate 3: {description} - FAILED ({reason})

**Quality Score**: {score}/100

**Threshold**: {min_acceptable}
**Result**: {PASS|FAIL}
```

### 7. ISSUES (Problems Encountered)
```markdown
## 🐛 ISSUES

<If no issues: "No issues encountered.">

<If issues exist:>

### Issue #1: {Title}
**Severity**: {CRITICAL|HIGH|MEDIUM|LOW}
**Phase**: {phase_name}
**Description**: {what_went_wrong}
**Impact**: {how_it_affects_output}
**Suggested Fix**: {actionable_solution}
**Stack Trace**: {if_applicable}

### Issue #2: {Title}
...
```

### 8. RECOMMENDATIONS (Next Steps)
```markdown
## 💡 RECOMMENDATIONS

**Immediate Actions**:
1. {action_1}
2. {action_2}

**Future Improvements**:
- {improvement_1}
- {improvement_2}

**Next Phase**: {what_to_do_next}
```

### 9. FOOTER (Compliance)
```markdown
---

**Report Generated**: {ISO-8601}
**Report Version**: 1.0.0 (REPORT_STANDARD.md)
**Compliant**: ✅ All mandatory sections present
**Location**: `{report_file_path}`
```

---

## 🔧 JSON STRUCTURE (Mandatory Fields)

```json
{
  "report_metadata": {
    "component_type": "builder|validator|workflow",
    "component_name": "string",
    "component_version": "string",
    "execution_id": "string (UUID or short_id)",
    "timestamp_start": "ISO-8601",
    "timestamp_end": "ISO-8601",
    "duration_seconds": "float",
    "status": "SUCCESS|PARTIAL|FAILURE"
  },
  "summary": {
    "status": "SUCCESS|PARTIAL|FAILURE",
    "score": "float (0-100, null if N/A)",
    "items_processed": "integer",
    "items_passed": "integer",
    "items_failed": "integer",
    "warnings_count": "integer",
    "errors_count": "integer",
    "key_metrics": {
      "metric_name": "value"
    }
  },
  "inputs": {
    "arguments": {
      "$arg_name": "value"
    },
    "files_read": ["array of paths"],
    "configuration": {},
    "environment": {}
  },
  "execution": {
    "phases": [
      {
        "phase_number": "integer",
        "phase_name": "string",
        "duration_seconds": "float",
        "status": "SUCCESS|PARTIAL|FAILURE",
        "actions_count": "integer",
        "output_summary": "string"
      }
    ]
  },
  "outputs": {
    "primary_outputs": {
      "$output_name": {
        "value": "any",
        "type": "string"
      }
    },
    "files_created": [
      {
        "path": "string",
        "size_bytes": "integer"
      }
    ],
    "files_modified": ["array of paths"],
    "files_deleted": ["array of paths"]
  },
  "validation": {
    "quality_gates": [
      {
        "gate_id": "string",
        "description": "string",
        "status": "PASSED|WARNING|FAILED",
        "reason": "string (if not passed)"
      }
    ],
    "quality_score": "float (0-100)",
    "threshold": "float",
    "result": "PASS|FAIL"
  },
  "issues": [
    {
      "issue_id": "integer",
      "title": "string",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "phase": "string",
      "description": "string",
      "impact": "string",
      "suggested_fix": "string",
      "stack_trace": "string (optional)"
    }
  ],
  "recommendations": {
    "immediate_actions": ["array of strings"],
    "future_improvements": ["array of strings"],
    "next_phase": "string"
  },
  "report_compliance": {
    "report_version": "1.0.0",
    "all_sections_present": "boolean",
    "generated_at": "ISO-8601",
    "report_path_md": "string",
    "report_path_json": "string"
  }
}
```

---

## 🎯 IMPLEMENTATION GUIDELINES

### For Builders

**When to Report**:
- After successful build completion
- After partial completion (some artifacts created)
- After failure (document what was attempted)

**Required Metrics**:
- Artifacts created count
- Files generated (paths + sizes)
- Build quality score (if applicable)
- Duration per phase

**Example**: `builders/02_agent_meta_constructor.py` after 5-phase ADW completion

### For Validators

**When to Report**:
- After validation run (pass or fail)

**Required Metrics**:
- Files validated count
- Validation score (0-100)
- Issues found (categorized by severity)
- Compliance percentage

**Example**: `validators/07_hop_sync_validator.py` after checking TAC-7 compliance

### For Workflows

**When to Report**:
- After each major phase
- After workflow completion (final summary report)

**Required Metrics**:
- Phases completed
- Overall workflow status
- Per-phase duration
- Total items processed

**Example**: `workflows/100_ADW_DOC_SYNC_WORKFLOW` after syncing all agents

---

## 📝 PYTHON IMPLEMENTATION TEMPLATE

```python
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

class ReportGenerator:
    """Standard report generator for CODEXA components."""

    def __init__(
        self,
        component_type: str,
        component_name: str,
        component_version: str,
        execution_id: str
    ):
        self.component_type = component_type
        self.component_name = component_name
        self.component_version = component_version
        self.execution_id = execution_id
        self.timestamp_start = datetime.now().isoformat()
        self.timestamp_end = None
        self.phases = []
        self.issues = []

    def add_phase(self, name: str, duration: float, status: str, actions: int, output: str):
        """Record a phase execution."""
        self.phases.append({
            "phase_number": len(self.phases) + 1,
            "phase_name": name,
            "duration_seconds": duration,
            "status": status,
            "actions_count": actions,
            "output_summary": output
        })

    def add_issue(self, title: str, severity: str, phase: str, description: str,
                  impact: str, fix: str, stack: str = None):
        """Record an issue."""
        self.issues.append({
            "issue_id": len(self.issues) + 1,
            "title": title,
            "severity": severity,
            "phase": phase,
            "description": description,
            "impact": impact,
            "suggested_fix": fix,
            "stack_trace": stack
        })

    def generate(
        self,
        status: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        validation: Dict[str, Any],
        recommendations: Dict[str, List[str]],
        output_dir: str
    ) -> tuple[str, str]:
        """Generate both MD and JSON reports.

        Returns:
            tuple: (markdown_path, json_path)
        """
        self.timestamp_end = datetime.now().isoformat()
        start = datetime.fromisoformat(self.timestamp_start)
        end = datetime.fromisoformat(self.timestamp_end)
        duration = (end - start).total_seconds()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_name = f"{self.component_name}_report_{timestamp}"

        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        # Generate JSON report
        json_report = self._generate_json(status, inputs, outputs, validation,
                                          recommendations, duration)
        json_path = Path(output_dir) / f"{report_name}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_report, f, indent=2, ensure_ascii=False)

        # Generate Markdown report
        md_report = self._generate_markdown(json_report)
        md_path = Path(output_dir) / f"{report_name}.md"
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_report)

        return str(md_path), str(json_path)

    def _generate_json(self, status, inputs, outputs, validation, recommendations, duration):
        """Generate JSON structure."""
        return {
            "report_metadata": {
                "component_type": self.component_type,
                "component_name": self.component_name,
                "component_version": self.component_version,
                "execution_id": self.execution_id,
                "timestamp_start": self.timestamp_start,
                "timestamp_end": self.timestamp_end,
                "duration_seconds": duration,
                "status": status
            },
            "summary": {
                "status": status,
                "score": validation.get("quality_score"),
                "items_processed": outputs.get("items_processed", 0),
                "items_passed": outputs.get("items_passed", 0),
                "items_failed": outputs.get("items_failed", 0),
                "warnings_count": len([i for i in self.issues if i["severity"] in ["MEDIUM", "LOW"]]),
                "errors_count": len([i for i in self.issues if i["severity"] in ["CRITICAL", "HIGH"]]),
                "key_metrics": outputs.get("metrics", {})
            },
            "inputs": inputs,
            "execution": {"phases": self.phases},
            "outputs": outputs,
            "validation": validation,
            "issues": self.issues,
            "recommendations": recommendations,
            "report_compliance": {
                "report_version": "1.0.0",
                "all_sections_present": True,
                "generated_at": self.timestamp_end
            }
        }

    def _generate_markdown(self, json_data: Dict) -> str:
        """Generate Markdown from JSON data."""
        md = f"""# ##report | {self.component_name} Execution Report

**Component**: {self.component_type} | {self.component_name}
**Version**: {self.component_version}
**Execution ID**: {self.execution_id}
**Timestamp Start**: {self.timestamp_start}
**Timestamp End**: {self.timestamp_end}
**Duration**: {json_data['report_metadata']['duration_seconds']:.2f}s
**Status**: {json_data['report_metadata']['status']}

---

## 📊 SUMMARY

**Status**: {self._status_emoji(json_data['summary']['status'])}
**Score**: {json_data['summary'].get('score', 'N/A')}/100
**Items Processed**: {json_data['summary']['items_processed']}
**Items Passed**: {json_data['summary']['items_passed']}
**Items Failed**: {json_data['summary']['items_failed']}
**Warnings**: {json_data['summary']['warnings_count']}
**Errors**: {json_data['summary']['errors_count']}

**Key Metrics**:
{self._format_metrics(json_data['summary']['key_metrics'])}

---

## 📥 INPUTS

**Arguments Received**:
{self._format_dict(json_data['inputs'].get('arguments', {}))}

---

## ⚙️ EXECUTION

{self._format_phases(json_data['execution']['phases'])}

---

## 📤 OUTPUTS

**Primary Outputs**:
{self._format_dict(json_data['outputs'].get('primary_outputs', {}))}

**Files Created**: {len(json_data['outputs'].get('files_created', []))}
{self._format_files(json_data['outputs'].get('files_created', []))}

---

## ✅ VALIDATION

{self._format_validation(json_data['validation'])}

---

## 🐛 ISSUES

{self._format_issues(json_data['issues'])}

---

## 💡 RECOMMENDATIONS

**Immediate Actions**:
{self._format_list(json_data['recommendations'].get('immediate_actions', []))}

**Future Improvements**:
{self._format_list(json_data['recommendations'].get('future_improvements', []))}

---

**Report Generated**: {json_data['report_compliance']['generated_at']}
**Report Version**: {json_data['report_compliance']['report_version']} (REPORT_STANDARD.md)
**Compliant**: ✅ All mandatory sections present
"""
        return md

    def _status_emoji(self, status: str) -> str:
        return {"SUCCESS": "✅ SUCCESS", "PARTIAL": "⚠️ PARTIAL", "FAILURE": "❌ FAILURE"}.get(status, status)

    def _format_metrics(self, metrics: Dict) -> str:
        return "\n".join(f"- {k}: {v}" for k, v in metrics.items()) if metrics else "- None"

    def _format_dict(self, d: Dict) -> str:
        return "\n".join(f"- `{k}`: {v}" for k, v in d.items()) if d else "- None"

    def _format_list(self, lst: List) -> str:
        return "\n".join(f"{i+1}. {item}" for i, item in enumerate(lst)) if lst else "- None"

    def _format_phases(self, phases: List) -> str:
        return "\n\n".join(
            f"### Phase {p['phase_number']}: {p['phase_name']}\n"
            f"**Duration**: {p['duration_seconds']:.2f}s\n"
            f"**Status**: {self._status_emoji(p['status'])}\n"
            f"**Actions**: {p['actions_count']}\n"
            f"**Output**: {p['output_summary']}"
            for p in phases
        ) if phases else "No phases recorded"

    def _format_files(self, files: List) -> str:
        return "\n".join(f"- `{f['path']}` ({f.get('size_bytes', 0)} bytes)" for f in files) if files else ""

    def _format_validation(self, validation: Dict) -> str:
        gates = validation.get('quality_gates', [])
        gates_text = "\n".join(
            f"- {self._status_emoji(g['status'])} {g['description']}"
            + (f" - {g.get('reason', '')}" if g['status'] != 'PASSED' else "")
            for g in gates
        ) if gates else "- No quality gates defined"

        return f"""**Quality Gates**:
{gates_text}

**Quality Score**: {validation.get('quality_score', 'N/A')}/100
**Threshold**: {validation.get('threshold', 'N/A')}
**Result**: {validation.get('result', 'N/A')}"""

    def _format_issues(self, issues: List) -> str:
        if not issues:
            return "No issues encountered."

        return "\n\n".join(
            f"### Issue #{i['issue_id']}: {i['title']}\n"
            f"**Severity**: {i['severity']}\n"
            f"**Phase**: {i['phase']}\n"
            f"**Description**: {i['description']}\n"
            f"**Impact**: {i['impact']}\n"
            f"**Suggested Fix**: {i['suggested_fix']}"
            for i in issues
        )
```

### Usage Example

```python
from report_generator import ReportGenerator

# Initialize reporter
reporter = ReportGenerator(
    component_type="builder",
    component_name="agent_meta_constructor",
    component_version="1.0.0",
    execution_id="abc123"
)

# Record phases
reporter.add_phase("Planning", 5.2, "SUCCESS", 3, "Plan created")
reporter.add_phase("Building", 12.5, "SUCCESS", 8, "Artifacts generated")

# Record issues (if any)
reporter.add_issue(
    title="Missing validation",
    severity="MEDIUM",
    phase="Building",
    description="Output schema validation skipped",
    impact="May produce invalid JSON",
    fix="Add schema validation in build phase"
)

# Generate reports
md_path, json_path = reporter.generate(
    status="SUCCESS",
    inputs={"arguments": {"$agent_description": "Test agent"}},
    outputs={"primary_outputs": {"$agent_name": "test-agent"}, "files_created": []},
    validation={"quality_score": 85, "quality_gates": [], "threshold": 70, "result": "PASS"},
    recommendations={
        "immediate_actions": ["Deploy to staging"],
        "future_improvements": ["Add more tests"]
    },
    output_dir="outputs/reports/"
)

print(f"Reports generated: {md_path}, {json_path}")
```

---

## ✅ COMPLIANCE CHECKLIST

Before releasing any builder/validator/workflow, verify:

- [ ] Component generates ##report on every execution
- [ ] Report includes all 9 mandatory sections (MD)
- [ ] Report includes all mandatory JSON fields
- [ ] Reports saved to appropriate directory
- [ ] Reports timestamped correctly
- [ ] Status reflects reality (SUCCESS/PARTIAL/FAILURE)
- [ ] Metrics are accurate
- [ ] Issues documented with severity
- [ ] Recommendations actionable
- [ ] Both MD and JSON formats generated

---

## 📚 RELATED STANDARDS

- `PRIME.md` - Principle #12: ##report Standard
- `templates/docs/README_TEMPLATE.md` - Documentation structure
- `validators/` - Validation patterns

---

**Version**: 1.0.0
**Created**: 2025-11-24
**Maintainer**: CODEXA Team
**Status**: ✅ Official Standard - Mandatory for all components
