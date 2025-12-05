# MANIFEST | BRAND_IDENTITY shared_knowledge v1.0.0

**Category**: BRAND_IDENTITY (Identidade de Marca)
**Type**: shared_knowledge (conhecimento compartilhado entre agentes)
**Version**: 1.0.0 | **Date**: 2025-12-05
**Files**: 5 | **Total Tokens**: ~12,000
**Status**: PRODUCTION READY

---

## PURPOSE

Conhecimento fundamental sobre estrategia de marca, posicionamento e identidade visual para o mercado brasileiro. Consolidado a partir do marca_agent e disponibilizado para todos os agentes do ecossistema.

**Casos de Uso**:
- Criacao de marcas do zero
- Reposicionamento de marcas existentes
- Consistencia de comunicacao cross-channel
- Treinamento de novos agentes/usuarios

---

## FILE INVENTORY (5 Files)

| # | File | Tokens | Purpose |
|---|------|--------|---------|
| 00 | MANIFEST.md | ~400 | Category index e instrucoes de uso |
| 01 | archetype_guide.md | ~3,000 | 12 arquetipos de marca (Carl Jung) |
| 02 | visual_identity.md | ~2,500 | Psicologia das cores, tipografia, imagem |
| 03 | voice_guidelines.md | ~2,500 | Framework de tom de voz |
| 04 | positioning_frameworks.md | ~3,500 | Ries & Trout, Blue Ocean, JTBD, StoryBrand |

---

## CROSS-REFERENCES

### Agents que Consomem

| Agent | Uso | Arquivos Prioritarios |
|-------|-----|----------------------|
| **marca_agent** | Core knowledge - base de toda estrategia | Todos (01-04) |
| **anuncio_agent** | Tom de voz e arquetipos para copy | 01, 03 |
| **photo_agent** | Diretrizes visuais para imagens | 02 |
| **video_agent** | Identidade visual + voz para roteiros | 02, 03 |
| **curso_agent** | Posicionamento de infoprodutos | 01, 04 |

### Integracao com Workflows

| ADW | Fase de Uso | Conhecimento |
|-----|-------------|--------------|
| 100_ADW_RUN_MARCA | Fases 2-7 | Todos os arquivos |
| 100_ADW_RUN_ANUNCIO | Fase 1 (contexto) | 01_archetype_guide |
| 100_ADW_RUN_PHOTO | Pre-processamento | 02_visual_identity |
| 100_ADW_RUN_VIDEO | Roteiro + visual | 02, 03 |

---

## KNOWLEDGE CARD FORMAT

Cada arquivo segue o formato padrao de knowledge card:

```markdown
# [TITULO] | shared_knowledge

**Category**: BRAND_IDENTITY
**Purpose**: [Objetivo especifico]
**Version**: 1.0.0 | **Updated**: 2025-12-05
**Cross-ref**: [Agentes relacionados]

---

## OVERVIEW
[Contexto e importancia]

## CONTENT
[Conhecimento estruturado]

## BRAZILIAN CONTEXT
[Adaptacoes para mercado BR]

## QUICK REFERENCE
[Tabelas e checklists]

---

**Status**: [Production/Draft]
**Integration**: [Como usar em workflows]
```

---

## USAGE INSTRUCTIONS

### Para LLMs

```
1. Carregar 00_MANIFEST.md primeiro (este arquivo)
2. Identificar tarefa e selecionar arquivos relevantes
3. Carregar arquivos na ordem: 01 → 02 → 03 → 04
4. Aplicar conhecimento conforme cross-references
```

### Para Desenvolvedores

```python
# Exemplo de integracao com Scout
from mcp_scout import discover

# Encontrar conhecimento relevante
files = discover(
    query="arquetipos de marca para fitness",
    path="shared_knowledge/BRAND_IDENTITY"
)
```

---

## MAINTENANCE

**Owner**: marca_agent (source of truth)
**Update Cycle**: Trimestral ou quando marca_agent atualizar
**Validation**: Score minimo 7.0/10 em cada arquivo

### Change Process

1. marca_agent atualiza iso_vectorstore
2. codexa_agent sincroniza para shared_knowledge
3. Testes de integracao com agentes consumidores
4. Deploy e notificacao

---

## CHANGELOG

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-05 | Initial release - 5 knowledge cards |

---

**Category**: BRAND_IDENTITY shared_knowledge v1.0.0
**Status**: PRODUCTION READY
**Tokens**: ~12,000 total
**Date**: 2025-12-05
