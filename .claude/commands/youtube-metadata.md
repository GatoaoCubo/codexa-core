# /youtube-metadata - Generate Complete YouTube Upload Package

## PURPOSE
Execute the unified YouTube metadata optimizer (ADW-105) to generate a complete upload package in a single run.

**Input**: Video brief (topic, audience, duration)
**Output**: Title + Description + Tags + Thumbnail Text + Chapters

---

## PRE-REQUISITES

Before executing, ensure:
- [ ] Video brief with: topic, target_audience, key_benefit, video_duration
- [ ] Optional: $script from video production (improves chapters)
- [ ] Optional: $brand_profile from marca_agent

---

## INSTRUCTIONS FOR AI ASSISTANTS

### Step 1: Collect Brief

Gather the following from user:

**Required:**
```json
{
  "topic": "Primary keyword/topic",
  "target_audience": "Who is this for?",
  "key_benefit": "Main value proposition",
  "video_duration": "MM:SS (e.g., 15:30)"
}
```

**Optional:**
```json
{
  "title_working": "Current working title",
  "script": {},
  "brand_profile": {},
  "seo_keywords": [],
  "channel_name": "Your channel name"
}
```

### Step 2: Execute Unified Pipeline

Read workflow: `codexa.app/agentes/video_agent/workflows/105_ADW_YOUTUBE_FULL_METADATA.md`

**PHASE 1: TITLE (~30s)** [Sequential]
```
HOP: prompts/60_title_optimizer_HOP.md
Config: config/youtube_title_rules.json
Output: 5 angles → 4D scoring → $title_final
```

**PHASE 2: PARALLEL (~40s)** [Spawn 3 agents]
```
Agent A: Description (HOP-61) → 5 sections
Agent B: Thumbnail Text (HOP-63) → 3 variants
Agent C: Chapters (HOP-64) → 5-10 timestamps
```

**PHASE 3: TAGS (~30s)** [Sequential]
```
HOP: prompts/62_tags_optimizer_HOP.md
Config: config/youtube_tags_rules.json
Output: 30-50 tags across 4 categories
```

**PHASE 4: CONSOLIDATE (~10s)**
```
Merge all outputs
Calculate consolidated score
Generate copy-paste ready output
```

### Step 3: Quality Gates

Verify all pass:
```
[ ] Title score >= 7.5
[ ] Description score >= 7.5
[ ] Tags score >= 7.5
[ ] Thumbnail score >= 7.0
[ ] Chapters score >= 7.0 (if applicable)
[ ] Keyword consistency >= 85%
```

### Step 4: Output

Return to user:
- **Title**: Ready for YouTube title field
- **Description**: Full formatted text with sections
- **Tags**: Comma-separated list (copy-paste ready)
- **Thumbnail Text**: Recommended + alternatives with design specs
- **Chapters**: Formatted timestamps (if video >= 3min)
- **Scores**: Individual + consolidated

---

## EXAMPLE EXECUTION

**User Input:**
```
Generate YouTube metadata for:
- Topic: ChatGPT para programação
- Audience: Desenvolvedores iniciantes
- Benefit: Acelerar desenvolvimento com IA
- Duration: 15:30
```

**AI Response:**

### Title (Score: 8.72)
```
7 Prompts de ChatGPT Que Todo Dev Precisa Conhecer
```

### Description (Score: 8.35)
```
ChatGPT para programação: os 7 prompts que vão revolucionar seu workflow.
Depois de testar 50+ prompts, esses são os que realmente funcionam.

📌 O QUE VOCÊ VAI APRENDER:
• Prompt para debug inteligente
• Prompt para refatoração automática
• Prompt para documentação
...

⏱️ CAPÍTULOS:
00:00 - Introdução
01:45 - Setup Básico
04:15 - Prompt #1: Debug
...

🔗 RECURSOS:
• PDF com todos prompts: [link]
...

#ChatGPT #Programação #IA #DevTips
```

### Tags (Score: 8.92)
```
ChatGPT,programação,IA,prompts,ChatGPT tutorial,programar com IA,
ChatGPT dicas,desenvolvimento com IA,prompts ChatGPT,machine learning,
produtividade,tecnologia,como usar ChatGPT para programar...
```
(43 tags, 498 chars)

### Thumbnail Text (Score: 8.72)
```
Recommended: "2x Dev Speed"
- Font: 32px semi-bold
- Case: Mixed
- Contrast: High

Alternatives:
- "Hack Secreto" (hook angle)
- "Ninguém Conta" (curiosity angle)
```

### Chapters (Score: 8.42)
```
00:00 - Introdução e Overview
01:45 - Configurando o Ambiente
04:15 - Prompt #1: Debug Inteligente
07:30 - Prompt #2: Refatoração
10:15 - Prompt #3: Documentação
12:45 - Dicas Avançadas
15:00 - Resumo e Próximos Passos
```

### Consolidated
```
Overall Score: 8.62/10
Keyword Consistency: 96%
Ready for Upload: ✓
```

---

## PARALLEL EXECUTION

For maximum speed, use `/spawn` pattern:

```
/spawn model:sonnet
1. explore: Read 105_ADW_YOUTUBE_FULL_METADATA.md
2. haiku: Generate title (HOP-60)
3. haiku: Generate description (HOP-61) [after title]
4. haiku: Generate thumbnail text (HOP-63) [after title]
5. haiku: Generate chapters (HOP-64) [after title]
6. haiku: Generate tags (HOP-62) [after desc]
```

---

## ERROR HANDLING

| Error | Solution |
|-------|----------|
| Missing video_duration | Ask user, required for chapters |
| Score < 7.5 | Regenerate weakest component |
| Chapters skipped | Video < 3min, normal behavior |
| Timeout | Reduce parallel agents |

---

## RELATED COMMANDS

- `/video` - Generate the actual video first
- `/prime-video` - Load full video agent context
- `/prime-anuncio` - For product copy/description

---

**Version**: 1.0.0
**ADW**: 105_ADW_YOUTUBE_FULL_METADATA.md
**Duration**: ~90-150 seconds
**Output**: Complete YouTube upload package
