# Marketplace Image Requirements

**Version**: 1.0.0 | **Updated**: 2025-12-05 | **Region**: Brazil (BR)

---

## OVERVIEW

Cada marketplace tem requisitos especificos para imagens de produto. Este guia cobre os principais marketplaces brasileiros e internacionais.

---

## MERCADO LIVRE

### Imagem Principal (Obrigatoria)

| Requisito | Especificacao |
|-----------|---------------|
| Fundo | Branco puro (#FFFFFF) |
| Dimensao Minima | 500 x 500 px |
| Dimensao Recomendada | 1200 x 1200 px |
| Aspecto | 1:1 (quadrado) |
| Formato | JPG, PNG |
| Tamanho Max | 10 MB |
| Ocupacao | Produto ocupa 85%+ do frame |

### Restricoes

```
PROIBIDO:
- Texto sobreposto (preco, descricao)
- Logos e marcas d'agua
- Bordas e molduras
- Colagens de multiplas imagens
- Fundos coloridos ou com textura
- Sombras pesadas
- Reflexos
- Elementos promocionais
- Pessoas (exceto vestuario)
```

### Imagens Secundarias (Galeria)

```
Quantidade: Ate 10 imagens
Permitido:
- Lifestyle shots
- Detalhes do produto
- Diferentes angulos
- Produto em uso
- Comparacao de tamanho

Ainda proibido:
- Texto promocional
- Precos
- Informacoes de contato
```

### Prompt Template (ML Main)

```
Professional product photograph of {{PRODUCT}}, perfectly centered
in frame, pure white seamless studio backdrop #FFFFFF, soft diffused
lighting eliminating all shadows, product occupies 85% of frame,
50mm lens f/8 for complete sharpness, no text no logo no watermark,
isolated product, Mercado Livre marketplace compliant, commercial
e-commerce quality
```

---

## SHOPEE

### Imagem Principal

| Requisito | Especificacao |
|-----------|---------------|
| Fundo | Branco preferido (nao obrigatorio) |
| Dimensao Minima | 500 x 500 px |
| Dimensao Recomendada | 800 x 800 px ou maior |
| Aspecto | 1:1 (quadrado) |
| Formato | JPG, PNG |
| Tamanho Max | 2 MB |

### Mais Flexivel que ML

```
PERMITIDO:
- Fundos coloridos (desde que clean)
- Lifestyle shots como principal
- Multiplos angulos em colagem
- Infograficos (com restricoes)

PROIBIDO:
- Informacoes de contato
- Precos e promocoes
- Watermarks intrusivos
- Conteudo ofensivo
```

### Imagens de Galeria

```
Quantidade: Ate 9 imagens
Recomendado:
- 1a: Pack shot (fundo branco/limpo)
- 2a-4a: Diferentes angulos
- 5a-7a: Detalhes e features
- 8a-9a: Lifestyle/uso
```

### Prompt Template (Shopee)

```
Product photograph of {{PRODUCT}}, clean composition, white or
light neutral background, engaging angle showing product features,
commercial quality suitable for Shopee marketplace, sharp focus,
professional lighting, no contact information or prices visible
```

---

## AMAZON BRASIL

### Imagem Principal (MAIN)

| Requisito | Especificacao |
|-----------|---------------|
| Fundo | Branco puro RGB (255,255,255) |
| Dimensao Minima | 1000 px no lado maior |
| Dimensao Recomendada | 2000 x 2000 px |
| Aspecto | 1:1 preferido |
| Formato | JPEG, PNG, GIF, TIFF |
| Tamanho Max | 10 MB |
| Ocupacao | Produto ocupa 85%+ do frame |

### Amazon Strict Requirements

```
OBRIGATORIO:
- Produto real (nao ilustracao)
- Fundo branco puro
- Sem texto, logos, watermarks
- Produto inteiro visivel
- Cores precisas

PROIBIDO:
- Embalagem (exceto se relevante)
- Props (exceto se parte do produto)
- Multiplos produtos (exceto kit)
- Placeholder images
- Nudez/conteudo adulto
```

### Imagens Secundarias (Variantes)

```
Quantidade: Ate 9 imagens totais
Tipos recomendados:
- MAIN: Pack shot branco (obrigatorio)
- PT01-PT08: Angulos, lifestyle, infograficos

Permitido em secundarias:
- Texto descritivo
- Lifestyle com props
- Infograficos de features
- Comparacoes de tamanho
```

### Prompt Template (Amazon MAIN)

```
Professional Amazon product photograph of {{PRODUCT}}, perfectly
centered, pure white background RGB 255 255 255, product occupies
85 percent of frame, complete product visible, accurate color
representation, no text no graphics no watermarks, professional
studio lighting eliminating shadows, commercial grade photography,
Amazon marketplace compliant
```

---

## MAGALU (MAGAZINE LUIZA)

### Imagem Principal

| Requisito | Especificacao |
|-----------|---------------|
| Fundo | Branco ou neutro |
| Dimensao Minima | 500 x 500 px |
| Dimensao Recomendada | 1000 x 1000 px |
| Aspecto | 1:1 |
| Formato | JPG, PNG |

### Guidelines

```
RECOMENDADO:
- Fundo branco limpo
- Produto em destaque
- Alta qualidade
- Angulos multiplos

PROIBIDO:
- Precos e promocoes
- Informacoes de contato
- Logos de terceiros
- Watermarks intrusivos
```

### Prompt Template (Magalu)

```
Product photograph of {{PRODUCT}}, clean white background,
centered composition, professional lighting, sharp focus,
commercial e-commerce quality, no promotional text,
suitable for Magazine Luiza marketplace listing
```

---

## SHEIN

### Requisitos de Moda

| Requisito | Especificacao |
|-----------|---------------|
| Fundo | Branco ou cinza claro |
| Dimensao | 800 x 1200 px (portrait) |
| Aspecto | 2:3 (vertical) |
| Formato | JPG |

### Fashion-Specific

```
IMAGEM PRINCIPAL:
- Modelo vestindo produto
- Fundo branco/cinza
- Corpo inteiro ou meio corpo
- Pose natural

IMAGENS SECUNDARIAS:
- Detalhes de tecido
- Close-up de acabamento
- Flat lay do produto
- Diferentes angulos
```

### Prompt Template (Shein Fashion)

```
Fashion photograph of model wearing {{PRODUCT}}, full body shot,
white seamless background, natural pose, professional studio
lighting, sharp focus on garment details, e-commerce fashion
photography style, clean minimal aesthetic
```

---

## ALIEXPRESS

### Requisitos

| Requisito | Especificacao |
|-----------|---------------|
| Fundo | Branco preferido |
| Dimensao Minima | 800 x 800 px |
| Dimensao Recomendada | 1000 x 1000 px |
| Formato | JPG, PNG |
| Tamanho Max | 5 MB |

### Flexibilidade

```
PERMITIDO:
- Infograficos com texto
- Colagens comparativas
- Lifestyle shots
- Props contextuais

PROIBIDO:
- Watermarks cobrindo produto
- Informacoes de contato
- Conteudo ofensivo
```

---

## AMERICANAS / SUBMARINO / SHOPTIME (B2W)

### Requisitos Unificados

| Requisito | Especificacao |
|-----------|---------------|
| Fundo | Branco (#FFFFFF) |
| Dimensao Minima | 500 x 500 px |
| Dimensao Ideal | 1500 x 1500 px |
| Aspecto | 1:1 |
| Formato | JPG, PNG |

### Guidelines B2W

```
MAIN IMAGE:
- Fundo branco puro
- Produto centralizado
- Sem texto overlay
- Alta resolucao

GALERIA:
- Angulos variados
- Detalhes
- Lifestyle permitido
- Ate 6 imagens
```

---

## RESUMO COMPARATIVO

| Platform | Bg Color | Min Size | Aspect | Text OK | Max Images |
|----------|----------|----------|--------|---------|------------|
| Mercado Livre | #FFFFFF | 500px | 1:1 | No | 10 |
| Shopee | White/Color | 500px | 1:1 | Limited | 9 |
| Amazon BR | RGB 255 | 1000px | 1:1 | No (main) | 9 |
| Magalu | White | 500px | 1:1 | No | 6 |
| Shein | White/Gray | 800px | 2:3 | No | 8 |
| AliExpress | White | 800px | 1:1 | Yes | 6 |
| B2W | #FFFFFF | 500px | 1:1 | No | 6 |

---

## PROMPT UNIVERSAL (ALL MARKETPLACES)

### Main Image (Safe for All)

```
Professional commercial product photograph of {{PRODUCT}},
perfectly centered in frame, pure white seamless studio backdrop
#FFFFFF, soft diffused multi-source lighting creating even
illumination with no shadows, product occupies 85 percent of
frame, complete product visible without cropping, 50mm lens at
f/8 for complete depth of field, accurate color representation,
no text no logos no watermarks no graphics, high resolution
commercial e-commerce photography, marketplace compliant,
isolated product presentation
```

### Lifestyle/Secondary (Where Allowed)

```
Lifestyle photograph of {{PRODUCT}} in {{ENVIRONMENT}},
authentic natural setting, product clearly visible and in focus,
{{LIGHTING_TYPE}} creating inviting atmosphere, 85mm lens with
shallow depth of field, editorial quality, suitable for
e-commerce gallery, no promotional text or pricing visible
```

---

## CHECKLIST PRE-SUBMISSAO

### Imagem Principal

- [ ] Fundo branco puro (#FFFFFF / RGB 255,255,255)
- [ ] Produto centralizado
- [ ] Produto ocupa 85%+ do frame
- [ ] Produto completo visivel (nao cortado)
- [ ] Sem texto overlay
- [ ] Sem logos ou watermarks
- [ ] Sem sombras pesadas
- [ ] Resolucao minima atendida
- [ ] Aspecto correto (1:1)
- [ ] Formato correto (JPG/PNG)
- [ ] Tamanho do arquivo OK

### Imagens de Galeria

- [ ] Angulos variados incluidos
- [ ] Detalhes/close-ups
- [ ] Lifestyle (se permitido)
- [ ] Informacao de escala
- [ ] Consistencia visual
- [ ] Quantidade maxima respeitada

---

## DICAS DE OTIMIZACAO

### Para Todos os Marketplaces

1. **Comece com ML/Amazon** - mais restritivos
2. **Master image em 2000x2000** - downsize conforme necessario
3. **Salve originais** - para diferentes crops
4. **Nomenclatura clara** - MAIN_product.jpg, ANGLE_45.jpg
5. **Batch process** - mesmas configs para consistencia

### Erros Comuns a Evitar

```
1. Fundo off-white (parece sujo)
2. Produto muito pequeno no frame
3. Sombras no fundo
4. Bordas do produto cortadas
5. Reflexos indesejados
6. Cores incorretas
7. Texto promocional escondido
```

---

## REFERENCIAS

- Mercado Livre: https://www.mercadolivre.com.br/ajuda/requisitos-fotos
- Amazon: https://sellercentral.amazon.com.br/gp/help/1881
- Shopee: https://seller.shopee.com.br/edu/article/5053
- Shein: Partner guidelines (internal)

---

**Version**: 1.0.0 | **Status**: Production Ready
