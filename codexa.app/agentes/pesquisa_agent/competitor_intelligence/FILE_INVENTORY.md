# Inventário Completo de Arquivos - Competitor Intelligence System

**Data**: 2025-11-23
**Sessão**: Criação inicial do sistema

---

## 📊 Resumo Quantitativo

| Categoria | Quantidade | Tamanho Total |
|-----------|------------|---------------|
| **Documentação Core** | 6 arquivos | ~60 KB |
| **Configuração** | 1 arquivo | 4.1 KB |
| **Source Databases** | 4 arquivos | ~31 KB |
| **Scripts** | 2 arquivos | ~14 KB |
| **Docs Gerados** | 4 arquivos | ~23 KB |
| **Relatórios** | 1 arquivo | 11 KB |
| **Comandos** | 1 arquivo | 3.8 KB |
| **TOTAL** | **19 arquivos** | **~147 KB** |

---

## 📁 Arquivos Criados Hoje (2025-11-23)

### Documentação Principal (8 arquivos)
```
competitor_intelligence/
├── INDEX.md                    (8.6 KB) - Hub central de navegação
├── README.md                   (13 KB)  - Documentação completa
├── QUICKSTART.md               (6.4 KB) - Guia rápido 5 min
├── EXAMPLES.md                 (12 KB)  - 8 exemplos práticos
├── SYSTEM_OVERVIEW.md          (15 KB)  - Visão técnica
├── config.json                 (4.1 KB) - Configuração sistema
├── FILE_INVENTORY.md           (este)   - Inventário de arquivos
└── commands/
    └── update_competitor_docs.md (3.8 KB) - Slash command
```

### Source Databases (4 arquivos - 31 KB)
```
sources/
├── ai_courses_platforms.json   (6.9 KB) - 10 plataformas
├── marketplaces_docs.json      (7.2 KB) - 9 marketplaces
├── ecommerce_trends.json       (8.5 KB) - 12 fontes
└── compliance_sources.json     (8.8 KB) - 8 regulações
```

### Scripts de Automação (2 arquivos - 14 KB)
```
scripts/
├── fetch_docs.py               (8.5 KB) - Fetcher Python
└── monitor_changes.sh          (5.7 KB) - Monitor Bash
```

### Documentação Gerada (4 arquivos - 23 KB)
```
docs/
├── ecommerce_trends/
│   └── pwc_brasil/
│       ├── overview_2025-11-23_160800.md (4.2 KB)
│       └── latest.md                      (4.2 KB)
└── compliance_sources/
    └── anpd/
        ├── overview_2025-11-23_160800.md (7.1 KB)
        └── latest.md                      (7.1 KB)
```

### Relatórios (1 arquivo - 11 KB)
```
snapshots/
└── 2025-11-23/
    └── update_report_quick_2025-11-23_160800.md (11 KB)
```

---

## 🔄 Oportunidades de Consolidação

### 1. Documentação Principal → system

**Problema**: 6 arquivos de documentação com overlapping

**Proposta de Consolidação**:
```
system/
├── system.meta.json           # Template meta-configurável
├── docs.template.md           # Template unificado de docs
└── generated/                 # Docs geradas dinamicamente
    ├── INDEX.md
    ├── README.md
    ├── QUICKSTART.md
    └── EXAMPLES.md
```

### 2. Source Databases → system

**Problema**: 4 JSONs com estrutura similar

**Proposta**:
```
system/
├── source.schema.json         # Schema genérico
└── sources.meta.json          # Meta-configuração
    {
      "categories": {
        "{CATEGORY_NAME}": {
          "metadata": "{META}",
          "sources": "{SOURCES}"
        }
      }
    }
```

### 3. Scripts → system

**Problema**: 2 scripts com lógica duplicada

**Proposta**:
```
system/
├── workflow.meta.json         # Define workflows
└── scripts/
    └── executor.py            # Executor genérico
```

---

## 🎯 Arquivos Candidatos para Camada system

### Alta Prioridade (Máximo Reuso)

#### 1. **source.schema.json** → Template de Fonte
```json
{
  "{SOURCE_ID}": {
    "name": "{DISPLAY_NAME}",
    "tier": "{free|paid|premium|...}",
    "priority": "{high|medium|low}",
    "urls": {
      "{URL_TYPE}": "{URL}"
    },
    "monitoring": {
      "{METRIC}": "{BOOLEAN|THRESHOLD}"
    },
    "metrics": {
      "{METRIC_NAME}": "{VALUE|RANGE}"
    }
  }
}
```

**Benefícios**:
- Adicionar fontes sem reescrever estrutura
- Validação automática via JSON Schema
- Flexível para qualquer tipo de fonte

#### 2. **doc.template.md** → Template de Documentação
```markdown
# {TITLE}

**Fonte**: {SOURCE_NAME}
**URL**: {SOURCE_URL}
**Data**: {FETCH_DATE}
**Categoria**: {CATEGORY}
**Prioridade**: {PRIORITY}

---

## {SECTION_1_TITLE}

{SECTION_1_CONTENT}

---

## 💡 {INSIGHTS_SECTION}

{INSIGHTS_LIST}

---

## 📈 {ACTIONS_SECTION}

{ACTIONS_LIST}

---

**Status**: {STATUS}
**Próxima atualização**: {NEXT_UPDATE}
```

**Benefícios**:
- Consistência automática
- Fácil personalização por tipo de fonte
- Geração dinâmica

#### 3. **workflow.meta.json** → Workflows Configuráveis
```json
{
  "workflows": {
    "{WORKFLOW_NAME}": {
      "description": "{DESCRIPTION}",
      "triggers": {
        "schedule": "{CRON_EXPRESSION}",
        "manual": "{COMMAND}",
        "event": "{EVENT_TYPE}"
      },
      "steps": [
        {
          "action": "{ACTION_TYPE}",
          "params": {
            "{PARAM}": "{VALUE}"
          },
          "on_success": "{NEXT_STEP}",
          "on_failure": "{ERROR_HANDLER}"
        }
      ],
      "output": {
        "format": "{markdown|json|html}",
        "destination": "{PATH_TEMPLATE}"
      }
    }
  }
}
```

**Benefícios**:
- Workflows sem código
- Fácil A/B testing de processos
- Reutilizável entre projetos

#### 4. **system.meta.json** → Configuração Mestra
```json
{
  "project": {
    "name": "{PROJECT_NAME}",
    "version": "{VERSION}",
    "description": "{DESCRIPTION}"
  },
  "context": {
    "market": "{MARKET}",
    "language": "{LANGUAGE}",
    "domain": "{DOMAIN}"
  },
  "categories": [
    {
      "id": "{CATEGORY_ID}",
      "name": "{CATEGORY_NAME}",
      "schema": "{SCHEMA_PATH}",
      "update_frequency": "{FREQUENCY}"
    }
  ],
  "integrations": {
    "{INTEGRATION_NAME}": {
      "enabled": "{BOOLEAN}",
      "config": "{CONFIG_PATH}"
    }
  },
  "user_preferences": {
    "{PREFERENCE}": "{VALUE|NULL}"
  }
}
```

**Benefícios**:
- Single source of truth
- Fácil clonagem para outros mercados/domínios
- User-driven customization

---

## 🏗️ Arquitetura Proposta: Camada system

### Estrutura Atual vs. Proposta

#### ATUAL (Hardcoded)
```
competitor_intelligence/
├── sources/
│   ├── ai_courses_platforms.json      # Hardcoded
│   ├── marketplaces_docs.json         # Hardcoded
│   ├── ecommerce_trends.json          # Hardcoded
│   └── compliance_sources.json        # Hardcoded
├── scripts/
│   ├── fetch_docs.py                  # Lógica fixa
│   └── monitor_changes.sh             # Lógica fixa
└── [...]
```

#### PROPOSTA (Meta-Driven)
```
competitor_intelligence/
├── system/                            # NOVA CAMADA
│   ├── system.meta.json               # Config mestra
│   ├── schemas/
│   │   ├── source.schema.json
│   │   ├── doc.template.md
│   │   └── workflow.schema.json
│   ├── templates/
│   │   ├── report.template.md
│   │   ├── insight.template.md
│   │   └── action_plan.template.md
│   └── user_context/                  # Aguarda input user
│       ├── preferences.json
│       ├── custom_categories.json
│       └── custom_sources.json
│
├── sources/                           # Geradas de system
│   └── {category}.json
├── scripts/
│   └── meta_executor.py               # Engine genérico
└── [...]
```

---

## 📋 Templates system Propostos

### 1. **system/system.meta.json**
```json
{
  "project": {
    "name": "{NULL - user defines}",
    "domain": "{NULL - e.g., 'ai_courses', 'saas_tools', 'marketplaces'}",
    "market": "{NULL - e.g., 'brazil', 'latam', 'global'}",
    "language": "{NULL - e.g., 'pt-BR', 'en-US'}"
  },
  "categories": "{NULL - user adds categories dynamically}",
  "sources": "{NULL - user adds sources via schema}",
  "workflows": "{NULL - user defines custom workflows}",
  "integrations": {
    "claude_code": true,
    "mcp_servers": "{NULL - user enables}",
    "external_apis": "{NULL - user configures}"
  },
  "user_preferences": {
    "update_frequency": "{NULL - daily|weekly|monthly}",
    "alert_channels": "{NULL - slack|email|discord}",
    "priority_threshold": "{NULL - high|medium|low}",
    "output_format": "{NULL - markdown|json|html}"
  }
}
```

### 2. **system/schemas/source.schema.json**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "{source_id}": {
      "type": "object",
      "required": ["name", "urls"],
      "properties": {
        "name": {"type": "string"},
        "tier": {
          "type": "string",
          "enum": ["{USER_DEFINED}"]
        },
        "priority": {
          "type": "string",
          "enum": ["high", "medium", "low"]
        },
        "urls": {
          "type": "object",
          "additionalProperties": {"type": "string"}
        },
        "monitoring": {
          "type": "object",
          "additionalProperties": {"type": ["boolean", "number"]}
        },
        "metrics": {
          "type": "object",
          "additionalProperties": true
        },
        "custom_fields": {
          "type": "object",
          "description": "User can add ANY field"
        }
      }
    }
  }
}
```

### 3. **system/templates/doc.template.md**
```markdown
# {{title}}

**Fonte**: {{source.name}}
**URL**: {{source.url}}
**Data de Coleta**: {{fetch_date}}
**Categoria**: {{category}}
**Prioridade**: {{priority}}

---

{{#sections}}
## {{section.title}}

{{section.content}}

---
{{/sections}}

{{#insights}}
## 💡 {{insights.title}}

{{#insights.items}}
### {{insight.number}}. {{insight.title}}
**{{insight.type}}**: {{insight.description}}
**Ação**: {{insight.action}}
**Fonte**: {{insight.source}}

{{/insights.items}}
{{/insights}}

{{#actions}}
## 📈 {{actions.title}}

{{#actions.categories}}
### {{category.name}}

{{#category.items}}
{{item.checkbox}} {{item.description}}
{{/category.items}}

{{/actions.categories}}
{{/actions}}

---

**Status**: {{status}}
**Próxima atualização**: {{next_update}}
**Confiabilidade**: {{reliability}}
```

### 4. **system/workflows/default.workflow.json**
```json
{
  "quick_update": {
    "description": "Quick update - high priority sources only",
    "steps": [
      {
        "action": "load_sources",
        "filter": {"priority": "high"},
        "params": {
          "categories": "{NULL - user selects or 'all'}"
        }
      },
      {
        "action": "fetch_content",
        "method": "{NULL - 'webfetch'|'scraping'|'api'}",
        "params": {
          "rate_limit": "{NULL - user defines}",
          "timeout": "{NULL - user defines}"
        }
      },
      {
        "action": "extract_insights",
        "engine": "{NULL - 'claude'|'gpt'|'regex'}",
        "params": {
          "prompt_template": "{NULL - user provides}"
        }
      },
      {
        "action": "generate_docs",
        "template": "{NULL - 'doc.template.md' or custom}",
        "output_path": "{NULL - user defines pattern}"
      },
      {
        "action": "generate_report",
        "format": "{NULL - 'markdown'|'json'|'html'}",
        "template": "{NULL - user selects}"
      }
    ]
  }
}
```

---

## 🎯 Valores Intencionalmente em Branco (NULL)

### Filosofia

**Princípio**: Deixar placeholders `{NULL}` para que o **usuário escolha** baseado em:
- Contexto específico do projeto
- Preferências pessoais
- Restrições técnicas
- Objetivos de negócio

### Campos Principais com {NULL}

| Campo | Por que NULL? | Preenchimento |
|-------|---------------|---------------|
| `project.name` | Cada projeto é único | User input on init |
| `project.domain` | Domínio varia (AI, SaaS, etc.) | User selects from list |
| `market` | Brasil, LATAM, Global? | User defines |
| `categories` | Depende do domínio | User adds dynamically |
| `update_frequency` | Daily? Weekly? Custom? | User preference |
| `alert_channels` | Slack? Email? None? | User configures |
| `fetch_method` | WebFetch? Scraping? API? | User chooses per source |
| `output_format` | Markdown? JSON? Both? | User decides |
| `workflows` | Custom per use case | User defines steps |

---

## 🚀 Proposta de Implementação

### Fase 1: Criar Camada system
```bash
mkdir -p competitor_intelligence/system/{schemas,templates,workflows,user_context}
```

### Fase 2: Migrar para Templates
1. Extrair padrões dos JSONs atuais → `source.schema.json`
2. Converter docs → `doc.template.md`
3. Definir workflows → `*.workflow.json`

### Fase 3: User Context Layer
```json
// system/user_context/init.json
{
  "wizard": {
    "questions": [
      {
        "id": "project_name",
        "question": "What is your project name?",
        "type": "text",
        "required": true
      },
      {
        "id": "domain",
        "question": "What domain are you tracking?",
        "type": "choice",
        "options": [
          "ai_courses",
          "saas_tools",
          "marketplaces",
          "ecommerce_platforms",
          "other (specify)"
        ]
      },
      {
        "id": "market",
        "question": "Target market?",
        "type": "choice",
        "options": ["brazil", "latam", "global", "custom"]
      },
      {
        "id": "update_frequency",
        "question": "How often to update?",
        "type": "choice",
        "options": ["daily", "weekly", "monthly", "on-demand"]
      }
    ]
  }
}
```

### Fase 4: Meta Executor
```python
# system/executor.py
class MetaExecutor:
    def __init__(self, meta_config_path):
        self.meta = self.load_meta(meta_config_path)
        self.user_context = self.load_user_context()

    def execute_workflow(self, workflow_name, user_params=None):
        """Execute workflow with user context"""
        workflow = self.meta['workflows'][workflow_name]
        context = self.merge_context(self.user_context, user_params)

        for step in workflow['steps']:
            self.execute_step(step, context)

    def merge_context(self, base, user_params):
        """Merge base context with user runtime params"""
        # User params override defaults
        return {**base, **(user_params or {})}
```

---

## 📊 Comparação: Antes vs. Depois

### ANTES (Hardcoded)
```bash
# Para adicionar nova categoria:
1. Criar novo JSON: sources/new_category.json
2. Escrever estrutura completa manualmente
3. Atualizar fetch_docs.py
4. Atualizar monitor_changes.sh
5. Atualizar documentação (5 arquivos)

# Tempo estimado: 2-3 horas
```

### DEPOIS (system)
```bash
# Para adicionar nova categoria:
1. Adicionar em system.meta.json:
   {
     "categories": {
       "new_category": {
         "schema": "source.schema.json",
         "update_frequency": "weekly"
       }
     }
   }

2. Adicionar fontes via schema validado

3. python meta/executor.py --category new_category

# Tempo estimado: 5-10 minutos
```

---

## 💡 Benefícios da Arquitetura system

### 1. **Flexibilidade Máxima**
- User escolhe o que quer rastrear
- Sem código hardcoded
- Fácil A/B testing

### 2. **Reusabilidade**
- Mesmo sistema para qualquer domínio
- Clone para novos projetos em minutos
- Templates compartilháveis

### 3. **Manutenibilidade**
- Single source of truth (system/system.meta.json)
- Mudanças propagam automaticamente
- Versionamento simplificado

### 4. **Evolução Incremental**
- User começa simples
- Adiciona complexidade quando precisa
- Não força decisões prematuras

### 5. **Context-Aware**
- Sistema se adapta ao contexto do user
- Decisões em runtime, não design-time
- Feedback loop contínuo

---

## 🎯 Próximos Passos Sugeridos

### Curto Prazo
1. [ ] Criar estrutura `system/`
2. [ ] Extrair schema de source.json atual
3. [ ] Criar doc.template.md base
4. [ ] Testar geração a partir de meta

### Médio Prazo
5. [ ] Implementar meta_executor.py
6. [ ] Criar wizard de inicialização
7. [ ] Migrar sources atuais para meta
8. [ ] Validar com user feedback

### Longo Prazo
9. [ ] UI web para configuração meta
10. [ ] Marketplace de templates
11. [ ] AI-powered template generation
12. [ ] Multi-project orchestration

---

## 🤔 Perguntas para o Usuário

Para definir melhor os {NULL} values:

1. **Domínio**: Focar só em "AI courses" ou permitir qualquer domínio?
2. **Mercado**: Brasil only ou preparar para expansão LATAM/Global?
3. **Automação**: Quer wizard interativo ou config manual via JSON?
4. **Output**: Prefere Markdown, JSON, ambos, ou deixar escolha por workflow?
5. **Integração**: Quais MCP servers ou APIs quer habilitar?
6. **Prioridades**: Qual {NULL} preencher primeiro? (ex: workflows > schemas > templates)

---

**Próxima ação recomendada**: Criar estrutura system/ e migrar 1 categoria como POC?
