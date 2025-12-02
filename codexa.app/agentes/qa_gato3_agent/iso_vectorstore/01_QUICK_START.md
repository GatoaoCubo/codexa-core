# QA GATO3 Agent | Quick Start

## Overview
Quality Assurance agent for GATO3 landing pages. Tests pages for SEO, accessibility, checkout flow, and overall page quality.

## Quick Commands

```bash
# Load agent context
/prime-qa

# Run full QA suite
qa_gato3_agent run --all

# Run specific tests
qa_gato3_agent run --seo
qa_gato3_agent run --a11y
qa_gato3_agent run --checkout
```

## File Structure

```
qa_gato3_agent/
├── PRIME.md           # Agent philosophy
├── INSTRUCTIONS.md    # Usage guide
├── README.md          # Quick reference
├── SETUP.md           # Installation
├── VISION.md          # Future roadmap
├── config.json        # Configuration
└── prompts/
    ├── qa_seo_HOP.md      # SEO testing
    ├── qa_a11y_HOP.md     # Accessibility
    ├── qa_checkout_HOP.md # Checkout flow
    └── qa_pages_HOP.md    # Page quality
```

## Key Features

1. **SEO Testing** - Meta tags, structured data, crawlability
2. **Accessibility** - WCAG compliance, screen reader support
3. **Checkout Flow** - Cart, payment, order confirmation
4. **Page Quality** - Performance, content, UX

## Next Steps

1. Read `02_PRIME.md` for agent philosophy
2. Read `03_INSTRUCTIONS.md` for detailed usage
3. Check `prompts/` for individual test modules

---

**Version**: 1.0.0 | **Updated**: 2025-11-30
