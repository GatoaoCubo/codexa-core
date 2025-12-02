# system - Meta-Configurable Competitor Intelligence

**Version**: 1.0.0
**Philosophy**: Flexibility over determinism, context over assumptions
**Architecture**: User-driven meta-configuration system

---

## 🎯 What is system?

**system** is a layer of abstraction that transforms hardcoded configuration into flexible, user-driven templates.

Instead of:
```json
{"name": "Sebrae", "price": 0}
```

You get:
```json
{"{SOURCE_ID}": {"name": "{NULL}", "price": "{NULL}", "{ANY_FIELD}": "{USER_DEFINES}"}}
```

**Result**: Same system works for AI courses, SaaS tools, marketplaces, or ANY domain you want to track.

---

## 🏗️ Architecture

```
system/
├── system.meta.json              # Master configuration (all {NULL} by default)
├── schemas/
│   └── source.schema.json        # Flexible JSON Schema for sources
├── templates/
│   ├── doc.template.md           # Documentation template (Mustache-style)
│   ├── report.template.md        # Report template
│   └── insight.template.md       # Insight extraction template
├── workflows/
│   ├── quick_update.workflow.json   # Configurable workflows
│   └── full_refresh.workflow.json
├── user_context/
│   └── user_config.json          # User fills this (via wizard or manual)
├── executor.py                   # Meta-driven workflow engine
├── init_wizard.py                # Interactive setup wizard
└── README.md                     # This file
```

---

## 🚀 Quick Start

### 1. Initialize Your Project

```bash
cd system/
python init_wizard.py
```

**The wizard will ask**:
- Project name? → YOUR choice
- Domain? → AI courses | SaaS | Marketplaces | Custom
- Market? → Brazil | LATAM | Global
- Categories? → Define what you want to track
- Preferences? → Output format, frequency, etc.

**All intentionally blank - YOU decide!**

### 2. Add Sources

Edit generated files in `sources/`:
```bash
sources/
├── ai_courses.json      # If you chose "AI courses"
└── marketplaces.json    # If you chose "Marketplaces"
```

Or use schema validation:
```json
{
  "sebrae": {
    "name": "Sebrae - IA na Prática",
    "tier": "free",
    "priority": "high",
    "urls": {"main": "https://..."},
    "custom_fields": {
      "whatever_you_want": "flexible!"
    }
  }
}
```

### 3. Run Workflow

```bash
python executor.py --workflow quick_update --priority high
```

**Done!** Docs generated, insights extracted, report created.

---

## 🎯 Core Concepts

### 1. **{NULL} Philosophy**

We deliberately leave values blank so YOU fill them based on YOUR context:

```json
{
  "project": {
    "name": null,          // You decide
    "domain": null,        // Your domain
    "market": null         // Your market
  },
  "preferences": {
    "update_frequency": null,  // Daily? Weekly? You choose
    "output_format": null,      // Markdown? JSON? Both?
    "alert_channels": null      // Slack? Email? None?
  }
}
```

**Why?**
- No assumptions about your needs
- Maximum flexibility
- Learn from your usage
- Evolve incrementally

### 2. **Runtime Configuration**

Values substituted at execution time:

```json
{
  "action": "fetch",
  "params": {
    "method": "{{parameters.fetch_method}}"  // User decides: webfetch|scraping|api
  }
}
```

User can override:
```bash
python executor.py --workflow quick_update --fetch-method scraping
```

### 3. **Schema Validation**

Sources validated against flexible schema:

```json
{
  "$schema": "source.schema.json",
  "{SOURCE_ID}": {
    "name": "{REQUIRED}",
    "priority": "{OPTIONAL}",
    "{ANY_FIELD}": true  // ← Completely flexible!
  }
}
```

Add fields on the fly - no code changes needed.

### 4. **Template-Driven Output**

All documentation generated from templates:

```markdown
# {{source.name}}

{{#insights}}
### {{number}}. {{title}}
**Action**: {{action}}
{{/insights}}
```

Change template → change all outputs. No code touched.

---

## 📋 Workflows

### Pre-Built Workflows

#### **quick_update**
- Fetches high-priority sources only
- ~15 minutes
- Generates summary report

```bash
python executor.py --workflow quick_update
```

#### **full_refresh**
- All sources, all categories
- ~60 minutes
- Comprehensive report

```bash
python executor.py --workflow full_refresh
```

#### **category_update**
- Specific category only

```bash
python executor.py --workflow category_update --category ai_courses
```

### Custom Workflows

Create `system/workflows/custom.workflow.json`:

```json
{
  "workflow_id": "my_custom_workflow",
  "steps": [
    {"action": "load_sources", "params": {...}},
    {"action": "fetch_content", "params": {...}},
    {"action": "your_custom_action", "params": {...}}
  ]
}
```

Execute:
```bash
python executor.py --workflow my_custom_workflow
```

---

## 🔧 Extending the System

### Add Custom Action

Edit `executor.py`:

```python
def _action_my_custom_action(self, params: Dict, context: Dict):
    """Your custom logic here."""
    # Access params
    my_param = params.get('my_param')

    # Access context
    sources = context.get('sources_list', [])

    # Do your thing
    result = do_something(sources, my_param)

    # Return output
    return result
```

Use in workflow:
```json
{
  "action": "my_custom_action",
  "params": {"my_param": "value"}
}
```

### Add Custom Template

Create `system/templates/custom.template.md`:

```markdown
# {{title}}

{{#custom_data}}
## {{section}}
{{content}}
{{/custom_data}}
```

Reference in workflow:
```json
{
  "action": "generate_docs",
  "params": {
    "template": "system/templates/custom.template.md"
  }
}
```

---

## 📊 Examples

### Example 1: Track SaaS Competitors

```bash
# 1. Init
python init_wizard.py
> Project name? SaaS Competitors Tracker
> Domain? [2] SaaS Tools
> Market? [3] Global

# 2. Add sources
# Edit sources/saas_tools.json
{
  "notion": {
    "name": "Notion",
    "tier": "freemium",
    "urls": {"main": "https://notion.so", "pricing": "https://notion.so/pricing"},
    "metrics": {"users": "30M+", "valuation_usd": "10B"}
  }
}

# 3. Run
python executor.py --workflow quick_update
```

### Example 2: Custom Fields

```json
{
  "tiktok_shop": {
    "name": "TikTok Shop",
    "priority": "high",
    "urls": {...},

    // Standard fields
    "metrics": {"gmv_2024": "20B"},

    // YOUR custom fields - anything goes!
    "custom_fields": {
      "ai_features": ["GMV Max", "Search Ads", "Creative Studio"],
      "target_demographics": ["Gen Z", "Millennials"],
      "competitive_moat": "Social + Commerce integration",
      "my_random_note": "Whatever I want to track!"
    }
  }
}
```

### Example 3: Multi-Market Setup

```bash
# Brazil project
python init_wizard.py --config brazil_config
> Market? Brazil
> Language? pt-BR

# LATAM project (reuse same system!)
python init_wizard.py --config latam_config
> Market? LATAM
> Language? es

# Same system, different contexts!
```

---

## 🎓 Philosophy & Design Principles

### 1. **User-Driven Configuration**
- System asks, doesn't assume
- User provides context
- No hardcoded values

### 2. **Flexibility Over Determinism**
- Templates not fixed structures
- Runtime params not compile-time
- Evolution not revolution

### 3. **Context-Aware Execution**
- Decisions based on user context
- Adaptive to changing needs
- Feedback loop for learning

### 4. **Minimal Assumptions**
- Don't guess user intent
- Provide escape hatches everywhere
- Make overrides easy

### 5. **Incremental Complexity**
- Start simple (wizard)
- Add complexity when needed
- Never force premature optimization

---

## 🔍 Advanced Usage

### Conditional Workflows

```json
{
  "steps": [
    {
      "action": "fetch",
      "condition": "{{parameters.fetch_enabled}}",  // Only if user enables
      "params": {...}
    }
  ]
}
```

### Nested Placeholders

```json
{
  "output_path": "docs/{{project.domain}}/{{category}}/{{source.id}}/"
}
```

Resolves to: `docs/ai_courses/platforms/sebrae/`

### Dynamic Filters

```json
{
  "action": "load_sources",
  "params": {
    "filter": {
      "priority": "{{parameters.priority_filter}}",  // Runtime choice
      "market": "{{project.market}}"                  // From user config
    }
  }
}
```

---

## 📚 API Reference

### MetaExecutor

```python
from meta.executor import MetaExecutor

executor = MetaExecutor()

# Execute with defaults
executor.execute_workflow('quick_update')

# Execute with overrides
executor.execute_workflow('quick_update', user_params={
    'priority_filter': 'critical',
    'max_sources': 5,
    'generate_report': False
})
```

### Init Wizard

```python
from meta.init_wizard import InitWizard

wizard = InitWizard()
wizard.run()  # Interactive mode

# Or programmatic
wizard.config = {...}
wizard._save_configuration()
```

---

## 🐛 Troubleshooting

**Q: Workflow fails with "unknown action"**
A: Action not implemented in executor.py - add custom action handler

**Q: Template placeholders not substituted**
A: Check placeholder syntax: `{{variable}}` not `{variable}`

**Q: Source validation fails**
A: Check against `schemas/source.schema.json` - or modify schema!

**Q: Want different template style**
A: Create custom template in `templates/` - any format works

---

## 🚀 Next Steps

1. **Run wizard**: `python init_wizard.py`
2. **Add sources**: Edit `sources/*.json`
3. **Execute workflow**: `python executor.py --workflow quick_update`
4. **Customize**: Modify templates, workflows, schemas
5. **Extend**: Add custom actions, integrations, outputs

---

## 💡 Tips & Tricks

- **Start simple**: Use wizard, add complexity later
- **Validate schemas**: Use JSON Schema validators
- **Version control**: Git-track your user_context/
- **Share templates**: Templates are portable!
- **A/B test workflows**: Easy to try different approaches

---

**Welcome to the meta layer - where YOUR context drives the system!** 🎯

**Status**: ✅ Production-ready
**Flexibility**: ⭐⭐⭐⭐⭐ Maximum
**Learning Curve**: ⭐⭐ Gentle (wizard-driven)
