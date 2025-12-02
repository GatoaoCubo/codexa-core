<!-- iso_vectorstore -->
<!--
  Source: 100_ADW_QA_WORKFLOW.md
  Agent: qa_gato3_agent
  Synced: 2025-11-30
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# ADW-100: QA Workflow | GATO3 E-commerce

> **Version**: 1.0.0 | **Agent**: qa_gato3_agent | **Type**: Agentic Developer Workflow

---

## IDENTITY

**Purpose**: Automated quality assurance workflow for GATO3 e-commerce platform
**Domain**: E-commerce QA (pages, SEO, accessibility, checkout, chat)
**Output**: QA Report (MD + JSON) with issues and recommendations

---

## TRIGGER

```yaml
triggers:
  - command: /qa-gato3
  - command: /qa-full
  - command: /qa-smoke
  - event: pre-deploy
  - event: scheduled (daily 6am)
```

---

## WORKFLOW PHASES

### Phase 1: DISCOVERY (5 min)

```yaml
phase: discovery
objective: Identify what to test
actions:
  - Load config.json for environment and routes
  - Check which HOPs are available
  - Determine test scope (full/smoke/specific)

outputs:
  - test_plan: List of tests to run
  - environment: production/staging/local
  - scope: full|smoke|pages|seo|a11y|checkout
```

**HOP to use**: None (config loading)

### Phase 2: PAGE VALIDATION (10 min)

```yaml
phase: page_validation
objective: Validate all pages load correctly
actions:
  - For each route in config.routes:
    - Take screenshot
    - Check HTTP status
    - Verify no console errors
    - Check load time < 3s
    - Verify all images loaded

outputs:
  - page_results: Array of page validations
  - screenshots: Captured for each page
  - errors: Any page failures
```

**HOP to use**: `prompts/qa_pages_HOP.md`

### Phase 3: SEO VALIDATION (5 min)

```yaml
phase: seo_validation
objective: Validate SEO elements on all pages
actions:
  - For each route:
    - Check <title> present and valid
    - Check <meta description> present
    - Verify single <h1>
    - Check all images have alt text
    - Verify canonical URL
    - Check og:image present

outputs:
  - seo_results: Array of SEO validations
  - seo_score: Overall SEO score
```

**HOP to use**: `prompts/qa_seo_HOP.md`

### Phase 4: ACCESSIBILITY VALIDATION (5 min)

```yaml
phase: a11y_validation
objective: WCAG 2.1 AA compliance check
actions:
  - For priority pages (critical+high):
    - Check color contrast
    - Verify keyboard navigation
    - Check ARIA labels
    - Verify form labels
    - Check focus visibility

outputs:
  - a11y_results: Array of a11y validations
  - a11y_score: WCAG compliance score
```

**HOP to use**: `prompts/qa_a11y_HOP.md`

### Phase 5: CHECKOUT FLOW (5 min)

```yaml
phase: checkout_validation
objective: End-to-end checkout flow test
actions:
  - Navigate to catalog
  - Add product to cart
  - Open cart drawer
  - Verify cart contents
  - Click checkout
  - Verify Shopify redirect

outputs:
  - checkout_result: pass/fail
  - checkout_steps: Step-by-step results
  - checkout_errors: Any failures
```

**HOP to use**: `prompts/qa_checkout_HOP.md`

### Phase 6: REPORT GENERATION (2 min)

```yaml
phase: report_generation
objective: Generate comprehensive QA report
actions:
  - Aggregate all phase results
  - Calculate overall scores
  - Prioritize issues (P0/P1/P2)
  - Generate recommendations
  - Create MD and JSON reports

outputs:
  - qa_report.md: Human-readable report
  - qa_report.json: Structured data
  - summary: Executive summary
```

---

## EXECUTION MODES

### Full QA (30 min)

```bash
/qa-gato3 --mode full
```

Runs all phases on all routes.

### Smoke Test (10 min)

```bash
/qa-gato3 --mode smoke
```

Runs only critical pages + checkout flow.

### Specific Check

```bash
/qa-gato3 --mode seo
/qa-gato3 --mode a11y
/qa-gato3 --mode checkout
```

Runs specific phase only.

---

## QUALITY GATES

```yaml
quality_gates:
  critical:
    - All critical pages load (HTTP 200)
    - Checkout flow completes
    - No P0 issues

  release_ready:
    - Pass rate >= 95%
    - SEO score >= 80%
    - A11y score >= 80%
    - No P0 or P1 issues
```

---

## TOOLS REQUIRED

| Tool | Usage |
|------|-------|
| mcp__browser__screenshot | Page captures |
| mcp__browser__extract_text | Content extraction |
| mcp__browser__extract_html | SEO element checks |
| Bash | npm commands, lighthouse |
| Grep | Code pattern search |

---

## OUTPUT LOCATION

```
qa_gato3_agent/reports/
├── qa_report_YYYYMMDD_HHMMSS.md
├── qa_report_YYYYMMDD_HHMMSS.json
└── screenshots/
    ├── home.png
    ├── catalogo.png
    └── ...
```

---

## INTEGRATION

**Upstream**: None (entry point)
**Downstream**: Deploy pipeline (blocks if P0 issues)

---

**Created by**: qa_gato3_agent v1.0.0
**Last Updated**: 2025-11-30
