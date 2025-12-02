# ═══════════════════════════════════════════════════════════════════════════
# CODEX-ANUNCIO: VIDEO SCRIPT VEO3 MODULE (HOP v2.1)
# ═══════════════════════════════════════════════════════════════════════════

[MODULE_METADATA]
name: "video_script_veo3_HOP"
version: "2.1.0"
framework: "HOP (Hierarchical Operational Protocol)"
specialization: "Video script generation for AI video synthesis (VEO3, Runway, Pika)"
output_type: "structured_markdown_json"
target_format: "9:16 vertical (mobile-first)"
target_duration: "30-60 seconds"
target_scenes: "6-9 scenes"
generation_time_target: "<20s"

[CORE_MISSION]
Generate **universal video scripts** for AI video generation (Google VEO3, Runway Gen-3, Pika 1.5) that:
→ Work for ANY product/service/brand (generic template)
→ Use `[VARIAVEL]` as dynamic placeholder for product identity
→ Follow proven 7-element narrative structure (Problem → Solution → Demo → Benefits → Result → CTA)
→ Are **copy-paste ready** for immediate use in AI video generators
→ Contain **objective visual descriptions** (AI-generatable, not subjective)
→ Leave **intentional gaps** (exact camera paths, secondary props) for model creativity
→ Comply with **AI generation limitations** (no extreme close-ups on faces, realistic movements)
→ Optimize for **mobile-first 9:16 vertical format** (Stories, Reels, Shorts)

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 1: INPUT PROTOCOL
## ═══════════════════════════════════════════════════════════════════════════

[REQUIRED_INPUTS]
1. **[VARIAVEL]**: Product/service/brand name or description
   - Example: "Cama Suspensa para Gato com Ventosas"
   - Example: "Fone Bluetooth Over-Ear ANC Preto"
   - Example: "Protetor Solar FPS 50+ Facial"

2. **[DOR_PRINCIPAL]**: Main pain point/problem product solves
   - Example: "falta de espaço em apartamentos pequenos"
   - Example: "ruído externo atrapalha concentração no home office"
   - Example: "manchas e envelhecimento precoce da pele"

3. **[SOLUCAO_OFERECIDA]**: How product solves the problem
   - Example: "fixação vertical em janelas economiza 100% do espaço no chão"
   - Example: "cancelamento de ruído ANC isola 98% dos sons externos"
   - Example: "proteção UVA/UVB ampla com textura invisível"

4. **[BENEFICIOS_FUNCIONAIS]**: Tangible functional benefits (2-3 key benefits)
   - Example: ["economia de espaço 100%", "ventosas suportam 15kg", "instalação sem furos"]
   - Example: ["bateria 40h", "ANC 30dB", "conforto memory foam"]
   - Example: ["FPS 50+ resistente água", "textura seca toque", "sem marcas brancas"]

5. **[BENEFICIOS_EMOCIONAIS]**: Emotional gains desired
   - Example: ["tranquilidade do tutor", "conforto do pet", "organização visual"]
   - Example: ["produtividade recuperada", "concentração total", "paz mental"]
   - Example: ["confiança na pele", "liberdade sem preocupação", "aparência saudável"]

6. **[CONTEXTO_USO]**: Where/how product is used
   - Example: "fixado em janela de apartamento, gato descansando"
   - Example: "home office ruidoso, pessoa trabalhando com fone"
   - Example: "praia, piscina, outdoor durante dia ensolarado"

7. **[RESULTADO_TRANSFORMACAO]**: Desired "after" state
   - Example: "espaço livre no chão + gato confortável na altura"
   - Example: "silêncio total + produtividade máxima"
   - Example: "pele protegida + curtir o sol sem medo"

[OPTIONAL_INPUTS]
8. **[CATEGORIA]**: Product category (for mood adaptation)
   - Example: "Pet Shop", "Eletrônicos", "Cosméticos", "Casa & Decoração"

9. **[PUBLICO_ALVO]**: Target audience (for scene context)
   - Example: "tutores de gatos, 25-45 anos, apartamentos urbanos"

10. **[REFERENCE_VIDEO_URL]**: URL to reference video style (if available)

[CONFIGURATION_FLAGS]
- **TARGET_PLATFORM**: `veo3` (default) | `runway` | `pika` | `universal`
- **DURATION_PREFERENCE**: `short` (30-35s) | `medium` (40-50s) | `long` (55-60s)
- **RANDOMIZE_MOOD**: `on` | `off` (default: off) — enables mood variation banks

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 2: TECHNICAL SPECIFICATIONS FOR AI VIDEO GENERATION
## ═══════════════════════════════════════════════════════════════════════════

### [SPECS_FORMAT]
aspect_ratio: "9:16 (vertical — mobile-first for Stories, Reels, Shorts)"
resolution: "1080×1920 (Full HD vertical)"
fps: "24fps (default) | 30fps (smoother motion)"
duration_total: "30-60 seconds"
scenes_count: "6-9 scenes"
scene_duration: "3-10 seconds per scene"

### [SPECS_CAMERA_MOVEMENTS]
Purpose: Define realistic camera movements AI can generate

**ALLOWED (AI-friendly):**
- Pan horizontal/vertical (slow, steady)
- Tilt up/down (gradual)
- Zoom in/out (subtle, not extreme)
- Orbit 180° (slow circular around object)
- Dolly in/out (forward/backward movement)
- Static shot (no movement)

**AVOID (AI struggles):**
- Handheld shaky (inconsistent results)
- Extreme zooms (distortion risk)
- Complex crane shots (beyond AI capability)
- Rapid whip pans (motion blur artifacts)
- 360° full orbit (continuity breaks)

### [SPECS_LIGHTING]
Purpose: Objective lighting descriptions AI can interpret

**ALLOWED:**
- "Natural daylight soft diffused"
- "Studio lighting 360° even"
- "Golden hour warm lateral"
- "Overhead key light with fill"
- "High-key bright minimal shadows"
- "Low-key dramatic contrast"

**AVOID:**
- Subjective terms ("beautiful lighting", "cinematic mood")
- Specific lux values (AI doesn't understand "5000 lux")
- Complex multi-light setups (AI simplifies)

### [SPECS_TRANSITIONS]
**RECOMMENDED (AI-friendly):**
- Cut (simple, instant)
- Dissolve (crossfade, 0.5-1s)
- Match cut (same object, different context)
- Fade to black (end of video)

**AVOID:**
- Wipes (complex, inconsistent)
- 3D transitions (beyond AI capability)
- Glitch effects (artifact risk)

### [SPECS_AI_PLATFORM_LIMITATIONS]

**VEO3 (Google):**
- ✅ Excellent: Smooth camera movements, object consistency
- ✅ Good: Product shots, natural environments
- ⚠️ Limited: Detailed human faces, complex animal movements
- ❌ Avoid: Extreme close-ups on faces

**Runway Gen-3:**
- ✅ Excellent: Static product shots, cinematic lighting
- ✅ Good: Slow-motion, controlled environments
- ⚠️ Limited: Fast motion, animals in action
- ❌ Avoid: Rapid cuts, shaky cam

**Pika 1.5:**
- ✅ Excellent: Transformations, lighting effects
- ✅ Good: Short scenes (<6s), visual effects
- ⚠️ Limited: Long scenes (>8s), consistency
- ❌ Avoid: Extended sequences

### [GLOBAL_CONSTRAINTS]
Apply to ALL scenes (non-negotiable):
```
- No extreme close-ups on human faces (AI struggles with facial detail)
- No text/captions in video (add in post-production)
- No complex acrobatics or unrealistic movements (AI cannot generate)
- No copyrighted music references (add audio in post)
- Objective visual descriptions only (not subjective like "beautiful", "amazing")
- Movements must be realistic and physically possible
- Lighting must be natural or standard studio setup
```

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 3: NARRATIVE STRUCTURE (7-ELEMENT FRAMEWORK)
## ═══════════════════════════════════════════════════════════════════════════

### [NARRATIVE_OVERVIEW]
Purpose: Proven storytelling structure for product videos

**7 Mandatory Elements:**
1. **GANCHO/PROBLEMA** (Hook/Problem) — 3-5s
2. **SOLUÇÃO VISUAL** (Visual Solution) — 5-7s
3. **DEMONSTRAÇÃO** (Demonstration) — 8-12s (2 scenes)
4. **BENEFÍCIO 1 FUNCIONAL** (Functional Benefit) — 5-7s
5. **BENEFÍCIO 2 EMOCIONAL** (Emotional Benefit) — 5-7s
6. **RESULTADO FINAL/TRANSFORMAÇÃO** (Final Result) — 5-7s
7. **CTA VISUAL** (Call to Action) — 3-5s

**Total**: 6-9 scenes, 30-60 seconds

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ ELEMENTO 1: GANCHO/PROBLEMA (3-5s) — CENA 1                          ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[ELEMENT_1_SPECS]
objective: "Capture attention by showing pain point visually"
duration: "3-5 seconds"
scene_count: 1
mood: "Frustrating, relatable, urgent"
rhythm: "Fast-paced (hook attention immediately)"

[FORMULA_ELEMENT_1]
```
Visual scene showing [DOR_PRINCIPAL] in realistic context, expressing frustration or discomfort without narration, focus on universal relatable pain
```

[SCENE_TEMPLATE_ELEMENT_1]
```
CENA 1 (3-5s): PROBLEMA/GANCHO
Visual: [CONTEXT_DESCRIPTION] showing [DOR_PRINCIPAL] visually. [ACTION_EXPRESSING_FRUSTRATION]. Camera [CAMERA_MOVEMENT] revealing problem. [ENVIRONMENT_DETAILS].

Lighting: [LIGHTING_TYPE]
Mood: [EMOTIONAL_TONE_PROBLEM]
Camera Movement: [PAN | TILT | STATIC]
Duration: [3-5] seconds
Transition: [Dissolve | Cut] to next scene
```

[EXAMPLE_ELEMENT_1]
Product: "Cama Suspensa para Gato com Ventosas"
```
CENA 1 (4s): PROBLEMA/GANCHO
Visual: Small apartment living room congested with furniture. Camera pans horizontally revealing large cat bed on floor occupying valuable space, objects around cramped, person nearly tripping on bed. Cat resting on floor without elevated option. Visual expression of "lack of space" and organizational discomfort.

Lighting: Natural soft daylight, slightly blurred background to focus on obstacle
Mood: Frustrating, claustrophobic, need for solution
Camera Movement: Slow horizontal pan
Duration: 4 seconds
Transition: Dissolve to next scene
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ ELEMENTO 2: SOLUÇÃO VISUAL (5-7s) — CENA 2                           ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[ELEMENT_2_SPECS]
objective: "Present product as natural answer to problem"
duration: "5-7 seconds"
scene_count: 1
mood: "Elegant solution, premium quality, 'this is what you need'"
rhythm: "Moderate (allow product reveal to breathe)"

[FORMULA_ELEMENT_2]
```
Elegant reveal of [VARIAVEL] as hero, gradual presentation, product complete and clean (product shot), highlight main visual differentiator
```

[SCENE_TEMPLATE_ELEMENT_2]
```
CENA 2 (5-7s): SOLUÇÃO VISUAL
Visual: [PRODUCT_REVEAL_STYLE] of [VARIAVEL] on [BACKGROUND_TYPE]. Camera [CAMERA_MOVEMENT] around product showing [KEY_VISUAL_DIFFERENTIATORS]. [LIGHTING_HIGHLIGHTS_QUALITY].

Lighting: [STUDIO | NATURAL] lighting, [SOFT | DRAMATIC] shadows for dimension
Mood: [ELEGANT_SOLUTION_TONE]
Camera Movement: [ORBIT 180° | ZOOM IN | STATIC WITH FOCUS SHIFT]
Duration: [5-7] seconds
Transition: [Cut | Dissolve] to next scene
```

[EXAMPLE_ELEMENT_2]
```
CENA 2 (6s): SOLUÇÃO VISUAL
Visual: Smooth dissolve to close-up of Cama Gato Janela on clean neutral background. Camera orbits slowly 180° around bed showing compact design, 4 large transparent suction cups on top, elegant gray Oxford fabric, visible soft cushion. Soft light highlights product quality and suction cups.

Lighting: Studio soft 360° lighting, subtle shadows for dimension
Mood: Elegant solution, premium quality, "this is what you need"
Camera Movement: Slow orbit 180°
Duration: 6 seconds
Transition: Cut to next scene
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ ELEMENTO 3: DEMONSTRAÇÃO (8-12s) — CENAS 3-4                         ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[ELEMENT_3_SPECS]
objective: "Show product in real use, demonstrate ease of installation/use"
duration: "8-12 seconds (split into 2 scenes)"
scene_count: 2
mood: "Easy, fast, no complications"
rhythm: "Demonstrative clear (show functionality step-by-step)"

[FORMULA_ELEMENT_3]
```
SCENE 3: [VARIAVEL] being installed/set up in real context, demonstrate installation ease
SCENE 4: [VARIAVEL] in use with user/pet interacting naturally, functionality in action
```

[SCENE_TEMPLATE_ELEMENT_3_PART_1]
```
CENA 3 (4-5s): DEMONSTRAÇÃO INSTALAÇÃO
Visual: [USER_ACTION_INSTALLING] [VARIAVEL] in [REAL_CONTEXT]. [INSTALLATION_STEPS_VISUAL]. Camera shows [EASE_OF_INSTALLATION_PROOF].

Lighting: [NATURAL | AMBIENT] lighting from [LIGHT_SOURCE]
Mood: [EASY_FAST_SIMPLE]
Camera Movement: [CLOSE-UP | MID-SHOT]
Duration: [4-5] seconds
Transition: [Cut | Match Cut] to next scene
```

[SCENE_TEMPLATE_ELEMENT_3_PART_2]
```
CENA 4 (6-8s): DEMONSTRAÇÃO USO
Visual: [WIDE | MID] shot showing [VARIAVEL] now [IN_USE_STATE]. [USER/PET] [INTERACTION_ACTION]. [CONTEXT_BACKGROUND_BLURRED].

Lighting: [NATURAL | SOFT] lighting [TIME_OF_DAY]
Mood: [IMMEDIATE_COMFORT_APPROVAL_PROVEN_FUNCTIONALITY]
Camera Movement: [STATIC | SLOW_ZOOM_IN]
Duration: [6-8] seconds
Transition: [Cut | Dissolve] to next scene
```

[EXAMPLE_ELEMENT_3]
```
CENA 3 (5s): DEMONSTRAÇÃO INSTALAÇÃO
Visual: Hands cleaning glass window with cloth. Then positioning bed against glass, pressing each suction cup sequentially (quick close-up on suction cups adhering with small visual "click"). Camera shows secure fixation.

Lighting: Natural window lighting, real apartment ambient
Mood: Easy, fast, no complications
Camera Movement: Close-up sequence on installation steps
Duration: 5 seconds
Transition: Cut to next scene

CENA 4 (7s): DEMONSTRAÇÃO USO
Visual: Wide shot showing bed now fixed on window at mid-height. Cat (gray or orange) approaching curious, sniffing, then easily climbing onto bed. Cat settles in natural curled position. Urban window view blurred background.

Lighting: Soft natural afternoon light
Mood: Immediate comfort, pet approval, proven functionality
Camera Movement: Static wide shot
Duration: 7 seconds
Transition: Dissolve to next scene
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ ELEMENTO 4: BENEFÍCIO 1 FUNCIONAL (5-7s) — CENA 5                    ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[ELEMENT_4_SPECS]
objective: "Highlight main functional benefit in action"
duration: "5-7 seconds"
scene_count: 1
mood: "Liberating, practical, 'I got my [X] back'"
rhythm: "Demonstrative (show tangible benefit visually)"

[FORMULA_ELEMENT_4]
```
Close or medium shot focusing on [BENEFICIO_FUNCIONAL_1] being demonstrated visibly, use before/after if applicable
```

[SCENE_TEMPLATE_ELEMENT_4]
```
CENA 5 (5-7s): BENEFÍCIO FUNCIONAL 1
Visual: [BEFORE_AFTER_SPLIT | SINGLE_SHOT] showing [BENEFICIO_FUNCIONAL_1] in action. [TANGIBLE_PROOF_OF_BENEFIT]. [USER/PET] [ENJOYING_BENEFIT].

Lighting: [CONSISTENT | NATURAL] lighting
Mood: [LIBERATING_PRACTICAL_GAIN]
Camera Movement: [STATIC | SLOW_PAN]
Duration: [5-7] seconds
Transition: [Dissolve | Cut] to next scene
```

[EXAMPLE_ELEMENT_4]
```
CENA 5 (6s): BENEFÍCIO FUNCIONAL 1 (Economia de Espaço)
Visual: Split screen or quick transition showing "before" (congested living room floor with bed on ground) and "after" (same living room with free spacious floor - bed now on window). Person walking freely through recovered space, perhaps placing decorative vase where bed used to be.

Lighting: Consistent natural lighting between before/after
Mood: Liberating, "I got my space back", practicality
Camera Movement: Static before/after comparison
Duration: 6 seconds
Transition: Dissolve to next scene
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ ELEMENTO 5: BENEFÍCIO 2 EMOCIONAL (5-7s) — CENA 6                    ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[ELEMENT_5_SPECS]
objective: "Show emotional gain/desired result being experienced"
duration: "5-7 seconds"
scene_count: 1
mood: "Peace, tranquility, full comfort, 'my [user/pet] is happy'"
rhythm: "Emotional, slower (emphasize feeling)"

[FORMULA_ELEMENT_5]
```
[BENEFICIO_EMOCIONAL] being experienced, focus on sensation, emotion, satisfaction shown through scene (not narrated)
```

[SCENE_TEMPLATE_ELEMENT_5]
```
CENA 6 (5-7s): BENEFÍCIO EMOCIONAL
Visual: [CLOSE | MID] shot of [USER/PET] experiencing [BENEFICIO_EMOCIONAL]. [EMOTIONAL_EXPRESSION_DETAILS]. [SUBTLE_SLOW_MOTION_OPTIONAL] to emphasize tranquility. [AMBIENT_CONTEXT].

Lighting: [GOLDEN_HOUR | SOFT_NATURAL] lighting [WARM_TONE]
Mood: [PEACE_TRANQUILITY_COMFORT]
Camera Movement: [STATIC | SLOW_ZOOM_IN]
Duration: [5-7] seconds
Transition: [Dissolve | Cut] to next scene
```

[EXAMPLE_ELEMENT_5]
```
CENA 6 (6s): BENEFÍCIO EMOCIONAL (Conforto Total)
Visual: Close-up of cat deeply resting in window bed, half-closed eyes in total relaxation, paw stretched comfortably. Soft natural window light illuminating cat's fur. Subtle slow motion 50% to emphasize tranquility. Subtle window reflection showing external view.

Lighting: Golden hour natural soft (afternoon)
Mood: Peace, tranquility, full comfort, "my cat is happy"
Camera Movement: Slow zoom in on cat's peaceful face
Duration: 6 seconds
Transition: Dissolve to next scene
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ ELEMENTO 6: RESULTADO FINAL/TRANSFORMAÇÃO (5-7s) — CENA 7            ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[ELEMENT_6_SPECS]
objective: "Show ideal 'after' state, achieved transformation"
duration: "5-7 seconds"
scene_count: 1
mood: "Satisfaction, balance, 'problem solved', life improved"
rhythm: "Satisfying, resolution (convey 'worth it')"

[FORMULA_ELEMENT_6]
```
Wide shot showing ideal situation: [PROBLEMA] solved, [USER] satisfied, [VARIAVEL] perfectly integrated in life
```

[SCENE_TEMPLATE_ELEMENT_6]
```
CENA 7 (5-7s): RESULTADO FINAL/TRANSFORMAÇÃO
Visual: Wide shot of [FULL_ENVIRONMENT_IMPROVED]. [VARIAVEL] visible [IN_BACKGROUND | INTEGRATED]. [USER/PET] [ENJOYING_IMPROVED_STATE]. [HARMONY_DETAILS]. Everything transmits [TRANSFORMATION_ACHIEVED].

Lighting: [NATURAL_SOFT | WARM] and welcoming
Mood: [SATISFACTION_BALANCE_LIFE_IMPROVED]
Camera Movement: [STATIC_WIDE | SLOW_PAN]
Duration: [5-7] seconds
Transition: [Dissolve | Cut] to next scene
```

[EXAMPLE_ELEMENT_6]
```
CENA 7 (6s): RESULTADO FINAL/TRANSFORMAÇÃO
Visual: Wide shot of organized spacious living room. Cat sleeping comfortably in window bed in background, person on couch reading book relaxed in foreground, clean harmonious environment. Decorative plant where floor bed used to be. Everything transmits organization, mutual comfort (human + pet), intelligent solution.

Lighting: Natural soft welcoming light
Mood: Satisfaction, balance, "problem solved", improved life
Camera Movement: Static wide shot
Duration: 6 seconds
Transition: Dissolve to next scene
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ ELEMENTO 7: CTA VISUAL (3-5s) — CENA 8                               ║
### ╚═══════════════════════════════════════════════════════════════════════╝

[ELEMENT_7_SPECS]
objective: "Visual call to action with product in spotlight"
duration: "3-5 seconds"
scene_count: 1
mood: "Invitation to action, 'this product can be yours'"
rhythm: "Conclusive (prepare for text CTA in post-production)"

[FORMULA_ELEMENT_7]
```
Final shot of [VARIAVEL] in clean hero shot, slow zoom or reveal, prepare for text CTA overlay (added in post-production)
```

[SCENE_TEMPLATE_ELEMENT_7]
```
CENA 8 (3-5s): CTA VISUAL
Visual: Hero shot of [VARIAVEL] on [CLEAN_BACKGROUND], [ANGLE_45_OR_FRONTAL]. Camera [SLOW_ZOOM_IN | SUBTLE_ORBIT]. [LIGHTING_HIGHLIGHTS_PRODUCT]. Product centered, perfect for adding text "[CTA_TEXT]" in post-production.

Lighting: [STUDIO_CLEAN | HIGH-KEY] 360° soft lighting
Mood: [INVITATION_TO_ACTION]
Camera Movement: [SLOW_ZOOM_IN | SUBTLE_ORBIT]
Duration: [3-5] seconds
Transition: Fade to black
```

[EXAMPLE_ELEMENT_7]
```
CENA 8 (4s): CTA VISUAL
Visual: Hero shot of Cama Gato Janela on clean white background, elegant 45° angle. Camera does slow zoom in on product while lighting highlights suction cups and Oxford texture. Product centered, perfect for adding text "Get Yours Now" or CTA in post-production.

Lighting: Studio clean 360° soft lighting
Mood: Invitation to action, "this product can be yours"
Camera Movement: Slow zoom in
Duration: 4 seconds
Transition: Fade to black

[Space for text CTA in post-production: "Buy Now" or "Learn More"]
```

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 4: VALIDATION PROTOCOL
## ═══════════════════════════════════════════════════════════════════════════

### [VALIDATION_CHECKLIST]
Each generated script MUST pass these checks:

**Structural Validation:**
- [ ] 6-9 scenes (not less, not more)
- [ ] Total duration 30-60 seconds (sum all scenes)
- [ ] Each scene 3-10 seconds
- [ ] Format 9:16 vertical mentioned in specs
- [ ] All 7 narrative elements present (Problem → Solution → Demo → Benefits → Result → CTA)

**Content Quality:**
- [ ] Visual descriptions are objective (not subjective like "beautiful", "amazing")
- [ ] Lighting described for each scene
- [ ] Mood/emotion described for each scene
- [ ] Camera movements are realistic and AI-generatable
- [ ] No extreme close-ups on human faces
- [ ] No impossible effects for AI (complex acrobatics, unrealistic physics)

**Technical Compliance:**
- [ ] Camera movements from ALLOWED list (pan, tilt, zoom, orbit, dolly, static)
- [ ] Transitions from RECOMMENDED list (cut, dissolve, match cut)
- [ ] Lighting descriptions are objective and AI-interpretable
- [ ] No copyrighted music references
- [ ] No text/captions in video (noted for post-production only)

**Meta-Prompt Integrity:**
- [ ] Uses `[VARIAVEL]` as placeholder (not specific product hardcoded)
- [ ] Generic enough to work for any product in category
- [ ] Leaves intentional gaps (exact camera paths, secondary props)
- [ ] Copy-paste ready for AI video generator input

### [DURATION_ADJUSTMENT_RULES]

**If total duration <30s:**
- Expand demonstration scenes (3-4) by +2s each
- Add extra functional benefit scene
- Lengthen emotional benefit scene by +2s

**If total duration >60s:**
- Reduce hook scene to 3s (minimum)
- Combine benefits into single scene
- Remove least critical scene (usually functional benefit 1)
- Shorten CTA to 3s

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 5: MOOD & RHYTHM STRATEGIES BY CATEGORY
## ═══════════════════════════════════════════════════════════════════════════

### [MOOD_BANK_PET_SHOP]
emotional_tone: "Cuteness, comfort, love for pet"
lighting: "Soft and warm"
rhythm: "Moderate with slow motion in tender moments"
special_elements: "Slow motion 50% during pet interaction moments"

### [MOOD_BANK_ELETRONICOS]
emotional_tone: "Sleek, modern, technological"
lighting: "High contrast dramatic"
rhythm: "Fluid product movement, dynamic"
special_elements: "Smooth camera orbits, LED highlights"

### [MOOD_BANK_CASA_DECORACAO]
emotional_tone: "Cozy, harmonious, aspirational"
lighting: "Natural golden hour"
rhythm: "Wide shots showing environment, slower pace"
special_elements: "Ambient integration, lifestyle context"

### [MOOD_BANK_FITNESS_ESPORTE]
emotional_tone: "Energy, movement, results"
lighting: "Dynamic high-key"
rhythm: "Faster pace, frequent cuts"
special_elements: "Action shots, sweat details, intensity"

### [MOOD_BANK_COSMETICOS]
emotional_tone: "Self-care, confidence, transformation"
lighting: "Soft diffused flattering"
rhythm: "Intimate close-ups, slower sensorial"
special_elements: "Texture close-ups, before/after reveal"

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 6: EXECUTION LOGIC & WORKFLOW
## ═══════════════════════════════════════════════════════════════════════════

### [EXECUTION_STEPS]

**STEP 1: PARSE INPUT**
- Extract `[VARIAVEL]`, `[DOR_PRINCIPAL]`, `[SOLUCAO_OFERECIDA]`, `[BENEFICIOS_FUNCIONAIS]`, `[BENEFICIOS_EMOCIONAIS]`, `[CONTEXTO_USO]`, `[RESULTADO_TRANSFORMACAO]`
- Determine `TARGET_PLATFORM`: veo3, runway, pika, or universal
- Check `DURATION_PREFERENCE`: short (30-35s), medium (40-50s), long (55-60s)
- Check `RANDOMIZE_MOOD` flag: if on, activate mood variation banks

**STEP 2: GENERATE 7-ELEMENT NARRATIVE**
- For each element (1-7):
  → Apply element-specific formula (FORMULA_ELEMENT_X)
  → Replace `[VARIAVEL]` with input value
  → Replace `[DOR_PRINCIPAL]`, `[BENEFICIOS_FUNCIONAIS]`, etc. with input values
  → If `RANDOMIZE_MOOD=on`: inject random mood from MOOD_BANK by category
  → Validate duration per scene (3-10s)
  → Validate camera movements against ALLOWED list
  → Validate lighting descriptions are objective

**STEP 3: CALCULATE TOTAL DURATION**
- Sum all scene durations
- If <30s: apply DURATION_ADJUSTMENT_RULES (expand)
- If >60s: apply DURATION_ADJUSTMENT_RULES (reduce)
- Re-validate after adjustments

**STEP 4: VALIDATE SCRIPT**
- Run VALIDATION_CHECKLIST (structural, content, technical, meta-prompt)
- Flag any violations
- Provide compliance score: `PASS (all checks)` or `PARTIAL (X/N checks failed)`

**STEP 5: FORMAT OUTPUT**
- Structure as markdown + JSON hybrid (readable + parseable)
- Include scene-by-scene breakdown with all specs
- Provide narrative summary
- Include validation report
- Add copy-paste ready prompts for AI video generator

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 7: OUTPUT TEMPLATE (STRUCTURED MARKDOWN + JSON)
## ═══════════════════════════════════════════════════════════════════════════

### [OUTPUT_FORMAT_TEMPLATE]

```markdown
# ═══════════════════════════════════════════════════════════════════════════
# VIDEO SCRIPT VEO3: [VARIAVEL]
# ═══════════════════════════════════════════════════════════════════════════

[METADATA]
product: "[VARIAVEL]"
category: "[CATEGORIA]"
target_platform: "[veo3 | runway | pika | universal]"
format: "9:16 (vertical mobile-first)"
resolution: "1080×1920 (Full HD vertical)"
fps: "24fps"
duration_total: "[XX] seconds"
scenes_count: [6-9]
validation_status: "PASS (all checks)" | "PARTIAL (X/N)" | "FAIL"

---

## ESPECIFICAÇÕES TÉCNICAS

**Formato:** 9:16 (vertical — Stories, Reels, Shorts)
**Resolução:** 1080×1920 (Full HD)
**FPS:** 24fps
**Duração Total:** [XX] segundos
**Número de Cenas:** [N]

---

## NARRATIVA VISUAL (7 ELEMENTOS)

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ CENA 1: GANCHO/PROBLEMA (Xs)                                         ║
### ╚═══════════════════════════════════════════════════════════════════════╝

**Elemento Narrativo:** 1. GANCHO/PROBLEMA
**Duração:** [X] segundos
**Objetivo:** Capturar atenção mostrando dor visualmente

**Descrição Visual:**
[Generated visual description based on input]

**Lighting:** [Lighting type and mood]
**Mood:** [Emotional tone]
**Camera Movement:** [Movement type from ALLOWED list]
**Transition to Next:** [Transition type]

**AI Generator Prompt (Copy-Paste Ready):**
```
[Generated prompt for AI video generator, objective and specific]
```

---

### ╔═══════════════════════════════════════════════════════════════════════╗
### ║ CENA 2: SOLUÇÃO VISUAL (Xs)                                          ║
### ╚═══════════════════════════════════════════════════════════════════════╝

**Elemento Narrativo:** 2. SOLUÇÃO VISUAL
**Duração:** [X] segundos
**Objetivo:** Apresentar produto como resposta natural

**Descrição Visual:**
[Generated visual description]

**Lighting:** [Lighting specs]
**Mood:** [Emotional tone]
**Camera Movement:** [Movement type]
**Transition to Next:** [Transition type]

**AI Generator Prompt (Copy-Paste Ready):**
```
[Generated prompt]
```

---

[... Continue for all 7 elements / 8 scenes ...]

---

## RESUMO NARRATIVO

**História do Vídeo:**
[Generated narrative summary: problema → solução → demonstração → benefícios → resultado → CTA]

**Keywords Visuais:**
[Generated list of visual keywords for search/tags]

---

## RELATÓRIO DE VALIDAÇÃO

**Validação Estrutural:**
- [✅] 6-9 cenas: [N] cenas ✓
- [✅] Duração 30-60s: [XX]s ✓
- [✅] Cada cena 3-10s: ✓
- [✅] Formato 9:16: ✓
- [✅] 7 elementos narrativos: ✓

**Validação de Conteúdo:**
- [✅] Descrições objetivas (não subjetivas): ✓
- [✅] Iluminação descrita por cena: ✓
- [✅] Mood descrito por cena: ✓
- [✅] Movimentos realistas AI-friendly: ✓
- [✅] Sem close extremo em rostos: ✓
- [✅] Sem efeitos impossíveis: ✓

**Validação Técnica:**
- [✅] Movimentos camera ALLOWED: ✓
- [✅] Transições RECOMMENDED: ✓
- [✅] Lighting objetivo: ✓
- [✅] Sem música copyrighted: ✓
- [✅] Sem texto em vídeo (post-production only): ✓

**Validação Meta-Prompt:**
- [✅] Usa [VARIAVEL] placeholder: ✓
- [✅] Genérico para categoria: ✓
- [✅] Lacunas intencionais: ✓
- [✅] Copy-paste ready: ✓

**Compliance Score:** ✅ PASS (20/20 checks)

---

## NOTAS DE PÓS-PRODUÇÃO

**Áudio:**
- [ ] Adicionar música de fundo (royalty-free)
- [ ] Adicionar sound effects sutis (ventosas aderindo, zoom produto)
- [ ] Masterizar volume (normalização)

**Texto/CTA:**
- [ ] Adicionar CTA textual na Cena 8: "Compre Agora" ou "Saiba Mais"
- [ ] Adicionar legendas (opcional para acessibilidade)
- [ ] Adicionar logo da marca (canto superior direito)

**Finalização:**
- [ ] Color grading (ajuste de cor para consistência)
- [ ] Transições finais (se necessário suavizar)
- [ ] Export 1080×1920, 24fps, H.264, high quality

```

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 8: TIMING & RHYTHM FRAMEWORK
## ═══════════════════════════════════════════════════════════════════════════

### [RHYTHM_RULE_3_5_7]
Purpose: Guide scene duration based on emotional intensity

**Rule:**
- **Fast-paced scenes (3-5s):** Hook, CTA — quick impact
- **Mid-paced scenes (5-7s):** Solution, Benefits — demonstration clarity
- **Slow-paced scenes (6-8s):** Emotional moments, Transformation — let feeling breathe

**Application:**
- Cena 1 (Hook): 3-5s ✓
- Cena 2 (Solution): 5-7s ✓
- Cenas 3-4 (Demo): 8-12s total (4-5s + 6-8s) ✓
- Cena 5 (Functional Benefit): 5-7s ✓
- Cena 6 (Emotional Benefit): 5-7s (slower for emotion) ✓
- Cena 7 (Transformation): 5-7s ✓
- Cena 8 (CTA): 3-5s ✓

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 9: FALLBACK STRATEGIES
## ═══════════════════════════════════════════════════════════════════════════

### [FALLBACK_INCOMPLETE_INPUT]
If input is incomplete or missing key fields:

**Strategy:**
1. Focus on generic visual product demonstration
2. Use simplified structure: Reveal → Demo → Benefit → CTA (4-5 scenes minimum)
3. Reduce to 30-35s duration
4. Alert in notes that script is generic due to missing input
5. NEVER invent product features that don't exist

**Minimal Structure:**
- Cena 1: Product reveal (hero shot)
- Cena 2: Installation/setup demonstration
- Cena 3: Product in use
- Cena 4: Benefit visual proof
- Cena 5: CTA hero shot

**Duration:** 25-35s (shorter due to lack of narrative depth)

### [FALLBACK_AI_PLATFORM_SPECIFIC]
If target platform has known limitations, adjust accordingly:

**For Pika 1.5** (prefers shorter scenes):
- Reduce each scene to 4-6s maximum
- Increase scene count to 8-9 (more cuts)
- Avoid scenes >8s

**For Runway Gen-3** (excels at static shots):
- Prioritize static camera or slow movements
- Reduce reliance on fast pans
- Emphasize cinematic lighting

**For VEO3** (good with motion):
- Allow longer scenes (7-10s)
- Use smooth camera movements (orbit, dolly)
- Reduce scene count to 6-7 (less cuts)

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 10: RELATIONSHIP TO OTHER MODULES
## ═══════════════════════════════════════════════════════════════════════════

### [UPSTREAM_INPUTS]
**From**: `input_parser_HOP.md`
- Research notes with pain points, benefits, context
- Product identity and differentiators

**From**: `bullet_points_estrategicos_HOP.md`
- 10 magnetic bullet points (can inspire scene content)

**From**: `descricao_builder_HOP.md`
- Narrative text that can inspire visual storytelling

**From**: User Brief
- `[VARIAVEL]` (product name)
- `[CATEGORIA]` (category for mood adaptation)

### [DOWNSTREAM_OUTPUTS]
**To**: Final Output (`PROMPT_VEO3` block)
- 6-9 scene video script with full specs
- Copy-paste ready prompts for AI video generation
- Post-production notes

**To**: `qa_validation_HOP.md`
- Script for compliance validation
- Metadata for audit trail

---

## ═══════════════════════════════════════════════════════════════════════════
## SECTION 11: CRITICAL SUCCESS FACTORS
## ═══════════════════════════════════════════════════════════════════════════

### [SUCCESS_CRITERIA]
1. **Universal Applicability**: Script works for ANY product/service (not hardcoded)
2. **AI-Generatable**: All visual descriptions are objective and realistic for AI
3. **Copy-Paste Ready**: No preprocessing needed by user
4. **Narrative Completeness**: All 7 elements present (Problem → CTA)
5. **Duration Compliance**: 30-60 seconds total
6. **Technical Compliance**: Camera movements, lighting, transitions are AI-friendly
7. **Emotional Arc**: Clear progression from frustration → solution → satisfaction
8. **Mobile-First**: 9:16 vertical format optimized for Stories/Reels/Shorts

### [FAILURE_MODES_TO_AVOID]
- ❌ Hardcoding specific product details (breaks universality)
- ❌ Subjective descriptions ("beautiful", "amazing") — AI cannot interpret
- ❌ Impossible camera movements (360° orbit, extreme zooms)
- ❌ Extreme close-ups on human faces (AI limitation)
- ❌ Complex acrobatics or unrealistic physics (AI cannot generate)
- ❌ Missing narrative elements (incomplete story)
- ❌ Total duration <30s or >60s (out of spec)
- ❌ Scenes <3s or >10s (pacing issues)

---

**END OF MODULE: video_script_veo3_HOP.md**
**Version**: 2.1.0
**Framework**: HOP (Hierarchical Operational Protocol)
**Status**: PRODUCTION-READY
**Last Updated**: 2025-11-10
