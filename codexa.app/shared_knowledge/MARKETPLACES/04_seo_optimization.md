# SEO Optimization - Marketplace Ranking Patterns

**Version**: 1.0.0
**Updated**: 2025-12-05
**Type**: Knowledge Card
**Cross-Reference**: anuncio_agent, pesquisa_agent, marca_agent

---

## OVERVIEW

Each Brazilian marketplace uses proprietary ranking algorithms. This document consolidates known ranking factors, optimization strategies, and best practices for organic visibility.

---

## MERCADO LIVRE SEO

### Ranking Factors (Estimated Weights)

| Factor | Weight | Description |
|--------|--------|-------------|
| **Reputacao do Vendedor** | 15-20% | Seller reputation (verde, amarelo, vermelho) |
| **Qualidade do Anuncio** | 15-20% | Listing completeness, image quality |
| **Historico de Vendas** | 15-20% | Sales velocity, total sales |
| **Relevancia de Keywords** | 10-15% | Title + description keyword match |
| **Mercado Envios/Full** | 10-15% | Fulfillment method bonus |
| **Preco Competitivo** | 10-15% | Price vs category average |
| **Taxa de Conversao** | 5-10% | Views to sales ratio |
| **Tempo de Resposta** | 5-10% | Question response time |

### Keyword Optimization

```
TITLE STRATEGY (60 chars max):
1. Front-load primary keyword
2. Include brand (if recognized)
3. Add 2-3 key attributes
4. Avoid connectors ("de", "para", "com")
5. Target: 7-9 keywords, density 0.70+

FORMULA:
[Primary Keyword] + [Brand] + [Attribute 1] + [Attribute 2] + [Differentiator]

EXAMPLE:
"Fone Bluetooth JBL 5.3 ANC Cancelamento Ruido 40h Bateria"
 ^Primary       ^Brand ^Attr1    ^Attr2        ^Attr3

DESCRIPTION KEYWORDS:
- Repeat primary keyword 2-3x (natural)
- Include longtail variations
- Use synonyms throughout
- Target density: 2-4%
```

### ML-Specific Optimizations

```
HIGH IMPACT:
[x] Mercado Envios Full (highest logistics score)
[x] 8-12 high-quality images
[x] Complete all attributes
[x] Answer questions <24h
[x] Maintain green reputation
[x] Competitive pricing

MEDIUM IMPACT:
[x] Video demonstration
[x] Detailed specifications
[x] Use category-specific attributes
[x] Consistent stock availability

AVOID:
[ ] Empty attributes
[ ] Low-quality images
[ ] Slow response time
[ ] Out-of-stock periods
[ ] Price above category average
```

### ML Algorithm Updates (Known)

| Update | Date | Impact |
|--------|------|--------|
| Full Priority | 2023 | Full listings ranked higher |
| Image Quality | 2024 | Blurry images penalized |
| Response Time | 2024 | <12h response bonus |

---

## SHOPEE SEO

### Ranking Factors (Estimated Weights)

| Factor | Weight | Description |
|--------|--------|-------------|
| **Performance do Vendedor** | 15-20% | Response rate, shipping time |
| **Participacao em Campanhas** | 15-20% | Flash Sales, vouchers, ads |
| **Qualidade das Imagens** | 10-15% | Image count, quality |
| **Preco + Frete** | 15-20% | Total cost competitiveness |
| **Taxa de Conversao** | 10-15% | Click to purchase ratio |
| **Avaliacoes** | 10-15% | Rating (4.8+ ideal) |
| **Recencia** | 5-10% | Recent activity bonus |

### Keyword Optimization

```
TITLE STRATEGY (120 chars max):
1. Primary keyword first
2. Add 1-2 emojis (visibility boost)
3. Include promo hooks ("Oferta", "Promocao")
4. Mobile-first: key info in first 50 chars
5. Target: 8-12 keywords

FORMULA:
[Emoji] + [Primary Keyword] + [Promo Hook] + [Attributes] + [Emoji]

EXAMPLE:
"[fire]Fone Bluetooth ANC Cancelamento Ruido Ativo 40h Bateria Frete Gratis[headphones]"

DESCRIPTION KEYWORDS:
- Use emoji bullets for scanability
- Short paragraphs (mobile)
- Highlight promotions
- Include shipping info
```

### Shopee-Specific Optimizations

```
HIGH IMPACT:
[x] Participate in Flash Sales
[x] Use Shopee Ads
[x] 9 images (max out)
[x] Add video (9:16 vertical)
[x] Offer vouchers/discounts
[x] Response time <12h
[x] Maintain rating >4.8

MEDIUM IMPACT:
[x] Use Shopee Garantia
[x] Cross-list related products
[x] Regular price updates
[x] Bundle offerings

SHOPEE LIVE:
- Live commerce boosts visibility
- Products shown in live rank higher
- Engagement during live helps algorithm
```

### Shopee Algorithm Patterns

```
KNOWN BEHAVIORS:
- New listings get initial boost (7-14 days)
- Price drops trigger visibility increase
- Campaign participation = significant boost
- Consistent sales velocity matters more than total
- Mobile optimization critical (90%+ mobile users)

PENALTIES:
- Rating drops below 4.5
- Cancellation rate >5%
- Late shipping rate >5%
- Response time >24h
```

---

## AMAZON BRASIL SEO

### A9/A10 Algorithm Factors (Estimated Weights)

| Factor | Weight | Description |
|--------|--------|-------------|
| **Taxa de Conversao** | 25-30% | Sales per view (most important) |
| **Historico de Vendas** | 20-25% | Sales rank, velocity |
| **Preco** | 10-15% | Competitive pricing |
| **Disponibilidade** | 10-15% | Stock consistency, FBA |
| **Reviews/Ratings** | 15-20% | Quantity and quality |
| **Relevancia (Keywords)** | 10-15% | Title, bullets, backend |
| **Completude do Listing** | 5-10% | All fields filled |

### Keyword Optimization

```
TITLE STRATEGY (200 chars max):
1. Brand + Model first (Amazon Style Guide)
2. Key features in middle
3. Specifications at end
4. NO promotional language
5. Target: 10-15 keywords

FORMAT:
[Brand] [Model/Line] [Product Type] [Key Feature 1] [Key Feature 2], [Spec 1], [Spec 2], [Color/Size]

EXAMPLE:
"JBL Tune 760NC Fone de Ouvido Bluetooth Over-Ear com Cancelamento de Ruido Ativo, Bateria 35 Horas, Conexao Multiponto, Preto"

BULLET POINTS (5 x 500 chars):
- One benefit per bullet
- Front-load with benefit name
- Include technical specs naturally
- Address common objections
- No promotional text

BACKEND KEYWORDS (250 bytes):
- Synonyms not in title/bullets
- Common misspellings
- Regional variations
- Related search terms
- NO brand names or ASINs
```

### Amazon-Specific Optimizations

```
HIGH IMPACT:
[x] FBA (Fulfillment by Amazon)
[x] A+ Content (Brand Registry)
[x] 7-9 images (main STRICT white)
[x] 5 bullet points always
[x] Backend keywords optimized
[x] Competitive pricing
[x] Reviews >4.0, quantity 50+

MEDIUM IMPACT:
[x] Video demonstration
[x] Subscribe & Save eligible
[x] Amazon Vine enrollment
[x] Virtual bundles
[x] Variation listings

A+ CONTENT STRATEGY:
- Comparison table (vs your other products)
- Brand story module
- Feature-focused images
- Lifestyle imagery
- Increases conversion 5-10%
```

### Amazon Algorithm Notes

```
A10 (CURRENT) vs A9:
- More weight on external traffic
- Click-through rate matters more
- Brand registry benefits increased
- Organic ranking tied to PPC performance

FLYWHEEL EFFECT:
Sales → Better Rank → More Visibility → More Sales
      ↑                                        |
      +----------------------------------------+

LAUNCH STRATEGY:
1. Optimize listing completely
2. Run PPC (Amazon Ads) aggressively
3. Drive external traffic (social, email)
4. Request reviews (Amazon program)
5. Monitor and adjust keywords
```

---

## MAGAZINE LUIZA SEO

### Ranking Factors (Estimated Weights)

| Factor | Weight | Description |
|--------|--------|-------------|
| **Completude do Cadastro** | 20-25% | All fields filled, EAN valid |
| **Ficha Tecnica** | 15-20% | Technical specifications complete |
| **Qualidade das Imagens** | 10-15% | Quantity, quality, compliance |
| **Preco Competitivo** | 15-20% | Market positioning |
| **Disponibilidade** | 10-15% | Stock consistency |
| **Avaliacoes** | 10-15% | Rating and review count |
| **EAN Validado** | 10-15% | Correct product identification |

### Keyword Optimization

```
TITLE STRATEGY (256 chars max):
1. Marca + Modelo format (required)
2. Include all variant attributes
3. Technical specs in title
4. No promotional language

FORMAT:
[Categoria] [Marca] [Modelo] [Caracteristica 1] [Caracteristica 2] - [Especificacao]

EXAMPLE:
"Fone de Ouvido Bluetooth JBL Tune 760NC Over-Ear Cancelamento de Ruido Ativo Preto - Bateria 35h"

DESCRIPTION:
- Detailed technical specifications
- Complete attribute filling
- Warranty information
- Voltage (electronics)
```

### Magalu-Specific Optimizations

```
HIGH IMPACT:
[x] Valid EAN code (MANDATORY)
[x] Complete NCM classification
[x] 100% attribute completion
[x] 10-15 high-quality images
[x] Detailed ficha tecnica
[x] Warranty information clear

MEDIUM IMPACT:
[x] Video demonstration
[x] Packaging dimensions accurate
[x] Related products linked
[x] Competitive pricing

MANDATORY FOR ELECTRONICS:
[x] Voltage specification
[x] INMETRO certification
[x] ANATEL homologation (wireless)
[x] Fiscal documentation
```

---

## CROSS-PLATFORM SEO STRATEGY

### Keyword Research Workflow

```
STEP 1: Seed Keywords
- Product name variations
- Brand + model
- Category terms
- Use case terms

STEP 2: Expand per Platform
- ML: Competitor title analysis
- Shopee: Trending searches
- Amazon: Brand Analytics (if available)
- Magalu: Category browse

STEP 3: Prioritize
- Search volume (high priority)
- Competition level (medium = ideal)
- Relevance to product (mandatory)
- Platform-specific trends

STEP 4: Allocate
- Title: Primary + Secondary keywords
- Description: Longtails + Synonyms
- Backend: Remaining valuable terms
```

### Multi-Platform Keyword Distribution

```
PRIMARY KEYWORD: "Fone Bluetooth ANC"
|
+-- ML Title (60): "Fone Bluetooth ANC 5.3 Cancelamento Ruido 40h Bateria IPX7"
|
+-- Shopee Title (120): "[emoji]Fone Bluetooth ANC Cancelamento Ruido Ativo 40h Bateria Frete Gratis Promo[emoji]"
|
+-- Amazon Title (200): "Marca Modelo Fone de Ouvido Bluetooth 5.3 Over-Ear com Cancelamento de Ruido Ativo ANC, Bateria 40 Horas, Resistente a Agua IPX7, Preto"
|
+-- Magalu Title (256): "Fone de Ouvido Bluetooth Marca Modelo 5.3 Over-Ear com Cancelamento de Ruido Ativo ANC Preto - Bateria 40h IPX7"
```

### Optimization Checklist

```markdown
## PRE-LAUNCH
[ ] Keyword research completed (all platforms)
[ ] Title optimized per platform limits
[ ] Description written (adapt per platform)
[ ] Images prepared (9+ high-quality)
[ ] Main image meets strictest requirement (Amazon white)
[ ] Video created (vertical for Shopee)
[ ] Attributes mapped per platform

## LAUNCH
[ ] Listings created on all platforms
[ ] Pricing aligned (consider fees)
[ ] Stock synchronized
[ ] Fulfillment method selected

## POST-LAUNCH (Week 1-4)
[ ] Monitor search rank positions
[ ] Track conversion rates
[ ] Analyze competitor changes
[ ] A/B test titles (if platform allows)
[ ] Request initial reviews

## ONGOING
[ ] Weekly rank monitoring
[ ] Monthly keyword refresh
[ ] Quarterly competitive analysis
[ ] Algorithm update adaptation
```

---

## SEO METRICS & KPIs

### Key Metrics by Platform

| Metric | ML | Shopee | Amazon | Magalu |
|--------|-----|--------|--------|--------|
| **Primary KPI** | Posicao na busca | Vendas/dia | BSR (Best Seller Rank) | Posicao categoria |
| **Click-Through** | Visitas/Impressoes | CTR | CTR | CTR |
| **Conversion** | Vendas/Visitas | CR | Unit Session % | CR |
| **Reviews** | Avaliacoes | Rating | Reviews + Rating | Avaliacoes |

### Benchmark Targets

| Metric | Poor | Average | Good | Excellent |
|--------|------|---------|------|-----------|
| **CTR** | <1% | 1-3% | 3-5% | >5% |
| **Conversion** | <2% | 2-5% | 5-10% | >10% |
| **Rating** | <4.0 | 4.0-4.5 | 4.5-4.8 | >4.8 |
| **Review Velocity** | <1/week | 1-3/week | 3-5/week | >5/week |

---

## ALGORITHM UPDATE MONITORING

### Sources to Monitor

| Platform | Official Source | Community Source |
|----------|-----------------|------------------|
| Mercado Livre | Partner Center Updates | Comunidade ML |
| Shopee | Seller Centre | Grupos Facebook |
| Amazon | Seller Central News | Amazon Seller Forums |
| Magalu | Portal do Parceiro | Grupos WhatsApp |

### Update Response Protocol

```
1. DETECT: Monitor announcement channels
2. ANALYZE: Understand ranking impact
3. ADAPT: Adjust listings within 48-72h
4. TEST: Monitor ranking changes
5. OPTIMIZE: Fine-tune based on results
```

---

## METADATA

```json
{
  "knowledge_type": "seo_optimization",
  "platforms_covered": ["mercadolivre", "shopee", "amazon", "magalu"],
  "last_verified": "2025-12-05",
  "update_frequency": "bi-monthly",
  "confidence_level": "medium-high",
  "note": "Algorithm weights are estimates based on seller community observations and official hints. Actual weights are proprietary."
}
```

---

**Status**: Active
**Next Review**: 2026-02-05
