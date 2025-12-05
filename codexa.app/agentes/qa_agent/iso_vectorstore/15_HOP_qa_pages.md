<!-- iso_vectorstore -->
<!--
  Source: qa_pages_HOP.md
  Agent: qa_agent
  Synced: 2025-12-05
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# MODULE_METADATA
id: qa_pages_check
version: 1.0.0
purpose: Validar carregamento de todas as paginas do {{BRAND_NAME}}
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
**Objective**: Verificar que todas as paginas do {{BRAND_NAME}} carregam corretamente

## Standards
- Pagina deve retornar 200 OK
- Nenhum erro visivel no conteudo
- Conteudo principal presente
- Tempo de carregamento < 5s

## Constraints
- Usar browser MCP para screenshots
- Usar extract_text para verificar conteudo
- Reportar todos os erros encontrados

# VALIDATION

- [ ] Todas as rotas criticas testadas
- [ ] Screenshots salvos para falhas
- [ ] Tempo de execucao < 5min
- [ ] Relatorio gerado em formato padrao

# CONTEXT

**Upstream**: /prime-qa
**Downstream**: qa_report_generator
**Usage**: Primeiro step do QA suite completo
