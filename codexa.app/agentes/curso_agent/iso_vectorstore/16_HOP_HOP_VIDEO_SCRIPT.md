<!-- iso_vectorstore -->
<!--
  Source: HOP_VIDEO_SCRIPT.md
  Agent: curso_agent
  Synced: 2025-11-30
  Version: 2.0.0
  Package: iso_vectorstore (export package)
-->

# HOP: Video Script Generator
## TAC-7 Format

### T - Title
Generate a 15-30 minute video script for CODEXA course module

### A - Audience
Course creators building CODEXA-based educational content for Brazilian market

### C - Context
- Module: [MODULE_ID] - [MODULE_NAME]
- Layer: [LAYER_LEVEL] (1=Conceito, 2=Prática, 3=Mestria)
- Prerequisites: [PREREQUISITES]
- Duration target: [DURATION_MINUTES] minutes

Brand Voice:
- Seed words: Meta-Construção, Destilação de Conhecimento, Cérebro Plugável
- Tone: Disruptivo-sofisticado
- Avoid: Revolucionário, mágico, único no mercado

### T - Task
Create a complete video script with:
1. Hook (<=90 seconds) that captures attention
2. Clear learning objectives (measurable)
3. Content sections with timing marks [00:00]
4. Real CODEXA demonstrations
5. Brazilian market examples
6. Recap and call-to-action

### A - Approach
1. Start with problem/pain point (not feature)
2. Use storytelling with real scenarios
3. Include [OPEN_VARIABLES] for customization (>=2)
4. Add timing marks every 2-3 minutes
5. End with actionable next step

### C - Constraints
- Duration: 15-30 minutes
- Hook: <=90 seconds
- [OPEN_VARIABLES]: >=2
- No hype words (revolucionário, mágico, único)
- Examples: Brazilian market context
- Demo: Real CODEXA usage

### E - Example Output
```markdown
# Módulo [MODULE_ID]: [MODULE_NAME]
## Duração: [DURATION] minutos

### HOOK [00:00 - 01:30]
[Problema/dor do público]

### OBJETIVOS [01:30 - 02:00]
Ao final deste módulo, você será capaz de:
1. [Objetivo mensurável 1]
2. [Objetivo mensurável 2]

### CONTEÚDO [02:00 - 25:00]
#### Seção 1: [TITULO] [02:00 - 08:00]
[Conteúdo com demonstração CODEXA]

[OPEN_VARIABLE: EXEMPLO_NEGOCIO]
Exemplo: [Inserir caso do seu negócio]

...

### RECAP [25:00 - 28:00]
[Resumo dos pontos principais]

### CTA [28:00 - 30:00]
[Próximo passo acionável]
```

---
**Version**: 2.0.0 | **Type**: HOP (TAC-7) | **Output**: Video Script
