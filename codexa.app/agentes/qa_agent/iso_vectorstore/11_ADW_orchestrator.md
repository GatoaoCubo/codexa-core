<!-- iso_vectorstore -->
<!--
  Source: 100_ADW_QA_WORKFLOW.md
  Agent: qa_agent
  Synced: 2025-12-05
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# ADW-100: QA Workflow | {{BRAND_NAME}} E-commerce

> **Version**: 1.0.0 | **Agent**: qa_agent | **Type**: Agentic Developer Workflow

---

## IDENTITY

**Purpose**: Automated quality assurance workflow for {{BRAND_NAME}} e-commerce platform
**Domain**: E-commerce QA (pages, SEO, accessibility, checkout, chat)
**Output**: QA Report (MD + JSON) with issues and recommendations

---

## TRIGGER

```yaml
triggers:
  - command: /qa
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

**HOP to use**: `prompts/qa_pages_HOP.md`

### Phase 3: SEO VALIDATION (5 min)

**HOP to use**: `prompts/qa_seo_HOP.md`

### Phase 4: ACCESSIBILITY VALIDATION (5 min)

**HOP to use**: `prompts/qa_a11y_HOP.md`

### Phase 5: CHECKOUT FLOW (5 min)

**HOP to use**: `prompts/qa_checkout_HOP.md`

### Phase 6: REPORT GENERATION (2 min)

---

## EXECUTION MODES

### Full QA (30 min)

```bash
/qa --mode full
```

### Smoke Test (10 min)

```bash
/qa --mode smoke
```

### Specific Check

```bash
/qa --mode seo
/qa --mode a11y
/qa --mode checkout
```

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
qa_agent/reports/
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

**Created by**: qa_agent v1.0.0
**Last Updated**: 2025-12-05
