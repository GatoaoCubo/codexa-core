<!-- iso_vectorstore -->
<!--
  Source: qa_pages_HOP.md
  Agent: qa_gato3_agent
  Synced: 2025-12-02
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# MODULE_METADATA
id: qa_pages_check
version: 1.0.0
purpose: Validar carregamento de todas as paginas do GATO3
category: qa/pages
dependencies: [browser_mcp]

# INPUT_CONTRACT
$base_url: string (URL base do projeto)
$routes: array (lista de rotas para validar)

# OUTPUT_CONTRACT
$report: PageCheckReport {
  total: number,
  passed: number,
  failed: number,
  results: PageResult[]
}

# TASK

**Role**: QA Page Validator
**Objective**: Verificar que todas as paginas do GATO3 carregam corretamente

## Standards
- Pagina deve retornar 200 OK
- Nenhum erro visivel no conteudo
- Conteudo principal presente
- Tempo de carregamento < 5s

## Constraints
- Usar browser MCP para screenshots
- Usar extract_text para verificar conteudo
- Reportar todos os erros encontrados

# STEPS

### 1. Preparar Lista de Rotas
Carregar rotas do config.json ou usar padrao:
- `/` (B2C Landing)
- `/b2b` (Partners)
- `/catalogo` (Catalog)
- `/produto/tapete-refrescante-65x50` (Product sample)
- `/login` (Auth)

### 2. Para Cada Rota
```
a. Construir URL completa: $base_url + $route
b. Executar mcp__browser__screenshot
c. Executar mcp__browser__extract_text
d. Verificar presenca de conteudo esperado
e. Verificar ausencia de mensagens de erro
f. Registrar resultado (PASS/FAIL)
```

### 3. Analisar Resultados
```
- Contar total de paginas testadas
- Contar paginas OK vs falhas
- Identificar patterns de erro
```

### 4. Gerar Relatorio
```markdown
## Page Load Check Results

| Route | Status | Time | Notes |
|-------|--------|------|-------|
| / | PASS | 1.2s | OK |
| /catalogo | PASS | 2.1s | OK |
| /produto/xyz | FAIL | - | 404 Not Found |

### Summary
- Total: X
- Passed: Y
- Failed: Z
```

# VALIDATION

- [ ] Todas as rotas criticas testadas
- [ ] Screenshots salvos para falhas
- [ ] Tempo de execucao < 5min
- [ ] Relatorio gerado em formato padrao

# CONTEXT

**Upstream**: /prime-qa-gato3
**Downstream**: qa_report_generator
**Usage**: Primeiro step do QA suite completo
