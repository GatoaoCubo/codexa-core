# Google Veo 3 - Guia de Prompt Engineering

**Versão**: 3.1 (2025) | **Empresa**: Google DeepMind | **Status**: Mainstream

---

## Overview

Veo 3 é o modelo de geração de vídeo mais avançado do Google, com áudio nativo sincronizado, realismo físico superior e forte aderência a prompts complexos.

**Specs**:
- Duração: até 8 segundos
- Resolução: 720p/1080p
- Áudio: nativo (ambiente, SFX, diálogo)
- Aspect Ratios: 16:9, 9:16, 1:1

---

## Estrutura de Prompt Recomendada

### Checklist Oficial Google (2025)
```
[Subject] + [Context] + [Action] + [Style] + [Camera] + [Composition] + [Lighting] + [Audio]
```

### Template Básico
```
[Camera movement]: [Establishing scene]. [Subject description]. [Action]. [Lighting]. [Style qualifiers]. [Audio description].
```

### Exemplo Completo
```
Slow dolly forward: A Brazilian e-commerce entrepreneur sits at a modern desk with multiple monitors showing sales dashboards. He leans back with a confident smile as charts animate upward. Warm golden hour lighting through floor-to-ceiling windows. Cinematic 4K quality, shallow depth of field. Ambient office sounds with soft keyboard clicks.
```

---

## Camera Keywords (Alta Aderência)

### Movimentos
| Keyword | Descrição | Uso |
|---------|-----------|-----|
| `slow dolly-in` | Aproximação suave | Intensificar emoção |
| `static on tripod` | Câmera fixa estável | Estabilidade, confiança |
| `handheld tracking` | Seguindo sujeito | Energia, dinamismo |
| `crane shot` | Movimento vertical amplo | Revelação épica |
| `aerial view` | Vista aérea | Estabelecer contexto |
| `slow pan` | Panorâmica horizontal | Explorar ambiente |
| `POV shot` | Primeira pessoa | Imersão |

### Ângulos
| Keyword | Efeito |
|---------|--------|
| `low angle` | Poder, grandeza |
| `high angle` | Vulnerabilidade |
| `eye level` | Neutralidade, conexão |
| `dutch angle` | Tensão, desconforto |
| `extreme close-up` | Intimidade, detalhe |

---

## Diálogo e Áudio

### Formatação de Diálogo
```
✅ CORRETO: Character says: "Conheça o futuro do e-commerce"
❌ ERRADO: "Conheça o futuro do e-commerce"
```

### Evitar Legendas Automáticas
```
Adicionar ao prompt: (no subtitles)
Se persistir: No subtitles. No text overlays. No captions.
```

### Camadas de Áudio
```
Sound effects: [sons específicos da cena]
Ambient noise: [ruído de fundo do ambiente]
Dialogue: [fala do personagem]
Music: [descrição da trilha]
```

### Exemplo com Áudio
```
Close-up of hands typing on a premium keyboard. The interface shows CODEXA logo materializing. Character says: "Automatize seu negócio" (no subtitles). Sound effects: satisfying mechanical keyboard clicks. Ambient: soft office hum. Music: subtle tech ambient score.
```

---

## Style Keywords (Magic Words)

### Cinematográfico
- `cinematic film look`
- `shot on 35mm film`
- `anamorphic widescreen`
- `professional 4K quality`
- `shallow depth of field`
- `dramatic lighting`

### Animação
- `Japanese anime style`
- `Pixar-like 3D animation`
- `claymation style`
- `stop motion aesthetic`

### Artístico
- `in the style of [artista]`
- `Art Deco design`
- `neon noir aesthetic`
- `minimalist modern`

---

## JSON Prompting (Avançado)

Para controle granular, Veo 3 aceita estruturas JSON:

```json
{
  "scene": {
    "location": "modern office with glass walls",
    "time_of_day": "golden hour",
    "weather": "clear"
  },
  "subject": {
    "description": "Brazilian entrepreneur, 30s, confident",
    "clothing": "smart casual, navy blazer",
    "action": "reviewing analytics on large monitor"
  },
  "camera": {
    "movement": "slow dolly forward",
    "angle": "eye level",
    "lens": "50mm",
    "depth_of_field": "shallow"
  },
  "lighting": {
    "key": "warm natural from window",
    "fill": "soft ambient",
    "mood": "optimistic"
  },
  "audio": {
    "dialogue": null,
    "sfx": ["keyboard clicks", "mouse clicks"],
    "ambient": "quiet office atmosphere",
    "music": "subtle inspirational"
  },
  "style": {
    "look": "cinematic",
    "color_grade": "warm highlights, lifted shadows",
    "quality": "4K professional"
  }
}
```

---

## Consistência de Personagem

Para manter personagem consistente entre shots:

```
Shot 1: "A man with short dark hair, olive skin, wearing a navy blazer and white shirt, sitting at desk..."

Shot 2: "The same man with short dark hair, olive skin, navy blazer and white shirt, now standing..."
```

**Regra**: Quanto mais específica e única a descrição, melhor a continuidade.

---

## Erros Comuns e Soluções

| Problema | Causa | Solução |
|----------|-------|---------|
| Legendas indesejadas | Diálogo mal formatado | `(no subtitles)` + formato correto |
| Movimento flutuante | Sem ancoragem | Adicionar `static on tripod` |
| Física irreal | Prompt vago | Descrever massa, fricção, movimento |
| Inconsistência visual | Descrição genérica | Detalhes específicos e únicos |
| Áudio dessincronizado | Timing não especificado | Descrever quando sons ocorrem |

---

## Casos de Uso E-commerce

### Product Reveal
```
Cinematic product reveal: A premium sneaker rotates slowly on a white pedestal, studio lighting creating dramatic shadows and highlights. Camera slowly orbits the product. Golden rim light accentuates the silhouette. 4K quality, shallow depth of field. Subtle whoosh sound effect as product appears.
```

### Transformation Story
```
Split screen transition: Left side shows frustrated seller with declining graphs in blue cold lighting. Right side gradually reveals the same person smiling with rising graphs in warm golden lighting. Smooth morph transition between states. Inspirational ambient music builds.
```

### CTA/Urgency
```
Dynamic motion graphics: Countdown timer pulses with urgency, golden CTA button glows and pulses. Text "ÚLTIMAS VAGAS" appears with particle effects. Dark premium background with floating golden particles. Energetic electronic accent sounds sync with visual pulses.
```

---

## Referências

- [Google Cloud - Ultimate Prompting Guide for Veo 3.1](https://cloud.google.com/blog/products/ai-machine-learning/ultimate-prompting-guide-for-veo-3-1)
- [Vertex AI - Video Gen Prompt Guide](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide)
- [Replicate - How to Prompt Veo 3](https://replicate.com/blog/using-and-prompting-veo-3)
- [Superprompt - Veo 3 Best Practices](https://superprompt.com/blog/veo3-prompting-best-practices)
- [DataCamp - Veo 3 Practical Guide](https://www.datacamp.com/tutorial/veo-3)

---

**Última atualização**: 2025-11-24
