# SETUP GUIDE | [AGENT_NAME] v[VERSION]

**Universal setup instructions** for deploying [AGENT_NAME] across different LLM platforms.

**Last Updated**: [LAST_UPDATED]

---

## 📋 PRE-REQUISITES

### Required Files

Ensure you have the complete `[AGENT_DIRECTORY]/` folder with:
- ✅ **PRIME.md** - Entry point for agent context
- ✅ **INSTRUCTIONS.md** - Agent instructions (for builders)
- ✅ **config/** - Agent configurations + execution plans
- ✅ **prompts/** - [PROMPT_COUNT] modular prompts
- ✅ **templates/** - Output templates
- ✅ **[OUTPUT_DIRECTORY]/** - Output directory

### Minimum Capabilities Required

- [REQUIRED_CAPABILITY_1] - [CAPABILITY_STATUS_1] ([CAPABILITY_DESCRIPTION_1])
- [REQUIRED_CAPABILITY_2] - [CAPABILITY_STATUS_2] ([CAPABILITY_DESCRIPTION_2])
- [REQUIRED_CAPABILITY_3] - [CAPABILITY_STATUS_3] ([CAPABILITY_DESCRIPTION_3])
- [REQUIRED_CAPABILITY_4] - [CAPABILITY_STATUS_4] ([CAPABILITY_DESCRIPTION_4])

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
   cd [ABSOLUTE_AGENT_PATH]
   ```

2. Load context via slash command:
   ```bash
   # If you have a /prime-[agent] command configured:
   /prime-[AGENT_SLUG]

   # Otherwise, manually load PRIME.md:
   cat PRIME.md
   ```

3. Provide input:
   ```
   [EXAMPLE_INPUT_PROMPT]
   ```

4. Agent will auto-detect capabilities and execute

**Capabilities in Claude Code**:
- [CLAUDE_CODE_CAPABILITY_1]: [CLAUDE_CODE_STATUS_1]
- [CLAUDE_CODE_CAPABILITY_2]: [CLAUDE_CODE_STATUS_2]
- [CLAUDE_CODE_CAPABILITY_3]: [CLAUDE_CODE_STATUS_3]
- [CLAUDE_CODE_CAPABILITY_4]: [CLAUDE_CODE_STATUS_4]

**Output Location**: `[OUTPUT_DIRECTORY]/[OUTPUT_FILE_PATTERN]`

#### Option B: Claude Web/API

**Steps**:

1. Open Claude web interface or API client

2. Copy-paste full context:
   - Paste entire `PRIME.md` content
   - Optional: Paste relevant config files for reference

3. Provide input in conversation

4. Agent adapts to available tools

**Capabilities**:
- [CLAUDE_WEB_CAPABILITY_1]: [CLAUDE_WEB_STATUS_1]
- [CLAUDE_WEB_CAPABILITY_2]: [CLAUDE_WEB_STATUS_2]
- [CLAUDE_WEB_CAPABILITY_3]: [CLAUDE_WEB_STATUS_3]

---

### 2. OPENAI (ChatGPT / API)

#### Option A: GPT-4 Assistants API (Recommended)

**Steps**:

1. Create a new Assistant in OpenAI Platform:
   - Go to https://platform.openai.com/assistants
   - Click "Create Assistant"

2. Configure Assistant:
   ```yaml
   Name: [AGENT_NAME]
   Model: [RECOMMENDED_OPENAI_MODEL]
   Instructions: [PASTE_INSTRUCTIONS_MD_CONTENT]
   Tools:
     - [OPENAI_TOOL_1]
     - [OPENAI_TOOL_2]
     - [OPENAI_TOOL_3]
   Temperature: [TEMPERATURE]
   ```

3. Upload knowledge files to Vector Store:
   - Create new Vector Store: "[AGENT_NAME] Knowledge Base"
   - Upload files:
     ```
     [KNOWLEDGE_FILE_1]
     [KNOWLEDGE_FILE_2]
     [KNOWLEDGE_FILE_3]
     [KNOWLEDGE_FILE_4]
     ```
   - Attach Vector Store to Assistant

4. Configure file_search tool:
   ```yaml
   file_search:
     max_num_results: [MAX_RESULTS]
     ranking_options:
       score_threshold: [SCORE_THRESHOLD]
   ```

5. Test with sample input

**Capabilities**:
- [OPENAI_CAPABILITY_1]: [OPENAI_STATUS_1]
- [OPENAI_CAPABILITY_2]: [OPENAI_STATUS_2]
- [OPENAI_CAPABILITY_3]: [OPENAI_STATUS_3]

#### Option B: ChatGPT Custom GPT

**Steps**:

1. Go to https://chat.openai.com/gpts/editor

2. Configure GPT:
   ```yaml
   Name: [AGENT_NAME]
   Description: [AGENT_DESCRIPTION]
   Instructions: [PASTE_INSTRUCTIONS_MD_CONTENT]
   Conversation starters:
     - [STARTER_1]
     - [STARTER_2]
     - [STARTER_3]
   Capabilities:
     - [GPT_CAPABILITY_1]: [GPT_CAPABILITY_STATUS_1]
     - [GPT_CAPABILITY_2]: [GPT_CAPABILITY_STATUS_2]
   ```

3. Upload knowledge files (max 20 files, 512MB total):
   - Click "Upload files"
   - Select files from `config/`, `templates/`, etc.

4. Save and test

**Capabilities**:
- [CUSTOM_GPT_CAPABILITY_1]: [CUSTOM_GPT_STATUS_1]
- [CUSTOM_GPT_CAPABILITY_2]: [CUSTOM_GPT_STATUS_2]

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
   [GEMINI_INSTRUCTIONS_PROMPT]
   ```

4. Provide input

**Capabilities**:
- [GEMINI_CAPABILITY_1]: [GEMINI_STATUS_1]
- [GEMINI_CAPABILITY_2]: [GEMINI_STATUS_2]
- [GEMINI_CAPABILITY_3]: [GEMINI_STATUS_3]

**Limitations**:
- [GEMINI_LIMITATION_1]
- [GEMINI_LIMITATION_2]

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
   [GEMINI_API_CODE_EXAMPLE]
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
     [PRIORITY_A_FILE_1]
     [PRIORITY_A_FILE_2]
     [PRIORITY_A_FILE_3]
     ```
   - Priority B (Recommended):
     ```
     [PRIORITY_B_FILE_1]
     [PRIORITY_B_FILE_2]
     ```

3. **Configure Capabilities**:
   - Enable: [REQUIRED_CAPABILITY_LIST]
   - Recommended: [OPTIONAL_CAPABILITY_LIST]

4. **Set Parameters**:
   ```yaml
   temperature: [TEMPERATURE]
   max_tokens: [MAX_TOKENS]
   top_p: [TOP_P]
   ```

5. **Test**: Provide sample input and verify output structure

---

## ✅ VERIFICATION

### Post-Setup Checklist

After setup, verify agent is working correctly:

**Test 1: Basic Execution**
```
Input: [TEST_INPUT_1]
Expected Output: [TEST_OUTPUT_1]
```

**Test 2: [TEST_NAME_2]**
```
Input: [TEST_INPUT_2]
Expected Output: [TEST_OUTPUT_2]
```

**Test 3: [TEST_NAME_3]**
```
Input: [TEST_INPUT_3]
Expected Output: [TEST_OUTPUT_3]
```

### Validation Criteria

✅ Agent responds in [EXPECTED_LANGUAGE]
✅ Output follows [OUTPUT_FORMAT]
✅ [VALIDATION_CRITERION_1]
✅ [VALIDATION_CRITERION_2]
✅ [VALIDATION_CRITERION_3]

---

## 🔧 TROUBLESHOOTING

### Issue 1: [COMMON_ISSUE_1]

**Symptoms**: [SYMPTOMS_1]

**Solution**:
1. [SOLUTION_STEP_1]
2. [SOLUTION_STEP_2]
3. [SOLUTION_STEP_3]

---

### Issue 2: [COMMON_ISSUE_2]

**Symptoms**: [SYMPTOMS_2]

**Solution**:
1. [SOLUTION_STEP_1]
2. [SOLUTION_STEP_2]

---

### Issue 3: [COMMON_ISSUE_3]

**Symptoms**: [SYMPTOMS_3]

**Solution**:
1. [SOLUTION_STEP_1]
2. [SOLUTION_STEP_2]

---

## 📊 PLATFORM COMPARISON

| Feature | Claude Code | Claude Web | OpenAI API | Custom GPT | Gemini |
|---------|-------------|------------|------------|------------|--------|
| [FEATURE_1] | [CLAUDE_CODE_1] | [CLAUDE_WEB_1] | [OPENAI_1] | [GPT_1] | [GEMINI_1] |
| [FEATURE_2] | [CLAUDE_CODE_2] | [CLAUDE_WEB_2] | [OPENAI_2] | [GPT_2] | [GEMINI_2] |
| [FEATURE_3] | [CLAUDE_CODE_3] | [CLAUDE_WEB_3] | [OPENAI_3] | [GPT_3] | [GEMINI_3] |
| [FEATURE_4] | [CLAUDE_CODE_4] | [CLAUDE_WEB_4] | [OPENAI_4] | [GPT_4] | [GEMINI_4] |
| **Recommended** | [CLAUDE_CODE_REC] | [CLAUDE_WEB_REC] | [OPENAI_REC] | [GPT_REC] | [GEMINI_REC] |

**Legend**: ✅ Full support | ⚠️ Partial support | ❌ Not supported

---

## 🎯 RECOMMENDED SETUP

**For best results**:

1. **Platform**: [RECOMMENDED_PLATFORM]
2. **Model**: [RECOMMENDED_MODEL]
3. **Why**: [RECOMMENDATION_REASON]

**Alternative**:

1. **Platform**: [ALTERNATIVE_PLATFORM]
2. **Model**: [ALTERNATIVE_MODEL]
3. **Why**: [ALTERNATIVE_REASON]

---

## 📚 ADDITIONAL RESOURCES

**Documentation**:
- [PRIME.md](PRIME.md) - Agent philosophy and principles
- [INSTRUCTIONS.md](INSTRUCTIONS.md) - Technical instructions for AI assistants
- [README.md](README.md) - Agent overview and structure
- [ARCHITECTURE.md](ARCHITECTURE.md) - Detailed technical architecture (if exists)

**Configuration Files**:
- [CONFIG_FILE_1] - [CONFIG_DESCRIPTION_1]
- [CONFIG_FILE_2] - [CONFIG_DESCRIPTION_2]

**Examples**:
- [EXAMPLE_FILE_1] - [EXAMPLE_DESCRIPTION_1]
- [EXAMPLE_FILE_2] - [EXAMPLE_DESCRIPTION_2]

---

**Version**: [VERSION]
**Created**: [CREATED_DATE]
**Last Updated**: [LAST_UPDATED]
**Maintainer**: [MAINTAINER]
**Support**: [SUPPORT_CONTACT]

---

> 🚀 **Ready to deploy** - Follow platform-specific instructions above
> 💡 **Pro Tip**: [PRO_TIP]
> ✅ **Verified**: Tested on [TESTED_PLATFORMS]
