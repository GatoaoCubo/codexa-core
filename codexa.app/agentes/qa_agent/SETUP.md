# QA Agent | SETUP

> Configuration guide for automated QA validation

---

## Prerequisites

- Node.js >= 18.x
- npm or yarn
- Chrome/Chromium (for Lighthouse)
- Access to target environments

---

## Target Environments

| Environment | URL | Purpose |
|-------------|-----|---------|
| **Production** | {{DOMAIN}} | Final validation |
| **Staging** | {{BASE_URL}} | Pre-release testing |
| **Local** | localhost:5173 | Development testing |

---

## Installation

### 1. Install Dependencies

```bash
npm install
```

### 2. Install Lighthouse (Optional)

```bash
npm install -g lighthouse
```

### 3. Configure Environment

Create `.env.local`:

```env
# Target URL
QA_BASE_URL=https://{{BASE_URL}}

# Supabase (for Edge Function testing)
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_ANON_KEY=xxx

# Shopify (for checkout testing)
SHOPIFY_STORE={{SHOPIFY_DOMAIN}}
```

---

## Tools Setup

### Browser MCP

Ensure Browser MCP is configured in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "browser": {
      "command": "node",
      "args": ["mcp-servers/browser-mcp/index.js"]
    }
  }
}
```

### Available Browser Tools

```javascript
mcp__browser__screenshot({ url: "..." })
mcp__browser__screenshot_full({ url: "..." })
mcp__browser__extract_text({ url: "..." })
mcp__browser__extract_html({ url: "..." })
```

---

## Validation Rules Configuration

### Page Load Thresholds

```javascript
const THRESHOLDS = {
  loadTime: 3000,      // Max 3 seconds
  cls: 0.1,            // Cumulative Layout Shift
  lcp: 2500,           // Largest Contentful Paint
  fid: 100             // First Input Delay
};
```

### SEO Requirements

```javascript
const SEO_RULES = {
  title: { maxLength: 60 },
  description: { minLength: 50, maxLength: 160 },
  h1: { count: 1 },
  images: { requireAlt: true },
  canonical: { required: true }
};
```

### Accessibility (WCAG 2.1 AA)

```javascript
const A11Y_RULES = {
  colorContrast: 4.5,    // Minimum contrast ratio
  keyboard: true,         // All interactive elements
  ariaLabels: true,       // Required on buttons/links
  formLabels: true,       // Associated labels
  skipLink: true          // Skip to content
};
```

---

## Routes to Validate

| Priority | Route | Checks |
|----------|-------|--------|
| CRITICAL | `/` | Load, SEO, A11Y |
| CRITICAL | `/catalogo` | Load, Products, SEO |
| CRITICAL | `/produto/:slug` | Load, Schema, SEO |
| CRITICAL | `/carrinho` | Checkout flow |
| HIGH | `/b2b` | Form, SEO |
| MEDIUM | `/admin/*` | Auth, Functions |
| LOW | `/privacidade` | Content |
| LOW | `/termos` | Content |

---

## Edge Function Testing

### Functions to Test

| Function | Type | Test Method |
|----------|------|-------------|
| `{{AI_CHAT_FUNCTION}}` | Public | Send message, verify response |
| `{{AI_RECOMMENDATIONS_FUNCTION}}` | Public | Send issue, verify products |
| `{{AI_TTS_FUNCTION}}` | Public | Send text, verify audio |
| `create-shopify-checkout` | Public | Add product, verify URL |
| `fetch-from-shopify` | Admin | Verify product sync |

### Test Commands

```bash
# Test chat
curl -X POST \
  "$SUPABASE_URL/functions/v1/{{AI_CHAT_FUNCTION}}" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -d '{"message": "{{CHAT_TEST_1_INPUT}}"}'

# Test checkout
curl -X POST \
  "$SUPABASE_URL/functions/v1/create-shopify-checkout" \
  -H "Authorization: Bearer $SUPABASE_ANON_KEY" \
  -d '{"items": [{"variantId": "xxx", "quantity": 1}]}'
```

---

## AI Chat Test Scenarios

```javascript
const SCENARIOS = [
  { input: "{{CHAT_TEST_1_INPUT}}", expect: "{{CHAT_TEST_1_EXPECT}}" },
  { input: "{{CHAT_TEST_2_INPUT}}", expect: "{{CHAT_TEST_2_EXPECT}}" },
  { input: "{{CHAT_TEST_3_INPUT}}", expect: "{{CHAT_TEST_3_EXPECT}}" },
  { input: "{{CHAT_TEST_4_INPUT}}", expect: "{{CHAT_TEST_4_EXPECT}}" },
  { input: "{{CHAT_TEST_5_INPUT}}", expect: "{{CHAT_TEST_5_EXPECT}}" }
];
```

---

## Running Tests

### Full QA Suite

```bash
/prime-qa
# Follow QA workflow
```

### Specific Checks

```bash
# Screenshots
mcp__browser__screenshot({ url: "https://{{BASE_URL}}" })

# SEO check
mcp__browser__extract_html({ url: "..." })
# Then analyze <title>, <meta>, <h1>, etc.

# Performance
npx lighthouse https://{{BASE_URL}} --output=json
```

---

## Report Output

Reports are saved to `outputs/qa_reports/`:

```
outputs/qa_reports/
├── YYYY-MM-DD_production_report.md
├── YYYY-MM-DD_production_screenshots/
└── YYYY-MM-DD_production_metrics.json
```

---

## CI/CD Integration

### GitHub Actions (Example)

```yaml
name: QA Validation

on:
  push:
    branches: [main]

jobs:
  qa:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run QA
        run: |
          npm install
          npm run qa:validate
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Screenshot fails | Check Browser MCP is running |
| Lighthouse error | Install Chrome/Chromium |
| Edge Function timeout | Check Supabase logs |
| False positives | Adjust thresholds |

---

**Version**: 1.0.0
**Last Updated**: 2025-12-05
