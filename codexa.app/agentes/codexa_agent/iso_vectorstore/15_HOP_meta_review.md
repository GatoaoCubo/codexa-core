<!-- iso_vectorstore -->
<!--
  Source: 93_meta_review_HOP.md
  Agent: codexa_agent
  Synced: 2025-11-30
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# 93_meta_review_HOP | Work Review Against Specification

**ID**: meta_review_HOP | **Version**: 2.0.0 | **Created**: 2025-11-24 | **Updated**: 2025-11-24
**Purpose**: Review completed work against specification to ensure requirements are met
**Dependencies**: None | **Category**: reviewer | **Framework**: TAC-7
**Usage**: Quality assurance | Spec compliance | Work validation | Screenshot-based verification

---

## PROMPT_LAYER_COMPOSITION

This HOP composes the following prompt layers for review work:

| Layer | Purpose | Usage in HOP |
|-------|---------|--------------|
| `01_identity_layer.md` | Agent identity & role | Defines reviewer personality |
| `02_operating_modes.md` | 7 operating modes | Uses REVIEW → VERIFICATION flow |
| `03_tool_usage_layer.md` | Tool definitions | Read, Glob, screenshot tools |
| `07_steering_hooks.md` | Behavior steering | Quality gates, thresholds |

**Composition Type**: `VERIFICATION_AGENT` (Identity + Modes + Tools + Steering)

**Runtime Composition**:
```python
from src.runtime import PromptLoader, CompositionType

loader = PromptLoader()
base_prompt = loader.load_composition(CompositionType.VERIFICATION_AGENT)
hop_prompt = loader.load_hop("93_meta_review_HOP")
full_prompt = base_prompt + "\n\n" + hop_prompt
```

---

## TASK_BOUNDARY

**Mode**: REVIEW (READ_ONLY with screenshot capture)

**Mode Transitions**:
```
IDLE → REVIEW (on spec file received)
REVIEW → VERIFICATION (checking requirements)
VERIFICATION → REVIEW (if more items to check)
REVIEW → DOCUMENTATION (generating report)
DOCUMENTATION → IDLE (report complete)
```

**Constraints**:
- READ_ONLY for code analysis (no modifications)
- SCREENSHOT capture enabled (for visual evidence)
- WRITE_ENABLED only for report/image output

**Progress Communication**:
```python
from builders.task_boundary import TaskBoundary, AgentMode

boundary = TaskBoundary(mode=AgentMode.REVIEW, workflow_name="Spec Review")
boundary.add_task("Parse spec", "Parsing specification", estimated_min=3)
boundary.add_task("Check requirements", "Checking requirements", estimated_min=15)
boundary.add_task("Capture screenshots", "Capturing visual evidence", estimated_min=5)
boundary.add_task("Document issues", "Documenting issues", estimated_min=5)
boundary.add_task("Generate report", "Generating review report", estimated_min=3)
```

---

## SRC_INTEGRATION

This HOP integrates with the following `src/` modules:

**Tool Execution** (`src/tools/`):
```python
from src import ToolExecutor, FileTools

executor = ToolExecutor()

# Read spec file
spec_content = await FileTools.read(spec_file)

# Check git diff
git_diff = await BashTools.run("git diff origin/main")

# Glob for test files
tests = await FileTools.glob(f".claude/commands/e2e/test_{feature}*.md")
```

**Report Generation** (`artifacts/generators/`):
```python
from artifacts.generators.report_generator import ReviewReportBuilder, ReportGenerator

report_data = (ReviewReportBuilder()
    .with_feature_name(feature_name)
    .with_decision(decision)
    .with_scores(scores)
    .build())

generator = ReportGenerator()
generator.generate_review_report(report_data, output_path)
```

---

## INPUT_CONTRACT

### Required
- **$spec_file** (string) - Path to specification file | Format: Markdown (spec/*.md) | Validation: File exists, readable | Ex: `"specs/add_dark_mode_20251124.md"`
- **$adw_id** (string) - Workflow ID for tracking | Format: Alphanumeric | Validation: Non-empty | Ex: `"a7b3c2f1"`

### Optional
- **$agent_name** (string) - Name of review agent | Default: "review_agent" | Validation: Valid identifier | Ex: `"dark_mode_reviewer"`
- **$review_image_dir** (string) - Directory to save review screenshots | Default: `agents/{adw_id}/{agent_name}/review_img/` | Validation: Writable path | Ex: `"agents/a7b3/reviewer/screenshots/"`
- **$git_diff_available** (boolean) - Whether git diff is available | Default: true | Validation: Boolean | Ex: true

---

## OUTPUT_CONTRACT

### Primary
- **$review_report** (object) - Complete review assessment
  - Format: Markdown + JSON
  - Structure: `{review_status: "pass|fail|partial", spec_compliance_score: 0-100, features_implemented: [{feature, status: "complete|incomplete|missing", evidence_path}], review_issues: [{issue, severity: "critical|high|medium|low", screenshot_path, suggested_fix}], screenshots: [{path, description, critical: boolean}], recommendation: "approve|revise|reject"}`
  - Validation: All spec requirements checked | ≥1 screenshot for critical features | All issues documented | Clear recommendation

### Secondary
- **$comparison_matrix** (array) - Spec vs Implementation comparison | Structure: `[{requirement, specified, implemented, match: boolean}]`
- **$visual_evidence** (array) - Screenshot proofs | Structure: `[{screenshot_path, feature_verified, pass: boolean}]`

---

## TASK

**Role**: Review Module (CODEXA system)

**Objective**: Systematically compare completed work against specification to verify all requirements are met and document any discrepancies

**Quality Standards**: Thorough comparison | Visual proof for UI changes | Clear issue documentation | Actionable feedback | No false positives/negatives

**Constraints**: Use spec file as single source of truth | Focus only on requirements in spec (no scope creep) | Provide visual evidence for UI features | Document critical path only (not every screen) | Be objective, not prescriptive

**Input**: $spec_file + $adw_id + optional ($agent_name, $review_image_dir, $git_diff_available)
**Output**: $review_report (complete assessment with evidence)

---

## STEPS

### STEP 1: Understand Current Context
**Actions**:
- Check current git branch: `git branch`
- If $git_diff_available:
  - Run: `git diff origin/main` (or appropriate base branch)
  - Analyze changes (files modified, additions, deletions)
  - Note: Continue even if no diff available (review deployed state)
- Identify current environment (local dev, staging, production)
**Output**: Context summary (branch, changes, environment)
**Validation**: Branch identified | Diff analyzed (if available)

### STEP 2: Parse Specification File
**Actions**:
- Read $spec_file completely
- Extract requirements:
  - Feature description (what to build)
  - Acceptance criteria (how to verify)
  - File references (where changes expected)
  - Success metrics (quantitative goals)
- Build requirements checklist: `[{req_id, description, acceptance_criteria, priority}]`
- Identify critical path features (must-have vs nice-to-have)
**Output**: Requirements checklist (structured)
**Validation**: All requirements extracted | Priority assigned | Acceptance criteria clear

### STEP 3: Identify Verification Method
**Purpose**: Determine if review needs UI validation or code-only review
**Actions**:
- Analyze requirement type:
  - **UI Feature**: Requires visual verification (screenshots)
  - **API/Backend**: Requires code inspection + tests
  - **Configuration**: Requires file checks
  - **Documentation**: Requires content review
- If UI feature:
  - Check for e2e test files: `./claude/commands/e2e/test_*.md` matching feature name
  - Use e2e tests as navigation guide ONLY (not as test execution)
- Set verification strategy per requirement
**Output**: Verification plan: `[{req_id, method: "visual|code|test|docs"}]`
**Validation**: Every requirement has method | UI features flagged for screenshots

### STEP 4: Execute Review Per Requirement
**Actions**: For each requirement in checklist:

**4A. Code Review** (if applicable):
- Locate relevant files (from spec or git diff)
- Verify implementation matches spec
- Check edge cases handled
- Document discrepancies

**4B. Visual Review** (if UI feature):
- Navigate to feature in application
- **CRITICAL**: Capture screenshot of feature in action
- Numbering: `01_<descriptive_name>.png`, `02_<descriptive_name>.png`, etc.
- Save to $review_image_dir
- Compare visual result to spec description
- **Target**: 1-5 screenshots showing critical functionality (not entire flow)
- Document visual issues (layout, behavior, missing elements)

**4C. Test Review**:
- Check if tests exist and pass
- Verify test coverage for requirement
- Run relevant tests if needed

**4D. Documentation Review**:
- Verify docs updated (if spec required)
- Check accuracy and completeness

**For each requirement**:
- Status: ✅ Complete | ⚠️ Incomplete | ❌ Missing
- Evidence: Code reference, screenshot path, test results
- Issues: List problems (if any)

**Output**: Per-requirement assessment + screenshots
**Validation**: All requirements checked | Critical features have screenshots | Issues documented

### STEP 5: Document Review Issues
**Purpose**: Capture problems found during review
**Actions**: For each issue discovered:
- **Screenshot**: Capture visual proof of problem
- **Description**: What's wrong (specific, not vague)
- **Severity**:
  - **Critical**: Feature broken/missing, blocks deployment
  - **High**: Major deviation from spec, affects UX significantly
  - **Medium**: Minor deviation, workaround exists
  - **Low**: Cosmetic issue, nice-to-fix
- **Suggested Fix**: Actionable solution (with file:line if possible)
- **Spec Reference**: Which requirement this violates
**Format**:
```markdown
### Issue #1: Dark Mode Toggle Missing from Settings Page
**Severity**: Critical
**Screenshot**: `review_img/03_missing_toggle.png`
**Description**: Spec requires dark mode toggle in Settings > Appearance, but toggle is not present. Only light mode visible.
**Spec Reference**: Section 2.1 "Settings UI Changes"
**Suggested Fix**: Add toggle component in `components/Settings/Appearance.tsx` line 42, follow spec mockup
```
**Output**: Review issues array (0-N issues)
**Validation**: Each issue has screenshot | Severity assigned | Fix suggested | Spec linked

### STEP 6: Calculate Compliance Score
**Actions**:
- Count requirements: Total, Complete, Incomplete, Missing
- Calculate: `compliance_score = (Complete / Total) * 100`
- Weight by priority if specified in spec:
  - Critical requirements: 2x weight
  - High: 1.5x weight
  - Medium: 1x weight
  - Low: 0.5x weight
- Determine review status:
  - **Pass**: compliance_score ≥90% AND no critical issues
  - **Partial**: 70% ≤ compliance_score <90% OR critical issues exist but fixable
  - **Fail**: compliance_score <70% OR critical issues unfixable
**Output**: Compliance score + status
**Validation**: Score calculated | Status assigned | Justification clear

### STEP 7: Generate Review Report
**Actions**:
- Compile all findings into structured report (see Report Format below)
- Copy all screenshots to $review_image_dir
- Create summary (pass/fail, score, issue count)
- Make recommendation:
  - **Approve**: All requirements met, no blockers (may have low-severity issues)
  - **Revise**: Most requirements met, issues need fixing before approval
  - **Reject**: Significant requirements missing, re-work needed
- Save report as:
  - Markdown: `agents/{adw_id}/{agent_name}/review_report.md`
  - JSON: `agents/{adw_id}/{agent_name}/review_report.json`
**Output**: $review_report (both formats)
**Validation**: Report complete | All sections filled | Screenshots referenced | Recommendation clear

### STEP 8: Return $arguments for Next Phase
**Actions**: Prepare outputs for downstream:
- $review_status: "pass|partial|fail"
- $compliance_score: 0-100
- $critical_issues_count: Integer
- $review_report_path: Path to saved report
- $next_action: "deploy|fix|rework" (based on recommendation)
**Output**: $arguments object

---

## REVIEW REPORT FORMAT

```markdown
# Review Report: <Feature Name>

**Spec File**: `<spec_file_path>`
**ADW ID**: <adw_id>
**Reviewer**: <agent_name>
**Review Date**: <timestamp>
**Git Branch**: <branch_name>

---

## 📊 SUMMARY

**Review Status**: <PASS|PARTIAL|FAIL>
**Compliance Score**: <score>/100
**Requirements**: <total> total | <complete> complete | <incomplete> incomplete | <missing> missing
**Issues Found**: <count> (<critical_count> critical, <high_count> high, <medium_count> medium, <low_count> low)
**Recommendation**: <APPROVE|REVISE|REJECT>

---

## ✅ REQUIREMENTS CHECKLIST

### Requirement 1: <Title>
**Status**: ✅ Complete | ⚠️ Incomplete | ❌ Missing
**Evidence**: `<screenshot_path>` or `<code_reference>`
**Notes**: <Observations>

### Requirement 2: <Title>
...

---

## 🖼️ VISUAL EVIDENCE (Screenshots)

1. **`01_feature_main_screen.png`** - Main feature interface showing [describe what's visible]
2. **`02_feature_settings.png`** - Settings panel with [critical element]
3. **`03_edge_case_scenario.png`** - Edge case: [scenario]
...

**Critical Screenshots**: <list paths of must-see screenshots>

---

## 🐛 REVIEW ISSUES

<If no issues: "No issues found. All requirements met.">

<If issues exist:>

### Issue #1: <Title>
**Severity**: <Critical|High|Medium|Low>
**Screenshot**: `<path>`
**Description**: <What's wrong>
**Spec Reference**: <Section>
**Suggested Fix**: <Actionable solution>

### Issue #2: <Title>
...

---

## 📋 COMPARISON MATRIX

| Requirement | Specified | Implemented | Match |
|-------------|-----------|-------------|-------|
| Feature A   | Details X | Details X   | ✅    |
| Feature B   | Details Y | Details Z   | ❌    |
...

---

## 💡 RECOMMENDATION

**<APPROVE|REVISE|REJECT>**

<Reasoning>:
- <Key point 1>
- <Key point 2>
- <Key point 3>

**Next Steps**:
<If APPROVE>: Ready for deployment. Consider addressing low-severity issues in future iteration.
<If REVISE>: Fix <critical_count> critical and <high_count> high-severity issues, then re-review.
<If REJECT>: Significant rework needed. <missing_count> requirements missing. Schedule review after re-implementation.

---

**Review Complete**: <timestamp>
**Report Generated**: ✅
```

---

## VALIDATION

**Quality Gates** (before returning $review_report):
- ✅ **Spec Fully Parsed**: All requirements identified | Verify: Checklist matches spec | Fix: Re-read spec, extract missed requirements
- ✅ **All Requirements Checked**: Every requirement has status | Verify: No "pending" or "unknown" statuses | Fix: Complete review for all items
- ✅ **Visual Evidence Present**: UI features have screenshots (1-5) | Verify: Critical path documented | Fix: Navigate app, capture missing screenshots
- ✅ **Issues Documented**: All problems have severity + fix suggestion | Verify: Issues actionable | Fix: Add details, suggest solutions
- ✅ **Score Calculated**: Compliance score accurate | Verify: Math correct, weighted properly | Fix: Recalculate
- ✅ **Recommendation Justified**: Recommendation matches findings | Verify: Pass/Fail aligns with score + issues | Fix: Re-evaluate recommendation
- ✅ **Screenshots Saved**: All images in $review_image_dir | Verify: Paths correct, files exist | Fix: Copy missing files

**Quality Score** (1-10): Thoroughness 30% | Evidence Quality 30% | Issue Documentation 25% | Actionability 15% | **Min acceptable: 8.0** | If <8.0: Expand weak area

---

## CONTEXT

**Usage**: Feature review post-implementation | Spec compliance verification | QA workflows | Release gates | Visual regression testing

**Upstream**: Spec file created (from planning phase) | Work completed (feature implemented) | Prerequisites: Git repo, spec file, application running (if UI review)

**Downstream**: $review_report → Fix issues (if REVISE) → Re-review (if needed) → Deploy (if APPROVE) | $review_issues → Bug tracker | $screenshots → Documentation/archive

**Argument Chaining**: Typically **AFTER build/test phases** | Pattern: `[Plan] → [Build] → [Test] → meta_review_HOP → $review_report → [Deploy|Fix]`
Example: `step_1: {build_feature} → step_2: {run_tests} → step_3: {hop_module: "93_meta_review_HOP.md", inputs: {$spec_file, $adw_id}} → step_4: {if: $step_3.review_status == "pass", action: deploy}`

**Assumptions**:
- Spec file exists and is authoritative
- Work is "complete" (not mid-development)
- Application accessible (if UI review)
- Git available (for diff)
- Screenshots possible (browser/app access)
- Reviewer is objective (compares to spec, not personal preference)

---

## ARTIFACT_OUTPUTS

This HOP generates the following artifacts:

### Primary Artifacts (Review Files)

| Artifact | Purpose | Location |
|----------|---------|----------|
| `review_report.md` | Human-readable review report | `agents/{adw_id}/{agent_name}/` |
| `review_report.json` | Machine-parsable review data | `agents/{adw_id}/{agent_name}/` |
| `{N}_{description}.png` | Visual evidence screenshots | `agents/{adw_id}/{agent_name}/review_img/` |

### Secondary Artifacts (##report)

| Artifact | Purpose | Location |
|----------|---------|----------|
| `{execution_id}_report.md` | Standardized review report | `outputs/` |
| `{execution_id}_report.json` | Standardized review data | `outputs/` |

**Report Generation**:
```python
from artifacts.generators.report_generator import ReviewReportBuilder, ReportGenerator

report_data = (ReviewReportBuilder()
    .with_feature_name(feature_name)
    .with_decision(review_status)  # APPROVE, REVISE, REJECT
    .with_scores({
        "code_structure": structure_score,
        "code_quality": quality_score,
        "testing": test_score,
        "documentation": doc_score,
        "spec_compliance": compliance_score
    })
    .build())

generator = ReportGenerator()
generator.generate_review_report(report_data, Path(f"agents/{adw_id}/review_report.md"))
```

---

## FEEDBACK_LOOP

**Pattern**: Review → Issues → Fix → Re-Review (Closing the Loop)

**Implementation**:
```python
def review_with_fix_loop(spec_file, adw_id, max_reviews=3):
    for review_round in range(max_reviews):
        # Execute review
        review = execute_review(spec_file, adw_id)

        if review.status == "pass" and review.compliance_score >= 90:
            return {"status": "approved", "report": review.report}

        if review.status == "fail" or review.critical_issues > 0:
            # Trigger fix phase
            fix_results = execute_fixes(review.issues)

            # Re-verify fixes
            continue  # Next review round

    return {"status": "rejected", "reason": "Max reviews exceeded"}
```

**Quality Gates (Before Approval)**:
- Compliance Score ≥ 90%
- No Critical Issues
- All screenshots captured for UI features
- All issues have suggested fixes
- Report complete with all sections

**Walkthrough Generation**:
When `--generate-walkthrough` flag is set, additionally generate:
```python
def generate_walkthrough(screenshots, issues):
    """Generate visual walkthrough document."""
    walkthrough = {
        "title": f"Feature Review Walkthrough - {feature_name}",
        "screenshots": [
            {"path": s.path, "description": s.description, "pass": s.pass}
            for s in screenshots
        ],
        "critical_path": [s for s in screenshots if s.critical],
        "issues_highlighted": issues
    }
    return walkthrough
```

---

**Version**: 2.0.0 | **Updated**: 2025-11-24 | **Maintainer**: CODEXA Team
**Related**: 92_meta_chore_plan_HOP.md (planning) | 91_meta_build_agent_HOP.md (building)

**Changelog v2.0.0**:
- Added PROMPT_LAYER_COMPOSITION section
- Added TASK_BOUNDARY section with REVIEW mode
- Added SRC_INTEGRATION section with code examples
- Added ARTIFACT_OUTPUTS section with ##report integration
- Added FEEDBACK_LOOP section (Review → Fix → Re-Review pattern)
- Added Walkthrough Generation feature
