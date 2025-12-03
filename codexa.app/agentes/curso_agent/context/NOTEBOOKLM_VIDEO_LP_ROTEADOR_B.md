# NOTEBOOKLM_VIDEO_LP_ROTEADOR_B.md

**NotebookLM Integration for Video B (Pain-First Variation)** | v1.0.0 | 2025-12-03

---

## TRINITY STRUCTURE B

This file is part of Video B's trinity:

```
VIDEO_LP_ROTEADOR_B.md              → Script B (pain-first hook)
DIRECAO_VISUAL_LP_ROTEADOR_B.md     → Visual direction B (demo-heavy)
NOTEBOOKLM_VIDEO_LP_ROTEADOR_B.md   → This file (NotebookLM prompts B)
```

**Purpose**: Generate Video B with NotebookLM Audio Overview - shorter, more urgent, pain-focused variation for paid ads and cold audiences.

---

## PARTE 1: ARQUIVOS PARA UPLOAD

Upload these files to NotebookLM before generating audio:

### Core Script Files
1. **VIDEO_LP_ROTEADOR_B.md** (primary script)
   - Path: `codexa.app/agentes/curso_agent/context/VIDEO_LP_ROTEADOR_B.md`
   - Contains: Pain-first script, 6-8 min duration, urgent tone

2. **DIRECAO_VISUAL_LP_ROTEADOR_B.md** (visual direction)
   - Path: `codexa.app/agentes/curso_agent/context/DIRECAO_VISUAL_LP_ROTEADOR_B.md`
   - Contains: Demo-heavy visuals, multiple CTAs, CHURU MODE easter egg

### Context Files
3. **GLOSSARIO.md** (terminology)
   - Path: `codexa.app/agentes/curso_agent/context/GLOSSARIO.md`
   - Contains: Tech terms, acronyms, pronunciation guide

### Agent Context (optional but recommended)
4. **anuncio_agent/PRIME.md**
   - Path: `codexa.app/agentes/anuncio_agent/PRIME.md`
   - Context: Product copywriting philosophy

5. **pesquisa_agent/PRIME.md**
   - Path: `codexa.app/agentes/pesquisa_agent/PRIME.md`
   - Context: Market research approach

6. **photo_agent/PRIME.md**
   - Path: `codexa.app/agentes/photo_agent/PRIME.md`
   - Context: Visual design principles

---

## PARTE 2: PROMPT PRINCIPAL

Copy this prompt into NotebookLM's "Audio Overview" generation:

```
Create a podcast-style audio discussion about this AI agent workflow automation course landing page.

CRITICAL CONSTRAINTS:
- Duration: 6-8 minutes (strict maximum)
- Tone: Urgent, punchy, direct-response marketing
- Hook: Start with PAIN/FRUSTRATION (not results)
- Structure: Problem → Agitation → Solution → Demo → Multiple CTAs
- Demo-heavy: More "show don't tell" moments
- Easter egg: Include "CHURU MODE" reference naturally (around 5-6 min mark)

HOSTS:
- Host A (Sara): Skeptical marketer, burned by automation promises before
  - Frustrated, impatient, wants proof fast
  - "Yeah but..." energy
  - Questions everything

- Host B (Mike): Pragmatic developer, has tried building this before
  - Technical but accessible
  - "Let me show you" energy
  - Walks through actual workflow

TONE KEYWORDS:
- Urgent (not calm)
- Punchy (not flowing)
- Direct (not educational)
- Demo-focused (not conceptual)
- Multiple CTAs (not single soft CTA)

PAIN POINTS TO EMPHASIZE:
1. "You're still copying-pasting between tools"
2. "Your team is waiting on you for every single piece of content"
3. "You're paying for 5 different AI subscriptions that don't talk to each other"
4. "Every product launch takes 3 days just for the marketing assets"
5. "You know automation exists but don't know where to start"

SCRIPT STRUCTURE:
[0:00-0:30] HOOK - Sara vents about her morning wasting 2 hours on content
[0:30-1:30] PROBLEM - Mike validates, shares he built something similar
[1:30-3:00] AGITATE - Both discuss what they tried before (ChatGPT tabs, Make.com hell)
[3:00-5:00] SOLUTION - Mike walks through actual codexa.app workflow with examples
[5:00-5:30] DEMO - "Let me show you CHURU MODE" (easter egg moment)
[5:30-6:30] BENEFITS - Time saved, cost saved, team unblocked
[6:30-7:00] CTA 1 - "Click the link, download the workflow pack"
[7:00-7:30] CTA 2 - "Join the Discord, see it working live"
[7:30-8:00] URGENCY - "We're closing enrollment in 48 hours"

DEMO MOMENTS (be specific):
- "So you paste your product idea, it hits pesquisa_agent..."
- "Watch this - one click, 22 images generated, all on-brand"
- "Here's the wild part - it writes the ad copy AND generates the visual at the same time"
- "CHURU MODE is when you stack three agents in parallel - pesquisa, anuncio, photo - boom, full campaign in 4 minutes"

MULTIPLE CTAs (use all):
1. "Click the link in the description" (early, 6:30 mark)
2. "Download the workflow pack now" (mid, 7:00 mark)
3. "Join the Discord to see this live" (late, 7:15 mark)
4. "Enrollment closes in 48 hours" (urgency, 7:30 mark)

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
- Easter egg: MUST mention "CHURU MODE" naturally
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
- Frustration in Sara's voice (opening)
- Excitement in Mike's demos
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
"Are you still copying and pasting between AI tools?"
- Sara's frustrated morning
- Mike validates the pain
- Ends with "There's a better way" (cut to link)

SHORT 2 - CHURU MODE DEMO (5:00-6:30)
"Let me show you CHURU MODE"
- Quick explanation of parallel agents
- Example: "22 images in 4 minutes"
- Ends with "Download the workflow" (CTA)

SHORT 3 - URGENCY CLOSER (7:00-8:00)
"We're closing enrollment in 48 hours"
- Stack all CTAs (link, Discord, workflow pack)
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
- Image: Person surrounded by 10 browser tabs (ChatGPT, Claude, Midjourney)
- Text: "Stop Switching Between 5 AI Tools"
- Color: Red/orange (frustration)
- Face: Overwhelmed/annoyed

THUMBNAIL B2 - TIME WASTE
- Image: Clock showing 2 hours, pile of unfinished content
- Text: "2 Hours For One Product Ad?"
- Color: Yellow/black (warning)
- Face: Stressed/rushed

THUMBNAIL B3 - COST PAIN
- Image: Stack of subscription receipts ($20 + $30 + $25...)
- Text: "Paying $200/mo For AI That Doesn't Connect"
- Color: Dark red/gray (pain)
- Face: Frustrated/resigned

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
| **Hook** | "Here's what you'll build" (result) | "Are you wasting 2 hours a day?" (pain) |
| **Duração** | 10-12 min (deep dive) | 6-8 min (punchy) |
| **Tom** | Calm, patient, teaching | Urgent, frustrated, selling |
| **Estrutura** | Linear (concept → demo → CTA) | Agitate (pain → demo → CTAs) |
| **CTAs** | 1 soft CTA at end | 4+ hard CTAs throughout |
| **Easter Egg** | Cat Coding meme (playful) | CHURU MODE (product name) |
| **Foco Principal** | "Scale without risk" | "Save time NOW" |
| **Demonstrações** | Conceptual (how it works) | Specific (exact workflow) |
| **Target Audience** | Warm (already interested) | Cold (need convincing) |
| **Visual Style** | Screen recordings, diagrams | Fast cuts, text overlays |
| **Background Music** | Lo-fi, calm | Upbeat, driving |

### Quando Usar Video A
- Organic traffic (YouTube search)
- Warm audience (email list, retargeting)
- Educational content funnel
- Long-form platforms (YouTube, blog embeds)
- High-intent keywords ("how to automate AI workflows")

### Quando Usar Video B
- Paid ads (Facebook, Google, TikTok)
- Cold audiences (never heard of codexa.app)
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
- Workflow pack downloads
- Discord joins
- Course enrollments

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

Test duration: 14 days
Traffic split: 50/50
Winner: Highest ROAS (revenue / ad spend)
```

---

## PARTE 5: CHURU MODE EASTER EGG

**Context**: CHURU MODE is Video B's signature moment (replaces "Cat Coding" from Video A).

### What is CHURU MODE?
- **Name Origin**: CHURU = cat treat brand (parallel to "Cat Coding" theme)
- **Technical Meaning**: Running 3+ agents in parallel (pesquisa + anuncio + photo simultaneously)
- **Narrative Function**: Makes parallel execution memorable/shareable

### How to Introduce (in audio):
```
Mike: "Okay, you ready for this? Let me show you CHURU MODE."
Sara: "CHURU what?"
Mike: "CHURU MODE - it's when you run pesquisa, anuncio, and photo agents at the same time. Like... [excited] you paste your product idea, hit go, and BOOM - 4 minutes later you have market research, ad copy, AND 22 branded images. All done. While you get coffee."
Sara: "Wait, all three at once?"
Mike: "All three at once. That's CHURU MODE. It's in the workflow pack."
```

### Visual Pairing (for video edit):
- Screen: Terminal showing 3 parallel processes running
- Text overlay: "CHURU MODE" in large letters
- Animation: 3 progress bars filling simultaneously
- Sound effect: Satisfying "ding" when all complete

### Why This Works:
1. **Memorable**: Weird name sticks in memory
2. **Shareable**: "Have you tried CHURU MODE?" (social proof)
3. **Technical**: Actually describes parallel execution
4. **On-brand**: Matches codexa.app's playful-but-powerful tone
5. **CTA hook**: "CHURU MODE is in the workflow pack" (gives reason to download)

---

## PARTE 6: POST-PRODUCTION CHECKLIST

After NotebookLM generates the audio, verify:

### Audio Quality Gates
- [ ] Duration: Under 8 minutes (strict)
- [ ] Hook: Pain-first (not result-first) in first 30 sec
- [ ] Tone: Urgent/frustrated (not calm/educational)
- [ ] Demo: 3+ specific workflow examples mentioned
- [ ] CTAs: 4+ calls to action (not just 1 at end)
- [ ] Easter egg: "CHURU MODE" mentioned naturally around 5-6 min
- [ ] Pacing: Fast (minimal pauses between sections)

### Content Accuracy
- [ ] Technical terms match GLOSSARIO.md
- [ ] Workflow steps match VIDEO_LP_ROTEADOR_B.md script
- [ ] Agent names correct (pesquisa_agent, anuncio_agent, photo_agent)
- [ ] URLs/links match actual landing page
- [ ] Timing claims realistic (4 min for CHURU MODE, etc)

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

### Problem: CHURU MODE Sounds Forced
**Solution**: Rewrite introduction:
- Don't explain the name origin (just use it)
- Lead with the result ("3 agents at once")
- Let Sara ask "What's CHURU MODE?" (natural curiosity)

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
Upload VIDEO_LP_ROTEADOR_B.md, DIRECAO_VISUAL_LP_ROTEADOR_B.md, GLOSSARIO.md

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
Track CTR, completion, CPA, ROAS for 14 days
```

---

## REFERENCES

| File | Purpose |
|------|---------|
| VIDEO_LP_ROTEADOR_B.md | Script B (pain-first) |
| DIRECAO_VISUAL_LP_ROTEADOR_B.md | Visual direction B (demo-heavy) |
| NOTEBOOKLM_VIDEO_LP_ROTEADOR_A.md | Video A integration (comparison) |
| GLOSSARIO.md | Terminology/pronunciation |
| TIMING_AUDIT_VIDEO_LP.md | Timing analysis (both videos) |

---

**Version**: 1.0.0
**Type**: NotebookLM Integration (Video B Variation)
**Parent**: curso_agent context
**Last Updated**: 2025-12-03

## Changelog
- **v1.0.0** (2025-12-03): Initial Video B NotebookLM integration with pain-first approach, CHURU MODE easter egg, A/B test framework
