# SETUP GUIDE | Pesquisa Agent v3.0.0

**Universal setup instructions** for loading the Pesquisa Agent into different LLM platforms.

---

## 📋 PRE-REQUISITES

### Required Files
Ensure you have the complete `pesquisa_agent/` folder with:
- ✅ **PRIME.md** - Entry point
- ✅ **config/** - Agent configs + marketplaces + execution plans
- ✅ **prompts/** - 7 modular prompts
- ✅ **templates/** - research_notes.md template
- ✅ **user_research/** - Output directory

### Minimum Capabilities Required
- ✅ **web_search** - REQUIRED (cannot run without it)
- 📄 **vision** - Optional (enables screenshot analysis)
- 📄 **file_search** - Optional (enables compliance rules lookup)
- 📄 **code_interpreter** - Optional (enables advanced metrics)

---

## 🤖 PLATFORM SETUP

### 1. CLAUDE (Anthropic)

#### Option A: Claude Code CLI

**Steps**:
1. Navigate to agent folder:
   ```bash
   cd path/to/pesquisa_agent/
   ```

2. Load PRIME context:
   ```bash
   # If you have a /prime-pesquisa command configured:
   /prime-pesquisa

   # Otherwise, manually load:
   cat PRIME.md
   ```

3. Provide a product brief:
   ```
   Execute market research for:

   Product: Fone de ouvido Bluetooth esportivo
   Category: Eletrônicos > Áudio
   Target Audience: Atletas, 18-35 anos
   Price Range: R$ 150 - R$ 280
   Marketplace: Mercado Livre
   ```

4. Agent will auto-detect capabilities and execute research

**Capabilities in Claude Code**:
- ✅ web_search (via WebFetch tool)
- ✅ vision (via Read tool for images)
- ❌ file_search (not available - will use web-only)
- ❌ code_interpreter (not available - manual metrics)

**Output Location**: `user_research/[produto]_research_notes.md`

#### Option B: Claude Web/API

**Steps**:
1. Open Claude web interface or API client

2. Copy-paste full context:
   - Paste entire `PRIME.md` content
   - Optional: Paste `config/marketplaces.json` for marketplace reference

3. Provide product brief in conversation

4. Agent adapts to available tools

**Capabilities**:
- ✅ web_search (if enabled in Claude web)
- ✅ vision (native Claude feature)
- ❌ file_search (not available)
- ❌ code_interpreter (not available)

---

### 2. OPENAI (ChatGPT / API)

#### Option A: GPT-4 Assistants API (Recommended)

**Steps**:
1. Create a new Assistant in OpenAI Platform:
   - Go to https://platform.openai.com/assistants
   - Click "Create Assistant"

2. Configure Assistant:
   ```yaml
   Name: Pesquisa Agent BR
   Model: gpt-4-turbo-preview or gpt-4o
   Description: Brazilian e-commerce market research specialist
   ```

3. Set Instructions:
   - Copy entire `PRIME.md` content
   - Paste into "Instructions" field

4. Enable Tools:
   - ✅ **Web Browsing** (web_search)
   - ✅ **Vision** (for screenshot analysis)
   - ✅ **Code Interpreter** (for metrics)
   - ❌ **File Search** - Create Vector Store (optional, see below)

5. Create Vector Store (Optional - for compliance rules):
   - Go to "Storage" → "Create Vector Store"
   - Name: "Pesquisa Knowledge Base"
   - Upload files:
     - `config/agent.json`
     - `config/marketplaces.json`
     - Any internal compliance docs (ANVISA, INMETRO rules)
   - Attach to Assistant

6. Test:
   ```
   Execute market research for: Garrafa de água reutilizável, R$ 89-129
   ```

**Capabilities**:
- ✅ web_search (Web Browsing tool)
- ✅ vision (native GPT-4 Vision)
- ✅ file_search (if Vector Store created)
- ✅ code_interpreter (native)

#### Option B: ChatGPT Web Interface

**Steps**:
1. Open ChatGPT (Plus/Pro account for web browsing)

2. Create Custom GPT:
   - Click profile → "My GPTs" → "Create a GPT"
   - Name: "Pesquisa Agent BR"
   - Description: "Brazilian market research for e-commerce"

3. Configure:
   - **Instructions**: Paste `PRIME.md` content
   - **Capabilities**:
     - ✅ Enable "Web Browsing"
     - ✅ Enable "DALL-E" (not used, but keeps vision)
     - ❌ Enable "Code Interpreter" (optional)
   - **Knowledge Files**:
     - Upload `config/agent.json`
     - Upload `config/marketplaces.json`

4. Test GPT:
   ```
   Research: Tênis de corrida masculino, R$ 200-400, Mercado Livre
   ```

**Capabilities**:
- ✅ web_search (Web Browsing)
- ✅ vision (native)
- ✅ file_search (Knowledge Files)
- ✅ code_interpreter (optional)

---

### 3. GOOGLE GEMINI

#### Option A: Google AI Studio

**Steps**:
1. Go to https://aistudio.google.com/

2. Create New Prompt:
   - Click "Create new prompt"
   - Select "Freeform prompt"

3. System Instructions:
   - Copy entire `PRIME.md` content
   - Paste in "System instructions" section

4. Grounding (Optional):
   - Enable "Google Search" grounding
   - This provides web_search capability

5. Upload Context Files:
   - Click "Add file"
   - Upload `config/marketplaces.json`
   - Upload `templates/research_notes.md`

6. Test:
   ```
   Execute research for: Mouse gamer RGB, R$ 80-150, gamers 16-30 anos
   ```

**Capabilities**:
- ✅ web_search (via Google Search grounding)
- ✅ vision (native Gemini Vision)
- ⚠️ file_search (via uploaded files, limited)
- ❌ code_interpreter (not available)

#### Option B: Gemini API

**Steps**:
1. Set up API key: https://ai.google.dev/

2. Create application with system prompt:
   ```python
   import google.generativeai as genai

   genai.configure(api_key='YOUR_API_KEY')

   # Load PRIME.md as system instruction
   with open('PRIME.md', 'r', encoding='utf-8') as f:
       system_instruction = f.read()

   model = genai.GenerativeModel(
       model_name='gemini-1.5-pro',
       system_instruction=system_instruction,
       tools=['google_search_retrieval']  # Enable web search
   )

   # Execute research
   response = model.generate_content("""
   Execute research for:
   Product: Suplemento whey protein
   Category: Suplementos > Proteína
   Price: R$ 80-120
   Marketplace: Mercado Livre
   """)
   ```

**Capabilities**:
- ✅ web_search (google_search_retrieval tool)
- ✅ vision (native)
- ❌ file_search (manual context injection)
- ❌ code_interpreter (not available)

---

### 4. LOCAL LLMs (Ollama, LM Studio, etc.)

#### Requirements

**Minimum Model Capabilities**:
- Model size: ≥13B parameters (for quality research)
- Context window: ≥32k tokens (to hold PRIME.md + brief + research)
- Function calling: Recommended (for tool use)

**Recommended Models**:
- Llama 3.1 70B (via Ollama)
- Mixtral 8x22B
- Qwen 2.5 72B
- Command R+ 104B

#### Setup Steps

**Option A: Ollama**

1. Install Ollama: https://ollama.ai/

2. Pull model:
   ```bash
   ollama pull llama3.1:70b
   ```

3. Create Modelfile with system prompt:
   ```bash
   # Create Modelfile
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
   ```

4. Run:
   ```bash
   ollama run pesquisa-agent
   ```

5. Provide brief in conversation

**Capabilities**:
- ❌ web_search (not native - see workaround below)
- ✅ vision (if using vision model variant like llama3.2-vision)
- ❌ file_search (manual context injection)
- ❌ code_interpreter (not available)

**Web Search Workaround**:
- Use external tools: BraveSearch API, SerpAPI, or custom scrapers
- Manual search: User provides URLs or search results as text
- Agent prompts: "Since I don't have web_search, please provide URLs for: [query]"

**Option B: LM Studio**

1. Download LM Studio: https://lmstudio.ai/

2. Load model (Llama, Mixtral, Qwen)

3. Configure System Prompt:
   - Settings → "System Prompt"
   - Paste `PRIME.md` content

4. Optional: Enable OpenAI-compatible API:
   - Tools → "Local Server" → Start
   - Use API endpoint for automation

5. Chat normally

**Capabilities**:
- ❌ web_search (requires external integration)
- ⚠️ vision (if vision model loaded)
- ❌ file_search (manual injection)
- ❌ code_interpreter (not available)

---

## 🔧 CAPABILITIES CONFIGURATION

### Declaring Capabilities

**Method 1: Auto-Detection (All Platforms)**

Let the agent detect on first tool use:
```
Agent: "Attempting web search..."
[Success] → web_search = true
[Failure] → web_search = false, fallback to manual
```

**Method 2: User Declaration (First Run)**

Agent asks:
```
Agent: "To optimize the research workflow, which capabilities do you have?"
User: "web_search: yes, vision: yes, file_search: no"
Agent: "Got it! Adapting workflow: Full web research + screenshot analysis, no internal rules lookup."
```

**Method 3: Environment File (Advanced)**

Create `.env` in `pesquisa_agent/` folder:
```bash
# Pesquisa Agent Capabilities
WEB_SEARCH=true           # Required for execution
VISION=true               # Optional (screenshot analysis)
FILE_SEARCH=false         # Optional (compliance rules)
CODE_INTERPRETER=false    # Optional (advanced metrics)

# Brazilian Marketplaces Priority (1-9)
MARKETPLACE_PRIORITY=mercadolivre,shopee,magazineluiza,amazon_br

# Performance
MAX_EXECUTION_TIME_MIN=30
CONCURRENT_SEARCHES=3
```

Agent reads on startup (if platform supports file reading).

---

## 📦 OUTPUT DIRECTORY SETUP

**Default Location**: `user_research/` (inside `pesquisa_agent/` folder)

**Structure**:
```
user_research/
├── garrafa_agua_research_notes.md
├── garrafa_agua_metadata.json
├── garrafa_agua_queries.json
├── fone_bluetooth_research_notes.md
├── fone_bluetooth_metadata.json
└── fone_bluetooth_queries.json
```

**Create directory** (if not exists):
```bash
cd pesquisa_agent/
mkdir user_research
```

**Permissions**: Ensure write access for agent to save outputs.

---

## ✅ VALIDATION & TESTING

### Quick Test (Any Platform)

**Minimum Brief**:
```
Product: Mochila para notebook
Category: Mochilas e Bolsas
Target Audience: Estudantes e profissionais
Price: R$ 100-180
```

**Expected Output**:
- File created: `user_research/mochila_notebook_research_notes.md`
- All 22 blocks present
- ≥3 competitors analyzed
- ≥15 queries logged

**Validation**:
```bash
# Check output exists
ls user_research/*.md

# Count blocks (expect 22)
grep "^## \[" user_research/mochila_notebook_research_notes.md | wc -l

# Check metadata quality
cat user_research/mochila_notebook_metadata.json
```

---

## 🐛 TROUBLESHOOTING

### Issue: "web_search not available"

**Cause**: Platform doesn't have web search capability

**Solutions**:
1. **OpenAI**: Enable "Web Browsing" tool in Assistant
2. **Claude**: Use WebFetch tool (available in Claude Code)
3. **Gemini**: Enable "Google Search" grounding
4. **Local LLMs**: Provide manual URLs or integrate external API

### Issue: "Output file not created"

**Cause**: No write permissions or wrong directory

**Solutions**:
1. Check `user_research/` folder exists
2. Verify write permissions: `touch user_research/test.txt`
3. If in cloud LLM, agent may output inline instead of file (copy-paste manually)

### Issue: "Low quality score (<0.75)"

**Cause**: Insufficient web searches or data

**Solutions**:
1. Re-run with more detailed brief
2. Extend search to more marketplaces
3. Check if web_search is working properly

### Issue: "Too many [SUGESTÃO] placeholders (>10%)"

**Cause**: Niche product or limited public data

**Solutions**:
1. Add more context to brief (competitors, attributes, images)
2. Accept if <30% (some products inherently data-scarce)
3. Supplement with manual research

---

## 📚 NEXT STEPS

1. ✅ **Setup complete?** Test with quick brief (5 min test)
2. 📖 **Ready for full research?** Read `PRIME.md` workflow
3. 🎯 **Custom workflows?** Check `config/plans/` for templates
4. 🔗 **Integration?** See `/prime-anuncio` (ad agent), `/prime-marca` (brand agent)

---

**Version**: 3.0.0 | **Updated**: 2025-11-30
**Platforms Tested**: Claude Code ✅ | OpenAI Assistants ✅ | Gemini AI Studio ✅ | Ollama ⚠️
