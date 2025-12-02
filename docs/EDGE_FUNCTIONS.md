# Edge Functions - Guia Completo de Gerenciamento

## Visao Geral

Este documento descreve todas as Edge Functions do projeto GATO3, seus endpoints, parametros e procedimentos de manutencao.

**Supabase Project URL**: `https://fuuguegkqnpzrrhwymgw.supabase.co`
**Functions Base URL**: `https://fuuguegkqnpzrrhwymgw.supabase.co/functions/v1`
**Dashboard**: https://supabase.com/dashboard/project/fuuguegkqnpzrrhwymgw

---

## Inventario de Edge Functions

| Funcao | Tipo | Critico | Descricao |
|--------|------|---------|-----------|
| `create-shopify-checkout` | public | SIM | Cria checkout no Shopify |
| `ronronalda-chat` | public | SIM | Chat com IA da Ronronalda |
| `ronronalda-recommendations` | public | NAO | Recomendacoes de produtos |
| `ronronalda-tts` | public | NAO | Text-to-speech |
| `fetch-from-shopify` | admin | NAO | Busca dados do Shopify |
| `migrate-product` | admin | NAO | Migra produto para Supabase |
| `sync-shopify-product` | admin | NAO | Sincroniza produto Shopify |
| `shopify-webhook-handler` | webhook | NAO | Processa webhooks Shopify |

---

## 1. create-shopify-checkout

**Tipo**: Public (sem auth)
**Criticidade**: ALTA - Funcao de conversao

### Endpoint
```
POST /functions/v1/create-shopify-checkout
```

### Request Body
```json
{
  "items": [
    {
      "variantId": "gid://shopify/ProductVariant/123456",
      "quantity": 1
    }
  ],
  "note": "Origem: gatoaocubo.lovable.app"
}
```

### Response
```json
{
  "checkoutUrl": "https://gatoaocubo.myshopify.com/cart/123:1",
  "checkoutId": "abc123"
}
```

### Teste Manual
```bash
curl -X POST \
  'https://izjbfnhppclkpxgflsnh.supabase.co/functions/v1/create-shopify-checkout' \
  -H 'Content-Type: application/json' \
  -d '{"items":[{"variantId":"gid://shopify/ProductVariant/TEST","quantity":1}]}'
```

---

## 2. ronronalda-chat

**Tipo**: Public
**Criticidade**: ALTA - Funcao de conversao

### Endpoint
```
POST /functions/v1/ronronalda-chat
```

### Request Body
```json
{
  "message": "Meu gato arranha o sofa",
  "sessionId": "optional-session-id",
  "context": {
    "previousMessages": []
  }
}
```

### Response
```json
{
  "reply": "Entendo! Gatos precisam arranhar...",
  "products": [
    {
      "id": "123",
      "name": "Arranhador Vertical",
      "slug": "arranhador-vertical",
      "price": 89.90
    }
  ],
  "intent": "scratching_furniture"
}
```

### Cenarios de Teste
| Input | Keyword Esperado |
|-------|------------------|
| "Meu gato arranha o sofa" | arranhador |
| "Gato vomitando apos comer" | comedouro |
| "Gato estressado com mudanca" | toca |
| "Xixi fora da caixa" | caixa |

---

## 3. ronronalda-recommendations

**Tipo**: Public
**Criticidade**: Media

### Endpoint
```
POST /functions/v1/ronronalda-recommendations
```

### Request Body
```json
{
  "currentProductId": "123",
  "category": "arranhadores",
  "limit": 4
}
```

---

## 4. ronronalda-tts

**Tipo**: Public
**Criticidade**: Baixa

### Endpoint
```
POST /functions/v1/ronronalda-tts
```

### Request Body
```json
{
  "text": "Ola! Eu sou a Ronronalda...",
  "voice": "alloy"
}
```

### Response
Audio stream (audio/mpeg)

---

## 5. fetch-from-shopify

**Tipo**: Admin (requer auth)
**Criticidade**: Media

### Endpoint
```
POST /functions/v1/fetch-from-shopify
Authorization: Bearer <SERVICE_ROLE_KEY>
```

### Request Body
```json
{
  "query": "products",
  "filters": {
    "limit": 50,
    "status": "active"
  }
}
```

---

## 6. migrate-product

**Tipo**: Admin (requer auth)
**Criticidade**: Media

### Endpoint
```
POST /functions/v1/migrate-product
Authorization: Bearer <SERVICE_ROLE_KEY>
```

### Request Body
```json
{
  "shopifyProductId": "gid://shopify/Product/123456",
  "overwrite": false
}
```

### Fluxo de Migracao
```
1. Busca produto no Shopify
2. Transforma para schema Supabase
3. Faz upsert na tabela products
4. Sincroniza imagens para Storage
5. Retorna produto migrado
```

---

## 7. sync-shopify-product

**Tipo**: Admin (requer auth)
**Criticidade**: Media

### Endpoint
```
POST /functions/v1/sync-shopify-product
Authorization: Bearer <SERVICE_ROLE_KEY>
```

### Request Body
```json
{
  "productId": "123",
  "direction": "shopify_to_supabase"
}
```

---

## 8. shopify-webhook-handler

**Tipo**: Webhook
**Criticidade**: Media

### Endpoint
```
POST /functions/v1/shopify-webhook-handler
X-Shopify-Topic: products/update
X-Shopify-Hmac-SHA256: <signature>
```

### Eventos Suportados
- `products/create`
- `products/update`
- `products/delete`
- `orders/create`
- `inventory_levels/update`

---

## Gerenciamento via CLI

### Listar Funcoes
```bash
npx supabase functions list
```

### Deploy de Funcao
```bash
# Deploy individual
npx supabase functions deploy create-shopify-checkout

# Deploy todas
npx supabase functions deploy
```

### Logs
```bash
# Tempo real
npx supabase functions logs create-shopify-checkout --tail

# Ultimos 100
npx supabase functions logs ronronalda-chat --limit 100
```

### Variaveis de Ambiente
```bash
# Listar secrets
npx supabase secrets list

# Adicionar secret
npx supabase secrets set SHOPIFY_ACCESS_TOKEN=shpat_xxx

# Remover secret
npx supabase secrets unset OLD_KEY
```

---

## Secrets Necessarios

| Secret | Descricao | Usado por |
|--------|-----------|-----------|
| `SHOPIFY_ACCESS_TOKEN` | Token de acesso Shopify | checkout, fetch, sync |
| `SHOPIFY_STORE_DOMAIN` | gatoaocubo.myshopify.com | checkout, fetch, sync |
| `OPENAI_API_KEY` | API key OpenAI | ronronalda-chat |
| `ELEVEN_LABS_KEY` | API key ElevenLabs | ronronalda-tts |

---

## Health Checks

### Script de Verificacao
```bash
#!/bin/bash
BASE="https://fuuguegkqnpzrrhwymgw.supabase.co/functions/v1"

echo "Checking Edge Functions..."

# create-shopify-checkout
curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/create-shopify-checkout" \
  -H "Content-Type: application/json" \
  -d '{"items":[]}' && echo " create-shopify-checkout OK"

# ronronalda-chat
curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/ronronalda-chat" \
  -H "Content-Type: application/json" \
  -d '{"message":"teste"}' && echo " ronronalda-chat OK"

echo "Done."
```

---

## Troubleshooting

### Erro 500 - Internal Server Error
1. Verificar logs: `npx supabase functions logs <nome>`
2. Checar secrets configurados
3. Verificar quota de API externas

### Erro 401 - Unauthorized (funcoes admin)
1. Verificar header Authorization
2. Confirmar SERVICE_ROLE_KEY correto
3. Checar se funcao requer auth

### Timeout (>60s)
1. Edge Functions tem limite de 60s
2. Otimizar queries
3. Considerar processamento async

---

## Integracao com anuncio_agent

O `anuncio_agent` pode usar as Edge Functions admin para:

1. **Publicar anuncio** -> `migrate-product` cria o produto
2. **Atualizar copy** -> `sync-shopify-product` sincroniza
3. **Verificar status** -> `fetch-from-shopify` consulta

Ver: `docs/SUPABASE_ADMIN_SETUP.md` para configuracao completa.

---

**Versao**: 1.0.0
**Atualizado**: 2025-11-28
