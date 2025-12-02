# 📖 HOW TO USE photo_agent - Quick Setup Guide

> **TL;DR**: Upload all 20 files from `iso_vectorstore/` folder to your LLM platform (Claude Projects, ChatGPT, etc.) + paste the Custom Instructions below.

---

## 🚀 3-Step Setup

### Step 1: Upload Files (Knowledge Base)

**Navigate to**:
```
photo_agent/iso_vectorstore/
```

**Upload ALL 20 files** to your LLM platform's Knowledge/Files area:
- Claude Projects → "Add Content" → "Upload Files"
- ChatGPT → "Configure" → "Upload Files"
- Other platforms → Knowledge Base / Files section

**Files to upload** (just select all 20):
```
01_ROOT_PRIME.md
02_ROOT_README.md
03_CODEXA_PRIME.md
04_CODEXA_README.md
05_CODEXA_INSTRUCTIONS.md
06_HOP_FRAMEWORK.md
07_photo_agent_PRIME.md
08_photo_agent_INSTRUCTIONS.md
09_photo_agent_README.md
10_photo_agent_SETUP.md
11_photo_input_schema.json
12_photo_marketplace_output.json
13_photo_brand_output.json
14_photo_camera_profiles.json
15_photo_photography_styles.json
16_photo_pnl_triggers.json
17_photo_schemas_guide.md
18_AGENT_REGISTRY.json
19_DOCUMENTATION_INDEX.md
20_photo_agent_CHANGELOG.md
```

**Tip**: Use Ctrl+A (Select All) → Drag & Drop! 🖱️

---

### Step 2: Custom Instructions (Copy & Paste)

**Copy this** into the "Custom Instructions" field:

```markdown
You are photo_agent, a specialized photography prompt generator.

SCOPE DEFINITION:
- Files 01-06 are SYSTEM CONTEXT ONLY (describing the larger CODEXA system)
- Files 07-10 are YOUR CORE (photo_agent only)
- Files 11-17 are YOUR TOOLS (photo_agent specific)
- Files 18-20 are SHARED RESOURCES

YOUR CAPABILITIES (photo_agent only):
- Professional photography prompt generation (Midjourney, DALL-E, Stable Diffusion)
- 9-scene storytelling workflows
- Camera/lighting/composition technical direction
- PNL emotional triggers integration
- Brand photography (color consistency, mood alignment)
- Marketplace photography (compliance for ML, Amazon, Shopee)

DO NOT claim capabilities from other agents (anuncio, marca, mentor, pesquisa, codexa).

WORKFLOW SOURCE: 08_photo_agent_INSTRUCTIONS.md (read this as your main operational guide)
```

**Character count**: ~850 chars (may need shortening for some platforms)

---

### Step 2b: Shorter Version (If Character Limit is Tight)

**Use this if the platform has a strict character limit**:

```markdown
You are photo_agent - ONLY a photography prompt generator.

Files 01-06 = context about other systems (IGNORE their capabilities)
Files 07-10 = YOUR core (read 07_photo_agent_PRIME.md + 08_photo_agent_INSTRUCTIONS.md)
Files 11-17 = YOUR tools (schemas, configs, guides)

YOUR ONLY CAPABILITIES:
- Generate professional photography prompts (Midjourney/DALL-E/SD)
- 9-scene workflows with camera/lighting/composition specs
- PNL emotional triggers
- Brand photography + Marketplace compliance

Follow workflows in 08_photo_agent_INSTRUCTIONS.md. Do NOT claim other agents' capabilities.
```

**Character count**: ~560 chars ✅

---

### Step 3: Test It!

**Send this first message**:

```
Olá! Confirme que você leu todos os 20 arquivos do iso_vectorstore e está pronto para gerar prompts fotográficos profissionais.
```

**Expected response**:
```
✅ Sim! Li todos os 20 arquivos:
- System context (01-06)
- photo_agent core (07-10)
- Schemas e configs (11-17)
- Shared resources (18-20)

Estou pronto para gerar prompts fotográficos profissionais!
Posso ajudar com:
- Geração de 9 cenas (standard workflow)
- Workflow de marca (brand integration)
- Workflow de marketplace (compliance)
...
```

---

## 📝 Example Usage

### Simple Product Photography (9 Scenes)

**Input**:
```
Gere 9 cenas fotográficas para: "Garrafa de água de vidro premium"
Estilo: editorial
Output: grid_3x3
```

**Output**: 9 prompts profissionais com composição, iluminação, camera settings, e PNL triggers.

---

### Brand Photography with Custom Colors

**Input**:
```
Subject: "Tênis esportivo"
Style: lifestyle
Brand: {
  "colors": ["#FF6B35", "#004E89"],
  "mood": "energetic",
  "target_audience": "atletas urbanos 25-35"
}
Scenes: 9
```

**Output**: 9 prompts com cores da marca integradas, mood consistente, e target audience alignment.

---

### Marketplace Compliance (Mercado Livre)

**Input**:
```
Produto: "Fone de ouvido Bluetooth"
Marketplace: mercado_livre
Scenes: 6
```

**Output**: 6 prompts otimizados para Mercado Livre (background branco, sem texto, sem logos de terceiros, resolution requirements).

---

## 🔍 Key Files Reference

| File | Purpose | When to Reference |
|------|---------|-------------------|
| **08_photo_agent_INSTRUCTIONS.md** | Complete workflows | Always (main guide) |
| **07_photo_agent_PRIME.md** | Philosophy & principles | First read |
| **14_photo_camera_profiles.json** | Camera settings | Scene generation |
| **15_photo_photography_styles.json** | Style presets | Style selection |
| **16_photo_pnl_triggers.json** | Emotional triggers | PNL integration |
| **11_photo_input_schema.json** | Input validation | Input structure |
| **12_photo_marketplace_output.json** | Marketplace schemas | Marketplace workflows |
| **13_photo_brand_output.json** | Brand schemas | Brand workflows |

---

## ⚠️ Common Issues

### Issue 1: "I can't see the files"
**Solution**: Make sure you uploaded to **Knowledge/Files** area, not Custom Instructions field.

### Issue 2: "Custom Instructions too long"
**Solution**: Use the short version (see Step 2). The detailed instructions are in the uploaded files.

### Issue 3: "Agent doesn't follow workflows"
**Solution**: Remind it: "Follow the workflows in 08_photo_agent_INSTRUCTIONS.md step by step."

---

## 🎯 Quick Reference Card (Bookmark This!)

**Upload**: All 20 files from `iso_vectorstore/`
**Instructions**: See Step 2 above
**Main file**: `08_photo_agent_INSTRUCTIONS.md`
**Test prompt**: "Confirme que você leu os arquivos e está pronto"

---

## 📚 Need More Help?

- Read `09_photo_agent_README.md` (uploaded) for detailed capabilities
- Check `17_photo_schemas_guide.md` (uploaded) for schema documentation
- Review `08_photo_agent_INSTRUCTIONS.md` (uploaded) for complete workflows

---

**Version**: 1.0.0
**Last updated**: 2025-11-15
**Status**: ✅ Production Ready

🚀 **You're ready to go! Happy prompting!**
