# QA Agent Vision | Framework Universal de Quality Assurance

> **De**: Agente especifico GATO3
> **Para**: Framework QA reutilizavel para qualquer projeto web

---

## PROBLEMA ATUAL

Testes de qualidade em projetos web sao:
1. **Manuais** - Alguem precisa lembrar de rodar
2. **Inconsistentes** - Cada dev testa diferente
3. **Sem historico** - Nao sabemos se melhorou ou piorou
4. **Acoplados** - Cada projeto reinventa os checks
5. **Reativos** - Descobrimos bugs depois do deploy

---

## VISAO: QA-as-Code Framework

### Conceito Core

```
QA Agent = Config + Checks + Reports + History
```

Um unico agente que:
1. **Le configuracao** do projeto (qa.config.json)
2. **Executa checks** modulares e extensiveis
3. **Gera reports** padronizados (MD + JSON + HTML)
4. **Armazena historico** para comparacao
5. **Integra CI/CD** (GitHub Actions, pre-commit)

---

## ARQUITETURA PROPOSTA

```
qa_universal_agent/
├── core/
│   ├── runner.py           # Orquestrador de checks
│   ├── reporter.py         # Gerador de relatorios
│   ├── history.py          # Armazenamento de historico
│   └── config_loader.py    # Parser de qa.config.json
│
├── checks/                  # Checks modulares
│   ├── base_check.py       # Interface base
│   ├── pages/
│   │   ├── load_check.py   # Paginas carregam
│   │   ├── 404_check.py    # Links quebrados
│   │   └── redirect_check.py
│   ├── seo/
│   │   ├── meta_check.py   # Title, description
│   │   ├── og_check.py     # Open Graph
│   │   ├── schema_check.py # JSON-LD
│   │   └── sitemap_check.py
│   ├── a11y/
│   │   ├── aria_check.py   # ARIA labels
│   │   ├── contrast_check.py
│   │   ├── keyboard_check.py
│   │   └── heading_check.py
│   ├── performance/
│   │   ├── lcp_check.py    # Core Web Vitals
│   │   ├── cls_check.py
│   │   └── fid_check.py
│   ├── security/
│   │   ├── headers_check.py # Security headers
│   │   ├── https_check.py
│   │   └── cors_check.py
│   └── ecommerce/          # Checks especificos e-commerce
│       ├── checkout_check.py
│       ├── cart_check.py
│       └── payment_check.py
│
├── integrations/
│   ├── github_actions.py   # CI/CD
│   ├── slack_notifier.py   # Alertas
│   ├── supabase_store.py   # Persistencia
│   └── mcp_browser.py      # Browser automation
│
├── templates/
│   ├── report.md.jinja     # Template MD
│   ├── report.html.jinja   # Template HTML
│   └── config.example.json # Config exemplo
│
└── cli/
    ├── run.py              # CLI runner
    └── init.py             # Inicializador de projeto
```

---

## CONFIGURACAO POR PROJETO

Cada projeto tem seu `qa.config.json`:

```json
{
  "$schema": "https://qa-agent.gato3.dev/schema.json",
  "project": "gato3-landing",
  "version": "1.0.0",

  "environments": {
    "production": "https://gatoaocubo.lovable.app",
    "staging": "https://staging.gatoaocubo.lovable.app",
    "local": "http://localhost:5173"
  },

  "routes": [
    { "path": "/", "name": "Home", "critical": true },
    { "path": "/catalogo", "name": "Catalog", "critical": true },
    { "path": "/produto/:slug", "name": "Product", "critical": true, "samples": ["tapete-gelado"] },
    { "path": "/b2b", "name": "B2B", "critical": false }
  ],

  "checks": {
    "pages": { "enabled": true, "timeout": 30000 },
    "seo": {
      "enabled": true,
      "rules": {
        "title_max": 60,
        "description_min": 50,
        "description_max": 160
      }
    },
    "a11y": { "enabled": true, "level": "AA" },
    "performance": {
      "enabled": true,
      "thresholds": { "lcp": 2500, "cls": 0.1 }
    },
    "security": { "enabled": true },
    "ecommerce": {
      "enabled": true,
      "checkout_endpoint": "/functions/v1/create-shopify-checkout",
      "test_variant_id": "gid://shopify/ProductVariant/123"
    }
  },

  "integrations": {
    "github_actions": true,
    "slack_webhook": "https://hooks.slack.com/...",
    "history_storage": "supabase"
  },

  "thresholds": {
    "pass_rate": 0.95,
    "critical_must_pass": true,
    "block_deploy_on_fail": true
  }
}
```

---

## CASOS DE USO

### 1. Developer Local
```bash
# Instalar
npm install -g @gato3/qa-agent

# Inicializar projeto
qa init

# Rodar checks
qa run --env local

# Rodar check especifico
qa run --check seo

# Ver historico
qa history --last 10
```

### 2. CI/CD (GitHub Actions)
```yaml
# .github/workflows/qa.yml
name: QA Checks

on:
  pull_request:
  push:
    branches: [main]

jobs:
  qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gato3/qa-action@v1
        with:
          config: qa.config.json
          environment: staging
          fail_on_critical: true
```

### 3. Pre-commit Hook
```bash
# .husky/pre-push
qa run --check pages,seo --env local --quick
```

### 4. Scheduled Monitoring
```yaml
# Cron job diario
on:
  schedule:
    - cron: '0 6 * * *'  # 6am daily

jobs:
  monitor:
    runs-on: ubuntu-latest
    steps:
      - uses: gato3/qa-action@v1
        with:
          environment: production
          notify: slack
```

---

## TIPOS DE CHECKS

### Tier 1: Universal (qualquer site)
| Check | Descricao | Automacao |
|-------|-----------|-----------|
| PageLoad | Todas paginas retornam 200 | Browser MCP |
| BrokenLinks | Links internos funcionam | Crawler |
| SEOMeta | Title, description, h1 | DOM extraction |
| SEOSchema | JSON-LD valido | Parser |
| A11yAria | ARIA labels presentes | DOM scan |
| A11yHeadings | Hierarquia correta | DOM scan |
| SecurityHeaders | CSP, HSTS, X-Frame | HTTP headers |
| Performance | Core Web Vitals | Lighthouse |

### Tier 2: E-commerce
| Check | Descricao | Automacao |
|-------|-----------|-----------|
| CartFlow | Add to cart funciona | API call |
| CheckoutFlow | Checkout redireciona | API call |
| PriceDisplay | Precos formatados | DOM extraction |
| StockDisplay | Estoque atualizado | API validation |
| PaymentGateway | Gateway responde | Health check |

### Tier 3: Projeto-Especifico
| Check | Descricao | Automacao |
|-------|-----------|-----------|
| CustomAPI | Endpoints especificos | Configurable |
| CustomFlow | Fluxos de usuario | Playwright script |
| CustomValidation | Regras de negocio | Custom function |

---

## SISTEMA DE REPORTS

### Report Structure
```json
{
  "meta": {
    "project": "gato3-landing",
    "environment": "production",
    "timestamp": "2025-11-28T14:30:00Z",
    "duration_ms": 45000,
    "agent_version": "1.0.0"
  },
  "summary": {
    "total_checks": 45,
    "passed": 42,
    "failed": 2,
    "warnings": 1,
    "score": 93.3,
    "grade": "A"
  },
  "categories": {
    "pages": { "passed": 10, "failed": 0, "score": 100 },
    "seo": { "passed": 8, "failed": 1, "score": 88.9 },
    "a11y": { "passed": 12, "failed": 1, "score": 92.3 },
    "performance": { "passed": 4, "failed": 0, "score": 100 },
    "security": { "passed": 5, "failed": 0, "score": 100 },
    "ecommerce": { "passed": 3, "failed": 0, "score": 100 }
  },
  "issues": [
    {
      "id": "seo-001",
      "severity": "warning",
      "category": "seo",
      "check": "meta_description",
      "page": "/",
      "message": "Description too short (45 chars, min 50)",
      "suggestion": "Expand meta description to 50-160 characters"
    }
  ],
  "history": {
    "previous_score": 91.2,
    "trend": "+2.1",
    "runs_analyzed": 10
  }
}
```

### Report Formats
1. **JSON** - Para integracao e historico
2. **Markdown** - Para PRs e documentacao
3. **HTML** - Para visualizacao interativa
4. **Slack** - Resumo para notificacoes

---

## HISTORICO E TRENDS

### Armazenamento
```sql
-- Supabase table
CREATE TABLE qa_runs (
  id UUID PRIMARY KEY,
  project TEXT NOT NULL,
  environment TEXT NOT NULL,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  score NUMERIC(5,2),
  grade TEXT,
  summary JSONB,
  issues JSONB,
  duration_ms INTEGER
);

CREATE INDEX idx_qa_runs_project ON qa_runs(project, timestamp DESC);
```

### Metricas de Evolucao
- Score medio por semana
- Trend de issues por categoria
- Tempo de resolucao de issues
- Regressoes detectadas

### Dashboard
```
Project: GATO3 Landing
Period: Last 30 days

Score Trend:
  Week 1: 85.2 [====----]
  Week 2: 88.5 [=====---]
  Week 3: 91.3 [======--]
  Week 4: 93.3 [=======-] <- Current

Issues Resolved: 12
New Issues: 3
Net Improvement: +9

Top Categories:
  SEO: +8.2 points
  A11y: +5.1 points
  Performance: +3.0 points
```

---

## ROADMAP DE IMPLEMENTACAO

### Phase 1: Core Framework (MVP)
- [ ] Config loader (qa.config.json)
- [ ] Check runner (orquestrador)
- [ ] Basic checks (pages, seo, a11y)
- [ ] MD report generator
- [ ] CLI (qa run, qa init)

### Phase 2: E-commerce & CI/CD
- [ ] E-commerce checks (cart, checkout)
- [ ] GitHub Actions integration
- [ ] JSON report format
- [ ] History storage (Supabase)

### Phase 3: Advanced Features
- [ ] Performance checks (Lighthouse)
- [ ] Security checks (headers, CORS)
- [ ] Slack notifications
- [ ] HTML dashboard
- [ ] Trend analysis

### Phase 4: Extensibility
- [ ] Custom check API
- [ ] Plugin system
- [ ] Multi-project dashboard
- [ ] Scheduled monitoring

---

## BENEFICIOS

### Para Developers
- Setup em 5 minutos (qa init)
- Checks consistentes entre projetos
- Historico de evolucao
- Bloqueio de deploy em falha critica

### Para Negocio
- Menos bugs em producao
- SEO monitorado continuamente
- Acessibilidade garantida
- Metricas de qualidade

### Para Escala
- Um agente, N projetos
- Configuracao declarativa
- Extensivel com plugins
- Integracao CI/CD nativa

---

## EXEMPLO DE USO CROSS-PROJECT

```bash
# Projeto 1: GATO3
cd gato3-landing
qa run --env production
# Score: 93.3 (A)

# Projeto 2: Outro e-commerce
cd outro-ecommerce
qa run --env production
# Score: 87.1 (B+)

# Projeto 3: Site institucional
cd site-institucional
qa run --env production
# Score: 95.8 (A+)

# Dashboard consolidado
qa dashboard --projects gato3,outro,institucional
# Mostra scores comparativos
```

---

## CONCLUSAO

O agente QA atual eh um **ponto de partida**. A visao eh evoluir para um **framework universal** que:

1. **Separa configuracao de implementacao**
2. **Modulariza checks** para reuso
3. **Persiste historico** para analise
4. **Integra CI/CD** nativamente
5. **Escala** para multiplos projetos

**Proximo passo**: Decidir se implementamos o framework ou se o agente atual atende as necessidades imediatas do GATO3.

---

**Version**: Vision 1.0
**Author**: CODEXA Meta-Construction System
**Date**: 2025-11-28
