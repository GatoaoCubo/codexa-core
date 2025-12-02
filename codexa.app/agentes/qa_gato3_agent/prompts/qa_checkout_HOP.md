# MODULE_METADATA
id: qa_checkout_flow
version: 1.0.0
purpose: Validar fluxo de checkout do GATO3 ate redirect Shopify
category: qa/checkout
dependencies: [browser_mcp, web_fetch]

# INPUT_CONTRACT
$base_url: string (URL base)
$test_product_slug: string (slug do produto de teste)
$supabase_functions_url: string (URL das Edge Functions)

# OUTPUT_CONTRACT
$report: CheckoutFlowReport {
  success: boolean,
  steps: StepResult[],
  checkout_url: string | null,
  error: string | null
}

# TASK

**Role**: QA Checkout Tester
**Objective**: Validar fluxo completo de checkout desde adicao ao carrinho ate redirect para Shopify

## Critical Path
1. Pagina de produto acessivel
2. Botao "Adicionar ao carrinho" funcional
3. Cart drawer abre com item
4. Botao "Finalizar compra" funcional
5. Redirect para gatoaocubo.myshopify.com

## Success Criteria
- Todos os 5 steps passam
- URL de checkout valida retornada
- Items preservados no redirect

# STEPS

### 1. Acessar Pagina de Produto
```
URL: $base_url/produto/$test_product_slug
Action: Screenshot + extract_text
Verify: Nome do produto visivel, botao de adicionar presente
```

### 2. Testar Endpoint de Checkout
```
POST $supabase_functions_url/create-shopify-checkout
Body: {
  "items": [{
    "shopifyVariantId": "gid://shopify/ProductVariant/[ID]",
    "quantity": 1
  }]
}
Verify: 200 OK, checkoutUrl presente
```

### 3. Validar URL de Checkout
```
Parse checkoutUrl
Verify:
  - Domain = gatoaocubo.myshopify.com
  - Path contains /cart/c/ or /checkouts/
  - channel=online_store presente
```

### 4. Acessar URL de Checkout
```
Action: Screenshot do Shopify checkout
Verify: Pagina carrega, item visivel
```

### 5. Gerar Relatorio
```markdown
## Checkout Flow Test

### Steps
1. [PASS] Product page accessible
2. [PASS] Add to cart functional
3. [PASS] Checkout API returns valid URL
4. [PASS] Redirect to Shopify works
5. [PASS] Items preserved in checkout

### Checkout URL
https://gatoaocubo.myshopify.com/cart/c/...

### Screenshots
- product_page.png
- shopify_checkout.png
```

# VALIDATION

- [ ] Endpoint retorna 200
- [ ] checkoutUrl eh URL valida
- [ ] Domain correto (myshopify.com)
- [ ] Pagina Shopify carrega

# ERROR HANDLING

| Error | Action |
|-------|--------|
| 400 Bad Request | Verificar shopifyVariantId |
| 500 Server Error | Verificar SHOPIFY_STOREFRONT_TOKEN |
| Timeout | Retry 3x com backoff |
| Invalid URL | Log e reportar falha |

# CONTEXT

**Upstream**: qa_pages_check
**Downstream**: qa_report_generator
**Critical**: Este teste eh BLOQUEANTE - falha impede deploy
