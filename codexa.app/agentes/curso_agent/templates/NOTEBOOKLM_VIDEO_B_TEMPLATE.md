# NOTEBOOKLM_VIDEO_B_TEMPLATE.md

**NotebookLM Integration for Video B (Pain-First Variation)** | v1.0.0 | {{LAST_UPDATED}}

---

## TRINITY STRUCTURE B

This file is part of Video B's trinity:

```
VIDEO_LP_{{PRODUCT_NAME}}_B.md              → Script B (pain-first hook)
DIRECAO_VISUAL_LP_{{PRODUCT_NAME}}_B.md     → Visual direction B (demo-heavy)
NOTEBOOKLM_VIDEO_LP_{{PRODUCT_NAME}}_B.md   → This file (NotebookLM prompts B)
```

**Purpose**: Generate Video B with NotebookLM Audio Overview - shorter, more urgent, pain-focused variation for paid ads and cold audiences.

---

## PARTE 1: ARQUIVOS PARA UPLOAD

Upload these files to NotebookLM before generating audio:

### Core Script Files
1. **VIDEO_LP_{{PRODUCT_NAME}}_B.md** (primary script)
   - Path: `{{AGENT_DIR}}/context/VIDEO_LP_{{PRODUCT_NAME}}_B.md`
   - Contains: Pain-first script, 6-8 min duration, urgent tone

2. **DIRECAO_VISUAL_LP_{{PRODUCT_NAME}}_B.md** (visual direction)
   - Path: `{{AGENT_DIR}}/context/DIRECAO_VISUAL_LP_{{PRODUCT_NAME}}_B.md`
   - Contains: Demo-heavy visuals, multiple CTAs, {{EASTER_EGG_NAME}} easter egg

### Context Files
3. **GLOSSARIO.md** (terminology)
   - Path: `{{AGENT_DIR}}/context/GLOSSARIO.md`
   - Contains: Tech terms, acronyms, pronunciation guide

### Agent Context (optional but recommended)
4. **{{AGENT_1_NAME}}/PRIME.md**
   - Path: `{{AGENTES}}/{{AGENT_1_NAME}}/PRIME.md`
   - Context: {{AGENT_1_PURPOSE}}

5. **{{AGENT_2_NAME}}/PRIME.md**
   - Path: `{{AGENTES}}/{{AGENT_2_NAME}}/PRIME.md`
   - Context: {{AGENT_2_PURPOSE}}

6. **{{AGENT_3_NAME}}/PRIME.md**
   - Path: `{{AGENTES}}/{{AGENT_3_NAME}}/PRIME.md`
   - Context: {{AGENT_3_PURPOSE}}

---

## PARTE 2: PROMPT PRINCIPAL

Copy this prompt into NotebookLM's "Audio Overview" generation:

```
Create a podcast-style audio discussion about this {{PRODUCT_DESCRIPTION}} landing page.

CRITICAL CONSTRAINTS:
- Duration: 6-8 minutes (strict maximum)
- Tone: Urgent, punchy, direct-response marketing
- Hook: Start with PAIN/FRUSTRATION (not results)
- Structure: Problem → Agitation → Solution → Demo → Multiple CTAs
- Demo-heavy: More "show don't tell" moments
- Easter egg: Include "{{EASTER_EGG_NAME}}" reference naturally (around 5-6 min mark)

HOSTS:
- Host A ({{HOST_A_NAME}}): {{HOST_A_PERSONA}}
  - {{HOST_A_TRAIT_1}}
  - {{HOST_A_TRAIT_2}}
  - {{HOST_A_TRAIT_3}}

- Host B ({{HOST_B_NAME}}): {{HOST_B_PERSONA}}
  - {{HOST_B_TRAIT_1}}
  - {{HOST_B_TRAIT_2}}
  - {{HOST_B_TRAIT_3}}

TONE KEYWORDS:
- Urgent (not calm)
- Punchy (not flowing)
- Direct (not educational)
- Demo-focused (not conceptual)
- Multiple CTAs (not single soft CTA)

PAIN POINTS TO EMPHASIZE:
1. "{{PAIN_POINT_1}}"
2. "{{PAIN_POINT_2}}"
3. "{{PAIN_POINT_3}}"
4. "{{PAIN_POINT_4}}"
5. "{{PAIN_POINT_5}}"

SCRIPT STRUCTURE:
[0:00-0:30] HOOK - {{HOST_A_NAME}} vents about {{PAIN_SCENARIO}}
[0:30-1:30] PROBLEM - {{HOST_B_NAME}} validates, shares {{PERSONAL_EXPERIENCE}}
[1:30-3:00] AGITATE - Both discuss what they tried before ({{FAILED_SOLUTION_1}}, {{FAILED_SOLUTION_2}})
[3:00-5:00] SOLUTION - {{HOST_B_NAME}} walks through actual {{BRAND_URL}} workflow with examples
[5:00-5:30] DEMO - "Let me show you {{EASTER_EGG_NAME}}" (easter egg moment)
[5:30-6:30] BENEFITS - {{BENEFIT_1}}, {{BENEFIT_2}}, {{BENEFIT_3}}
[6:30-7:00] CTA 1 - "{{CTA_1_TEXT}}"
[7:00-7:30] CTA 2 - "{{CTA_2_TEXT}}"
[7:30-8:00] URGENCY - "{{URGENCY_TEXT}}"

DEMO MOMENTS (be specific):
- "{{DEMO_EXAMPLE_1}}"
- "{{DEMO_EXAMPLE_2}}"
- "{{DEMO_EXAMPLE_3}}"
- "{{EASTER_EGG_EXPLANATION}}"

MULTIPLE CTAs (use all):
1. "{{CTA_1_TEXT}}" (early, 6:30 mark)
2. "{{CTA_2_TEXT}}" (mid, 7:00 mark)
3. "{{CTA_3_TEXT}}" (late, 7:15 mark)
4. "{{CTA_4_TEXT}}" (urgency, 7:30 mark)

AVOID:
- Long educational explanations
- Calm, patient tone
- Single soft CTA at end
- Theoretical discussions
- "You could maybe possibly..."

DO THIS INSTEAD:
- Show actual workflow steps
- Urgent, frustrated opening
- Multiple hard CTAs throughout
- Specific examples with numbers
- "Here's exactly what happens..."

QUALITY GATES:
- Duration: MUST be under 8 minutes (check at 6 min mark)
- Hook: MUST start with pain/frustration (not results)
- Demo: MUST include 3+ specific workflow examples
- CTAs: MUST include 4+ calls to action
- Easter egg: MUST mention "{{EASTER_EGG_NAME}}" naturally
- Tone: MUST sound urgent (not educational)

Generate the audio overview now.
```

---

## PARTE 3: PROMPTS AUXILIARES

### 3.1 Narração Urgente (Post-Processing)

If the initial audio is too calm, use this follow-up prompt:

```
Regenerate the audio with MORE URGENCY:

INCREASE:
- Speaking pace (faster)
- Interruptions (more natural overlap)
- Frustration in {{HOST_A_NAME}}'s voice (opening)
- Excitement in {{HOST_B_NAME}}'s demos
- Pressure in CTAs ("right now", "before it closes")

DECREASE:
- Pauses between sections
- Explanatory transitions
- Educational tone
- Politeness (be more direct)

Keep same structure, just increase intensity by 30%.
```

### 3.2 Shorts / Vertical Cuts

Extract these segments for TikTok/Reels:

```
Create 3 short audio clips (60-90 seconds each) from the main audio:

SHORT 1 - PAIN HOOK (0:00-1:30)
"{{PAIN_HOOK_QUESTION}}"
- {{HOST_A_NAME}}'s {{PAIN_SCENARIO}}
- {{HOST_B_NAME}} validates the pain
- Ends with "There's a better way" (cut to link)

SHORT 2 - {{EASTER_EGG_NAME}} DEMO (5:00-6:30)
"Let me show you {{EASTER_EGG_NAME}}"
- Quick explanation of {{EASTER_EGG_FEATURE}}
- Example: "{{DEMO_STAT}}"
- Ends with "{{SHORT_CTA_TEXT}}" (CTA)

SHORT 3 - URGENCY CLOSER (7:00-8:00)
"{{URGENCY_TEXT}}"
- Stack all CTAs ({{CTA_LIST}})
- Time/cost savings recap
- Hard close

TONE: Even MORE urgent than main video (these are ads)
EDIT: Add music breaks between speakers (for visual cuts)
```

### 3.3 Thumbnail Variations (Pain-Focused)

Generate thumbnails to match Video B's pain-first approach:

```
Create 3 thumbnail concepts for Video B (pain-focused):

THUMBNAIL B1 - FRUSTRATION
- Image: {{THUMBNAIL_B1_IMAGE_DESCRIPTION}}
- Text: "{{THUMBNAIL_B1_TEXT}}"
- Color: {{THUMBNAIL_B1_COLOR_SCHEME}}
- Face: {{THUMBNAIL_B1_EMOTION}}

THUMBNAIL B2 - TIME WASTE
- Image: {{THUMBNAIL_B2_IMAGE_DESCRIPTION}}
- Text: "{{THUMBNAIL_B2_TEXT}}"
- Color: {{THUMBNAIL_B2_COLOR_SCHEME}}
- Face: {{THUMBNAIL_B2_EMOTION}}

THUMBNAIL B3 - COST PAIN
- Image: {{THUMBNAIL_B3_IMAGE_DESCRIPTION}}
- Text: "{{THUMBNAIL_B3_TEXT}}"
- Color: {{THUMBNAIL_B3_COLOR_SCHEME}}
- Face: {{THUMBNAIL_B3_EMOTION}}

All thumbnails should:
- Show PROBLEM first (not solution)
- Use contrasting colors (stand out in feed)
- Include human face (emotion)
- Be readable on mobile (large text)
```

---

## PARTE 4: A/B TEST NOTES

Compare Video A vs Video B performance:

| Aspecto | Video A (Educational) | Video B (Pain-First) |
|---------|----------------------|---------------------|
| **Hook** | "{{VIDEO_A_HOOK}}" (result) | "{{VIDEO_B_HOOK}}" (pain) |
| **Duração** | 10-12 min (deep dive) | 6-8 min (punchy) |
| **Tom** | Calm, patient, teaching | Urgent, frustrated, selling |
| **Estrutura** | Linear (concept → demo → CTA) | Agitate (pain → demo → CTAs) |
| **CTAs** | 1 soft CTA at end | 4+ hard CTAs throughout |
| **Easter Egg** | {{VIDEO_A_EASTER_EGG}} | {{EASTER_EGG_NAME}} |
| **Foco Principal** | "{{VIDEO_A_FOCUS}}" | "{{VIDEO_B_FOCUS}}" |
| **Demonstrações** | Conceptual (how it works) | Specific (exact workflow) |
| **Target Audience** | Warm (already interested) | Cold (need convincing) |
| **Visual Style** | Screen recordings, diagrams | Fast cuts, text overlays |
| **Background Music** | Lo-fi, calm | Upbeat, driving |

### Quando Usar Video A
- Organic traffic (YouTube search)
- Warm audience (email list, retargeting)
- Educational content funnel
- Long-form platforms (YouTube, blog embeds)
- High-intent keywords ("{{HIGH_INTENT_KEYWORD_EXAMPLE}}")

### Quando Usar Video B
- Paid ads (Facebook, Google, TikTok)
- Cold audiences (never heard of {{BRAND_URL}})
- Retargeting (visited but didn't convert)
- Short-form platforms (Reels, Shorts, TikTok)
- Direct response campaigns (limited-time offers)

### Métricas para Comparar
Track these metrics for both videos:

```
ENGAGEMENT:
- Watch time (avg % completion)
- Hook retention (0-30 sec drop-off)
- Click-through rate (CTA clicks)
- Shares/saves

CONVERSION:
- Landing page visits
- {{CONVERSION_METRIC_1}}
- {{CONVERSION_METRIC_2}}
- {{CONVERSION_METRIC_3}}

COST (if paid):
- CPM (cost per 1000 impressions)
- CPC (cost per click)
- CPA (cost per acquisition)
- ROAS (return on ad spend)
```

### Hipótese de Teste
```
H1: Video B will have HIGHER CTR (paid ads) due to pain-first hook
H2: Video A will have HIGHER completion rate (organic) due to educational value
H3: Video B will have LOWER CPA (paid) due to multiple CTAs
H4: Video A will have HIGHER satisfaction (NPS) due to depth

Test duration: {{TEST_DURATION_DAYS}} days
Traffic split: 50/50
Winner: Highest ROAS (revenue / ad spend)
```

---

## PARTE 5: {{EASTER_EGG_NAME}} EASTER EGG

**Context**: {{EASTER_EGG_NAME}} is Video B's signature moment (replaces "{{VIDEO_A_EASTER_EGG}}" from Video A).

### What is {{EASTER_EGG_NAME}}?
- **Name Origin**: {{EASTER_EGG_NAME_ORIGIN}}
- **Technical Meaning**: {{EASTER_EGG_TECHNICAL_MEANING}}
- **Narrative Function**: {{EASTER_EGG_NARRATIVE_FUNCTION}}

### How to Introduce (in audio):
```
{{HOST_B_NAME}}: "Okay, you ready for this? Let me show you {{EASTER_EGG_NAME}}."
{{HOST_A_NAME}}: "{{EASTER_EGG_NAME}} what?"
{{HOST_B_NAME}}: "{{EASTER_EGG_NAME}} - {{EASTER_EGG_EXPLANATION}}. Like... [excited] {{EASTER_EGG_DEMO_EXAMPLE}}."
{{HOST_A_NAME}}: "Wait, {{EASTER_EGG_CLARIFICATION_QUESTION}}?"
{{HOST_B_NAME}}: "{{EASTER_EGG_CONFIRMATION}}. That's {{EASTER_EGG_NAME}}. {{EASTER_EGG_AVAILABILITY}}."
```

### Visual Pairing (for video edit):
- Screen: {{VISUAL_SCREEN_DESCRIPTION}}
- Text overlay: "{{EASTER_EGG_NAME}}" in large letters
- Animation: {{VISUAL_ANIMATION_DESCRIPTION}}
- Sound effect: {{VISUAL_SOUND_EFFECT}}

### Why This Works:
1. **Memorable**: {{MEMORABLE_REASON}}
2. **Shareable**: "{{SHAREABLE_PHRASE}}" (social proof)
3. **Technical**: {{TECHNICAL_REASON}}
4. **On-brand**: Matches {{BRAND_URL}}'s {{BRAND_PERSONALITY}} tone
5. **CTA hook**: "{{EASTER_EGG_CTA_HOOK}}" (gives reason to download)

---

## PARTE 6: POST-PRODUCTION CHECKLIST

After NotebookLM generates the audio, verify:

### Audio Quality Gates
- [ ] Duration: Under 8 minutes (strict)
- [ ] Hook: Pain-first (not result-first) in first 30 sec
- [ ] Tone: Urgent/frustrated (not calm/educational)
- [ ] Demo: 3+ specific workflow examples mentioned
- [ ] CTAs: 4+ calls to action (not just 1 at end)
- [ ] Easter egg: "{{EASTER_EGG_NAME}}" mentioned naturally around 5-6 min
- [ ] Pacing: Fast (minimal pauses between sections)

### Content Accuracy
- [ ] Technical terms match GLOSSARIO.md
- [ ] Workflow steps match VIDEO_LP_{{PRODUCT_NAME}}_B.md script
- [ ] Agent names correct ({{AGENT_LIST}})
- [ ] URLs/links match actual landing page
- [ ] Timing claims realistic ({{TIMING_CLAIM_EXAMPLE}})

### A/B Test Differentiation
- [ ] Noticeably different from Video A (not just shorter)
- [ ] Pain-first hook (vs Video A's result-first)
- [ ] Multiple CTAs (vs Video A's single CTA)
- [ ] Urgent tone (vs Video A's calm tone)
- [ ] Demo-heavy (vs Video A's conceptual)

---

## TROUBLESHOOTING

### Problem: Audio Too Calm/Educational
**Solution**: Use "Narração Urgente" prompt (Section 3.1) to regenerate

### Problem: Duration Over 8 Minutes
**Solution**: Edit script to remove:
1. Long explanations (keep only demos)
2. Transition phrases ("So let me explain...")
3. Theoretical discussions (show, don't tell)

### Problem: {{EASTER_EGG_NAME}} Sounds Forced
**Solution**: Rewrite introduction:
- Don't explain the name origin (just use it)
- Lead with the result ("{{EASTER_EGG_RESULT_LEAD}}")
- Let {{HOST_A_NAME}} ask "What's {{EASTER_EGG_NAME}}?" (natural curiosity)

### Problem: Not Different Enough from Video A
**Solution**: Increase contrast:
- Make hook MORE frustrated
- Cut duration by 20%
- Add 2 more CTAs
- Speed up speaking pace
- Remove all calm music cues

---

## USAGE WORKFLOW

```bash
# 1. Upload files to NotebookLM
Upload VIDEO_LP_{{PRODUCT_NAME}}_B.md, DIRECAO_VISUAL_LP_{{PRODUCT_NAME}}_B.md, GLOSSARIO.md

# 2. Generate audio with Prompt Principal (Parte 2)
Copy prompt → NotebookLM → Generate Audio Overview

# 3. Review against Quality Gates (Parte 6)
Check duration, hook, tone, CTAs, easter egg

# 4. If needed, regenerate with Narração Urgente (Parte 3.1)
Increase urgency by 30%

# 5. Extract Shorts (Parte 3.2)
Create 3x 60-90 sec clips for social

# 6. Design thumbnails (Parte 3.3)
Pain-focused visuals (frustration, time waste, cost)

# 7. A/B test vs Video A (Parte 4)
Track CTR, completion, CPA, ROAS for {{TEST_DURATION_DAYS}} days
```

---

## REFERENCES

| File | Purpose |
|------|---------|
| VIDEO_LP_{{PRODUCT_NAME}}_B.md | Script B (pain-first) |
| DIRECAO_VISUAL_LP_{{PRODUCT_NAME}}_B.md | Visual direction B (demo-heavy) |
| NOTEBOOKLM_VIDEO_LP_{{PRODUCT_NAME}}_A.md | Video A integration (comparison) |
| GLOSSARIO.md | Terminology/pronunciation |
| TIMING_AUDIT_VIDEO_LP.md | Timing analysis (both videos) |

---

**Version**: {{VERSION}}
**Type**: NotebookLM Integration Template (Video B Variation)
**Parent**: {{AGENT_DIR}}
**Last Updated**: {{LAST_UPDATED}}

## Changelog
- **v1.0.0** ({{LAST_UPDATED}}): Initial Video B NotebookLM integration template with pain-first approach, {{EASTER_EGG_NAME}} easter egg, A/B test framework
