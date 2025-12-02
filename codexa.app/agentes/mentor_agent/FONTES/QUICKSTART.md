# FONTES - Quick Start (1 Minuto)

## 🎯 O QUE É?
Sistema de documentação externa sempre atualizada (LLMs, marketplaces, frameworks).

---

## ⚡ USO RÁPIDO

### Comando Principal (99% dos casos)
```bash
/fontes sync
```
**Faz**: Check updates + Download docs + Validate links

---

## 📅 QUANDO USAR

| Situação | Comando | Frequência |
|----------|---------|------------|
| Rotina semanal | `/fontes sync --priority critical` | Toda segunda |
| Rotina mensal | `/fontes sync` | 1x por mês |
| Verificar status | `/fontes status` | Conforme necessário |
| Health check | `/fontes validate` | Mensal |

---

## 🤖 PARA AGENTES

### Quando Rodar?
```python
# User menciona docs desatualizados
→ /fontes sync

# Antes de responder sobre APIs/plataformas
→ /fontes status --show-pending
→ Se pending: /fontes sync
```

### O Que Buscar?
**Scout detecta automaticamente** quando buscar em FONTES/:
- LLM APIs → `anthropic`, `claude`, `openai`, `gpt`
- Marketplaces → `mercado livre`, `shopee`, `amazon`
- Frameworks → `langchain`, `vercel`, `llamaindex`
- E-commerce → `seo`, `copywriting`, `conversion`

---

## 📂 O QUE TEM NO FONTES/

- **LLM_PLATFORMS/** - Anthropic, OpenAI, Google, Cohere
- **MARKETPLACES/** - Mercado Livre, Shopee, Amazon, Magalu
- **FRAMEWORKS/** - LangChain, Vercel AI SDK, LlamaIndex, CrewAI
- **ECOMMERCE/** - SEO, copywriting, CRO, analytics

**Total**: 16 fontes externas

---

## 🚨 REGRAS CRÍTICAS

1. ✅ **Use `/fontes sync`** (comando unificado)
2. ❌ **NÃO edite manualmente** .md files em FONTES/ (serão sobrescritos)
3. ✅ **Atualize semanalmente** (Monday mornings)
4. ✅ **Verifique antes** de responder sobre plataformas externas

---

## 📖 DOCS COMPLETAS

- `FONTES/README.md` - Guia completo (4000+ palavras)
- `.claude/commands/fontes.md` - Referência do comando
- `INSTRUCTIONS.md` - Integração com workflows

---

**Versão**: 2.1.0 (Simplificado)
**Status**: ✅ Production Ready
**Comando**: `/fontes sync`

---

> 💡 **Lembre**: 1 comando (`/fontes sync`), não 4 scripts separados!
