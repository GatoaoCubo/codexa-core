# SETUP - Universal Installation Guide | Anuncio Agent

**Purpose**: Platform-agnostic setup for Claude Code, OpenAI, Gemini, and Local LLMs
**Time**: 5-15 minutes | **Difficulty**: Beginner-friendly

---

## 🎯 OVERVIEW

Anuncio Agent works on **any LLM platform** through auto-discovery of available capabilities. This guide covers setup for:

1. **Claude Code** (Recommended - full capabilities)
2. **OpenAI Assistants** (via Vector Store)
3. **Google Gemini** (via Google AI Studio)
4. **Local LLMs** (Ollama, LM Studio - limited)

---

## 1. PREREQUISITES

### Required
- **Python 3.10+** (for local execution)
- **API Keys** (platform-specific, auto-detected)
- **Research Notes** (from `pesquisa_agent` or manual creation)

### Optional
- **UV** package manager (faster, recommended)
- **Git** (for version control)

---

## 2. INSTALLATION

### 2.1 Via pip (Standard)

```bash
cd anuncio_agent
pip install -r requirements.txt
```

### 2.2 Via uv (Recommended - Faster)

```bash
cd anuncio_agent
uv pip install -r requirements.txt
```

### 2.3 Verify Installation

```bash
python codex_anuncio.py --version
# Expected: CodeXAnuncio v1.2.0
```

---

## 3. CONFIGURATION

### 3.1 Auto-Discovery Mode (Default - Recommended)

**No configuration needed!** Agent automatically detects:
- Available LLM capabilities (web_search, vision, code_interpreter)
- Marketplace specs from `config/marketplace_specs.json`
- Compliance rules from `config/copy_rules.json`

Run directly:
```bash
python codex_anuncio.py generate sample_data/research_notes_example.md
```

### 3.2 Manual .env Configuration (Optional)

Create `.env` file:
```bash
# LLM Provider (auto-detected if not set)
ANTHROPIC_API_KEY=your_claude_key_here
OPENAI_API_KEY=your_openai_key_here
GOOGLE_API_KEY=your_gemini_key_here

# Marketplace (default: mercadolivre)
DEFAULT_MARKETPLACE=mercadolivre

# Output Directory (default: user_anuncios/)
OUTPUT_DIR=user_anuncios/
```

---

## 4. PLATFORM-SPECIFIC SETUP

### 4.1 Claude Code (Recommended - Full Features)

**Why Claude Code?**
- ✅ Native file system access
- ✅ Best compliance validation
- ✅ Fastest execution (2-3 min)
- ✅ Full auto-discovery support

**Setup Steps:**
1. Copy `anuncio_agent/` folder to Claude Code workspace
2. Load context:
   ```bash
   /prime-anuncio
   ```
3. Generate ad:
   ```bash
   /anuncio "research_notes.md" "mercadolivre"
   ```

**Expected Output:**
- `user_anuncios/anuncio_[timestamp].md`
- `user_anuncios/anuncio_[timestamp].llm.json`
- `user_anuncios/anuncio_[timestamp].meta.json`

---

### 4.2 OpenAI Assistants (Vector Store)

**Use Case**: Standalone deployment, API-driven workflows

**Step 1: Prepare Files (5 min)**

Option A - Automated (Windows):
```powershell
.\prepare_for_openai.ps1
```

Option B - Manual:
```bash
mkdir openai_vector_store
cp prompts/* openai_vector_store/
cp config/* openai_vector_store/
cp README.md ARCHITECTURE.md openai_vector_store/
```

**Step 2: Create Assistant (5 min)**

1. Access: https://platform.openai.com/playground/assistants
2. Click "Create Assistant"
3. Configure:
   - **Name**: `CodeXAnuncio - Gerador de Anúncios`
   - **Model**: `gpt-4o` or `gpt-4-turbo-preview`
   - **Temperature**: `0.7`
4. **Instructions**: Copy content from `prompts/10_main_agent_hop.md`
5. **Tools**: Enable
   - ✅ File Search (mandatory)
   - ✅ Code Interpreter (recommended)

**Step 3: Configure Vector Store (5 min)**

1. In Tools section, click "Add Vector Store"
2. Create new: `CodeXAnuncio-Knowledge-Base`
3. Upload ALL files from `openai_vector_store/`:
   - **Prompts**: 10 files (10_main_agent_hop.md through 90_qa_validation.md)
   - **Configs**: 3 files (copy_rules.json, persuasion_patterns.json, marketplace_specs.json)
   - **Docs**: 4 files (README.md, ARCHITECTURE.md, PRIME.md, SETUP.md)
4. Wait for indexing (1-3 min)
5. Save Assistant

**Step 4: Test**

Prompt:
```
Generate complete ad for:
Product: Cat Window Bed with Reinforced Suction Cups
Marketplace: mercadolivre
Execute all 7 phases.
```

Expected: 3 titles (58-60 chars), 2 keyword blocks, description ≥3,300 chars

---

### 4.3 Google Gemini (Experimental)

**Use Case**: Google ecosystem, multimodal analysis

**Step 1: Google AI Studio Setup**

1. Access: https://aistudio.google.com/
2. Create new prompt
3. Upload knowledge files:
   - `prompts/10_main_agent_hop.md` (system prompt)
   - `config/copy_rules.json` (compliance)
   - `config/marketplace_specs.json` (specs)

**Step 2: Configure Function Calling**

```json
{
  "name": "generate_anuncio",
  "description": "Generate complete marketplace ad",
  "parameters": {
    "type": "object",
    "properties": {
      "research_notes": {"type": "string"},
      "marketplace": {"type": "string", "enum": ["mercadolivre", "shopee", "magalu", "amazon"]}
    },
    "required": ["research_notes", "marketplace"]
  }
}
```

**Step 3: Test Execution**

Input research notes as context, invoke function.

**Limitations**:
- ⚠️ No native file system access (paste research manually)
- ⚠️ Output validation less robust
- ⚠️ Slower (4-6 min vs 2-3 min Claude)

---

### 4.4 Local LLMs (Ollama, LM Studio)

**Use Case**: Privacy-first, offline, no API costs

**Minimum Requirements:**
- **Model**: Llama 3.1 70B+ or Mixtral 8x22B+
- **RAM**: 48GB+ (for 70B Q4 quantization)
- **GPU**: 24GB VRAM recommended (RTX 4090, A6000)

**Setup via Ollama:**

```bash
# Install model
ollama pull llama3.1:70b

# Set environment
export OLLAMA_HOST=http://localhost:11434

# Run agent
python codex_anuncio.py generate research_notes.md --local
```

**Prompt Adaptation:**

Local LLMs require simplified prompts (reduce from 1000+ lines to 200-300 lines):
- Use `prompts/10_main_agent_hop.md` summary section only
- Remove advanced persuasion patterns
- Focus on compliance validation

**Limitations**:
- ⚠️ Slower (10-15 min vs 2-3 min)
- ⚠️ Lower persuasion quality (score 0.65-0.75 vs 0.80-0.90)
- ⚠️ Requires prompt engineering expertise
- ✅ Zero API costs
- ✅ Full privacy/offline

---

## 5. AUTO-DISCOVERY CAPABILITIES

**How It Works:**

Agent detects capabilities on first run:

```python
# Automatic detection
capabilities = {
    'web_search': False,      # Real-time competitor research
    'vision': False,          # Image analysis
    'code_interpreter': True, # JSON validation (recommended)
    'file_search': True       # Knowledge base access
}
```

**Adaptation Logic:**

| Capability | If Available | If Not Available |
|-----------|--------------|------------------|
| `web_search` | Augment research with real-time data | Use provided research only (standard) |
| `vision` | Analyze competitor images | Skip visual analysis |
| `code_interpreter` | Programmatic validation | Text-based validation |
| `file_search` | Auto-load configs/prompts | Manual config required |

**Fallback Strategy:**

All critical features work **without** external capabilities. Auto-discovery only enhances quality, never blocks execution.

---

## 6. TESTING INSTALLATION

### Test 1: Version Check
```bash
python codex_anuncio.py --version
# Expected: v1.2.0
```

### Test 2: Generate Sample Ad
```bash
python codex_anuncio.py generate sample_data/research_notes_example.md
```

**Expected Output:**
- File: `user_anuncios/anuncio_[timestamp].md`
- Validation: AUDITORIA_QA shows "PASS (100%)"
- Time: <3 minutes

### Test 3: Validate Compliance
```bash
python codex_anuncio.py validate user_anuncios/anuncio_[timestamp].md
```

**Expected:**
- ✅ 3 titles (58-60 chars)
- ✅ 2 keyword blocks (115-120 terms each)
- ✅ Description ≥3,300 chars
- ✅ No HTML, emojis, prohibited claims
- ✅ Compliance: 100%

---

## 7. TROUBLESHOOTING

### Issue: "Research notes invalid"
**Cause**: File not found or wrong format
**Solution**: Verify path, use absolute path if needed

### Issue: Titles not 58-60 characters
**Cause**: LLM not following strict constraint
**Solution**: Add explicit validation in prompt:
```
CRITICAL: Titles MUST be EXACTLY 58-60 characters. Count before confirming.
```

### Issue: Description too short (<3,300 chars)
**Cause**: Prompt truncation or LLM shortcuts
**Solution**: Force validation:
```
After generating, COUNT characters. If <3,300, expand until minimum reached.
```

### Issue: Compliance violations (emojis, HTML)
**Cause**: LLM not consulting copy_rules.json
**Solution**: Explicitly reference:
```
Before finalizing, consult config/copy_rules.json and validate ALL rules.
```

### Issue: Slow execution (>5 min)
**Cause**: Network latency, large context
**Solution**:
- Use `gpt-4o` instead of `gpt-4-turbo-preview` (faster)
- Reduce temperature to 0.6 (less creative, faster)
- Clear LLM cache between runs

---

## 8. NEXT STEPS

### New User Path
1. ✅ Complete setup (this guide)
2. 📖 Read [README.md](README.md) for overview
3. 🚀 Generate first ad (3 min)
4. 📊 Review [ARCHITECTURE.md](ARCHITECTURE.md) for technical details

### Production Path
1. 📈 Scale to 10-50 products (batch generation)
2. 🧪 Implement A/B testing (3 variations)
3. 🔄 Configure learning loop (monthly iteration)
4. 📊 Track ROI metrics (conversion, time saved)

---

## 9. PLATFORM COMPARISON

| Feature | Claude Code | OpenAI | Gemini | Local LLMs |
|---------|-------------|--------|--------|------------|
| **Execution Time** | 2-3 min | 3-4 min | 4-6 min | 10-15 min |
| **Persuasion Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Compliance Validation** | ✅ Excellent | ✅ Good | ⚠️ Fair | ⚠️ Basic |
| **Auto-Discovery** | ✅ Full | ✅ Partial | ⚠️ Limited | ❌ None |
| **Cost** | API usage | API usage | API usage | Free (hardware) |
| **Privacy** | API-dependent | API-dependent | API-dependent | ✅ Fully offline |
| **Setup Complexity** | ⭐ Easy | ⭐⭐ Medium | ⭐⭐⭐ Hard | ⭐⭐⭐⭐ Expert |

**Recommendation**: Start with **Claude Code** for best results, fall back to **OpenAI** for API-driven workflows, use **Local LLMs** only for privacy-critical scenarios.

---

**Version**: 1.2.1
**Last Updated**: 2025-11-14
**Consolidated From**: QUICK_START.md, INSTALLATION_CHECKLIST.md, OPENAI_DEPLOYMENT_GUIDE.md
**Status**: Production-Ready
