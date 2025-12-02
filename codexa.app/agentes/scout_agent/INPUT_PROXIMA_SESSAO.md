# INPUT: Sessão de Expansão Agentes Mínimos

> **Data**: 2025-11-30 | **Contexto**: Builder criado, agentes mínimos pendentes

---

## RESUMO DA SESSÃO ATUAL

### P0 Concluído: Builder de Sincronização iso_vectorstore
- **Criado**: `codexa_agent/builders/18_iso_vectorstore_sync.py`
- **Funcionalidade**: Sincroniza fonte → iso_vectorstore automaticamente
- **Hook pre-commit**: `agentes/.pre-commit-config.yaml` configurado
- **Teste**: 107 arquivos sincronizados em 12 agentes com sucesso

### P1 Concluído: Sincronização Inicial Executada
Status atual dos iso_vectorstore por agente:

| Agente | Arquivos | Status |
|--------|----------|--------|
| anuncio_agent | 23 | Maduro |
| codexa_agent | 29 | Maduro |
| curso_agent | 27 | Maduro |
| marca_agent | 32 | Maduro |
| mentor_agent | 31 | Maduro |
| pesquisa_agent | 30 | Maduro |
| photo_agent | 27 | Maduro |
| video_agent | 25 | Maduro |
| **qa_gato3_agent** | **9** | **Mínimo** |
| **ronronalda_agent** | **5** | **Mínimo** |
| **scout_agent** | **8** | **Mínimo** |
| **voice_agent** | **7** | **Mínimo** |

### Arquivos Criados/Atualizados
```
codexa_agent/builders/
├── 18_iso_vectorstore_sync.py     # Builder de sync
└── hooks/
    └── pre-commit-iso-sync        # Script hook

agentes/
└── .pre-commit-config.yaml        # Configuração pre-commit
```

---

## DECISÕES TOMADAS

1. **Tipo de Builder**: Hook pre-commit (automático)
2. **Limite de Arquivos**: Flexível 20+ (máx 4096 tokens/arquivo para chunking)
3. **Prioridade**: Builder primeiro ✓

---

## USO DO BUILDER

```bash
# Sync todos os agentes
python codexa_agent/builders/18_iso_vectorstore_sync.py

# Sync agente específico
python codexa_agent/builders/18_iso_vectorstore_sync.py --agent anuncio_agent

# Dry run (preview)
python codexa_agent/builders/18_iso_vectorstore_sync.py --dry-run

# Modo pre-commit (apenas agentes com mudanças)
python codexa_agent/builders/18_iso_vectorstore_sync.py --pre-commit

# Verbose
python codexa_agent/builders/18_iso_vectorstore_sync.py --verbose
```

### Instalação do Hook
```bash
cd agentes
pip install pre-commit
pre-commit install
```

---

## PENDENTE: P2 - Expandir Agentes Mínimos

### 4 Agentes Precisam de Mais Conteúdo:

#### 1. ronronalda_agent (5 arquivos)
- Falta: ARCHITECTURE.md, workflows/, prompts/ detalhados
- Ação: Criar conteúdo ou marcar como agente simples

#### 2. qa_gato3_agent (9 arquivos)
- Tem: 4 HOPs (a11y, checkout, pages, seo)
- Falta: config/, workflows/, execution_plans
- Ação: Criar ADW de QA workflow

#### 3. scout_agent (8 arquivos)
- Tem: 3 configs (categories, ignore, weights)
- Falta: workflows/, mais HOPs
- Ação: Criar ADW de discovery workflow

#### 4. voice_agent (7 arquivos)
- Tem: 1 HOP (voice_interaction)
- Falta: config/, workflows/, mais HOPs
- Ação: Criar ADW de voice interaction

---

## TAREFAS PARA PRÓXIMA SESSÃO

### P0: Expandir qa_gato3_agent
1. Criar `workflows/100_ADW_QA_WORKFLOW.md`
2. Criar `config/qa_rules.json`
3. Rodar sync: `python 18_iso_vectorstore_sync.py --agent qa_gato3_agent`

### P1: Expandir scout_agent
1. Criar `workflows/100_ADW_DISCOVERY_WORKFLOW.md`
2. Criar `prompts/` com HOPs de discovery
3. Rodar sync

### P2: Expandir voice_agent
1. Criar `workflows/100_ADW_VOICE_INTERACTION.md`
2. Expandir `config/` com settings de voz
3. Rodar sync

### P3: Avaliar ronronalda_agent
1. Determinar se precisa expansão ou é intencionalmente simples
2. Documentar decisão

---

## MAPEAMENTO DO BUILDER

O `18_iso_vectorstore_sync.py` faz o seguinte mapeamento:

```
FONTE                      → iso_vectorstore
────────────────────────────────────────────
PRIME.md                   → 02_PRIME.md
INSTRUCTIONS.md            → 03_INSTRUCTIONS.md
README.md                  → 04_README.md
ARCHITECTURE.md            → 05_ARCHITECTURE.md
CHANGELOG.md               → 20_CHANGELOG.md
templates/output_template  → 07_output_template.md
config/*.json              → 08-10_*.json
plans/*.json               → 12_execution_plans.json (consolidado)
workflows/100_ADW*.md      → 11_ADW_orchestrator.md
prompts/*.md               → 13-19_HOP_*.md
[auto-gerado]              → 01_QUICK_START.md
[auto-gerado]              → 06_input_schema.json
```

---

## COMANDOS ÚTEIS

```bash
# Verificar status de sync
python codexa_agent/builders/18_iso_vectorstore_sync.py --dry-run

# Sync apenas agentes mínimos
python 18_iso_vectorstore_sync.py --agent qa_gato3_agent
python 18_iso_vectorstore_sync.py --agent scout_agent
python 18_iso_vectorstore_sync.py --agent voice_agent
python 18_iso_vectorstore_sync.py --agent ronronalda_agent
```

---

---

## SESSÃO CONCLUÍDA

### Arquivos Criados Nesta Sessão

```
codexa_agent/builders/
├── 18_iso_vectorstore_sync.py      # Builder principal
└── hooks/
    └── pre-commit-iso-sync         # Script hook

agentes/
└── .pre-commit-config.yaml         # Config pre-commit

qa_gato3_agent/
├── workflows/100_ADW_QA_WORKFLOW.md
└── config/qa_rules.json

scout_agent/
└── workflows/100_ADW_DISCOVERY_WORKFLOW.md

voice_agent/
└── workflows/100_ADW_VOICE_INTERACTION.md

ronronalda_agent/
├── workflows/100_ADW_RONRONALDA.md
├── config/persona.json
└── prompts/01_ronronalda_chat_HOP.md
```

### Status Final iso_vectorstore

| Agent | Antes | Depois | Delta |
|-------|-------|--------|-------|
| anuncio_agent | 23 | 23 | - |
| codexa_agent | 29 | 29 | - |
| curso_agent | 27 | 27 | - |
| marca_agent | 32 | 32 | - |
| mentor_agent | 31 | 31 | - |
| pesquisa_agent | 30 | 30 | - |
| photo_agent | 27 | 27 | - |
| video_agent | 25 | 25 | - |
| **qa_gato3_agent** | 9 | **11** | +2 |
| **ronronalda_agent** | 5 | **8** | +3 |
| **scout_agent** | 8 | **9** | +1 |
| **voice_agent** | 7 | **9** | +2 |
| **TOTAL** | ~251 | **261** | +10 |

### Próximas Melhorias (Opcional)

Os agentes mínimos ainda podem ser expandidos:
- ronronalda: Adicionar mais HOPs (recommendations, tts)
- scout: Adicionar HOPs de search/discovery
- voice: Adicionar HOPs de TTS/loop

Mas já estão funcionais com os arquivos atuais.

---

**Sessão completa!** Builder funcionando, hook configurado, 261 arquivos sincronizados.
