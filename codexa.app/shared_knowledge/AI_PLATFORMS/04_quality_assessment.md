# Quality Assessment | shared_knowledge

**Purpose**: Framework for evaluating AI-generated outputs
**Version**: 1.0.0 | **Updated**: 2025-12-05
**Quality Score**: 0.86/1.00

---

## OVERVIEW

This knowledge card provides a comprehensive framework for assessing the quality of AI-generated images, videos, and audio. Defines scoring criteria, thresholds, and review processes to ensure consistent output quality.

**Philosophy**: Quality gates prevent bad outputs from reaching production.

---

## QUALITY DIMENSIONS

### Universal Dimensions (All Media)

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Technical Quality | 30% | Resolution, artifacts, sharpness |
| Prompt Adherence | 25% | Does output match the prompt? |
| Brand Alignment | 20% | Consistent with brand guidelines |
| Commercial Viability | 15% | Usable for intended purpose |
| Aesthetic Appeal | 10% | Subjective visual quality |

### Total Score Formula

```
SCORE = (Technical * 0.30) + (Adherence * 0.25) + (Brand * 0.20) +
        (Commercial * 0.15) + (Aesthetic * 0.10)
```

**Quality Threshold**: >= 7.0/10.0 for production use

---

## IMAGE QUALITY ASSESSMENT

### Technical Quality Checklist

| Criterion | Pass | Fail |
|-----------|------|------|
| Resolution meets spec | >= 1024px | < 1024px |
| No visible artifacts | Clean | Blur, noise, compression |
| Proper aspect ratio | Matches request | Distorted |
| Color accuracy | Natural, balanced | Over/undersaturated |
| Focus/sharpness | Subject sharp | Soft, blurry |
| Edge quality | Clean edges | Haloing, fringing |

**Common Image Artifacts to Check**:
```
- Blur/softness in subject
- Background bleeding into subject
- Unnatural hand/finger rendering
- Text distortion (if any)
- Repetitive patterns
- Color banding
- Over-smoothing (plastic look)
```

### Prompt Adherence Scoring

| Score | Description |
|-------|-------------|
| 10 | Perfect match to all prompt elements |
| 8-9 | Minor details missing or different |
| 6-7 | Major elements present, some wrong |
| 4-5 | Partial match, several errors |
| 1-3 | Does not match prompt intent |

**Evaluation Questions**:
- Is the subject correct?
- Is the environment/background as specified?
- Is the lighting as described?
- Are style elements present?
- Is the composition correct?

### Marketplace Image Requirements

#### Mercado Livre

| Requirement | Specification |
|-------------|---------------|
| Background | Pure white (#FFFFFF) |
| Minimum resolution | 500x500px |
| Optimal resolution | 1200x1200px |
| Format | JPG, PNG |
| Max file size | 10MB |
| Product coverage | 80-90% of frame |
| Text on image | Not allowed (main image) |

#### Shopee

| Requirement | Specification |
|-------------|---------------|
| Background | White or solid color |
| Minimum resolution | 500x500px |
| Optimal resolution | 800x800px |
| Format | JPG, PNG |
| Aspect ratio | 1:1 (square) |
| Watermarks | Not allowed |

#### Amazon BR

| Requirement | Specification |
|-------------|---------------|
| Background | Pure white (RGB 255,255,255) |
| Minimum resolution | 1000px (longest side) |
| Optimal resolution | 2000px+ |
| Format | JPEG, TIFF, PNG, GIF |
| Product coverage | 85%+ of frame |
| Props/accessories | Only if included in sale |

### Image Quality Scorecard

```markdown
## Image Quality Assessment

**File**: [filename]
**Platform**: [target platform]
**Date**: [assessment date]

### Scores (1-10)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Technical | __/10 | |
| Adherence | __/10 | |
| Brand | __/10 | |
| Commercial | __/10 | |
| Aesthetic | __/10 | |

### Weighted Total: __/10

### Issues Found:
- [ ] Issue 1
- [ ] Issue 2

### Verdict: PASS / FAIL / NEEDS REVISION
```

---

## VIDEO QUALITY ASSESSMENT

### Technical Video Checklist

| Criterion | Pass | Fail |
|-----------|------|------|
| Resolution | >= 1080p | < 720p |
| Frame rate | 24-60fps consistent | Variable, stuttering |
| Duration | Within platform spec | Too short/long |
| Motion quality | Smooth, natural | Jittery, warping |
| Audio sync | Perfect sync (if audio) | Out of sync |
| Compression | Clean | Blocking, banding |

**Common Video Artifacts**:
```
- Temporal flickering
- Object morphing/warping
- Unnatural motion (physics breaks)
- Hand/face distortion
- Background inconsistency
- Abrupt transitions
- Audio desync
```

### Motion Quality Scoring

| Score | Motion Quality |
|-------|----------------|
| 10 | Physically accurate, cinematic |
| 8-9 | Natural movement, minor issues |
| 6-7 | Acceptable, some unnatural moments |
| 4-5 | Noticeable issues, jarring |
| 1-3 | Broken physics, unwatchable |

### Platform-Specific Video Requirements

#### Instagram Reels

| Requirement | Specification |
|-------------|---------------|
| Aspect ratio | 9:16 (vertical) |
| Resolution | 1080x1920 |
| Duration | 15-90 seconds |
| Safe zones | Top 5%, Bottom 20% |
| Audio | Recommended |
| Captions | Auto-generated |

#### TikTok

| Requirement | Specification |
|-------------|---------------|
| Aspect ratio | 9:16 (vertical) |
| Resolution | 1080x1920 |
| Duration | 15-180 seconds |
| Safe zones | Top 10%, Bottom 25% |
| Audio | Required for engagement |
| Hooks | First 3 seconds critical |

#### YouTube Shorts

| Requirement | Specification |
|-------------|---------------|
| Aspect ratio | 9:16 (vertical) |
| Resolution | 1080x1920 |
| Duration | 15-60 seconds |
| Safe zones | Top 5%, Bottom 15% |
| Audio | Recommended |

#### YouTube (Standard)

| Requirement | Specification |
|-------------|---------------|
| Aspect ratio | 16:9 (horizontal) |
| Resolution | 1920x1080 minimum |
| Duration | No limit |
| Audio | Required |

### Video Quality Scorecard

```markdown
## Video Quality Assessment

**File**: [filename]
**Platform**: [target platform]
**Duration**: [seconds]
**Date**: [assessment date]

### Scores (1-10)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Technical | __/10 | |
| Motion | __/10 | |
| Adherence | __/10 | |
| Brand | __/10 | |
| Commercial | __/10 | |

### Weighted Total: __/10

### Timestamp Issues:
- 0:02 - [Issue description]
- 0:05 - [Issue description]

### Verdict: PASS / FAIL / NEEDS REVISION
```

---

## AUDIO QUALITY ASSESSMENT

### Technical Audio Checklist

| Criterion | Pass | Fail |
|-----------|------|------|
| Sample rate | >= 44.1kHz | < 22kHz |
| Bit depth | 16-24 bit | 8 bit |
| Noise level | Clean | Audible hiss/hum |
| Clipping | None | Distortion peaks |
| Consistency | Even volume | Jumps, drops |

### Voice Quality (TTS)

| Criterion | Score 8-10 | Score 5-7 | Score 1-4 |
|-----------|------------|-----------|-----------|
| Naturalness | Human-like | Slightly robotic | Obviously synthetic |
| Pronunciation | Perfect | Minor errors | Multiple errors |
| Pacing | Natural rhythm | Slightly off | Monotone/rushed |
| Emotion | Appropriate tone | Flat | Wrong tone |
| Clarity | Crystal clear | Understandable | Hard to understand |

### Audio Quality Scorecard

```markdown
## Audio Quality Assessment

**File**: [filename]
**Voice/Model**: [voice name]
**Duration**: [seconds]
**Date**: [assessment date]

### Scores (1-10)

| Dimension | Score | Notes |
|-----------|-------|-------|
| Technical | __/10 | |
| Naturalness | __/10 | |
| Clarity | __/10 | |
| Brand Voice | __/10 | |

### Total: __/10

### Issues:
- [ ] Issue 1
- [ ] Issue 2

### Verdict: PASS / FAIL / NEEDS REVISION
```

---

## BRAND ALIGNMENT ASSESSMENT

### Brand Consistency Checklist

| Element | Check |
|---------|-------|
| Color palette | Within brand colors |
| Typography style | Matches brand fonts (if text) |
| Tone/mood | Aligns with brand personality |
| Subject matter | Appropriate for brand |
| Quality level | Matches brand positioning |

### Brand Alignment Scoring Matrix

| Score | Description |
|-------|-------------|
| 10 | Perfect brand representation |
| 8-9 | Minor deviations, on-brand |
| 6-7 | Some off-brand elements |
| 4-5 | Significant misalignment |
| 1-3 | Does not represent brand |

### Brand Safety Checks

```
- [ ] No competitor logos/products visible
- [ ] No inappropriate content
- [ ] No unintended messages
- [ ] Cultural sensitivity (Brazil market)
- [ ] No trademark violations
- [ ] Age-appropriate content
```

---

## AUTOMATED QUALITY CHECKS

### Pre-Generation Validation

```python
def validate_prompt(prompt: str) -> dict:
    """Validate prompt before generation."""
    issues = []

    # Length check
    if len(prompt) < 20:
        issues.append("Prompt too short")
    if len(prompt) > 1000:
        issues.append("Prompt too long")

    # Required elements
    required = ["subject", "lighting", "style"]
    for element in required:
        if element not in prompt.lower():
            issues.append(f"Missing element: {element}")

    # Anti-patterns
    if "don't" in prompt.lower() or "no " in prompt.lower():
        issues.append("Contains negative instructions")

    return {
        "valid": len(issues) == 0,
        "issues": issues
    }
```

### Post-Generation Validation

```python
from PIL import Image

def validate_image(image_path: str, requirements: dict) -> dict:
    """Validate generated image against requirements."""
    img = Image.open(image_path)
    issues = []

    # Resolution check
    min_res = requirements.get("min_resolution", 1024)
    if min(img.size) < min_res:
        issues.append(f"Resolution too low: {img.size}")

    # Aspect ratio check
    target_ratio = requirements.get("aspect_ratio", 1.0)
    actual_ratio = img.width / img.height
    if abs(actual_ratio - target_ratio) > 0.1:
        issues.append(f"Wrong aspect ratio: {actual_ratio:.2f}")

    # File size check
    import os
    file_size = os.path.getsize(image_path)
    max_size = requirements.get("max_size_mb", 10) * 1024 * 1024
    if file_size > max_size:
        issues.append(f"File too large: {file_size / 1024 / 1024:.1f}MB")

    # Background color check (for marketplace)
    if requirements.get("white_background"):
        corners = [
            img.getpixel((0, 0)),
            img.getpixel((img.width-1, 0)),
            img.getpixel((0, img.height-1)),
            img.getpixel((img.width-1, img.height-1))
        ]
        for corner in corners:
            if corner[:3] != (255, 255, 255):
                issues.append("Background is not pure white")
                break

    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "metadata": {
            "size": img.size,
            "format": img.format,
            "mode": img.mode
        }
    }
```

---

## QUALITY GATE WORKFLOW

### Decision Tree

```
START: Output generated
        |
        v
   [Automated Checks]
        |
        +--- FAIL --> [Auto-retry?]
        |                  |
        |                  +--- Yes --> Regenerate (max 3x)
        |                  |
        |                  +--- No --> Flag for review
        |
        +--- PASS
              |
              v
       [Score >= 7.0?]
              |
              +--- No --> Manual review
              |
              +--- Yes
                    |
                    v
              [Brand Check]
                    |
                    +--- FAIL --> Revise prompt
                    |
                    +--- PASS --> Approve for use
```

### Batch Quality Processing

```python
def process_batch_quality(outputs: list, threshold: float = 7.0) -> dict:
    """Process quality for a batch of outputs."""
    results = {
        "passed": [],
        "failed": [],
        "needs_review": []
    }

    for output in outputs:
        score = calculate_quality_score(output)

        if score >= threshold:
            results["passed"].append(output)
        elif score >= threshold - 1.0:
            results["needs_review"].append(output)
        else:
            results["failed"].append(output)

    return {
        "results": results,
        "stats": {
            "total": len(outputs),
            "passed": len(results["passed"]),
            "pass_rate": len(results["passed"]) / len(outputs)
        }
    }
```

---

## HUMAN REVIEW CRITERIA

### When Human Review is Required

1. **Score 6.0-6.9**: Borderline quality
2. **Brand content**: Logos, faces, sensitive material
3. **New prompt templates**: First use validation
4. **Platform-specific**: Compliance verification
5. **High-value outputs**: Hero images, main videos

### Review Checklist for Humans

```markdown
## Human Review Checklist

**Output ID**: [id]
**Auto Score**: [score]/10
**Review Date**: [date]
**Reviewer**: [name]

### Visual Inspection
- [ ] Subject is correctly rendered
- [ ] No visible artifacts or distortions
- [ ] Lighting matches prompt
- [ ] Composition is appropriate
- [ ] Colors are accurate

### Brand Check
- [ ] Aligns with brand guidelines
- [ ] No inappropriate elements
- [ ] Suitable for target audience
- [ ] Marketplace compliant

### Commercial Viability
- [ ] Would use for paid advertising
- [ ] Represents product accurately
- [ ] Professional quality

### Final Decision
[ ] APPROVE - Ready for production
[ ] REVISE - Specific changes needed: ___________
[ ] REJECT - Regenerate with new prompt

### Notes:
[Free text notes]
```

---

## QUALITY METRICS & REPORTING

### Key Performance Indicators

| Metric | Target | Formula |
|--------|--------|---------|
| First-Pass Rate | >= 80% | Passed / Total |
| Average Score | >= 8.0 | Sum(Scores) / Count |
| Retry Rate | <= 20% | Retries / Total |
| Human Review Rate | <= 10% | Reviews / Total |
| Platform Rejection | <= 5% | Rejections / Published |

### Quality Report Template

```markdown
# Quality Report - [Period]

## Summary
- Total outputs: [N]
- First-pass rate: [%]
- Average score: [X.X]/10
- Retry rate: [%]

## By Platform
| Platform | Outputs | Pass Rate | Avg Score |
|----------|---------|-----------|-----------|
| Imagen 3 | N | %         | X.X       |
| Runway   | N | %         | X.X       |

## Common Issues
1. [Issue] - [frequency]
2. [Issue] - [frequency]

## Recommendations
- [Improvement suggestion]
- [Prompt optimization]
```

---

## INTEGRATION

**photo_agent**: Uses image quality checks before saving outputs
**video_agent**: Applies video quality scoring post-generation
**qa_agent**: Provides human review interface
**Cross-reference**: See [01_platform_comparison.md](01_platform_comparison.md) for platform specs

---

**Package**: AI_PLATFORMS v1.0.0
**Card**: 04_quality_assessment
**Quality**: 0.86/1.00
**Date**: 2025-12-05
