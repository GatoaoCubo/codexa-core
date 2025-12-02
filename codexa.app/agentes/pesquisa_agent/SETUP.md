# SETUP GUIDE | Pesquisa Agent v2.6

**Universal setup instructions** for loading the Pesquisa Agent into different LLM platforms.

**Last Updated**: 2025-11-26

---

## 📋 PRE-REQUISITES

### Required Files
Ensure you have the complete `pesquisa_agent/` folder with:
- ✅ **PRIME.md** - Entry point
- ✅ **config/** - Agent configs + marketplaces + execution plans
- ✅ **prompts/** - 12 modular prompts
- ✅ **templates/** - research_notes.md template
- ✅ **user_research/** - Output directory

### Minimum Capabilities Required
- ✅ **web_search** - REQUIRED (cannot run without it)
- 📄 **vision** - Optional (enables screenshot analysis)
- 📄 **file_search** - Optional (enables compliance rules lookup)
- 📄 **code_interpreter** - Optional (enables advanced metrics)

---

## 🤖 PLATFORM SETUP

### 1. CLAUDE CODE (Recommended)

#### Quick Start

```bash
# Navigate to agent folder
cd path/to/pesquisa_agent/

# Load context via slash command (if configured)
/prime-pesquisa

# Or manually load PRIME.md
# Claude Code will auto-detect capabilities
```

#### Tools Mapping (Auto-Detected)

| Generic Capability | Claude Code Tool | Status |
|--------------------|------------------|--------|
| `web_search` | **WebSearch** | ✅ Required |
| `vision` | **Read** (images/PDFs) | ✅ Available |
| `file_search` | **Grep** + **Glob** | ✅ Available |
| `web_fetch` | **WebFetch** | ✅ 1380+ URLs |
| `code_interpreter` | **Bash** + **mcp__ide__executeCode** | ⚠️ Partial |

#### Example Usage

```
Execute market research for:

Product: Fone de ouvido Bluetooth esportivo
Category: Eletrônicos > Áudio
Target Audience: Atletas, 18-35 anos
Price Range: R$ 150 - R$ 280
Marketplace: Mercado Livre
```

**Output Location**: `user_research/[produto]_research_notes.md`

#### MCP Voice (Optional)

If MCP Voice is configured, you can:
- `mcp__voice__listen` - Voice input for briefs
- `mcp__voice__speak` - Read results aloud
- `mcp__voice__ask_agent` - Query pesquisa agent

---

### 2. OPENAI (GPT-4 Assistants)

#### Setup Steps

1. **Create Assistant** at https://platform.openai.com/assistants

2. **Configure**:
   ```yaml
   Name: Pesquisa Agent BR
   Model: gpt-4-turbo-preview or gpt-4o
   Description: Brazilian e-commerce market research specialist
   ```

3. **Set Instructions**: Paste entire `PRIME.md` content

4. **Enable Tools**:
   - ✅ **Web Browsing** (web_search)
   - ✅ **Code Interpreter** (metrics)
   - ✅ **File Search** (see step 5)

5. **Create Vector Store** (for iso_vectorstore):
   - Name: "Pesquisa Knowledge Base"
   - Upload all 20 files from `iso_vectorstore/`
   - Attach to Assistant

**Capabilities**:
- ✅ web_search (Web Browsing)
- ✅ vision (native GPT-4 Vision)
- ✅ file_search (Vector Store)
- ✅ code_interpreter (native)

---

### 3. CUSTOM GPT (ChatGPT Plus)

#### Setup Steps

1. Go to https://chat.openai.com/gpts/editor

2. **Configure**:
   ```yaml
   Name: Pesquisa Agent BR
   Description: Brazilian market research for e-commerce (22-block reports)
   Instructions: [PASTE PRIME.md CONTENT]
   ```

3. **Enable Capabilities**:
   - ✅ Web Browsing
   - ✅ Code Interpreter (optional)

4. **Upload Knowledge Files**:
   - `config/agent.json`
   - `config/marketplaces.json`
   - `config/accessible_urls.md`
   - `templates/research_notes.md`
   - Or upload all 20 files from `iso_vectorstore/`

5. **Conversation Starters**:
   - "Research: [product], R$ [price], [marketplace]"
   - "Analyze competitors for [product] on Mercado Livre"
   - "Build SEO taxonomy for [category]"

---

### 4. GEMINI (Google AI Studio)

#### Setup Steps

1. Go to https://aistudio.google.com/

2. **Create Prompt**:
   - Click "Create new prompt" → "Freeform prompt"

3. **System Instructions**: Paste `PRIME.md` content

4. **Enable Grounding**: Turn on "Google Search" for web_search capability

5. **Upload Files**:
   - `config/marketplaces.json`
   - `templates/research_notes.md`

**Capabilities**:
- ✅ web_search (Google Search grounding)
- ✅ vision (native Gemini Vision)
- ⚠️ file_search (via uploaded files, limited)
- ❌ code_interpreter (not available)

---

### 5. LOCAL LLMs (Ollama, LM Studio)

#### Requirements

**Minimum**:
- Model size: ≥13B parameters
- Context window: ≥32k tokens
- Function calling: Recommended

**Recommended Models**:
- Llama 3.1 70B (Ollama)
- Mixtral 8x22B
- Qwen 2.5 72B

#### Ollama Setup

```bash
# Pull model
ollama pull llama3.1:70b

# Create Modelfile with PRIME.md as system prompt
cat > Modelfile <<EOF
FROM llama3.1:70b

SYSTEM """
$(cat PRIME.md)
"""

PARAMETER temperature 0.7
PARAMETER num_ctx 32768
EOF

# Create custom model
ollama create pesquisa-agent -f Modelfile

# Run
ollama run pesquisa-agent
```

**Capabilities**:
- ❌ web_search (not native - user provides URLs manually)
- ⚠️ vision (if using llama3.2-vision)
- ❌ file_search (manual context injection)
- ❌ code_interpreter (not available)

**Web Search Workaround**: Use `config/accessible_urls.md` (1380+ URLs) for manual research.

---

## 🔧 CAPABILITIES CONFIGURATION

### Method 1: Auto-Detection (All Platforms)

Agent auto-detects on first tool use:
```
Agent: "Attempting web search..."
[Success] → web_search = true
[Failure] → web_search = false, fallback to manual
```

### Method 2: User Declaration

On first run, declare:
```
web_search: yes, vision: yes, file_search: no
```

### Method 3: Environment File

Create `.env`:
```bash
WEB_SEARCH=true           # Required
VISION=true               # Optional
FILE_SEARCH=false         # Optional
CODE_INTERPRETER=false    # Optional
MARKETPLACE_PRIORITY=mercadolivre,shopee,magazineluiza
MAX_EXECUTION_TIME_MIN=30
```

---

## 📦 OUTPUT DIRECTORY

**Location**: `user_research/` (inside `pesquisa_agent/`)

**Structure**:
```
user_research/
├── [produto]_research_notes.md      # 22-block report (human-readable)
├── [produto]_research_notes.llm.json # LLM-structured JSON
├── [produto]_metadata.json          # Quality scores, duration
└── [produto]_queries.json           # All web searches logged
```

**Create if missing**:
```bash
mkdir -p user_research
```

---

## ✅ VALIDATION & TESTING

### Quick Test

**Minimum Brief**:
```
Product: Mochila para notebook
Category: Mochilas e Bolsas
Target Audience: Estudantes e profissionais
Price: R$ 100-180
```

**Expected Output**:
- File: `user_research/mochila_notebook_research_notes.md`
- All 22 blocks present
- ≥3 competitors analyzed
- ≥15 queries logged

### Validation Commands

```bash
# Check output exists
ls user_research/*.md

# Count blocks (expect 22)
grep "^## \[" user_research/*_research_notes.md | wc -l

# Check quality metadata
cat user_research/*_metadata.json
```

---

## 🐛 TROUBLESHOOTING

### "web_search not available"

| Platform | Solution |
|----------|----------|
| Claude Code | Use `WebSearch` tool (built-in) |
| OpenAI | Enable "Web Browsing" in Assistant |
| Gemini | Enable "Google Search" grounding |
| Local LLMs | Provide URLs from `config/accessible_urls.md` |

### "Low quality score (<0.75)"

1. Re-run with more detailed brief
2. Add known competitors to brief
3. Extend search to more marketplaces

### "Too many [SUGESTÃO] placeholders (>10%)"

1. Add more context (attributes, images, competitors)
2. Accept if <30% (niche products are data-scarce)
3. Supplement with manual research

### "Output not saved"

1. Check `user_research/` folder exists
2. Verify write permissions
3. In cloud LLMs, copy-paste output manually

---

## 📊 PLATFORM COMPARISON

| Feature | Claude Code | OpenAI API | Custom GPT | Gemini | Local LLM |
|---------|-------------|------------|------------|--------|-----------|
| web_search | ✅ WebSearch | ✅ Browsing | ✅ Browsing | ✅ Grounding | ❌ Manual |
| vision | ✅ Read | ✅ Native | ✅ Native | ✅ Native | ⚠️ Vision models |
| file_search | ✅ Grep/Glob | ✅ Vector Store | ✅ Knowledge | ⚠️ Uploaded | ❌ Manual |
| code_interpreter | ⚠️ Bash/Jupyter | ✅ Native | ✅ Native | ❌ No | ❌ No |
| Auto-capability | ✅ Yes | ✅ Yes | ⚠️ Partial | ⚠️ Partial | ❌ No |
| **Recommended** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐ | ⭐ |

**Legend**: ✅ Full support | ⚠️ Partial | ❌ Not supported

---

## 🎯 RECOMMENDED SETUP

**Best Experience**:
1. **Claude Code** with `/prime-pesquisa` slash command
2. All tools auto-detected, no manual config needed

**Alternative**:
1. **OpenAI Assistants API** with Vector Store
2. Upload `iso_vectorstore/` for full knowledge base

---

## 📚 ADDITIONAL RESOURCES

**Documentation**:
- [PRIME.md](PRIME.md) - Complete agent instructions + tools mapping
- [README.md](README.md) - Overview + structure (~80 files)
- [config/accessible_urls.md](config/accessible_urls.md) - 1380+ tested URLs

**Knowledge Base** (for external LLMs):
- `iso_vectorstore/` - 20 files optimized for vector stores

**Competitive Intelligence**:
- `competitor_intelligence/` - 40+ tracked sources with automation

---

**Version**: 2.6.0
**Last Updated**: 2025-11-26
**Maintainer**: CODEXA Team
**Platforms Tested**: Claude Code ✅ | OpenAI Assistants ✅ | Custom GPT ✅ | Gemini ✅ | Ollama ⚠️

---

> 🚀 **Ready to deploy** - Follow platform-specific instructions above
> 💡 **Pro Tip**: Claude Code users just need `/prime-pesquisa` - everything else is auto-detected
> ✅ **Verified**: ~80 files, 22-block output, 1380+ URLs, 40+ competitor sources
