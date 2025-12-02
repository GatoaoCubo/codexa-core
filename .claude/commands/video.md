# /video - Generate E-commerce Product Video

## PURPOSE
Execute the complete 5-stage video generation pipeline for e-commerce products.

**Input**: Product brief
**Output**: Final MP4 video + Trinity metadata

---

## PRE-REQUISITES

Before executing, ensure:
- [ ] `/prime-video` has been loaded (or read PRIME.md)
- [ ] Brief has: produto, duracao, objetivo
- [ ] FFmpeg is installed (for editing)
- [ ] At least one video API key set (RUNWAY_API_KEY or PIKA_API_KEY)

---

## INSTRUCTIONS FOR AI ASSISTANTS

### Step 1: Collect Brief

Gather the following from user:

**Required:**
```json
{
  "produto": "Product name/description (3-200 chars)",
  "duracao": 30,  // 15-60 seconds
  "objetivo": "Main video objective (10-500 chars)"
}
```

**Optional:**
```json
{
  "formato": "9:16",  // or "16:9", "1:1"
  "tom": "energetico",  // or "calmo", "dramatico", "minimal", "cinematico"
  "preco": "R$ 599",
  "brand_profile": {}
}
```

### Step 2: Validate Brief

```
Required fields present
Duration in range (15-60)
Objective has clear focus
```

### Step 3: Execute Pipeline

**STAGE 1: CONCEPT (~5s)**
```
Read: prompts/10_concept_planner_HOP.md
Generate: 6-8 shot storyboard with narrative arc
Validate: First shot = hook, Last shot = CTA
Output: concept.json
```

**STAGE 2: SCRIPT (~3s)**
```
Read: prompts/20_script_writer_HOP.md
Generate: Narration segments + text overlays + music selection
Validate: No overlapping segments, CTA overlay exists
Output: script.json
```

**STAGE 3: VISUAL (~10s)**
```
Read: prompts/30_visual_prompter_HOP.md
Generate: Runway/Pika prompts in English
Validate: Prompts 20-500 chars, all shots covered
Output: visual_prompts.json
```

**STAGE 4: PRODUCTION (120-300s)**
```
Read: prompts/40_production_runner_HOP.md
Execute: Async API calls (parallel, max 5 concurrent)
Validate: Success rate >=80%, cost <=$2.00
Output: clips/*.mp4
```

**STAGE 5: EDITING (~15s)**
```
Read: prompts/50_editor_assembler_HOP.md
Execute: FFmpeg concatenation + TTS + audio mix + text overlays
Validate: Duration matches, audio present, file playable
Output: final_video.mp4 + .llm.json + .meta.json
```

### Step 4: Validate Quality

Run 11-point checklist:
```
[ ] Duration 15-60s
[ ] Resolution >=1080p
[ ] Frame rate >=24fps
[ ] Audio sync +-100ms
[ ] Text visible
[ ] Brand compliant
[ ] No artifacts
[ ] File size <50MB/min
[ ] Codec H.264
[ ] Aspect ratio correct
[ ] Metadata complete
```

### Step 5: Output

Return to user:
- Final video path
- Duration and file size
- Quality score
- Cost breakdown

---

## EXAMPLE EXECUTION

**User Input:**
```
Generate a 30s video for "Nike Air Max 2024" with energetic style,
highlighting amortecimento Air e design moderno
```

**AI Response:**

1. **Brief validated** - All required fields present

2. **Storyboard generated** (6 shots):
   - Shot 1: Hook - Product reveal 360
   - Shot 2-3: Build - Feature showcase
   - Shot 4-5: Benefit/Proof - In action
   - Shot 6: CTA - Price and action

3. **Script written**:
   - 4 narration segments
   - 3 text overlays
   - Upbeat music selected

4. **Prompts generated** (6 Runway prompts in English)

5. **Clips generated** (280s, $1.38)

6. **Video assembled** (19s editing)

**Final Output:**
```
outputs/nike_air_max_2024_30s.mp4
- Duration: 30.2s
- Resolution: 1080x1920
- Quality: 10.0/10.0
- Cost: $1.38
```

---

## ERROR HANDLING

| Error | Solution |
|-------|----------|
| Missing brief field | Ask user for missing info |
| Duration out of range | Adjust to 15-60 range |
| API timeout | Retry with fallback API |
| FFmpeg error | Return video without effects |
| Low quality clips | Regenerate with higher settings |

---

## RELATED COMMANDS

- `/prime-video` - Load full video context first
- `/photo` - Generate product photos instead

---

**Version**: 1.0.0
**Pipeline**: 5 stages, 3-7 minutes total
**Cost**: ~$1.00/video (30s, 6 shots)
