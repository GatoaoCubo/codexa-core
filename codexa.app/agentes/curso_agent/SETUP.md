# SETUP GUIDE | CODEXA Curso Agent v2.0.0

**Universal setup instructions** for deploying curso_agent across different LLM platforms.

**Last Updated**: 2025-11-21

---

## PRE-REQUISITES

### Required Files

Ensure you have the complete `curso_agent/` folder with:
- **PRIME.md** - Entry point for agent context
- **INSTRUCTIONS.md** - Agent instructions (for builders)
- **README.md** - Overview and quick start
- **config/** - Path management (paths.py)
- **builders/** - 5 LLM-Powered Meta-Builders
- **validators/** - 5 Quality Validators
- **commands/** - 6 Slash Commands
- **workflows/** - 3 ADW Workflows
- **prompts/** - 5 HOPs (TAC-7)
- **templates/** - 4 Templates with [OPEN_VARIABLES]
- **context/** - 10 Course content files
- **outputs/** - Generated content directory

### Minimum Capabilities Required

| Capability | Status | Notes |
|------------|--------|-------|
| File I/O | REQUIRED | Read/write files |
| Python 3.8+ | REQUIRED | Run builders/validators |
| JSON parsing | REQUIRED | Parse configuration |
| Markdown | REQUIRED | Process templates |

---

## PLATFORM SETUP

### 1. CLAUDE CODE CLI (Recommended)

**Steps**:

1. Navigate to agent folder:
   ```bash
   cd path/to/curso_agent
   ```

2. Load context via slash command:
   ```bash
   /prime-curso
   ```

3. Run a builder:
   ```bash
   python builders/02_video_script_builder.py --module 01 --verbose
   ```

4. Validate output:
   ```bash
   python validators/01_content_quality_validator.py --file outputs/video_scripts/01_*.md
   ```

**Output Location**: `outputs/`

### 2. CLAUDE WEB/API

**Steps**:

1. Copy-paste `PRIME.md` content into conversation
2. Optionally include relevant context files
3. Provide input: "Generate video script for Module 01"
4. Agent will generate Trinity output

### 3. OPENAI GPT-4 ASSISTANTS

**Steps**:

1. Create new Assistant:
   - Name: CODEXA Curso Agent
   - Model: gpt-4
   - Instructions: Paste INSTRUCTIONS.md content

2. Upload knowledge files:
   - PRIME.md
   - context/*.md (all 10 files)
   - prompts/*.md (all 5 HOPs)

3. Enable tools:
   - Code Interpreter
   - File Search

4. Configure:
   ```yaml
   Temperature: 0.7
   max_tokens: 4096
   ```

### 4. CUSTOM PLATFORM

**For any LLM supporting custom instructions**:

1. **Instructions**: Paste INSTRUCTIONS.md content
2. **Knowledge**: Upload PRIME.md + context/ files
3. **Parameters**: Temperature 0.7, max_tokens 4096

---

## VERIFICATION

### Post-Setup Checklist

**Test 1: Builder Execution**
```bash
python builders/02_video_script_builder.py --module 01 --verbose
# Expected: Trinity output in outputs/video_scripts/
```

**Test 2: Validator Execution**
```bash
python validators/01_content_quality_validator.py --file outputs/video_scripts/01_*.md --verbose
# Expected: Score >= 7.0/10.0 PASSED
```

**Test 3: Path Validation**
```bash
python -c "from config.paths import validate_paths; validate_paths()"
# Expected: All paths valid
```

### Validation Criteria

- Agent responds in Portuguese (BR)
- Output follows Trinity format (.md + .llm.json + .meta.json)
- Quality threshold >= 7.0 met
- All context files accessible
- Builders/validators execute without errors

---

## TROUBLESHOOTING

### Issue 1: Unicode Errors (Windows)

**Symptoms**: UnicodeEncodeError with emojis

**Solution**:
```bash
# Set UTF-8 encoding
set PYTHONIOENCODING=utf-8
# Or run with:
python -X utf8 builders/02_video_script_builder.py
```

### Issue 2: Path Not Found

**Symptoms**: FileNotFoundError for context files

**Solution**:
1. Verify you're in curso_agent/ directory
2. Check config/paths.py is correct
3. Run path validation:
   ```bash
   python -c "from config.paths import validate_paths; validate_paths()"
   ```

### Issue 3: Low Validation Score

**Symptoms**: Score < 7.0

**Solution**:
1. Check output has [OPEN_VARIABLES] (need >= 2)
2. Verify hook is <= 90 seconds
3. Ensure timing marks present
4. Add Brazilian market examples

---

## QUICK REFERENCE

### Run Builder
```bash
python builders/02_video_script_builder.py --module [01-06] --verbose
```

### Run Validator
```bash
python validators/01_content_quality_validator.py --file [PATH] --verbose
```

### Validate All
```bash
python validators/01_content_quality_validator.py --file outputs/video_scripts/*.md
python validators/02_brand_voice_validator.py --file outputs/video_scripts/*.md
```

---

## ADDITIONAL RESOURCES

**Documentation**:
- [PRIME.md](PRIME.md) - Agent philosophy
- [INSTRUCTIONS.md](INSTRUCTIONS.md) - AI integration guide
- [README.md](README.md) - Overview

**Workflows**:
- workflows/01_ADW_QUICK_COURSE.md - 5-10 min
- workflows/02_ADW_FULL_MODULE.md - 30-45 min
- workflows/03_ADW_SALES_PACKAGE.md - 20-30 min

**Commands**:
- /curso_outline - Generate course structure
- /curso_script - Generate video script
- /curso_workbook - Generate workbook
- /curso_sales - Generate sales materials
- /curso_validate - Run validation suite
- /curso_package - Package for Hotmart

---

**Version**: 2.0.0
**Last Updated**: 2025-11-21
**Maintainer**: CODEXA Team

---

> **Ready to deploy** - Follow platform-specific instructions above
> **Pro Tip**: Start with /curso_script for quick testing
> **Verified**: Tested on Claude Code, OpenAI API
