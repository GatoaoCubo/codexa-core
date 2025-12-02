# HOP: Email Sequence Generator
## TAC-7 Format

### T - Title
Generate a 6-email nurture sequence for CODEXA course launch

### A - Audience
Email marketers, course creators building launch sequences

### C - Context
- Course: [COURSE_NAME]
- Launch date: [LAUNCH_DATE]
- Target: [TARGET_PERSONA]
- Price: R$ [PRICE]

Sequence Structure:
1. Awareness (emails 1-2)
2. Consideration (emails 3-4)
3. Action (emails 5-6)

Brand Voice:
- Tone: Disruptivo-sofisticado
- Personal, not corporate
- Value-first approach

### T - Task
Create 6 emails with:
1. Email 1: Problem awareness
2. Email 2: Solution introduction
3. Email 3: Social proof / case study
4. Email 4: Objection handling
5. Email 5: Urgency (real, not fake)
6. Email 6: Final call + reminder

Each email needs:
- Subject line (A/B options)
- Preview text
- Body copy
- CTA

### A - Approach
1. Each email stands alone but builds on previous
2. Subject lines: Curiosity or benefit-driven
3. Keep emails scannable (short paragraphs)
4. One clear CTA per email
5. Include [OPEN_VARIABLES] for personalization

### C - Constraints
- No spam trigger words
- CAN-SPAM compliant (unsubscribe)
- No fake scarcity or urgency
- Max 300 words per email body
- [OPEN_VARIABLES]: >=1 per email
- Brazilian Portuguese

### E - Example Output
```markdown
# Email Sequence: [COURSE_NAME]

---

## EMAIL 1: Awareness
**Send**: D-7 (7 dias antes do lançamento)

### Subject Line
A: [Pergunta provocativa]
B: [Dado surpreendente]

### Preview Text
[Complemento do subject]

### Body
Olá [OPEN_VARIABLE: NOME],

[Parágrafo 1: Identificar a dor]

[Parágrafo 2: Validar a frustração]

[Parágrafo 3: Teaser da solução]

[CTA: Saiba mais / Leia o artigo]

[Assinatura]

---

## EMAIL 2: Solution Introduction
**Send**: D-5

### Subject Line
A: [Benefício principal]
B: [Como resolver o problema]

...

---

## EMAIL 6: Final Call
**Send**: D+1 (ou deadline)

### Subject Line
A: Últimas horas: [Oferta]
B: [Nome], sua decisão

### Body
[Urgência real: deadline de preço/bônus]

[Recap dos benefícios principais]

[CTA Final]

[P.S.: Garantia reminder]
```

---
**Version**: 2.0.0 | **Type**: HOP (TAC-7) | **Output**: Email Sequence
