# 40_brand_validator_HOP.md | photo_agent - Brand & Compliance Validation

**Version**: 2.0.0
**Type**: HOP (Higher-Order Prompt)
**Status**: Integrated with ADW Workflow v2.0.0
**Last Updated**: 2025-11-17
**Integrated with**: workflows/100_ADW_RUN_PHOTO.md

**Purpose**: Validate brand consistency, marketplace compliance, and calculate quality score
**Input**: Phase 3 output (9 AI prompts generated)
**Output**: Validated prompts + quality score (≥7.0/10) + compliance report
**Estimated Duration**: 3-7 minutes

---

## OBJECTIVE

Validate that all 9 AI prompts maintain brand consistency, comply with marketplace-specific requirements (Mercado Livre, Shopee, TikTok), meet technical standards (resolution, file size, format), and achieve minimum quality score of 7.0/10 across technical, compositional, and brand dimensions.

---

## CONTEXT REQUIREMENTS

**Before executing this prompt, ensure:**
- Phase 3 completed: 9 AI prompts generated (≥80 words each)
- Brand guidelines available (if provided in Phase 1, else use generic e-commerce standards)
- Marketplace rules loaded:
  - Mercado Livre: White bg, no watermarks, 85%+ product visibility, resolution ≥1200px
  - Shopee: Max 9 images, lifestyle allowed, clear product visibility
  - TikTok: Vertical 9:16, engaging first frame, motion-friendly
- Quality scoring rubric defined (Technical 0-10, Composition 0-10, Brand 0-10)

---

## INSTRUCTIONS

### Step 1: Check Brand Consistency

**Validate alignment with brand guidelines across all 9 prompts:**

#### **A. Color Palette Consistency**

**If brand guidelines provided:**
1. Extract brand colors from Phase 1 (e.g., "navy blue #1A2B3C, gold #D4AF37, white #FFFFFF")
2. Verify each prompt references brand colors:
   - Check subject description for color mentions
   - Check background/props for color coordination
   - Ensure no conflicting colors (e.g., brand is blue but prompt uses red)

**Validation:**
- ✅ All prompts use brand colors (or compatible neutrals)
- ⚠️ Warn if prompt uses off-brand colors: "Scene 4 uses 'bright orange' but brand palette is blue/gold/white. Adjust to brand colors."

**If no brand guidelines:**
- Use generic e-commerce best practices:
  - Hero shots (1-3): White/neutral backgrounds
  - Lifestyle (4-5): Natural tones (wood, beige, gray)
  - Details (7-9): Clean backgrounds (white, light gray)

---

#### **B. Style Consistency**

**Verify all prompts match photography style from Phase 1:**

**Style Attributes to Check:**

| Style | Expected Keywords | Background | Mood |
|-------|-------------------|------------|------|
| Minimalist | clean, simple, white space, neutral | White, plain | Calm, professional |
| Lifestyle | natural, cozy, warm, contextual | Natural environments | Inviting, relatable |
| Commercial | professional, balanced, polished | Gradient, studio | Trustworthy, quality |
| Editorial | artistic, dramatic, creative | Dark, textured | Luxurious, exclusive |

**Validation:**
- ✅ All prompts contain style-appropriate keywords
- ⚠️ Warn if style mismatch: "Scene 2 uses 'dramatic dark background' but style is minimalist (requires white/neutral). Adjust to match minimalist aesthetic."

---

#### **C. Brand Personality Alignment**

**Check mood/PNL triggers match brand personality:**

**Brand Personality Types:**
- **Modern/Tech**: Keywords: sleek, innovative, cutting-edge, futuristic, minimalist
- **Playful/Fun**: Keywords: vibrant, colorful, energetic, cheerful, dynamic
- **Luxury/Premium**: Keywords: elegant, sophisticated, exclusive, refined, prestigious
- **Eco-Conscious**: Keywords: natural, organic, sustainable, earthy, authentic
- **Traditional**: Keywords: classic, timeless, heritage, crafted, reliable

**Validation:**
- ✅ PNL triggers in prompts align with brand personality
- ⚠️ Warn if personality mismatch: "Scene 5 uses 'playful, vibrant' but brand is luxury/premium. Replace with 'elegant, sophisticated'."

**If no brand personality specified:**
- Default to "trustworthy, professional, high-quality" (universal e-commerce safe)

---

### Step 2: Validate Marketplace Compliance

**Check each prompt against platform-specific rules:**

#### **A. Mercado Livre (Scene 1 - Main Image)**

**Requirements:**
1. **Background**: Pure white (#FFFFFF), no gradients/textures
2. **Product Visibility**: 85%+ of frame (product must be prominent)
3. **No Watermarks**: No logos, text overlays, borders, frames
4. **No Text**: Product name/price cannot be in image
5. **Resolution**: Minimum 1200 x 1200px (square) or 1200px shortest side
6. **File Size**: <5MB (ideally 1-3MB)
7. **Format**: JPG or PNG (JPG preferred for photos)
8. **Focus**: Product sharp and clear (no blur)

**Validation for Scene 1:**
```markdown
✅ White background mentioned: "[prompt contains 'pure white background' or 'white studio background']"
✅ Product prominence: "[prompt mentions 'centered', 'occupies 85% of frame', or similar]"
✅ No watermarks: "[prompt does NOT mention logos, watermarks, text]"
✅ Sharpness: "[camera specs include f/8+ aperture for deep DOF]"
```

**Error Handling:**
- ❌ If white bg missing → **HALT**: "Scene 1 (ML main) missing white background requirement. Add: 'pure white studio background (#FFFFFF), product isolated'"
- ❌ If watermark mentioned → **HALT**: "Scene 1 cannot have watermarks (ML policy violation). Remove any logo/text overlay references."
- ⚠️ If product <85% frame → **WARN**: "Scene 1 may have too much negative space. Ensure product is prominent (85%+ of frame)."

---

#### **B. Shopee (Scenes 2, 4, 5 - Carousel)**

**Requirements:**
1. **Image Count**: Max 9 images total (we have 9 scenes, perfect fit)
2. **Lifestyle Allowed**: Props, environments, models permitted
3. **Product Visibility**: Product must be clearly visible (50%+ of frame)
4. **Engaging**: Thumbnail (Scene 2) should be eye-catching (angled, dimensional)
5. **Resolution**: Min 800 x 800px (1200px+ recommended)
6. **Aspect Ratio**: Square (1:1) or portrait (3:4)
7. **No Explicit Content**: No violence, nudity, offensive imagery

**Validation for Scenes 2, 4, 5:**
```markdown
✅ Scene 2 engaging angle: "[prompt has '45°', 'angled', 'dimensional']"
✅ Scene 4 lifestyle context: "[prompt has props, environment, 'lifestyle']"
✅ Scene 5 use case: "[prompt shows product being used, 'hand', 'wearing']"
✅ Product visible: "[all prompts ensure product is main focus]"
```

**Error Handling:**
- ⚠️ If Scene 2 not engaging → **WARN**: "Scene 2 (Shopee thumbnail) is straight-on. Change to 45° angle for more engaging thumbnail."
- ⚠️ If product hidden → **WARN**: "Scene 4 has too many props. Ensure product is still 50%+ visible."

---

#### **C. TikTok (Scene 5 - Vertical Video Still)**

**Requirements:**
1. **Aspect Ratio**: 9:16 vertical (1080 x 1920px)
2. **First Frame**: Eye-catching (scene must work as thumbnail)
3. **Natural Feel**: Authentic, not overly staged (lifestyle > studio)
4. **Motion-Friendly**: Composition allows for movement (if video)
5. **Bright**: Well-lit, visible (avoid dark/moody for TikTok)
6. **Text Space**: Leave room for captions (top/bottom thirds)

**Validation for Scene 5:**
```markdown
✅ Vertical format: "[prompt mentions '9:16', 'vertical', 'portrait orientation']"
✅ Natural/authentic: "[prompt has 'natural light', 'lifestyle', 'authentic']"
✅ Eye-catching: "[prompt has 'dynamic', 'engaging', 'energetic']"
✅ Bright lighting: "[lighting is natural/ambient, not dark]"
```

**Error Handling:**
- ❌ If not vertical → **HALT**: "Scene 5 (TikTok) must be 9:16 vertical. Add: 'vertical 9:16 aspect ratio, portrait orientation'."
- ⚠️ If overly staged → **WARN**: "Scene 5 too studio-like for TikTok. Use natural light and authentic pose."

---

### Step 3: Verify Technical Requirements

**Check that prompts will generate technically compliant images:**

#### **A. Resolution Requirements**

**Minimum Resolutions by Platform:**
- Mercado Livre: 1200 x 1200px (square) or 1200px shortest side
- Shopee: 800 x 800px (min), 1200px+ recommended
- TikTok: 1080 x 1920px (9:16 vertical)
- Instagram: 1080 x 1080px (square) or 1080 x 1350px (portrait)

**Validation:**
- ✅ All prompts include "8K resolution" or "4K" or "high resolution" keywords
- ✅ Scene 5 (TikTok) specifies "1080 x 1920px" or "9:16 vertical"
- ✅ Scene 1 (ML) implies square/standard format (1200px+)

**Error Handling:**
- ⚠️ If no resolution mentioned → **WARN**: "Add resolution keywords: 'ultra-sharp 8K resolution' or '4K professional quality'."

---

#### **B. File Format & Size**

**Requirements:**
- Format: JPG (photos), PNG (graphics with transparency)
- File Size: <5MB (ML strict), <10MB (Shopee), <30MB (TikTok)
- Compression: Balance quality vs file size (aim for 1-3MB per image)

**Validation:**
- ✅ Prompts don't specify format (AI generators auto-export JPG/PNG)
- ✅ High quality keywords present ("studio quality", "commercial photography")
- ℹ️ Note: File size managed post-generation (not in prompt)

---

#### **C. Image Quality (Sharpness, Grain, Exposure)**

**Requirements:**
- Sharpness: No blur (unless intentional background bokeh)
- Grain: Minimal noise (ISO 100-400 preferred)
- Exposure: Properly lit (not overexposed/underexposed)
- Color Accuracy: True-to-life colors (no heavy filters)

**Validation:**
- ✅ Camera specs use low ISO (100-400) for clean images
- ✅ Aperture appropriate (f/8+ for hero, f/2.8-f/5.6 for lifestyle)
- ✅ Prompts include sharpness keywords ("ultra-sharp", "crisp focus", "hyper-realistic")
- ✅ Lighting adequate (studio/soft box for controlled, natural for lifestyle)

**Error Handling:**
- ⚠️ If high ISO (1600+) → **WARN**: "Scene 4 has ISO 1600 (potential grain). Acceptable for lifestyle, but note possible noise."
- ⚠️ If wide aperture (f/1.8) + deep DOF claim → **CONFLICT**: "Scene X has f/1.8 but claims 'everything sharp'. Use f/8+ for deep DOF."

---

### Step 4: Calculate Quality Score (Technical + Composition + Brand)

**Score each prompt on 3 dimensions (0-10 scale), then average:**

#### **A. Technical Score (0-10)**

**Criteria:**
1. Camera specs complete and accurate (2 pts)
2. Lighting design appropriate for scene (2 pts)
3. ISO range appropriate (100-400 for hero, 800+ okay for lifestyle) (2 pts)
4. Aperture matches DOF intent (f/8+ for sharp, f/2.8-f/4 for bokeh) (2 pts)
5. Resolution keywords present (8K, 4K, high-res) (2 pts)

**Scoring:**
- 9-10: Perfect technical execution
- 7-8: Minor technical issues (e.g., slightly high ISO)
- 5-6: Moderate issues (missing specs, incorrect settings)
- 0-4: Major issues (impossible settings, incomplete specs)

---

#### **B. Composition Score (0-10)**

**Criteria:**
1. Compositional technique mentioned (rule of thirds, centered, etc.) (2 pts)
2. Framing appropriate for scene type (hero centered, lifestyle off-center) (2 pts)
3. Negative space used effectively (2 pts)
4. Angle/perspective matches scene purpose (2 pts)
5. Visual balance (subject, props, background proportions) (2 pts)

**Scoring:**
- 9-10: Excellent composition, professional framing
- 7-8: Good composition, minor improvements possible
- 5-6: Adequate composition, some awkward framing
- 0-4: Poor composition, unbalanced or confusing

---

#### **C. Brand Score (0-10)**

**Criteria:**
1. Brand colors consistent (or appropriate neutrals) (2 pts)
2. Photography style matches brand personality (2 pts)
3. PNL triggers align with brand voice (2 pts)
4. Mood/emotion appropriate for brand (2 pts)
5. Marketplace compliance for brand context (2 pts)

**Scoring:**
- 9-10: Perfect brand alignment, no deviations
- 7-8: Good brand fit, minor inconsistencies
- 5-6: Some brand misalignment (wrong colors/mood)
- 0-4: Major brand conflicts (completely off-brand)

---

#### **D. Calculate Average Score**

**Formula:**
```
Quality Score = (Technical Score + Composition Score + Brand Score) / 3
```

**Requirement:**
- **Minimum**: 7.0/10 average to pass validation
- **Target**: 8.0/10+ for high-quality output
- **Excellent**: 9.0/10+ for professional-grade

**Validation:**
- ✅ Quality Score ≥7.0 → PASS (proceed to Phase 5)
- ⚠️ Quality Score 6.0-6.9 → WARN (acceptable but recommend improvements)
- ❌ Quality Score <6.0 → FAIL (must revise prompts before Phase 5)

---

### Step 5: Generate Validation Report

**Create comprehensive validation output:**

```markdown
## PHASE 4 OUTPUT: Brand & Compliance Validation

### Brand Consistency Check
- **Color Palette**: ✅ Consistent (brand colors: white, wood, gold across all scenes)
- **Photography Style**: ✅ Minimalist style maintained (clean, simple, white space)
- **Brand Personality**: ✅ Aligned (professional, trustworthy, Scandinavian aesthetic)
- **Overall Brand Consistency**: ✅ PASS

### Marketplace Compliance

#### Mercado Livre (Scene 1)
- ✅ White background: Present ("pure white background #FFFFFF")
- ✅ Product visibility: 85% of frame (mentioned in prompt)
- ✅ No watermarks: Confirmed (no text overlays)
- ✅ Resolution: 8K keywords present
- ✅ Sharpness: f/8 aperture (deep DOF)
- **Status**: ✅ COMPLIANT

#### Shopee (Scenes 2, 4, 5)
- ✅ Scene 2 engaging: 45° angle (dimensional thumbnail)
- ✅ Scene 4 lifestyle: Context with props (desk, book)
- ✅ Scene 5 use case: Hand holding mug (functionality)
- ✅ Product visible: All scenes 50%+ product visibility
- **Status**: ✅ COMPLIANT

#### TikTok (Scene 5)
- ✅ Vertical format: 9:16 aspect ratio mentioned
- ✅ Natural feel: Natural lighting, authentic pose
- ✅ Eye-catching: Dynamic composition
- ✅ Bright: Well-lit (4000K ambient)
- **Status**: ✅ COMPLIANT

### Technical Requirements
- ✅ Resolution: All prompts include "8K" or "ultra-sharp" keywords
- ✅ Format: Standard JPG/PNG (auto-generated by AI)
- ✅ Quality: Low ISO (100-400 for heroes, 800 for lifestyle acceptable)
- ✅ Sharpness: Appropriate apertures (f/8 hero, f/2.8-f/5.6 lifestyle)
- **Status**: ✅ PASS

### Quality Scores (by Scene)

| Scene | Technical | Composition | Brand | Average | Status |
|-------|-----------|-------------|-------|---------|--------|
| 1 - Front View | 10/10 | 9/10 | 10/10 | **9.7** | ✅ Excellent |
| 2 - 45° Angle | 9/10 | 9/10 | 9/10 | **9.0** | ✅ Excellent |
| 3 - Top-Down | 9/10 | 8/10 | 9/10 | **8.7** | ✅ Great |
| 4 - Lifestyle | 8/10 | 9/10 | 9/10 | **8.7** | ✅ Great |
| 5 - Use Case | 8/10 | 8/10 | 8/10 | **8.0** | ✅ Great |
| 6 - Scale Ref | 9/10 | 8/10 | 9/10 | **8.7** | ✅ Great |
| 7 - Texture | 9/10 | 9/10 | 9/10 | **9.0** | ✅ Excellent |
| 8 - Feature | 9/10 | 9/10 | 9/10 | **9.0** | ✅ Excellent |
| 9 - Branding | 10/10 | 9/10 | 9/10 | **9.3** | ✅ Excellent |

**Overall Average Quality Score**: **8.9/10** ✅ EXCELLENT

### Validation Summary
- ✅ Brand Consistency: PASS
- ✅ Marketplace Compliance: PASS (ML, Shopee, TikTok)
- ✅ Technical Requirements: PASS
- ✅ Quality Score: 8.9/10 (exceeds 7.0 minimum)
- ✅ Ready for Phase 5: Batch Assembly & QA

---
**Phase 4 Duration**: [X minutes]
**Status**: ✅ COMPLETE
**Next Phase**: Phase 5 - Batch Assembly & QA (use 50_batch_assembler_HOP.md)
```

---

## OUTPUT FORMAT

**Complete Phase 4 validation report structure shown above, including:**
1. Brand Consistency Check (colors, style, personality)
2. Marketplace Compliance (ML, Shopee, TikTok rules)
3. Technical Requirements (resolution, format, quality)
4. Quality Scores (per scene + overall average)
5. Validation Summary (pass/fail status)

---

## VALIDATION CHECKLIST

**Before proceeding to Phase 5, confirm:**
- ✅ Brand consistency verified (colors, style, personality aligned)
- ✅ Marketplace compliance checked (ML, Shopee, TikTok rules met)
- ✅ Technical requirements validated (resolution, ISO, aperture, sharpness)
- ✅ Quality scores calculated (Technical + Composition + Brand per scene)
- ✅ Overall quality score ≥7.0/10 (minimum passing threshold)
- ✅ Validation report generated (structured markdown output)
- ✅ No critical blockers (if any failures, prompts must be revised)

---

## ERROR HANDLING

### Common Issues & Solutions

**Issue 1: Brand Color Mismatch**
- **Error**: "Scene 4 uses 'bright orange props' but brand colors are blue/white/gold"
- **Solution**: Revise Scene 4 prompt to replace orange with brand-compliant colors:
  - "Replace 'bright orange notebook' with 'navy blue notebook (brand color)' to maintain brand consistency"

**Issue 2: Mercado Livre Non-Compliance**
- **Error**: "Scene 1 missing white background requirement (critical ML violation)"
- **Solution**: Add white bg to Scene 1 prompt:
  - Insert: "pure white studio background (#FFFFFF), product isolated with no shadows, Mercado Livre marketplace compliant"

**Issue 3: TikTok Format Missing**
- **Error**: "Scene 5 doesn't specify 9:16 vertical format (TikTok requirement)"
- **Solution**: Add aspect ratio to Scene 5 prompt:
  - Append: "vertical 9:16 aspect ratio optimized for TikTok video stills, portrait orientation"

**Issue 4: Quality Score Too Low (<7.0)**
- **Error**: "Scene 6 quality score: 6.2/10 (Technical: 5/10, Composition: 7/10, Brand: 7/10)"
- **Analysis**: Technical score low (5/10) → likely missing camera specs or incorrect settings
- **Solution**: Review Scene 6 prompt:
  - Add missing camera specs (lens, aperture, ISO, shutter)
  - Fix any impossible settings (e.g., f/0.5 → f/1.8 or f/5.6)
  - Add resolution keywords ("8K resolution", "ultra-sharp")
  - Recalculate score (should reach 7+ after fixes)

**Issue 5: Style Inconsistency Across Prompts**
- **Error**: "Scenes 1-3 are minimalist (white bg, clean) but Scene 4 has 'dark moody background' (editorial style)"
- **Solution**: Align Scene 4 with minimalist style:
  - Replace "dark moody background" with "clean natural environment, light wood table, neutral tones"
  - Ensure all 9 scenes reflect the same photography style from Phase 1

**Issue 6: PNL Triggers Misaligned with Brand**
- **Error**: "Scene 2 uses 'playful, vibrant, fun' but brand personality is luxury/premium"
- **Solution**: Replace PNL triggers with brand-appropriate keywords:
  - Change "playful, vibrant, fun" to "elegant, sophisticated, premium, refined"
  - Ensure all scenes use triggers matching brand personality

---

## EXAMPLES

### Example 1: Full Validation Report (Minimalist Ceramic Mug)

**Input**: 9 prompts for matte white ceramic mug (minimalist style, Hygge brand)

**Output:**

```markdown
## PHASE 4 OUTPUT: Brand & Compliance Validation

### Brand Consistency Check
- **Color Palette**: ✅ Consistent
  - Brand: White #FFFFFF, Wood (natural), Gold #D4AF37
  - Prompts: All use white mug, wood handle, gold accent, white/neutral backgrounds
  - No off-brand colors detected

- **Photography Style**: ✅ Minimalist maintained
  - Expected: Clean, simple, white space, neutral tones
  - Prompts: All include "minimalist", "clean", "white background", "simple composition"

- **Brand Personality**: ✅ Aligned (Scandinavian aesthetic)
  - Expected: Professional, trustworthy, calm, quality
  - Prompts: Use "Scandinavian elegance", "professional", "high-quality craftsmanship"

- **Overall Brand Consistency**: ✅ PASS

### Marketplace Compliance

#### Mercado Livre (Scene 1 - Main Image)
- ✅ White background: "pure white studio background (#FFFFFF)"
- ✅ Product visibility: "product occupies 85% of frame"
- ✅ No watermarks: No text/logo overlays mentioned
- ✅ Resolution: "8K resolution" keyword present
- ✅ Sharpness: Camera f/8 aperture (deep DOF)
- **Compliance**: ✅ FULLY COMPLIANT

#### Shopee (Scenes 2, 4, 5)
- ✅ Scene 2: "45-degree angle" (engaging thumbnail)
- ✅ Scene 4: "mug on wooden desk with book" (lifestyle context)
- ✅ Scene 5: "hand holding mug" (use case demo)
- ✅ All scenes: Product clearly visible (50%+)
- **Compliance**: ✅ FULLY COMPLIANT

#### TikTok (Scene 5)
- ✅ Vertical format: "9:16 aspect ratio"
- ✅ Natural feel: "natural ambient lighting", "authentic lifestyle moment"
- ✅ Eye-catching: "dynamic composition"
- ✅ Bright: "4000K neutral daylight" (well-lit)
- **Compliance**: ✅ FULLY COMPLIANT

### Technical Requirements
- ✅ Resolution: All prompts include "8K" or "ultra-sharp 4K"
- ✅ Format: Standard (AI auto-exports JPG/PNG)
- ✅ ISO: Scenes 1-3 (100), 4-6 (400-800), 7-9 (200) - all appropriate
- ✅ Aperture: Hero f/8+ (sharp), lifestyle f/2.8-f/4 (bokeh), macro f/5.6-f/8
- ✅ Sharpness keywords: "ultra-sharp", "hyper-realistic", "crisp focus"
- **Technical Validation**: ✅ PASS

### Quality Scores

| Scene | Tech | Comp | Brand | Avg | Notes |
|-------|------|------|-------|-----|-------|
| 1 - Front | 10 | 9 | 10 | 9.7 | Perfect ML compliance |
| 2 - 45° | 9 | 9 | 9 | 9.0 | Excellent depth |
| 3 - Top | 9 | 8 | 9 | 8.7 | Strong flat lay |
| 4 - Lifestyle | 8 | 9 | 9 | 8.7 | Great context |
| 5 - Use Case | 8 | 8 | 8 | 8.0 | Good demo |
| 6 - Scale | 9 | 8 | 9 | 8.7 | Clear comparison |
| 7 - Texture | 9 | 9 | 9 | 9.0 | Excellent macro |
| 8 - Feature | 9 | 9 | 9 | 9.0 | Great detail |
| 9 - Branding | 10 | 9 | 9 | 9.3 | Perfect auth |

**Overall Average**: **8.9/10** ✅ EXCELLENT (exceeds 7.0 minimum)

### Validation Summary
- ✅ Brand Consistency: PASS (all colors, style, personality aligned)
- ✅ Marketplace Compliance: PASS (ML, Shopee, TikTok all compliant)
- ✅ Technical Requirements: PASS (resolution, ISO, aperture correct)
- ✅ Quality Score: 8.9/10 ✅ EXCELLENT (far exceeds 7.0 threshold)
- ✅ **STATUS**: Ready for Phase 5 - Batch Assembly & QA

---
**Phase 4 Duration**: 5 minutes
**Status**: ✅ COMPLETE - NO REVISIONS NEEDED
**Next Phase**: Phase 5 - Batch Assembly & QA (use 50_batch_assembler_HOP.md)
```

---

### Example 2: Validation with Issues (Requires Fixes)

**Scenario**: Quality score below 7.0 for Scene 6, ML non-compliance for Scene 1

**Output:**

```markdown
## PHASE 4 OUTPUT: Brand & Compliance Validation

### Marketplace Compliance

#### Mercado Livre (Scene 1)
- ❌ White background: NOT MENTIONED (critical violation)
- ✅ Product visibility: "centered composition" (okay)
- ✅ No watermarks: Confirmed
- ✅ Resolution: "8K" present
- ⚠️ Sharpness: f/5.6 aperture (should be f/8+ for ML)
- **Status**: ❌ NON-COMPLIANT - REVISIONS REQUIRED

**Required Fixes for Scene 1:**
1. Add: "pure white studio background (#FFFFFF), product isolated"
2. Change aperture: f/5.6 → f/8 (for deeper DOF)
3. Add: "Mercado Livre marketplace compliant, no shadows"

### Quality Scores

| Scene | Tech | Comp | Brand | Avg | Status |
|-------|------|------|-------|-----|--------|
| 1 | 7 | 8 | 9 | 8.0 | ⚠️ ML fixes needed |
| 6 | 5 | 7 | 7 | 6.3 | ❌ Below 7.0 |

**Scene 6 Issues (Quality: 6.3/10)**:
- Technical: 5/10 - Missing shutter speed, ISO not specified
- Composition: 7/10 - Adequate but could improve framing
- Brand: 7/10 - Colors okay but lacks brand personality keywords

**Required Fixes for Scene 6:**
1. Add camera specs: "50mm lens, f/5.6 aperture, ISO 400, 1/125s shutter"
2. Improve composition: "Rule of thirds with mug and phone balanced in frame"
3. Add brand keywords: "professional product photography, Scandinavian minimalist aesthetic"
4. Recalculate expected score: Technical 8/10, Comp 8/10, Brand 8/10 → **8.0/10** ✅

### Validation Summary
- ✅ Brand Consistency: PASS
- ❌ Marketplace Compliance: FAIL (Scene 1 ML non-compliant)
- ⚠️ Quality Score: Scene 6 at 6.3/10 (below 7.0 minimum)
- ❌ **STATUS**: REVISIONS REQUIRED BEFORE PHASE 5

**Action Items:**
1. Fix Scene 1: Add white bg + f/8 aperture + ML compliance statement
2. Fix Scene 6: Add missing camera specs + improve composition description
3. Re-run Phase 4 validation after fixes
4. Proceed to Phase 5 only after all scenes ≥7.0/10 and ML compliant

---
**Phase 4 Duration**: 6 minutes
**Status**: ⚠️ INCOMPLETE - REVISIONS IN PROGRESS
**Next Step**: Fix Scenes 1 & 6, then re-validate
```

---

## NOTES FOR LLM EXECUTION

1. **Quality Score Philosophy**:
   - Be strict but fair (7.0 is "good", 8.0 is "great", 9.0+ is "excellent")
   - Technical score: Objective (specs correct = points)
   - Composition score: Slightly subjective (professional judgment)
   - Brand score: Objective if brand guidelines provided, else generic e-commerce standards

2. **Marketplace Priority Enforcement**:
   - **Mercado Livre (Scene 1)**: CRITICAL - white bg is non-negotiable (major traffic source)
   - **Shopee (Scenes 2, 4, 5)**: Important but flexible (lifestyle allowed)
   - **TikTok (Scene 5)**: Format critical (9:16 vertical), style flexible

3. **Validation Efficiency**:
   - Run all checks in one pass (don't require multiple iterations)
   - Flag all issues at once (batch feedback, not sequential)
   - Provide specific fix instructions (actionable guidance)

4. **No Brand Guidelines Fallback**:
   - Use generic e-commerce best practices
   - Default colors: White, neutral, clean
   - Default personality: Professional, trustworthy, quality
   - Default style: Commercial/minimalist (safest for marketplaces)

5. **Pass Threshold Flexibility**:
   - 7.0-7.9: Good (acceptable, proceed)
   - 6.0-6.9: Borderline (warn but may proceed if minor issues)
   - <6.0: Fail (must revise before Phase 5)

---

**End of 40_brand_validator_HOP.md**
