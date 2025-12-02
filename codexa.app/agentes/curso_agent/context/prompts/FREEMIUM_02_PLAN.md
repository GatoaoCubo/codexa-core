# FREEMIUM 02: PLAN | O Planejador Universal

**ID**: FREEMIUM_02_PLAN | **Version**: 1.0.0 | **Created**: 2025-11-29
**Purpose**: Teach LLMs to plan before executing (supervision)
**Language**: Instructions in English | Output in Brazilian Portuguese (PT-BR)
**Compatibility**: ChatGPT, Claude, Gemini, Llama, Mistral (any LLM)
**Domain**: Universal (works for ANY task, ANY industry)
**Core Concept**: SUPERVISION - Stop executing blind, start validating plans

---

## TABLE OF CONTENTS

1. [The Supervision Paradigm](#1-the-supervision-paradigm)
2. [Why Plans Matter](#2-why-plans-matter)
3. [The Planning Framework](#3-the-planning-framework)
4. [The Universal Plan Prompt](#4-the-universal-plan-prompt)
5. [Plan Quality Criteria](#5-plan-quality-criteria)
6. [Adjusting Plans](#6-adjusting-plans)
7. [Example Plans](#7-example-plans)
8. [Advanced Planning](#8-advanced-planning)
9. [Common Mistakes](#9-common-mistakes)
10. [Integration](#10-integration)

---

## 1. THE SUPERVISION PARADIGM

### The Old Way (Execute and Hope)

```
You give instruction
  → AI executes immediately
  → Output might be wrong
  → You fix it
  → AI executes again
  → Still not right
  → Multiple iterations
  → Time wasted

Result: Trial and error, expensive iterations
```

### The New Way (Plan Then Execute)

```
You give instruction
  → AI creates plan FIRST
  → You review the plan
  → You approve or adjust
  → AI executes the approved plan
  → Output is right first time

Result: Right first time, you're in control
```

### The Core Insight

**AI doesn't know what you want until you validate.**

When AI executes immediately, it's GUESSING what you want.
When AI shows a plan first, you can VALIDATE before execution.

This is the difference between:
- **Operator** (you do the work, AI assists)
- **Supervisor** (AI does the work, you approve)

Plan-first transforms you into a SUPERVISOR.

---

## 2. WHY PLANS MATTER

### Problem 1: Misaligned Execution

Without a plan:
```
You: "Write a blog post about productivity"
AI: *writes 2000 words about time management*
You: "No, I wanted it about focus techniques, not time management"
AI: *rewrites everything*
```

With a plan:
```
You: "Write a blog post about productivity"
AI: "Here's my plan:
     1. Focus on time blocking technique
     2. Include 3 case studies
     3. Format: Hook + 5 sections + CTA
     Do you approve?"
You: "Change to focus techniques instead of time blocking"
AI: "Updated. Proceeding with focus techniques."
```

**Saved**: 5 minutes of rewriting + frustration

### Problem 2: Hidden Assumptions

AI makes assumptions you don't see until the output is wrong.

Without a plan: Assumptions hidden in execution
With a plan: Assumptions visible for review

**Plan reveals assumptions before they cause problems.**

### Problem 3: Scope Creep

AI might do MORE or LESS than you wanted.

Without a plan: You discover scope issues after execution
With a plan: You set clear boundaries before execution

### Problem 4: Quality Uncertainty

You can't evaluate AI's approach until you see results.

With a plan, you evaluate the APPROACH, not just the RESULT.

**Better approaches = Better results**

---

## 3. THE PLANNING FRAMEWORK

### The STEPS Structure

Every good plan has five elements:

```
S - SCOPE (Escopo)
    What will be done? What won't?
    Clear boundaries of the task

T - TASKS (Tarefas)
    What are the individual steps?
    Numbered, sequential actions

E - EXPECTATIONS (Expectativas)
    What will the output look like?
    Format, length, style

P - PITFALLS (Armadilhas)
    What could go wrong?
    How will it be avoided?

S - SUCCESS (Sucesso)
    How will we know it worked?
    What does "done" look like?
```

### Why STEPS Works

- **SCOPE** prevents scope creep and misalignment
- **TASKS** shows the approach for validation
- **EXPECTATIONS** aligns output format
- **PITFALLS** addresses risks proactively
- **SUCCESS** defines clear completion criteria

### The Plan-Execute-Review Loop

```
PLAN
  │
  v
REVIEW ← ─ ─ (adjust if needed)
  │
  v
APPROVE
  │
  v
EXECUTE
  │
  v
VALIDATE (does output match plan?)
```

---

## 4. THE UNIVERSAL PLAN PROMPT

### Core Planning Instruction (Add to Any Request)

```markdown
Antes de executar, crie um PLANO detalhado.

O plano deve incluir:

## ESCOPO
- O que SERA feito
- O que NAO sera feito
- Premissas que estou assumindo

## ETAPAS
1. [Primeira etapa]
2. [Segunda etapa]
3. [Terceira etapa]
...

## EXPECTATIVA DE OUTPUT
- Formato: [como sera entregue]
- Tamanho: [extensao aproximada]
- Estilo: [tom, abordagem]

## RISCOS E MITIGACOES
- Risco 1: [risco] → Mitigacao: [como evitar]
- Risco 2: [risco] → Mitigacao: [como evitar]

## CRITERIO DE SUCESSO
- [Como saberemos que esta pronto e bom]

---

ME MOSTRE O PLANO ANTES DE EXECUTAR.
Aguarde minha aprovacao para prosseguir.
```

---

### Complete Plan Request Template

```markdown
# SOLICITACAO COM PLANO

## MINHA TAREFA
[Descreva o que voce quer que seja feito]

## CONTEXTO RELEVANTE
[Informacoes de fundo que a IA precisa saber]

## REQUISITOS ESPECIFICOS
- [Requisito 1]
- [Requisito 2]
- [Requisito 3]

## O QUE NAO QUERO
- [Anti-requisito 1]
- [Anti-requisito 2]

---

## INSTRUCOES DE PLANEJAMENTO

Antes de executar esta tarefa, preciso que voce:

1. Crie um PLANO DETALHADO seguindo esta estrutura:

### ESCOPO
- Limites claros do que sera/nao sera feito
- Premissas que voce esta assumindo
- Dependencias ou pre-requisitos

### ETAPAS DE EXECUCAO
Numere cada etapa na ordem que sera realizada.
Para cada etapa, indique:
- O que sera feito
- Quanto tempo/esforco relativo
- Output dessa etapa

### FORMATO DO OUTPUT
- Estrutura exata do deliverable
- Secoes que tera
- Tamanho aproximado

### PONTOS DE ATENCAO
- O que pode dar errado
- Como voce vai evitar/mitigar
- Onde precisa de mais clareza minha

### DEFINICAO DE PRONTO
- Criterios que indicam conclusao
- Como validar qualidade

2. ME APRESENTE O PLANO e aguarde aprovacao.

3. So execute APOS minha aprovacao ou ajustes.

---

**AGUARDO O PLANO.**
```

---

### Quick Version (For Simple Tasks)

```
[Sua solicitacao]

---
Antes de fazer, me mostra o plano:
- O que vai fazer (escopo)
- Como vai fazer (etapas)
- O que vou receber (formato)

Aguarda minha OK pra executar.
```

---

## 5. PLAN QUALITY CRITERIA

### How to Evaluate a Plan

When AI shows you a plan, check:

**Clarity** (5 = Crystal clear, 1 = Confusing)
- [ ] Entendo exatamente o que sera feito?
- [ ] As etapas estao claras?
- [ ] O output esperado esta definido?

**Completeness** (5 = Nothing missing, 1 = Major gaps)
- [ ] Todas as partes da tarefa estao cobertas?
- [ ] Tem algum requisito meu nao enderecado?
- [ ] Os riscos estao identificados?

**Alignment** (5 = Exactly what I want, 1 = Wrong direction)
- [ ] O escopo esta correto?
- [ ] A abordagem faz sentido?
- [ ] O formato de output e o que preciso?

**Feasibility** (5 = Will work, 1 = Won't work)
- [ ] O plano e realista?
- [ ] As etapas fazem sentido na ordem proposta?
- [ ] Tem algo que vai dar errado?

### Scoring

```
20-25: Excelente - Aprovar e executar
15-19: Bom - Pequenos ajustes e executar
10-14: Regular - Ajustes significativos necessarios
5-9:   Fraco - Replanejar do zero
```

### Quick Validation Questions

Pergunte a si mesmo:
1. "Se seguir esse plano, vou ter o que preciso?"
2. "Tem algo que vai dar errado?"
3. "Falta alguma coisa importante?"

Se todas as respostas forem positivas, aprove.

---

## 6. ADJUSTING PLANS

### How to Request Changes

**Template para ajustes**:
```
O plano esta bom, mas preciso de ajustes:

1. MANTER: [o que esta correto]
2. MUDAR: [o que precisa ser diferente]
3. ADICIONAR: [o que esta faltando]
4. REMOVER: [o que nao deveria estar]

Por favor, atualize o plano e me mostre novamente.
```

### Common Adjustments

**Scope too broad**:
```
O escopo esta muito amplo. Reduz para focar apenas em [X].
Remove [Y] e [Z] do plano.
```

**Scope too narrow**:
```
Falta cobrir [X]. Adiciona uma etapa para isso.
O output tambem precisa incluir [Y].
```

**Wrong approach**:
```
A abordagem nao vai funcionar porque [razao].
Em vez de [abordagem atual], usa [abordagem alternativa].
```

**Missing detail**:
```
A etapa [N] esta vaga demais.
Detalha como exatamente voce vai fazer [aspecto especifico].
```

**Format mismatch**:
```
O formato proposto nao serve.
Preciso que o output seja [formato desejado] porque [razao].
```

### Iterating on Plans

It's OK to iterate on the plan. Better to iterate on plan than on execution.

```
Plan v1 → Review → Adjust → Plan v2 → Review → Approve → Execute
```

**Rule**: Max 3 iterations on plan. If more needed, restart with clearer request.

---

## 7. EXAMPLE PLANS

### Example 1: Content Creation

**Request**:
```
Escreve um artigo de blog sobre como aumentar produtividade trabalhando remoto.
Publico: Gestores de equipes remotas.
```

**Good Plan**:
```
## ESCOPO

**Sera feito:**
- Artigo de blog (1500-2000 palavras)
- Foco: Produtividade para GESTORES de equipes remotas
- Angulo: Como ajudar a EQUIPE a ser produtiva (nao produtividade pessoal)

**Nao sera feito:**
- Ferramentas especificas (para nao ficar datado)
- Produtividade pessoal generica
- Aspectos legais de trabalho remoto

**Premissas:**
- Leitor ja gerencia equipe remota (nao iniciante)
- Busca taticas praticas, nao teoria
- Prefere conteudo direto ao ponto

## ETAPAS

1. **Hook** (150 palavras)
   - Estatistica sobre produtividade remota
   - Pergunta provocativa

2. **Contexto** (200 palavras)
   - Por que gestao remota e diferente
   - O erro comum de gestores

3. **5 Estrategias** (1000 palavras, 200 cada)
   - Comunicacao assincrona estruturada
   - Definicao de expectativas claras
   - Check-ins efetivos (nao microgestao)
   - Automacao de acompanhamento
   - Cultura de documentacao

4. **Implementacao** (200 palavras)
   - Como comecar amanha
   - Uma acao por estrategia

5. **CTA** (100 palavras)
   - Resumo
   - Proximo passo sugerido

## FORMATO DO OUTPUT

```markdown
# [Titulo atraente]

[Hook com estatistica]

## Por Que Gestao Remota e Diferente
[...]

## 5 Estrategias Que Funcionam

### 1. [Estrategia]
[Explicacao + Exemplo pratico]

[... repete para 5 estrategias ...]

## Como Comecar Amanha
[Lista de acoes imediatas]

## Conclusao
[Resumo + CTA]
```

## RISCOS E MITIGACOES

- **Risco**: Ficar muito generico
  → Mitigacao: Incluir exemplo pratico em cada estrategia

- **Risco**: Tom muito tecnico
  → Mitigacao: Usar linguagem de gestor para gestor

- **Risco**: Muito longo e cansativo
  → Mitigacao: Bullets, subtitulos, paragrafos curtos

## CRITERIO DE SUCESSO

- [ ] Artigo entre 1500-2000 palavras
- [ ] 5 estrategias claras e acionaveis
- [ ] Cada estrategia tem exemplo pratico
- [ ] Leitor sabe exatamente o que fazer amanha
- [ ] Tom profissional mas acessivel
```

---

### Example 2: Data Analysis

**Request**:
```
Analisa os dados de vendas que vou te passar e me diz o que fazer para melhorar.
```

**Good Plan**:
```
## ESCOPO

**Sera feito:**
- Analise dos dados de vendas fornecidos
- Identificacao de padroes e anomalias
- Recomendacoes acionaveis para melhoria

**Nao sera feito:**
- Projecoes estatisticas complexas (sem ferramentas adequadas)
- Comparacao com benchmarks de mercado (sem dados externos)
- Implementacao das recomendacoes

**Premissas:**
- Dados sao representativos do negocio
- Objetivo e aumentar receita/lucro
- Tenho autonomia para implementar mudancas

## ETAPAS

1. **Limpeza e Entendimento** (10%)
   - Verificar completude dos dados
   - Identificar colunas e metricas disponiveis
   - Notar limitacoes dos dados

2. **Analise Descritiva** (25%)
   - Metricas basicas (total, media, mediana)
   - Distribuicao por periodo/produto/canal
   - Identificacao de outliers

3. **Analise de Padroes** (25%)
   - Tendencias temporais
   - Sazonalidade
   - Correlacoes entre variaveis

4. **Diagnostico** (20%)
   - O que esta funcionando bem
   - O que esta com problema
   - Hipoteses para os problemas

5. **Recomendacoes** (20%)
   - Acoes de curto prazo (0-30 dias)
   - Acoes de medio prazo (30-90 dias)
   - Prioridades baseadas em impacto/esforco

## FORMATO DO OUTPUT

```markdown
## RESUMO EXECUTIVO
[3-5 bullet points com principais achados]

## VISAO GERAL DOS DADOS
[Metricas basicas e contexto]

## ACHADOS PRINCIPAIS

### O Que Esta Funcionando
[Lista com dados]

### Problemas Identificados
[Lista com dados e evidencias]

## RECOMENDACOES

### Acao Imediata (Proximos 7 dias)
| Acao | Impacto Esperado | Esforco |
|------|-----------------|---------|
| ...  | ...             | ...     |

### Curto Prazo (30 dias)
[Tabela similar]

### Medio Prazo (90 dias)
[Tabela similar]

## LIMITACOES DA ANALISE
[O que NAO podemos concluir com esses dados]

## PROXIMOS PASSOS
[O que fazer com essa analise]
```

## RISCOS E MITIGACOES

- **Risco**: Dados incompletos levam a conclusoes erradas
  → Mitigacao: Documentar limitacoes claramente

- **Risco**: Recomendacoes muito vagas
  → Mitigacao: Cada recomendacao tera impacto esperado quantificado

- **Risco**: Muitas recomendacoes sobrecarregam
  → Mitigacao: Maximo 3 por horizonte temporal

## CRITERIO DE SUCESSO

- [ ] Analise cobre todas as dimensoes dos dados
- [ ] Achados sao baseados em evidencias (numeros)
- [ ] Recomendacoes sao especificas e acionaveis
- [ ] Limitacoes estao claras
- [ ] Leitor sabe exatamente o que fazer primeiro
```

---

## 8. ADVANCED PLANNING

### Technique 1: Milestone Plans

For large projects, break into milestones:

```
PLANO DE MILESTONES

Milestone 1: [Fase inicial]
- Entregas: [...]
- Checkpoint: [Como saber que esta pronto]

Milestone 2: [Fase intermediaria]
- Entregas: [...]
- Checkpoint: [...]
- Depende de: Milestone 1

[... continua ...]

Milestone Final: [Conclusao]
- Entregas: [...]
- Criterio de sucesso final: [...]
```

### Technique 2: Decision Points

Include decision points in the plan:

```
ETAPA 3: [Analise]

PONTO DE DECISAO:
Se encontrar [condicao A] → Sigo para Etapa 4A
Se encontrar [condicao B] → Sigo para Etapa 4B

Vou te informar qual condicao encontrei antes de prosseguir.
```

### Technique 3: Risk-Adjusted Plans

For high-stakes tasks:

```
PLANO PRIMARIO
[Abordagem principal]

PLANO CONTINGENCIA (se X acontecer)
[Abordagem alternativa]

CRITERIO DE ATIVACAO DO PLANO B
[Quando mudar de abordagem]
```

### Technique 4: Iterative Plans

For exploratory tasks:

```
ITERACAO 1: Exploracao
- Objetivo: Entender o problema
- Entrega: Hipoteses iniciais
- Checkpoint: Apresentar achados para direcao

ITERACAO 2: Aprofundamento
- Objetivo: Validar hipoteses selecionadas
- Entrega: Evidencias e analise
- Checkpoint: Confirmar direcao

ITERACAO 3: Solucao
- Objetivo: Desenvolver recomendacoes
- Entrega: Plano de acao final
```

---

## 9. COMMON MISTAKES

### Mistake 1: Approving Without Reading

Don't just say "OK" without actually reviewing the plan.
**Read each section. Ask yourself if it makes sense.**

### Mistake 2: Vague Feedback

**Bad**: "Isso nao ta bom, refaz"
**Good**: "A etapa 3 nao cobre [aspecto X]. Adiciona uma sub-etapa para isso."

**Be specific about what to change.**

### Mistake 3: Over-Planning Simple Tasks

For simple tasks, simple plans:
```
Simples: 3-5 linhas de plano
Medio: 10-15 linhas
Complexo: Plano estruturado completo
```

Don't request a 500-word plan for "escreve um email de agradecimento".

### Mistake 4: Not Saving Good Plans

Good plans are REUSABLE.
If AI created a great plan for a task type, save it as template.

### Mistake 5: Skipping Directly to Execution

Even if you're in a hurry, a quick plan check saves time overall.
**5 seconds reviewing a plan < 5 minutes fixing wrong output**

---

## 10. INTEGRATION

### With Meta-Prompt (FREEMIUM_01)

```
Session 1: Meta-Prompt
  → Output: Structured prompt for your task

Session 2: Plan
  → Input: The structured prompt + specific instance
  → Output: Execution plan for approval
```

### With Implement (FREEMIUM_03)

```
After Plan is approved:

"Plano aprovado. Agora executa e entrega em formato que eu possa
salvar e reusar. Formato: [markdown/json/etc.]"
```

### Complete Workflow

```
META-PROMPT → PLAN → IMPLEMENT

1. AI builds the right prompt (delegation)
2. AI shows the plan (supervision)
3. AI delivers reusable output (asset creation)
```

---

## SUMMARY

### The Plan Mindset

1. **Never execute blind.** Always request a plan first.
2. **You are the supervisor.** AI proposes, you approve.
3. **Plans reveal assumptions.** Catch mistakes early.
4. **Iterate on plans, not outputs.** Cheaper and faster.
5. **Save good plans.** They're reusable templates.

### Quick Reference

```
WHEN TO USE PLAN:
- Any task with multiple steps
- When output format matters
- When you're not 100% sure what you want
- When mistakes would be costly

HOW TO USE:
1. Add "Me mostra o plano antes de executar"
2. Review the plan critically
3. Request adjustments if needed
4. Approve only when satisfied
5. Then execute

THE FORMULA:
  Request + "Mostra o plano primeiro" = Control + Quality
```

---

## METADATA

| Field | Value |
|-------|-------|
| ID | FREEMIUM_02_PLAN |
| Version | 1.0.0 |
| Created | 2025-11-29 |
| Author | CODEXA System |
| Type | Freemium Educational Content |
| Domain | Universal (any task, any industry) |
| Core Concept | Supervision |
| Previous | FREEMIUM_01_META_PROMPT.md |
| Next | FREEMIUM_03_IMPLEMENT.md |

---

## LICENSE

This is **FREEMIUM CONTENT** from CODEXA.

Use freely. Share freely. Teach others.

---

**Don't be an operator executing tasks.**
**Be a supervisor validating plans.**

---

**Built with CODEXA Meta-Construction System**
