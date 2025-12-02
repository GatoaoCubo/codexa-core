# SETUP GUIDE | video_agent v1.0.0

**Universal setup instructions** for deploying video_agent across different LLM platforms.

**Last Updated**: 2025-11-24

---

## PRE-REQUISITES

### Required Files

Ensure you have the complete `video_agent/` folder with:
- PRIME.md - Entry point for agent context
- INSTRUCTIONS.md - Agent instructions (for builders)
- config/ - API configurations and style presets
- prompts/ - 5 modular HOPs (one per stage)
- builders/ - 5 Python builders
- outputs/ - Output directory (auto-created)

### Minimum Capabilities Required

- FFmpeg - REQUIRED (local video processing)
- Anthropic API - REQUIRED (Claude for reasoning)
- Runway API - RECOMMENDED (primary video generation)
- Pika API - OPTIONAL (fallback video generation)
- ElevenLabs API - OPTIONAL (TTS narration)

**Legend**:
- REQUIRED - Agent cannot run without this
- RECOMMENDED - Agent works better with this
- OPTIONAL - Nice to have, not critical

---

## SYSTEM REQUIREMENTS

### FFmpeg Installation

**Windows**:
```bash
# Using Chocolatey
choco install ffmpeg

# Or download from https://ffmpeg.org/download.html
# Add to PATH: C:\ffmpeg\bin
```

**macOS**:
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt update
sudo apt install ffmpeg
```

**Verify installation**:
```bash
ffmpeg -version
ffprobe -version
```

### Python Dependencies

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Install dependencies
pip install anthropic httpx aiofiles python-dotenv

# Optional: TTS support
pip install elevenlabs
```

---

## API CONFIGURATION

### 1. Environment Variables

Create `.env` file in video_agent directory:

```env
# Required
ANTHROPIC_API_KEY=sk-ant-xxx

# Video Generation (at least one required)
RUNWAY_API_KEY=rw_xxx
PIKA_API_KEY=pk_xxx

# Optional (TTS)
ELEVENLABS_API_KEY=el_xxx
```

### 2. API Config File

Edit `config/api_config.json`:

```json
{
  "runway": {
    "base_url": "https://api.runwayml.com/v1",
    "model": "gen-3",
    "quality": "high",
    "timeout_seconds": 300,
    "max_concurrent": 5
  },
  "pika": {
    "base_url": "https://api.pika.art/v1",
    "model": "1.5",
    "quality": "medium",
    "timeout_seconds": 180,
    "max_concurrent": 3
  },
  "elevenlabs": {
    "model": "eleven_multilingual_v2",
    "voice_id": "Rachel",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.75
    }
  }
}
```

### 3. Style Presets

Review/customize `config/video_styles.json`:

```json
{
  "energetic": {
    "camera": "dynamic tracking",
    "lighting": "high contrast",
    "pacing": "fast cuts (2-3s)",
    "transitions": "hard cut",
    "use_cases": ["sports", "tech", "youth"]
  },
  "calm": {
    "camera": "slow, smooth",
    "lighting": "soft, warm",
    "pacing": "slow dissolves (4-5s)",
    "transitions": "dissolve",
    "use_cases": ["wellness", "luxury", "lifestyle"]
  }
}
```

---

## PLATFORM SETUP

### 1. CLAUDE (Anthropic)

#### Option A: Claude Code CLI (Recommended)

**Steps**:

1. Navigate to agent folder:
   ```bash
   cd codexa.app/agentes/video_agent
   ```

2. Load context via slash command:
   ```bash
   # If you have /prime-video configured:
   /prime-video

   # Otherwise, manually load PRIME.md:
   cat PRIME.md
   ```

3. Provide input:
   ```
   Generate a 30s video for "Nike Air Max 2024" with energetic style,
   focusing on amortecimento Air e design moderno
   ```

4. Agent will auto-detect capabilities and execute

**Capabilities in Claude Code**:
- File reading/writing: Full support
- Code execution: Full support (Python)
- External APIs: Full support (via Python)
- FFmpeg: Requires system installation

**Output Location**: `outputs/*.mp4`

#### Option B: Claude Web/API

**Steps**:

1. Open Claude web interface or API client

2. Copy-paste full context:
   - Paste entire `PRIME.md` content
   - Paste `config/video_styles.json` for reference
   - Paste ADW workflow for execution steps

3. Provide input in conversation

4. Agent will generate code snippets for each phase
   - User must execute locally or provide execution environment

**Capabilities**:
- Reasoning: Full (storyboard, script generation)
- Code generation: Full (builders, FFmpeg commands)
- API calls: Requires external execution

---

### 2. OPENAI (ChatGPT / API)

#### Option A: GPT-4 Assistants API (Recommended)

**Steps**:

1. Create a new Assistant in OpenAI Platform:
   - Go to https://platform.openai.com/assistants
   - Click "Create Assistant"

2. Configure Assistant:
   ```yaml
   Name: video_agent
   Model: gpt-4-turbo
   Instructions: [PASTE INSTRUCTIONS.md CONTENT]
   Tools:
     - code_interpreter
     - file_search
   Temperature: 0.7
   ```

3. Upload knowledge files to Vector Store:
   - Create new Vector Store: "video_agent Knowledge Base"
   - Upload files:
     ```
     PRIME.md
     config/video_styles.json
     config/api_config.json
     workflows/100_ADW_RUN_VIDEO.md
     ```
   - Attach Vector Store to Assistant

4. Configure file_search tool:
   ```yaml
   file_search:
     max_num_results: 10
     ranking_options:
       score_threshold: 0.5
   ```

5. Test with sample input

**Capabilities**:
- Reasoning: Full
- Code generation: Full
- File execution: Via code_interpreter (limited)

**Limitations**:
- No FFmpeg in code_interpreter
- Requires external video processing

#### Option B: ChatGPT Custom GPT

**Steps**:

1. Go to https://chat.openai.com/gpts/editor

2. Configure GPT:
   ```yaml
   Name: video_agent
   Description: AI-powered e-commerce video generator
   Instructions: [PASTE INSTRUCTIONS.md CONTENT]
   Conversation starters:
     - "Create a 30s video for a sneaker product"
     - "Generate energetic video for tech gadget"
     - "Make a calm wellness product video"
   Capabilities:
     - Code Interpreter: enabled
     - Web Browsing: disabled
   ```

3. Upload knowledge files (max 20 files, 512MB total):
   - Upload: PRIME.md, video_styles.json, api_config.json

4. Save and test

---

### 3. GEMINI (Google)

#### Option A: Gemini Web

**Steps**:

1. Go to https://gemini.google.com

2. Upload context files:
   - Upload `PRIME.md`
   - Upload `config/video_styles.json`

3. Paste instructions:
   ```
   You are video_agent, a specialized AI for e-commerce video production.
   Follow the 5-stage pipeline: Concept -> Script -> Visual -> Production -> Editing.
   Generate detailed outputs for each phase.
   ```

4. Provide input

**Capabilities**:
- Reasoning: Full
- Code generation: Full
- Execution: None (requires external)

**Limitations**:
- No code execution
- Limited file handling
- Manual phase execution

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
   model = genai.GenerativeModel('gemini-pro')

   # Load PRIME.md as system context
   with open('PRIME.md', 'r') as f:
       prime_context = f.read()

   chat = model.start_chat(history=[
       {"role": "user", "parts": [prime_context]},
       {"role": "model", "parts": ["video_agent loaded. Ready for briefs."]}
   ])

   response = chat.send_message("Generate 30s video for Nike Air Max")
   ```

---

### 4. ANY LLM / AGENT BUILDER

#### Universal Setup (Manual Configuration)

**For platforms supporting custom instructions** (LangChain, AutoGen, etc.):

1. **Copy Instructions**:
   - Open `INSTRUCTIONS.md`
   - Copy entire content
   - Paste into "Instructions" field of your platform

2. **Upload Knowledge Files** (if supported):
   - Priority A (Critical):
     ```
     PRIME.md
     workflows/100_ADW_RUN_VIDEO.md
     config/video_styles.json
     ```
   - Priority B (Recommended):
     ```
     config/api_config.json
     schemas/video_input.json
     schemas/video_output.json
     ```

3. **Configure Capabilities**:
   - Enable: Code execution, File I/O
   - Recommended: API calls, External tools

4. **Set Parameters**:
   ```yaml
   temperature: 0.7
   max_tokens: 4096
   top_p: 0.9
   ```

5. **Test**: Provide sample input and verify output structure

---

## VERIFICATION

### Post-Setup Checklist

After setup, verify agent is working correctly:

**Test 1: FFmpeg Check**
```bash
ffmpeg -version
# Expected: ffmpeg version X.X.X
```

**Test 2: API Connection**
```bash
python -c "
import os
from anthropic import Anthropic
client = Anthropic()
print('Anthropic API connected')
"
```

**Test 3: Mock Pipeline**
```bash
VIDEO_AGENT_MOCK_API=true python src/video_agent.py \
  --produto "Test Product" \
  --duracao 15 \
  --formato "9:16" \
  --mock
```

### Validation Criteria

- Agent responds with structured JSON
- Output follows 5-stage pipeline
- Concept generates 3-8 shots
- Script has narration and overlays
- Visual prompts are in English
- Final output is valid MP4 (mock mode: placeholder)

---

## TROUBLESHOOTING

### Issue 1: FFmpeg Not Found

**Symptoms**: "ffmpeg: command not found" or "FileNotFoundError"

**Solution**:
1. Verify FFmpeg installation: `ffmpeg -version`
2. Add FFmpeg to system PATH
3. On Windows, check: `where ffmpeg`
4. On macOS/Linux, check: `which ffmpeg`

---

### Issue 2: API Timeout

**Symptoms**: "Request timed out" after 300s

**Solution**:
1. Check API status (Runway/Pika dashboard)
2. Reduce concurrent requests in config
3. Enable fallback API (Runway -> Pika)
4. Use mock mode for testing: `VIDEO_AGENT_MOCK_API=true`

---

### Issue 3: TTS Not Working

**Symptoms**: Video has no narration audio

**Solution**:
1. Verify ELEVENLABS_API_KEY is set
2. Install library: `pip install elevenlabs`
3. Check quota in ElevenLabs dashboard
4. Fallback: Video will be music-only

---

### Issue 4: Font Not Found (Text Overlays)

**Symptoms**: Text overlays missing or error in FFmpeg

**Solution**:
1. Check font path in `05_editing_builder.py`
2. Windows: Verify `C:/Windows/Fonts/arial.ttf` exists
3. Linux: Install fonts: `sudo apt install fonts-dejavu`
4. macOS: Use system fonts `/System/Library/Fonts/`

---

## PLATFORM COMPARISON

| Feature | Claude Code | Claude Web | OpenAI API | Custom GPT | Gemini |
|---------|-------------|------------|------------|------------|--------|
| Reasoning | Full | Full | Full | Full | Full |
| Code Execution | Full | Manual | Partial | Partial | None |
| File I/O | Full | None | Partial | Limited | None |
| FFmpeg | System | None | None | None | None |
| API Calls | Full | Manual | Via code | None | Manual |
| **Recommended** | Production | Design | Integration | Demo | Reasoning |

**Legend**: Full support | Partial support | None

---

## RECOMMENDED SETUP

**For best results**:

1. **Platform**: Claude Code CLI
2. **Model**: Claude Sonnet 4 (reasoning) + Claude Haiku (validation)
3. **Why**: Full code execution, file I/O, system tool access (FFmpeg), native API integration

**Alternative**:

1. **Platform**: OpenAI Assistants API + Local execution
2. **Model**: GPT-4 Turbo
3. **Why**: Good reasoning, but requires local FFmpeg execution

---

## ADDITIONAL RESOURCES

**Documentation**:
- [PRIME.md](PRIME.md) - Agent philosophy and principles
- [INSTRUCTIONS.md](INSTRUCTIONS.md) - Technical instructions for AI assistants
- [README.md](README.md) - Agent overview and structure

**Configuration Files**:
- `config/api_config.json` - API endpoints and rate limits
- `config/video_styles.json` - 5 style presets

**Examples**:
- `examples/tenis_nike_30s.md` - Complete example output
- `examples/tenis_nike_30s.llm.json` - Structured metadata

---

**Version**: 1.0.0
**Created**: 2025-11-24
**Last Updated**: 2025-11-24
**Maintainer**: CODEXA Meta-Constructor
**Support**: Check TROUBLESHOOTING section above

---

> Ready to deploy - Follow platform-specific instructions above
> Pro Tip: Start with mock mode (VIDEO_AGENT_MOCK_API=true) to test pipeline before using real APIs
> Verified: Tested on Claude Code CLI + FFmpeg
