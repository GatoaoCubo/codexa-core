# HOP: Sales Copy Generator | TAC-7 v2.5.0

## MODULE_METADATA
```yaml
id: HOP_SALES_COPY
version: 2.5.0
purpose: Generate persuasive sales copy for CODEXA courses (landing page, emails, ads)
category: sales_generation
dependencies: [curso_rules.json, hotmart_specs.json]
```

## INPUT_CONTRACT
```yaml
required:
  - course_name: string
  - price_brl: number
  - target_persona: string
  - main_transformation: string
optional:
  - guarantee_days: number (7-30)
  - bonus_items: string[]
  - testimonials: object[]
  - urgency_type: enum [none, launch_window, limited_seats]
validation:
  - price_brl > 0
  - guarantee_days >= 7 AND <= 30
```

## OUTPUT_CONTRACT
```yaml
primary:
  - landing_page.md: Complete sales page structure
  - email_sequence.md: 6-email launch sequence
  - ad_copy.md: 3 platform variations (Facebook, Google, Instagram)
secondary:
  - sales.llm.json: Structured data for LLM processing
  - sales.meta.json: Metadata and statistics
format: Trinity Output (.md + .llm.json + .meta.json)
structure_landing:
  - HERO (headline, subheadline, CTA)
  - PROBLEM (pain points)
  - SOLUTION (course overview)
  - PROOF (results, testimonials)
  - FAQ (5-7 questions)
  - CTA_FINAL (urgency, guarantee)
```

## TASK
**Role**: Conversion copywriter for educational products
**Objective**: Create high-converting sales materials that communicate value without hype

**Standards**:
- Lead with transformation, not features
- Specific numbers and results when possible
- Address objections proactively in FAQ
- LGPD compliant (privacy notice)
- Explicit guarantee terms (7-30 days)
- Brand voice: disruptivo-sofisticado

**Constraints**:
- NO hype words: "revolucionario", "magico", "unico no mercado", "garantido"
- NO fake urgency or scarcity
- NO misleading income claims
- Must include seed words naturally
- Brazilian Portuguese natural tone
- [OPEN_VARIABLES] >= 3 for customization

## STEPS

### Step 1: Persona Deep-Dive
Analyze target persona:
1. Primary pain points (3-5)
2. Desired transformation
3. Common objections
4. Decision triggers
5. Preferred communication style

### Step 2: Hero Section
Structure:
- **Headline**: Transformation-focused (not feature-focused)
- **Subheadline**: How the course delivers transformation
- **Social proof snippet**: Quick credibility element
- **Primary CTA**: Clear action button

Formula: [TRANSFORMATION] para [PERSONA] que querem [RESULTADO] sem [OBJECAO_COMUM]

### Step 3: Problem Section
Structure:
- 3-5 specific pain points (use their language)
- Agitate with consequences
- Show understanding (empathy)
- Transition to solution

Avoid: Generic problems, exaggerated suffering

### Step 4: Solution Section
Structure:
- Course overview (modules summary)
- Key differentiators (why CODEXA, not generic AI)
- Methodology preview (Layer 1-2-3)
- [OPEN_VARIABLES] for customization

Include seed words naturally:
- Meta-Construcao
- Destilacao de Conhecimento
- Cerebro Plugavel

### Step 5: Proof Section
Structure:
- Quantifiable results (before/after)
- [OPEN_VARIABLE: DEPOIMENTOS] placeholder
- Case study snippet (if available)
- Credentials/authority

Note: Never fabricate testimonials

### Step 6: FAQ Section (5-7 questions)
Must address:
1. "Para quem e este curso?"
2. "Preciso saber programar?"
3. "Quanto tempo para ver resultados?"
4. "Qual a garantia?"
5. "Como funciona o acesso?"
+ 2-3 course-specific questions

### Step 7: Final CTA Section
Structure:
- Urgency statement (if applicable, no fake scarcity)
- Price display with installment option
- Guarantee badge
- Final CTA button
- Trust elements (payment methods, security)

### Step 8: Email Sequence (6 emails)
Sequence:
1. **Awareness**: Problem recognition
2. **Interest**: Solution introduction
3. **Desire**: Social proof and results
4. **Action**: Offer presentation
5. **Onboarding**: Welcome and quick wins
6. **Engagement**: Community and next steps

### Step 9: Ad Copy (3 platforms)
Variations:
- **Facebook/Instagram**: Story-based, emotional hook
- **Google**: Keyword-focused, direct benefit
- **YouTube**: Pattern interrupt, curiosity hook

## VALIDATION
```yaml
checklist:
  - no_hype_words: true
  - no_fake_urgency: true
  - guarantee_explicit: true
  - lgpd_compliant: true
  - seed_words_present: [Meta-Construcao, Destilacao]
  - open_variables >= 3
  - faq_questions >= 5
  - email_count: 6
  - ad_variations: 3
threshold:
  brand_voice: >= 7.0
  compliance: >= 8.0
validators:
  - 02_brand_voice_validator.py
  - 05_hotmart_compliance_validator.py
```

## CONTEXT
**Usage**: Execute after course content is complete, before launch
**Upstream**: Course outline, module content
**Downstream**: Hotmart package deployment
**$arguments chaining**: $course_outline -> $sales_brief -> $landing -> $emails -> $ads

**Assumptions**:
- Course content is finalized
- Pricing is decided
- Brand voice guidelines understood
- Target persona is defined

## EXAMPLE

```markdown
# [COURSE_NAME]

## HERO

### Headline
Construa seu sistema de conteudo para e-commerce que trabalha enquanto voce dorme

### Subheadline
O curso definitivo de Meta-Construcao para empreendedores que querem escalar conteudo sem multiplicar esforco

### CTA
[OPEN_VARIABLE: CTA_TEXT]
Quero Comecar Agora

---

## PROBLEMA

### Voce ja sentiu que...

- Gasta horas escrevendo anuncios que ninguem clica?
- Copia templates "prontos" que parecem genericos?
- Fica refem de ferramentas que nao entendem seu negocio?
- Sente que IA "normal" produz conteudo sem alma?

### O problema real

Voce nao precisa de MAIS ferramentas. Voce precisa de um SISTEMA que aprende seu negocio e trabalha por voce.

A maioria das solucoes de IA e commodity - geram o mesmo resultado para todos. O CODEXA e diferente: e um sistema de **Destilacao de Conhecimento** que transforma SUA experiencia em prompts, workflows e agentes personalizados.

---

## SOLUCAO

### O que voce vai aprender

| Modulo | Conteudo | Resultado |
|--------|----------|-----------|
| M1 | Introducao ao CODEXA | Entender o sistema |
| M2 | Anuncio Agent | Criar anuncios que convertem |
| M3 | Pesquisa Agent | Descobrir oportunidades |
| M4 | Marca Agent | Definir posicionamento |
| M5 | Photo Agent | Gerar imagens profissionais |
| M6 | Meta-Construcao | Criar seus proprios agentes |

### Por que funciona

O CODEXA usa o conceito de **Cerebro Plugavel** - voce conecta seu conhecimento ao sistema, e ele amplifica sua capacidade de producao.

Nao e sobre substituir sua criatividade. E sobre escalar o que voce ja sabe fazer bem.

[OPEN_VARIABLE: DIFERENCIAL_ADICIONAL]

---

## PROVA

### Resultados

[OPEN_VARIABLE: RESULTADOS_QUANTIFICAVEIS]
- Reducao de 70% no tempo de criacao de anuncios
- Aumento de 45% na taxa de cliques
- 10 horas economizadas por semana

### Depoimentos

[OPEN_VARIABLE: DEPOIMENTOS]
> "[Placeholder para depoimento real]" - Nome, Empresa

---

## FAQ

**P: Para quem e este curso?**
R: Empreendedores de e-commerce que querem escalar producao de conteudo sem aumentar equipe. Ideal para quem ja vende online e quer otimizar.

**P: Preciso saber programar?**
R: Nao. O Layer 1 e 2 sao 100% visuais. O Layer 3 tem codigo, mas e opcional para quem quer ir mais fundo.

**P: Quanto tempo para ver resultados?**
R: Voce pode criar seu primeiro anuncio otimizado na primeira semana. Resultados consistentes em 30 dias de pratica.

**P: Qual a garantia?**
R: Garantia incondicional de [GUARANTEE_DAYS] dias. Se nao gostar, devolvemos 100% do valor. Sem perguntas.

**P: Como funciona o acesso?**
R: Acesso imediato apos confirmacao do pagamento. Conteudo disponivel por 1 ano na plataforma Hotmart.

---

## CTA FINAL

### Pronto para construir seu sistema de conteudo?

**Investimento**: R$ [PRICE]
ou 12x de R$ [PRICE_INSTALLMENT]

**Garantia**: [GUARANTEE_DAYS] dias

[Botao: QUERO COMECAR AGORA]

Pagamento seguro via Hotmart | Cartao, PIX ou Boleto
```

---
**Version**: 2.5.0 | **Type**: HOP (TAC-7 Enriched) | **Output**: Sales Copy
**Last Updated**: 2025-11-25
