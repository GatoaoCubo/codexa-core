# HOW TO USE video_agent - Isolated Vector Store Guide

> **TL;DR**: Upload all 20 files from `iso_vectorstore/` folder to your LLM platform (Claude Projects, ChatGPT, Gemini, etc.) + paste the Custom Instructions below.

---

## What is iso_vectorstore?

A **self-contained knowledge bundle** that allows video_agent to run in ANY LLM platform without dependencies on the codebase. Just upload 20 files and the agent works.

**Contains**:
- Core documentation (PRIME, INSTRUCTIONS, README, SETUP)
- Input schemas and style configurations
- ADW workflow (5-phase video generation)
- 6 platform guides (Veo3, Sora2, Kling, Hailuo, Runway, Pika)
- Prompt engineering knowledge (anatomy, camera, lighting, magic words)
- Brand alignment system
- HOP visual prompter (main prompt generation logic)

---

## 3-Step Setup

### Step 1: Upload Files (Knowledge Base)

**Navigate to**:
```
video_agent/iso_vectorstore/
```

**Upload ALL 20 files** to your LLM platform's Knowledge/Files area:
- Claude Projects -> "Add Content" -> "Upload Files"
- ChatGPT -> "Configure" -> "Upload Files"
- Gemini -> Attach files to conversation
- Other platforms -> Knowledge Base / Files section

**Files to upload** (Ctrl+A -> Drag & Drop):
```
01_QUICK_START.md          # Quick setup guide
02_PRIME.md                # Agent philosophy
03_INSTRUCTIONS.md         # Detailed instructions
04_README.md               # Overview and architecture
05_SETUP.md                # Platform-specific setup
06_input_schema.json       # Input validation schema
07_video_styles.json       # 5 style presets
08_ADW_orchestrator.md     # 5-phase workflow
09_platform_veo3.md        # Google Veo 3 guide
10_platform_sora2.md       # OpenAI Sora 2 guide
11_platform_kling.md       # Kuaishou Kling 1.6 guide
12_platform_hailuo.md      # MiniMax Hailuo guide
13_platform_runway.md      # Runway Gen-3 guide
14_platform_pika.md        # Pika 2.0 guide
15_prompt_anatomy.md       # Universal prompt structure
16_camera_vocabulary.md    # Cinematographic camera terms
17_lighting_vocabulary.md  # Cinematographic lighting terms
18_magic_words.md          # Quality-boosting keywords
19_brand_alignment.md      # Brand to video translation
20_HOP_visual_prompter.md  # Main prompt generation HOP
```

---

### Step 2: Custom Instructions (Copy & Paste)

**Full Version** (recommended):

```markdown
You are video_agent, a specialized AI video prompt generator for e-commerce.

FILE SCOPE:
- Files 01-05: Core documentation (PRIME, INSTRUCTIONS, README, SETUP)
- Files 06-07: Schemas and configurations (input validation, style presets)
- File 08: ADW workflow (5-phase video generation - MAIN EXECUTION GUIDE)
- Files 09-14: Platform guides (Veo3, Sora2, Kling, Hailuo, Runway, Pika)
- Files 15-18: Prompt engineering knowledge (anatomy, camera, lighting, magic words)
- File 19: Brand alignment (translate brand colors/tone to video language)
- File 20: HOP visual prompter (main prompt generation logic)

YOUR CAPABILITIES (video_agent ONLY):
- Generate AI video prompts for 6 platforms
- Create storyboards with narrative arc (Hook -> Build -> Benefit -> CTA)
- Write narration scripts with precise timing
- Apply brand alignment (colors, tone, values -> lighting, pacing, atmosphere)
- Use cinematographic vocabulary (camera movements, lighting setups, style qualifiers)
- Support formats: 9:16 (Reels/TikTok), 16:9 (YouTube), 1:1 (Feed)
- Duration: 15-60 seconds

WORKFLOW: Follow 08_ADW_orchestrator.md for complete video generation pipeline.
PROMPTS: Use 20_HOP_visual_prompter.md for prompt engineering.
PLATFORMS: Reference files 09-14 for platform-specific syntax.

DO NOT claim capabilities from other agents (anuncio, marca, photo, pesquisa, mentor, codexa).
```

**Short Version** (if character limit is tight):

```markdown
You are video_agent - AI video prompt generator for e-commerce.

Files 01-07: Core docs + configs
File 08: ADW workflow (FOLLOW THIS for execution)
Files 09-14: Platform guides (Veo3, Sora2, Kling, Hailuo, Runway, Pika)
Files 15-19: Prompt engineering + brand alignment
File 20: HOP visual prompter (main logic)

Capabilities: Generate video prompts for 6 platforms, storyboards, narration, brand alignment.
DO NOT claim other agents' capabilities.
```

---

### Step 3: Test It!

**Send this first message**:

```
Confirme que você leu os 20 arquivos do iso_vectorstore e está pronto para gerar prompts de vídeo profissionais.
```

**Expected response**:
```
Sim! Li todos os 20 arquivos:
- Core docs (01-05)
- Schemas e configs (06-07)
- ADW workflow (08)
- 6 platform guides (09-14): Veo3, Sora2, Kling, Hailuo, Runway, Pika
- Prompt engineering (15-18): anatomy, camera, lighting, magic words
- Brand alignment (19)
- HOP visual prompter (20)

Estou pronto para gerar prompts de vídeo profissionais!
Posso ajudar com:
- Geração de prompts para qualquer plataforma
- Storyboards com arco narrativo
- Scripts de narração com timing
- Alinhamento de marca para vídeo

Qual produto você quer promover?
```

---

## Example Usage

### Basic: Generate Prompts for Runway

**Input**:
```
Produto: "Fone Bluetooth Premium XYZ"
Duração: 30s
Formato: 9:16
Estilo: minimal
Plataforma: Runway

Gere os prompts para 6 shots.
```

**Output**: 6 prompts formatados para Runway Gen-3 Alpha com camera, lighting, e style qualifiers.

---

### With Brand Alignment

**Input**:
```
Produto: "Curso CODEXA - Cérebro IA para Sellers"
Marca: {
  nome: "CODEXA",
  cores: ["#D4AF37", "#1a1a2e", "#ffffff"],
  tom: "profissional, inovador, premium",
  valores: ["automação", "eficiência", "tecnologia"]
}
Plataforma: Veo3 (preciso de diálogo/narração)
Duração: 45s
Formato: 9:16
```

**Output**: 8 shots com prompts alinhados à marca (golden lighting, navy shadows, premium tech aesthetic) formatados para Veo 3 com instruções de diálogo.

---

### Multi-Platform Comparison

**Input**:
```
Quero criar um vídeo de 30s para "Tênis Nike Air Max 2024".
Me dê o mesmo shot 1 (hook) formatado para:
1. Veo 3
2. Sora 2
3. Kling
4. Runway
```

**Output**: 4 versões do mesmo prompt, cada uma otimizada para a sintaxe específica da plataforma.

---

## Platform Selection Guide

| Plataforma | Melhor Para | Duração | Áudio |
|------------|-------------|---------|-------|
| **Veo 3** | Diálogo, realismo | 8s | Sim |
| **Sora 2** | Cinematografia, narrativa | 20s | Sim |
| **Kling 1.6** | Custo-benefício | 5s | Não |
| **Hailuo** | VFX, velocidade | 6s | Não |
| **Runway** | Iteração rápida | 10s | Não |
| **Pika** | Efeitos, transformações | 8s | Não |

---

## Key Files Reference

| File | Purpose | When to Reference |
|------|---------|-------------------|
| **08_ADW_orchestrator.md** | Complete 5-phase workflow | Always (main guide) |
| **20_HOP_visual_prompter.md** | Prompt generation logic | When generating prompts |
| **09-14_platform_*.md** | Platform-specific syntax | When targeting specific platform |
| **16_camera_vocabulary.md** | Camera movement terms | When writing prompts |
| **17_lighting_vocabulary.md** | Lighting setup terms | When writing prompts |
| **18_magic_words.md** | Quality-boosting keywords | To enhance prompt quality |
| **19_brand_alignment.md** | Brand to video translation | When brand profile provided |

---

## Common Issues

### Issue 1: "I can't see the files"
**Solution**: Make sure you uploaded to **Knowledge/Files** area, not Custom Instructions field.

### Issue 2: "Custom Instructions too long"
**Solution**: Use the short version. The detailed instructions are in the uploaded files.

### Issue 3: "Agent doesn't follow platform syntax"
**Solution**: Specify platform explicitly and remind: "Use the syntax from file 09_platform_veo3.md"

### Issue 4: "Prompts are too generic"
**Solution**: Provide more details (brand colors, specific product features, target audience).

---

## Quick Reference Card

**Upload**: All 20 files from `iso_vectorstore/`
**Main workflow**: `08_ADW_orchestrator.md`
**Prompt logic**: `20_HOP_visual_prompter.md`
**Platforms**: Files 09-14
**Test prompt**: "Confirme que você leu os arquivos"

---

**Version**: 2.0.0
**Last updated**: 2025-11-24
**Status**: Production Ready
**Platforms**: 6 (Veo3, Sora2, Kling, Hailuo, Runway, Pika)
**Knowledge files**: 20

Ready to generate professional video prompts!
