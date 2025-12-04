<!-- iso_vectorstore -->
<!--
  Source: 01_brand_identity_HOP.md
  Agent: marca_agent
  Synced: 2025-12-02
  Version: 1.0.0
  Package: iso_vectorstore (export package)
-->

# Brand Identity Generator | HOP Module 01

**Module ID**: 01_brand_identity_HOP
**Version**: 1.0.0
**Purpose**: Generate brand names, taglines, and archetype selection for e-commerce products
**Type**: HOP (Higher-Order Prompt) - TAC-7 Framework
**Category**: Brand Strategy - Identity Creation
**Dependencies**: brand_archetypes.json, MASTER_INSTRUCTIONS.md
**Updated**: 2025-11-14

---

## MODULE_METADATA

```yaml
id: 01_brand_identity
version: 1.0.0
purpose: Generate 3 brand names + 3 taglines (40-60 chars strict) + select primary/secondary archetype
dependencies:
  - brand_archetypes.json (12 archetypes: Hero, Sage, Innocent, Explorer, Creator, Ruler, Magician, Lover, Caregiver, Jester, Everyman, Rebel)
  - MASTER_INSTRUCTIONS.md (brand creation methodology)
  - Product brief (input)
category: identity_creation
execution_time: 2-3 minutes
output_format: structured_markdown
```

---

## INPUT_CONTRACT

### Required Inputs

```yaml
$product_brief:
  type: object
  required:
    - product_name: string          # Name or description of product
    - category: string               # Product category (e.g., "water bottle", "skincare", "clothing")
    - target_audience: string        # Who is this for? (age, psychographic, behavioral)
    - price_range: string            # Price in BRL (e.g., "R$ 89-129")
  optional:
    - marketplace_target: string     # "mercadolivre" | "shopee" | "magalu" | "amazon_br" | "all"
    - brand_inspirations: array      # Existing brands user admires (for reference, not copying)
    - tone_preference: string        # "professional" | "playful" | "luxury" | "accessible"
    - USPs: array                    # Unique selling propositions
```

### Input Validation

```python
# Minimum brief validation
assert len(product_brief["product_name"]) > 0, "Product name required"
assert len(product_brief["category"]) > 0, "Category required"
assert len(product_brief["target_audience"]) >= 10, "Target audience too vague (min 10 chars)"
assert "R$" in product_brief["price_range"], "Price must be in BRL (R$)"
```

---

## OUTPUT_CONTRACT

### Primary Output

```yaml
brand_identity:
  brand_names:
    type: array
    min_items: 3
    max_items: 3
    items:
      - name: string                # Brand name
        type: string                # "descriptive" | "evocative" | "creative"
        rationale: string           # Why this name works (50-100 chars)
        availability_note: string   # Domain/social media consideration

  taglines:
    type: array
    min_items: 3
    max_items: 3
    items:
      - text: string                # Tagline text
        length: integer             # Character count (MUST be 40-60)
        archetype_alignment: string # How it reinforces archetype
        marketplace_fit: string     # Which marketplace this works best for

  archetype:
    primary: string                 # One of 12 valid archetypes
    secondary: string               # Complementary archetype (optional)
    rationale: string               # Why this archetype (100-150 chars)
    core_desire: string             # What customer desires (from archetype definition)

  personality_traits:
    type: array
    min_items: 5
    max_items: 5
    items: string                   # Adjectives describing brand personality

  brand_essence:
    type: string
    description: "One-sentence core identity (what the brand IS)"
    min_length: 50
    max_length: 150
```

### Secondary Output

```yaml
metadata:
  execution_time: string            # Time taken to generate
  archetype_confidence: float       # 0.0-1.0 confidence in archetype selection
  name_diversity_score: float       # 0.0-1.0 how different the 3 names are
  quality_score: float              # 0.0-1.0 overall quality estimate
```

---

## TASK

### Role

You are a **Brand Identity Specialist** with expertise in:
- Brazilian e-commerce marketplace branding (Mercado Livre, Shopee, Magalu, Amazon BR)
- Brand archetype psychology (12 Jungian archetypes)
- Naming strategies (descriptive, evocative, creative/invented)
- Tagline copywriting (40-60 character strict enforcement)
- Cultural nuances of Portuguese (BR) brand communication

### Objective

Generate a **complete brand identity foundation** consisting of:
1. **3 distinct brand names** (descriptive, evocative, creative)
2. **3 taglines** (40-60 characters STRICT - no exceptions)
3. **Primary + secondary archetype** selection with rationale
4. **5 personality traits** that define brand voice
5. **Brand essence** statement (one-sentence core identity)

### Standards

**CRITICAL**:
- ALL taglines MUST be exactly 40-60 characters (strict enforcement)
- Archetype MUST be one of 12 valid options (see brand_archetypes.json)
- Names must be in Portuguese (BR) unless product is international/tech
- Consider marketplace title limits (ML: 60 chars, Shopee: 255 chars, etc.)

**QUALITY**:
- Names must be memorable, pronounceable, and distinctive
- Taglines must communicate value proposition clearly
- Archetype must align with target audience psychographics
- Avoid generic brand names ("Premium", "Quality", "Best")
- No trademark conflicts (check common Brazilian brands)

### Constraints

**Regulatory** (Brazilian Compliance):
- No health claims without ANVISA approval ("cura", "trata")
- No superlatives without proof ("#1", "melhor do Brasil")
- Avoid trademarked terms (Nike, Adidas, etc.)
- Consider INPI (trademark) availability

**Marketplace**:
- Mercado Livre: Max 60 chars title, no emojis
- Shopee: Max 255 chars, emojis allowed (limit 3)
- Amazon BR: Max 200 chars, no promotional language
- Magalu: Max 150 chars, family-friendly

**Cultural**:
- Avoid anglicisms unless target is tech/young audience
- Consider Brazilian pronunciation (avoid complex consonant clusters)
- Regional sensitivity (North/South/Northeast cultural differences)
- Avoid slang that may date quickly

---

## STEPS

### Step 1: Analyze Product Brief

**Action**: Deep analysis of input brief

```python
# Extract key insights
product_category = extract_category(brief)
target_demographics = extract_demographics(brief)
price_positioning = classify_price_tier(brief)  # "budget" | "mid-range" | "premium" | "luxury"
emotional_benefits = infer_emotional_benefits(brief)
functional_benefits = extract_functional_benefits(brief)
marketplace_constraints = get_marketplace_limits(brief.marketplace_target)
```

**Output**: Internal product understanding map

**Quality Check**:
- ✅ Target audience clearly understood
- ✅ Price positioning identified (budget/mid/premium/luxury)
- ✅ Primary benefit (emotional vs functional) identified

---

### Step 2: Select Brand Archetype

**Action**: Choose primary + optional secondary archetype from 12 options

**Valid Archetypes** (from brand_archetypes.json):
1. **Hero** - Prove worth through courage (sports, performance, security)
2. **Sage** - Discover and share truth (education, consulting, finance)
3. **Innocent** - Experience happiness (natural products, children)
4. **Explorer** - Self-discovery through experience (outdoor, travel, adventure)
5. **Creator** - Create lasting value (design, art, creative tools)
6. **Ruler** - Control, create prosperity (luxury, premium services)
7. **Magician** - Transform reality (entertainment, cosmetics)
8. **Lover** - Intimacy, sensory experience (fashion, chocolates, perfumes)
9. **Caregiver** - Protect and care for others (health, childcare, insurance)
10. **Jester** - Live in the moment with joy (entertainment, snacks)
11. **Everyman** - Belong, connect with others (accessible retail, everyday products)
12. **Rebel** - Revolution, break conventions (alternative brands, streetwear)

**Selection Criteria**:
```yaml
IF target_audience == "young, innovation-seeking" AND price == "mid-premium":
  primary_archetype = "Creator" or "Explorer"

IF product_category == "health/wellness" AND tone == "caring":
  primary_archetype = "Caregiver"

IF price == "luxury" AND exclusivity important:
  primary_archetype = "Ruler" or "Lover"

IF product == "fun/entertainment" AND audience == "mass market":
  primary_archetype = "Jester" or "Everyman"
```

**Output**:
```yaml
archetype:
  primary: "Explorer"
  secondary: "Hero"  # Optional: adds nuance
  rationale: "Target is adventure-seeking sports enthusiasts (Explorer) who value performance and self-improvement (Hero secondary)"
  core_desire: "Freedom to discover and experience new possibilities"
```

**Quality Check**:
- ✅ Archetype aligns with target audience values
- ✅ Archetype supports price positioning
- ✅ Core desire matches emotional benefits from brief

---

### Step 3: Generate 3 Brand Names

**Action**: Create 3 diverse brand names using different naming strategies

**Naming Strategies**:

1. **Descriptive** (literal, functional)
   - Pattern: [Benefit] + [Category] or [Attribute] + [Product]
   - Example: "HidrataPro" (hydration + professional)
   - Pros: Clear, SEO-friendly
   - Cons: Less memorable, harder to trademark

2. **Evocative** (emotional, associative)
   - Pattern: Metaphor, imagery, feeling
   - Example: "Nascente" (spring/source - evokes purity, freshness)
   - Pros: Memorable, emotionally resonant
   - Cons: Requires more brand building

3. **Creative/Invented** (coined, abstract)
   - Pattern: Made-up word, portmanteau, playful
   - Example: "Fluiva" (fluid + viva)
   - Pros: Unique, trademarkable
   - Cons: Requires explanation initially

**Generation Process**:
```python
for strategy in ["descriptive", "evocative", "creative"]:
    name = generate_name(
        strategy=strategy,
        archetype=selected_archetype,
        product_benefits=extracted_benefits,
        target_audience=demographics,
        language="pt-BR",
        avoid_list=common_brazilian_brands
    )

    # Validate
    assert 3 <= len(name) <= 18, "Name too short or too long"
    assert is_pronounceable_in_portuguese(name), "Pronunciation difficulty"
    assert not contains_offensive_terms(name, language="pt-BR")
    assert check_domain_availability_heuristic(name)  # .com.br availability estimate

    brand_names.append({
        "name": name,
        "type": strategy,
        "rationale": explain_name_choice(name, strategy, archetype),
        "availability_note": f"Check {name}.com.br and @{name.lower()} on Instagram"
    })
```

**Output Example**:
```yaml
brand_names:
  - name: "HidroVida"
    type: "descriptive"
    rationale: "Combina 'hidro' (hydration) com 'vida' (life), comunicando benefício funcional de forma clara"
    availability_note: "Check hidrovida.com.br and @hidrovida - common name, verify trademark"

  - name: "Nascente"
    type: "evocative"
    rationale: "Evoca pureza e origem natural, alinha com arquétipo Explorer (descoberta de fontes puras)"
    availability_note: "Poetic name, good brandability, check INPI trademark database"

  - name: "Fluiva"
    type: "creative"
    rationale: "Portmanteau de 'fluido' + 'viva', sugere movimento e vitalidade de forma única"
    availability_note: "Invented word, high trademark potential, easy to pronounce"
```

**Quality Check**:
- ✅ All 3 names are distinct (different strategies)
- ✅ Names are in Portuguese (unless product is international)
- ✅ No obvious trademark conflicts
- ✅ Pronounceable and memorable

---

### Step 4: Create 3 Taglines (40-60 chars STRICT)

**Action**: Craft taglines that communicate value proposition

**Tagline Formula**:
```
[Emotional Benefit] + [How Product Delivers]
OR
[Unique Value] + [For Whom]
OR
[Problem Solved] + [Brand Promise]
```

**Character Count ENFORCEMENT**:
```python
def validate_tagline(tagline: str) -> bool:
    # Remove markdown formatting if present
    clean_tagline = tagline.strip().replace("**", "").replace("*", "")
    length = len(clean_tagline)

    # STRICT: Must be 40-60 characters
    if length < 40:
        raise ValueError(f"Tagline too short: {length} chars (min 40)")
    if length > 60:
        raise ValueError(f"Tagline too long: {length} chars (max 60)")

    return True
```

**Generation Process**:
```python
for i in range(3):
    # Generate initial tagline
    tagline = create_tagline(
        archetype=selected_archetype,
        value_proposition=main_benefit,
        tone=archetype_tone_mapping[selected_archetype],
        marketplace=marketplace_target
    )

    # Adjust length to 40-60 chars
    while len(tagline) < 40:
        tagline = expand_tagline(tagline)  # Add descriptors

    while len(tagline) > 60:
        tagline = compress_tagline(tagline)  # Remove filler words

    # Final validation
    validate_tagline(tagline)

    taglines.append({
        "text": tagline,
        "length": len(tagline),
        "archetype_alignment": explain_archetype_fit(tagline, selected_archetype),
        "marketplace_fit": assess_marketplace_compatibility(tagline, marketplace_target)
    })
```

**Output Example**:
```yaml
taglines:
  - text: "Hidratação sustentável para quem não para de se mover"
    length: 54
    archetype_alignment: "Explorer: 'não para de se mover' reforça movimento e descoberta"
    marketplace_fit: "Mercado Livre: claro e funcional, comunica benefício direto"

  - text: "Cada gota conta na sua jornada de performance"
    length: 47
    archetype_alignment: "Hero secondary: 'jornada de performance' evoca conquista pessoal"
    marketplace_fit: "Shopee: emocional, funciona bem com público jovem"

  - text: "Pureza em movimento: sua parceira de aventuras"
    length: 48
    archetype_alignment: "Explorer: 'aventuras' é palavra-chave do arquétipo"
    marketplace_fit: "Amazon BR: qualidade premium, evoca confiança"
```

**Quality Check**:
- ✅ ALL taglines are 40-60 characters (STRICT - zero exceptions)
- ✅ Communicate primary benefit clearly
- ✅ Align with selected archetype
- ✅ No prohibited claims (ANVISA/CONAR compliance)

---

### Step 5: Define Personality Traits

**Action**: Select 5 adjectives that define brand personality

**Trait Selection** (aligned with archetype):
```python
archetype_trait_mapping = {
    "Hero": ["corajoso", "determinado", "confiável", "inspirador", "resiliente"],
    "Explorer": ["aventureiro", "curioso", "independente", "autêntico", "energético"],
    "Caregiver": ["acolhedor", "protetor", "empático", "confiável", "generoso"],
    "Creator": ["inovador", "original", "expressivo", "visionário", "inspirador"],
    "Sage": ["sábio", "analítico", "confiável", "educador", "objetivo"],
    # ... (continue for all 12)
}

# Select 5 traits
personality_traits = select_traits(
    archetype_primary=selected_archetype,
    archetype_secondary=secondary_archetype,  # Optional blend
    target_audience=demographics,
    avoid_generic=True  # Avoid "qualidade", "excelência", etc.
)
```

**Output Example**:
```yaml
personality_traits:
  - "Aventureiro"    # Explorer core
  - "Sustentável"    # Product attribute
  - "Energético"     # Audience alignment
  - "Autêntico"      # Differentiation
  - "Determinado"    # Hero secondary
```

**Quality Check**:
- ✅ Traits align with archetype
- ✅ No generic corporate buzzwords
- ✅ Traits support tone of voice (next module)

---

### Step 6: Craft Brand Essence Statement

**Action**: One-sentence core identity (50-150 chars)

**Formula**:
```
[Brand Name] + [verb] + [what] + [for whom] + [why it matters]
```

**Output Example**:
```yaml
brand_essence: "Fluiva capacita aventureiros urbanos a manterem alta performance com hidratação consciente e sustentável."
# Length: 112 chars ✅
```

**Quality Check**:
- ✅ 50-150 characters
- ✅ Captures "what the brand IS" (not just what it does)
- ✅ Mentions target audience
- ✅ Hints at unique value

---

## VALIDATION

### Quality Gates

```yaml
required_validations:
  - tagline_length_strict:
      rule: "ALL 3 taglines must be 40-60 characters (zero tolerance)"
      threshold: 100%
      severity: CRITICAL

  - archetype_validity:
      rule: "Primary archetype must be one of 12 valid options"
      threshold: 100%
      severity: CRITICAL

  - name_diversity:
      rule: "3 names must use different naming strategies"
      threshold: 100%
      severity: HIGH

  - personality_trait_uniqueness:
      rule: "No generic traits (qualidade, excelência, inovação alone)"
      threshold: 80%
      severity: MEDIUM

  - brand_essence_completeness:
      rule: "Essence must mention product, audience, and value"
      threshold: 100%
      severity: HIGH
```

### Compliance Checks

```yaml
anvisa_compliance:
  - No medical claims ("cura", "trata", "previne doenças")
  - No unsubstantiated health benefits

conar_compliance:
  - No superlatives without proof ("#1", "melhor")
  - No misleading environmental claims ("100% sustentável" requires cert)

marketplace_compliance:
  - Tagline length compatible with title limits
  - No emojis (if targeting Mercado Livre)
  - Family-friendly language (all marketplaces)
```

### Quality Thresholds

```python
def calculate_quality_score(brand_identity):
    score = 0.0

    # Tagline compliance (40% weight)
    if all(40 <= len(t["text"]) <= 60 for t in brand_identity["taglines"]):
        score += 0.40

    # Name diversity (20% weight)
    name_types = set(n["type"] for n in brand_identity["brand_names"])
    if len(name_types) == 3:
        score += 0.20

    # Archetype alignment (20% weight)
    if archetype_is_valid(brand_identity["archetype"]["primary"]):
        score += 0.20

    # Trait uniqueness (10% weight)
    generic_traits = ["qualidade", "excelência", "inovação", "premium"]
    unique_traits = [t for t in brand_identity["personality_traits"] if t.lower() not in generic_traits]
    if len(unique_traits) >= 4:
        score += 0.10

    # Essence completeness (10% weight)
    essence = brand_identity["brand_essence"]
    if 50 <= len(essence) <= 150:
        score += 0.10

    return score

# Threshold: Score >= 0.85 (excellent)
assert calculate_quality_score(output) >= 0.85, "Quality below threshold"
```

---

## CONTEXT

### Usage

**When to use this module**:
- Beginning of brand strategy creation (first step of 8-step workflow)
- Rebranding existing product with new identity
- Creating sub-brand under existing brand umbrella

**When NOT to use**:
- Brand already has established name/tagline (skip to positioning module)
- Logo design phase (this generates PROMPTS for visuals, not actual designs)

### Upstream Dependencies

**Requires**:
- Product brief (user input)
- brand_archetypes.json (12 archetype definitions)
- MASTER_INSTRUCTIONS.md (methodology reference)

**Optional**:
- research_notes.md (from pesquisa_agent - market insights)
- competitor_analysis.md (for differentiation)

### Downstream Consumers

**Next modules**:
- 02_positioning_HOP.md (uses archetype + brand names)
- 03_tone_of_voice_HOP.md (uses personality traits)
- 04_visual_identity_HOP.md (uses archetype for color/typography)

**Output used by**:
```yaml
02_positioning_HOP:
  inputs: [archetype, brand_essence, personality_traits]

03_tone_of_voice_HOP:
  inputs: [personality_traits, archetype]

04_visual_identity_HOP:
  inputs: [archetype, brand_names, taglines]

07_validation_HOP:
  inputs: [all identity components for consistency check]
```

### $arguments Chaining

```yaml
# This module outputs
$brand_identity = {
  "brand_names": [...],
  "taglines": [...],
  "archetype": {...},
  "personality_traits": [...],
  "brand_essence": "..."
}

# Next module consumes
$positioning_input = {
  "brand_identity": $brand_identity,  # Entire output from this module
  "product_brief": $product_brief     # Original brief
}
```

### Assumptions

1. **Target market is Brazil**: All content in Portuguese (BR) unless specified
2. **E-commerce focus**: Optimized for marketplace listing constraints
3. **Single product brands**: Not designed for corporate/multi-product portfolios
4. **Archetype psychology works**: Assumes Jungian archetype framework is valid
5. **Tagline length matters**: 40-60 chars is optimal for memorability + marketplace titles

### Edge Cases

**Edge Case 1: Very niche product**
```
Problem: Product so niche that common archetypes don't fit well
Solution: Blend 2 archetypes (primary + strong secondary)
Example: "Artisanal soap for engineers" = Creator (primary) + Sage (secondary)
```

**Edge Case 2: International brand entering Brazil**
```
Problem: Should name be in English or Portuguese?
Solution:
  - IF target == "tech-savvy, young, urban" → English acceptable
  - IF target == "mass market, 35+, regional" → Portuguese required
  - ALWAYS tagline in Portuguese (BR)
```

**Edge Case 3: Tagline cannot fit value proposition in 60 chars**
```
Problem: Complex product needs longer explanation
Solution: Use 2-part tagline strategy:
  - Primary: 40-60 chars (for marketplaces)
  - Extended: 80-120 chars (for website, packaging)
```

---

## EXAMPLES

### Example 1: Sustainable Water Bottle

**Input**:
```yaml
product_brief:
  product_name: "Garrafa de água reutilizável, ecológica"
  category: "Acessórios esportivos"
  target_audience: "Pessoas conscientes que praticam esportes, 25-40 anos"
  price_range: "R$ 89-129"
  marketplace_target: "mercadolivre"
```

**Output**:
```yaml
brand_identity:
  brand_names:
    - name: "HidroAtivo"
      type: "descriptive"
      rationale: "Combina hidratação + estilo de vida ativo, comunicação direta"
      availability_note: "Check hidroativo.com.br - nome comum, verificar marca"

    - name: "Nascente"
      type: "evocative"
      rationale: "Evoca pureza, origem natural, ressoa com valores ecológicos"
      availability_note: "Nome poético, alta brandabilidade, verificar INPI"

    - name: "Fluiva"
      type: "creative"
      rationale: "Fluido + viva = movimento e vitalidade, único e memorável"
      availability_note: "Palavra inventada, alto potencial de trademark"

  taglines:
    - text: "Hidratação sustentável para quem não para de se mover"
      length: 54
      archetype_alignment: "Explorer: movimento constante, descoberta"
      marketplace_fit: "ML: claro, funcional, SEO-friendly"

    - text: "Cada gota conta na sua jornada de performance"
      length: 47
      archetype_alignment: "Hero secondary: jornada pessoal, conquista"
      marketplace_fit: "Shopee: emocional, público jovem"

    - text: "Pureza em movimento: sua parceira de aventuras"
      length: 48
      archetype_alignment: "Explorer: aventuras, liberdade"
      marketplace_fit: "Amazon BR: premium, confiança"

  archetype:
    primary: "Explorer"
    secondary: "Hero"
    rationale: "Público busca autodescoberta através do esporte (Explorer) e autossuperação (Hero)"
    core_desire: "Liberdade para explorar e experimentar sem limites"

  personality_traits:
    - "Aventureiro"
    - "Sustentável"
    - "Energético"
    - "Autêntico"
    - "Determinado"

  brand_essence: "Fluiva capacita aventureiros urbanos a manterem alta performance com hidratação consciente e sustentável."
```

---

**Status**: Ready for production | **Version**: 1.0.0 | **Module**: 01/09 | **Execution Time**: 2-3 min
**Next Module**: 02_positioning_HOP.md (uses $brand_identity output)

---

> 💡 **TIP**: Use this HOP as the first step in the 8-step brand strategy workflow
> 🎯 **CRITICAL**: Tagline length 40-60 chars is STRICTLY enforced (brand_validator.py will fail otherwise)
> ✅ **VALIDATED**: This HOP follows TAC-7 framework (Metadata, Input, Output, Task, Steps, Validation, Context)
