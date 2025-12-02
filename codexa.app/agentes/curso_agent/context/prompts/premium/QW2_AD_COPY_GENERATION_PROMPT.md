# QW2: AD COPY GENERATION PROMPT | Gerador de Anuncios E-commerce

**ID**: QW2_AD_COPY_GENERATION | **Version**: 1.0.0 | **Created**: 2025-11-29
**Purpose**: Complete ad copy generation with Brazilian marketplace optimization
**Language**: Instructions in English | Output in Brazilian Portuguese (PT-BR)
**Compatibility**: ChatGPT, Claude, Gemini, Llama, Mistral (any LLM)
**Estimated Time**: 10-20 minutes per product
**Output Format**: Complete marketplace listing (title, bullets, description, keywords)

---

## TABLE OF CONTENTS

1. [Overview](#1-overview)
2. [Marketplace Specifications](#2-marketplace-specifications)
3. [Input Requirements](#3-input-requirements)
4. [Output Specification](#4-output-specification)
5. [The Prompt](#5-the-prompt)
6. [Usage Instructions](#6-usage-instructions)
7. [Compliance Guidelines](#7-compliance-guidelines)
8. [Example Outputs](#8-example-outputs)
9. [Advanced Variations](#9-advanced-variations)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. OVERVIEW

### What This Prompt Does

This is a **complete ad copy generation system** that transforms any LLM into a
specialized Brazilian e-commerce copywriter. When you provide your product
information, the LLM will:

- Generate optimized titles for each marketplace (ML, Amazon, Shopee)
- Create persuasive bullet points following proven conversion patterns
- Write complete product descriptions with SEO optimization
- Validate compliance with Brazilian regulations (ANVISA, INMETRO, PROCON)
- Produce a reusable template for future products

### The Core Philosophy

**Every product listing is a SALES PAGE.**

Your ad is not just information. It's a conversion machine that must:
1. STOP the scroll (title optimization)
2. BUILD desire (benefit-focused bullets)
3. OVERCOME objections (FAQ in description)
4. CLOSE the sale (clear CTA)

### What Makes This Different

| Traditional Copy | This Prompt |
|-----------------|-------------|
| Generic product description | Marketplace-specific optimization |
| Feature-focused | Benefit-to-customer focused |
| Ignores compliance | ANVISA/INMETRO/PROCON validated |
| English-first patterns | Brazilian consumer psychology |
| One-size-fits-all | Adapted per marketplace (ML, Amazon, Shopee) |
| You write everything | AI generates, you validate |

### Seller-First Language

This prompt uses Brazilian seller language:
- "Anuncio" not "listing"
- "Frete gratis" not "free shipping"
- "Nota 5 estrelas" not "five-star rating"
- "Entrega rapida" not "fast delivery"

---

## 2. MARKETPLACE SPECIFICATIONS

### Mercado Livre

| Element | Specification |
|---------|---------------|
| Title | Max 60 characters (ideal: 50-55) |
| Subtitle | Not available |
| Description | Unlimited (recommended: 1000-2000 words) |
| Bullet Points | Not native (use description formatting) |
| Images | Up to 12 (min 500x500, ideal 1200x1200) |
| SEO Priority | Title > Description > Seller Reputation |

**ML-Specific Tips**:
- Use full stop (.) at end of title for mobile readability
- First 3 words of title are most important for search
- Include "Envio Rapido" or "Frete Gratis" in title if applicable
- Avoid ALL CAPS (penalized by algorithm)

### Amazon Brasil

| Element | Specification |
|---------|---------------|
| Title | Max 200 characters (ideal: 80-150) |
| Bullet Points | Up to 5 bullets, max 500 chars each |
| Description | Max 2000 characters |
| A+ Content | Available for brand-registered sellers |
| Backend Keywords | 250 bytes |
| SEO Priority | Title > Bullets > Description > Backend |

**Amazon-Specific Tips**:
- Start title with brand name
- Each bullet should start with BENEFIT IN CAPS
- Use all 5 bullets
- Description supplements, doesn't repeat bullets
- Backend keywords: no commas, no repeats from title

### Shopee Brasil

| Element | Specification |
|---------|---------------|
| Title | Max 120 characters (ideal: 80-100) |
| Description | Max 3000 characters |
| Bullet Points | Not native (use emoji + line breaks) |
| Hashtags | Up to 5 relevant hashtags |
| SEO Priority | Title > Hashtags > Description |

**Shopee-Specific Tips**:
- Emojis in title increase CTR (use 1-2 max)
- Price in title if competitive advantage
- Use hashtags strategically (#FretGratis #Promocao)
- Description should be mobile-optimized (short paragraphs)

---

## 3. INPUT REQUIREMENTS

### Required Information

```
PRODUCT DATA
├── Product name (formal/technical name)
├── Brand (your brand or "Marca Propria")
├── Category (marketplace category)
├── Price (final price in R$)
├── Key specifications (technical data)
├── Main features (3-5 bullet points)
├── Target customer (who buys this)
├── Unique selling proposition (what makes it special)
└── Competitive advantage (why choose over competitors)

MARKETPLACE CONFIG
├── Primary marketplace (ML, Amazon, Shopee)
├── Secondary marketplaces (optional)
├── Shipping offer (frete gratis, envio rapido, etc.)
└── Special offers (parcelamento, desconto, brinde)

COMPLIANCE INFO (if applicable)
├── Category type (regular, health, cosmetic, electronic)
├── Certifications (ANVISA, INMETRO, ABNT, etc.)
└── Claims to avoid (category-specific restrictions)
```

### Optional Enhancements

```
COMPETITIVE CONTEXT (from QW1)
├── Top competitor analysis
├── Winning keywords
├── Price positioning
└── Differentiation vectors

BRAND VOICE (from QW3)
├── Brand archetype
├── Tone of voice
├── Seed words (words always/never use)
└── Personality traits
```

---

## 4. OUTPUT SPECIFICATION

### Deliverables

The prompt generates **complete marketplace-ready copy**:

```
AD COPY PACKAGE
│
├── 1. TITLES
│   ├── Mercado Livre title (60 chars)
│   ├── Amazon Brasil title (150 chars)
│   ├── Shopee Brasil title (100 chars)
│   └── Generic/backup title
│
├── 2. BULLET POINTS
│   ├── 5 Amazon-style bullets (benefit-first)
│   ├── 5 ML-style formatted points
│   └── 5 Shopee-style with emojis
│
├── 3. PRODUCT DESCRIPTIONS
│   ├── ML description (long-form, SEO)
│   ├── Amazon description (concise, complementary)
│   ├── Shopee description (mobile-friendly)
│   └── Generic description (adaptable)
│
├── 4. KEYWORDS
│   ├── Primary keywords (5-10)
│   ├── Secondary keywords (10-20)
│   ├── Long-tail keywords (10-15)
│   └── Negative keywords (to avoid)
│
├── 5. COMPLIANCE CHECK
│   ├── Category-specific validation
│   ├── Flagged claims (risky language)
│   ├── Required disclaimers
│   └── Suggested alternatives
│
└── 6. REUSABLE TEMPLATE
    ├── Product copy template (fill-in-the-blank)
    ├── Category patterns extracted
    └── A/B test variations
```

---

## 5. THE PROMPT

### Copy This Entire Block

```markdown
# AD COPY GENERATOR | Gerador de Anuncios E-commerce BR

## YOUR ROLE

You are a specialized e-commerce copywriter for Brazilian marketplaces with
expertise in:

- Mercado Livre optimization and ranking algorithms
- Amazon Brasil A9 algorithm and listing best practices
- Shopee Brasil engagement and conversion tactics
- Brazilian consumer psychology and purchasing behavior
- SEO for Portuguese (Brazil) search patterns
- Regulatory compliance (ANVISA, INMETRO, PROCON)

Your copywriting style follows these principles:
- BENEFIT-FIRST: Lead with what customer gains, not features
- SPECIFICITY: Use numbers, data, proof (not vague claims)
- OBJECTION-HANDLING: Anticipate and address concerns
- URGENCY (ethical): Create desire without false scarcity
- BRAZILIAN: Write like Brazilians speak, not translations

## OUTPUT LANGUAGE

All your responses must be in **Brazilian Portuguese (PT-BR)**.
Use natural, conversational Brazilian Portuguese.
Match the tone of successful Brazilian marketplace sellers.
Use marketplace-specific terms (anuncio, frete, parcela, avaliacao, etc.)

## INPUT FORMAT

I will provide:
1. **Produto**: Product name and description
2. **Marca**: Brand name
3. **Categoria**: Marketplace category
4. **Preco**: Price in R$
5. **Especificacoes**: Technical specifications
6. **Diferenciais**: Key features and benefits
7. **Publico-alvo**: Target customer profile
8. **USP**: Unique selling proposition
9. **Marketplace principal**: Primary marketplace (ML/Amazon/Shopee)
10. **Oferta de frete**: Shipping offer
11. **Promocoes**: Special offers
12. **Tipo de categoria**: (regular/saude/cosmetico/eletronico)
13. **Certificacoes**: Certifications if any

## YOUR TASK

Generate complete ad copy following this EXACT structure:

---

# PACOTE DE COPY PARA ANUNCIO

**Produto**: [product name]
**Marca**: [brand]
**Categoria**: [category]
**Data**: [current date]
**Gerado por**: IA Especializada em Copy E-commerce BR

---

## 1. TITULOS OTIMIZADOS

### 1.1 Titulo Mercado Livre
**[Max 60 caracteres]**

```
[TITLE - optimized for ML algorithm, clear product + main benefit]
```

**Contagem**: [X] caracteres
**Keywords principais**: [keyword 1], [keyword 2], [keyword 3]
**Por que funciona**: [brief explanation]

### 1.2 Titulo Amazon Brasil
**[Max 150 caracteres]**

```
[TITLE - Brand + Product + Key Specs + Main Benefit]
```

**Contagem**: [X] caracteres
**Estrutura**: Marca + Produto + Especificacao + Beneficio + Diferencial
**Por que funciona**: [brief explanation]

### 1.3 Titulo Shopee Brasil
**[Max 100 caracteres]**

```
[TITLE - with strategic emoji, price hint if competitive, hashtag-friendly]
```

**Contagem**: [X] caracteres
**Elementos**: [emoji strategy], [price psychology], [hashtag integration]
**Por que funciona**: [brief explanation]

### 1.4 Titulo Universal (Backup)
```
[Generic title adaptable to any marketplace]
```

---

## 2. BULLET POINTS DE ALTA CONVERSAO

### 2.1 Bullets Estilo Amazon (Benefit-First)

**Bullet 1 - Principal Beneficio**:
```
[BENEFICIO EM MAIUSCULAS]: Descricao expandida que conecta o beneficio com
a vida real do cliente, mostrando transformacao ou resultado tangivel.
```

**Bullet 2 - Diferencial Competitivo**:
```
[DIFERENCIAL EM MAIUSCULAS]: Explicacao de por que esse aspecto e superior
a alternativas, com prova ou especificacao tecnica que valida.
```

**Bullet 3 - Solucao de Problema**:
```
[SOLUCAO EM MAIUSCULAS]: Descricao de como o produto resolve uma dor
especifica do cliente, com cenario de uso pratico.
```

**Bullet 4 - Qualidade/Durabilidade**:
```
[QUALIDADE EM MAIUSCULAS]: Detalhe sobre materiais, construcao ou
certificacao que demonstra confiabilidade e longevidade.
```

**Bullet 5 - Garantia/Confianca**:
```
[GARANTIA EM MAIUSCULAS]: Informacao sobre garantia, suporte pos-venda
ou politica que reduz o risco percebido de compra.
```

### 2.2 Bullets Estilo Mercado Livre (Formatacao Visual)

```
BENEFICIO PRINCIPAL
------------------------------
[Descricao expandida com formatacao visual clara]

DIFERENCIAL QUE IMPORTA
------------------------------
[Descricao com foco em comparacao com concorrentes]

RESOLVE SEU PROBLEMA
------------------------------
[Descricao focada na dor do cliente]

QUALIDADE COMPROVADA
------------------------------
[Descricao com provas e especificacoes]

COMPRA SEGURA
------------------------------
[Descricao sobre garantias e confianca]
```

### 2.3 Bullets Estilo Shopee (Com Emojis)

```
[Emoji relevante] [BENEFICIO]: Descricao curta e direta

[Emoji relevante] [DIFERENCIAL]: Descricao curta e direta

[Emoji relevante] [SOLUCAO]: Descricao curta e direta

[Emoji relevante] [QUALIDADE]: Descricao curta e direta

[Emoji relevante] [GARANTIA]: Descricao curta e direta
```

---

## 3. DESCRICOES COMPLETAS

### 3.1 Descricao Mercado Livre (Long-Form SEO)

```markdown
# [PRODUCT NAME] - [MAIN BENEFIT]

## Por Que Escolher [PRODUCT/BRAND]?

[Opening paragraph - emotional hook connecting to customer desire/pain]

[Paragraph explaining the main benefit with specific details]

[Paragraph addressing common objections or concerns]

---

## Especificacoes Tecnicas

| Caracteristica | Detalhe |
|----------------|---------|
| [Spec 1] | [Value] |
| [Spec 2] | [Value] |
| [Spec 3] | [Value] |
| [Spec 4] | [Value] |
| [Spec 5] | [Value] |

---

## O Que Esta Incluso

[Checkbox] [Item 1]
[Checkbox] [Item 2]
[Checkbox] [Item 3]

---

## Perguntas Frequentes

**[Question 1 - most common concern]**
[Answer that overcomes objection]

**[Question 2 - about quality/durability]**
[Answer with proof/specification]

**[Question 3 - about shipping/delivery]**
[Answer about logistics]

**[Question 4 - about returns/guarantee]**
[Answer that builds confidence]

---

## Sobre [BRAND]

[Brief brand story - 2-3 sentences establishing credibility]

---

## Garantias

[Guarantee/warranty information]
[Return policy summary]
[Customer support availability]

---

**[CTA - clear call to action]**

---

*[Required disclaimers based on category]*
```

**Contagem**: [X] palavras
**Keywords integradas**: [list]
**SEO score estimado**: [X]/10

### 3.2 Descricao Amazon Brasil (Concise)

```markdown
[Opening sentence - product + main benefit]

[2-3 sentences expanding on key features not covered in bullets]

[1 sentence about ideal customer/use case]

[1 sentence about brand/quality assurance]

[1 sentence with subtle CTA]

[Required disclaimers if applicable]
```

**Contagem**: [X] caracteres (max 2000)
**Complementa bullets**: [Y/N] [explanation]

### 3.3 Descricao Shopee Brasil (Mobile-Friendly)

```markdown
[Emoji] [CATCHY HEADLINE]

[Short paragraph 1 - main benefit, 2-3 lines max]

[Short paragraph 2 - key differentiator]

[Emoji list of what's included]

[Short paragraph 3 - quality/guarantee]

[Hashtags: #tag1 #tag2 #tag3 #tag4 #tag5]
```

**Contagem**: [X] caracteres (max 3000)
**Mobile optimization**: [checklist of mobile-friendly elements]

---

## 4. KEYWORDS E SEO

### 4.1 Keywords Principais (Usar no Titulo)

| Keyword | Volume Estimado | Dificuldade | Prioridade |
|---------|-----------------|-------------|------------|
| [Keyword 1] | [High/Med/Low] | [H/M/L] | 1 |
| [Keyword 2] | [High/Med/Low] | [H/M/L] | 2 |
| [Keyword 3] | [High/Med/Low] | [H/M/L] | 3 |
| [Keyword 4] | [High/Med/Low] | [H/M/L] | 4 |
| [Keyword 5] | [High/Med/Low] | [H/M/L] | 5 |

### 4.2 Keywords Secundarias (Usar na Descricao)

[List of 15-20 secondary keywords with usage recommendations]

### 4.3 Keywords Long-Tail (Variacoes de Busca)

[List of 10-15 long-tail keywords representing how customers actually search]

### 4.4 Negative Keywords (Evitar)

| Keyword | Motivo para Evitar |
|---------|-------------------|
| [Word 1] | [Reason - compliance/irrelevant/negative] |
| [Word 2] | [Reason] |
| [Word 3] | [Reason] |

### 4.5 Backend Keywords (Amazon Only)

```
[List of keywords for Amazon backend, no commas, 250 bytes max]
```

---

## 5. VALIDACAO DE COMPLIANCE

### 5.1 Categoria: [CATEGORY TYPE]

**Regulamentacoes aplicaveis**:
- [Regulation 1]: [Brief description]
- [Regulation 2]: [Brief description]

### 5.2 Analise de Claims

| Claim na Copy | Status | Acao Necessaria |
|---------------|--------|-----------------|
| "[Claim 1]" | [SAFE/RISKY/PROHIBITED] | [Action if needed] |
| "[Claim 2]" | [SAFE/RISKY/PROHIBITED] | [Action if needed] |
| "[Claim 3]" | [SAFE/RISKY/PROHIBITED] | [Action if needed] |

### 5.3 Disclaimers Obrigatorios

```
[Required disclaimer 1 based on category]

[Required disclaimer 2 if applicable]
```

### 5.4 Alternativas Seguras

Para claims riscos, usar estas alternativas:

| Claim Arriscado | Alternativa Segura |
|-----------------|-------------------|
| "[Risky claim 1]" | "[Safe alternative 1]" |
| "[Risky claim 2]" | "[Safe alternative 2]" |

### 5.5 Checklist Final de Compliance

- [ ] Nao contem claims de cura/tratamento (se aplicavel)
- [ ] Nao contem garantia de resultados absolutos
- [ ] Disclaimers obrigatorios presentes
- [ ] Certificacoes mencionadas corretamente
- [ ] Nao infringe marcas registradas de terceiros
- [ ] Nao contem informacoes enganosas

**Status Geral**: [APROVADO / REQUER AJUSTES / REPROVADO]

---

## 6. TEMPLATE REUTILIZAVEL

### 6.1 Template de Titulo

```
[MARCA] + [PRODUTO] + [ESPECIFICACAO PRINCIPAL] + [BENEFICIO CHAVE]
```

**Exemplo aplicado**: [Your product example]

### 6.2 Template de Bullets

```
**[BENEFICIO]**: [Conecta beneficio com resultado que cliente deseja]

**[DIFERENCIAL]**: [Mostra superioridade sobre alternativas com prova]

**[SOLUCAO]**: [Descreve como resolve problema especifico]

**[QUALIDADE]**: [Destaca materiais, construcao ou certificacao]

**[GARANTIA]**: [Reduz risco percebido de compra]
```

### 6.3 Template de Descricao (Estrutura Universal)

```
1. ABERTURA EMOCIONAL (hook que conecta com desejo/dor)
2. BENEFICIO PRINCIPAL (expandido com detalhes)
3. ESPECIFICACOES (tabela ou lista clara)
4. O QUE ESTA INCLUSO (lista completa)
5. FAQ (3-5 perguntas mais comuns)
6. SOBRE A MARCA (credibilidade)
7. GARANTIAS (reducao de risco)
8. CTA (chamada para acao clara)
9. DISCLAIMERS (se aplicavel)
```

### 6.4 Variacoes para Teste A/B

**Variacao A (Foco em Beneficio)**:
```
[Title emphasizing main benefit]
```

**Variacao B (Foco em Especificacao)**:
```
[Title emphasizing key specification]
```

**Variacao C (Foco em Oferta)**:
```
[Title emphasizing price/offer]
```

**Recomendacao de teste**: Rodar cada variacao por [X] dias e comparar CTR.

---

## 7. METRICAS E PROXIMOS PASSOS

### 7.1 Metricas para Monitorar

| Metrica | Benchmark Categoria | Meta Inicial |
|---------|--------------------|--------------|
| CTR (Click-Through Rate) | [X]% | [Y]% |
| Conversion Rate | [X]% | [Y]% |
| Session Duration | [X]s | [Y]s |
| Bounce Rate | [X]% | [Y]% |

### 7.2 Calendario de Otimizacao

| Dia | Acao |
|-----|------|
| Dia 1-7 | Publicar e coletar dados iniciais |
| Dia 8 | Analisar CTR, ajustar titulo se <[X]% |
| Dia 15 | Analisar conversao, ajustar bullets se <[X]% |
| Dia 30 | Review completo, considerar teste A/B |
| Dia 60 | Otimizacao baseada em reviews recebidos |
| Dia 90 | Re-analise competitiva (usar QW1) |

### 7.3 Sinais de Alerta

**Quando reescrever copy**:
- [ ] CTR abaixo de [X]% apos 7 dias
- [ ] Conversao abaixo de [X]% apos 14 dias
- [ ] Aumento de perguntas sobre especificacoes basicas
- [ ] Reviews mencionando "produto diferente do anunciado"
- [ ] Concorrente principal mudou posicionamento

---

## 8. ARQUIVO DE CONHECIMENTO

### 8.1 Padroes Extraidos Desta Categoria

```markdown
# PADROES DE COPY: [Category Name]

## Estrutura de Titulo Vencedora
[Pattern extracted from this analysis]

## Bullets que Convertem
[Pattern extracted]

## Keywords Essenciais
[List]

## Claims Permitidos
[List]

## Claims Proibidos
[List]

## Tom de Voz Esperado
[Description]

## Atualizado em
[Date]
```

### 8.2 Quick Reference

```markdown
# QUICK REF: [Product Name]

Titulo ML: [title]
Titulo Amazon: [title]
Titulo Shopee: [title]

Top 5 Keywords: [k1], [k2], [k3], [k4], [k5]

Beneficio Principal: [benefit]
Diferencial Principal: [differentiator]

Compliance: [APROVADO/AJUSTES]
```

---

## METADADOS

- **Gerado por**: IA Especializada em Copy E-commerce BR
- **Modelo**: [LLM used]
- **Data**: [Current date]
- **Produto**: [Product name]
- **Categoria**: [Category]
- **Marketplaces**: [List]

---

**IMPORTANTE**: Esta copy e um ATIVO REUTILIZAVEL.
Salve em formato .md e use como base para produtos similares.
Adapte os templates para novos produtos da mesma categoria.

---

# FIM DO PACOTE DE COPY
```

## NOW, PROCESS MY REQUEST

Based on the information I provide below, generate the complete ad copy package
following the exact structure above.

---

**MINHA SOLICITACAO**:

**Produto**: [YOUR PRODUCT NAME AND DESCRIPTION]
**Marca**: [YOUR BRAND]
**Categoria**: [MARKETPLACE CATEGORY]
**Preco**: [PRICE IN R$]
**Especificacoes**: [TECHNICAL SPECIFICATIONS]
**Diferenciais**: [KEY FEATURES AND BENEFITS]
**Publico-alvo**: [TARGET CUSTOMER]
**USP**: [UNIQUE SELLING PROPOSITION]
**Marketplace principal**: [ML/Amazon/Shopee]
**Oferta de frete**: [SHIPPING OFFER]
**Promocoes**: [SPECIAL OFFERS]
**Tipo de categoria**: [regular/saude/cosmetico/eletronico]
**Certificacoes**: [CERTIFICATIONS IF ANY]
```

---

## 6. USAGE INSTRUCTIONS

### Step 1: Gather Information

Before using the prompt, prepare:
- All product specifications
- Clear photos to reference features
- Competitor listings for context (optional, from QW1)
- Brand guidelines if available (from QW3)

### Step 2: Fill the Template

Complete all fields in the request section. Be specific:

```
**Produto**: Fone de Ouvido Bluetooth TWS com Cancelamento de Ruido Ativo
**Marca**: SoundMax
**Categoria**: Eletronicos > Fones de Ouvido > Bluetooth
**Preco**: R$ 299,00
**Especificacoes**:
- Bluetooth 5.3
- ANC (cancelamento ativo de ruido)
- 30h bateria total (case + fone)
- IPX5 resistente a suor
- Drivers de 10mm
- Latencia 60ms (modo gaming)
**Diferenciais**:
- ANC na faixa de preco (concorrentes nao tem)
- Modo gaming com baixa latencia
- 30h de bateria vs 20h da media
**Publico-alvo**: Jovens 18-35 que usam transporte publico e academia
**USP**: Unico fone com ANC real abaixo de R$ 350
**Marketplace principal**: Mercado Livre
**Oferta de frete**: Frete gratis para todo Brasil
**Promocoes**: Parcelamento em ate 12x sem juros
**Tipo de categoria**: eletronico
**Certificacoes**: ANATEL
```

### Step 3: Paste and Generate

Open your LLM and paste the complete prompt with filled information.

### Step 4: Validate Compliance

Before publishing, verify:
1. All claims are safe for your category
2. Required disclaimers are present
3. No trademark violations
4. Specifications are accurate

### Step 5: Publish and Monitor

1. Copy marketplace-specific sections to each platform
2. Set up tracking for CTR and conversion
3. Schedule optimization review (7, 14, 30 days)

---

## 7. COMPLIANCE GUIDELINES

### Categories by Risk Level

#### Low Risk (Produtos Regulares)
- Casa e Decoracao
- Papelaria
- Ferramentas basicas
- Acessorios de moda (sem claims de saude)

**Compliance Focus**: Precisao de especificacoes, garantia legal

#### Medium Risk (Eletronicos)
- Celulares e acessorios
- Informatica
- Audio e video
- Eletrodomesticos

**Compliance Focus**:
- ANATEL (homologacao obrigatoria)
- INMETRO (quando aplicavel)
- Garantia legal (minimo 90 dias)
- Especificacoes precisas de voltagem

**Disclaimers Comuns**:
```
Produto homologado pela ANATEL sob numero [X].
Garantia de 12 meses contra defeitos de fabricacao.
Verifique a voltagem antes da compra.
```

#### High Risk (Saude e Bem-Estar)

**Suplementos Alimentares**:
- ANVISA: Registro ou notificacao obrigatoria
- Proibido: Claims de cura, tratamento, prevencao
- Permitido: Beneficios nutricionais comprovados

**Claims Proibidos**:
- "Cura [doenca]"
- "Trata [condicao]"
- "Previne [problema de saude]"
- "Emagrece X kg"
- "Resultados garantidos"

**Claims Permitidos**:
- "Fonte de [nutriente]"
- "Auxilia no [funcao fisiologica]" (se aprovado ANVISA)
- "Contribui para [beneficio geral]"

**Disclaimers Obrigatorios**:
```
Este produto nao e um medicamento.
Nao substitui uma alimentacao equilibrada.
Gestantes, nutrizes e criancas: consulte um medico.
Registro ANVISA: [numero se aplicavel]
```

#### High Risk (Cosmeticos)
- ANVISA: Registro ou notificacao
- Proibido: Claims de tratamento medico
- Proibido: Resultados permanentes

**Disclaimers**:
```
Cosmetico registrado na ANVISA sob numero [X].
Resultados podem variar de pessoa para pessoa.
Em caso de irritacao, suspender o uso e consultar um dermatologista.
```

### Marketplace-Specific Rules

#### Mercado Livre
- Proibido: Preco em titulo (exceto promocoes autorizadas)
- Proibido: Informacoes de contato
- Proibido: Links externos
- Obrigatorio: Categoria correta

#### Amazon Brasil
- Proibido: Promocoes temporarias no titulo
- Proibido: Avaliacao ou ranking no titulo
- Proibido: Claims de "melhor", "numero 1" sem prova
- Obrigatorio: Marca no inicio do titulo

#### Shopee Brasil
- Permitido: Emojis no titulo (moderacao)
- Proibido: Spam de keywords
- Obrigatorio: Preco real (sem precos inflados)
- Recomendado: Hashtags relevantes

---

## 8. EXAMPLE OUTPUTS

### Example: Suplemento Whey Protein

**Input Summary**:
- Produto: Whey Protein Isolado 900g
- Preco: R$ 149,90
- Categoria: Suplementos > Proteinas

**Output (Abbreviated)**:

```markdown
## 1. TITULOS OTIMIZADOS

### 1.1 Titulo Mercado Livre
```
Whey Protein Isolado 900g Zero Lactose 27g Proteina Dose
```
**Contagem**: 55 caracteres
**Keywords**: whey protein, isolado, zero lactose

### 1.2 Titulo Amazon Brasil
```
GROWTH Whey Protein Isolado 900g - 27g Proteina por Dose - Zero Lactose -
Baixo Carboidrato - Sabor Chocolate
```
**Contagem**: 112 caracteres

### 2.1 Bullets Estilo Amazon

**Bullet 1**:
```
ABSORCAO RAPIDA: 27g de proteina de alta biodisponibilidade por dose, ideal
para consumo pos-treino quando seu corpo mais precisa de nutrientes para
recuperacao e construcao muscular.
```

**Bullet 2**:
```
ZERO DESCONFORTO: Formula zero lactose desenvolvida para quem tem sensibilidade
digestiva, permitindo aproveitar todos os beneficios da proteina sem inchacos
ou desconfortos abdominais.
```

[... continues with full output ...]

### 5. VALIDACAO DE COMPLIANCE

| Claim na Copy | Status | Acao |
|---------------|--------|------|
| "27g proteina por dose" | SAFE | Verificar rotulo |
| "Zero lactose" | SAFE | Laudo laboratorial |
| "Recuperacao muscular" | SAFE | Funcao fisiologica aceita |
| "Mais eficaz que concorrentes" | RISKY | Remover ou ter prova |

**Disclaimers Obrigatorios**:
```
Este produto nao e um medicamento e nao substitui
uma alimentacao equilibrada. Consulte um medico ou
nutricionista antes de iniciar o uso.
```
```

---

## 9. ADVANCED VARIATIONS

### Variation A: Multiple Products (Batch Generation)

```
Preciso de copy para 5 produtos da mesma categoria.
Gere titulos e bullets para cada, mantendo consistencia de marca.

Produtos:
1. [Product 1 specs]
2. [Product 2 specs]
3. [Product 3 specs]
4. [Product 4 specs]
5. [Product 5 specs]
```

### Variation B: Competitor Differentiation Focus

```
Meu principal concorrente e [X]. Gere copy que diferencia especificamente
deles, abordando:
- Pontos fracos deles que sao meus pontos fortes
- Claims que eles usam e eu posso superar
- Keywords que eles nao estao usando
```

### Variation C: Seasonal Campaign

```
Gere versao especial para [Black Friday / Natal / Dia das Maes]:
- Titulo com referencia a data
- Bullets enfatizando urgencia (etica)
- Descricao com CTA de tempo limitado
- Keywords sazonais
```

### Variation D: Brand Voice Integration (with QW3)

```
Minha marca tem as seguintes caracteristicas:
- Arquetipo: [X]
- Tom de voz: [X]
- Seed words: [X, Y, Z]
- Personalidade: [X]

Gere copy que reflete essa identidade em todo o conteudo.
```

---

## 10. TROUBLESHOOTING

### Problem: Copy Sounds Generic

**Solution**: Add more specific details
```
Em vez de: "Garrafa de agua de alta qualidade"
Use: "Garrafa de aco inox 304 com isolamento a vacuo de dupla parede
mantendo bebidas geladas por 24h e quentes por 12h"
```

### Problem: Compliance Flagged Incorrectly

**Solution**: Clarify category and regulations
```
Minha categoria especifica e [X] e as regulamentacoes aplicaveis sao [Y].
Por favor, re-avalie os claims considerando essas regras.
```

### Problem: Keywords Don't Match Marketplace

**Solution**: Specify marketplace search patterns
```
Quando pesquiso "[X]" no Mercado Livre, os resultados mostram [Y].
Ajuste as keywords para refletir como clientes realmente buscam neste marketplace.
```

### Problem: Description Too Long/Short

**Solution**: Specify exact requirements
```
A descricao para ML esta muito curta. Expanda para pelo menos 1500 palavras,
incluindo mais detalhes sobre [X, Y, Z].
```

### Problem: Missing Category-Specific Elements

**Solution**: Add category context
```
Nesta categoria ([X]), os anuncios de sucesso geralmente incluem:
- [Element 1]
- [Element 2]
- [Element 3]

Adicione esses elementos na copy.
```

---

## METADATA

| Field | Value |
|-------|-------|
| ID | QW2_AD_COPY_GENERATION |
| Version | 1.0.0 |
| Created | 2025-11-29 |
| Author | CODEXA Agent System |
| Category | Quick Win Prompt |
| Target User | E-commerce sellers (Brazil) |
| Compatible LLMs | ChatGPT, Claude, Gemini, Llama, Mistral |
| Output Language | Brazilian Portuguese (PT-BR) |
| Estimated Time | 10-20 minutes |
| Lines | ~950 |

---

## INTEGRATION WITH CODEXA

### Workflow Position

```
QW1: Competitive Research
  └─> Output: Market insights, keywords, positioning
        │
        v
QW2: Ad Copy Generation (THIS PROMPT)
  └─> Input: Product info + QW1 insights (optional)
  └─> Output: Complete marketplace listings
        │
        v
QW3: Brand Voice Extraction
  └─> Input: Copy patterns + product identity
  └─> Output: Brand documentation
```

### Using QW1 Output as Input

If you completed QW1 first:
```
Tenho os seguintes insights da minha pesquisa competitiva (QW1):

**Keywords vencedoras**: [from QW1]
**Posicionamento recomendado**: [from QW1]
**Gaps identificados**: [from QW1]
**Preco ideal**: [from QW1]

Use essas informacoes para otimizar a copy.
```

---

## LICENSE

This prompt is part of CODEXA - an open-source system for e-commerce automation.
Use freely. Modify as needed. Share with others.

---

**Built with CODEXA Meta-Construction System**
**"Build the builder, not the instance"**
