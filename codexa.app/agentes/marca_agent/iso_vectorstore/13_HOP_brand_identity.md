# HOP 13: Brand Identity Generator | marca_agent v3.0.0

**Purpose**: Generate brand names, taglines, and archetype selection
**Scope**: BRAND_STRATEGY | **Output**: brand_identity block (5 components)
**Duration**: 2-3 min | **Module**: 1/8

---

## INPUT

- `$product_brief` (required):
  - product_name, category, target_audience, price_range
- Optional: marketplace_target, brand_inspirations, USPs

---

## RULES (CRITICAL)

1. **Taglines MUST be 40-60 chars** (strict, no exceptions)
2. **Archetype MUST be from 12 valid options**: Hero, Sage, Innocent, Explorer, Creator, Ruler, Magician, Lover, Caregiver, Jester, Everyman, Rebel
3. **Names in Portuguese (BR)** unless product is tech/international
4. **No ANVISA violations**: avoid "cura", "trata", "melhor"
5. **3 naming strategies**: descriptive, evocative, creative

---

## STEPS

### 1. Analyze Brief
Extract: category, demographics, price tier (budget/mid/premium/luxury), benefits

### 2. Select Archetype
Choose primary + optional secondary from 12 archetypes based on:
- Target audience values
- Price positioning
- Emotional benefits

### 3. Generate 3 Brand Names
| Type | Pattern | Example |
|------|---------|---------|
| Descriptive | [Benefit]+[Category] | HidroVida |
| Evocative | Metaphor, feeling | Nascente |
| Creative | Invented word | Fluiva |

### 4. Create 3 Taglines (40-60 chars)
Formula: [Benefit] + [For Whom] OR [Value] + [Promise]

**VALIDATION**: Count chars before output. Reject if <40 or >60.

### 5. Define 5 Personality Traits
Aligned with archetype. Avoid generic: "qualidade", "excelência"

### 6. Craft Brand Essence (50-150 chars)
Formula: [Brand] + [verb] + [what] + [for whom] + [why]

---

## OUTPUT FORMAT

```yaml
brand_identity:
  brand_names:
    - name: "NomeMarca"
      type: "descriptive|evocative|creative"
      rationale: "Why this name works (50-100 chars)"

  taglines:
    - text: "Tagline text here (40-60 chars strict)"
      length: 52
      archetype_alignment: "How it reinforces archetype"

  archetype:
    primary: "Explorer"
    secondary: "Hero"
    rationale: "Why this archetype (100-150 chars)"
    core_desire: "What customer desires"

  personality_traits: ["trait1", "trait2", "trait3", "trait4", "trait5"]

  brand_essence: "One-sentence core identity (50-150 chars)"
```

---

## VALIDATION

- [ ] ALL 3 taglines are 40-60 chars? (CRITICAL)
- [ ] Archetype is one of 12 valid options?
- [ ] 3 names use different strategies?
- [ ] No generic traits?
- [ ] Brand essence 50-150 chars?
- [ ] No ANVISA/CONAR violations?

**Quality Score**: >= 0.85 required

---

**HOP**: 13 | **Agent**: marca_agent | **Version**: 3.0.0
**Tokens**: ~800 (optimized from ~6,000)
