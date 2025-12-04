<!-- iso_vectorstore -->
<!--
  Source: qa_a11y_HOP.md
  Agent: qa_gato3_agent
  Synced: 2025-12-02
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# MODULE_METADATA
id: qa_accessibility_check
version: 1.0.0
purpose: Auditar acessibilidade WCAG 2.1 AA do GATO3
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

# STEPS

### 1. Verificar Skip Link
```
Buscar no HTML:
<a href="#main-content" class="skip-link">Pular para conteudo</a>

Result: CRITICAL se ausente
```

### 2. Verificar ARIA Labels
```
Buscar buttons e links sem aria-label:
<button>X</button>  // Needs aria-label
<a href="#"><svg></svg></a>  // Needs aria-label

Result: MAJOR para cada encontrado
```

### 3. Verificar Form Labels
```
Buscar inputs sem label associado:
<input type="text" id="name">  // Missing <label for="name">

Ou verificar aria-label presente:
<input type="text" aria-label="Nome completo">

Result: MAJOR para cada input sem label
```

### 4. Verificar Heading Hierarchy
```
Extrair todos os headings:
h1 -> h2 -> h3

Rules:
- Apenas 1 h1 por pagina
- Nao pular niveis (h1 -> h3 sem h2)
- Todos presentes

Result: MINOR para violacoes
```

### 5. Verificar Alt Text
```
Buscar todas as imagens:
<img src="..." alt="">  // Empty alt (decorative OK)
<img src="..." >        // Missing alt (ERROR)

Result: MAJOR para imagens sem alt
```

### 6. Verificar Codigo
```
Usar Grep para verificar patterns no codigo:

# Buttons sem aria-label
Grep("onClick.*>.*</button>", glob="src/**/*.tsx")

# Inputs sem label
Grep("<input(?!.*aria-label)(?!.*id=)", glob="src/**/*.tsx")

# Links vazios
Grep("<a.*href.*>\\s*<", glob="src/**/*.tsx")
```

### 7. Calcular Score
```
Base: 100 pontos
- CRITICAL: -25 pontos
- MAJOR: -10 pontos
- MINOR: -3 pontos

Score = max(0, 100 - deducoes)
```

### 8. Gerar Relatorio
```markdown
## Accessibility Audit Report

### Score: 78/100

### Issues Summary
| Severity | Count |
|----------|-------|
| Critical | 1 |
| Major | 2 |
| Minor | 3 |

### Critical Issues
- Missing skip link (affects keyboard navigation)

### Major Issues
- Cart button missing aria-label
- Search input missing label

### Minor Issues
- Heading hierarchy violation on /b2b
- Decorative image without empty alt
- Focus not visible on mobile menu

### Recommendations
1. Add skip link component
2. Add aria-label to icon buttons
3. Associate labels with form inputs

### WCAG 2.1 AA Compliance
- Perceivable: 80%
- Operable: 75%
- Understandable: 90%
- Robust: 85%
```

# VALIDATION

- [ ] Skip link presente
- [ ] Nenhum CRITICAL issue em paginas criticas
- [ ] Score >= 70 para passar

# CONTEXT

**Upstream**: qa_pages_check
**Downstream**: qa_report_generator
**Priority**: MEDIUM
**Standard**: WCAG 2.1 AA
