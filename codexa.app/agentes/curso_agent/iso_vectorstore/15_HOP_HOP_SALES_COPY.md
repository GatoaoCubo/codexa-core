<!-- iso_vectorstore -->
<!--
  Source: HOP_SALES_COPY.md
  Agent: curso_agent
  Synced: 2025-11-30
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# HOP: Sales Copy Generator
## TAC-7 Format

### T - Title
Generate persuasive sales copy for CODEXA course landing page

### A - Audience
Marketing teams, course creators selling CODEXA courses in Brazilian market

### C - Context
- Course: [COURSE_NAME]
- Price: R$ [PRICE]
- Target customer: [TARGET_PERSONA]
- Main transformation: [TRANSFORMATION]

Brand Voice:
- Seed words: Meta-Construção, Destilação de Conhecimento, Cérebro Plugável
- Tone: Disruptivo-sofisticado
- Attack: Banalização, lock-in, commodity knowledge
- NEVER use: Revolucionário, mágico, único no mercado

### T - Task
Create landing page copy with:
1. Hero section (headline + subheadline + CTA)
2. Problem section (pain points)
3. Solution section (how course solves)
4. Proof section (results, testimonials placeholder)
5. FAQ section (5-7 questions)
6. Final CTA section

### A - Approach
1. Lead with transformation, not features
2. Use specific numbers when possible
3. Address objections in FAQ
4. Create urgency without fake scarcity
5. Include [OPEN_VARIABLES] for customization

### C - Constraints
- No hype words (revolucionário, mágico, único)
- No fake urgency or scarcity
- LGPD compliant (privacy notice)
- Garantia: 7-30 days explicit
- Brazilian Portuguese natural tone
- [OPEN_VARIABLES]: >=3

### E - Example Output
```markdown
# [COURSE_NAME]

## HERO
### Headline
[Transformação principal em uma frase]

### Subheadline
[Como o curso entrega essa transformação]

### CTA
[OPEN_VARIABLE: CTA_TEXT]
[Texto do botão de ação]

---

## PROBLEMA
### Você já sentiu que...
- [Dor 1]
- [Dor 2]
- [Dor 3]

### O problema real
[Explicação do problema raiz]

---

## SOLUÇÃO
### O que você vai aprender
1. Módulo 1: [Título] - [Benefício]
2. Módulo 2: [Título] - [Benefício]
...

### Por que funciona
[Diferencial da metodologia CODEXA]

---

## PROVA
### Resultados
[OPEN_VARIABLE: RESULTADOS]
- [Resultado quantificável 1]
- [Resultado quantificável 2]

### Depoimentos
[OPEN_VARIABLE: DEPOIMENTOS]
"[Placeholder para depoimento]" - [Nome]

---

## FAQ
**P: [Pergunta 1]**
R: [Resposta]

**P: Qual a garantia?**
R: Garantia incondicional de [7-30] dias.

---

## CTA FINAL
### [Headline de urgência sem fake scarcity]

[Botão CTA]

**Garantia**: [X] dias | **Suporte**: [Canal]
```

---
**Version**: 2.0.0 | **Type**: HOP (TAC-7) | **Output**: Sales Copy
