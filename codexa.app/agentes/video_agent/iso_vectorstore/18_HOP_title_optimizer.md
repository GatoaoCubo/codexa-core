# HOP: YouTube Title Optimizer (ISO Vectorstore Sync)

**Version**: 1.0.0 | **Stage**: 6+ | **Category**: YouTube Optimization

---

## QUICK REFERENCE

### When to Use
- After Phase 5 (editor_assembler) for YouTube uploads
- Standalone via `/youtube-title` command
- When optimizing video titles for CTR

### Input Required
```json
{
  "video_brief": {
    "title_working": "string (5-100 chars)",
    "topic": "string (primary keyword)",
    "target_audience": "string",
    "key_benefit": "string"
  }
}
```

### Output Delivered
- 5 title candidates (one per psychological angle)
- Recommended winner with rationale
- 4D scoring breakdown
- A/B test suggestions

---

## 5 PSYCHOLOGICAL ANGLES

| ID | Angle | Formula | CTR Multiplier |
|----|-------|---------|----------------|
| A | Question | `[Keyword] + [Question]?` | 1.25x |
| B | Number | `[N] + [Benefit] + [Keyword]` | **1.36x** ⭐ |
| C | Social Proof | `[Keyword] + [Transformation]` | 1.18x |
| D | How-To | `Como + [Action] + [Keyword]` | 1.22x |
| E | Comparison | `[A] vs [B] + [Decision]` | 1.30x |

**Best Numbers**: 3, 5, 7, 10, 15, 21 (odd outperform even)

---

## 4D SCORING SYSTEM

```
Total Score = (CTR × 0.35) + (SEO × 0.30) + (Brand × 0.20) + (Technical × 0.15)
```

### Dimension Breakdown

| Dimension | Weight | Key Factors |
|-----------|--------|-------------|
| CTR Prediction | 35% | Angle multiplier, power words, curiosity gap |
| SEO Alignment | 30% | Keyword presence, position ≤40 chars |
| Brand Alignment | 20% | Tone match, voice markers |
| Technical | 15% | 50-70 chars, no banned patterns |

### Thresholds
- **Excellent**: ≥9.0
- **Good**: ≥7.5 (minimum recommend)
- **Acceptable**: ≥6.5
- **Reject**: <6.5

---

## 3-PHASE WORKFLOW

```
PHASE 1: RESEARCH (~10s)
├── Extract primary keyword from topic
├── Infer audience pain points
├── Map brand tone to title style
└── Output: research_summary

PHASE 2: GENERATE (~15s)
├── Create Title A (Question)
├── Create Title B (Number) ⭐
├── Create Title C (Social Proof)
├── Create Title D (How-To)
├── Create Title E (Comparison)
└── Output: 5 titles_generated

PHASE 3: VALIDATE (~10s)
├── Score each title (4D system)
├── Select highest scorer as recommended
├── Provide alternatives ≥7.0
├── Generate A/B test suggestion
└── Output: titles_scored + recommended
```

---

## CHARACTER RULES

| Rule | Value |
|------|-------|
| Minimum | 50 chars |
| Maximum | 70 chars |
| Optimal | 55-65 chars |
| Keyword position | ≤40 chars from start |
| Mobile preview | First 45 chars must hook |

---

## BANNED PATTERNS

### Formatting
- ALL CAPS titles
- Multiple !!! or ???
- Emojis (unless brand allows)

### Clickbait
- "Você não vai acreditar..."
- Generic superlatives ("O melhor", "Incrível")
- Unverifiable claims ("#1", "Número 1")

### Technical
- Year in evergreen content (unless dated)
- Starting with connector ("De", "Para", "E")

---

## POWER WORDS (PT-BR)

| Category | Words |
|----------|-------|
| Urgency | Agora, Hoje, Rápido, Imediato |
| Exclusivity | Segredo, Revelado, Escondido |
| Transformation | Transforme, Mude, Revolucione |
| Specificity | Exato, Passo a Passo, Comprovado |
| Authority | Especialista, Definitivo, Expert |

---

## INTEGRATION MODES

### Mode 1: Pipeline (Post Phase 5)
```
Phase 5 complete → Title Optimizer → youtube_titles added to output
```

### Mode 2: Standalone
```
/youtube-title "topic, audience, benefit" → titles.json
```

---

## EXAMPLE OUTPUT

```json
{
  "recommended": {
    "text": "7 Prompts de ChatGPT Que Todo Dev Precisa Conhecer",
    "angle": "number",
    "score_total": 8.9,
    "ctr_multiplier": 1.36,
    "rationale": "Number angle (best CTR), strong keyword position"
  },
  "alternatives": [
    {"text": "ChatGPT vs Copilot: Qual Usar Para Programar", "score": 8.6}
  ]
}
```

---

## FILES REFERENCE

| File | Location | Purpose |
|------|----------|---------|
| HOP | `prompts/60_title_optimizer_HOP.md` | Core prompt |
| ADW | `workflows/103_ADW_YOUTUBE_TITLE.md` | Workflow documentation |
| Config | `config/youtube_title_rules.json` | Formulas + thresholds |
| Schema | `schemas/title_optimizer_input.json` | Input validation |

---

**Source**: `prompts/60_title_optimizer_HOP.md`
**Synced**: 2025-12-04
**Quality Score**: 9.0/10 (production-ready)
