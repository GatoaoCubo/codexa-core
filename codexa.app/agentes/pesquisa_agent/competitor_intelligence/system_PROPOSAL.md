# Proposta: Evolução para Arquitetura system

## Conceito

Transformar sistema atual (hardcoded) em sistema **meta-configurável** onde:
- Estruturas são templates
- Valores são placeholders {NULL}
- Usuário define contexto em runtime
- Sistema se adapta dinamicamente

## Quick Example

### ATUAL
```json
// sources/ai_courses_platforms.json
{
  "platforms": {
    "sebrae": {
      "name": "Sebrae - IA na Prática",
      "priority": "high",
      "price_brl": 0
    }
  }
}
```

### system
```json
// system/system.meta.json
{
  "project": {
    "domain": "{NULL - user defines}",
    "market": "{NULL - user defines}"
  }
}

// system/schemas/source.schema.json
{
  "{source_id}": {
    "name": "{REQUIRED}",
    "priority": "{OPTIONAL - default: medium}",
    "{ANY_FIELD}": "{USER_DEFINES}"
  }
}

// User runtime:
$ python meta/init.py
> Domain? ai_courses
> Market? brazil
> Add source? sebrae
> Name? Sebrae - IA na Prática
> Custom fields? price_brl=0, tier=free
✓ Source added with your context!
```

## Benefits

1. **Reusable**: Same system for AI courses, SaaS tools, marketplaces
2. **Flexible**: User chooses what matters
3. **Maintainable**: Single template vs 40+ hardcoded files
4. **Scalable**: Add categories in minutes

## Implementation

See FILE_INVENTORY.md for full proposal.
