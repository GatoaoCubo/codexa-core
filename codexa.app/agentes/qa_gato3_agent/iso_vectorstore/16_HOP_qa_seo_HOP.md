<!-- iso_vectorstore -->
<!--
  Source: qa_seo_HOP.md
  Agent: qa_gato3_agent
  Synced: 2025-12-02
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# MODULE_METADATA
id: qa_seo_check
version: 1.0.0
purpose: Auditar SEO de todas as paginas GATO3
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

# STEPS

### 1. Para Cada Pagina
```
a. mcp__browser__extract_html para obter DOM
b. Extrair elementos SEO
c. Validar contra regras
d. Registrar issues
```

### 2. Extracoes
```javascript
// Title
<title>...</title>

// Meta Description
<meta name="description" content="...">

// H1
<h1>...</h1>

// OG Tags
<meta property="og:title" content="...">
<meta property="og:description" content="...">
<meta property="og:image" content="...">

// Canonical
<link rel="canonical" href="...">

// JSON-LD
<script type="application/ld+json">...</script>
```

### 3. Regras de Validacao
```
Title:
  - Presente: ERROR se ausente
  - Comprimento: WARNING se > 60 chars
  - Unico: ERROR se duplicado com outra pagina

Description:
  - Presente: WARNING se ausente
  - Comprimento: WARNING se < 50 ou > 160 chars

H1:
  - Presente: ERROR se ausente
  - Quantidade: WARNING se > 1

OG Tags:
  - og:image: WARNING se ausente

Canonical:
  - Presente: WARNING se ausente

Images:
  - alt: WARNING para cada imagem sem alt
```

### 4. Calcular Score
```
Base: 100 pontos
- ERROR: -10 pontos cada
- WARNING: -3 pontos cada
Score final = max(0, base - deducoes)
```

### 5. Gerar Relatorio
```markdown
## SEO Audit Report

### Score: 85/100

### Issues by Page

#### / (Homepage)
- [ERROR] Missing H1 tag
- [WARN] Description too short (45 chars)

#### /catalogo
- [PASS] All checks passed

### Summary
| Check | Pass | Fail |
|-------|------|------|
| Title | 5 | 0 |
| Description | 4 | 1 |
| H1 | 4 | 1 |
| OG Image | 5 | 0 |

### Recommendations
1. Add H1 to homepage
2. Expand meta description on homepage
```

# VALIDATION

- [ ] Todas as paginas auditadas
- [ ] Nenhum ERROR em paginas criticas
- [ ] Score >= 80

# CONTEXT

**Upstream**: qa_pages_check
**Downstream**: qa_report_generator
**Priority**: MEDIUM (nao bloqueia deploy, mas importante)
