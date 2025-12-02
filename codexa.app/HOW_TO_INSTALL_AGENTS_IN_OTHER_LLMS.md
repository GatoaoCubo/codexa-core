# 📖 HOW TO INSTALL AGENTS IN OTHER LLMS

**Purpose**: Guide for installing CODEXA agents in other LLM platforms (ChatGPT, Claude Projects, Gemini, etc.)
**Last Updated**: 2025-11-17
**Applies to**: All 6 agents with iso_vectorstore (anuncio, codexa, marca, mentor, pesquisa, photo)

---

## 🎯 OVERVIEW

Each agent's `iso_vectorstore` directory contains **20 carefully curated files** (≤20 limit) representing the agent's complete capabilities for standalone operation. This guide explains which files to copy to Custom Instructions in other LLMs.

---

## 📋 PRIORITY ORDER (COPY THESE FILES)

### TIER 1: CRITICAL (ALWAYS COPY) - ~60-100KB

These files are **absolutely essential** for agent functionality:

```
1. XX_[agent]_PRIME.md                    (PRIMARY INSTRUCTIONS)
   - Agent identity, capabilities, constraints
   - Execution guidelines
   - Core behavioral patterns
   - Size: ~7-9KB
   - Example: 03_photo_agent_PRIME.md

2. XX_[agent]_README.md                   (AGENT DOCUMENTATION)
   - Overview, quick start, input/output schemas
   - Architecture (Dual-Layer ADW + HOP)
   - Usage examples
   - Size: ~18-20KB
   - Example: 05_photo_agent_README.md

3. 15-20_ADW_RUN_[AGENT].md              (WORKFLOW ORCHESTRATION)
   - Complete workflow (5-9 phases)
   - Phase objectives, inputs, outputs
   - Validation criteria, error handling
   - Size: ~16-47KB
   - Example: 15_ADW_RUN_PHOTO.md

4. 02_HOP_FRAMEWORK.md                    (EXECUTION PATTERN)
   - HOP (Higher-Order Prompt) methodology
   - TAC-7 format guidelines
   - Integration patterns
   - Size: ~11KB
   - Universal across all agents
```

**Total Tier 1**: ~52-87KB (4 files)

---

### TIER 2: OPERATIONAL (HIGH PRIORITY) - ~50-150KB

These files enable **full operational capability**:

```
5-N. XX_[specific]_HOP.md                 (EXECUTION PROMPTS)
   - Detailed step-by-step instructions per phase
   - Examples, error handling, validation
   - Size: ~17-26KB each
   - Count: Varies by agent

   Examples (photo_agent):
   - 16_scene_planner_HOP.md (17KB)
   - 17_camera_designer_HOP.md (22KB)
   - 18_prompt_generator_HOP.md (20KB)
   - 19_brand_validator_HOP.md (26KB)
   - 20_batch_assembler_HOP.md (25KB)

6. XX_[agent]_INSTRUCTIONS.md             (DETAILED INSTRUCTIONS)
   - Extended operational guidelines
   - Advanced features, edge cases
   - Size: ~27KB
   - Example: 04_photo_agent_INSTRUCTIONS.md
```

**Total Tier 2**: ~50-150KB (depending on agent complexity)

---

### TIER 3: CONFIGURATION (MEDIUM PRIORITY) - ~50-100KB

These files provide **domain-specific knowledge**:

```
7-12. Config JSON files                   (DOMAIN DATA)
   - Schemas, profiles, triggers, marketplaces
   - Size: 10-35KB each (photo_agent has large schemas)

   Examples (photo_agent):
   - 10_photo_camera_profiles.json (11KB)
   - 11_photo_photography_styles.json (10KB)
   - 12_photo_pnl_triggers.json (20KB)
   - 07_photo_input_schema.json (12KB)
   - 08_photo_marketplace_output.json (25KB)
   - 09_photo_brand_output.json (35KB)
```

**Total Tier 3**: ~50-100KB (varies by agent)

---

### TIER 4: CONTEXT (LOW PRIORITY) - ~20-30KB

These files provide **ecosystem context** (optional):

```
13. 01_CODEXA_INSTRUCTIONS.md            (CODEXA SYSTEM)
   - Meta-system guidelines
   - Size: ~8KB

14. 13_AGENT_REGISTRY.json               (AGENT METADATA)
   - Agent registration info
   - Size: ~7KB

15. 14_[agent]_Custom_Instructions.md    (CUSTOM PROMPTS)
   - Platform-specific adaptations
   - Size: ~19KB
   - Example: 14_photo_Custom_Instructions.md
```

**Total Tier 4**: ~20-30KB (3 files)

---

## 🚀 INSTALLATION STRATEGIES (BY PLATFORM)

### STRATEGY 1: ChatGPT Custom GPT (Recommended for Full Agents)

**Limits**:
- Custom Instructions: ~8,000 characters (~8KB)
- Knowledge Base: Upload files (512MB total, 20 files max per upload)

**Installation Steps**:

1. **Create Custom GPT**:
   - Go to ChatGPT → Explore GPTs → Create
   - Name: "[Agent Name] - CODEXA Agent"
   - Description: Copy from README.md overview

2. **Custom Instructions** (paste in "Instructions" field):
   ```
   Copy ONLY:
   - XX_[agent]_PRIME.md (full content)

   Truncate if needed, prioritize:
   - Agent identity
   - Core capabilities
   - Execution guidelines
   ```

3. **Knowledge Base** (upload to "Knowledge" section):
   ```
   Upload ALL remaining iso_vectorstore files:
   - README.md
   - ADW_RUN_[AGENT].md
   - All HOP files
   - All config JSON files
   - INSTRUCTIONS.md
   - HOP_FRAMEWORK.md

   ChatGPT will auto-index and retrieve when needed.
   ```

**Result**: Agent has full context via knowledge retrieval.

---

### STRATEGY 2: Claude Projects (Best for Large Agents)

**Limits**:
- Custom Instructions: ~20,000 characters (~20KB)
- Project Knowledge: 100+ files, 10MB+ total

**Installation Steps**:

1. **Create Project**:
   - Claude → Projects → Create New Project
   - Name: "[Agent Name] Agent"

2. **Custom Instructions** (Project Instructions):
   ```
   Copy in this order (up to 20KB):

   1. XX_[agent]_PRIME.md (FULL)
   2. Truncated README.md (overview + architecture section only)
   3. Reference to project knowledge:
      "Additional context available in Project Knowledge:
      - ADW workflow: [filename]
      - HOP prompts: [list]
      - Config files: [list]"
   ```

3. **Project Knowledge** (Add all files):
   ```
   Upload ALL iso_vectorstore files except PRIME:
   - README.md (full version)
   - ADW workflow
   - All HOP files
   - All config files
   - INSTRUCTIONS.md
   - HOP_FRAMEWORK.md
   - Custom_Instructions.md
   ```

**Result**: Agent has full context, can reference any file.

---

### STRATEGY 3: Standard LLM Chat (Lightweight Setup)

**Limits**:
- System Prompt: Varies (typically 2,000-8,000 chars)
- No file upload (must paste text)

**Installation Steps**:

1. **System Prompt / Custom Instructions**:
   ```
   Copy in priority order until limit:

   1. XX_[agent]_PRIME.md (abbreviated version)
      - Keep: Identity, capabilities, core guidelines
      - Remove: Examples, extended documentation

   2. Key excerpt from ADW workflow:
      - Workflow phases overview (just phase names + objectives)
      - Remove: Detailed actions, examples

   3. Reference statement:
      "For detailed execution, request specific HOP prompts:
      - Phase 1: [HOP name]
      - Phase 2: [HOP name]
      ..."
   ```

2. **During Execution** (paste on-demand):
   ```
   When agent reaches a phase:

   User: "Execute Phase 2 using HOP prompt"
   Agent: (expects HOP content)
   User: [Paste 20_camera_designer_HOP.md content]

   Agent processes and executes.
   ```

**Result**: Lightweight setup, manual HOP loading per phase.

---

## 📝 EXAMPLE INSTALLATION: photo_agent

### Option A: ChatGPT Custom GPT (FULL AGENT)

**Step 1: Custom Instructions** (8KB limit):
```markdown
[PASTE FULL CONTENT OF: 03_photo_agent_PRIME.md]

Note: Complete documentation, workflows, and execution prompts
available in Knowledge Base.
```

**Step 2: Knowledge Base Upload** (19 files):
```
✅ 01_CODEXA_INSTRUCTIONS.md
✅ 02_HOP_FRAMEWORK.md
✅ 04_photo_agent_INSTRUCTIONS.md
✅ 05_photo_agent_README.md
✅ 06_photo_agent_SETUP.md
✅ 07_photo_input_schema.json
✅ 08_photo_marketplace_output.json
✅ 09_photo_brand_output.json
✅ 10_photo_camera_profiles.json
✅ 11_photo_photography_styles.json
✅ 12_photo_pnl_triggers.json
✅ 13_AGENT_REGISTRY.json
✅ 14_photo_Custom_Instructions.md
✅ 15_ADW_RUN_PHOTO.md ← WORKFLOW
✅ 16_scene_planner_HOP.md ← PHASE 1
✅ 17_camera_designer_HOP.md ← PHASE 2
✅ 18_prompt_generator_HOP.md ← PHASE 3
✅ 19_brand_validator_HOP.md ← PHASE 4
✅ 20_batch_assembler_HOP.md ← PHASE 5
```

**Step 3: Test**:
```
User: "Generate 9 AI photography prompts for a ceramic mug, minimalist style"

Agent will:
1. Load PRIME from instructions
2. Reference ADW workflow from knowledge
3. Execute phases using HOP prompts from knowledge
4. Use config files for camera/lighting specs
5. Generate complete output
```

---

### Option B: Claude Project (RECOMMENDED)

**Step 1: Project Instructions** (20KB limit):
```markdown
[PASTE FULL CONTENT OF: 03_photo_agent_PRIME.md]

---

[PASTE ARCHITECTURE SECTION FROM: 05_photo_agent_README.md]
(Lines 11-50: Dual-Layer Integration explanation)

---

EXECUTION WORKFLOW:
Primary workflow available in Project Knowledge:
- File: 15_ADW_RUN_PHOTO.md
- 5 phases: Input Processing → Camera Design → Prompt Generation →
  Validation → Batch Assembly

HOP Prompts available in Project Knowledge:
- Phase 1: 16_scene_planner_HOP.md
- Phase 2: 17_camera_designer_HOP.md
- Phase 3: 18_prompt_generator_HOP.md
- Phase 4: 19_brand_validator_HOP.md
- Phase 5: 20_batch_assembler_HOP.md

Configuration files available in Project Knowledge:
- Camera profiles, photography styles, PNL triggers, schemas

TO EXECUTE: Reference specific files as needed during workflow execution.
```

**Step 2: Upload to Project Knowledge** (all 19 remaining files)

**Step 3: Test**: Same as ChatGPT example

---

## 🎯 QUICK REFERENCE: MINIMUM VIABLE AGENT

If you have **severe space constraints**, copy ONLY these 3 files:

```
MINIMUM (Tier 1 only):
1. XX_[agent]_PRIME.md          (Identity + Core Guidelines)
2. XX_[agent]_README.md         (Architecture + Usage)
3. XX_ADW_RUN_[AGENT].md        (Workflow Orchestration)

Total: ~52-80KB (3 files)

This gives basic agent capability. Load HOP prompts on-demand during execution.
```

---

## 📊 FILE SIZE REFERENCE (photo_agent)

```
TIER 1 (CRITICAL):
03_photo_agent_PRIME.md               7.3 KB  ★ ALWAYS INCLUDE
05_photo_agent_README.md             20.0 KB  ★ ALWAYS INCLUDE
15_ADW_RUN_PHOTO.md                  18.0 KB  ★ ALWAYS INCLUDE
02_HOP_FRAMEWORK.md                  11.0 KB  ★ ALWAYS INCLUDE
                                    ─────────
TIER 1 SUBTOTAL:                     56.3 KB

TIER 2 (OPERATIONAL):
16_scene_planner_HOP.md              17.0 KB
17_camera_designer_HOP.md            22.0 KB
18_prompt_generator_HOP.md           20.0 KB
19_brand_validator_HOP.md            26.0 KB
20_batch_assembler_HOP.md            25.0 KB
04_photo_agent_INSTRUCTIONS.md       27.0 KB
                                    ─────────
TIER 2 SUBTOTAL:                    137.0 KB

TIER 3 (CONFIGURATION):
07_photo_input_schema.json           12.0 KB
08_photo_marketplace_output.json     25.0 KB
09_photo_brand_output.json           35.0 KB
10_photo_camera_profiles.json        11.0 KB
11_photo_photography_styles.json     10.0 KB
12_photo_pnl_triggers.json           20.0 KB
                                    ─────────
TIER 3 SUBTOTAL:                    113.0 KB

TIER 4 (CONTEXT):
01_CODEXA_INSTRUCTIONS.md             8.0 KB
13_AGENT_REGISTRY.json                7.0 KB
14_photo_Custom_Instructions.md      19.0 KB
06_photo_agent_SETUP.md              19.0 KB
                                    ─────────
TIER 4 SUBTOTAL:                     53.0 KB

═══════════════════════════════════════════
TOTAL iso_vectorstore:              359.3 KB (20 files)
```

---

## 🔧 PLATFORM-SPECIFIC TIPS

### ChatGPT Custom GPTs
- **Pros**: Knowledge retrieval works well, no manual file loading
- **Cons**: 8KB instructions limit (only fits PRIME)
- **Best For**: Agents with many HOP prompts (anuncio, pesquisa, photo)
- **Tip**: Upload ALL files to Knowledge, agent auto-retrieves

### Claude Projects
- **Pros**: 20KB instructions (fits PRIME + README summary), excellent file handling
- **Cons**: None significant
- **Best For**: All agents (most versatile platform)
- **Tip**: Reference files by name in instructions for faster retrieval

### Gemini with Google Drive
- **Pros**: Can link Google Drive folder with all files
- **Cons**: Retrieval less reliable than Claude/ChatGPT
- **Best For**: Agents with large config files (mentor_agent 654KB catalogo)
- **Tip**: Put critical files in prompt, supplementary in Drive

### Perplexity Pro
- **Pros**: Good web search integration (useful for pesquisa_agent)
- **Cons**: Limited custom instructions support
- **Best For**: Lightweight agents or research-focused (pesquisa)
- **Tip**: Focus on PRIME only, load HOPs as needed

---

## ⚠️ COMMON MISTAKES

### ❌ DON'T:
1. Copy ALL 20 files into Custom Instructions (exceeds limits)
2. Skip the PRIME file (agent loses identity)
3. Skip the ADW workflow (agent can't orchestrate)
4. Paste files out of order (confuses agent)
5. Use file numbering in chat (remove "03_", "15_" prefixes in paste)

### ✅ DO:
1. Copy PRIME first (always)
2. Upload remaining files to Knowledge/Project (when available)
3. Reference files by name in instructions
4. Test with simple task first
5. Keep iso_vectorstore folder intact for reference

---

## 📚 AGENT-SPECIFIC NOTES

### anuncio_agent (Ad Copywriting)
- **Critical**: 10 HOP prompts (title, keywords, bullets, description, etc.)
- **Strategy**: ChatGPT Custom GPT with all HOPs in Knowledge
- **Minimum**: PRIME + ADW + 10_main_agent_hop.md

### codexa_agent (Meta-Constructor)
- **Critical**: 5 Python modules (builder scripts)
- **Strategy**: Local execution (Python required) OR Claude Project
- **Minimum**: PRIME + 99_ADW_SYSTEM_UPGRADE.md

### marca_agent (Brand Strategy)
- **Critical**: brand_strategy.json, color_psychology.json
- **Strategy**: Claude Project (good JSON handling)
- **Minimum**: PRIME + ADW + config JSONs

### mentor_agent (E-commerce Mentoring)
- **Critical**: 654KB catalogo.json (massive knowledge base)
- **Strategy**: Claude Project (handles large files) OR Gemini + Drive
- **Minimum**: PRIME + ADW + catalogo.json

### pesquisa_agent (Market Research)
- **Critical**: 12 HOP prompts (web search, analysis, etc.)
- **Strategy**: Perplexity Pro OR ChatGPT (web search integration)
- **Minimum**: PRIME + ADW + web_search HOPs

### photo_agent (AI Photography)
- **Critical**: 5 HOP prompts + camera/lighting configs
- **Strategy**: Claude Project OR ChatGPT Custom GPT
- **Minimum**: PRIME + ADW + 5 HOP prompts

---

## 🎓 ADVANCED: CONSOLIDATION STRATEGY

If you need to fit an agent in <50KB total:

1. **Merge PRIME + README**: Create single "Agent Core" document
2. **Summarize ADW**: Keep phase names + objectives, remove examples
3. **Select 1-2 critical HOPs**: Based on most-used features
4. **Inline small configs**: Paste JSON directly into instructions
5. **Reference remaining files**: "Additional HOPs available on request"

**Example Consolidated Prompt** (photo_agent in 45KB):
```markdown
# photo_agent - AI Photography Prompt Generator

[PRIME.md identity section - 3KB]

## Architecture Overview
[README.md Dual-Layer section - 5KB]

## Workflow (5 Phases)
[ADW phase summary - 8KB]

## Phase 3 Execution (Most Critical)
[18_prompt_generator_HOP.md full - 20KB]

## Configurations (Inline)
[camera_profiles.json - 5KB]
[photography_styles.json - 4KB]

---
Total: ~45KB
Missing: Phases 1,2,4,5 HOP prompts (load on-demand if needed)
```

---

## ✅ VERIFICATION CHECKLIST

After installation, verify agent works:

- [ ] Agent responds with correct identity (from PRIME)
- [ ] Agent can describe its workflow (from ADW)
- [ ] Agent can execute at least 1 complete phase (from HOP)
- [ ] Agent uses config files (camera profiles, schemas, etc.)
- [ ] Agent produces expected output format (Trinity: .md + .json files)

---

## 🆘 TROUBLESHOOTING

**Agent doesn't know its identity**:
→ PRIME.md not loaded or truncated

**Agent can't find workflow**:
→ ADW file not in Knowledge/Project, or not referenced

**Agent gives generic responses**:
→ HOP prompts missing, agent falling back to base LLM knowledge

**Agent can't access configs**:
→ JSON files not uploaded or not readable by platform

**Agent workflow stops mid-execution**:
→ Missing HOP for current phase, need to paste manually

---

## 📞 SUPPORT

For issues:
1. Check `iso_vectorstore/` folder has all 20 files
2. Verify file sizes match this guide
3. Test with minimum viable setup first (PRIME + ADW + 1 HOP)
4. Consult agent's README.md for specific requirements

---

**Last Updated**: 2025-11-17
**Applies To**: All CODEXA agents with synchronized iso_vectorstore
**Document Version**: 1.0.0
