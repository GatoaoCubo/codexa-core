# Platform Specifications - Technical Requirements by Marketplace

**Version**: 1.0.0
**Updated**: 2025-12-05
**Type**: Knowledge Card
**Cross-Reference**: anuncio_agent, pesquisa_agent, marca_agent

---

## QUICK REFERENCE TABLE

### Character Limits

| Element | Mercado Livre | Shopee | Amazon | Magalu |
|---------|---------------|--------|--------|--------|
| **Title Min** | 10 | 10 | 10 | 10 |
| **Title Max** | 60 | 120 | 200 | 256 |
| **Title Optimal** | 58-60 | 80-120 | 150-200 | 150-200 |
| **Description Min** | 100 | 100 | 100 | 200 |
| **Description Max** | 50,000 | 3,000 | 2,000 | 4,000 |
| **Description Optimal** | 3,000-5,000 | 1,500-2,500 | 1,500-2,000 | 2,500-3,500 |
| **Bullet Points** | N/A | N/A | 5 x 500 chars | N/A |

### Image Specifications

| Spec | Mercado Livre | Shopee | Amazon | Magalu |
|------|---------------|--------|--------|--------|
| **Min Images** | 1 | 3 | 1 | 1 |
| **Max Images** | 12 | 9 | 9 | 20 |
| **Optimal** | 8-12 | 9 | 7-9 | 10-15 |
| **Min Size** | 800x800px | 800x800px | 1000x1000px | 1000x1000px |
| **Optimal Size** | 1200x1200px | 1000x1000px | 1500x1500px | 1500x1500px |
| **Max File Size** | 10MB | 5MB | 10MB | 5MB |
| **Format** | JPG, PNG | JPG, PNG | JPG, PNG | JPG, PNG |
| **Background (Main)** | White/Neutral | White/Lifestyle | White ONLY (RGB 255,255,255) | White |

### Video Specifications

| Spec | Mercado Livre | Shopee | Amazon | Magalu |
|------|---------------|--------|--------|--------|
| **Max Videos** | 1 | 1 | 1 | 1 |
| **Max Duration** | 60s | 60s | 120s | 120s |
| **Format** | MP4 | MP4 | MP4 | MP4 |
| **Max Size** | 100MB | 30MB | 500MB | 50MB |
| **Aspect Ratio** | 16:9 or 1:1 | 9:16 (vertical) | 16:9 or 1:1 | 16:9 or 1:1 |

---

## MERCADO LIVRE - DETAILED SPECS

### Title

```
LIMITS:
- Minimum: 10 characters
- Maximum: 60 characters (STRICT)
- Optimal: 58-60 characters (max SEO)

ALLOWED:
- Letters (a-z, A-Z, acentos)
- Numbers (0-9)
- Spaces
- Hyphens (-)
- Commas (,)

PROHIBITED:
- Emojis
- Special symbols (!@#$%^&*)
- HTML tags
- ALL CAPS words (excessive)
- "Mercado Livre" or "ML"
- Contact information
- Promotional text ("Frete gratis")

BEST PRACTICES:
- Front-load keywords (most important first)
- Use full product name + key attributes
- Include brand (if authorized)
- Avoid connectors ("de", "para", "com")

EXAMPLE (Good):
"Fone Bluetooth 5.3 ANC Cancelamento Ruido 40h Bateria IPX7"
(59 chars, 8 keywords, density 0.80)

EXAMPLE (Bad):
"O Melhor Fone de Ouvido Bluetooth do Brasil com Frete Gratis"
(61 chars, OVER LIMIT, promotional, superlative)
```

### Description

```
LIMITS:
- Minimum: 100 characters
- Maximum: 50,000 characters
- Optimal: 3,000-5,000 characters

HTML ALLOWED:
- <b> / <strong>
- <i> / <em>
- <u>
- <br>
- <p>

HTML PROHIBITED:
- <script>
- <iframe>
- <style>
- <img> (use official image upload)
- <a href> (external links)
- JavaScript

STRUCTURE RECOMMENDED:
1. Hook (benefit-focused opening)
2. Key benefits (3-5 paragraphs)
3. Technical specifications (bullet list)
4. Included items
5. Warranty information
6. Compliance (ANVISA/INMETRO if applicable)

PROHIBITED CONTENT:
- External links (websites, social media)
- Contact information (phone, email, WhatsApp)
- Competitor comparisons (direct)
- Unsubstantiated claims
- "Loja Oficial" without verification
```

### Images

```
QUANTITY:
- Minimum: 1
- Maximum: 12
- Optimal: 8-12

DIMENSIONS:
- Minimum: 800x800 pixels
- Recommended: 1200x1200 pixels or higher
- Aspect ratio: 1:1 (square)

FILE:
- Format: JPG, PNG
- Max size: 10MB per image
- Color mode: RGB

MAIN IMAGE (First):
- Background: White or neutral
- Product: Must occupy 75-90% of frame
- No text overlays
- No promotional badges
- No watermarks
- Product must be complete and visible

SECONDARY IMAGES (2-12):
- Detail shots (close-ups)
- Multiple angles
- Size comparison
- Lifestyle/usage context
- Packaging (optional)
- Infographics (specs)

PROHIBITED:
- Text over product (excessive)
- Other platform watermarks
- Contact information
- QR codes
- Blurry/low quality images
```

---

## SHOPEE - DETAILED SPECS

### Title

```
LIMITS:
- Minimum: 10 characters
- Maximum: 120 characters
- Optimal: 80-120 characters (mobile-optimized)

ALLOWED:
- Letters, numbers, spaces
- Some emojis (1-2 MAX)
- Basic symbols

PROHIBITED:
- HTML
- Spam keywords (repetition >2x)
- ALL CAPS (excessive)
- "Shopee" in title
- False claims

BEST PRACTICES:
- Mobile-first (visible in first 40-50 chars)
- Include 1-2 emojis for visibility
- Promo hooks work well ("Oferta", "Promocao")
- Regional terms accepted

EXAMPLE (Good):
"Fone Bluetooth ANC [emoji]Cancelamento Ruido Ativo 40h Bateria Entrega Rapida"
(78 chars, mobile-friendly, promo hook)

EXAMPLE (Bad):
"FONE FONE FONE BLUETOOTH BLUETOOTH BLUETOOTH MELHOR PRECO"
(Spam, ALL CAPS, keyword stuffing)
```

### Description

```
LIMITS:
- Minimum: 100 characters
- Maximum: 3,000 characters
- Optimal: 1,500-2,500 characters

HTML ALLOWED:
- NONE (plain text only)

STRUCTURE (Mobile-Optimized):
1. Visual hook + emoji
2. Promo information (discount, frete, parcelas)
3. Key benefits (short paragraphs)
4. Specs (bullet format with emojis: checkmark)
5. Social proof (if available)

BEST PRACTICES:
- Short paragraphs (2-3 lines max)
- Use emojis as bullet points
- Highlight promotions
- Include shipping information
- Mobile-first formatting

EXAMPLE FORMAT:
"[fire emoji] OFERTA IMPERDIVEL! [fire emoji]

[check emoji] Cancelamento de Ruido Ativo (ANC)
[check emoji] 40 horas de bateria
[check emoji] Bluetooth 5.3 conexao estavel
[check emoji] Resistente a agua IPX7

FRETE GRATIS para todo Brasil!
Parcele em ate 12x sem juros

[star emoji] +500 clientes satisfeitos!"
```

### Images

```
QUANTITY:
- Minimum: 3 (MANDATORY)
- Maximum: 9
- Optimal: 9 (always max out)

DIMENSIONS:
- Minimum: 800x800 pixels
- Recommended: 1000x1000 pixels
- Aspect ratio: 1:1 (square)

FILE:
- Format: JPG, PNG
- Max size: 5MB per image
- Color mode: RGB

MAIN IMAGE:
- Product clearly visible
- White or lifestyle background
- No text overlay (minimal allowed)

VIDEO:
- Recommended: 15-30 seconds
- Aspect ratio: 9:16 (VERTICAL for mobile)
- Increases conversion ~30%

PROHIBITED:
- Text overlay (excessive)
- Other seller images
- Other platform watermarks
- Low quality/blurry
```

---

## AMAZON BRASIL - DETAILED SPECS

### Title

```
LIMITS:
- Minimum: 10 characters
- Maximum: 200 characters
- Optimal: 150-200 characters (max SEO)

FORMAT REQUIRED:
[Brand] + [Model] + [Key Features] + [Specifications]

ALLOWED:
- Letters, numbers, spaces
- Hyphens, commas
- Parentheses (for specs)

PROHIBITED:
- Emojis
- ALL CAPS
- Promotional text ("Desconto", "Frete Gratis")
- "Amazon" or "Prime"
- Seller name
- Special symbols (!@#$%)
- HTML

AMAZON STYLE GUIDE:
- Capitalize first letter of each major word
- Numbers: write out one through nine, use numerals for 10+
- Units: abbreviate (cm, kg, W)
- Color: include if variant
- Size: include if variant

EXAMPLE (Good):
"JBL Tune 760NC Fone de Ouvido Bluetooth Over-Ear com Cancelamento de Ruido Ativo, Bateria 35 Horas, Conexao Multiponto, Preto"
(152 chars, proper format, no promotional)

EXAMPLE (Bad):
"MELHOR FONE DO MERCADO!!! JBL BLUETOOTH DESCONTO DE 50% FRETE GRATIS AMAZON PRIME!!!"
(Promotional, ALL CAPS, claims, platform mention)
```

### Bullet Points

```
LIMITS:
- Minimum: 3 bullets
- Maximum: 5 bullets
- Optimal: 5 (always use all)
- Max characters per bullet: 500
- Optimal per bullet: 150-250

STRUCTURE:
- Start with benefit/feature name (CAPS or bold visual)
- Follow with explanation
- End without period (if single sentence)

FORMAT:
"CANCELAMENTO DE RUIDO ATIVO: Tecnologia ANC hibrida elimina ate 95% do ruido ambiente para concentracao total em musica ou chamadas"

BEST PRACTICES:
- One main benefit per bullet
- Front-load most important benefits
- Include technical specs naturally
- Address common questions/objections
- Use parallel structure

PROHIBITED:
- Promotional language
- Pricing information
- Shipping information
- Competitor mentions
- HTML/special formatting
```

### Description

```
LIMITS:
- Minimum: 100 characters
- Maximum: 2,000 characters
- Optimal: 1,500-2,000 characters

HTML ALLOWED:
- NONE (use A+ Content for rich formatting)

A+ CONTENT (Brand Registry):
- Available for Brand Registered sellers
- Increases conversion 5-10%
- Allows images, comparison tables, brand story
- Recommended modules:
  - Comparison table
  - Image with text
  - Feature focus
  - Image carousel

BACKEND KEYWORDS:
- Max: 250 bytes
- Format: space-separated (not comma)
- Include: synonyms, misspellings, variations
- Exclude: brand names, ASINs, profanity
- Do NOT repeat title/bullet keywords
```

### Images

```
QUANTITY:
- Minimum: 1
- Maximum: 9
- Optimal: 7-9

MAIN IMAGE (STRICT REQUIREMENTS):
- Background: Pure white (RGB 255,255,255)
- Product: Must occupy 85% of frame
- No text or graphics
- No accessories not included
- No packaging (unless selling package)
- No lifestyle/model images
- Professional quality required

SECONDARY IMAGES:
- Infographics allowed
- Lifestyle images allowed
- Size comparison
- Feature callouts
- Multiple angles
- Packaging/unboxing

DIMENSIONS:
- Minimum: 1000x1000 pixels (for zoom)
- Recommended: 1500x1500 pixels or higher
- Aspect ratio: 1:1 preferred

FILE:
- Format: JPG (preferred), PNG
- Max size: 10MB
- Color mode: RGB/sRGB
```

---

## MAGAZINE LUIZA (MAGALU) - DETAILED SPECS

### Title

```
LIMITS:
- Minimum: 10 characters
- Maximum: 256 characters
- Optimal: 150-200 characters

FORMAT REQUIRED:
[Marca] + [Modelo] + [Caracteristicas Principais]

ALLOWED:
- Letters, numbers, spaces
- Hyphens
- Basic punctuation

PROHIBITED:
- Emojis
- ALL CAPS (excessive)
- Special symbols
- Promotional text
- Contact information

EXAMPLE (Good):
"Fone de Ouvido Bluetooth JBL Tune 760NC Over-Ear com Cancelamento de Ruido Ativo Preto - Bateria 35h"

EXAMPLE (Bad):
"FONE JBL PROMOCAO IMPERDIVEL MELHOR PRECO DO BRASIL!!!"
```

### Description

```
LIMITS:
- Minimum: 200 characters
- Maximum: 4,000 characters
- Optimal: 2,500-3,500 characters

HTML ALLOWED:
- NONE (plain text only)

STRUCTURE:
1. Product introduction
2. Main features and benefits
3. Technical specifications (detailed)
4. Package contents
5. Warranty information
6. Compliance (INMETRO, etc.)

REQUIRED:
- Complete technical specifications
- Clear warranty terms
- Voltage information (electronics)
- Compatibility information (if applicable)
```

### Images

```
QUANTITY:
- Minimum: 1
- Maximum: 20
- Optimal: 10-15

DIMENSIONS:
- Minimum: 1000x1000 pixels
- Recommended: 1500x1500 pixels
- Aspect ratio: 1:1 (square)

FILE:
- Format: JPG, PNG
- Max size: 5MB per image

MAIN IMAGE (STRICT):
- Background: Pure white
- No text overlay
- No watermarks
- No other brand logos
- Professional quality

PROHIBITED (ALL IMAGES):
- Text on images (except product labeling)
- Other seller logos
- Contact information
- QR codes
- Links
```

### MANDATORY FIELDS

```
REQUIRED FOR ALL PRODUCTS:
- EAN code (GTIN-13 or GTIN-14)
- NCM code (tax classification)
- Brand
- Model
- Category
- Price
- Stock quantity
- Warranty period

REQUIRED FOR ELECTRONICS:
- Voltage (127V, 220V, Bivolt)
- Power consumption
- INMETRO certification (if applicable)
- ANATEL homologation (if wireless)

DOCUMENTATION:
- Seller must have valid CNPJ
- Fiscal notes required for electronics
- Certifications on file for regulated products
```

---

## CROSS-PLATFORM OPTIMIZATION

### Title Adaptation Strategy

```python
# Pseudo-code for multi-platform title generation

def adapt_title(base_title, platform):
    if platform == "mercadolivre":
        # Strict 60 chars, max keyword density
        return truncate_smart(base_title, 60, prioritize="keywords")

    elif platform == "shopee":
        # 120 chars, allow 1-2 emojis, promo hooks
        title = add_emoji(base_title, max=2)
        return truncate_smart(title, 120)

    elif platform == "amazon":
        # 200 chars, strict format, no promotional
        title = format_amazon_style(base_title)
        title = remove_promotional(title)
        return truncate_smart(title, 200)

    elif platform == "magalu":
        # 256 chars, marca + modelo format
        title = format_marca_modelo(base_title)
        return truncate_smart(title, 256)
```

### Image Set Recommendations

```
IDEAL IMAGE SET (9 images):
1. Main: Product on white background
2. Angle: 45-degree view
3. Back: Rear view
4. Detail: Close-up of key feature
5. Scale: Size comparison (with hand/common object)
6. Infographic: Key specs overlay
7. Lifestyle: Product in use
8. Packaging: Box/contents
9. Accessories: What's included

ADAPTATION BY PLATFORM:
- ML: Use all 9, add 3 more angles (12 total)
- Shopee: Use all 9, prioritize lifestyle
- Amazon: Use all 9, ensure main is STRICT white
- Magalu: Use all 9, add more detail shots (15+ total)
```

---

## METADATA

```json
{
  "knowledge_type": "technical_specifications",
  "platforms_covered": ["mercadolivre", "shopee", "amazon", "magalu"],
  "last_verified": "2025-12-05",
  "update_frequency": "monthly",
  "data_sources": [
    "seller_central_docs",
    "partner_center_docs",
    "platform_help_centers"
  ]
}
```

---

**Status**: Active
**Next Review**: 2026-01-05
