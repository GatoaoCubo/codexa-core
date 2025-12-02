# Google SEO Starter Guide: Best Practices

**Fonte**: developers.google.com/search/docs/fundamentals/seo-starter-guide
**Atualizado**: 2025-12-02
**Categoria**: ECOMMERCE
**Plataforma**: SEO

---

## Core Principles

**Foundational Goal:** Help search engines understand your content while making it discoverable to users.

> "Sites that follow the Search Essentials are more likely to show up in Google's search results."

---

## Making Your Site Discoverable

### Check Current Indexation
Use the `site:` search operator to verify Google has indexed your content:
```
site:yoursite.com
```

### Optimize for Crawler Visibility
- Ensure Google can access the same resources as users (CSS, JavaScript)
- Verify your page displays identically to how users see it
- Use URL Inspection Tool in Search Console

---

## Site Organization & Structure

### URL Best Practices

| ✅ Good | ❌ Bad |
|---------|--------|
| `example.com/pets/cats.html` | `example.com/2/6772756D707920636174` |
| Descriptive, readable URLs | Random identifiers |
| Relevant keywords in path | Encoded strings |

### Directory Organization
- Group topically related pages in folders
- Helps Google learn crawl frequency patterns
- Static content (`/policies/`) crawled less often than dynamic (`/promotions/`)

### Handle Duplicate Content
- Specify canonical URL using `rel="canonical"`
- Implement 301 redirects from non-preferred to preferred URLs
- Each content piece accessible via one primary URL

---

## Content Quality Standards

### Essential Characteristics

| Characteristic | Description |
|----------------|-------------|
| **Readable** | Clear paragraphs, sections, headings, grammatically correct |
| **Unique** | Original content; avoid copying |
| **Current** | Regularly update or remove outdated material |
| **Helpful** | Include expert or experienced perspectives |

---

## Title Links & Snippets

### Crafting Effective Titles
- Unique to each page
- Clear, concise, descriptive
- May include business name, location
- Appears in browser tab, bookmarks, search results

### Meta Descriptions
- Brief 1-2 sentence summary
- Keep concise; highlight relevant information
- You have control over snippet language

---

## Visual Content Optimization

### Images
- High-quality, sharp images near relevant text
- Position contextually (product photos near descriptions)
- Add descriptive **alt text** explaining the image

### Videos
- Embed on dedicated pages with surrounding text
- Write descriptive titles and descriptions
- Apply title-writing best practices

---

## Internal Linking Strategy

### Effective Link Practices
- Write descriptive anchor text
- Link to relevant internal and external resources
- Add context for users and search engines

### Outbound Links
- Trust resources before linking
- Use `nofollow` for untrusted external sites
- Apply `nofollow` to all user-generated content

---

## Low-Impact Factors (Don't Prioritize)

| Factor | Reality |
|--------|---------|
| Meta keywords tag | Google ignores entirely |
| Keyword stuffing | Violates spam policies |
| Domain keywords | Minimal ranking impact |
| TLD choice | Irrelevant except for geo-targeting |
| Content length | No magical word count |
| PageRank alone | One of many signals |

---

## Realistic Expectations

**Timeline:** Changes take weeks to months to reflect in results. Not all modifications produce noticeable impact.

---

## Aplicação CODEXA

**Quando usar este conhecimento:**
- Ao otimizar títulos de anúncios
- Ao estruturar descrições de produtos
- Ao criar URLs amigáveis
- Ao melhorar rankings em Google Shopping

**Tags**: seo, google, titles, descriptions, urls, structured_data
