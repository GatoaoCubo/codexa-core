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

**Nota**: Puppeteer baixará automaticamente o Chromium (~150MB) durante a instalação. Isso garante que o browser funcione sem Chrome pré-instalado.

### Chrome/Chromium Setup

O servidor usa uma estratégia inteligente de fallback:

1. **Bundled Chromium (Padrão)**: Puppeteer baixa automaticamente uma versão do Chromium
   - Local: `node_modules/puppeteer/.local-chromium/`
   - Não requer Chrome instalado no sistema
   - Funciona em qualquer ambiente

2. **System Chrome (Opcional)**: Use o Chrome do sistema com variável de ambiente
   ```bash
   # Windows
   set CHROME_PATH=C:\Program Files\Google\Chrome\Application\chrome.exe

   # Linux
   export CHROME_PATH=/usr/bin/google-chrome

   # macOS
   export CHROME_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
   ```

3. **Fallback Automático**: Se o launch falhar, tenta com configuração mínima

### Troubleshooting

**Erro: "Failed to launch browser"**
- Solução 1: `npm install puppeteer` (garante que Chromium seja baixado)
- Solução 2: Defina `CHROME_PATH` para seu Chrome local
- Solução 3: Verifique permissões e espaço em disco (~200MB necessário)

**Chromium não baixou durante instalação**
```bash
# Força o download do Chromium
node node_modules/puppeteer/install.js
```

**Windows: Erro de permissão**
- Execute o terminal como Administrador
- Ou instale em diretório com permissões de escrita

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

## Arquitetura de Fallback

O `getBrowser()` implementa 3 níveis de fallback:

```javascript
// Nível 1: System Chrome (se CHROME_PATH definido)
if (process.env.CHROME_PATH) {
  launchOptions.executablePath = process.env.CHROME_PATH;
}

// Nível 2: Bundled Chromium (default Puppeteer)
// executablePath omitido = usa Chromium do npm

// Nível 3: Retry com args mínimos
minimalOptions = { headless: 'new', args: ['--no-sandbox'] }
```

**Benefícios**:
- Funciona sem Chrome instalado (Chromium bundled)
- Usa Chrome do sistema se disponível (melhor performance)
- Retry automático com configuração mínima
- Mensagens de erro com soluções claras

---

**Versão**: 1.1.0 (2025-12-04)
**Dependências**: Puppeteer (bundled Chromium), Puppeteer Stealth, MCP SDK
**Changelog**: v1.1.0 - Adicionado fallback para Chromium bundled, erro handling robusto
