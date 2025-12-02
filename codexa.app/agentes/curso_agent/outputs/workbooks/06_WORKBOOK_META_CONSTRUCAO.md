# Apostila - Modulo 06: Meta-Construcao

**Curso**: CODEXA - Cerebro IA para Sellers
**Modulo**: 06 - Meta-Construcao (Avancado)
**Duracao de estudo**: 3-4 horas
**XP Disponivel**: 200 XP (MODULO MASTER!)

---

## Indice

1. [Objetivos de Aprendizagem](#1-objetivos-de-aprendizagem)
2. [A Mudanca de Paradigma](#2-a-mudanca-de-paradigma)
3. [Os 12 Pontos de Alavancagem](#3-os-12-pontos-de-alavancagem)
4. [Os 4 Nucleos de Um Agente](#4-os-4-nucleos-de-um-agente)
5. [Template Your Engineering](#5-template-your-engineering)
6. [Criando Seu Primeiro Agente](#6-criando-seu-primeiro-agente)
7. [Exercicios Praticos](#7-exercicios-praticos)
8. [Templates Avancados](#8-templates-avancados)

---

## 1. Objetivos de Aprendizagem

| Objetivo | Verbo (Bloom) | Validacao |
|----------|---------------|-----------|
| Entender perspectiva agentiva | Compreender | Quiz conceitual |
| Aplicar 12 pontos de alavancagem | Aplicar | Ponto escolhido e justificado |
| Controlar 4 nucleos | Analisar | Agente planejado |
| Criar agente customizado | Criar | Agente funcional |

---

## 2. A Mudanca de Paradigma

### Principio Fundamental

```
+-----------------------------------------------+
|                                               |
|   O AGENTE JA SABE EXECUTAR.                  |
|   VOCE PRECISA APRENDER A ORQUESTRAR.         |
|                                               |
+-----------------------------------------------+
```

### Application Layer vs Agentic Layer

```
APPLICATION LAYER (Onde voce TRABALHAVA)
+-----------------------------------------------+
| * Criar anuncio manualmente                   |
| * Pesquisar concorrencia no Google            |
| * Escrever descricoes uma por uma             |
|                                               |
| PROBLEMA: 1x voce = 1x resultado              |
+-----------------------------------------------+
                    |
                    v
AGENTIC LAYER (Onde voce DEVE trabalhar)
+-----------------------------------------------+
| * Criar TEMPLATES que geram 10 anuncios       |
| * Construir AGENTE que pesquisa automatico    |
| * Definir PADROES que todos seguem            |
|                                               |
| SOLUCAO: 1x template -> 10x planos -> 100x    |
+-----------------------------------------------+
```

### Regra de Ouro

> **Passe pelo menos 50% do seu tempo na camada agentiva,**
> **nao na camada de aplicacao.**

### Pergunta-Chave de Auto-Avaliacao

| Pergunta | Se Sim | Acao |
|----------|--------|------|
| Estou resolvendo ESTE problema? | Camada errada | Suba para agentiva |
| Estou construindo SISTEMA que resolve CLASSE de problemas? | Camada certa | Continue |

### Exercicio: Auto-Diagnostico

**[OPEN_VARIABLE: DIAGNOSTICO_CAMADA]**

```
Liste 5 tarefas que voce fez ontem:

1. _______________
   Camada: [ ] Application [ ] Agentic

2. _______________
   Camada: [ ] Application [ ] Agentic

3. _______________
   Camada: [ ] Application [ ] Agentic

4. _______________
   Camada: [ ] Application [ ] Agentic

5. _______________
   Camada: [ ] Application [ ] Agentic

% na Application Layer: ____%
% na Agentic Layer: ____%

Meta: Inverter essa proporcao em 30 dias.
```

---

## 3. Os 12 Pontos de Alavancagem

### Hierarquia Completa (Menos -> Mais Poderoso)

```
PODER DE ALAVANCAGEM (crescente)

12. Context          -> O que o agente sabe
11. Model            -> Quao inteligente e
10. Prompt           -> Como voce instrui
9.  Tools            -> O que pode fazer
--------------------------------------------
8.  Standard Out     -> Formato de saida
7.  Types            -> Fluxo de dados
6.  Documentation    -> Base de conhecimento
5.  Tests            -> Auto-validacao
--------------------------------------------
4.  Architecture     -> Padroes consistentes
3.  Plans            -> Prompts massivos
2.  Templates        -> Prompts reusaveis **
1.  ADWs             -> Workflows autonomos ***
```

### Divisao Fundamental

| Categoria | Pontos | % Esforco | Quando |
|-----------|--------|-----------|--------|
| IN-AGENT | 12-9 (Context, Model, Prompt, Tools) | 20% | Configure BEM no inicio |
| OUT-AGENT | 8-1 (Standard Out ate ADWs) | 80% | Construa CONTINUAMENTE |

### Detalhamento: 4 IN-AGENT

#### 12. CONTEXT - O que o agente sabe

```
Arquivos de contexto:
+-- PRIME.md           -> Instrucoes primarias
+-- iso_vectorstore/   -> Conhecimento isolado
+-- context/           -> Dominio especifico
```

**Pergunta:** Que conhecimento seu agente precisa ter?

#### 11. MODEL - Capacidade de raciocinio

| Modelo | Uso Ideal | Trade-off |
|--------|-----------|-----------|
| Claude Sonnet 4 | Raciocinio complexo | Mais lento |
| Claude Haiku | Velocidade | Menos profundo |
| GPT-4 | Meta-construction | Alto custo |

**Pergunta:** Qual nivel de raciocinio a tarefa exige?

#### 10. PROMPT - Como voce comunica

```
Tipos de prompt:
+-- /prime-*           -> Comandos de verticalizacao
+-- HOPs               -> Higher Order Prompts
+-- [OPEN_VARIABLES]   -> Flexibilidade
```

**Pergunta:** Como estruturar instrucoes claras?

#### 9. TOOLS - O que pode fazer

```
Built-in: Read, Write, Edit, Bash, Grep, Glob
Custom:   Builders, Validators, APIs externas
```

**Pergunta:** Quais ferramentas o agente precisa?

### Detalhamento: 8 OUT-AGENT

#### 8-7. STANDARD OUT + TYPES

```
Trinity Output: .md + .llm.json + .meta.json
Garante consistencia entre formatos
```

#### 6. DOCUMENTATION

```
Todo conhecimento explicito em arquivos
Agentes aprendem com docs
Conhecimento tribal -> Conhecimento persistido
```

#### 5. TESTS - Auto-validacao **

```
Validators com quality gates
Feedback loops automaticos
Agente corrige seu proprio trabalho
```

#### 4. ARCHITECTURE

```
Estrutura fractal (mesma em todos os niveis)
Previsibilidade = Escalabilidade
```

#### 3. PLANS - Prompts massivos

```
specs/*.md com passos detalhados
Orquestra trabalho complexo
```

#### 2. TEMPLATES - Reusaveis **

```
1 template -> 10 planos -> 100 resultados
Codifica expertise em estrutura
```

#### 1. ADWs - O mais poderoso ***

```
AI Developer Workflows
Agente trabalha enquanto voce esta AFK
Autonomia maxima
```

### Exercicio: Escolha Seu Ponto

**[OPEN_VARIABLE: MEU_PONTO_FOCO]**

```
Analisando os 12 pontos:

Ponto que vou focar PRIMEIRO: _______________

Justificativa:
_______________________________________________
_______________________________________________

Primeira acao concreta:
_______________________________________________

Resultado esperado:
_______________________________________________
```

---

## 4. Os 4 Nucleos de Um Agente

### Diagrama Estrutural

```
+--------------------------------------------------+
|                     AGENTE                        |
+--------------------------------------------------+
|  +---------------+      +---------------+         |
|  |    CONTEXT    |      |     MODEL     |         |
|  |   O que sabe  |      |   Raciocinio  |         |
|  +---------------+      +---------------+         |
|                                                   |
|  +---------------+      +---------------+         |
|  |    PROMPT     |      |     TOOLS     |         |
|  |   Interface   |      |  Capacidades  |         |
|  +---------------+      +---------------+         |
+--------------------------------------------------+
```

### Checklist por Nucleo

| Nucleo | Perguntas-Chave |
|--------|-----------------|
| **CONTEXT** | Que conhecimento precisa? Quais arquivos? Qual dominio? |
| **MODEL** | Qual nivel de raciocinio? Velocidade vs profundidade? |
| **PROMPT** | Qual comando principal? Quais inputs/outputs? |
| **TOOLS** | Quais capacidades? APIs? Validators? |

### Exemplo Completo: Agente de Compliance

```markdown
## AGENTE: Compliance Checker

### 1. CONTEXT (O que sabe)
- Regulamentacoes ANVISA
- Regras INMETRO
- Normas Procon
- Casos de violacao (exemplos)
- Templates de avisos legais

### 2. MODEL (Raciocinio)
- Claude Sonnet (analise complexa)
- Modo analitico (nao criativo)
- Temperature baixa (precisao)

### 3. PROMPT (Interface)
- Comando: /compliance_check
- Input: Texto do anuncio
- Output: Relatorio de conformidade
  - Status: [OK | ALERTA | BLOQUEIO]
  - Problemas encontrados
  - Sugestoes de correcao

### 4. TOOLS (Capacidades)
- Validador regex (palavras proibidas)
- Database de termos ANVISA
- Gerador de alternativas
- API de verificacao INMETRO
```

### Exercicio: Planeje Seu Agente

**[OPEN_VARIABLE: MEU_AGENTE_PLANEJADO]**

```
## AGENTE: _______________

### 1. CONTEXT (O que sabe)
- _______________
- _______________
- _______________

### 2. MODEL (Raciocinio)
- Modelo: _______________
- Modo: _______________
- Por que: _______________

### 3. PROMPT (Interface)
- Comando: /_______________
- Input: _______________
- Output: _______________

### 4. TOOLS (Capacidades)
- _______________
- _______________
- _______________
```

---

## 5. Template Your Engineering

### Principio: 1x -> 10x -> 100x

```
TRADICIONAL:
Problema -> Solucao -> Feito
(1x esforco = 1x resultado)

META-CONSTRUCAO:
Problema -> Template -> Multiplas Solucoes -> Feito
(1x esforco = 100x resultados)
```

### Framework de Templating

```markdown
# Template: [NOME_DO_TEMPLATE]

## Input
$variavel_1: tipo (required/optional)
$variavel_2: tipo (default: valor)

## Processo
1. [Passo com $variavel_1]
2. [Passo com $variavel_2]
3. [Validacao]

## Output
- Formato esperado
- Quality gates

## Exemplos de Uso
- Caso 1: ...
- Caso 2: ...
```

### Identificando Oportunidades de Template

| Sinal | Acao |
|-------|------|
| Faco isso toda semana | TEMPLATE |
| Sempre comeco do zero | TEMPLATE |
| Outros perguntam como faco | TEMPLATE |
| Tenho checklist mental | TEMPLATE |
| Ja errei por esquecer passos | TEMPLATE |

### Exercicio: Identifique Templates

**[OPEN_VARIABLE: MEUS_TEMPLATES]**

```
Liste 3 tarefas repetitivas no seu negocio:

TAREFA 1: _______________
Frequencia: [ ] Diaria [ ] Semanal [ ] Mensal
Variaveis que mudam: _______________
Template possivel: _______________

TAREFA 2: _______________
Frequencia: [ ] Diaria [ ] Semanal [ ] Mensal
Variaveis que mudam: _______________
Template possivel: _______________

TAREFA 3: _______________
Frequencia: [ ] Diaria [ ] Semanal [ ] Mensal
Variaveis que mudam: _______________
Template possivel: _______________

Qual vou templatear PRIMEIRO: _______________
```

---

## 6. Criando Seu Primeiro Agente

### Comando Principal

```
/prime-codexa

"Crie um agente de [FUNCAO] para [CONTEXTO] com:

CONTEXT:
- [Conhecimento 1]
- [Conhecimento 2]
- [Conhecimento 3]

MODEL:
- [Caracteristicas de raciocinio]
- [Tom/modo]

PROMPT:
- Comando: /[nome]
- Recebe: [input]
- Retorna: [output]

TOOLS:
- [Ferramenta 1]
- [Ferramenta 2]
- [Ferramenta 3]"
```

### Exemplo Pratico: Agente de Atendimento

```
/prime-codexa

"Crie um agente de Atendimento ao Cliente para minha loja de
garrafas termicas com:

CONTEXT:
- FAQ de 20 perguntas frequentes
- Politica de troca/devolucao
- Informacoes de produtos
- Historico de reclamacoes comuns

MODEL:
- Rapido e eficiente (Haiku)
- Tom amigavel e prestativo
- Nao inventa informacoes

PROMPT:
- Comando: /atendimento
- Recebe: pergunta do cliente
- Retorna: resposta + categoria + protocolo

TOOLS:
- Busca em FAQ
- Gerador de protocolo
- Escalacao para humano (se necessario)
- Log de interacoes"
```

### Resultado Esperado

```
Novo agente criado em:
agentes/atendimento_agent/
+-- PRIME.md            (instrucoes)
+-- FAQ.md              (base de conhecimento)
+-- context/            (arquivos de contexto)
+-- commands/           (slash commands)
    +-- atendimento.md

Comando disponivel: /prime-atendimento
```

---

## 7. Exercicios Praticos

### Exercicio 1: Auditoria de Camadas (30 min)

**Objetivo:** Mapear onde voce gasta tempo

1. Liste TODAS as tarefas da ultima semana
2. Classifique cada uma: Application ou Agentic
3. Calcule a proporcao
4. Identifique 3 tarefas para "subir de camada"

**Template de Auditoria:**

| Tarefa | Tempo | Camada | Pode Subir? |
|--------|-------|--------|-------------|
| ___ | ___ min | [ ] App [ ] Agent | [ ] Sim |
| ___ | ___ min | [ ] App [ ] Agent | [ ] Sim |
| ___ | ___ min | [ ] App [ ] Agent | [ ] Sim |

**Conclusao:**
- % Application: ___
- % Agentic: ___
- Meta em 30 dias: ___

---

### Exercicio 2: Design de Agente (45 min)

**Objetivo:** Planejar agente completo

1. Identifique um problema recorrente no seu negocio
2. Preencha o template dos 4 nucleos (Secao 4)
3. Valide com as perguntas-chave

**Checklist de Validacao:**

- [ ] Context: Todos os conhecimentos mapeados?
- [ ] Model: Nivel de raciocinio adequado?
- [ ] Prompt: Interface clara e util?
- [ ] Tools: Todas as capacidades necessarias?

---

### Exercicio 3: Criacao de Agente (60 min)

**Objetivo:** Criar agente funcional

1. Use o planejamento do Exercicio 2
2. Execute `/prime-codexa` com seu brief
3. Teste o agente criado
4. Itere e refine

**Template de Teste:**

| Teste | Input | Output Esperado | Output Real | OK? |
|-------|-------|-----------------|-------------|-----|
| 1 | ___ | ___ | ___ | [ ] |
| 2 | ___ | ___ | ___ | [ ] |
| 3 | ___ | ___ | ___ | [ ] |

---

### Exercicio 4: Template Engineering (30 min)

**Objetivo:** Criar template reusavel

1. Escolha tarefa repetitiva (Exercicio da Secao 5)
2. Identifique variaveis
3. Escreva template no formato padrao
4. Teste com 2 casos diferentes

**Validacao:**

- [ ] Template funciona para caso 1?
- [ ] Template funciona para caso 2?
- [ ] Variaveis sao suficientes?
- [ ] Output e consistente?

---

## 8. Templates Avancados

### Template: Agent Brief

```markdown
# AGENT BRIEF

## Identidade
**Nome:** _______________
**Funcao:** _______________
**Dominio:** _______________

## 4 Nucleos

### CONTEXT
Conhecimentos necessarios:
1. _______________
2. _______________
3. _______________

Arquivos de referencia:
- _______________
- _______________

### MODEL
- Modelo base: _______________
- Modo: [ ] Criativo [ ] Analitico [ ] Hibrido
- Temperature: [ ] Baixa [ ] Media [ ] Alta
- Justificativa: _______________

### PROMPT
- Comando principal: /_______________
- Aliases: _______________
- Input format: _______________
- Output format: _______________

### TOOLS
Built-in:
- [ ] Read [ ] Write [ ] Edit [ ] Bash [ ] Grep [ ] Glob

Custom:
1. _______________
2. _______________

## Quality Gates
- [ ] _______________
- [ ] _______________

## Exemplos de Uso
### Caso 1
Input: _______________
Output esperado: _______________

### Caso 2
Input: _______________
Output esperado: _______________
```

### Template: ADW Workflow

```markdown
# ADW: [NOME_DO_WORKFLOW]

## Objetivo
_______________________________________________

## Fases

### 1. PLAN
Inputs:
- _______________

Outputs:
- spec.md com plano detalhado

### 2. BUILD
Inputs:
- spec.md

Outputs:
- _______________

Validacao:
- [ ] _______________

### 3. TEST
Inputs:
- Output do BUILD

Testes:
- [ ] _______________
- [ ] _______________

### 4. REVIEW
Criterios:
- [ ] _______________

Se falhar: Volta para BUILD

### 5. DOCUMENT
Outputs finais:
- _______________
- _______________

## Triggers
Quando executar:
- [ ] _______________
- [ ] Agendado: _______________
```

### Template: Meta-Reflexao Semanal

```markdown
# META-REFLEXAO SEMANAL

**Semana:** _______________
**Data:** _______________

## 1. Camadas
Tempo na Application Layer: ___%
Tempo na Agentic Layer: ___%
Meta: 50/50

## 2. Pontos de Alavancagem
Ponto mais usado esta semana: _______________
Ponto que vou adicionar: _______________

## 3. Agentes
Agentes criados: ___
Agentes melhorados: ___
Agentes mais usados:
1. _______________
2. _______________

## 4. Templates
Novos templates: ___
Templates mais usados:
1. _______________
2. _______________

## 5. Proxima Semana
Foco principal: _______________
Agente a criar: _______________
Template a desenvolver: _______________

## 6. Insights
_______________________________________________
_______________________________________________
```

---

## Reflexao Final

### As 3 Perguntas do Meta-Construtor

Antes de qualquer tarefa, pergunte-se:

1. **"Estou na camada certa?"**
   - Application (executando) vs Agentic (construindo sistemas)

2. **"Isso e uma vez ou para sempre?"**
   - Uma vez = faca
   - Para sempre = template + agente

3. **"Quem deveria fazer isso?"**
   - Eu = Alto valor, criativo, estrategico
   - Agente = Repetitivo, padronizado, escalavel

---

## XP Summary

| Atividade | XP |
|-----------|-----|
| Completar modulo | +50 |
| Executar `/prime-codexa` | +25 |
| Criar agente funcional | +50 |
| Criar template reusavel | +25 |
| Auditoria de camadas completa | +25 |
| 4 nucleos documentados | +25 |
| **TOTAL** | **200** |

---

## Achievement Desbloqueado

```
+--------------------------------------------------+
|                                                  |
|   ACHIEVEMENT: META-GOD                          |
|                                                  |
|   Voce entende como os agentes pensam.           |
|   Voce pode criar qualquer agente.               |
|   Voce trabalha na Agentic Layer.                |
|                                                  |
|   Bem-vindo ao mundo da Meta-Construcao.         |
|                                                  |
+--------------------------------------------------+
```

---

**Workbook Version**: 2.0.0
**Pages**: 16
**Exercises**: 4
**XP Total**: 200
**Generated**: 2025-11-24

