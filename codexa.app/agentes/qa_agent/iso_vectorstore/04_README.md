<!-- iso_vectorstore -->
<!--
  Source: README.md
  Agent: qa_agent
  Synced: 2025-12-05
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# qa_agent | Quality Assurance Specialist

> **Version**: 1.0.0
> **Type**: QA & Validation
> **Domain**: E-commerce (Generic)
> **Created**: 2025-12-05

---

## PURPOSE

Agente especializado em Quality Assurance para projetos e-commerce. Automatiza validacoes de UI, fluxos de usuario, SEO, acessibilidade e integridade do sistema.

## CAPABILITIES

### Core Validations

| Check | Description | Priority |
|-------|-------------|----------|
| Page Load | Verifica se todas as paginas carregam sem erros | CRITICAL |
| Images | Valida se imagens estao acessiveis e otimizadas | HIGH |
| Checkout Flow | Testa fluxo ate redirect para Shopify | CRITICAL |
| Responsiveness | Valida layout em mobile/tablet/desktop | HIGH |
| SEO | Checa title, meta, h1, structured data | MEDIUM |
| Broken Links | Encontra links quebrados internos/externos | HIGH |
| AI Chat | Testa chatbot AI com cenarios pre-definidos | HIGH |
| B2B Form | Valida formulario de contato B2B | MEDIUM |
| Accessibility | Verifica ARIA labels, contraste, navegacao | MEDIUM |

### Tools Available

- **Browser MCP**: screenshot, screenshot_full, extract_text, extract_html
- **Bash**: Executar comandos, rodar testes, verificar build
- **Read/Grep**: Inspecionar codigo, buscar patterns
- **WebFetch**: Verificar endpoints externos

## USAGE

### Quick Start

```bash
# Primar o agente
/prime-qa

# Executar suite completa
/qa-run-all

# Executar check especifico
/qa-check pages
/qa-check checkout
/qa-check seo
/qa-check a11y
```

### Slash Commands

| Command | Description |
|---------|-------------|
| `/prime-qa` | Carrega contexto do agente |
| `/qa-run-all` | Executa todos os checks |
| `/qa-check [type]` | Executa check especifico |
| `/qa-report` | Gera relatorio consolidado |

## STRUCTURE

```
qa_agent/
├── README.md           # Este arquivo
├── PRIME.md            # Contexto de dominio
├── INSTRUCTIONS.md     # Instrucoes operacionais
├── config.json         # Configuracao do agente
├── config/
│   ├── qa_rules.json       # Regras de QA
│   └── brand_example.json  # Exemplo de marca
├── prompts/            # HOPs de QA
│   ├── qa_pages_HOP.md
│   ├── qa_checkout_HOP.md
│   ├── qa_seo_HOP.md
│   └── qa_a11y_HOP.md
└── reports/            # Relatorios gerados
    └── .gitkeep
```

## CHANGELOG

### v1.0.0 (2025-12-05)
- Distilled from qa_gato3_agent
- Generic placeholders for any brand
- 9 core validation checks
- 4 slash commands
- Markdown + JSON reports
