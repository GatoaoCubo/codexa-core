<!-- iso_vectorstore -->
<!--
  Source: PRIME.md
  Agent: qa_agent
  Synced: 2025-12-05
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# /prime-qa | QA Agent Context

> **Scout**: Para descoberta de arquivos, use `mcp__scout__*` | [SCOUT_INTEGRATION.md](../SCOUT_INTEGRATION.md)

## PURPOSE

**QA Agent para {{BRAND_NAME}}**: Validacao automatizada de qualidade para e-commerce de {{PRODUCT_CATEGORY}}.

**Target**: {{BASE_URL}} | {{DOMAIN}}

**Stack**: React + Vite + Tailwind + Supabase + Shopify

## DOMAIN CONTEXT

### Project Structure

```
{{PROJECT_FOLDER}}/
├── src/
│   ├── pages/           # Paginas React
│   ├── components/      # Componentes UI
│   ├── hooks/           # Custom hooks
│   ├── stores/          # Zustand stores
│   └── lib/             # Utilities
├── supabase/
│   └── functions/       # Edge Functions
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
   - Home -> Catalogo -> Product -> Add to Cart -> Checkout (Shopify redirect)

2. **AI Consultation**:
   - Home -> Open {{AI_ASSISTANT_NAME}} -> Send message -> Receive recommendation -> View product

3. **B2B Lead**:
   - B2B page -> Fill form -> Submit -> Confirmation

## VALIDATION RULES

### Page Load Checks
- HTTP 200
- No console errors
- All images loaded
- Interactive within 3s
- No layout shifts (CLS < 0.1)

### SEO Checks
- Title present and unique (max 60 chars)
- Meta description present (50-160 chars)
- Single h1 per page
- All images have alt text
- Canonical URL present
- og:image present

### Accessibility Checks (WCAG 2.1 AA)
- Color contrast >= 4.5:1
- All interactive elements keyboard accessible
- ARIA labels on buttons/links
- Form labels associated
- Skip to content link
- Focus visible

---

**Version**: 1.0.0
**Updated**: 2025-12-05
**Agent Type**: QA Specialist
**Domain**: Generic E-commerce
