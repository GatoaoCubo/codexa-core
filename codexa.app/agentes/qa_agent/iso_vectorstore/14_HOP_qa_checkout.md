<!-- iso_vectorstore -->
<!--
  Source: qa_checkout_HOP.md
  Agent: qa_agent
  Synced: 2025-12-05
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# MODULE_METADATA
id: qa_checkout_flow
version: 1.0.0
purpose: Validar fluxo de checkout do {{BRAND_NAME}} ate redirect Shopify
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
5. Redirect para {{SHOPIFY_DOMAIN}}

## Success Criteria
- Todos os 5 steps passam
- URL de checkout valida retornada
- Items preservados no redirect

# VALIDATION

- [ ] Endpoint retorna 200
- [ ] checkoutUrl eh URL valida
- [ ] Domain correto (myshopify.com)
- [ ] Pagina Shopify carrega

# CONTEXT

**Upstream**: qa_pages_check
**Downstream**: qa_report_generator
**Critical**: Este teste eh BLOQUEANTE - falha impede deploy
