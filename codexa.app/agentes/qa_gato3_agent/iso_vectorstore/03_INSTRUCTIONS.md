<!-- iso_vectorstore -->
<!--
  Source: INSTRUCTIONS.md
  Agent: qa_gato3_agent
  Synced: 2025-11-30
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# INSTRUCTIONS | qa_gato3_agent

## QUICK START

```bash
# 1. Prime the agent
/prime-qa-gato3

# 2. Run full suite
/qa-run-all

# 3. Check specific area
/qa-check pages|checkout|seo|a11y|chat|forms
```

## EXECUTION MODES

### Mode 1: Full Suite (30-45 min)

Complete validation of all aspects.

```
Steps:
1. Build verification (npm run build)
2. All pages load check
3. All images accessible
4. SEO audit all pages
5. Checkout flow test
6. Ronronalda chat test (4 scenarios)
7. B2B form submission test
8. Accessibility audit
9. Performance check (Lighthouse)
10. Generate full report
```

### Mode 2: Pre-Deploy (10-15 min)

Quick check before deployment.

```
Steps:
1. Build verification
2. Critical pages only (/, /catalogo, /produto/:slug)
3. Checkout flow
4. Generate quick report
```

### Mode 3: Post-Deploy (5 min)

Smoke test after deployment.

```
Steps:
1. Health check URLs
2. Screenshot comparison
3. Checkout smoke test
4. Report status
```

### Mode 4: Specific Check

Single area validation.

```
/qa-check pages     # All page loads
/qa-check checkout  # Checkout flow only
/qa-check seo       # SEO elements only
/qa-check a11y      # Accessibility only
/qa-check chat      # Ronronalda only
/qa-check forms     # Forms only
```

## VALIDATION PROCEDURES

### V1: Page Load Check

```javascript
For each route in ROUTES:
  1. Screenshot page
  2. Extract text content
  3. Check for error messages
  4. Verify main content present
  5. Record load time
  6. Log result
```

### V2: Image Check

```javascript
1. Extract all <img> tags
2. For each image:
   - Verify src is accessible (200 OK)
   - Check alt text present
   - Check dimensions specified
   - Check lazy loading on below-fold
3. Flag missing/broken images
```

### V3: SEO Check

```javascript
For each page:
  1. Extract <title>
  2. Extract <meta name="description">
  3. Count <h1> tags (should be 1)
  4. Extract og:* tags
  5. Check canonical URL
  6. Validate structured data (JSON-LD)
  7. Score and report
```

### V4: Checkout Flow

```javascript
1. Navigate to /catalogo
2. Select first available product
3. Click "Adicionar ao carrinho"
4. Open cart drawer
5. Verify item in cart
6. Click "Finalizar compra"
7. Verify redirect to myshopify.com
8. Verify URL contains cart items
```

### V5: Ronronalda Chat

```javascript
Test scenarios:
[
  { msg: "Meu gato arranha o sofa", expect: products with "arranhador" },
  { msg: "Gato vomitando apos comer", expect: products with "comedouro" },
  { msg: "Gato estressado", expect: products with "toca|cama" },
  { msg: "Xixi fora da caixa", expect: products with "caixa" }
]

For each:
  1. POST to /functions/v1/ronronalda-chat
  2. Verify 200 response
  3. Verify reply contains expected keywords
  4. Verify products array not empty
```

### V6: B2B Form

```javascript
1. Navigate to /b2b
2. Fill form with test data:
   - Nome: "Teste QA"
   - Email: "qa@test.com"
   - Telefone: "11999999999"
   - Empresa: "Teste LTDA"
   - Mensagem: "Teste automatizado QA"
3. Submit form
4. Verify success message
5. (Optional) Check Supabase for entry
```

### V7: Accessibility

```javascript
1. Check skip link present
2. Check focus visible on tab
3. Check ARIA labels on buttons
4. Check form labels
5. Check color contrast (if tool available)
6. Check heading hierarchy
7. Generate a11y report
```

## OUTPUT FORMAT

### Console Output

```
[INFO] Starting QA Suite...
[INFO] Environment: production
[INFO] Base URL: https://gatoaocubo.lovable.app

[CHECK] Page Load: /
[PASS] / - Loaded in 1.2s

[CHECK] Page Load: /catalogo
[PASS] /catalogo - Loaded in 2.1s

[CHECK] SEO: /
[WARN] / - Description too short (45 chars, min 50)

[CHECK] Checkout Flow
[PASS] Cart creation successful
[PASS] Redirect to Shopify confirmed

[FAIL] Ronronalda Chat - Scenario 3
       Expected: products with "toca"
       Received: empty array

---
SUMMARY: 42 passed, 2 failed, 1 warning
```

### Report File

Generate:
- `reports/qa_report_YYYYMMDD_HHMMSS.md`
- `reports/qa_report_YYYYMMDD_HHMMSS.json`

## ERROR HANDLING

### Common Issues

| Error | Solution |
|-------|----------|
| Page 404 | Check route exists in App.tsx |
| Image broken | Check Supabase storage/CDN |
| Checkout fails | Check Shopify API token |
| Chat empty | Check Lovable API key |
| Timeout | Increase wait time, check network |

### Retry Logic

```javascript
maxRetries = 3
retryDelay = 2000 // ms

for (attempt = 1; attempt <= maxRetries; attempt++) {
  try {
    result = await check()
    break
  } catch (e) {
    if (attempt === maxRetries) throw e
    await sleep(retryDelay * attempt)
  }
}
```

## BEST PRACTICES

1. **Run on staging first** - Validate before production
2. **Screenshot failures** - Visual evidence helps debugging
3. **Log everything** - Detailed logs for troubleshooting
4. **Retry flaky tests** - Network issues happen
5. **Update selectors** - UI changes break tests
6. **Track metrics** - Compare runs over time

---

**Version**: 1.0.0
**Last Updated**: 2025-11-28
