# PLACEHOLDERS Reference

**Version**: 1.0.0
**Updated**: 2025-12-03
**Purpose**: Standard placeholder definitions for template distillation

---

## Standard Syntax

**Official**: `{{MUSTACHE_FORMAT}}` - Double curly braces, UPPERCASE_SNAKE_CASE

```
{{BRAND_NAME}}     ✓ Correct
{BRAND_NAME}       ✗ Legacy (migrate)
[BRAND_NAME]       ✗ Legacy (migrate)
{$brand_name}      ✗ Legacy (migrate)
```

---

## Brand Placeholders

Used in marketing, content, and user-facing documents.

| Placeholder | Type | Description | Example Value |
|-------------|------|-------------|---------------|
| `{{BRAND_NAME}}` | string | Company/product name | CODEXA |
| `{{BRAND_URL}}` | url | Main website URL | codexa.app |
| `{{TAGLINE}}` | string | Brand tagline/slogan | "Build the builder" |
| `{{CONTACT_EMAIL}}` | email | Contact email | hello@brand.com |
| `{{TARGET_AUDIENCE}}` | string | Primary audience | "e-commerce sellers" |
| `{{PRODUCT_CATEGORY}}` | string | Main product category | "AI tools" |

---

## Visual Placeholders

Used in design, styling, and visual assets.

| Placeholder | Type | Description | Example Value |
|-------------|------|-------------|---------------|
| `{{PRIMARY_COLOR}}` | hex | Brand primary color | #0D9488 |
| `{{SECONDARY_COLOR}}` | hex | Brand secondary color | #14B8A6 |
| `{{ACCENT_COLOR}}` | hex | Accent/CTA color | #F59E0B |
| `{{LOGO_PATH}}` | path | Path to logo asset | /assets/logo.svg |
| `{{FAVICON_PATH}}` | path | Path to favicon | /assets/favicon.ico |

---

## Content Placeholders

Used in generated content and marketing materials.

| Placeholder | Type | Description | Example Value |
|-------------|------|-------------|---------------|
| `{{CTA_TEXT}}` | string | Call-to-action text | "Start now" |
| `{{AGENT_COUNT}}` | number | Number of agents/features | 6 |
| `{{FEATURE_LIST}}` | array | List of features | ["AI", "Templates"] |
| `{{PRICE}}` | currency | Product price | R$ 49,90 |
| `{{DISCOUNT_PERCENT}}` | number | Discount percentage | 20 |

---

## Path Placeholders

Used in code, configurations, and system references.

| Placeholder | Resolves To | Description |
|-------------|-------------|-------------|
| `{{PROJECT_ROOT}}` | `.` | Project root directory |
| `{{CODEXA_APP}}` | `./codexa.app` | CODEXA application root |
| `{{AGENTES}}` | `./codexa.app/agentes` | Agents directory |
| `{{MCP_SERVERS}}` | `./mcp-servers` | MCP servers directory |
| `{{CLAUDE_DIR}}` | `./.claude` | Claude configuration |

---

## Agent Placeholders

Used within agent contexts (resolved per-agent).

| Placeholder | Resolves To | Description |
|-------------|-------------|-------------|
| `{{AGENT_DIR}}` | `{{AGENTES}}/{agent_name}` | Agent root directory |
| `{{AGENT_CONFIG}}` | `{{AGENT_DIR}}/config` | Agent configuration |
| `{{AGENT_ISO}}` | `{{AGENT_DIR}}/iso_vectorstore` | Agent knowledge base |
| `{{AGENT_WORKFLOWS}}` | `{{AGENT_DIR}}/workflows` | Agent ADW files |
| `{{AGENT_PROMPTS}}` | `{{AGENT_DIR}}/prompts` | Agent HOP files |
| `{{AGENT_BUILDERS}}` | `{{AGENT_DIR}}/builders` | Agent builder scripts |
| `{{AGENT_VALIDATORS}}` | `{{AGENT_DIR}}/validators` | Agent validators |

---

## Document Placeholders

Used in generated documentation.

| Placeholder | Type | Description |
|-------------|------|-------------|
| `{{VERSION}}` | semver | Document version (e.g., 1.2.0) |
| `{{LAST_UPDATED}}` | date | Last update (ISO-8601) |
| `{{AUTHOR}}` | string | Document author |
| `{{STATUS}}` | enum | production/draft/deprecated |

---

## Usage

### In Templates

```markdown
# Welcome to {{BRAND_NAME}}

{{TAGLINE}}

Visit us at [{{BRAND_URL}}](https://{{BRAND_URL}})

Contact: {{CONTACT_EMAIL}}
```

### Hydration (Filling Placeholders)

```json
{
  "BRAND_NAME": "CODEXA",
  "BRAND_URL": "codexa.app",
  "TAGLINE": "Build the builder",
  "CONTACT_EMAIL": "hello@codexa.app"
}
```

### Result

```markdown
# Welcome to CODEXA

Build the builder

Visit us at [codexa.app](https://codexa.app)

Contact: hello@codexa.app
```

---

## Validation

A properly distilled document:
- [ ] Contains NO hardcoded brand names
- [ ] Contains NO hardcoded URLs
- [ ] Contains NO hardcoded hex colors
- [ ] Uses ONLY `{{PLACEHOLDER}}` syntax
- [ ] All placeholders are from this reference

---

## See Also

- [CLAUDE.md](../CLAUDE.md) - LAW 1: Distillation Principle
- [path_registry.json](../path_registry.json) - Path placeholder definitions
