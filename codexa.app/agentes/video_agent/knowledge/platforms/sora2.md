# OpenAI Sora 2 - Guia de Prompt Engineering

**Versão**: 2.0 (2025) | **Empresa**: OpenAI | **Status**: Mainstream

---

## Overview

Sora 2 é o modelo de vídeo da OpenAI com foco em direção cinematográfica, física realista e áudio nativo. Excelente para narrativas visuais e consistência entre múltiplos shots.

**Specs**:
- Duração: até 20 segundos
- Resolução: até 1080p
- Áudio: nativo (soundscape, diálogo com lip-sync, SFX)
- Estilos: realista, cinematográfico, anime

---

## Filosofia de Prompting

> "Pense em prompting como briefar um cinematógrafo que nunca viu seu storyboard. Se você omitir detalhes, ele vai improvisar."

### Duas Abordagens Válidas
1. **Detalhado**: Controle e consistência máximos
2. **Leve**: Espaço para interpretação criativa

---

## Estrutura de Prompt Cinematográfico

### Para Shots Complexos (Estilo Diretor → Equipe)
```
[LOOK]: Visual style, color grade, film stock
[CAMERA]: Lens, movement, angle, framing
[LIGHTING]: Key, fill, mood, time of day
[SOUNDSCAPE]: Ambient, SFX, music
[ACTION]: Subject movement, timing
[DIALOGUE]: Spoken words (if any)
```

### Exemplo Profissional
```
LOOK: Shot on ARRI Alexa, warm color grade with lifted shadows, 2.39:1 anamorphic
CAMERA: 35mm lens, slow dolly forward, eye level, medium shot
LIGHTING: Golden hour through window, soft fill from left, optimistic mood
SOUNDSCAPE: Quiet office ambient, soft keyboard clicks, subtle inspirational score
ACTION: Entrepreneur reviews dashboard, leans back with satisfied expression, charts animate upward
DIALOGUE: None
```

---

## Física e Realismo

Sora 2 modela interações físicas de forma crível. Descreva explicitamente:

### Propriedades de Materiais
```
✅ "wet nylon jacket glistening"
✅ "heavy wooden desk"
✅ "lightweight paper floating"
```

### Forças e Ambiente
```
✅ "8-10 mph crosswind from camera left"
✅ "footfalls splashing in shallow puddles"
✅ "soft shadow penumbra on wall"
```

### Exemplo com Física
```
A skateboard rolls across wet concrete, wheels creating thin spray trails. The rider's loose cotton shirt ripples in the 15mph headwind. Board hits a crack, wobbles slightly, rider adjusts weight. Camera tracks at ankle height, capturing water droplets catching golden sunset light.
```

---

## Camera Keywords

### Movimentos (Um por Shot)
| Keyword | Efeito | Uso |
|---------|--------|-----|
| `dolly-in` | Aproximação emotiva | Intensificar momento |
| `crane rise` | Elevação reveladora | Mostrar escala |
| `steadicam tracking` | Seguimento fluido | Acompanhar ação |
| `handheld` | Movimento orgânico | Urgência, documentário |
| `static locked` | Estabilidade total | Confiança, formalidade |
| `slow orbit` | Rotação ao redor | Explorar objeto |

### Lentes
| Lens | Efeito |
|------|--------|
| `wide-angle (24mm)` | Distorção, espaço amplo |
| `standard (50mm)` | Natural, como olho humano |
| `telephoto (85mm+)` | Compressão, intimidade |
| `anamorphic` | Look cinematográfico, flares |

---

## Diálogo e Lip-Sync

### Bloco de Diálogo Dedicado
```
DIALOGUE:
Character: "Automatize 80% do seu trabalho"
Delivery: Confident, measured pace
```

### Regras
- Mantenha diálogo curto (cabe em ~8s)
- Use bloco separado para precisão de lip-sync
- Especifique tom de entrega

---

## Workflow de Produção

### Fase 1: Pré-Produção
- Script de beat sheet
- Storyboard visual
- Definir "style spine" (estética consistente)

### Fase 2: Exploração Low-Res
- Gerar 3-5 variantes curtas por shot
- Testar ideias antes de commitar

### Fase 3: Produção Final
- Prompts detalhados por shot
- Manter consistência de personagem
- Um movimento de câmera por shot

---

## Estilos Cinematográficos

### Referências que Funcionam
```
"shot on IMAX" - Épico, grande escala
"35mm handheld" - Orgânico, documentário
"vintage 16mm" - Nostálgico, granulado
"Alexa cinema camera" - Profissional, clean
"anamorphic widescreen" - Cinematográfico, flares
```

### Keywords de Estilo
```
"shallow depth of field" - Foco seletivo
"slow-motion" - Dramático
"backlight" - Silhueta, drama
"neon cyberpunk" - Futurista
"nostalgic retro" - Vintage
"dreamy slow fades" - Onírico
```

---

## Consistência Multi-Shot

### Storyboard cada Shot
```
SHOT 1:
- Framing: Wide establishing
- DOF: Deep focus
- Lighting: Blue cold from monitors
- Palette: Desaturated, blue-grey
- Action: Seller slumped at desk

SHOT 2:
- Framing: Medium close-up
- DOF: Shallow
- Lighting: Transitioning to warm
- Palette: Blue transitioning to gold
- Action: Same seller discovers CODEXA interface
```

---

## Casos de Uso E-commerce

### Narrativa de Transformação
```
LOOK: Cinematic, transitioning from cold desaturated to warm golden
CAMERA: Slow push-in, 50mm, eye level
LIGHTING: Opening: blue monitor glow. Ending: warm golden ambient
SOUNDSCAPE: Keyboard stress typing → satisfying notification chime → uplifting score
ACTION: Frustrated seller transforms to confident entrepreneur as interface appears

Shot 1: Cold, stressed, declining graphs
Shot 2: Discovery moment, light begins to warm
Shot 3: Warm, confident, rising metrics
```

### Product Demo
```
LOOK: Clean product photography aesthetic, high-key lighting
CAMERA: Slow 360 orbit, macro lens for details
LIGHTING: Soft studio lighting, white background
SOUNDSCAPE: Subtle whoosh for rotation, premium click sounds
ACTION: Product rotates, key features highlighted as camera moves
```

---

## Erros Comuns

| Problema | Solução |
|----------|---------|
| Movimento de câmera caótico | Um movimento por shot |
| Física irreal | Descrever materiais e forças |
| Inconsistência entre shots | Manter descrições idênticas |
| Diálogo cortado | Manter curto, ~8 segundos |
| Estética inconsistente | Definir "style spine" |

---

## Referências

- [OpenAI Cookbook - Sora 2 Prompting Guide](https://cookbook.openai.com/examples/sora/sora2_prompting_guide)
- [OpenAI - Sora 2 Announcement](https://openai.com/index/sora-2/)
- [Superprompt - Sora 2 Complete Guide](https://superprompt.com/blog/openai-sora-2-complete-guide)
- [Atlabs - Sora 2 Prompt Best Practices](https://www.atlabs.ai/blog/sora-2-prompt-guide)
- [Higgsfield - Sora 2 Professional Tips](https://higgsfield.ai/sora-2-prompt-guide)

---

**Última atualização**: 2025-11-24
