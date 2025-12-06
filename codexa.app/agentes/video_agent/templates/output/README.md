# Templates de Output - 200_ADW

**Version**: 2.1.0 | **Status**: Production Ready

---

## Arquivos

| Arquivo | Tipo | Proposito |
|---------|------|-----------|
| `PRODUCTION_TEMPLATE.json` | JSON | Template LLM-optimized com {{PLACEHOLDERS}} |
| `PRODUCTION_TEMPLATE.md` | Markdown | Template human-optimized copy-paste |
| `index_template.html` | HTML | Template de visualizacao web |

---

## Como Usar

### 1. Execucao Automatica (Recomendado)

O workflow `200_ADW_FULL_VIDEO_PRODUCTION` usa esses templates automaticamente:

```bash
/full-video-production "Brief: Seu tema aqui" --perspectiva didatica
```

### 2. Geracao Manual

1. Copie os templates para seu diretorio de output
2. Substitua os `{{PLACEHOLDERS}}` com seus valores
3. Renomeie para `PRODUCTION.json`, `PRODUCTION.md`, `index.html`

### 3. Carregamento Dinamico (HTML)

O `index_template.html` carrega dados automaticamente de `PRODUCTION.json`:

```bash
# Coloque ambos no mesmo diretorio
outputs/
├── PRODUCTION.json   # Dados
└── index.html        # Template (copiado de index_template.html)

# Inicie servidor local
python -m http.server 8080

# Acesse http://localhost:8080/index.html
```

---

## Placeholders Principais

### Meta
- `{{PRODUCTION_ID}}` - ID unico (ex: prod_tema_20251205)
- `{{TEMA}}` - Titulo principal
- `{{PERSPECTIVA}}` - persuasiva ou didatica
- `{{TOM}}` - urgencia ou calmo

### Conceito
- `{{PROBLEMA}}` - Dor que o conteudo resolve
- `{{SOLUCAO}}` - Solucao oferecida
- `{{METAFORA}}` - Frase de impacto

### Shorts
- `{{SHORT_001_HOOK}}` - Hook do short 1
- `{{SHORT_001_SCRIPT}}` - Roteiro completo
- `{{SHORT_001_TIKTOK}}` - Legenda TikTok
- ... (repete para 002-005)

### Metricas
- `{{QUALITY_SCORE}}` - Score de qualidade (0-10)
- `{{TOTAL_ASSETS}}` - Total de assets gerados
- `{{COST_USD}}` - Custo estimado

---

## Cores por Perspectiva

### Persuasiva
```css
--primary: #f97316;      /* Laranja */
--primary-glow: rgba(249, 115, 22, 0.3);
```

### Didatica
```css
--primary: #0d9488;      /* Teal */
--primary-glow: rgba(13, 148, 136, 0.3);
```

---

## Integracao com perspectives.json

Os templates sao preenchidos de acordo com `config/perspectives.json`:

```json
{
  "perspectiva": "didatica",
  "hook_patterns": {
    "number": "Deixa eu te mostrar as {{N}} formas..."
  },
  "cta_patterns": {
    "comment": "Me conta nos comentarios..."
  }
}
```

---

**Gerado por**: CODEXA Meta-Constructor
**Ultima Atualizacao**: 2025-12-05
