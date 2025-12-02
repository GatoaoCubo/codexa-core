# Apostila - Modulo 05: Fotos com IA

**Curso**: CODEXA - Cerebro IA para Sellers
**Modulo**: 05 - Fotos com IA
**Duracao de estudo**: 1.5-2 horas
**XP Disponivel**: 40 XP

---

## Indice

1. [Objetivos de Aprendizagem](#1-objetivos-de-aprendizagem)
2. [Photo Agent - Visao Geral](#2-photo-agent---visao-geral)
3. [Requisitos por Marketplace](#3-requisitos-por-marketplace)
4. [O Grid 3x3 Perfeito](#4-o-grid-3x3-perfeito)
5. [Os 7 Estilos Fotograficos](#5-os-7-estilos-fotograficos)
6. [Brand Alignment](#6-brand-alignment)
7. [Exercicios Praticos](#7-exercicios-praticos)
8. [Templates](#8-templates)

---

## 1. Objetivos de Aprendizagem

| Objetivo | Verbo (Bloom) | Validacao |
|----------|---------------|-----------|
| Gerar fotos profissionais | Criar | Grid completo gerado |
| Criar grid 9 fotos | Aplicar | 3x3 preenchido |
| Aplicar estilos fotograficos | Aplicar | 2 estilos escolhidos |
| Otimizar para marketplaces | Analisar | Specs verificados |

---

## 2. Photo Agent - Visao Geral

### Arquitetura Dual-Layer

```
+--------------------------------------------------+
| ADW (AI Developer Workflow)                       |
| -> O QUE fazer (5 fases)                          |
|    Plan -> Generate -> Validate -> Refine -> Deliver
+--------------------------------------------------+
| HOP (Higher Order Prompts)                        |
| -> COMO fazer (prompts modulares)                 |
|    Cada cena tem seu proprio prompt otimizado     |
+--------------------------------------------------+
```

### Capacidades do Photo Agent

| Componente | Descricao |
|------------|-----------|
| 12 Perfis de Camera | Canon, Sony, Fuji, Nikon... |
| 7 Estilos Fotograficos | Minimalist, Dramatic, Lifestyle... |
| 9 Specs de Marketplace | Resolucao, aspect ratio por plataforma |
| Brand Alignment | Herda diretrizes do Marca Agent |

### Comando Principal

```
/prime-photo

"Crie grid 9 fotos para [PRODUTO]:
- Estilo: [ESTILO_PRIMARIO] + [ESTILO_SECUNDARIO]
- Marca: [NOME_MARCA] ([CORES], [VALORES])
- Marketplace: [PLATAFORMA] ([RESOLUCAO] min)"
```

---

## 3. Requisitos por Marketplace

### Tabela de Especificacoes

| Marketplace | Resolucao Min | Recomendado | Fundo | Formato |
|-------------|---------------|-------------|-------|---------|
| Mercado Livre | 1200x1200 | 1600x1600 | Branco (principal) | JPG/PNG |
| Amazon BR | 1000x1000 | 2000x2000 | Branco obrigatorio | JPG |
| Shopee | 800x800 | 1200x1200 | Livre | JPG/PNG |
| Magalu | 1000x1000 | 1500x1500 | Branco preferencial | JPG |
| Americanas | 1000x1000 | 1500x1500 | Branco | JPG |
| Shein | 800x800 | 1200x1200 | Branco | JPG |

### Regras de Ouro

```
REGRA 1: Gere SEMPRE na maior resolucao
         -> Reduza para cada plataforma
         -> NUNCA aumente (perde qualidade)

REGRA 2: Foto principal = Fundo branco
         -> Melhor CTR
         -> Padrao da maioria

REGRA 3: Produto ocupa 85% do frame
         -> Nem muito pequeno
         -> Nem cortado

REGRA 4: Iluminacao uniforme
         -> Sem sombras duras
         -> Profissional
```

### Exercicio: Meus Requisitos

**[OPEN_VARIABLE: MEUS_REQUISITOS]**

```
Meu marketplace principal: _______________
Resolucao que vou usar: _______________
Formato de arquivo: _______________
Estilo de fundo: _______________

Marketplaces secundarios:
1. _______________ (resolucao: ___)
2. _______________ (resolucao: ___)
```

---

## 4. O Grid 3x3 Perfeito

### Estrutura Visual

```
+------------------+------------------+------------------+
|    1. HERO       |    2. DETALHE    |    3. ANGULO     |
|    Principal     |    Material      |    Superior      |
|    Fundo branco  |    Textura       |    Vista de cima |
+------------------+------------------+------------------+
|    4. LIFESTYLE  |    5. ESCALA     |    6. EMBALAGEM  |
|    Em uso        |    Comparacao    |    Como chega    |
|    Contexto real |    Tamanho real  |    Unboxing      |
+------------------+------------------+------------------+
|    7. AMBIENTE   |    8. FEATURES   |    9. INFOGRAFICO|
|    Outdoor/indoor|    Detalhe tampa |    Specs visuais |
|    Mood          |    Diferencial   |    Beneficios    |
+------------------+------------------+------------------+
```

### Detalhamento por Posicao

| # | Tipo | Objetivo | Especificacao |
|---|------|----------|---------------|
| 1 | Hero | Primeira impressao | Fundo branco, 85% preenchido, alta resolucao |
| 2 | Detalhe | Mostrar qualidade | Close no material, textura visivel |
| 3 | Angulo | Dimensoes | Vista superior ou lateral, proporcoes claras |
| 4 | Lifestyle | Emocao | Pessoa usando, contexto aspiracional |
| 5 | Escala | Tamanho real | Objeto comum de referencia (mao, caneta) |
| 6 | Embalagem | Expectativa | Como o cliente recebe, unboxing |
| 7 | Ambiente | Contexto | Onde o produto "vive" (outdoor/indoor) |
| 8 | Features | Diferencial | Destaque do que torna unico |
| 9 | Infografico | Specs | Texto + imagem, beneficios visuais |

### Exercicio: Meu Grid Planejado

**[OPEN_VARIABLE: MEU_GRID]**

```
Meu produto: _______________

1. HERO:
   Descricao: _______________
   Fundo: _______________

2. DETALHE:
   O que mostrar: _______________
   Close em: _______________

3. ANGULO:
   Vista: [ ] Superior [ ] Lateral [ ] 45 graus
   Objetivo: _______________

4. LIFESTYLE:
   Cenario: _______________
   Pessoa: [ ] Sim [ ] Nao
   Acao: _______________

5. ESCALA:
   Objeto de referencia: _______________
   Tamanho real: _______________

6. EMBALAGEM:
   Tipo: [ ] Caixa [ ] Sacola [ ] Envelope
   Mostrar: _______________

7. AMBIENTE:
   Local: [ ] Indoor [ ] Outdoor
   Descricao: _______________

8. FEATURES:
   Diferencial principal: _______________
   Como mostrar: _______________

9. INFOGRAFICO:
   Specs a destacar: _______________
   Beneficios: _______________
```

---

## 5. Os 7 Estilos Fotograficos

### Quadro de Referencia

| # | Estilo | Caracteristicas | Ideal Para |
|---|--------|-----------------|------------|
| 1 | **Minimalist** | Fundo limpo, cores neutras, foco total | Tech, premium, clean |
| 2 | **Dramatic** | Contraste alto, sombras marcadas | Luxo, esporte, masculino |
| 3 | **Lifestyle** | Contexto real, pessoas usando | Moda, casa, bem-estar |
| 4 | **Editorial** | Composicao artistica, storytelling | Moda, arte, design |
| 5 | **Commercial** | Profissional, direto, confianca | B2B, corporativo |
| 6 | **Cinematic** | Mood dramatico, cores gradientes | Premium, experiencia |
| 7 | **Vintage** | Filtros retro, nostalgia | Handmade, organico |

### Matriz de Escolha

| Seu Produto | Estilo Primario | Estilo Secundario |
|-------------|-----------------|-------------------|
| Tech/Eletronicos | Minimalist | Commercial |
| Moda/Vestuario | Lifestyle | Editorial |
| Alimentos | Lifestyle | Vintage |
| Esportes/Fitness | Dramatic | Lifestyle |
| Eco/Sustentavel | Minimalist | Lifestyle |
| Premium/Luxo | Cinematic | Dramatic |
| Infantil | Lifestyle | Commercial |
| Decoracao | Editorial | Lifestyle |

### Exercicio: Meus Estilos

**[OPEN_VARIABLE: MEUS_ESTILOS]**

```
Meu produto: _______________
Meu publico: _______________

Estilo PRIMARIO escolhido: _______________
Por que: _______________________________________________

Estilo SECUNDARIO escolhido: _______________
Por que: _______________________________________________

Como vou combinar:
_______________________________________________
```

---

## 6. Brand Alignment

### Conceito: Heranca Automatica

O Photo Agent herda automaticamente do Marca Agent:

```
Marca Agent define:
+-- Paleta de cores    -> Photo Agent usa nas composicoes
+-- Arquetipo          -> Photo Agent escolhe mood compativel
+-- Tom de voz         -> Photo Agent traduz em visual
+-- Posicionamento     -> Photo Agent reforca diferencial
```

### Traducao Marca -> Foto

| Elemento Marca | Traducao Visual |
|----------------|-----------------|
| Arquetipo Heroi | Angulos heroicos, luz dramatica |
| Arquetipo Explorador | Outdoor, natureza, movimento |
| Arquetipo Cuidador | Luz suave, tons quentes, aconchego |
| Arquetipo Mago | Efeitos, misterio, transformacao |
| Tom Formal | Composicao simetrica, clean |
| Tom Casual | Espontaneo, dinamico |
| Cores Quentes | Energia, paixao, urgencia |
| Cores Frias | Confianca, calma, profissionalismo |

### Template: Brand-to-Photo Brief

```markdown
## BRAND-TO-PHOTO BRIEF

### Da Marca
Arquetipo primario: _______________
Arquetipo secundario: _______________
Paleta de cores: _______________
Tom de voz: _______________

### Para Foto
Mood geral: _______________
Iluminacao: [ ] Suave [ ] Dramatica [ ] Natural
Ambiente: [ ] Estudio [ ] Outdoor [ ] Indoor real
Props: _______________
Evitar: _______________
```

---

## 7. Exercicios Praticos

### Exercicio 1: Planejamento de Grid (20 min)

**Objetivo:** Planejar grid completo antes de gerar

1. Escolha um produto do seu catalogo
2. Preencha o template da Secao 4
3. Valide cada foto contra os objetivos

**Checklist de validacao:**
- [ ] Todas as 9 posicoes preenchidas?
- [ ] Hero com fundo branco?
- [ ] Lifestyle com contexto real?
- [ ] Infografico com specs claros?

---

### Exercicio 2: Geracao com Photo Agent (30 min)

**Objetivo:** Gerar grid completo

1. Execute o comando:

```
/prime-photo

"Crie grid 9 fotos para [SEU_PRODUTO]:
- Estilo: [ESTILO_1] + [ESTILO_2]
- Marca: [SUA_MARCA]
- Paleta: [SUAS_CORES]
- Marketplace: [PLATAFORMA] ([RESOLUCAO])"
```

2. Avalie cada foto gerada:

| Foto # | Aprovada? | Ajuste Necessario |
|--------|-----------|-------------------|
| 1 | [ ] Sim [ ] Nao | _______________ |
| 2 | [ ] Sim [ ] Nao | _______________ |
| 3 | [ ] Sim [ ] Nao | _______________ |
| 4 | [ ] Sim [ ] Nao | _______________ |
| 5 | [ ] Sim [ ] Nao | _______________ |
| 6 | [ ] Sim [ ] Nao | _______________ |
| 7 | [ ] Sim [ ] Nao | _______________ |
| 8 | [ ] Sim [ ] Nao | _______________ |
| 9 | [ ] Sim [ ] Nao | _______________ |

---

### Exercicio 3: Comparacao A/B (15 min)

**Objetivo:** Comparar fotos geradas com fotos atuais

1. Selecione 3 fotos atuais do seu produto
2. Gere 3 fotos equivalentes com Photo Agent
3. Compare:

| Criterio | Foto Atual | Foto IA | Melhor |
|----------|------------|---------|--------|
| Qualidade | ___/10 | ___/10 | [ ] Atual [ ] IA |
| Profissionalismo | ___/10 | ___/10 | [ ] Atual [ ] IA |
| Brand alignment | ___/10 | ___/10 | [ ] Atual [ ] IA |
| Atratividade | ___/10 | ___/10 | [ ] Atual [ ] IA |

**Conclusao:**
_______________________________________________

---

## 8. Templates

### Template: Brief de Foto

```markdown
## BRIEF DE FOTOGRAFIA

**Produto:** _______________
**SKU:** _______________

### Especificacoes Tecnicas
- Resolucao: _______________
- Formato: [ ] JPG [ ] PNG
- Fundo: [ ] Branco [ ] Contextual [ ] Transparente
- Aspect ratio: [ ] 1:1 [ ] 4:3 [ ] 16:9

### Diretrizes de Marca
- Paleta: _______________
- Estilo: _______________
- Mood: _______________

### Grid Solicitado
[ ] Grid 3x3 completo (9 fotos)
[ ] Hero apenas
[ ] Hero + Lifestyle
[ ] Personalizado: _______________

### Observacoes
_______________________________________________
```

### Template: Checklist de Qualidade

```markdown
## CHECKLIST DE QUALIDADE - FOTO

**Produto:** _______________
**Data:** _______________

### Tecnicos
- [ ] Resolucao minima atingida
- [ ] Formato correto
- [ ] Produto ocupa 85% do frame
- [ ] Sem distorcao

### Esteticos
- [ ] Iluminacao uniforme
- [ ] Cores fieis ao produto
- [ ] Composicao equilibrada
- [ ] Sem elementos distrativos

### Brand
- [ ] Alinhado com paleta da marca
- [ ] Mood coerente com arquetipo
- [ ] Transmite posicionamento

### Marketplace
- [ ] Atende requisitos da plataforma
- [ ] Fundo apropriado
- [ ] Pronto para upload

**Score geral:** ___/10
**Aprovado:** [ ] Sim [ ] Nao
```

### Template: Inventario de Fotos

```markdown
## INVENTARIO DE FOTOS - [PRODUTO]

| # | Tipo | Arquivo | Resolucao | Marketplace | Status |
|---|------|---------|-----------|-------------|--------|
| 1 | Hero | ___.jpg | ___x___ | ___ | [ ] OK |
| 2 | Detalhe | ___.jpg | ___x___ | ___ | [ ] OK |
| 3 | Angulo | ___.jpg | ___x___ | ___ | [ ] OK |
| 4 | Lifestyle | ___.jpg | ___x___ | ___ | [ ] OK |
| 5 | Escala | ___.jpg | ___x___ | ___ | [ ] OK |
| 6 | Embalagem | ___.jpg | ___x___ | ___ | [ ] OK |
| 7 | Ambiente | ___.jpg | ___x___ | ___ | [ ] OK |
| 8 | Features | ___.jpg | ___x___ | ___ | [ ] OK |
| 9 | Infografico | ___.jpg | ___x___ | ___ | [ ] OK |

**Total:** ___ fotos
**Completo:** [ ] Sim [ ] Nao
```

---

## XP Summary

| Atividade | XP |
|-----------|-----|
| Completar modulo | +20 |
| Executar `/prime-photo` | +10 |
| Grid 9 fotos completo | +10 |
| **TOTAL** | **40** |

---

**Workbook Version**: 2.0.0
**Pages**: 10
**Exercises**: 3
**Generated**: 2025-11-24

