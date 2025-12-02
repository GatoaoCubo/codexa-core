# photo_agent

**Version**: 1.0.0
**Type**: Specialized Photography AI Agent
**Status**: Production Ready

## Overview

`photo_agent` is a specialized agent for professional AI image generation using advanced photography techniques, scene composition, lighting design, and programação neurolinguística (PNL). It transforms any subject (products, people, scenes, concepts) into professionally-directed photography prompts for AI image generators.

## Architecture: Dual-Layer Integration (v2.0.0)

`photo_agent` implements a professional **Dual-Layer Architecture** combining orchestration with detailed execution:

### Layer 1: ADW (Agentic Developer Workflow)
- **File**: `workflows/100_ADW_RUN_PHOTO.md` (v2.0.0)
- **Purpose**: High-level workflow orchestration (WHAT to do, WHEN to do it)
- **Structure**: 5-phase workflow with clear objectives, inputs, outputs, and validations
- **Duration**: 15-30 minutes end-to-end

### Layer 2: HOP (Higher-Order Prompts)
- **Location**: `prompts/` directory (5 modular prompts)
- **Purpose**: Detailed step-by-step execution instructions (HOW to do it)
- **Content**: Comprehensive guides with examples, error handling, and validation checklists
- **Total Size**: ~50KB of specialized photography knowledge

### Workflow Phases → HOP Mapping

| Phase | Workflow Step | HOP Prompt | Output |
|-------|--------------|------------|--------|
| 1 | Input Processing & Scene Planning | `10_scene_planner_HOP.md` | 9-scene grid (3x3) |
| 2 | Camera & Lighting Design | `20_camera_designer_HOP.md` | Camera specs + lighting |
| 3 | Prompt Generation (Scenes 1-9) | `30_prompt_generator_HOP.md` | 9 AI prompts (≥80 words) |
| 4 | Brand & Compliance Validation | `40_brand_validator_HOP.md` | Quality score ≥7.0/10 |
| 5 | Batch Assembly & QA | `50_batch_assembler_HOP.md` | Trinity output (.md/.json) |

### Benefits
- **Modularity**: Each HOP prompt is independently updatable
- **Clarity**: Separation between workflow logic (ADW) and execution details (HOP)
- **Reusability**: HOP prompts can be used standalone or in custom workflows
- **Scalability**: Easy to extend with new phases or modify existing ones

### Quick Start with Dual-Layer
```bash
# For AI Assistants: Execute complete workflow
READ: agentes/photo_agent/workflows/100_ADW_RUN_PHOTO.md

# For specific phase details:
READ: agentes/photo_agent/prompts/30_prompt_generator_HOP.md  # Phase 3 example
```

## Key Capabilities

### 1. Photography Technical Mastery
- **Camera Simulation**: Focal lengths (24mm-100mm), aperture control (f/2.8-f/8), shutter speeds, ISO ranges
- **Lighting Design**: 3-point lighting, classic setups (Rembrandt, Butterfly, Loop), natural light (golden hour), studio configurations (high-key, low-key)
- **Optics Quality**: 8K resolution, color space management (sRGB), white balance control, ETTR exposure, microcontrast

### 2. Composition Theory
- Classic rules: Rule of thirds, golden ratio (1.618), golden triangle, dynamic symmetry
- Advanced techniques: Leading lines, framing, negative space, visual hierarchy, depth layers

### 3. Photography Style Presets
- **Minimalist**: Clean backgrounds, soft lighting, muted colors, negative space
- **Dramatic**: Low-key lighting, high contrast, bold compositions, atmospheric effects
- **Lifestyle**: Natural light, contextual environments, warm tones, shallow DOF
- **Editorial**: Controlled studio lighting, magazine-quality composition, neutral grading
- **Commercial**: Product focus, high-key lighting, brand integration, marketplace compliant

### 4. Programação Neurolinguística (PNL)
- 10+ emotional triggers (confiança, conforto, clareza, calma, desejo, urgência)
- Visual storytelling arcs (establish → problem → solution → proof → transformation)
- Psychological anchors embedded in scene descriptions

### 5. Brand Visual Identity Integration
- Color palette enforcement (hex codes)
- Mood/tone consistency (professional, playful, luxury, minimal)
- Target audience alignment
- Logo placement rules (optional)

## Quick Start

### Basic Usage

```markdown
**Input:**
- Subject: "Luxury leather handbag with gold hardware"
- Style: "editorial"
- Scenes: 9
- Output: "grid_3x3"

**Output:**
9 professional photography prompts ready for Midjourney/DALL-E 3/Stable Diffusion
```

### Advanced Usage with Brand Profile

```json
{
  "subject": "Minimalist ceramic vase",
  "style": "minimalist",
  "scenes": 9,
  "brand_profile": {
    "colors": ["#F5F5DC", "#8B7355", "#FFFFFF"],
    "mood": "serene zen aesthetic",
    "target_audience": "interior design enthusiasts"
  },
  "pnl_triggers": ["calma", "clareza", "pertencimento"],
  "ai_model": "midjourney",
  "output_format": "grid_3x3"
}
```

## Input Schema

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `subject` | string | Yes | Main subject to photograph |
| `style` | enum | No | Photography style preset (default: editorial) |
| `scenes` | integer | No | Number of scenes 1-9 (default: 9) |
| `brand_profile` | object | No | Brand visual identity settings |
| `pnl_triggers` | array | No | Emotional anchors to embed |
| `technical_overrides` | object | No | Manual camera/lighting overrides |
| `ai_model` | enum | No | Target AI model (default: midjourney) |
| `output_format` | enum | No | Grid or sequential (default: grid_3x3) |

## Output Format

### Trinity Output Pattern
- **Markdown (.md)**: Human-readable prompts with metadata
- **LLM JSON (.llm.json)**: Structured data for AI consumption
- **Meta JSON (.meta.json)**: Validation report and quality metrics

### Sample Output Structure
```markdown
# Photo Prompts: [Subject]

## Scene 1: Hero White Background
**Camera**: 50mm f/8 1/160s ISO 100
**Lighting**: High-key clean, soft uniform shadows
**Composition**: Centered, rule of thirds
**PNL**: "clareza que valida sua escolha"

**Prompt**: "Professional editorial photography, [subject], pure white background..."

[... 8 more scenes ...]

## Quality Report
- Total Prompts: 9
- Average Validation Score: 0.92
- Compliance: PASS (11/11 checks)
```

## Photography Styles Guide

### Minimalist
- **Background**: White, light gray, soft pastels
- **Lighting**: Soft even, no harsh shadows
- **Composition**: Centered, rule of thirds, negative space
- **Color**: Muted, desaturated, monochromatic
- **Best for**: Skincare, home decor, stationery, minimal tech

### Dramatic
- **Background**: Dark, textured, atmospheric
- **Lighting**: Low-key, strong shadows, high contrast
- **Composition**: Diagonal, asymmetric, bold
- **Color**: Rich saturated, cinematic grading
- **Best for**: Luxury goods, automotive, fashion, spirits

### Lifestyle
- **Background**: Real-world contexts (homes, cafes, outdoors)
- **Lighting**: Natural light, golden hour, window light
- **Composition**: Candid, authentic moments
- **Color**: Warm tones (2800-4000K)
- **Best for**: Consumer products, food, wellness, apparel

### Editorial
- **Background**: Studio or controlled environments
- **Lighting**: Precision 3-point lighting
- **Composition**: Magazine-quality balanced
- **Color**: Neutral, accurate representation
- **Best for**: Fashion editorials, beauty, professional gear

### Commercial
- **Background**: White (#FFFFFF) or brand colors
- **Lighting**: High-key bright, optimistic
- **Composition**: Product hero 80-90% frame
- **Color**: Brand palette integration
- **Best for**: E-commerce, marketplace listings, ads

## Camera & Lighting Profiles

### Camera Settings by Scene Type
| Scene Type | Focal Length | Aperture | Shutter | ISO | DOF |
|------------|--------------|----------|---------|-----|-----|
| Hero Product | 50mm | f/8 | 1/160s | 100 | Full focus |
| Lifestyle | 85mm | f/4 | 1/160s | 400 | Shallow |
| Macro Detail | 100mm | f/2.8 | 1/160s | 100 | Ultra shallow |
| Editorial | 85mm | f/5.6 | 1/160s | 100 | Moderate |
| Top-down | 50mm | f/8 | 1/160s | 100 | Full focus |

### Lighting Setups
- **High-key**: Bright even lighting, minimal shadows, white background
- **Low-key**: Dramatic shadows, dark background, selective lighting
- **3-Point Classic**: Key (45°), Fill (-1EV), Rim (back separation)
- **Rembrandt**: 45° key light creating triangle on cheek
- **Natural Golden Hour**: 5500K warm, soft directional, long shadows

## Validation & Compliance

### 11-Point Quality Checklist
1. Length: 80-350 characters
2. Camera specified (focal + aperture)
3. Lighting described (type + direction)
4. Background mentioned
5. Composition defined
6. Resolution stated ("8K high quality")
7. Contains "no watermarks"
8. Contains "no text overlay"
9. Contains "no third-party logos"
10. PNL trigger included
11. No impossible AI instructions

### Compliance Modes
- **Marketplace**: Enforces white background for scenes 1 & 9 (Amazon/ML/Shopee)
- **Artistic**: Flexible backgrounds, creative freedom
- **Brand**: Brand guideline compliance (colors, mood, style)

## Use Cases

### E-commerce Product Photography
Generate 9-scene grids for marketplace listings with lifestyle context and white background compliance.

### Brand Campaign Assets
Create cohesive visual campaigns with consistent brand identity across multiple scenes.

### Social Media Content
Generate carousel-ready images with emotional storytelling arcs.

### Editorial Photography
Produce magazine-quality compositions with professional lighting and composition.

### Concept Visualization
Transform abstract concepts into visual metaphors using advanced composition theory.

## Advanced Features

### Intentional Gaps Strategy
The agent deliberately leaves secondary elements unspecified (exact prop placement, minor angle variations, background texture details) to allow AI model creativity while maintaining technical control.

### PNL Emotional Triggers
Embeds psychological anchors like "superfície que convida ao toque" (surface that invites touch) to influence viewer perception and emotional response.

### Multi-Scene Orchestration
Coordinates 1-9 scenes with narrative flow: establish context → show benefit → prove quality → deliver transformation.

### Brand Lock Instruction
Every prompt includes "brand/style lock to [subject]" ensuring visual consistency across all generated scenes.

## Architecture

### Modular HOP Structure
```
photo_agent/
├── prompts/
│   └── 60_prompt_generator.md    # Main HOP (adapted from anuncio_agent)
├── config/
│   ├── photography_styles.json   # 5+ style presets
│   ├── camera_profiles.json      # Camera technical specs
│   └── pnl_triggers.json          # Emotional triggers
└── schemas/
    ├── photo_input.json                  # Input validation
    ├── photo_output.json                 # Generic output structure
    ├── photo_marketplace_output.json     # 🆕 Marketplace workflow (anuncio_agent)
    └── photo_brand_output.json           # 🆕 Brand social media (marca_agent)
```

### Standalone Operation
- No dependencies on other agents (except codexa_agent meta-framework)
- Self-contained configuration files
- Independent validation and quality gates

## 🆕 Dual Output Schemas (2025-11-15)

### Overview
Photo agent now supports **2 specialized output workflows**:

1. **Marketplace Output** (`photo_marketplace_output.json`) - Integration with `anuncio_agent`
2. **Brand Social Media Output** (`photo_brand_output.json`) - Integration with `marca_agent`

### Key Differences

| Feature | Marketplace Schema | Brand Social Media Schema |
|---------|-------------------|---------------------------|
| **Purpose** | Product listings (ML, Shopee, Amazon, Magalu) | Brand social content (Instagram, TikTok, Pinterest) |
| **White BG Compliance** | ✅ **MANDATORY** Scenes 1 + 9 = #FFFFFF | ❌ NO compliance, creative backgrounds OK |
| **Reference Image** | Inline `{INSERIR_IMAGEM_PRODUTO_AQUI}` placeholder | Optional inline placeholder |
| **Aspect Ratios** | Fixed 1:1 (grid) or sequential | Variable: 1:1, 4:5, 9:16, 16:9, 2:3 |
| **Brand Integration** | Basic (colors optional) | **DEEP** - Reads `brand_strategy.md` |
| **PNL Triggers** | Generic emotional anchors | **Aligned to brand archetype** (Hero, Sage, etc.) |
| **Integration Agent** | `anuncio_agent` (ad copy generation) | `marca_agent` (brand strategy) |
| **Validation Target** | ≥0.90 (strict marketplace compliance) | ≥0.85 (brand consistency) |
| **Primary Use Case** | E-commerce product photography | Social media brand campaigns |
| **Compliance Checks** | 13-point checklist (scenes 1+9 white, no logos, etc.) | 11-point brand alignment (colors, mood, archetype) |
| **Output Files** | `.md`, `.llm.json`, `.meta.json` (Trinity) | `.md`, `.llm.json`, `.meta.json` (Trinity) |

### Workflow Selection Guide

**Use MARKETPLACE schema when:**
- Creating product photos for marketplace listings (ML, Shopee, Amazon BR, Magalu)
- Need compliance with marketplace image policies (white background scenes 1+9)
- Integrating with `anuncio_agent` for complete ad generation
- Reference image fidelity is CRITICAL (product must look identical across scenes)
- Target: conversion-optimized product photography

**Use BRAND SOCIAL MEDIA schema when:**
- Creating social media content (Instagram, Facebook, TikTok, Pinterest)
- Have existing `brand_strategy.md` from `marca_agent`
- Need brand consistency (colors, mood, archetype personality)
- Want varied aspect ratios (feed 1:1, stories 9:16, reels)
- PNL triggers must align with brand archetype (Hero = courage, Caregiver = comfort)
- Target: brand awareness and engagement

### Example Usage

**Marketplace Workflow:**
```bash
# 1. User provides product image + subject
Input: "Garrafa de água 750ml aço inox" + product_image.png

# 2. Photo agent generates 9 prompts (marketplace schema)
Output: 9 prompts, scenes 1+9 with #FFFFFF background
        Each prompt has {INSERIR_IMAGEM_PRODUTO_AQUI} placeholder

# 3. User copies prompt, pastes product image, generates in LLM
# 4. Repeat 9x for complete grid

# 5. Use generated images in anuncio_agent for ad copy
```

**Brand Social Media Workflow:**
```bash
# 1. User has brand_strategy.md from marca_agent
Brand: HeroWater (archetype: Hero, colors: #FF5722, #212121)

# 2. Photo agent reads brand_strategy.md
# 3. Generates 9 prompts aligned with brand identity
Output: Scenes with brand colors, Hero archetype mood (energetic, bold)
        PNL triggers: "coragem que prova valor" (aligned to Hero)
        Aspect ratios: 4:5 (feed), 9:16 (stories), 1:1 (carousel)

# 4. User generates images for Instagram/TikTok campaign
```

### Schema Documentation

**Full Schema Specs:**
- `photo_marketplace_output.json` - 650 lines, 13-point compliance validation
- `photo_brand_output.json` - 750 lines, 11-point brand alignment validation

**Key Fields:**
- **Marketplace**: `reference_instructions`, `marketplace_compliance`, `anuncio_integration`
- **Brand**: `brand_integration`, `social_media_specs`, `archetype_pnl_mapping`

---

## Differences from anuncio_agent

| Feature | anuncio_agent | photo_agent |
|---------|---------------|-------------|
| **Focus** | E-commerce ads | Pure photography artistry |
| **Compliance** | Marketplace required | Optional/customizable |
| **Styles** | Commercial only | 5+ presets (min, drama, life, edit, comm) |
| **Subjects** | Products only | Any subject (products, people, scenes) |
| **Brand** | Implicit briefing | Explicit brand profile system |
| **Autonomy** | Embedded workflow | Standalone agent |

## Performance Targets

- **Prompt Generation**: <10s for 9 prompts
- **Validation**: <5s for 9 prompts
- **Total Pipeline**: <20s complete workflow
- **Quality Score**: ≥0.85 average validation score

## Getting Started

### 1. Review Documentation
- Read `PRIME.md` for AI assistant entry point
- Review `INSTRUCTIONS.md` for operational details
- Check `SETUP.md` for configuration options

### 2. Configure Preferences
- Select photography style preset or customize
- Define brand profile (optional)
- Choose PNL triggers for emotional tone

### 3. Generate Prompts
- Provide subject description
- Run generation workflow
- Receive 9 copy-paste ready prompts

### 4. Use with AI Image Generators
- **Midjourney**: Paste prompt + `--ar 1:1 --q 2`
- **DALL-E 3**: Paste prompt directly
- **Stable Diffusion**: Paste prompt + adjust sampling
- **Imagen**: Paste prompt + safety settings

## Support & Resources

- **Design Spec**: `workflows/ADW_photo_agent_design.md`
- **Source Knowledge**: `anuncio_agent/prompts/60_image_prompts.md`
- **Configuration Files**: `config/` directory
- **Schemas**: `schemas/` for input/output contracts

## Self-Containment & Isolation

### Standalone Operation
`photo_agent` is **100% self-contained** and designed for isolated operation in Agent builders or LLM knowledge bases.

**Zero External Dependencies**:
- All code uses only Python standard library (json, pathlib, datetime, hashlib, argparse, sys, re)
- No pip install required
- No API keys needed
- No database connections
- Configuration uses hardcoded fallbacks (config files optional)

**Embedded Knowledge**:
- Photography theory embedded in code defaults
- Camera profiles, lighting setups, PNL triggers all hardcoded
- Schemas define complete input/output contracts
- No external file dependencies for core operation

### Essential Files for Agent Builder

**Core Execution** (3 files):
```
photo_agent.py          # CLI entry point (350 lines)
processor.py            # Prompt generation logic (700+ lines)
trinity_writer.py       # Output writer (300+ lines)
```

**Validation** (3 files):
```
validators/
  marketplace_validator.py  # 13-point checklist (350 lines)
  brand_validator.py        # 11-point checklist (350 lines)
  schema_validator.py       # JSON schema validation (200 lines)
```

**Schemas** (5 files):
```
schemas/
  photo_marketplace_output.json  # Marketplace schema (709 lines)
  photo_brand_output.json        # Brand schema (989 lines)
  photo_input.json               # Input validation
  photo_output.json              # Generic output
  SCHEMAS_GUIDE.md               # Technical guide (400+ lines)
```

**Documentation** (4 files):
```
README.md           # This file - Overview & capabilities
PRIME.md            # AI assistant entry point (TAC-7 format)
INSTRUCTIONS.md     # Operational workflows (696 lines)
SETUP.md            # Configuration guide (726 lines)
```

**Command Documentation** (2 files):
```
commands/
  photo_marketplace.md  # /photo_marketplace slash command
  photo_brand.md        # /photo_brand slash command
```

**Examples** (6 files):
```
examples/
  marketplace_garrafa_agua.md         # Human-readable example
  marketplace_garrafa_agua.llm.json   # LLM-consumable example
  marketplace_garrafa_agua.meta.json  # Metadata example
  brand_hero_water.md                 # Brand example
  brand_hero_water.llm.json           # Brand LLM example
  brand_hero_water.meta.json          # Brand metadata
```

**Optional Config** (3 files - uses defaults if missing):
```
config/
  photography_styles.json  # Style presets (optional)
  camera_profiles.json     # Camera specs (optional)
  pnl_triggers.json        # Emotional triggers (optional)
```

**Total**: 26 files, ~3,500+ lines of code, 0 external dependencies

### Usage in Agent Builder

1. **Copy all files** to Agent Builder knowledge base
2. **Point to PRIME.md** as entry point for AI assistant
3. **Reference README.md** for user-facing documentation
4. **Use schemas/*.json** for structured input/output validation
5. **Execute via CLI**: `python photo_agent.py --workflow [marketplace|brand] --subject "..." --output "..."`

---

## Version History

- **1.0.0** (2025-11-14): Initial release with 5 photography styles, 9-scene orchestration, PNL triggers, brand profile system
- **1.1.0** (2025-11-15): Dual output schemas (marketplace + brand), validators, examples, self-contained operation

---

**License**: MIT
**Maintained by**: CODEXA Meta-Construction Framework
**Contact**: See `PRIME.md` for AI assistant interaction guidelines
