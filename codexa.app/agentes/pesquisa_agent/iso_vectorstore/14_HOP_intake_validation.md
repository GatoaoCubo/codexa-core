# HOP 14: INTAKE VALIDATION | pesquisa_agent v3.0.0

**Purpose**: Validate research brief and detect LLM capabilities
**Scope**: RESEARCH | **Output**: validated_brief + capabilities + gaps

---

## INPUT

- `{$brief}` - Raw product brief (text or JSON)
- `{$capabilities}` - Available LLM tools (auto-detect)

---

## RULES

1. web_search capability is REQUIRED - abort if unavailable
2. Minimum 4 fields required: product, category, audience, price
3. Generate assumptions for missing optional fields
4. Flag high-risk categories (health, kids, electronics)

### REQUIRED FIELDS
- `product_name` (string) - Product or service name
- `category` (string) - E-commerce category path
- `target_audience` (string) - Primary audience segment
- `price_range` (string) - Price range in BRL

### OPTIONAL FIELDS
- `marketplace_target` (string[]) - Target marketplaces
- `competitors` (string[]) - Known competitors
- `image_urls` (string[]) - Product images for analysis
- `special_requirements` (string) - Compliance, certifications

---

## STEPS

1. **Detect capabilities**: Check web_search, vision, file_search
2. **Parse brief**: Extract fields from text or JSON
3. **Validate required**: Abort if missing product/category
4. **Identify gaps**: List missing optional fields
5. **Generate assumptions**: Create reasonable defaults
6. **Flag risks**: Health (ANVISA), Kids (INMETRO), Electronics (ANATEL)

---

## OUTPUT FORMAT

```markdown
## BRIEF VALIDADO

### Campos Obrigatorios
- Produto: {product_name}
- Categoria: {category}
- Publico: {target_audience}
- Preco: {price_range}

### Capabilities
- web_search: YES/NO (required)
- vision: YES/NO (optional)
- file_search: YES/NO (optional)

### Lacunas do Brief
- {campo_1}: [SUGESTAO] {assumption}
- {campo_2}: [SUGESTAO] {assumption}

### Riscos Identificados
- {risk_1}: {mitigation}
```

---

## VALIDATION

- [ ] web_search confirmed
- [ ] 4 required fields present
- [ ] Gaps documented
- [ ] Risks flagged

---

**HOP**: 14 | **Agent**: pesquisa_agent | **Version**: 3.0.0
**Tokens**: ~700 (optimized)
