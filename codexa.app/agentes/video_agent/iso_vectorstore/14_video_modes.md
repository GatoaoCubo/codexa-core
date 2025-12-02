# Video Modes: Overlay vs Clean | video_agent

**Version**: 1.0.0
**Purpose**: Reference guide for video_mode selection ("overlay" vs "clean" / --NO TEXT)

---

## DOIS MODOS

### Mode: "overlay" (Default)
Video com texto sobreposto.

```json
{
  "video_mode": "overlay",
  "text_overlays": [
    {"type": "product_name"},
    {"type": "benefit"},
    {"type": "cta_price"}
  ]
}
```

**Caracteristicas**:
- Texto reforça mensagem visual
- CTA com preco visivel
- Funciona sem audio (feed silencioso)
- Ideal para conversao direta

### Mode: "clean" (--NO TEXT)
Video sem NENHUM texto renderizado.

```json
{
  "video_mode": "clean",
  "text_overlays": [],
  "narration": "required"
}
```

**Caracteristicas**:
- Zero texto no video
- Narracao carrega toda mensagem
- Video pode ser traduzido (trocar audio)
- Aparencia cinematografica premium
- Usa legendas automaticas das plataformas

---

## QUANDO USAR

### Use "overlay" quando:
- Conversao direta e objetivo
- Instagram/TikTok como plataforma
- Preco precisa estar visivel
- Usuarios assistem sem som
- CTA claro e necessario

### Use "clean" quando:
- Video sera traduzido (multiplos idiomas)
- Tom premium/cinematografico
- YouTube (legendas automaticas)
- Brand awareness (nao conversao)
- Video sera reaproveitado

---

## LOGICA DE SELECAO

```python
def select_video_mode(brief):
    # CLEAN quando:
    if any([
        brief.get("international", False),
        brief.get("tom") == "premium",
        brief.get("objective") == "brand_awareness",
        brief.get("repurpose", False),
        "youtube" in brief.get("platforms", [])
    ]):
        return "clean"

    # OVERLAY quando:
    if any([
        brief.get("objective") == "conversao",
        "instagram" in brief.get("platforms", []),
        "tiktok" in brief.get("platforms", []),
        brief.get("preco") is not None,
        brief.get("cta_required", True)
    ]):
        return "overlay"

    return "overlay"  # Default
```

---

## IMPACTO NOS HOPs

### Script Writer (20_)
- "overlay": text_overlays >= 1
- "clean": text_overlays = []

### Visual Prompter (30_)
- "overlay": Reserve bottom 20% for text
- "clean": Full frame composition

### Editor (50_)
- "overlay": FFmpeg drawtext filter
- "clean": Skip text rendering

---

## EXEMPLOS

### Exemplo 1: Promocao Instagram
```json
{
  "video_mode": "overlay",
  "brief": {
    "produto": "Nike Air Max",
    "objetivo": "conversao",
    "platforms": ["instagram"]
  },
  "output": {
    "text_overlays": ["NIKE AIR MAX", "CONFORTO", "R$ 599"]
  }
}
```

### Exemplo 2: Campanha Global
```json
{
  "video_mode": "clean",
  "brief": {
    "produto": "Nike Air Max",
    "objetivo": "brand_awareness",
    "international": true
  },
  "output": {
    "text_overlays": [],
    "audio_tracks": ["ptbr.mp3", "en.mp3", "es.mp3"]
  }
}
```

---

## REGRAS DE VALIDACAO

| Modo | text_overlays | narration | Composicao |
|------|---------------|-----------|------------|
| overlay | >= 1 | opcional | Reserve bottom 20% |
| clean | == 0 | REQUIRED | Full frame |

---

**File**: 22_video_modes.md
**Category**: video_configuration
**Last Updated**: 2025-11-25
