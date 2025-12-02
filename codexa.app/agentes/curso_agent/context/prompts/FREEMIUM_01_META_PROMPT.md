# FREEMIUM 01: META-PROMPT | O Construtor Universal de Prompts

**ID**: FREEMIUM_01_META_PROMPT | **Version**: 1.0.0 | **Created**: 2025-11-29
**Purpose**: Teach LLMs to build structured prompts FOR you (delegation)
**Language**: Instructions in English | Output in Brazilian Portuguese (PT-BR)
**Compatibility**: ChatGPT, Claude, Gemini, Llama, Mistral (any LLM)
**Domain**: Universal (works for ANY task, ANY industry)
**Core Concept**: DELEGATION - Stop writing prompts, start delegating

---

## TABLE OF CONTENTS

1. [The Paradigm Shift](#1-the-paradigm-shift)
2. [Why Meta-Prompts Matter](#2-why-meta-prompts-matter)
3. [The Framework](#3-the-framework)
4. [The Universal Meta-Prompt](#4-the-universal-meta-prompt)
5. [Domain Variations](#5-domain-variations)
6. [Advanced Techniques](#6-advanced-techniques)
7. [Example Outputs](#7-example-outputs)
8. [Building Your Prompt Library](#8-building-your-prompt-library)
9. [Common Mistakes](#9-common-mistakes)
10. [Integration with Plan & Implement](#10-integration-with-plan--implement)

---

## 1. THE PARADIGM SHIFT

### The Old Way (You Work, AI Assists)

```
YOU write detailed prompt
  → YOU structure it correctly
  → YOU anticipate edge cases
  → YOU iterate and refine
  → AI executes

Result: You do 80% of the cognitive work
```

### The New Way (AI Works, You Direct)

```
YOU describe what you want (1 sentence)
  → AI asks clarifying questions
  → AI structures the prompt
  → AI anticipates edge cases
  → YOU approve or adjust
  → AI executes with its own prompt

Result: You do 20% of the cognitive work
```

### The Core Insight

**You don't need to learn "prompt engineering."**
**You need to learn "prompt delegation."**

The AI already knows how to write good prompts. It's been trained on millions
of them. Your job is to DIRECT the AI to build the right prompt for YOUR need.

This is what we call a **META-PROMPT** - a prompt that generates prompts.

---

## 2. WHY META-PROMPTS MATTER

### Problem 1: The Knowledge Gap

To write a good prompt, you need to know:
- Optimal structure (role, context, task, format)
- Best practices for the specific task type
- Edge cases to handle
- Output format specifications
- Constraints and guardrails

Most people don't know these things. They write vague prompts and get vague results.

**Meta-Prompt Solution**: The AI knows all of this. Let IT structure the prompt.

### Problem 2: The Iteration Trap

Traditional prompting:
```
Write prompt → Get mediocre result → Rewrite → Better result → Rewrite → Good result
```
This takes 5-10 iterations. Each iteration costs time and tokens.

**Meta-Prompt Solution**: Get it right the first time by having AI build a robust prompt.

### Problem 3: The Expertise Barrier

Different domains need different prompting approaches:
- Code generation needs different structure than copywriting
- Data analysis needs different structure than creative writing
- Technical explanations need different structure than sales copy

You'd need expertise in many domains to prompt effectively for all of them.

**Meta-Prompt Solution**: AI adapts the prompt structure to the domain automatically.

### Problem 4: The Reusability Problem

Every time you need something, you start from scratch.
No accumulation of knowledge. No compound improvement.

**Meta-Prompt Solution**: Meta-prompts generate REUSABLE prompts you can save and use forever.

---

## 3. THE FRAMEWORK

### The RTFC Structure

Every effective prompt has four components:

```
R - ROLE (Papel)
    Who should the AI be?
    What expertise should it have?
    What perspective should it take?

T - TASK (Tarefa)
    What exactly needs to be done?
    What is the desired outcome?
    What problem is being solved?

F - FORMAT (Formato)
    How should the output be structured?
    What sections/elements are needed?
    What length/depth is appropriate?

C - CONSTRAINTS (Regras)
    What should be avoided?
    What limitations exist?
    What quality standards apply?
```

### Why RTFC Works

When you give an AI all four components:
- **ROLE** activates relevant knowledge
- **TASK** focuses the generation
- **FORMAT** ensures usable output
- **CONSTRAINTS** prevents common errors

Missing any component leads to suboptimal results.

### The Meta-Prompt Principle

Instead of YOU filling in RTFC, you ask the AI:
1. "Here's what I want to accomplish"
2. "Ask me questions to understand better"
3. "Then build a RTFC prompt I can use"

The AI becomes your prompt engineer.

---

## 4. THE UNIVERSAL META-PROMPT

### The Core Prompt (Copy This)

```markdown
# PROMPT BUILDER | Construtor de Prompts

## YOUR ROLE

You are an expert prompt engineer. Your specialty is taking vague requests
and transforming them into highly effective, structured prompts that any
AI can execute with excellent results.

You understand:
- How different LLMs process instructions
- Best practices for prompt structure (RTFC: Role, Task, Format, Constraints)
- Domain-specific prompting techniques
- Edge cases and failure modes to prevent
- Output format optimization

## YOUR TASK

I will describe what I want to accomplish in 1-3 sentences.

Your job is to:
1. Ask me UP TO 5 clarifying questions to understand my need deeply
2. Based on my answers, create a complete, structured prompt
3. The prompt you create should be something I can copy-paste into any AI

## YOUR PROCESS

### Phase 1: Understanding (Ask Questions)

Ask me questions about:
- **Contexto**: What's the broader situation? Who is this for?
- **Especificidade**: What specific details matter for this task?
- **Formato desejado**: How do I want the output structured?
- **Restricoes**: What should definitely be avoided?
- **Exemplo**: Do I have an example of good output?

Ask ONLY the questions that are truly necessary. Maximum 5.
Ask them all at once, numbered.

### Phase 2: Building (Create Prompt)

After I answer, create a prompt with this EXACT structure:

```
# [DESCRIPTIVE TITLE]

## PAPEL (Role)
[Who the AI should be, what expertise it should have]

## CONTEXTO (Context)
[Background information the AI needs to know]

## TAREFA (Task)
[Clear description of what needs to be done]

## FORMATO DE SAIDA (Output Format)
[Exact structure of expected output]

## REGRAS (Constraints)
[What to do and what to avoid]

## EXEMPLO (Example) [if applicable]
[Example of good output]

---
EXECUTE NOW:
[Clear instruction to begin]
```

### Phase 3: Delivery

Present the prompt in a code block so I can easily copy it.
Explain briefly why you structured it this way.
Ask if I want any adjustments.

## OUTPUT LANGUAGE

The prompt you create should be in **Portuguese (Brazil)** unless I specify otherwise.
Your questions to me can be in Portuguese too.

## BEGIN

I will now tell you what I want to accomplish. Ask your clarifying questions.

---

**O QUE EU QUERO**: [DESCRIBE IN 1-3 SENTENCES]
```

---

### How to Use

1. Copy the entire prompt above
2. Paste into any LLM (ChatGPT, Claude, Gemini, etc.)
3. Replace `[DESCRIBE IN 1-3 SENTENCES]` with your need
4. Answer the AI's questions
5. Receive a structured prompt
6. **SAVE the generated prompt** for future reuse

---

## 5. DOMAIN VARIATIONS

### Variation A: Code Generation

Add to your request:
```
**O QUE EU QUERO**: [Your coding need]

**CONTEXTO ADICIONAL**:
- Linguagem: [Python/JavaScript/etc.]
- Framework: [if applicable]
- Nivel de experiencia: [Iniciante/Intermediario/Avancado]
- Ambiente: [Local/Producao/Testes]
```

### Variation B: Content Writing

Add to your request:
```
**O QUE EU QUERO**: [Your content need]

**CONTEXTO ADICIONAL**:
- Tom de voz: [Formal/Casual/Tecnico/Amigavel]
- Publico-alvo: [Who will read this]
- Plataforma: [Blog/LinkedIn/Instagram/Email]
- Comprimento desejado: [Curto/Medio/Longo]
```

### Variation C: Data Analysis

Add to your request:
```
**O QUE EU QUERO**: [Your analysis need]

**CONTEXTO ADICIONAL**:
- Tipo de dados: [Vendas/Usuarios/Financeiro/etc.]
- Formato dos dados: [CSV/Excel/JSON/etc.]
- Perguntas principais: [What questions to answer]
- Visualizacoes desejadas: [Tabelas/Graficos/Resumo]
```

### Variation D: Problem Solving

Add to your request:
```
**O QUE EU QUERO**: [Your problem]

**CONTEXTO ADICIONAL**:
- O que ja tentei: [Previous attempts]
- Recursos disponiveis: [What I have to work with]
- Restricoes: [Time/budget/technical limitations]
- Criterio de sucesso: [How I'll know it's solved]
```

### Variation E: Learning/Explanation

Add to your request:
```
**O QUE EU QUERO**: [What I want to learn/understand]

**CONTEXTO ADICIONAL**:
- Meu nivel atual: [Leigo/Basico/Intermediario/Avancado]
- Por que preciso saber: [Practical application]
- Estilo preferido: [Analogias/Tecnico/Exemplos praticos]
- Tempo disponivel: [Quick overview/Deep dive]
```

---

## 6. ADVANCED TECHNIQUES

### Technique 1: Chained Meta-Prompts

For complex projects, chain multiple meta-prompts:

```
Meta-Prompt 1: Build prompt for research
  → Output: Research prompt
  → Execute: Get research results

Meta-Prompt 2: Build prompt for analysis (using research)
  → Output: Analysis prompt
  → Execute: Get analysis

Meta-Prompt 3: Build prompt for recommendations
  → Output: Recommendations prompt
  → Execute: Get final output
```

Each generated prompt is saved and can be reused.

### Technique 2: Template Extraction

After receiving a good prompt, extract the template:

```
Ask the AI:
"Transforma esse prompt em um TEMPLATE com [VARIAVEIS] que eu possa
reusar para casos similares. Marca claramente o que precisa ser
preenchido a cada uso."
```

Now you have a reusable template, not just a one-time prompt.

### Technique 3: Quality Layers

Add quality requirements to your meta-prompt request:

```
**O QUE EU QUERO**: [Your need]

**NIVEL DE QUALIDADE DESEJADO**:
- [ ] Rapido e funcional (bom o suficiente)
- [ ] Profissional (alta qualidade)
- [ ] Expert (maximo rigor e profundidade)

O prompt gerado deve refletir esse nivel de qualidade.
```

### Technique 4: Self-Validation

Request built-in validation:

```
**REQUISITO ADICIONAL**:
O prompt gerado deve incluir uma secao de "VALIDACAO" que lista
criterios para verificar se o output esta bom. Assim posso checar
a qualidade antes de usar.
```

### Technique 5: Multi-Perspective

For important decisions:

```
**O QUE EU QUERO**: [Your need]

**REQUISITO ESPECIAL**:
O prompt deve pedir que a IA analise de MULTIPLAS PERSPECTIVAS:
- Perspectiva otimista
- Perspectiva pessimista
- Perspectiva pragmatica
E depois sintetize uma conclusao balanceada.
```

---

## 7. EXAMPLE OUTPUTS

### Example 1: Content Creation Request

**Input**:
```
O QUE EU QUERO: Criar posts para LinkedIn sobre produtividade
```

**AI Questions**:
```
Para criar o melhor prompt possivel, preciso entender:

1. CONTEXTO: Qual e sua area de atuacao? Voce quer se posicionar
   como especialista em que tema especifico de produtividade?

2. PUBLICO: Quem sao seus seguidores ideais? (Profissionais de
   qual area? Nivel de senioridade?)

3. FORMATO: Prefere posts curtos e diretos ou posts mais longos
   com storytelling?

4. RESTRICOES: Algo que voce quer evitar? (Tom muito vendedor,
   cliches, etc.)

5. EXEMPLO: Tem algum post de produtividade que voce achou bom
   e gostaria de usar como referencia de estilo?
```

**User Answers**:
```
1. Sou gerente de projetos, quero falar sobre gestao de tempo
2. Gestores e coordenadores de empresas medias
3. Posts medios com storytelling e dicas praticas
4. Evitar parecer coach, nada de frases motivacionais vazias
5. Gosto do estilo do Thiago Nigro - direto mas com historias reais
```

**Generated Prompt**:
```markdown
# GERADOR DE POSTS LINKEDIN | Gestao de Tempo para Gestores

## PAPEL
Voce e um ghostwriter especializado em conteudo de LinkedIn para
profissionais de gestao. Seu estilo combina storytelling com
praticidade - igual Thiago Nigro: direto, sem enrolacao, mas
usando historias reais para ilustrar pontos.

## CONTEXTO
Estou criando conteudo para um gerente de projetos que quer se
posicionar como referencia em gestao de tempo. O publico sao
gestores e coordenadores de empresas medias que enfrentam
sobrecarga de demandas e reunioes.

## TAREFA
Crie um post de LinkedIn sobre gestao de tempo seguindo a
estrutura:

1. HOOK (primeira linha que para o scroll - controversa ou curiosa)
2. HISTORIA (situacao real de 3-5 linhas que o leitor se identifica)
3. VIRADA (o que mudou ou o insight que veio)
4. DICA PRATICA (acao concreta que o leitor pode aplicar hoje)
5. CTA (pergunta que gera comentarios)

## FORMATO DE SAIDA
- Comprimento: 150-200 palavras
- Paragrafos curtos (1-2 linhas max)
- Usar espacamento para facilitar leitura mobile
- Uma linha em branco entre cada secao

## REGRAS
FAZER:
- Usar linguagem de gestor para gestor (peer-to-peer)
- Incluir numeros ou dados quando possivel
- Terminar com pergunta que gera discussao

NAO FAZER:
- Tom de coach ou motivacional vazio
- Frases como "acredite em voce" ou "o sucesso depende de voce"
- Excesso de emojis (maximo 2)
- Parecer que esta vendendo algo

## EXEMPLO DE ESTILO
"Rejeitei 3 reunioes hoje.

Meu chefe achou estranho. Minha equipe achou que eu tava doente.

Mas essas 3 horas me deram tempo de resolver um problema que
estava travado ha 2 semanas.

Reuniao virou a nova procrastinacao corporativa.

A pergunta nao e 'preciso estar nessa reuniao?'
E 'o que deixo de fazer se for?'

Quantas horas voce perdeu em reunioes essa semana?"

---
EXECUTE: Crie um post sobre [TEMA ESPECIFICO DE GESTAO DE TEMPO]
```

---

### Example 2: Technical Task Request

**Input**:
```
O QUE EU QUERO: Analisar dados de vendas do meu e-commerce
```

**AI Questions**:
```
1. DADOS: Que informacoes voce tem disponveis? (Periodo, produtos,
   canais, etc.)

2. OBJETIVO: O que especificamente voce quer descobrir com essa
   analise? (Tendencias? Problemas? Oportunidades?)

3. FORMATO: Como voce quer receber os insights? (Relatorio?
   Dashboard? Lista de acoes?)

4. CONTEXTO: Algo especifico acontecendo no negocio que devo
   considerar? (Lancamento? Sazonalidade? Problema?)
```

**Generated Prompt**:
```markdown
# ANALISTA DE DADOS E-COMMERCE | Diagnostico de Vendas

## PAPEL
Voce e um analista de dados senior especializado em e-commerce.
Sua abordagem e pragmatica: menos teoria, mais insights acionaveis.
Voce sabe que donos de e-commerce querem saber O QUE FAZER, nao
apenas ver numeros bonitos.

## CONTEXTO
Vou compartilhar dados de vendas dos ultimos [PERIODO]. O negocio
e [TIPO DE E-COMMERCE]. Estou querendo entender [OBJETIVO ESPECIFICO].

## TAREFA
Analise os dados e entregue:

1. DIAGNOSTICO RAPIDO (3-5 bullet points com achados principais)
2. PROBLEMAS IDENTIFICADOS (o que esta errado ou subotimo)
3. OPORTUNIDADES (o que poderia ser melhor explorado)
4. ACOES RECOMENDADAS (o que fazer nos proximos 7/30/90 dias)

## FORMATO DE SAIDA
```
## DIAGNOSTICO RAPIDO
- [Achado 1]
- [Achado 2]
...

## PROBLEMAS
| Problema | Impacto | Urgencia |
|----------|---------|----------|
| ...      | Alto/Medio/Baixo | Alta/Media/Baixa |

## OPORTUNIDADES
| Oportunidade | Potencial | Esforco |
|--------------|-----------|---------|
| ...          | R$ X      | Alto/Medio/Baixo |

## PLANO DE ACAO
### Proximos 7 dias
1. [Acao]
### Proximos 30 dias
1. [Acao]
### Proximos 90 dias
1. [Acao]
```

## REGRAS
- Seja direto e pratico
- Priorize insights acionaveis sobre analises teoricas
- Sempre quantifique impacto quando possivel
- Foque no que pode ser mudado (nao adianta analisar o que nao
  tenho controle)

---
DADOS PARA ANALISE:
[COLE SEUS DADOS AQUI]
```

---

## 8. BUILDING YOUR PROMPT LIBRARY

### The Compound Effect

Every prompt generated by meta-prompt is a **REUSABLE ASSET**.

After 30 days of using meta-prompts, you'll have:
- 5-10 prompts for your most common tasks
- Templates for each domain you work in
- A personal "prompt library" that keeps improving

### Organization System

Create a folder structure:

```
minha_biblioteca_prompts/
├── trabalho/
│   ├── analise_dados.md
│   ├── relatorios.md
│   └── emails_profissionais.md
├── conteudo/
│   ├── linkedin_posts.md
│   ├── blog_articles.md
│   └── social_media.md
├── pessoal/
│   ├── planejamento.md
│   └── aprendizado.md
└── templates/
    ├── template_analise.md
    └── template_conteudo.md
```

### Version Control

When you improve a prompt, save as new version:

```
linkedin_posts_v1.md  (original)
linkedin_posts_v2.md  (after feedback)
linkedin_posts_v3.md  (current best)
```

Keep old versions - you might want to go back.

### Sharing Prompts

Good prompts can be shared with:
- Team members (alignment)
- Freelancers (consistency)
- Community (karma)

A prompt library is **intellectual property** with real value.

---

## 9. COMMON MISTAKES

### Mistake 1: Too Vague Initial Request

**Bad**: "Quero criar conteudo"
**Good**: "Quero criar posts de LinkedIn sobre gestao de tempo para gestores"

Give the meta-prompt enough to work with.

### Mistake 2: Not Answering AI Questions

The AI's questions are designed to make the prompt better.
Skipping them or giving vague answers = worse prompt.

**Take time to answer thoughtfully.**

### Mistake 3: Not Saving Generated Prompts

You spent 5 minutes creating a great prompt.
Then you close the chat and lose it forever.

**Always save prompts you might reuse.**

### Mistake 4: Not Iterating

First generated prompt not perfect? Ask for adjustments:

```
"Esse prompt ficou bom, mas quero que [ADJUSTMENT].
Por favor, atualize."
```

### Mistake 5: Using Once and Forgetting

A good prompt should be used MANY times.
Build a library. Create templates. Compound your investment.

---

## 10. INTEGRATION WITH PLAN & IMPLEMENT

### The Complete Workflow

Meta-Prompt is the FIRST step of three:

```
STEP 1: META-PROMPT (This document)
  → Delegation: AI builds the prompt
  → Output: Structured, reusable prompt

STEP 2: PLAN (FREEMIUM_02_PLAN.md)
  → Supervision: AI shows plan before executing
  → Output: Step-by-step plan for approval

STEP 3: IMPLEMENT (FREEMIUM_03_IMPLEMENT.md)
  → Asset Creation: AI delivers in reusable format
  → Output: Portable knowledge file
```

### Why This Order

1. **META-PROMPT first**: Creates the right instructions
2. **PLAN second**: Ensures AI will do the right thing
3. **IMPLEMENT third**: Ensures output is reusable

### Chaining in Practice

```
Session 1: Meta-Prompt
  You: "Quero criar analises de vendas mensais"
  AI: [Asks questions]
  You: [Answers]
  AI: [Generates prompt]
  You: [Saves prompt as analise_vendas.md]

Session 2: Plan
  You: [Pastes analise_vendas.md] + "Cria plano para analisar dados de janeiro"
  AI: [Shows 5-step plan]
  You: "Aprovado, mas adiciona analise de sazonalidade"
  AI: [Updates plan]

Session 3: Implement
  You: "Executa o plano e entrega em formato que eu possa reusar"
  AI: [Executes and delivers reusable document]
  You: [Saves as relatorio_janeiro_2025.md]
```

**Result**: You have both a reusable PROMPT and a reusable OUTPUT.

---

## SUMMARY

### The Meta-Prompt Mindset

1. **You are not a prompt writer. You are a prompt director.**
2. **AI knows how to structure prompts. Let it.**
3. **Every generated prompt is an asset. Save it.**
4. **Templates compound. Libraries grow. Knowledge accumulates.**
5. **This is the new investment: building portable, reusable AI knowledge.**

### Quick Reference

```
WHEN TO USE META-PROMPT:
- Any new type of task
- When you're not sure how to prompt
- When you want reusable output
- When quality matters

HOW TO USE:
1. Copy the Universal Meta-Prompt
2. Describe your need in 1-3 sentences
3. Answer AI's questions thoughtfully
4. Review and adjust generated prompt
5. SAVE for future use

THE FORMULA:
  Vague need + Meta-Prompt = Structured, reusable prompt
```

---

## METADATA

| Field | Value |
|-------|-------|
| ID | FREEMIUM_01_META_PROMPT |
| Version | 1.0.0 |
| Created | 2025-11-29 |
| Author | CODEXA System |
| Type | Freemium Educational Content |
| Domain | Universal (any task, any industry) |
| Core Concept | Delegation |
| Next | FREEMIUM_02_PLAN.md |

---

## LICENSE

This is **FREEMIUM CONTENT** from CODEXA.

Use freely. Share freely. Teach others.

This knowledge is universal - it works for anyone, any domain, any LLM.

---

**The new literacy is not writing prompts.**
**It's directing AI to write prompts for you.**

---

**Built with CODEXA Meta-Construction System**
