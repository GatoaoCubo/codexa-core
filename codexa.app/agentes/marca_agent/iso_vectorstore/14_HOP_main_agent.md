# HOP 14: Main Agent Orchestrator | marca_agent v3.0.0

**Purpose**: Orchestrate 8-step brand strategy workflow
**Scope**: BRAND_STRATEGY | **Output**: brand_strategy.md (32 blocks)
**Duration**: 15-20 min | **Role**: Meta-HOP Orchestrator

---

## INPUT

- `$brief` (required): product_name, category, target_audience, price_range
- `$execution_plan` (optional): "full" (default) | "quick"
- `$marketplace_target`: "mercadolivre" | "shopee" | "amazon_br" | "all"

---

## WORKFLOW (8 Steps)

Each step output becomes input for next step ($arguments chaining).

### STEP 1: INTAKE & VALIDATION (2-3 min)
- Validate brief vs schema
- Ask 3-5 strategic questions if insufficient
- Set quality thresholds

### STEP 2: BRAND IDENTITY (2-3 min)
**Doc**: `13_HOP_brand_identity.md`
- Generate 3 names (descriptive, evocative, creative)
- Create 3 taglines (40-60 chars STRICT)
- Select archetype (from 12)
- Define 5 personality traits
**Gate**: Names unique, taglines within limits

### STEP 3: POSITIONING (2-3 min)
- Craft UVP (unique value proposition)
- Define target segment (demo + psycho + behavioral)
- Map competitive differentiation
**Gate**: UVP >= 70% differentiated

### STEP 4: TONE OF VOICE (1-2 min)
- Define 4 personality dimensions (1-5 scale)
- Create language style guide
- List 5 do's + 5 don'ts
**Gate**: Tone aligns with archetype

### STEP 5: VISUAL IDENTITY (2-3 min)
- Select color palette (HEX + RGB + psychology)
- Choose typography (primary + secondary)
- Generate 9 mood board prompts
**Gate**: >= 2 color pairs meet WCAG Level AA

### STEP 6: BRAND NARRATIVE (3-4 min)
- Write origin story (>= 500 chars)
- Craft mission (100-150 chars)
- Articulate vision (100-150 chars)
- Define 5 values (non-generic)
**Gate**: Narrative harmony with values

### STEP 7: BRAND GUIDELINES (1-2 min)
- List 8-10 messaging do's
- List 8-10 messaging don'ts
- Document compliance (ANVISA/INMETRO/CONAR)
**Gate**: Compliance matches category

### STEP 8: VALIDATION & OUTPUT (2-3 min)
- Run Brand Fingerprint validation
- Calculate consistency score
- Format using brand_strategy template
**Gate**: Consistency >= 0.85, Uniqueness >= 8.0/10

---

## QUALITY GATES (8 Critical)

| Gate | Threshold |
|------|-----------|
| Consistency Score | >= 0.85 |
| Uniqueness Score | >= 8.0/10 |
| WCAG Contrast | Level AA |
| Tagline Length | 40-60 chars |
| Seed Words | >= 2 |
| Tone Alignment | 95% |
| Compliance | PASS |
| Values | Non-generic |

---

## OUTPUT FORMAT

```
brand_strategy.md (32 blocks):

SECTION 1: BRAND IDENTITY (5 blocks)
SECTION 2: POSITIONING (5 blocks)
SECTION 3: TONE OF VOICE (5 blocks)
SECTION 4: VISUAL IDENTITY (4 blocks)
SECTION 5: BRAND NARRATIVE (5 blocks)
SECTION 6: BRAND GUIDELINES (4 blocks)
SECTION 7: VALIDATION & AUDIT (4 blocks)
```

---

## VALIDATION

- [ ] All 8 steps completed?
- [ ] All gates passed?
- [ ] brand_strategy.md has 32 blocks?
- [ ] Consistency >= 0.85?
- [ ] No compliance violations?

---

**HOP**: 14 | **Agent**: marca_agent | **Version**: 3.0.0
**Tokens**: ~700 (optimized from ~6,000)
