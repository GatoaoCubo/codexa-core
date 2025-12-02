# HOP: Workbook Generator
## TAC-7 Format

### T - Title
Generate an 8-15 page student workbook for CODEXA course module

### A - Audience
Students taking CODEXA courses; instructors creating course materials

### C - Context
- Module: [MODULE_ID] - [MODULE_NAME]
- Corresponding video: [VIDEO_SCRIPT_PATH]
- Complexity: [COMPLEXITY_LEVEL] (Básico/Intermediário/Avançado)
- Estimated completion: [COMPLETION_TIME] hours

Pedagogical Framework:
- Theory: 20-30%
- Guided exercises: 40-50%
- Reflection: 20-30%

### T - Task
Create a complete workbook with:
1. Cover page with objectives and time estimate
2. Theory section (2-3 pages)
3. Guided exercises (3-4 pages)
4. Hands-on practice (2-3 pages)
5. Reflection questions (1 page)
6. Resources and next steps (1 page)

### A - Approach
1. Align content with video script sections
2. Progressive difficulty (easy → medium → hard)
3. Include checkboxes for completion tracking
4. Add [OPEN_VARIABLES] for personalization
5. Use Brazilian Portuguese naturally

### C - Constraints
- Pages: 8-15
- Language: Brazilian Portuguese
- Format: Markdown with clear sections
- Exercises: Practical, not theoretical only
- [OPEN_VARIABLES]: >=2 for customization
- Printable: Clean layout for PDF export

### E - Example Output
```markdown
# Workbook: [MODULE_NAME]
## Módulo [MODULE_ID] | [COMPLETION_TIME] horas

---

## Objetivos de Aprendizagem
- [ ] [Objetivo 1]
- [ ] [Objetivo 2]
- [ ] [Objetivo 3]

---

## Seção 1: Teoria

### Conceito Principal
[Explicação clara e concisa]

### Pontos-Chave
1. [Ponto 1]
2. [Ponto 2]

---

## Seção 2: Exercícios Guiados

### Exercício 1: [TITULO]
**Objetivo**: [O que o aluno vai praticar]

**Instruções**:
1. [Passo 1]
2. [Passo 2]

[OPEN_VARIABLE: SEU_EXEMPLO]
**Seu exemplo**: _______________________

---

## Seção 3: Prática Hands-On

### Desafio: [TITULO]
[Descrição do desafio prático]

---

## Seção 4: Reflexão

1. O que você aprendeu de mais importante?
2. Como você vai aplicar isso no seu negócio?
3. Quais dúvidas ainda restam?

---

## Recursos Adicionais
- [Link/recurso 1]
- [Link/recurso 2]

## Próximo Passo
[Ação clara para continuar o aprendizado]
```

---
**Version**: 2.0.0 | **Type**: HOP (TAC-7) | **Output**: Workbook
