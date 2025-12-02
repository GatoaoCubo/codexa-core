<!-- iso_vectorstore -->
<!--
  Source: HOP_LANDING_PAGE.md
  Agent: curso_agent
  Synced: 2025-11-30
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# HOP: Landing Page Structure Generator
## TAC-7 Format

### T - Title
Generate complete landing page wireframe and copy for CODEXA course

### A - Audience
Web designers, marketers building Hotmart course pages

### C - Context
- Course: [COURSE_NAME]
- Platform: Hotmart
- Price: R$ [PRICE]
- Modules: [MODULE_COUNT]

Page Sections (Order):
1. Hero
2. Problem
3. Solution
4. Curriculum
5. Instructor
6. Proof
7. Pricing
8. FAQ
9. Final CTA

### T - Task
Create landing page with:
1. Each section's copy
2. Visual suggestions (images, icons)
3. Mobile-first considerations
4. Hotmart integration points

### A - Approach
1. Above-the-fold: Hero + CTA must convert
2. Scroll depth: Key info in first 3 sections
3. Social proof: Spread throughout
4. Multiple CTAs: After each major section
5. Include [OPEN_VARIABLES] for customization

### C - Constraints
- Hotmart checkout integration
- Mobile responsive
- LGPD compliant (cookie notice, privacy)
- Garantia visible
- No hype words
- Load speed: Optimize images
- [OPEN_VARIABLES]: >=4

### E - Example Output
```markdown
# Landing Page: [COURSE_NAME]

---

## Section 1: HERO
**Position**: Above the fold

### Elements
- [ ] Background: [OPEN_VARIABLE: HERO_IMAGE]
- [ ] Headline: [Transformação em 1 frase]
- [ ] Subheadline: [Como/Quem/Por que]
- [ ] CTA Button: [Texto do botão]
- [ ] Social proof mini: [X alunos / X avaliação]

### Copy
**H1**: [Headline principal]
**H2**: [Subheadline]
**CTA**: [Botão]

---

## Section 2: PROBLEM
**Position**: First scroll

### Elements
- [ ] Icon list or illustration
- [ ] 3-5 pain points

### Copy
**Headline**: Você reconhece esses problemas?
- [Dor 1]
- [Dor 2]
- [Dor 3]

---

## Section 3: SOLUTION
**Position**: Second scroll

### Elements
- [ ] Course mockup/preview
- [ ] Key benefits (3-5)

### Copy
**Headline**: [Como o curso resolve]
**Benefits**:
1. [Benefício 1] → [Resultado]
2. [Benefício 2] → [Resultado]

---

## Section 4: CURRICULUM
**Position**: Middle page

### Elements
- [ ] Accordion or tabs
- [ ] Module icons
- [ ] Time estimates

### Copy
[OPEN_VARIABLE: CURRICULUM]
**Módulo 1**: [Título] - [Duração]
- Aula 1.1: [Tema]
- Aula 1.2: [Tema]
...

---

## Section 5: INSTRUCTOR
**Position**: After curriculum

### Elements
- [ ] Photo: [OPEN_VARIABLE: INSTRUCTOR_PHOTO]
- [ ] Bio
- [ ] Credentials

### Copy
**Name**: [Nome]
**Bio**: [2-3 parágrafos]
**Credentials**: [Lista]

---

## Section 6: PROOF
**Position**: Before pricing

### Elements
- [ ] Testimonials (video preferred)
- [ ] Results/numbers
- [ ] Logos (if B2B)

### Copy
[OPEN_VARIABLE: TESTIMONIALS]
"[Depoimento]" - [Nome, Cargo]

---

## Section 7: PRICING
**Position**: Late page

### Elements
- [ ] Price display
- [ ] Payment options
- [ ] Bonus list
- [ ] Garantia badge

### Copy
**Price**: R$ [PRICE]
**Parcelamento**: até 12x
**Garantia**: [X] dias
**Bônus**: [Lista]

---

## Section 8: FAQ
**Position**: Before final CTA

### Questions (5-7)
1. Para quem é este curso?
2. Quanto tempo tenho acesso?
3. Tem garantia?
4. Preciso de conhecimento prévio?
5. Como funciona o suporte?

---

## Section 9: FINAL CTA
**Position**: Footer area

### Elements
- [ ] Urgency element (if real)
- [ ] Main CTA button
- [ ] Garantia reminder
- [ ] Support contact

### Copy
**Headline**: [Chamada final]
**CTA**: [Botão]
**Footer**: Garantia [X] dias | Suporte [canal]
```

---
**Version**: 2.0.0 | **Type**: HOP (TAC-7) | **Output**: Landing Page
