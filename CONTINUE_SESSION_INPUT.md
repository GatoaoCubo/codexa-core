# SESSION INPUT | GATO³ + CODEXA Development

**Data**: 2025-12-02
**Projeto**: gato³ (e-commerce felino) + CODEXA (sistema de agentes IA)
**Working Directory**: `C:\Users\Dell\Documents\GitHub\connect-my-github\codexa.gato`

---

## CONTEXTO RÁPIDO

Estamos trabalhando no ecossistema **GATO³ / CODEXA**:

- **GATO³**: E-commerce de produtos para gatos (gatoaocubo.lovable.app / gato3.com.br)
- **CODEXA**: Sistema de 14 agentes IA para automação de e-commerce brasileiro

---

## ESTRUTURA DO PROJETO

```
C:\Users\Dell\Documents\GitHub\connect-my-github\    ← SITE GATO³ (Lovable)
├── src/pages/Index.tsx          # Landing Page CODEXA
├── src/components/              # React components
├── supabase/functions/          # Edge Functions (4 criadas)
├── .github/workflows/           # CI/CD (qa-validation.yml)
│
└── codexa.gato/                 ← SISTEMA DE AGENTES
    ├── PRIME.md                 # Navigator principal
    ├── CLAUDE.md                # Project laws
    ├── .env                     # Chaves configuradas ✅
    ├── .mcp.json                # MCP Servers (voice, browser, scout)
    │
    └── codexa.app/agentes/      # 14 agentes especializados
        ├── anuncio_agent/       # 90 arquivos - Ad generation
        ├── pesquisa_agent/      # 103 arquivos - Market research
        ├── photo_agent/         # 75 arquivos - Photo prompts
        ├── ronronalda_agent/    # 24 arquivos - AI Chat assistant
        ├── qa_gato3_agent/      # 23 arquivos - QA automation
        ├── codexa_agent/        # 239 arquivos - Meta-constructor
        ├── mentor_agent/        # 413 arquivos - Strategic planning
        └── ...outros
```

---

## INTEGRAÇÕES ATIVAS

| Sistema | URL/Config | Status |
|---------|------------|--------|
| **Supabase** | fuuguegkqnpzrrhwymgw.supabase.co | ✅ 22 produtos |
| **Shopify** | gatoaocubo.myshopify.com | ✅ HTTP 200 |
| **Lovable** | gatoaocubo.lovable.app | ✅ Auto-deploy via Git |
| **GitHub** | GatoaoCubo/connect-my-github | ✅ main branch |

---

## CHAVES CONFIGURADAS (.env)

```
✅ ANTHROPIC_API_KEY      - Claude AI
✅ ELEVENLABS_API_KEY     - TTS
✅ SUPABASE_URL           - Database
✅ SUPABASE_SERVICE_ROLE_KEY - Admin access (ESCRITA habilitada)
✅ GOOGLE_API_KEY         - Gemini/Imagen
```

---

## MCP SERVERS ATIVOS

```json
{
  "voice": "codexa.app/voice/server.py",
  "browser": "codexa.app/mcp-servers/browser-mcp/index.js",
  "scout": "codexa.app/mcp-servers/scout-mcp/index.js"
}
```

Ferramentas disponíveis:
- `mcp__scout__discover` - Buscar arquivos
- `mcp__scout__smart_context` - Contexto de agente
- `mcp__browser__screenshot` - Capturar páginas
- `mcp__browser__search_marketplace` - Pesquisar ML/Shopee/Amazon
- `mcp__voice__speak` / `listen_start` - Voz

---

## O QUE FOI FEITO NA ÚLTIMA SESSÃO

### 1. Diagnóstico Completo
- Scout index: 1,724 arquivos
- 14 agentes mapeados
- Paths verificados e funcionando

### 2. QA do Site (Score: 82/100)
- 6 rotas testadas (HTTP 200)
- Issues P0: GA4 placeholder `G-XXXXXXX`
- Issues P1: skip links, canonical /login, meta tags

### 3. Edge Functions Versionadas
```
supabase/functions/
├── ronronalda-chat/index.ts
├── ronronalda-recommendations/index.ts
├── ronronalda-tts/index.ts
├── create-shopify-checkout/index.ts
├── config.toml
└── README.md
```

### 4. CI/CD Configurado
```
.github/workflows/qa-validation.yml
- Build + Lint
- TypeScript check
- Lighthouse audit
- A11y check
```

### 5. Links Corrigidos na LP CODEXA
```typescript
GATO3_LINKS = {
  site: "https://gato3.com.br",
  mercadoLivre: "https://lista.mercadolivre.com.br/pagina/gatogato20230820110715/...",
  shopee: "https://shopee.com.br/shop/1057176206",
}
```

### 6. Commit Realizado e Pushed
```
6260f4a feat: Add Edge Functions, CI/CD pipeline + fix Gato³ links
```

---

## CAPACIDADES DISPONÍVEIS

| Ação | Como Usar |
|------|-----------|
| Listar produtos | `python scripts/list_products.py` |
| Reformar produto | `/reform-product "Nome do Produto"` |
| Pesquisar concorrência | `/pesquisa "termo"` ou `mcp__browser__search_marketplace` |
| Modificar site | Edit `src/` + `git push` → Lovable deploy |
| Sync Shopify | `python scripts/sync_all_shopify.py` |
| Screenshot | `mcp__browser__screenshot({ url: "..." })` |
| Contexto agente | `mcp__scout__smart_context({ agent: "anuncio_agent" })` |

---

## PRODUTOS NO SUPABASE (22 total)

| # | Produto | Preço |
|---|---------|-------|
| 1 | Tapete Refrescante Gelado 65x50cm | R$ 58.39 |
| 2 | Tapete Gelado Grande 50x90cm | R$ 68.93 |
| 3 | Tapete Refrescante 40x50cm | R$ 28.90 |
| 4 | Portão Retrátil 1.80m | R$ 213.00 |
| 5 | Caixa Transportadora PP | R$ 11.00 |
| 6 | Guia Pet Cintura Bolsa | R$ 36.90 |
| 7 | Bola Frisbee 2 em 1 | R$ 27.70 |
| 8 | Escova Massageadora Canto | R$ 11.30 |
| 9 | Laser Interativo | R$ 6.90 |
| 10 | Assento Carro Pet | R$ 79.90 |
| 11 | Arranhador Papelão | R$ 38.33 |
| 12 | Caixa Transporte Retrátil | R$ 279.33 |
| 13 | Tapete Gelado Colchonete | R$ 36.69 |
| 14 | Brinquedo Catnip Corda | R$ 11.30 |
| 15 | Grade Ajustável 1.80m | R$ 215.30 |
| 16 | Mochila Cápsula Astronauta | R$ 77.33 |
| 17 | Cama Suspensa Janela | R$ 43.90 |
| 18 | Varinha Ventosa Pena | R$ 19.30 |
| 19 | Rolo Tira Pelos | R$ 6.30 |
| 20 | Comedouro Retrátil | R$ 17.35 |
| 21 | Bola Inteligente USB | R$ 77.33 |
| 22 | Brinquedo Automático Corda | R$ 36.30 |

---

## PRÓXIMOS PASSOS SUGERIDOS

1. **Corrigir P0 (GA4)** - Substituir `G-XXXXXXX` por ID real
2. **Reformar produtos** - Rodar pipeline em produtos selecionados
3. **Deploy Edge Functions** - `supabase functions deploy`
4. **Mobile QA** - Verificar responsividade

---

## COMANDOS PARA INICIAR

```bash
# Carregar contexto
/prime-scout

# Verificar status
mcp__scout__stats

# Listar produtos
cd codexa.app/agentes/anuncio_agent && python scripts/list_products.py
```

---

**Gerado**: 2025-12-02 08:55 UTC-3
**Git**: 6260f4a (pushed to main)
**Status**: Pronto para operação
