<!-- iso_vectorstore -->
<!--
  Source: PRIME.md
  Agent: qa_gato3_agent
  Synced: 2025-11-30
  Version: 1.0.1
  Package: iso_vectorstore (export package)
-->

# /prime-qa-gato3 | QA Agent Context

> **Scout**: Para descoberta de arquivos, use `mcp__scout__*` | [SCOUT_INTEGRATION.md](../SCOUT_INTEGRATION.md)

## PURPOSE

**QA Agent para GATO3**: Validacao automatizada de qualidade para e-commerce de produtos felinos.

**Target**: gatoaocubo.lovable.app | gato3.com.br

**Stack**: React + Vite + Tailwind + Supabase + Shopify

## DOMAIN CONTEXT

### Project Structure

```
connect-my-github/
├── src/
│   ├── pages/           # Paginas React
│   │   ├── B2C.tsx      # Landing principal
│   │   ├── B2B.tsx      # Pagina parceiros
│   │   ├── Catalogo.tsx # Lista produtos
│   │   ├── ProductDetail.tsx
│   │   └── ...
│   ├── components/      # Componentes UI
│   ├── hooks/           # Custom hooks
│   ├── stores/          # Zustand stores
│   └── lib/             # Utilities
├── supabase/
│   └── functions/       # 8 Edge Functions
└── public/              # Static assets
```

### Routes to Validate

| Route | Page | Priority |
|-------|------|----------|
| `/` | B2C Landing | CRITICAL |
| `/b2b` | B2B/Partners | HIGH |
| `/catalogo` | Product catalog | CRITICAL |
| `/produto/:slug` | Product detail | CRITICAL |
| `/carrinho` | Cart (drawer) | CRITICAL |
| `/admin/*` | Admin panel | MEDIUM |
| `/login` | Auth | MEDIUM |
| `/privacidade` | Privacy Policy | LOW |
| `/termos` | Terms of Service | LOW |

### Critical User Flows

1. **Browse to Checkout**:
   - Home → Catalogo → Product → Add to Cart → Checkout (Shopify redirect)

2. **AI Consultation**:
   - Home → Open Ronronalda → Send message → Receive recommendation → View product

3. **B2B Lead**:
   - B2B page → Fill form → Submit → Confirmation

### Edge Functions

| Function | Type | Test |
|----------|------|------|
| create-shopify-checkout | Public | Cart → Checkout URL |
| ronronalda-chat | Public | Send message → AI response |
| ronronalda-recommendations | Public | Issue → Products |
| ronronalda-tts | Public | Text → Audio |
| fetch-from-shopify | Admin | Sync product data |
| migrate-product | Admin | AI data extraction |
| sync-shopify-product | Admin | Push to Shopify |
| shopify-webhook-handler | Webhook | Receive updates |

## VALIDATION RULES

### Page Load Checks

```javascript
// Success criteria
- HTTP 200
- No console errors
- All images loaded
- Interactive within 3s
- No layout shifts (CLS < 0.1)
```

### SEO Checks

```javascript
// Required elements
- <title> present and unique (max 60 chars)
- <meta name="description"> present (50-160 chars)
- Single <h1> per page
- All images have alt text
- Canonical URL present
- og:image present
```

### Accessibility Checks

```javascript
// WCAG 2.1 AA
- Color contrast >= 4.5:1
- All interactive elements keyboard accessible
- ARIA labels on buttons/links
- Form labels associated
- Skip to content link
- Focus visible
```

### Checkout Flow

```javascript
// Test steps
1. Add product to cart
2. Open cart drawer
3. Verify items displayed
4. Click checkout
5. Verify redirect to gatoaocubo.myshopify.com
6. Verify cart preserved
```

### Ronronalda Chat

```javascript
// Test scenarios
const scenarios = [
  { input: "Meu gato arranha o sofa", expect: "arranhador" },
  { input: "Gato vomitando apos comer", expect: "comedouro" },
  { input: "Gato estressado com mudanca", expect: "toca|cama" },
  { input: "Xixi fora da caixa", expect: "caixa|areia" }
];
```

## TOOLS USAGE

### Browser MCP

```javascript
// Screenshot
mcp__browser__screenshot({ url: "https://gatoaocubo.lovable.app" })

// Full page
mcp__browser__screenshot_full({ url: "https://gatoaocubo.lovable.app/catalogo" })

// Extract text
mcp__browser__extract_text({ url: "https://gatoaocubo.lovable.app" })

// Extract HTML
mcp__browser__extract_html({ url: "https://gatoaocubo.lovable.app" })
```

### Bash Commands

```bash
# Build check
npm run build

# Run tests
npm run test

# Lint
npm run lint

# Type check
npx tsc --noEmit

# Lighthouse
npx lighthouse https://gatoaocubo.lovable.app --output=json
```

### Grep Patterns

```bash
# Find console.log in production
Grep("console\\.log", glob="src/**/*.{ts,tsx}")

# Find TODO/FIXME
Grep("TODO|FIXME", glob="src/**/*.{ts,tsx}")

# Find hardcoded URLs
Grep("localhost|127\\.0\\.0\\.1", glob="src/**/*.{ts,tsx}")
```

## REPORT TEMPLATE

```markdown
# QA Report - GATO3

**Date**: [TIMESTAMP]
**Environment**: [production|staging|local]
**URL**: [BASE_URL]

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Checks | X |
| Passed | X |
| Failed | X |
| Warnings | X |
| Score | X% |

## Critical Issues (P0)

- [ ] [PAGE] [DESCRIPTION]

## High Priority (P1)

- [ ] [PAGE] [DESCRIPTION]

## Medium Priority (P2)

- [ ] [PAGE] [DESCRIPTION]

## Detailed Results

### Pages
[TABLE]

### SEO
[TABLE]

### Accessibility
[TABLE]

### Performance
[METRICS]

## Recommendations

1. [ACTION]
2. [ACTION]

## Next Steps

- [ ] Fix P0 issues
- [ ] Re-run QA
- [ ] Deploy

---
Generated by qa_gato3_agent v1.0.0
```

## SELF-IMPROVEMENT

After each run:
1. Identify flaky tests
2. Update selectors if needed
3. Add new scenarios from failures
4. Optimize execution time

---

## SHARED PRINCIPLES

> See full details: [SHARED_PRINCIPLES.md](../SHARED_PRINCIPLES.md)

### Tasks vs Roles (Sub-agents)
- ❌ "You are a QA expert" → ✅ "Run accessibility audit on ProductDetail page"
- ❌ "Test the application" → ✅ "Execute smoke tests for checkout flow"

### Human Ownership (Before Deploy)
```markdown
- [ ] P0 issues resolved (blocker bugs)
- [ ] Smoke tests pass on staging
- [ ] Performance metrics within threshold
- [ ] No accessibility regressions
- [ ] Cross-browser check complete
```

### Value Function (Test Confidence)
| Suite | Confidence Check |
|-------|------------------|
| Smoke | All critical paths pass? |
| E2E | Checkout flow complete? |
| Visual | No regression screenshots? |
| Performance | LCP <2.5s? FID <100ms? |

---

**Version**: 1.0.1
**Updated**: 2025-11-29
**Agent Type**: QA Specialist
**Domain**: GATO3 E-commerce
