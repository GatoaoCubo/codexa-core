# Getting Started with CODEXA

**Time to read**: 5 minutes | **Time to first result**: 10 minutes

---

## What is CODEXA?

CODEXA is a **meta-construction framework** - a system of AI agents that work together to create content for Brazilian e-commerce. Think of it as a team of specialists, each expert in one domain.

**In one sentence**: Tell it what you need, it routes to the right specialist and delivers structured output.

---

## What Can It Do?

| I want to... | Use this | Example |
|--------------|----------|---------|
| Create product listings | `/prime-anuncio` | Titles, bullets, descriptions for Mercado Livre |
| Research competitors | `/prime-pesquisa` | Market analysis, pricing, SEO keywords |
| Build brand strategy | `/prime-marca` | Brand identity, tone of voice, visual guidelines |
| Generate photo prompts | `/prime-photo` | AI photography prompts for Midjourney/DALL-E |
| Create video content | `/prime-video` | Scripts, storyboards, Reels/TikTok |
| Build online courses | `/prime-curso` | Course structure, scripts, sales pages |
| Get mentoring | `/prime-mentor` | Practical guidance for e-commerce sellers |

---

## Your First Task (3 Steps)

### Step 1: Choose What You Need

**Most common starting point**: Research → Listing → Photos

```
/prime-pesquisa    → Get market research
/prime-anuncio     → Create optimized listing
/prime-photo       → Generate photo prompts
```

### Step 2: Provide a Brief

Example brief for product listing:
```
Product: Garrafa de água térmica 500ml
Category: Casa e Jardim > Cozinha
Target: Profissionais home office, 25-45 anos
Price Range: R$ 89 - R$ 129
Marketplace: Mercado Livre
```

### Step 3: Get Your Output

The agent will deliver:
- Structured markdown (human-readable)
- JSON metadata (machine-readable)
- Validation report (quality score)

---

## Navigation Quick Reference

### Commands by Goal

```
CONTENT CREATION:
  /prime-anuncio    Product listings (ML, Shopee, Amazon BR)
  /prime-photo      AI photography prompts
  /prime-video      Video scripts & storyboards
  /prime-curso      Online course content

STRATEGY:
  /prime-pesquisa   Market research & competitor analysis
  /prime-marca      Brand strategy & identity
  /prime-mentor     Practical e-commerce coaching

SYSTEM:
  /prime            System overview & navigation
  /prime-codexa     Build new agents/prompts (advanced)
  /prime-scout      File discovery & navigation
```

### Understanding the Structure

Every agent follows the same pattern:
```
PRIME.md         → What it does, when to use (read first)
INSTRUCTIONS.md  → How to execute step-by-step
README.md        → Full reference & architecture
```

---

## For External LLMs (ChatGPT, Gemini, etc.)

If you're NOT using Claude Code, you can still use CODEXA:

1. **Download an agent's `iso_vectorstore/` folder**
2. **Upload to your LLM** (drag & drop)
3. **Start with**: "Read 01_QUICK_START.md and help me with [task]"

Each `iso_vectorstore/` is self-contained and works with any LLM.

**File reading order**:
```
01_QUICK_START.md    → 5-min orientation
02_PRIME.md          → Agent identity
03_INSTRUCTIONS.md   → Step-by-step workflow
06_input_schema.json → What inputs are needed
07_output_template   → What output looks like
```

---

## Common Questions

**Q: Which agent should I start with?**
A: For product sellers, start with `/prime-pesquisa` (research), then `/prime-anuncio` (listing).

**Q: Can agents work together?**
A: Yes! Common chains:
- `pesquisa → anuncio → photo` (full product content)
- `marca → anuncio` (brand-aligned copy)
- `curso → video` (course content)

**Q: What if I'm not sure where to start?**
A: Type `/prime` for system navigation, or just describe what you need.

**Q: Is this only for Brazilian e-commerce?**
A: The agents are optimized for Brazilian Portuguese and marketplace rules (ANVISA, INMETRO), but the framework works for any domain.

---

## Next Steps

| Your Goal | Next Document |
|-----------|---------------|
| Understand the system deeply | Read `PRIME.md` (15 min) |
| Learn the operating principles | Read `CLAUDE.md` (20 min) |
| Build your own agents | Read `/prime-codexa` (30 min) |
| See agent connections | Read `docs/AGENT_CHAINS.md` |

---

## Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "Which file do I read?" | Always start with `PRIME.md` |
| "Agent doesn't understand" | Provide more context in your brief |
| "Output quality is low" | Check if input matches `input_schema.json` |
| "Can't find a file" | Use `mcp__scout__discover("description")` |

---

**Version**: 1.0.0 | **Language**: English | **See also**: [CLAUDE.md](CLAUDE.md) (for LLMs), [PRIME.md](PRIME.md) (system overview)
