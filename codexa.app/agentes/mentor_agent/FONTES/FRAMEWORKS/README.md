# Frameworks & SDKs Documentation

This directory contains documentation for AI/LLM development frameworks.

## 🛠️ Frameworks

### LangChain
- **Docs**: https://python.langchain.com/docs
- **Focus**: Agents, chains, RAG, tools, memory
- **Refresh**: Weekly (High)
- **Local files**: `langchain/`

### Vercel AI SDK
- **Docs**: https://sdk.vercel.ai/docs
- **Focus**: Streaming, React hooks, generative UI
- **Refresh**: Weekly (High)
- **Local files**: `vercel_ai_sdk/`

### LlamaIndex
- **Docs**: https://docs.llamaindex.ai
- **Focus**: Indexing, querying, RAG, vector stores
- **Refresh**: Bi-weekly (Medium)
- **Local files**: `llamaindex/`

### CrewAI
- **Docs**: https://docs.crewai.com
- **Focus**: Multi-agent systems, crews, collaboration
- **Refresh**: Bi-weekly (Medium)
- **Local files**: `crewai/`

---

## 📖 Usage

### Read Locally
```bash
# LangChain docs
cat langchain/agents.md
cat langchain/rag_guide.md

# Vercel AI SDK
cat vercel_ai_sdk/streaming.md
```

### Refresh Documentation
```bash
# Refresh specific framework
python scripts/fontes/refresh_fonte.py --fonte langchain_docs

# Refresh all frameworks
python scripts/fontes/sync_all.py --priority high
```

---

## 🔄 Update Schedule

| Framework | Priority | Frequency | Next Check |
|-----------|----------|-----------|------------|
| LangChain | High | Weekly | 2025-12-01 |
| Vercel AI SDK | High | Weekly | 2025-12-01 |
| LlamaIndex | Medium | Bi-weekly | 2025-12-08 |
| CrewAI | Medium | Bi-weekly | 2025-12-08 |

---

## 🎯 When to Use

Use these docs when:
- 🤖 **Building agents** - Agent architectures and patterns
- 🔗 **Creating chains** - Sequential operations
- 📚 **Implementing RAG** - Retrieval-augmented generation
- 🛠️ **Using tools** - External tool integration
- 🧠 **Managing memory** - Conversation context
- 🎨 **Building UI** - AI-powered user interfaces

---

**Last Updated**: 2025-11-24
**Total Frameworks**: 4
**Focus**: AI/LLM application development
