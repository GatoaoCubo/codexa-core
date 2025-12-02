# LLM Platforms Documentation

This directory contains documentation snapshots from major LLM providers.

## 🤖 Platforms

### Anthropic (Claude)
- **Docs**: https://docs.anthropic.com
- **Focus**: Prompt engineering, tool use, vision, streaming
- **Refresh**: Weekly (Critical)
- **Local files**: `anthropic/`

### OpenAI (GPT)
- **Docs**: https://platform.openai.com/docs
- **Focus**: GPT-4, embeddings, fine-tuning, assistants API
- **Refresh**: Weekly (High)
- **Local files**: `openai/`

### Google (Gemini)
- **Docs**: https://ai.google.dev/docs
- **Focus**: Gemini API, multimodal, function calling
- **Refresh**: Weekly (High)
- **Local files**: `google/`

### Cohere
- **Docs**: https://docs.cohere.com
- **Focus**: Embeddings, rerank, RAG
- **Refresh**: Bi-weekly (Medium)
- **Local files**: `cohere/`

---

## 📖 Usage

### Read Locally
All documentation is stored as Markdown files for offline access:

```bash
# Read Anthropic docs
cat anthropic/api_reference.md
cat anthropic/prompt_engineering.md

# Read OpenAI docs
cat openai/gpt_best_practices.md
```

### Refresh Documentation

```bash
# Refresh specific platform
python scripts/fontes/refresh_fonte.py --fonte anthropic_docs

# Refresh all LLM platforms
python scripts/fontes/sync_all.py --priority critical
```

### Search Across Platforms

The Scout system automatically searches across all LLM platform docs when you ask questions about:
- API usage
- Prompt engineering
- Function calling / tool use
- Vision capabilities
- Streaming responses
- Rate limits
- Best practices

---

## 🔄 Update Schedule

| Platform | Priority | Frequency | Next Check |
|----------|----------|-----------|------------|
| Anthropic | Critical | Weekly | 2025-12-01 |
| OpenAI | High | Weekly | 2025-12-01 |
| Google | High | Weekly | 2025-12-01 |
| Cohere | Medium | Bi-weekly | 2025-12-08 |

---

## 🎯 When to Use

Use these docs when:
- 🔧 **Developing agents** - Learn API patterns and best practices
- 📝 **Optimizing prompts** - Study prompt engineering techniques
- 🛠️ **Implementing features** - Tool use, vision, streaming
- 🐛 **Debugging issues** - Rate limits, errors, troubleshooting
- 📊 **Comparing platforms** - Choose the right LLM for your needs

---

**Last Updated**: 2025-11-24
**Total Platforms**: 4
**Total Documentation Files**: ~20 files
