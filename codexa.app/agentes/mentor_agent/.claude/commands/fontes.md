# /fontes - Gerenciar Documentação Externa

**Comando unificado** para todo o sistema FONTES/ (LLMs, marketplaces, frameworks, e-commerce).

---

## 🎯 USO SIMPLIFICADO

### Comando Principal (Recomendado)
```bash
/fontes sync
```
**O que faz**: Roda workflow completo (check + refresh + validate)

---

## 📋 COMANDOS DISPONÍVEIS

### 1. `/fontes sync` - Sincronização Completa
Verifica atualizações, baixa docs novos, valida links.

```bash
/fontes sync                      # Sync tudo
/fontes sync --priority critical  # Só fontes críticas
/fontes sync --dry-run            # Apenas verifica (não baixa)
```

**Usa quando**:
- Rotina semanal/mensal
- Detectou docs desatualizados
- Nova feature lançada por plataforma (Anthropic, OpenAI, etc)

---

### 2. `/fontes status` - Ver Estado Atual
Mostra status de todas as fontes (última atualização, prioridade).

```bash
/fontes status                    # Ver status básico
/fontes status --show-pending     # Ver + updates pendentes
```

**Usa quando**:
- Quer ver quando foi última atualização
- Verificar quais fontes precisam refresh
- Debug de problemas

---

### 3. `/fontes validate` - Validar Saúde
Testa se todos os links externos estão funcionando.

```bash
/fontes validate                  # Validar todos os links
```

**Usa quando**:
- Mensalmente (health check)
- Após detectar link quebrado
- Antes de confiar em fonte específica

---

## 🔄 WORKFLOW RECOMENDADO

### Rotina Semanal (Segunda-feira)
```bash
/fontes sync --priority critical
```
Atualiza Anthropic, OpenAI, Mercado Livre (fontes críticas)

### Rotina Mensal (1ª Segunda)
```bash
/fontes sync
/fontes validate
```
Sync completo + health check

### On-Demand (Quando Necessário)
```bash
/fontes status --show-pending    # Ver o que precisa atualizar
/fontes sync                     # Atualizar tudo
```

---

## 📊 O QUE ESTÁ NO FONTES/

### LLM Platforms (Critical/High)
- **Anthropic** - Claude API, prompt engineering, tool use, vision
- **OpenAI** - GPT-4, embeddings, fine-tuning, assistants
- **Google AI** - Gemini API, multimodal, function calling
- **Cohere** - Embeddings, rerank, RAG

### Marketplaces (Critical/High)
- **Mercado Livre** - API, SEO, product catalog
- **Shopee** - Product API, order management
- **Amazon BR** - Selling Partner API, FBA
- **Magalu** - Integration API

### Frameworks (High/Medium)
- **LangChain** - Agents, chains, RAG, tools
- **Vercel AI SDK** - Streaming, React hooks, generative UI
- **LlamaIndex** - Indexing, querying, vector stores
- **CrewAI** - Multi-agent systems

### E-commerce (Medium/Low)
- **Google Search Central** - SEO best practices
- **Copywriting Resources** - Product descriptions, conversion copy
- **CRO Guides** - Conversion rate optimization
- **Analytics** - GA4, tracking, funnels

**Total**: 16 fontes externas

---

## 🤖 PARA AGENTES (Como Usar)

### Quando Rodar Sync?
```python
# 1. Usuário menciona que docs estão desatualizados
User: "A documentação do Claude API mudou"
Agent: "Vou atualizar as docs externas"
→ Roda: /fontes sync --priority critical

# 2. Rotina programada (cron/scheduler)
Every Monday 8 AM
→ Roda: /fontes sync --priority critical

# 3. Antes de responder sobre plataforma externa
User: "Como usar a API do Mercado Livre?"
Agent (internal): Verifica se docs estão frescos
→ Roda: /fontes status --show-pending
→ Se pending: /fontes sync
```

### Quando Verificar Status?
```python
# Antes de usar docs externos
antes_de_responder():
    status = run("/fontes status --show-pending")
    if status.has_pending:
        run("/fontes sync")
```

### Quando Validar?
```python
# Mensalmente ou quando link quebrado
monthly_health_check():
    run("/fontes validate")
```

---

## 📝 SAÍDA ESPERADA

### Sync Bem-Sucedido
```
🚀 Starting FONTES synchronization...
============================================================
STEP 1: Checking for updates
============================================================
  Checking anthropic_docs...
  Checking openai_docs...

✅ Found 2 sources with updates

============================================================
STEP 2: Refreshing updated sources
============================================================
  🔄 Refreshing: anthropic_docs
    ✅ 5 files refreshed

✅ Refreshed 2 sources

============================================================
STEP 3: Validating source URLs
============================================================

✅ Validation: 100.0% URLs accessible

📄 Report saved: outputs/fontes_reports/sync_report_20251124_010000.md

✅ Sync complete!
```

### Status Output
```
📊 FONTES Status
================================================================================

📂 LLM_PLATFORMS
--------------------------------------------------------------------------------
  ✅ 🔴 anthropic_docs                   | Last refresh: 2 days ago
  ✅ 🟡 openai_docs                      | Last refresh: 3 days ago
  ✅ 🟡 google_ai_docs                   | Last refresh: 5 days ago

📂 MARKETPLACES
--------------------------------------------------------------------------------
  ✅ 🔴 mercadolivre_api                 | Last refresh: 7 days ago
  ✅ 🟡 shopee_docs                      | Last refresh: Never
```

---

## ⚡ QUICK REFERENCE

| Comando | Quando Usar | Frequência |
|---------|-------------|------------|
| `/fontes sync` | Atualizar docs externas | Semanal |
| `/fontes status` | Ver estado atual | Conforme necessário |
| `/fontes validate` | Health check | Mensal |

---

## 🚨 TROUBLESHOOTING

### "No updates detected" mas docs mudaram
```bash
# Limpar cache e forçar sync
rm -rf FONTES/.cache/
/fontes sync
```

### "Connection timeout"
```bash
# Tentar novamente (pode ser rate limit)
# Aguardar alguns minutos e:
/fontes sync
```

### "Link quebrado" no validate
```bash
# Ver relatório detalhado
cat outputs/fontes_reports/validation_report_*.md

# Atualizar catalogo_fontes.json com nova URL
# Depois:
/fontes sync
```

---

## 📚 ARQUIVOS RELACIONADOS

- **catalogo_fontes.json** - Master index (16 fontes)
- **FONTES/README.md** - Documentação completa
- **scripts/fontes.py** - CLI unificado (consolidado)
- **outputs/fontes_reports/** - Relatórios gerados

---

**Versão**: 2.1.0 (Simplificado)
**Criado**: 2025-11-24
**Tipo**: Comando unificado
**Status**: ✅ Production Ready

---

> 💡 **Dica**: Use `/fontes sync` toda segunda-feira para manter tudo atualizado!
