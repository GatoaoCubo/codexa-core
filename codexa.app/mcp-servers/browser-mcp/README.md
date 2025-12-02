# Browser MCP Server

**Version**: 1.0.0 | **Status**: Production | **Purpose**: Visual market research

MCP Server para pesquisa de mercado com capacidade de screenshot e extração de dados de marketplaces brasileiros.

## Features

### Anti-Detection
- **Puppeteer Stealth Plugin** - Evita detecção de bot
- **User-Agent Rotation** - 5 user agents realistas
- **Viewport Randomization** - 4 resoluções comuns
- **Human-like Delays** - Delays aleatórios entre ações
- **Brazilian Locale** - Headers pt-BR configurados

### Tools Disponíveis

| Tool | Descrição |
|------|-----------|
| `screenshot` | Screenshot do viewport visível |
| `screenshot_full` | Screenshot da página inteira (com scroll) |
| `extract_html` | HTML renderizado (após JavaScript) |
| `extract_text` | Texto visível da página |
| `search_marketplace` | Busca em marketplace BR + screenshot |
| `multi_search` | Busca em múltiplos marketplaces |
| `list_screenshots` | Lista screenshots capturados |

### Marketplaces Suportados

- Mercado Livre
- Amazon BR
- Shopee
- Magazine Luiza
- Americanas
- Casas Bahia
- Submarino

## Instalação

```bash
cd codexa.app/mcp-servers/browser-mcp
npm install
```

## Configuração Claude Code

Adicione ao `.mcp.json`:

```json
{
  "mcpServers": {
    "browser": {
      "type": "stdio",
      "command": "node",
      "args": ["path/to/browser-mcp/index.js"]
    }
  }
}
```

## Uso

Após reiniciar Claude Code, as tools estarão disponíveis:

```
mcp__browser__screenshot(url)
mcp__browser__screenshot_full(url)
mcp__browser__extract_text(url)
mcp__browser__search_marketplace(marketplace, query)
mcp__browser__multi_search(query)
```

### Workflow de Pesquisa

1. `multi_search("garrafa termica")` - Busca em todos marketplaces
2. `Read` no filepath retornado - Análise visual do screenshot
3. Extrair insights de preços, títulos, badges

## Screenshots

Screenshots são salvos em:
```
browser-mcp/screenshots/
├── mercadolivre_com_br_garrafa_1234567890.png
├── amazon_com_br_s_k_garrafa_1234567891.png
└── ...
```

## Integração com Pesquisa Agent

Este MCP habilita o pesquisa_agent a:
- Capturar visualmente resultados de busca
- Analisar layouts e posicionamento de produtos
- Extrair dados mesmo de páginas com anti-scraping
- Coletar evidências visuais para relatórios

---

**Versão**: 1.0.0 (2025-11-27)
**Dependências**: Puppeteer, Puppeteer Stealth, MCP SDK
