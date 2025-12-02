# Marketplaces Documentation

This directory contains API documentation and guides from Brazilian e-commerce marketplaces.

## 🛒 Marketplaces

### Mercado Livre
- **Docs**: https://developers.mercadolivre.com.br
- **Focus**: Listings API, SEO, product catalog, advertising
- **Refresh**: Monthly (Critical)
- **Local files**: `mercadolivre/`

### Shopee
- **Docs**: https://open.shopee.com/documents
- **Focus**: Product API, order management, logistics
- **Refresh**: Monthly (High)
- **Local files**: `shopee/`

### Amazon BR
- **Docs**: https://developer-docs.amazon.com/sp-api/
- **Focus**: Selling Partner API, catalog, FBA, SEO
- **Refresh**: Monthly (Medium)
- **Local files**: `amazon_br/`

### Magazine Luiza (Magalu)
- **Docs**: https://integrador.magazineluiza.com.br
- **Focus**: Product integration, order management
- **Refresh**: Monthly (Medium)
- **Local files**: `magalu/`

---

## 📖 Usage

### Read Locally
```bash
# Mercado Livre docs
cat mercadolivre/api_reference.md
cat mercadolivre/seo_guide.md

# Shopee docs
cat shopee/product_guide.md
```

### Refresh Documentation
```bash
# Refresh specific marketplace
python scripts/fontes/refresh_fonte.py --fonte mercadolivre_api

# Refresh all marketplaces
python scripts/fontes/sync_all.py --priority critical
```

---

## 🔄 Update Schedule

| Marketplace | Priority | Frequency | Next Check |
|-------------|----------|-----------|------------|
| Mercado Livre | Critical | Monthly | 2025-12-24 |
| Shopee | High | Monthly | 2025-12-24 |
| Amazon BR | Medium | Monthly | 2025-12-24 |
| Magalu | Medium | Monthly | 2025-12-24 |

---

## 🎯 When to Use

Use these docs when:
- 🔌 **Integrating APIs** - Learn authentication and endpoints
- 📈 **Optimizing SEO** - Platform-specific SEO rules
- 🤖 **Automating listings** - Bulk upload, updates
- 📦 **Managing logistics** - Shipping, fulfillment options
- 📊 **Understanding categories** - Product taxonomies
- 💰 **Setting up ads** - Marketplace advertising APIs

---

**Last Updated**: 2025-11-24
**Total Marketplaces**: 4
**Focus**: Brazilian e-commerce platforms
