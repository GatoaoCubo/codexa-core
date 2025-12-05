# MCP Server Architecture Patterns

**Domain**: MCP (Model Context Protocol)
**Category**: MCP_PATTERNS
**Source**: MCP SDK + Production implementations
**Quality Score**: 0.83

---

## Resumo Executivo

MCP servers sao processos separados que fornecem tools, resources e prompts para LLMs via protocolo padronizado. Uma boa arquitetura de server garante performance, confiabilidade e extensibilidade. Este documento cobre patterns arquiteturais para MCP servers em producao.

## Conceitos-Chave

### **Server Lifecycle**
Fases do ciclo de vida de um MCP server:

```
INITIALIZE
  └─> Load config
  └─> Build index (if needed)
  └─> Register tools
  └─> Start listening

RUNNING
  └─> Handle requests
  └─> Maintain state
  └─> Update index (incremental)

SHUTDOWN
  └─> Persist state
  └─> Close connections
  └─> Cleanup resources
```

### **Request/Response Pattern**
Estrutura padrao de comunicacao:

```json
// Request
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "mcp__scout__discover",
    "arguments": {
      "query": "find HOP files"
    }
  },
  "id": 1
}

// Response
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found 15 HOP files..."
      }
    ]
  },
  "id": 1
}
```

### **State Management**
Gerenciar estado entre requests:

```python
class ServerState:
    def __init__(self):
        self.index = None        # File index
        self.cache = LRUCache()  # Result cache
        self.sessions = {}       # Active sessions

    async def initialize(self):
        self.index = await build_index()

    def get_cached(self, key):
        return self.cache.get(key)

    def set_cached(self, key, value, ttl=300):
        self.cache.set(key, value, ttl)
```

### **Concurrency Model**
Lidar com multiplas requests simultaneas:

```python
# Option 1: Async handlers (recommended)
async def handle_request(request):
    async with rate_limiter:
        result = await process(request)
    return result

# Option 2: Thread pool for blocking operations
from concurrent.futures import ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=4)

async def handle_blocking(request):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(executor, blocking_function, request)
    return result
```

## Como Aplicar

1. **Estruturar o servidor**
   ```
   mcp-servers/scout-mcp/
   ├── index.js              # Entry point
   ├── package.json          # Dependencies
   ├── src/
   │   ├── server.js         # Server setup
   │   ├── handlers/
   │   │   ├── discover.js   # Tool handlers
   │   │   ├── search.js
   │   │   └── context.js
   │   ├── services/
   │   │   ├── index.js      # Indexing service
   │   │   ├── search.js     # Search service
   │   │   └── cache.js      # Caching service
   │   └── utils/
   │       ├── logger.js
   │       └── config.js
   └── README.md
   ```

2. **Implementar inicializacao**
   ```javascript
   import { Server } from '@modelcontextprotocol/sdk/server/index.js';

   class ScoutServer {
       constructor() {
           this.server = new Server({
               name: 'scout-mcp',
               version: '1.0.0'
           });
           this.state = new ServerState();
       }

       async initialize() {
           // Build file index
           await this.state.buildIndex();

           // Register tools
           this.registerTools();

           // Start server
           await this.server.connect(transport);
       }

       registerTools() {
           this.server.setRequestHandler('tools/list', () => ({
               tools: TOOL_DEFINITIONS
           }));

           this.server.setRequestHandler('tools/call', (request) =>
               this.handleToolCall(request)
           );
       }
   }
   ```

3. **Implementar handlers com error handling**
   ```javascript
   async handleToolCall(request) {
       const { name, arguments: args } = request.params;

       try {
           const handler = this.handlers[name];
           if (!handler) {
               throw new ToolNotFoundError(name);
           }

           const result = await handler(args, this.state);

           return {
               content: [{
                   type: 'text',
                   text: JSON.stringify(result, null, 2)
               }]
           };
       } catch (error) {
           return {
               content: [{
                   type: 'text',
                   text: JSON.stringify({
                       error: true,
                       code: error.code || 'INTERNAL_ERROR',
                       message: error.message
                   })
               }],
               isError: true
           };
       }
   }
   ```

4. **Configurar para Claude Code**
   ```json
   // .mcp.json
   {
       "mcpServers": {
           "scout": {
               "command": "node",
               "args": ["path/to/mcp-servers/scout-mcp/index.js"],
               "env": {
                   "SCOUT_ROOT": "{{PROJECT_ROOT}}",
                   "SCOUT_LOG_LEVEL": "info"
               }
           }
       }
   }
   ```

## Exemplos Praticos

### Exemplo 1: Server com Caching

**Problema**: Searches repetidas sao lentas

**Solucao**:
```javascript
class CachedSearchService {
    constructor() {
        this.cache = new Map();
        this.ttl = 60000; // 1 minute
    }

    async search(query, options) {
        const cacheKey = this.getCacheKey(query, options);

        // Check cache
        const cached = this.cache.get(cacheKey);
        if (cached && !this.isExpired(cached)) {
            return cached.results;
        }

        // Execute search
        const results = await this.executeSearch(query, options);

        // Store in cache
        this.cache.set(cacheKey, {
            results,
            timestamp: Date.now()
        });

        return results;
    }

    isExpired(entry) {
        return Date.now() - entry.timestamp > this.ttl;
    }
}
```

**Resultado**: 90% hit rate, 10x faster repeated queries

### Exemplo 2: Graceful Shutdown

**Problema**: Server perde estado ao reiniciar

**Solucao**:
```javascript
class PersistentServer {
    async start() {
        // Load persisted state
        this.state = await this.loadState();

        // Register shutdown handlers
        process.on('SIGTERM', () => this.shutdown());
        process.on('SIGINT', () => this.shutdown());
    }

    async shutdown() {
        console.log('Shutting down gracefully...');

        // Save current state
        await this.saveState();

        // Close connections
        await this.server.close();

        process.exit(0);
    }

    async saveState() {
        const state = {
            index: this.state.index.serialize(),
            lastUpdated: Date.now()
        };
        await fs.writeFile('.scout-state.json', JSON.stringify(state));
    }
}
```

**Resultado**: Index preservado entre restarts

## Quando Usar

- **USE async/await quando**:
  - I/O bound operations (file, network)
  - Multiple concurrent requests expected
  - Need to avoid blocking

- **USE thread pool quando**:
  - CPU-bound processing
  - Legacy sync libraries
  - Large file parsing

- **USE caching quando**:
  - Same queries repeat frequently
  - Results dont change often
  - Latency is critical

- **USE state persistence quando**:
  - Index build is expensive
  - Server restarts are common
  - Data changes infrequently

## Relacionado

- Ver tambem: `tool_design.md`
- SDK: @modelcontextprotocol/sdk
- Reference: scout_agent/PRIME.md

---

**Processado**: 2025-12-05
**Tokens**: ~1150
