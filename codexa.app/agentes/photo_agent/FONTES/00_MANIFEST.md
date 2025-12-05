# FONTES - photo_agent Knowledge Base

**Sistema de conhecimento externo para AI Image Generation**

---

## O QUE E FONTES/

FONTES/ e o sistema de **conhecimento tecnico especializado** do photo_agent que mantem documentacao sobre:

- **AI_PLATFORMS/** - Midjourney, DALL-E 3, Imagen 3, Flux
- **PHOTOGRAPHY/** - Tecnicas de fotografia de produto, composicao
- **MARKETPLACE_VISUALS/** - Requisitos de imagem por marketplace

---

## ARQUITETURA

```
FONTES/
├── 00_MANIFEST.md              # Este arquivo (indice)
│
├── AI_PLATFORMS/               # Plataformas de geracao de imagem AI
│   ├── midjourney_v6.md        # Midjourney v6 prompting guide
│   ├── dalle3.md               # DALL-E 3 patterns
│   ├── imagen3.md              # Google Imagen 3 API
│   └── flux.md                 # Flux model guide
│
├── PHOTOGRAPHY/                # Tecnicas de fotografia
│   ├── product_photography.md  # E-commerce product shots
│   └── composition_rules.md    # Regras de composicao, iluminacao
│
└── MARKETPLACE_VISUALS/        # Especificacoes por marketplace
    └── platform_requirements.md # Image specs per platform
```

---

## QUICK REFERENCE

### AI Platforms Comparison

| Platform | Best For | Prompt Style | Max Resolution |
|----------|----------|--------------|----------------|
| Midjourney V6 | Aesthetic, artistic | Natural + parameters | 2048x2048 |
| DALL-E 3 | Accuracy, text | Natural language | 1792x1024 |
| Imagen 3 | Photorealism | Detailed descriptions | 1024x1024 |
| Flux | Speed, customization | Weighted tokens | 2048x2048 |

### When to Use Each Platform

```
Midjourney V6  → Hero shots, brand imagery, artistic lifestyle
DALL-E 3       → Precise compositions, text in image, infographics
Imagen 3       → Ultra-realistic products, natural lighting
Flux           → Fast iterations, custom models, LoRA integration
```

---

## NAVEGACAO POR TAREFA

### Gerar prompts para Midjourney
1. Leia: `AI_PLATFORMS/midjourney_v6.md`
2. Aplique: Parameters (--ar, --v 6, --style raw)
3. Valide: Multi-prompt syntax

### Gerar prompts para DALL-E 3
1. Leia: `AI_PLATFORMS/dalle3.md`
2. Aplique: Natural language structure
3. Valide: Size/quality settings

### Gerar prompts para Imagen 3
1. Leia: `AI_PLATFORMS/imagen3.md`
2. Aplique: API parameters
3. Valide: Safety filters compliance

### Fotografia de Produto
1. Leia: `PHOTOGRAPHY/product_photography.md`
2. Aplique: Lighting setups, angles
3. Valide: `MARKETPLACE_VISUALS/platform_requirements.md`

---

## INTEGRACAO COM PHOTO_AGENT

### Fluxo de Uso

```
1. photo_agent recebe descricao do produto
2. Consulta FONTES/ para tecnicas aplicaveis
3. Gera prompts otimizados para plataforma-alvo
4. Valida contra requisitos de marketplace
5. Output: Prompts copy-paste ready
```

### Arquivos Relacionados

| Arquivo | Proposito |
|---------|-----------|
| `prompts/30_prompt_generator_HOP.md` | Gera prompts (usa FONTES/) |
| `config/camera_profiles.json` | Specs de camera |
| `config/photography_styles.json` | Estilos visuais |
| `validators/marketplace_validator.py` | Valida compliance |

---

## ATUALIZACAO

### Frequencia de Review

| Categoria | Frequencia | Razao |
|-----------|------------|-------|
| AI_PLATFORMS | Mensal | Updates frequentes de modelos |
| PHOTOGRAPHY | Trimestral | Tecnicas estabilizadas |
| MARKETPLACE_VISUALS | Mensal | Politicas mudam |

### Como Atualizar

1. Verifique documentacao oficial da plataforma
2. Atualize arquivo correspondente em FONTES/
3. Incremente versao no header do arquivo
4. Atualize data em 00_MANIFEST.md

---

## METRICAS

- **Total de Arquivos**: 7
- **Plataformas AI Cobertas**: 4
- **Marketplaces Documentados**: 5 (ML, Shopee, Amazon BR, Magalu, Shein)
- **Ultima Atualizacao**: 2025-12-05

---

**Version**: 1.0.0
**Created**: 2025-12-05
**Agent**: photo_agent
**Purpose**: AI image generation knowledge base
**Status**: Production Ready
