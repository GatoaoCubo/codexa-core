# 📘 Apostila - Módulo 03: Pesquisa de Mercado

**Curso**: CODEXA - Cérebro IA para Sellers
**Módulo**: 03 - Pesquisa
**Duração de estudo**: 1-2 horas
**XP Disponível**: 40 XP

---

## 📋 Índice

1. [Objetivos de Aprendizagem](#1-objetivos-de-aprendizagem)
2. [Os 3 Tipos de Pesquisa](#2-os-3-tipos-de-pesquisa)
3. [Análise Competitiva](#3-análise-competitiva)
4. [Gap Analysis](#4-gap-analysis)
5. [Exercícios Práticos](#5-exercícios-práticos)
6. [Templates](#6-templates)

---

## 1. Objetivos de Aprendizagem

| Objetivo | Verbo (Bloom) | Validação |
|----------|---------------|-----------|
| Executar análise competitiva | Aplicar | Relatório gerado |
| Identificar gaps de mercado | Analisar | 3+ gaps identificados |
| Definir estratégia de preço | Avaliar | Preço definido com dados |

---

## 2. Os 3 Tipos de Pesquisa

### Quadro Comparativo

| Tipo | Tempo | Quando Usar | Entrega |
|------|-------|-------------|---------|
| **Quick** | 15-20 min | Validação rápida | Overview básico |
| **Standard** | 30-40 min | Lançamento | Análise completa |
| **Comprehensive** | 60+ min | Nova categoria | Estratégia full |

### Quick Research

**Comando:**
```
/prime-pesquisa
"Quick research: [produto] no [marketplace]"
```

**Checklist de entrega:**
- [ ] Top 10 concorrentes
- [ ] Faixa de preços (min/med/max)
- [ ] Volume estimado
- [ ] Features principais

### Standard Research

**Comando:**
```
/prime-pesquisa
"Standard research: [produto]
Inclua: competitiva, tendências, gaps, recomendações"
```

**Checklist de entrega:**
- [ ] Análise competitiva completa
- [ ] Tendências da categoria
- [ ] Gaps de oportunidade
- [ ] Recomendações estratégicas

### Comprehensive Research

**Comando:**
```
/prime-pesquisa
"Comprehensive research: [categoria]
Deep dive com forecast e estratégia de entrada"
```

---

## 3. Análise Competitiva

### Os 4 Pilares

```
┌─────────────────────────────────────┐
│ PILAR 1: POSICIONAMENTO             │
│ Como cada concorrente se posiciona? │
├─────────────────────────────────────┤
│ PILAR 2: PREÇOS                     │
│ Faixa, estratégias, promoções       │
├─────────────────────────────────────┤
│ PILAR 3: FEATURES                   │
│ O que tem, o que falta              │
├─────────────────────────────────────┤
│ PILAR 4: REVIEWS                    │
│ Elogios e reclamações               │
└─────────────────────────────────────┘
```

### Template de Análise

**[OPEN_VARIABLE: SUA_ANALISE]**

```markdown
## Análise Competitiva: [CATEGORIA]

### Concorrentes Analisados
| # | Seller | Preço | Diferencial |
|---|--------|-------|-------------|
| 1 | ______ | R$ __ | ___________ |
| 2 | ______ | R$ __ | ___________ |
| 3 | ______ | R$ __ | ___________ |

### Faixa de Preços
- Mínimo: R$ _____
- Médio: R$ _____
- Máximo: R$ _____
- Sweet spot: R$ _____

### Features
| Obrigatórias | Diferenciadoras | Ausentes |
|--------------|-----------------|----------|
| ____________ | ______________ | ________ |
| ____________ | ______________ | ________ |

### Insights de Reviews
- Top elogio: _______________
- Top reclamação: _______________
- Oportunidade: _______________
```

---

## 4. Gap Analysis

### Framework

```
O que TODOS fazem?     → Não compete aqui
O que POUCOS fazem?    → Considere como diferencial
O que NINGUÉM faz?     → OPORTUNIDADE
```

### Exercício Gap Analysis

**[OPEN_VARIABLE: SEU_GAP]**

```
Minha categoria: _______________

TODOS FAZEM:
1. _______________
2. _______________
3. _______________

POUCOS FAZEM:
1. _______________
2. _______________

NINGUÉM FAZ:
1. _______________
2. _______________

MINHA OPORTUNIDADE:
_______________________________________________
_______________________________________________
```

---

## 5. Exercícios Práticos

### Exercício 1: Quick Research (15 min)

**Objetivo:** Validar uma categoria rapidamente

1. Escolha um produto que você está considerando
2. Execute: `/prime-pesquisa "Quick research: [produto]"`
3. Preencha:

| Métrica | Valor |
|---------|-------|
| # Concorrentes | ___ |
| Preço mínimo | R$ ___ |
| Preço máximo | R$ ___ |
| Feature #1 | ___ |

**Decisão:** Vale a pena investir? [ ] Sim [ ] Não
**Por quê:** _______________

---

### Exercício 2: Análise Competitiva (30 min)

**Objetivo:** Entender a concorrência a fundo

1. Escolha uma categoria que você já vende
2. Execute análise dos 4 pilares
3. Preencha o template da Seção 3

**Insight principal descoberto:**
_______________________________________________

---

### Exercício 3: Gap Finding (20 min)

**Objetivo:** Encontrar oportunidades

1. Use os dados do exercício 2
2. Aplique o framework de Gap Analysis
3. Identifique pelo menos 3 gaps

**Gaps identificados:**
1. _______________
2. _______________
3. _______________

**Melhor oportunidade e por quê:**
_______________________________________________

---

## 6. Templates

### Template: Brief de Pesquisa

```markdown
## BRIEF DE PESQUISA

**Tipo:** [ ] Quick [ ] Standard [ ] Comprehensive

**Categoria/Produto:**
_______________

**Marketplace(s):**
[ ] Mercado Livre [ ] Amazon [ ] Shopee [ ] Magalu [ ] Outro: ___

**Objetivo:**
[ ] Validar ideia
[ ] Lançar produto
[ ] Entender concorrência
[ ] Definir preço
[ ] Encontrar nicho

**Perguntas específicas:**
1. _______________
2. _______________
3. _______________

**Deadline:**
_______________
```

### Template: Relatório de Pesquisa

```markdown
## RELATÓRIO DE PESQUISA

**Data:** _______________
**Categoria:** _______________
**Tipo:** _______________

### Resumo Executivo
[3 linhas com principais descobertas]

### Dados Quantitativos
| Métrica | Valor |
|---------|-------|
| Total concorrentes | ___ |
| Preço médio | R$ ___ |
| Volume estimado | ___ |

### Análise Qualitativa
[Principais insights]

### Oportunidades Identificadas
1. _______________
2. _______________

### Recomendação
[ ] Entrar [ ] Não entrar [ ] Mais pesquisa necessária

**Justificativa:**
_______________________________________________
```

---

## 🎮 XP Summary

| Atividade | XP |
|-----------|-----|
| Completar módulo | +25 |
| Executar `/prime-pesquisa` | +10 |
| Análise competitiva completa | +5 |
| **TOTAL** | **40** |

---

**Workbook Version**: 2.0.0
**Pages**: 8
**Exercises**: 3
**Generated**: 2025-11-24
