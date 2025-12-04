# HOP: YouTube Description Optimizer (ISO Vectorstore Sync)

**Version**: 1.0.0 | **Stage**: 6++ | **Category**: YouTube Optimization

---

## QUICK REFERENCE

### When to Use
- After Title Optimizer (Phase 6+) for complete YouTube metadata
- Standalone via `/youtube-description` command
- When optimizing video descriptions for SEO and engagement

### Input Required
```json
{
  "video_brief": {
    "title_final": "string (from title_optimizer or working)",
    "topic": "string (primary keyword)",
    "target_audience": "string",
    "key_benefit": "string",
    "video_duration": "string (MM:SS or HH:MM:SS)"
  }
}
```

### Output Delivered
- Complete 5-section description
- Above-fold preview (100-150 chars)
- 4D scoring breakdown
- Keyword analysis (density, position)
- Timestamps (if video >= 3min)

---

## 5-SECTION STRUCTURE

| Section | Purpose | Char Limit | Required |
|---------|---------|------------|----------|
| **Hook** | Above-fold scroll-stopper | 100-150 | Yes |
| **Value Prop** | What viewer gets | 150-300 | Yes |
| **Timestamps** | Navigation + watch time | Variable | If >= 3min |
| **Links/CTAs** | Conversions, engagement | 200-400 | Yes |
| **Hashtags** | Discoverability | 50-100 | Yes |

---

## SECTION FORMULAS

### 1. HOOK (Above Fold) - CRITICAL
```
Formula: [Keyword] + [Curiosity/Value Hook] + [Promise]
Limit: 100-150 chars (visible in search)

BANNED OPENINGS:
- "Neste vídeo..."
- "Olá pessoal..."
- "E aí galera..."
```

**Good Examples**:
- "ChatGPT para programação: os 7 prompts que vão revolucionar seu workflow..."
- "Cansei de perder 2 horas por anúncio. Descobri um método que cria 22 em 18 minutos."

### 2. VALUE PROPOSITION
```
📌 O QUE VOCÊ VAI APRENDER:
• [Benefit 1]
• [Benefit 2]
• [Benefit 3]

👤 PARA QUEM É:
• [Audience descriptor]
```

### 3. TIMESTAMPS
```
Requirements:
- First MUST be 00:00
- Minimum 3 chapters
- Max 50 chars per title
- Ascending order

⏱️ CAPÍTULOS:
00:00 - Introdução
01:45 - [Chapter 2]
03:22 - [Chapter 3]
```

### 4. LINKS & CTAs
```
🔗 RECURSOS:
• [Resource]: [URL]

📱 ME SIGA:
• Instagram: [URL]

🔔 Inscreva-se e ative o sininho!
```

### 5. HASHTAGS & KEYWORDS
```
[Natural keyword sentence]

#Tag1 #Tag2 #Tag3 #Tag4 #Tag5

Rules: 3-5 hashtags (1 broad + 2-3 specific + 1 branded)
```

---

## 4D SCORING SYSTEM

```
Total Score = (Engagement × 0.35) + (SEO × 0.30) + (Brand × 0.20) + (Technical × 0.15)
```

### Dimension Breakdown

| Dimension | Weight | Key Factors |
|-----------|--------|-------------|
| Engagement | 35% | Hook quality, CTA effectiveness, scanability |
| SEO Alignment | 30% | Keyword in first 25 words, density 1-3% |
| Brand Alignment | 20% | Tone consistency with title, voice markers |
| Technical | 15% | Under 5000 chars, proper formatting |

### Thresholds
- **Excellent**: >= 9.0
- **Good**: >= 7.5 (minimum recommend)
- **Acceptable**: >= 6.5
- **Reject**: < 6.5

---

## 3-PHASE WORKFLOW

```
PHASE 1: RESEARCH (~10s)
├── Extract primary keyword from topic
├── Parse video_duration for timestamp decision
├── Load title_optimizer keywords for consistency
├── Determine content_strategy (length, template)
└── Output: research_summary + content_strategy

PHASE 2: GENERATE (~15s)
├── Create Hook (above-fold)
├── Create Value Proposition
├── Create Timestamps (if >= 3min)
├── Create Links & CTAs
├── Create Hashtags & Keywords
└── Output: 5-section description

PHASE 3: VALIDATE (~10s)
├── Score each dimension (4D system)
├── Check quality gate (>= 7.5)
├── Verify keyword density (1-3%)
├── Generate optimization notes
└── Output: description_scored + preview
```

---

## CHARACTER LIMITS

| Element | Limit |
|---------|-------|
| Total | 5000 chars max |
| Above-fold | 100-150 chars |
| Recommended | 500-1500 chars |
| Hook | 150 chars max |
| Value Prop | 300 chars max |
| Hashtags | 3-5 tags |

---

## LENGTH GUIDELINES

| Video Duration | Description Length | Timestamps |
|----------------|-------------------|------------|
| < 5 min | 300-500 chars | No |
| 5-15 min | 500-1000 chars | Yes |
| 15-60 min | 1000-2000 chars | Yes (detailed) |
| 60+ min | 1500-2500 chars | Yes (comprehensive) |

---

## KEYWORD RULES

| Rule | Value |
|------|-------|
| Primary keyword position | First 25 words |
| Keyword density | 1-3% |
| Max occurrences | 5 |
| Integration style | Natural, not stuffing |

---

## BANNED PATTERNS

### Keyword Issues
- Stuffing (same keyword 5+ times)
- Unnatural repetition
- Keyword lists instead of sentences

### Formatting Issues
- Wall of text (500+ chars no sections)
- Excessive CAPS (> 2 words)
- More than 10 links (spam)

### Content Issues
- Fake urgency ("LAST CHANCE" without deadline)
- Empty promises ("garantido", "impossível falhar")
- Generic openings ("Neste vídeo...")

---

## POWER PHRASES (PT-BR)

### Hooks
- "Você já se perguntou..."
- "O segredo que ninguém conta..."
- "Pare de fazer isso errado..."
- "Depois de testar 50+ opções..."

### CTAs
- "Se esse vídeo te ajudou, deixa o like!"
- "Inscreva-se para mais conteúdo como esse"
- "Me conta nos comentários..."

### Value Intros
- "Neste vídeo você vai descobrir..."
- "O que você vai aprender:"
- "Prepare-se para aprender..."

---

## INTEGRATION MODES

### Mode 1: Pipeline (Post Title Optimizer)
```
Title Optimizer → Description Optimizer → youtube_description added to output
```

### Mode 2: Standalone
```
/youtube-description "title, topic, duration, audience" → description.json
```

---

## EXAMPLE OUTPUT

```json
{
  "description_full": "ChatGPT para programação: os 7 prompts que vão...",
  "char_count": 847,
  "scores": {
    "engagement": 8.5,
    "seo": 8.2,
    "brand": 7.8,
    "technical": 9.0
  },
  "score_total": 8.35,
  "preview": {
    "above_fold": "ChatGPT para programação: os 7 prompts que vão revolucionar seu workflow...",
    "char_count": 142
  },
  "keyword_analysis": {
    "primary": "ChatGPT programação",
    "density": "2.1%",
    "first_position": 0
  }
}
```

---

## FILES REFERENCE

| File | Location | Purpose |
|------|----------|---------|
| HOP | `prompts/61_description_optimizer_HOP.md` | Core prompt |
| ADW | `workflows/104_ADW_YOUTUBE_DESCRIPTION.md` | Workflow documentation |
| Config | `config/youtube_description_rules.json` | Formulas + thresholds |
| Schema | `schemas/description_optimizer_input.json` | Input validation |

---

## CHAIN WITH TITLE OPTIMIZER

```
video_brief
    ↓
60_title_optimizer → $youtube_titles
    ↓
61_description_optimizer → $youtube_description
    ↓
YouTube Upload (both title + description ready)
```

---

**Source**: `prompts/61_description_optimizer_HOP.md`
**Synced**: 2025-12-04
**Quality Score**: 9.0/10 (production-ready)
**Predecessor**: `18_HOP_title_optimizer.md`
