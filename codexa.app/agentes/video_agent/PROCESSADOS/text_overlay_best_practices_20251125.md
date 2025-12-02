# Best Practices para Text Overlays em Video

**Categoria**: text_overlay_rules
**Assunto**: regras_texto_video
**Nivel**: basico
**Aplicacao**: quando_adicionar_texto
**Tags**: overlay, cta, legibilidade, ffmpeg

## RESUMO EXECUTIVO

Text overlays sao elementos de texto sobrepostos ao video para reforcar mensagens-chave. Quando bem aplicados, aumentam conversao. Quando mal aplicados, poluem visualmente e reduzem engagement.

## REGRAS DE OURO

### 1. Maximo 6 Palavras por Overlay

```
BOM:  "FRETE GRATIS"
BOM:  "R$ 599 | COMPRE AGORA"
RUIM: "Aproveite nosso frete gratis para todo Brasil"
```

### 2. CAPS para Enfase

```python
overlay_text = texto.upper()
# "compre agora" -> "COMPRE AGORA"
```

### 3. Alto Contraste para Mobile

```css
/* FFmpeg drawtext settings */
fontcolor=white
borderw=3
bordercolor=black
```

### 4. Duracao Minima 2 Segundos

```json
{
  "overlay": {
    "text": "NIKE AIR MAX",
    "start": 1.0,
    "end": 4.0,
    "duration": 3.0
  }
}
```

## TIPOS DE OVERLAY

### 1. Product Name (Inicio)
- **Quando**: Shots 1-2
- **Posicao**: Bottom
- **Estilo**: Bold
- **Duracao**: 3-4s

```json
{
  "type": "product_name",
  "start": 1,
  "end": 4,
  "text": "NIKE AIR MAX 2024",
  "position": "bottom",
  "style": "bold"
}
```

### 2. Benefit (Meio)
- **Quando**: Shots 3-4
- **Posicao**: Center
- **Estilo**: Normal
- **Duracao**: 3-4s

```json
{
  "type": "benefit",
  "start": 10,
  "end": 14,
  "text": "CONFORTO O DIA TODO",
  "position": "center",
  "style": "normal"
}
```

### 3. CTA + Preco (Final)
- **Quando**: Ultimo shot
- **Posicao**: Center
- **Estilo**: Bold + Destaque
- **Duracao**: 4-5s

```json
{
  "type": "cta_price",
  "start": 26,
  "end": 30,
  "text": "R$ 599 | COMPRE AGORA",
  "position": "center",
  "style": "cta"
}
```

## COMO APLICAR

### FFmpeg Drawtext Comando

```bash
ffmpeg -i input.mp4 \
  -vf "drawtext=fontfile='/fonts/bold.ttf':text='NIKE AIR MAX':fontsize=48:fontcolor=white:borderw=3:bordercolor=black:x=(w-text_w)/2:y=h-100:enable='between(t,1,4)'" \
  output.mp4
```

### Python Implementation

```python
def add_text_overlay(video, overlay):
    """
    Adiciona overlay de texto via FFmpeg
    """
    filter_str = (
        f"drawtext="
        f"fontfile='{overlay['font']}':"
        f"text='{overlay['text']}':"
        f"fontsize={overlay['size']}:"
        f"fontcolor={overlay['color']}:"
        f"borderw={overlay['border_width']}:"
        f"bordercolor={overlay['border_color']}:"
        f"x={get_x_position(overlay['position'])}:"
        f"y={get_y_position(overlay['position'])}:"
        f"enable='between(t,{overlay['start']},{overlay['end']})'"
    )
    return apply_ffmpeg_filter(video, filter_str)
```

### Posicoes Pre-definidas

```python
POSITIONS = {
    "top": "y=50",
    "center": "y=(h-text_h)/2",
    "bottom": "y=h-100",
    "top_left": "x=50:y=50",
    "top_right": "x=w-text_w-50:y=50",
    "bottom_left": "x=50:y=h-100",
    "bottom_right": "x=w-text_w-50:y=h-100"
}
```

## EXEMPLOS PRATICOS

### Exemplo 1: Video de Tenis (30s)

```json
{
  "text_overlays": [
    {
      "start": 1,
      "end": 4,
      "text": "NIKE AIR MAX 2024",
      "position": "bottom",
      "style": "bold"
    },
    {
      "start": 12,
      "end": 16,
      "text": "AMORTECIMENTO AIR",
      "position": "center",
      "style": "normal"
    },
    {
      "start": 26,
      "end": 30,
      "text": "R$ 599 | COMPRE AGORA",
      "position": "center",
      "style": "cta"
    }
  ]
}
```

### Exemplo 2: Video Promocional (15s)

```json
{
  "text_overlays": [
    {
      "start": 0.5,
      "end": 3,
      "text": "MEGA OFERTA",
      "position": "top",
      "style": "bold"
    },
    {
      "start": 11,
      "end": 15,
      "text": "50% OFF | SO HOJE",
      "position": "center",
      "style": "cta"
    }
  ]
}
```

### Exemplo 3: Video Clean (NO TEXT)

```json
{
  "video_mode": "clean",
  "text_overlays": [],
  "narration_required": true
}
```

## ESTILOS PRE-DEFINIDOS

```json
{
  "styles": {
    "bold": {
      "font": "Inter-Bold.ttf",
      "size": 56,
      "color": "white",
      "border_width": 3,
      "border_color": "black"
    },
    "normal": {
      "font": "Inter-Medium.ttf",
      "size": 48,
      "color": "white",
      "border_width": 2,
      "border_color": "black"
    },
    "cta": {
      "font": "Inter-ExtraBold.ttf",
      "size": 64,
      "color": "#FFD700",
      "border_width": 4,
      "border_color": "black",
      "background": "rgba(0,0,0,0.5)"
    },
    "subtle": {
      "font": "Inter-Regular.ttf",
      "size": 36,
      "color": "rgba(255,255,255,0.8)",
      "border_width": 1,
      "border_color": "rgba(0,0,0,0.5)"
    }
  }
}
```

## ARMADILHAS COMUNS

- **Erro 1**: Texto muito longo -> Corta no mobile, ilegivel
- **Erro 2**: Fonte pequena (<36px) -> Invisivel em tela pequena
- **Erro 3**: Texto sobre area movimentada -> Dificil leitura
- **Erro 4**: Muitos overlays simultaneos -> Poluicao visual
- **Erro 5**: Duracao muito curta (<2s) -> Nao da tempo de ler

## QUANDO USAR

- **SEMPRE**: CTA com preco no final
- **RECOMENDADO**: Nome do produto no inicio
- **OPCIONAL**: Beneficio-chave no meio
- **EVITAR**: Mais de 3 overlays por video
- **NUNCA**: Texto sobre rosto ou produto em destaque

## QUANDO NAO USAR (MODO CLEAN)

Ative modo `--NO TEXT` quando:
- Video para multiplos idiomas
- Tom premium/cinematografico
- YouTube (legendas automaticas)
- Brand awareness (nao conversao)

## RELACIONADO

- Ver tambem: video_modes_text_vs_clean_20251125.md
- Ver tambem: voice_config_ptbr_narracao_20251125.md

---
**Fonte**: prompts/20_script_writer_HOP.md + CODEXA UX Research
**Processado**: 2025-11-25
**Quality Score**: 0.87/1.0
