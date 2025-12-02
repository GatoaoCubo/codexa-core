# /curso_sales | Generate Sales Collateral

## Purpose
Generate complete sales package: landing page, email sequence (6), ad copy (3 platforms).

## Usage
```
/curso_sales "[course_name]"
```

## Parameters
- **course_name**: Course title (e.g., "CODEXA Layer 1-2 Transition")

## Workflow

### Step 1: Execute Builder
```bash
python builders/04_sales_collateral_builder.py --course "[NAME]" --verbose
```

### Step 2: Validate Brand Voice
```bash
python validators/02_brand_voice_validator.py --file outputs/sales/*_sales.md
```

## Output
Trinity format in outputs/sales/:
- [name]_sales.md (meta-prompt)
- [name]_sales.llm.json
- [name]_sales.meta.json

## Deliverables Generated
1. **Landing Page** - Hero, Problem, Solution, Proof, FAQ, CTA
2. **Email Sequence** - 6 emails (Awareness → Action → Engagement)
3. **Ad Copy** - Facebook, Google, LinkedIn variations

## Brand Voice
- Seed Words: Meta-Construção, Destilação de Conhecimento, Cérebro Plugável
- Tone: Disruptivo-sofisticado
- Attack: Banalização, lock-in, commodity knowledge
- Avoid: Revolucionário, mágico, único no mercado

## Example
```
User: /curso_sales "CODEXA Masterclass Layer 1-2"
Agent: Generating sales collateral...
Agent: [OK] Landing page structure generated
Agent: [OK] 6-email sequence generated
Agent: [OK] Ad copy for 3 platforms generated
Agent: [OK] Brand voice validation: 8.0/10.0 PASSED
Agent: Output: outputs/sales/codexa-masterclass_layer_1-2_sales.md
```

---
**Version**: 2.0.0 | **Builder**: 04_sales_collateral_builder.py | **Validator**: 02_brand_voice_validator.py
