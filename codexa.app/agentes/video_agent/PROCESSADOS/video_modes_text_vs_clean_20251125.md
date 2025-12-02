# Modos de Video: NO TEXT vs Text Overlays

**Categoria**: video_modes
**Assunto**: modo_no_text_vs_overlays
**Nivel**: basico
**Aplicacao**: quando_definir_estilo_video
**Tags**: no-text, clean-video, text-overlays, pure-visual

## RESUMO EXECUTIVO

O video_agent suporta dois modos principais de producao: **CLEAN VIDEO (NO TEXT)** para videos puramente visuais com apenas narracao, e **TEXT OVERLAY MODE** para videos com texto sobreposto. A escolha impacta legibilidade, traducao e uso multiplataforma.

## CONCEITOS-CHAVE

### Modo 1: CLEAN VIDEO (--NO TEXT)

Video sem nenhum texto renderizado no frame. Toda comunicacao e feita via narracao (audio).

```json
{
  "video_mode": "clean",
  "text_overlays": [],
  "narration": "required",
  "use_case": "international, repurpose, premium"
}
```

**Caracteristicas**:
- Zero texto no video
- Narracao carrega toda mensagem
- Video pode ser traduzido facilmente (so trocar audio)
- Aparencia cinematografica premium
- Funciona bem com legendas automaticas das plataformas

### Modo 2: TEXT OVERLAY MODE (Padrao)

Video com texto sobreposto em momentos estrategicos (CTA, beneficios, preco).

```json
{
  "video_mode": "overlay",
  "text_overlays": [
    {"type": "product_name", "position": "bottom"},
    {"type": "benefit", "position": "center"},
    {"type": "cta_price", "position": "center"}
  ],
  "narration": "optional",
  "use_case": "social_ads, marketplace, promo"
}
```

**Caracteristicas**:
- Texto reforça mensagem visual
- CTA com preco sempre visivel
- Funciona sem audio (feed silencioso)
- Mais direto para conversao

## COMO APLICAR

### Configuracao no Brief

```json
{
  "produto": "Nike Air Max 2024",
  "duracao": 30,
  "video_mode": "clean",
  "text_config": {
    "mode": "no_text",
    "subtitles": false,
    "platform_captions": true
  },
  "voice_config": {
    "voice_id": "pMsXgVXv3BLzUgSXRplE",
    "required": true
  }
}
```

### Logica de Selecao Automatica

```python
def select_video_mode(brief):
    """
    Selecao automatica do modo de video
    """
    # CLEAN VIDEO quando:
    if any([
        brief.get("international", False),
        brief.get("tom") == "premium",
        brief.get("objective") == "brand_awareness",
        brief.get("repurpose", False),
        "youtube" in brief.get("platforms", [])
    ]):
        return "clean"

    # TEXT OVERLAY quando:
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

### Implementacao no HOP

Para ativar modo CLEAN no `20_script_writer_HOP.md`:

```python
if video_mode == "clean":
    text_overlays = []  # Nenhum overlay
    narration_required = True
    # Toda comunicacao via audio
else:
    text_overlays = generate_overlays(concept, brief)
    narration_required = brief.get("narration", True)
```

## EXEMPLOS PRATICOS

### Exemplo 1: Video Premium Internacional
**Modo**: CLEAN (NO TEXT)
**Objetivo**: Brand awareness global

```json
{
  "video_mode": "clean",
  "text_overlays": [],
  "narration": [
    {"start": 0, "end": 4, "text": "Experience the future of comfort"},
    {"start": 10, "end": 14, "text": "Nike Air Max - Just Do It"}
  ],
  "output": {
    "video_clean": "nike_clean.mp4",
    "audio_ptbr": "narration_ptbr.mp3",
    "audio_en": "narration_en.mp3",
    "audio_es": "narration_es.mp3"
  }
}
```
**Resultado**: Um video, multiplos audios para diferentes mercados

### Exemplo 2: Anuncio Instagram Promocional
**Modo**: TEXT OVERLAY
**Objetivo**: Conversao direta

```json
{
  "video_mode": "overlay",
  "text_overlays": [
    {"start": 1, "end": 3, "text": "NIKE AIR MAX 2024", "position": "bottom", "style": "bold"},
    {"start": 8, "end": 12, "text": "CONFORTO QUE DURA", "position": "center", "style": "normal"},
    {"start": 25, "end": 30, "text": "R$ 599 | COMPRE AGORA", "position": "center", "style": "cta"}
  ],
  "narration": [
    {"start": 0, "end": 3, "text": "Conheca o futuro do conforto"}
  ]
}
```
**Resultado**: Video otimizado para conversao com CTA claro

### Exemplo 3: Video Cinematografico
**Modo**: CLEAN (NO TEXT)
**Objetivo**: Storytelling de marca

```json
{
  "video_mode": "clean",
  "visual_style": "cinematic",
  "text_overlays": [],
  "narration": [
    {"start": 0, "end": 5, "text": "Todo grande passo comeca com um sonho"},
    {"start": 20, "end": 25, "text": "Nike - Just Do It"}
  ],
  "end_card": {
    "logo": true,
    "duration": 3
  }
}
```
**Resultado**: Video premium com logo apenas no final

## ARMADILHAS COMUNS

- **Erro 1**: Modo CLEAN sem narracao -> Video mudo, perde mensagem
- **Erro 2**: Modo OVERLAY com muito texto -> Poluicao visual, cansativo
- **Erro 3**: Texto pequeno no modo OVERLAY -> Ilegivel no mobile
- **Erro 4**: Modo CLEAN para videos promocionais -> Perde CTA direto

## QUANDO USAR

### Use CLEAN (NO TEXT) quando:
- Video sera traduzido para outros idiomas
- Tom premium/cinematografico desejado
- YouTube ou plataformas com legendas automaticas
- Brand awareness (nao conversao direta)
- Video sera reaproveitado em diferentes contextos

### Use TEXT OVERLAY quando:
- Conversao direta e objetivo
- Instagram/TikTok como plataforma principal
- Preco precisa estar visivel
- Usuarios assistem sem som (feed silencioso)
- CTA claro e necessario

## RELACIONADO

- Ver tambem: voice_config_ptbr_narracao_20251125.md
- Ver tambem: text_overlay_best_practices_20251125.md

---
**Fonte**: CODEXA Best Practices + Social Media Research
**Processado**: 2025-11-25
**Quality Score**: 0.90/1.0
