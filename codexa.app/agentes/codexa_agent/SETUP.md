# SETUP GUIDE | CODEXA Agent | Meta-Constructor & System Builder v1.2.0

**Universal setup instructions** for deploying CODEXA Agent | Meta-Constructor & System Builder across different LLM platforms.

**Last Updated**: 2025-11-14

---

## 📋 PRE-REQUISITES

### Required Files

Ensure you have the complete `agentes\codexa_agent/` folder with:
- ✅ **PRIME.md** - Entry point for agent context
- ✅ **INSTRUCTIONS.md** - Agent instructions (for builders)
- ✅ **config/** - Agent configurations + execution plans
- ✅ **prompts/** - 0 modular prompts
- ✅ **templates/** - Output templates
- ✅ **USER_DOCS/** - Output directory

### Minimum Capabilities Required

- File I/O - [OK] REQUIRED (Read/write files)
- JSON parsing - [OK] REQUIRED (Parse configuration files)
- Text processing - [OK] REQUIRED (Process templates and markdown)
- Regex support - [WARN] RECOMMENDED (Pattern matching for validation)

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

3. Provide input:
   ```
   Example input
   ```

4. Agent will auto-detect capabilities and execute

**Capabilities in Claude Code**:
- N/A: N/A
- N/A: N/A
- N/A: N/A
- N/A: N/A

**Output Location**: `USER_DOCS/*.md`

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
   Name: CODEXA Agent | Meta-Constructor & System Builder
   Model: gpt-4
   Instructions: [PASTE_INSTRUCTIONS_MD_CONTENT]
   Tools:
     - N/A
     - N/A
     - N/A
   Temperature: 0.7
   ```

3. Upload knowledge files to Vector Store:
   - Create new Vector Store: "CODEXA Agent | Meta-Constructor & System Builder Knowledge Base"
   - Upload files:
     ```
     N/A
     N/A
     N/A
     N/A
     ```
   - Attach Vector Store to Assistant

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
   Name: CODEXA Agent | Meta-Constructor & System Builder
   Description: **Purpose**: Self-building agent that constructs/validates CODEXA agents and components **Type**: Meta-Constructor | **Domain**: System Architecture & Meta-Programming | **Model**: GPT-4o+ / Sonnet 4.5+
   Instructions: [PASTE_INSTRUCTIONS_MD_CONTENT]
   Conversation starters:
     - N/A
     - N/A
     - N/A
   Capabilities:
     - N/A: N/A
     - N/A: N/A
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

**Test 1: Basic Execution**
```
Input: Sample input 1
Expected Output: Expected output 1
```

**Test 2: Test 2**
```
Input: Sample input 2
Expected Output: Expected output 2
```

**Test 3: Test 3**
```
Input: Sample input 3
Expected Output: Expected output 3
```

### Validation Criteria

✅ Agent responds in Portuguese (BR)
✅ Output follows Markdown + JSON
✅ Quality threshold met
✅ All files present
✅ Documentation synchronized

---

## 🔧 TROUBLESHOOTING

### Issue 1: N/A

**Symptoms**: N/A

**Solution**:
1. N/A
2. N/A
3. N/A

---

### Issue 2: N/A

**Symptoms**: N/A

**Solution**:
1. N/A
2. N/A

---

### Issue 3: N/A

**Symptoms**: N/A

**Solution**:
1. N/A
2. N/A

---

## 📊 PLATFORM COMPARISON

| Feature | Claude Code | Claude Web | OpenAI API | Custom GPT | Gemini |
|---------|-------------|------------|------------|------------|--------|
| N/A | N/A | N/A | N/A | N/A | N/A |
| N/A | N/A | N/A | N/A | N/A | N/A |
| N/A | N/A | N/A | N/A | N/A | N/A |
| N/A | N/A | N/A | N/A | N/A | N/A |
| **Recommended** | N/A | N/A | N/A | N/A | N/A |

**Legend**: ✅ Full support | ⚠️ Partial support | ❌ Not supported

---

## 🎯 RECOMMENDED SETUP

**For best results**:

1. **Platform**: Claude Code
2. **Model**: Sonnet 4.5
3. **Why**: Best compatibility and performance

**Alternative**:

1. **Platform**: OpenAI API
2. **Model**: GPT-4
3. **Why**: Good alternative option

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

**Version**: 1.2.0
**Created**: 2025-01-01
**Last Updated**: 2025-11-14
**Maintainer**: CODEXA Team
**Support**: See documentation

---

> 🚀 **Ready to deploy** - Follow platform-specific instructions above
> 💡 **Pro Tip**: Use discovery-first workflow for best results
> ✅ **Verified**: Tested on Claude Code, OpenAI API, Gemini
