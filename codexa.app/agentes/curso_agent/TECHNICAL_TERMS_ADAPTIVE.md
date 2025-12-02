# 🔤 TECHNICAL TERMS - ADAPTIVE EXPLANATION SYSTEM
**Sistema de Jargões com Neuroplasticidade LLM**

**Versão:** 1.0.0
**Data:** 2025-11-24
**Filosofia:** Precisão técnica + Adaptação entrópica

---

## 🧠 CONCEITO CENTRAL

Jargões técnicos são necessários (precisão). Mas explicações rígidas são chatas (morte pedagógica).

**Solução:** Template com `[VARIABLES]` abertas para LLM preencher baseado em contexto do usuário.

### Princípios

1. **Termo oficial preservado** (educacional)
2. **Template de explicação** com `[OPEN_VARIABLES]`
3. **LLM adapta entropicamente** ao {user} {empresa} {contexto}
4. **Personalização automática** sem perder precisão

### Exemplo Rápido

**Jargão:** Context Pollution

**Template:**
```
[AGENT_NAME] sofre context pollution quando [TOO_MANY_RESPONSIBILITIES].

Como se [USER_FAMILIAR_METAPHOR].

Resultado: [NEGATIVE_OUTCOME].

Solução: [PRINCIPLE].
```

**LLM preenche para seller:**
> Anuncio Agent sofre context pollution quando precisa fazer copywriting + pesquisa + fotos + compliance.
>
> Como se você tentasse vender, repor estoque e fazer contabilidade simultaneamente.
>
> Resultado: Anúncios genéricos sem personalidade.
>
> Solução: OPOP - One Agent, One Purpose.

**LLM preenche para dev:**
> Your AI suffers context pollution when handling auth + payments + notifications + analytics.
>
> Like a microservice violating Single Responsibility Principle.
>
> Result: Tight coupling, bugs everywhere.
>
> Solution: OPOP - Specialized agents for specialized tasks.

---

## 📚 GLOSSÁRIO COMPLETO - TEMPLATES

### 1. Context Pollution

**Categoria:** Architecture Pattern
**Nível:** Intermediário

**Template de Explicação:**
```markdown
## Context Pollution

**O que é:**
[AGENT_OR_SYSTEM] sofre **context pollution** quando [RECEIVES_TOO_MANY_RESPONSIBILITIES].

**Metáfora para você:**
[USER_FAMILIAR_SCENARIO_FROM_THEIR_BUSINESS].

**Por que é ruim:**
- [PERFORMANCE_DEGRADATION]
- [QUALITY_DEGRADATION]
- [MAINTENANCE_NIGHTMARE]

**Como evitar:**
Princípio **OPOP** (One Purpose One Agent):
- [SINGLE_RESPONSIBILITY_EXAMPLE_1]
- [SINGLE_RESPONSIBILITY_EXAMPLE_2]

**No seu caso:**
[SPECIFIC_APPLICATION_TO_USER_CONTEXT]
```

**Campos `[VARIABLE]` que LLM preenche:**
- `[AGENT_OR_SYSTEM]` - Nome relevante ao contexto
- `[RECEIVES_TOO_MANY_RESPONSIBILITIES]` - Exemplo concreto
- `[USER_FAMILIAR_SCENARIO]` - Analogia da indústria do usuário
- `[PERFORMANCE_DEGRADATION]` - Impacto em performance
- `[QUALITY_DEGRADATION]` - Impacto em qualidade
- `[MAINTENANCE_NIGHTMARE]` - Impacto em manutenibilidade
- `[SINGLE_RESPONSIBILITY_EXAMPLE_1/2]` - Exemplos práticos
- `[SPECIFIC_APPLICATION]` - Aplicação ao caso do usuário

---

### 2. $arguments-chaining

**Categoria:** Data Flow Pattern
**Nível:** Intermediário

**Template:**
```markdown
## $arguments-chaining

**O que é:**
Output de [PHASE_N] vira input de [PHASE_N+1] automaticamente.

**Como funciona:**
1. [STEP_1_DESCRIPTION]
2. [STEP_2_DESCRIPTION]
3. [STEP_3_DESCRIPTION]

**Analogia:**
Como [PHYSICAL_PROCESS_USER_KNOWS]:
- [STAGE_1] → passa para [STAGE_2]
- [STAGE_2] → passa para [STAGE_3]
- [RESULT_EMERGES]

**Por que importa:**
- [VALUE_PROPOSITION_1]
- [VALUE_PROPOSITION_2]
- [VALUE_PROPOSITION_3]

**Exemplo prático no seu negócio:**
[USER_SPECIFIC_WORKFLOW_EXAMPLE]
```

**Campos `[VARIABLE]`:**
- `[PHASE_N]` - Fase atual nomeada
- `[PHASE_N+1]` - Próxima fase nomeada
- `[STEP_X_DESCRIPTION]` - Descrição de cada passo
- `[PHYSICAL_PROCESS]` - Processo físico análogo
- `[STAGE_X]` - Estágios do processo análogo
- `[VALUE_PROPOSITION_X]` - Valores para usuário
- `[USER_SPECIFIC_WORKFLOW]` - Workflow real do usuário

---

### 3. Quality Gates

**Categoria:** Validation Pattern
**Nível:** Básico

**Template:**
```markdown
## Quality Gates

**O que são:**
Thresholds automáticos que [VALIDATION_ACTION] antes de [NEXT_STEP].

**Tipo checklist de qualidade em [USER_INDUSTRY_ANALOGY]:**
- [QUALITY_CHECK_1]
- [QUALITY_CHECK_2]
- [QUALITY_CHECK_3]

**Previnem:**
[FAILURE_MODE_WITHOUT_GATES]

**Garantem:**
[SUCCESS_OUTCOME_WITH_GATES]

**Exemplo concreto:**
[SPECIFIC_GATE_IN_USER_CONTEXT]
- Threshold: [SPECIFIC_THRESHOLD]
- Se passar: [WHAT_HAPPENS]
- Se falhar: [WHAT_HAPPENS]
```

**Campos `[VARIABLE]`:**
- `[VALIDATION_ACTION]` - O que valida
- `[NEXT_STEP]` - Próximo passo
- `[USER_INDUSTRY_ANALOGY]` - Analogia da indústria
- `[QUALITY_CHECK_X]` - Checks específicos
- `[FAILURE_MODE]` - O que acontece sem gates
- `[SUCCESS_OUTCOME]` - O que acontece com gates
- `[SPECIFIC_GATE/THRESHOLD]` - Exemplo concreto

---

### 4. Trinity Output

**Categoria:** Output Format Pattern
**Nível:** Intermediário

**Template:**
```markdown
## Trinity Output

**Conceito:**
Cada output tem 3 formatos:
1. **[FORMAT_1]** para [AUDIENCE_1]
2. **[FORMAT_2]** para [AUDIENCE_2]
3. **[FORMAT_3]** para [AUDIENCE_3]

**Por que 3?**
[MULTI_STAKEHOLDER_JUSTIFICATION]

**Exemplo no seu contexto:**

**[FORMAT_1_NAME]:**
- Quem usa: [HUMAN_STAKEHOLDER]
- Para que: [HUMAN_USE_CASE]
- Como lê: [READING_METHOD]

**[FORMAT_2_NAME]:**
- Quem usa: [MACHINE_STAKEHOLDER]
- Para que: [MACHINE_USE_CASE]
- Como processa: [PROCESSING_METHOD]

**[FORMAT_3_NAME]:**
- Quem usa: [SYSTEM_STAKEHOLDER]
- Para que: [SYSTEM_USE_CASE]
- Como rastreia: [TRACKING_METHOD]

**Vantagem para você:**
[USER_SPECIFIC_BENEFIT]
```

**Campos `[VARIABLE]`:**
- `[FORMAT_X]` - Nome do formato
- `[AUDIENCE_X]` - Quem consome
- `[MULTI_STAKEHOLDER_JUSTIFICATION]` - Por que múltiplos
- `[X_STAKEHOLDER]` - Tipo de stakeholder
- `[X_USE_CASE]` - Caso de uso específico
- `[X_METHOD]` - Método de uso
- `[USER_SPECIFIC_BENEFIT]` - Benefício concreto

---

### 5. [OPEN_VARIABLES]

**Categoria:** Meta-Construction Pattern
**Nível:** Avançado

**Template:**
```markdown
## [OPEN_VARIABLES]

**O que são:**
Campos intencionalmente deixados em branco onde [LLM_CREATIVE_PROCESS].

**Contraste:**

**Campos Fixos:**
```
[FIXED_EXAMPLE_IN_USER_DOMAIN]
```
→ [LIMITATION_OF_FIXED]

**Campos Abertos:**
```
[OPEN_EXAMPLE_IN_USER_DOMAIN]
```
→ [ADVANTAGE_OF_OPEN]

**Benefício:**
[ADAPTABILITY_VALUE_PROPOSITION]

**Quando usar:**
- [USE_CASE_1_FOR_USER]
- [USE_CASE_2_FOR_USER]
- [USE_CASE_3_FOR_USER]

**Exemplo prático:**
[REAL_TEMPLATE_FROM_USER_WORK]
```

**Campos `[VARIABLE]`:**
- `[LLM_CREATIVE_PROCESS]` - O que LLM faz
- `[FIXED_EXAMPLE]` - Exemplo rígido
- `[LIMITATION_OF_FIXED]` - Por que rígido é ruim
- `[OPEN_EXAMPLE]` - Exemplo com variables
- `[ADVANTAGE_OF_OPEN]` - Por que aberto é bom
- `[ADAPTABILITY_VALUE]` - Valor da adaptação
- `[USE_CASE_X]` - Casos de uso específicos
- `[REAL_TEMPLATE]` - Template real do trabalho do usuário

---

### 6. Neuroplasticidade LLM

**Categoria:** System Property
**Nível:** Avançado

**Template:**
```markdown
## Neuroplasticidade LLM

**Conceito:**
Sistema se adapta automaticamente a:
- [USER_BRAND_ASPECT]
- [USER_MARKET_ASPECT]
- [USER_PRODUCT_ASPECT]

**Analogia biológica:**
Como cérebro que [NEUROPLASTICITY_COMPARISON].

**Diferente de IA genérica:**

| IA Genérica | CODEXA (Neuroplástico) |
|-------------|------------------------|
| [GENERIC_LIMITATION_1] | [CODEXA_ADVANTAGE_1] |
| [GENERIC_LIMITATION_2] | [CODEXA_ADVANTAGE_2] |
| [GENERIC_LIMITATION_3] | [CODEXA_ADVANTAGE_3] |

**Resultado para você:**
[PERSONALIZATION_OUTCOME_IN_USER_BUSINESS]

**Exemplo concreto:**
[ADAPTATION_EXAMPLE_FROM_USER_CONTEXT]
```

**Campos `[VARIABLE]`:**
- `[USER_X_ASPECT]` - Aspectos do negócio do usuário
- `[NEUROPLASTICITY_COMPARISON]` - Comparação biológica
- `[GENERIC_LIMITATION_X]` - Limitações de IA genérica
- `[CODEXA_ADVANTAGE_X]` - Vantagens do CODEXA
- `[PERSONALIZATION_OUTCOME]` - Resultado da personalização
- `[ADAPTATION_EXAMPLE]` - Exemplo real de adaptação

---

### 7. HOPs (Higher-Order Prompts)

**Categoria:** Prompt Engineering Pattern
**Nível:** Avançado

**Template:**
```markdown
## HOPs (Higher-Order Prompts)

**O que são:**
Prompts que [ORCHESTRATION_FUNCTION].

**Framework TAC-7:**
1. **[TAC_COMPONENT_1]** - [EXPLANATION_FOR_USER_LEVEL]
2. **[TAC_COMPONENT_2]** - [EXPLANATION_FOR_USER_LEVEL]
3. **[TAC_COMPONENT_3]** - [EXPLANATION_FOR_USER_LEVEL]
[...7 componentes total]

**Prompt simples vs HOP:**

**Prompt Simples:**
```
[SIMPLE_PROMPT_EXAMPLE]
```
→ [WHY_SIMPLE_IS_LIMITED]

**HOP:**
```
[HOP_STRUCTURE_EXAMPLE]
```
→ [WHY_HOP_IS_BETTER]

**Quando usar no seu negócio:**
[USE_CASE_IN_USER_DOMAIN]

**ROI:**
[TIME_SAVED_OR_QUALITY_IMPROVED]
```

**Campos `[VARIABLE]`:**
- `[ORCHESTRATION_FUNCTION]` - O que HOP orquestra
- `[TAC_COMPONENT_X]` - Componente do TAC-7
- `[EXPLANATION_FOR_USER_LEVEL]` - Explicação nivelada
- `[SIMPLE_PROMPT_EXAMPLE]` - Exemplo de prompt básico
- `[WHY_SIMPLE_IS_LIMITED]` - Limitação do simples
- `[HOP_STRUCTURE_EXAMPLE]` - Estrutura de HOP
- `[WHY_HOP_IS_BETTER]` - Vantagem do HOP
- `[USE_CASE_IN_USER_DOMAIN]` - Caso de uso do usuário
- `[TIME_SAVED/QUALITY]` - ROI mensurável

---

### 8. ADWs (AI Developer Workflows)

**Categoria:** Workflow Pattern
**Nível:** Avançado

**Template:**
```markdown
## ADWs (AI Developer Workflows)

**O que são:**
Workflows multi-fase que [AUTOMATE_COMPLEX_TASK].

**Estrutura típica:**
[N_PHASES] fases:
1. [PHASE_1_NAME] - [WHAT_IT_DOES]
2. [PHASE_2_NAME] - [WHAT_IT_DOES]
[...todas as fases]

**Analogia industrial:**
Como [MANUFACTURING_OR_INDUSTRIAL_PROCESS]:
- [STAGE_1] → [STAGE_2] → [STAGE_3]
- Quality control em cada estágio
- Output final perfeito

**ROI no seu caso:**
- Antes: [MANUAL_TIME] horas
- Depois: [ADW_TIME] minutos
- Economia: [SAVINGS] por [FREQUENCY]

**Exemplo de ADW para você:**
[SPECIFIC_ADW_APPLICATION_TO_USER_TASK]
```

**Campos `[VARIABLE]`:**
- `[AUTOMATE_COMPLEX_TASK]` - Tarefa que automatiza
- `[N_PHASES]` - Número de fases
- `[PHASE_X_NAME/WHAT_IT_DOES]` - Descrição de fase
- `[MANUFACTURING_PROCESS]` - Processo análogo
- `[STAGE_X]` - Estágios do processo
- `[MANUAL_TIME]` - Tempo antes
- `[ADW_TIME]` - Tempo depois
- `[SAVINGS/FREQUENCY]` - Economia real
- `[SPECIFIC_ADW_APPLICATION]` - Aplicação concreta

---

### 9. Meta-Construção

**Categoria:** Architectural Concept
**Nível:** Avançado

**Template:**
```markdown
## Meta-Construção

**Definição:**
Construir [SYSTEM_THAT_BUILDS_SYSTEMS].

**Níveis:**

**[APPLICATION_LAYER_NAME]:**
- Você [APPLICATION_LEVEL_ACTION]
- Exemplo: [APPLICATION_EXAMPLE_FOR_USER]

**[AGENTIC_LAYER_NAME]:**
- Você [AGENTIC_LEVEL_ACTION]
- Exemplo: [AGENTIC_EXAMPLE_FOR_USER]

**Analogia arquitetural:**
[ARCHITECTURE_METAPHOR_USER_UNDERSTANDS]:
- [LAYER_1] vs [LAYER_2]
- [LAYER_2] constrói [LAYER_1]
- Leverage exponencial

**Impact no seu negócio:**
- 1 hora na agentic layer = [MULTIPLICATION_FACTOR]x resultado
- vs 1 hora na application layer = [LINEAR_RESULT]

**Como começar:**
[FIRST_STEP_FOR_USER_TO_START_META_CONSTRUCTION]
```

**Campos `[VARIABLE]`:**
- `[SYSTEM_THAT_BUILDS]` - Sistema recursivo
- `[X_LAYER_NAME]` - Nome das camadas
- `[X_LEVEL_ACTION]` - Ação em cada nível
- `[X_EXAMPLE_FOR_USER]` - Exemplo do contexto
- `[ARCHITECTURE_METAPHOR]` - Metáfora arquitetural
- `[LAYER_X]` - Camadas específicas
- `[MULTIPLICATION_FACTOR]` - Fator de leverage
- `[LINEAR_RESULT]` - Resultado linear
- `[FIRST_STEP]` - Primeiro passo prático

---

### 10. OPOP (One Prompt One Purpose)

**Categoria:** Design Principle
**Nível:** Básico

**Template:**
```markdown
## OPOP (One Prompt One Purpose)

**Princípio:**
Um agente faz [SINGLE_RESPONSIBILITY].
Não faz [OUT_OF_SCOPE_EXAMPLES].

**Por que especialização?**
[QUALITY_VS_GENERALIZATION_TRADEOFF_EXPLANATION]

**No seu negócio:**

**Especialista:**
- [AGENT_NAME] faz [SPECIFIC_TASK]
- Qualidade: [QUALITY_METRIC]
- Tempo: [TIME_METRIC]

**Generalista:**
- Tenta fazer [MULTIPLE_TASKS]
- Qualidade: [DEGRADED_QUALITY]
- Tempo: [INCREASED_TIME]

**Resultado:**
[SPECIALIST_VALUE_FOR_USER]

**Como aplicar:**
[PRACTICAL_STEPS_TO_APPLY_OPOP]
```

**Campos `[VARIABLE]`:**
- `[SINGLE_RESPONSIBILITY]` - Responsabilidade única
- `[OUT_OF_SCOPE]` - O que NÃO faz
- `[QUALITY_VS_GENERALIZATION]` - Trade-off explicado
- `[AGENT_NAME]` - Nome do agente especialista
- `[SPECIFIC_TASK]` - Tarefa específica
- `[QUALITY/TIME_METRIC]` - Métricas mensuráveis
- `[MULTIPLE_TASKS]` - Múltiplas responsabilidades
- `[DEGRADED_QUALITY/INCREASED_TIME]` - Degradação
- `[SPECIALIST_VALUE]` - Valor da especialização
- `[PRACTICAL_STEPS]` - Como aplicar na prática

---

### 11. Composable Agentic Primitives

**Categoria:** System Architecture
**Nível:** Avançado

**Template:**
```markdown
## Composable Agentic Primitives

**Conceito:**
Primitivas são como [LEGO_OR_BUILDING_BLOCKS_METAPHOR].

**As 12 Primitivas:**
[LIST_OF_12_LEVERAGE_POINTS_CONTEXTUALIZED]

**Composição:**
[PRIMITIVE_A] + [PRIMITIVE_B] = [NEW_WORKFLOW]

**Poder combinatorial:**
[NUMBER_OF_PRIMITIVES]² = [POSSIBLE_COMBINATIONS] possibilidades

**Exemplo da sua área:**
[USER_SPECIFIC_COMBINATION]:
1. [PRIMITIVE_USED_1]
2. [PRIMITIVE_USED_2]
3. [PRIMITIVE_USED_3]
→ Cria [EMERGENT_CAPABILITY]

**Como você usa isso:**
[PRACTICAL_APPLICATION_GUIDE]
```

**Campos `[VARIABLE]`:**
- `[LEGO_METAPHOR]` - Metáfora de blocos
- `[LIST_OF_12_LEVERAGE_POINTS]` - Lista contextualizada
- `[PRIMITIVE_A/B]` - Primitivas específicas
- `[NEW_WORKFLOW]` - Resultado da composição
- `[NUMBER_OF_PRIMITIVES]` - Quantas primitivas
- `[POSSIBLE_COMBINATIONS]` - Combinações possíveis
- `[USER_SPECIFIC_COMBINATION]` - Combo real do usuário
- `[PRIMITIVE_USED_X]` - Primitivas usadas
- `[EMERGENT_CAPABILITY]` - Capacidade emergente
- `[PRACTICAL_APPLICATION]` - Guia prático

---

### 12. Feedback Loops (Closing the Loop)

**Categoria:** Quality Pattern
**Nível:** Intermediário

**Template:**
```markdown
## Feedback Loops (Closing the Loop)

**Pattern:**
[REQUEST] → [EXECUTE] → [VALIDATE] → [FIX_IF_NEEDED] → [REPEAT]

**Sem loop:**
[MANUAL_PROCESS_USER_DOES]:
- Você [MANUAL_STEP_1]
- Você [MANUAL_STEP_2]
- Você [MANUAL_STEP_3]
→ [MANUAL_PROBLEMS]

**Com loop:**
[AUTOMATED_PROCESS]:
- Sistema [AUTO_STEP_1]
- Sistema [AUTO_STEP_2]
- Sistema [AUTO_STEP_3]
→ [AUTO_BENEFITS]

**Analogia de QA:**
Como [TESTING_METAPHOR_USER_KNOWS]:
- [TEST_STEP_1]
- [TEST_STEP_2]
- [RESULT_GUARANTEED]

**Threshold de qualidade:**
[QUALITY_THRESHOLD_EXPLANATION]

**No seu workflow:**
[USER_SPECIFIC_FEEDBACK_LOOP_EXAMPLE]
```

**Campos `[VARIABLE]`:**
- `[REQUEST/EXECUTE/VALIDATE/FIX]` - Passos do loop
- `[MANUAL_PROCESS]` - Processo manual atual
- `[MANUAL_STEP_X]` - Passos manuais
- `[MANUAL_PROBLEMS]` - Problemas do manual
- `[AUTOMATED_PROCESS]` - Processo automatizado
- `[AUTO_STEP_X]` - Passos automatizados
- `[AUTO_BENEFITS]` - Benefícios da automação
- `[TESTING_METAPHOR]` - Metáfora de QA
- `[TEST_STEP_X]` - Passos de teste
- `[RESULT_GUARANTEED]` - Garantia de qualidade
- `[QUALITY_THRESHOLD]` - Threshold explicado
- `[USER_SPECIFIC_LOOP]` - Loop real do usuário

---

## 🎯 IMPLEMENTAÇÃO NO CURSO

### Como Usar Este Sistema

**Quando jargão aparece pela primeira vez:**

```markdown
## [Seção do Módulo]

[Conteúdo normal...]

### **Context Pollution**

[AGENT_OR_SYSTEM] sofre **context pollution** quando [RECEIVES_TOO_MANY_RESPONSIBILITIES].

[LLM PREENCHE AUTOMATICAMENTE BASEADO EM CONVERSA COM USUÁRIO]

**Metáfora para você:**
[USER_FAMILIAR_SCENARIO]

[Resto do template...]
```

**Após primeira aparição, usar shorthand:**

```markdown
Para evitar **context pollution**, use princípio OPOP.
```

### Diretrizes para LLM

**Ao preencher `[VARIABLES]`:**

1. **Detectar contexto do usuário:**
   - Indústria/setor
   - Nível técnico
   - Produtos vendidos
   - Problemas atuais

2. **Escolher analogias relevantes:**
   - Se seller → analogias de vendas/estoque/marketplace
   - Se dev → analogias de código/arquitetura/deploy
   - Se gestor → analogias de processos/equipes/ROI

3. **Manter precisão técnica:**
   - Termo oficial sempre presente
   - Conceito core não distorcido
   - Apenas a explicação adapta

4. **Ser conciso:**
   - Metáfora em 1-2 frases
   - Exemplo em 3-5 linhas
   - Total ≤ 200 palavras por jargão

---

## 📊 EXEMPLOS DE ADAPTAÇÃO

### Exemplo 1: Context Pollution

**Para seller de cosméticos:**
> Anuncio Agent sofre **context pollution** quando você pede para ele escrever copy + validar ANVISA + escolher fotos + definir preço.
>
> Como você tentar formular produto + vender + fazer compliance + fotografar ao mesmo tempo.
>
> Resultado: Tudo medíocre. Anúncios genéricos.
>
> Solução: OPOP - Anuncio Agent só faz copywriting. Pesquisa Agent faz pricing. Photo Agent faz imagens.

**Para dev de SaaS:**
> Your service suffers **context pollution** when handling auth + billing + notifications + analytics.
>
> Like a microservice violating Single Responsibility Principle.
>
> Result: Tight coupling everywhere, maintenance hell.
>
> Solution: OPOP - One service per domain. Compose via events.

### Exemplo 2: $arguments-chaining

**Para seller:**
> **$arguments-chaining** = Pesquisa Agent cria research_notes.md → Anuncio Agent lê e usa para copywriting → Photo Agent usa para gerar imagens alinhadas.
>
> Como linha de produção: matéria-prima → processamento → produto final.
>
> Você não precisa copiar/colar manualmente entre agentes.

**Para dev:**
> **$arguments-chaining** = Phase N output becomes Phase N+1 input automatically.
>
> Like Unix pipes: `cat | grep | sort | uniq`
>
> Data flows through pipeline without manual intervention.

---

## 🎨 TOM & ESTILO

### Manter Tom Sério-Sofisticado

**NÃO fazer:**
- ❌ "Context pollution é tipo quando o agente fica confuso sabe?"
- ❌ "É super importante entender isso haha"
- ❌ "Vou explicar de um jeito bem zoeira..."

**FAZER:**
- ✅ "Context pollution degrada output quality systematically."
- ✅ "This principle has measurable impact on performance."
- ✅ "Elegante na simplicidade. Poderoso na execução."

### Ocasional Humor Inteligente

**Exemplo aceitável:**
> "Quality gates são seu CTO robótico. Zero exceções. Zero 'mas funciona na minha máquina'."

**Exemplo não aceitável:**
> "LOL imagine seu agente bugado KKKK tem que ter quality gate né mano"

---

## 🔧 MAINTENANCE & EVOLUTION

### Adding New Terms

**Template para novo jargão:**

```markdown
### [TERM_NUMBER]. [TECHNICAL_TERM]

**Categoria:** [CATEGORY]
**Nível:** [LEVEL]

**Template:**
```markdown
## [TECHNICAL_TERM]

[CORE_EXPLANATION_WITH_VARIABLES]

[METAPHOR_SECTION]

[CONTRAST_OR_COMPARISON]

[USER_APPLICATION]

[PRACTICAL_EXAMPLE]
```

**Campos `[VARIABLE]`:**
- `[VARIABLE_1]` - [Description]
- `[VARIABLE_2]` - [Description]
[...all variables listed]
```

### Versioning

Quando adicionar novo termo:
```
v1.0.0 → 12 terms
v1.1.0 → 15 terms (added 3)
v1.1.1 → 15 terms (improved explanations)
```

---

## 📈 METRICS & QUALITY

### Como Avaliar Qualidade das Explicações

**Critérios:**

1. **Precisão Técnica:** Termo oficial correto? ✅/❌
2. **Relevância:** Metáfora faz sentido pro usuário? ✅/❌
3. **Concisão:** ≤ 200 palavras? ✅/❌
4. **Clareza:** Usuário entende em 1 leitura? ✅/❌
5. **Utilidade:** Pode aplicar imediatamente? ✅/❌

**Score mínimo:** 4/5 ✅

---

**Versão:** 1.0.0
**Criado:** 2025-11-24
**Mantido por:** CODEXA Team

**Changelog:**
- v1.0.0 - Sistema completo de jargões adaptativos
- 12 termos técnicos com templates
- Sistema de `[VARIABLES]` para adaptação entrópica
- Exemplos multi-contexto

---

> 💡 **Axioma:**
> "Precisão sem adaptação é pedantismo.
> Adaptação sem precisão é confusão.
> Template com [VARIABLES] é sabedoria."
