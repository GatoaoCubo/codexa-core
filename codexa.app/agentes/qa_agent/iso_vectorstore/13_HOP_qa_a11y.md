<!-- iso_vectorstore -->
<!--
  Source: qa_a11y_HOP.md
  Agent: qa_agent
  Synced: 2025-12-05
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# MODULE_METADATA
id: qa_accessibility_check
version: 1.0.0
purpose: Auditar acessibilidade WCAG 2.1 AA do {{BRAND_NAME}}
category: qa/accessibility
dependencies: [browser_mcp, grep]

# INPUT_CONTRACT
$base_url: string
$routes: array
$wcag_level: string ("AA" default)

# OUTPUT_CONTRACT
$report: A11yReport {
  total_issues: number,
  critical: number,
  major: number,
  minor: number,
  score: number,
  details: A11yIssue[]
}

# TASK

**Role**: Accessibility Auditor
**Objective**: Verificar conformidade WCAG 2.1 AA

## Checks
1. Skip link presente
2. ARIA labels em elementos interativos
3. Form labels associados
4. Heading hierarchy (h1 > h2 > h3)
5. Alt text em imagens
6. Focus visible em tab
7. Contraste de cores (se possivel)

# VALIDATION

- [ ] Skip link presente
- [ ] Nenhum CRITICAL issue em paginas criticas
- [ ] Score >= 70 para passar

# CONTEXT

**Upstream**: qa_pages_check
**Downstream**: qa_report_generator
**Priority**: MEDIUM
**Standard**: WCAG 2.1 AA
