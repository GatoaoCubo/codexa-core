# Regulatory Framework - Brazilian E-commerce Compliance

**Version**: 1.0.0
**Updated**: 2025-12-05
**Type**: Knowledge Card (CRITICAL)
**Cross-Reference**: anuncio_agent, pesquisa_agent, marca_agent

---

## OVERVIEW

Brazilian e-commerce operates under multiple regulatory bodies. Non-compliance can result in listing removal, account suspension, fines, or legal action.

### Regulatory Hierarchy

```
Constitution (Consumer Rights)
    |
    v
CDC (Consumer Defense Code) - Lei 8.078/1990
    |
    +-- CONAR (Advertising Self-Regulation)
    |
    +-- ANVISA (Health Products)
    |
    +-- INMETRO (Technical Standards)
    |
    +-- ANATEL (Telecommunications)
    |
    +-- Marketplace-Specific Policies
```

---

## 1. CDC - CODIGO DE DEFESA DO CONSUMIDOR

**Scope**: All consumer transactions in Brazil
**Enforcement**: PROCON (state level), Judiciary

### Key Requirements for E-commerce

| Requirement | Description | Penalty |
|-------------|-------------|---------|
| Clear Pricing | Price must include all taxes/fees | Fine + listing removal |
| Product Information | Complete, accurate description | Fine + damages |
| Right to Regret | 7-day return for online purchases | Mandatory refund |
| Warranty | Minimum 90 days (durable goods) | Legal action |
| Delivery Commitment | Stated deadline must be met | Fine + damages |

### Prohibited Practices (Art. 37)

```
MISLEADING ADVERTISING (Publicidade Enganosa):
- False claims about product characteristics
- Hidden defects or limitations
- Fake discounts (original price manipulation)
- False scarcity ("last units!")
- Unverified testimonials

ABUSIVE ADVERTISING (Publicidade Abusiva):
- Discrimination of any kind
- Exploiting fear or superstition
- Inciting violence
- Exploiting children's vulnerability
- Environmental misinformation
```

### Copy Implications

| Avoid | Use Instead |
|-------|-------------|
| "Melhor do mercado" (without proof) | "Alta qualidade" + specific features |
| "100% natural" (unverified) | "Ingredientes naturais selecionados" |
| "Cura/trata" (medical claims) | "Auxilia no/Contribui para" |
| "Ultimas unidades" (false) | Real stock information |
| "De R$X por R$Y" (fake original) | Documented original price |

---

## 2. ANVISA - AGENCIA NACIONAL DE VIGILANCIA SANITARIA

**Scope**: Health products, food, cosmetics, supplements
**Website**: anvisa.gov.br

### Product Categories Requiring ANVISA

| Category | Registration Type | Requirement Level |
|----------|-------------------|-------------------|
| Medicamentos | Registro | MANDATORY |
| Suplementos Alimentares | Notificacao | MANDATORY |
| Cosmeticos | Notificacao/Registro | MANDATORY |
| Alimentos | Depends on type | VARIES |
| Saneantes (cleaning) | Notificacao | MANDATORY |
| Produtos para Saude | Registro | MANDATORY |

### Registration Number Format

```
ANVISA Registration: XX.XXX.XXXX/XXXX-XX
                     |  |    |     |   |
                     |  |    |     |   +-- Check digit
                     |  |    |     +------ Year
                     |  |    +------------ Sequential
                     |  +----------------- Category
                     +-------------------- Entity type
```

### Copy Requirements by Category

**Suplementos Alimentares**:
```
REQUIRED DISCLAIMERS:
- "Este produto nao e um medicamento"
- "Nao exceder a recomendacao diaria de consumo indicada na embalagem"
- "Mantenha fora do alcance de criancas"

PROHIBITED CLAIMS:
- Therapeutic claims (cura, trata, previne)
- Weight loss promises without evidence
- Performance enhancement without studies
- Comparison with medications
```

**Cosmeticos**:
```
REQUIRED:
- ANVISA notification number
- Ingredients list (INCI names)
- Usage instructions
- Expiration date

PROHIBITED:
- Medical/therapeutic claims
- "Dermatologicamente testado" without proof
- "Hipoalergenico" without studies
- Before/after photos suggesting treatment
```

**Alimentos**:
```
REQUIRED (varies by category):
- Nutritional table
- Ingredients list
- Allergen warnings (MANDATORY)
- Storage instructions
- Validity date

ALLERGEN WARNING FORMAT:
"ALERGENICOS: CONTEM [ALLERGEN]"
"ALERGENICOS: PODE CONTER [ALLERGEN]"
```

### ANVISA Violation Consequences

| Violation | Consequence |
|-----------|-------------|
| No registration | Product seizure, fine R$2K-1.5M |
| False claims | Fine, product recall |
| Missing disclaimers | Warning, fine |
| Therapeutic claims | Severe fine, legal action |

---

## 3. INMETRO - INSTITUTO NACIONAL DE METROLOGIA

**Scope**: Product safety, technical standards, metrology
**Website**: inmetro.gov.br

### Mandatory Certification Categories

| Category | Certification | Products |
|----------|---------------|----------|
| Eletroeletronicos | INMETRO seal | Chargers, adapters, LEDs |
| Brinquedos | INMETRO seal | All toys for children |
| EPIs | CA number | Safety equipment |
| Autopecas | INMETRO | Brake pads, lights |
| Moveis | INMETRO | Cribs, chairs |
| Capacetes | INMETRO | Motorcycle, bicycle |

### INMETRO Seal Format

```
SELO INMETRO:
+------------------------+
|      INMETRO          |
|    [Organismo]        |
|   Registro: XXXXX     |
|   Validade: XX/XXXX   |
+------------------------+
```

### Product-Specific Requirements

**Eletronicos (Electronics)**:
```
REQUIRED:
- INMETRO certification seal
- Voltage specification (127V, 220V, bivolt)
- Power consumption (W)
- Certification organism name
- Registration number

PROHIBITED:
- Uncertified imports
- Products without voltage marking
- Safety claims without certification
```

**Brinquedos (Toys)**:
```
REQUIRED:
- INMETRO certification
- Age indication ("Nao recomendado para menores de X anos")
- Choking hazard warning (small parts)
- Material composition
- Manufacturer/importer identification

MANDATORY WARNINGS:
- "ATENCAO: CONTEM PECAS PEQUENAS. NAO RECOMENDADO PARA CRIANCAS MENORES DE 3 ANOS"
- Age-appropriate warnings per product
```

**EPIs (Safety Equipment)**:
```
REQUIRED:
- CA (Certificado de Aprovacao) number
- Validity date
- Protection level/class
- Usage instructions
- Maintenance requirements

CA FORMAT: CA XXXXX
```

### Copy Implications

| Product Type | Required in Listing |
|--------------|---------------------|
| Electronics | INMETRO registration, voltage |
| Toys | Age recommendation, INMETRO |
| Safety Equipment | CA number, protection class |
| Auto Parts | INMETRO certification |

---

## 4. CONAR - CONSELHO NACIONAL DE AUTORREGULAMENTACAO PUBLICITARIA

**Scope**: Advertising ethics and self-regulation
**Website**: conar.org.br

### CONAR Code Key Principles

| Principle | Description |
|-----------|-------------|
| Honestidade | No deception, no omission of relevant facts |
| Responsabilidade Social | No prejudice to society or environment |
| Identificacao | Ads must be identifiable as such |
| Fundamentacao | Claims must be substantiated |
| Respeitabilidade | No offense to moral standards |

### Prohibited Advertising Practices

```
COMPARATIVE ADVERTISING:
- Must be objective and verifiable
- Cannot denigrate competitors
- Must compare similar products
- Claims must be documented

TESTIMONIALS:
- Must be genuine and verifiable
- Person must have actually used product
- Cannot imply guaranteed results
- Celebrities must disclose sponsorship

CHILDREN (under 12):
- Cannot directly address children
- Cannot use children's trust
- Cannot suggest social advantage
- Cannot use cartoon characters to sell

ENVIRONMENTAL CLAIMS:
- "Ecologico" - must be certified
- "Sustentavel" - must be documented
- "100% reciclavel" - must be accurate
- Carbon neutral claims - must be verified
```

### Copy Safe Harbor Phrases

| Instead of | Use |
|------------|-----|
| "O melhor" | "Um dos melhores" or specific ranking with source |
| "O mais vendido" | "Entre os mais vendidos" + source |
| "Revolucionario" | "Inovador" or specific innovation |
| "Garantido" | "Satisfacao garantida conforme CDC" |
| "Natural" | "Com ingredientes naturais" |

---

## 5. ANATEL - AGENCIA NACIONAL DE TELECOMUNICACOES

**Scope**: Telecommunications equipment
**Website**: anatel.gov.br

### Products Requiring Homologation

| Category | Examples | Requirement |
|----------|----------|-------------|
| Wireless | Bluetooth, WiFi devices | Homologation |
| Mobile | Smartphones, tablets | Homologation |
| Telecom | Modems, routers | Homologation |
| Radiocommunication | Walkie-talkies | Homologation |

### Homologation Number Format

```
ANATEL: XXXXX-XX-XXXXX
        |     |  |
        |     |  +-- Sequential
        |     +----- Year
        +----------- Category code
```

### Copy Requirements

```
REQUIRED IN LISTING:
- Homologation number
- "Este produto e homologado pela ANATEL"
- Frequency/band information (if applicable)

PROHIBITED:
- Selling non-homologated wireless devices
- Claiming compatibility without verification
- Omitting certification requirements
```

---

## COMPLIANCE CHECKLIST BY CATEGORY

### Electronics

```markdown
[ ] INMETRO certification number
[ ] Voltage specification (127V/220V/Bivolt)
[ ] Power consumption (Watts)
[ ] ANATEL homologation (if wireless)
[ ] Warranty information (minimum 90 days)
[ ] Safety warnings
[ ] Manufacturer/importer CNPJ
```

### Health & Beauty

```markdown
[ ] ANVISA notification/registration number
[ ] Ingredients list (INCI format for cosmetics)
[ ] Usage instructions
[ ] Contraindications/warnings
[ ] Expiration date mention
[ ] Required disclaimers
[ ] No therapeutic claims
```

### Toys

```markdown
[ ] INMETRO certification
[ ] Age recommendation
[ ] Small parts warning (if applicable)
[ ] Material composition
[ ] Safety instructions
[ ] Manufacturer identification
```

### Food & Supplements

```markdown
[ ] ANVISA registration (if applicable)
[ ] Nutritional information
[ ] Ingredients list
[ ] Allergen warnings (BOLD, CAPS)
[ ] Storage instructions
[ ] Expiration date mention
[ ] Required disclaimers for supplements
```

### Safety Equipment (EPI)

```markdown
[ ] CA (Certificado de Aprovacao) number
[ ] Protection class/level
[ ] Usage instructions
[ ] Maintenance requirements
[ ] Validity information
[ ] Manufacturer data
```

---

## MARKETPLACE COMPLIANCE INTEGRATION

### Mercado Livre

| Regulation | ML Policy |
|------------|-----------|
| ANVISA | Required for health categories |
| INMETRO | Required for regulated categories |
| CDC | Strictly enforced (7-day returns) |
| CONAR | No misleading claims |

**Auto-flagged terms**: "cura", "trata", "milagroso", "100% natural" (health), "original" (without brand auth)

### Shopee

| Regulation | Shopee Policy |
|------------|---------------|
| ANVISA | Required, less strict verification |
| INMETRO | Required for key categories |
| CDC | Enforced via disputes |
| CONAR | Monitored for reports |

**Auto-flagged terms**: Similar to ML, less aggressive filtering

### Amazon

| Regulation | Amazon Policy |
|------------|---------------|
| ANVISA | Strict verification |
| INMETRO | Category-specific |
| CDC | Full compliance required |
| CONAR | Style guide enforced |

**Auto-flagged terms**: Aggressive filtering, documentation required

### Magalu

| Regulation | Magalu Policy |
|------------|---------------|
| ANVISA | Mandatory for applicable categories |
| INMETRO | Strictly required |
| CDC | Full compliance |
| EAN | Mandatory for all products |

**Special**: EAN code validation, stricter than other platforms

---

## VIOLATION CONSEQUENCES

| Level | Description | Consequence |
|-------|-------------|-------------|
| Warning | First minor offense | Listing edit required |
| Suspension | Repeated violations | Account limited |
| Removal | Serious violation | Product/listing removed |
| Ban | Severe/repeated | Account terminated |
| Legal | Criminal/civil violation | Fines, prosecution |

### Fine Ranges

| Agency | Fine Range |
|--------|------------|
| PROCON (CDC) | R$400 - R$7M |
| ANVISA | R$2K - R$1.5M |
| INMETRO | R$100 - R$1.5M |
| CONAR | Public retraction, no fines (self-regulation) |

---

## METADATA

```json
{
  "knowledge_type": "regulatory_compliance",
  "jurisdiction": "Brazil",
  "agencies_covered": ["CDC", "ANVISA", "INMETRO", "CONAR", "ANATEL"],
  "last_verified": "2025-12-05",
  "update_frequency": "as_regulations_change",
  "priority": "CRITICAL",
  "sources": [
    "planalto.gov.br",
    "anvisa.gov.br",
    "inmetro.gov.br",
    "conar.org.br",
    "anatel.gov.br"
  ]
}
```

---

**Status**: Active
**Priority**: CRITICAL - Always load for regulated product categories
