# Google E-commerce SEO Best Practices

**Fonte**: developers.google.com/search/docs/specialty/ecommerce
**Atualizado**: 2025-12-02
**Categoria**: ECOMMERCE
**Plataforma**: SEO

---

## Overview

> "A critical challenge for any ecommerce website is being discovered in Search."

Google's comprehensive guide helps optimize online stores for search visibility across Google's platforms.

---

## Key Topics

### 1. Content Visibility

Understanding where ecommerce content appears:
- Google Search (organic results)
- Google Shopping
- Google Images
- Google Lens

**Focus:** Multiple touchpoints throughout the customer journey.

### 2. Product Data Sharing

Strategic approaches for submitting product information:

| Method | Best For |
|--------|----------|
| **Structured Data** | All sites |
| **Google Merchant Center** | Shopping ads + free listings |
| **Content API** | Large catalogs |
| **Automatic Extraction** | Backup method |

### 3. Structured Data Implementation

Essential markup for ecommerce sites:

```json
{
  "@context": "https://schema.org/",
  "@type": "Product",
  "name": "Nome do Produto",
  "image": "url-da-imagem.jpg",
  "description": "Descrição do produto",
  "sku": "SKU123",
  "brand": {
    "@type": "Brand",
    "name": "Marca"
  },
  "offers": {
    "@type": "Offer",
    "price": "99.90",
    "priceCurrency": "BRL",
    "availability": "https://schema.org/InStock"
  }
}
```

---

## Technical Architecture

| Area | Best Practice |
|------|---------------|
| **URL Structure** | Design patterns avoiding crawling issues |
| **Site Navigation** | Internal linking hierarchy showing importance |
| **Pagination** | UX patterns balanced with indexing needs |
| **Canonical Tags** | Avoid duplicate content issues |
| **Mobile-First** | Responsive design priority |

---

## URL Best Practices para E-commerce

### ✅ Good URLs
```
/categoria/subcategoria/produto-nome
/camisetas/masculinas/camiseta-algodao-preta
```

### ❌ Bad URLs
```
/product.php?id=12345&cat=7
/p/SKU123456789
```

---

## Structured Data Priority

| Schema Type | Impact |
|-------------|--------|
| **Product** | Essential - enables rich snippets |
| **Offer** | Price and availability |
| **AggregateRating** | Review stars |
| **BreadcrumbList** | Navigation context |
| **Organization** | Brand identity |

---

## Content Quality

- High-quality product reviews
- Unique descriptions (not manufacturer copy)
- User-generated content (reviews, Q&A)
- Detailed specifications
- High-quality images

---

## Site Launch Strategy

1. Register with Google Search Console
2. Submit sitemap
3. Ensure proper robots.txt
4. Implement structured data
5. Connect Google Merchant Center

---

## Aplicação CODEXA

**Quando usar este conhecimento:**
- Ao estruturar URLs de produtos
- Ao implementar schema markup
- Ao otimizar para Google Shopping
- Ao lançar nova loja e-commerce

**Tags**: seo, ecommerce, structured_data, schema, google_shopping
