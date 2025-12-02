# PHOTO AGENT | Documento de Referencia para Video Tutorial

**Proposito**: Fonte de conhecimento para NotebookLM gerar video tutorial
**Agente**: photo_agent v2.5.0
**Duracao do Video**: 3-5 minutos

---

## O QUE E O PHOTO AGENT

O Photo Agent e um diretor de fotografia especializado em e-commerce. Ele gera prompts profissionais para IAs de imagem (Midjourney, DALL-E, Flux, Imagen) que criam fotos de produto de alta qualidade.

**Transformacao**: Descricao do produto → 2 prompts de fotografia (Grid 3x3 + 9 individuais)
**Duracao da execucao**: 10-20 minutos (full) / 3-5 minutos (quick)
**Output**: Prompts em markdown prontos para copiar

---

## COMO O USUARIO INICIA

O usuario digita uma frase simples:

```
"Quero foto de [URL do produto]"
```

ou

```
"Quero foto de garrafa termica inox preta 500ml"
```

O agente NAO conversa. Ele EXECUTA o workflow completo automaticamente.

---

## O QUE O AGENTE ENTREGA

### PROMPT 1: Grid 3x3 Master
- 9 cenas em 1 unica imagem
- Layout grid profissional
- 500-800 palavras
- Ideal para visao geral do produto

### PROMPT 2: 9 Prompts Individuais
- 1 prompt por cena (180-300 palavras cada)
- Maior controle criativo
- Variacoes de seed para multiplas opcoes

### Formato do Prompt
```
{user_image} {seed:[RANDOM]}
[DESCRICAO TECNICA DA CENA]
Camera: [ESPECIFICACOES]
Lighting: [TIPO E DIRECAO]
Composition: [REGRA COMPOSITIVA]
Background: [COR/AMBIENTE]
Mood: [EMOCAO/GATILHO PNL]
```

---

## AS 9 CENAS PADRAO

| Cena | Nome | Proposito | Background |
|------|------|-----------|------------|
| 1 | Pack Shot | Produto limpo para catalogo | Branco #FFFFFF |
| 2 | Hero Shot | Impacto visual, destaque | Gradiente/Cor |
| 3 | Detail Shot | Textura, material, acabamento | Neutro |
| 4 | Scale Shot | Tamanho real, proporcao | Contextual |
| 5 | Lifestyle | Uso real, pessoa interagindo | Ambiente |
| 6 | In-Context | Produto no ambiente de uso | Ambiente real |
| 7 | Flat Lay | Vista superior, composicao | Cor solida |
| 8 | Group Shot | Variantes, cores, tamanhos | Neutro |
| 9 | Clean Shot | Marketplace compliant | Branco #FFFFFF |

**IMPORTANTE**: Cenas 1 e 9 SEMPRE com fundo branco puro (#FFFFFF) para compliance de marketplace.

---

## O WORKFLOW COMPLETO

### Fase 1: Scene Planning
- Analisa produto e categoria
- Define 9 cenas otimizadas
- Mapeia gatilhos PNL por cena

### Fase 2: Technical Setup
- Define camera specs (focal, aperture, ISO)
- Escolhe lighting setup (5 opcoes profissionais)
- Define composicao (rule of thirds, golden ratio, centered)

### Fase 3: Prompt Generation
- Gera PROMPT 1 (Grid 3x3)
- Gera PROMPT 2 (9 individuais)
- Adiciona {user_image} {seed:[RANDOM]}
- Inclui [OPEN_VARIABLES] para customizacao

### Fase 4: Brand Validation (opcional)
- Verifica alinhamento com cores da marca
- Ajusta mood para arquetipo da marca
- Valida consistencia visual

### Fase 5: Output Assembly
- Formata em markdown copiavel
- Adiciona comandos de geracao
- Valida 13 criterios de qualidade

---

## ESPECIFICACOES TECNICAS

### Camera Profiles
```
STUDIO: 85mm f/2.8, ISO 100, 1/125s - Retratos de produto
MACRO: 100mm f/4, ISO 200, 1/60s - Detalhes e texturas
WIDE: 35mm f/5.6, ISO 400, 1/250s - Ambientes e contexto
LIFESTYLE: 50mm f/1.8, ISO 800, 1/500s - Pessoas e acao
```

### Lighting Setups
```
SOFTBOX: Luz suave, difusa, sem sombras duras
RING LIGHT: Iluminacao uniforme, ideal para pack shots
RIM LIGHT: Contorno do produto, separacao do fundo
NATURAL: Luz de janela, look organico
DRAMATIC: Alto contraste, sombras definidas
```

### Composition Rules
```
RULE OF THIRDS: Produto em intersecao de linhas
CENTERED: Produto centralizado, simetria
GOLDEN RATIO: Proporcao aurea, elegancia
LEADING LINES: Linhas guiam olhar ao produto
NEGATIVE SPACE: Espaco vazio intencional
```

---

## GATILHOS PNL POR CENA

| Cena | Gatilho | Emocao |
|------|---------|--------|
| 1 Pack Shot | Clareza | Confianca |
| 2 Hero Shot | Desejo | Aspiracao |
| 3 Detail | Qualidade | Seguranca |
| 4 Scale | Praticidade | Racional |
| 5 Lifestyle | Pertencimento | Social |
| 6 In-Context | Projecao | Imaginacao |
| 7 Flat Lay | Organizacao | Controle |
| 8 Group | Escolha | Liberdade |
| 9 Clean | Profissionalismo | Credibilidade |

---

## EXEMPLO DE OUTPUT

**Input**:
```
Quero foto de garrafa termica inox preta 500ml
```

**Output (Cena 5 - Lifestyle)**:
```
{user_image} {seed:42}

Professional product photography of black stainless steel
thermal bottle 500ml in lifestyle setting.

Scene: [YOUNG_PROFESSIONAL/ATHLETE/STUDENT] using the bottle
during [MORNING_ROUTINE/WORKOUT/WORK_BREAK] in
[MODERN_KITCHEN/GYM/OFFICE_SPACE].

Camera: Canon EOS R5, 50mm f/1.8 lens, ISO 800, 1/500s
Lighting: Natural window light with subtle fill,
golden hour warmth, soft shadows
Composition: Rule of thirds, subject on left third,
product prominent in hand
Background: [MINIMALIST_INTERIOR/URBAN_BACKDROP/NATURE_BLUR]
Mood: Aspirational, healthy lifestyle, premium quality

Style: Editorial photography, lifestyle brand aesthetic,
warm color grading, shallow depth of field on background

--ar 4:5 --v 6 --style raw
```

---

## POR QUE USAR O PHOTO AGENT

1. **Economia**: Prompts profissionais vs contratar fotografo
2. **Consistencia**: 9 cenas padronizadas para qualquer produto
3. **Marketplace Ready**: Cenas 1+9 com fundo branco #FFFFFF
4. **Flexibilidade**: Funciona em Midjourney, DALL-E, Flux, Imagen
5. **PNL Integrado**: Cada cena com gatilho emocional

---

## CONEXAO COM OUTROS AGENTES

```
PESQUISA AGENT
     |
     | research_notes.md
     v
ANUNCIO AGENT
     |
     | anuncio.md + brand_profile
     v
PHOTO AGENT ← Voce esta aqui
     |
     | 2 prompts (Grid + 9 individuais)
     v
IA DE IMAGEM → Midjourney, DALL-E, Flux, Imagen
```

O Photo Agent usa informacoes do Anuncio Agent (se disponivel) para alinhar as fotos com a copy.

---

## MODOS DE EXECUCAO

| Modo | Duracao | Cenas | Quando usar |
|------|---------|-------|-------------|
| **Full** | 10-20min | 9 | Lancamento de produto |
| **Quick** | 3-5min | 3 | Hero + Lifestyle + Pack |
| **Single** | 1-2min | 1 | Cena especifica |

---

## COMO USAR O OUTPUT

1. Copie o prompt gerado
2. Abra sua IA de imagem preferida (Midjourney, DALL-E, Flux)
3. Cole o prompt
4. Faca upload da foto real do seu produto (se a IA suportar)
5. Gere a imagem
6. Use {seed:[NUMERO]} para variacoes consistentes

---

## MENSAGEM CHAVE PARA O VIDEO

"O Photo Agent transforma qualquer produto em 9 fotos profissionais. Voce digita uma frase, ele gera prompts tecnicos com camera, iluminacao, composicao e gatilhos emocionais. Use em Midjourney, DALL-E ou qualquer IA de imagem. Pack shot, lifestyle, detalhes - tudo pronto para marketplace."

---

**Arquivo fonte**: agentes/photo_agent/PRIME.md
**Versao**: 2.5.0
