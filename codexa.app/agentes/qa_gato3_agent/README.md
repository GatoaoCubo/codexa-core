# qa_gato3_agent | Quality Assurance Specialist

> **Version**: 1.0.0
> **Type**: QA & Validation
> **Domain**: E-commerce GATO3
> **Created**: 2025-11-28

---

## PURPOSE

Agente especializado em Quality Assurance para o projeto GATO3 (gatoaocubo.lovable.app). Automatiza validacoes de UI, fluxos de usuario, SEO, acessibilidade e integridade do sistema.

## CAPABILITIES

### Core Validations

| Check | Description | Priority |
|-------|-------------|----------|
| Page Load | Verifica se todas as paginas carregam sem erros | CRITICAL |
| Images | Valida se imagens estao acessiveis e otimizadas | HIGH |
| Checkout Flow | Testa fluxo ate redirect para Shopify | CRITICAL |
| Responsiveness | Valida layout em mobile/tablet/desktop | HIGH |
| SEO | Checa title, meta, h1, structured data | MEDIUM |
| Broken Links | Encontra links quebrados internos/externos | HIGH |
| Ronronalda Chat | Testa chatbot AI com cenarios pre-definidos | HIGH |
| B2B Form | Valida formulario de contato B2B | MEDIUM |
| Accessibility | Verifica ARIA labels, contraste, navegacao | MEDIUM |

### Tools Available

- **Browser MCP**: screenshot, screenshot_full, extract_text, extract_html
- **Bash**: Executar comandos, rodar testes, verificar build
- **Read/Grep**: Inspecionar codigo, buscar patterns
- **WebFetch**: Verificar endpoints externos

## USAGE

### Quick Start

```bash
# Primar o agente
/prime-qa-gato3

# Executar suite completa
/qa-run-all

# Executar check especifico
/qa-check pages
/qa-check checkout
/qa-check seo
/qa-check a11y
```

### Slash Commands

| Command | Description |
|---------|-------------|
| `/prime-qa-gato3` | Carrega contexto do agente |
| `/qa-run-all` | Executa todos os checks |
| `/qa-check [type]` | Executa check especifico |
| `/qa-report` | Gera relatorio consolidado |

## STRUCTURE

```
qa_gato3_agent/
├── README.md           # Este arquivo
├── PRIME.md            # Contexto de dominio
├── INSTRUCTIONS.md     # Instrucoes operacionais
├── config.json         # Configuracao do agente
├── prompts/            # HOPs de QA
│   ├── qa_pages_HOP.md
│   ├── qa_checkout_HOP.md
│   ├── qa_seo_HOP.md
│   └── qa_a11y_HOP.md
└── reports/            # Relatorios gerados
    └── .gitkeep
```

## INTEGRATION

### Dependencies

- Browser MCP Server (screenshots, DOM extraction)
- Project running locally (`npm run dev`) or staging URL
- Supabase Edge Functions deployed

### Environment

```env
GATO3_BASE_URL=https://gatoaocubo.lovable.app
GATO3_LOCAL_URL=http://localhost:5173
```

## WORKFLOWS

### W1: Full QA Suite

```
1. Build check (npm run build)
2. Page load validation (all routes)
3. Image accessibility check
4. SEO validation
5. Checkout flow test
6. Ronronalda chat test
7. B2B form test
8. Accessibility audit
9. Generate report
```

### W2: Pre-Deploy Check

```
1. Build check
2. Critical pages only (/, /catalogo, /produto/:slug)
3. Checkout flow
4. Generate quick report
```

### W3: Post-Deploy Verification

```
1. Health check all endpoints
2. Screenshot comparison
3. Smoke test critical flows
4. Notify success/failure
```

## REPORTS

Output format: Markdown + JSON

```markdown
# QA Report - GATO3
Date: 2025-11-28 14:30:00

## Summary
- Total Checks: 45
- Passed: 42
- Failed: 2
- Warnings: 1

## Critical Issues
- [FAIL] /produto/tapete-gelado - 404 Not Found
- [FAIL] Checkout button unresponsive on mobile

## Warnings
- [WARN] Missing alt text on 3 images

## Details
...
```

## CHANGELOG

### v1.0.0 (2025-11-28)
- Initial release
- 9 core validation checks
- 4 slash commands
- Markdown + JSON reports
