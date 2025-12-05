<!-- iso_vectorstore -->
<!--
  Source: qa_seo_HOP.md
  Agent: qa_agent
  Synced: 2025-12-05
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# MODULE_METADATA
id: qa_seo_check
version: 1.0.0
purpose: Auditar SEO de todas as paginas {{BRAND_NAME}}
category: qa/seo
dependencies: [browser_mcp]

# INPUT_CONTRACT
$base_url: string
$routes: array

# OUTPUT_CONTRACT
$report: SEOReport {
  total_pages: number,
  issues: SEOIssue[],
  score: number,
  recommendations: string[]
}

# TASK

**Role**: SEO Auditor
**Objective**: Verificar elementos SEO essenciais em todas as paginas

## Checklist
- Title tag (presente, unico, < 60 chars)
- Meta description (presente, 50-160 chars)
- H1 (unico por pagina)
- Open Graph tags (og:title, og:description, og:image)
- Canonical URL
- Structured Data (JSON-LD)
- Alt text em imagens

# VALIDATION

- [ ] Todas as paginas auditadas
- [ ] Nenhum ERROR em paginas criticas
- [ ] Score >= 80

# CONTEXT

**Upstream**: qa_pages_check
**Downstream**: qa_report_generator
**Priority**: MEDIUM (nao bloqueia deploy, mas importante)
