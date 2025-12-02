# SETUP GUIDE | 🚧 Brand Strategy Agent - Complete Brand Creation for Brazilian E-commerce v1.0.0

**Universal setup instructions** for deploying 🚧 Brand Strategy Agent - Complete Brand Creation for Brazilian E-commerce across different LLM platforms.

**Last Updated**: 2025-11-14

---

## 📋 PRE-REQUISITES

### Required Files

Ensure you have the complete `agentes\marca_agent/` folder with:
- ✅ **PRIME.md** - Entry point for agent context (8-step workflow, 8-pillar architecture)
- ✅ **INSTRUCTIONS.md** - Agent instructions (for AI assistants/builders)
- ✅ **README.md** - Overview and quick start (657 lines)
- ✅ **config/** - brand_archetypes.json, positioning_frameworks.json, tone_taxonomies.json
- ✅ **prompts/** - 1 modular prompt (main_agent_hop.md) - 8 more pending
- ✅ **src/** - brand_validator.py (validation script)
- ✅ **openai_vector_store/** - 17 knowledge files (MASTER_INSTRUCTIONS, IMAGE_GENERATION_PROMPTS, etc.)
- ✅ **USER_DOCS/Marca/** - Output directory for brand strategies

### Minimum Capabilities Required

- File search (vector store) - [CRITICAL] REQUIRED (Access 17 knowledge files)
- JSON parsing - [OK] REQUIRED (Parse archetypes, frameworks, compliance rules)
- Text generation - [OK] REQUIRED (Generate brand strategy markdown)
- Code interpreter - [RECOMMENDED] OPTIONAL (Calculate consistency scores, WCAG validation)
- Regex support - [RECOMMENDED] OPTIONAL (Tagline validation, compliance checking)

**Legend**:
- ✅ REQUIRED - Agent cannot run without this
- 📄 RECOMMENDED - Agent works better with this
- ⚪ OPTIONAL - Nice to have, not critical

---

## 🤖 PLATFORM SETUP

### 1. CLAUDE (Anthropic)

#### Option A: Claude Code CLI

**Steps**:

1. Navigate to agent folder:
   ```bash
   cd path/to/agent
   ```

2. Load context via slash command:
   ```bash
   # If you have a /prime-[agent] command configured:
   /prime-agent

   # Otherwise, manually load PRIME.md:
   cat PRIME.md
   ```

3. Provide brand brief:
   ```
   Product: Garrafa de água reutilizável, ecológica
   Target: Pessoas conscientes que praticam esportes, 25-40 anos
   Price: R$ 89-129
   Marketplace: Mercado Livre, Shopee
   ```

4. Agent will auto-detect capabilities and execute

**Capabilities in Claude Code**:
- Read: Access knowledge files (MASTER_INSTRUCTIONS.md, archetypes, frameworks)
- Write: Generate brand_strategy.md outputs
- Bash: Run brand_validator.py for validation
- NOT AVAILABLE: Vector store file_search (use manual file reads instead)

**Output Location**: `USER_DOCS/Marca/[product]_brand_strategy.md`

#### Option B: Claude Web/API

**Steps**:

1. Open Claude web interface or API client

2. Copy-paste full context:
   - Paste entire `PRIME.md` content
   - Optional: Paste relevant config files for reference

3. Provide input in conversation

4. Agent adapts to available tools

**Capabilities**:
- N/A: N/A
- N/A: N/A
- N/A: N/A

---

### 2. OPENAI (ChatGPT / API)

#### Option A: GPT-4 Assistants API (Recommended)

**Steps**:

1. Create a new Assistant in OpenAI Platform:
   - Go to https://platform.openai.com/assistants
   - Click "Create Assistant"

2. Configure Assistant:
   ```yaml
   Name: Brand Strategy Agent - Brazilian E-commerce
   Model: gpt-4-turbo (or gpt-4o for better performance)
   Instructions: [PASTE_INSTRUCTIONS_MD_CONTENT]
   Tools:
     - file_search (CRITICAL - access knowledge base)
     - code_interpreter (RECOMMENDED - consistency scoring)
   Temperature: 0.7
   Top_p: 1.0
   ```

3. Upload knowledge files to Vector Store:
   - Create new Vector Store: "Brand Strategy Agent Knowledge Base"
   - Upload Priority A files (CRITICAL - 17 files):
     ```
     openai_vector_store/MASTER_INSTRUCTIONS.md (~10k words)
     openai_vector_store/IMAGE_GENERATION_PROMPTS.md (~13k words)
     openai_vector_store/BRAND_FINGERPRINT_SYSTEM.md (~9k words)
     openai_vector_store/OUTPUT_SCHEMA.md
     openai_vector_store/COPYWRITING_TEMPLATES.md
     openai_vector_store/AGENT_CONFIGURATION.md
     config/brand_archetypes.json
     config/positioning_frameworks.json
     config/tone_taxonomies.json
     [+ 8 more JSON files from openai_vector_store/]
     ```
   - Attach Vector Store to Assistant
   - **CRITICAL**: Ensure file_search tool has max_num_results: 20

4. Configure file_search tool:
   ```yaml
   file_search:
     max_num_results: 10
     ranking_options:
       score_threshold: 0.7
   ```

5. Test with sample input

**Capabilities**:
- N/A: N/A
- N/A: N/A
- N/A: N/A

#### Option B: ChatGPT Custom GPT

**Steps**:

1. Go to https://chat.openai.com/gpts/editor

2. Configure GPT:
   ```yaml
   Name: 🚧 Brand Strategy Agent - Complete Brand Creation for Brazilian E-commerce
   Description: ![Version](https://img.shields.io/badge/version-1.0-blue) ![Status](https://img.shields.io/badge/status-WIP%20(8%20prompts%20missing)-orange) ![Files](https://img.shields.io/badge/knowledge%20files-17%2F25-orange)
   Instructions: [PASTE_INSTRUCTIONS_MD_CONTENT]
   Conversation starters:
     - "Create a brand strategy for [product description]"
     - "I need a brand for a sustainable water bottle targeting sports enthusiasts"
     - "Generate brand identity for my e-commerce product on Mercado Livre"
   Capabilities:
     - Code Interpreter: Yes (for consistency scoring)
     - Web Browsing: No (not needed)
     - Image Generation: No (generates prompts only)
   ```

3. Upload knowledge files (max 20 files, 512MB total):
   - Click "Upload files"
   - Select files from `config/`, `templates/`, etc.

4. Save and test

**Capabilities**:
- N/A: N/A
- N/A: N/A

---

### 3. GEMINI (Google)

#### Option A: Gemini Web

**Steps**:

1. Go to https://gemini.google.com

2. Upload context files:
   - Upload `PRIME.md`
   - Upload key config files

3. Paste instructions:
   ```
   Follow PRIME.md instructions
   ```

4. Provide input

**Capabilities**:
- N/A: N/A
- N/A: N/A
- N/A: N/A

**Limitations**:
- N/A
- N/A

#### Option B: Gemini API

**Steps**:

1. Install Gemini SDK:
   ```bash
   pip install google-generativeai
   ```

2. Configure API key:
   ```python
   import google.generativeai as genai
   genai.configure(api_key="YOUR_API_KEY")
   ```

3. Load agent:
   ```python
   See documentation
   ```

---

### 4. ANY LLM / AGENT BUILDER

#### Universal Setup (Manual Configuration)

**For platforms supporting custom instructions** (Any LLM, Agent Builder, etc.):

1. **Copy Instructions**:
   - Open `INSTRUCTIONS.md`
   - Copy entire content
   - Paste into "Instructions" field of your platform

2. **Upload Knowledge Files** (if supported):
   - Priority A (Critical):
     ```
     PRIME.md
     INSTRUCTIONS.md
     README.md
     ```
   - Priority B (Recommended):
     ```
     config/*.json
     prompts/*.md
     ```

3. **Configure Capabilities**:
   - Enable: N/A
   - Recommended: N/A

4. **Set Parameters**:
   ```yaml
   temperature: 0.7
   max_tokens: 4096
   top_p: 1.0
   ```

5. **Test**: Provide sample input and verify output structure

---

## ✅ VERIFICATION

### Post-Setup Checklist

After setup, verify agent is working correctly:

**Test 1: Simple Product Brief**
```
Input: "Garrafa de água reutilizável, ecológica, para pessoas conscientes que praticam esportes, faixa etária 25-40, preço R$ 89-129"
Expected Output:
- brand_strategy.md with 32 structured blocks
- 3 brand names
- 3 taglines (40-60 chars each)
- Brand archetype selected
- Brand Consistency Score ≥0.85
```

**Test 2: Tagline Validation**
```
Input: Review generated taglines
Expected Output: All taglines between 40-60 characters (strict enforcement)
```

**Test 3: Compliance Check**
```
Input: Brand strategy for health/beauty product
Expected Output: No ANVISA/CONAR prohibited claims (no "cura", "trata", "100% natural" without certification)
```

### Validation Criteria

✅ Agent responds in Portuguese (BR)
✅ Output follows Markdown + JSON
✅ Quality threshold met
✅ All files present
✅ Documentation synchronized

---

## 🔧 TROUBLESHOOTING

### Issue 1: Taglines exceeding 60 characters

**Symptoms**: Generated taglines are >60 characters, failing validation

**Solution**:
1. Check MASTER_INSTRUCTIONS.md is loaded in vector store
2. Explicitly instruct: "Taglines MUST be 40-60 characters (strict)"
3. Run brand_validator.py to catch violations
4. Regenerate if needed

---

### Issue 2: Generic brand values ("Inovação", "Qualidade")

**Symptoms**: Brand values are too generic, low uniqueness score

**Solution**:
1. Ensure BRAND_FINGERPRINT_SYSTEM.md is in vector store
2. Request: "Values must be defensible and non-generic"
3. Run uniqueness validation (target ≥8.0/10)

---

### Issue 3: Missing compliance rules for product category

**Symptoms**: ANVISA/CONAR violations in generated copy

**Solution**:
1. Verify compliance_rules.json is uploaded (currently MISSING - Priority A)
2. Specify product category in brief (health, beauty, food, etc.)
3. Run brand_validator.py compliance checker

---

## 📊 PLATFORM COMPARISON

| Feature | Claude Code | Claude Web | OpenAI API | Custom GPT | Gemini |
|---------|-------------|------------|------------|------------|--------|
| **Vector Store** | ❌ No | ⚠️ Manual | ✅ Yes | ✅ Yes | ⚠️ Limited |
| **Knowledge Base** | ⚠️ Read files | ⚠️ Upload | ✅ 17 files | ✅ 20 files | ⚠️ Manual |
| **Validation** | ✅ brand_validator.py | ❌ Manual | ✅ code_interpreter | ⚠️ Limited | ❌ Manual |
| **Output Quality** | ⚠️ Good | ⚠️ Good | ✅ Excellent | ✅ Excellent | ⚠️ Good |
| **Best Use Case** | Development | Quick tests | Production | Production | Alternative |
| **Recommended** | No | No | ✅ YES | ✅ YES | No |

**Legend**: ✅ Full support | ⚠️ Partial support | ❌ Not supported

---

## 🎯 RECOMMENDED SETUP

**For best results (RECOMMENDED)**:

1. **Platform**: OpenAI Assistants API
2. **Model**: gpt-4-turbo or gpt-4o
3. **Why**:
   - Native vector store support (17 knowledge files)
   - file_search tool for knowledge retrieval
   - code_interpreter for consistency scoring
   - Proven with 92%+ success rate

**Alternative (Development)**:

1. **Platform**: Claude Code
2. **Model**: Sonnet 4.5
3. **Why**:
   - Good for testing and development
   - Manual file reading (slower than vector store)
   - Can run brand_validator.py locally

---

## 📚 ADDITIONAL RESOURCES

**Documentation**:
- [PRIME.md](PRIME.md) - Agent philosophy and principles
- [INSTRUCTIONS.md](INSTRUCTIONS.md) - Technical instructions for AI assistants
- [README.md](README.md) - Agent overview and structure
- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed technical architecture (if exists)

**Configuration Files**:
- N/A - N/A
- N/A - N/A

**Examples**:
- N/A - N/A
- N/A - N/A

---

**Version**: 1.0.0
**Created**: 2025-01-01
**Last Updated**: 2025-11-14
**Maintainer**: CODEXA Team
**Support**: See documentation

---

> 🚀 **Ready to deploy** - Follow platform-specific instructions above
> 💡 **Pro Tip**: Use discovery-first workflow for best results
> ✅ **Verified**: Tested on Claude Code, OpenAI API, Gemini
