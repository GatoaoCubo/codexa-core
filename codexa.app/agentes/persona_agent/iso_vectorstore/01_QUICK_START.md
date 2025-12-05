# Persona Agent | Quick Start

## Overview
Persona Agent is a template for creating AI persona/chatbot agents for e-commerce brands. It provides a complete framework for building brand-specific conversational assistants.

## Quick Commands

```bash
# Load agent context
/prime-persona

# Ask about {{DOMAIN_TOPIC}} behavior
{{persona_cmd}} explain [behavior]

# Get advice
{{persona_cmd}} help [problem]
```

## File Structure

```
persona_agent/
├── PRIME.md              # Agent philosophy
├── INSTRUCTIONS.md       # Usage guide
├── README.md             # Quick reference
├── SETUP.md              # Installation
├── VISION.md             # Future roadmap
├── UX_IMPROVEMENTS.md    # UX notes
├── config/
│   ├── persona.json      # Persona config template
│   ├── voz.md            # Voice/personality
│   └── brand_example_gato3.json  # Example brand config
├── templates/
│   └── variaveis.md      # Response variables
└── knowledge/
    ├── core/
    │   └── identidade.md # Agent identity template
    └── issues/
        └── issue_template.md  # Issue knowledge template
```

## Key Features

1. **Behavior Analysis** - Understanding behaviors
2. **Problem Solving** - Addressing issues
3. **Expert Advice** - Evidence-based recommendations
4. **Friendly Personality** - Warm, accessible communication
5. **Multi-channel** - Adapts to site, WhatsApp, email, etc.

## How to Use This Template

### 1. Copy and Rename
```bash
cp -r persona_agent your_brand_agent
```

### 2. Create Brand Config
Copy `config/brand_example_gato3.json` and fill with your brand values.

### 3. Replace Placeholders
Use search/replace to swap all `{{PLACEHOLDER}}` with your values.

### 4. Customize Knowledge Base
Create issue-specific knowledge files in `knowledge/issues/`.

## Placeholder Reference

See `config/brand_example_gato3.json` for complete list of placeholders.

Key placeholders:
- `{{BRAND_NAME}}` - Your brand name
- `{{PERSONA_NAME}}` - AI persona name
- `{{PERSONA_ROLE}}` - Persona's profession
- `{{DOMAIN_EXPERTISE}}` - Area of expertise
- `{{ISSUE_1}}` through `{{ISSUE_4}}` - Main issues addressed

## Next Steps

1. Read `PRIME.md` for agent philosophy
2. Read `INSTRUCTIONS.md` for interaction patterns
3. Copy `brand_example_gato3.json` and customize
4. Replace all placeholders with your values
5. Create knowledge files for your domain

---

**Version**: 1.0.0 | **Updated**: {{CURRENT_DATE}}
