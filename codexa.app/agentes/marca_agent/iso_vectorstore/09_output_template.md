# marca_agent | Output Template v3.0.0

**Purpose**: Standardized output format for brand strategy generation
**Output**: brand_strategy.md (32 blocks) + validation_report.txt + metadata.json

---

## OUTPUT FILES (Trinity Format)

```
USER_DOCS/Marca/
├── [produto]_brand_strategy.md      # Human-readable (32 blocks)
├── [produto]_brand_strategy.llm.json # Structured data for LLMs
└── [produto]_brand_strategy.meta.json # Execution metadata
```

---

## BRAND_STRATEGY.MD TEMPLATE

```markdown
# BRAND STRATEGY - [BRAND_NAME]

**Generated**: [DATE]
**Version**: 3.0.0
**Agent**: marca_agent
**Execution Mode**: [full|quick]

---

## SECTION 1: BRAND IDENTITY

### 1. Brand Names
| Type | Name | Rationale |
|------|------|-----------|
| Descriptive | [NAME_1] | [Why this name works] |
| Evocative | [NAME_2] | [Emotional connection] |
| Creative | [NAME_3] | [Unique positioning] |

**Recommended**: [SELECTED_NAME]

### 2. Taglines
| # | Tagline | Chars | Type |
|---|---------|-------|------|
| 1 | [TAGLINE_1] | [##] | Functional |
| 2 | [TAGLINE_2] | [##] | Emotional |
| 3 | [TAGLINE_3] | [##] | Aspirational |

**Validation**: All taglines 40-60 chars [PASS/FAIL]

### 3. Brand Archetype
**Primary**: [ARCHETYPE_1] - [Core Desire]
**Secondary**: [ARCHETYPE_2] - [Supporting Trait]
**Expression**: "[How archetype manifests in brand]"

### 4. Personality Traits
1. [TRAIT_1] - [Description]
2. [TRAIT_2] - [Description]
3. [TRAIT_3] - [Description]
4. [TRAIT_4] - [Description]
5. [TRAIT_5] - [Description]

### 5. Brand Essence
> [One-sentence core identity that captures the soul of the brand]

---

## SECTION 2: POSITIONING

### 6. Unique Value Proposition (UVP)
> [Differentiated promise that sets this brand apart]

### 7. Target Segment
**Demographics**: [Age, gender, income, location]
**Psychographics**: [Values, lifestyle, interests]
**Behavioral**: [Purchase habits, brand loyalty, usage patterns]

### 8. Competitive Differentiation
| Factor | This Brand | Competitor A | Competitor B |
|--------|------------|--------------|--------------|
| [Factor 1] | [Advantage] | [Position] | [Position] |
| [Factor 2] | [Advantage] | [Position] | [Position] |
| [Factor 3] | [Advantage] | [Position] | [Position] |

### 9. Brand Promise
> [What customers can always expect from this brand]

### 10. Positioning Statement
> For [TARGET_SEGMENT] who [NEED/WANT], [BRAND_NAME] is the [CATEGORY] that [UNIQUE_BENEFIT]. Unlike [COMPETITORS], we [PROOF/DIFFERENTIATION].

---

## SECTION 3: TONE OF VOICE

### 11. Personality Dimensions
| Dimension | Scale (1-5) | Description |
|-----------|-------------|-------------|
| Formal <-> Casual | [#] | [Explanation] |
| Enthusiastic <-> Matter-of-fact | [#] | [Explanation] |
| Respectful <-> Irreverent | [#] | [Explanation] |
| Serious <-> Funny | [#] | [Explanation] |

### 12. Language Style
- **Vocabulary Level**: [Simple/Moderate/Sophisticated]
- **Sentence Structure**: [Short/Medium/Complex]
- **Linguistic Patterns**: [Key patterns to use]

### 13. Messaging Do's
1. [DO_1]
2. [DO_2]
3. [DO_3]
4. [DO_4]
5. [DO_5]

### 14. Messaging Don'ts
1. [DONT_1]
2. [DONT_2]
3. [DONT_3]
4. [DONT_4]
5. [DONT_5]

### 15. Example Phrases
1. "[PHRASE_1]"
2. "[PHRASE_2]"
3. "[PHRASE_3]"
4. "[PHRASE_4]"
5. "[PHRASE_5]"
6. "[PHRASE_6]"
7. "[PHRASE_7]"
8. "[PHRASE_8]"
9. "[PHRASE_9]"
10. "[PHRASE_10]"

---

## SECTION 4: VISUAL IDENTITY

### 16. Color Palette
| Role | Color | HEX | RGB | Psychology |
|------|-------|-----|-----|------------|
| Primary | [NAME] | #[HEX] | rgb([R],[G],[B]) | [Meaning] |
| Secondary | [NAME] | #[HEX] | rgb([R],[G],[B]) | [Meaning] |
| Accent | [NAME] | #[HEX] | rgb([R],[G],[B]) | [Meaning] |

**WCAG Compliance**: [# pairs] pass Level AA [PASS/FAIL]

### 17. Typography
| Role | Font | Fallback | Usage |
|------|------|----------|-------|
| Primary | [FONT_1] | [FALLBACK] | Headlines |
| Secondary | [FONT_2] | [FALLBACK] | Body text |

### 18. Mood Board Prompts
| # | Prompt (for AI image generation) |
|---|----------------------------------|
| 1 | [PROMPT_1] |
| 2 | [PROMPT_2] |
| 3 | [PROMPT_3] |
| 4 | [PROMPT_4] |
| 5 | [PROMPT_5] |
| 6 | [PROMPT_6] |
| 7 | [PROMPT_7] |
| 8 | [PROMPT_8] |
| 9 | [PROMPT_9] |

### 19. Visual Style Guidelines
- **Photography Style**: [Description]
- **Illustration Style**: [Description]
- **Iconography**: [Description]
- **Graphic Elements**: [Description]

---

## SECTION 5: BRAND NARRATIVE

### 20. Origin Story
[ORIGIN_STORY - minimum 500 characters]
[Compelling narrative about why this brand exists and the problem it solves]

### 21. Mission Statement
> [MISSION - 100-150 characters, action-oriented]

### 22. Vision Statement
> [VISION - 100-150 characters, aspirational]

### 23. Core Values
| # | Value | Definition | How We Live It |
|---|-------|------------|----------------|
| 1 | [VALUE_1] | [Definition] | [Manifestation] |
| 2 | [VALUE_2] | [Definition] | [Manifestation] |
| 3 | [VALUE_3] | [Definition] | [Manifestation] |
| 4 | [VALUE_4] | [Definition] | [Manifestation] |
| 5 | [VALUE_5] | [Definition] | [Manifestation] |

### 24. Brand Manifesto
[MANIFESTO - minimum 300 characters]
[Emotional rallying cry that captures the brand's purpose and passion]

---

## SECTION 6: BRAND GUIDELINES

### 25. Messaging Do's (Extended)
1. [DO_1] - Example: "[example]"
2. [DO_2] - Example: "[example]"
3. [DO_3] - Example: "[example]"
4. [DO_4] - Example: "[example]"
5. [DO_5] - Example: "[example]"
6. [DO_6] - Example: "[example]"
7. [DO_7] - Example: "[example]"
8. [DO_8] - Example: "[example]"

### 26. Messaging Don'ts (Extended)
1. [DONT_1] - Why: "[reason]"
2. [DONT_2] - Why: "[reason]"
3. [DONT_3] - Why: "[reason]"
4. [DONT_4] - Why: "[reason]"
5. [DONT_5] - Why: "[reason]"
6. [DONT_6] - Why: "[reason]"
7. [DONT_7] - Why: "[reason]"
8. [DONT_8] - Why: "[reason]"

### 27. Compliance Rules
**Category**: [PRODUCT_CATEGORY]
**Applicable Regulations**:
- ANVISA: [Specific rules]
- INMETRO: [Specific rules]
- CONAR: [Specific rules]
- CDC: [Consumer protection rules]

### 28. Consistency Checklist
- [ ] Brand name used consistently
- [ ] Tagline within 40-60 chars
- [ ] Colors match palette (HEX exact)
- [ ] Typography follows guidelines
- [ ] Tone matches personality dimensions
- [ ] Values reflected in messaging
- [ ] Archetype expression consistent
- [ ] Compliance rules followed
- [ ] WCAG contrast validated
- [ ] Seed words present in copy

---

## SECTION 7: VALIDATION & AUDIT

### 29. Brand Consistency Score
**Score**: [0.XX] / 1.00
**Rating**: [Excellent >= 0.85 | Good >= 0.75 | Needs Work < 0.75]

| Check | Status | Weight |
|-------|--------|--------|
| Identity-Positioning | [PASS/FAIL] | 15% |
| Archetype-Tone | [PASS/FAIL] | 15% |
| Visual-Personality | [PASS/FAIL] | 15% |
| Narrative-Values | [PASS/FAIL] | 15% |
| Compliance | [PASS/FAIL] | 10% |
| WCAG | [PASS/FAIL] | 10% |
| Seed Words | [PASS/FAIL] | 10% |
| Tone Consistency | [PASS/FAIL] | 10% |

### 30. Brand Uniqueness Score
**Score**: [X.X] / 10.0
**Rating**: [Excellent >= 8.0 | Good >= 6.0 | Generic < 6.0]

| Dimension | Score | Notes |
|-----------|-------|-------|
| Purpose Specificity | [X]/10 | [Notes] |
| Values Uniqueness | [X]/10 | [Notes] |
| Seed Words Usage | [X]/10 | [Notes] |
| Tone Consistency | [X]/10 | [Notes] |
| Benchmark Differentiation | [X]/10 | [Notes] |

### 31. Competitive Audit
| Aspect | [BRAND] | Competitor 1 | Competitor 2 | Competitor 3 |
|--------|---------|--------------|--------------|--------------|
| Positioning | [Position] | [Position] | [Position] | [Position] |
| Price Point | [Range] | [Range] | [Range] | [Range] |
| Target | [Segment] | [Segment] | [Segment] | [Segment] |
| Strength | [Key] | [Key] | [Key] | [Key] |
| Gap | [Opportunity] | - | - | - |

### 32. Integration Notes
**For anuncio_agent**:
- Use tone dimensions for ad copy
- Apply color palette to visuals
- Follow messaging do's/don'ts
- Include seed words in copy

**For pesquisa_agent**:
- Use positioning for keyword research
- Apply target segment for audience analysis
- Reference competitors for benchmarking

---

## EXECUTION METADATA

**Generated By**: marca_agent v2.5.0
**Execution Mode**: [full|quick]
**Duration**: [XX] minutes
**Model**: [GPT-5|Claude Sonnet 4.5]
**Quality Gates**: [X/8] passed
**Timestamp**: [ISO_DATE]
```

---

## VALIDATION CHECKLIST

Before finalizing output, verify:

### Content Validation
- [ ] All 32 blocks present
- [ ] Taglines 40-60 chars each
- [ ] Origin story >= 500 chars
- [ ] Manifesto >= 300 chars
- [ ] Mission/Vision 100-150 chars each
- [ ] 5 core values defined
- [ ] 10 example phrases included
- [ ] 9 mood board prompts

### Quality Validation
- [ ] Consistency score >= 0.85
- [ ] Uniqueness score >= 8.0/10
- [ ] WCAG Level AA (>= 2 color pairs)
- [ ] Seed words >= 2 in critical pieces
- [ ] Tone consistency >= 95%

### Compliance Validation
- [ ] ANVISA rules checked
- [ ] INMETRO rules checked
- [ ] CONAR rules checked
- [ ] No forbidden claims

---

**Version**: 3.0.0
**Updated**: 2025-11-30
